---
name: super-ship
description: The bulletproof ship for structural work. Run the full drift audit, fix the broken and stale findings, then ship the combined result live via the ship flow. Use when asked to super ship, audit and ship, or ship bulletproof, or when shipping a structural change where the docs and skills may have gone stale. For a small change, plain ship is enough.
icon: rocket_launch
displayDescription: "Chains the drift audit into the ship flow for structural work. Runs the full audit first, fixes the broken and stale findings it surfaces, then ships the combined result: full verify, merge into main, push, CI watched to green, and the live site proven rendering. Gap findings and new-validator recommendations are reported as follow-ups, never built mid-ship."
invoke: ["super ship","super ship it","audit and ship","bulletproof ship"]
---

# super-ship

Drift audit, fix, ship — one invocation. A higher-order skill: it composes `drift-audit` and `ship` and owns only the rules of the composition. Everything about *how* to audit lives in `.claude/skills/drift-audit/SKILL.md`; everything about *how* to ship lives in `.claude/skills/ship/SKILL.md`. Read both and follow them; this file only says how they connect.

## When invoked

Use this skill when asked to "super ship", "audit and ship", or ship "bulletproof" — typically after structural or architectural work (a moved directory, a new build step, a renamed surface, a changed dependency model) where the repo's self-descriptions may have gone stale and a plain ship would deploy them stale.

**Not for small changes.** A colour tweak, a copy fix, a single-component change: that's plain `ship`. The audit sweeps every skill and doc, and running it for a one-line change is ceremony, not safety. If invoked on something clearly small, say so and offer plain `ship` instead.

**Invoking this skill is the ask to ship.** `ship`'s guardrail says never to chain into it automatically from other work, and `drift-audit`'s says the report is the deliverable and fixes wait for approval. This skill is the sanctioned exception to both: by invoking it, Rob has pre-approved fixing the drift the audit finds *and* deploying the result. The carve-outs below say where that pre-approval stops.

## Instructions

### 1. Audit

Run the full `drift-audit` flow per its SKILL.md — every section, not a lightened pass. The one behavioural change: at its final step, do not stop to ask whether to apply fixes. The full report still gets produced; it becomes part of the final report here.

If the audit finds `validate-registry` itself broken, stop the whole flow and report — its own rule, and nothing downstream is trustworthy until it's fixed.

### 2. Fix

Apply the **Broken** and **Stale** findings in-session. All of `drift-audit`'s guardrails still hold while fixing: never edit a generated file to resolve a finding, never weaken a validator.

Two categories of finding are **reported, not acted on**:

- **Gaps** (missing skill coverage, a recommended new validator): these are new work, not drift repair. Building a validator mid-ship is scope creep; list them as follow-ups.
- **Judgement calls**: a finding that might be deliberate scope, or whose fix could reasonably go two ways, or that touches a decision recorded elsewhere (e.g. a settled decision with an authoritative comment). Stop and ask rather than resolving it silently to keep the pipeline moving. A super ship that pauses on a real question is working as designed.

### 3. Re-check

Re-run the audit's mechanical checks over whatever the fixes touched (at minimum `npm run validate-registry`), so a fix can't itself introduce a dangling reference. There's no need to repeat the full prose read.

### 4. Ship

Follow the `ship` flow per its SKILL.md, from its step 0, with everything that entails — tree survey, full verify, logical commits, merge if on a branch, push, CI watched to green, and the live render proven with the deployed-site smoke. Two composition rules on top:

- **Commit the drift fixes separately** from the session's own work — they are a different concern, and ship's one-commit-per-concern rule already implies it. Something like `docs: repair drift found by pre-ship audit` with the findings named in the body.
- **Ship the combined result or nothing.** Never push the session work while leaving audit fixes uncommitted, or the reverse — the whole point is that what deploys and what describes it move together. If verify goes red on an audit fix, that fix is in scope to repair, same as session work.

### 5. Report

One combined final message:

- The audit summary in `drift-audit`'s report format (broken / stale / gaps / verified counts), with what was executed versus only read
- Which findings were fixed and shipped, and which are left as follow-ups (gaps, judgement calls)
- Everything `ship`'s report requires: commits pushed, verify and CI results, files left out, what visibly changes on the live site

## Guardrails

- This file never restates a step from `drift-audit` or `ship` — a change to either flows through automatically. If a conflict appears between this file and one of them, theirs wins for their own steps; this file wins only on the composition rules above.
- The pre-approval covers fixing drift and deploying; it does not cover resolving judgement calls, building new validators, or resolving merge conflicts — those stop and ask, per the rules above and ship's own guardrails.
- If the audit comes back completely clean and there is nothing to ship, say so and stop — a clean audit is a valid outcome, not a failure to find something.
