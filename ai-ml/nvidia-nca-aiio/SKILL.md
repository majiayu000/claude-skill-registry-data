---
name: nvidia-nca-aiio
description: Use when preparing for NVIDIA-Certified Associate AI Infrastructure and Operations (NCA-AIIO) — AI and accelerated-computing fundamentals, GPU servers and interconnects, data-centre networking and storage for AI, power and cooling, cluster management and monitoring, virtualisation and containers for AI workloads, and practising with questions checked against NVIDIA documentation. Also use when writing or verifying practice questions on AI infrastructure at associate level.
---

# NVIDIA-Certified Associate: AI Infrastructure and Operations (NCA-AIIO)

Bottom line: **it is an infrastructure exam with an AI vocabulary**. Know why AI workloads need GPUs, how GPUs are connected and fed with data, and how clusters are scheduled and monitored — at the level of "which component solves this bottleneck".

## Exam shape (confirm on NVIDIA's certification page)

- Online, remotely proctored, 60 minutes, in English; multiple-choice questions; result reported as pass/fail; the credential is valid for a limited period and renewed by re-taking.
- Areas: essential AI knowledge (AI/ML/DL concepts, training vs inference, the GPU software stack), AI infrastructure (compute, networking, storage, data-centre considerations) and AI operations (management, monitoring, orchestration). Check the exam page for the current weights and objectives.

Primary sources: NVIDIA certification page (https://www.nvidia.com/en-us/learn/certification/), the exam study guide, NVIDIA documentation for the products named in the objectives.

## Concept map

| Topic | Know |
|---|---|
| Why GPUs | Massive parallelism for matrix operations; CPU vs GPU roles; tensor cores and reduced precision (FP16/BF16/FP8, INT8) for training vs inference |
| Training vs inference | Training: large batch, high memory and interconnect bandwidth; inference: latency, throughput, model optimisation and serving |
| Software stack | CUDA, CUDA-X libraries, containers from NGC, frameworks, inference servers (e.g. Triton), NVIDIA AI Enterprise |
| Scale-up interconnect | NVLink / NVSwitch inside a server or rack |
| Scale-out networking | InfiniBand and Ethernet (RoCE) for multi-node training; RDMA; DPUs offloading networking, storage and security |
| Storage | High-throughput parallel or network file systems; GPUDirect Storage avoiding CPU copies |
| Data centre | Power density, liquid vs air cooling, reference architectures (DGX systems and SuperPOD-style designs) |
| Operations | Cluster schedulers (Slurm, Kubernetes with GPU operators), GPU monitoring (DCGM), utilisation and health metrics, Multi-Instance GPU (MIG) and virtual GPUs for sharing |

## Study loop

1. Turn each objective in the study guide into a one-line "problem → component" pair (e.g. "multi-node training stalls on gradient exchange → faster interconnect, RDMA").
2. Read the NVIDIA documentation overview page for each named product; note its purpose, not its configuration flags.
3. Practise scenario questions and justify every option.
4. Revisit terms that sound alike (NVLink vs NVSwitch, MIG vs vGPU, DPU vs SmartNIC) until you can contrast them in one sentence.

## Writing practice questions

- Ground each answer in NVIDIA documentation or the original papers for general AI concepts; verify any arithmetic (memory per parameter, bandwidth estimates) by recomputing.
- Use scenarios with different bottlenecks rather than definition lists.

## Pitfalls

- Treating inference and training requirements as the same.
- Confusing scale-up (inside a node) with scale-out (across nodes) networking.
- Assuming more GPUs always helps; data loading and communication often become the bottleneck.
- Mixing up virtualisation options: MIG partitions one GPU in hardware; vGPU shares through a hypervisor.
- Product names change across generations; learn the role, then check current names.

## Self-check

- A practice set within 60 minutes with clear margin.
- Draw a multi-node training cluster from storage to GPUs and label each interconnect.
- Explain three ways to share a GPU among workloads and when to use each.
