# Cassandra-Flask App
Este proyecto es una aplicación web construida con Flask que se conecta a una base de datos Apache Cassandra para gestionar y mostrar información de clientes, pedidos y productos.

# Estructura del proyecto

cassandra-flask-app/               
|--data/                                     # Carpeta con los archivos necesarios de Cassandra
|    |--secure-connect-test-cassandra.zip    # Archivo ZIP de Cassandra
|    |--test_cassandra-token.json            # Credenciales de acceso
|--env                                       # Archivo para configurar variables de entorno (como token y credenciales)
|--.gitignore                                # Archivo que especifica qué archivos ignorar
|--app.py                                    # Aplicación Python que interactúa con Cassandra
|--Dockerfile                                # Instrucciones para construir la imagen de Docker
|--insert_data.py                            # Script para insertar datos de ejemplo
|--README.md                                 # Documentación del proyecto
|--requirements.txt                          # Listado de dependencias necesarias (como 'cassandra-driver')


# Requisitos
Python 3.11

Docker para la ejecución del contenedor

Acceso a una base de datos Apache Cassandra. En este caso, DataStax


# Configuración

1. Copia el archivo .env.example a .env y configura las variables
    CASSANDRA_KEYSPACE=test
    SECURE_CONNECT_BUNDLE=data/secure-connect-test-cassandra.zip
2. Coloca tus credenciales de Cassandra en data/test_cassandra-token.json


# Instalación

1. Clona el repositorio
2. Instala las dependencias
    pip install -r requirements.txt


# Uso

## Ejecución local

python app.py
La aplicación estará disponible en http://localhost:5000

## Ejecución con Docker

1. Construye la imagen:
    docker build -t cassandra-flask-app .

2. Ejecuta el contenedor:
    docker run -p 5000:5000 cassandra-flask-app

## Población de datos

Para insertar datos de ejemplo en las tablas:
    python insert_data.py


## Endpoints disponibles
/ - Página de inicio con lista de endpoints

/clientes - Muestra todos los clientes

/pedidos_por_cliente - Muestra pedidos organizados por cliente

/pedidos_por_fecha - Muestra pedidos organizados por fecha

/productos_por_pedido - Muestra productos organizados por pedido


## Estructura de la base de datos
La aplicación crea automáticamente las siguientes tablas:

- clientes: Información básica de clientes

- pedidos_por_cliente: Pedidos organizados por cliente

- pedidos_por_fecha: Pedidos organizados por fecha

- productos_por_pedido: Productos asociados a cada pedido


## Autor 

- Andrés Flores