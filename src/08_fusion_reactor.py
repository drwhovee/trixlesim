import numpy as np
import pyvista as pv
import time

class FusionReactor:
    def __init__(self):
        self.plotter = pv.Plotter(title="Trixle Theory: Hydrogen Fusion Event")
        self.bend_factor = 0.015  # Proton curvature
        
        # We simulate two protons
        self.proton_size = 1836
        self.actor_a = None
        self.actor_b = None
        self.actor_he = None
        
        # Animation State
        self.separation = 4.0 # Starting distance
        self.merged = False
        self.flash_intensity = 0.0
        self.frame_count = 0
        
        self.setup_scene()
        
    def generate_proton_loop(self, steps):
        """ Generates a single Proton Loop (Figure-8 Topology) """
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        path = []
        for i in range(steps):
            last_three = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[idx] for idx in last_three]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(f_verts, axis=0)
            
            # Apply a twist modulation to create the Figure-8 lobes
            modulation = 1.0 + 0.05 * np.sin(i * 4 * np.pi / steps)
            
            direction = old_vertex - face_center
            edge_vector = f_verts[1] - f_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            theta = self.bend_factor * modulation
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            new_pos = face_center - v_rot
            vertices.append(new_pos)
            path.append(new_pos)
            
        return np.array(path)

    def update_text(self, text):
        # By using name='status', PyVista automatically replaces the old text
        self.plotter.add_text(
            text, 
            name='status', 
            position='upper_left', 
            font_size=12, 
            color='white'
        )

    def update_animation(self):
        # PHASE 1: COMPRESSION (Moving Closer)
        if self.separation > 0.1:
            self.separation -= 0.05
            
            # Move Actor A (Left)
            if self.actor_a: self.actor_a.position = (-self.separation, 0, 0)
            # Move Actor B (Right)
            if self.actor_b: self.actor_b.position = (self.separation, 0, 0)
            
            self.update_text(f"STATUS: COMPRESSION (Dist: {self.separation:.2f})")

        # PHASE 2: FUSION (The Merge)
        elif not self.merged:
            self.merged = True
            self.flash_intensity = 1.0
            
            # Hide the two separate protons
            if self.actor_a: self.plotter.remove_actor(self.actor_a)
            if self.actor_b: self.plotter.remove_actor(self.actor_b)
            
            # Show the merged Helium Nucleus (Tighter, brighter)
            he_path = self.generate_proton_loop(3600) 
            he_spline = pv.Spline(he_path, 3600)
            he_tube = he_spline.tube(radius=0.4)
            
            self.actor_he = self.plotter.add_mesh(
                he_tube, 
                color='cyan', 
                style='wireframe', 
                line_width=4,
                emissive=True
            )
            self.update_text("STATUS: FUSION IGNITION (Energy Release)")

        # PHASE 3: ENERGY RELEASE (The Flash)
        if self.merged and self.flash_intensity > 0:
            # Simulate Gamma Flash
            flash_val = self.flash_intensity * 0.8 # Make it bright
            self.plotter.set_background((flash_val, flash_val, flash_val))
            
            self.flash_intensity -= 0.02
            if self.flash_intensity <= 0: 
                self.plotter.set_background('black')
                self.update_text("STATUS: STABLE HELIUM-4")

        self.frame_count += 1
        time.sleep(0.016)

    def setup_scene(self):
        # 1. Generate the Geometry
        print("Generating Proton A (1836 Trixles)...")
        path_a = self.generate_proton_loop(self.proton_size)
        
        print("Generating Proton B (1836 Trixles)...")
        path_b = self.generate_proton_loop(self.proton_size)
        
        # 2. Create Meshes
        spline_a = pv.Spline(path_a, 1000)
        tube_a = spline_a.tube(radius=0.3)
        
        spline_b = pv.Spline(path_b, 1000)
        tube_b = spline_b.tube(radius=0.3)
        
        # 3. Add to Scene
        self.actor_a = self.plotter.add_mesh(
            tube_a, color='orange', style='wireframe', line_width=2
        )
        
        self.actor_b = self.plotter.add_mesh(
            tube_b, color='red', style='wireframe', line_width=2
        )
        
        # 4. Initial UI
        self.update_text("Initializing Reactor...")
        
        self.plotter.set_background('black')
        self.plotter.view_isometric()
        self.plotter.camera.zoom(1.5)
        
        print("Starting Fusion Simulation...")
        self.plotter.show(interactive_update=True)
        
        while True:
            try:
                self.update_animation()
                self.plotter.update()
            except AttributeError:
                # This only catches window closure
                break
            except Exception as e:
                # Now we print the real error if something goes wrong
                print(f"Simulation Crashed: {e}")
                break

if __name__ == "__main__":
    FusionReactor()