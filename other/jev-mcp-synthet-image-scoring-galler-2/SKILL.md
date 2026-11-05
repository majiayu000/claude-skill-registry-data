---
name: jev-mcp
description: Use when evaluating typed semantic judgments with TypeSafe Jev / System One — Choice, Score, or Noul questions against text or structured state; also when reranking candidates, verifying evidence support, routing/classifying text, or the user mentions jev-mcp, jev_choice, jev_score, jev_noul, or jev_system_one.
capability: "TypeSafe System One judgments via jev-mcp"
side_effect_level: remote_write
approval_required: true
requires_tools: "MCP server jev-rw-systemone (jev_choice, jev_score, jev_noul, jev_system_one)"
output_schema: "Normalized judgment envelope with model, usage, and answers"
risk_class: medium
---

# Jev MCP (System One)

Prefer MCP tools from **`jev-rw-systemone`** when connected. Each call hits the paid TypeSafe API —
batch related questions in one `jev_system_one` request when possible.

Jev is **not** a generative LLM and **not** a vision model. `state` must be a string, JSON object,
or array of strings. Preprocess images/audio into text fields before calling.

## Tools

| Tool | Use when |
|------|----------|
| `jev_choice` | Pick one label from a closed set |
| `jev_score` | Score along ordered criteria levels |
| `jev_noul` | Yes/no probability for one proposition |
| `jev_system_one` | Multiple typed questions against the same `state` |

Default model pin is `jev-1.13.0` (override only when the user asks). Keep workflow, side effects,
and deterministic rules in normal code; give Jev narrow semantic judgments only.

## How to call

1. Confirm `jev-rw-systemone` is connected. If not, say so and stop — do not invent probabilities.
2. Build compact `state` with only the fields the questions need.
3. Prefer one `jev_system_one` over many single-tool calls.
4. Read `ok` / `error` envelopes. On `missing_credential`, tell the user to set `JEV_TOKEN` (or
   `TYPESAFE_API_KEY`); never invent keys.
5. Return the selected answer fields (`choice` / `score` / `noul`), `confidence` / `probabilities`
   when present, and the `model` used. Do not dump secrets or raw SDK internals.

## Harness decision points (automatic)

This repo's Claude Code hooks call the sibling backend harness
(`../image-scoring-pipeline/scripts/agent_harness`), which asks Jev per-turn questions through the
backend's `modules/typesafe` client: which rule packs a request sees, whether a script may run, whether
files may go to an external reviewer, whether a subtask can leave the main model, and whether a subgoal
is a duplicate. Modes live in `.agent/jev_harness.json`. See
[JEV_AGENT_HARNESS.md](https://github.com/synthet/image-scoring-pipeline/blob/master/docs/technical/JEV_AGENT_HARNESS.md).
Use the `jev-rw-systemone` MCP tools for ad-hoc judgments; leave those decision points to the harness.

## Boundaries

- Do not treat Jev as a chat model, coder, or image judge.
- Do not bypass MCP by pasting API keys into prompts or tool args.
- Canonical server lives at `D:\Projects\jev-mcp` (`AGENTS.md`, `README.md`).
