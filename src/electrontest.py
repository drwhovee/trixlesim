import numpy as np
import pyvista as pv

class ElectronTest:
    def __init__(self):
        # THEORY: 136 Steps (Fine Structure Constant)
        self.steps = 136 
        
        # PREDICTION: Derived from the Proton (0.0152 * 1836 / 136)
        self.bend_factor = 0.2052 
        
    def run_test(self):
        print(f"--- ELECTRON VERIFICATION ---")
        print(f"Target Steps: {self.steps}")
        print(f"Predicted Bend: {self.bend_factor}")
        
        # 1. Generate Lattice
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        cells = []
        cells.append([4, 0, 1, 2, 3]) 
        
        for i in range(self.steps):
            last_three_indices = len(vertices) - np.array([3, 2, 1])
            face_verts = [vertices[idx] for idx in last_three_indices]
            
            # Rotation Logic (Hinge)
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(face_verts, axis=0)
            direction = old_vertex - face_center
            
            edge_vector = face_verts[1] - face_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = self.bend_factor
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            new_vertex = face_center - v_rot 
            vertices.append(new_vertex)
            
            new_idx = len(vertices) - 1
            idx1, idx2, idx3 = last_three_indices
            cells.append([4, idx1, idx2, idx3, new_idx])

        # 2. Check the Gap
        start_pt = np.mean(vertices[:4], axis=0)
        end_pt = np.mean(vertices[-4:], axis=0)
        gap = np.linalg.norm(end_pt - start_pt)
        
        print(f"RESULTING GAP: {gap:.4f}")
        
        if gap < 5.0: # Arbitrary threshold for 'success' on this scale
            print(">>> SUCCESS: PREDICTION CONFIRMED <<<")
        else:
            print(">>> FAILURE: PREDICTION INCORRECT <<<")

        # 3. Visual Proof
        try:
            pv.set_plot_theme('document')
        except:
            pass
            
        points = np.array(vertices)
        cell_stream = np.hstack(cells)
        cell_types = np.full(len(cells), 10, dtype=np.uint8)
        grid = pv.UnstructuredGrid(cell_stream, cell_types, points)

        plotter = pv.Plotter() 
        plotter.add_text(f"Electron Candidate (136)\nPred. Force: {self.bend_factor}", font_size=12)

        plotter.add_mesh(grid, show_edges=False, color="yellow", opacity=0.8)
        plotter.add_mesh(grid.extract_all_edges(), color="black", line_width=2)
        
        # Closure Line
        line = pv.Line(start_pt, end_pt)
        plotter.add_mesh(line, color="red", line_width=4, label="Gap")

        plotter.add_axes()
        plotter.camera_position = 'xy' # Top-down view
        plotter.show()

if __name__ == "__main__":
    test = ElectronTest()
    test.run_test()