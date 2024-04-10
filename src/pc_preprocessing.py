import open3d as o3d

def voxel_down_sample(pcd, voxel_size=0.0):
    """
    Reducción de muestras de la nube de puntos mediante voxelización.

    Parámetros:
        pcd (open3d.geometry.PointCloud): Nube de puntos de entrada.
        voxel_size (float): Tamaño del voxel para el muestreo (0.0 por defecto para no muestrear).

    Devuelve:
        open3d.geometry.PointCloud: Nube de puntos reducida.
    """
    if voxel_size > 0.0:
        return pcd.voxel_down_sample(voxel_size=voxel_size)
    else:
        return pcd

def remove_outliers(pcd, nb_neighbors=20, std_ratio=2.0, print_progress=True):
    """
    Elimina los puntos atípicos de la nube de puntos utilizando estadísticas de distancia local.

    Parámetros:
        pcd (open3d.geometry.PointCloud): Nube de puntos de entrada.
        nb_neighbors (int): Número de vecinos para calcular la distancia (20 por defecto).
        std_ratio (float): Proporción del desvío estándar para determinar el umbral de distancia (2.0 por defecto).

    Devuelve:
        open3d.geometry.PointCloud: Nube de puntos sin puntos atípicos.
        list: Lista de índices de puntos considerados como no atípicos.
    """
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio, print_progress=print_progress)
    return cl, ind


def pc_preprocessing(pcds, voxel_size=0.0, remove_outliers_params=None):
    """
    Realiza preprocesamiento en una lista de nubes de puntos.

    Parámetros:
        pcds (list): Lista de nubes de puntos de entrada.
        voxel_size (float): Tamaño del voxel para el muestreo (0.0 por defecto para no muestrear).
        remove_outliers_params (dict): Parámetros para la función remove_outliers.

    Devuelve:
        list: Lista de nubes de puntos preprocesadas.
    """
    processed_pcds = []
    for pcd in pcds:
        # Obtener el tipo de datos de la nube de puntos original
        pcd_type = type(pcd)
        
        # Aplicar voxel_down_sample si es necesario
        pcd_processed = voxel_down_sample(pcd, voxel_size=voxel_size)
        
        # Aplicar remove_outliers si se proporcionan parámetros
        if remove_outliers_params is not None:
            pcd_processed, indices = remove_outliers(pcd_processed, **remove_outliers_params)
            pcd_processed = o3d.geometry.PointCloud(pcd_processed)
            
        processed_pcds.append(pcd_processed)

    return processed_pcds
