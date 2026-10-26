---
name: encode-lesson
description: Turn a correction, recurring mistake, or review finding into permanent repo machinery — a doc line, path rule, lint rule, test, hook, or persona check — so it never has to be said again. Use whenever the user corrects the same thing twice, a persona repeats a finding across PRs, a retro assigns a lesson, or anyone says "make sure this never happens again" / "remember this". This is the flywheel that makes the whole harness improve (Constitution Art. VI).
argument-hint: [the lesson / mistake to encode]
allowed-tools: Read Write Edit Grep Glob AskUserQuestion Bash(npm run lint*) Bash(npm test*) Bash(npm run docs:lint*) Bash(npm run typecheck*)
---

## Task

Durably encode: **$ARGUMENTS**

1. **Understand the failure, not the symptom.** What was the mistake, why did it happen, and at what moment would an intervention have prevented it? Restate it in one sentence and confirm with the user if ambiguous.

2. **Choose the strongest enforcement that fits** — prefer mechanisms that _cannot be ignored_ over prose (this escalation ladder is the whole game):

| Strength             | Mechanism                                                                                             | Use when                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1. Blocking          | ESLint rule / `boundaries/*` / tsconfig (`eslint.config.js`)                                          | Expressible statically — the gold standard                        |
| 2. Blocking          | Test or repo check (Jest/RNTL, `scripts/*.mjs`, a Maestro flow)                                       | Verifiable by running something                                   |
| 3. Blocking          | docs-lint rule (`scripts/docs-lint.mjs`) or Claude hook (`scripts/hooks/*` + `.claude/settings.json`) | Doc integrity / agent tool behavior (protected paths, formatting) |
| 4. Reviewed          | Persona doc (`docs/personas/*.md`)                                                                    | Judgment call a reviewer should weigh every PR                    |
| 5. Loaded in context | Convention doc (`docs/conventions/*.md`) + AGENTS.md pointer                                          | Guidance needed while editing matching files                      |
| 6. Grounding         | AGENTS.md / feature doc / ADR                                                                         | Global operating knowledge or a decision record                   |

Often correct: one blocking mechanism + one doc line explaining _why_ (gates without rationale get fought; rationale without gates gets ignored).

3. **Implement it.** Keep the change minimal; run the gate to prove it now fails the bad pattern (and passes the good one). For lint/CI/gate changes, Constitution Art. IV applies: dedicated commit, clearly described, owner-aware.

4. **Record:** one line in the most relevant doc (dated, in the convention file or `docs/quality/quality-score.md`). If the lesson reveals a wrong settled decision → supersede the ADR instead of editing it.

5. **Report** what was encoded, at which strength, and what would have to happen for this mistake to ever recur. If the honest answer is "someone repeats it anyway", you chose too weak a mechanism — go up the ladder.
