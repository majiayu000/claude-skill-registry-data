---
name: speckit-constitution
description: Enforce a mandatory Parse, Don't Validate constitution section
argument-hint: "Principles or values for the project constitution"
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: preset:parse-dont-validate
user-invocable: true
disable-model-invocation: false
---

# Speckit Constitution Skill

## User Input

```text
$ARGUMENTS
```

You MUST consider the user input before proceeding.

## Wrapper Layer

This preset wraps `/speckit-constitution` (and any inner wrapper the core-flow
seam expands to). It adds exactly one thing: it enforces a canonical
**Parse, Don't Validate** section in `.specify/memory/constitution.md`
after the core flow has written it. It does not otherwise change the workflow.

Other presets may stack the same way and inject their own governance sections.
Never assume this preset owns the whole document.

### Core Flow


## User Input

```text
$ARGUMENTS
```

You MUST consider the user input before proceeding.

## Wrapper Layer

This preset wraps `/speckit-constitution` (and any inner wrapper the core-flow
seam expands to). It adds exactly one thing: it enforces a canonical
**Functional Programming Paradigms** section in `.specify/memory/constitution.md`
after the core flow has written it. It does not otherwise change the workflow.

Other presets may stack the same way and inject their own governance sections.
Never assume this preset owns the whole document.

### Core Flow


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Scope Guard

This command's own work is limited to updating the project constitution itself. Dependent templates
and commands read the constitution at runtime and are not modified here.

- Classify every part of the user input as either constitution content or a separate,
  non-governance intent.
- If the input includes feature implementation, code generation, refactoring, building, or
  deployment requests, you **MUST NOT** execute them. Extract them as deferred intents instead.
- You **MUST NOT** create, modify, or delete application source files, feature routes,
  components, tests, deployment files, or other artifacts unrelated to the constitution
  workflow.
- If it is unclear whether an instruction is constitution content, ask for clarification before
  making changes.
- After completing the constitution update, include a `Next Actions` section for each deferred
  intent. List the original intent and suggest the appropriate follow-up Spec Kit command, such
  as `/speckit-specify`, without invoking it.
- If there are no non-governance intents, omit the `Next Actions` section.

## Pre-Execution Checks

**Check for extension hooks (before constitution update)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_constitution` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Outline.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values and (b) fill the template precisely.

**Note**: If `.specify/memory/constitution.md` does not exist yet, it should have been initialized from `.specify/templates/constitution-template.md` during project setup. If it's missing, copy the template first.

Follow this execution flow:

1. Load the existing constitution at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Follow-up TODOs if any placeholders intentionally deferred.

5. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

6. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

7. Output a final summary to the user with:
   - New version and bump rationale.
   - Any TODO placeholders or deferred items requiring manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).
   - A `Next Actions` section for any deferred non-governance intents.

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

## Post-Execution Checks

**Check for extension hooks (after constitution update)**:
Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_constitution` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently


## Enforcement Rules (MANDATORY — after the core flow)

Once the entire core flow above has completed and the constitution has been
written, ensure the canonical section below exists **exactly once**.

- **Match on the section title, not on its number.** A section counts as
  already present if its heading ends with `Functional Programming Paradigms (MANDATORY)`,
  whatever roman numeral it currently carries. Replace that entire section body
  with the canonical text below, keeping its existing number.
- If no such section exists, insert it as a new numbered principle section,
  after the last existing numbered principle section, preserving all other
  constitution content.
- **Renumber all numbered principle sections sequentially** (`### I.`,
  `### II.`, `### III.`, …) in document order after inserting. Another preset
  stacked on this command injects its own section the same way, so the numeral
  in the canonical text below is a placeholder — the final numbering is
  whatever sequential position the section lands in. Never emit two sections
  with the same numeral.
- Do not weaken, paraphrase, or omit any of the constraints.
- Do not remove or reword a governance section injected by another preset.

### Re-run the core flow's bookkeeping if this layer changed anything

The core flow performs its semantic-version bump, Sync Impact Report, validation,
and final user summary **before** this layer runs, so a section inserted or
rewritten above is invisible to all of it. Left alone, the constitution's
governance metadata contradicts its own contents — the classic case being a
constitution that already carried a sibling preset's section, so the core flow
saw "no change" while this layer went on to add a whole new principle.

First decide what this layer actually did:

- **No change** — the section was already present and its body already matched
  the canonical text verbatim. Do nothing further; skip the rest of this section.
  A re-run must not bump the version.
- **Body-only change** — the section existed and its body was replaced, or the
  only difference is renumbering. This is a `PATCH`-level change.
- **New principle added** — no such section existed and one was inserted. This
  is at least a `MINOR` change.

Then repeat the core flow's finalization steps for that change, in the same file:

1. **Version.** Re-derive `CONSTITUTION_VERSION` under the core flow's own
   semver rules, treating an added principle as `MINOR` and a body-only edit as
   `PATCH`. **Bump at most once per run.** If this run's Sync Impact Report
   already records a bump of equal or greater significance — because the core
   flow bumped, or because another stacked preset's layer already did — do not
   bump again; record your change under that existing version. Two stacked
   presets each adding a principle is one `MINOR` bump, not two.
2. **Sync Impact Report.** Update the HTML comment at the top of the file so it
   describes the constitution as it now stands: list this section under added or
   modified principles, and correct the `old → new` version line if step 1
   changed it. Amend the existing report; do not prepend a second one.
3. **`LAST_AMENDED_DATE`.** Set it to today if it is not already today's date.
4. **Validation.** Re-run the core flow's validation checks over the final file —
   the version line matches the report, no unexplained bracket tokens, dates are
   ISO `YYYY-MM-DD`, and principle numbering is sequential with no duplicates.
5. **Summary.** The core flow already reported a version and rationale to the
   user. If step 1 changed either, correct it in your final summary and say
   which section caused the change, so the user is not told a version that is no
   longer in the file.

## Canonical Section (body MUST be present verbatim)

The roman numeral below is a placeholder; the body is what must appear verbatim.

### I. Functional Programming Paradigms (MANDATORY)

All implementation MUST follow functional programming discipline throughout the codebase.
No exceptions are permitted without an explicit governance amendment.

- **Pure functions**: Every function MUST be free of observable side effects and MUST NOT
  mutate state outside its own scope.
- **Higher-order functions**: `map`, `filter`, `reduce`, and function composition MUST replace
  imperative loops (`for`/`while`). Recursion or functional iterators MUST be used instead.
- **Referential transparency**: Any function call MUST be replaceable with its return value
  without altering program behavior. Functions that violate this are not permitted.
- **No shared mutable state**: All required data MUST be passed as arguments. Global or
  shared mutable variables are prohibited.
- **Declarative style**: Code MUST describe *what* is computed, not *how* iteration proceeds.

## Output

The core flow writes `.specify/memory/constitution.md`. This layer edits that
file in place to enforce the section above, leaving every other section — including
governance sections injected by other stacked presets — untouched.


## Enforcement Rules (MANDATORY — after the core flow)

Once the entire core flow above has completed and the constitution has been
written, ensure the canonical section below exists **exactly once**.

- **Match on the section title, not on its number.** A section counts as
  already present if its heading ends with `Parse, Don't Validate (MANDATORY)`,
  whatever roman numeral it currently carries. Replace that entire section body
  with the canonical text below, keeping its existing number.
- If no such section exists, insert it as a new numbered principle section,
  after the last existing numbered principle section, preserving all other
  constitution content.
- **Renumber all numbered principle sections sequentially** (`### I.`,
  `### II.`, `### III.`, …) in document order after inserting. Another preset
  stacked on this command injects its own section the same way, so the numeral
  in the canonical text below is a placeholder — the final numbering is
  whatever sequential position the section lands in. Never emit two sections
  with the same numeral.
- Do not weaken, paraphrase, or omit any of the constraints.
- Do not remove or reword a governance section injected by another preset.

### Re-run the core flow's bookkeeping if this layer changed anything

The core flow performs its semantic-version bump, Sync Impact Report, validation,
and final user summary **before** this layer runs, so a section inserted or
rewritten above is invisible to all of it. Left alone, the constitution's
governance metadata contradicts its own contents — the classic case being a
constitution that already carried a sibling preset's section, so the core flow
saw "no change" while this layer went on to add a whole new principle.

First decide what this layer actually did:

- **No change** — the section was already present and its body already matched
  the canonical text verbatim. Do nothing further; skip the rest of this section.
  A re-run must not bump the version.
- **Body-only change** — the section existed and its body was replaced, or the
  only difference is renumbering. This is a `PATCH`-level change.
- **New principle added** — no such section existed and one was inserted. This
  is at least a `MINOR` change.

Then repeat the core flow's finalization steps for that change, in the same file:

1. **Version.** Re-derive `CONSTITUTION_VERSION` under the core flow's own
   semver rules, treating an added principle as `MINOR` and a body-only edit as
   `PATCH`. **Bump at most once per run.** If this run's Sync Impact Report
   already records a bump of equal or greater significance — because the core
   flow bumped, or because another stacked preset's layer already did — do not
   bump again; record your change under that existing version. Two stacked
   presets each adding a principle is one `MINOR` bump, not two.
2. **Sync Impact Report.** Update the HTML comment at the top of the file so it
   describes the constitution as it now stands: list this section under added or
   modified principles, and correct the `old → new` version line if step 1
   changed it. Amend the existing report; do not prepend a second one.
3. **`LAST_AMENDED_DATE`.** Set it to today if it is not already today's date.
4. **Validation.** Re-run the core flow's validation checks over the final file —
   the version line matches the report, no unexplained bracket tokens, dates are
   ISO `YYYY-MM-DD`, and principle numbering is sequential with no duplicates.
5. **Summary.** The core flow already reported a version and rationale to the
   user. If step 1 changed either, correct it in your final summary and say
   which section caused the change, so the user is not told a version that is no
   longer in the file.

## Canonical Section (body MUST be present verbatim)

The roman numeral below is a placeholder; the body is what must appear verbatim.

### I. Parse, Don't Validate (MANDATORY)

Untrusted data MUST be parsed into precise domain types at the boundary, never
merely validated and passed along as loose primitives. A validator answers
"is this ok?" and discards the answer the instant it returns; a parser returns a
more precise type that carries the proof forward. The type system MUST carry the
proof, not the programmer's memory. This principle is language-general and
applies to every TypeScript and Python surface in the codebase.

- **Keep the boundary untyped-safe**: All data entering the system from outside
  (network, disk, env, user input, `JSON.parse` / `json.loads`) MUST stay
  untyped-safe until parsed — `unknown` in TypeScript, or handed straight to a
  parser in Python. The `any` type (TypeScript) and the `Any` type (Python) are
  prohibited in domain code.
- **Branded / nominal domain types**: Values the program has earned the right to
  trust MUST be encoded as distinct types (e.g. `Email`, `UserId`), not bare
  `string`/`number`/`int`. Primitives that can be confused MUST be branded
  (TypeScript `unique symbol` / schema `.brand()`; Python `NewType`, pydantic /
  attrs model, or frozen dataclass) so they are not interchangeable.
- **Parsers, not validators**: Boundary functions MUST return a parsed domain
  type — a discriminated `Result` (`{ kind: "ok" | "err" }`) in TypeScript, or
  the parsed model / a single typed parse error in Python. Boolean `isValid*` /
  `is_valid_*` / `validate*` functions and scattered `throw`/`raise`-based
  validation at boundaries are prohibited.
- **The cast is confined to the parser**: Type assertions that mint a branded
  type (`x as Brand` in TypeScript, `cast(Brand, x)` in Python) are permitted
  ONLY inside the parser module that owns that brand. Forging a brand anywhere
  else is prohibited.
- **No shotgun parsing**: A given piece of data MUST be parsed once, at its
  boundary. Re-checking already-parsed values with scattered defensive `if`
  statements is prohibited.

## Output

The core flow writes `.specify/memory/constitution.md`. This layer edits that
file in place to enforce the section above, leaving every other section — including
governance sections injected by other stacked presets — untouched.
