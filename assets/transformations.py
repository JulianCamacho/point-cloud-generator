import open3d as o3d
import numpy as np
import os

def load_point_clouds(folder_path, voxel_size=0.0):
    pcds = []
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.pcd'):  # Filtra solo archivos de nubes de puntos
            print(file_name)
            pcd = o3d.io.read_point_cloud(file_path)
            pcds.append(pcd)
    
    return pcds

def calculate_pairwise_transformations(pcds):
    pairs = []
    transformations = []
    
    for i in range(len(pcds)):
        for j in range(i + 1, len(pcds)):
            source_pcd = pcds[i]
            target_pcd = pcds[j]
            threshold = 0.02  # Umbral para ICP
            
            # Registro ICP para calcular la transformación entre las nubes de puntos
            result = o3d.pipelines.registration.registration_icp(
                source_pcd, target_pcd, threshold, np.identity(4),
                o3d.pipelines.registration.TransformationEstimationPointToPoint())
            
            # Añadir el par y la transformación correspondiente a la lista
            pairs.append((source_pcd, target_pcd))
            transformations.append(result.transformation)
    
    return pairs, transformations

# Cargar las nubes de puntos desde una carpeta
folder_path = "../data/"
pcds = load_point_clouds(folder_path)

# Calcular los pares de nubes de puntos con sus transformaciones correspondientes
pcd_pairs, transformations = calculate_pairwise_transformations(pcds)

# Imprimir los pares y sus transformaciones
for i, (pair, transformation) in enumerate(zip(pcd_pairs, transformations)):
    print(f"Par {i+1}:")
    print("Transformación:")
    print(transformation)
