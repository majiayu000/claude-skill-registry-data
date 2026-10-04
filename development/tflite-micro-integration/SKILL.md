---
name: tflite-micro-integration
description: Use when integrating or debugging TensorFlow Lite Micro (LiteRT) on MCUs — op resolver, tensor arena sizing, AllocateTensors, Invoke, int8 quantization, and missing-op errors
---

# TensorFlow Lite Micro Integration

## Overview

Use this skill to bring up TensorFlow Lite for Microcontrollers (TFLM / LiteRT for Microcontrollers) on an MCU: register exactly the ops the model uses, size the `tensor_arena` correctly, and quantize inputs so `Invoke()` returns valid output. Most failures are missing ops, an undersized arena, or unquantized input, not model logic. TFLM is Google's official microcontroller runtime and is integrated by several vendor toolchains — Espressif `esp-tflite-micro` (with ESP-NN kernels), NXP eIQ, and ST X-CUBE-AI, where TFLM is available as an optional runtime alongside ST's own proprietary Cube.AI runtime. Use `tinymaix-integration` instead when you want a lighter, dependency-free runtime.

## When To Use

Use this skill when:

- The user runs `tensorflow/tflite-micro` and works with `tflite::MicroInterpreter`, `tflite::MicroMutableOpResolver`, `AllocateTensors()`, or `Invoke()`.
- The build or runtime hits `Didn't find op for builtin opcode 'CONV_2D'`, `'QUANTIZE'`, arena/`AllocateTensors` failures, or output that is all zeros or drifting.
- The project embeds a `.tflite` model as a C array (`xxd -i`) and needs int8 `scale`/`zero_point` handling.

Do not use this skill when the model is not yet converted and quantized to `.tflite`; run the TFLite converter and validate on the host first.

## First Questions

Ask for:

- Target core, RAM/flash, and toolchain; whether CMSIS-NN / ESP-NN / vendor kernels are used.
- The `.tflite` model, its op list (from Netron or `flatc`), and its input/output dtype (`int8`, `uint8`, or `float32`).
- Current `kTensorArenaSize` and whether `AllocateTensors()` returns `kTfLiteOk`.
- Input `scale`/`zero_point` and expected output; a known golden input/output pair.
- Exact symptom: link error, missing-op error, allocation failure, or wrong output.

## Integration Checklist

1. Convert and embed the model.
   Produce a quantized `.tflite`, then `xxd -i model.tflite > model.cc`. Reference it via `tflite::GetModel(g_model)` and check `model->version() != TFLITE_SCHEMA_VERSION`.

1. Register only the needed ops.
   Use `tflite::MicroMutableOpResolver<N>` where `N` matches the exact count of `AddConv2D()`, `AddDepthwiseConv2D()`, `AddFullyConnected()`, `AddReshape()`, `AddSoftmax()`, `AddQuantize()`, etc. `AllOpsResolver` (which registers all built-in ops) bloats flash; avoid it in production.

1. Allocate the tensor arena.
   Declare `alignas(16) uint8_t tensor_arena[kTensorArenaSize];`, construct `tflite::MicroInterpreter` with the model, resolver, `tensor_arena`, and `kTensorArenaSize`, then use `MicroPrintf` for logging.

1. Allocate tensors and check the code.
   Call `interpreter.AllocateTensors()` and confirm it returns `kTfLiteOk`. Grow `kTensorArenaSize` if it fails, then trim toward `interpreter.arena_used_bytes()`.

1. Quantize the input.
   Read `input->params.scale` and `input->params.zero_point`, compute `q = round(real / scale) + zero_point`, clamp to `[-128, 127]`, and write `input->data.int8[i]`.

1. Invoke and dequantize.
   Check `interpreter.Invoke() == kTfLiteOk`, then convert `output->data.int8[i]` back with `real = (q - zero_point) * scale`.

## Common Failures

- `Didn't find op for builtin opcode 'CONV_2D'` / `'QUANTIZE'`: op missing from the resolver, or `N` in `MicroMutableOpResolver<N>` too small to hold all `Add*` calls.
- Opcode version mismatch (same message with `version 'N'` plus "An older version of this builtin might be supported"): model exported by a newer converter than the runtime; rebuild `tflite-micro` or re-export.
- `AllocateTensors()` fails or returns non-`kTfLiteOk` because `kTensorArenaSize` is too small.
- Output is all zeros or drifts: input written as raw floats/pixels without applying `scale`/`zero_point`.
- Hard fault or stack overflow inside `AllocateTensors()`/`Invoke()`: give the calling thread enough stack (typically several KB).
- Unaligned or too-small `tensor_arena` (missing `alignas(16)`) causing allocation errors.

## Verification

Before claiming TFLM inference works:

- State the model, its op list, input/output dtype, and `kTensorArenaSize` vs `arena_used_bytes()`.
- Confirm `AllocateTensors()` and `Invoke()` both return `kTfLiteOk`.
- Confirm a golden input reproduces the host reference output within quantization tolerance.
- Confirm input quantization and output dequantization use the tensor's actual `scale`/`zero_point`.

## Example

User:

```text
TFLM 里 Invoke 报 "Didn't find op for builtin opcode 'DEPTHWISE_CONV_2D'"。
```

Agent:

1. Asks for the model op list (Netron/`flatc`) and the current `MicroMutableOpResolver<N>` registrations.
1. Adds `resolver.AddDepthwiseConv2D()` and bumps `N` to match the total `Add*` count.
1. Re-runs, confirms `AllocateTensors()` and `Invoke()` return `kTfLiteOk`, and checks a golden vector.
