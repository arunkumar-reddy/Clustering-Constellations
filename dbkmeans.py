import math;
import random;
import copy;
import dataProcessing;
import visualization;
import basicFun;
import argparse;
import numpy;
from dbscan import densityBasedClustering;
from sklearn import metrics;
from scipy.spatial import distance;

class DBKmeans():
	def __init__(self,stars,K,number):
		self.assignments = copy.deepcopy(stars);
		self.K = K;
		self.adjustedScore = 0;
		self.silhouetteScore = 0;
		self.n_clusters = number;
		self.coordinates = [];
		for i in range(len(self.assignments)):
			coordinate = [self.assignments[i]['x'], self.assignments[i]['y'], self.assignments[i]['z']];
			self.coordinates.append(coordinate);
		for i in range(len(self.assignments)):
			self.assignments[i]['visited'] = False;

	def ComputeCentroids(self):
		centroids = [];
		count = 0;
		for i in range(self.n_clusters):
			key = 'centroid_' + str(i+1);
			centroid = [0,0,0];
			for star in self.assignments:
				if star['assignment'] == key:
					centroid[0] += star['x'];
					centroid[1] += star['y'];
					centroid[2] += star['z'];
			norm = basicFun.getNorm(centroid);
			if norm == 0:
				continue;
			centroid[0] /= norm;
			centroid[1] /= norm;
			centroid[2] /= norm;
			centroids.append(centroid);
		return centroids;

	def update(self,a,b):
		m = min(a,b);
		centroid = [0,0,0];
		for i in range(self.n_clusters):
			key1 = 'centroid_' + str(a+1);
			key2 = 'centroid_' + str(b+1);
			for i in range(len(self.assignments)):
				if (self.assignments[i]['assignment'] == key1 or self.assignments[i]['assignment'] == key2):
					centroid[0] += self.assignments[i]['x'];
					centroid[1] += self.assignments[i]['y'];
					centroid[2] += self.assignments[i]['z'];
					self.assignments[i]['assignment'] = 'centroid_'+ str(m+1);
			norm = basicFun.getNorm(centroid);
			if norm == 0:
				continue;
			centroid[0] /= norm;
			centroid[1] /= norm;
			centroid[2] /= norm;
		return centroid;

	def runDBKMeans(self,belongs,number):
		for i in range(len(belongs)):
			self.assignments[i]['assignment'] = 'centroid_' + str(belongs[i]+1);
		centroids = self.ComputeCentroids();
		while(number>self.K):
			lim = 1000;
			x = 0;
			y = 0;
			for i in range(len(centroids)):
				for j in range(len(centroids)):
					if(i==j):
						continue;
					dist = basicFun.cosDissimilarity([centroids[i][0],centroids[i][1],centroids[i][2]], [centroids[j][0],centroids[j][1],centroids[j][2]]);
					if(dist<lim):
						lim = dist;
						x = i;
						y = j;
			centroid = self.update(x,y);
			centroids[min(x,y)] = centroid;
			del centroids[max(x,y)];
			number -= 1;
		clusters = [];
		for i in range(len(self.assignments)):
			clusters.append(self.assignments[i]['assignment'][9:]);
		distMatrix = distance.squareform(distance.pdist(self.coordinates, 'cosine'));
		self.silhouetteScore = metrics.silhouette_score(distMatrix, clusters, metric = 'cosine');
		trueLabel = dataProcessing.getTrueLabel(self.assignments);
		self.adjustedScore = metrics.adjusted_rand_score(clusters, trueLabel);

def main():
	parser = argparse.ArgumentParser();
	parser.add_argument('k',type = int, help = 'Input number of clusters');
	parser.add_argument('eps',type = float, help = 'Epilson');
	parser.add_argument('samples',type = int, help = 'Minimum Samples');
	args = parser.parse_args();
	database = dataProcessing.readJson();
	starsNeedClustering = dataProcessing.selectBrightness(database, 4.6);
	constellationNames = dataProcessing.getConstellationNames(starsNeedClustering);
	dbscan = densityBasedClustering(starsNeedClustering,args.eps,args.samples);
	dbscan.runDBA();
	labels = dbscan.getClusterLabels();
	num = dbscan.getNumOfClusters();
	print(dbscan.adjustedScore);
	classifier = DBKmeans(starsNeedClustering,args.k,num);
	classifier.runDBKMeans(labels,num);
	print(classifier.silhouetteScore);
	print(classifier.adjustedScore);
	visualization.visualize(classifier.assignments, 'DBKmeans');

main();