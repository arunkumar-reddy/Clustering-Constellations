import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import scipy.cluster.hierarchy as hac

def out(x):
	if(x>100 or x<(-100)):
		return True;
	else:
		return False;

def visualize(assignments, algorithm):
	x = [];
	y = [];
	z = [];
	size = [];
	color = [];
	for idx in range(len(assignments)):
		star = assignments[idx];
		if(out(star['x']) or out(star['y']) or out(star['z'])):
			continue;
		x.append(star['x']);
		y.append(star['y']);
		z.append(star['z']);
		size.append(600/math.exp(star['mag']));
		color.append(int(star['assignment'][-1]));
	fig = plt.figure();
	ax = fig.add_subplot(111, projection = '3d');
	ax.scatter(x,y,z,c=color,marker='o');
	#ax.set_xlabel('X Axis');
	#ax.set_ylabel('Y Axis');
	#ax.set_zlabel('Z Axis');
	ax.set_xticks([]);
	ax.set_yticks([]);
	ax.set_zticks([]);
	ax.set_axis_off();
	ax.set_title(algorithm);
	plt.show();

def clusters(assignments, algorithm):
	x = [];
	y = [];
	z = [];
	color = [];
	for idx in range(len(assignments)):
		star = assignments[idx];
		if(out(star['x']) or out(star['y']) or out(star['z'])):
			continue;
		x.append(star['x']);
		y.append(star['y']);
		z.append(star['z']);
		color.append(star['assignment']);
	fig = plt.figure();
	ax = fig.add_subplot(111, projection = '3d');
	ax.scatter(x,y,z,c=color,marker='o');
	ax.set_xticks([]);
	ax.set_yticks([]);
	ax.set_zticks([]);
	ax.set_axis_off();
	ax.set_title(algorithm);
	plt.show();	

def drawDendrogram(linkMatrix):
	fig = plt.figure(linewidth=10);
	ax = fig.add_subplot(111);
	tree = hac.dendrogram(linkMatrix);
	ax.set_yticks([]);
	ax.set_xticks([]);
	ax.set_axis_off();
	plt.show();

