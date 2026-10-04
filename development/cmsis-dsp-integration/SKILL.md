---
name: cmsis-dsp-integration
description: Use when integrating, configuring, or debugging CMSIS-DSP, ARM math functions, FFT, filters, fixed-point DSP, vector math, or Cortex-M signal processing
---

# CMSIS-DSP Integration

## Overview

Use this skill to integrate CMSIS-DSP by matching the target core, FPU/DSP extensions, data type, scaling, and buffer alignment. DSP bugs often come from numeric format and build flags rather than function calls.

## When To Use

Use this skill when:

- The user wants CMSIS-DSP or ARM math functions on Cortex-M or Cortex-A/R targets.
- The task involves FFT, FIR/IIR filters, matrix math, statistics, PID, Q15/Q31/f32, or optimized vector operations.
- Results are wrong, saturated, NaN, too slow, or differ from desktop reference output.

Do not use this skill for TinyML inference runtime integration. Use `tinymaix-integration` or ML-specific skills instead.

## First Questions

Ask for:

- MCU/core, FPU/DSP extension, compiler, and build flags.
- CMSIS-DSP version and how it is included.
- Function family and data type: f32, f16, q7, q15, q31, or mixed.
- Input range, expected output, reference data, and buffer sizes.
- Whether performance, code size, or accuracy is the primary goal.

## Integration Checklist

1. Match core flags.
   Compiler options must match FPU, ABI, and DSP extensions.

1. Choose numeric format deliberately.
   Fixed-point Q formats need scaling, saturation, and headroom analysis.

1. Validate buffers.
   FFT/filter/state buffers must be sized and aligned as required.

1. Compare with golden vectors.
   Use known input/output before live sensor data.

1. Measure performance on target.
   Desktop estimates do not prove MCU timing.

## Common Failures

- FPU ABI mismatch between objects.
- Q15/Q31 overflow from missing scaling.
- FFT length or bit-reversal config wrong.
- Filter state buffer too small.
- Cache/DMA buffer incoherency around ADC/audio data.
- Reference output uses different normalization.

## Verification

Before claiming CMSIS-DSP works:

- State core, build flags, data type, function, and buffer sizes.
- Confirm golden-vector output within tolerance.
- Confirm no saturation/NaN unless expected.
- Report runtime cycles/time if performance is in scope.

## Example

User:

```text
CMSIS-DSP 做 FFT 结果不对。
```

Agent:

1. Asks for core flags, FFT length, data type, input scaling, and reference output.
1. Checks buffer sizes and normalization.
1. Verifies with a single-tone golden vector before live ADC data.
