package DecisionTree;

import java.util.Arrays;
import java.util.BitSet;
import java.util.LinkedList;

public class AttrSelector {
	public int selectAttribute(LinkedList<BitSet> examples, BitSet freeAttributes, int attrCnt, int targetAttr) {
		assert(freeAttributes.cardinality() > 0);
		int card = freeAttributes.cardinality();
		int bestAttr = -1; 
		double bestGain = 0.0;
		int pos=0, neg=0;
		
		for(BitSet el : examples)  
			if(el.get(targetAttr))
				pos++;
			else 
				neg++;
		
		
		for(int attr=0;attr<attrCnt; ++attr) 
			if(freeAttributes.get(attr)) {
				int[][] counts = new int[2][2];
				Arrays.fill(counts[0], 0);Arrays.fill(counts[1], 0);
				for(BitSet el : examples) { 
					counts[ el.get(attr)?1:0 ][ el.get(targetAttr)?1:0 ]++;
				}
				
				double newGain = gain(counts, pos, neg);
				if(bestAttr == -1 || newGain > bestGain) {
					bestGain = newGain;
					bestAttr = attr;
				}	
				
		//		if(card == targetAttr)
		//			System.out.println("Attribute no." + attr + " , gain " + newGain);
			}
		
		assert(bestAttr != -1); 
		
		if(bestAttr == -1) {
			System.err.println("No attribute choosen");
			
		}
		
		//System.out.println("Choosen Attribute " + bestAttr + " , best gain " + bestGain);
		return bestAttr;
	} 
	
	protected double gain(int[][] counts, int wholePos, int wholeNeg) {
		
		return 0;
	}
}
