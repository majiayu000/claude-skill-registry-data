---
name: implement-from-plan
description: >-
  Load this skill when building from a planning document: implement a SKELETON.md or ITER_NN.md,
  including variants like SKELETON_v2.md or v2_ITER_03.md. Reads the plan frontmatter for artifact
  type and scope, then implements each in-scope section in order. Trigger on "implement from plan",
  "build from the plan", "implement the skeleton", "build ITER_02". Not for writing the plan (use
  plan-fullstack-app), auditing built code against a plan (use review-against-plan), or a small
  non-feature change to a built version (use apply-small-fix-to-version).
argument-hint: "[plan-file]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Implement From Plan

Translate a SKELETON.md or ITER_NN.md into working code, section by section, without inventing
scope beyond what is written. Done means every in-scope section is implemented and the completion
summary is reported.

Read `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md` for the full schema before starting. The
section table, pointer rules, and resolution order there are authoritative.

## Procedure

### 1. Locate and parse the plan docs

1. Find the target plan files and the target family by "Locating plan files" in
   `${CLAUDE_PLUGIN_ROOT}/references/plan-schema.md`.
2. Within the target version, the iteration whose frontmatter has `mvp: true` is the sequence
   terminator: the plan runs SKELETON → ITER_01 → … → that terminator.
3. Read the YAML frontmatter to determine:
   - `artifact`: is this SKELETON or ITER?
   - For ITER: `sections_changed` (implement these), `sections_unchanged` (resolve via pointer),
     `depends_on` (the prior artifacts whose content this iteration relies on, its dependency
     chain).
   - For SKELETON: `sections` (implement all listed sections).
4. By default the target is the whole sequence up to and including the `mvp: true` iteration:
   implement the SKELETON, then each ITER_NN in `depends_on` order. Never sweep past the mvp
   terminator in a default full-sequence run. If the user named a single iteration, target only
   that one and use its `depends_on` chain to resolve unchanged sections for context.
5. Exclude **patch ITERs** (frontmatter `patch: true`) from the default run. They sit past the
   terminator and are produced by the `apply-small-fix-to-version` skill. Implement one only when it is
   the named target, on its own.

### 2. Resolve pointers before starting

For any section in `sections_unchanged`, find its authoritative spec now, before writing any code,
by following the resolution order in `plan-schema.md`. Load that content into context so
implementation is not interrupted to look it up.

### 3. Implement section by section

Work through sections in numerical order. For each section:

1. State which section you are starting and what it covers (one line).
2. Read the section spec. Implement exactly what is specified, no more, no less.
3. When you finish a section, confirm it is done before moving to the next.

Section-specific notes:

- **§01 Concept**: no code output. Load the concept as context. Confirm your understanding in one
  sentence so the user can catch misreads early.
- **§02 Architecture**: create the project scaffold (directories, empty modules), stub data model
  classes/types, and stub route handlers. Do not fill in logic yet unless the spec includes it.
- **§03 Tech Stack**: install and configure the specified stack. Pin versions only if the spec
  specifies them.
- **§04 Backend**: read `${CLAUDE_PLUGIN_ROOT}/references/implementation-gotchas.md` before
  implementing any backend code and avoid the applicable traps. If the project has its own
  `implementation-gotchas.md`, read it as well. Implement the endpoints and services described for
  this section only.
- **§05 Frontend**: same as §04, read the shared `implementation-gotchas.md` first. Implement only
  the screens and components listed in this section's spec.
- **§06 LLM/Prompts**: only present if the app has LLM integration. Implement the model wiring,
  system prompt, and input/output handling as specified.

## Rules

- Do not implement sections outside `sections_changed` (ITER) or `sections` (SKELETON).
- Do not add features, routes, components, or dependencies not in the spec.
- If the spec is ambiguous, state your assumption and use the simplest interpretation. Never guess
  silently.

## Output

After all sections are done, report:

- Sections implemented and key artifacts created
- Assumptions made
- Sections skipped and why (e.g. §06 absent because no LLM integration)
- Items the user should verify manually (e.g. env vars needing real values)

## Stop conditions

- A section spec is missing or incomplete → ask instead of inventing it. With no human to answer,
  skip that section and list it under sections skipped, since invented spec is worse than a gap.
- More than one plan family exists and the user named none → take the highest version, per
  "Locating plan files", and say which.
