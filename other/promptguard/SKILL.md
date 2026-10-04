---
name: promptguard
description: >
  Audit system prompts, agent prompts, router prompts, tool/function-call prompts,
  and coding-agent instructions as executable contracts. Use before writing or
  seeding prompts; blocks vague "fix this / write code" tasks missing ownership
  and verification. Works with Hermes, Claude Code, Codex, OpenCode, OpenClaw.
version: 0.4.2
metadata:
  short-description: Audit prompts as executable contracts
  hermes:
    tags: [prompt, safety, guardrails, agents, coding, contracts, pre-write]
    category: devops
---

# PromptGuard

Audit prompts as executable contracts, not writing style.
The core job is to compare what the prompt literally says with what the user expects the model to do.

## When Triggered

Use this skill when the user shares, writes, reviews, debugs, or asks to improve:
- system prompts
- agent/router prompts
- evaluator prompts
- tool or function-call instructions
- prompt files in a repo

## Workflow

1. Identify the surface: TUI, web chat, API, router, tool call, evaluator, or agent persona.
2. Extract contracts: role, task, input, context, output, boundaries, safety escalation, memory/state, tool schema, evaluation.
3. Flag failures: missing contract, conflicting instruction, ambiguous boundary, passive safety escalation, role drift, provider schema mismatch.
   Also flag vague intent, later-rule override, context retention illusion, and false certainty.
   For coding/build prompts, flag missing responsibility, owned surface, constraints, verification, and accountability report.
4. Return findings as:
   `Severity | Evidence | Impact | Missing/Conflicting Contract | Clarification Contract | Questions to Ask | Approval Contract | Fix Draft`

Clarification questions must be generated from the missing decision point. Do not hardcode them to one example like reports.

## Pre-Write Guard

If the user asks to add, save, insert, seed, update, or write a prompt, audit the proposed prompt before editing files.

For pasted prompt text:

```bash
printf '%s' '<prompt text>' | python3 skills/promptguard/scripts/audit_prompt.py - --format markdown
```

If high or critical findings appear, do not write yet. Show findings and ask for explicit approval or offer a fixed draft.

## Deterministic Audit

Prefer the installed package when available:

```bash
promptguard audit path/to/prompt-file --profile coding-agent --fail-on high --format markdown
promptguard audit-repo . --profile coding-agent --fail-on high --format sarif
```

Skill scripts delegate to the same CLI (package import or repo `pip install -e .`):

```bash
python3 skills/promptguard/scripts/audit_prompt.py path/to/prompt-file --profile coding-agent --fail-on high --format markdown
python3 skills/promptguard/scripts/audit_repo.py . --profile system --format markdown
```

Supported flags (shared with package CLI):

- `--profile general|coding-agent|system|security`
- `--fail-on critical|high|medium|low|info|none`
- `--rules PATH`
- `--format markdown|json|table|csv|sarif`
- `--accept-risk ID:reason` (repeatable)
- `--apply-accepted`
- `--save`

Installed skill script paths (first that exists):

```bash
# Hermes (active profile home; often ~/.hermes or ~/.serhatagent)
python3 "$HERMES_HOME/skills/promptguard/scripts/audit_prompt.py" …
python3 ~/.hermes/skills/promptguard/scripts/audit_prompt.py …
# Codex / Claude / OpenCode
python3 ~/.codex/skills/promptguard/scripts/audit_prompt.py …
python3 ~/.claude/skills/promptguard/scripts/audit_prompt.py …
python3 ~/.config/opencode/skills/promptguard/scripts/audit_prompt.py …
```

Prefer the installed `promptguard` package when importable (`pip install -e .` / pipx).

Do not stop after discovering prompt files. Discovery is not completion. If a prompt-like file exists and the script exists, running the script is mandatory.

## Severity

- `critical`: unsafe, illegal, or harmful behavior risk.
- `high`: privacy, routing, parsing, or tool-call breakage.
- `medium`: inconsistent UX or agent boundary drift.
- `low`: maintainability or clarity issue.

Prefer concrete contract fixes over generic prompt advice.

## Out of scope (this skill)

- Network LLM / remote model calls (stay offline and deterministic)
- Runtime chat firewalls / red-team attack generation
