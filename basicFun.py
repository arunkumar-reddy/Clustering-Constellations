from math import cos;
from math import sin;
from math import asin;
import math;

def getEuclideanDistance(list_1, list_2):
	dist = 0;
	for i in range(len(list_1)):
		dist += (list_1[i]-list_2[i])**2;
	return math.sqrt(dist);

def getSphericalDistance(list_1, list_2):
	dist = getEuclideanDistance(list_1,list_2);
	return 2*asin(0.5*dist);

def cosDissimilarity(list_1, list_2):
	return 1 - (list_1[0] * list_2[0] + list_1[1] * list_2[1] + list_1[2] * list_2[2]);

def weightedCosDissimilarity(list_1, list_2, brightness):
	return math.exp(-brightness)*cosDissimilarity(list_1, list_2);

def getNorm(a_list):
	return math.sqrt(a_list[0]**2 + a_list[1]**2 + a_list[2]**2);

