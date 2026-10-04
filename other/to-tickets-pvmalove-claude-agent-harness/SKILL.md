---
name: to-tickets
description: Break a plan, spec, or conversation into a set of tracer-bullet tickets with blocking edges, and publish them to the configured tracker.
disable-model-invocation: true
---

# To Tickets

**Objective:** Break a plan, spec, or conversation into a set of **tickets** — tracer-bullet vertical slices, each declaring its blocking edges.

The issue tracker and triage label vocabulary should have been provided to you. If not, tell the user to run `/setup-matt-pocock-skills`.

## Execution in Two Phases

You must execute this skill in two distinct phases. Do NOT publish anything to the issue tracker or create local files until the user explicitly approves the ticket breakdown.

### Phase 1: Drafting & Review
1. **Gather Context:** Work from the conversation context. If passed a reference (spec path, issue number/URL), read its full body and comments.
2. **Explore the Codebase (Optional):** Use the project's domain glossary. Look for prefactoring opportunities ("Make the change easy, then make the easy change").
3. **Draft Vertical Slices:** Break the work into **tracer bullet** tickets.
    - *Vertical Slices:* Cut a narrow but COMPLETE path through every layer (schema, API, UI, tests). Must be demoable/verifiable on its own and fit in a single context window.
    - *Wide Refactors (Exception):* If a change has a massive blast radius (e.g., renaming a shared column), use **expand-contract** instead of vertical slicing. Sequence as: Expand → Migrate (in batches) → Contract.
    - *Blocking Edges:* Give each ticket its blocking edges (which other tickets must complete first).
    - *Story Points:* Assign every `afk` ticket a Fibonacci story-point score, using `story_points.scale` from `.harness/project.json` when present, otherwise `1, 2, 3, 5, 8, 13…`. This is a decomposition-quality signal, not a commitment. `hitl` tickets never receive a score — skip this field for them.
    - *Escalation Pass:* If a ticket's primary score equals `story_points.gray_zone` (default `4`), run one cheap-model advisory call for that ticket alone (`model: haiku` or the cheapest configured equivalent — same model-selection rule as step 4's Discovery Context call, but one call per gray-zone ticket, not one call for the whole batch). If the two scores disagree, keep the higher (more conservative) one. If no cheap-model route exists, stop and report the blocker before presenting the approval request, same as step 4.
    - *Pipeline Label:* Derive the ticket's `pipeline::*` label from its final score: `pipeline::fast` when the score is `≤ story_points.fast_threshold` (default `3`) *and* `Execution: afk`; `pipeline::full` when the score is `≥ story_points.full_threshold` (default `5`) *and* `Execution: afk`. A score `≥13` also means the slice isn't tracer-bullet-sized — flag it on the STOP-AND-ASK gate in step 5 as needing further splitting. `hitl` tickets never receive a `pipeline::*` label.
4. **Prepare Discovery Context (when the parent has `## Relevant Files (Discovery Context)`):** Parse that section after drafting the proposed tickets. It is an approved starting context, not a replacement for a ticket's own scope.
    - Assign every listed path to every tracer bullet it materially supports; a shared path may belong to more than one ticket. For each assignment, retain the supplied context and add one short ticket-specific reason. If a path supports no proposed ticket, surface it as **unassigned** and stop for the user's decision; never assign it artificially.
    - Build a **Path inventory** for the whole batch. For each Discovery Context path, include the path and enumerate every path under those directories: its direct containing directory, plus existing `tests/` and `shared/` directories. Apply the repository's default exclusions while expanding directories: secrets, dependencies, build/dist output, caches, generated/minified files, large logs, databases, temporary data, and unrelated media. Keep an explicitly approved Discovery Context file even if it matches an exclusion, but never expand that excluded category. A Discovery Context file at repository root is included as that file, never by adding the repository root. Do not read or send file contents or symbol signatures, and do not include paths outside these directories.
    - Use **one cheap-model advisory call** exactly once per batch. If the runtime can pin a model, use `model: haiku` (or the cheapest configured equivalent); otherwise use the runtime's configured cheapest-model route. Give it the proposed ticket titles, scopes, assigned paths, and the Path inventory. Ask it to return only additions: for each ticket, exact paths already present in the Path inventory and one concise reason each. It may add dependencies, especially tests and shared code; it must not remove or move assigned paths, invent paths, or change ticket scope. If no cheap-model route exists, stop and report blocker before presenting the approval request; never substitute the current model.
    - Add every valid suggested dependency to the relevant ticket's Discovery Context with its reason. Discard suggestions that are not exact Path inventory paths or do not support that ticket's end-to-end behavior. The resulting per-ticket lists are ready only when every original path is assigned (or explicitly surfaced as unassigned) and every addition is traceable to the Path inventory.
5. **STOP AND ASK (Quiz the User):** Present the proposed breakdown as a numbered list. For each ticket, show:
    - **Title:** Short descriptive name
    - **Blocked by:** Which tickets gate it
    - **Story Points / Pipeline:** For `afk` tickets, the final Fibonacci score and the derived `pipeline::fast`/`pipeline::full` label, flagged `⚠️ score ≥13 — split further` when that applies. Omit for `hitl` tickets — they carry neither a score nor a `pipeline::*` label.
    - **What it delivers:** The end-to-end behavior
    - **Relevant Files (Discovery Context):** Assigned and advisory-added paths, each with its reason; omit this field when the parent has no Discovery Context.
    - *Ask the user:* Does the granularity feel right? Are blocking edges correct? Should anything be merged/split? Does the story-point score feel right, and is the derived pipeline label correct — the user may override the label on the gate without changing the score.
    - **DO NOT PROCEED TO PHASE 2 UNTIL APPROVED.**

### Phase 2: Publishing & Summarizing (After Approval)
1. **Publish to the Tracker:** The method depends on the configured tracker:
    - **Integration branch:** Read the parent epic's `## Integration Branch` section before writing
      any child ticket. Copy its exact branch name into every child ticket; if the epic has no
      integration branch, stop and report the missing prerequisite instead of inferring one.
    - **Local files:** Write one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md` (01, 02...). Use `<local-ticket-template>`. Include the finished per-ticket `Relevant Files (Discovery Context)` list when Discovery Context was present. Set `**Workflow:**` to `status::blocked` if it has blockers, otherwise `status::ready`. Set `**Execution:**` to `hitl` or `afk` per your best judgment of the ticket (see `docs/agents/triage-labels.md`). For `afk` tickets, set `**Story Points:**` to the final score from step 3 and `**Pipeline:**` to the label approved on the STOP-AND-ASK gate — the derived label, or the user's override if they changed it there; the score itself never changes. Omit both lines entirely for `hitl` tickets. Add `**Task report:** required` unless told to skip it (omit the line entirely if not required). `/implement` finds the next ticket by reading each file's `**Workflow:**` field — a purely linear chain resolves top to bottom.
    - **GitHub / Real Tracker:**
        - Publish one issue per ticket in dependency order using `gh issue create --body-file <path>`. **CRITICAL:** Do NOT use inline `--body` heredoc, as it breaks bash quoting.
        - Include the finished per-ticket `## Relevant Files (Discovery Context)` section when Discovery Context was present. Preserve the exact paths and their reasons; it is the implementation ticket's curated starting context.
        - Include the finished `## Story Points` section (the approved score) for `afk` tickets; omit the section entirely for `hitl` tickets.
        - Apply labels (see `docs/agents/triage-labels.md` for the full taxonomy): `type::*`, `status::ready` (or `status::blocked` if gated by another ticket in this batch), `hitl`/`afk`, `pipeline::fast` or `pipeline::full` for `afk` tickets — the label approved on the STOP-AND-ASK gate, the derived label or the user's override, never applied to `hitl` tickets — and `task-report::required` unless told to skip it.
        - *Grouping:* Link every ticket to the parent epic as a **native sub-issue**. Do NOT use `epic::<slug>` labels.
        - *Local Mirror:* The epic spec already lives in its own folder under `docs/tasks/` (per `docs/agents/artifacts.md`) — rename that folder to `issue-<epic-id>-<epic-slug>/` first if it was still slug-only. Save each published ticket's issue body into that folder's `tickets/` subfolder, as `tickets/issue-<ID>-<slug>.md` — not flat alongside the spec.
        - *Frontier:* Don't trace `Blocked by` by hand to find what's takeable — query it, the same fields and mechanism as `/wayfinder`'s frontier query (`docs/agents/issue-tracker.md#wayfinding-operations`), scoped to the epic's sub-issues instead of the map's children. `/implement` runs this same query itself when handed the epic instead of a specific ticket.
        - Do NOT close or rewrite the parent epic issue, except to append a short list of the subtask numbers you created.
2. **Summarize the Batch:**
    - Read `language` from `.harness/project.json` (default `ru` if the file or field is absent) — this decides only the "What to build" column below, not the ticket titles/bodies you publish, which stay in whatever language you drafted them in.
    - If this runtime supports dispatching a sub-agent pinned to a specific model, send a single call with `model: haiku` (cheapest available, one call for the whole batch) — pass it every ticket's title and body plus the target language, asking for one concise sentence per ticket written in that language. Otherwise, write the descriptions yourself, on your own model, in the same language.
    - Output a final table compiling all data. The labels column must list all applied taxonomy tags (e.g., `type::feature`, `status::ready`, `afk`, `pipeline::fast`, `task-report::required`).

   | Ticket | What to build | Story Points | Labels |
      |---|---|---|---|
   | <number/link/path> | <one-line summary> | <score, or "—" for `hitl`> | <comma-separated labels> |

---

<local-ticket-template>
# <NN> — <Ticket title>

**What to build:** The end-to-end behavior this ticket makes work from the user's perspective.
**Blocked by:** The numbers/titles of the tickets that gate this one, or "None — can start immediately".
**Integration branch:** The exact branch recorded by the parent epic.

## Relevant Files (Discovery Context)
- `<path>` — why this ticket needs it (omit this section when the parent has no Discovery Context).

**Category:** type::bug / type::feature / type::refactoring / type::chore / type::security / type::performance / type::hotfix
**Workflow:** status::ready (or status::blocked)
**Execution:** hitl / afk
**Story Points:** Fibonacci score (afk tickets only; omit the line entirely for hitl tickets)
**Pipeline:** pipeline::fast / pipeline::full (afk tickets only, derived from Story Points; omit the line entirely for hitl tickets)
**Task report:** required (omit the line entirely if not required)

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
  </local-ticket-template>

<issue-template>
## Parent
A reference to the parent issue on the tracker (if applicable).

## Integration Branch

The exact integration branch recorded by the parent epic. Child implementation branches start
from this branch and their PRs target it.

## What to build
The end-to-end behavior this ticket makes work from the user's perspective.

## Story Points
The approved Fibonacci score (afk tickets only; omit this section entirely for hitl tickets — the
derived pipeline::fast/pipeline::full label is applied on the tracker, not written here).

## Relevant Files (Discovery Context)
- `<path>` — why this ticket needs it (omit this section when the parent has no Discovery Context).

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by
- A reference to each blocking ticket, or "None — can start immediately".
  </issue-template>

*Note for both templates: `Relevant Files (Discovery Context)` is the sole file-path section; keep only the assigned paths and their short reasons. Avoid paths and code snippets everywhere else unless it is a vital prototype snippet (trim to decision-rich parts only).*

<!--
<local-ticket-template>
# <NN> — <Название задачи>

**What to build:** Поведение системы от начала до конца, которое эта задача делает рабочим с точки зрения пользователя.
**Blocked by:** Номера/названия задач, которые блокируют эту, или "None — can start immediately".
**Integration branch:** Точная ветка, записанная родительским эпиком.

## Relevant Files (Discovery Context)
- `<path>` — зачем этот файл нужен задаче (пропустите секцию, если в эпике нет Discovery Context).

**Category:** type::bug / type::feature / type::refactoring / type::chore / type::security / type::performance / type::hotfix
**Workflow:** status::ready (или status::blocked)
**Execution:** hitl / afk
**Story Points:** Оценка по Фибоначчи (только для afk-тикетов; полностью пропустите строку для hitl-тикетов)
**Pipeline:** pipeline::fast / pipeline::full (только для afk-тикетов, производная от Story Points; полностью пропустите строку для hitl-тикетов)
**Task report:** required (полностью пропустите эту строку, если не требуется)

- [ ] Критерий приемки 1
- [ ] Критерий приемки 2
  </local-ticket-template>

<issue-template>
## Parent
Ссылка на родительскую задачу в трекере (если применимо).

## Integration Branch

Точная интеграционная ветка, записанная родительским эпиком. Дочерние ветки реализации начинаются
с этой ветки, и их PR направляются в неё.

## What to build
Поведение системы от начала до конца, которое эта задача делает рабочим с точки зрения пользователя.

## Story Points
Итоговая оценка по Фибоначчи (только для afk-тикетов; полностью пропустите секцию для hitl-тикетов —
производная метка pipeline::fast/pipeline::full выставляется в трекере, а не пишется здесь).

## Relevant Files (Discovery Context)
- `<path>` — зачем этот файл нужен задаче (пропустите секцию, если в эпике нет Discovery Context).

## Acceptance criteria
- [ ] Критерий 1
- [ ] Критерий 2

## Blocked by
- Ссылка на каждую блокирующую задачу, или "None — can start immediately".
  </issue-template>

*Примечание к обоим шаблонам: `Relevant Files (Discovery Context)` — единственная секция с путями; оставляйте в ней только назначенные файлы и краткие причины. В остальных секциях избегайте путей и фрагментов кода, кроме жизненно важного фрагмента прототипа (оставьте только части, насыщенные решением).*
-->
