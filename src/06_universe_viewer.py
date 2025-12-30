import numpy as np
import pyvista as pv

class TrixleUniverse:
    def __init__(self):
        self.plotter = pv.Plotter(title="Trixle Theory: The Geometric Universe")
        self.bend_factor = 0.01525 # The Proton Tune
        
        # UI State
        self.current_mesh = None
        self.text_actor = None
        
        self.setup_scene()
        
    def generate_lattice(self, steps, particle_name):
        """ Generates the 3D Lattice for a specific particle resonance """
        print(f"Generating {particle_name} (N={steps})...")
        
        vertices = [
            np.array([1.0, 1.0, 1.0]),
            np.array([1.0, -1.0, -1.0]),
            np.array([-1.0, 1.0, -1.0]),
            np.array([-1.0, -1.0, 1.0])
        ]
        
        # Color Map data (Torsion/Strain per step)
        scalars = [0, 0, 0, 0]
        
        for i in range(steps):
            last_three = len(vertices) - np.array([3, 2, 1])
            f_verts = [vertices[idx] for idx in last_three]
            
            old_vertex = vertices[len(vertices) - 4]
            face_center = np.mean(f_verts, axis=0)
            direction = old_vertex - face_center
            edge_vector = f_verts[1] - f_verts[0]
            k = edge_vector / np.linalg.norm(edge_vector)
            
            # Apply Curvature
            theta = self.bend_factor
            v_rot = (direction * np.cos(theta) + 
                     np.cross(k, direction) * np.sin(theta) + 
                     k * np.dot(k, direction) * (1 - np.cos(theta)))

            vertices.append(face_center - v_rot)
            
            # Add a scalar value for color (Simulate Torsion Stress)
            # Higher stress = Warmer color
            stress = (np.sin(i * 0.1) + 1) / 2 # Simple wave for visualization
            scalars.append(stress)

        # Convert to PyVista Mesh (Tube)
        points = np.array(vertices)
        spline = pv.Spline(points, 1000)
        tube = spline.tube(radius=0.1)
        
        return tube, points

    def render_particle(self, n, name):
        # Clear old mesh
        if self.current_mesh:
            self.plotter.remove_actor(self.current_mesh)
            
        # Generate new data
        tube, points = self.generate_lattice(n, name)
        
        # Add to scene
        self.current_mesh = self.plotter.add_mesh(
            tube, 
            cmap="plasma", 
            show_scalar_bar=False,
            opacity=0.9,
            specular=0.5
        )
        
        # Update Label
        if self.text_actor:
            self.plotter.remove_actor(self.text_actor)
        
        status_text = (
            f"OBJECT: {name}\n"
            f"LATTICE STEPS: {n}\n"
            f"GEOMETRY: Boerdijk-Coxeter Helix\n"
            f"STATUS: Resonance Lock"
        )
        self.text_actor = self.plotter.add_text(
            status_text, 
            position='upper_left', 
            font_size=12, 
            color='white',
            font='courier'
        )
        
        # Auto-Zoom to fit
        self.plotter.view_isometric()
        self.plotter.reset_camera()

    def setup_scene(self):
        # Background
        self.plotter.set_background("#050510") # Deep Space Blue
        
        # Instructions
        self.plotter.add_text(
            "CONTROLS:\n[1] Higgs (N=122)\n[2] Electron (N=136)\n[3] Proton (N=1836)\n[4] DNA Scale (N=500)",
            position='lower_left',
            font_size=10,
            color='gray'
        )

        # Key Bindings
        self.plotter.add_key_event("1", lambda: self.render_particle(122, "HIGGS BOSON (Ground State)"))
        self.plotter.add_key_event("2", lambda: self.render_particle(136, "ELECTRON (Lepton Loop)"))
        self.plotter.add_key_event("3", lambda: self.render_particle(1836, "PROTON (Baryon Knot)"))
        self.plotter.add_key_event("4", lambda: self.render_particle(500, "HELIX MACRO-VIEW"))

        # Initial View
        self.render_particle(122, "HIGGS BOSON (Ground State)")
        
        print("Launching Trixle Universe...")
        self.plotter.show()

if __name__ == "__main__":
    TrixleUniverse()