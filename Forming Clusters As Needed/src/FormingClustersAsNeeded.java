/* @author Aidan Kierans
 * V#: V00819990
 *
 * CMSC 409 AI Fall 2019
 */

import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.ListIterator;
import java.util.Scanner;
import java.util.HashSet;

public class FormingClustersAsNeeded {

	public static void main(String[] args) throws IOException {
		ArrayList<String[]> sentences = fileToArrayList("sentences.txt");
		String[] stopWords = fileToArray("stop_words.txt");

		ArrayList<String[]> featureVector = generateFeatureVector(sentences, stopWords);
		arrayListToFile(featureVector, "feature_vector.csv");

		String[] terms = generateTermsArray(featureVector);
		//ArrayList<String[]> termL = new ArrayList<String[]>();
		//termL.add(terms);
		//arrayListToFile(termL, "terms.csv");

		int[][] tdm = generateTDM(featureVector, terms);
		tdmToFile(tdm, terms, "term_document_matrix.csv");


		/*String[][] distanceMatrix = new String[tdm.length][tdm.length];
		for(int i = 0; i < distanceMatrix.length; i++) {
			for(int j = 0; j < distanceMatrix.length; j++) {
				distanceMatrix[i][j] = Double.toString(Cluster.distance(tdm[i], tdm[j]));
			}
		}
		ArrayList<String[]> dm = new ArrayList<String[]>(Arrays.asList(distanceMatrix));
		arrayListToFile(dm, "distance_matrix.csv");*/
		
		ArrayList<Cluster> clusters = formClustersAsNeeded(tdm, 1.1, 3.5);

		clustersToFile(clusters, sentences, "clusters.txt");


		System.out.println("Sentence clusters:");
		int count = 0;
		for(Cluster clu : clusters) {
			if(clu.getDocuments().size() > 1) {
				for(double[] doc : clu.getDocuments()) {
					System.out.print((int) doc[0] + ",");
					count++;
				}
				System.out.println();
			}
		}
		System.out.println("\nCount: " + count);

	}

	public static String[] fileToArray(String filepath) throws FileNotFoundException {
		ArrayList<String[]> wordsTemp = fileToArrayList(filepath);

		String[] words = new String[wordsTemp.size()];
		int i = 0;
		for(String[] word: wordsTemp) {
			words[i] = word[0];
			i++;
		}

		return words;
	}

	public static ArrayList<String[]> fileToArrayList(String filepath) throws FileNotFoundException {
		List<String[]> sentences = new ArrayList<String[]>();

		Scanner rows = new Scanner(new FileReader(filepath));
		while(rows.hasNext()) {
			// get the next sentence from the document
			String sentence = rows.nextLine();
			// split it up into an array of words
			String[] sArr = sentence.split(" ");

			// add the array of words to the list to the list
			sentences.add(sArr.clone());
		}

		rows.close();
		return (ArrayList<String[]>) sentences;
	}

	public static void arrayListToFile(ArrayList<String[]> al, String filepath) throws IOException {
		BufferedWriter out = new BufferedWriter(new FileWriter(filepath));

		for(String[] arr: al) {
			for(int i = 0; i < arr.length - 1; i++) {
				out.append(arr[i] + ",");
			}
			out.append(arr[arr.length - 1]);
			out.newLine();
		}

		out.close();
	}

	public static void tdmToFile(int[][] tdm, String[] terms, String filepath) throws IOException {
		BufferedWriter out = new BufferedWriter(new FileWriter(filepath));

		// Write heading
		out.append("Stemmed keyword set,");
		for(int i = 0; i < terms.length - 1; i++) {
			out.append(terms[i] + ",");
		}
		out.append(terms[terms.length - 1]);
		out.newLine();

		// Write rows
		for(int i = 0; i < tdm.length - 1; i++) {
			out.append("Sentence " + (i + 1) + ",");
			for(int j = 0; j < tdm[i].length - 1; j++) {
				out.append(tdm[i][j] + ",");
			}
			out.append(tdm[i][tdm[i].length - 1] + "");
			out.newLine();
		}

		out.close();	
	}

	public static void clustersToFile(ArrayList<Cluster> clusters, ArrayList<String[]> sentences, String filepath) throws IOException {
		BufferedWriter out = new BufferedWriter(new FileWriter(filepath));

		int i = 0;
		for(Cluster clu : clusters) {
			if(clu.getDocuments().size() > 1) {
				out.append("Cluster " + i);
				out.newLine();
				for(double[] arr : clu.getDocuments()) {
					String[] sentence = sentences.get((int) arr[0]);
					for(int j = 0; j < sentence.length; j++) {
						out.append(sentence[j] + " ");
					}
					out.newLine();
				}
				out.newLine();
				out.newLine();
				i++;
			}
		}
		
		out.append("Unable to cluster:");
		out.newLine();
		for(Cluster clu : clusters) {
			if(clu.getDocuments().size() == 1) {
				double[] arr = clu.getDocuments().get(0);
				String[] sentence = sentences.get((int) arr[0]);
				for(int j = 0; j < sentence.length; j++) {
					out.append(sentence[j] + " ");
				}
				out.newLine();
			}
		}

		out.close();	
	}

	public static ArrayList<String[]> generateFeatureVector(ArrayList<String[]> sentences, String[] stopWords) {
		ArrayList<String[]> featureVector = new ArrayList<String[]>();

		// process the text to reduce dimensionality
		for(String[] sentence: sentences) {
			sentence = splitSpecificPunctuation(sentence, "\\."); // "." must be escaped because it's a RegEx wildcard
			sentence = splitSpecificPunctuation(sentence, "-");
			sentence = splitSpecificPunctuation(sentence, "/");
			sentence = removePuncNumsAndStopWords(sentence, stopWords);
			sentence = stem(sentence);
			sentence = combineStemmedSynonyms(sentence);
			featureVector.add(sentence);
		}

		ArrayList<Token[]> tokenVector = Token.tokenize(featureVector);
		featureVector.clear();

		for(Token[] tk : tokenVector) {			
			// Extract most frequent words
			tk = removeByWeightedFreq(tk, 0.5);
			featureVector.add(Token.toStringArray(tk));
		}			

		return featureVector;
	}

	/** Removes punctuation, special characters, numbers, and stop words from the input sentence.
	 * 
	 * @param sentence A String array of words
	 * @param stopWords A String array of stop words to be removed from sentence
	 * @return 
	 */
	public static String[] removePuncNumsAndStopWords(String[] sentence, String[] stopWords) {
		List<String> s = new ArrayList<String>(Arrays.asList(sentence));

		// Make each word lowercase and remove all punctuation, special characters, and numerals	
		s.replaceAll(str -> str.toLowerCase().replaceAll("[^a-z]", ""));

		// If a string was removed entirely, such as a numeral that was on its own, remove that word from the list
		// An "s" by itself indicates that some kind of plural was cut off, such as "1950s", so remove that too.
		s.removeAll(Arrays.asList("", null, "s"));

		// Remove numbers that are written out as English words.
		// For this project, I know that the data only contains a few numbers written like 
		// this, so for efficiency reasons I'll only be checking for small numbers.
		List<String> numbers = new ArrayList<String>(Arrays.asList("zero", "one", "two", 
				"three", "four", "five", "six", "seven", "eight", "nine", "ten", "single",
				"double", "triple", "quadruple", "quintuple"));
		s.removeAll(numbers);

		// Remove all stop words
		List<String> sWords = new ArrayList<String>(Arrays.asList(stopWords));
		s.removeAll(sWords);

		sentence = new String[s.size()];
		sentence = s.toArray(sentence);

		return sentence;
	}

	/** Split words connected by a slash or a hyphen into two separate words.
	 * 
	 * @param sentence The array of Strings to be split
	 * @param removePattern The RegEx pattern of the character to remove/split around
	 * @return The sentence with whatever words were connected now considered separate
	 */
	public static String[] splitSpecificPunctuation(String[] sentence, String removePattern) {
		ArrayList<String> s = new ArrayList<String>();

		for(int i = 0; i < sentence.length; i++) {
			String[] words = sentence[i].split(removePattern);
			for(int j = 0; j < words.length; j++) {
				s.add(words[j]);
			}
		}
		sentence = new String[s.size()];
		sentence = s.toArray(sentence);

		return sentence;
	}

	/** Run Porter stemmer to reduce the words to their stems.
	 * See {@link http://www.tartarus.org/~martin/PorterStemmer} or the original paper for more
	 * information: 
	 * Porter, 1980, An algorithm for suffix stripping, Program, Vol. 14,
	 * no. 3, pp 130-137
	 * 
	 * @param sentence The String array of words to reduce to their stems. All of the words should
	 * 	be lowercase and free from numbers, punctuation, and special characters.
	 * @return A String array of stemmed words.
	 */
	public static String[] stem(String[] sentence) {		
		for(int i = 0; i < sentence.length; i++) {
			Stemmer stemmer = new Stemmer();
			stemmer.add(sentence[i].toCharArray(), sentence[i].length());
			stemmer.stem();
			sentence[i] = stemmer.toString();
		}

		return sentence;
	}

	/** For any two stemmed words or phrases that describe the same topic, pick one and change 
	 * the second to a copy of the first. This is done to reduce the number of dimensions of the 
	 * feature space. I have chosen to write the list of words and their synonyms by hand, since 
	 * this dataset is relatively small and I don't want to try to work with an actual thesaurus.
	 * Since the matter of whether to merge a word with a synonym depends on whether the ability
	 * to distinguish between the two would be worth the added complexity, and I don't know which
	 * words are worth merging without trying them, I decided which words to merge based on
	 * educated guesses plus trial and error.
	 * 
	 * @param sentence The String array of stemmed words to be checked against a list of synonyms
	 * @return A sentence in which all words are replaced with their synonyms if possible.
	 */
	public static String[] combineStemmedSynonyms(String[] sentence) {
		// concatenate the entire sentence so phrases can be considered in context
		String concat = "";
		for(String word : sentence) {
			concat += word + " ";
		}

		// Define thesaurus such that thesaurus[n][0] is a basic word and thesaurus[n][1] is 
		// a RegEx representation of the word/phrase with redundant meaning that it should replace
		String[][] thesaurus = new String[][] {
			{"car","sedan"},
			{"car","passeng vehicl"},
			{"car","vehicl"},
			{"mile","kilomet"},
			{" artifici intellig "," ai "},
			{"gener intellig","sentienc"},
			{"home","hous"},
			{"home","apartment"},
			{"home","townhome"},
			{"anim","pet"},
			{"oxid","monoxid"},
			{"main","primari"},
			{"self drive","autonom"},			
			{"recogn","recognit"},
			{"drive","driven"},
			{"bed size","king size"},
			{"bed size","queen size"},
			{"bed size","twin size"},
			{"car part","chassi"},
			{"size","larger"},
			{"size","large"},
			{"size","smaller"},
			{"size","shorter"},
			{"size","small"},
			{"fuel","ga"},
			{"bath","bathroom"},
			{"room","bath"},
			{"room","bedroom"},
			{"room","kitchen"},
			{"room","area"},
			{"room","space"},
			{"new","freshli"},
			{"new","updat"},
			{"new","renov"},
			{"new","newli"},
			{"new","remodel"},
			{"new","recent"},
			{"closet","chest drawer"},
			{"closet","desk"},
			{"owner","tenant"},
			{"design","adorn"},
			//{"",""},
		};

		for(int i = 0; i < thesaurus.length; i++) {
			concat = concat.replaceAll(thesaurus[i][1], thesaurus[i][0]);
		}
		//System.out.println(concat);
		sentence = concat.split(" ");
		return sentence;
	}

	/** Remove the Tokens that have low frequency within a given document relative to the other
	 * 	documents. In other words, remove the tokens with very low discriminatory power.
	 * 
	 * @param tk An array of Tokens with a typical weightedFreq between 0.3 and 5.5.
	 * @param threshold A double representing the minimum acceptable value for weightedFreq.
	 * @return The same Token array, but only including the tokens for which weightedFreq
	 * 	is greater than or equal to the threshold.
	 */
	public static Token[] removeByWeightedFreq(Token[] tk, double threshold) {
		List<Token> t = new ArrayList<Token>(Arrays.asList(tk));	
		t.removeIf(token -> token.getWeightedFreq() < threshold);
		return tk;
	}

	public static String[] generateTermsArray(ArrayList<String[]> featureVector) {
		ArrayList<String> termsAL = new ArrayList<String>();
		for(String[] stArr : featureVector) {
			for(int i = 0; i < stArr.length; i++) {
				termsAL.add(stArr[i]);
			}
		}
		termsAL = new ArrayList<String>(new HashSet<String>(termsAL));
		String[] terms = new String[termsAL.size()];
		termsAL.toArray(terms);
		Arrays.sort(terms);

		return terms;
	}

	public static int[][] generateTDM(ArrayList<String[]> featureVector, String[] terms) {
		// the outer dimension is the set of sentences, the inner dimension is the set of terms
		int[][] tdm = new int[featureVector.size()][terms.length];
		int count;
		for(int dIndex = 0; dIndex < tdm.length; dIndex++) {
			for(int tIndex = 0; tIndex < tdm[dIndex].length; tIndex++) {
				count = 0;
				for(String t : featureVector.get(dIndex)) {
					if(t.equals(terms[tIndex])) {
						count++;
					}
				}
				tdm[dIndex][tIndex] = count;
			}
		}
		return tdm;
	}

	/** Form an ArrayList of clusters using the FCAN algorithm on a Term Document Matrix.
	 * 
	 * @param tdm The TDM.
	 * @return The ArrayList of clusters.
	 */
	public static ArrayList<Cluster> formClustersAsNeeded(int[][] tdm, double alpha, double threshold) {
		double[][] orderedTDM = tdmToOrderedTDM(tdm);
		//orderedTDM = reorderTDM(orderedTDM);

		ArrayList<Cluster> clusters = new ArrayList<Cluster>();
		// Apply first pattern and form first cluster
		clusters.add(new Cluster(orderedTDM[0], alpha, threshold));

		for(int i = 1; i < orderedTDM.length; i++) {
			double minDistance = threshold * 2;
			double distance = 0.0;
			double[] w = new double[0];
			// Find the minimum distance from next pattern to each cluster
			ListIterator<Cluster> iter = clusters.listIterator();
			while(iter.hasNext()) {
				Cluster c = iter.next();
				distance = Cluster.distanceFromCluster(c.weights, orderedTDM[i]);
				if(distance < minDistance) {
					minDistance = distance;
					w = c.weights;
				}
			}
			if(minDistance <= threshold) {
				iter = clusters.listIterator();
				while(iter.hasNext()) {
					Cluster c = iter.next();
					if(c.weights.equals(w)) {
						c.addDocument(orderedTDM[i]);
						iter.set(c);
						break;
					}
				}
			}
			else {
				// Form a new cluster
				clusters.add(new Cluster(orderedTDM[i], alpha, threshold));
			}
		}

		clusters = reorderClusters(clusters);		
		return clusters;
	}

	/** Add a column to the TDM before the columns for words, to record which row 
	 * each sentence was originally in.
	 * @param tdm The Term Document Matrix.
	 * @return The Term Document Matrix with the order recorded.
	 */
	public static double[][] tdmToOrderedTDM(int[][] tdm) {
		double[][] orderedTDM = new double[tdm.length][tdm[0].length + 1];
		for(int i = 0; i < tdm.length; i++) {
			orderedTDM[i][0] = (double) i;		
			// copy all of the data for the original TDM
			for(int j = 0; j < tdm[i].length; j++) {
				orderedTDM[i][j + 1] = (double) tdm[i][j];
			}
		}		
		return orderedTDM;
	}

	public static double[][] reorderTDM(double[][] orderedTDM) {
		ArrayList<double[]> reordered = new ArrayList<double[]>();
		for(int i = 0; i < orderedTDM.length; i++) {
			reordered.add((int)(Math.random()*(reordered.size() - 1)), orderedTDM[i]);
		}	
		return reordered.toArray(orderedTDM);
	}

	/** Reorder an ArrayList of clusters so that all of the clusters containing only
	 * a single document are moved to the end.
	 * 
	 * @param clusters An ArrayList of clusters in no particular order.
	 * @return An ArrayList of clusters in the order described above.
	 */
	private static ArrayList<Cluster> reorderClusters(ArrayList<Cluster> clusters) {
		ArrayList<Cluster> singles = new ArrayList<Cluster>();
		ListIterator<Cluster> iter = clusters.listIterator();
		while(iter.hasNext()) {
			Cluster c = iter.next();
			if(c.getDocuments().size() == 1) {
				singles.add(c);
				iter.remove();
			}
		}
		clusters.addAll(singles);
		return clusters;
	}
}