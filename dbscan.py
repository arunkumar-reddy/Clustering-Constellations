import math;
import random;
import copy;
import dataProcessing;
import argparse;
import visualization;
import numpy;
from sklearn.cluster import DBSCAN;
from scipy.spatial import distance;
from sklearn import metrics;

class densityBasedClustering:
	def __init__(self, stars, Eps, minDist):
		self.assignments = copy.deepcopy(stars);
		self.Eps = Eps;
		self.minDist = minDist;
		self.coordinates = [];
		self.numOfClusters = 0;
		self.silhouetteScore = 0;
		self.adjustedScore = 0;
		self.belongs = [];
		for i in range(len(self.assignments)):
			coordinate = [self.assignments[i]['x'], self.assignments[i]['y'], self.assignments[i]['z']];
			self.coordinates.append(coordinate);

	def runDBA(self):
		distMatrix = distance.squareform(distance.pdist(self.coordinates, 'cosine'));
		model = DBSCAN(eps = self.Eps, min_samples = self.minDist).fit(distMatrix);
		self.belongs = model.labels_.tolist();
		for i in range(len(self.belongs)):
			self.assignments[i]['assignment'] = 'centroid_' + str(self.belongs[i]+1);
		self.numOfClusters = len(set(self.belongs)) - (1 if -1 in self.belongs else 0);
		self.silhouetteScore = metrics.silhouette_score(distMatrix, model.labels_, metric = 'cosine');
		trueLabel = dataProcessing.getTrueLabel(self.assignments);
		self.adjustedScore = metrics.adjusted_rand_score(self.belongs, trueLabel);

	def getNumOfClusters(self):
		return self.numOfClusters;

	def getClusterLabels(self):
		return self.belongs;

	def getCluster(self, clusterIdx):
		cluster = [];
		key = 'centroid_' + str(clusterIdx+1);
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
	
	def getNoise(self):
		noise = []
		for i in range(len(self.assignments)):
			if self.assignments[i]['assignment'] == 'centroid_0':
				noise.append(self.assignments[i])
		return noise;

def main():
	parser = argparse.ArgumentParser();
	parser.add_argument('eps',type = float, help = 'Epilson');
	parser.add_argument('samples',type = int, help = 'Minimum Samples');
	args = parser.parse_args();
	database = dataProcessing.readJson();
	starsNeedClustering = dataProcessing.selectBrightness(database, 4.6);
	constellationNames = dataProcessing.getConstellationNames(starsNeedClustering);
	dbscan = densityBasedClustering(starsNeedClustering,args.eps,args.samples);
	dbscan.runDBA();
	print('The number of clusters are '+str(dbscan.getNumOfClusters()));
	print('The Silhouette score is '+str(dbscan.silhouetteScore));
	print('The Adjusted Rand Index is '+str(dbscan.adjustedScore));
	visualization.visualize(dbscan.assignments, 'DBSCAN');

#main();