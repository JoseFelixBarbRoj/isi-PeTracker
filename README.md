Se asume instalación previa de Python 3.12+ Para instalar el paquete:
Se recomienda utilizar entornos virtuales para instalar el proyecto.
1) Clonar el repositorio: https://github.com/JoseFelixBarbRoj/isi-PeTracker
2) Instalar dependencias:
    a) Para usuarios finales: pip install . 
    b) Para **desarrolladores** del proyecto: pip install -e .
3) Modificar el archivo config.json con tu usuario y contraseña de MySQLServer, así como la secret key que desees utilizar.
4) Descargar el archivo **best.pth** correspondiente al modelo (disponible en releases: https://github.com/JoseFelixBarbRoj/isi-PeTracker/releases/tag/0.1.0 ) en **backend/inference/models**.
5) Ejecutar el servidor: python backend/app.py
6) Utilizar cualquier navegador como cliente y acceder al servidor.
**Opcional** Para entrenar el modelo:
-Descargar el dataset de entrenamiento: python /backend/inference/data/populate_data.py  (tarda un poco).
-Ejecutar python /backend/inference/data/gen_data_csv.py para generar el fichero .csv con las particiones del dataset para el modelo.
-Entrenar el modelo ejecutando python /backend/inference/train_model.py (se recomienda disponer de una GPU NVIDIA)
