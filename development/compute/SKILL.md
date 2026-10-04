---
name: compute
description: High-performance numerical and quantum compute skill for scientific workloads; use when working on numeric algorithms, simulation, or acceleration.
---

# Skill: Compute

Domain: `build` | Depth: `axiom`

## Capabilities
- High-performance numerical computation (numpy, scipy, numba)
- JIT compilation for CPU/GPU acceleration (numba)
- Scientific computing: optimization, integration, interpolation (scipy)
- Quantum circuit simulation (qiskit, pennylane, cirq)
- GPU tensor compute via Apple MPS (torch)
- Parallel and vectorized operations

## Apple Silicon (local)

| Path | Role |
|------|------|
| `agents/core/stream.py` | MLX + Ollama streaming |
| `agents/core/memory/vector.py` | ONNX Runtime → CoreML EP (Neural Engine) for embeddings |
| `scripts/mlx-neural-bridge.sh` | Trinity MLX HTTP helper (mirror `nexus-core/mlx-neural-bridge.py`) |

## Libraries
| Library   | Purpose |
|-----------|---------|
| numpy     | Vectorized array compute |
| scipy     | Scientific algorithms |
| numba     | JIT compilation — CPU/GPU |
| torch     | GPU compute via MPS |
| qiskit    | Quantum circuit simulation |
| pennylane | Quantum ML and variational circuits |
| cirq      | Google quantum framework |

## Module
`agents/skills/compute.py`

## Key Functions
- `jit_compute(fn, *args)` — JIT-compile and run a function
- `optimize(fn, x0)` — numerical optimization
- `fft(signal)` — fast Fourier transform
- `quantum_circuit(gates)` — build and simulate a quantum circuit
- `gpu_tensor(data)` — move tensor to MPS (Apple GPU)
