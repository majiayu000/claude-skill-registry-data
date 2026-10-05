---
name: ai-research-skills
description: "AI/ML engineering and research library: 98 modules for model training, RAG, evaluation, experiments, research ideas, papers and plots. TR: AI araştır, model eğit, RAG kur, ML makalesi, deney planla."
license: MIT
---

# AI Research Skills Library

Upstream [orchestra-research/AI-research-SKILLs](https://github.com/orchestra-research/AI-research-SKILLs) (MIT, 773a529 2026-06-15) — full library. Upstream technical resources are retained; controlling instructions in autoresearch and research-manager have documented authorization/privacy adaptations; paths inside a module are relative to that module's folder.

## Execution protocol

Read [research execution and data boundaries](yigit/execution-protocol.md) before any module. Existing host permissions and task-specific authorization apply to every technical example.

## How to use

- Starting or steering an AI/ML research project end to end → `autoresearch` module; it routes to the domain modules below.
- A specific framework, technique or deliverable → open that module directly and read it completely.
- Research or thesis ideas in any field → `brainstorming-research-ideas`, then `creative-thinking-for-research`; translate CS/ML examples to the user's field.
- Install the Python packages a module lists only when the task needs them; ask before installing GPU, cloud or paid tooling.

## Modules by category

### 0-autoresearch-skill

- [`autoresearch`](modules/autoresearch/MODULE.md) — Orchestrates end-to-end autonomous AI research projects using a two-loop architecture.

### 01-model-architecture

- [`litgpt`](modules/litgpt/MODULE.md) — Implements and trains LLMs using Lightning AI's LitGPT with 20+ pretrained architectures (Llama, Gemma, Phi, Qwen, Mistral).
- [`mamba`](modules/mamba/MODULE.md) — State-space model with O(n) complexity vs Transformers' O(n²).
- [`nanogpt`](modules/nanogpt/MODULE.md) — Educational GPT implementation in ~300 lines.
- [`rwkv`](modules/rwkv/MODULE.md) — RNN+Transformer hybrid with O(n) inference.
- [`torchtitan`](modules/torchtitan/MODULE.md) — Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP).

### 02-tokenization

- [`huggingface-tokenizers`](modules/huggingface-tokenizers/MODULE.md) — Fast tokenizers optimized for research and production.
- [`sentencepiece`](modules/sentencepiece/MODULE.md) — Language-independent tokenizer treating text as raw Unicode.

### 03-fine-tuning

- [`axolotl`](modules/axolotl/MODULE.md) — Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support
- [`llama-factory`](modules/llama-factory/MODULE.md) — Expert guidance for fine-tuning LLMs with LLaMA-Factory - WebUI no-code, 100+ models, 2/3/4/5/6/8-bit QLoRA, multimodal support
- [`peft`](modules/peft/MODULE.md) — Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods.
- [`unsloth`](modules/unsloth/MODULE.md) — Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization

### 04-mechanistic-interpretability

- [`nnsight`](modules/nnsight/MODULE.md) — Provides guidance for interpreting and manipulating neural network internals using nnsight with optional NDIF remote execution.
- [`pyvene`](modules/pyvene/MODULE.md) — Provides guidance for performing causal interventions on PyTorch models using pyvene's declarative intervention framework.
- [`saelens`](modules/saelens/MODULE.md) — Provides guidance for training and analyzing Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpre…
- [`transformer-lens`](modules/transformer-lens/MODULE.md) — Provides guidance for mechanistic interpretability research using TransformerLens to inspect and manipulate transformer internals via HookP…

### 05-data-processing

- [`nemo-curator`](modules/nemo-curator/MODULE.md) — GPU-accelerated data curation for LLM training.
- [`ray-data`](modules/ray-data/MODULE.md) — Scalable data processing for ML workloads.

### 06-post-training

- [`grpo-rl-training`](modules/grpo-rl-training/MODULE.md) — Expert guidance for GRPO/RL fine-tuning with TRL for reasoning and task-specific model training
- [`miles`](modules/miles/MODULE.md) — Provides guidance for enterprise-grade RL training using miles, a production-ready fork of slime.
- [`openrlhf`](modules/openrlhf/MODULE.md) — High-performance RLHF framework with Ray+vLLM acceleration.
- [`simpo`](modules/simpo/MODULE.md) — Simple Preference Optimization for LLM alignment.
- [`slime`](modules/slime/MODULE.md) — Provides guidance for LLM post-training with RL using slime, a Megatron+SGLang framework.
- [`torchforge`](modules/torchforge/MODULE.md) — Provides guidance for PyTorch-native agentic RL using torchforge, Meta's library separating infra from algorithms.
- [`trl-fine-tuning`](modules/trl-fine-tuning/MODULE.md) — Fine-tune LLMs using reinforcement learning with TRL - SFT for instruction tuning, DPO for preference alignment, PPO/GRPO for reward optimi…
- [`verl`](modules/verl/MODULE.md) — Provides guidance for training LLMs with reinforcement learning using verl (Volcano Engine RL).

### 07-safety-alignment

- [`constitutional-ai`](modules/constitutional-ai/MODULE.md) — Anthropic's method for training harmless AI through self-improvement.
- [`llamaguard`](modules/llamaguard/MODULE.md) — Meta's 7-8B specialized moderation model for LLM input/output filtering.
- [`nemo-guardrails`](modules/nemo-guardrails/MODULE.md) — NVIDIA's runtime safety framework for LLM applications.
- [`prompt-guard`](modules/prompt-guard/MODULE.md) — Meta's 86M prompt injection and jailbreak detector.

### 08-distributed-training

- [`accelerate`](modules/accelerate/MODULE.md) — Simplest distributed training API.
- [`deepspeed`](modules/deepspeed/MODULE.md) — Expert guidance for distributed training with DeepSpeed - ZeRO optimization stages, pipeline parallelism, FP16/BF16/FP8, 1-bit Adam, sparse…
- [`megatron-core`](modules/megatron-core/MODULE.md) — Trains large language models (2B-462B parameters) using NVIDIA Megatron-Core with advanced parallelism strategies.
- [`pytorch-fsdp2`](modules/pytorch-fsdp2/MODULE.md) — Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed precision/offload config, and distributed checkpoin…
- [`pytorch-lightning`](modules/pytorch-lightning/MODULE.md) — High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks system, and minimal boilerp…
- [`ray-train`](modules/ray-train/MODULE.md) — Distributed training orchestration across clusters.

### 09-infrastructure

- [`lambda-labs`](modules/lambda-labs/MODULE.md) — Reserved and on-demand GPU cloud instances for ML training and inference.
- [`modal`](modules/modal/MODULE.md) — Serverless GPU cloud platform for running ML workloads.
- [`skypilot`](modules/skypilot/MODULE.md) — Multi-cloud orchestration for ML workloads with automatic cost optimization.

### 10-optimization

- [`awq`](modules/awq/MODULE.md) — Activation-aware weight quantization for 4-bit LLM compression with 3x speedup and minimal accuracy loss.
- [`bitsandbytes`](modules/bitsandbytes/MODULE.md) — Quantizes LLMs to 8-bit or 4-bit for 50-75% memory reduction with minimal accuracy loss.
- [`flash-attention`](modules/flash-attention/MODULE.md) — Optimizes transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction.
- [`gguf`](modules/gguf/MODULE.md) — GGUF format and llama.cpp quantization for efficient CPU/GPU inference.
- [`gptq`](modules/gptq/MODULE.md) — Post-training 4-bit quantization for LLMs with minimal accuracy loss.
- [`hqq`](modules/hqq/MODULE.md) — Half-Quadratic Quantization for LLMs without calibration data.
- [`ml-training-recipes`](modules/ml-training-recipes/MODULE.md) — Battle-tested PyTorch training recipes for all domains — LLMs, vision, diffusion, medical imaging, protein/drug discovery, spatial omics, g…

### 11-evaluation

- [`bigcode-evaluation-harness`](modules/bigcode-evaluation-harness/MODULE.md) — Evaluates code generation models across HumanEval, MBPP, MultiPL-E, and 15+ benchmarks with pass@k metrics.
- [`lm-evaluation-harness`](modules/lm-evaluation-harness/MODULE.md) — Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag).
- [`nemo-evaluator`](modules/nemo-evaluator/MODULE.md) — Evaluates LLMs across 100+ benchmarks from 18+ harnesses (MMLU, HumanEval, GSM8K, safety, VLM) with multi-backend execution.

### 12-inference-serving

- [`llama-cpp`](modules/llama-cpp/MODULE.md) — Runs LLM inference on CPU, Apple Silicon, and consumer GPUs without NVIDIA hardware.
- [`sglang`](modules/sglang/MODULE.md) — Fast structured generation and serving for LLMs with RadixAttention prefix caching.
- [`tensorrt-llm`](modules/tensorrt-llm/MODULE.md) — Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency.
- [`vllm`](modules/vllm/MODULE.md) — Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching.

### 13-mlops

- [`mlflow`](modules/mlflow/MODULE.md) — Track ML experiments, manage model registry with versioning, deploy models to production, and reproduce experiments with MLflow - framework…
- [`swanlab`](modules/swanlab/MODULE.md) — Provides guidance for experiment tracking with SwanLab.
- [`tensorboard`](modules/tensorboard/MODULE.md) — Visualize training metrics, debug models with histograms, compare experiments, visualize model graphs, and profile performance with TensorB…
- [`weights-and-biases`](modules/weights-and-biases/MODULE.md) — Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model regist…

### 14-agents

- [`a-evolve`](modules/a-evolve/MODULE.md) — Provides guidance for automatically evolving and optimizing AI agents across any domain using LLM-driven evolution algorithms.
- [`autogpt`](modules/autogpt/MODULE.md) — Autonomous AI agent platform for building and deploying continuous agents.
- [`crewai`](modules/crewai/MODULE.md) — Multi-agent orchestration framework for autonomous AI collaboration.
- [`langchain`](modules/langchain/MODULE.md) — Framework for building LLM-powered applications with agents, chains, and RAG.
- [`llamaindex`](modules/llamaindex/MODULE.md) — Data framework for building LLM applications with RAG.

### 15-rag

- [`chroma`](modules/chroma/MODULE.md) — Open-source embedding database for AI applications.
- [`faiss`](modules/faiss/MODULE.md) — Facebook's library for efficient similarity search and clustering of dense vectors.
- [`pinecone`](modules/pinecone/MODULE.md) — Managed vector database for production AI applications.
- [`qdrant`](modules/qdrant/MODULE.md) — High-performance vector similarity search engine for RAG and semantic search.
- [`sentence-transformers`](modules/sentence-transformers/MODULE.md) — Framework for state-of-the-art sentence, text, and image embeddings.

### 16-prompt-engineering

- [`dspy`](modules/dspy/MODULE.md) — Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy - St…
- [`guidance`](modules/guidance/MODULE.md) — Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step work…
- [`instructor`](modules/instructor/MODULE.md) — Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type s…
- [`outlines`](modules/outlines/MODULE.md) — Guarantee valid JSON/XML/code structure during generation, use Pydantic models for type-safe outputs, support local models (Transformers, v…

### 17-observability

- [`langsmith`](modules/langsmith/MODULE.md) — LLM observability platform for tracing, evaluation, and monitoring.
- [`phoenix`](modules/phoenix/MODULE.md) — Open-source AI observability platform for LLM tracing, evaluation, and monitoring.

### 18-multimodal

- [`audiocraft`](modules/audiocraft/MODULE.md) — PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen).
- [`blip-2`](modules/blip-2/MODULE.md) — Vision-language pre-training framework bridging frozen image encoders and LLMs.
- [`clip`](modules/clip/MODULE.md) — OpenAI's model connecting vision and language.
- [`cosmos-policy`](modules/cosmos-policy/MODULE.md) — Evaluates NVIDIA Cosmos Policy on LIBERO and RoboCasa simulation environments.
- [`llava`](modules/llava/MODULE.md) — Large Language and Vision Assistant.
- [`openpi`](modules/openpi/MODULE.md) — Fine-tune and serve Physical Intelligence OpenPI models (pi0, pi0-fast, pi0.5) using JAX or PyTorch backends for robot policy inference acr…
- [`openvla-oft`](modules/openvla-oft/MODULE.md) — Fine-tunes and evaluates OpenVLA-OFT and OpenVLA-OFT+ policies for robot action generation with continuous action heads, LoRA adaptation, a…
- [`segment-anything`](modules/segment-anything/MODULE.md) — Foundation model for image segmentation with zero-shot transfer.
- [`stable-diffusion`](modules/stable-diffusion/MODULE.md) — State-of-the-art text-to-image generation with Stable Diffusion models via HuggingFace Diffusers.
- [`whisper`](modules/whisper/MODULE.md) — OpenAI's general-purpose speech recognition model.

### 19-emerging-techniques

- [`knowledge-distillation`](modules/knowledge-distillation/MODULE.md) — Compress large language models using knowledge distillation from teacher to student models.
- [`long-context`](modules/long-context/MODULE.md) — Extend context windows of transformer models using RoPE, YaRN, ALiBi, and position interpolation techniques.
- [`model-merging`](modules/model-merging/MODULE.md) — Merge multiple fine-tuned models using mergekit to combine capabilities without retraining.
- [`model-pruning`](modules/model-pruning/MODULE.md) — Reduce LLM size and accelerate inference using pruning techniques like Wanda and SparseGPT.
- [`moe-training`](modules/moe-training/MODULE.md) — Train Mixture of Experts (MoE) models using DeepSpeed or HuggingFace.
- [`speculative-decoding`](modules/speculative-decoding/MODULE.md) — Accelerate LLM inference using speculative decoding, Medusa multiple heads, and lookahead decoding techniques.

### 20-ml-paper-writing

- [`academic-plotting`](modules/academic-plotting/MODULE.md) — Generates publication-quality figures for ML papers from research context.
- [`ml-paper-writing`](modules/ml-paper-writing/MODULE.md) — Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI, COLM.
- [`presenting-conference-talks`](modules/presenting-conference-talks/MODULE.md) — Generates conference presentation slides (Beamer LaTeX PDF and editable PPTX) from a compiled paper with speaker notes and talk script.
- [`systems-paper-writing`](modules/systems-paper-writing/MODULE.md) — Comprehensive guide for writing systems papers targeting OSDI, SOSP, ASPLOS, NSDI, and EuroSys.

### 21-research-ideation

- [`brainstorming-research-ideas`](modules/brainstorming-research-ideas/MODULE.md) — Guides researchers through structured ideation frameworks to discover high-impact research directions.
- [`creative-thinking-for-research`](modules/creative-thinking-for-research/MODULE.md) — Applies cognitive science frameworks for creative thinking to CS and AI research ideation.

### 22-agent-native-research-artifact

- [`compiler`](modules/compiler/MODULE.md) — Compiles any research input — PDF papers, GitHub repositories, experiment logs, code directories, or raw notes — into a complete Agent-Nati…
- [`research-manager`](modules/research-manager/MODULE.md) — Records research provenance as a post-task epilogue, scanning conversation history at the end of a coding or research session to extract de…
- [`rigor-reviewer`](modules/rigor-reviewer/MODULE.md) — Performs ARA Seal Level 2 semantic epistemic review on Agent-Native Research Artifacts, scoring six dimensions (evidence relevance, falsifi…
