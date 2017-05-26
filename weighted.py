import math;
import random;
import copy;
import dataProcessing;
import visualization;
import basicFun;
import argparse;
import numpy;
from sklearn import metrics;
from scipy.spatial import distance;

class Kmeans:
	def __init__(self, stars, K, centroid = None):
		self.K = K;
		self.assignments = copy.deepcopy(stars);
		self.silhouetteScore = 0;
		self.adjustedScore = 0;
		self.coordinates = [];
		for i in range(len(self.assignments)):
			coordinate = [self.assignments[i]['x'], self.assignments[i]['y'], self.assignments[i]['z']];
			self.coordinates.append(coordinate);
		for idx in range(len(self.assignments)):
			self.assignments[idx]['assignment'] = 'centroid_1';
		if centroid == None:
			self.centroid = {}
			for i in range(K):
				key = 'centroid_' + str(i+1);
				self.centroid[key] = [0, 0, 0];
		else:
		  self.centroid = centroid;

	def randInitCentroid(self):
		for i in range(self.K):
			key = 'centroid_' + str(i+1);
			x = random.uniform(-100,100);
			y = random.uniform(-100,100);
			z = random.uniform(-100,100); 
			self.centroid[key] = [x,y,z];
		return;
	
	def decisiveInitCentroid(self):
		chosenStars = random.sample(self.assignments, self.K);
		for i in range(self.K):
			key = 'centroid_' + str(i+1);
			self.centroid[key] = [chosenStars[i]['x'], chosenStars[i]['y'], chosenStars[i]['z']];
		return;
	
	def densityBasedInitCentroid(self):
		return;

	def getCluster(self,centroidIdx):
		key = 'centroid_' + str(centroidIdx+1);
		cluster = [];
		for i in range(len(self.assignments)):
			if self.assignments[i]['assignment'] == key:
				cluster.append(self.assignments[i]);
		return cluster;

	def getDissimilarity(self):
		dissimilarity = 0;
		for idx in range(len(self.assignments)):
			star = self.assignments[idx];
			belong = star['assignment'];
			dissimilarity += basicFun.cosDissimilarity([star['x'], star['y'], star['z']], \
					[self.centroid[belong][0], self.centroid[belong][1], self.centroid[belong][2]]);
		return dissimilarity;

	def runStandardKmeansWithIter(self, maxIter):
		# performing K-means
		count = 1;
		while count <= maxIter:
			count += 1;
			# step 1: updating the assignments
			for star in self.assignments:
				dist = [];
				x = star['x'];
				y = star['y'];
				z = star['z'];
				for i in range(len(self.centroid)):
					key = 'centroid_' + str(i+1);
					x_center = self.centroid[key][0];
					y_center = self.centroid[key][1];
					z_center = self.centroid[key][2];
					#dist.append(basicFun.cosDissimilarity([x,y,z], [x_center, y_center, z_center]))
					dist.append(basicFun.weightedCosDissimilarity([x,y,z], [x_center, y_center, z_center], star['mag']));
				idx = dist.index(min(dist));
				star['assignment'] = 'centroid_' + str(idx+1);

			for i in range(len(self.centroid)):
				key = 'centroid_' + str(i+1);
				self.centroid[key]=[0,0,0];
				for star in self.assignments:
					if star['assignment'] == key:
						self.centroid[key][0] += star['x'];
						self.centroid[key][1] += star['y'];
						self.centroid[key][2] += star['z'];
				norm = basicFun.getNorm(self.centroid[key]);
				if norm == 0:
					continue;
				self.centroid[key][0] /= norm;
				self.centroid[key][1] /= norm;
				self.centroid[key][2] /= norm;
		distMatrix = distance.squareform(distance.pdist(self.coordinates, 'cosine'));
		belongs = [];
		for i in range(len(self.assignments)):
			belongs.append(self.assignments[i]['assignment'][9:]);
		trueLabel = dataProcessing.getTrueLabel(self.assignments);
		self.silhouetteScore = metrics.silhouette_score(distMatrix, belongs, metric = 'cosine');
		self.adjustedScore = metrics.adjusted_rand_score(belongs, trueLabel);	
		return;

def main():
	parser = argparse.ArgumentParser();
	parser.add_argument('k',type = int, help = 'Input number of clusters');
	args = parser.parse_args();
	database = dataProcessing.readJson();
	starsNeedClustering = dataProcessing.selectBrightness(database, 4.6);
	constellationNames = dataProcessing.getConstellationNames(starsNeedClustering);
	classifier = Kmeans(starsNeedClustering,args.k);
	classifier.randInitCentroid();
	classifier.runStandardKmeansWithIter(500);
	print('The Silhouette score is '+str(classifier.silhouetteScore));
	print('The Adjusted Rand index score is '+str(classifier.adjustedScore));
	visualization.visualize(classifier.assignments, 'Kmeans');

main();