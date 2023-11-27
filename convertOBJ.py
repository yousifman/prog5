import json

def parse_obj_file(file_path):
    vertices = []
    normals = []
    uvs = []  # New list for texture coordinates
    triangles = []

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                vertex_data = list(map(float, line[2:].strip().split()))
                scaled_vertex = [coord * (1/100) for coord in vertex_data]
                vertices.append(scaled_vertex)
            elif line.startswith('vn '):
                normal_data = list(map(float, line[3:].strip().split()))
                normals.append(normal_data)
            elif line.startswith('vt '):  # Parse texture coordinates
                uv_data = list(map(float, line[3:].strip().split()[:2]))  # Discard the third value
                uvs.append(uv_data)
            elif line.startswith('f '):
                face_data = line[2:].strip().split()
                face_indices = [int(data.split('/')[0]) - 1 for data in face_data]
                triangles.append(face_indices)

    return vertices, normals, uvs, triangles  # Include uvs in the return

def translate_to_point(vertices, point, scale_factor=1.0):  # Add a scale_factor parameter
    scaled_vertices = [[v[0] * scale_factor + point[0], v[1] * scale_factor + point[1], v[2] * scale_factor + point[2]] for v in vertices]
    return scaled_vertices

def mirror_xy_plane(vertices):
    mirrored_vertices = [[v[0], v[1], -v[2]] for v in vertices]
    return mirrored_vertices

def mirror_normals(normals):
    mirrored_normals = [[n[0], n[1], -n[2]] for n in normals]
    return mirrored_normals

# Modify the create_json function to include uvs
def create_json(vertices, normals, uvs, triangles):
    data = {
        "material": {"ambient": [0.1, 0.1, 0.1], "diffuse": [0.9, 0.9, 0.9], "specular": [0.3, 0.3, 0.3], "n": 11, "alpha": 1.0, "texture": "Portal_Companion_Cube.png"},
        "vertices": vertices,
        "normals": normals,
        "uvs": uvs,
        "triangles": triangles
    }

    return [data]

def obj_to_json(obj_file_path, output_json_path, scale_factor=1.0):  # Add a scale_factor parameter
    vertices, normals, uvs, triangles = parse_obj_file(obj_file_path)
    translated_vertices = translate_to_point(vertices, [1/2, 1/8, -0.5], scale_factor=scale_factor)  # Pass scale_factor
    mirrored_vertices = mirror_xy_plane(translated_vertices)
    mirrored_normals = mirror_normals(normals)
    data = create_json(mirrored_vertices, mirrored_normals, uvs, triangles)

    with open(output_json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage with a scale factor of 2.0
obj_file_path = "Cube.obj"  # Replace with the path to your .obj file
output_json_path = "Cube.json"  # Replace with the desired output JSON file path

obj_to_json(obj_file_path, output_json_path, scale_factor=100.0)
