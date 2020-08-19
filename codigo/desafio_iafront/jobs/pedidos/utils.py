import os
import pandas as pd

from desafio_iafront.data.dataframe_utils import read_partitioned_json, join_datasets,keep_columns, rename_columns
from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.pedidos.contants import KEPT_COLUNS, COLUMN_RENAMES, SAVING_PARTITIONS, ENCODE_COLUMNS
from desafio_iafront.jobs.contants import COLUNA_DEPARTAMENTO


def _prepare(pedidos_joined: pd.DataFrame) -> pd.DataFrame:
    # Remove colunas resultantes do merge
    result_dataset = drop_merged_columns(pedidos_joined)
    # Remove colunas que não serão usadas
    result_dataset = result_dataset[KEPT_COLUNS]
    # Renomeia colunas
    result_dataset = result_dataset.rename(columns=COLUMN_RENAMES)

    return result_dataset


def drop_merged_columns(data_frame: pd.DataFrame) -> pd.DataFrame:
    result_dataset = data_frame.copy(deep=True)
    for column in data_frame.columns:
        if column.endswith("_off"):
            result_dataset = data_frame.drop(column, axis=1)
    return result_dataset


def save_prepared(saida: str, dataframe: pd.DataFrame):
    # extracting time and hour from timestamp
    save_partitioned(dataframe, saida, SAVING_PARTITIONS)


def merge_visita_produto(data_str: str, hour: int, pedidos_df: pd.DataFrame, produtos_df: pd.DataFrame, \
                         visitas_df:pd.DataFrame) -> pd.DataFrame:
    df_joint_visita_produto = join_datasets('product_id', 'inner', visitas_df, produtos_df)

    df_joint_visita_produto_pedido = df_joint_visita_produto.merge(pedidos_df, how="left",
                                                                            on="visit_id", suffixes=("", "_off"))
    df_joint_visita_produto_pedido["data"] = data_str
    df_joint_visita_produto_pedido["hora"] = hour

    return df_joint_visita_produto_pedido


def clean_and_prepare(df_to_be_cleaned: pd.DataFrame):
    # Remove colunas que não serão usadas e rearranja
    removed = keep_columns(df_to_be_cleaned, KEPT_COLUNS)
    # Renomeia colunas
    visita_com_produto_pedido_cleaned = rename_columns(removed, COLUMN_RENAMES)

    return visita_com_produto_pedido_cleaned


def create_pedidos_df(date_partition: str, hour_snnipet: str, pedidos: str) -> pd.DataFrame:
    path = os.path.join(os.path.join(pedidos, date_partition), hour_snnipet)
    pedidos_df = read_partitioned_json(path)
    pedidos_df["visit_id"] = pedidos_df["visit_id"].astype(str)
    # pedidos_partition = os.path.join(pedidos, date_partition, hour_snnipet)
    # pedidos_df = read_partitioned_json(pedidos_partition)
    # pedidos_df["visit_id"] = pedidos_df["visit_id"].astype(str)

    return pedidos_df


def create_visitas_df(date_partition: str, hour_snnipet: str, visitas: str) -> pd.DataFrame:
    path = os.path.join(os.path.join(visitas, date_partition), hour_snnipet)
    visitas_df = read_partitioned_json(path)
    visitas_df["product_id"] = visitas_df["product_id"].astype(str)
    visitas_df["visit_id"] = visitas_df["visit_id"].astype(str)

    return visitas_df


def prepare_files(data_str: str, hour: int, pedidos: str, produtos_df: pd.DataFrame, saida: str,
                        visitas: str) -> pd.DataFrame:
    date_partition = f"data={data_str}"
    hour_snnipet = f"hora={hour}"

    visitas_df = create_visitas_df(date_partition, hour_snnipet, visitas)

    pedidos_df = create_pedidos_df(date_partition, hour_snnipet, pedidos)

    visita_com_produto_pedido_df = merge_visita_produto(data_str, hour, pedidos_df, produtos_df,
                                                        visitas_df)
    visita_com_produto_pedido_cleaned = clean_and_prepare(visita_com_produto_pedido_df)

    write_depts(visita_com_produto_pedido_cleaned, COLUNA_DEPARTAMENTO)

    save_prepared(saida, visita_com_produto_pedido_cleaned)

    print(f"Concluído para {date_partition} {hour}h")


def write_depts(dataframe : pd.DataFrame, coluna : str):
    listadepts = list(dataframe[coluna].unique())
    with open("deptos.py", "w") as outfile:
        outfile.write("\n".join(str(item) for item in listadepts))
    return F'deptos.py writed \n'
