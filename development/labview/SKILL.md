---
name: labview
description: "Automate LabVIEW dataflow and build workflows, integrate NI-DAQmx or VISA instruments, and diagnose hardware communication."
category: scientific
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["labview", "ni-daqmx", "g-language", "producer-consumer-qmh", "visa-scpi", "g-cli", "data-acquisition", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# NI LabVIEW Graphical Dataflow & DAQ AI Skill Guide (Claude)

## Overview & Engine Architecture
National Instruments (NI) LabVIEW is a graphical dataflow programming environment (G-Language) engineered for automated test, laboratory instrumentation, industrial data acquisition (DAQ), and real-time FPGA control (CompactRIO / PXI). The platform couples a visual **Front Panel UI** with an asynchronous **Block Diagram Execution Engine**, utilizing design patterns like the **Producer-Consumer Queued Message Handler (QMH)**. LabVIEW integrates natively with **NI-DAQmx**, **NI-VISA (SCPI standard)**, and executes headless continuous integration builds via the **LabVIEW CLI (`LabVIEWCLI.exe`)** and **`g-cli`**. Claude operates as a Principal Test & Measurement Systems Architect and Automated Test Engineer, specializing in **DAQmx high-speed streaming**, **Producer-Consumer thread safety**, **VISA instrument automation (`pyvisa`)**, and **headless VI build scripting**.

### LabVIEW G-Dataflow Engine & Hardware Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 NI LabVIEW Architecture                     │
│                                                             │
│  Presentation & Design Pattern Tier                         │
│  ├── Front Panel UI Controls & Waveform Graphs              │
│  ├── Block Diagram G-Dataflow Engine (Wires, Nodes, Tunnels)│
│  └── Queued Message Handler (QMH: Producer & Consumer Loops)│
│                                                             │
│  Hardware Driver & Instrument Communication                 │
│  ├── NI-DAQmx Hardware Subsystem (Analog, Digital, Counters)│
│  ├── NI-VISA Standard (GPIB, USB-TMC, RS-232, TCP-IP SCPI) │
│  └── Real-Time & FPGA Modules (CompactRIO / PXI Targets)    │
│                                                             │
│  Automation & CI/CD Tooling Core                            │
│  ├── LabVIEW CLI (`LabVIEWCLI.exe -OperationName RunVI`)    │
│  ├── `g-cli` Open-Source Command Line Interface             │
│  └── VI Package Manager (VIPM Community Toolkits)           │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **NI-DAQmx Python Hardware Automation**: Author Python scripts using the `nidaqmx` API to configure multi-channel hardware tasks, establish continuous sample clocks, and stream voltage data without buffer overruns.
2. **Producer-Consumer QMH Architecture Triage**: Refactor race-prone G-code architectures using thread-safe Queue primitives to isolate high-speed acquisition from disk logging and UI rendering.
3. **VISA SCPI Instrument Scripting (`pyvisa`)**: Build robust instrument communication scripts enforcing correct termination characters (`\n` / `0x0A`) and timeout parameters.
4. **Headless `g-cli` Continuous Integration**: Construct automated CI/CD pipelines executing unit tests (`VI Tester`), building VIPM packages, and generating standalone executables (`.exe`).

---

## Production Python Automation: Continuous High-Speed DAQmx Streamer (`nidaqmx`)

Save this script as `daqmx_continuous_stream.py` (requires `pip install nidaqmx numpy` and connected NI-DAQ hardware):

```python
"""
NI-DAQmx Continuous Analog Input Streaming Client
Streams multi-channel analog voltage data (ai0, ai1) using hardware sample clocking and circular buffers.
"""

import sys
import time
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration

DEVICE_NAME = "Dev1"
SAMPLE_RATE = 10000.0  # 10 kHz
SAMPLES_PER_CHANNEL = 1000 # Read 1000 samples (100ms chunk) per loop iteration

def continuous_daq_acquisition():
    print(f"--- [INITIALIZING NI-DAQMX CONTINUOUS ACQUISITION: {DEVICE_NAME}] ---")

    try:
        with nidaqmx.Task() as task:
            # 1. Add Analog Input Voltage Channels (Differential Mode)
            task.ai_channels.add_ai_voltage_chan(
                f"{DEVICE_NAME}/ai0",
                name_to_assign_to_channel="Ch0_Pressure",
                terminal_config=TerminalConfiguration.DIFF,
                min_val=-10.0,
                max_val=10.0
            )
            task.ai_channels.add_ai_voltage_chan(
                f"{DEVICE_NAME}/ai1",
                name_to_assign_to_channel="Ch1_Temperature",
                terminal_config=TerminalConfiguration.DIFF,
                min_val=-10.0,
                max_val=10.0
            )

            # 2. Configure Hardware Sample Clock & Continuous Mode
            task.timing.cfg_samp_clk_timing(
                rate=SAMPLE_RATE,
                sample_mode=AcquisitionType.CONTINUOUS,
                samps_per_chan=SAMPLES_PER_CHANNEL * 10 # Circular buffer capacity
            )

            print(f"• Sample Rate:     {SAMPLE_RATE} Hz")
            print(f"• Chunk Size:      {SAMPLES_PER_CHANNEL} samples per channel")
            print("Starting acquisition loop (Press Ctrl+C to stop)...\n")

            task.start()
            iteration = 0

            while iteration < 10: # Collect 10 chunks (1 second total)
                # 3. Read Stream Data from Onboard Buffer
                data = task.read(number_of_samples_per_channel=SAMPLES_PER_CHANNEL, timeout=2.0)
                data_np = np.array(data)

                # Calculate RMS / Peak-to-Peak Metrics
                ch0_mean = np.mean(data_np[0])
                ch1_mean = np.mean(data_np[1])
                iteration += 1

                print(f"• Chunk #{iteration:>2}: Ch0 Avg = {ch0_mean:>+7.3f} V | Ch1 Avg = {ch1_mean:>+7.3f} V")

            print("\n✅ Acquisition sequence completed successfully.")

    except nidaqmx.errors.DaqError as e:
        print(f"🚨 DAQmx Error [{e.error_code}]: {e.error_description}")

if __name__ == "__main__":
    continuous_daq_acquisition()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **DAQmx Error -200279 (Buffer Overflow)** | Acquisition loop processing time exceeds sample interval, filling circular onboard FIFO buffer. | 1. Increase buffer size: `task.timing.cfg_samp_clk_timing(..., samps_per_chan=100000)`.<br>2. Move heavy disk I/O / UI operations to a separate Consumer loop via Queues. |
| **Broken Run Arrow on Block Diagram** | Type mismatch between wired data types (e.g. 1D Array wired into Scalar Double terminal). | Click the broken Run Arrow to open the **Error List** window $\rightarrow$ Double-click error to jump to broken wire terminal. |
| **VISA Error `-1073807343` (`VI_ERROR_TMO`)** | Connected instrument did not receive expected line termination character (e.g. `\n`) or timeout exceeded. | 1. In VISA Configure Serial Port, enable **Termination Character** (`0x0A` / `\n`).<br>2. Increase VISA timeout from $2000\text{ms}$ to $5000\text{ms}$. |
| **Race Conditions / Intermittent Data Glitches** | Multiple parallel execution loops writing to the same Global Variable without synchronization. | Replace Global Variables with a **Functional Global Variable (FGV)** (Uninitialized Shift Register in a While Loop) or thread-safe Queues. |

---

## Command Line Syntax & `g-cli` Recipes

```bash
# 1. Run LabVIEW VI via LabVIEWCLI
LabVIEWCLI.exe -OperationName RunVI -VIPath "C:\Automation\RunTestSequence.vi"

# 2. Execute Headless VI Build via g-cli
g-cli -- "C:\Automation\BuildApplication.vi" -- "C:\Projects\TestEngine.lvproj"

# 3. Query Connected NI DAQ Hardware via NI-MAX CLI
nisysapi -devices
```

### Essential File Locations
- **LabVIEW Configuration**: `C:\Program Files\National Instruments\LabVIEW 2024\labview.ini`
- **Data Root**: `%USERPROFILE%\Documents\LabVIEW Data\`
- **VI Package Manager Cache**: `C:\ProgramData\JKI\VIPM\`

---

## Agent Operational Directive
> **MANDATORY**: For continuous high-speed DAQ acquisition, always implement the Producer-Consumer pattern with G-Queues to decouple real-time hardware buffer reads from disk writes and front-panel chart rendering.
