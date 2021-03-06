import click

from desafio_iafront.jobs.graphics.utils import plot_map
from bokeh.io import output_file, save


@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--cluster-method', type=str)
@click.option('--scaler', type=str)


def main(dataframe_path: str, saida: str, data_inicial, data_final, cluster_method: str, scaler: str ):
    output_file(saida)

    fig = plot_map(dataframe_path, data_inicial, data_final, cluster_method, scaler)

    save(fig)


if __name__ == '__main__':
    main()


