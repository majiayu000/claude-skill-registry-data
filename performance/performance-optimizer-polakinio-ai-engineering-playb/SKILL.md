---
name: performance-optimizer
description: Review or plan changes that affect latency, throughput, caching, batching, scaling behavior, or duplicate work.
metadata:
  short-description: Optimize performance-critical changes safely
---

# performance-optimizer

## Purpose During Development

Use this skill when Codex and similar AI coding agents are reviewing or implementing performance-related changes such as latency reduction, duplicate-work removal, scaling improvements, batching, caching, or throughput improvements.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being reviewed.

## When To Apply

- performance-focused features or refactors
- PRs that claim to speed up code paths
- bugs involving timeouts, duplicate work, memory growth, or slow orchestration
- changes that introduce caching, batching, concurrency, or reuse

## What To Inspect

- performance goals or claims
- instrumentation, traces, or timing evidence
- high-cost paths and repeated calls
- cache or reuse semantics
- tests or benchmarks that verify the claim

## Rules To Enforce

- require evidence for performance claims
- remove duplicate work before speculative micro-optimization
- keep performance behavior visible and debuggable
- do not weaken safety, correctness, or contract clarity for speed
- make caching and reuse explicit to callers and reviewers

## Common Anti-Patterns To Catch

- performance claims without measurement
- hidden or stale caches
- performance shortcuts that skip validation or safety controls
- optimizing low-cost code while ignoring dominant bottlenecks
- scattering reuse logic across unrelated modules

## Expected Output From The Agent

- bottleneck summary
- evidence review
- optimization options with trade-offs
- regression risks
- verification guidance

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Evidence Reviewed
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Review this PR that claims to reduce latency and check whether the evidence supports the claim."

"Use this skill to plan safe duplicate-work reduction in a multi-stage workflow."
