import open3d as o3d
import json

def write_combined_pcd(preprocessed_pcds, pose_graph_optimized, config_file):
    """
    Transforma y combina todas las nubes de puntos y las guarda en un solo archivo .pcd.

    Parameters:
        preprocessed_pcds: List[open3d.geometry.PointCloud]
            Lista de nubes de puntos preprocesadas.
        pose_graph_optimized: open3d.pipelines.registration.PoseGraph
            Grafo de poses optimizado.
        config_file: str
            Ruta del archivo de configuración JSON que contiene la ruta del archivo de salida .pcd.

    Returns:
        None
    """
    # Abrir y leer el archivo de configuración JSON
    with open(config_file, 'r') as f:
        config_data = json.load(f)
    
    # Obtener la ruta del archivo de salida .pcd del archivo de configuración
    output_file = config_data.get("output_file")

    print("Transformando puntos y combinando en una sola nube de puntos")

    # Inicializar una nube de puntos vacía para combinar todas las nubes transformadas
    combined_pcd = o3d.geometry.PointCloud()

    # Transformar y combinar todas las nubes de puntos
    for point_id in range(len(preprocessed_pcds)):
        print(pose_graph_optimized.nodes[point_id].pose)
        preprocessed_pcds[point_id].transform(pose_graph_optimized.nodes[point_id].pose)
        # Agregar los puntos de la nube de puntos transformada a la nube de puntos combinada
        combined_pcd += preprocessed_pcds[point_id]

    # Guardar la nube de puntos combinada en un archivo .pcd
    o3d.io.write_point_cloud(output_file, combined_pcd)
    
    output_pcd = o3d.io.read_point_cloud(output_file)
    o3d.visualization.draw_geometries([output_pcd])
