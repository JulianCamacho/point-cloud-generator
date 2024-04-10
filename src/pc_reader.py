import os
import json
import open3d as o3d

def load_point_clouds(config_file, voxel_size=0.0):
    """
    Carga nubes de puntos desde archivos PCD en una carpeta especificada en un archivo de configuración JSON.

    Parámetros:
        config_file (str): Ruta al archivo de configuración JSON.
        voxel_size (float): Tamaño del voxel para el muestreo (0.0 por defecto para no muestrear).

    Devuelve:
        list: Lista de nubes de puntos cargadas.
    """
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        input_path = config.get("input_path")
        if input_path is None:
            print("Error: No se proporcionó la ruta de la carpeta en el archivo de configuración.")
            return []

        if not os.path.isdir(input_path):
            print(f"Error: La ruta especificada '{input_path}' no es un directorio válido.")
            return []
        
        print(f"Éxito en la lectura del archivo de configuración: La ruta especificada para nubes de puntos de entrada es: '{input_path}'.")
        pcds = []
        for file in os.listdir(input_path):
            if file.endswith(".pcd"):
                pcd_path = os.path.join(input_path, file)
                pcd = o3d.io.read_point_cloud(pcd_path)
                pcds.append(pcd)

        if not pcds:
            print("Advertencia: No se encontraron archivos PCD en la carpeta especificada.")
        return pcds

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de configuración {config_file}.")
        return []
    except json.JSONDecodeError:
        print(f"Error: No se pudo analizar el archivo JSON {config_file}.")
        return []
