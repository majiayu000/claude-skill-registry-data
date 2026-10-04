---
name: codesys
description: "Develop CODESYS Structured Text and Python ScriptEngine workflows; troubleshoot fieldbus and OPC UA integration in a test environment."
category: plc-industrial
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["codesys", "iec-61131-3", "structured-text", "scriptengine", "ethercat", "opc-ua", "plc-programming", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# CODESYS V3.5 IEC 61131-3 Industrial Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
CODESYS V3.5 is the global industry standard, hardware-agnostic IEC 61131-3 automation software and PLC programming platform powering over 400+ controller manufacturers (Beckhoff, WAGO, Festo, Schneider Electric, Eaton, Berghof). The platform combines the **CODESYS Control V3 Real-Time Runtime**, full **IEC 61131-3 language support (Structured Text ST, Continuous Function Chart CFC, Function Block Diagram FBD, Sequential Function Chart SFC, Ladder Diagram LD)**, integrated **Fieldbus protocol stacks (EtherCAT Master, PROFINET IO Controller, Modbus TCP/RTU, CANopen)**, an embedded **OPC UA Server**, and the **CODESYS ScriptEngine (Python automation API)**. Claude operates as a Principal Industrial Automation Architect and Controls Software Engineer, specializing in **Structured Text (ST) state machine authoring**, **ScriptEngine automated build pipelines**, **EtherCAT topology validation**, and **CODESYS Gateway communication diagnostics**.

### CODESYS Multi-Tier Architecture & Fieldbus Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 CODESYS V3.5 Architecture                   │
│                                                             │
│  Engineering & ScriptEngine Tier                            │
│  ├── CODESYS Development System IDE (POUs, GVls, Data Types)│
│  ├── CODESYS ScriptEngine (Python Automation & CI/CD)       │
│  └── CODESYS Visualization (TargetVisu & WebVisu HTML5)     │
│                                                             │
│  IEC 61131-3 Execution & Real-Time Runtime                  │
│  ├── CODESYS Control V3 Runtime (Preemptive Task Scheduler) │
│  ├── Task Configuration (Cyclic, Event, Freewheeling Tasks) │
│  └── SoftMotion CNC & Robotics 3D Coordinate Transformer    │
│                                                             │
│  Industrial Communications & Fieldbus Core                  │
│  ├── Embedded OPC UA Server (Data Access & Methods)         │
│  ├── Fieldbus Masters (EtherCAT, PROFINET, Modbus TCP, CAN) │
│  └── CODESYS Gateway Service (SysService Communication:1217)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **ScriptEngine CI/CD Build Pipelines**: Author Python scripts for CODESYS ScriptEngine to automate project opening, syntax verification, POU generation, compilation, and boot application deployment.
2. **IEC 61131-3 Structured Text (ST) Authoring**: Construct robust, type-safe Structured Text function blocks implementing deterministic finite state machines (FSM) and alarm handling.
3. **Gateway & Communication Triage**: Resolve PLC connection drops and Gateway routing failures across TCP port 1217 and UDP discovery ports.
4. **Fieldbus & Real-Time Task Jitter Optimization**: Configure cyclic task priorities and optimize EtherCAT distributed clock (DC) synchronization to eliminate task watchdog violations ($<1\text{ms}$ cycle times).

---

## Production Python Automation: Headless CODESYS Project Builder & Compiler (`ScriptEngine`)

Save this script as `build_and_export_boot.py` and run via `CODESYS.exe --profile="CODESYS V3.5 SP20" --runscript="build_and_export_boot.py" --noUI`:

```python
# ==============================================================================
# CODESYS ScriptEngine: Automated Headless Project Build & Boot App Generator
# Opens a .project file, compiles all POUs, audits errors, and creates boot app.
# ==============================================================================
import sys
import os

PROJECT_PATH = r"C:\AutomationProjects\PackagingLine.project"

def build_codesys_project():
    print("--- [INITIALIZING CODESYS SCRIPTENGINE BUILD PIPELINE] ---")

    if not os.path.exists(PROJECT_PATH):
        print("🚨 Error: Project file not found at: " + PROJECT_PATH)
        return

    # 1. Open Project
    print("Opening project: " + PROJECT_PATH)
    proj = projects.open(PROJECT_PATH)

    # 2. Find Primary Application Node
    app = None
    for obj in proj.get_children(recursive=True):
        if obj.is_type("Application"):
            app = obj
            break

    if not app:
        print("🚨 Error: No Application object found in project tree.")
        proj.close()
        return

    print("Found Application: " + app.get_name())

    # 3. Clean and Compile Project
    print("Compiling Application...")
    app.clean()
    messages = app.build()

    error_count = 0
    warning_count = 0

    for msg in messages:
        if msg.severity == Severity.Error:
            error_count += 1
            print("  🚨 ERROR: " + msg.text)
        elif msg.severity == Severity.Warning:
            warning_count += 1

    print("\nCompilation Summary: " + str(error_count) + " Error(s), " + str(warning_count) + " Warning(s)")

    if error_count > 0:
        print("🚨 Build Failed! Halting deployment.")
    else:
        print("✅ Build Succeeded. Generating Boot Application...")
        app.create_boot_application()
        print("✅ Boot application created successfully.")

    proj.save()
    proj.close()
    print("Project saved and closed cleanly.")

if __name__ == "__main__":
    build_codesys_project()
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **"Communication error: Device not reachable"** | CODESYS Gateway service stopped or firewall blocking TCP port 1217 on target PLC. | 1. In Windows Services, verify **CODESYS Gateway SysService** is running.<br>2. On Linux target, check daemon: `sudo systemctl status codesyscontrol`.<br>3. Verify target port: `telnet <PLC_IP> 1217`. |
| **"Boot application too large for memory"** | Compiled binary footprint exceeds the target controller's flash memory allocation partition. | 1. In Application $\rightarrow$ Properties $\rightarrow$ Build, uncheck unused libraries.<br>2. In *Build $\rightarrow$ Memory Utilization*, identify large global array buffers and move to dynamically allocated heap. |
| **Watchdog Timeout Exception on Real-Time Task** | Task cycle execution time exceeded the configured watchdog limit (e.g. $10\text{ms}$). | 1. Increase task cycle time or optimize Structured Text nested loops.<br>2. Check Real-Time Linux kernel for PREEMPT_RT patches on IPC targets. |
| **EtherCAT Bus Enters `SAFE-OP with Error`** | Physical slave order mismatch or missing ESI (EtherCAT Slave Information) XML file. | 1. Right-click EtherCAT Master $\rightarrow$ Select **Scan for Devices** to verify physical topology order.<br>2. In Device Repository, install missing vendor `.xml` ESI descriptors. |

---

## Command Line Syntax & ScriptEngine Invocations

```bash
# 1. Execute Headless CODESYS Python Script via CLI
"C:\Program Files\CODESYS 3.5\CODESYS\Common\CODESYS.exe" --profile="CODESYS V3.5 SP20" --runscript="C:\Scripts\build_and_export_boot.py" --noUI

# 2. Inspect CODESYS Control Linux Runtime Logs
tail -f /tmp/codesyscontrol.log

# 3. Restart Linux CODESYS Control Daemon
sudo /etc/init.d/codesyscontrol restart
```

### Essential File Locations
- **ScriptEngine Documentation**: Embedded within CODESYS Online Help
- **Runtime Configuration**: `/etc/CODESYSControl_V3.cfg` (Linux) or `%APPDATA%\CODESYS\CODESYSControl_V3\` (Windows)
- **Device Repository**: `%APPDATA%\CODESYS\DeviceRepository\`

---

## Agent Operational Directive
> **MANDATORY**: When authoring automated build pipelines with CODESYS ScriptEngine, always verify that `app.build()` returns zero `Severity.Error` messages before executing `app.create_boot_application()`.
