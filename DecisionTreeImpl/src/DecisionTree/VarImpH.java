package DecisionTree;

import java.util.BitSet;
import java.util.LinkedList;

import Util.Pair;

public class VarImpH extends AttrSelector{
/*	@Override
	public int selectAttribute(LinkedList<BitSet> examples, BitSet freeAttributes, int attrCnt, int targetAttr) {
		for(int i=0;i<attrCnt;++i)
			if(freeAttributes.get(i))
				return i;
		
		return 0;
	}
	*/
	
	protected double gain(int[][] counts, int wholePos, int wholeNeg) {

		double wholeImpVar = ImpVar(wholePos,wholeNeg);
		double firstSplitImpVar = ImpVar(counts[0][0],counts[0][1]);
		double secondSplitImpVar = ImpVar(counts[1][0],counts[1][1]);
		double sum = counts[0][0] + counts[0][1] + counts[1][0] + counts[1][1];
		if(sum == 0) return 0;

		double gain = wholeImpVar 
						- ( (counts[0][0]+counts[0][1]) / sum * firstSplitImpVar  )
						- ( (counts[1][0]+counts[1][1]) / sum * secondSplitImpVar );

		//System.out.println( wholeImpVar + " " + firstSplitImpVar + " " + secondSplitImpVar + " " + gain);
		return gain;
	}
	
	public static double ImpVar(int pos, int neg) {
		if(pos + neg == 0) return 0;
		double sum = pos + neg;
		return (pos*neg)/(sum*sum);
	}
}