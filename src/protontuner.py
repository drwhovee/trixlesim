import numpy as np
import pyvista as pv

class ProtonTuner:
    def __init__(self, target_steps=1836):
        self.steps = target_steps
        self.best_factor = 0
        
    def generate_lattice(self, bend_factor):
        # FAST GENERATOR
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        for i in range(self.steps):
            last_three_indices = len(vertices) - np.array([3, 2, 1])
            face_verts = [vertices[idx] for idx in last_three_indices]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(face_verts, axis=0)
            direction = old_vertex - face_center
            
            # --- FIXED BEND LOGIC ---
            # Old Way (Broken): k = Face Normal (Parallel to direction)
            # New Way (Working): k = Edge Vector (Perpendicular to direction)
            
            # Use the first edge of the face as the hinge
            edge_vector = face_verts[1] - face_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector) # Normalize axis
            
            theta = bend_factor
            
            # Rodrigues rotation
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            new_vertex = face_center - v_rot 
            vertices.append(new_vertex)
            
        # DISTANCE CHECK
        start_point = np.mean(vertices[:4], axis=0)
        end_point = np.mean(vertices[-4:], axis=0)
        dist = np.linalg.norm(end_point - start_point)
        
        return dist

    def find_resonance(self):
        print(f"--- SCANNING FOR PROTON (Hinge Axis Fix) ---")
        
        # We need very small bends now because 'Hinge' is powerful
        search_space = np.linspace(0.001, 0.02, 100)
        
        best_dist = float('inf')
        best_val = 0
        
        for factor in search_space:
            dist = self.generate_lattice(factor)
            
            if dist < best_dist:
                best_dist = dist
                best_val = factor
                print(f"  -> Bending... Factor: {factor:.5f} | Gap: {dist:.2f}")

        print(f"\n--- WINNER ---")
        print(f"Magic Bend Factor: {best_val:.5f}")
        print(f"Final Gap: {best_dist:.2f}")
        self.best_factor = best_val

    def visualize_best(self):
        print("Rendering Proton...")
        
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        cells = []
        cells.append([4, 0, 1, 2, 3]) 
        
        bend_factor = self.best_factor
        
        for i in range(self.steps):
            last_three_indices = len(vertices) - np.array([3, 2, 1])
            face_verts = [vertices[idx] for idx in last_three_indices]
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(face_verts, axis=0)
            direction = old_vertex - face_center
            
            # Use Edge as Hinge
            edge_vector = face_verts[1] - face_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = bend_factor
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            new_vertex = face_center - v_rot 
            vertices.append(new_vertex)
            
            new_idx = len(vertices) - 1
            idx1, idx2, idx3 = last_three_indices
            cells.append([4, idx1, idx2, idx3, new_idx])

        # PLOT
        try:
            pv.set_plot_theme('document')
        except:
            pass

        points = np.array(vertices)
        cell_stream = np.hstack(cells)
        cell_types = np.full(len(cells), 10, dtype=np.uint8)
        grid = pv.UnstructuredGrid(cell_stream, cell_types, points)

        plotter = pv.Plotter() 
        plotter.add_text(f"Proton Loop\nBend: {self.best_factor:.5f}", font_size=12)

        plotter.add_mesh(grid, show_edges=False, color="cyan", opacity=0.6)
        edges = grid.extract_all_edges()
        plotter.add_mesh(edges, color="black", line_width=1, opacity=0.3)

        # Connection line
        start_pt = np.mean(vertices[:4], axis=0)
        end_pt = np.mean(vertices[-4:], axis=0)
        line = pv.Line(start_pt, end_pt)
        plotter.add_mesh(line, color="red", line_width=5, label="Gap Closure")

        plotter.show_grid()
        plotter.show()

if __name__ == "__main__":
    tuner = ProtonTuner(target_steps=1836)
    tuner.find_resonance()
    tuner.visualize_best()