package Util;

public class Pair<T1,T2> implements Comparable<Pair>{
	public static int cnt = 0;
	public T1 first;
	public T2 second;
	public Pair(T1 first, T2 second) {
		this.first = first;
		this.second = second;
	}
	@Override
	public int compareTo(Pair o) {
		return ((Comparable) second).compareTo(o.second);
	}
	
	protected void finalize(){
		cnt++;
	}
	
	@Override
	public String toString() {
		return  "<" + first + ":" + second + ">";			
	}
}
