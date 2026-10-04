---
name: evo-r2r-linearization
description: Derives linearized state-space model (A, B matrices) for 6-section R2R system, computes steady-state operating points, discretizes, and computes LQR gain.
---

# evo-r2r-linearization

Computes linearized state-space model for R2R web handling systems.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-r2r-linearization/scripts')
from utils import (
    compute_steady_state_velocities,
    compute_steady_state_torques,
    build_continuous_AB,
    discretize_system,
    compute_lqr_gain,
    get_full_reference_state
)
```

## Key Functions
- `compute_steady_state_velocities(T_ref, EA, v0)` - Cascade velocities using (EA-T) formula
- `compute_steady_state_torques(T_ref, v_ref, R, fb)` - Compute equilibrium torques
- `build_continuous_AB(T_ss, v_ss, EA, L, R, J, fb, v0)` - Build 12x12 A and 12x6 B Jacobians
- `discretize_system(A_cont, B_cont, dt)` - ZOH discretization via scipy
- `compute_lqr_gain(Ad, Bd, Q, R_mat)` - Solve DARE, return K_lqr and P
- `get_full_reference_state(T_ref, EA, v0, R, fb)` - Get full x_ref and u_ref
