---
name: evo-r2r-mpc-controller
description: Implements MPC controller with prediction matrices, QP formulation, simulation loop for R2R web handling. Generates controller_params.json, control_log.json, and metrics.json.
---

# evo-r2r-mpc-controller

MPC controller for 6-section R2R system with reference step tracking.

## Usage
```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-r2r-mpc-controller/scripts')
from utils import (
    build_prediction_matrices,
    build_qp_matrices,
    solve_mpc_step,
    run_simulation_loop,
    compute_performance_metrics,
    save_output_files
)
```

## Key Functions
- `build_prediction_matrices(Ad, Bd, N)` - Build Phi and Gamma matrices
- `build_qp_matrices(Phi, Gamma, Q, R_mat, P, N)` - Build QP Hessian and gradient
- `solve_mpc_step(H, F, dx, N, nu)` - Solve one MPC step (unconstrained)
- `run_simulation_loop(sim, linearize_fn, get_ref_fn, Q, R_mat, N, num_steps)` - Full sim loop
- `compute_performance_metrics(log_data, T_ref_final)` - Compute SSE, settling time, etc.
- `save_output_files(controller_params, log_data, metrics)` - Save all 3 JSON files

## Output Files
- controller_params.json: A_matrix (continuous), B_matrix (continuous), K_lqr, Q_diag, R_diag, horizon_N
- control_log.json: phase="control", data array with time/tensions/velocities/control_inputs/references
- metrics.json: steady_state_error, settling_time, max_tension, min_tension
