---
name: nvidia-nca-genl
description: Use when preparing for NVIDIA-Certified Associate Generative AI LLMs (NCA-GENL) — machine-learning and deep-learning fundamentals, transformers and attention, tokenisation and embeddings, prompting, fine-tuning and parameter-efficient methods, retrieval-augmented generation, evaluation, inference optimisation and responsible AI, plus practice questions checked against papers and NVIDIA documentation. Also use when writing or verifying LLM practice questions at associate level.
---

# NVIDIA-Certified Associate: Generative AI LLMs (NCA-GENL)

Bottom line: **understand the transformer pipeline end to end** — text → tokens → embeddings → attention layers → logits → decoding — then the ways to adapt (prompting, RAG, fine-tuning) and to serve (quantisation, batching) a model. Most questions ask which technique fits a situation.

## Exam shape (confirm on NVIDIA's certification page)

- Online, remotely proctored, 60 minutes, in English; multiple-choice questions; pass/fail result; credential valid for a limited period.
- Topics span ML fundamentals, LLM architecture, data and experimentation, software development with LLMs, deployment and trustworthy AI. Check the exam page for current objectives and weights.

Primary sources: NVIDIA certification page (https://www.nvidia.com/en-us/learn/certification/), the exam study guide, original papers (e.g. "Attention Is All You Need", LoRA, RAG), NVIDIA documentation (NeMo, TensorRT-LLM, Triton, NIM).

## Concept map

| Topic | Know |
|---|---|
| ML basics | Supervised/unsupervised, loss, gradient descent, overfitting, regularisation, train/validation/test splits, metrics |
| Architecture | Self-attention (Q, K, V), multi-head attention, positional encoding, encoder-only vs decoder-only vs encoder-decoder, context length |
| Tokens and embeddings | Subword tokenisation (BPE, SentencePiece), embedding vectors, cosine similarity |
| Decoding | Greedy, beam search, temperature, top-k, top-p; effect on diversity and determinism |
| Adaptation | Prompt engineering (zero/few-shot, chain of thought), RAG, full fine-tuning, parameter-efficient fine-tuning (LoRA, adapters, prompt tuning), instruction tuning, RLHF/DPO at a conceptual level |
| RAG | Chunking, embedding models, vector search, re-ranking, grounding and citations; when RAG beats fine-tuning (changing knowledge) |
| Evaluation | Perplexity, BLEU/ROUGE and their limits, task benchmarks, human and model-graded evaluation, hallucination checks |
| Inference | Quantisation (INT8/FP8/INT4), KV cache, batching, tensor/pipeline parallelism, latency vs throughput |
| Trustworthy AI | Bias, privacy, safety guardrails, data licensing, transparency |

## Study loop

1. Explain the forward pass of a decoder-only model aloud, naming tensor shapes at each step.
2. For each adaptation method: what changes (weights, inputs, retrieval), cost, data needed, and when it fails.
3. Do quick calculations: parameters × bytes per parameter = memory for weights; how quantisation changes it.
4. Practise scenario questions and justify each option.

## Writing practice questions

- Ground definitions in the original papers or NVIDIA documentation; recompute any numbers.
- Create situations (a team with little labelled data, frequently changing documents, strict latency) rather than definitions only.

## Pitfalls

- Thinking fine-tuning is the default way to add new facts (RAG usually fits changing knowledge better).
- Confusing temperature with top-p, or perplexity with accuracy.
- Assuming larger context always improves answers (cost and "lost in the middle" effects).
- Mixing encoder-only models (good for embeddings/classification) with decoder-only generators.

## Self-check

- A practice set within 60 minutes with clear margin.
- Explain LoRA in three sentences including what is frozen and what is trained.
- Choose and justify an approach for five different product scenarios.
