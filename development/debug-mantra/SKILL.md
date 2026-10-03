---
name: debug-mantra
description: "Four-mantra debugging discipline — reproduce, trace the fail path, falsify the hypothesis, cross-reference every breadcrumb. Recite the mantra block verbatim at the start of any debugging session, then apply the four steps in order before proposing any fix. Trigger on /debug-mantra and proactively whenever debugging starts — user reports a bug, says something is broken/throwing/failing, asks to debug/diagnose/investigate an issue, pastes a stack trace or error log, or asks an attribution question ('where is this coming from?', 'what posts/triggers/generates this?', 'why is X appearing?') where the answer is an unknown source to find, not just a crash to fix. Also trigger on /debug-mantra plan, and proactively when writing or reviewing the acceptance criteria of a plan, capture doc, or marathon plan — apply the same four mantras through the pivots in 'When the target is a plan, not a bug'. Adapted from: https://github.com/thananon/9arm-skills"
---

# Debug Mantra

Four-step discipline for any debug session. Recite verbatim, then apply in order. When the target is a plan rather than a bug, the same four steps apply read through the pivots in [When the target is a plan, not a bug](#when-the-target-is-a-plan-not-a-bug).

## Recite this — verbatim, as the first thing in your first response

> **Mantra:**
> 1. **First is reproducibility.** Can the issue — or the artifact — be reproduced or observed reliably?
> 2. **Know the fail path.** Debugger first; then source trace + knob enumeration; then in-code instrumentation.
> 3. **Question your hypothesis.** What would disprove it?
> 4. **Every run is a breadcrumb.** Cross-reference all of them.

Then begin work.

---

## 1. Reproduce reliably

Establish ground truth before anything else — a runnable repro for a failure, a direct look at the real artifact for an attribution question.

**Reproduce = observe the primitive ground truth, not your impression of it.** For a crash that's a failing test; for an *attribution* question ("what posts this?", "where does X come from?") it's inspecting the actual artifact — the real message, record, or raw bytes — **before** theorising about its origin. A screenshot, a rendered view, or a remembered detail is an **observation to verify, not an axiom to build on**: name it as assumption-zero and check it first. The cheapest disproof is usually looking straight at the thing — one query against the real object beats a sweep of the code that *might* have produced it. Beware visual grouping and other rendering artifacts: what looks like "one consolidated thing" may be many separate ones (or vice versa) — confirm against the raw object before any hypothesis inherits the shape.

- **Reliable repro** → capture the exact steps, inputs, and environment as a runnable artifact: failing test, curl script, CLI invocation, replay harness.
- **Flaky repro** → the bug is not yet debuggable. Raise the rate first: loop the trigger, parallelise, add stress, narrow timing windows, inject sleeps. 50% flake is debuggable; 1% is not.
- **No repro at all** → stop. Say so explicitly. Ask the user for env access, captured artifacts (HAR, log dump, core), or permission to instrument. Do **not** proceed to hypothesise.

Target: a fast (1–5 s), deterministic pass/fail signal. Pin time, seed the RNG, freeze network, isolate filesystem.

## 2. Know the fail path

Once reproducible, find *where* the code breaks and *what stops it from breaking*. The differential narrows the search. Try in this order — escalate only when the prior tactic fails.

1. **Attach a debugger.** If the env supports it, attach and step to the failure site. One breakpoint beats ten logs. Do this **before** turning any knobs.
2. **Source trace + knob enumeration.** If no debugger (or it can't reach the bug), trace the code path end-to-end and list every knob that can influence the outcome:
   - config flags, env vars, feature toggles
   - branch conditions, input shape
   - timing, concurrency, build options
   Each knob is a candidate axis to flip in the differential. Flip one at a time.
3. **In-code instrumentation.** If outside knobs can't move the failure, go inside: `printf` / log statements at the suspected fail site, dump the relevant internal state. Tag every probe with a unique prefix (e.g. `[DBG-a4f2]`) so cleanup is a single grep. Let the trace show where reality diverges from your model.

## 3. Falsify the hypothesis

When a candidate root cause surfaces, scrutinise it **before** testing it.

- Does it actually explain the symptom end-to-end? Walk it through.
- What is the simplest **proof**? What is the cleanest **disproof**?
- Run the **disproof first**. If the hypothesis survives, it's real. If it dies, you saved yourself from chasing a phantom.
- Generate 3–5 ranked hypotheses, not one. Single-hypothesis thinking anchors on the first plausible idea.

**Root cause or proximate cause?** A hypothesis that survives disproof explains *this* failure; it does not yet prove you are standing at the origin. Before accepting it, run the class-vs-instance test: *if I fix here, does the whole class of failure go away, or only this instance?* If only the instance, keep asking **"what let that happen?"** — one hop upstream at a time — until the answer is a design decision, a contract violation, or the place the bad state was first *produced*, not the line where it was first *noticed*. Record each hop; the chain is evidence, not narrative.

- **The symptom-fix trap** (named anti-pattern): guarding, try/catching, null-defaulting, retrying, or widening a type at the crash site when the bad state was produced upstream. The crash site is where the invariant was *checked*; the bug is where it was *broken*. A fix that makes the checker tolerant hides the next occurrence instead of preventing it — and without the root-vs-proximate gate above, a green repro makes the session *look* fixed. The tell: the fix adds a defensive branch and cannot say what upstream change would make that branch dead code.
- A fix at the proximate site is sometimes right (the origin is external, out of contract, or a separate issue) — but that is a *decision* to record with its reason, never a default.

## 4. Every run is a breadcrumb

Maintain a running **ledger** of every experiment in this session. Each entry: what changed, what happened, what it ruled in or out.

- When a new hypothesis surfaces, walk the ledger. Does it hold for **every** prior observation, not just the most recent?
- If any past run contradicts it, the hypothesis is wrong or incomplete — refine or discard.
- When in doubt, design the **single experiment** whose outcome makes it certain. Run that next, instead of churning on adjacent runs.
- Update the ledger after every run. It is your memory across the session.
- **Close the ledger with one RC statement** before proposing the fix: `Root cause: <origin> ; Fix site: <where> ; Why not upstream/downstream: <reason>`. If the fix site is not the origin, the third field must justify it. If you cannot fill the first field, you are not done with mantra 3.

---

## When the target is a plan, not a bug

Invoked as `/debug-mantra plan`, or proactively when writing or reviewing the acceptance criteria of a plan, capture doc, or marathon plan. The four mantras apply unchanged and the recital stands verbatim — "the issue — or the artifact" includes the plan's own evidence. Each step is read through its pivot:

| Step | Debug reading | Plan pivot |
|---|---|---|
| 1. Reproduce | Runnable repro of the failure. | **Measured ground truth at plan time.** Every count, `file:line`, and live-state claim in the plan is re-run now, not remembered — a "measured, not assumed" evidence table (claim · command run · observed value) is the shape. A recalled repo state is hypothesis-zero. |
| 2. Fail path | Trace the code that breaks. | **Trace the real path the plan changes**, before proposing: walk it and enumerate every caller and surface it touches. A criterion about a path nobody traced is a guess wearing a checkbox. |
| 3. Falsify | Disprove the root-cause hypothesis. | **Falsify the acceptance criteria.** Each criterion must name how it fails — a criterion that cannot fail is decorative, and one an empty input satisfies passes vacuously. Specify the red control *and where its evidence will land* (`test/baselines/` negative-control pattern). Rank 3–5 alternatives for the load-bearing design choice and name the strongest counterargument (an explicit "Open question for the reviewers" block is the pattern). **Root vs proximate, at plan time:** name the origin the plan fixes and state whether the change removes the failure class or one instance; a plan whose fix site is downstream of the origin must say why (the RC statement from mantra 4 is the shape). |
| 4. Breadcrumbs | Session experiment ledger. | **Recon ledger.** Record the greps, counts, and probes that grounded the plan, citable from the plan or its capture doc. Before finalizing, walk the ledger against what is already shipped — a plan resting on a stale claim (feature already exists, path already changed) inherits the stale claim. |

**The plan-only rule, and why pivot 3 is the strictest:** at plan time falsification is *specified*, not *performed* — strictly weaker evidence than a red control you have watched fire. That gap is why each criterion must name a destination for its red evidence: a planned red control that is not witnessed when implemented is a promise, not a control. Plan reviews have caught criteria "satisfiable by an empty pre-created file" and "satisfiable by a print statement while the defect persisted" — both passed review as written.

Scale rigor as ever: a one-line fix's plan needs a confirming observation, not the full table; a marathon or large-refactor plan needs every pivot. For large refactors this is the SOP "Arc planning" discipline applied debug-mantra-first.

## Operating rules

- Recite the mantra block **once** per debug session, in your first response. Do not re-recite mid-session.
- Recite **verbatim**. Never paraphrase or abridge the recital.
- If the user says "skip the mantra" → skip the recital but still apply the four steps silently.
- Apply the four steps **in order**:
  - Do not propose a fix before #1 is satisfied (reliable repro exists).
  - Do not start testing hypotheses before #2 has narrowed the fail path.
  - Do not commit to a hypothesis before #3 has tried to disprove it.
  - Do not declare a hypothesis correct until #4 confirms it against every prior breadcrumb.
  - Do not propose a fix until the RC statement names the origin, the fix site, and — if they differ — why.
- **Scale rigor to the bug.** The gate is on *evidence*, not ceremony: a trivially obvious defect — a typo, a stack trace pointing straight at the line — needs a confirming **observation**, not necessarily a runnable harness or a written ledger. The burden stays on a direct look, never on assumption.
- If you catch yourself proposing a fix without a reliable repro, stop and return to step 1.
- If you catch yourself building on an unverified observation ("it's obviously X", "that's clearly one Y") — especially one drawn from a screenshot, a rendered view, or memory — stop and inspect the raw artifact first. The impression is hypothesis-zero, not ground truth, and a single direct look at the real object usually settles it faster than any search of the code that might explain it.
- The mantra is a constraint **you** carry through the session — not advice to deliver back to the user.
