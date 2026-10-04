---
name: feature-slicing
description: Slice a goal into the smallest feature slices that can each be PROVEN — every slice ships with a named eval and an end-to-end test, and a slice you can't evaluate or test doesn't get selected. Use after the goal is set and before the spec, so only provable features make the build.
---

# /feature-slicing

Usage: `/feature-slicing <the goal, or what "done" looks like>`

A feature you can't evaluate is a guess. A feature you can't test end-to-end is a hope. This skill turns a goal into a short list of **vertical slices** — each a thin, shippable piece of the goal — and **keeps only the slices that come with a way to prove them.** It runs after the goal is pinned (`/write-a-goal`, or a one-line acceptance) and before `/spec`, so the spec describes provable features, not a wishlist.

## The rule

> If you can't name the eval and the end-to-end test for a slice, it doesn't get built yet.

That's the whole discipline. A slice with no eval is either too vague (sharpen it) or not actually part of the goal (drop it). The selection gate is **provability**, not enthusiasm.

## The method

1. **Cut vertically, not by layer.** A slice is a thin end-to-end thing a user can actually do — not "the database layer." Aim for the smallest slice that moves the goal's metric.
2. **For each candidate slice, write three things up front:**
   - **Eval** — the measurable check that says this slice meets its bar. Tie it to the goal's metric where you can (reuse the numbers from `/write-a-goal`). Deterministic where possible; an LLM-judge rubric only when the output is genuinely subjective. This is the eval the build is written against, and it joins the project's eval harness.
   - **End-to-end test** — the real user journey that proves it works in the running app, start to finish (not a unit test of one function). For UI, a browser path; for an API, a request→response contract.
   - **Tracking** — how we'll see real users use it: for a new screen/tab/mode, a virtual `page_view` path; for a new interaction, an event name + low-cardinality params; or an explicit *"not worth tracking — \<why\>"*. Deciding is mandatory, tracking isn't — but a slice whose usage question ("did anyone touch this?") has no answer planned is instrumentation debt the founder pays later (see `/user-analytics` Recipe F). "Events fire" joins the slice's e2e check.
3. **Apply the selection gate.** Keep a slice only if **both** the eval and the e2e test are defined and runnable. If either is missing: sharpen the slice until they exist, or defer it (write down why) — don't smuggle an unprovable feature into the spec.
4. **Order by risk-and-value.** Sequence the kept slices riskiest/highest-value first, so the goal's metric moves early and a dead end is found cheap.
5. **Hand off.** Output the selected slices, each with its eval + e2e test, as the input to `/spec` → `/plan`. In the per-task loop, the eval and e2e test are written **first** (TDD) and are the slice's acceptance gate.

## Output shape

```
Goal: <the measurable outcome>

Selected (build these):
1. <slice> — Eval: <measurable check> · E2E: <user journey> · Track: <event(s)+params | page_view path | "none — why"> · Why first: <risk/value>
2. ...

Deferred (can't prove yet):
- <slice> — missing: <eval | e2e> — <reshape-or-revisit note>
```

## Why this exists

Eval-driven development (see `factory/playbooks/ai-native-2026/eval-driven-development.md`) says the eval comes before the code. Slicing is where that happens at the *feature* level: the gate that keeps the build honest. You only commit to features you can prove, and "done" for each is a green eval and a passing end-to-end test — not an opinion. It's the feature-level twin of [`write-a-goal`](../write-a-goal/SKILL.md), which does the same for the objective as a whole.
