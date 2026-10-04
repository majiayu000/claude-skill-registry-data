---
name: llm-output-reviewer
description: Review or plan changes that affect prompts, model output validation, fallback behavior, or LLM-driven decisions.
metadata:
  short-description: Review prompts and model-driven behavior
---

# llm-output-reviewer

## Purpose During Development

Use this skill when Codex and similar AI coding agents are reviewing or implementing prompt logic, model output validation, fallback behavior, model-driven decisions, or other LLM-integrated code paths.

This is a reusable development-time reasoning framework. It is not runtime code and must not be coupled into the product being reviewed.

## When To Apply

- prompt or system-instruction changes
- output-schema or validation changes
- fallback-path changes for failed or missing model responses
- PRs that make product behavior depend on model output

## What To Inspect

- prompt construction
- input shaping
- output validation
- fallback behavior
- downstream consumers of model output
- tests or fixtures covering malformed responses

## Rules To Enforce

- raw model output must not be trusted directly
- validated structure must match downstream expectations
- fallback behavior must remain safe and operational
- prompts must not silently demand a new output shape without validation changes
- model-driven decisions must remain bounded by repository policy

## Common Anti-Patterns To Catch

- accepting arbitrary JSON or text without validation
- prompt changes that drift from validators
- fallback behavior that is less safe than the primary path
- passing model output across layers without normalization
- mixing product presentation needs into validator logic

## Expected Output From The Agent

- prompt/output alignment review
- safety and fallback risks
- downstream compatibility concerns
- suggested validation hardening
- regression tests for malformed outputs

## Output Structure

- Summary
- Key Findings
- Risks
- Affected Files
- Affected Flows
- Suggested Improvements
- Suggested Tests
- Skills applied

## Example Usage

"Review this PR for prompt-validator drift and unsafe fallback behavior."

"Use this skill to check whether LLM output remains safe, validated, and consumable."
