import numpy as np
import pyvista as pv

class LatticeTapestry:
    def __init__(self):
        self.plotter = pv.Plotter(title="Trixle Theory: The Vacuum Tapestry")
        self.bend_factor = 0.015  # The fundamental grain
        self.strand_length = 300  # Length of the threads
        # How far apart the strands are packed
        self.packing_radius = 1.6 
        
        self.setup_scene()
        
    def generate_helix_path(self, start_offset):
        """ 
        Generates a standard BC-helix, shifted by a starting offset vector.
        """
        # Standard starting tetrahedron
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        # Shift initial vertices by the offset
        offset_vec = np.array(start_offset)
        vertices = [v + offset_vec for v in vertices]
        
        path = []
        
        for i in range(self.strand_length):
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

    def setup_scene(self):
        print("Weaving the Lattice Tapestry...")
        
        # Define packing arrangement (A central strand surrounded by 6 hex neighbors)
        r = self.packing_radius
        # Using sin/cos for a hexagonal packing pattern around the Z-axis roughly
        offsets = [
            (0, 0, 0), # Center
            (r, 0, 0),
            (-r, 0, 0),
            (r * np.cos(np.pi/3), r * np.sin(np.pi/3), 0),
            (r * np.cos(np.pi/3), -r * np.sin(np.pi/3), 0),
            (-r * np.cos(np.pi/3), r * np.sin(np.pi/3), 0),
            (-r * np.cos(np.pi/3), -r * np.sin(np.pi/3), 0),
        ]
        
        colors = ['cyan', 'blue', 'blue', 'teal', 'teal', 'dodgerblue', 'dodgerblue']

        # Generate and add each strand
        for i, offset in enumerate(offsets):
            print(f"Generating Strand {i+1}/{len(offsets)}...")
            path = self.generate_helix_path(offset)
            
            # Create the visual tube
            spline = pv.Spline(path, len(path) * 2)
            # Radius 0.5 ensures they nestle without totally overlapping
            tube = spline.tube(radius=0.5, n_sides=16)
            
            # Add to scene with wireframe style to see inside the structure
            self.plotter.add_mesh(
                tube, 
                style='wireframe', 
                color=colors[i % len(colors)], 
                opacity=0.6, # Semi-transparent to see depth
                line_width=1
            )

        # Aesthetics
        self.plotter.set_background('#050505') # Almost black
        self.plotter.add_text("The Trixle Vacuum Lattice\n(Hexagonal Packing of BC-Helices)", 
                              position='upper_left', color='white', font_size=10)
        
        # Orient the camera to look down the "barrels" initially
        self.plotter.view_yz()
        
        # FIX: Set the roll property directly (don't call it)
        self.plotter.camera.roll += 90 
        self.plotter.camera.zoom(1.5)

        print("Visualization Ready. Use mouse to rotate and zoom into the structure.")
        self.plotter.show()

if __name__ == "__main__":
    LatticeTapestry()