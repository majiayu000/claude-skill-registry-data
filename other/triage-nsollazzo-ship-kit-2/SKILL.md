---
name: triage
description: |
  Diagnose a bug, test failure, or unexpected behavior BEFORE any fix — fan parallel
  sub-agents across different angles (reproduce, recent changes, backward root-cause trace,
  pattern/blast-radius), adversarially verify the leading hypothesis, then propose the best
  fix with evidence. Read-only: it produces a diagnosis, it never edits code. Use when asked
  to "triage", "debug", "investigate this bug", "why is this failing", "what's the root
  cause", "this is broken", "track this down", or "tests are failing". To actually apply the
  fix, hand off to the `fix` skill (branch + implement + ship).
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
argument-hint: "<issue description or reference>"
---

# Triage — symptom in, verified root cause + proposed fix out

Turn a reported problem into a **diagnosis you can trust**: a disciplined path from symptom
to a root cause backed by evidence, plus the fix it points to. This skill only *investigates
and proposes* — it changes no code. The applier is the `fix` skill.

## The Iron Law

**No proposed fix without a root cause first.** You may not recommend a fix until you can
point at the evidence — a `file:line`, a command's output, a diff — that explains *why* the
bug happens. "It's probably X" is not a root cause; it's a guess.

## Sub-agents — fan the investigation out, then verify

Where your agent can spawn sub-agents — Claude Code `Agent`/Task, Codex `worker` / custom
agents, Grok parallel sub-agents, Hermes `delegate_task`, OpenClaw `sessions_spawn` — use
them; investigation parallelizes cleanly. If your agent can't, run the same angles
sequentially yourself: the result is identical, just slower.

1. **Fan out investigators**, one sub-agent per angle, scaled to the issue — a one-line
   typo needs none (just look), a cross-component failure warrants the full set. Give each
   the symptom, the files/commands to start from, and instructions to report findings as
   `{evidence (file:line / output), what it shows}` — reading the real code, not guessing:
   - **reproduce** — read the *whole* error/stack trace, then get it to fail on demand in a
     clean state; write down the exact steps. Not reproducible ⇒ not yet understood.
   - **recent changes** — `git log`, `git diff`, `git blame` on the failing path; recent
     deploys, new deps, config changes. Most bugs are a recent delta.
   - **root-cause trace** — walk the bad value *backward* up the call chain to where it
     first appears, not where the error surfaces. See `root-cause-tracing.md`.
   - **pattern / blast-radius** — find similar code that works, list *every* difference
     however small, and map what else depends on the broken path (config, env, ordering,
     shared state) — who else this bug touches.
   - In a multi-component system, add a **boundary-instrumentation** angle: log what enters
     and leaves each boundary (API → worker → DB, ingest → process → serve), run once, let
     the evidence show which component breaks before diving in.
2. **Collect + reconcile.** Merge what the angles found; where they disagree, surface it and
   pick the better-supported one (don't average them).
3. **Verify adversarially.** Form **one** hypothesis ("X is the root cause because Y"), then
   spawn an independent sub-agent whose job is to **refute** it: open the cited evidence, run
   the smallest check, and default to "not the cause" unless the evidence holds. Survives ⇒
   you have your root cause. Refuted ⇒ form a *new* hypothesis, don't pile a guess on a guess.

## Workflow

1. **Scope the issue** from the argument: an error message, a failing test, a PR/issue
   reference, or a described misbehavior. Pull the full context (the whole trace, the failing
   command) before fanning out.
2. **Investigate** — run the fan-out + adversarial verification above (or each angle as a
   sequential pass with no sub-agents).
3. **Propose the fix at the source.** Once the root cause is verified, recommend the fix that
   corrects the *origin*, not the symptom — plus, where they apply: a failing-test-first
   reproduction, and (judiciously, not everywhere) hardening the layers the bad data passed
   through so the bug becomes structurally impossible (see `defense-in-depth.md`).
4. **Report the diagnosis** (below). Stop there — proposing is the whole job of this skill.

## When 3 candidate fixes look like they'd fail — question the architecture

If every fix you can think of just moves the problem elsewhere or needs "massive
refactoring," **stop and say so.** That pattern means the design is wrong, not that you need
a cleverer patch. Surface it to the requester as a design question rather than recommending
fix #4.

## Verify before you call anything confirmed

A claim ("X is the root cause", "this reproduces") counts only with evidence you gathered
*this run*: the command you ran, its output, the `file:line` you read. Never "should be,"
"looks like," or "probably." A reproduction counts only once you've actually seen it fail.

## Red flags — STOP and go back to investigating

If you catch yourself thinking any of these, you're guessing, not triaging:

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "It's probably X" — without having traced the data flow
- "I don't fully get it but this might work"
- Proposing a fix before the bad value is traced to its origin

## Reporting the diagnosis

Give the requester, in plain language and in this order:

- **Symptom** — what's observably wrong.
- **Root cause** — the origin, *with the evidence* (`file:line`, command output, diff) that
  proves it.
- **Recommended fix** — the source-level fix, and any alternatives worth weighing (one-line
  tradeoff each), led by your recommendation.
- **Next step** — typically "hand to `fix` to implement + ship", or, if you couldn't reach a
  root cause, exactly what's still unknown and what evidence would resolve it (never bluff a
  cause you don't have).
