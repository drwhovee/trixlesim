import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

class QuarkScanner:
    def __init__(self):
        self.steps = 1836
        # The Proton Resonance we found earlier
        self.bend_factor = 0.01520 
        self.vertices = []
        
    def generate_proton(self):
        print("Generating Proton Lattice...")
        self.vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        for i in range(self.steps):
            last_three_indices = len(self.vertices) - np.array([3, 2, 1])
            face_verts = [self.vertices[idx] for idx in last_three_indices]
            
            old_vertex = self.vertices[len(self.vertices) - 4]
            face_center = np.mean(face_verts, axis=0)
            direction = old_vertex - face_center
            
            # Hinge Logic
            edge_vector = face_verts[1] - face_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = self.bend_factor
            
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            new_vertex = face_center - v_rot 
            self.vertices.append(new_vertex)

    def analyze_structure(self):
        print("Analyzing Internal Structure...")
        points = np.array(self.vertices)
        
        # 1. Find the Center of Mass of the ring
        center_of_mass = np.mean(points, axis=0)
        
        # 2. Measure distance of every point from the center
        distances = []
        for p in points:
            d = np.linalg.norm(p - center_of_mass)
            distances.append(d)
            
        # 3. Smooth the data (Rolling average) to remove "Digital Jitter"
        # We want to see the macro-shape, not the jagged triangle edges
        window_size = 50
        smoothed = np.convolve(distances, np.ones(window_size)/window_size, mode='valid')
        
        return smoothed

    def plot_quarks(self, data):
        # Setup the Graph
        plt.figure(figsize=(10, 6))
        plt.plot(data, color='blue', linewidth=2, label='Lattice Radius')
        
        plt.title(f"Proton Internal Geometry (N={self.steps})")
        plt.xlabel("Lattice Step (0 - 1836)")
        plt.ylabel("Radial Distance (Structure)")
        plt.grid(True, alpha=0.3)
        
        # Draw lines for where Quarks *should* be (every 1/3rd)
        plt.axvline(x=1836/3, color='red', linestyle='--', alpha=0.5, label='Quark Boundary 1')
        plt.axvline(x=1836*2/3, color='red', linestyle='--', alpha=0.5, label='Quark Boundary 2')
        
        plt.legend()
        print("Opening Analysis Graph...")
        plt.show()

if __name__ == "__main__":
    scanner = QuarkScanner()
    scanner.generate_proton()
    structure_data = scanner.analyze_structure()
    scanner.plot_quarks(structure_data)