import numpy as np
from sklearn.cluster import KMeans, DBSCAN, OPTICS, Birch, MiniBatchKMeans



def kmeans(vector: np.array, n: int):
    k = KMeans(n_clusters=n, init='k-means++', n_init=6)
    cluster_coordinate = k.fit_transform(vector)
    cluster_label = k.fit(vector)
    score = k.score(vector)

    return cluster_coordinate, cluster_label.labels_, cluster_label.inertia_, score

def dbscan(vector: np.array, eps : float, samples: int ):
    k = DBSCAN(eps=eps, min_samples=samples)

    # cluster_coordinate = k.fit_predict(vector)
    cluster_label = k.fit(vector)

    return cluster_label.labels_

def optics(vector: np.array, samples: int ):
    k = OPTICS(min_samples=samples, min_cluster_size=0.05, cluster_method='xi', xi=0.05)

    # cluster_coordinate = k.fit_predict(vector)
    cluster_label = k.fit(vector)

    return cluster_label.labels_


def birch(vector: np.array, n: int, threshold: float):
    k = Birch(n_clusters=n, threshold=threshold)

    cluster_label = k.fit(vector)

    return cluster_label.labels_

def minibatch_kmeans(vector: np.array, n: int, batch_size: int ):
    k = MiniBatchKMeans(n_clusters=n, init='k-means++', batch_size=batch_size)

    cluster_label = k.fit(vector)
    score = k.score(vector)

    return cluster_label.labels_, cluster_label.inertia_, score



 #### need scikit-learn-extra para isto!!!

# def kmedoids(vector: np.array, n: int):
#     k = KMedoids(n_clusters=n, init="k-medoids++", random_state=0)
#
#     cluster_label = k.fit(vector)
#
#     return cluster_label.labels_, cluster_label.inertia_

# from sklearn_extra.cluster import KMedoids