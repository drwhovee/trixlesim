import numpy as np
import pyvista as pv

class ElectronScanner:
    def __init__(self, target_steps=136):
        self.steps = target_steps
        self.best_factor = 0
        
    def generate_lattice(self, bend_factor):
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
            
            # Hinge Logic
            edge_vector = face_verts[1] - face_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = bend_factor
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            new_vertex = face_center - v_rot 
            vertices.append(new_vertex)
            
        start_pt = np.mean(vertices[:4], axis=0)
        end_pt = np.mean(vertices[-4:], axis=0)
        
        return np.linalg.norm(end_pt - start_pt)

    def find_resonance(self):
        print(f"--- WIDE SCAN INITIATED (136 Steps) ---")
        
        # SEARCH RANGE: 0.05 (Weak) to 0.50 (Strong)
        # We check 500 different frequencies
        search_space = np.linspace(0.05, 0.50, 500)
        
        best_dist = float('inf')
        best_val = 0
        
        count = 0
        for factor in search_space:
            count += 1
            dist = self.generate_lattice(factor)
            
            # Print a 'Heartbeat' every 50 checks so you know it's alive
            if count % 50 == 0:
                print(f"  ...scanning {factor:.3f} (Current Best Gap: {best_dist:.2f})")
            
            if dist < best_dist:
                best_dist = dist
                best_val = factor
                print(f"  -> NEW RECORD: Factor {factor:.5f} | Gap: {dist:.2f}")

        print(f"\n--- RESULTS ---")
        print(f"Best Bend Factor: {best_val:.5f}")
        print(f"Final Gap: {best_dist:.2f}")
        
        self.visualize(best_val)

    def visualize(self, factor):
        print("Rendering visualization...")
        vertices = [np.array([1.,1.,1.]), np.array([1.,-1.,-1.]), np.array([-1.,1.,-1.]), np.array([-1.,-1.,1.])]
        cells = [[4,0,1,2,3]]
        
        for i in range(self.steps):
            last_three = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[i] for i in last_three]
            old = vertices[len(vertices) - 4]
            center = np.mean(f_verts, axis=0)
            direct = old - center
            edge = f_verts[1] - f_verts[0]
            k = edge / np.linalg.norm(edge)
            
            theta = factor
            rot = (direct * np.cos(theta) + np.cross(k, direct) * np.sin(theta) + k * np.dot(k, direct) * (1 - np.cos(theta)))
            vertices.append(center - rot)
            cells.append([4, last_three[0], last_three[1], last_three[2], len(vertices)-1])

        try: pv.set_plot_theme('document')
        except: pass
        
        grid = pv.UnstructuredGrid(np.hstack(cells), np.full(len(cells), 10, dtype=np.uint8), np.array(vertices))
        pl = pv.Plotter()
        pl.add_mesh(grid, show_edges=True, color="yellow", opacity=0.8)
        pl.add_text(f"Electron (136)\nBend: {factor:.5f}", font_size=12)
        
        # Show the Gap Line
        start_pt = np.mean(vertices[:4], axis=0)
        end_pt = np.mean(vertices[-4:], axis=0)
        line = pv.Line(start_pt, end_pt)
        pl.add_mesh(line, color="red", line_width=4, label="Gap")
        
        pl.camera_position = 'xy'
        pl.show()

if __name__ == "__main__":
    ElectronScanner().find_resonance()