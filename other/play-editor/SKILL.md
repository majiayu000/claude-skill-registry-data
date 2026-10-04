---
name: play-editor
description: >
  Modify an existing compiled play — change its goal, a constraint, a failure condition,
  a success scenario, a step, the workflow shape, or the agents/skills it uses — by
  editing the play's ICE source and recompiling, never by hand-patching the output into
  disagreement with its intent. This is the companion to play-creator (which makes new
  plays). Use this whenever the user wants to edit, change, modify, update, tweak, extend,
  or fix an existing play — or says "edit the play", "change this play", "add a constraint
  to the play", "the play needs a new failure condition / step / scenario", "play-editor",
  or "recompile the play after I changed its intent" — even if they don't say "play"
  outright but are clearly reshaping a workflow recipe that already exists.
user-invocable: true
model: best
---

# play-editor

The play editor for garura. It changes an existing compiled play by editing the
play's **ICE source and recompiling** — not by patching the compiled `SKILL.md` in a way
that drifts from its intent.

Companion to `play-creator`: play-creator builds a new play from scratch; play-editor
changes one that already exists. (If you only want to *find* a play's gaps, that's
play-creator's read-only review mode — play-editor is how you then fix them.)

A built play is wired the harness-led way — **play** orchestrates, **subagents** gather
context and verify, **skills** do the work, **scripts** do the mechanical parts — and every
play → subagent → skill handoff is a **JSON contract** that carries file paths while the
real outputs live on disk (the model `play-creator` builds with). An edit must keep that
wiring intact: a dispatch you change keeps its JSON contract and its on-disk outputs, and a
new dispatch you add follows the same shape. Never quietly collapse a contract handoff into
inline prose.

## The core discipline: edit the source, recompile

A play is a *compiled artifact*. Its real source is its **ICE** — the Intent triple
(goal, constraints, failure conditions), the Context, and the generated Expectation
(success scenarios + recovery). So an edit is not a patch to the body; it is a change to
the ICE followed by a recompile.

This is the whole point of the skill. If you hand-edit the compiled play to say something
its intent does not, the play and its intent silently drift apart — and the next coverage
check, or the next person who reads it, hits the contradiction. The compiled play even
records a fingerprint of its intent + expectation precisely so that drift is detectable.
Keep them in lockstep: change the source, then recompile from it.

The one safe exception is a pure wording cleanup with **no** semantic change (fix a typo,
reword for clarity). That touches nothing in the ICE, so it can be edited directly.

## What you can edit, and what it touches

| The change | Where it really lives |
|------------|----------------------|
| The goal, or a constraint, or a failure condition | the **Intent** triple (and usually ripples into the Expectation) |
| A success scenario, or a recovery entry | the **Expectation** |
| The workflow shape, a phase, or a step | the workflow + task DAG |
| An agent or skill the play uses | the agent/skill set (+ re-audit any new agent) |
| Wording only, no meaning change | the compiled play directly — the safe exception |

## Pipeline

### 1 — Load the play and its ICE
Read the existing play (`SKILL.md`). If it has a separate ICE source (intent-triple +
expectation files), read that too — but often it won't: in this model the compiled play
is usually the single artifact, with its ICE *embedded*. When there is no separate source,
**reconstruct the ICE map from the compiled play itself** — pull constraints from the
pre-flight table and the eval strings, failure conditions and their recovery from the
Recovery section, and scenarios from the scenario evals. (Some constraints may only be
implied by an eval string rather than spelled out; treat the eval as the constraint's
definition.)

Either way, end with a map of what's there: constraints (C*), failure conditions (F*),
scenarios (S*), step and scenario evals (SE*/SCE*), the workflow, the agents/skills, and
which eval covers which constraint/failure/scenario. You cannot safely edit what you have
not read — most bad edits come from changing one thing and missing what depended on it.

### 2 — Classify the change and name its blast radius
Pin down exactly what is changing and the *smallest* set of things it reaches. Reword one
constraint and the blast radius is tiny. Add a failure condition and it ripples into a new
step eval and a new recovery entry. Change the goal and it can ripple through the whole
expectation. Name the blast radius before touching anything — then re-derive only what the
change reaches and preserve everything it doesn't. A play that gets needlessly reshaped on
a small edit is a failed edit.

### 3 — Apply the change to the ICE first
Make the change in the source:
- A changed/added/removed constraint or failure condition, or a changed goal → update the
  **Intent** triple.
- If that shifts what success or recovery looks like → regenerate the affected
  **Expectation** pieces (success scenarios from the changed intent, exactly one recovery
  per failure condition). Regenerate — don't hand-author — so they still trace back to the
  intent. Leave untouched scenarios as they are; re-confirm only what actually changed.

### 4 — Propagate only what the change reached
- **Pre-flight:** add or drop a check only if a constraint's environmental precondition
  changed.
- **Workflow:** change the structure, a phase, or a step only if the edit warrants it —
  don't reshape a play that didn't need reshaping.
- **Evals:** regenerate step evals for changed constraints/failures and scenario evals for
  changed scenarios; **remove** any eval whose constraint/failure/scenario no longer exists.
- **Agents/skills:** if the change adds or drops a capability, re-identify the needed
  skills/agents and audit any *new* agent against
  [`references/agent-audit.md`](references/agent-audit.md) (P1–P11). Apply the short-circuit
  rule — don't add an agent for something the play can compute inline.
- **Scripts:** if the edit adds a mechanical, deterministic step (or turns an existing step
  mechanical), route that work to a script — extend one already in the play's `scripts/` or
  add a new one — and have the step *call* it; don't inline the logic as prose the play
  re-reasons each run. If the edit removes a step that owned a script, delete the now-orphan
  script. Leave the play's other scripts untouched. (Same harness-led discipline play-creator
  builds with.)

### 5 — Recompile
Re-emit the `SKILL.md` with every required section intact — match
[`references/compiled-play-example.md`](references/compiled-play-example.md). Update the
intent + expectation fingerprint in the metadata so the play and its source stay in
lockstep — recompute it mechanically with `shasum -a 256` over the (edited) intent +
expectation; don't hand-write a hash. (For workflow questions, see
[`references/workflow-structures.md`](references/workflow-structures.md).)

### 6 — Re-verify with the linter (coverage + no orphans)
Don't re-count by hand — run the bundled script on the recompiled play:

```
python3 scripts/lint_play.py <path-to-the-play>
```

It does both halves mechanically: full coverage (every constraint/failure/scenario
covered, exactly one recovery per failure, all required sections present, a real
fingerprint) **and** the no-orphans check (nothing referencing a constraint/failure/
scenario you removed). This is exactly where edits go wrong — you delete something and
leave a dangling reference, or add something and forget its eval — and it's exactly what
the script catches for free. Fix every GAP and re-run until clean; the fix is yours.

The one thing the linter can't judge is whether each eval is *meaningful* and
**executable from what earlier steps capture**. Check that yourself: if an eval inspects
data no earlier step recorded, fix the earlier step, not the eval.

### 7 — Show what changed
Present a short summary the reader can scan: which ICE elements changed, which
evals/recovery/sections were added, removed, or regenerated, and a confirmation that
coverage and the no-orphans check pass. The blast radius should be visible at a glance.

## Hard rules

- Edit the ICE and recompile — never hand-patch the compiled play into disagreement with
  its intent. Pure wording cleanups with no semantic change are the only safe direct edit.
- Keep the blast radius minimal — re-derive only what the change reaches; preserve the rest.
- Regenerate scenarios and evals from the changed source — don't hand-author them, so they
  keep tracing back.
- No orphans — remove every eval and recovery tied to something you deleted, and cover
  everything you added. A script whose step was removed is an orphan too — delete it.
- Keep the play harness-led — new mechanical work goes into a script the step calls, not
  into prose; preserve the play's existing scripts.
- Preserve the wiring — play orchestrates, subagents gather context and verify, skills do
  the work; every dispatch stays a JSON contract over files on disk. An edit never collapses
  a contract handoff into inline data.
- Re-run the linter (`scripts/lint_play.py`), clear every gap, and update the fingerprint
  (`shasum -a 256`) before declaring the edit done.
- Keep the cardinal rule wired. If the play recommends, suggests, advises, or ranks, it
  must keep citing `standards/rules/no-unbacked-recommendation.md` and keep all four
  pieces — the constraint, the failure condition, the step eval, and the strip-not-replace
  recovery. An edit must never introduce a default, generic pointer, or substitute play
  name where the play cannot back an answer; the linter's `no-unbacked-recommendation`
  check enforces it.
- Keep the **Next** command wired. The play must have an entry in
  `standards/rules/pipeline-next.md` (or be `meta_exempt` there), and the recompiled
  Standard Play Close must render its Next line from that map — the linter's
  `next-command (pipeline-next)` check enforces it. If an edit changes what a play hands
  off to, update its entry in the successor map too.
