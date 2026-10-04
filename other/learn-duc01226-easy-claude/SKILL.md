---
name: learn
version: 4.3.0
description: '[Utilities] Use when teaching Claude a lesson that persists across sessions, including an extra rule for one skill or task kind (routes to project-skill-protocol).'
disable-model-invocation: false
---

## Quick Summary

**Goal:** Teach Claude lessons that persist across sessions by generalizing each lesson to its failure mode and routing it to the carrier a future session will actually read — the matching skill's project protocol when the lesson is skill-specific, otherwise the best-fit prose reference doc, `docs/project-config.json` when the lesson is really a machine-readable project fact, or the root `CLAUDE.md` project-rules section when it is a short, broad, project-specific rule or context note every task benefits from.

**Summary:** read-this-if-nothing-else digest of the main steps —

- **Generalize before anything else** — climb from the incident to the reusable failure mode; a lesson naming this ticket's files/services/tools is not a lesson yet.
- **Triage (value + recurrence + auto-fix) BEFORE routing** — persist only a project convention or a universal best-practice protocol worth reading on everyday work; a rare AI-agent quirk, a one-off incident or a detail of the current task is noise, and so is a lesson a review skill already catches.
- **Skill-specific lessons use the project protocol route:** when the lesson is an extra rule for a skill — learned during an active skill invocation, during a task whose route matched a skill, naming a skill, or about the kind of task one skill mainly owns (e.g. "when writing integration tests…" → `integration-test`) — treat it as a candidate overlay for that skill, compare it against the project-reference docs (`docs/project-reference` by default) and `docs/project-config.json` before recommending, ask the Carrier Choice question, and on an overlay pick call `/project-skill-protocol` with `add` for a new overlay or `update <exact-name>` only after exact-name resolution; save to a reference doc or config field only when the user picks that carrier.
- **Root-context route (CLAUDE.md):** a lesson that is a general project rule/convention or project context info (architecture constraint, naming rule, domain term, tool quirk of THIS project) is a candidate for the hand-owned `## Project Rules & Context` section of the root `CLAUDE.md` — only when ALL of: applies to most tasks, ≤ 3 lines, project-specific (a universal framework rule is never a project note), not better served by a reference doc / overlay / config field, and size headroom exists (root ≤ 32768 bytes). Show the exact line + target section and get the user's confirmation, write only that section, then run `sync-codex` so `AGENTS.md` and the mirrors follow. Otherwise keep today's routing. Full gate: [Project Root Context Route](#project-root-context-route-claudemd-blocking).
- **Ask which carrier, with a recommendation:** present the carrier options via `AskUserQuestion` — recommended option first, labelled `(Recommended)` — before any write; never pick the carrier silently.
- **Keep ordinary routing for ordinary lessons:** when the lesson is not skill-specific or no active/matching skill exists, use the existing FACT/RULE carrier route and confirmation flow.
- **Classify the carrier, don't default to prose:** a lesson stating a project FACT (path, run-command, module map, convention, tooling choice) belongs in `docs/project-config.json`, the machine-readable map every skill reads first; a lesson stating a RULE or pattern belongs in the matching `docs/project-reference/` doc. Both can apply — write the fact to config AND the rule to prose. To learn what the config holds and its exact field names, read the file or use `/project-config` (it runs `--describe`).
- **Delegate overlay correctness:** `/project-skill-protocol` retains its mode resolution, target/scope resolution, additive-only constraint, collision/contradiction handling, proposal/user-confirmation gate and two-write contract; Learn must not bypass or replace it.
- **Assess prevention depth** — doc/config update, prompt rule, static protocol lesson, hook, test, or skill update.
- **Confirm target with the user, save, then run the 3 mandatory end tasks** — Learn Review → `/why-review` → carrier-specific final quality pass (Markdown enhancement + AI-discovery, or configuration parser/schema validation).

**Workflow:**

1. **Capture** -- Identify the lesson from user instruction or experience
2. **Route** -- Analyze lesson content against any active/matching skill, the Reference Doc Catalog, AND `docs/project-config.json`; select the project-protocol route for skill-specific lessons, otherwise the best target carrier (prose doc, config field, or both)
3. **Save** -- After the applicable confirmation gates, delegate a skill-specific lesson the user placed in an overlay to `/project-skill-protocol`; otherwise append the lesson to the selected file (a CLAUDE.md pick writes only the hand-owned `## Project Rules & Context` section, and `sync-codex` runs after the end tasks)
4. **Confirm** -- Acknowledge what was saved and where
5. **Learn Review** -- Run the mandatory 2-step end gate (`Learn Review` + `/why-review`)
6. **Final quality pass** -- Supported prose uses `/prompt-enhance` then the AI-discovery gate; machine-readable configuration uses its owner parser/schema validation after the final write.

**Key Rules:**

- **GENERALIZE FIRST (the #1 protocol):** Extract the GENERIC lesson that applies to many cases — NEVER save the specific case as-is. The user's words describe one incident; your job is to climb from that incident to the reusable rule. Strip every project/file/tool/domain name. If the saved text only helps on this exact ticket, you failed — abstract it up a level. (Enforced by the Lesson Quality Gate below.)
- Triggers on "remember this", "always do X", "never do Y"
- **Triage first:** pass the Value gate (project convention or universal best-practice protocol, worth reading on everyday work) + Recurrence gate + Auto-fix gate BEFORE routing or saving
- Smart-route to the most relevant file, NOT always `lessons.md` in the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path)
- **Consider `docs/project-config.json` on EVERY routing decision** — a lesson that is really a project fact (path, run-command, module map, tooling choice) belongs in the machine-readable map, not in prose; read it or use `/project-config` to know its schema before deciding
- Use exact config schema field names (`node .claude/hooks/lib/project-config-schema.cjs --describe`) and prefer an existing field — NEVER invent a key, and route config writes through `/project-config`
- Check for existing entries before creating duplicates
- Confirm target file with user before writing
- **Skill-specific route:** When any trigger of the [Skill-Specific Project-Protocol Route](#skill-specific-project-protocol-route-blocking) holds (active skill, matched route, named skill, or a task kind one skill owns), treat the lesson as a candidate extension of that skill's project protocol and compare carriers before asking. On an overlay pick, call `/project-skill-protocol add ...` for a new overlay, or `/project-skill-protocol update <exact-name> ...` only after exact-name resolution identifies an existing overlay. Save it only to a reference doc, `lessons.md` or a config field when the user picks that carrier.
- **Protocol authority:** Preserve `/project-skill-protocol`'s mode resolution, target/scope resolution, additive-only constraint, target-collision and contradiction handling, proposal/user-confirmation gate, three-write contract, and mirror-sync rule. Learn must not bypass or replace any of them.
- **Confirmation remains required:** Keep Learn's existing user confirmation and mandatory end-task flow; delegating a skill-specific candidate does not waive the project protocol's own proposal/user-confirmation gate.
- **Ordinary-route fallback:** When no active/matching skill exists or the lesson is not skill-specific, keep the existing FACT/RULE classification, carrier routing, confirmation, save, and end-task flow.
- **CLAUDE.md is a destination, not a default:** offer it only when every Root-Context condition holds (broad + ≤ 3 lines + project-specific + no better carrier + headroom); a detailed, lookup-style or niche lesson stays in its reference doc, a one-skill rule in an overlay, a machine-readable fact in config, a universal framework rule in a shared protocol. — why: CLAUDE.md is loaded into every session, so each byte costs every task.
- **CLAUDE.md consent + sync:** NEVER silently self-edit an instruction file — show the exact proposed line and target section, ask via `AskUserQuestion`, write only after confirmation, then run `sync-codex` (after the end tasks) and report which mirrors changed.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

## Usage

### Add a lesson

```
/learn always use the validation framework fluent API instead of throwing ValidationException
/learn never call external APIs in command handlers - use Entity Event Handlers
/learn prefer async/await over .then() chains
```

### Add a skill-specific lesson (routes to a `/project-skill-protocol` overlay)

```
/learn when reviewing changes, always check that migration scripts are idempotent
/learn /plan should always include a rollback step
```

### Add a project-wide rule or context note (routes to the root `CLAUDE.md` when it qualifies)

```
/learn in this repo every new module needs an entry in the module registry before any other change
/learn the term "tenant" always means the billing account here, never a user group
```

### List lessons

```
/learn list
```

### Remove a lesson

```
/learn remove 3
```

### Clear all lessons

```
/learn clear
```

## Reference Doc Catalog (READ before routing)

Each file in the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path) is auto-initialized by `session-init-docs.cjs` hook and populated by `/scan-*` skills. Understanding their roles is **critical** for correct routing: routing is static — read the doc whose **Read Trigger** matches your task.

| File                             | Role & Content                                                                                   | Read Trigger (static)               | Scan Skill                |
| -------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------- | ------------------------- |
| `project-structure-reference.md` | Architecture, directory tree, tech stack, module registry, service map                           | New area / architecture work        | `/scan --target=project-structure` |
| `backend-patterns-reference.md`  | Backend/hook patterns: CJS modules, CQRS, repositories, validation, message bus, background jobs | Editing backend / CQRS / API files  | `/scan --target=backend-patterns`  |
| `seed-test-data-reference.md`    | Seed/dev-data patterns: environment gate, idempotency loop, DI scope safety, command-dispatch    | Seeder / DataSeeder file edits      | `/scan --target=seed-test-data` |
| `frontend-patterns-reference.md` | Frontend patterns: components, state mgmt, API services, styling conventions, directives         | Editing frontend / UI files         | `/scan --target=frontend-patterns` |
| `integration-test-reference.md`  | Test architecture: base classes, fixtures, helpers, service-specific setup, test runners         | Integration test file edits         | `/scan --target=integration-tests` |
| `feature-spec-reference.md`      | Feature doc templates, app-to-service mapping, doc structure conventions                         | Authoring / reading feature specs   | `/scan --target=feature-spec`      |
| `code-review-rules.md`           | Review rules, conventions, anti-patterns, decision trees, checklists                             | Any review skill activation         | `/scan --target=code-review-rules` |
| `lessons.md`                     | General lessons — fallback catch-all. Read on EVERY task (per project-reference-docs gate)       | Every task                          | Managed by `/learn`       |
| Configured styling reference | CSS/preprocessor conventions, naming, tokens, theming, responsive behavior | Styling edits | Follow the configured scan owner; generic custom docs use `scan --target=generic-reference-doc --filename=<configured-file>`; manual docs remain owner-maintained |
| `design-system/README.md`        | Design system: tokens overview, component inventory, app-to-doc mapping                          | Design / UI file edits              | `/scan --target=design-system`     |
| `e2e-test-reference.md`          | E2E test patterns: framework, page objects, config, best practices                               | E2E file edits                      | `/scan --target=e2e-tests`         |
| `domain-entities-reference.md`   | Domain entities, data models, DTOs, aggregate boundaries, ER diagrams, cross-service sync        | Backend / frontend domain work      | `/scan --target=domain-entities`   |
| `docs-index-reference.md`        | Documentation tree, file counts, doc relationships, keyword-to-doc lookup                        | Doc lookup / navigation             | `/scan --target=docs-index`        |

**Key insight:** `lessons.md` and `code-review-rules.md` are the highest-recurrence routing targets — read them on every relevant task. Place high-recurrence lessons where the matching **Read Trigger** guarantees a future session opens them.

### Also a routing destination: `docs/project-config.json` (machine-readable, NOT prose)

The catalog above is prose. `docs/project-config.json` is the project's **machine-readable map** — modules/paths, framework + search keywords, test/E2E/integration run-commands, design system, architecture rules, workflow patterns — and it is what `CLAUDE.md` and the `docs/project-reference/**` docs are generated from. Every skill is told to read it BEFORE investigating, planning, or coding, so a fact recorded there reaches more sessions than the same fact written into one prose doc.

**Read Trigger:** every task, ahead of the prose docs. **Owned by:** `/project-config`.

**Learn its shape before routing anything into it** — either read `docs/project-config.json` directly, or invoke `/project-config`, which knows the schema and its exact field names:

```bash
node .claude/hooks/lib/project-config-schema.cjs --describe   # exact field names + per-field derivation notes
```

| Lesson really is…                                                                                          | Carrier                                             |
| ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| A project **FACT** a schema field already models — a path, glob, run-command, module/service map, framework or tooling choice, doc root, test/E2E/integration setup, startup or health-check command | `docs/project-config.json` (via `/project-config`)  |
| A **RULE, pattern, or anti-pattern** an agent must reason with                                              | the matching doc in the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path)          |
| Both — a new fact AND the rule for using it                                                                 | write the fact to config AND the rule to prose      |

Rules:

- MUST check `docs/project-config.json` as a candidate on EVERY routing decision — why: a project fact written only as prose is invisible to the tooling that reads the config, and is silently overwritten the next time the generated docs regenerate from it.
- MUST use exact schema field names (`--describe`, copy verbatim) and prefer an EXISTING field over a new one — why: unknown keys are accepted as warnings (`project-config-schema.cjs` unknown-key warnings), so an invented key looks like it worked while no consumer ever reads it.
- No existing field fits → do NOT invent a top-level key silently. Route the lesson to prose and surface the gap to the user as a proposed schema addition — why: a schema change is a framework decision, not a side effect of `/learn`.
- Prefer routing the config write through `/project-config` (Plan → Review → Execute + validation) over hand-editing the JSON — why: it validates after each phase and knows the field names this skill would otherwise guess.
- Config carries FACTS, never prose lessons — NEVER paste a narrative lesson into a config string field. — why: the config is consumed by tooling and by every skill's prefetch; prose there bloats every session and belongs in a reference doc.

---

## Smart File Routing (CRITICAL)

### Lesson Triage Gate (MANDATORY — run FIRST, before routing or saving)

| Gate           | Question                                                                               | Pass           | Fail → Action                                        |
| -------------- | -------------------------------------------------------------------------------------- | -------------- | ---------------------------------------------------- |
| **Value**      | "Is this a project convention (a stable rule this codebase follows in everyday work) or a universal best-practice protocol — worth an agent reading on an ordinary day?" | Yes → continue | No → skip `/learn`; rare AI-agent quirks, one-off incidents, tool/environment hiccups and details of the current session's task are not lessons |
| **Recurrence** | "Would this mistake recur in a future session WITHOUT this reminder?"                  | Yes → continue | No → skip `/learn`; mistake is situational           |
| **Auto-fix**   | "Could `/code-quality-review`, `/simplify`, `/security-audit`, or a linter catch this automatically?" | No → continue  | Yes → skip `/learn`; update the review skill instead |

**All three gates must pass.** Persistent memory is read on every task, so it holds only what makes everyday work better: a project convention or a universal best practice. A rare agent quirk or a detail of this session's task costs every future reader attention and prevents nothing; a lesson review skills already catch adds noise; a one-off situational mistake won't be prevented by a persisted rule.

---

### Skill-Specific Project-Protocol Route (BLOCKING)

A project overlay (owned by `/project-skill-protocol`) is the carrier that fires exactly when the skill runs — a skill-specific rule saved to `lessons.md` or a prose doc reaches the skill only by chance. Before applying the generic Routing Table, detect whether ANY trigger holds:

| # | Trigger | Example |
| --- | --- | --- |
| T1 | The user asks to learn something during an active skill invocation | mid-`/changes-review`: "remember to also check X" |
| T2 | The lesson is learned while performing a task whose route matched a skill | a `custom-simple [… → changes-review]` route surfaces a review gap |
| T3 | The lesson names a skill, or adds a rule/step/check to what a skill does | "`/plan` should always list rollback steps" |
| T4 | The lesson is about a kind of task one skill mainly owns, even without naming it | "when writing integration tests, always seed via commands" → `integration-test` |

**Resolve the owning skill (T3/T4):** match the lesson's task kind against skill `Use when …` descriptions in the skills catalog; cite the matching description. One clear owner → `exact` target. A family sharing a name pattern (e.g. every `*-review` skill) → `glob` target. Two or more owners that share no name pattern → one `exact` overlay per owner, listed together in the Carrier Choice question. No owner, or the rule applies across unrelated tasks → the lesson is NOT skill-specific; use the generic Routing Table. — why: a guessed owner puts the rule where it never fires.

When any trigger holds:

1. Identify the target skill (or glob family) by its exact name, with the evidence that matched it.
2. Treat the lesson as a candidate extension of that skill's project protocol.
3. **Compare carriers before recommending (BLOCKING).** The overlay is a candidate, not the default. Check it against the same carriers the generic route uses: the [Reference Doc Catalog](#reference-doc-catalog-read-before-routing) and [Routing Table](#routing-table) (resolved under the reference-docs root, default `docs/project-reference`), and `docs/project-config.json` (FACT vs RULE). Recommend the reference doc when its Read Trigger already fires for this kind of task and the rule is not about the skill's own steps (a T4 lesson about integration tests usually belongs in `integration-test-reference.md`); recommend the overlay when the rule changes what the skill itself does. — why: a project-reference doc is read by every agent doing that kind of work, while an overlay reaches only runs of that one skill.
4. **Carrier Choice question (BLOCKING).** `AskUserQuestion` with the recommended option FIRST, labelled `(Recommended)`, each option naming its concrete target path:
    - *Skill overlay for `<skill>` via `/project-skill-protocol`* — an `exact` overlay applies on every run of that skill; a `glob` overlay applies unless an `exact` overlay for the same skill exists, because the most specific tier wins
    - *Overlay + reference doc* — only when the lesson also carries a project-wide rule beyond the skill; name the doc path
    - *Reference doc only* — name the path, e.g. `integration-test-reference.md` or `lessons.md` under the reference-docs root
    - *Project config field* — when the lesson is a machine-readable FACT (see FACT vs RULE)
    - *Root `CLAUDE.md` project note + `sync-codex`* — only when the lesson also passes the Project Root Context Route candidate test (C1–C5) despite being skill-related; each question holds 2–4 options, so drop the weakest

    State a one-line reason for the recommendation. When the Prevention Depth Assessment applies, ask it as a SECOND question in the same `AskUserQuestion` call (each question holds 2–4 options), so the user answers once. — why: the user owns where a persistent rule lives; a silent carrier choice is the main way lessons land where no future run reads them.
5. **MUST ATTENTION** On an overlay choice, call `/project-skill-protocol add ...` for a new overlay or `/project-skill-protocol update <exact-name> ...` only after exact-name resolution identifies an existing overlay (run its `list` first when unsure).
6. **MUST ATTENTION** Let `/project-skill-protocol` perform its own mode resolution, target/scope resolution, additive-only screen, target-collision and contradiction handling, proposal/user-confirmation gate and two-write contract. Do not write overlay bodies or index rows directly from Learn.
7. On a *Reference doc only* or *Project config field* pick, continue with Routing Decision Process steps 9–10 (append to the doc, or route the config value through `/project-config`). On *Overlay + reference doc*, do both. Do not save the candidate only to `lessons.md` or another generic prose carrier unless the user picked that option.

If no trigger holds, continue with the generic Routing Table — the carrier confirmation there still offers the options with a recommendation.

---

### Project Root Context Route (CLAUDE.md) (BLOCKING)

The root `CLAUDE.md` is loaded into EVERY session automatically, so a line there reaches every task with no read step — and costs tokens in every session. It is the right carrier for a short, broad, project-specific rule or context note, and the wrong one for anything detailed. Evaluate this route for every lesson that passed the Triage Gate, alongside the FACT-vs-RULE classification and (when a T1–T4 trigger holds) the skill-specific route.

**Candidate test — ALL five must hold, otherwise use today's routing:**

| # | Condition | Fails when → fall back to |
| --- | --- | --- |
| C1 | **Broad** — applies to most tasks in this project, not one file type, phase or skill | one area → its reference doc; one skill → overlay |
| C2 | **Short** — states as ≤ 3 lines / ≤ ~300 characters, one rule or fact per entry | detailed, example-heavy or lookup-style → a project reference doc |
| C3 | **Project-specific** — a convention, architecture constraint, naming rule, domain term, or tool quirk of THIS project | universal framework rule → the Static Protocol Lesson route (shared protocols, framework maintainers) — never a CLAUDE.md note |
| C4 | **No better carrier** — no reference doc whose Read Trigger already fires for this work, no skill overlay, no `docs/project-config.json` field (a FACT such as a path or run-command is config data; the generator renders it into `CLAUDE.md`) | that carrier |
| C5 | **Headroom** — `CLAUDE.md` exists and stays ≤ 32768 bytes after the edit (the generator's `ROOT_OVERFLOW` threshold in `generate-claude-md.cjs`), and the `## Project Rules & Context` section stays ≤ ~2 KiB / ≤ ~12 entries | a project reference doc (or condense the section first — never add beyond budget) |

**Which destination fits:**

| The lesson is… | Destination | Why |
| --- | --- | --- |
| Broad + short + project-specific rule, convention or context with no schema field | root `CLAUDE.md` → `## Project Rules & Context`, then `sync-codex` | always in context, AGENTS.md follows |
| Machine-readable project fact the config models (path, run-command, module map, tooling) | `docs/project-config.json` via `/project-config` | every skill reads it first; generators render it into the root |
| Detailed, niche or lookup-style rule, pattern, anti-pattern or checklist for one kind of work | matching project reference doc (Read Trigger) | read only when that work starts |
| Rule bound to one skill's own steps | skill overlay via `/project-skill-protocol` | fires exactly when that skill runs |
| General catch-all lesson that is not broad or short enough for the root | `lessons.md` | dated catch-all, budgeted |
| Universal framework rule (any project, silent failure, high recurrence) | NOT a project note — Static Protocol Lesson promotion to the shared protocols, reviewed by framework maintainers | project notes must not carry framework rules |

**Durable home (write ONLY here):** a hand-owned `## Project Rules & Context` section placed outside every `<!-- SECTION:key -->` fence and every `CK:*` managed block. `ai-context-refresh --mode update` rewrites only fence bodies and keeps everything outside them verbatim (`updateMarkedSections` in `generate-claude-md.cjs`), and the Codex projection is a heading whitelist (`AGENTS_PROJECTION_HEADINGS` in `sync-context-workflows.mjs`) that includes this heading. A note inside a fence is overwritten by the next regeneration; a note under a heading the whitelist omits never reaches `AGENTS.md`. If the section is absent, create it (heading + bullets) immediately after the `## Doc Lookup — What to Read When` section, so it projects early into `AGENTS.md` and reads before the generated rules. No `CLAUDE.md` yet → not a candidate: run `/ai-context-refresh` first or route elsewhere. A path-scoped rule that the project already renders from `contextGroups[].rules` belongs in config via `/project-config` (regenerated by `ai-context-refresh --mode update`), not in this section.

**Procedure when C1–C5 hold:**

1. **Measure** — read `CLAUDE.md` byte size (`node -e "console.log(require('fs').statSync('CLAUDE.md').size)"`, platform-neutral) and the section's current size; C5 fails → say so and fall back.
2. **Draft** — one generic bullet, ≤ 3 lines, no incident nouns (Lesson Quality Gate; the project-convention exception keeps the convention's own terms). Check the section for an existing entry on the same rule — update it instead of adding a duplicate.
3. **Confirm (BLOCKING)** — `AskUserQuestion` with the recommended option first, labelled `(Recommended)`. Show the exact proposed line, the target section, and `size before → after / 32768`. Options: *Root CLAUDE.md project note (+ sync-codex)* · *Reference doc (name the path)* · *lessons.md* · *Skill overlay / config field* when one applies (2–4 options; drop the weakest). A rejected or unanswered question writes nothing.
4. **Write** — Edit only the hand-owned section; never touch a fence, a `CK:*` block, or generated text.
5. **End tasks** — Learn Review → `/why-review` → `/prompt-enhance` scoped to the section (never the generated fences) → AI-discovery gate.
6. **Sync (after the final CLAUDE.md edit)** — when `AGENTS.md` or `.codex/` exists, run `node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --skip=claude-md` (the same root-source handoff `ai-context-refresh` uses; Windows/macOS/Linux neutral). If the runner fails, keep the task open, report the failing stage and the recovery command, and do not claim the mirrors are current. No Codex mirrors in the project → record "no mirrors" and skip.
7. **Verify, read-only** — (a) re-measure `CLAUDE.md` bytes ≤ 32768; (b) the new line lies outside every `<!-- SECTION:… -->` fence (fence open/close lines above it balance), which is what guarantees `update` preserves it; (c) the line appears in `AGENTS.md`; (d) `git status --short AGENTS.md .codex .agents .opencode` lists the mirrors that changed — report them, never stage or commit.

---

### Routing Table

Route to the **most relevant file** based on lesson content. Every bare `*.md` filename in the `Route to` column resolves inside the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path):

| If lesson is about...                                                                                                                    | Route to                                                | Section hint                                                    |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| Code review rules, anti-patterns, review checklists, YAGNI/KISS/DRY, naming conventions, review process                                  | `code-review-rules.md`           | Add to most relevant section (anti-patterns, rules, checklists) |
| Backend/hook patterns: modules, CQRS, repositories, entities, validation, message bus, background jobs, migrations, configured persistence | `backend-patterns-reference.md`  | Add to relevant section or Anti-Patterns section                |
| Frontend patterns: components, state stores, forms, API services, styling conventions, directives, pipes                                  | `frontend-patterns-reference.md` | Add to relevant section or Anti-Patterns section                |
| Integration/unit tests: test base classes, fixtures, test helpers, test patterns, assertions, test runners                               | `integration-test-reference.md`  | Add to relevant section                                         |
| E2E tests: Playwright, Cypress, Selenium, page objects, E2E config, browser automation, visual regression                                | `e2e-test-reference.md`          | Add to relevant section                                         |
| Domain entities, data models, DTOs, aggregates, entity relationships, cross-service data sync, ER diagrams                               | `domain-entities-reference.md`   | Add to Entity Catalog or Relationships section                  |
| Project structure, directory organization, module boundaries, tech stack choices, service architecture                                   | `project-structure-reference.md` | Add to relevant architecture section                            |
| Styling conventions selected by project config, including CSS/preprocessor rules, tokens, theming, and responsive design | Configured styling reference | Add to the relevant styling section or route it to the document owner |
| Design system, design tokens, component library, UI kit conventions, Figma-to-code patterns                                              | `design-system/README.md`        | Add to relevant design section                                  |
| Feature documentation, doc templates, doc structure conventions, app-to-service doc mapping                                              | `feature-spec-reference.md`      | Add to relevant conventions section                             |
| Documentation indexing, doc organization, doc-to-code relationships, doc lookup patterns                                                 | `docs-index-reference.md`        | Add to relevant section                                         |
| **Project FACTS the config models:** source/module paths, globs, service or app maps, framework + search keywords, test / E2E / integration run-commands, system startup or health-check commands, doc roots, design-system or styling locations, tooling choices | `docs/project-config.json` **via `/project-config`**    | Existing schema field, exact name from `--describe` — NEVER an invented key |
| **Broad + short (≤ 3 lines) project rule, convention or context** that passes all five conditions of the [Project Root Context Route](#project-root-context-route-claudemd-blocking) | root `CLAUDE.md` `## Project Rules & Context`, then `sync-codex` | Bullet in the hand-owned section; user confirmation first |
| General lessons, workflow tips, tooling, AI behavior, project conventions, anything not matching above                                   | `lessons.md`                     | Append as dated list entry                                      |

---

### Prevention Depth Assessment (MANDATORY before saving)

Before saving any lesson, critically evaluate whether a doc update alone is sufficient or a deeper prevention mechanism is needed:

| Prevention Layer                            | When to use                                                                   | Example                                                                                     |
| ------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Doc update only**                         | Team convention or rule needed only when doing that kind of work (the lesson already passed the Value gate) | "Always use fluent validation API" → `backend-patterns-reference.md` |
| **Project config field** (`docs/project-config.json`) | The lesson is a machine-readable project FACT every skill should ground on before acting | "Integration tests need the system started first" → `integrationTestVerify.startupScript` / `systemCheckCommand` via `/project-config` |
| **Root project note** (`CLAUDE.md` `## Project Rules & Context`) | A short, broad, project-specific rule or context note every task benefits from (Root Context Route C1–C5) | "Every new module is registered in the module registry first" → root `CLAUDE.md` + `sync-codex` |
| **Prompt rule** (`development-rules.md`)    | Rule that ALL agents must follow on every task                                | "Grep after bulk edits" → `.claude/docs/development-rules.md`                               |
| **Static protocol lesson** (`sync-inline-versions.md`) | Universal AI mistake, high recurrence, silent failure, any project | "Re-read files after context compaction" → `.claude/skills/shared/sync-inline-versions.md` |
| **Hook** (`.claude/hooks/`)                 | Automated enforcement, must never be forgotten                                | "Marker strings must match across producer and consumer" → a shared constants module + consistency test |
| **Test** (`.claude/hooks/tests/`)           | Regression prevention, verifiable invariant                                   | "All hooks import from shared module" → test in `test-all-hooks.cjs`                        |
| **Skill update** (`.claude/skills/`)        | Workflow step that should always include this check                           | "Review changes must check doc staleness" → skill SKILL.md update                           |

**Decision flow:**

1. **Capture** the lesson
2. **Ask:** "Could this mistake recur if the AI forgets this lesson?" If yes → needs more than a doc update
3. **Ask:** "Can this be caught automatically by a test or hook?" If yes → recommend hook/test
4. **Evaluate Static Protocol Lesson promotion** (see below)
5. **Present options to user** with `AskUserQuestion` — recommended option first, labelled `(Recommended)`, with a one-line reason; on the skill-specific route, ask them as the second question of the Carrier Choice `AskUserQuestion` call instead of asking twice:
    - "Doc update only" — save to the best-fit reference file (default for most lessons)
    - "Doc + prompt rule" — also add to `development-rules.md` so all agents see it
    - "Doc + Static Protocol Lesson" — also add to shared protocol lessons (see criteria below)
    - "Full prevention" — plan a hook, test, or shared module to enforce it automatically
6. **Execute** the chosen option. For "Full prevention", create a plan via `/plan` instead of just saving.

### Static Protocol Lesson Promotion (MANDATORY evaluation)

After generalizing a lesson, evaluate whether it qualifies as a **Static Protocol Lesson** in `.claude/skills/shared/sync-inline-versions.md`. Static protocol lessons live in that canonical file and reach every session through the universal hook (the `universal` group of `protocol-groups.json`); the root `CLAUDE.md` and `AGENTS.md` carry none of them.

**Qualification criteria (ALL must be true):**

1. **Universal** — Applies to ANY AI coding project, not just this codebase
2. **High recurrence** — AI agents make this mistake repeatedly across sessions without the reminder
3. **Silent failure** — The mistake produces no error/warning; it silently degrades output quality
4. **Not already covered** — No existing Static Protocol Lesson addresses the same root cause

> **Static Protocol Lessons** — Universal AI mistake prevention rules delivered by the universal hook. Stored in `.claude/skills/shared/sync-inline-versions.md` under the `ai-mistake-prevention` SYNC block (published to `.claude/skills/shared/protocols/ai-mistake-prevention.md`). Each must be universal, high-recurrence, and silent-failure.
> READ `.claude/skills/shared/sync-inline-versions.md` to check for duplicates before adding.

**If qualified:** Recommend "Doc + Static Protocol Lesson" option. On user approval, append the lesson as a new bullet to the relevant shared SYNC blocks, then run `node .claude/scripts/build-protocol-projection.cjs` so the hook-delivered projection regenerates from the canonical source. The build fails when the protocol's universal bin exceeds its character budget: condense existing bullets before adding one.

**If NOT qualified:** Explain why (e.g., "A project convention, not universal", "Already covered by existing Static Protocol Lesson about X", "Not silent — the failure is already visible"). Proceed with doc-only or prompt-rule option. (A rare or one-off lesson never reaches this step — the Value gate already rejected it.)

### Lesson Quality Gate (BLOCKING — generalize before you save)

> **CORE PROTOCOL — do not skip:** A `/learn` request always arrives as a SPECIFIC case ("don't migrate via the bus and spam Elasticsearch"). Saving it verbatim is the default failure mode. You MUST transform specific → generic BEFORE writing: name the underlying class of mistake, drop the incident's nouns, and write a rule that fires across many future cases ("migrations write the DB directly, never via message bus — applies to all migrations"). If you cannot state the lesson without naming this ticket's files/services/tools, it is NOT generic yet — climb one more abstraction level. When in doubt, save the MORE generic version; a too-specific lesson is dead weight injected on every prompt.

Every lesson MUST be **root-cause level and generic across any codebase**. Apply this 3-step extraction before saving:

**Step 1 — Name the FAILURE MODE, not the symptom:**

The failure mode is the reasoning or assumption that broke — not what the output looked like.

| Symptom (BAD — reject this)       | Failure mode (GOOD — save this)                                                                                  |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| "Used wrong enum value"           | "Generated code using an assumed API without verifying it exists in source"                                      |
| "Wrong namespace/import"          | "Assumed project setup from convention without reading project-specific config files first"                      |
| "Happy-path test failed in CI"    | "Wrote assertions without tracing what runtime infrastructure the code path requires"                            |
| "Set properties that don't exist" | "Assumed all types in a hierarchy share the same interface without reading the base class"                       |
| "Always read file X before Y"     | "Assumed execution context without reading the owning layer's contract — fixed at symptom site instead of cause" |

**Step 2 — Verify generality:**

Does this failure mode apply to ≥3 different contexts or codebases? If only one file or one specific case → go up one abstraction level. A good lesson prevents an entire _class_ of mistakes.

**Step 3 — Write as a universal rule:**

- Strip ALL project-specific names, file paths, class names, and tool names
- Must be useful on any codebase, any language, any task type
- If multiple mistakes share the same failure mode → consolidate to ONE lesson, not many
- Test: "Would an AI working in Java, Go, or Python on a different project benefit from this?" If yes → good. If no → rewrite.
- **Project-convention exception:** a stable rule of THIS codebase (the Value gate's first kind) keeps the convention's own terms — state the rule an agent follows on everyday work here, never this session's incident, and route it to the project doc whose Read Trigger fires for that work.

**Anti-pattern examples:**

- BAD: "Always check `src/shared/markers.ts` for marker strings" → project-specific path
- GOOD: "When consolidating modules, ensure shared constants are imported from a single source of truth — never define inline duplicates."
- BAD: "Update `.claude/docs/hooks/README.md` after deleting hooks" → project-specific file
- GOOD: "Deleting components causes documentation staleness cascades — map all referencing docs before removal."
- BAD: "Read GlobalUsings.cs before adding usings in \*.IntegrationTests" → project-specific file
- GOOD: "Before generating code that uses project conventions (imports, namespaces, annotations), read the project's bootstrap/configuration files for that layer — convention files override framework defaults silently."

### End-Phase Learn Review Gate (MANDATORY before marking complete)

Run these 2 tasks at the end of every `/learn` operation:

**Task 1 — Learn Review (value + generality + recurrence):**

- Keep only lessons with clear prevention value.
- Lesson must be either:
    - Universal across many projects/codebases, OR
    - A stable project-wide principle (architecture invariant, naming invariant, workflow invariant).
- Reject lessons that are:
    - Specific to the current ticket/change/file or to what happened in this session's task,
    - Rare AI-agent quirks or edge cases with low recurrence — nothing an agent would benefit from reading on an ordinary day,
    - Already covered by existing lessons or review skills.
- If target is `lessons.md` (injected on every prompt), apply stricter bar: high impact + high recurrence only.

**Task 2 — Run `/why-review` (adversarial challenge):**

- Use `/why-review` to challenge whether this lesson deserves persistent memory.
- Verify:
    - Why this lesson prevents repeated mistakes,
    - Why this should be a lesson instead of a one-time note,
    - Why auto-checks (`/code-quality-review`, `/simplify`, `/security-audit`, linters, hook/test) are insufficient.
- If rationale is weak, rewrite at higher abstraction or skip `/learn`.

### Routing Decision Process

1. **Run Triage Gate** — value + recurrence + auto-fix filters; stop here if any fails
2. **Read the lesson text** — identify keywords and domain
3. **Apply Lesson Quality Gate** — analyze root cause, generalize, verify universality
4. **Detect skill-specific route.** If any trigger T1–T4 holds, follow the Skill-Specific Project-Protocol Route: it runs step 5 (FACT vs RULE) and step 6 (Prevention Depth) as part of its carrier comparison and Carrier Choice question, then replaces steps 7–8 (steps 9–10 still save a doc or config pick); otherwise continue.
5. **Classify the carrier — FACT vs RULE (do this BEFORE the generic Routing Table).** Ask: *"Is this a machine-readable project fact, or a rule an agent must reason with?"* Fact → `docs/project-config.json`; rule → a prose reference doc; both → both. To decide, read the config or use `/project-config` (`--describe`) so the judgment rests on the real schema, never on a guess about what the config holds. — why: skipping this step is how a project fact ends up as prose that no tooling reads and the next regeneration contradicts.
6. **Run Prevention Depth Assessment** — determine if doc/config-only or deeper prevention needed
7. **Match against the generic Routing Table** — pick the best-fit file (or config field); run the [Project Root Context Route](#project-root-context-route-claudemd-blocking) candidate test (C1–C5) — when all five hold, `CLAUDE.md` joins the options
8. **Ask the user with a recommendation:** `AskUserQuestion` with the best-fit carrier first as `(Recommended)` plus the one-line reason, then the viable alternatives (another doc, config field, the root `CLAUDE.md` note when C1–C5 hold, a skill overlay if a weak T4 owner exists)
9. **On confirm** — read target file, find the right section, append the lesson (config target → route through `/project-config`; `CLAUDE.md` target → follow the Root Context Route procedure: write only the hand-owned section, end tasks, `sync-codex`, verify)
10. **On reject** — ask user which file to use instead

### Format by Target File

**For `lessons.md`** (general lessons):

```markdown
- [YYYY-MM-DD] <lesson text>
```

**For root `CLAUDE.md`** (project rules and context):

```markdown
## Project Rules & Context

- <rule or context note, ≤ 3 lines, present tense, no incident nouns>
```

- Hand-owned section outside every `<!-- SECTION:… -->` fence; bullets only, no dates, no headings inside
- Budget: ≤ ~2 KiB / ≤ ~12 entries; over budget → condense or merge entries first, or route the lesson to a reference doc

**For pattern/rules files** (code-review-rules, backend-patterns, frontend-patterns, integration-test):

- Find the most relevant existing section in the file
- Append the lesson as a rule, anti-pattern entry, or code example
- Use the file's existing format (tables, code blocks, bullet lists)
- If no section fits, append to the Anti-Patterns or general rules section

## Budget Enforcement (MANDATORY for `lessons.md`)

`lessons.md` — resolved inside the reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path) — is a static project-reference carrier read during project work. Token budget must be controlled.

**Hard limit:** 20000 characters (~6666 tokens). Check BEFORE saving any new lesson.

**Workflow when adding to `lessons.md`:**

1. Read file, count characters (run `wc -c` on the resolved `lessons.md` path)
2. If current + new lesson > 20000 chars → trigger **Budget Trim** before saving
3. If under budget → save normally

**Budget Trim process:**

1. Display all current lessons with char count each
2. Evaluate each lesson on two axes:
    - **Universality** — How often does this apply? (every session vs rare edge case)
    - **Recurrence risk** — How likely is the AI to repeat this mistake without the reminder?
3. Score each: **HIGH** (keep as-is), **MEDIUM** (candidate to condense), **LOW** (candidate to remove)
4. Present to user with `AskUserQuestion`: "Budget exceeded. Recommend removing/condensing these LOW/MEDIUM items: [list]. Approve?"
5. On approval: condense MEDIUM items (shorten wording), remove LOW items, then save new lesson
6. On rejection: ask user which to remove/condense

**Condensing rules:**

- Remove examples, keep the rule: `"Patterns like X break Y syntax"` → just state the rule
- Merge related lessons into one if they share the same root cause
- Target: each lesson ≤ 250 chars (one concise sentence + bold title)

**Does NOT apply to:** Other routing targets (`backend-patterns-reference.md`, `code-review-rules.md`, etc.) — those files have their own size and are injected contextually, not on every prompt.

## Behavior

1. **`/learn <text>`** — Run the existing triage and quality gates; for a skill-specific lesson, follow the Skill-Specific Project-Protocol Route (an overlay pick calls `/project-skill-protocol add ...` or `update <exact-name> ...`), otherwise route and append to the best-fit file (check budget if target is `lessons.md`)
2. **`/learn list`** — Read and display lessons from ALL 12 target files (show file grouping + char count for `lessons.md`), plus the `## Project Rules & Context` entries of the root `CLAUDE.md` when that section exists (show its byte size and the root size against 32768)
3. **`/learn remove <N>`** — Remove lesson from `lessons.md` by line number
4. **`/learn clear`** — Clear all lessons from `lessons.md` only (confirm first)
5. **`/learn trim`** — Manually trigger Budget Trim on `lessons.md`
6. **File creation** — If target file doesn't exist, create with header only (never create a root `CLAUDE.md` here — that is `/ai-context-refresh`)
7. **Removing a root-note entry** — `/learn remove` still targets `lessons.md` by line number; removing a `## Project Rules & Context` entry follows the same confirm → edit that section only → `sync-codex` flow

## Auto-Inferred Activation

When Claude detects correction phrases in conversation (e.g., "always use X", "remember this", "never do Y", "from now on"), this skill auto-activates. When auto-inferred (not explicit `/learn`), **confirm with the user before saving**: "Save this as a lesson? [Y/n]". If any Skill-Specific Project-Protocol Route trigger (T1–T4) holds, use that route; otherwise use ordinary routing.

## How Lessons Reach the AI

Lessons and pattern references are read per the universal `project-reference-docs-guide` protocol (delivered by the universal hook) and the Doc Lookup table in `CLAUDE.md`:

- `lessons.md` — read on **every** task (the gate always includes it).
- Pattern/rule references (`backend-patterns-reference.md`, `code-review-rules.md`, etc.) — read by their matching trigger (see the Reference Doc Catalog table above).
- Root `CLAUDE.md` `## Project Rules & Context` — in context from session start on every task; `AGENTS.md` carries it after `sync-codex`.

Claude and Codex load the same lessons and patterns: the protocol comes from the universal hook, the routing table from the root file.

## Prompt Enhancement (MANDATORY final step)

After saving a lesson, route the final quality pass by carrier. Supported Markdown prose: run `/prompt-enhance` on the modified prose file(s) to optimize attention anchoring and token quality. Machine-readable configuration (including project-config JSON): NEVER pass it to the Markdown enhancer or insert summary/reminder prose; run the owning configuration parser/schema validator after the final write and record its result. Unsupported carriers require their owner's validation route, not a guessed prose rewrite.

**When to run:**

- After every successful save to a supported Markdown carrier (subject to the skip conditions below)
- Pass the specific file path(s) that were modified

**What it does:**

- Ensures the new lesson integrates with existing top/bottom summary anchoring
- Optimizes token usage — tightens prose, merges redundant content
- Verifies no content loss from the save operation

**Then run the AI-discovery gate (`SYNC:ai-discovery-doc-quality`) on each modified prose file (configuration uses its schema gate instead):** a lesson reaches the file's top critical rules or closing reminders only when it outranks a rule already there (those anchors hold 1–3 rules; otherwise it stays in its section, stated once); the carrier stays reachable from the docs index or root context (a new carrier doc gets a trigger row there); an edited pointer to another doc is `read <path> when <situation>` with an existing target.

**How to invoke** — substitute the resolved reference-docs root (default `docs/project-reference`; a `docsRoots.projectReference.path` entry in `docs/project-config.json` overrides the path):

```
/prompt-enhance <reference-docs root>/<modified-file>.md
```

For a root `CLAUDE.md` save, scope the enhance to the `## Project Rules & Context` section only — never rewrite a generated `SECTION:*` fence or `CK:*` block — and run `sync-codex` AFTER it, so the mirrors capture the final root.

**Skip conditions (do NOT run prompt-enhance if):**

- The carrier is machine-readable configuration: use its owner parser/schema validation after the final write instead
- The save was to `lessons.md` AND the file is under 1500 chars (too small to benefit)
- The user explicitly requests "save only, no enhance"

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ATTENTION ask user whether to skip.
>
> **Mandatory end tasks are ALWAYS (in order):**
>
> 1. "Run **Learn Review** (lesson value + generality + recurrence gate)."
> 2. "Run `/why-review` to challenge whether the lesson is worth persistent memory."
> 3. "Run the carrier-specific final quality pass: `/prompt-enhance <modified-prose-file>` when applicable, or owner parser/schema validation after the final configuration write."
>
> Do NOT mark the skill complete until review, rationale challenge and the applicable final quality pass have evidence. Record documented prose skip conditions explicitly.

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `ai-discovery-doc-quality` — Agent-guide content value, authority, retention and verified discovery; writing a doc that an agent reads → .claude/skills/shared/protocols/ai-discovery-doc-quality.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:ai-discovery-doc-quality:reminder -->

**MUST ATTENTION** AI-read guides: purpose/read-when and priorities first; retain action-changing rules, exceptions and rationale; verify triggered discovery and parser contracts. Use the content-value and semantic-disposition gate after enhancement; keep evidence in temporary reports and fix generated output at its source.

<!-- /SYNC:ai-discovery-doc-quality:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION** GENERALIZE FIRST — extract the generic, many-cases rule; NEVER persist the specific incident as written. Strip all ticket/file/service/tool names before saving.

**IMPORTANT MUST ATTENTION** Skill-specific route: when the lesson is learned during an active skill or a skill-matched route, names a skill, or concerns the kind of task one skill mainly owns (T1–T4), compare the overlay with the project-reference docs and config, ask the Carrier Choice question with the best carrier as `(Recommended)`, then save to the picked carrier: an overlay through `/project-skill-protocol` — `add` for a new overlay, `update <exact-name>` only after exact-name resolution — or a reference doc / config field through Routing Decision Process steps 9–10.

**IMPORTANT MUST ATTENTION** Root-context route: a lesson that is a general project rule/convention or project context info qualifies for the root `CLAUDE.md` ONLY when it is broad (most tasks), short (≤ 3 lines), project-specific, not better served by a reference doc / overlay / config field, and the root stays ≤ 32768 bytes; write only the hand-owned `## Project Rules & Context` section (outside every `SECTION:*` fence) after `AskUserQuestion` confirmation showing the exact line, then run `sync-codex` (`node .claude/skills/sync-codex/scripts/run-codex-sync.mjs --skip=claude-md`), re-check the size and report the changed mirrors — otherwise fall back to a reference doc / `lessons.md` / overlay / config — why: CLAUDE.md is in every session's context, so it carries only what every task needs, and a note inside a generated fence is overwritten by the next regeneration.

**IMPORTANT MUST ATTENTION** Preserve `/project-skill-protocol`'s mode resolution, target/scope resolution, additive-only constraint, collision/contradiction handling, proposal/user-confirmation gate and two-write contract; Learn must not bypass or replace that protocol. Keep ordinary carrier routing when no active/matching skill exists or the lesson is not skill-specific.

**IMPORTANT MUST ATTENTION Goal:** Persist each lesson at its failure-mode level into the carrier a future session will actually read — the matching skill's project protocol when the lesson is skill-specific, otherwise the best-fit prose reference doc or `docs/project-config.json` when the lesson is really a machine-readable project fact.

**IMPORTANT MUST ATTENTION** main steps, in order: generalize → Triage Gate → Lesson Quality Gate → detect skill-specific route (**compare carriers; an overlay pick delegates to `/project-skill-protocol`**) OR **classify carrier (FACT → config · RULE → prose · both → both)** → Prevention Depth Assessment → confirm with user → save → Learn Review → `/why-review` → carrier-specific final quality pass (prose enhancement + AI-discovery, or configuration parser/schema validation) → `sync-codex` + size/mirror verification (root `CLAUDE.md` saves only).
**IMPORTANT MUST ATTENTION** run Triage Gate FIRST — if the lesson is not a project convention or a universal best-practice protocol worth reading on everyday work, OR recurrence is low, OR review skills can catch it, skip `/learn` entirely
**IMPORTANT MUST ATTENTION** check Reference Doc Catalog to find the best target file — NOT always `lessons.md`
**IMPORTANT MUST ATTENTION** consider `docs/project-config.json` as a candidate carrier on EVERY routing decision, alongside the prose docs — read it directly or use `/project-config` to learn its sections and exact field names first — why: a project fact written only as prose is invisible to the tooling that reads the config and is contradicted the next time the generated docs regenerate from it.
**IMPORTANT MUST ATTENTION** when routing into the config, copy field names verbatim from `node .claude/hooks/lib/project-config-schema.cjs --describe`, prefer an EXISTING field, and route the write through `/project-config`; no field fits → surface a proposed schema addition to the user instead of inventing a key — why: unknown keys only warn (`project-config-schema.cjs` unknown-key warnings), so an invented key looks applied while no consumer reads it.
**IMPORTANT MUST ATTENTION** keep the config to FACTS — NEVER paste a narrative lesson into a config string field; the rule belongs in the matching prose reference doc.
**IMPORTANT MUST ATTENTION** mandatory end tasks are ALWAYS: `Learn Review` → `/why-review` → the applicable carrier-specific final quality pass (in order; documented prose skip conditions recorded)
**IMPORTANT MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting
**IMPORTANT MUST ATTENTION** prefer auto-injected files for high-recurrence lessons (higher visibility)

**Anti-Rationalization:**

| Evasion                                          | Rebuttal                                                                                             |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| "It's a lesson, so it goes in a lessons doc"     | Classify FACT vs RULE first. A path, run-command, or module map is config data — prose hides it from every consumer that reads the config. |
| "I know roughly what the config holds"           | Read it or run `/project-config` (`--describe`). Routing on a guessed schema writes a field nobody reads. |
| "No field fits, I'll add a sensible key"         | Unknown keys only warn. Surface a proposed schema addition to the user — never invent one silently.   |
| "Saving the user's exact words is most faithful" | Verbatim is the default failure mode. Climb to the failure mode; strip this ticket's nouns.           |
| "Small lesson, skip the end gate"                | Learn Review and `/why-review` run on every save; final quality pass follows the carrier and documented prose skip conditions.                    |
| "Every agent should see it — put it in CLAUDE.md" | Only a broad, ≤ 3-line, project-specific note with size headroom qualifies; detail goes to a reference doc, a one-skill rule to an overlay, a universal framework rule to the shared protocols. |
| "I'll drop it into a generated CLAUDE.md block"  | Fences are regenerated from config and template. Write only the hand-owned `## Project Rules & Context` section, after user confirmation, then `sync-codex`. |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
