---
name: yi-guide
description: Build with 01.AI's Yi models — capable bilingual open models with strong Chinese-English performance.
category: ai-research
---

## Overview

Yi (01.AI, founded by Kai-Fu Lee) is a bilingual open-model family with
particularly strong Chinese-English performance — the Yi models debuted with
impressive benchmark scores in their size classes and a focus on high-quality
bilingual training. Available in multiple sizes including long-context
variants, Yi serves builders needing strong Chinese language capability in an
open model.

For builders, Yi's place is in the bilingual open-model evaluation set: if
your application serves Chinese-speaking users, Yi deserves benchmarking
alongside Qwen, DeepSeek, and other bilingual families. The models run on
standard stacks and are hosted by inference providers.

The practical stance: evaluate Yi where bilingual quality matters. Include it
in the comparison set; let your evals decide.

## When to use

- Bilingual Chinese-English applications needing strong Chinese quality.
- Open-model evaluations for Chinese-language tasks.
- Long-context bilingual document processing (Yi's long-context variants).
- Fine-tuning bilingual base models.
- Self-hosting capable bilingual open models.
- Diversifying beyond the most common open families.

## Core concepts

- **Bilingual training focus**: strong Chinese and English from the training
  mix. For Chinese-language products, this is the relevant axis — test it
  directly.
- **Size options**: multiple sizes across releases. Benchmark the ladder to
  right-size for your task.
- **Long-context variants**: extended-context versions for document-scale
  bilingual work. Test long-context quality on your real documents.
- **Open weights**: downloadable, self-hostable, fine-tunable. Check license
  terms per release.
- **Standard-stack compatibility**: runs on vLLM, TGI, llama.cpp, and
  provider APIs. No special deployment requirements.
- **Instruction-tuned variants**: chat-tuned versions for assistants and
  dialogue.
- **Vision extensions**: multimodal Yi variants for image+text bilingual
  tasks — evaluate against alternatives on your images.
- **Release cadence**: the family evolves; track new releases and re-benchmark
  deliberately.

## Practical workflow

1. **Define bilingual requirements.** Which tasks in Chinese, which in English,
   which mixed? The eval set should reflect the real language mix.
2. **Benchmark against bilingual peers.** Yi vs. Qwen, DeepSeek, and others on
   your bilingual eval set. Per-language scores, not just aggregates.
3. **Test long-context if relevant.** Your longest real bilingual documents;
   questions spanning the input.
4. **Right-size via the ladder.** Smallest adequate size for your quality bar.
5. **Check licensing.** Verify terms per release for your use case.
6. **Evaluate deployment.** API for speed; self-hosted for volume economics.
7. **Pin versions; track releases.** Production pins; deliberate re-evaluation
   on new releases.

Checklist for Yi in production:
- Bilingual eval set reflecting your real language mix.
- Benchmarked against bilingual peer models.
- Long-context validated on real documents (if used).
- License verified; version pinned.
- Deployment economics modeled.

## Common pitfalls

- **Aggregate-score blindness.** A good average hiding weak Chinese (or
  English). Score per language.
- **Ignoring bilingual peers.** Evaluating Yi alone instead of against Qwen,
  DeepSeek, and others. The decision is relative.
- **Long-context assumed.** Extended window without testing quality over long
  bilingual inputs.
- **License not verified.** Assuming terms across releases.
- **Wrong size.** Not ladder-testing; over- or under-provisioning.
- ** monolingual evals for bilingual products.** Testing only English for a
  Chinese-serving product (or vice versa).
- **Version drift.** Floating references updating underneath production.
- **Static choice.** Not re-evaluating as the bilingual open-model field
  advances.
