from pc_reader import load_point_clouds
from config_reader import load_config
from pc_preprocessing import pc_preprocessing
from pc_comparator import check_all_pc_combinability
from pc_stacking import pairwise_registration
from pc_full_registration import full_registration
from pose_graph_optimization import optimize_pose_graph
from pc_writer import write_combined_pcd
import open3d as o3d

def main():
    # Ruta al archivo de configuración JSON
    config_file = "../data/config.json"
    
    ###==============%%%   Lectura de nubes de puntos   %%%==============###
    # Cargar nubes de puntos desde el archivo de configuración
    pcds = load_point_clouds(config_file)
    if len(pcds) == 0:
        return   
    # Imprimir el número de nubes de puntos cargadas
    print(f"Se cargaron {len(pcds)} nubes de puntos.")

    ###====%%%   Visualización de nubes originales   %%%====###
    colors = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0],
              [0, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 0],
              [0.5, 0, 0], [0, 0.5, 0], [0, 0, 0.5]]  # Colores RGB para
    for i in range(len(pcds)):
        pcds[i].paint_uniform_color(colors[i])
    o3d.visualization.draw(pcds)
    
    ###==============%%%   Preprocesamiento de nubes   %%%==============###
    
    ###====%%%   Lectura de configuraciones   %%%====###
    config_params = load_config(config_file)
    print(f"Los parámetros de configuración son: {config_params}")
    voxel_size = config_params.get("voxel_size")
    remove_outliers_params = config_params.get("remove_outliers_params")
    combinability_threshold = config_params.get("combinability_threshold")
    print(f"Éxito al validar los contenidos del archivo de configuración, iniciando el procesamiento") 
       
    ###====%%%   Downsampling y outlier detection   %%%====###
    preprocessed_pcds = pc_preprocessing(pcds, voxel_size, remove_outliers_params)
    print(f"Se preprocesaron {len(preprocessed_pcds)} nubes de puntos.")
    
    ###====%%%   Visualización de nubes preprocesadas   %%%====###
    for i in range(len(preprocessed_pcds)):
        preprocessed_pcds[i].paint_uniform_color(colors[i])
    o3d.visualization.draw(preprocessed_pcds)
    
    ###====%%%   Combinabilidad   %%%====###
    combinable_pcds = check_all_pc_combinability(preprocessed_pcds, combinability_threshold)
    print("Pares combinables:", combinable_pcds)

    # Llamar a la función registration
    if len(combinable_pcds) == 1: #0
        print("Las nubes de puntos no tienen suficientes coincidencias para ser combinadas.")
    else:    
        
    ###==============%%%   Algoritmo de Stacking   %%%==============###
        print("Éxito, combinando las siguientes nubes de puntos: ")
        max_correspondence_distance_coarse = voxel_size * 15
        max_correspondence_distance_fine = voxel_size * 1.5
    
        n_pcds = len(preprocessed_pcds)
        for source_id in range(n_pcds):
            for target_id in range(source_id + 1, n_pcds):
                transformation_icp, information_icp = pairwise_registration(preprocessed_pcds[source_id], preprocessed_pcds[target_id], max_correspondence_distance_coarse, max_correspondence_distance_fine)
                print("transformation_icp: ", transformation_icp)
                print("information_icp: ", information_icp)
                print("========================")
                
        pose_graph = full_registration(preprocessed_pcds,
                                       max_correspondence_distance_coarse,
                                       max_correspondence_distance_fine)

        # Llama a la función optimize_pose_graph para optimizar el grafo de poses
        pose_graph_optimized = optimize_pose_graph(pose_graph, max_correspondence_distance_fine)
        
        print(f"Éxito al aplicar el algoritmo, guardando archivo de salida") 
        # Llamar a la función write_combined_pcd para escribir las nubes de puntos combinadas en un archivo .pcd
        write_combined_pcd(preprocessed_pcds, pose_graph_optimized, config_file)
        
        #print("Transform points and display")
        #for point_id in range(len(preprocessed_pcds)):
        #    print(pose_graph_optimized.nodes[point_id].pose)
        #    preprocessed_pcds[point_id].transform(pose_graph_optimized.nodes[point_id].pose)
        #o3d.visualization.draw(preprocessed_pcds)

if __name__ == "__main__":
    main()
    