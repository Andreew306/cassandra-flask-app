import os
import json
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from flask import Flask

# Cargar variables de entorno
load_dotenv()

# Configuración básica
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")
SECURE_BUNDLE = os.getenv("SECURE_CONNECT_BUNDLE")

# Conexión a Cassandra
cloud_config = {
    'secure_connect_bundle': SECURE_BUNDLE
}
with open("data/test_cassandra-token.json") as f:
    secrets = json.load(f)
CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace(KEYSPACE) 

# Crear las tablas si no existen

## TABLA 1 - Primera consulta
session.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        cliente_id UUID PRIMARY KEY,
        nombre TEXT,
        direccion TEXT,
        telefono TEXT
    )
""")

## TABLA 2 - Segunda consulta
session.execute("""
    CREATE TABLE IF NOT EXISTS pedidos_por_cliente (
        cliente_id UUID,
        pedido_id UUID,
        fecha TIMESTAMP,
        estado TEXT,
        PRIMARY KEY (cliente_id, pedido_id)
    )
""")

## Tabla 3 - Tercera consulta
session.execute("""
    CREATE TABLE IF NOT EXISTS pedidos_por_fecha (
        fecha TIMESTAMP,
        pedido_id UUID,
        cliente_id UUID,
        estado TEXT,
        PRIMARY KEY (fecha, pedido_id)
    )
""")

## Tabla 4 - Cuarta consulta
session.execute("""
    CREATE TABLE IF NOT EXISTS productos_por_pedido (
        pedido_id UUID,
        producto_id UUID,
        nombre_producto TEXT,
        cantidad INT,
        precio DECIMAL,
        PRIMARY KEY (pedido_id, producto_id)
    )
""")

# Aplicación Flask
app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h1>Bienvenido a la API de Cassandra</h1>
    <p>Usa las siguientes rutas:</p>
    <ul>
        <li>/clientes - Ver todos los clientes</li>
        <li>/pedidos_por_cliente - Ver pedidos por cliente</li>
        <li>/pedidos_por_fecha - Ver pedidos por fecha</li>
        <li>/productos_por_pedido - Ver productos por pedido</li>
    </ul>
    """

@app.route("/clientes")
def mostrar_clientes():
    rows = session.execute("SELECT * FROM clientes")
    return "<br>".join([str(row) for row in rows])

@app.route("/pedidos_por_cliente")
def mostrar_pedidos_por_cliente():
    rows = session.execute("SELECT * FROM pedidos_por_cliente")
    return "<br>".join([str(row) for row in rows])

@app.route("/pedidos_por_fecha")
def mostrar_pedidos_por_fecha():
    rows = session.execute("SELECT * FROM pedidos_por_fecha")
    return "<br>".join([str(row) for row in rows])

@app.route("/productos_por_pedido")
def mostrar_productos_por_pedido():
    rows = session.execute("SELECT * FROM productos_por_pedido")
    return "<br>".join([str(row) for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)