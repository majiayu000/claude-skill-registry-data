---
name: aiwf-embedded-edge-ai
description: Use for embedded systems, microcontrollers, RTOS, SBCs, Jetson, sensors, firmware boundaries, power, thermal, edge inference, and embedded AI deployment planning.
---

# AIWF Embedded Edge AI

## Core Rule

Inventory the physical target before choosing architecture. Embedded and edge AI work depends on board, CPU/GPU/NPU, RAM/VRAM, storage, power, thermal envelope, OS/RTOS, firmware boundary, sensor buses, actuator interfaces, and deployment/update path.

## Workflow

1. Identify target class: microcontroller, RTOS device, Raspberry Pi/SBC, Jetson, industrial PC, laptop prototype, or simulation-only target.
2. Record constraints: voltage/current, battery or mains, thermal limits, enclosure, IO buses, camera/sensor interfaces, motor/control interfaces, storage, boot mode, and update method.
3. Split responsibilities: firmware, real-time control, Linux services, model inference, logging, UI/API, remote telemetry, and recovery mode.
4. For edge AI, identify model format, runtime, acceleration stack, quantization, memory budget, latency budget, and fallback behavior.
5. Validate with cheap probes: version inventory, import checks, build checks, device-tree/config review, dry-run, or small sample inference.

## Guardrails

- Do not assume a microcontroller can run model inference or networking without checking memory, timing, and power.
- Do not assume Jetson/CUDA/TensorRT availability from a project name. Verify JetPack, drivers, CUDA, cuDNN, TensorRT, and target module.
- Keep real-time safety/control paths separate from high-latency AI reasoning paths.
- Require watchdog, safe boot, log retrieval, and rollback/update notes for field devices.
- Add `aiwf-nvidia-cuda-cudnn-sdk` for CUDA/cuDNN/TensorRT code details.
- Add `aiwf-robotics-systems` for sensor/actuator integration and robot architecture.
- Add `aiwf-networking-iot` for telemetry, device networking, MQTT, or customer-site connectivity.

## Validation Defaults

Use available local checks only:

```powershell
nvidia-smi
nvcc --version
python -c "import platform; print(platform.platform())"
python -m pytest <embedded-or-edge-tests>
```

For microcontroller or RTOS work, prefer build/config validation unless a device is explicitly connected and approved for flashing.

## Primary Source Anchors

- NVIDIA Jetson embedded systems: https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/
- NVIDIA JetPack: https://developer.nvidia.com/embedded/jetpack
- Zephyr Project documentation: https://docs.zephyrproject.org/latest/index.html
- FreeRTOS documentation: https://www.freertos.org/

Verify the exact board, SDK, and firmware toolchain before recommending install, flash, or deployment steps.
