import numpy as np
import open3d as o3d
import networkx as nx

def check_pc_combinability(source, target, threshold):
    """
    Comprueba la combinabilidad de dos nubes de puntos en función de la distancia entre ellas.

    Parameters:
        source: open3d.geometry.PointCloud
            Nube de puntos de origen.
        target: open3d.geometry.PointCloud
            Nube de puntos de destino.
        threshold: float
            Umbral para determinar la combinabilidad.

    Returns:
        combinable: bool
            True si las nubes de puntos son combinables, False de lo contrario.
    """
    # Calcular la distancia entre las nubes de puntos
    distance = source.compute_point_cloud_distance(target)
    distance_ = np.asarray(distance)
    average_distance = np.mean(distance_)
    print(f"Pair: ({source}, {target}), O3D Distance: {average_distance}")

    # Comprobar si la distancia es menor que el umbral
    combinable = average_distance < threshold

    return combinable

def build_combination_graph(pcds, threshold):
    """
    Construye un grafo de combinabilidad para las nubes de puntos.

    Parameters:
        pcds: List[open3d.geometry.PointCloud]
            Lista de nubes de puntos.
        threshold: float
            Umbral para determinar la combinabilidad.

    Returns:
        G: networkx.Graph
            Grafo de combinabilidad de las nubes de puntos.
    """
    G = nx.Graph()

    # Añadir nodos al grafo
    for i in range(len(pcds)):
        G.add_node(i)

    # Añadir aristas al grafo para las nubes de puntos combinables
    for i in range(len(pcds)):
        for j in range(i + 1, len(pcds)):
            if check_pc_combinability(pcds[i], pcds[j], threshold):
                G.add_edge(i, j)

    return G

def get_largest_combination_component(pcds, threshold):
    """
    Obtiene la lista más grande de nubes de puntos combinables.

    Parameters:
        pcds: List[open3d.geometry.PointCloud]
            Lista de nubes de puntos.
        threshold: float
            Umbral para determinar la combinabilidad.

    Returns:
        largest_component_pcds: List[open3d.geometry.PointCloud]
            Lista de nubes de puntos en el componente más grande.
    """
    # Construir el grafo de combinabilidad
    G = build_combination_graph(pcds, threshold)

    # Encontrar el componente conectado más grande
    largest_component = max(nx.connected_components(G), key=len)

    # Obtener las nubes de puntos en el componente más grande
    largest_component_pcds = [pcds[i] for i in largest_component]

    return largest_component_pcds

def check_all_pc_combinability(pcds, threshold):
    """
    Comprueba la combinabilidad de todas las nubes de puntos en una lista.

    Parameters:
        pcds: List[open3d.geometry.PointCloud]
            Lista de nubes de puntos.
        threshold: float
            Umbral para determinar la combinabilidad.

    Returns:
        combinable_pairs: List[Tuple[int, int]]
            Lista de nubes de puntos combinables.
    """
    combinable_pairs = get_largest_combination_component(pcds, threshold)
    return combinable_pairs