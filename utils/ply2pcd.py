import os
import open3d as o3d

def ply_to_pcd(input_file, output_file):
    # Cargar el archivo PLY
    pcd = o3d.io.read_point_cloud(input_file)
    
    # Guardar como archivo PCD
    o3d.io.write_point_cloud(output_file, pcd)
    print(f"El archivo PCD se ha guardado en: {output_file}")

if __name__ == "__main__":
    # Ruta de la carpeta de entrada y salida
    input_folder = "../data/7-scenes-redkitchen"
    output_folder = "../data/7-scenes-redkitchen"

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Listar todos los archivos en la carpeta de entrada
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".ply"):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, file_name[:-4] + ".pcd")  # Cambiar la extensión a .pcd
            ply_to_pcd(input_file, output_file)
