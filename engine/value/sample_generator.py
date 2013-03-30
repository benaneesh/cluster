"""
=================================================
Demo of affinity propagation clustering algorithm
=================================================

Reference:
Brendan J. Frey and Delbert Dueck, "Clustering by Passing Messages
Between Data Points", Science Feb. 2007

"""
print __doc__

import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.datasets.samples_generator import *

##############################################################################

#######################################
## Generate cluster blob sample data
#######################################

centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=300, centers=centers, cluster_std=0.5)

"""
    this give us 300 points in a randon number of blobs
"""
#######################################
## Generate classification sample data
#######################################

Y = make_classification(
    n_samples=100, 
    n_features=20, 

    # following is the characteristic of the features
    n_informative=2, 
    n_redundant=2, 
    n_repeated=0, 
    n_classes=2, 
    n_clusters_per_class=2, 
    weights=None, 
    flip_y=0.01, 
    class_sep=1.0, 
    hypercube=True, 
    shift=0.0, 
    scale=1.0, 
    shuffle=True, 
    random_state=None)

"""
print Y
print len(Y)
print len(Y[0]) # 100 points vector
print len(Y[1]) # 100 points label
print len(Y[0][0]) # vector size is 20 -> 20 features

    this give us 100 points with feature vector of 20

    notes:
    random_state: 
    if int, random_state is the seed used by the random number generator; 
    If RandomState instance, random_state is the random number generator; 
    If None, the random number generator is the RandomState instance used by np.random.

    return:
    X : array of shape [n_samples, n_features]
        The generated samples.

    y : array of shape [n_samples]
        The integer labels for class membership of each sample.
"""


#######################################
## Generate circles sample data
#######################################
Z = make_circles(n_samples=100, shuffle=True, noise=None, random_state=None, factor=0.80000000000000004)
"""
Z[0] is all the data points(2D), including one big circle, one small circle
z[1] is all the labels of the data
print Z
"""

#######################################
## Generate moon sample data
#######################################
#Z = make_moons(n_samples=1500, shuffle=True, noise=0.5, random_state=None)
Z = make_moons(n_samples=1500, noise=.05)

##############################################################################





# Plot result
import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()

# Plot All Graphs
colors = 'bgrcmykbgrcmykbgrcmykbgrcmyk'
for count in range(len(Z[0])):
    point = Z[0][count]
    label = Z[1]
    pl.plot(point[0], point[1], colors[label[count]]+'.')
pl.show()

"""
colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_membera = laels == k
    cluster_center = X[cluster_centers_indices[k]]
    print cluster_center
    print class_members

    print len(X[class_members])
    pl.plot(X[class_members, 0], X[class_members, 1], col + '.')
    pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)
    for x in X[class_members]:
        pl.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

pl.title('Estimated number of clusters: %d' % n_clusters_)
#pl.show()
"""
