import numpy as np
import matplotlib.pyplot as plt

class AlphaScanner:
    """
    Scans the Trixle Lattice around the N=136 (Electron) region to investigate
    the geometric origin of the Fine Structure Constant (1/137).
    
    Hypothesis:
    - Mass (Particle Stability) maximizes at N=136.
    - Charge (Torsional Stress) minimizes at N=137.
    - Alpha is the coupling oscillation between Mass-Stable and Torsion-Stable states.
    """
    def __init__(self):
        self.bend_factor = 0.1555 # The Electron Resonance Bend
        
    def get_torsion_and_gap(self, steps):
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        # Build the chain
        for i in range(steps):
            last_three = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[idx] for idx in last_three]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(f_verts, axis=0)
            direction = old_vertex - face_center
            edge_vector = f_verts[1] - f_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = self.bend_factor
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            vertices.append(face_center - v_rot)
            
        # 1. MEASURE CLOSURE GAP (Mass Potential)
        start_center = np.mean(vertices[:4], axis=0)
        end_center = np.mean(vertices[-4:], axis=0)
        gap = np.linalg.norm(end_center - start_center)

        # 2. MEASURE TORSION (Magnetic Potential)
        def get_normal(indices):
            p1, p2, p3 = vertices[indices[0]], vertices[indices[1]], vertices[indices[2]]
            v1 = p2 - p1
            v2 = p3 - p1
            n = np.cross(v1, v2)
            return n / np.linalg.norm(n)

        n_start = get_normal([0, 1, 2])
        n_end = get_normal([len(vertices)-3, len(vertices)-2, len(vertices)-1])
        
        dot = np.clip(np.dot(n_start, n_end), -1.0, 1.0)
        torsion_degrees = np.degrees(np.arccos(dot))
        
        return gap, torsion_degrees

    def run_scan(self):
        print("--- FINE STRUCTURE SCAN (130-145) ---")
        ns, gaps, torsions = [], [], []
        
        for n in range(130, 145):
            gap, torsion = self.get_torsion_and_gap(n)
            ns.append(n)
            gaps.append(gap)
            torsions.append(torsion)
            
        # Plotting
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        ax1.set_xlabel('Lattice Steps (N)')
        ax1.set_ylabel('Closure Gap (Mass)', color='blue', fontweight='bold')
        ax1.plot(ns, gaps, color='blue', marker='o', linewidth=2, label='Mass (Gap)')
        ax1.tick_params(axis='y', labelcolor='blue')
        
        ax2 = ax1.twinx() 
        ax2.set_ylabel('Torsional Twist (Degrees)', color='red', fontweight='bold')
        ax2.plot(ns, torsions, color='red', marker='x', linestyle='--', linewidth=2, label='Charge (Torsion)')
        ax2.tick_params(axis='y', labelcolor='red')
        
        plt.title('The Origin of Alpha: Mass (136) vs Magnetism (137)')
        plt.grid(True, alpha=0.3)
        plt.axvline(x=136, color='green', linestyle=':', label='Electron Mass Peak')
        plt.axvline(x=137, color='purple', linestyle=':', label='Magnetic Relaxation')
        
        plt.tight_layout()
        plt.savefig('results/alpha_structure_137.png')
        print("Graph saved to results/alpha_structure_137.png")
        plt.show()

if __name__ == "__main__":
    AlphaScanner().run_scan()