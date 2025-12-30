import numpy as np
import matplotlib.pyplot as plt

def simulate_jamming():
    # Packing fractions (phi)
    # 0.35 (Vacuum) -> 0.856 (Max Tetrahedral Packing)
    phi = np.linspace(0.35, 0.856, 100)
    
    # Rotational Freedom (Omega) 
    # Defined as the 'Gap Space' available for a Trixle to rotate 60 degrees
    # This falls off non-linearly as we approach the Jamming Point
    omega = np.maximum(0, (0.856 - phi)**1.5 / (0.856 - 0.35)**1.5)
    
    # Effective Speed of Information (c_prime)
    # Proportional to the ability of the lattice to vibrate
    c_prime = omega * 100 # Normalized to 100% at vacuum
    
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    
    plt.plot(phi, c_prime, color='cyan', linewidth=3, label="Propagation Speed (c)")
    plt.axvline(x=0.35, color='green', linestyle='--', label="Vacuum Density")
    plt.axvline(x=0.856, color='red', linestyle='--', label="Black Hole Core (Jamming)")
    
    # Shading the 'Slush' zone (General Relativity effects)
    plt.fill_between(phi, c_prime, color='blue', alpha=0.2)
    
    plt.title("The Trixle Jamming Transition: From Vacuum to Black Hole")
    plt.xlabel("Packing Density (phi)")
    plt.ylabel("Clock Speed (% of c)")
    plt.legend()
    plt.grid(alpha=0.2)
    
    print("--- GEOMETRIC ANALYSIS ---")
    print(f"Vacuum Propagation: 100% c")
    print(f"Intermediate Density (phi=0.6): {np.interp(0.6, phi, c_prime):.2f}% c")
    print(f"Jamming Point (phi=0.856): 0% c (Time Stops)")
    
    plt.show()

if __name__ == "__main__":
    simulate_jamming()