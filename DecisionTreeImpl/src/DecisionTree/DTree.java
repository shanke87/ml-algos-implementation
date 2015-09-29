package DecisionTree;

import java.util.Arrays;
import java.util.BitSet;
import java.util.LinkedList;
import java.util.ListIterator;

import Util.Pair;

public class DTree implements Cloneable {
	DTreeNode root ;
	AttrSelector func;
	String[] attrNames;
	int attrCnt;
	int targetAttrId;
	public static int MAX_DEPTH;
	
	protected DTree() { 
		root = null;
		func = null;
	}
	
	public static DTreeNode ID3(LinkedList<BitSet> examples, BitSet freeAttributes, DTree dt, int depth) {
		// GET THE COUNTS
		int pos = 0, neg = 0;
		for(BitSet el : examples) {
			if(el.get(dt.targetAttrId)) ++pos;
			else neg++;			
		}
		DTreeNode node = new DTreeNode();
		node.posE = pos;
		node.negE = neg;
	
		// BASE CASE
		// combining the pure case & no attributes case
		if( pos == 0 || neg == 0   || freeAttributes.cardinality() == 0  || depth > MAX_DEPTH ) {
			
			node.isLeaf = true;
			node.target = (pos >= neg);
//			assert(pos == neg);
			
			if(freeAttributes.cardinality() > 0) {
				node.attributes = new int[freeAttributes.cardinality()]; 
				for(int i=0,j=0;i<dt.attrCnt; ++i)
					if(freeAttributes.get(i)) 
						node.attributes[j++] = i;
			}
			
			node.examples = examples;
			return node;
		} 
		
		assert(pos > 0 && neg > 0 && freeAttributes.cardinality() > 0);
		
		int choosenAttr = dt.func.selectAttribute(examples, freeAttributes, dt.attrCnt,dt.targetAttrId);
		//System.out.println("Free attributes " + freeAttributes + " - " + choosenAttr);
		assert(freeAttributes.get(choosenAttr));
		
		node.attributes = new int[1]; 
		node.attributes[0] = choosenAttr;
		
		LinkedList<BitSet> rightExamples = new LinkedList<BitSet>();
		int i=0 , count = examples.size();
		for(ListIterator<BitSet> it = examples.listIterator(); it.hasNext(); ) {
			BitSet el = it.next();
			//System.out.println(i + " " + el);
			if(el.get(choosenAttr) == true) {
				it.previous();
				it.remove();
				rightExamples.add(el);
			}
			
			++i;
		}

		assert(i == count);
		// examples LIST IS MODIFIED.
		freeAttributes.clear(choosenAttr);
				
		node.left = ID3(examples, freeAttributes, dt, depth+1);
		node.right = ID3(rightExamples, freeAttributes, dt, depth+1);

		if(examples.size() == 0 ) node.left.target = pos > neg;
		if(rightExamples.size() == 0) node.right.target = pos > neg;
		
		freeAttributes.set(choosenAttr);
		
		return node;
	}	
	
	public static DTree create(DataFrame train, AttrSelector hueristic) {
		
		DTree dtree = new DTree();
		dtree.func = hueristic;
		dtree.attrNames = train.attrNames;
		dtree.targetAttrId = train.targetAttrId;
		dtree.attrCnt = train.attrNames.length - 1;
		
		BitSet freeAttrs = new BitSet(dtree.attrCnt);
		freeAttrs.set(0, dtree.attrCnt);
		
		LinkedList<BitSet> examples = new LinkedList<BitSet>();
		for(int i=0;i<train.examples.length; ++i) {
			// creating a new bitset for them.
			examples.add((BitSet) train.examples[i].clone());
		}	
		
		dtree.root = ID3(examples, freeAttrs, dtree, 1);
		
		return dtree;
	}

	@Override
	protected Object clone() throws CloneNotSupportedException {
		DTree cloned = (DTree) super.clone();
		
		cloned.attrNames = new String[attrNames.length];
		for(int i=0;i<cloned.attrNames.length;++i)
			cloned.attrNames[i] = new String(attrNames[i]);
		cloned.root = DTreeNode.copyTree(root);
		return cloned;
	}
	
	public void prune(int L,int K, DataFrame test) {
		
		/* double bestAcc = test(test);
		DTreeNode bestTree = root; */
		if(K == 0) return; 
		
		double bestAcc = 0; 
		DTreeNode bestTree = root;
		int nonlfcnt = DTreeNode.getNonLeafNodeCount(root);
		//System.out.println("Number of non leaf nodes" + nonlfcnt);
		
		for(int l=0; l<L; ++l) {
			DTreeNode cproot = getTreeCopy();
			int M = Math.min(DTBuilder.HQRAND.nextInt(K) + 1, nonlfcnt);
			int nlcnttmp = nonlfcnt;

			StringBuilder sb = new StringBuilder(); 
			for(int m=0; m<M && nlcnttmp > 0; ++m) {
				int P = DTBuilder.RAND.nextInt(nlcnttmp) + 1;
				sb.append(P + " ");
				Pair<DTreeNode,Integer> res = DTreeNode.deleteInOrder(cproot,P);
				cproot = res.first;
				int removednonlfcnt = res.second;
				nlcnttmp -= removednonlfcnt;
			}
			double newAccur = this.test(test,cproot, this.targetAttrId);
			//System.out.println("Removed Nodes : " + M + " order : " + sb.toString() + " , " + newAccur);
			if(newAccur > bestAcc) {
				bestAcc = newAccur;
				bestTree = cproot;				
			} else {
				DTreeNode.freeTree(cproot);
			}
			if(l%5 == 0) System.gc();
		}
		
		root = bestTree;
	}

	private DTreeNode getTreeCopy() {
		DTreeNode cprooted = null;
		try {
			cprooted = DTreeNode.copyTree(root);
		} catch (CloneNotSupportedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			System.out.println("Unable to clone DTreeNode");
			System.exit(-1);
		}
		return cprooted;
	}
	
	public double test(DataFrame test) {
		return test(test, root, targetAttrId);
	} 
	
	protected double test(DataFrame test, DTreeNode root, int targetAttrId) {
		double accur ;
		int cnt = 0,i=0;
		for(BitSet el : test.examples) {
			DTreeNode tmp = root;
			int last = -1;
			while(!tmp.isLeaf) {
				assert(tmp.attributes.length == 1);
				last = tmp.attributes[0];
				if(el.get(tmp.attributes[0]))
					tmp = tmp.right;
				else
					tmp = tmp.left;
				
			}
			//int s = (tmp.target ? 1:0) + (el.get(targetAttrId)? 1:0); 
			// both leaf_target and example_target should be same
			// here since its logical true false, code is different
			//if(s == 0 || s == 2) ++cnt;
			//System.out.println("ex" + i + " leaf " + last  + " value " + tmp.target + " " + 
			//		targetAttrId + "," + el.get(targetAttrId) + " computed " + s + " " + cnt);
			
			if((tmp.target && el.get(targetAttrId)) || (!tmp.target && !el.get(targetAttrId)))
				++cnt;
			++i;
		}
		//System.out.println("Final count" + cnt);
		accur = cnt/(double)test.examples.length;
		return accur;
	}
	
	public void print() {
		print(root, 0);
	}
	
	private void print(DTreeNode root, int level) {
		if(!root.isLeaf) {
			for(int j=0; j<2; ++j) {
				System.out.print("\n");
				for(int i=0;i<level; ++i)
					System.out.print("|");
				System.out.print(attrNames[root.attributes[0]] + ": " + j + ": ");
				//System.out.print(">" + root.attributes[0] + "< = " + j + "(" + root.posE + "," + root.negE + ")" + " : ");
				print( j == 0 ? root.left : root.right, level+1 );
			} 
			
		} else {
			System.out.print(root.target ? 1 : 0);
			//System.out.print( (root.target ? 1 : 0) + " (" + root.posE + "," + root.negE + ")" );
			//System.out.println(root.examples);
		}	
		if(level == 0) System.out.println("");
	}

	private void copyprint(DTree s) {
		System.out.println(s.hashCode());
		System.out.println( "ATTR NAMes: " + Arrays.toString(s.attrNames) +
							"\n Att id : " + Arrays.toString(s.root.attributes) +
							"\n Root pose : " + s.root.posE +
							"\n Root left attr : " + Arrays.toString(s.root.left.attributes) +
							"\n Root left nege : " + s.root.left.negE +
							"\n Root left left examples : " + s.root.left.left.examples  
							+ "\n"
						);	
	}
	
	public void free() { 
		Arrays.fill(attrNames, null);
		attrNames = null;
		DTreeNode.freeTree(root);
	}
}
