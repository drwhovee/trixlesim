import numpy as np
import pyvista as pv

class TrixleLattice:
    def __init__(self, num_tetrahedra=30):
        self.num_steps = num_tetrahedra
        self.vertices = []
        self.cells = []
        self.edges = []
        
        # Build the universe immediately
        self._genesis()

    def _genesis(self):
        """
        Generates the Boerdijk-Coxeter helix with Curvature (Gravity/Strain).
        """
        print(f"--- GENESIS INITIATED ---")
        
        # 1. Base Regular Tetrahedron (vertices at corners of a cube)
        v = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        self.vertices.extend(v)
        
        # The first cell connects vertices [0, 1, 2, 3]
        self.cells.append([4, 0, 1, 2, 3]) 

        # --- PHYSICS PARAMETER: LATTICE CURVATURE ---
        # 0.0 = Straight Vacuum (Infinite Line)
        # 0.0035 = The specific strain required to curve 1836 steps into a loop
        bend_factor = 0.0035 

        # 2. Iteratively Stack with Curvature
        for i in range(self.num_steps):
            # Find the last 3 vertices added
            last_three_indices = len(self.vertices) - np.array([3, 2, 1])
            face_verts = [self.vertices[idx] for idx in last_three_indices]
            
            # The vertex to reflect is the one BEFORE those three
            old_vertex = self.vertices[len(self.vertices) - 4]
            face_center = np.mean(face_verts, axis=0)
            
            # Vector from center to old vertex (this is what we reflect)
            direction = old_vertex - face_center
            
            # --- APPLY THE BEND ---
            # To simulate lattice strain, we rotate the reflection vector slightly.
            # We rotate around the "Normal" of the current face.
            
            # Calculate Face Normal
            v1 = face_verts[1] - face_verts[0]
            v2 = face_verts[2] - face_verts[0]
            normal = np.cross(v1, v2)
            # Normalize the vector to length 1
            normal = normal / np.linalg.norm(normal) 
            
            # Rodrigues' Rotation Formula
            # This rotates the 'direction' vector around 'normal' by 'bend_factor'
            theta = bend_factor # Radians
            k = normal
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            # Calculate new vertex position: Face Center - Rotated Vector
            new_vertex = face_center - v_rot 
            
            # Add new point to universe
            self.vertices.append(new_vertex)
            
            # Connect the new point to the previous 3 to form a tetrahedron
            new_idx = len(self.vertices) - 1
            idx1, idx2, idx3 = last_three_indices
            self.cells.append([4, idx1, idx2, idx3, new_idx])
            
        print(f"Universe created with {len(self.cells)} tetrahedra.")
        print(f"Lattice Length: {len(self.vertices)} vertices.")

    def visualize(self, show_edges=True, show_volumes=True):
        """
        Renders the Trixle Universe using PyVista.
        """
        # Set the visual theme globally to avoid version errors
        try:
            pv.set_plot_theme('document')
        except AttributeError:
            pass

        # Prepare data for PyVista
        points = np.array(self.vertices)
        cell_stream = np.hstack(self.cells)
        cell_types = np.full(len(self.cells), 10, dtype=np.uint8)
        
        # Create the grid object
        grid = pv.UnstructuredGrid(cell_stream, cell_types, points)

        # Initialize the plotter
        plotter = pv.Plotter() 
        plotter.add_text(f"Trixle Proton: {self.num_steps} Steps", font_size=12)

        # 1. Render the Lattice Volumes (Glassy look)
        if show_volumes:
            plotter.add_mesh(grid, show_edges=False, color="cyan", opacity=0.3, label="Lattice Tension")

        # 2. Render the Lattice Skeleton (The Edges)
        if show_edges:
            edges = grid.extract_all_edges()
            plotter.add_mesh(edges, color="black", line_width=1, label="Geometric Web")

        # 3. Visualize a 'Dark Matter' Loop (Red Ring)
        # We place this in the middle of the chain
        mid = len(self.vertices) // 2
        # Ensure we don't go out of bounds if the chain is short
        if mid + 3 < len(self.vertices):
            loop_indices = [mid, mid+1, mid+2, mid+3, mid]
            loop_points = points[loop_indices]
            
            path = pv.Spline(loop_points, 100)
            plotter.add_mesh(path, color="red", line_width=5, render_lines_as_tubes=True, label="Energy Loop")

        plotter.add_legend()
        plotter.show_grid()
        plotter.camera_position = 'xy'
        
        print("Opening visualization window...")
        plotter.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # We set this to 1836 to look for the Proton Loop
    steps = 1836 
    
    universe = TrixleLattice(num_tetrahedra=steps)
    universe.visualize()