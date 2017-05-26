import json;
import math;

inputFileName = 'hyg.json';
def readJson():
	outputDict = {};
	inputJson = open(inputFileName);
	data = json.load(inputJson);
	inputJson.close()
	return data;

def transformCoordinate(data):
	for i in range(len(data)):
		if data[i]['theta'] == None or data[i]['phi'] == None:
			continue;
		data[i]['theta'] *= math.pi/180;
		data[i]['phi'] *= math.pi/180;
		data[i]['x'] = basicFun.getXCoor(data[i]['theta'], data[i]['phi']);
		data[i]['y'] = basicFun.getYCoor(data[i]['theta'], data[i]['phi']);
		data[i]['z'] = basicFun.getZCoor(data[i]['theta'], data[i]['phi']);
	return data;

def chooseStarWithName(data):
	starWithName = [];
	for index in range(len(data)):
		if data[index]['name'] == '' or 'NOVA' in data[index]['name'] or data[index]['mag'] == None:
			continue;
		starWithName.append(data[index]);
	return starWithName;


def selectBrightness(data, threshold, constellationName = None):
	selectedStars = [];
	for index in range(len(data)):
		if constellationName == None:
			if data[index]['mag'] <= threshold:
				selectedStars.append(data[index]);
		else:
			if data[index]['mag'] <= threshold and constellationName in data[index]['name']:
				selectedStars.append(data[index]);
	return selectedStars;

def selectNames(data, constellationName, threshold = None):
	selectedStars = [];
	for index in range(len(data)):
		if threshold == None:
			if constellationName in data[index]['name']:
				selectedStars.append(data[index]);
		else:
			if constellationName in data[index]['name'] and data[index]['mag'] <= threshold:
				selectedStars.append(data[index]);
	return selectedStars;

def getConstellationNames(data):
	constellationNames = {};
	for index in range(len(data)):
		constellationNames[data[index]['name'][-3:]] = 1;
	return constellationNames;

def getTrueLabel(data):
	trueLabel = [];
	constellationNames = list(getConstellationNames(data));
	for i in range(len(data)):
		for j in range(len(constellationNames)):
			if data[i]['name'][-3:] == constellationNames[j]:
				trueLabel.append(j);
				continue;
	return trueLabel;


