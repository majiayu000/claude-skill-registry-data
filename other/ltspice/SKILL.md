---
name: ltspice
description: "Build LTspice netlists, automate measurements, and investigate convergence or switching-converter simulation behavior."
category: eda
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["ltspice", "spice-simulation", "analog-devices", "circuit-design", "convergence-tuning", "switch-mode-power", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Analog Devices LTspice Circuit Simulation AI Skill Guide (Claude)

## Overview & Engine Architecture
Analog Devices LTspice is a high-performance SPICE simulation engine engineered specifically for non-linear power electronics, switch-mode power supplies (SMPS), RF amplifiers, and mixed-signal circuits. LTspice features a **modified Berkeley SPICE3 core with proprietary solver enhancements**, multiple numerical integration engines (**Modified Trapezoidal, Trapezoidal, and Gear**), compact binary waveform format (**`.raw`**), and a native schematic format (**`.asc`**). Claude operates as a Principal Analog Power Electronics Engineer and SPICE Modeling Specialist, specializing in **switching converter stability & efficiency analysis**, **SPICE numerical convergence tuning**, **batch CLI parametric automation**, and **custom `.subckt` model integration**.

### LTspice Core Engine & Simulation Subsystems

```
┌─────────────────────────────────────────────────────────────┐
│                 LTspice Simulation Architecture             │
│                                                             │
│  Schematic & Netlist Ingestion                              │
│  ├── `.asc` Schematic & Hierarchy Parser                    │
│  ├── SPICE Netlist Generator (`.cir` / `.net`)              │
│  └── Sub-Circuit (`.subckt`) & Vendor Model Library Loader  │
│                                                             │
│  Mathematical Solver & Waveform Engine                      │
│  ├── Modified Nodal Analysis (MNA Matrix Solver)            │
│  ├── Dynamic Timestep Controller & Gear/Trap Integration    │
│  ├── Waveform Binary Streamer (`.raw` Data Engine)          │
│  └── Waveform Post-Processor (`.MEAS` Directive Evaluator)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **SPICE Convergence Troubleshooting**: Remediate fatal `Time step too small` errors and infinite iteration loops on high-frequency switching converters by tuning integration methods (`method=Gear`), damping parameters, and timestep limits.
2. **Automated Batch Parametric Runs**: Author headless CLI scripts (`LTspice.exe -b -Run`) pairing with Python to iterate component values across temperature and tolerance corners.
3. **Measurement Directive Formulation (`.MEAS`)**: Construct precise `.MEAS` statements to compute power supply ripple, efficiency ($\eta = P_{\text{out}} / P_{\text{in}}$), bandwidth, slew rate, and total harmonic distortion (THD).
4. **Third-Party Model Ingestion**: Convert vendor PSpice, TINA-TI, and HSPICE models into native LTspice `.subckt` definitions, fixing pin ordering and unsupported mathematical functions.

---

## Production Python Automation: Automated Synchronous Buck Converter Efficiency Sweeper

Save this script as `run_buck_efficiency_sweep.py` (requires `pip install PyLTSpice` or runs standalone with binary parsing):

```python
"""
LTspice Automated SMPS Efficiency Characterization Tool
Executes batch simulations sweeping load currents (0.5A to 5.0A) and logs efficiency.
"""

import sys
import os
import subprocess
import re

LTSPICE_EXE = r"C:\Program Files\ADI\LTspice\LTspice.exe"

NETLIST_TEMPLATE = """* Synchronous Buck Converter Parametric Testbench
.param Rload_val = {r_load}
.param Vin_val = 12.0

* Power Stage
Vin IN 0 {Vin_val}
S1 IN SW GATE1 0 MYSW
S2 0 SW GATE2 0 MYSW
L1 SW OUT 10u Rser=10m
C1 OUT 0 100u Rser=5m
Rload OUT 0 {r_load}

* Ideal Gate Drive Signals (500kHz, 40% Duty Cycle)
Vgate1 GATE1 0 PULSE(0 10 0 10n 10n 800n 2u)
Vgate2 GATE2 0 PULSE(10 0 0 10n 10n 800n 2u)

.model MYSW SW(Ron=10m Roff=1Meg Vt=5)

* Simulation & Convergence Options
.tran 0 2m 1.8m 10n startup
.options method=Gear maxstep=10n

* Measurement Directives
.meas TRAN Vout_avg AVG V(OUT)
.meas TRAN Iout_avg AVG I(Rload)
.meas TRAN Pin_avg AVG -V(IN)*I(Vin)
.meas TRAN Pout_avg PARAM Vout_avg * Iout_avg
.meas TRAN Efficiency PARAM (Pout_avg / Pin_avg) * 100.0

.backanno
.end
"""

def sweep_efficiency(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    load_resistances = [10.0, 5.0, 2.5, 1.25, 1.0] # Sweeping from ~0.5A to 5.0A at 5V output
    results = []

    print(f"--- [STARTING LTSPICE EFFICIENCY SWEEP: {len(load_resistances)} POINTS] ---")

    for idx, r_val in enumerate(load_resistances):
        cir_path = os.path.join(output_dir, f"sim_run_{idx}.cir")
        log_path = os.path.join(output_dir, f"sim_run_{idx}.log")

        with open(cir_path, "w") as f:
            f.write(NETLIST_TEMPLATE.format(r_load=r_val))

        # Run Headless Batch Simulation
        cmd = [LTSPICE_EXE, "-b", "-Run", cir_path]
        subprocess.run(cmd, check=True)

        # Parse .MEAS Results from Log File
        eff_val = 0.0
        pout_val = 0.0
        if os.path.exists(log_path):
            with open(log_path, "r") as lf:
                log_content = lf.read()
                eff_match = re.search(r"efficiency:\s+pout_avg/pin_avg\*100\.0=([\d\.]+)", log_content, re.IGNORECASE)
                pout_match = re.search(r"pout_avg:\s+vout_avg\*iout_avg=([\d\.]+)", log_content, re.IGNORECASE)
                
                if eff_match:
                    eff_val = float(eff_match.group(1))
                if pout_match:
                    pout_val = float(pout_match.group(1))

        print(f"  • Load R: {r_val:>5.2f} Ω | Power Out: {pout_val:>5.2f} W | Efficiency: {eff_val:>6.2f} %")
        results.append((r_val, pout_val, eff_val))

    print("\nEfficiency sweep completed successfully.")

if __name__ == "__main__":
    out_dir = r"C:\Temp\LTspice_Sweep"
    sweep_efficiency(out_dir)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Analysis: Time step too small` on Switching Circuit** | Numerical solver trapped in infinite slope transition on fast switching edges or non-linear diode recovery. | 1. In Simulation Command, add: `.options method=Gear maxstep=10n`.<br>2. Add small parasitic series resistance to inductors (`Rser=1m`) and capacitors (`Rser=5m`).<br>3. Set `cshunt=1e-15` to stabilize high-impedance floating nodes. |
| **Trapezoidal Ringing / Spurious High-Frequency Noise** | The standard Trapezoidal integration method oscillates around sharp square-wave step discontinuities. | 1. Change solver integration method to **Gear** (`.options method=Gear`) or **Modified Trap**.<br>2. In Control Panel $\rightarrow$ *SPICE*, ensure **Integration Method** is set to `Gear` or `Modified Trap`. |
| **Third-Party Model Ingestion Fails: `Unknown subckt / Syntax error`** | PSpice/HSPICE models using nested `.LIB` calls, proprietary table functions, or mismatched node count. | 1. Check `.SUBCKT` header for number of pins vs symbol pin count.<br>2. Replace `.FUNC myfunc(x) = ...` with `.PARAM myfunc(x) = ...`.<br>3. Flatten nested library includes into direct `.INCLUDE` directives. |
| **Simulation Runs Extremely Slow (<10ns/sec)** | Excessive timestep refinement caused by ideal switch model without transition slope (`Ron`, `Roff`, `Vt`). | 1. Ensure switch models define finite transition slopes: `.model MYSW SW(Ron=10m Roff=1Meg Vt=2.5 Vh=-1.0)`.<br>2. Avoid zero rise/fall times in voltage pulse generators (`trise=10n`, `tfall=10n`). |

---

## Command Line Syntax & Operational Recipes

```bash
# 1. Run Headless Batch Simulation on Schematic File
"C:\Program Files\ADI\LTspice\LTspice.exe" -b -Run "C:\Circuits\PowerSupply.asc"

# 2. Run Batch Netlist Simulation and Generate ASCII Waveforms
"C:\Program Files\ADI\LTspice\LTspice.exe" -b -ascii "C:\Circuits\Filter.cir"

# 3. macOS CLI Execution (via Application Bundle)
/Applications/LTspice.app/Contents/MacOS/LTspice -b -Run ~/Circuits/Amp.asc
```

### Essential File Locations
- **Windows User Models & Symbols**: `%USERPROFILE%\Documents\LTspice\lib`
- **Windows Global Installation**: `C:\Program Files\ADI\LTspice`
- **macOS Preferences**: `~/Library/Application Support/LTspice`

---

## Agent Operational Directive
> **MANDATORY**: For switch-mode power supply (SMPS) simulations, always specify non-zero rise and fall times (`trise`, `tfall`), add parasitic ESR (`Rser`) to passive elements, and set `.options method=Gear maxstep=...` to guarantee numerical convergence.
