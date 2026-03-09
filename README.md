Se asume instalación previa de Python 3.12+ Para instalar el paquete:
Se recomienda utilizar entornos virtuales para instalar el proyecto.
1) Clonar el repositorio: https://github.com/JoseFelixBarbRoj/isi-PeTracker
2) Para usuarios finales: pip install . 
3) Para **desarrolladores** del proyecto: pip install -e .
4) Modificar el archivo config.json con tu usuario y contraseña de MySQLServer.
5) Descargar el dataset de entrenamiento: python /backend/inference/data/populate_data.py  (tarda un poco)
6) Ejecutar: python /backend/inference/data/gen_data_csv para generar el fichero .csv con las particiones del dataset para el modelo
7) (Opcional) Para entrenar el modelo: python backend/inference/train_model.py (recomendado solo con una CUDA GPU)
8) Ejecutar el servidor: python backend/app.py
9) Utilizar cualquier navegador como cliente y acceder al servidor