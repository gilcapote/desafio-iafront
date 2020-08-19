from setuptools import setup, find_packages

setup(
    name='desafio_iafront',
    version='0.0.3',
    packages=find_packages(),
    url='',
    license='LICENSE',
    author='Time IA-FRONT',
    author_email='gilcapote85@gmail.com',
    description='',
    install_requires=[
        "scikit-learn==0.23.1",
        "click==7.1.2",
        "bokeh==2.1.1",
        "dataset-loader==1.6",
        'pandas==1.1.0',
        'numpy==1.19.1'
    ],
    entry_points={
        'console_scripts': [
            'prepara-pedidos = desafio_iafront.jobs.pedidos.job:main',
            'normalizar = desafio_iafront.jobs.escala_pedidos.job_normalizacao:main',
            'kmeans = desafio_iafront.jobs.clusters.job_kmeans:main',
            'agglomerative = desafio_iafront.jobs.clusters.job_agglomerative:main',
            'dbscan = desafio_iafront.jobs.clusters.job_dbscan:main',
            'optics = desafio_iafront.jobs.clusters.job_optics:main',
            'birch = desafio_iafront.jobs.clusters.job_birch:main']
    }
)


# 'cria-visitas=desafio_iafront.jobs.create_visits:main'

# 'escala-normalizer = desafio_iafront.jobs.escala_pedidos.job_normalizacao:main',
#             'escala-minmaxscaler = desafio_iafront.jobs.escala_pedidos.job_minmaxscaler:main',
#             'escala-standardscaler = desafio_iafront.jobs.escala_pedidos.job_standardscaler:main',
#             'escala-maxabsscaler = desafio_iafront.jobs.escala_pedidos.job_maxabsscaler:main',
#             'escala-robustscaler = desafio_iafront.jobs.escala_pedidos.job_robustscaler:main',
#             'escala-powertransformer = desafio_iafront.jobs.escala_pedidos.job_powertransformer:main',
#             'cria-sem-escalar = desafio_iafront.jobs.escala_pedidos.job_sem_normalizar:main',
#             'kmeans = desafio_iafront.jobs.clusters.job_kmeans_mio:main',
#             'graphics = desafio_iafront.jobs.graphics.job_graphics_mio:main'