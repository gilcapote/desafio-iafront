import click
from bokeh.io import output_file, save
from functools import partial


from desafio_iafront.jobs.graphics.utils import plot
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--x_axis')
@click.option('--y_axis')
@click.option('--cluster_label')
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))

def main(dataframe_path: str, saida: str, x_axis, y_axis, cluster_label, data_inicial, data_final):

    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)

    output_file(saida)

    figura = plot(dataframe, x_axis, y_axis, cluster_label)

    save(figura)


if __name__ == '__main__':
    main()
