import math;
import random;
import copy;
import dataProcessing;
import visualization;
import numpy;

class roteClassification:
	def __init__(self, stars, constellationNames):
		self.assignments = copy.deepcopy(stars);
		self.constellationNames = constellationNames.keys();

	def runRoteClassification(self):
		for idx in range(len(self.assignments)):
			for i in range(len(self.constellationNames)):
				if self.assignments[idx]['name'][-3:] == self.constellationNames[i]:
					key = 'centroid_' + str(i+1);
					self.assignments[idx]['assignment'] = key;
					continue;

	def getNumOfClusters(self):
		return len(self.constellationNames);

	def getCluster(self, clusterIdx):
		cluster = [];
		key = 'centroid_' + str(clusterIdx + 1);
		for i in range(len(self.assignments)):
			if self.assignments[i]['assignment'] == key:
				cluster.append(self.assignments[i]);
		return cluster;

	def getClustername(self,clusterIdx):
		key = 'centroid_' + str(clusterIdx + 1);
		for i in range(len(self.assignments)):
			if(self.assignments[i]['assignment']==key):
				return self.assignments[i]['name'][-3:];

	def getClusterCenter(self, clusterIdx):
		center = {};
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
	database = dataProcessing.readJson();
	starsNeedClustering = dataProcessing.selectBrightness(database, 4.6);
	constellationNames = dataProcessing.getConstellationNames(starsNeedClustering);
	classifier = roteClassification(starsNeedClustering,constellationNames);
	classifier.runRoteClassification();
	visualization.visualize(classifier.assignments, 'Original');
	#centers = [];
	#for i in range(len(constellationNames)):
		#print(classifier.getClustername(i));
		#visualization.visualize(classifier.getCluster(i),'Original');
main();