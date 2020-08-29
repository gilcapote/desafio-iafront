#!/bin/bash

#variables

data_inicial="01/06/2020"
data_final="08/06/2020"
departamentos="perfumaria, artes, esporte_lazer, bebes, utilidades_domesticas, instrumentos_musicais"
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

data=./datasets/dataset-desafio-ia-front
results=../resultados
kmn_path=$results/clusters/$cluster_method/$scaler
db_path=$results/clusters/$cluster_method/$scaler
mink_path=$results/clusters/$cluster_method/$scaler
opt_path=$results/clusters/$cluster_method/$scaler
bi_path=$results/clusters/$cluster_method/$scaler

# clean .html files
rm $results/*.html

#Pipeline

echo "==> Create virtualenv (desafio)"
python -m venv desafio

echo "==> Activate virtualenv (desafio)"
source desafio/bin/activate

echo "==> Install libraries of setup.py on virtualenv"
pip3 install -e .

echo "==> Run job to create the dataset "
## prepara-pedidos --pedidos="datasets\dataset-desafio-ia-front\pedidos" --visitas="datasets\dataset-desafio-ia-front\visitas" --produtos="datasets\dataset-desafio-ia-front\produtos.csv" --saida="results\preparados" --data-inicial="01/06/2020" --data-final="08/06/2020"
python ./desafio_iafront/jobs/pedidos/job.py --pedidos $data/pedidos --visitas $data/visitas --produtos $data/produtos.csv --saida $results/preparados --data-inicial $data_inicial --data-final $data_final

echo "==> Run job to normalize with --scaler parameter"
### normalizar --visitas-com-conversao="results\preparados" --saida="results\escalados" --data-inicial="01/06/2020" --data-final="08/06/2020" --departamentos="perfumaria, artes, esporte_lazer, bebes, utilidades_domesticas, instrumentos_musicais" --scaler="robustscaler"
python ./desafio_iafront/jobs/escala_pedidos/job_normalizacao.py --visitas-com-conversao $results/preparados --saida $results/escalados/$scaler --data-inicial $data_inicial --data-final $data_final --departamentos $departamentos --scaler $scaler

echo "==> Run job to run kmeans clusterization(by clust and by data)"
### kmeans --dataset="results\escalados\scaler_robustscaler" --number_of_cluster=4 --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="results\clusters\robustscaler\kmeans"
python ./desafio_iafront/jobs/clusters/job_kmeans.py --dataset $results/escalados/$scaler --number_of_cluster $number_of_cluster --data-inicial $data_inicial --data-final $data_final --saida $kmn_path

#echo "==> Run job to run other clusters_dbscan"
### dbscan --dataset="results\escalados\scaler_robustscaler" --eps=0.4 --samples=100 --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="results\clusters\robustscaler\dbscan"
#python ./desafio_iafront/jobs/clusters/job_dbscan.py --dataset $results/escalados/$scaler eps $eps samples $samples --data-inicial $data_inicial --data-final $data_final --saida $db_path
#
#echo "==> Run job to run other clusters_birch"
### birch --dataset="results\escalados\scaler_robustscaler" --number_of_cluster=4 --threshold=0.5 --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="results\clusters\robustscaler\birch"
#python ./desafio_iafront/jobs/clusters/job_birch.py --dataset $results/escalados/$scaler --number_of_cluster $number_of_cluster --threshold $threshold --data-inicial $data_inicial --data-final $data_final --saida $bi_path
#
#echo "==> Run job to run other clusters_minibatch_kmeans"
#### minikmeans --dataset="results\escalados\scaler_robustscaler" --number_of_cluster=4 --batch-size=10000 --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="results\clusters\robustscaler\minikmeans"
#python ./desafio_iafront/jobs/clusters/job_minibatch_kmeans.py --dataset $results/escalados/$scaler --number_of_cluster $number_of_cluster --batch-size $batch_size --data-inicial $data_inicial --data-final $data_final --saida $mink_path
#
#echo "==> Run job to run other clusters_optics"
###optics --dataset="results\escalados\scaler_robustscaler" --samples=100 --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="results\clusters\optics\robustscaler"
#python ./desafio_iafront/jobs/clusters/job_optics.py --dataset $results/escalados/$scaler --samples $samples --data-inicial $data_inicial --data-final $data_inicial --saida $opt_path

echo "==> Run job to see graph and histogram before and after transformation"
# graficar --dataframe-path="results\escalados\scaler_robustscaler" --x_axis="longitude" --y_axis="latitude" --cluster_label="convertido" --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="preco_prazo.html"
python ./desafio_iafront/jobs/graphics/job_graphic.py --dataframe-path $results/escalados/$scaler --x_axis longitude  --y_axis latitude --cluster_label convertido --data-inicial $data_inicial --data-final $data_final --saida $results/mapa_convertidos.html
python ./desafio_iafront/jobs/graphics/job_histogram.py --dataframe-path $results/escalados/$scaler --axe frete  --bins $bins --data-inicial $data_inicial --data-final $data_final --saida $results/histograma_frete.html

echo "==> Run job to see dash of normalized scatter combinations and histograms of each variable"
#dash --dataframe-path="..\resultados\escalados" --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="..\resultados\dash_histogram.html" --dash-type="histogram" --cluster-label="convertido" --scaler="robustscaler" --bins=20
python ./desafio_iafront/jobs/graphics/job_dash.py --dataframe-path $results/escalados --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type --saida $results/dash_scatter.html --scaler $scaler --cluster-label convertido
python ./desafio_iafront/jobs/graphics/job_dash.py --dataframe-path $results/escalados --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type2 --saida $results/dash_hist.html --bins $bins --scaler $scaler --cluster-label convertido

echo "==> Run job to see dash of clusterized scatter atribute combinations"
python ./desafio_iafront/jobs/graphics/job_dash.py --dataframe-path $results/clusters/$cluster_method --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type --saida $results/dash_scatter_cluster.html --scaler $scaler --cluster-label cluster_label

echo "==> Run job to see map of clusters scatter"
# clust_map --dataframe-path="..\resultados\clusters" --saida="..\resultados\map_kmeans_robust.html" --data-inicial="01/06/2020" --data-final="08/06/2020" --cluster-method="kmeans" --scaler="robustscaler"
python ./desafio_iafront/jobs/graphics/job_clust_map.py --dataframe-path $results/clusters --data-inicial $data_inicial --data-final $data_final --dash-type $dash_type --saida $results/map_scatter_cluster.html --scaler $scaler --cluster-method $cluster_method


echo "==> Run job to see bargraph of total conversion in data interval"
## conversion --dataframe-path="..\resultados\clusters" --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="..\resultados\conversion.html" --cluster-method="kmeans" --scaler="robustscaler"
python ./desafio_iafront/jobs/graphics/job_convert.py --dataframe-path $results/clusters --data-inicial $data_inicial --data-final $data_final --saida $results/total_conversion.html --cluster-method $cluster_method --scaler $scaler


echo "==> Run job to see graph of total conversion in data interval"
# clust_series --dataframe-path="..\resultados\clusters" --data-inicial="01/06/2020" --data-final="08/06/2020" --saida="..\resultados\serie_timescale_minuto.html" --cluster-method="kmeans" --scaler="robustscaler" --timescale="minuto"
python ./desafio_iafront/jobs/graphics/job_series.py --dataframe-path $results/clusters --data-inicial $data_inicial --data-final $data_final --saida $results/serie_timescale_dia.html --cluster-method $cluster_method --scaler $scaler --timescale $timescale

