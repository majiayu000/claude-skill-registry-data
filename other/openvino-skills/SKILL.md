---
name: openvino-skills
description: End-to-end OpenVINO standard operating procedures for model conversion, quantization/compression, deployment, smoke testing, benchmarking, device selection, and troubleshooting. Use when the user asks to deploy a model with OpenVINO, convert or quantize a Hugging Face/ONNX/TensorFlow/PyTorch model to OpenVINO IR, serve models with OpenVINO Model Server or OpenAI-compatible endpoints, test local OpenVINO artifacts, or benchmark CPU/GPU/NPU/AUTO performance.
---

# OpenVINO SOP

## Language

Use Chinese by default for user-facing explanations, progress updates, final reports, and troubleshooting summaries. Keep command names, code, model ids, file paths, API names, and OpenVINO technical terms in their original form when that is clearer or required for execution.

## Core Rule

Treat OpenVINO work as a pipeline: lock inputs, convert or pull the model, validate files, run a smoke test, deploy, benchmark, then document the exact device/config/result. Do not jump straight to deployment before the artifact has been validated locally.

## Workflow Selector

1. **Convert or quantize a model**: read `references/convert-quantize-sop.md`.
2. **Deploy or serve a model**: read `references/deploy-sop.md`.
3. **Test or benchmark a model**: read `references/test-benchmark-sop.md`.
4. **Choose CPU/GPU/NPU/AUTO or debug failures**: read `references/device-troubleshooting-sop.md`.
5. **Start from a model/use-case type**: read `references/model-playbooks.md`.
6. **Use a known local model case**: read `references/local-model-cases.md`.
7. **Target NPU specifically**: read `references/npu-playbook.md`.
8. **Handle Windows/WSL paths**: read `references/path-conventions.md`.

For remote HPCCube model quantization and delivery to `D:\models\ov`, use the separate `openvino-model-quantization` skill.

## Required Preflight

Before making changes or running long jobs, record:

- Source model id/path and license/access constraints.
- Task type: `text-generation`, `feature-extraction`, `rerank`, `text-to-image`, `image-to-text`, ASR, CV classification/detection, or generic IR.
- Target artifact directory, usually `D:\models\ov\<name>` for local Windows storage. Use `/mnt/d/models/ov/<name>` only inside WSL/Linux commands.
- Target device: `CPU`, `GPU`, `NPU`, `AUTO`, or explicit priority such as `AUTO:GPU,CPU`.
- Precision target: FP32/FP16, INT8, INT4, NF4, or already-compressed OpenVINO model.
- Deployment target: Python runtime, OpenVINO GenAI, OVMS Docker, OVMS bare metal, or KServe.

## Done Criteria

A task is not complete until these are reported:

- Final model path and key files (`.xml`/`.bin`, tokenizer files, `openvino_config.json` when applicable).
- Conversion/quantization command and major options.
- Device probe or target-device confirmation.
- Smoke-test command and result.
- Benchmark result when performance was part of the request.
- Deployment command or endpoint, including port, task, model name, and target device.

Use `references/report-template.md` for the final report shape when the task includes conversion, deployment, or benchmarking.

## Low-Friction Tools

- `scripts/inspect_openvino_artifact.py <MODEL_DIR>`: classify and check a local OpenVINO artifact folder.
- `scripts/openvino_probe.py`: print OpenVINO version and available devices.
- `scripts/smoke_llm.py <MODEL_DIR> --device CPU`: run a small Optimum causal-LM generation smoke test.
- `scripts/smoke_embedding.py <MODEL_DIR>`: run a small Optimum feature-extraction smoke test.
- `scripts/benchmark_openvino_model.py <MODEL_DIR> --kind llm --devices CPU GPU NPU`: run a repeatable local benchmark wrapper.
- `scripts/ovms_chat_smoke.py --model <MODEL_NAME>`: call OVMS `/v3/chat/completions`.
