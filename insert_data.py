import json
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Cassandra
KEYSPACE = os.getenv("CASSANDRA_KEYSPACE")
SECURE_BUNDLE = os.getenv("SECURE_CONNECT_BUNDLE")

with open("data/test_cassandra-token.json") as f:
    secrets = json.load(f)

CLIENT_ID = secrets["clientId"]
CLIENT_SECRET = secrets["secret"]

cloud_config = {'secure_connect_bundle': SECURE_BUNDLE}
auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session.set_keyspace(KEYSPACE)

# Insertar datos solo si no existen previamente
def insert_data():
    print("Insertando datos en la base de datos...")

    ## Insertar clientes
    clientes = [
        ("Juan Pérez", "Calle 123, Ciudad A", "123456789"),
        ("María López", "Av. Reforma 456, Ciudad B", "987654321"),
        ("Carlos Sánchez", "Carrera 78, Ciudad C", "555123456"),
        ("Ana Torres", "Calle del Sol 89, Ciudad D", "666789123"),
        ("Pedro Ramírez", "Paseo de la Luna 22, Ciudad E", "777888999"),
        ("Laura Martínez", "Blvd. Central 100, Ciudad F", "111222333"),
        ("José Fernández", "Av. Principal 250, Ciudad G", "444555666"),
        ("Sofía Castro", "Calle de la Rosa 5, Ciudad H", "999000111"),
        ("Roberto Gómez", "Camino Verde 78, Ciudad I", "222333444"),
        ("Isabel Díaz", "Paseo del Río 15, Ciudad J", "555666777"),
    ]

    for nombre, direccion, telefono in clientes:
        session.execute("""
            INSERT INTO clientes (cliente_id, nombre, direccion, telefono)
            VALUES (uuid(), %s, %s, %s);
        """, (nombre, direccion, telefono))

    ## Insertar pedidos por cliente
    pedidos = [
        ("2024-03-25 10:30:00", "En proceso"),
        ("2024-03-20 15:45:00", "Entregado"),
        ("2024-03-18 09:15:00", "Pendiente"),
        ("2024-03-28 18:20:00", "Cancelado"),
        ("2024-03-30 12:50:00", "En camino"),
        ("2024-03-22 08:10:00", "Entregado"),
        ("2024-03-21 20:40:00", "Pendiente"),
        ("2024-03-24 14:00:00", "En proceso"),
        ("2024-03-27 17:30:00", "Entregado"),
        ("2024-03-29 11:45:00", "Pendiente"),
    ]

    for fecha, estado in pedidos:
        session.execute("""
            INSERT INTO pedidos_por_cliente (cliente_id, pedido_id, fecha, estado)
            VALUES (uuid(), uuid(), %s, %s);
        """, (fecha, estado))

    ## Insertar pedidos por fecha
    for fecha, estado in pedidos:
        session.execute("""
            INSERT INTO pedidos_por_fecha (fecha, pedido_id, cliente_id, estado)
            VALUES (%s, uuid(), uuid(), %s);
        """, (fecha, estado))

    ## Insertar productos por pedido
    productos = [
        ("Laptop HP", 1, 850.99),
        ("Mouse inalámbrico", 2, 19.99),
        ("Teclado mecánico", 1, 49.99),
        ("Monitor 24 pulgadas", 1, 129.99),
        ("Silla ergonómica", 1, 199.99),
    ]

    for nombre_producto, cantidad, precio in productos:
        session.execute("""
            INSERT INTO productos_por_pedido (pedido_id, producto_id, nombre_producto, cantidad, precio)
            VALUES (uuid(), uuid(), %s, %s, %s);
        """, (nombre_producto, cantidad, precio))

    print("Datos insertados correctamente.")

if __name__ == "__main__":
    insert_data()
