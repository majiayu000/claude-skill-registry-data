---
name: agent-style
type: workflow
description: "Provides the vendored agent-style v0.3.5 prose rule pack as a portable Claude skill. Use when installing, syncing, applying, or auditing SDD Agent-Style support in another project, or when a style-review workflow needs the bundled rules."
argument-hint: "[install-check | audit FILE.md | compare BEFORE.md AFTER.md]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
effort: 2
context: main
agent: technical-writer
when_to_use: "Use when Agent-Style must travel with .claude/skills during SDD apply/sync, or when an agent needs the pinned rule pack without relying on a repository-level .agent-style directory."
---

# Agent Style

Portable SDD wrapper for the vendored `agent-style` v0.3.5 rule pack.

This skill exists so Agent-Style support moves with `.claude/skills/` when SDD
is applied to another project. It does not enable global writing style, does not
edit `AGENTS.md` or `CLAUDE.md`, and does not replace `style-review`.

## Bundled Source

- Rules: `references/RULES.md`
- Upstream pin: `references/UPSTREAM.md`
- Attribution: `references/NOTICE.md`
- Detector notes: `references/rule-detectors.md`
- Revision prompt: `references/revision-prompt.md`

Retain `references/NOTICE.md` when copying or redistributing this skill.

## Install Check

When asked whether Agent-Style is available in a target project, verify:

1. `.claude/skills/agent-style/SKILL.md` exists.
2. `.claude/skills/agent-style/references/RULES.md` exists.
3. `.claude/skills/style-review/SKILL.md` points to the bundled agent-style
   references, not a required repository-level `.agent-style/` directory.

If the target project still uses `.agent-style/` directly, migrate by copying
this entire skill folder and updating `style-review` source paths.

## CLI Check

For deterministic audits, check:

```bash
agent-style --version
```

If missing, report:

```text
agent-style deterministic audit unavailable: `agent-style` CLI is not on PATH. Bundled rules remain available for semantic review through `.claude/skills/agent-style/references/`.
```

Do not install dependencies unless the user asks.

## Audit Routing

For file review, use `style-review`. This skill supplies the portable rule pack;
`style-review` supplies the review workflow, audit command, polish invariants,
and completion evidence.

Use this skill directly only for:

- Checking whether Agent-Style travels with SDD apply/sync.
- Reading the pinned rules or upstream metadata.
- Migrating an older `.agent-style/`-based repo into `.claude/skills`.
