---
name: cross-checking-research
description: Cross-check a consumer repo against a research hub both ways — pull hub concepts/sources to cite or adopt, push the repo's reusable findings back as ready-to-PR drafts. Use after an ADR/plan milestone.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Glob, Grep, Bash, Workflow
  argument-hint: "<consumer-repo-path> [research-hub-path] [focus]"
  stability: experimental
---

# Research Cross-Check

**Target**: $ARGUMENTS

Bidirectional cross-check between a **consumer** repo (a project with ADRs, plans, findings) and a
**research hub** (a catalog of concepts, tools, and per-repo learnings):

- **Pull** — hub concepts/tools/sources the consumer has not yet cited or applied, each mapped to
  the consumer file (ADR or plan) that should cite or adopt it.
- **Push** — the consumer's reusable findings the hub does not yet capture, with the top ones
  drafted in the hub's per-repo-learnings format, ready to PR.

## Arguments

| Position | Name | Required | Default | Description |
| --- | --- | --- | --- | --- |
| 1 | `consumer-repo-path` | yes | — | Absolute path to the consumer repo. |
| 2 | `research-hub-path` | yes* | — | Absolute path to the hub. *Ask the user if not given; do not guess. |
| 3 | `focus` | no | — | Narrows the cross-check to a topic (e.g. `evaluation`, `governance`). |

## When NOT to use

- The consumer has no decisions/findings yet (nothing to push, nothing to map pulls onto).
- You only need a literature search — use a research skill instead.

## Workflow

1. **Resolve paths.** Confirm both directories exist and are readable. The hub should contain an
   index/README and a per-repo learnings dir (e.g. `docs/learnings/per-repo/`); if its layout
   differs, tell the user rather than guessing receptacles.
2. **Run the bundled workflow** (the instruction to call Workflow is the opt-in):

   ```text
   Workflow({
     scriptPath: "${CLAUDE_PLUGIN_ROOT}/workflows/research-cross-check.js",
     args: { consumer: "<abs path>", research: "<abs path>", focus: "<optional>" }
   })
   ```

   `args` reaches the script as a JSON string; it is parsed there. Phases: **Scan** (read both
   repos in parallel) → **Diff** (pull + push candidates) → **Draft** (top 4 push items).
   All agents are **read-only**; nothing is written to either repo.
3. **Fallback** when the Workflow tool is unavailable: do the same three phases inline — read the
   consumer's `docs/decisions/`, `docs/plans/`, AGENTS/README/CHANGELOG; read the hub's index and
   the landscape docs matching the consumer's domain; list pulls and pushes; draft the top items.

## Output

- **Pull table**: hub concept · hub doc · why · target consumer file · action (`cite` /
  `adopt-via-new-ADR` / `evaluate`) · priority.
- **Push table**: finding · target hub file · rationale · provenance · priority.
- **Drafts**: for each, target path, title, full markdown, and a one-paragraph PR note. Present
  them to the user — writing files or opening PRs in either repo is a separate, explicit step.

## Quality check

- Every pull cites a real hub doc path; every push cites consumer evidence (file path).
- Drafts contain no facts absent from the consumer scan ("do not invent" is in the draft prompt).
- Nothing already cited in the consumer appears as a pull.
