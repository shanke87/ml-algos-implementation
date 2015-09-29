package DecisionTree;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.BitSet;
import java.util.Scanner;

import Util.Pair;

public class DataFrame  {
	public String[] attrNames;
	public BitSet[] examples;
	public int targetAttrId;
	
	public static DataFrame createBitSetExamples(String dataFile) throws Exception {
		FileInputStream fis = null;
		Scanner read_file = null;
		DataFrame df = new DataFrame();
		try {
			fis = new FileInputStream(dataFile);
			read_file = new Scanner(fis);
			String line = read_file.nextLine();
			df.attrNames = line.split(",");
			df.targetAttrId = df.attrNames.length - 1;
			ArrayList<BitSet> bsArray = new ArrayList<BitSet>();
			
			while(read_file.hasNextLine()) {
				line = read_file.nextLine();
				BitSet tmp = new BitSet(df.attrNames.length);
				int c = 0;
				for(int i=0;i<line.length();++i)
					if(line.charAt(i) == '1') {
						tmp.set(c++);
					} else if(line.charAt(i) == '0') {
						c++;
					}
				bsArray.add(tmp);
			}
			df.examples = (BitSet[]) bsArray.toArray(new BitSet[bsArray.size()]);
			bsArray.clear();
			bsArray = null;
		} catch (Exception e) {
			System.out.println("Encountered error" + e.getStackTrace());
			throw e;
		} finally {
			if(fis != null)
				try {
					fis.close();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			if(read_file != null)
				read_file.close();
		}
		return df;
	}
	
	public void print() {
		for(int i=0;i<attrNames.length; ++i)
			System.out.print(attrNames[i] + " ");
		System.out.println("");
		
		for(int i=0;i<examples.length;++i) {
//			System.out.print("[");
			for(int j=0;j<attrNames.length; ++j)
				System.out.print((examples[i].get(j) == true ? 1 : 0) + ",");
			System.out.println("");
		}
	}

	
	public Pair<Integer,Integer> getCounts() {
		Pair<Integer, Integer> ret = new Pair<Integer, Integer>(0,0);
		
		for(int i=0;i<examples.length;++i)
			if(examples[i].get(targetAttrId)) 
				++(ret.first);
			else
				++(ret.second);
		
		return ret;
	}

	public void free() {
		if(attrNames != null) 
			attrNames = null;

		if(examples != null)
			Arrays.fill(examples,null);
		examples = null;
	}
}
