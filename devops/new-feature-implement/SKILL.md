---
name: new-feature-implement
description: Implements one already-approved UC-NNN-spec.md — one-time setup pre-flight, then java-spring-boot-developer in three chained block groups, then git-publish. The second half of the feature pipeline; /new-feature designs the spec
disable-model-invocation: true
argument-hint: "UC-NNN-slug of an approved case | empty to list"
model: sonnet
---

# `/new-feature-implement` — Feature implement orchestrator

## Why this is Form 2 (manual skill)

Axis 2 (manual trigger) + axis 5 (procedural) + axis 8 (both). It was input row 3 of
`/new-feature` until the two flows of the pipeline became two pieces: an implement run loaded
the whole design procedure — about 10k tokens of steps 1–6 and consolidation it never runs — on
every main-thread turn, and it ran on the `opus` the design needs. A subagent was rejected: the
executor is already the isolated part, and this thread only chains it
(`@.claude/decisions/0135-new-feature-split-spec-and-implement.md`).

**Manual only.** `disable-model-invocation: true` hides this skill from the model: the
`Skill` tool can't call it, and trying is blocked. When a conversation reaches the point
of running it, print the exact command for the user to type — don't attempt the call.

---

Pinned to `sonnet`: this thread runs a detection, chains three `Agent` calls and copies their
findings — no design. The executor declares its own model
(`@.claude/decisions/0081-skill-model-required-per-class.md`). A skill's `model` holds for the
turn it runs in; a background executor's hand-back opens a new turn, which may run on the
session's model — measured in the run's audit report, not assumed.

## Contract

**Class:** orchestrator — `skill_classes.orchestrator` in `@.claude/schemas/extensions.json`,
with `overrides.new-feature-implement.write_allow: []`: this thread writes nothing. Every write
of a run is a subagent's, judged by its own `agent_classes` entry — the executor's and the
installers' — never by this phase (`@.claude/decisions/0059-agent-classes-territory-schema.md`).
The class keeps `design_phase: true`, so `ArchHook.java guard` refuses a `Skill` call to a
`build`-class skill while the run is open.

**Ownership:** Feature spec→code orchestrator. Owns the pre-flight, the group chain, the
hand-off between groups, and the `git-publish` offer of an implemented case. Does **not** own
the spec — `/new-feature` writes it and its `status:` up to `approved`;
`java-spring-boot-developer` writes `implemented` or `implemented-blocked`
(`@.claude/skills/new-feature/SKILL.md` § Spec lifecycle).

**Reads:**
- `@.claude/skills/new-feature/references/entry-guardrail.md` — survey, classification, error
  rule, worktree, project, disk; shared with `/new-feature`, owned there
- `docs/use-cases/UC-*/` — folder existence and each spec's `status:` line, by command
- `docs/use-cases/UC-NNN-<slug>/UC-NNN-spec.md` — the checklist, to find where the chain starts,
  and `## Infrastructure`, for the services the run adds and reports
- `@.claude/skills/docker-architect/references/compose-service-decision.md` — what each
  `## Infrastructure` decision means, and who acts on it
- `src/test/**`, the `commons` package, the root `CLAUDE.md`'s `**Mappers:` paragraph — by
  command, for the pre-flight

**Writes (indirectly):**
- `src/**`, `pom.xml` and the spec's checklist and `status:` — via `java-spring-boot-developer`
- the ArchUnit tests and coverage gate — via `test-architect` setup mode → `archunit-installer`
- the logging/masking classes — via `commons-logging-installer`, from this skill's
  `templates/commons/*.example`
- the project's mapper mechanism — the `**Mappers:` paragraph, and for MapStruct the build wiring
  and every converted mapper — via `mapstruct-installer`, from this skill's
  `templates/mapstruct/*.example`
- `docker-compose.yml` and what a service needs next to it — via `compose-service-installer`,
  which runs `docker-architect` for every `materialize` row of the spec

**Writes (directly): none.**

**Never runs `git add`, `git commit`, or `git push`.** Git happens only through `git-publish`,
behind its two confirmations. No end of this flow is left without an explicit git instruction.

**Integrates with:**
1. `test-architect` (setup mode), `commons-logging-installer` and `mapstruct-installer` —
   pre-flight, each only when its gap is found; the first two when the user answers **Install
   now**, the third with whichever mechanism the user picks
2. `java-spring-boot-developer` — three chained delegations, one per block group
3. `compose-service-installer` — on success, only when the spec has a `materialize` row
4. `git-publish` — on success

---

## Procedure

### 1 · Entry guardrail

Runs before any skill invocation, any delegation, and any question. **Read
`@.claude/skills/new-feature/references/entry-guardrail.md`** and run its § 1 (survey and
classify), then evaluate this table in order and **stop at the first row that matches**:

| # | Input | Result |
|---|---|---|
| 1 | empty | ✅ list the survey — each case with its `status` — and stop |
| 2 | `EXACT`, `FOLDER`, status `approved` | ✅ implement: § 2 onwards. The argument is the request; nothing is asked before the pre-flight |
| 3 | `EXACT`, `FOLDER`, status `draft` or `(no spec)` | ❌ `<UC-NNN-slug> is <status> — design and approve it first` — plus `/new-feature <UC-NNN-slug>` |
| 4 | `EXACT`, `FOLDER`, status `implemented` or `implemented-blocked` | ❌ `already implemented — describe the change as a new feature` — plus `/new-feature <description>` |
| 5 | no `FOLDER`, and the argument's `UC-NNN` resolves to **exactly one** folder on disk | ❌ `<UC-NNN> is <real-slug>, status <status>` — plus the exact command for that status: `/new-feature-implement <real-slug>` when approved, `/new-feature <real-slug>` when open |
| 6 | `EXACT`, no `FOLDER`, number resolving to zero or several folders | ❌ `use case not found` |
| 7 | `UC_LIKE` but not `EXACT` (slug plus context, malformed slug, two slugs, a path) | ❌ `ambiguous argument` |
| 8 | free text | ❌ `this skill implements an approved case; to design one, /new-feature <description>` |
| — | anything else | ❌ `unrecognized argument` |

Every error follows the rule of the reference's § 1 — fixed shape, ends the run, no side
effect:

```text
❌ /new-feature-implement: <reason>.
Usage: /new-feature-implement UC-NNN-slug    → implement an approved case
       /new-feature-implement                → list
       /new-feature <feature description>    → design a new case
```

Row 8 exists because free text is what `/new-feature` takes: a description typed here was meant
there, and running the design from this skill would load the body this split exists to keep out.

Then the reference's §§ 2–4 (worktree, project, disk), in that order. `IGNORED` and the list of
pre-existing changes travel to `git-publish` at the end of the run.

### 2 · Implement

1. **One-time setup pre-flight, before delegating.** The executor is about to write the
   first `.java` under `src/` for this project run — the only point in the pipeline
   where "is the one-time infrastructure installed yet" actually matters. Detect what's
   missing, don't assume:

   ```bash
   grep -rl "ArchRule\|ArchTest" --include='*.java' src/test/ 2>/dev/null | head -1
   find . -type d -iname commons -o -type d -path '*shared/logging' 2>/dev/null
   grep -n '^\*\*Mappers:' CLAUDE.md 2>/dev/null
   ```

   First command empty → ArchUnit not installed yet (the same gap `/new-feature`'s
   consolidation step 3 already flagged, if this use case is the first one). Second command
   empty, or the directory it finds has nothing but `package-info.java` → commons-logging
   classes not installed yet. Third command empty → the project never chose its mapper
   mechanism (`.claude/rules/mapping.md` § One mechanism per project). Any gap found →
   `AskUserQuestion`, one question per gap found: **Install now** / **Skip for this run** for
   the first two; for the mappers, **Keep manual mappers** (recorded, never asked again) /
   **Install MapStruct** (converts every existing mapper; needs a clean `src/`).
   - ArchUnit, install now → **invoke** `test-architect` via the `Skill` tool with **no
     argument at all** (setup mode) — the route `/new-feature`'s consolidation step 3
     names; never invoke `archunit-installer` directly, it stays `test-architect`'s alone.
   - Commons-logging, install now → **invoke** `commons-logging-installer` directly via
     the `Agent` tool. No owning per-feature skill to route through: this orchestrator
     is the trigger, same as it owns `git-publish`'s invocation.
   - Mappers, either answer → **invoke** `mapstruct-installer` directly via the `Agent` tool,
     with the mode — `manual` or `install` — and the project root. It writes the
     `**Mappers:` paragraph either way, so the question is never asked twice. **When its mode is
     `install`, run it first and alone, and wait for it before the other two**: it refuses a
     source tree with uncommitted changes — so `git restore` can undo its conversion — and the
     other two installers write under `src/`. When the worktree check already listed
     pre-existing changes under `src/` or in a build file, don't invoke it: say why, and the
     executor writes manual mappers this run — the next run asks again, and an install then
     converts them with the rest. A failure it reports (dirty `src/`, red baseline, red after conversion) leaves
     no paragraph: say so, show its one line, and proceed to the executor with the manual
     mechanism for this run — the next run asks again.
   - **Both gaps found and both answered "Install now" → either order works, and the
     same turn is fine.** This used to be the one place in the repo that could deadlock
     itself: `Skill(test-architect)` opened a design phase and
     `Agent(commons-logging-installer)` closed one, two `PreToolUse` hooks with no ordering
     guarantee between them, and the loser blocked every write the other agent made under
     `src/` for the rest of the run — lessons-learned-006 § 1 is the run that hit it (138k
     tokens, zero files written, had to relaunch alone). `agent_classes` retired it: a
     subagent's write is judged by its own `agent_type`, so no phase reaches it and nothing
     closes a phase on an `Agent` call any more
     (`@.claude/decisions/0059-agent-classes-territory-schema.md`).
   - Either **Skip** of the first two → proceed to the executor anyway. A spec that doesn't cite
     `@LogExecution`/`@MaskSensitiveData` or ArchUnit doesn't need either installed to
     compile; skipping isn't a gate failure, it's the user's call.
   - No gap found → skip this pre-flight silently, no question asked.

2. **Three delegations to `java-spring-boot-developer`, chained.** Every turn of the executor
   rereads its whole context, so one run carrying Block 1 into Block 4 pays for it on every
   later turn — 427,889 tokens of context and 531,362 billable tokens in the run that reopened this
   (`0130`). Each group starts again from the spec and what is on disk:

   | Group | Blocks | Checklist steps it ticks |
   |---|---|---|
   | `domain` | 1, 2 | 1–12 |
   | `adapters` | H, A, I, 3, G, S, M, J, C — those the spec carries | 13–15 |
   | `tests` | 4 | 16–19, then the `status:` line |

   - **Where the chain starts.** At the first group with a checklist step neither ticked nor
     `n/a`. A group ticks its steps only when it ends green, so a run that failed in
     `adapters` starts there again, and a fresh spec starts at `domain`.
   - **Each delegation sends** the spec path, the group, and — from the second on — the
     `Blocks` lines and findings of every earlier group, copied from their reports. A
     decision a group took that is in neither the spec nor the disk reaches the next one only
     this way.
   - **Launch the next group in the turn that receives the previous one's report, and ask
     nothing in between.** The `tests` Stop gate defers while a writer subagent of the
     session runs; a turn that ends between two groups has none running, and the gate tests
     a half-built tree (`@.claude/decisions/0116-tests-defers-while-a-writer-subagent-runs.md`).
   - **A group that fails stops the chain** → report its failure, name the group, and stop.
     No git. `/new-feature-implement UC-NNN-<slug>` again resumes at that group.
   - **Success** — the `tests` group reports the checklist complete, the build green, and the
     spec at `status: implemented` (or `implemented-blocked`, which is a success too, with the
     case it blocks on named) → item 3 below, then **invoke** `git-publish` via the `Skill` tool,
     with `feat(UC-NNN-<slug>): <one-line summary>` as context.

3. **Add the compose services the spec decided.** Read the spec's `## Infrastructure`. A
   `materialize` row → **invoke** `compose-service-installer` via the `Agent` tool, in the
   foreground and in the same turn as the `tests` report, with the use case folder and those
   rows. It runs `docker-architect`, which this thread cannot call: the class keeps
   `design_phase`, and the guard skips the `Skill` call of a classed agent instead
   (`@.claude/decisions/0137-pending-compose-service-decided-at-design-materialized-at-implement.md`).
   No `materialize` row, or no section → skip silently. The agent failing does not stop the
   run: the code is green, the row is reported with the `/docker-architect` command, and
   `git-publish` is still offered.

`git-publish`'s two confirmation gates decide whether anything is committed or pushed —
this orchestrator only triggers the offer.

### 3 · Long-running background work

Implementing a complete feature takes dozens of minutes. An executor launched in the
background **doesn't survive the machine sleeping**: the watchdog cuts the stream and
execution dies where it was. This happened three times in a row on the first real
feature, with not a single file written, because all three died still in the reading
phase.

Before delegating the first group in the background, warn once and offer both options:
keep the machine awake for the whole chain (`caffeinate -i` on macOS), or implement on the
main thread, which is resumable. The executor writes by checkpoint precisely so that an
interruption leaves reusable progress — but no checkpoint helps if execution dies before the
first `Write`. A chain cut between groups resumes at the first group with open steps
(§ Procedure, step 2).

### 4 · Final report

Last message of the run, and the only report: the spec path and its `status:`, the groups that
ran and how each ended, **every `## Infrastructure` row of the spec, with what this run did to it** —
`added` or `failed` by the installer, `already present`, `external` with its address, or
`pending` with the `/docker-architect` command (or "none") — **every approved use case this
run left unreachable end to end**, with the backlog row that restores it named by its `BL-NN`
(or "none"), **every item deferred, with
its owner** (or "none"), **every guarantee delegated to a consumer outside this project whose
idempotency is assumed or unknown** (or "none"), and **every personal-data field that crosses
a boundary in clear, with its receiver** (or "none") — the findings come from the `tests`
group's report, which carries every group's lines — what `git-publish` did, and the next
command: `/clear` before the next `/new-feature`. A clean context per use case keeps cost
measurable per case. A failed group's report instead names the group, its failure, and
`/new-feature-implement UC-NNN-<slug>` to resume there.

---

## References

- **`@.claude/decisions/0130-executor-split-by-block-group-implement-in-clean-session.md`** — the
  three groups, the hand-off, launching in the same turn, the clean session.
- **`@.claude/decisions/0135-new-feature-split-spec-and-implement.md`** — why this flow is a
  skill of its own, its model and its empty territory.
- **`@.claude/decisions/0067-implement-entry-row.md`** — the single door to the implement half,
  input row 3 of `/new-feature` until 0135.
- **`@.claude/decisions/0116-tests-defers-while-a-writer-subagent-runs.md`** — why the next
  group launches in the turn that receives the previous one's report.
- **`@.claude/agents/commons-logging-installer.md`** — one-time logging/masking setup,
  triggered directly from the pre-flight, from this skill's `templates/commons/`.
- **`@.claude/agents/mapstruct-installer.md`** — records the project's mapper mechanism once;
  for MapStruct, wires the build from this skill's `templates/mapstruct/` and converts every
  existing mapper.
- **`@.claude/agents/compose-service-installer.md`** — adds the spec's `materialize` services
  through `docker-architect`, after the `tests` group and before `git-publish`.
- **`@.claude/decisions/0137-pending-compose-service-decided-at-design-materialized-at-implement.md`**
  — why the service is decided at design time and added here, by an agent.

---

## Entry into generated projects

Step 6.6 writes the skills into the project, this one included — the user runs
`/new-feature-implement UC-NNN-<slug>` after `/new-feature` approves a spec.
