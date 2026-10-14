---
name: demo-guide
version: 2.0.0
description: '[Documentation] Use when you need to generate a step-by-step demo guide (demo script / walkthrough) covering all main user stories and their test cases — scope from a named feature, else the current working context, else confirm with the user — explaining for each case how the domain data is stored/changed and how the domain solves the feature. Triggers: demo guide, generate demo guide, demo script, demo walkthrough, how to demo, prepare demo, sprint demo, user story demo.'
---

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** **UNDERSTAND the feature first, then script it** — investigate the capability end-to-end until you can answer the comprehension bar with `file:line`, and only then produce a stakeholder-ready demo guide that lists every **main user story** with its **REAL test-case IDs**, gives a **step-by-step demo flow** per case, explains **how the domain stores/changes the data and how that solves the feature**, and places every case on the **proof ladder** — so the presenter can show the behaviour, explain the data behind it, and never claim proof that was not earned.

**Summary — read this if nothing else.** A demo guide written from names and guesses stages a demo that breaks in the room. So: investigate first, prove every claim, then write. Main steps, in order:

1. **RESOLVE scope** — prompt → current working context → `AskUserQuestion`. NEVER invent the feature silently.
2. **LOAD the contract** (`references/demo-guide-template.md`) and **SIZE the target into a tier S0–S4**; announce both in one line.
3. **DECOMPOSE into story groups** (≥2 from tier S2) and **BREAK THE WORK INTO TASKS before the first deep read** — `TaskList` first; a group task completes only when its block is **on disk**.
4. **[BLOCKING GATE] UNDERSTAND the feature** — clear the 6-question comprehension bar with `file:line` each, **delegating to read-only investigation skills** (`/scout`, `/investigate`, `/debug-investigate`, `/graph-trace`, `/spec-index`) when a direct read cannot answer one. No demo step is written before this gate clears.
5. **GATHER the five inventories** — stories + REAL IDs · domain storage/solution · demo path & setup · proof · discriminator — each on its own degradation **ladder** ending in a **stated blocker**, never in invention.
6. **MAP story → cases** and persist the map before writing.
7. **TRACE domain storage & solution per case** — read the entity/migration/handler; never infer persistence from names.
8. **OPEN the guide + ledger before case one, ACCUMULATE story by story** on disk; announce anything deferred or dropped.
9. **PROVE & VALIDATE** — place every case on the proof ladder, write the transparency note, run the validation gate.

**Flags:** `feature-or-scope` arg · `--context` · `--output` · `--lang` · `--html` · `--stories`.

**Workflow:**

0. **Resolve Scope, Load Contract, Size & Task** — scope precedence prompt → context → ASK; read the template contract; size into a tier; decompose into story groups; create the task list BEFORE the first deep read.
1. **Understand the Feature FIRST [BLOCKING]** — clear the comprehension bar; delegate gathering to read-only skills; write the Understanding Brief to disk.
2. **Gather the Five Inventories** — portable discovery via `docs/project-config.json`; every inventory walks its ladder and records the rung it landed on.
3. **Map Stories → Cases** — main stories, REAL `TC-*` / test IDs, coverage gaps named.
4. **Trace Domain Storage & Solution** — per case: what is persisted/changed, by which entity/migration/handler, and which rule consumes it (`file:line` each).
5. **Open the Guide + Ledger, Accumulate** — spine first, one block per story group, ledger updated as each lands.
6. **Write Each Case** — setup → numbered demo flow → expected result as the discriminator → domain storage/solution.
7. **Prove** — proof ladder per case + test-execution transparency note.
8. **Validate** — the gate below; nothing declared done before it passes.

**Key Rules (the contract):**

- **UNDERSTAND BEFORE YOU SCRIPT.** The Step 1 comprehension bar is a **[BLOCKING] gate**: until you can answer all six questions with `file:line`, you have no demo to write. — why: a demo step invented from a screen name is a demo that fails live, in front of the people it was written for.
- **Scope precedence is prompt → current context → ASK.** An explicit feature in the prompt wins; else derive from current work; else `AskUserQuestion` — NEVER invent a feature.
- **Every case carries four parts:** setup/preconditions · numbered **step-by-step demo flow** · **expected result phrased as the discriminator** vs the old behaviour · **how the domain stores/changes data & solves the feature**. A case missing the storage/solution part is incomplete.
- **PROOF IS EARNED, NEVER ASSERTED.** Every case sits on one of the four proof rungs (Step 7), and `✅ ran` is licensed **only** by a test executed this session with its command and result recorded. There is no fifth rung: a case you cannot place is a **stated blocker**.
- **REAL IDs ONLY — NEVER invent a test case ID.** A story with no case says _"no test covers this"_ and is recorded as a coverage gap. — why: a fabricated ID retires a risk that is still live.
- **Cite `file:line` for every storage/behaviour claim** — read the entity, the mapping, and the migration. NEVER infer persistence from a field name.
- **A demo step is traced to a real user path, or it is a stated blocker** — NEVER an invented click, endpoint, or screen, and never state faked by a path a user could not reach.
- **DELEGATE THE GATHERING, NEVER THE SCRIPTING.** Read-only delegates only; their output is INPUT, re-verified at `file:line` before it becomes a claim. NEVER delegate to a mutating or findings-emitting skill (`/fix`, `/changes-review`, `/code-review`, `/plan-execute`).
- **ACCUMULATE ON DISK, NEVER IN CONTEXT.** Open the guide before case one; append per case and per story group; synthesize the guide-level sections **from the written blocks**. — why: partial results on disk beat complete results that never got written.
- **NO SECRET VALUES, ANYWHERE.** Setup steps, run commands, and seed instructions name the setting, the file, and the account **role** — never a credential, token, key, connection string, or customer identifier. Secrets render `<redacted:…>` from the moment they would enter context.
- **NO SILENT TRUNCATION.** Anything deferred, sampled, or dropped is named in the guide header AND the chat summary — bounded coverage must never read as complete coverage.
- **Portable — discover, don't hardcode.** Resolve source roots, spec/test locations, run commands, and output dir from `docs/project-config.json`; degrade gracefully and say which rung you landed on.
- **Scale buys MORE STORY GROUPS, never FEWER PARTS per case.** _"Too big to demo properly"_ is a conclusion this skill may never reach.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.**

---

# Demo Guide — Investigate-First, Proof-Carrying Demo Script

You are an **investigator first, a presenter's coach second** — in that order, and the order is the whole point.

- **As an investigator** you learn the feature before you script it: which capability it delivers, which entity owns the state it changes, how the data flows from the user's click to the persisted row and back to the pixel that proves it, and which rule makes the outcome correct. You read the code; you never infer persistence from a name.
- **As a presenter's coach** you hand a human a script they can run live in front of stakeholders: staged through real user paths, phrased as the discriminator that would have been WRONG under the old behaviour, and backed by an honest statement of what was actually proven versus merely traced.

> **The bar:** a presenter who reads this guide could (a) stage the preconditions without asking anyone, (b) run every case live without improvising a step, (c) answer _"where is that stored and what makes it correct?"_ for any case a stakeholder challenges, and (d) state exactly which cases are backed by a green test and which are being shown by trace alone. Anything less is a wish-list, not a demo guide.

Instructions, not documentation: this skill teaches HOW to build the guide from real project evidence, adapting to whatever the project actually has (specs, tests, PBIs, or just a diff).

## Invocation

```
/demo-guide [feature-or-scope] [--context] [--output path] [--lang xx] [--html] [--stories "A,B"]
```

| Flag / arg         | Meaning                                                                                            |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| `feature-or-scope` | Named feature, spec title, PBI/story id, path, or free-text scope. Highest precedence.             |
| `--context`        | Force "derive scope from current working context" (branch diff / staged + unstaged / active work). |
| `--output path`    | Where to write the guide. Default: project demo-guide dir (see Configuration), else a temp file.   |
| `--lang xx`        | Also emit a translated copy in the given language (keep code identifiers/paths/IDs in English).    |
| `--html`           | After the markdown, offer/produce a self-contained HTML runbook (via the Artifact flow).           |
| `--stories "A,B"`  | Restrict to the named stories instead of all main stories.                                         |

## Step 0 — Resolve Scope, Load the Contract, Size & Task (cheap — costs seconds)

**0.1 Resolve scope (prompt → context → ASK).** Apply the precedence strictly — the skill's defining behaviour:

1. **Prompt names a feature/scope** → use it. Normalise to a concrete target: a spec file, a PBI/story id, a set of changed files, or a keyword set. Confirm it resolves to real artifacts before proceeding.
2. **Prompt empty / only "generate demo guide"** → derive from the **current working context**, in this order until one yields signal: active task list / workflow goal → `git status` + `git diff` (staged and unstaged) + branch name → recent commits vs the main branch → any in-progress plan/spec/release-note.
3. **No usable signal** → **STOP and `AskUserQuestion`**: _"Which feature should I generate the demo guide for?"_ Offer the best 2-4 candidates you did find plus free-text. NEVER pick one silently.

State the resolved scope and its source in one line (e.g. `Scope: <feature> — derived from branch diff (7 changed files)`).

**0.2 Load the output contract BEFORE gathering.** Read `references/demo-guide-template.md` — the document structure, the per-case block, the proof rungs, the storage-block field map, and the translation/HTML rules. The shape of the guide decides what you must collect; improvising it from memory guarantees a thin case block. **If the file is missing** (partial distribution, vendored copy, incomplete mirror sync), degrade **out loud, never silently**: say which file is absent in one line and run on the inline contract in this file (Step 6's four mandatory parts, Step 7's proof ladder). The guide is still owed in full; only the elaboration is lost.

**0.3 Size the target into a tier (count, do not estimate).** In-scope **files**, distinct user-facing **capabilities/flows**, distinct **modules/bounded contexts** (`docs/project-config.json` → modules), and **changed lines** where a diff exists. First row whose trigger matches, top-down. Announce it: `Scope: S2 · Multi — 14 files, 3 capabilities → 3 story groups`.

| Tier             | Trigger (first match wins)                             | Story groups        | How the work runs                            |
| ---------------- | ------------------------------------------------------ | ------------------- | -------------------------------------------- |
| **S0 · Point**   | One case, one bug fix, one screen                      | 1                   | Inline, case by case                         |
| **S1 · Small**   | < 10 in-scope files, one capability                    | 1                   | Inline, case by case                         |
| **S2 · Multi**   | ≥ 10 files **OR** ≥ 2 capabilities/flows/contexts      | 2–6                 | Inline, story group by story group           |
| **S3 · Large**   | > 40 files **OR** > 6 story groups                     | 6–12                | One sub-agent per group, front-loaded writes |
| **S4 · Program** | Whole product · multi-service · "demo the whole thing" | Grouped per context | Group agents → context synthesis → spine     |

> Thresholds are the framework's existing map-reduce ladder (`SYNC:systematic-review-batching`: < 10 sequential · ≥ 10 batch · > 6 categories or > 40 files hierarchical) and match `/understand`'s tiers deliberately. — why: a feature that gets understood and then demoed must be partitioned the same way twice, not by two competing maps.

**Tier is a SHAPE dial, not a depth dial.** It changes how many story groups exist and how the work is dispatched. It NEVER removes a case part, a proof rung, or the storage explanation.

**0.4 Decompose into story groups, then task the work — BEFORE any deep read.**

- **A story group is a demoable unit** — one user-facing capability whose cases can be staged in one sitting, ≤ 8 files or ≤ 2000 diff-lines. Decomposition axis, first rung yielding ≥2 cohesive groups: **capability / user story** → **end-to-end flow** → **module / bounded context** → **screen or endpoint cluster** (last resort, labelled _"structural grouping — not a story boundary"_). Record which rung you landed on. Tier S0/S1 → exactly one group.
- **[BLOCKING] Create the task list BEFORE gathering.** `TaskList` FIRST — an interrupted or compacted run **resumes its tasks, never duplicates them**. Then one task per story group plus the fixed tasks: _size & decompose · understand-gate · scope-wide gather · open guide + ledger · {one per group} · proof & transparency · validate_. Exactly one `in_progress`. **A group task completes ONLY when that group's block is on disk** — evidence is the path plus the cases it carries, never a summary in context. — why: a run that dies mid-guide must show exactly where it stopped.

## Step 1 — Understand the Feature FIRST **[BLOCKING GATE]**

**No demo step, no expected result, and no storage claim is written before this gate clears.** Investigation is not a preamble to the guide — it is the thing that makes the guide true.

**The comprehension bar — answer all six with `file:line`, for each story group:**

1. **What capability does this deliver, and what did the system do before it?** The before → after in _behaviour_ terms — this is what the demo's expected result must discriminate against.
2. **Which entity/aggregate owns the state the feature changes, and which field/column/table holds it?** Read the entity, the mapping/configuration, and the migration — not the property name.
3. **What is the end-to-end flow?** Entry point (screen/endpoint/job) → validation → handler/domain rule → persistence → the read path that renders the outcome the presenter will point at.
4. **Which business rule or invariant makes the expected result correct, and where is it enforced?** This is what a stakeholder's _"but what if…"_ attacks.
5. **What preconditions must exist, and which REAL user path stages each?** Roles, configuration, seed data, prior state — every one reachable through actions a user could actually perform.
6. **What proves it?** The REAL `TC-*` / test IDs covering each case, which of them are runnable in this environment, and which cases have none.

**Cannot answer one? Keep investigating — or delegate. NEVER paper over the gap with a plausible-looking step.**

| The gate needs…                                                       | Invoke                                 | Feeds                                         |
| --------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------- |
| Where the feature's files even are, across a large or unfamiliar repo | `/scout`                               | Step 0.4 group decomposition + file lists     |
| How the existing feature actually works, beyond what one read shows   | `/investigate`                         | Bar Q1 · Q3 · Q4 → the storage/solution block |
| Why a fixed defect now behaves differently (bug-fix demo)             | `/debug-investigate`                   | Bar Q1's before → after discriminator         |
| The call/flow chain and which read path renders the outcome           | `/graph-trace` · `/graph-blast-radius` | Bar Q3 · the "where to look" demo step        |
| Which spec owns the capability, when finding it is itself the problem | `/spec-index` · `/spec`                | Bar Q6 → REAL `TC-*` IDs                      |

1. **Read-only delegates ONLY.** NEVER invoke a skill that mutates files or issues findings/verdicts (`/fix`, `/changes-review`, `/code-review`, `/why-review`, `/plan-execute`) — this skill emits a script, not a verdict, and mutates nothing but its own output.
2. **MUST ATTENTION delegate on evidence of need — NEVER by reflex.** Try read + grep + trace first, within the group's budget. Announce each delegation in one line and record it in the guide header: `Delegated: /investigate — Story B mechanics`. — why: the reader calibrates on the provenance chain exactly as on a grep-derived claim.
3. **A delegate's output is INPUT, never a finished block.** Re-verify every claim at `file:line` before it enters the guide; a `TC-*` ID that arrives through a delegate is still one you must have read yourself. The anti-hallucination bar does not relax by passing through another skill.
4. **At tier S3+, delegation happens INSIDE the group's sub-agent**, never in the orchestrator. — why: delegating from the orchestrator pulls a whole investigation transcript into the one context the grouping exists to protect.

**Gate exit — write the Understanding Brief to disk before Step 2 ends:** per story group, the six answers with their `file:line` anchors, the delegations used, and any question you could NOT answer (named as a blocker, never left blank). This brief is what Steps 4, 6 and 7 are written from — never memory.

## Step 2 — Gather the Five Inventories (portable discovery)

Read `docs/project-config.json` (and the project-reference docs it points to) to locate — do NOT hardcode: **source roots** (entities, handlers, migrations, models), **spec / feature-doc location** (canonical stories, ACs, `TC-*` IDs), **test locations** (integration/unit/e2e — the ground truth of "what is proven"), **release-notes / changelog / PBI-story** dirs, and **run/test commands**. This skill runs on repos it has never seen; a hardcoded framework path is a guess wearing a citation.

Each inventory walks its ladder top-down and **records the rung it landed on** — the reader calibrates on it. **Every ladder ends in a stated blocker; none has a rung of invention.**

1. **Story & test-case inventory** (feeds the story map, §Quick-reference). The main user-facing capabilities in scope, each as _As a … I want … so that …_, plus the REAL cases proving each — spec `TC-*` IDs and/or the integration/unit/e2e `it` / `[Fact]` / scenario names. Reconcile the union of spec TCs and test-code cases. _Ladder:_ specs → tests → PBIs/release notes/commit messages → the diff itself → **state that no story source exists**.
2. **Domain storage & solution inventory** (feeds each case's fourth part). Per case: the persisted field/column/table, the owning entity/value object, the migration that added or altered it, the value actually written (anchored/computed), and the rule/method/invariant that consumes it. _Ladder:_ entity + mapping + migration read → graph trace of the writer/reader → schema dump → **state the blocker**.
3. **Demo path & setup inventory** (feeds setup/preconditions and the numbered steps). The real user path to each precondition: roles/permissions, configuration flags, seed or fixture entry points, which app/screen/endpoint, and what input. _Ladder:_ existing seeders/fixtures → e2e test setup → manual path traced through the UI/API code → **state that the precondition cannot be staged**.
4. **Proof inventory** (feeds the proof rung per case). Which suites/cases exist, which are runnable here (resolve the command — never guess it), and what a run actually returned this session. _Ladder:_ `project-config.json` commands → the CI workflow's own commands → the test-runner manifest (`package.json` scripts, `*.csproj`, `Makefile`) → **state that no command could be resolved**.
5. **Discriminator inventory** (feeds every expected result). Per case, the value/state that would have been WRONG under the old behaviour — from the diff, the fixed defect, the spec's AC, or the test's assertion. _Ladder:_ the test assertion → the diff's before/after → the spec AC → **state that the discriminator is unknown** rather than writing "it succeeds".

> **[SECURITY]** Record every command, credential, and account in **placeholder form** at the moment of collection — not at write time. Environment variables, connection strings, tokens, keys, passwords, and customer identifiers are referenced by NAME and rendered `<redacted:…>`; demo accounts are named by **role** (`<demo user: approver>`), never by real login. This is the point where a secret would first enter context, so it is the point that must refuse it.

> When `.code-graph/graph.db` exists, run `python .claude/scripts/code_graph trace <entity-or-handler> --direction both --json` to map how a stored field flows to the reader that solves the case — this is how the "how the domain solves the feature" claim is backed by structure instead of guesswork.

## Step 3 — Map Stories → Cases (persist the map)

- **Main user story** = a user-facing capability/outcome the feature delivers. Prefer the spec's stories; else synthesise one per distinct capability from ACs/tests. Keep to the _main_ stories — group minor variants under the case list, don't inflate the count.
- **Cases per story** = the real cases that prove it. Use the **ACTUAL IDs** — NEVER invent case numbers. A story with no case is a **coverage gap to report**, never a gap to fill with a plausible ID.

Write the story → case map to disk before writing any case block, and cross-check it against the full changed-file list so no main area is missed. — why: the map is the coverage contract; held only in context it is one cutoff from gone.

## Step 4 — Trace Domain Storage & Solution (the distinctive step)

For **each main case**, open the owning code and answer both questions with `file:line` evidence:

- **How is the domain data stored or changed?** The persisted field(s)/column(s)/table, the value object or entity that owns it, the migration that added/altered it, the anchored/computed value actually written, and whether the change is additive/nullable/backfilled. Read the entity, the DTO mapping, and the migration — NEVER infer persistence from names.
- **How does the domain solve the feature?** The rule/method/invariant that consumes that stored data to produce the demoed outcome (resolver/derivation/gate), and why storing it this way makes the case correct — edge cases, legacy fallback, cross-tier parity.

A display-only case with no persistence change says so **explicitly** and describes the **representation** that solves it instead (what value/shape is computed and why it is correct). _"No storage change"_ is a valid and important answer for a demo — an empty block is not.

## Step 5 — Open the Guide + Ledger, Accumulate Story by Story

**Create the guide file BEFORE writing case one**, then append as you produce it. Never hold the whole guide in context and write once at the end.

**Write order is fixed:** header FIRST — scope + source, sources used, delegations, tier + group count, and the **group ledger** with every row `pending` → then group by group (trace → write that group's cases → update its ledger row to `written` with its case count → complete that task) → then the guide-level sections (storage summary, quick-reference table, transparency note) **from the written blocks** → then the chat summary. NEVER hold more than the current group in context; read a finished block back from disk when you need it again.

**After a cutoff, compaction, or resume:** `TaskList` → read the ledger → **verify every `written` row against the filesystem** (the file exists AND carries its cases; an absent or truncated block resets to `pending`) → re-read the contract and the Understanding Brief → continue at the first unfinished group. NEVER restart a finished group and never re-derive a written block from memory.

> **[NO SILENT TRUNCATION]** If any cap, budget, or interruption leaves part of the resolved scope uncovered, name what was deferred or dropped **in the guide header AND in the chat summary** — _"Story D (bulk import, 9 cases) deferred — not covered by this guide."_ — why: bounded coverage that reads as complete coverage sends a presenter into a room unprepared for the question nobody examined.

**Write location — the demo guide is a DELIVERABLE, not a working artifact.** It is written to the project's demo-guide dir (Configuration below) and is meant to be shared and version-controlled. **This is a deliberate divergence from `/understand`, whose report is a git-ignored working artifact** — do NOT copy that skill's git-ignored-only rule here. — why: a demo script the team cannot find in the repo is a demo script nobody uses.

## Step 6 — Write Each Case (four mandatory parts)

Follow `references/demo-guide-template.md`. Per **main case** the guide MUST contain:

1. **Setup / preconditions** — the exact state to stage before demoing (roles, configuration, seed data, which app/screen), staged through **real user paths** — never by faking state a user could not reach. Secrets as `<redacted:…>`, accounts by role.
2. **Step-by-step demo flow** — numbered, concrete, click-/action-level steps a presenter follows live: who acts, on which screen/endpoint, with what input, and where to look. A step you cannot trace to a real user path is a **stated blocker**, never an invented click.
3. **Expected result** — the observable outcome phrased as **the discriminator**: the value that would have been WRONG under the old behaviour, not a generic "it succeeds".
4. **How the domain stores/changes data + solves it** — the Step-4 explanation in plain team language, keeping the `file:line` anchors for credibility.

Also include: the scope/source header, per-story grouping, the **main test-case quick-reference table** (ID · what it proves · proof rung), the **domain storage summary** per story, and the **test-execution transparency note**. Keep prose tight (output-quality principles).

`--lang` given → emit a translated copy (prose translated; code identifiers, `file:line`, `TC-*` IDs, and numeric values kept verbatim). `--html` given → follow the Artifact flow to render a self-contained runbook **after** the markdown is approved.

## Step 7 — Prove (the proof ladder)

Every case sits on exactly one rung. State it per case AND in the quick-reference table.

| Rung                | Means                                                                 | Licence                                                             |
| ------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `✅ ran`            | The test was **executed this session**                                | The ONLY rung that may claim green. Record the command + pass/fail. |
| `⚠️ trace-verified` | Code read end-to-end, the `file:line` chain is complete, not executed | Demo it live; say it was not run.                                   |
| `📄 spec-only`      | Asserted by a spec/TC; the code path was not traced                   | Weakest rung — say so explicitly.                                   |
| `❌ no coverage`    | No test exists for this case                                          | A reported gap. NEVER filled with a plausible ID.                   |

**There is no fifth rung.** A case you cannot place on one of these four is a **stated blocker**, not a case you quietly promote.

**Proof chain per case** — the `file:line` links a challenger can walk: **where the value is written** → **where it is read** → **where the presenter sees it**. A case whose chain has a missing link cannot sit above `📄 spec-only`.

**Transparency note (mandatory, at the end of the guide):** what was proven this session (suites/cases executed + pass/fail counts), what was not and why (runner blocker, environment, no coverage), and which cases are therefore being shown live rather than via a green run. NEVER imply a run that did not happen.

## Step 8 — Validate

Before declaring done, verify each — evidence, not assertion:

- **MUST ATTENTION** the resolved scope and its source (prompt / context / user-confirmed) are recorded in the guide header.
- **MUST ATTENTION** the Step 1 comprehension bar was cleared per story group, with `file:line` per answer, and the Understanding Brief is on disk.
- **MUST ATTENTION** every main user story is present, each with its REAL test-case IDs — **no invented numbers** — and every story with no case is named as a coverage gap.
- **MUST ATTENTION** every case has all four parts: setup · numbered demo flow · expected result as the discriminator · domain storage/solution.
- **MUST ATTENTION** every storage/behaviour claim cites `file:line` from a read entity/migration/handler — nothing inferred from a name.
- **MUST ATTENTION** every case carries a proof rung and a proof chain; `✅ ran` appears only where a command was executed and recorded.
- **MUST ATTENTION** no secret value appears anywhere — settings, files, and account roles named; credentials rendered `<redacted:…>`.
- **MUST ATTENTION** anything deferred, sampled, or dropped is named in the guide header AND the chat summary.
- **MUST ATTENTION** the ledger's `written` rows are verified against the filesystem, and the output landed at the resolved path; translation/HTML produced only if requested.

## Configuration

Resolve everything project-specific from `docs/project-config.json`; an optional block overrides demo-guide defaults:

```json
{
    "demoGuide": {
        "outputDir": "docs/demo-guides",
        "specDir": "docs/specs",
        "translateDefaultLang": null,
        "storyGranularity": "main"
    }
}
```

Block or file absent → degrade gracefully: default `outputDir` to the project's docs/demo dir if one exists, else a temp file; discover spec/test/source locations from the project-reference docs; and **state the fallbacks you used**.

## Integration with Other Skills

- **`/understand`** — reuse its Purpose→How→Why framing for the "how the domain solves the feature" explanation. ⚠️ **Boundary — decide by audience, not by overlap:** `/understand` §11 _Test & Demo_ is **reviewer-facing** — how to run and see the change you are about to review, scoped to that change. This skill is **presenter-facing** — a standalone, stakeholder-ready script that walks a room through a whole feature. The per-case block is deliberately the same shape in both so they converge instead of drifting; showing finished work to people → here, preparing to review it → `/understand`.
- **`/investigate`** / **`/scout`** / **`/debug-investigate`** / **`/graph-trace`** — the Step 1 gate's read-only gather delegates. Their output is INPUT, re-verified at `file:line`; they never author a case block.
- **`/spec`** — the canonical source of user stories + `TC-*` IDs when the project maintains feature specs. **A business `TC-*` and a demo case are the SAME event for two audiences** — the spec states it as intent, this guide stages it for a room. So they converge by construction: reuse the TC's demo flow and expected result rather than re-deriving them, and **cite the `TC-*` ID per case** so the two cannot drift apart. ⚠️ **A `TC-*` you cannot stage as a live demo is a finding, not a formatting problem** — it means a non-demoable (technical) case reached the business spec, which violates **M7**. Report it; do NOT invent a demo to cover for it.
- **`/release-doc`** / **`/changelog`** — sibling generators; `demo-guide` is presenter-facing (how to show it), they are change-facing (what changed).
- **`/commit`** — commit the generated guide when the user wants it version-controlled.

---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — one per story group (understand → trace → write) so a long feature can't overflow context. Persist the Understanding Brief and the story→case map early; NEVER hold them only in memory.

**IMPORTANT MANDATORY Steps:** resolve-scope-load-contract-size-and-task-first -> understand-the-feature-blocking-gate-six-question-bar -> gather-five-inventories-with-ladders -> map-stories-to-real-case-ids -> trace-domain-storage-and-solution -> open-guide-and-ledger-accumulate-story-by-story -> write-each-case-four-parts -> place-every-case-on-the-proof-ladder -> validate

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.**

<!-- SYNC:understand-code-first -->

> **Understand Code First** — HARD-GATE: Do NOT write, plan, or fix until you READ existing code.
>
> 1. Search 3+ similar patterns (`grep`/`glob`) — cite `file:line` evidence
> 2. Read existing files in target area — understand structure, base classes, conventions
> 3. Run `python .claude/scripts/code_graph trace <file> --direction both --json` when `.code-graph/graph.db` exists
> 4. Map dependencies via `connections` or `callers_of` — know what depends on your target
> 5. Write investigation to `.ai/workspace/analysis/` for non-trivial tasks (3+ files)
> 6. Re-read analysis file before implementing — never work from memory alone. — why: long context drifts from the file; the file is ground truth
> 7. NEVER invent new patterns when existing ones work — match exactly or document deviation. — why: divergent patterns fragment the codebase and slow every future reader
>
> **BLOCKED until:** `- [ ]` Read target files `- [ ]` Grep 3+ patterns `- [ ]` Graph trace (if graph.db exists) `- [ ]` Assumptions verified with evidence

<!-- /SYNC:understand-code-first -->

<!-- SYNC:evidence-based-reasoning -->

> **Evidence-Based Reasoning** — Speculation is FORBIDDEN. Every claim needs proof.
>
> 1. Cite `file:line`, grep results, or framework docs for EVERY claim
> 2. Declare confidence: >80% act freely, 60-80% verify first, <60% DO NOT recommend
> 3. Cross-service validation required for architectural changes
> 4. "I don't have enough evidence" is valid and expected output
>
> **BLOCKED until:** `- [ ]` Evidence file path (`file:line`) `- [ ]` Grep search performed `- [ ]` 3+ similar patterns found `- [ ]` Confidence level stated
>
> **Forbidden without proof:** "obviously", "I think", "should be", "probably", "this is because"
> **If incomplete →** output: `"Insufficient evidence. Verified: [...]. Not verified: [...]."`

<!-- /SYNC:evidence-based-reasoning -->

<!-- SYNC:graph-assisted-investigation -->

> **Graph-Assisted Investigation** — MANDATORY when `.code-graph/graph.db` exists.
>
> **HARD-GATE:** MUST ATTENTION run at least ONE graph command on key files before concluding any investigation.
>
> **Pattern:** Grep finds files → `trace --direction both` reveals full system flow → Grep verifies details
>
> | Task                | Minimum Graph Action                         |
> | ------------------- | -------------------------------------------- |
> | Investigation/Scout | `trace --direction both` on 2-3 entry files  |
> | Fix/Debug           | `callers_of` on buggy function + `tests_for` |
> | Feature/Enhancement | `connections` on files to be modified        |
> | Code Review         | `tests_for` on changed functions             |
> | Blast Radius        | `trace --direction downstream`               |
>
> **CLI:** `python .claude/scripts/code_graph {command} --json`. Use `--node-mode file` first (10-30x less noise), then `--node-mode function` for detail.

<!-- /SYNC:graph-assisted-investigation -->

<!-- SYNC:incremental-persistence -->

> **Incremental Result Persistence** — MANDATORY for all sub-agents or heavy inline steps processing >3 files.
>
> 1. **Before starting:** Create report file `plans/reports/{skill}-{date}-{slug}.md`
> 2. **After each file/section reviewed:** Append findings to report immediately — never hold in memory
> 3. **Return to main agent:** Summary only (per SYNC:subagent-return-contract) with `Full report:` path
> 4. **Main agent:** Reads report file only when resolving specific blockers
>
> **Why:** Context cutoff mid-execution loses ALL in-memory findings. Each disk write survives compaction. Partial results are better than no results.
>
> **Report naming:** `plans/reports/{skill-name}-{YYMMDD}-{HHmm}-{slug}.md`

<!-- /SYNC:incremental-persistence -->

<!-- SYNC:output-quality-principles -->

> **Output Quality** — Token efficiency without sacrificing quality.
>
> 1. No inventories/counts — AI can `grep | wc -l`. Counts go stale instantly
> 2. No directory trees — AI can `glob`/`ls`. Use 1-line path conventions
> 3. No TOCs — AI reads linearly. TOC wastes tokens
> 4. No examples that repeat what rules say — one example only if non-obvious
> 5. Lead with answer, not reasoning. Skip filler words and preamble
> 6. Sacrifice grammar for concision in reports
> 7. Unresolved questions at end, if any

<!-- /SYNC:output-quality-principles -->

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:ai-mistake-prevention -->

> **AI Mistake Prevention** — Failure modes to avoid on every task:
>
> **Re-read files after context changes.** Context compaction, resume, or long-running work can make memory stale; verify current files before acting.
> **Verify generated content against source evidence.** AI hallucinates APIs, names, claims, and document facts. Check the relevant source before documenting or referencing.
> **Check downstream references before deleting or renaming.** Removing an artifact can stale docs, generated mirrors, configs, and callers; map references first.
> **Trace the full impact chain after edits.** Changing a definition can miss derived outputs and consumers. Follow the affected chain before declaring done.
> **Verify ALL affected outputs, not just the first.** One green check is not all green checks; validate every output surface the change can affect.
> **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Before changing or reporting a constant, limit, flag, cutoff, wording, or pattern, read nearby context and history, the CALLER's ordering, and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard.
> **Surface ambiguity before acting — don't pick silently.** Multiple valid interpretations require an explicit question or stated assumption with risk.
> **Assert the outcome your system owns, not the intermediate state your infrastructure owns.** When verifying async work, assert the final business state — never the delivery/retry bookkeeping held in shared infrastructure that any co-running process can write. Such a check passes when run alone and flakes the moment anything else shares that infrastructure.
> **Keep shared guidance role-relevant.** Universal guidance must help every receiving skill or agent; code-specific obligations belong only in code-specific protocols.

<!-- /SYNC:ai-mistake-prevention -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim (confidence >80% to act). NEVER speculate without proof.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:understand-code-first:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code BEFORE any explanation. Run graph trace when graph.db exists.
  <!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

- **MANDATORY IMPORTANT MUST ATTENTION** run at least ONE graph command on key files when graph.db exists. Pattern: grep → graph trace → grep verify.
  <!-- /SYNC:graph-assisted-investigation:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- SYNC:output-quality-principles:reminder -->

**IMPORTANT MUST ATTENTION** follow output quality principles: token efficiency, lead with answer, no filler.

<!-- /SYNC:output-quality-principles:reminder -->

<!-- SYNC:parallel-subagent-dispatch -->

> **Parallel Sub-Agent Dispatch** — Plan parallelism the moment a task breakdown exists, BEFORE executing it — running provably independent tasks sequentially wastes wall-clock. Applies to every multi-step job: workflow steps, planning, batch updates, investigation, research, scans, reviews, doc sync. **Plan execution is metadata-gated, NEVER default-parallel** — fan-out follows ONLY what the plan declares (`PAR`/`SEQ` tags + per-phase write set); an untagged plan runs sequentially — why: a derived write set cannot see cascade or generated writes.
>
> 1. **Tag every task `PAR` or `SEQ`.** `PAR` = inputs exclude every pending task's output AND write set disjoint from every other `PAR`. Else `SEQ` — MUST ATTENTION name the dependency forcing it.
> 2. **Group `PAR` into waves.** No edge between members. Two writers of one file NEVER share a wave. Read-only work (search, investigation, review, research) parallelizes freely.
> 3. **Declare before dispatch:** `Parallel plan: wave 1 = [...] · wave 2 = [...] · SEQ = [...] (reason)`.
> 4. **Spawn each wave in ONE message** — every `Agent` call in one response, NEVER dripped per turn. Route each task to its specialist (`.claude/skills/shared/sub-agent-selection-guide.md`); NEVER `code-reviewer` as catch-all.
> 5. **Brief each sub-agent self-contained:** goal · scope + owned files · reference docs · return contract (summary + `Full report:` path, per SYNC:subagent-return-contract) · incremental persistence to `plans/reports/` (per SYNC:incremental-persistence).
> 6. **Barrier per wave.** Advance ONLY after EVERY member returns (a skipped conditional counts as returned). Merge, mark each task completed/skipped, THEN dispatch the next wave. Mutating steps wait for the barrier.
> 7. **One level deep.** A dispatched sub-agent executes its own brief; further fan-out stays the orchestrator's job unless that agent's `.claude/agents/*.md` definition authorizes it.
>
> **NEVER parallelize:** tasks sharing a write target · a task consuming a pending task's output · trivial single-file work (dispatch overhead > gain) · an order a skill or workflow explicitly fixes · gates awaiting user approval.
>
> **Blocked until:** MUST ATTENTION every task tagged PAR/SEQ with a named reason per SEQ · waves declared + write-set disjointness checked · each wave spawned in ONE message · barrier honored before the next wave.

<!-- /SYNC:parallel-subagent-dispatch -->

<!-- SYNC:parallel-subagent-dispatch:reminder -->

- **MANDATORY** After planning tasks, tag each PAR/SEQ and spawn every PAR wave as parallel sub-agents in ONE message — default parallel for workflows, batch updates, investigation, research, reviews; plan execution fans out ONLY on what the plan declares.
- **MANDATORY** Disjoint write sets per wave · all-return barrier before the next wave · specialist routing · sub-agents NEVER fan out further unless their own agent definition authorizes it.
  <!-- /SYNC:parallel-subagent-dispatch:reminder -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** UNDERSTAND the feature first, then script it — investigate until the comprehension bar is cleared with `file:line`, then produce a demo guide listing every main user story with its REAL test-case IDs, a step-by-step demo flow per case, how the domain stores/changes the data and solves the feature, and a proof rung per case — so the presenter shows the behaviour, explains the data behind it, and never claims proof that was not earned.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries) — MUST ATTENTION each:**

- **Understand Code First:** read the entity/migration/handler before explaining storage — NEVER infer persistence.
- **Evidence-Based Reasoning:** every storage/behaviour claim cites `file:line`; state confidence; "insufficient evidence" is valid output.
- **Graph-Assisted Investigation:** run a graph command on key files when `graph.db` exists — grep → trace → grep verify.
- **Incremental Persistence:** create the guide file BEFORE case one; append per case and per story group; NEVER hold results in memory.
- **Output Quality:** token efficiency, lead with the answer, no filler.
- **Critical Thinking:** traced proof per claim, confidence >80% to act, NEVER guess.
- **AI Mistake Prevention:** verify against evidence, re-read after context loss, surface ambiguity.

- **MUST ATTENTION** run the main steps in order, none skipped: (0) Resolve scope + load contract + size + task → (1) **UNDERSTAND the feature [BLOCKING gate]** → (2) Gather five inventories → (3) Map stories → REAL case IDs → (4) Trace domain storage/solution → (5) Open guide + ledger and accumulate → (6) Write each case's four parts → (7) Place every case on the proof ladder → (8) Validate.
- **MUST ATTENTION** Step 1 is a **[BLOCKING] gate, not a preamble** — until all six comprehension questions are answered with `file:line` per story group, NO demo step, expected result, or storage claim may be written. Unanswerable question → keep investigating, delegate, or **state it as a blocker**; NEVER paper over it with a plausible step.
- **MUST ATTENTION** scope precedence is **prompt → current context → ASK** — NEVER silently invent the feature.
- **MUST ATTENTION** DELEGATE the GATHERING to read-only skills (`/scout`, `/investigate`, `/debug-investigate`, `/graph-trace`, `/spec-index`) when read + grep + trace cannot clear the bar — NEVER to a mutating or findings-emitting skill, never let a delegate author a case block, and re-verify every delegated claim at `file:line` first. At S3+ delegation runs inside the group's sub-agent, not the orchestrator.
- **MUST ATTENTION** SIZE the target into a tier (S0–S4) and DECOMPOSE anything above S1 into story groups (≤8 files / ≤2000 diff-lines, each demoable in one sitting) — announce both in one line. Scale buys MORE GROUPS, never FEWER PARTS per case; _"too big to demo properly"_ is a conclusion this skill may never reach.
- **MUST ATTENTION** BREAK THE WORK INTO TASKS **before the first deep read** — `TaskList` first (resume, never duplicate), one task per story group plus the fixed tasks, exactly one `in_progress`, and a group task `completed` ONLY when its block is on disk.
- **MUST ATTENTION** OPEN the guide — header, ledger, group rows — before case one, ACCUMULATE story group by story group, and write the guide-level sections **from the written blocks**, never from memory. After any cutoff or compaction, verify every `written` ledger row against the filesystem before continuing.
- **MUST ATTENTION** every main case = setup/preconditions + numbered **step-by-step demo flow** + **expected result phrased as the discriminator** + **how the domain stores/changes data & solves the feature**. A case missing the storage/solution part is incomplete; a display-only case states _"no storage change"_ and describes the computed representation.
- **MUST ATTENTION** PROOF IS EARNED: every case sits on one of four rungs — `✅ ran` (executed THIS session, command + result recorded) · `⚠️ trace-verified` · `📄 spec-only` · `❌ no coverage` — plus a proof chain (written → read → seen, `file:line` each). **There is no fifth rung**; an unplaceable case is a stated blocker. NEVER imply a green run that did not happen.
- **MUST ATTENTION** use the project's REAL user stories and `TC-*` / test IDs — **NEVER invent a case number**. No coverage → say so; an admitted gap is a finding, a fabricated ID retires a live risk.
- **MUST ATTENTION** stage every precondition through a REAL user path and trace every demo step to real code — an untraceable step is a **stated blocker**, never an invented click, endpoint, or faked state.
- **MUST ATTENTION** cite `file:line` for every storage/behaviour claim from a read entity/mapping/migration/handler — NEVER infer persistence from a field name.
- **MUST ATTENTION** NEVER put a secret value in the guide, the setup steps, or the chat summary — name the setting, the file, and the account **role**; credentials, tokens, keys, connection strings, and customer identifiers render `<redacted:…>` from the moment they would enter context.
- **MUST ATTENTION** announce anything deferred, sampled, or dropped in BOTH the guide header and the chat summary — bounded coverage must never read as complete coverage.
- **MUST ATTENTION** stay portable — discover paths, spec/test locations, and run commands via `docs/project-config.json`; NEVER hardcode project specifics, and state which degradation rung you landed on.
- **MUST ATTENTION** the demo guide is a **shareable DELIVERABLE** written to the project's demo-guide dir — do NOT copy `/understand`'s git-ignored-working-artifact rule onto it.
- **MUST ATTENTION** break work into small todo tasks using `TaskCreate` BEFORE starting.

**Anti-Rationalization:**

| Evasion                                                       | Rebuttal                                                                                                                                        |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| "I know what this feature does — skip the understand gate"    | Then clearing the bar costs minutes. **You cannot skip it.** A demo written from an assumed flow fails live, in front of the room it was for.   |
| "The field name says what it stores"                          | A name is a hypothesis. Read the entity, the mapping, and the migration — persistence is never inferred.                                        |
| "This story probably has a test — I'll cite TC-042"           | NEVER invent a case ID. Cite the ID you actually read, or write "no test covers this case" and record the gap.                                  |
| "The suite is green on CI, so mark it ✅ ran"                 | `✅ ran` means executed THIS session with the command and result recorded. Anything else is `⚠️ trace-verified`.                                |
| "I'll write a reasonable-looking click path"                  | An untraceable step is a **stated blocker**. A presenter who follows an invented step discovers it live.                                        |
| "Expected result: it works"                                   | Failed section. State the discriminator — the value that would have been WRONG under the old behaviour.                                         |
| "Display-only case — nothing to say about storage"            | Say _"no storage change"_ and describe the computed representation that solves it. An empty block is a dropped part.                            |
| "Big feature — a high-level walkthrough IS the honest answer" | Wrong lever. Scale buys MORE STORY GROUPS, never fewer parts per case. Size it, decompose it, task it, accumulate it.                           |
| "I'll investigate everything first, then write the guide"     | Never. Header + ledger before case one, a block per group, ledger updated as each lands. Investigation held in context is one cutoff from gone. |
| "The sub-agent reported it wrote the block"                   | Verify the FILE. A summary is evidence of a reply, never of a block — check it exists, carries its cases, and cites REAL IDs.                   |
| "I'll call /changes-review to gather faster"                  | Delegates are READ-ONLY and gather-only. This skill emits a script, not findings — never delegate to a mutating or verdict-issuing skill.       |
| "The demo needs the admin password to be runnable"            | Name the role and the setting; render the value `<redacted:…>`. A guide is shared — a credential in it is a leak.                               |
| "Most stories are covered — close enough"                     | Name every deferred story in the header AND the chat summary. Bounded coverage that reads as complete is how a presenter gets ambushed.         |

**[TASK-PLANNING]** Before acting, analyze task scope and systematically break it into small todo tasks and sub-tasks using TaskCreate.
