---
name: to-specs
description: Use when a request or ticket needs to be turned into a spec and synced to the ticket system. Read-only (no code changes or implementation).
---

## Required `<project-root>/docs` reads

Read these before turning the request into a spec (shell `cat`/`ls` — may be in `.gitignore`, invisible to built-in search). Missing → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/code-navigation.md`
- `<project-root>/docs/database-tools.md`
- `<project-root>/docs/doc-lookup.md`
- `<project-root>/docs/issue-trackers.md`

Turn a request or ticket into a spec, sync to the ticket system. Read-only — no code changes, no implementation. Clarify requirements with the user before shaping — no assumptions, guesses, inferred intent. Treat ticket systems generically. Use `<additional-context>` for constraints and focus areas. Update existing tickets; create replacements only when asked. Big problems: name the destination first, keep all output on one ticket. Split into multiple tickets only when the user asks.

**Grill only for what the code cannot settle.** Repo, schema, docs, existing tickets are ground truth. Any question answerable by inspecting them gets answered by inspecting them, not asked. Grill the user only on critical decisions and genuine uncertainty the codebase cannot resolve: scope boundaries, business rules, product behavior choices, trade-offs between valid approaches, naming/placement when no existing pattern guides it, conflicts between the request and existing invariants. Before asking, try the codebase; if it resolves, record from inspection and do not ask.

**Loop with the user, never with yourself.** All iteration lives in the grilling phase (step 5) and the user-review gate (step 10) as back-and-forth with the user. No internal review/refactor/re-review cycles, re-shape loops, self-critique passes. Shape once from gathered context, present the spec exactly once (step 10), revise only on user request. Steps 8-9 are internal build steps — no draft, brief, plan, or partial spec to the user there. The user approves the final shaped spec once, before syncing.

<spec-template>

## Destination — the spec, decision, or change this effort delivers. One or two lines.
## Problem Statement — the user-facing problem or opportunity that drives the spec.
## Solution — the intended outcome from the user's perspective. Record each locked decision from grilling or repo inspection on one line with its source.
## Notes — other context, dependencies, or decisions worth keeping.

The description renders only the sections above. Implementation Items and Validation Items are NOT part of the description — they sync as checklists (short encoded form) and a patches comment (full structured blocks with `patch` code). See step 11.

</spec-template>

1. **Interpret Arguments**: Ticket reference/URL → `<ticket-url>`. Any other input → `<request>`. Extra focus areas or constraints → `<additional-context>`. No arguments → derive `<request>` from the conversation.

2. **Load Planning Context**: If `<ticket-url>` exists, load ticket context via the issue tracker tool (see `<project-root>/docs/issue-trackers.md`), store as `<planning-context>`. Read each attachment with `relativePath` via `read`. Describe images, extract key requirements from documents into `<attachment-insights>`, note inaccessible attachments. If `<ticket-url>` absent, treat the request or conversation as `<planning-context>`. Empty or missing → stop.

3. **Interpret Planning Context**: Derive from the full ticket (raw text + comments): `<planning-objective>`, `<operative-constraints>`, `<proposed-technical-direction>`, `<open-questions>` (unresolved only). Keep earlier comments that define constraints, business rules, implementation decisions, migration rules, naming, sequencing, scoping. Multiple independent subsystems → flag immediately, help the user identify the pieces, relationships, build order. Plan the first subsystem through the normal flow. Split into separate tickets only when the user asks.

4. **Gather Project Standards**: Read relevant `<project-root>/docs/` specs (project root and module-specific). Check the active memory provider for code standards, architecture, tech stack. Store as `<project-standards>`.

5. **Clarify Requirements with User (MANDATORY)**: Run a clarification interview before shaping by default. Only place iteration happens before shaping — loop with the user until shared understanding. Skipping is the exception; justify it in the spec output.

**Scope of grilling — code-answerable questions are out of bounds.** Before asking anything, try to resolve it from repo, schema, docs, existing tickets, `<project-standards>`. Questions about current behavior, existing patterns, callers, file locations, symbol names, data flow, schema shape, "how does X work today" → answered by inspection, never asked. Record from inspection, move on. Ask only about critical decisions and genuine uncertainty the codebase cannot settle: scope boundaries and out-of-scope, business rules and product behavior choices, trade-offs between valid approaches, naming/placement when no existing pattern guides it, conflicts between the request and existing invariants. Each question carries a recommended answer grounded in what the code does today, citing `file:line` where relevant.

Skip gate (all true): single atomic edit with no design decisions; `<proposed-technical-direction>` concrete and unambiguous; no earlier comments conflict; no open questions about scope, naming, placement, ordering, behavior; repo inspected and direction matches existing patterns; user explicitly confirmed in the current conversation.

Unclear request or any gate false/uncertain → invoke a clarification interview. If an accessible grilling or interview skill exists, load it and follow its discipline. Pass planning context, `<planning-objective>`, `<operative-constraints>`, `<proposed-technical-direction>`, `<open-questions>`, relevant module path(s). Store resolved decisions as `<clarified-requirements>`. Continue only after shared understanding. Reflect `<clarified-requirements>` in `<spec-description>`, `<requirement-items>`, or `<validation-items>`. Do not proceed to step 6 until all user inputs captured.

Skip reason (when used): `Skip reason: <all 6 conditions met because ...>`. Skipping without justification is a process violation.

6. **Gather Context** (repo, docs, skills):
- **Repo**: Entry points, existing patterns, callers, schema facts, `file:line` citations, validation of `<proposed-technical-direction>`, and a **surface inventory** of each layer the change touches (DB, model, policy, service, controller, API, UI, tests, config, docs, ops). For each layer: patch, new file, or no change, with concrete file(s) and symbol(s). Store as `<repo-context>`. `grep`/`find_file_by_name` for names, code navigation tool (see `<project-root>/docs/code-navigation.md`) for symbols/references, database tools (see `<project-root>/docs/database-tools.md`) for schema. Read one or two key files. Confirm current behavior and patterns. Note gaps; avoid false certainty.
- **Docs**: API signatures, version-specific behavior, gotchas for libraries, frameworks, Laravel features, `<proposed-technical-direction>`, API/best-practice questions. Store as `<doc-context>`. Use doc lookup per `<project-root>/docs/doc-lookup.md`.
- **Skills**: Planning touches specific domains (testing, frontend, Livewire) → invoke the relevant skills. Store as `<skill-context>`.

7. **Brainstorm Technical Approaches**: After inspecting the repo, brainstorm for complex tasks. Complex = touches multiple subsystems, multiple valid high-level approaches, lacks concrete `<proposed-technical-direction>`, or user flags it. Complex tasks: ask remaining clarifying questions one at a time — same rule as step 5, code-answerable questions resolved by inspection, not asked; ask only decisions the code cannot settle (approach trade-offs, scope, business rules); propose 2-3 approaches grounded in `<repo-context>` with trade-offs; lead with a recommendation; ask the user to choose one. Record as `<technical-approach-decision>`, get explicit alignment before shaping. Non-complex tasks: skip only when `<proposed-technical-direction>` is concrete and unambiguous and the user explicitly confirmed it.

8. **Build Action Inventory**: Before writing requirement items, list every concrete code change needed to deliver the destination. Use the surface inventory from `<repo-context>`. For each surface (DB, model, rules, services, API, UI, infra, tests, docs, ops), decide `no change` or a concrete action (`create`, `modify`, `delete`). Record `surface`, `action`, `target`, `depends-on`, `patch-ready` (`true` when the exact code change can be written from `<repo-context>`). Convert each `patch-ready` action into a requirement item in step 9. Every required action becomes a requirement item.

9. **Shape the Spec** (internal — do not present to the user): Write the spec using the template. Turn `<planning-objective>`, `<operative-constraints>`, `<proposed-technical-direction>`, `<clarified-requirements>`, `<technical-approach-decision>`, repo findings, `<project-standards>`, `<doc-context>`, `<skill-context>` into:
- `<spec-title>`: short, useful title.
- `<spec-description>`: the rendered spec template (Destination, Problem Statement, Solution, Notes only — NOT implementation/validation items). Must include: (a) destination and why it fixes scope, (b) chosen technical approach and why, (c) key user preferences and constraints, (d) accepted trade-offs. Specific to this spec and user.
- `<requirement-items>`: precise patch descriptions, one per spec step. Map each action from step 8 and each user preference from `<clarified-requirements>` to one or more requirement items.
- `<validation-items>`: validation checklist aligned with project testing conventions. Adhere to `<project-standards>`, `<doc-context>`, `<skill-context>`. Preserve valid technical details; improve incomplete ones when repo inspection gives better direction. No placeholder labels.

**Requirement Item Format**: Each `<requirement-item>` is a self-contained block an implementation agent can apply as a patch. No item describes an outcome without naming where the code changes. Required fields: `id` (stable spec-step-id like `S1` or short slug), `file` (repo-root-relative path(s); locator rule if multiple candidates), `symbol` (function/class/method/component; fully-qualified when ambiguous), `location` (exact insertion or modification point), `instruction` (one short imperative sentence: `add`/`remove`/`modify`/`replace`), `patch` (minimal code snippet or unified diff; required when target known; keep to the delta).

```
### S1: <title>
- file: app/Path/To/File.php
- symbol: ClassName::methodName
- location: inside methodName(), before `return $model;`
- instruction: Throw `ValidationException` when `$model->isLocked()`.
- patch:
  ```php
  if ($model->isLocked()) {
      throw ValidationException::withMessages(['status' => 'Model is locked.']);
  }
  ```
```

Rules: One item = one single-purpose patch. Split compound changes into separate items. Broader changes → sub-items (`S1a`, `S1b`). Verify paths and symbols against `<repo-context>`; no guesses. Cannot confirm a target → flag it in the item, let the user catch it at step 10 review. No exploratory steps ("investigate X", "consider Y", "ensure X", "update X as needed"). No alternative designs or re-evaluation after the user agrees on direction. Items describe code changes only. Runtime operations belong to the deploy process, not the spec: migrations, seeders, cache clears, queue restarts, and other user/ops actions are excluded even when the change requires them. The spec lists only what is included: exclusions decided during grilling shape the scope silently and appear nowhere in the spec — no "out of scope" lines, no mentions of excluded items.

10. **User Review** (the only spec presentation): Present the full shaped spec exactly once — `<spec-title>`, `<spec-description>`, `<requirement-items>`, `<validation-items>`. No brief or summary version first then the full version; one presentation only. In the same gate, reflect the user's inputs back: list 3-5 key decisions or constraints and where they appear (cite requirement/validation items); confirm the spec covers all concrete actions; then ask:
> Spec ready: `<spec-title>`. Implementation: N items. Validation: N items. Sync to the ticket system, or revise the spec?

This workflow is read-only. The only two outcomes of this gate: sync the spec or revise it. Never offer to apply, implement, or execute the spec — separate workflow. User asks to implement → decline, tell them to run the implementation workflow instead.

Wait for the user's response. Revise if asked. Sync only after approval.

11. **Sync Ticket**: Sync the spec to the ticket system via the issue tracker sync tool (see `<project-root>/docs/issue-trackers.md`). Final output: the ticket URL.
- `title`: `<spec-title>`, `description`: `<spec-description>` (Destination/Problem/Solution/Notes only — no implementation/validation items, no patch code).
- `checklists`: two non-empty sections as JSON array matching `{name, items: [{name, completed}]}`:
  - `{"name": "Implementation", "items": [{"name": "<requirement-item-encoded>", "completed": false}, ...]}`
  - `{"name": "Validation", "items": [{"name": "<validation-item>", "completed": false}, ...]}`
  - `<requirement-item-encoded>`: `S1: <title> - <file> @ <symbol>::<location> - <instruction>` (no `patch` code — checklists are short tracking items).
  - Before calling, verify the `checklists` schema against the sync tool's source.
- `patches comment`: post the full structured `<requirement-items>` blocks (with `patch` code) as a comment on the ticket via the issue tracker comment operation (see `<project-root>/docs/issue-trackers.md`). Keeps implementer code out of the card body, which overflows ticket systems with card-body limits (e.g. Trello). Skip only when the tracker has no comment support; then fall back to attaching the blocks as a file.
- `refUrl`: existing ticket URL → update; no `<ticket-url>` → omit `refUrl`, create new ticket, output the URL.

## Notes

- Ticket load tool downloads attachments to `storage/app/mcp/{source}` — read before planning. Use the ticket list tool to discover unresolved assigned tickets first. During clarification, ask the next question; do not restate previous answers.
