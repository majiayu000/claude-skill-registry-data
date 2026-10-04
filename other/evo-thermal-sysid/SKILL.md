---
name: evo-thermal-sysid
description: System identification utilities for first-order thermal systems. Runs open-loop step tests on HVAC simulator, collects calibration data, fits first-order exponential model, outputs estimated parameters (K, tau) with fit quality metrics.
---

# evo-thermal-sysid

System identification for first-order thermal HVAC systems.

## Functions

- `run_calibration_test(sim, heater_power=50.0, duration=60.0)` - Run open-loop step test, returns calibration_log dict
- `first_order_step_response(t, K, tau, T_amb, U_step)` - First-order model: T_amb + K*U_step*(1-exp(-t/tau))
- `identify_system_params(calibration_log)` - Fit K and tau from calibration data using curve_fit
- `filter_temperature_data(temp_data, window_length=11, polyorder=2)` - Savitzky-Golay filter
- `calculate_fit_metrics(T_actual, T_predicted)` - Returns (r_squared, rmse)
- `save_calibration_results(calibration_log, estimated_params)` - Save JSON files to /root/

## Usage

```python
import sys
sys.path.insert(0, '/app/environment/skills/evo-thermal-sysid/scripts')
from sysid_utils import run_calibration_test, identify_system_params, save_calibration_results

sys.path.insert(0, '/root')
from hvac_simulator import HVACSimulator

sim = HVACSimulator()
calib_log = run_calibration_test(sim, heater_power=50.0, duration=60.0)
params = identify_system_params(calib_log)
save_calibration_results(calib_log, params)
```

## Key Domain Knowledge

- First-order thermal model: dT/dt = (1/tau) * (K*u + T_amb - T)
- Step response: T(t) = T_amb + K*U_step*(1 - exp(-t/tau))
- K ~ 0.12 C/% power, tau ~ 40s for typical HVAC
- Use Savitzky-Golay filter (preserves exponential shape) not moving average
- Use curve_fit with bounds ([0.001, 1.0], [1.0, 200.0]) and maxfev=10000
- Calibration needs >= 30s duration, >= 20 data points
- R-squared > 0.95 indicates good first-order fit
