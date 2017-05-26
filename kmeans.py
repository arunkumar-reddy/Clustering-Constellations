import math;
import random;
import copy;
import dataProcessing;
import visualization;
import argparse;
import numpy;
from sklearn.cluster import KMeans;
from scipy.spatial import distance;
from sklearn import metrics;

class KMeansPlusPlus:
	def __init__(self, stars, K):
		self.assignments = copy.deepcopy(stars);
		self.K = K;
		self.coordinates = [];
		self.silhouetteScore = 0;
		self.adjustedScore = 0;
		for i in range(len(self.assignments)):
			coordinate = [self.assignments[i]['x'], self.assignments[i]['y'], self.assignments[i]['z']];
			self.coordinates.append(coordinate);

	def runKmeansPlusPlus(self):
		distMatrix = distance.squareform(distance.pdist(self.coordinates, 'cosine'));
		model = KMeans(n_clusters = self.K, init = 'k-means++', n_init = 10, max_iter = 300).fit(distMatrix);
		belongs = model.labels_.tolist();
		for i in range(len(belongs)):
			self.assignments[i]['assignment'] = 'centroid_' + str(belongs[i]+1);
		self.silhouetteScore = metrics.silhouette_score(distMatrix, model.labels_, metric = 'cosine');
		trueLabel = dataProcessing.getTrueLabel(self.assignments);
		self.adjustedScore = metrics.adjusted_rand_score(belongs, trueLabel);


	def getCluster(self, clusterIdx):
		cluster = [];
		key = 'centroid_' + str(clusterIdx+1)
		for i in range(len(self.assignments)):
			if self.assignments[i]['assignment'] == key:
				cluster.append(self.assignments[i]);
		return cluster;

	def getClusterCenter(self, clusterIdx):
		center['x'] = 0.0;
		center['y'] = 0.0;
		center['z'] = 0.0;
		center['assignment'] = clusterIdx+1;
		count = 0;
		key = 'centroid_' + str(clusterIdx + 1);
		for i in range(len(self.assignments)):
			if self.assignments[i]['assignment'] == key:
				center['x'] = center['x']+self.assignments[i]['x'];
				center['y'] = center['y']+self.assignments[i]['y'];
				center['z'] = center['z']+self.assignments[i]['z'];
				count += 1;
		center['x'] /= count;
		center['y'] /= count;
		center['z'] /= count;
		return center;

def main():
	parser = argparse.ArgumentParser();
	parser.add_argument('k',type = int, help = 'Input number of clusters');
	args = parser.parse_args();
	database = dataProcessing.readJson();
	starsNeedClustering = dataProcessing.selectBrightness(database, 2.6);
	constellationNames = dataProcessing.getConstellationNames(starsNeedClustering);
	standardKMeans = KMeansPlusPlus(starsNeedClustering,args.k);
	standardKMeans.runKmeansPlusPlus();
	print('The Silhouette score is '+str(standardKMeans.silhouetteScore));
	print('The Adjusted Rand Index is '+str(standardKMeans.adjustedScore));
	visualization.visualize(standardKMeans.assignments, 'Kmeans');

main();