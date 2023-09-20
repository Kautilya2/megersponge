import trimesh
import pyrender
import numpy as np

def create_menger_sponge(level, size, translation):
    if level == 0:
        # Create a small cube at the given translation
        cube = trimesh.creation.box(extents=size)
        cube.apply_translation(translation)
        return cube
    else:
        # Calculate the new size and translation for smaller cubes
        new_size = size / 3.0
        new_translation = translation - new_size

        # Create the Menger sponge by recursively creating smaller cubes
        sponge = trimesh.Trimesh()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if not (i == 1 and j == 1) and not (i == 1 and k == 1) and not (j == 1 and k == 1):
                        sub_cube = create_menger_sponge(level - 1, new_size, new_translation + np.array([i, j, k]) * new_size)
                        sponge += sub_cube

        return sponge

# Create a Menger sponge with a certain level of recursion
level = 4
size = np.array([1.0, 1.0, 1.0])
sponge = create_menger_sponge(level, size, np.array([0.0, 0.0, 0.0]))

# Create a scene and add the Menger sponge to it
scene = pyrender.Scene()
scene.add(pyrender.Mesh.from_trimesh(sponge))



# Create a viewer to render the scene
viewer = pyrender.Viewer(scene, use_raymond_lighting=True)
# Keep the viewer open until it's manually closed
viewer.render_lock.acquire()
viewer.render_scene()
viewer.render_lock.release()
while not viewer.should_quit:
    viewer.render_lock.acquire()
    viewer.render_scene()
    viewer.render_lock.release()
