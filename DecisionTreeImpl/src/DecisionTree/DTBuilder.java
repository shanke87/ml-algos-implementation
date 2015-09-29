package DecisionTree;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.Collections;
import java.util.LinkedList;
import java.util.ListIterator;
import java.util.Random;

import javax.swing.plaf.SliderUI;

import Util.Pair;

public class DTBuilder {
	public static int RAND_INIT = 12331111;
	public static Random RAND = new Random(RAND_INIT);
	private static int K;
	private static int L;
	private static String trainFile;
	private static String validFile;
	private static String testFile;
	private static boolean printTree;
	public static HighQualityRandom HQRAND = new HighQualityRandom();
	public static void main(String[] args) throws Exception {
		DTree.MAX_DEPTH = 1000;
		getParameters(args);
//		testCode();		
		hwSimul();
	}

	private static void hwSimul() throws Exception {
		DataFrame train = DataFrame.createBitSetExamples(trainFile);
		System.gc();
		
		// TREE BUILDING
		DTree dtInfo = DTree.create(train, new InfoGainH());
		System.gc();
		DTree dtVar = DTree.create(train, new VarImpH());
		System.gc();
		DataFrame test = DataFrame.createBitSetExamples(testFile);
		System.gc();
//		System.out.println("Accuracy for InfoGain Hueristic " + dtInfo.test(test));
//		System.out.println("Accuracy for VarImpurity Hueristic " + dtVar.test(test));
		
		// PRUNING STEP
		boolean prune = true;
		if(prune) {
			DataFrame validate = DataFrame.createBitSetExamples(validFile);
			dtInfo.prune(L, K, validate);
			System.gc();
			dtVar.prune(L, K, validate);
			System.gc();
//			System.out.println("After pruning accuracy for InfoGain Hueristic " + dtInfo.test(test));
//			System.out.println("After pruning accuracy for VarImpurity Hueristic " + dtVar.test(test));
			System.out.print(dtInfo.test(test) + " " );
			System.out.println(dtVar.test(test));
		}
		
		// TREE PRINTING
		//printTree = true;
		if(printTree) {
			System.out.println("InfoGain Decision Tree after pruning");
			dtInfo.print();
			System.out.println("VarImpurity Decision Tree after pruning");
			dtVar.print();
		}
	}
	
	private static void getParameters(String[] args) {
		if(args.length < 6) 
			System.out.println("Not enough parameters ");
		L = Integer.parseInt(args[0]);
		K = Integer.parseInt(args[1]);
		trainFile = args[2];
		validFile = args[3];
		testFile = args[4];
		printTree = args[5].charAt(0) == 'y' || args[5].charAt(0) == 'Y';
		
		//trainFile = "test/ds2/training_set.csv";
		//testFile = "test/ds2/validation_set.csv";
		//validFile = "test/ds2/test_set.csv";
		//trainFile ="test/training-tk.csv";
		//testFile = trainFile;
		//validFile = trainFile;
	}

	public static void testCode() throws Exception {
		//DataBuilder.getExprAndTest();
		//System.exit(-1);
		int[] l = { 10, 15, 20, 40, 100, 160, 260, 320, 400, 560};
		int[] k = { 1,   3, 10, 25,  40,  60,  70,  80,  90, 100};
		DataFrame train = DataFrame.createBitSetExamples(trainFile);
		DataFrame test = DataFrame.createBitSetExamples(testFile);
		DataFrame validate = DataFrame.createBitSetExamples(validFile);
		System.gc();
		double[] v = new double[100];
		double[] u = new double[100];
		for(int i=1;i<l.length; ++i) {
			double sumi = 0, sumv = 0;
			for(int jj=0;jj<100;++jj) { 
				L = l[i];
				K = k[i];
				// TREE BUILDING
				DTree dtInfo = DTree.create(train, new InfoGainH());
				System.gc();
				DTree dtVar = DTree.create(train, new VarImpH());
				System.gc();
				//System.out.println("Accuracy for InfoGain Hueristic " + dtInfo.test(test));
				//System.out.println("Accuracy for VarImpurity Hueristic " + dtVar.test(test));

				// PRUNING STEP
				boolean prune = true;
				if(prune) {
					dtInfo.prune(L, K, validate);
					System.gc();
					dtVar.prune(L, K, validate);
					System.gc();
					//System.out.println("After pruning accuracy for InfoGain Hueristic " + dtInfo.test(test));
					//System.out.println("After pruning accuracy for VarImpurity Hueristic " + dtVar.test(test));
				}
				v[jj] = dtInfo.test(test);
				sumi += (v[jj]);
				u[jj] = dtVar.test(test);
				sumv += (u[jj]);
			}
			
			double vari = 0, varv = 0;
			sumi /= 100 ; sumv /= 100;
			for(int jj=0;jj<100;++jj) {
				vari += (v[jj] - sumi) * (v[jj] - sumi);
				varv += (u[jj] - sumv) * (u[jj] - sumv);
			}
			vari /= 100; varv /= 100;
			System.out.format("L: %d K: %d  Accuray mean - %1.3f  variance - %1.3f\n", l[i],k[i], sumi, vari);
			System.out.format("L: %d K: %d  Accuray mean - %1.3f  variance - %1.3f\n", l[i],k[i], sumv, varv);
		} 
		Thread.sleep(2000);
	} 
}			