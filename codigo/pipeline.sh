#!/bin/bash

#variables

data_inicial="01/06/2020"
data_final="08/06/2020"
departamentos="perfumaria,artes,esporte_lazer,bebes,utilidades_domesticas,instrumentos_musicais"
scaler="robustscaler"
bins=20
number_of_cluster=4
eps=0.4
samples=50
threshold=0.5
batch_size=10000

## graphics

dash_type="scatter"
dash_type2="histogram"  ## trocar dash_type para "histogram" para ver histogramas
cluster_method="kmeans"
timescale="dia"  # pode ser "hora" ou "minuto"

#variables paths

data=../../data
results=../result_teste
kmn_path=$results/clusters/$cluster_method/$scaler
db_path=$results/clusters/$cluster_method/$scaler
mink_path=$results/clusters/$cluster_method/$scaler
opt_path=$results/clusters/$cluster_method/$scaler
bi_path=$results/clusters/$cluster_method/$scaler

# clean .html files
rm -f $results/*.html

#Pipeline
echo "==> installing virtualenv"
pip3 install virtualenv

echo "==> Create virtualenv (desafio)"
python3 -m virtualenv desafio

echo "==> Activate virtualenv (desafio)"
source desafio/bin/activate

echo "==> Install libraries of setup.py on virtualenv"
pip3 install -e .

echo "==> Run job to create the dataset "

python3 ./desafio_iafront/jobs/pedidos/job.py --pedidos $data/pedidos --visitas $data/visitas --produtos $data/produtos.csv --saida $results/preparados --data-inicial $data_inicial --data-final $data_final

echo "==> Run job to normalize with --scaler parameter"

python3 ./desafio_iafront/jobs/escala_pedidos/job_normalizacao.py --visitas-com-conversao $results/preparados --saida $results/escalados --data-inicial $data_inicial --data-final $data_final --departamentos $departamentos --scaler $scaler

echo "==> Run job to run kmeans clusterization(by clust and by data)"

python3 ./desafio_iafront/jobs/clusters/job_kmeans.py --dataset $results/escalados/$scaler --number_of_cluster $number_of_cluster --data-inicial $data_inicial --data-final $data_final --saida $kmn_path

#echo "==> Run job to run other clusters_dbscan"

#python3 ./desafio_iafront/jobs/clusters/job_dbscan.py --dataset $results/escalados/$scaler eps $eps samples $samples --data-inicial $data_inicial --data-final $data_final --saida $db_path
#
#echo "==> Run job to run other clusters_birch"

#python3 ./desafio_iafront/jobs/clusters/job_birch.py --dataset $results/escalados/$scaler --number_of_cluster $number_of_cluster --threshold $threshold --data-inicial $data_inicial --data-final $data_final --saida $bi_path
#
#echo "==> Run job to run other clusters_minibatch_kmeans"

#python3 ./desafio_iafront/jobs/clusters/job_minibatch_kmeans.py --dataset $results/escalados/$scaler --number_of_cluster $number_of_cluster --batch-size $batch_size --data-inicial $data_inicial --data-final $data_final --saida $mink_path
#
#echo "==> Run job to run other clusters_optics"

#python3 ./desafio_iafront/jobs/clusters/job_optics.py --dataset $results/escalados/$scaler --samples $samples --data-inicial $data_inicial --data-final $data_inicial --saida $opt_path

echo "==> Run job to see graph and histogram before and after transformation"

python3 ./desafio_iafront/jobs/graphics/job_graphic.py --dataframe-path $results/escalados/$scaler --x_axis longitude  --y_axis latitude --cluster_label convertido --data-inicial $data_inicial --data-final $data_final --saida $results/mapa_convertidos.html
python3 ./desafio_iafront/jobs/graphics/job_histogram.py --dataframe-path $results/escalados/$scaler --axe frete  --bins $bins --data-inicial $data_inicial --data-final $data_final --saida $results/histograma_frete.html

echo "==> Run job to see dash of normalized scatter combinations and histograms of each variable"

python3 ./desafio_iafront/jobs/graphics/job_dash.py --dataframe-path $results/escalados --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type --saida $results/dash_scatter.html --scaler $scaler --cluster-label convertido
python3 ./desafio_iafront/jobs/graphics/job_dash.py --dataframe-path $results/escalados --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type2 --saida $results/dash_hist.html --bins $bins --scaler $scaler --cluster-label convertido

echo "==> Run job to see dash of clusterized scatter atribute combinations"
python3 ./desafio_iafront/jobs/graphics/job_dash.py --dataframe-path $results/clusters/$cluster_method --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type --saida $results/dash_scatter_cluster.html --scaler $scaler --cluster-label cluster_label

echo "==> Run job to see map of clusters scatter"

python3 ./desafio_iafront/jobs/graphics/job_clust_map.py --dataframe-path $results/clusters --data-inicial $data_inicial --data-final $data_final --saida $results/map_scatter_cluster.html --scaler $scaler --cluster-method $cluster_method


echo "==> Run job to see bargraph of total conversion in data interval"

python3 ./desafio_iafront/jobs/graphics/job_convert.py --dataframe-path $results/clusters --data-inicial $data_inicial --data-final $data_final --saida $results/total_conversion.html --cluster-method $cluster_method --scaler $scaler


echo "==> Run job to see graph of total conversion in data interval"

python3 ./desafio_iafront/jobs/graphics/job_series.py --dataframe-path $results/clusters --data-inicial $data_inicial --data-final $data_final --saida $results/serie_timescale_dia.html --cluster-method $cluster_method --scaler $scaler --timescale $timescale

