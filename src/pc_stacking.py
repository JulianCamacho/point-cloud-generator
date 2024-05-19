import open3d as o3d
import numpy as np

def pairwise_registration(source, target, max_correspondence_distance_coarse,
                          max_correspondence_distance_fine):
    """
    Realiza el registro de dos nubes de puntos utilizando el método de registro de ICP punto a plano.

    Parameters:
        source: open3d.geometry.PointCloud
            La nube de puntos fuente que se registrará a la nube de puntos objetivo.
        target: open3d.geometry.PointCloud
            La nube de puntos objetivo a la cual se registrará la nube de puntos fuente.
        max_correspondence_distance_coarse: float
            Distancia máxima para buscar correspondencias durante el registro grueso.
        max_correspondence_distance_fine: float
            Distancia máxima para buscar correspondencias durante el registro fino.

    Returns:
        transformation_icp: numpy.ndarray
            La matriz de transformación resultante del registro ICP.
        information_icp: numpy.ndarray
            La matriz de información resultante del registro ICP.
    """

    # Estimación de normales para la nube de puntos objetivo
    print("Calculando normales para la nube de puntos objetivo...")
    target.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    # Registro grueso utilizando ICP punto a plano
    print("Aplicando ICP punto a plano (registro grueso)...")
    icp_coarse = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_coarse, np.identity(4),
        o3d.pipelines.registration.TransformationEstimationPointToPlane())

    # Registro fino utilizando ICP punto a plano con la transformación obtenida del registro grueso
    print("Aplicando ICP punto a plano (registro fino)...")
    icp_fine = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_fine,
        icp_coarse.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())

    # Obtener la matriz de transformación y la matriz de información resultantes
    transformation_icp = icp_fine.transformation
    information_icp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
        source, target, max_correspondence_distance_fine,
        icp_fine.transformation)

    return transformation_icp, information_icp
