---
name: sdlc-loop
description: Invoked explicitly by /sdlc. Reads workflow state and reports where every feature stands, which single command comes next, and what is blocking. Also runs --blast to show the regeneration scope of a spec change, --doctor to self-check the framework, and handles /fix-bug as a mid-chain entry point. This is the router for the development loop.
argument-hint: "[FEAT-ID] [--blast <FEAT-ID>] [--doctor] [--fix-bug <BUG-ID> \"<symptom>\"]"
disable-model-invocation: true
---

# /sdlc — the loop router

This skill **routes; it does not generate.** It reads state and findings, then names the
one command to run next. Never generate documents or code from here — hand off.

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

> Read-only by default: skip gate Step 4 (CHECKPOINT). `--fix-bug` writes state, so it
> checkpoints.

---

## Mode A — status (default, no arguments)

1. Run `state-loader.md`. It already emits the `[STATE]` block; do not duplicate it.
2. Add a per-feature table when more than one feature is tracked:

```
FEATURES
  FEAT-ID   Title                    Phase        Loop  Blocking  Next
  PTK-001   Policy summarizer        code          2      1       /sdlc  (blocked)
  PTK-002   Event replay endpoint    srs           0      0       /techdoc PTK-002
```

3. Determine the next command with this precedence:

   1. **Blocked input** — the next phase's input check returns `NOT_READY` or
      `NO_SOURCE`. The next step is a **person**, not a command: name the file, the
      sections, and the owning role. Run `/check {phase}` for the detail. This outranks
      everything else, because no generation command can move a feature whose input
      cannot support the next phase.
   2. **Edited artifacts** (a recorded `input_hash` no longer matches the file) → the
      earliest phase whose input changed. Say which artifact moved, and that its
      downstream gates now need re-earning. An edit is expected, not an error.
   3. **Open blocker/major findings** → look up each `route_to`, take the **earliest**
      phase among them, and suggest that. Name the finding ids.
   4. **Gate verdict `revise`/`block`** on the current phase → re-run the current phase
      after the listed fixes.
   5. Otherwise → `framework.yaml → next_command[<last command>]`.

4. Never suggest two commands. The value of this skill is that it answers "what now"
   with exactly one answer.

## Mode B — `--blast <FEAT-ID>`

Print the regeneration scope of a spec change **before** any tokens are spent
regenerating. This is the highest-value output in the framework.

1. Recompute the `spec_hash` of every scenario in the feature's `.feature` files.
2. Diff against `.agent/state/trace.tsv`. List the changed SC-IDs.
3. For each changed scenario, read its row and report `impl_refs`, `test_refs` and
   `prompt_ref`.
4. List the artifacts whose recorded `input_hash` no longer matches, and therefore which
   gates flip to `stale`.
5. State the regeneration scope as **exactly those files, scoped to the affected UCs** —
   not the whole feature.

```
BLAST RADIUS — {FEAT-ID}
  Changed scenarios : {FEAT-ID}-UC1-SC3
  Impacted code     : {impl_refs from the trace row}
  Impacted tests    : {test_refs from the trace row}
  Impacted prompt   : {prompt_ref, when the scenario is model-driven}
  Gates -> stale    : G3 G4 G5a G5b G6
  Regenerate        : UC1 only. UC2 is untouched.
  Amendment         : add a row to {{paths.srs_dir}}/{FEAT-ID}/SRS.md §10 Change log
```

A loop-back writes an **amendment, not a rewrite**. Say so in the report.

## Mode C — `--doctor`

Self-check the framework. No hooks exist to catch drift, so this is the manual
equivalent — run it before trusting the framework after edits.

**The check definitions are data**, in `.agent/framework.yaml` → `doctor`. Read the
patterns from there rather than spelling them out here: a skill that wrote the forbidden
strings into its own prose would trip its own check. `doctor.exempt_paths` lists the two
files that legitimately discuss the rules.

| Check | How | Severity |
|---|---|---|
| Stack literals in skills | grep `.claude/skills/` and `.claude/agents/` for `doctor.forbidden_literals_regex` (case-insensitive) | blocker |
| Project paths in skills | grep the same trees for `doctor.forbidden_paths_regex` | blocker |
| Copy-pasted step files | grep skills for any heading in `doctor.inlined_step_headings` | blocker |
| Missing shared preamble | every `sdlc-*` SKILL.md contains `doctor.required_skill_marker` | blocker |
| Auto-invocation leak | no description contains a `doctor.forbidden_description_words` entry; each starts with `doctor.required_description_prefix` | major |
| Profile schema | every id in `stack_profiles` has a `stack-profile.yaml` with all `_schema.yaml` required keys | blocker |
| Path reality | every `paths.*` value exists on disk | major |
| Gate coverage | every gate named in `framework.yaml → gates` has its file | blocker |
| Command/skill pairing | every `.claude/commands/*.md` names a skill that exists | major |
| Placeholders | no `{{` remains in `.agent/project-context.yaml` | blocker |
| CLAUDE.md markers | both `SDLC:PROJECT-FACTS` markers present and the block is not inside an HTML comment | blocker |
| Cache freshness | `context-cache.md` version and hash match | minor |

Report as a table with pass/fail and the offending file:line. Do not auto-fix — list the
fixes and let the user choose, the same contract the review phase honours.

## Mode D — `--fix-bug <BUG-ID> "<symptom>"`

The mid-chain entry point. A bug does **not** re-run PRD or SRS.

1. Create `.agent/state/features/<BUG-ID>.yaml` with `kind: bugfix`,
   `entry_phase: testcases`, `phase: testcases`, `related_ucs: [...]`, and gates
   `G1 G2 G3` recorded as `n/a (bugfix)`.
2. **Diagnose before fixing.** Classify the symptom against
   `framework.yaml → loop_routes` and say which one it is. Do not skip this — a fix
   applied to the wrong layer is how a spec bug becomes permanent.
3. **Write the failing test first.** Hand off to `/unittest <BUG-ID>` to produce a
   regression test tagged `@trace.verifies=<BUG-ID>`, or, for an LLM-output bug, an eval
   case in `cases.jsonl` with `origin: regression` and `trace: <BUG-ID>`. It must fail
   before anything is fixed. A "fix" with no failing test first is unverifiable.
4. Then `/gen-code` → G4 → G5 → G6 only.
5. Add a `trace.tsv` row with `scenario_id = <BUG-ID>` so the regression test is tracked
   permanently rather than orphaned.
6. **Promotion.** If diagnosis shows the spec was wrong rather than the code, write
   `promote_to: srs` into the bug's state, and route to `/srs` for an amendment plus a
   new SC-ID. The item then re-enters the normal chain scoped to that one UC.

The same shape serves `kind: prompt-change`: enter at `techdocs` for the version-bump
decision, then `/gen-code` for the new registry file, then G5b eval only.

---

## Diagnosis — mandatory before any finding is written

Every failure must be classified into one `loop_routes` key from `framework.yaml`
before a finding row is written. The `route_to` is what the router acts on, so an
unclassified finding is a finding the loop cannot use.

**Bias rule: when a test fails, the default is that the code is wrong, not the test.**
Routing to `tests` or `srs` requires stating why the test or scenario is wrong, and
leaves a change-log entry. Without that rule an agent quietly edits assertions until
everything is green, and the suite stops meaning anything.

## Termination

A feature reaches `done` when every gate G0–G6 is `pass` **and** zero `blocker`/`major`
findings remain open. Then: set `phase: done`, move its state file to
`.agent/state/archive/`, remove it from `current.yaml → features`, and suggest the PR.

**Anti-thrash guardrail.** `loop_iteration` increments on every loop-back. At
`framework.yaml → max_loop_iterations_without_progress` iterations **with no gate
advancing**, stop. Write an entry to the feature's `open_questions` with
`blocks: <phase>`, report it, and issue no further generation commands until a human
answers. An agent left to iterate on a mis-specified requirement burns the budget and
produces a mess — this guardrail is not negotiable and must not be waived from inside
the loop.

## Writing findings

Append to `.agent/state/findings.tsv`, one row per issue:

```
id	feat_id	opened	severity	category	found_in	route_to	ref	title	status	closed
```

`id` = `RF-<FEAT-ID>-<nnn>`, sequential per feature. `severity` and `category` use the
review report's vocabulary. `route_to` comes from the diagnosis above. Only `blocker`
and `major` affect routing.
