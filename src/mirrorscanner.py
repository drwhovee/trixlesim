import numpy as np
import pyvista as pv

class ChiralityTest:
    def __init__(self):
        self.steps = 1836
        
    def generate_lattice(self, bend_factor):
        # Standard Hinge Logic
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        for i in range(self.steps):
            last_three_indices = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[idx] for idx in last_three_indices]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(f_verts, axis=0)
            direction = old_vertex - face_center
            
            edge_vector = f_verts[1] - f_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            # THE VARIABLE: Positive or Negative Bend
            theta = bend_factor
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            vertices.append(face_center - v_rot)
            
        start_pt = np.mean(vertices[:4], axis=0)
        end_pt = np.mean(vertices[-4:], axis=0)
        return np.linalg.norm(end_pt - start_pt)

    def run_comparison(self):
        print("--- CHIRALITY TEST (MATTER VS ANTIMATTER) ---")
        
        # 1. Scan MATTER (Positive Bend)
        print("\nScanning MATTER (Right-Handed Twist)...")
        # We look around the known proton value (0.015)
        pos_range = np.linspace(0.010, 0.020, 100)
        best_pos_gap = float('inf')
        best_pos_val = 0
        
        for f in pos_range:
            gap = self.generate_lattice(f)
            if gap < best_pos_gap:
                best_pos_gap = gap
                best_pos_val = f
        
        print(f"BEST MATTER PROTON:")
        print(f"  Bend: {best_pos_val:.5f}")
        print(f"  Stability Gap: {best_pos_gap:.4f}")

        # 2. Scan ANTIMATTER (Negative Bend)
        print("\nScanning ANTIMATTER (Left-Handed Twist)...")
        # We look at the exact MIRROR range (-0.010 to -0.020)
        neg_range = np.linspace(-0.010, -0.020, 100)
        best_neg_gap = float('inf')
        best_neg_val = 0
        
        for f in neg_range:
            gap = self.generate_lattice(f)
            if gap < best_neg_gap:
                best_neg_gap = gap
                best_neg_val = f
                
        print(f"BEST ANTIMATTER PROTON:")
        print(f"  Bend: {best_neg_val:.5f}")
        print(f"  Stability Gap: {best_neg_gap:.4f}")
        
        # 3. THE VERDICT
        print("\n--- CONCLUSION ---")
        diff = best_neg_gap - best_pos_gap
        if diff > 1.0:
            print(">>> ASYMMETRY DETECTED: Antimatter is UNSTABLE.")
            print(f"    (Antimatter is {best_neg_gap/best_pos_gap:.1f}x harder to create)")
            print("    Theory explains Baryon Asymmetry.")
        elif abs(diff) < 0.1:
            print(">>> SYMMETRY DETECTED: Matter and Antimatter are Identical.")
            print("    Theory does not explain Asymmetry.")
        else:
            print(">>> INCONCLUSIVE result.")

if __name__ == "__main__":
    ChiralityTest().run_comparison()