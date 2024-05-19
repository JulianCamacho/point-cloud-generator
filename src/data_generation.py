import os
import open3d as o3d
import numpy as np
from pc_preprocessing import pc_preprocessing
import csv

def compute_fpfh_feature(point_cloud, voxel_size):
    """
    Compute the FPFH feature for the point cloud.
    """
    radius_feature = voxel_size * 5
    print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        point_cloud,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return fpfh

def compute_point_cloud_distance(pcd1, pcd2):
    """
    Compute the mean and standard deviation of distances from pcd1 to pcd2.
    """
    distances = pcd1.compute_point_cloud_distance(pcd2)
    mean_distance = np.mean(distances)
    distance_std = np.std(distances)
    return mean_distance, distance_std

def combine_features(fpfh1, fpfh2, mean_distance, distance_std):
    """
    Combine FPFH features and distance metrics into a single feature vector.
    """
    # Use mean FPFH features for simplicity
    mean_fpfh1 = np.mean(fpfh1.data, axis=1)
    mean_fpfh2 = np.mean(fpfh2.data, axis=1)
    
    # Combine FPFH features with distance metrics
    combined_features = [mean_fpfh1, mean_fpfh2, mean_distance, distance_std]
    return combined_features

def compute_alignment_quality(source, target):
    """
    Calcula la calidad de la alineación entre dos nubes de puntos.
    
    Parámetros:
        source (open3d.geometry.PointCloud): Nube de puntos de origen.
        target (open3d.geometry.PointCloud): Nube de puntos de destino.
        
    Devuelve:
        numpy.array: Vector de características que representan la calidad de la alineación.
    """
    voxel_size = 0.02
    radius_normal = voxel_size * 2
    source.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    target.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    
    # Compute FPFH features
    fpfh1 = compute_fpfh_feature(source, voxel_size)
    fpfh2 = compute_fpfh_feature(target, voxel_size)

    # Compute distance metrics
    mean_distance, distance_std = compute_point_cloud_distance(source, target)
    
    # Combine features
    combined_features = combine_features(fpfh1, fpfh2, mean_distance, distance_std)
    print("Combined Features:", combined_features)
    return combined_features

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
        csvwriter.writerow(['Source', 'Target', 'mean_fpfh1', 'mean_fpfh2', 'mean_distance', 'distance_std'])
        
        # Procesar cada par de nubes de puntos
        for i in range(len(pre_processed_pcds)):
            for j in range(len(pre_processed_pcds)):
                if i != j:
                    # Calcular características de calidad de alineación
                    features = compute_alignment_quality(pre_processed_pcds[i], pre_processed_pcds[j])
                    
                    # Escribir resultados en el archivo CSV
                    csvwriter.writerow([files[i], files[j]] + list(features))

# Ejemplo de uso
folder_path = "../data/test"
output_file = "train_2.csv"
process_point_clouds_in_folder(folder_path, output_file)
