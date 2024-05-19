import numpy as np
import open3d as o3d

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
            Lista de pares de índices de nubes de puntos combinables.
    """
    combinable_pairs = []

    # Iterar sobre todas las nubes de puntos en la lista
    for i in range(len(pcds)):
        for j in range(i+1, len(pcds)):
            # Comparar la combinabilidad de la nube de puntos i con la nube de puntos j
            combinable = check_pc_combinability(pcds[i], pcds[j], threshold)
            # Si las nubes de puntos son combinables, agregar el par de índices a la lista de combinables
            if combinable:
                combinable_pairs.append((i, j))

    return combinable_pairs