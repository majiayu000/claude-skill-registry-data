---
name: nvidia--cosmos
description: "NVIDIA Cosmos — open platform world models cho Physical AI: robotics, autonomous vehicles. Cosmos3-Nano (16B) + Super (64B). Text/video/action I/O. Diffusers/vLLM/NIM. OpenMDW-1.1."
allowed-tools: Bash, Read, Write
user-invocable: true
---

NVIDIA Cosmos: world model platform cho Physical AI — robots và autonomous vehicles hiểu + simulate thế giới vật lý thay vì chỉ generate text.

## Models — Cosmos 3

```
Cosmos3-Nano  (16B)  — compact, multimodal understanding + world simulation
Cosmos3-Super (64B)  — frontier-scale, advanced capabilities

Specialized:
  Text-to-image variants
  Image-to-video variants
  Robot policy models
```

## 2 Runtime Surfaces

```
Reasoner
  Input:  text + vision
  Output: text
  Uses:   world understanding, physical reasoning, task planning, autonomous decisions
  → "Is this grasp stable?" / "What happens if I push this box?"

Generator
  Input:  text + vision + sound + actions
  Output: visual content + audio + action sequences
  Uses:   simulation, synthetic training data, video generation
```

## Deployment Options

```bash
# Diffusers (research/dev)
pip install diffusers transformers
# huggingface: nvidia/Cosmos3-Nano

# vLLM-Omni (production API)
pip install vllm
vllm serve nvidia/Cosmos3-Nano --task generate

# NIM containers (turnkey)
docker run nvcr.io/nim/nvidia/cosmos3-nano:latest

# Cosmos Framework (training + eval)
git clone https://github.com/NVIDIA/cosmos
pip install -e .
```

## Key Capabilities

```
Video captioning + event detection
Embodied reasoning + physical plausibility analysis
Spatial grounding
Text-to-video + image-to-video generation
Action-conditioned simulation
Synthetic training data generation for robotics
```

## Khi nào dùng

- Research: physical AI, embodied reasoning
- Generate synthetic training data cho robot models
- Simulate robot scenarios trước khi deploy hardware
- Video generation có physics-aware

## Khi KHÔNG dùng

- General chatbot — dùng Claude
- Text generation — dùng Claude/GPT
- Requires NVIDIA GPU (A100/H100 recommended cho Super)

## License

OpenMDW-1.1 (custom NVIDIA license, not fully open-source)

## Source

https://github.com/NVIDIA/cosmos · OpenMDW-1.1 · +479⭐/week
