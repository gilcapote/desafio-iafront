## Analise

Partindo do problema solicitado (Associando visitas a pedidos), o codigo foi colocado no arquivo `pedidos/job.py`. 

As funções a criar (_create_pedidos_df_, _create_visitas_df_, _merge_visita_produto_, _save_prepared_), foram colocadas
 no arquivo `jobs/pedidos/utils.py`. 
 
 Foram descartados varios atributos que nao aportam informaçao à analise, tais como as dimensoes do produto e 
 comprimentos do nome e da descrição do produto. As colunas separadas para analise foram selecionadas mediante a lista 
 **KEPT_COLUNS** e os novos nomes das colunas foram introduzidos usando o diccionario **COLUMN_RENAMES**, ambos sendo 
 encontrados no arquivo `jobs/pedidos/contants.py`
  
 O método (_prepare_files_) que faz uso de todas as funçoes anteriores também foi colocado no arquivo anterior
 (_utils.py_). O codigo fica da seguinte forma:
 
  ```Python
def prepare_files(data_str: str, hour: int, pedidos: str, produtos_df: pd.DataFrame, saida: str,
                        visitas: str) -> pd.DataFrame:
    date_partition = f"data={data_str}"
    hour_snnipet = f"hora={hour}"

    visitas_df = create_visitas_df(date_partition, hour_snnipet, visitas)

    pedidos_df = create_pedidos_df(date_partition, hour_snnipet, pedidos)

    visita_com_produto_pedido_df = merge_visita_produto(data_str, hour, pedidos_df, produtos_df,
                                                        visitas_df)
    visita_com_produto_pedido_cleaned = _prepare(visita_com_produto_pedido_df)

    write_depts(visita_com_produto_pedido_cleaned, COLUNA_DEPARTAMENTO)

    save_prepared(saida, visita_com_produto_pedido_cleaned)

    print(f"Concluído para {date_partition} {hour}h")

```


  
 ## Scale de dados
Com os dados preparados, fico com os atributos:

_{"id_produto", "id_visita", "id_pedido", "datahora", "prazo", "preco", "frete", "coordenadas"}_

Ainda assim, e para o nosso analise, são consideradas somente os atributos 
_'preco', 'prazo' e 'frete'_. O atributo _"coordenadas"_ é dividido em colunas para _'latitude'_ e _'longitude'_ e istos
 sao adicionados à analise. Neste ponto tambem é criada a coluna 'convertido', que toma valores binarios quando uma visita resulta em uma 
compra(1) ou nao(0).

Nosso proximo passo é conseguir normalizar os dados e preparar os arrays para a clusterizacao que será realizada.
O job criado para o caso fica localizado em `jobs/escala_pedidos/job_normalizaçao.py`. 

Com o fim de simplificar o codigo, adiciono o argumento **--scaler** , um string que serve de chave no diccionario 
**LIST_SCALER**, presente no arquivo `jobs/escala_pedidos/constants.py`

 _**@click.option('--scaler', type=str, help="Tipo de escalador")**_

_LIST_SCALER = {'normalizer': Normalizer(), 'minmaxscaler': MinMaxScaler(), 'standardscaler': StandardScaler(),
          'maxabsscaler': MaxAbsScaler(), 'robustscaler': RobustScaler(), 'powertransformer': PowerTransformer(),
               'sem_normalizar': None}_
               
Com isto, é possivel escolher qual tecnica de normalizaçao será usada apartir de um string e assignar o objeto certo.

  
Desta forma todos os parametros necessarios sao passados. Para escalar os dados, executo o arquivo 
`jobs/pedidos/utils.py`. Na analise, usei os dados de 6 departamentos escolhidos mediante o argumento **--departamentos**:

_("perfumaria, artes, esporte_lazer, bebes, utilidades_domesticas, instrumentos_musicais")_

Num momento seguinte geramos os dois graficos scatter para analisar as mudanças ocorridas pela transformaçoes realizadas em 
cada um dos casos (`jobs/graphics/job_graphic.py`), assim como histogramas de cada atributo no mesmo caso(`jobs/graphics/job_histogram.py`).  

Idealmente para clusterizaçao precisamos de dados padronizados de forma que a distribuiçao original seja mantida 
e a variança seja unitaria ou similar para todos os atributos. Usualmente tecnicas de padronizaçao estao otimizadas para 
distribuicoes gaussianas, então deveria funcionar melhor nesses casos.  
Olhando os histogramas de cada atributo, é possivel observar o efeito de cada uma das transformaçoes realizadas. 

Transformaçoes do tipo power transformer e normalizer modificam de forma significativa a distribuiçao dos dados , 
pelo qual nao deveriam ser consideradas neste caso.  

Das outras transformaçoes consideradas, neste caso é mais interesante pensar em aquelas que ficam com os dados
centralizados em 0. Dessas duas ultimas, robustscaler e standardscaler, o robustscaler deveria apresentar melhor
comportamento na presenca de outliers, devido ao uso da mediana em vez da media e do uso do intervalo entre quartis 
como o rango de valores para o qual realizar a transformaçao. Isto permite eliminar efeitos provocados por outliers
na distribuiçao dos dados.

As transformaçoes mais promissoras escolhidas para a analise posterior foram robustscaler, standardscaler e minmaxscaler. 
  

### Gerando clusters

Com os dados devidamente escalados é possivel gerar entao os dados particionados por `cluster_label`, `data` e `hora` 
e tambem por  `data`, `hora` e `cluster_label`, modificando a entrada da funçao **save_partitioned** , localizada em `data/saving.py`.

Além do job para kmeans(`clusters/job_kmeans.py`), foram implementadas mais 4 jobs para implementar cada um das tecnicas de clusterizaçao escolhidas:

* MiniBatchKMeans(`job_minibatch_kmeans.py`)
* DBSCAN(`job_dbscan.py`)
* OPTICS(`job_optics.py`)
* Birch(`job_birch.py`)

Para a escolha, tentei colocar tecnicas de clusterizaçao que tenham metodos de natureza diferente e que sejam escalaveis para grandes quantidades de dados.
No caso do kmeans e o MiniBatchKMeans, sao baseados em distancias de acordo com a metrica escolhida(euclideana, manhattan). 
Já no caso de DBSCAN e OPTICS, usam uma estrategia de densidade e pontos proximos dentro de um radio definido. 
O caso de Birch é um metodo de aglomeracao que usa um esquema de arvore para agrupar instancias em nós que vao crescendo e formando os clusters numa estrategia bottom-up.
A maior vantagem é deste ultimo é que só precisa varrer o conjunto de dados em uma única passagem para realizar o clustering.
 
Cada um deles apresenta uma serie de parametros que modificam a forma em que os clusters sao calculados. 

Tambem foi criado um job que cria scatters ou histogramas(dependendo do argumento passado), que graficam todas as possiveis 
combinacoes duais entre a lista dos atributos que estejam sendo analisados. Neste caso, nosso job(`jobs/graphics/job_dash.py`) 
cria 3 graficos de scatter ou histogramas com todas as possiveis combinaçoes de frete, preço e prazo. 

De todas as combinacoes possiveis de escalador e clusterizaçao, decidi escolher aquela com o robustscaler como transformador e o kmeans como tecnica de clusterizaçao. 
Esta tecnica precisa ser introduzido o numero de clusters. Realizei varias corridas para diferentes numeros de clusters, e decidi usar 4 clusters. Para obter este 
parametro rodei a analise para numero de clusters de 1 até 10, percebendo que apartir de 3 o 4, a adicao de mais clusters nao aporta informacao relevante. 

Dada a natureza espacial dos dados de coordenadas, assim como a dependencia de outros atributos analisados da localizacao(prazo, frete), pensamos que
 o numero e a localizacao dos clusters devem ser estudados. Explorando esta ideia, grafiquei um mapa das coordenadas espaciais usando o cluster 
 label como agrupador e é claramente percibido que os clusters achados na clusterizacao correspondem às 4 regioes mais habitadas 
 do pais(suleste, nordeste, sul e centroeste). A regiao norte apresenta dados mais dispersos, o que dificulta a sua identificaçao. 
 
 Para desenhar os mapas de uma forma mais direta, criamos um job() que grafica agrupando por cluster label. 
 
 <img src="codigo/desafio_iafront/mapa.jpg">
 
 
 Estos resultados parecem ter muito sentido, dados os regimes diferentes de envio que existem usualmente para as diferentes regioes do pais, 
 incluindo prazos e fretes diferentes. A unica coluna que nao tem uma dependencia espacial é o preço do produto. 
 
 O nosso antigo **job_dash.py** permite tambem criar os novos graficos para comparar a distribuicao dos pontos com repeito aos clusters , 
 neste caso trocando o _"cluster_label"_ como agrupador (em vez da coluna _"convertidos"_). 
 
 Foi criado tambem um job que gera gráficos comparando a conversão total media de cada cluster para uma janela de data de entrada (`jobs/graphics/job_convert.py`).
  
O job final calcula a conversão agregada em uma escala recebida como parâmetro('dia','hora' e 'minuto')  e cria gráficos com séries temporais na escala digitada.
(`jobs/graphics/job_series.py`) 

Como conclusao temos que  cluster correspondente à regiao norte foi muito dificil de analisar (para os departamentos que realizamos a analise)
 pela esparsidade dos dados ao longo de vastos territorios.

Nas duas semanas analisadas(01/06-15/06), o cluster correspondente à regiao sul se mostrou com uma conversao acima da media das outras regioes 
 para as evoluçoes diarias e horarias. 
 
 Por outro lado, o cluster correspondente à regiao suleste apresentou um numero muito superior de visitas 
 totais(maior do que a soma dos outro tres clusters) e apresentou tambem a conversao mais baixa das 4 regioes. Isto sugere a existencia de 
 maior potencial nesta regiao, pelo qual eu recomendaria realizar maiores investimentos nela para ampliar a conversão. 
 
 Um fenomeno temporal observado que vale a pena mencionar foi que para as duas semanas estudadas, o horario de final da tarde(17-20 horas)
 parece ser um horario de queda no parametro de conversao. 
 
 
  







