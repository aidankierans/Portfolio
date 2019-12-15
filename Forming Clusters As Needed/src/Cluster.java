/* @author Aidan Kierans
 * V#: V00819990
 *
 * CMSC 409 AI Fall 2019
 */

import java.util.ArrayList;

public class Cluster {
	
	private ArrayList<double[]> documents;
	public double[] weights;
	public double alpha;
	public double threshold;
	
	/** Generate an initial cluster for a Term Document Matrix that has the
	 * order of the documents denoted by the first value in each row.
	 * 
	 * @param orderedTDM The TDM with its ordering recorded in the first column.
	 * @param alpha The learning rate of the cluster neuron.
	 * @param Threshold The maximum distance from the center of the cluster allowed.
	 */
	public Cluster(double[][] orderedTDM, double alpha, double threshold) {
		new Cluster(orderedTDM[0], alpha, threshold);
	}

	/** Generate a new cluster centered on the given point in hyperspace.
	 * 
	 * @param doc A document/coordinate vector in hyperspace for which the first
	 * value is the identifying index of the document and the rest of the values
	 * are its location.
	 * @param alpha The learning rate of the cluster neuron.
	 * @param threshold The maximum distance from the center of the cluster allowed.
	 */
	public Cluster(double[] doc, double alpha, double threshold) {
		this.weights = new double[doc.length - 1];
		for(int i = 0; i < weights.length; i++) {
			weights[i] = doc[i + 1];
		}
		this.alpha = alpha;
		this.threshold = threshold;
		this.documents = new ArrayList<double[]>();
		this.documents.add(doc);
	}
	
	public ArrayList<double[]> getDocuments() {
		return this.documents;
	}
	
	public void addDocument(double[] doc) {
		this.documents.add(doc);
		updateWeights();
	}
	
	/** Remove a document based on its double ID, which is the first double in
	 * each array in an orderedTDM.
	 * 
	 * @param originalID The ID of the document in the orderedTDM.
	 */
	public void removeDocument(double originalID) {
		this.documents.removeIf(doc -> doc[0] == originalID);
	}
	
	private void updateWeights() {
		// calculate the new weights
		// m is the number of documents in this cluster before the most recent one was added
		double m = (double)(documents.size() - 1);
		for(int i = 0; i < weights.length; i++) {
			double[] doc = documents.get(documents.size() - 1);
			weights[i] = m*weights[i] + alpha*doc[i + 1];
			weights[i] = weights[i]/(m + 1.0);
		}
	}
	
	@Override
	public String toString() {
		String str = "(";
		for(double[] d : documents) {
			str += Integer.toString((int)d[0]) + ", ";
		}
		str += ")";
		return str;
	}
	
	public boolean activates(double[] doc) {
		return distanceFromCluster(this.weights, doc) <= threshold;
	}
	
	/** Calculate the Euclidean distance between the centroid of this cluster and 
	 * some other cluster.
	 * 
	 * @param otherC The cluster to which the distance should be found from this one.
	 * @return The Euclidean distance to the other cluster from this one. 
	 */
	/*public double distance(Cluster otherC) {
		return distance(this.weights, otherC.weights);
	}*/

	/** Calculate the Euclidean distance between two points in n-dimensional space
	 * 
	 * @param w1 An array of length n
	 * @param w2 Another array of length n
	 * @return The Euclidean distance between w1 and w2.
	 */
	public static double distance(int[] w1, int[] w2) {
		double d = 0.0;
		for(int i = 0; i < w1.length; i++) {
			d += Math.pow((double)(w1[i] - w2[i]), 2);
		}
		return Math.sqrt(d);
	}
	
	public static double distanceFromCluster(double[] w, double[] doc) {
		double d = 0.0;
		for(int i = 0; i < w.length; i++) {
			d += Math.pow(w[i] - doc[i + 1], 2);
		}
		return Math.sqrt(d);
	}	
	
}
