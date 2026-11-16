---
name: microsoft--bitnet
description: "BitNet.cpp — official inference framework cho 1-bit LLMs: 1.37x-6.17x speedup, -55-82% energy. Chạy 100B model trên single CPU 5-7 tok/s. ARM + x86."
allowed-tools: Bash, Read, Write
user-invocable: true
---

BitNet.cpp: inference framework cho 1.58-bit quantized LLMs — lossless, fast, energy-efficient. Chạy model 100B trên CPU thông thường.

## Install

```bash
git clone https://github.com/microsoft/BitNet
cd BitNet
pip install -r requirements.txt
# Build: cmake + make
```

## Usage

```bash
# Inference
python run_inference.py \
  -m models/BitNet-b1.58-2B-4T \
  -p "What is AI?" \
  -cnv

# Benchmark
python benchmark.py -m models/BitNet-b1.58-2B-4T --threads 4

# Convert SafeTensors → BitNet format
python convert_safetensors.py --input model.safetensors
```

## Performance

```
ARM CPUs:  1.37x – 5.07x speedup | -55% – 70% energy
x86 CPUs:  2.37x – 6.17x speedup | -72% – 82% energy

100B model trên single CPU: 5-7 tokens/second
```

## Supported Models

```
Microsoft:
  BitNet-b1.58-2B-4T (2.4B params) — official flagship

Community:
  BitNet 0.7B – 3.3B
  Llama3-8B-1.58
  Falcon3 1B – 10B
  Falcon-E 1B – 3B

Kernels: I2_S, TL1, TL2 (platform-specific)
```

## Khi nào dùng

- Muốn chạy LLM local trên CPU không có GPU
- Edge deployment: embedded systems, IoT
- Energy-constrained environments
- Research: 1-bit quantization effects

## Khi KHÔNG dùng

- Cần full-precision quality → dùng llama.cpp với GGUF
- Cần model lớn hơn (70B+) → hardware constraints vẫn áp dụng

## Source

https://github.com/microsoft/BitNet · MIT · official inference framework
