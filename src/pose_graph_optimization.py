import open3d as o3d

def optimize_pose_graph(pose_graph, max_correspondence_distance_fine):
    """
    Optimiza el grafo de poses utilizando el método de optimización global.

    Parámetros:
        pose_graph: open3d.pipelines.registration.PoseGraph
            El grafo de poses a optimizar.
        max_correspondence_distance_fine: float
            Distancia máxima para buscar correspondencias durante la optimización.

    Retorna:
        pose_graph_optimized: open3d.pipelines.registration.PoseGraph
            El grafo de poses optimizado.
    """
    # Imprime un mensaje para indicar que se está realizando la optimización del grafo de poses
    print("Optimizando PoseGraph ...")
    
    # Configura las opciones para la optimización global
    option = o3d.pipelines.registration.GlobalOptimizationOption(
        max_correspondence_distance=max_correspondence_distance_fine,
        edge_prune_threshold=0.25,
        reference_node=0)
    
    # Utiliza un contexto de verbosidad para temporariamente establecer el nivel de verbosidad en "Debug"
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        
        # Realiza la optimización global del grafo de poses
        o3d.pipelines.registration.global_optimization(
            pose_graph,
            o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
            o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(),
            option)
    
    # Retorna el grafo de poses optimizado
    return pose_graph
