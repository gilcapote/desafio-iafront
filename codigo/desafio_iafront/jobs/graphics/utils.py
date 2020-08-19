import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import numpy as np
from desafio_iafront.jobs.graphics.constants import AXES

# from bokeh.io import output_file, show
# from bokeh.plotting import figure

#
from numpy import histogram, linspace
from scipy.stats.kde import gaussian_kde



def plot(dataframe: pd.DataFrame, x_axis, y_axis, cluster_label, title=""):
    clusters = [label for label in dataframe[cluster_label]]

    colors = [set_color(_) for _ in clusters]

    x = dataframe[x_axis].tolist()
    y = dataframe[y_axis].tolist()
    group = dataframe[cluster_label].astype(str)

    data = {'x_values': x,
            'y_values': y,
            'color': colors,
            'label': group}

    source = ColumnDataSource(data)

    p = figure(title=title)
    # legend field matches the column in the source
    p.scatter(x='x_values', y='y_values', color='color', legend_group='label', source=source)

    # p.scatter(dataframe[x_axis].tolist(), dataframe[y_axis].tolist(),fill_color=colors, legend_field = cluster_label)
    p.xaxis.axis_label = 'longitude'
    p.yaxis.axis_label = 'latitude'
    p.grid.grid_line_color = "white"
    p.legend.title = 'Clusters'

    return p


def _unique(original):
    return list(set(original))


def set_color(color):
    COLORS = ["green", "blue", "red", "orange", "purple"]

    index = color % len(COLORS)

    return COLORS[index]



# def plot_histogram(dataframe: pd.DataFrame, nbins: int, title=""):
#     linha = gaussian_kde(dataframe)
#     x = linspace(0, 250, 200)
#
#     p = figure(title= title)
#     p.line(x, linha(x))
#
#     # plot actual hist for comparison
#     hist, edges = histogram(dataframe, density=True, bins=nbins)
#     p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], alpha=0.4)
#
#     return p


def plot_histogram(dataframe: pd.DataFrame, cluster_label: str, nbins: int, title=" "):
    hist, edges = np.histogram(dataframe[cluster_label], density=False, bins=nbins)

    # clusters = [label for label in dataframe[cluster_label]]
    #
    # colors = [set_color(_) for _ in clusters]
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="navy", line_color="white", alpha=0.5, width = 0.6)

    p.xaxis.axis_label = 'Clusters'
    p.yaxis.axis_label = 'Frequencia'
    p.grid.grid_line_color = "white"
    return p