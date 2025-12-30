# The Trixle Theory: Geometric Origin of Mass
**A Computational Study of Boerdijk-Coxeter Lattice Resonances**

## Overview
This repository models the quantum vacuum as a discrete, helical packing of regular tetrahedra. It investigates whether fundamental particle masses arise as natural geometric resonances within this lattice.

## Key Findings
* **Higgs Candidate (N=122):** Identified a ground-state stability island at N=122, aligning with the Higgs mass (~125 GeV).
* **Dark Matter Ratio:** The Proton (N=1836) appears as the 15th harmonic of this ground state, explaining the 5:1 cosmological abundance ratio.
* **Diquark Structure:** Topological analysis of the proton loop reveals a spontaneous Figure-8/Dipole geometry.
* **Chiral Asymmetry:** Simulating "Antimatter" (Left-Handed curvature) requires 1.9x more geometric energy than Matter.

## Structure
* `src/`: Contains the resonance scanners and chirality tests.
* `paper/`: The draft manuscript of the findings.

## Advanced Findings (Update: Dec 29)

### 1. Internal Proton Topology (The Diquark Model)
Radial analysis of the Proton loop (N=1836) reveals that the geometry does not form a uniform torus. Instead, under minimizing strain, the lattice spontaneously forms a **Figure-8 Dipole**.
* **Observation:** The radial distance map (see `results/proton_diquark_structure.png`) shows two dominant lobes separated by tight "gluon" pinch points.
* **Implication:** This geometrically reproduces the **Diquark-Quark** clustering observed in QCD, where the proton behaves as a two-body system rather than a symmetric triplet.

### 2. The Geometric Origin of Alpha (1/137)
The simulation identified a critical "Hinge Mechanism" between N=136 and N=137 that explains the Fine Structure Constant ($\alpha$).
* **N=136 (The Electron):** Corresponds to minimum *Mass Gap* (Closure) but maximum *Torsional Stress* (~72° twist).
* **N=137 (The Vacuum):** Corresponds to minimum *Torsional Stress* (~10° twist) but unstable Mass Gap.
* **Conclusion:** Electromagnetism is the interaction between the particle (136) and the vacuum (137). The electron is a stable loop that is "phase-shifted" by 1 step from the magnetic ground state of the lattice. This torsional slip generates the electric charge. (See `results/alpha_mass_vs_charge.png`).