import numpy as np
import pyvista as pv

class IsotopeScanner:
    def __init__(self):
        self.results = []

    def get_closure_error(self, steps, bend_factor):
        # FAST GENERATOR (No cell data, just vertices)
        # We assume the "Hinge" logic we validated earlier
        vertices = [np.array([1.,1.,1.]), np.array([1.,-1.,-1.]), np.array([-1.,1.,-1.]), np.array([-1.,-1.,1.])]
        
        # Pre-calculate hinge vectors for standard orientation to speed up? 
        # No, geometry changes every step. Must compute loop.
        
        for i in range(steps):
            last_three_indices = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[idx] for idx in last_three_indices]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(f_verts, axis=0)
            direction = old_vertex - face_center
            
            edge_vector = f_verts[1] - f_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = bend_factor
            
            # Rotation
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            vertices.append(face_center - v_rot)
            
        start_pt = np.mean(vertices[:4], axis=0)
        end_pt = np.mean(vertices[-4:], axis=0)
        return np.linalg.norm(end_pt - start_pt)

    def optimize_mass(self, steps):
        # We know Bend ~ 21/Steps based on Electron data
        # We search a tight window around that estimation
        estimate = 21.0 / steps
        search_window = np.linspace(estimate * 0.5, estimate * 1.5, 40)
        
        best_gap = float('inf')
        
        # Coarse Scan
        for factor in search_window:
            gap = self.get_closure_error(steps, factor)
            if gap < best_gap:
                best_gap = gap
                best_factor = factor
        
        # Fine Scan (Zoom in on the best result)
        fine_window = np.linspace(best_factor * 0.95, best_factor * 1.05, 20)
        for factor in fine_window:
            gap = self.get_closure_error(steps, factor)
            if gap < best_gap:
                best_gap = gap
        
        return best_gap

    def run_sweep(self):
        print("--- INITIATING DARK MATTER SWEEP (Mass 80 - 250) ---")
        print("Searching for stable resonant loops...")
        
        # Sweep range
        mass_range = range(80, 251)
        
        for mass in mass_range:
            gap = self.optimize_mass(mass)
            self.results.append((mass, gap))
            
            # Visual heartbeat
            if mass % 10 == 0:
                print(f"  Scanning Mass {mass}... (Gap: {gap:.2f})")

        # SORT BY STABILITY (Lowest Gap)
        self.results.sort(key=lambda x: x[1])
        
        print("\n--- TOP 10 STABLE ISOTOPES ---")
        print(f"{'MASS':<10} | {'CLOSURE ERROR':<15} | {'STATUS'}")
        print("-" * 40)
        
        for i in range(15): # Show top 15
            mass, gap = self.results[i]
            status = "STABLE" if gap < 0.5 else "UNSTABLE"
            print(f"{mass:<10} | {gap:<15.4f} | {status}")

        # Check for our predictions
        print("\n--- HYPOTHESIS CHECK ---")
        self.check_mass(104)
        self.check_mass(204)
        
    def check_mass(self, target):
        # Find the specific result for a target mass
        for m, g in self.results:
            if m == target:
                status = "CONFIRMED" if g < 0.5 else "BUSTED"
                print(f"Mass {target}: Gap {g:.4f} -> {status}")

if __name__ == "__main__":
    scanner = IsotopeScanner()
    scanner.run_sweep()