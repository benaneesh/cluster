from parse_dataset import *
import numpy as np
import pylab as pl
from matplotlib import offsetbox
from sklearn.utils.fixes import qr_economic
from sklearn import manifold, datasets
from sklearn.cluster import AffinityPropagation
from itertools import cycle

sim = dataset_extractor()
sim = np.around(sim, decimals=4)

for i in range(sim.shape[1]):
    for j in range(sim.shape[0]):
        status = sim[i][j]==sim[j][i]
        if not status:
            print sim[i][j]
            print sim[j][i]

print "Computing MDS embedding"
clf = manifold.MDS(n_components=2, n_init=1, max_iter=100)
mds = clf.fit_transform(sim)

pl.close('all')
pl.figure(1)
pl.clf()

for i in mds:
    pl.plot(i[0], i[1], 'b.')
#pl.show()

pl.close('all')
pl.figure(1)
pl.clf()

af = AffinityPropagation().fit(sim, sim[1][1])
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

pl.close('all')
pl.figure(1)
pl.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = mds[cluster_centers_indices[k]]
    pl.plot(mds[class_members, 0], mds[class_members, 1], col + '.')
    pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)
    for x in mds[class_members]:
        pl.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()
