from pc_reader import load_point_clouds

def main():
    # Ruta al archivo de configuración JSON
    config_file = "../data/config.json"
    
    # Tamaño del voxel para el muestreo
    voxel_size = 0.01
    
    # Cargar nubes de puntos desde el archivo de configuración
    pcds = load_point_clouds(config_file, voxel_size)
    
    # Imprimir el número de nubes de puntos cargadas
    print(f"Se cargaron {len(pcds)} nubes de puntos.")

if __name__ == "__main__":
    main()
    