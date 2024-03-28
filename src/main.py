from pc_reader import load_point_clouds
from pc_preprocessing import pc_preprocessing
import open3d as o3d

def main():
    # Ruta al archivo de configuración JSON
    config_file = "../data/config.json"
    
    # Tamaño del voxel para el muestreo
    voxel_size = 0.01
    
    # Cargar nubes de puntos desde el archivo de configuración
    pcds = load_point_clouds(config_file, voxel_size)
    
    # Imprimir el número de nubes de puntos cargadas
    print(f"Se cargaron {len(pcds)} nubes de puntos.")
    
    # Aplicar preprocesamiento
    processed_pcds = pc_preprocessing(pcds, voxel_size=0.02, remove_outliers_params={"nb_neighbors": 20, "std_ratio": 2.0})

    # Imprimir el número de nubes de puntos preprocesadas
    print(f"Se preprocesaron {len(processed_pcds)} nubes de puntos.")
    # Guardar las nubes de puntos preprocesadas
    for i, pcd_processed in enumerate(processed_pcds):
        o3d.io.write_point_cloud(f"cloud_processed_{i}.pcd", pcd_processed)
            

if __name__ == "__main__":
    main()
    