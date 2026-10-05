---
name: style-review
type: workflow
description: "Reviews Markdown prose against the pinned agent-style v0.3.5 rules and optionally writes a polished copy beside the source. Use for specs, ADRs, PR bodies, release notes, and technical docs when prose quality or evidence discipline matters."
argument-hint: "[file.md | before.md after.md]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
effort: 3
context: main
agent: technical-writer
when_to_use: "Use as an opt-in REVIEW or SHIP gate for important prose artifacts. Do not use for every response, source code, casual chat, or non-English prose unless the user asks for style review."
---

# Style Review

Opt-in prose review for SDD artifacts using the portable `agent-style` v0.3.5
skill bundle. This skill is a second-pass review gate, not a global writing
mode. It does not edit `AGENTS.md`, `CLAUDE.md`, or any source document in
place.

## Source and Scope

- Rule pack: `.claude/skills/agent-style/references/RULES.md`
- Upstream note: `.claude/skills/agent-style/references/UPSTREAM.md`
- Attribution: `.claude/skills/agent-style/references/NOTICE.md`
- Detector reference: `.claude/skills/agent-style/references/rule-detectors.md`
- Revision prompt: `.claude/skills/agent-style/references/revision-prompt.md`

Use this skill for English technical prose where clarity, evidence, and review
readability matter:

- Specs and design docs
- ADRs and decision records
- PR titles and descriptions
- Release notes and changelog entries
- Runbooks, postmortems, and technical documentation

Do not use this skill for routine chat, code, generated logs, or prose where the
user's requested voice intentionally overrides formal technical style.

## Required CLI Check

Before any audit, check whether the CLI is available:

```bash
agent-style --version
```

If the command is missing, do not claim style review has run. Report this exact
fallback:

```text
style-review not run: `agent-style` CLI is not on PATH. Install with `pip install agent-style` or `npm install -g agent-style`, then rerun `/style-review <file>`.
```

Do not install dependencies unless the user explicitly asks.

## Single-File Workflow

Invocation:

```text
/style-review FILE.md
```

1. Read `FILE.md` and confirm it is prose that fits this skill's scope.
2. Run the deterministic audit:

   ```bash
   agent-style review --audit-only FILE.md
   ```

3. Add semantic judgment for rules the CLI marks as skipped because they need
   host-model context: RULE-01, RULE-03, RULE-04, RULE-08, RULE-11, RULE-F, and
   RULE-H. Use the bundled `agent-style` rules and detector reference as the
   source of truth.
4. Report a compact scorecard with per-rule counts and the first few examples.
5. Ask the user before writing any revised copy:

   ```text
   Produce a polished draft at FILE.reviewed.md?
   ```

6. On yes, compose the revision using the vendored revision prompt and write
   only `FILE.reviewed.md`. Never modify `FILE.md`.
7. Re-run the audit on `FILE.reviewed.md`.
8. Show before/after scorecard and a diff so the user can merge hunks manually.

## A/B Compare Workflow

Invocation:

```text
/style-review BEFORE.md AFTER.md
```

Run:

```bash
agent-style review --mechanical-only --compare BEFORE.md AFTER.md
```

Report the per-rule delta. Do not ask for polish and do not write files.

## Polish Invariants

The polished draft must obey these hard constraints:

- No new facts, metrics, citations, links, code behavior, or claims.
- Preserve Markdown structure unless the structure is the violation.
- Preserve meaning and approximate length budget.
- Resolve only flagged style issues.
- Write beside the source as `FILE.reviewed.md`.
- Never mutate or overwrite the source file.

If RULE-H flags unsupported claims, do not invent evidence. Keep the claim
flagged or ask the user for the missing source.

## SDD Integration

- In REVIEW, use this skill when a prose artifact is important enough that
  clarity or citation discipline affects review quality.
- In SHIP, use this skill before final PR bodies, release notes, or docs when
  the user asks for polish or when the agent claims prose quality.
- In verification-before-completion, a style-quality claim requires fresh audit
  evidence from this skill or a clear statement that style review was skipped.

## Self-Verification

When asked "is style-review active?", reply:

```text
style-review active: audit 21 rules from agent-style v0.3.5 (deterministic via CLI; semantic via host for RULE-01, 03, 04, 08, 11, F, H); workflow at .claude/skills/style-review/SKILL.md.
```
