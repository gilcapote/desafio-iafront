import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, OPTICS, Birch



def kmeans(vector: np.array, n: int):
    k = KMeans(n_clusters=n, random_state=0)
    cluster_coordinate = k.fit_transform(vector)
    cluster_label = k.fit(vector)

    return cluster_coordinate, cluster_label.labels_, cluster_label.inertia_   #adding inertia parameter

def dbscan(vector: np.array, eps : float, samples: int ):
    k = DBSCAN(eps=eps, min_samples=samples)

    # cluster_coordinate = k.fit_predict(vector)
    cluster_label = k.fit(vector)

    return cluster_label.labels_

def optics(vector: np.array, samples: int ):
    k = OPTICS(min_samples=samples, min_cluster_size=0.1)

    # cluster_coordinate = k.fit_predict(vector)
    cluster_label = k.fit(vector)

    return cluster_label.labels_

def agglomerativeclustering(vector: np.array, n: int):
    k = AgglomerativeClustering(n_clusters=n, linkage='ward')

    cluster_label = k.fit(vector)

    return cluster_label.labels_

def birch(vector: np.array, n: int, threshold: float):
    k = Birch(n_clusters=n, threshold=threshold)

    cluster_label = k.fit(vector)

    return cluster_label.labels_




 #### need scikit-learn-extra para isto!!!

# def kmedoids(vector: np.array, n: int):
#     k = KMedoids(n_clusters=n, init="k-medoids++", random_state=0)
#
#     cluster_label = k.fit(vector)
#
#     return cluster_label.labels_, cluster_label.inertia_

# from sklearn_extra.cluster import KMedoids