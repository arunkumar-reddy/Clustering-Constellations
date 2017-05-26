import math;
import random;
import copy;
import dataProcessing;
import argparse;
import visualization;
import numpy;
from sklearn.cluster import AffinityPropagation;
from scipy.spatial import distance;
from sklearn import metrics;

class affinityPropagation:
	def __init__(self, stars, damping, max_iter):
		self.assignments = copy.deepcopy(stars);
		self.damping = damping;
		self.max_iter = max_iter;
		self.coordinates = [];
		self.center_id = [];
		self.silhouetteScore = 0;
		self.adjustedScore = 0;
		for i in range(len(self.assignments)):
			coordinate = [self.assignments[i]['x'], self.assignments[i]['y'], self.assignments[i]['z']];
			self.coordinates.append(coordinate);

	def runAffinityPropagation(self):
		distMatrix = distance.squareform(distance.pdist(self.coordinates, 'cosine'));
		size = distMatrix.shape;
		for i in range(size[0]):
			for j in range(size[1]):
				distMatrix[i,j] = 2 - distMatrix[i,j];
		model = AffinityPropagation(damping = self.damping, max_iter = self.max_iter,affinity = 'precomputed');
		model.fit(distMatrix);
		self.center_id = model.cluster_centers_indices_.tolist();
		belongs = model.labels_.tolist();
		for i in range(len(belongs)):
			self.assignments[i]['assignment'] = 'centroid_' + str(belongs[i] + 1);
		self.silhouetteScore = metrics.silhouette_score(distMatrix, model.labels_, metric = 'cosine');
		trueLabel = dataProcessing.getTrueLabel(self.assignments);
		self.adjustedScore = metrics.adjusted_rand_score(belongs, trueLabel);

	def getNumOfClusters(self):
		return len(self.center_id);

	def getCenters(self):
		center = [];
		for i in range(len(self.center_id)):
			center.append(self.assignments[self.center_id[i]]);
		return center;

	def getCluster(self, clusterIdx):
		cluster = [];
		key = 'centroid_' + str(clusterIdx + 1);
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

	def getDissimilarity(self):
		dissimilarity = 0;
		for idx in range(len(self.assignments)):
			star = self.assignments[idx];
			belong = int(star['assignment'][-1])-1;
			dissimilarity += basicFun.cosDissimilarity([star['x'], star['y'], star['z']], \
					[self.assignments[self.center_id[belong]]['x'], self.assignments[self.center_id[belong]]['y'], self.assignments[self.center_id[belong]]['z']]);
		return dissimilarity;

def main():
	parser = argparse.ArgumentParser();
	parser.add_argument('damp',type = float, help = 'Damping Factor');
	parser.add_argument('iter',type = int, help = 'Max number of iterations');
	args = parser.parse_args();
	database = dataProcessing.readJson();
	starsNeedClustering = dataProcessing.selectBrightness(database, 2.6);
	constellationNames = dataProcessing.getConstellationNames(starsNeedClustering);
	affinityprop = affinityPropagation(starsNeedClustering,args.damp,args.iter);
	affinityprop.runAffinityPropagation();
	print('The number of clusters are '+str(affinityprop.getNumOfClusters()));
	print('The Silhouette score is '+str(affinityprop.silhouetteScore));
	print('The Adjusted Rand Index is '+str(affinityprop.adjustedScore));
	visualization.visualize(affinityprop.assignments, 'Affinity Propagation');

main();