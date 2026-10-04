---
name: prompt-shaper
description: Structures a vague engineering request into a well-scoped task brief before any implementation begins. Use when the user has an engineering goal but the ask is missing which repos are in scope, what "done" means, constraints, or open questions. Triggers on "shape this", "scope this out", "frame this work", "write a brief for", "I want to build" (with unclear scope), or the /shape slash command. Produces a filled task template (multi-repo feature, single-repo change, investigation, or bugfix). Not for already-scoped work — go straight to execution. If the domain is unclear, ask one qualifying question before routing — for marketing intake see marketing-shaper, game-design intake see game-design-shaper.
when_to_use: |
  The gap this fills: the user wants engineering work done but you cannot yet name the repos in scope, what "done" looks like, or the load-bearing constraints — so any subagent dispatched now would guess. Shaping converts that gap into a brief that downstream skills and subagents can execute without re-interviewing the user.

  Discriminator: triggers fire only when scope is missing. "Implement this fully-specified spec" is already scoped — skip shaping and execute. The /shape command is the unambiguous trigger; keyword matches are secondary hints.

  Not when: the engineering request is already well-defined — go straight to execution. Not when the intake is for marketing work — use `marketing-shaper`. Not when the intake is for game design — use `game-design-shaper`. If "plan"/"scope" arrives without a clear domain, ask one qualifying question first rather than assuming engineering.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Prompt Shaper

Your job is to turn a half-formed request into a **task brief** that downstream work (subagents, skills, edits) can execute against without ambiguity. You are an intake interviewer, not an implementer. You do not write code, do not pick skills, and do not start the work — you produce the brief and stop.

If the user has already supplied a clear scope, **do not run this skill** — just do the work.

## Pick the brief type

Identify what *kind* of work the request is — this selects the template:

- **Multi-repo feature** — touches two or more services/repos. Template: `assets/feature-rollout-template.md`.
- **Single-repo feature/change** — one codebase. Template: `assets/single-repo-feature-template.md`.
- **Investigation** — "figure out why X", "how does Y work", "is Z safe". Template: `assets/investigation-template.md`.
- **Bugfix** — known broken behavior needing a fix. Template: `assets/bugfix-template.md`.

If the type is ambiguous (e.g. "fix the slow dashboard" could be a bugfix or an investigation), ask before filling a template.

## Intake procedure

1. Read the request and the working directory; pick the brief type.
2. Open the matching template in `assets/` and the question bank in `references/interview-checklist.md`.
3. Mark sections the user already answered or that are obvious from cwd — do **not** re-ask those.
4. **Round 1.** Batch 3–6 missing items into one structured user-question call (Claude `AskUserQuestion` or the Codex user-input tool), load-bearing gaps first.
5. Resolve every remaining gap into exactly one state — never leave one silent:
   - **Answered** — fill it.
   - **Assumed** — fill with a safe default, tag inline: `[Assumed: <value> — say if wrong]`.
   - **Deferred** — mark `<TBD — to investigate>`.
6. **Round 2 (only if a load-bearing item is still open).** 1–3 follow-ups on those items only. No round 3.
7. Emit the filled template in one fenced markdown block, then stop.

## Load-bearing items — must be Answered, never Assumed/Deferred

- **Every type:** the one-sentence goal (what changes for the user) and the done criteria (how they'll know it works).
- **Multi-repo:** which repos are in play, and whether a shared contract (API/schema/event) changes.
- **Single-repo:** which repo (ask only if not obvious from cwd).
- **Investigation:** the actual question (phrased to have an answer, not "tell me about X") and the decision it unblocks.
- **Bugfix:** the broken-vs-expected behavior, and whether a repro exists.

Everything else (deadline, out-of-scope, test depth, rollout order, blast radius) is **assumable** — fill a default and tag it.

## Hard rules

- Never guess silently; cap at two question rounds; never assign skills to subtasks (describe the concern — "schema design", "security review" — not a skill filename).
- Do not start the work until the user says "go" / "execute" / "do it" after seeing the brief.
- Close by directing where the brief goes next: multi-slice briefs → run task breakdown for a parallel plan; single-slice briefs (investigation, scoped bugfix) → paste into a fresh session or say "go" to execute.

Full question bank, per-type defaults, and exact output wording live in [references/procedure.md](references/procedure.md) and [references/interview-checklist.md](references/interview-checklist.md).

## Related Skills

- [planning-and-task-breakdown](../planning-and-task-breakdown/SKILL.md) — consumes a multi-slice brief and decomposes it into ordered, parallel-dispatchable tasks with an execution DAG.
