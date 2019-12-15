/* @author Aidan Kierans
 * V#: V00819990
 *
 * CMSC 409 AI Fall 2019
 */

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;

/** The Token class represents linguistic tokens, i.e. words, with
 * data about frequency of occurrence attached.
 * 
 * @
 * @author Aidan Kierans
 */
public class Token extends Object {

	private String str; 
	private double localFreq;
	private double totalFreq;
	private double weightedFreq;

	public Token() {
		setStr(null);
		setLocalFreq(-1.0);
		setTotalFreq(-1.0);
		setWeightedFreq(-1.0);
	}

	public Token(String str) {
		setStr(str);
		setLocalFreq(-1.0);
		setTotalFreq(-1.0);	
		setWeightedFreq(-1.0);
	}

	public Token(String str, double localFreq, double totalFreq) {
		setStr(str);
		setLocalFreq(localFreq);
		setTotalFreq(totalFreq);
		setWeightedFreq(-1.0);
	}

	public Token(String str, double localFreq, double totalFreq, double weightedFreq) {
		setStr(str);
		setLocalFreq(localFreq);
		setTotalFreq(totalFreq);
		setWeightedFreq(weightedFreq);
	}

	public String getStr() {
		return str;
	}

	public void setStr(String str) {
		this.str = str;
	}

	public double getLocalFreq() {
		return localFreq;
	}

	public void setLocalFreq(double localFreq) {
		this.localFreq = localFreq;
	}

	public double getTotalFreq() {
		return totalFreq;
	}

	public void setTotalFreq(double totalFreq) {
		this.totalFreq = totalFreq;
	}

	public double getWeightedFreq() {
		return weightedFreq;
	}

	public void setWeightedFreq(double weightedFreq) {
		this.weightedFreq = weightedFreq;
	}

	/* Parts of this are broken into separate lines and commented out to make it
	 * easy to adjust the information displayed, for debugging purposes.
	 */
	@Override
	public String toString() {
		// double lf = (double) Math.round(getLocalFreq() * 1000.0) / 1000.0;
		// double tf = (double) Math.round(getTotalFreq() * 1000.0) / 1000.0;
		// double wf = (double) Math.round(getWeightedFreq() * 1000.0) / 1000.0;
		return str
				// + "(lf=" 
				// + lf 
				// + ")(tf=" 
				// + tf 
				// + ")(wf=" 
				// + "," + wf
				// + ")"
				;
	}

	public static String[] toStringArray(Token[] tk) {
		String[] str = new String[tk.length];
		for(int i = 0; i < tk.length; i++) {
			str[i] = tk[i].getStr();
		}
		return str;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj) {
			return true;
		}
		if (obj == null) {
			return false;
		}
		if (getClass() != obj.getClass()) {
			return false;
		}
		Token other = (Token) obj;
		if (str == null) {
			if (other.str != null) {
				return false;
			}
		} else if (!str.equals(other.str)) {
			return false;
		}
		return true;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		long temp;
		temp = Double.doubleToLongBits(localFreq);
		result = prime * result + (int) Math.abs(temp ^ (temp >>> 32));
		temp = Double.doubleToLongBits(totalFreq);
		result = prime * result + (int) Math.abs(temp ^ (temp >>> 32));
		result = prime * result + ((str == null) ? 0 : str.hashCode());
		return result;
	}

	/** Change the localFreq of each Token in a Token array to the
	 * 	frequency of that Token in the array.
	 * @param tk An array of Tokens
	 * @return
	 */
	public static Token[] updateLocalFreqs(Token[] tk) {
		// reset the local frequency
		for(int i = 0; i < tk.length; i++) {
			tk[i].setLocalFreq(-1.0);
		}

		for(int i = 0; i < tk.length; i++) {
			// only set the local frequency if it hasn't already been updated
			if(tk[i].getLocalFreq() != -1.0) {
				continue;
			}
			
			// note the instances of this token in the array
			ArrayList<Integer> indices = new ArrayList<Integer>(); 
			for(int j = i; j < tk.length; j++) {
				if(tk[i].equals(tk[j])) {
					indices.add(j);
				}
			}			
			// set localFreq for all instances of this token in the array
			for(int j : indices) {
				tk[j].setLocalFreq((double) indices.size()/tk.length);
			}

		}

		return tk;
	}

	/** Change the totalFreq of each Token in an ArrayList of Token 
	 * 	arrays to the frequency of that Token in the whole ArrayList
	 * @param tkArrL An ArrayList of arrays of Tokens 
	 * @return
	 */
	public static ArrayList<Token[]> updateTotalFreqs(ArrayList<Token[]> tkArrL) {
		ArrayList<Token> tkL = new ArrayList<Token>();
		for(Token[] tk : tkArrL) {
			for(int i = 0; i < tk.length; i++) {
				tkL.add(tk[i]);
			}
		}

		Token[] tkAll = new Token[tkL.size()];
		tkL.toArray(tkAll);

		// Find the total frequency for each token in an array, then put aside that array
		ArrayList<Token[]> tkTemp = new ArrayList<Token[]>();
		for(int i = 0; i < tkArrL.size(); i++) {
			// traverse the current token array
			Token[] tk = tkArrL.get(i);
			for(int j = 0; j < tk.length; j++) {
				// count the instances of this token in the ArrayList as a whole
				int count = 0;
				for(int k = 0; k < tkAll.length; k++) {
					if(tk[j].equals(tkAll[k])) {
						count++;
					}
				}
				// set totalFreq
				tk[j].setTotalFreq((double) count/tkAll.length);
			}

			// add the completed token array to the end of tkTemp
			tkTemp.add(i, tk);
		}

		return tkTemp;
	}

	/** Change the weightedFreq of each Token in an ArrayList of Token 
	 * 	arrays to the frequency of that Token in the array it's in
	 * 	weighted against the number of arrays it's in, to show its
	 * 	discriminatory power. Specifically, the weighted frequency is 
	 * 	the TF-IDF (Term Frequency multiplied by Inverse Document Frequency). 
	 * @param tkArrL An ArrayList of arrays of Tokens 
	 * @return The ArrayList of arrays of Tokens, with weightedFreq set 
	 * to the TF-IDF of each token.
	 */
	public static ArrayList<Token[]> updateWeightedFreqs(ArrayList<Token[]> tkArrL) {
		int arrFreq; // the number of arrays which contain a given token
		double inverseArrFreq; // the inverse of the number of arrays which contain a given token
		double maxLocalFreq; // the maximum of the local frequencies of the tokens in an array
		double normalizedFreq; // the localFreq of a token normalized by dividing it by maxLocalFreq

		// Find the weighted frequency for each token in an array, then put aside that array
		ArrayList<Token[]> tkTemp = new ArrayList<Token[]>();
		for(int i = 0; i < tkArrL.size(); i++) {
			Token[] tk = tkArrL.get(i);
			maxLocalFreq = 0.0;
			for(int j = 0; j < tk.length; j++) {
				if(maxLocalFreq < tk[j].getLocalFreq()) {
					maxLocalFreq = tk[j].getLocalFreq();
				}
			}
			for(int j = 0; j < tk.length; j++) {
				normalizedFreq = tk[j].getLocalFreq() / maxLocalFreq;

				arrFreq = 0;
				for(Token[] otherTk : tkArrL) {
					for(int k = 0; k < otherTk.length; k++) {
						if(tk[j].equals(otherTk[k])) {
							arrFreq ++;
							break;
						}
					}
				}
				// inverseArrFreq = log base 2 of (N/arrFreq), where N is total the number of arrays
				inverseArrFreq = Math.log((double) tkArrL.size()/arrFreq)/Math.log(2.0);

				// TF-IDF weighting (term frequency-inversed document frequency)
				tk[j].setWeightedFreq(normalizedFreq * inverseArrFreq);
			}

			// add the completed token array to the end of tkTemp
			tkTemp.add(i, tk);
		}

		return tkTemp;
	}

	/** Turn an array of Strings into an array of Tokens, with the
	 * 	local frequency of each token equal to its frequency in the
	 * 	array, and the total frequency of each token set to the default value.
	 * @param arr An array of Strings
	 * @return An array of Tokens
	 */
	public static Token[] tokenize(String[] arr) {
		Token[] tk = new Token[arr.length];
		for(int i = 0; i < tk.length; i++) {
			tk[i] = new Token(arr[i]);
		}
		tk = updateLocalFreqs(tk);
		return tk;
	}

	/** Turn an ArrayList of arrays of Strings into an ArrayList of arrays of 
	 * 	Tokens, with the local frequency of each token equal to its frequency in the
	 * 	array it's in, and the total frequency of each token equal to its frequency
	 * 	in the ArrayList as a whole.
	 * @param arr An array of Strings
	 * @return An array of Tokens
	 */
	public static ArrayList<Token[]> tokenize(ArrayList<String[]> arrL) {
		// Initialize the Token[] ArrayList
		ArrayList<Token[]> tkArrL = new ArrayList<Token[]>();
		for(String[] arr : arrL) {
			tkArrL.add(tokenize(arr));
		}

		tkArrL = updateTotalFreqs(tkArrL);
		tkArrL = updateWeightedFreqs(tkArrL);
		//		tkArrL = removeDuplicates(tkArrL);


		return tkArrL;
	}

	// Unused
	public static ArrayList<Token[]> removeDuplicates(ArrayList<Token[]> tkArrL) {
		// Find the total frequency for each token in an array, then put aside that array
		ArrayList<Token[]> tkTemp = new ArrayList<Token[]>();
		for(int i = 0; i < tkArrL.size(); i++) {
			// convert the current token array to a hash set and back to remove duplicates
			Token[] tk = tkArrL.get(i);
			HashSet<Token> hs = new HashSet<Token>();
			Collections.addAll(hs, tk);
			tk = new Token[hs.size()];
			hs.toArray(tk);

			// add the completed token array to the end of tkTemp
			tkTemp.add(i, tk);
		}		
		return tkArrL;
	}

}
