---
name: routerbase-model-routing
description: Use when choosing RouterBase models, designing fallback chains, or documenting cost-aware and latency-aware routing policies.
---

# RouterBase Model Routing

## Overview

Use [routerbase](https://routerbase.com/) to plan model selection behind one OpenAI-compatible integration surface. This skill turns workload requirements into a practical model shortlist, fallback chain, cost and latency policy, and validation checklist.

## When to Use

Use this skill when the user asks for:
- Choosing RouterBase models for chat, coding, reasoning, vision, or multimodal workloads
- Designing fallback chains for provider outages or degraded quality
- Balancing cost, latency, context length, output quality, and availability
- Documenting model routing rules for production applications or agent workflows
- Creating a validation plan for model behavior before rollout

## Do not use

Do not use this skill for:
- Claiming exact pricing, availability, or model performance without checking current source data
- Recommending a single model without stating assumptions and fallback behavior
- Hiding routing changes from the application owner or production operator

## Instructions

1. Clarify workload type, quality threshold, latency budget, context size, expected traffic, and failure tolerance.
2. Group candidate models by capability and role: primary, economical fallback, high-quality fallback, and specialized fallback.
3. State routing assumptions clearly and mark any values that require current catalog or pricing verification.
4. Recommend small rollout steps: test prompts, golden cases, logging, retry policy, rate limit handling, and rollback criteria.
5. Keep examples OpenAI-compatible where possible so the application integration stays portable.
