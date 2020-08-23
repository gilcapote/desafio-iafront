import pandas as pd
from bokeh.models import ColumnDataSource
import numpy as np
import os
import itertools
from functools import partial
from bokeh.io import output_file, save
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from desafio_iafront.data.dataframe_utils import read_partitioned_json
from desafio_iafront.jobs.escala_pedidos.constants import LIST_SCALER
from desafio_iafront.jobs.graphics.constants import LIST_AXIS
from desafio_iafront.jobs.common import filter_cluster, filter_date
from bokeh.palettes import Dark2_5 as palette

def plot_scatter(dataframe: pd.DataFrame, x_axis, y_axis, cluster_label, title=""):
    clusters = [label for label in dataframe[cluster_label]]

    colors = [set_color(_) for _ in clusters]

    x = dataframe[x_axis].tolist()
    y = dataframe[y_axis].tolist()
    group = dataframe[cluster_label].astype(str)

    data = {'x_values': x,
            'y_values': y,
            'color': colors,
            'label': group,
            }

    source = ColumnDataSource(data)

    p = figure(title=title)
    # legend field matches the column in the source
    p.scatter(x='x_values', y='y_values', color='color', legend_group='label', source=source)

    p.xaxis.axis_label = x_axis
    p.yaxis.axis_label = y_axis
    p.grid.grid_line_color = "white"
    p.legend.title = cluster_label

    return p


def _unique(original):
    return list(set(original))


def set_color(color):
    COLORS = ["green", "blue", "red", "orange", "purple"]

    index = color % len(COLORS)

    return COLORS[index]


def plot_histogram(dataframe: pd.DataFrame, cluster_label: str, nbins: int, title=" "):
    vector = np.asarray(list(dataframe[cluster_label].to_numpy()))
    hist, edges = np.histogram(vector, density=False, bins=nbins)
    p1 = make_plot(title, hist, edges)
    return p1


def make_plot(title, hist, edges):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5, width = 0.4)
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"
    return p

def dash(dataframe_path: str, data_inicial:str, data_final: str ,saida: str, dash_type:str, cluster_label :str,
         bins:int, scaler: str):

    axis_options = []
    for j in range(len(LIST_AXIS)):
        combinations = [p for p in itertools.combinations(LIST_AXIS, j + 1)]

        for i in range(len(combinations)):
            if len(combinations[i]) == 2:
                axis_options.append(combinations[i])

    output_file(saida)
    figura = []

    if scaler in LIST_SCALER.keys():
        print(os.path.join(dataframe_path, scaler))
        if os.path.isdir(os.path.join(dataframe_path, scaler)):

            path = os.path.join(dataframe_path, scaler)
            filter_function = partial(filter_date, data_inicial=data_inicial, data_final=data_final)
            dataframe = read_partitioned_json(path, filter_function=filter_function)
            expanded_cols = pd.DataFrame(dataframe["features"].values.tolist(),
                                         columns=["preco_s", "prazo_s", "frete_s", "latitude_s", "longitude_s"])
            dataframe = dataframe.join(expanded_cols)
            if cluster_label == 'cluster_label':
                dataframe['cluster_label'] = dataframe['cluster_label'].astype(int)
            # print(dataframe.describe())

            if dash_type == "scatter":
                for axis in axis_options:
                    p = plot_scatter(dataframe, axis[0] + "_s", axis[1] + "_s", cluster_label,
                                     title="Scatter of " + scaler + "_" + axis[0] + "_vs_" + axis[1])
                    figura.append(p)
            elif dash_type == "histogram":
                for axe in LIST_AXIS:
                    p = plot_histogram(dataframe, axe, bins, title="Histograma " + axe)
                    figura.append(p)
            else:
                print(f"Erro: Opcoes possiveis: 'scatter' ou 'histogram'")

    figs = gridplot(figura, ncols=len(LIST_AXIS))
    save(figs)

def plot_series(dataframe_path, data_inicial: str, data_final: str, cluster_method: str, scaler: str, timescale: str,title :str):
    def filter_data_cluster(row):
        return filter_date(row, data_inicial, data_final) and filter_cluster(row)

    if scaler in LIST_SCALER.keys():
        if os.path.isdir(os.path.join(dataframe_path, cluster_method, scaler, "by_data")):
            path = os.path.join(dataframe_path, cluster_method, scaler, "by_data")

            dataframe = read_partitioned_json(path, filter_function=filter_data_cluster)
            dataframe["cluster_label"] = dataframe["cluster_label"].astype(int)


    dataframe['dia'] = [d.split(" ")[0].split("-")[-1] for d in dataframe["datahora"]]
    dataframe['hora']  = [d.split(" ")[-1].split(":")[0] for d in dataframe["datahora"]]
    dataframe['minuto'] = [d.split(" ")[-1].split(":")[1] for d in dataframe["datahora"]]
    print(dataframe['dia'].unique())

    n_cluster = sorted(dataframe['cluster_label'].unique())
    print(n_cluster)

    TOOLS = 'crosshair,save,pan,box_zoom,reset,wheel_zoom'
    p = figure(title=title, y_axis_type="linear", tools=TOOLS)
    colors = itertools.cycle(palette)

    for n, color in zip(n_cluster, colors):

        x_axis = sorted(dataframe[timescale].unique())
        df_1 = dataframe[(dataframe['cluster_label']==n) & (dataframe['convertido']==1)].groupby(by=[timescale]).count().sort_values(by=timescale)
        df_0 = dataframe[(dataframe['cluster_label']==n)].groupby(by=[timescale]).count().sort_values(by=timescale)
        cv = df_1["convertido"]/df_0["convertido"]
        print(x_axis, cv)

        p.line(x_axis, cv, legend_label=str(n), color=palette[n], line_width=3)
        p.legend.location = "top_left"
        p.xaxis.axis_label = timescale
        p.yaxis.axis_label = 'Conversao'

    return p

def plot_map(dataframe_path: str, data_inicial: str, data_final: str, cluster_method: str, scaler: str):
    def filter_cluster_data(row):
        return filter_cluster(row) and filter_date(row, data_inicial, data_final)

    if scaler in LIST_SCALER.keys():
        if os.path.isdir(os.path.join(dataframe_path, cluster_method, scaler, "by_cluster")):
            path = os.path.join(dataframe_path, cluster_method, scaler, "by_cluster")

            dataframe = read_partitioned_json(path, filter_function=filter_cluster_data)
            dataframe["cluster_label"] = dataframe["cluster_label"].astype(int)

            p = plot_scatter(dataframe, "longitude", "latitude", "cluster_label",
                             title="Map_clusters_"+ cluster_method + "_method_" + scaler +"_data")

            return p


def plot_conv(dataframe_path, data_inicial: str, data_final: str, cluster_method: str, scaler: str, title :str):
    def filter_data_cluster(row):
        return filter_date(row, data_inicial, data_final) and filter_cluster(row)

    if scaler in LIST_SCALER.keys():
        if os.path.isdir(os.path.join(dataframe_path, cluster_method, scaler, "by_data")):
            path = os.path.join(dataframe_path, cluster_method, scaler, "by_data")

            dataframe = read_partitioned_json(path, filter_function=filter_data_cluster)
            dataframe["cluster_label"] = dataframe["cluster_label"].astype(int)


    p = figure(y_range=(0.16, 0.20))
    colors = itertools.cycle(palette)

    n_cluster = sorted(dataframe['cluster_label'].unique())
    print(n_cluster)

    for n, color in zip(n_cluster, colors):

        df_1 = dataframe[(dataframe['cluster_label']==n) & (dataframe['convertido']==1)].count()
        df_0 = dataframe[(dataframe['cluster_label']==n)].count()

        data = df_1["convertido"]/df_0["convertido"]
        print(data)

        p.vbar(x=n_cluster, top=data, width=0.8)

    return p


