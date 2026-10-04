---
name: comsol
description: "Automate COMSOL models through Python, Java, or MATLAB integrations and diagnose solver-convergence issues."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["comsol", "multiphysics", "finite-element-analysis", "mph-python", "livelink", "fea-solvers", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# COMSOL Multiphysics Finite Element Simulation AI Skill Guide (Claude)

## Overview & Engine Architecture
COMSOL Multiphysics 6.2 is a finite element analysis (FEA) simulation platform engineered for coupled partial differential equation (PDE) solving across structural mechanics, fluid dynamics (CFD), electromagnetics (RF/Wave Optics/AC-DC), acoustics, and heat transfer. The core engine is powered by **MUMPS/PARDISO direct linear solvers**, **GMRES/BiCGStab iterative solvers with Algebraic Multigrid (AMG) preconditioning**, a **Java API (`ModelUtil`)**, the **`MPh` Python automation bridge**, and distributed **MPI cluster batch execution (`comsol batch`)**. Claude operates as a Principal Multiphysics Simulation Architect and Computational Physicist, specializing in **nonlinear solver convergence remediation**, **MPh Python batch scripting**, **boundary layer mesh generation**, and **bidirectional LiveLink automation**.

### CODESYS & COMSOL Solver Architecture & API Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 COMSOL Multiphysics Stack                   │
│                                                             │
│  Engineering & Model Builder Layer                          │
│  ├── Model Tree (Geometry, Physics Interfaces, Multiphysics)│
│  ├── Application Builder (Custom Simulation Apps & WebApps) │
│  └── LiveLink Bridges (MATLAB, SolidWorks, AutoCAD, Revit)  │
│                                                             │
│  Numerical Discretization & Solver Core                     │
│  ├── Finite Element Engine (Lagrange, Serendipity, Nedelec) │
│  ├── Direct Solvers (PARDISO, MUMPS, SPOOLES)               │
│  └── Iterative Solvers (GMRES, FGMRES, AMG Preconditioners) │
│                                                             │
│  Automation & Headless Execution Subsystem                  │
│  ├── COMSOL MPHServer (Java IPC Daemon: Default Port 2036)  │
│  ├── `MPh` Python Automation Library (`import mph`)         │
│  └── MPI Cluster Batch Engine (`comsol batch -inputfile...`)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **MPh Python Automated Simulation Pipelines**: Author Python scripts utilizing the `MPh` library to connect to `mphserver`, parameterize geometric/physics properties, execute parametric sweeps, and export numerical datasets.
2. **Nonlinear Solver Convergence Triage**: Remediate divergence errors by switching from Fully Coupled to Segregated solvers, implementing Newton-Raphson damping ($0.5-0.75$), and designing Auxiliary parameter continuation sweeps.
3. **Geometry Defeaturing & Boundary Layer Meshing**: Eliminate CAD sliver faces and short edges using Virtual Operations (`Form Composite Faces`) and inject structured prism boundary layers for fluid wall shear and thermal gradients.
4. **HPC Batch Cluster Scripting**: Construct Slurm/PBS batch submission scripts executing distributed simulations across multi-node compute clusters via `comsol batch`.

---

## Production Python Automation: COMSOL Headless Simulation & Parameter Sweep (`MPh`)

Save this script as `run_thermal_simulation.py` (requires `pip install mph` and a running `comsol mphserver -port 2036`):

```python
"""
COMSOL Multiphysics Python Automation Client (MPh)
Connects to COMSOL MPHServer, modifies heat flux parameters, solves study, and extracts peak temperatures.
"""

import sys
import mph
import pandas as pd

COMSOL_PORT = 2036
MODEL_PATH = "C:/SimulationModels/HeatSink_Thermal_Stress.mph"

def run_parametric_study():
    print(f"--- [INITIALIZING COMSOL MULTIPHYSICS AUTOMATION PIPELINE] ---")
    
    # 1. Connect to Standalone COMSOL Server
    print(f"Connecting to COMSOL MPHServer on port {COMSOL_PORT}...")
    client = mph.start(port=COMSOL_PORT)
    print("✅ Connected to COMSOL Backend Server!")

    # 2. Load Model
    print(f"Loading Model: {MODEL_PATH}...")
    model = client.load(MODEL_PATH)

    # 3. Update Model Parameters
    heat_flux_values = [500.0, 1000.0, 1500.0, 2000.0] # W/m^2
    results_data = []

    print("\n--- [EXECUTING PARAMETRIC STUDY SWEEP] ---")
    for flux in heat_flux_values:
        print(f"Applying Heat Flux: {flux} W/m^2...")
        model.parameter("q_in", f"{flux}[W/m^2]")

        # 4. Solve Study (std1)
        print("  • Solving Finite Element Study (std1)...")
        model.solve("std1")

        # 5. Evaluate Maximum Temperature in Domain
        max_temp_degC = model.evaluate("maxop1(T)") - 273.15
        max_von_mises = model.evaluate("maxop1(solid.mises)") / 1e6 # Convert Pa to MPa

        print(f"  ✅ Max Temp: {max_temp_degC:.2f} °C | Max Von Mises: {max_von_mises:.2f} MPa")
        results_data.append({
            "Heat_Flux_W_m2": flux,
            "Max_Temperature_C": max_temp_degC,
            "Max_Von_Mises_MPa": max_von_mises
        })

    # 6. Export Results to CSV
    df = pd.DataFrame(results_data)
    df.to_csv("Thermal_Parametric_Results.csv", index=False)
    print(f"\n✅ Results exported to: Thermal_Parametric_Results.csv")

    # Clean disconnect
    client.clear()
    print("COMSOL session closed.")

if __name__ == "__main__":
    run_parametric_study()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **"Failed to find consistent initial values"** | Incompatible initial conditions in coupled Navier-Stokes / Heat Transfer equations. | 1. In Study Step $\rightarrow$ Solver Configurations, switch to **Segregated Solver**.<br>2. Add an **Auxiliary Sweep** starting with low fluid velocity to ramp initial conditions smoothly.<br>3. Set Newton-Raphson Method to **Constant (Damped)** with factor $0.5$. |
| **"Face has short edges / sliver surface" (Mesh Failure)** | Imported STEP/IGES CAD model contains sub-millimeter geometry defects. | Under Geometry $\rightarrow$ Virtual Operations, add **Form Composite Faces** and **Collapse Short Edges** to defeat micro-features. |
| **Out of Memory during 3D Solid Mechanics Solution** | Direct solver (PARDISO/MUMPS) exceeded available RAM during matrix factorization. | In Solver Configuration $\rightarrow$ Stationary Solver, change Direct Solver to an **Iterative Solver (GMRES)** with **Geometric Multigrid (GMG)** preconditioning. |
| **`MPh` Throws `Server Connection Refused`** | COMSOL MPHServer is not running or listening on a different TCP port. | Start the server in terminal: `comsol mphserver -port 2036 -login auto`. |

---

## Command Line Syntax & Batch Processing

```bash
# 1. Start COMSOL Headless MPHServer Daemon
comsol mphserver -port 2036 -login auto

# 2. Run Headless Batch Simulation on 16 CPU Cores
comsol batch -np 16 -inputfile "C:\Models\HeatSink.mph" -outputfile "C:\Results\HeatSink_Solved.mph" -study std1

# 3. Distributed MPI Cluster Batch Solve on Slurm
mpirun -np 64 comsol batch -inputfile "Turbine.mph" -outputfile "Turbine_Out.mph" -distributed
```

### Essential File Locations
- **COMSOL Preferences**: `%USERPROFILE%\.comsol\v62\comsol.prefs`
- **Recovery Directory**: `%USERPROFILE%\.comsol\v62\recoverydir\`
- **COMSOL Executable**: `C:\Program Files\COMSOL\COMSOL62\Multiphysics\bin\win64\comsol.exe`

---

## Agent Operational Directive
> **MANDATORY**: When solving highly nonlinear coupled multiphysics models (e.g. Joule heating with temperature-dependent conductivity), always configure a Segregated Solver with damped Newton iterations before resorting to direct solvers.
