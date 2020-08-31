#!/bin/bash

#variables

data_inicial="01/06/2020"
data_final="08/06/2020"
departamentos="perfumaria,artes,esporte_lazer,bebes,utilidades_domesticas,instrumentos_musicais"
scaler="robustscaler"
bins=20
number_of_cluster=4
eps=0.5
samples=50
threshold=0.5
batch_size=10000

## graphics

dash_type="scatter"
dash_type2="histogram"   ## trocar dash_type para "histogram" para ver histogramas
axe_hist="frete"	  ## Atributo para histogram antes e depois
cluster_method="kmeans"  ## Cluster para o qual gerar graficos("kmeans", "birch","minikmeans", "optics", "dbscan") 
timescale="hora"  	  ## Escala:pode ser "dia", "hora" ou "minuto"

# paths

data=../../data
results=../result_teste

kmn_path=$results/clusters/kmeans/$scaler
db_path=$results/clusters/dbscan/$scaler
mink_path=$results/clusters/minikmeans/$scaler
opt_path=$results/clusters/optics/$scaler
bi_path=$results/clusters/birch/$scaler

