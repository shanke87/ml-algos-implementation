package DecisionTree;

import java.util.Arrays;
import java.util.BitSet;
import java.util.LinkedList;
import java.util.ListIterator;

import Util.Pair;

public class DTreeNode implements Cloneable {
	public DTreeNode left, right;
	public int[] attributes;
	public int posE, negE; 
	public boolean isLeaf;
	public boolean target;
	public LinkedList<BitSet> examples;
	public static int count=1;
	public DTreeNode() {
		left = right = null;
		posE = negE = 0;
		isLeaf = false;
		examples = null;
		attributes = null;
	}
	
	@Override
	protected DTreeNode clone() throws CloneNotSupportedException {
		DTreeNode cloned = (DTreeNode) super.clone();
		
		if(attributes != null) {
			cloned.attributes = Arrays.copyOf(attributes, attributes.length);
		}

		if(examples != null) {
			cloned.examples = new LinkedList<BitSet>();
			for(ListIterator<BitSet> it = examples.listIterator(); it.hasNext(); ) {
				cloned.examples.add((BitSet) it.next().clone());	
			}
		}
		// left and right are not copied because it will handled from Dtree
		return cloned;
	}
	
	public static DTreeNode copyTree(DTreeNode root) throws CloneNotSupportedException {
		if(root == null) return null;
		DTreeNode cloned = root.clone();		
		cloned.left = copyTree(root.left);
		cloned.right = copyTree(root.right);
		return cloned;
	}
	
	void free() {
		if(examples != null) {
			examples.clear();
			examples = null;
		}
		left = right = null;
		attributes = null;
	}

	public static void freeTree(DTreeNode root) {
		if(root == null) return;
		freeTree(root.left);
		freeTree(root.right);
		root.free();
	}

	public static int getNonLeafNodeCount(DTreeNode root) {
	/*	if(!root.isLeaf && (root.left != null && root.right != null)) {} 
		else {
			System.out.println(" attri" + root.attributes[0] _);
		} */
		assert(!root.isLeaf && (root.left != null && root.right != null) || 
				root.isLeaf && root.left == null && root.right == null );
		if(root!=null && !root.isLeaf) {
			return  1 
					+ getNonLeafNodeCount(root.left) 
					+ getNonLeafNodeCount(root.right);
		} else 		
			return 0;
	}

	private static int counter, P;
	public static Pair<DTreeNode, Integer> deleteInOrder(DTreeNode root, int p) {
		counter = 0;
		P = p;
		removedNonLfCount = 0;
		root = deleteRecursive(root);
		return new Pair<DTreeNode,Integer>(root,removedNonLfCount);
	}

	private static DTreeNode deleteRecursive(DTreeNode root) {
		if(root == null || root.isLeaf || counter >= P) return root;
		counter++;
		if(counter == P) {
			DTreeNode newRoot = new DTreeNode();
			newRoot.posE = root.posE;
			newRoot.negE = root.negE;
			newRoot.isLeaf = true;
			newRoot.target = root.posE > root.negE;
			gathered = new LinkedList<BitSet>();
			gatherExamplesFromLeaf(root);
			newRoot.examples = gathered;
			freeTree(root);
			return newRoot;
		} else {
			root.left = deleteRecursive(root.left);
			root.right = deleteRecursive(root.right);
			return root;
		}
	}
	
	private static LinkedList<BitSet> gathered;
	private static int removedNonLfCount;
	private static void gatherExamplesFromLeaf(DTreeNode root) {
		if(root.isLeaf) {
			gathered.addAll(root.examples);
		} else {
			++removedNonLfCount;
			gatherExamplesFromLeaf(root.left);
			gatherExamplesFromLeaf(root.right);
		}
	}
}
