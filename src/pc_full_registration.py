import open3d as o3d
import numpy as np
from pc_stacking import pairwise_registration

def full_registration(pcds, max_correspondence_distance_coarse,
                      max_correspondence_distance_fine):
    """
    Realiza el registro completo de todas las nubes de puntos en la lista pcds.

    Parameters:
        pcds: List[open3d.geometry.PointCloud]
            Lista de nubes de puntos a registrar.
        max_correspondence_distance_coarse: float
            Distancia máxima para buscar correspondencias durante el registro grueso.
        max_correspondence_distance_fine: float
            Distancia máxima para buscar correspondencias durante el registro fino.

    Returns:
        pose_graph: open3d.pipelines.registration.PoseGraph
            El grafo de poses resultante del registro.
    """
    # Inicializa un grafo de poses
    pose_graph = o3d.pipelines.registration.PoseGraph()

    # Inicializa la matriz de odometría
    odometry = np.identity(4)

    # Añade el primer nodo al grafo de poses con la matriz de identidad como su pose
    pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(odometry))

    # Obtiene el número de nubes de puntos en la lista
    n_pcds = len(pcds)

    # Itera sobre todas las combinaciones posibles de pares de nubes de puntos
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            # Realiza el registro entre la nube de puntos fuente y la nube de puntos objetivo
            transformation_icp, information_icp = pairwise_registration(
                pcds[source_id], pcds[target_id],
                max_correspondence_distance_coarse,
                max_correspondence_distance_fine)

            # Imprime un mensaje indicando la construcción del grafo de poses
            print("Construyendo el grafo de poses")

            # Caso de odometría: si la nube objetivo es la siguiente en la secuencia
            if target_id == source_id + 1:
                # Actualiza la matriz de odometría acumulativa
                odometry = np.dot(transformation_icp, odometry)

                # Añade un nuevo nodo al grafo de poses con la inversa de la odometría acumulativa como su pose
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(
                        np.linalg.inv(odometry)))

                # Añade una arista al grafo de poses que representa la relación de transformación entre las dos nubes de puntos
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=False))
            else:  # Caso de cierre de bucle: si la nube objetivo no es la siguiente en la secuencia
                # Añade una arista al grafo de poses que representa la relación de transformación entre las dos nubes de puntos
                # Se marca como incierta porque no es una relación de odometría directa
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=True))
    return pose_graph
