package DecisionTree;

import java.util.BitSet;
import java.util.LinkedList;

public class InfoGainH extends AttrSelector {
	/*@Override
	public int selectAttribute(LinkedList<BitSet> examples, BitSet freeAttributes, int attrCnt) {
		
		return 0;
	} */
	
	@Override
	protected double gain(int[][] counts, int wholePos, int wholeNeg) {
		
		double wholeEntropy = entropy(wholePos,wholeNeg);
		double firstSplitEntropy = entropy(counts[0][0],counts[0][1]);
		double secondSplitEntropy = entropy(counts[1][0],counts[1][1]);
		double sum = counts[0][0] + counts[0][1] + counts[1][0] + counts[1][1];
		if(sum == 0) return 0;

		double gain = wholeEntropy 
						- ( (counts[0][0]+counts[0][1]) / sum * firstSplitEntropy  )
						- ( (counts[1][0]+counts[1][1]) / sum * secondSplitEntropy );

		//System.out.println( wholeEntropy + " " + firstSplitEntropy + " " + secondSplitEntropy + " " + gain);
		return gain;
	}
	
	//public static TreeMap<Integer,TreeMap<Integer,Double>> dic = new TreeMap<Integer,TreeMap<Integer,double>>(); 
	public static double entropy(int pos, int neg) {
		
		double sum = pos + neg;
		if(sum == 0) return 0;
		double entropy = 0.0;
		
		entropy +=  pos / sum * (pos != 0? Math.log10( pos/sum )/Math.log10(2) : 1);	
		entropy +=  neg / sum * (neg != 0? Math.log10( neg/sum )/Math.log10(2) : 1);	
		
		return Math.abs(entropy);
	}
}