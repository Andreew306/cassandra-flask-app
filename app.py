from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
from flask import Flask
from uuid import uuid4

# Conexión a Cassandra
cloud_config = {
    'secure_connect_bundle': 'data/secure-connect-test-cassandra.zip'
}
with open("data/test_cassandra-token.json") as f:
    secrets = json.load(f)
CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace('test')  # Asegúrate de usar tu keyspace

# Crear las tablas si no existen
session.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        cliente_id UUID PRIMARY KEY,
        nombre TEXT,
        direccion TEXT,
        telefono TEXT
    )
""")

session.execute("""
    CREATE TABLE IF NOT EXISTS pedido (
        cliente_id UUID,
        pedido_id UUID,
        fecha TIMESTAMP,
        estado TEXT,
        PRIMARY KEY (cliente_id, fecha, pedido_id)
    ) WITH CLUSTERING ORDER BY (fecha DESC)
""")

session.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        pedido_id UUID,
        producto_id UUID,
        nombre TEXT,
        cantidad INT,
        precio DECIMAL,
        PRIMARY KEY (pedido_id, producto_id)
    )
""")

# Insertar un cliente
session.execute("""
    INSERT INTO cliente (cliente_id, nombre, direccion, telefono)
    VALUES (%s, %s, %s, %s)
""", (uuid4(), 'Juan Pérez', 'Calle Ficticia 123', '555-1234'))

# Insertar un pedido
session.execute("""
    INSERT INTO pedido (cliente_id, pedido_id, fecha, estado)
    VALUES (%s, %s, %s, %s)
""", (uuid4(), uuid4(), '2025-03-28 10:30:00', 'Pendiente'))

# Insertar un producto
session.execute("""
    INSERT INTO producto (pedido_id, producto_id, nombre, cantidad, precio)
    VALUES (%s, %s, %s, %s, %s)
""", (uuid4(), uuid4(), 'Laptop', 1, 799.99))

# Aplicación Flask
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Bienvenido a la API de Cassandra</h1><p>Usa /clientes, /pedidos por cliente, /productos por pedido para ver los datos.</p>"

@app.route("/clientes")
def mostrar_clientes():
    rows = session.execute("SELECT * FROM cliente")
    return "<br>".join([str(row) for row in rows])

@app.route("/pedidos")
def mostrar_pedidos():
    rows = session.execute("SELECT * FROM pedido")
    return "<br>".join([str(row) for row in rows])

@app.route("/productos")
def mostrar_productos():
    rows = session.execute("SELECT * FROM producto")
    return "<br>".join([str(row) for row in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)