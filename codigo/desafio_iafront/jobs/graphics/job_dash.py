import click

from desafio_iafront.jobs.graphics.utils import dash
from bokeh.io import output_file, save


@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--dash-type', type=str)
@click.option('--scaler', type=str)
@click.option('--cluster-label', type=str, default="convertido")
@click.option('--bins', type=int, default=4)


def main(dataframe_path: str, saida: str, data_inicial, data_final, dash_type: str, bins: int, cluster_label:str, scaler:str):
    output_file(saida)

    figura = dash(dataframe_path, data_inicial, data_final, dash_type, cluster_label, bins, scaler)

    save(figura)

if __name__ == '__main__':
    main()



