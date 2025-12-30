import numpy as np
import pyvista as pv
import time

class QuantumFlow:
    def __init__(self):
        self.plotter = pv.Plotter(title="Trixle Theory: Soliton Gap Propagation")
        self.bend_factor = 0.015  
        self.tube_length = 400    
        
        self.playing = True
        self.frame = 0
        self.tube_mesh = None
        self.scalars = None
        
        self.setup_scene()
        
    def generate_path(self):
        """ Generates the Boerdijk-Coxeter Helix Points """
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        path = []
        for i in range(self.tube_length):
            last_three = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[idx] for idx in last_three]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(f_verts, axis=0)
            
            path.append(face_center)
            
            direction = old_vertex - face_center
            edge_vector = f_verts[1] - f_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = self.bend_factor
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            vertices.append(face_center - v_rot)
            
        return np.array(path)

    def update_animation(self):
        if not self.playing:
            return

        # 1. CALCULATE STATE
        # We are not moving an object. We are calculating the 'Stress Index'
        # of the lattice at this moment in time.
        idx = self.frame % self.tube_length
        
        # 2. RESET FIELD (The Vacuum)
        # Set background energy to 0.1 (Blue/Cold)
        self.scalars[:] = 0.1
        
        # 3. EXCITE THE FIELD (The Pulse)
        # We modify the scalar values of the lattice nodes directly.
        # This represents the "Twist" passing from neighbor to neighbor.
        pulse_width = 20
        for i in range(-pulse_width, pulse_width):
            target_idx = (idx + i) % self.tube_length
            
            # Create a Bell Curve of intensity (The Soliton shape)
            intensity = 1.0 - (abs(i) / pulse_width)
            if intensity < 0: intensity = 0
            
            # Update the scalar array
            self.scalars[target_idx] = 0.1 + (intensity * 2.0) 

        # 4. MAP DATA TO VISUALS
        # Expand the path scalars to match the tube mesh resolution
        mesh_points = self.tube_mesh.n_points
        expanded_scalars = np.repeat(self.scalars, mesh_points // self.tube_length + 1)[:mesh_points]
        
        # Inject the new data into the existing static mesh
        self.tube_mesh.point_data['Energy'][:] = expanded_scalars
        
        self.plotter.add_text(
            f"LATTICE STATE: Excitation at Node {idx}", 
            name='status', 
            position='upper_left', 
            color='white', 
            font_size=12
        )
        
        self.frame += 1
        time.sleep(0.01)

    def setup_scene(self):
        # 1. Generate Static Geometry (The Vacuum)
        print("Generating Vacuum Lattice...")
        path_points = self.generate_path()
        spline = pv.Spline(path_points, len(path_points) * 1)
        self.tube_mesh = spline.tube(radius=0.5, n_sides=12)
        
        # 2. Prepare Data Arrays
        self.scalars = np.zeros(self.tube_length)
        
        # Initialize the mesh with the data structure
        mesh_points = self.tube_mesh.n_points
        expanded_scalars = np.repeat(self.scalars, mesh_points // self.tube_length + 1)[:mesh_points]
        self.tube_mesh.point_data['Energy'] = expanded_scalars
        
        # 3. Render
        # Use 'plasma' colormap: Blue = Low Energy, Yellow = High Energy
        # Use 'wireframe' to emphasize that it is a lattice structure, not a solid pipe
        self.plotter.add_mesh(
            self.tube_mesh, 
            scalars='Energy',
            cmap='plasma', 
            style='wireframe',    
            line_width=3,        
            show_scalar_bar=False,
            lighting=False       
        )
        
        # 4. High Contrast Environment
        self.plotter.set_background('#202020') # Dark Grey (High visibility)
        self.plotter.add_axes()
        self.plotter.reset_camera()            
        self.plotter.camera.zoom(1.2)
        
        print("Starting Simulation...")
        print("Visualizing Lattice Excitation (No Particles)...")
        
        self.plotter.show(interactive_update=True)
        
        while True:
            try:
                self.update_animation()
                self.plotter.update()
            except AttributeError:
                break
            except Exception as e:
                print(f"Error: {e}")
                break

if __name__ == "__main__":
    QuantumFlow()