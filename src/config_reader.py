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
    # Configuración por defecto
    default_config = {
        "voxel_size": 0.02,
        "remove_outliers_params": {
            "nb_neighbors": 20,
            "std_ratio": 2.0
        },
        "combinability_threshold": 0.5
    }

    # Nombres esperados y sus tipos
    expected_params = {
        "voxel_size": float,
        "remove_outliers_params": {
            "nb_neighbors": int,
            "std_ratio": float
        },
        "combinability_threshold": float
    }

    def validate_config(config, expected_params):
        """
        Valida que la configuración tenga los nombres esperados y valores numéricos.

        Parámetros:
            config (dict): Configuración cargada.
            expected_params (dict): Estructura esperada de la configuración.

        Devuelve:
            bool: True si la configuración es válida, False de lo contrario.
        """
        for key, expected_type in expected_params.items():
            if key not in config:
                print(f"Advertencia: Falta la clave '{key}' en la configuración.")
                return False
            if isinstance(expected_type, dict):
                if not validate_config(config[key], expected_type):
                    return False
            elif not isinstance(config[key], expected_type):
                print(f"Advertencia: El valor de '{key}' debe ser de tipo {expected_type.__name__}.")
                return False
        return True

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)

        config_params = config.get("config_params", {})
        
        if validate_config(config_params, expected_params):
            return config_params
        else:
            print(f"Advertencia: La configuración no es válida. Se utilizarán los valores por defecto: {default_config}")
            return default_config

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de configuración {config_file}.")
        return default_config
    except json.JSONDecodeError:
        print(f"Error: No se pudo analizar el archivo JSON {config_file}.")
        return default_config

# Ejemplo de uso
config_file = "../data/config.json"
config = load_config(config_file)
print(config)
