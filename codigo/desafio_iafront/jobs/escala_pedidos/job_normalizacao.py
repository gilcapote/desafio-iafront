import click
from desafio_iafront.data.saving import save_partitioned
from desafio_iafront.jobs.common import prepare_dataframe, transform, prepare_features
import os
from desafio_iafront.jobs.escala_pedidos.constants import LIST_SCALER



@click.command()
@click.option('--visitas-com-conversao', type=click.Path(exists=True))
@click.option('--saida', type=click.Path(exists=False, dir_okay=True, file_okay=False))
@click.option('--data-inicial', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--data-final', type=click.DateTime(formats=["%d/%m/%Y"]))
@click.option('--departamentos', type=str, help="Departamentos separados por virgula")
@click.option('--scaler', type=str, help="Tipo de escalador")


def main(visitas_com_conversao, saida, data_inicial, data_final, departamentos, scaler=None):

    departamentos_lista = [departamento.strip() for departamento in departamentos.split(",")]
    print(departamentos_lista)
    result = prepare_dataframe(departamentos_lista, visitas_com_conversao, data_inicial, data_final)


    # Faz a escala dos valores
    if scaler in LIST_SCALER.keys():
        result = transform(result, LIST_SCALER[scaler])
        saida = os.path.join(saida, scaler)
        print(f"Scaling with {scaler}")

        # salva resultado
        save_partitioned(result, saida, ['data', 'hora'])
        print(f'saved ok')
    elif scaler is None:
        result = prepare_features(result)
        saida = os.path.join(saida, "sem_normalizar")
        print(f"Preparing data without scaling")

        # salva resultado
        save_partitioned(result, saida, ['data', 'hora'])
        print(f'saved ok')
    else:
        print(f"Error: Input correct key or None for original data")


if __name__ == '__main__':
    main()


