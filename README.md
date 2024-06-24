# ETL_con_API_Publica
Proyecto sencillo en FastAPI para extraer datos de una API pública.

**Descripción del Proyecto: Plataforma de Análisis de Datos del Anime Naruto**

Este proyecto se centra en el desarrollo de una plataforma web para el análisis y la extracción de datos del popular anime "Naruto". Consta de tres aplicaciones principales implementadas como microservicios, cada una cumpliendo un rol específico en el procesamiento y entrega de información:

1. **Extract-Service:** Este servicio se encarga de extraer datos de una API externa que contiene información extensa sobre personajes del anime "Naruto". Utiliza la API pública proporcionada por narutodb.xyz para acceder a datos detallados como habilidades, afiliaciones y más, facilitando una recopilación exhaustiva de información.
    
2. **Transform-Service:** El servicio de transformación toma los datos extraídos por Extract-Service y realiza un filtrado y procesamiento específico. Se enfoca en identificar y seleccionar los personajes principales del anime, agrupándolos por clanes y categorizando los ninjas más destacados. Esta fase de transformación permite optimizar la información para su análisis y posterior consumo.
    
3. **Load-Service:** Finalmente, Load-Service proporciona una interfaz para que los usuarios descarguen los datos procesados en formato CSV. Este servicio permite a los usuarios obtener fácilmente la lista filtrada de los ninjas principales, organizada por clanes, facilitando su uso en análisis posteriores o integración con otras herramientas.

Estructura del proyecto en local:
```bash
├── LICENSE
├── README.md
├── __init__.py
├── docker-compose.yml
├── extract-service
│   ├── Dockerfile  
│   ├── __init__.py
│   ├── app.py
│   ├── environment.py
│   └── requirements.txt
├── load-service
│   ├── Dockerfile   
│   ├── __init__.py
│   ├── app.py
│   ├── environment.py
│   └── requirements.txt
├── transform-service
│   ├── Dockerfile
│   ├── __init__.py
│   ├── app.py
│   ├── constants.py
│   ├── environment.py
│   └── requirements.txt
```

En producción se agrega:

```bash
├── deploy
│   └── prod
│       ├── Dockerfile_extract
│       ├── Dockerfile_load
│       ├── Dockerfile_transform
│       ├── cloudbuild_extract.yaml
│       ├── cloudbuild_load.yaml
│       └── cloudbuild_transform.yaml
├── deploy.sh
```


**Microservicios:**

- **extract-service:** Servicio encargado de extraer datos.
- **transform-service:** Servicio encargado de transformar datos.
- **load-service:** Servicio encargado de cargar datos.

**Comunicación entre Servicios:**

- Los servicios se comunican entre sí a través de una red Docker interna (`my-network` en el entorno de desarrollo y comunicación directa en producción usando URLs específicas).

**Empaquetado con Docker:**

- Cada servicio está empaquetado en un contenedor Docker individual para el despliegue local dentro de cada app independiente.
- En producción se tienen Dockerfiles específicos para cada servicio (`Dockerfile_extract`, `Dockerfile_transform`, `Dockerfile_load`).

**Despliegue en Servidor:**

- En desarrollo local, se utiliza un `docker-compose.yml` para orquestar los servicios y facilitar la comunicación:
```bash
	 docker-compose up -d --build
```
- En producción, se utiliza Google Cloud Run para desplegar cada servicio de manera independiente a través de Cloud Build.

Hay un manejador en el archivo `deploy.sh` que se encarga del depliegue (en Linux):

```bash
#En Local:
sudo chmod +x deploy.sh
./deploy.sh -l
```

Una vez montados los contenedores, para usar el servicio de Load que es quien da el producto final ingresamos a:

```exe
http://127.0.0.1:8005/exportar_csv
```

Y obtenemos el resultado, un discriminado de ninjas principales por clanes.

```bash
#En producción
sudp chmod +x deploy.sh
./deploy.sh -p
```
