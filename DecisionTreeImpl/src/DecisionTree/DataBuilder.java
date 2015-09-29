package DecisionTree;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Scanner;

public class DataBuilder {
	public static void getExprAndTest() {
		Scanner readInp = null;
		DataFrame df = new DataFrame();
		try {
			readInp = new Scanner(System.in);
			while(readInp.hasNext()) {
				String line = readInp.nextLine();
				links.clear();
				attrs.clear();
				Node root = genLogicTree(line, 0, line.length());
				root.print();
				int allposibs = 1<<attrs.size();
				
				DataFrame testDF = new DataFrame();
				BitSet[] examples = new BitSet[allposibs];
				testDF.attrNames = new String[attrs.size()+1];
				int cnt = 0;
				for(Iterator<Character> it = attrs.iterator(); it.hasNext(); ) {
					char c = it.next();
					testDF.attrNames[cnt ++ ] = c + "";
				}
				testDF.attrNames[cnt] = "Class";
				testDF.examples = examples;
				testDF.targetAttrId = attrs.size();
				
				for(int i=0; i< allposibs; ++i) {
					boolean target = evaluate(root, i);
					examples[i] = new BitSet();
					for(int j=0;j<attrs.size();++j)
						if( (i & (1<<j)) != 0)
							examples[i].set(j);
					examples[i].set(attrs.size(), target);
				}
				
				DataFrame validDF = new DataFrame();
				validDF.attrNames = testDF.attrNames;
				validDF.targetAttrId = testDF.targetAttrId;
				
				ArrayList<BitSet> trainAL = new ArrayList<BitSet>();
				ArrayList<BitSet> validAL = new ArrayList<BitSet>();
				for(int i=0;i<examples.length;++i)
					if(i%2== 0 && DTBuilder.RAND.nextBoolean()) 
						validAL.add(examples[i]);
					else 
						trainAL.add(examples[i]);
				
				testDF.examples = trainAL.toArray(new BitSet[0]);
				validDF.examples = validAL.toArray(new BitSet[0]);
				trainAL.clear(); trainAL = null; validAL.clear(); validAL = null;
				
				DTree dt = DTree.create(testDF, new InfoGainH());
				dt.prune(1000, 10, testDF);
				System.out.println(Arrays.toString(testDF.attrNames));
				testDF.print();
						
				System.out.println(line);
				System.out.println("Tree ");
				dt.print();
				System.out.println("Tree Accuracy " + dt.test(testDF));
				if(dt.test(testDF) < 1.0) 
					System.out.println("Accuracy Error");
					
				dt.free();
				testDF.free();
				validDF.free();
				System.gc();
			}
		} catch (Exception e) {
			System.out.println("Encountered error" + e.getStackTrace());
			throw e;
		} finally {
			if(readInp != null)
				readInp.close();
		}

	}
	
	private static boolean evaluate(Node root, int i) {
		if(root.isLeaf) {
			int cnt = 0;
			for(Iterator<Character> it = attrs.iterator(); it.hasNext(); ) {
				char c = it.next();
				if(root.attr == c) {
					//System.out.println(root.attr + "=" + ((i & (1<<cnt)) != 0) + " " + i);
					return ((i & (1<<cnt)) != 0);
				}
				++cnt;
			}
			assert(false);
		} else {
			if(root.isDisjunc)
				return evaluate(links.get(root.id)[0],i) || evaluate(links.get(root.id)[1],i);   
			else
				return evaluate(links.get(root.id)[0],i) && evaluate(links.get(root.id)[1],i);
		}
		assert(false);
		return true;
	}

	public static int NodeID = 1;
	static class Node {
		boolean isLeaf;
		boolean isDisjunc;
		char attr;
		int id; 
		public Node(boolean isLeaf, boolean isDisJunc, char attr) {
			id = NodeID++;
			if(isLeaf) {
				this.isLeaf = true;
				this.attr = attr;
			} else {
				this.isLeaf = false;
				this.isDisjunc = isDisJunc;
			}
		}
		public void print() { print(this,0); }
		private void print(Node root, int level) {
			if(!root.isLeaf) {
				Node[] childs = links.get(root.id);
				for(int j=0; j<2; ++j) {
					System.out.print("\n");
					for(int i=0;i<level; ++i)
						System.out.print("| ");
					System.out.print((root.isDisjunc ? "v" : "^")+ " = " + j + " : ");
					print(childs[j], level + 1);
				} 
				
			} else {
				System.out.print(root.attr);
				//System.out.print( (root.target ? 1 : 0) + " (" + root.posE + "," + root.negE + ")" );
				//System.out.println(root.examples);
			}	
			if(level == 0) System.out.println("");
		}
	}

	private static HashMap<Integer,Node[]> links = new HashMap<Integer,Node[]>(); 
	private static HashSet<Character> attrs = new HashSet<Character>();
	private static Node genLogicTree(String line, int st, int end) {
		if(st >= end) return null;
		Node root = null;
		int level = 0, lowestLevelD = 1000, lowestLevelDPos = -1;
		char lastseenAttr = '1';
		for(int i=st; i<end; ++i) {
			if(!Character.isWhitespace(line.charAt(i))) {
				char tmp = line.charAt(i);
				if(Character.isAlphabetic(tmp)) {
					lastseenAttr = tmp;
				} else if(tmp == '|' || tmp == '&') {
					if(lowestLevelD > level) {
						lowestLevelD = level;
						lowestLevelDPos = i;
					} 
				} else if(tmp == '(') {
					level ++;
				} else if(tmp == ')') {
					level --;
				}
			}
		}
		
		if(lowestLevelD == 1000) {
			root = new Node(true,false,lastseenAttr);
			attrs.add(lastseenAttr);
		} else {
			root = new Node(false, (line.charAt(lowestLevelDPos) == '|'),'-');
			Node[] childs = new Node[2];
			childs[0] = genLogicTree(line, st, lowestLevelDPos);
			childs[1] = genLogicTree(line, lowestLevelDPos + 1, end);
			links.put(root.id, childs);
		}
		return root;
	}
	
}
