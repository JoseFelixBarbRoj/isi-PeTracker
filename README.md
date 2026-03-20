Se asume instalación previa de Python 3.12+ Para instalar el paquete:
Se recomienda utilizar entornos virtuales para instalar el proyecto.
1) Clonar el repositorio: https://github.com/JoseFelixBarbRoj/isi-PeTracker
2) Instalar dependencias:
    a) Para usuarios finales: `pip install . `
    b) Para **desarrolladores** del proyecto: `pip install -e .`
3) Descargar los assets del proyecto tanto del front-end como del back-end (como el modelo de IA) utilizando el script `project_setup.py`. El siguiente comando descarga los assets necesarios: `python project_setup.py`
4) Ejecutar `docker compose up`
5) Ejecutar el servidor: `python backend/app.py`
6) Utilizar cualquier navegador como cliente y acceder al servidor.
7) Para ejecutar los tests: `make test`
   
**Opcional** Para entrenar el modelo:

-Descargar el dataset de entrenamiento: `python /backend/inference/data/populate_data.py`  (tarda aproximadamente 15-20m).

-Ejecutar `python /backend/inference/data/gen_data_csv.py` para generar el fichero CSV con las particiones del dataset para el modelo.

-Entrenar el modelo ejecutando `python /backend/inference/train_model.py` (se recomienda disponer de una GPU NVIDIA)

