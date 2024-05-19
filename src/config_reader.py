import os
import json

def load_config(config_file):
    """
    Carga la configuración desde un archivo JSON.

    Parámetros:
        config_file (str): Ruta al archivo de configuración JSON.

    Devuelve:
        dict: Configuración cargada desde el archivo JSON.
    """
    default_config = {
        "voxel_size": 0.02,
        "remove_outliers_params": {
            "nb_neighbors": 20,
            "std_ratio": 2.0
        },
        "combinability_threshold": 0.5
    }

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        config_params = config.get("config_params")

        if config_params:
            return config_params
        else:
            print("Advertencia: No se encontraron configuraciones en el archivo. Se utilizarán valores por defecto.")
            return default_config

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de configuración {config_file}.")
        return {}, {}
    except json.JSONDecodeError:
        print(f"Error: No se pudo analizar el archivo JSON {config_file}.")
        return {}, {}
