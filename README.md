Se asume instalación previa de Python 3.12+ Para instalar el paquete:
Se recomienda utilizar **entornos virtuales** para instalar el proyecto.
1) Clonar el repositorio: https://github.com/JoseFelixBarbRoj/isi-PeTracker
2) Ejecutar `docker compose up`. Si previamente has instalado estos volúmenes, o quieres tener los más actualizados, antes ejecuta: `docker compose down -v``. *Importante:**  Si este proceso falla, es debido a un error esporádico que experimenta la API de los gatos (https://api.thecatapi.com/). Basta con reintentar.
3) Utilizar cualquier navegador como cliente y acceder al servidor.

    Datos para el login:
    | **Usuario**       | **Contraseña** | **Tipo de usuario**|
    |-------------------|---------------|---------------------|
    | **carlos**        | **1234**      | **dueño**           |
    | **juan**          | **abcd**      | **dueño**           |
    | **maria**         | **5678**      | **dueño**           |
    | **huellas**       | **4321**      | **protectora**      |
    | **patas_felices** | **9876**      | **protectora**      |


Los **tests** se ejecutarán automáticamente una vez acabada la instalación de dependencias,  descarga de assets (como el modelo de IA usado por el servidor) y recopilación de los datos de las APIs empleadas.
   
**Opcional** Para entrenar el modelo:

-Ejecutar `python /backend/inference/data/gen_data_csv.py` para generar el fichero CSV con las particiones del dataset para el modelo.

-Entrenar el modelo ejecutando `python /backend/inference/train_model.py` (se recomienda disponer de una GPU NVIDIA)

