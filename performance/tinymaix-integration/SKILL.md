---
name: tinymaix-integration
description: Use when integrating, porting, configuring, or debugging TinyMaix MCU inference, model loading, tensor shapes, memory, quantization, or TinyML runtime issues
---

# TinyMaix Integration

## Overview

Use this skill to integrate TinyMaix by proving the model, tensor shapes, preprocessing, memory buffers, and target backend before optimizing inference speed. TinyML failures usually come from mismatched input format, quantization, or insufficient memory.

## When To Use

Use this skill when:

- The user wants to run TinyMaix on an MCU.
- The issue involves model conversion, `tm_load`, `tm_preprocess`, `tm_run`, tensor dimensions, quantized data, RAM/flash limits, or wrong inference results.
- The target has strict RAM, flash, CPU, or accelerator constraints.

Do not use this skill for full ML framework training or model design beyond embedded deployment checks.

## First Questions

Ask for:

- Target MCU/core, RAM/flash, compiler, and whether SIMD/FPU/DSP extensions exist.
- TinyMaix version/source and model format.
- Input shape, data type, quantization, preprocessing, and expected output.
- Memory allocation strategy and inference buffer sizes.
- Current symptom: compile error, load error, run error, wrong output, or too slow.

## Integration Checklist

1. Confirm model compatibility.
   Verify operator set, quantization type, input/output shapes, and converted model files.

1. Prove preprocessing.
   Normalize, resize, color order, layout, and quantization must match training/export assumptions.

1. Budget memory.
   Account for model, activations, input/output tensors, stack, and any temporary buffers.

1. Bring up one known sample.
   Run a golden input with expected output before using live sensor data.

1. Optimize only after correctness.
   CPU extensions, fixed-point paths, and memory placement come after correct inference.

## Common Failures

- Wrong NHWC/NCHW layout or color order.
- Input values are float-scaled but model expects int8/uint8 quantized data.
- Activation buffers overflow RAM.
- Model uses unsupported operations.
- Output interpretation ignores quantization scale/zero point.
- Benchmark uses live noisy data before golden-vector validation.

## Verification

Before claiming TinyMaix works:

- State model, input/output shapes, data type, quantization, and memory budget.
- Confirm a golden input produces expected class/value within tolerance.
- Confirm stack/heap/activation usage fits the target.
- Report inference time if performance is part of the task.

## Example

User:

```text
TinyMaix 跑起来了但识别结果全错。
```

Agent:

1. Asks for model format, input shape, preprocessing, quantization, and golden sample.
1. Checks layout, scale/zero-point, and output decoding.
1. Verifies with a known input before optimizing speed.
