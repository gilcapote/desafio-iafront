from functools import partial
import click
import numpy as np
import os

from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.clusters.clusters import optics
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataset', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--samples', type=click.INT)


def main(dataset: str, saida: str, data_inicial, data_final, samples: int):

    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    print(dataset)
    df = read_partitioned_json(file_path=dataset, filter_function=filter_function)
    print(df)

    vector = np.asarray(list(df['features'].to_numpy()))

    labels = optics(vector, samples)

    clust_quantity = set(labels)

    print(clust_quantity)
    print(len(clust_quantity))
    print(f"saving clusters...")

    df['cluster_label'] = list(labels)

    print(f"Saving partitioned by cluster first..")
    save_partitioned(df, os.path.join(saida,"by_cluster"), ['cluster_label', 'data', 'hora'])
    print(f"Saving partitioned by data first..")
    save_partitioned(df, os.path.join(saida,"by_data"), ['data', 'hora', 'cluster_label'])


if __name__ == '__main__':
    main()

