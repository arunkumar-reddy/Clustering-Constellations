### Constellation-clustering

Semester project

Author: Arun kumar Reddy

#### Running Command Version:
Running **Kmeans**:
  python kmeans.py -k (where k is replaced by the number of clusters)

Running **DBSCAN**:
  python dbscan.py -eps -mindist (where eps is the radius and mindist is the minimum number of points) 

Running **Hierachical Clustering**:
  python hierarchical.py -k (k is the number of clusters)

Running **Affinity Propagation**:
  python affinityprop.py  -d -iter (d is the damping factor(0 to 1) and iter is the number of iterations)

Running **Weighted K-Means**:
  python weighted.py -k (k is the number of clusters)

Running **Density based K-Means**:
  python dbkmeans.py -k -eps -mindist (parameters same as K-means and DBSCAN)

Running **Rote Classification**:
  python rote.py (Original constellations)

#### Files
dataprocessing.py - Data processing from the dataset.
visualization.py - Visualize the newly formed clusters.

#### Dataset
HYG star Catalog - Combines the Bright star and Hipparcos catalog. file - hyg.json
Brightstar Catalog - database.json

#### Requirements:
1. [scipy] - package for scientific computing.
2. [numpy] - package for numeric computing.
3. [sklearn] - package for machine learning algorithms.
