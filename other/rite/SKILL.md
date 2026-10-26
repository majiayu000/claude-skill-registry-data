---
name: rite
description: User-invoked DevRites menu and router; no args renders the menu, a verb invokes the matching `rite-<verb>` skill.
argument-hint: "[verb [args...]]"
user-invocable: true
disable-model-invocation: true
---
<!-- loads: {"always":["devrites-lib/reference/standards/core.md"],"triggers":{"intent":["devrites-lib/reference/intent-map.md"],"menu":["rite/reference/menu.md"],"dispatch":["devrites-lib/reference/parallel-dispatch.md"],"reply":["devrites-lib/reference/reply-contract.md"]},"rootOnly":["devrites-lib/reference/parallel-dispatch.md"]} -->
> Read-set manifest: `devrites-engine context --skills-root .agents/skills <slug> --skill rite` (no workspace: `--out <path>`) bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.

# $rite: DevRites menu + router

Two modes:

- **No args** → render the menu and stop. Do not execute a phase or infer
  workspace status; `$rite-status` owns that.
- **Verb arg** → pass-through invocation of the matching `rite-<verb>` skill (`$rite spec foo` ≡ `$rite-spec foo`); the called skill owns the output.

When the user asks which rite fits, load [`devrites-lib/reference/intent-map.md`](../devrites-lib/reference/intent-map.md).
When they ask how phases connect, load [`reference/menu.md`](reference/menu.md).

## Dispatch

If `$ARGUMENTS` starts with a verb in this table, **load the matching skill and execute its workflow** with the remainder of `$ARGUMENTS` as that skill's argument. Resolve the installed skill path:

```bash
V=<verb>; ARGS="<remaining args>"
F=.agents/skills/rite-$V/SKILL.md
# Then Read "$F" and follow its workflow with $ARGS as that skill's $ARGUMENTS.
```

`use` and `guide` are handled inline per the sections below, not via a skill file.

What each verb does lives once, in the Menu below; this table is the invocation map only.

| Verb | Skill |
|---|---|
| `spec [feature]` | `$rite-spec` |
| `adopt [area]` | `$rite-adopt` |
| `clarify [feature]` | `$rite-clarify` |
| `temper [--mode]` | `$rite-temper` |
| `define` | `$rite-define` |
| `vet [--cross-model]` | `$rite-vet` |
| `plan [mode]` | `$rite-plan` |
| `build [slice]` | `$rite-build` |
| `converge [slug]` | `$rite-converge` |
| `prove` | `$rite-prove` |
| `polish [mode]` | `$rite-polish` |
| `review [scope]` | `$rite-review` |
| `seal` | `$rite-seal` |
| `ship` | `$rite-ship` |
| `status [slug]` | `$rite-status` |
| `doctor` | `$rite-doctor` |
| `upgrade [slug]` | `$rite-upgrade` |
| `learn ["<lesson>"]` | `$rite-learn` |
| `explain [concept \| diff \| idea \| recap]` | `$rite-explain` |
| `pov [candidate]` | `$rite-pov` |
| `dogfood [--port N]` | `$rite-dogfood` |
| `harness [app] [--maintain]` | `$rite-harness` |
| `pr-feedback [PR\|thread]` | `$rite-pr-feedback` |
| `watch-pr [PR\|URL]` | `$rite-watch-pr` |
| `customize [instruction \| skill \| agent \| plugin]` | `$rite-customize` |
| `use <slug>` | (inline) |
| `guide` | (inline) |
| `resolve <qid> "<answer>"` | `$rite-resolve` |
| `prototype [question]` | `$rite-prototype` |
| `handoff [focus]` | `$rite-handoff` |
| `zoom-out` | `$rite-zoom-out` |
| `pressure-test` | `$rite-pressure-test` |
| `autocomplete [idea] [--ship]` | `$rite-autocomplete` |
| `quick [change]` | `$rite-quick` |
| `fast <task \| slug>` | `$rite-fast` |
| `frame [task]` | `$rite-frame` |

Both forms call the same skill. The menu supports discovery; `/rite-<verb>` is the direct form.

`use <slug>` is handled **inline**. There is no `rite-use` skill. Confirm
`<slug>` is a safe slug and `.devrites/work/<slug>/state.md` is a contained regular file, then re-point `.devrites/ACTIVE` to `<slug>` and report
the now-active feature. It is cheap context-switching only: no re-spec, no phase run. If
the workspace or its `state.md` is missing, list the slugs under `.devrites/work/` that have
`state.md` and stop.

`guide` is an inline walkthrough for the first feature. Agree on one **real, small**
change, then run spec → clarify → temper → define → vet → build → prove → polish → review → seal →
ship. Before each phase, say what it decides; after, name what it wrote and why. Pause at
every boundary and explain only what the user needs for the next decision.

Specialist triggers (model-invoked inside the above):
`devrites-frontend-craft` (UI) · `devrites-browser-proof` (UI verify) ·
`devrites-source-driven` (uncertain library) · `devrites-doubt` (non-trivial
decision) · `devrites-api-interface` (cross-boundary) ·
`devrites-audit <security|perf|simplify>` (single-axis review/polish pass) ·
`devrites-debug-recovery` (failures). Parallel reviewer fan-out at seal is a shared
reference (see [`devrites-lib/reference/parallel-dispatch.md`](../devrites-lib/reference/parallel-dispatch.md)).

## What to output

Reply-contract exception: `$rite` is the menu/router, not a workspace completion step.
Called phase skills own the shared completion reply contract
([`reply-contract.md`](../devrites-lib/reference/reply-contract.md)).

1. **Verb in `$ARGUMENTS`** → invoke the matching skill per the table above.
2. **No args** → menu mode, as above.
3. **Unrecognized first token** → tell the user the known verbs and stop. Don't guess.
4. **No active feature** and the user asked "where am I" → point at `$rite spec <feature>` (or `$rite-spec`). Don't summarize state yourself: `$rite status` (or `$rite-status`) owns that.

## Menu

```
DevRites — disciplined senior-engineer workflow
                              menu form           direct shortcut
SPEC          $rite spec               ≡    $rite-spec        investigate deeply → write spec.md
ADOPT         $rite adopt              ≡    $rite-adopt       onboard existing code → reverse-derive spec.md
CLARIFY       $rite clarify            ≡    $rite-clarify     close the complete decision surface before planning
TEMPER        $rite temper             ≡    $rite-temper      optional — strategic review: scope mode + pre-mortem, harden the spec
PLAN          $rite define             ≡    $rite-define      turn the spec into plan + task slices + state
VET           $rite vet                ≡    $rite-vet         mandatory every plan — light/full engineering review by stakes
REPLAN        $rite plan               ≡    $rite-plan        decompose / reslice / repair an active plan
BUILD         $rite build              ≡    $rite-build       one slice/wright; HITL stops, `.devrites/AFK` may chain
CONVERGE      $rite converge           ≡    $rite-converge    recovery — append work needed to meet intent
PROVE         $rite prove              ≡    $rite-prove       tests + build + runtime + browser evidence
POLISH        $rite polish             ≡    $rite-polish      code polish always; UI normalize + polish if UI
REVIEW        $rite review             ≡    $rite-review      feature-scoped multi-axis review
SEAL          $rite seal               ≡    $rite-seal        final GO / NO-GO decision (no git)
SHIP          $rite ship               ≡    $rite-ship        pre-GO read-only; fresh GO → commit; optional approved push/tag/PR → archive
STATUS        $rite status             ≡    $rite-status      active feature, next action, evidence, risks
DOCTOR        $rite doctor             ≡    $rite-doctor      installation and native host diagnostics
UPGRADE       $rite upgrade ...        ≡    $rite-upgrade     audit an older workspace; route only proven gaps
LEARN         $rite learn ...          ≡    $rite-learn       review captured lessons → promote to project rules / principles
EXPLAIN       $rite explain ...        ≡    $rite-explain     grounded concept/diff/idea/recap explainer
POV           $rite pov ...            ≡    $rite-pov         decide adopt / trial / hold / reject for an external option
DOGFOOD       $rite dogfood ...        ≡    $rite-dogfood     browser QA by changed user journey
HARNESS       $rite harness ...        ≡    $rite-harness     generate/maintain a project verify-<app> skill
PR FEEDBACK   $rite pr-feedback ...    ≡    $rite-pr-feedback fix and resolve PR review threads
WATCH PR      $rite watch-pr ...       ≡    $rite-watch-pr    observe PR/CI once without mutation
CUSTOMIZE     $rite customize ...      ≡    $rite-customize   author overrides/extensions without forking the pack
SWITCH        $rite use <slug>                                re-point .devrites/ACTIVE to another feature (inline)
GUIDE         $rite guide                                     first feature, guided — full lifecycle on one small real change (inline)
RESUME        $rite resolve ...        ≡    $rite-resolve     answer a HITL checkpoint
AUTO          $rite autocomplete ...   ≡    $rite-autocomplete  unattended lifecycle; `--ship` stops at Ship preflight
QUICK         $rite quick <change>     ≡    $rite-quick       express lane — one small reversible change (escalates if it grows)
FAST          $rite fast <task>        ≡    $rite-fast        short lane — spec + plan + questions, ≤10 slices, one check, review, prove
UTILITY       $rite frame | prototype | handoff | zoom-out | pressure-test  (or direct shortcuts)
```

> **Small one-off change?** A typo, copy tweak, config bump, or one-function fix → **`$rite-quick`**
> (express lane: one contract → build → prove → ship, no full workspace). It escalates to
> `$rite-spec` when the change is no longer small, reversible, and unambiguous. Use the
> full lifecycle above for features. Mid-size work that does not need a gate after every
> slice → **`$rite-fast`** (one spec-and-plan step, up to ten slices, one completeness check).

## Core operating rules (every DevRites skill enforces)

The operating rules live in `.agents/skills/devrites-lib/reference/standards/core.md`; DevRites skills Read it as
their first step, and the other rule files load on demand. See
[`.agents/skills/devrites-lib/reference/standards/README.md`](../devrites-lib/reference/standards/README.md) for the full index.
