---
name: ai-agent-development
description: Design, implement, and evaluate tool-using AI agents with explicit authority, typed tools, bounded loops, state, observability, cost controls, and failure.
license: MIT
---

# AI Agent Development

## Start with a task contract

Define users, goal, success metrics, allowed data/actions, prohibited actions, latency/cost limits, human approval points, failure impact, and deterministic alternatives. Do not build an agent when a normal function, workflow engine, or rules system is sufficient.

## Architecture

- Keep policy/authority in application code, not prompt text alone.
- Give tools narrow typed schemas, clear effects, least privilege, timeouts, idempotency, and safe errors.
- Separate read-only planning from mutating execution; require confirmation for destructive, costly, privileged, or externally visible actions.
- Bound steps, tool rounds, retries, concurrency, tokens, elapsed time, and spend.
- Treat user input, retrieved content, web pages, files, tool output, and memory as untrusted data.
- Keep durable state explicit and versioned. Store decisions/artifact pointers, not private chain-of-thought.
- Use multiple agents only for separable work or independent review; assign disjoint write ownership and integrate through evidence gates.

## Runtime neutrality

Inspect the installed SDK/provider packages and project configuration first. Keep model/provider IDs configurable and verify current support for tools, structured output, streaming, multimodal input, context, data retention, and reasoning controls. Do not switch providers, select a fixed model, or change reasoning effort automatically.

## Reliability and security

Validate every tool argument and model output. Add authorization at the tool/service boundary, replay protection, rate/resource limits, secret redaction, audit events, cancellation, circuit breakers, and bounded retries. Defend against prompt injection by separating instructions from data and rechecking authority before each effect.

## Evaluation

Build offline fixtures for normal, ambiguous, adversarial, missing-data, tool-failure, timeout, duplicate, and unauthorized-action cases. Measure task success, unsupported claims, schema/tool errors, denied actions, steps, latency, cost, and recovery. Use deterministic checks plus calibrated human review. Run a live smoke test only when credentials/network/cost are authorized.

## Completion report

Document architecture, tool contracts, authority matrix, state/memory, provider configuration source, limits, observability, evaluation results, deployment/rollback, and residual risks.
