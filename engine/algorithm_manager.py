import numpy as np
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.datasets.samples_generator import make_circles
from sklearn.datasets.samples_generator import *
from sklearn import cluster, datasets
from greedyCluster import *


def generate_blob_sample():
    X, y = datasets.make_blobs(n_samples=5000, random_state=8)
    blob_dict = {}
    count = 0
    for x in X:
        x1=float(x[0])
        x2=float(x[1])
        blob_dict[str(count)] = (x1,x2)
        count = count + 1
    print X
    print y
    print 'come on plz work'
    return blob_dict, X, y

def generate_circle_sample():

    #X[0] is all the data points(2D), including one big circle, one small circle
    #X[1] is all the labels of the data
    X,y = datasets.make_circles(n_samples=5000, factor=.5, noise=.05)

    circle_dict = {}
    count = 0
    for x in X:
        x1=float(x[0])
        x2=float(x[1])
        circle_dict[str(count)] = (x1,x2)
        count = count + 1

    return circle_dict, X, y


def generate_moon_sample():

    #X[0] is all the data points(2D), including two moon shape
    #X[1] is all the labels of the data
    X,y = datasets.make_moons(n_samples=5000, noise=.05)
    moon_dict = {}
    count = 0
    for x in X:
        x1=float(x[0])
        x2=float(x[1])
        moon_dict[str(count)] = (x1,x2)
        count = count + 1

    return moon_dict, X, y


from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import SpectralClustering
from sklearn.neighbors import kneighbors_graph

def call_kmean(num_cluster, data, update_flag):
    X = StandardScaler().fit_transform(data)
    bandwidth = cluster.estimate_bandwidth(X, quantile=0.3)
    two_means =  MiniBatchKMeans( n_clusters=num_cluster)
    labels = two_means.fit(X).labels_.astype(np.int)

    # if user upload files
    if update_flag:
        return labels


    label_dict = {}
    label_dict_count = 0
    for label in labels:
       label_dict[str(label_dict_count)] = float(label)
       label_dict_count = label_dict_count + 1
    print label_dict

    unique_dict = {}
    unique_dict_count = 0
    for uniq in np.unique(labels):
       print uniq
       unique_dict[str(unique_dict_count)] = float(uniq)
       unique_dict_count = unique_dict_count + 1
    print unique_dict

    return label_dict, unique_dict

def call_affinity(damp, data, update_flag):
    X = StandardScaler().fit_transform(data)
    af = AffinityPropagation(damping=damp,preference=-100).fit(X)
    labels = af.labels_

    if update_flag:
        return labels

    label_dict = {}
    label_dict_count = 0
    for label in labels:
       label_dict[str(label_dict_count)] = float(label)
       label_dict_count = label_dict_count + 1
    print labels
    print label_dict

    unique_dict = {}
    unique_dict_count = 0
    for uniq in np.unique(labels):
       print uniq
       unique_dict[str(unique_dict_count)] = float(uniq)
       unique_dict_count = unique_dict_count + 1
    print uniq
    print unique_dict

    return label_dict, unique_dict

def call_spectral(num_cluster ,mode_, data, update_flag):
    X = StandardScaler().fit_transform(data)
    spectral = SpectralClustering(n_clusters=num_cluster, eigen_solver='arpack', 
                                                        affinity='precomputed')
    connectivity = kneighbors_graph(X, n_neighbors=10)
    connectivity = 0.5 * (connectivity + connectivity.T)
    spectral.fit(connectivity)
    labels = spectral.labels_

    if update_flag:
        return labels


    label_dict = {}
    label_dict_count = 0
    for label in labels:
       label_dict[str(label_dict_count)] = float(label)
       label_dict_count = label_dict_count + 1
    print label_dict

    unique_dict = {}
    unique_dict_count = 0
    for uniq in np.unique(labels):
       print uniq
       unique_dict[str(unique_dict_count)] = float(uniq)
       unique_dict_count = unique_dict_count + 1
    print unique_dict

    return label_dict, unique_dict

def call_greedy(num_cluster , data, update_flag):
    
    S = (euclidean_distances(data))*-1
    N = size(S[0])

    idx, it, netcost = greedyCluster(-S, N, num_cluster, data)

    if update_flag:
        return labels


    label_dict = {}
    label_dict_count = 0
    for label in idx:
       label_dict[str(label_dict_count)] = float(label)
       label_dict_count = label_dict_count + 1
    print label_dict

    unique_dict = {}
    unique_dict_count = 0
    for uniq in np.unique(idx):
       print uniq
       unique_dict[str(unique_dict_count)] = float(uniq)
       unique_dict_count = unique_dict_count + 1
    print unique_dict

    return label_dict, unique_dict