import os
import open3d as o3d
import numpy as np
import csv
from pc_preprocessing import pc_preprocessing

def preprocess_point_cloud(point_cloud, voxel_size):
    """
    Preprocess the point cloud by downsampling and estimating normals.
    """
    print(":: Downsample with a voxel size %.3f." % voxel_size)
    pcd_down = point_cloud.voxel_down_sample(voxel_size)
    
    radius_normal = voxel_size * 2
    pcd_down.estimate_normals(
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))
    
    return pcd_down

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

def combine_features(fpfh1, fpfh2, distance_metrics):
    """
    Combine FPFH features and distance metrics into a single feature vector.
    """
    # Use mean FPFH features for simplicity
    mean_fpfh1 = np.mean(fpfh1.data, axis=1)
    mean_fpfh2 = np.mean(fpfh2.data, axis=1)
    
    # Combine FPFH features with distance metrics
    combined_features = np.hstack((mean_fpfh1, mean_fpfh2, distance_metrics))
    return combined_features

# Load point clouds
pcd1 = o3d.io.read_point_cloud("path_to_first_point_cloud.ply")
pcd2 = o3d.io.read_point_cloud("path_to_second_point_cloud.ply")

# Preprocess point clouds
voxel_size = 0.05  # Set the voxel size for downsampling
pcd1_down = preprocess_point_cloud(pcd1, voxel_size)
pcd2_down = preprocess_point_cloud(pcd2, voxel_size)

# Compute FPFH features
fpfh1 = compute_fpfh_feature(pcd1_down, voxel_size)
fpfh2 = compute_fpfh_feature(pcd2_down, voxel_size)

# Compute distance metrics
mean_distance, distance_std = compute_point_cloud_distance(pcd1_down, pcd2_down)

# Combine features
combined_features = combine_features(fpfh1, fpfh2, np.array([mean_distance, distance_std]))

print("Combined Features:", combined_features)
