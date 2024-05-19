# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2023 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------
"""Align multiple pieces of geometry in a global space"""

import open3d as o3d
import numpy as np
import os

def load_point_clouds(voxel_size=0.0):
    pcd_data = o3d.data.DemoICPPointClouds()
    pcds = []
    for i in range(3):
        pcd = o3d.io.read_point_cloud(pcd_data.paths[i])
        pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
        cl, ind = pcd_down.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0, print_progress=True)
        pcds.append(cl)
    return pcds

def load_point_clouds_local(folder_path, voxel_size=0.0):
    pcds = []
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.pcd'):  # Filtra solo archivos de nubes de puntos
            print(file_name)
            pcd = o3d.io.read_point_cloud(file_path)
            pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
            pcds.append(pcd_down)
    
    return pcds

def pairwise_registration(source, target, max_correspondence_distance_coarse,
                          max_correspondence_distance_fine):
    print("Computing normal for the target point cloud...")
    target.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

    print("Apply point-to-plane ICP")
    icp_coarse = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_coarse, np.identity(4),
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    icp_fine = o3d.pipelines.registration.registration_icp(
        source, target, max_correspondence_distance_fine,
        icp_coarse.transformation,
        o3d.pipelines.registration.TransformationEstimationPointToPlane())
    transformation_icp = icp_fine.transformation
    information_icp = o3d.pipelines.registration.get_information_matrix_from_point_clouds(
        source, target, max_correspondence_distance_fine,
        icp_fine.transformation)
    return transformation_icp, information_icp


def full_registration(pcds, max_correspondence_distance_coarse,
                      max_correspondence_distance_fine):
    pose_graph = o3d.pipelines.registration.PoseGraph()
    odometry = np.identity(4)
    pose_graph.nodes.append(o3d.pipelines.registration.PoseGraphNode(odometry))
    n_pcds = len(pcds)
    for source_id in range(n_pcds):
        for target_id in range(source_id + 1, n_pcds):
            transformation_icp, information_icp = pairwise_registration(
                pcds[source_id], pcds[target_id],
                max_correspondence_distance_coarse,
                max_correspondence_distance_fine)
            print("Build o3d.pipelines.registration.PoseGraph")
            if target_id == source_id + 1:  # odometry case
                odometry = np.dot(transformation_icp, odometry)
                pose_graph.nodes.append(
                    o3d.pipelines.registration.PoseGraphNode(
                        np.linalg.inv(odometry)))
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=False))
            else:  # loop closure case
                pose_graph.edges.append(
                    o3d.pipelines.registration.PoseGraphEdge(source_id,
                                                             target_id,
                                                             transformation_icp,
                                                             information_icp,
                                                             uncertain=True))
    return pose_graph

if __name__ == "__main__":
    voxel_size = 0.02
    dataset_folder = "../data/test"
    pcds_down = load_point_clouds_local(dataset_folder, voxel_size)
    #pcds_down = load_point_clouds(voxel_size)
    print(pcds_down)    
    o3d.visualization.draw(pcds_down)

    print("Full registration ...")
    max_correspondence_distance_coarse = voxel_size * 15
    max_correspondence_distance_fine = voxel_size * 1.5
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        pose_graph = full_registration(pcds_down,
                                       max_correspondence_distance_coarse,
                                       max_correspondence_distance_fine)

    print("Optimizing PoseGraph ...")
    option = o3d.pipelines.registration.GlobalOptimizationOption(
        max_correspondence_distance=max_correspondence_distance_fine,
        edge_prune_threshold=0.25,
        reference_node=0)
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        o3d.pipelines.registration.global_optimization(
            pose_graph,
            o3d.pipelines.registration.GlobalOptimizationLevenbergMarquardt(),
            o3d.pipelines.registration.GlobalOptimizationConvergenceCriteria(),
            option)

    print("Transform points and display")
    for point_id in range(len(pcds_down)):
        print(pose_graph.nodes[point_id].pose)
        pcds_down[point_id].transform(pose_graph.nodes[point_id].pose)
    o3d.visualization.draw(pcds_down)
