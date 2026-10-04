---
name: evo-thermal-pid-control
description: PID controller tuning, discrete-time PID with anti-windup, closed-loop simulation, and control performance metrics. Uses SIMC tuning rules for first-order systems.
---

# evo-thermal-pid-control

PID controller for HVAC thermal systems.

## Functions

- `calculate_simc_gains(K, tau, tau_c=None)` - SIMC PI gains; returns dict with Kp, Ki, Kd, lambda
- `DiscretePID(Kp, Ki, Kd, dt, output_min=0, output_max=100)` - PID class with anti-windup
- `run_closed_loop_control(sim, Kp, Ki, Kd, setpoint=22.0, duration=180.0)` - Run control loop
- `calculate_control_metrics(control_log)` - Compute rise_time, overshoot, settling_time, sse, max_temp
- `save_control_results(tuned_gains, control_log, metrics)` - Save JSON files to /root/

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-thermal-pid-control/scripts')
from pid_utils import calculate_simc_gains, run_closed_loop_control, calculate_control_metrics, save_control_results

gains = calculate_simc_gains(K=0.12, tau=40.0, tau_c=25.0)
sim = HVACSimulator()
sim.reset()
control_log = run_closed_loop_control(sim, gains['Kp'], gains['Ki'], gains['Kd'], setpoint=22.0, duration=180.0)
metrics = calculate_control_metrics(control_log)
save_control_results(gains, control_log, metrics)
```

## Key Domain Knowledge

- SIMC tuning: Kp = tau/(K*tau_c), Ti = min(tau, 4*tau_c), Ki = Kp/Ti, Kd = 0
- tau_c = 25s gives settling time ~100s (4*tau_c)
- Anti-windup: stop integrating when output saturated and error same sign
- Trapezoidal integration for integral term
- Derivative on measurement (not error) to avoid derivative kick
- Overshoot = (peak - setpoint) / (setpoint - T_initial)
- Settling time: trace backward to find last time outside +/-0.5C band
- Control duration must be >= 150s
- Heater power clamped to [0, 100]%
