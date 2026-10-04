---
name: edge-ai
description: "TinyML, neural network quantization (INT8), pruning, edge accelerators (Google Coral, Hailo, Jetson), and embedded inference"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/edge-ai/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# TinyML & Edge AI

## Scope
Edge AI deploys optimized deep learning inference models directly onto resource-constrained microcontrollers and edge accelerators with milliwatt power budgets.

## Model Optimization & Quantization
- **Quantization**: Converting 32-bit floating point weights ($FP32$) to 8-bit integers ($INT8$):
  $$q = \operatorname{round}\left(\frac{x}{S}\right) + Z$$
  where $S$ is scale factor and $Z$ is zero-point; reduces memory footprint by $75\%$ with minimal accuracy degradation.
- **Model Pruning**: Removing redundant weights and channels (structured/unstructured pruning).
- **Embedded Inference Engines**: TensorFlow Lite for Microcontrollers (TFLM), Edge Impulse, CMSIS-NN, ONNX Runtime.

## Tools & Standards
- **Hardware**: ARM Cortex-M55/M85 (with Helium vector extensions), ESP32-S3, Google Coral TPU, NVIDIA Jetson.
- **Canonical References**: Warden & Situnayake — *TinyML: Machine Learning with TensorFlow Lite on Arduino and Ultra-Low-Power Microcontrollers*.
