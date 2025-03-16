import sys
import cv2
import numpy as np
import open3d as o3d
import json
import torch
from midas.midas_net import MidasNet  # Ensure you have the MiDaS model implementation

# Load the MiDaS model
model_type = "DPT_Large"  # or "MiDaS_small" for a smaller model
model = MidasNet(model_type)
model.eval()

def predict_depth(image):
    # Preprocess the image for MiDaS
    input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    input_image = cv2.resize(input_image, (model.input_size, model.input_size))
    input_tensor = torch.from_numpy(input_image).unsqueeze(0).float() / 255.0
    with torch.no_grad():
        depth_map = model(input_tensor)
    return depth_map.squeeze().numpy()

def reconstruct_3D(image_path):
    # Load Image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read.")

    # Use the advanced depth estimation model
    depth_map = predict_depth(image)

    # Normalize Depth Map
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())

    # Create 3D Point Cloud
    h, w = depth_map.shape
    fx, fy = w / 2, h / 2
    cx, cy = w / 2, h / 2
    points = []

    for i in range(h):
        for j in range(w):
            z = depth_map[i, j]
            x = (j - cx) * z / fx
            y = (i - cy) * z / fy
            points.append([x, y, z])

    # Convert to Open3D Point Cloud
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(np.array(points))

    # Create mesh from point cloud
    mesh = create_mesh_from_point_cloud(point_cloud)

    # Apply texture mapping
    mesh = apply_texture(mesh, image)

    # Save the mesh
    model_path = "output/hologram_model.ply"
    o3d.io.write_triangle_mesh(model_path, mesh)

    return model_path

def create_mesh_from_point_cloud(point_cloud):
    # Estimate normals
    point_cloud.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    
    # Perform Poisson surface reconstruction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=9)
    
    # Remove vertices with low density
    vertices_to_remove = densities < np.mean(densities)
    mesh.remove_vertices_by_mask(vertices_to_remove)

    return mesh

def apply_texture(mesh, image):
    # Convert the image to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    texture = o3d.geometry.Image(image)

    # Generate UV coordinates (simple planar mapping)
    mesh.compute_vertex_normals()
    mesh.triangle_uvs = o3d.utility.Vector2dVector(np.array([[0, 0], [1, 0], [1, 1], [0, 1]]))  # Example UVs
    mesh.textures = [texture]

    return mesh

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python image_processing.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    model_url = reconstruct_3D(image_path)

    if model_url:
        print(json.dumps({"modelUrl": model_url}))
    else:
        print(json.dumps({"error": "Failed to process image"}))
