import nest_asyncio
nest_asyncio.apply()

from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.graph_traversal import __
import os

ENDPOINT = 'wss://acdbkrmgraph.gremlin.cosmos.azure.com:443/'
KEY = 'ggX7DuoWF3hzkxSXb36ZOZfVlf4xqFsDKY5WlUJmvGXOSsZGCf5Dp846Ya4ha0HgLMivQyUS4MFpACDb8KBzqQ=='
DATABASE = 'graphdb'
GRAPH = 'Persons'

# Configuración de las credenciales
GREMLIN_ENDPOINT = ENDPOINT
GREMLIN_KEY = KEY
DATABASE_NAME = DATABASE
GRAPH_NAME = GRAPH

# Construir la cadena de conexión
connection_string = f"{GREMLIN_ENDPOINT}/gremlin?ssl=true&username=/dbs/{DATABASE_NAME}/colls/{GRAPH_NAME}&password={GREMLIN_KEY}"

try:
    print("Iniciando conexión remota...")
    # Inicializar la conexión remota
    graph = Graph()
    remote_connection = DriverRemoteConnection(connection_string, 'g')
    g = graph.traversal().withRemote(remote_connection)
    print("Conexión remota establecida.")

    # Crear vértices
    print("Creando vértices...")
    try:
        g.addV('Persona').property('id', '1').property('nombre', 'Alice').property('edad', 30).iterate()
        print("Vértice Alice creado.")
    except Exception as e:
        print(f"Error al crear vértice Alice: {e}")

    try:
        g.addV('Persona').property('id', '2').property('nombre', 'Bob').property('edad', 25).iterate()
        print("Vértice Bob creado.")
    except Exception as e:
        print(f"Error al crear vértice Bob: {e}")

    try:
        g.addV('Persona').property('id', '3').property('nombre', 'Charlie').property('edad', 35).iterate()
        print("Vértice Charlie creado.")
    except Exception as e:
        print(f"Error al crear vértice Charlie: {e}")

    # Crear aristas
    print("Creando aristas...")
    try:
        g.V('1').addE('amigo_de').to(g.V('2')).property('desde', '2023-10-01').iterate()
        print("Arista de Alice a Bob creada.")
    except Exception as e:
        print(f"Error al crear arista de Alice a Bob: {e}")

    try:
        g.V('2').addE('amigo_de').to(g.V('3')).property('desde', '2023-10-05').iterate()
        print("Arista de Bob a Charlie creada.")
    except Exception as e:
        print(f"Error al crear arista de Bob a Charlie: {e}")

    try:
        g.V('3').addE('amigo_de').to(g.V('1')).property('desde', '2023-10-10').iterate()
        print("Arista de Charlie a Alice creada.")
    except Exception as e:
        print(f"Error al crear arista de Charlie a Alice: {e}")

    # Consultar el grafo: Obtener amigos de Alice
    print("Consultando amigos de Alice...")
    try:
        amigos_alice = g.V('1').out('amigo_de').values('nombre').toList()
        print(f"Amigos de Alice: {amigos_alice}")
    except Exception as e:
        print(f"Error al consultar amigos de Alice: {e}")

    # Consultar el grafo: Encontrar caminos entre Alice y Charlie
    print("Buscando caminos de Alice a Charlie...")
    try:
        caminos = g.V('1').repeat(__.out('amigo_de')).until(__.hasId('3')).path().by('nombre').toList()
        print(f"Caminos de Alice a Charlie: {caminos}")
    except Exception as e:
        print(f"Error al buscar caminos de Alice a Charlie: {e}")

except Exception as e:
    print(f"Error al establecer la conexión remota: {e}")
finally:
    try:
        remote_connection.close()
        print("Conexión remota cerrada.")
    except Exception as e:
        print(f"Error al cerrar la conexión remota: {e}")