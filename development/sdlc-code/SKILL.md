---
name: sdlc-code
description: Invoked explicitly by /gen-code. Implements a use case from its technical design, following the layer order in the active stack profile and tagging entry points with @trace.implements. Fans out one code-implementer agent per use case for multi-use-case features.
argument-hint: "<UC-ID | FEAT-ID>"
disable-model-invocation: true
---

# /gen-code — implementation

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

**Phase inputs** — phase `code`, gate `G4`, inputs
`{{paths.tech_docs_dir}}/{FEAT-ID}/TD-{FEAT-ID}.md` + the in-scope `.feature` files,
output: source under `{{layout.source_root}}`. This command modifies existing source, so
gate Step 4 (CHECKPOINT) always applies.

---

## Step 1 — Input check

Gate Step 2.7 has already run `.agent/steps/input-check.md` against
`input_contracts.code`. Act on its verdict:

- `NO_SOURCE` — no technical design. Report how to create one and **stop**.
- `NOT_READY` — usually a component map with no file paths, missing interface specs, or
  a schema change with no migration plan. Report and **stop**. Implementing from an
  under-specified design means the implementer makes the design decisions silently, and
  nobody reviews them.
- `PARTIAL` / `READY` — proceed.

If the design was **edited after its gate passed**, the gate reads `stale`. That is not a
block — a Tech Lead correcting the design is the system working. The input check has
already re-read the document as it stands now; implement against that, and note in the
report that G3 needs re-earning.

Load the architecture snippets named by the merged profile's `architecture_snippets`.
**This is the only phase that reads them** — they run to hundreds of lines and carry the
copy-paste patterns for this stack with correct trace tag placement already shown.

## Step 2 — Confirm the plan

From the techdoc's component map, list exactly which files will be created and which
modified, and which scenarios each realises. Present at CHECKPOINT.

If a component in the map conflicts with what is actually in the codebase — a module
that already does this, a different layering than the design assumed — stop and report
it. Do not reconcile silently; the design is the approved artifact and diverging from it
without a record breaks the trace.

## Step 3 — Implement

More than 3 UCs → `.agent/steps/spawn-agent.md`, one `code-implementer` per UC.
Otherwise implement directly, following the same rules.

Build in the profile's `layers` order. Do not skip a layer by folding its work into the
next one — the layering rules in `architecture.key_rules` are what the reviewer checks.

Read the modules you touch and their imports first. Match the surrounding idiom, naming
and comment density; code that reads as foreign is a maintenance cost even when correct.

**Tag as you go**, using the profile's `trace_tags` and `traceability`:

- `@trace.source=...` once per file at module level
- `@trace.implements={UC-ID}-SC{n}` on each entry point realising a scenario
- Only files matching `traceability.entrypoint_globs` need `implements`; do not scatter
  tags through internal helpers, where they add noise and rot

## Step 4 — AI implementation (when `ai_class != none`)

- Add a **new** `{registry}/{name}/{version}.yaml` at the version the techdoc decided.
  **Never edit a published version file** — the registry caches for the process lifetime
  and the published version is what the recorded eval score describes. Editing it makes
  the score a lie about code that no longer exists.
- Fill `metadata.eval_set` and `metadata.trace`; leave `eval_score` and `eval_run` null
  for `/eval` to write.
- Wire the call site through the LLM protocol so it can be mocked at unit level.
- Put input guardrails **before** the provider call.
- Parse and validate model output; never pass raw model text into the rest of the system.

## Step 5 — Run the checks

Run `format_check`, `lint`, `typecheck` and the install/build command from
`quality_commands`. Fix what they report. **At most three retry rounds** — past that,
stop and report, because the third failure is almost always a design problem rather than
a syntax one.

Never disable a rule, add an ignore comment, or loosen a type to get green. Report it
instead.

## Step 6 — Evaluate G4 and record

Run `.agent/gates/G4-code.yaml`: lint, format, typecheck, build, trace rules T1/T4/T5,
no `TODO`/`FIXME`/debug output in new code, components exist where the map says, and —
for AI — no in-place edit of a published prompt version.

Update state: `phase: code`, `scope.entrypoints`, the verdict and `input_hash`. The
`input_hash` is the **techdoc's** hash, so that a later design change automatically marks
this gate stale.

---

## Boundaries

- **Do not write tests.** `/gen-testcase` and `/unittest` own them, in a separate context
  window on purpose: tests written beside the implementation get shaped to its bugs.
- Do not implement behaviour that has no scenario. If you find a gap, report it as a
  finding routed to `srs` and implement the rest.
- Do not add a dependency. Report the need; it is an ADR-level decision.
- Do not refactor unrelated code. A tidy-up that rides along in a feature diff hides the
  feature from review.
- Do not write state files from a subagent.
