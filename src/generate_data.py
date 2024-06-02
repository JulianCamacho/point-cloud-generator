import os
import open3d as o3d
import numpy as np
from pc_preprocessing import pc_preprocessing
import csv

def compute_alignment_quality(source, target):
    """
    Calcula la calidad de la alineación entre dos nubes de puntos.
    
    Parámetros:
        source (open3d.geometry.PointCloud): Nube de puntos de origen.
        target (open3d.geometry.PointCloud): Nube de puntos de destino.
        
    Devuelve:
        numpy.array: Vector de características que representan la calidad de la alineación.
    """
    # Número total de puntos en cada nube de puntos
    num_points_source = len(source.points)
    num_points_target = len(target.points)
    
    # Diferencia en el número de puntos
    point_diff = abs(num_points_source - num_points_target) 
    
    # Número de correspondencias
    num_correspondences = min(num_points_source, num_points_target)
    
    # Distancia promedio entre correspondencias
    distances = []
    for i in range(num_correspondences):
        dist = np.linalg.norm(np.asarray(source.points[i]) - np.asarray(target.points[i]))
        distances.append(dist)
    mean_distance = np.mean(distances)

    distance = source.compute_point_cloud_distance(target)
    distance_ = np.asarray(distance)
    # Calcular la distancia promedio
    average_distance = np.mean(distance_)
    
    # Combina todas las medidas en un vector de características
    features = np.array([point_diff, mean_distance, average_distance])
    
    return features

def process_point_clouds_in_folder(folder_path, output_file):
    """
    Procesa cada par de nubes de puntos en una carpeta y guarda los resultados en un archivo CSV.
    
    Parámetros:
        folder_path (str): Ruta de la carpeta que contiene las nubes de puntos.
        output_file (str): Ruta del archivo CSV de salida.
    """
    # Obtener la lista de archivos en la carpeta
    files = os.listdir(folder_path)
    num_files = len(files)
    
    pcds = []
    for file in os.listdir(folder_path):
        if file.endswith(".pcd"):
            pcd_path = os.path.join(folder_path, file)
            pcd = o3d.io.read_point_cloud(pcd_path)
            pcds.append(pcd)
            
    # Aplicar preprocesamiento
    pre_processed_pcds = pc_preprocessing(pcds, voxel_size=0.02, 
                remove_outliers_params={"nb_neighbors": 20, "std_ratio": 2.0})
    print(f"Se preprocesaron {len(pre_processed_pcds)} nubes de puntos.")
    
    # Crear o abrir el archivo CSV de salida
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Escribir encabezados de las columnas en el archivo CSV
        csvwriter.writerow(['Source', 'Target', 'Point Difference', 
                            'Mean Distance', 'o3D Distance'])
        
        # Procesar cada par de nubes de puntos
        for i in range(len(pre_processed_pcds)):
            for j in range(len(pre_processed_pcds)):
                if i != j:
                    # Calcular características de calidad de alineación
                    features = compute_alignment_quality(pre_processed_pcds[i], pre_processed_pcds[j])
                    
                    # Escribir resultados en el archivo CSV
                    csvwriter.writerow([files[i], files[j]] + list(features))
