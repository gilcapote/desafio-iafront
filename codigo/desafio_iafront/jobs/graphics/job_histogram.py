import click
from bokeh.io import output_file, save
from functools import partial
from bokeh.layouts import gridplot
import pandas as pd


from desafio_iafront.jobs.graphics.utils import plot_histogram
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.common import filter_date


@click.command()
@click.option('--dataframe-path', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--axe', type=str )
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--bins', type=int, default=4)

def main(dataframe_path: str, saida: str, axe: str, bins: int, data_inicial, data_final):

    filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
    dataframe = read_partitioned_json(dataframe_path, filter_function=filter_function)
    expanded_cols = pd.DataFrame(dataframe["features"].values.tolist(),
                                 columns=["preco_s", "prazo_s", "frete_s", "latitude_s", "longitude_s"])
    dataframe = dataframe.join(expanded_cols)

    output_file(saida)
    p1 = plot_histogram(dataframe, axe, bins, title="Histograma " + axe + "_original")
    p2 = plot_histogram(dataframe, axe + "_s", bins, title="Histograma " + axe + "_escalado")

    figura = gridplot([p1, p2], ncols=2)
    save(figura)

if __name__ == '__main__':
    main()


