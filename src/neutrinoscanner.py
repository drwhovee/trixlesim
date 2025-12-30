import numpy as np

class NeutrinoScanner:
    def __init__(self):
        # We assume the neutrino uses the standard vacuum curvature
        self.bend_factor = 0.0 
        
    def check_loop(self, steps):
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
            
            # Neutrinos might be "Relaxed" (Zero Bend)
            theta = 0.0 
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            vertices.append(face_center - v_rot)
            
        start_center = np.mean(vertices[:4], axis=0)
        end_center = np.mean(vertices[-4:], axis=0)
        gap = np.linalg.norm(end_center - start_center)
        
        return gap

    def scan(self):
        print("--- NEUTRINO CANDIDATE SCAN (N=3 to N=12) ---")
        best_n = 0
        best_gap = 100
        
        for n in range(3, 13):
            gap = self.check_loop(n)
            print(f"N={n}: Gap {gap:.4f}")
            if gap < best_gap:
                best_gap = gap
                best_n = n
                
        print("-" * 30)
        print(f"BEST CANDIDATE: N={best_n}")
        if best_n == 5:
            print("Theory: The 'Pentagonal' Void.")
        elif best_n == 6:
            print("Theory: The 'Hexagonal' Closure.")

if __name__ == "__main__":
    NeutrinoScanner().scan()