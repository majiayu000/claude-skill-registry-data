---
name: conform
em-version: 1.22.0
description: >-
  Use when checking a ratified event model (and its slice docs) for drift against the codebase
  that implements it — advisory only, never a gate, never an unprompted edit — or when walking
  `em validate` diagnostics on a model to explain and fix rule violations. Drives `em`'s conform
  and validate phases.
---
<!-- GENERATED FILE from .claude/skills/event-modeling-conform/SKILL.md by scripts/build-plugin.ts — do not hand-edit; run npm run docs:generate -->

# Event Modeling — conform & validate

## Phase: `conform` — drift check against the codebase

Goal: check a **ratified** model (and its slice docs) against the codebase that implements it,
and report where they've drifted — advisory only, never a gate, never an unprompted edit.

Preconditions (tool check, model location) are the same as every other phase — see
`${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md`.

**Read `reference/conform.md` before doing any conform work** — it carries the full flow
(scope, evidence-first verification, `em diff --json`, classification, report) and the
stance guardrails (evidence-first, uncertainty is never drift, propose-don't-edit). It reuses
the `em:discover` skill's `extract` sourcing/mode rules
(`${CLAUDE_PLUGIN_ROOT}/skills/discover/reference/extract.md`) for reading the target codebase rather than
duplicating them.

In short: run `em conform-scope <model-name>.em --repo <target-repo-path> --seed-asis` to
compute the in-scope slice set (diff-scoped by default, via `Last conformance:` + the target
repo's changed paths mapped through each slice doc's `implementedIn:`) and seed the scratch
model in one step; for each in-scope slice, check for a `conformance/bindings/<key>.yaml` first
(GH #450) — verify it with `em conform bindings check` and scope the walk through it when it
exists, backfill it from this walk's own evidence when it doesn't — then gather code evidence
*before* comparing to the model or doc; write the as-is picture into that scratch model
(`<model-name>-asis.em`, reusing the canonical model's names wherever the code matches them);
run `em diff <model-name>.em
<model-name>-asis.em --json` and let `em` decide the structural deltas; classify every finding
(real drift / model gap / internal inconsistency / uncertainty) with cited evidence; write
`conformance/<date>-report.md` **and its structured twin `conformance/<date>-findings.json`**
(one entry per finding, `em conform-findings check <path>` to verify) with proposed `issue
"conformance: …"` red notes; apply only the proposals the user ratifies, then re-render and
validate; run `em state set-conformance <revision> --report <path>` to update the state file's
`Last conformance:` marker.

Ruling on a finding is a human gate, like ratifying a slice
(docs/process.md#the-slice-lifecycle-gates): the sweep gathers evidence and proposes, a person
decides, and `em conform-supersede ... --locus <model|doc|code|none> --by <name>` records the
ruling on the findings record (and stamps the report) — never rule on your own judgment. Once
every finding touching a slice is ruled, `em slice conform <model-name>.em <key> --at <rev>`
certifies that version of the slice (`--at build:<id>` / `deploy:<id>` when the swept commit
will not stay reachable — a PR branch under squash/rebase merges; GH #261).

End of phase: state file's `Last conformance:` marker updated (via `em state set-conformance` —
refuses while any `implemented` slice still has an unruled finding; `--partial` escapes with a
loud notice), Decisions log entry if any proposals were applied. Conform doesn't chain to
another phase — it's a recurring loop, run again whenever the codebase has moved.

A full (non-`--partial`) `em state set-conformance` also **certifies the model's current design
version** (MIL-218, `docs/process.md#model-versions`) — it refuses if no design version has ever
been bumped ("bump a model version first") or if the model changed during this run without a
re-bump; run `em model version bump <model-name>.em --by <name>` before the final `em state
set-conformance` call if either applies.

## Phase: `validate`

Run `em validate <model-name>.em` and walk through each diagnostic with the user, explaining the
rule (see `${CLAUDE_PLUGIN_ROOT}/shared/reference/em-dsl.md`) and proposing the fix. Apply fixes on
agreement. Common ones:

| Diagnostic | Fix |
|---|---|
| reaction triggers no command | Add the command it issues, in this same slice, or an explicit `arrow` to one elsewhere |
| **command has nothing that triggers it** | Add the `ui` it's issued from — or, if the system issues it, the reaction that triggers it, also in this slice. Ask *"who does this, and where are they when they do it?"* |
| **read model has no consumer** | Add the screen that displays it, or the reaction that watches it. If it's a repeat added only to shorten an arrow and nothing looks at it there, drop the instance |
| read model has no source | Add the missing `from "Event"` |
| command produces no event | Give the command its event, or drop the command |
| **event is not read by any read model** | Add the read slice that projects it — but ask *who looks at this and what do they do with it* first. "Nobody" is a real answer, and then the question is why it's recorded at all |
| **illegal `arrow` kind pair** | Don't reroute it — the model is missing an element. `command → view` needs the event between them; `view → command` needs a reaction. Between two instances of one read model, just delete the arrow: the repeat needs no connection |
| `view X again` with no earlier declaration | Declare the view plainly the first time it appears |
| event feeding an earlier view instance | Add a `view X again` where the event lands and move the source there |

For anything genuinely unresolved rather than a rule violation, prefer `issue "text"` on the
relevant element over a `# TBD` comment — it shows up as a red marker on the rendered diagram and
`em validate` tracks it as an open-issue warning, so it isn't lost once rendered. `em validate
--list-issues` gives a quick sweep of everything still open.

`em validate` now catches a reaction wired straight to an event too — any reaction with no
`command` in its own slice, and no explicit arrow to one, warns "triggers no command". A
`translation`/`processor`/`automation` should always trigger a `command` in its own slice
(`reaction → command → event`); if one instead records an event directly, route it through a
command instead.

Validate isn't pinned to this phase alone — every other phase runs it continuously as part of
the shared operating principles (`${CLAUDE_PLUGIN_ROOT}/shared/reference/operating-principles.md`).
This phase is for a dedicated, focused walkthrough of whatever diagnostics remain, and for the
full rule catalog in `${CLAUDE_PLUGIN_ROOT}/shared/reference/em-dsl.md`.
