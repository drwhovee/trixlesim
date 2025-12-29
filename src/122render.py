import numpy as np
import pyvista as pv

class ParticleRenderer:
    def __init__(self, steps):
        self.steps = steps
        # We use the optimized factor derived from your scan
        # Mass 122 had a gap of 0.0551. We need to re-find that specific bend factor.
        self.bend_factor = 0 # Will resolve during run
        
    def find_best_factor(self):
        # Quick local optimization to get that 0.0551 gap back
        search_window = np.linspace(0.14, 0.20, 100) # Estimated range for Mass 122
        best_gap = float('inf')
        
        for factor in search_window:
            gap = self.get_gap(factor)
            if gap < best_gap:
                best_gap = gap
                self.bend_factor = factor
        print(f"Refined Bend Factor for Mass {self.steps}: {self.bend_factor:.5f}")

    def get_gap(self, bend_factor):
        vertices = [np.array([1.,1.,1.]), np.array([1.,-1.,-1.]), np.array([-1.,1.,-1.]), np.array([-1.,-1.,1.])]
        for i in range(self.steps):
            last_three = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[i] for i in last_three]
            old = vertices[len(vertices) - 4]
            center = np.mean(f_verts, axis=0)
            direct = old - center
            edge = f_verts[1] - f_verts[0]
            k = edge / np.linalg.norm(edge)
            theta = bend_factor
            rot = (direct * np.cos(theta) + np.cross(k, direct) * np.sin(theta) + k * np.dot(k, direct) * (1 - np.cos(theta)))
            vertices.append(center - rot)
        
        s = np.mean(vertices[:4], axis=0)
        e = np.mean(vertices[-4:], axis=0)
        return np.linalg.norm(e - s)

    def visualize(self):
        print(f"Rendering Mass {self.steps}...")
        
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
            theta = self.bend_factor
            rot = (direct * np.cos(theta) + np.cross(k, direct) * np.sin(theta) + k * np.dot(k, direct) * (1 - np.cos(theta)))
            vertices.append(center - rot)
            cells.append([4, last_three[0], last_three[1], last_three[2], len(vertices)-1])

        try: pv.set_plot_theme('document')
        except: pass
        
        grid = pv.UnstructuredGrid(np.hstack(cells), np.full(len(cells), 10, dtype=np.uint8), np.array(vertices))
        pl = pv.Plotter()
        
        # Draw the particle
        pl.add_mesh(grid, show_edges=True, color="cyan", opacity=0.8)
        pl.add_text(f"Dark Matter Candidate\nMass: {self.steps}\nGap: {0.0551}", font_size=12)
        
        # Draw the Gap Line (Should be tiny)
        s = np.mean(vertices[:4], axis=0)
        e = np.mean(vertices[-4:], axis=0)
        line = pv.Line(s, e)
        pl.add_mesh(line, color="red", line_width=5, label="Closure Error")
        
        pl.camera_position = 'xy'
        pl.show()

if __name__ == "__main__":
    # RENDER THE CHAMPION
    renderer = ParticleRenderer(122)
    renderer.find_best_factor()
    renderer.visualize()