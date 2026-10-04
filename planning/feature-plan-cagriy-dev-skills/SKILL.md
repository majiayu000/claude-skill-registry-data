---
name: feature-plan
description: Produce a staged, TDD-driven implementation plan that maps 1:1 to an existing feature design under features/feature-v<N>-<description>/. Use when the user asks to plan an implementation, break a feature into stages, or write a plan/roadmap for an existing design — typically as a follow-up to /feature-design. Refuses to plan without a real design file (delegated to feature-resolve). Runs its planning core (design read, codebase grounding, drafting, review, tracker update, lessons capture) inside a single general-purpose subagent; the subagent never asks the user questions — planning-level gaps are decided autonomously and recorded in the plan's "Planning decisions taken" section, and design-level gaps halt back to the main agent with a pointer to /feature-design. Reviews the plan for design coverage, inaccuracies, conflicts, and security issues before presenting staged highlights, then updates the per-feature tracker. Closes the plan with an execution schedule that groups independent stages into parallel batches — judged by a named independence rule, serial whenever independence is in doubt, never splitting or inventing a stage to gain parallelism — so /feature-implement can build them concurrently. Step 0 confirms with the user via AskUserQuestion before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /feature-plan or just chained in from /feature-design.
user-invocable: true
disable-model-invocation: false
argument-hint: <optional v<N> to target a specific feature, or omit to use the latest with a design and no plan yet>
allowed-tools: Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill, Agent, Bash(ls *), Bash(find *), Bash(mkdir -p *), Bash(test *), Bash(cp *), Bash(pwd), Bash(date *)
---

# feature-plan — TDD-Staged Implementation Plan For A Design

You are running the `feature-plan` skill. The user may have arrived here by typing `/feature-plan` (with an optional version in `$ARGUMENTS`), by chaining in from `/feature-design`, or because the model proactively invoked the skill. Your job is to produce a detailed, staged, test-driven implementation plan tied to an existing design document at the path returned by `/feature-resolve`.

**Terminology (plugin-wide).** Two words are overloaded; keep them apart. A **step** is a numbered step of *this skill's own procedure* — the `## Step …` headings below (e.g. *Step 4*); the only other "steps" are the **TDD steps** inside a plan stage (write test → confirm fail → implement → confirm pass). A **stage** has two senses: a **chain stage** is one of `storm → design → plan → implement` (it shows up as `stage=…`, `stage_file`, and the tracker's `data-stage`), while a **plan stage** is a committable unit of work *inside* the implementation plan (e.g. `Stage 1`) — `/feature-plan` creates these and `/feature-implement` builds one per commit. A procedure step is never a plan stage, and a plan stage is never a procedure step.

**Execution model.** This skill has twelve steps (Steps 0–11), split across two contexts. Steps 0–2 and Step 11 run here, in the main agent — they are the only places the user can be prompted. Steps 3–10 (the planning core) run inside a **single general-purpose subagent** launched in Step 2; the subagent has no channel to the user, so it never asks questions — it decides and records (Step 6) or halts and returns (the `BLOCKED:` protocol in Step 2). Execute the steps in order. Do not skip Step 0 (proactive-invocation confirmation), Step 2 (subagent delegation and verification), Step 5 (design coverage map), Step 6 (planning-decision protocol), Step 7 (review and update), Step 8 (tracker update), or Step 9 (lessons capture) — they are the load-bearing steps.

## Step 0 — Confirm before proceeding (when invoked proactively) *(main agent)*

Check the most recent user message in the conversation for the literal tag `<command-name>/feature-plan</command-name>` (or, equivalently, a leading `/feature-plan` typed by the user). If present, the user has explicitly opted in via the slash command — skip this step and continue with Step 1.

Also treat as opt-in (and skip this step) if you were just invoked as a chain from `/feature-design`'s Step 11 — i.e. the immediately previous turn was an `AskUserQuestion` result with header `"Run /feature-plan?"` and the user selected the option starting `"Yes, run /feature-plan"`. In that case the user has already confirmed; do not re-ask.

Otherwise (you arrived here because the model decided to invoke this skill proactively from natural-language intent, with no recent chained opt-in), call `AskUserQuestion` exactly once before any other work:

- **question**: `"Launch /feature-plan to produce a TDD-staged plan for <design version, e.g. v3>?"` — name the specific feature you'd plan against.
- **header**: `"Run /feature-plan?"`
- **options**:
  - `{ "label": "Yes, proceed", "description": "Run the skill and produce the implementation plan." }` (mark this as Recommended)
  - `{ "label": "No", "description": "Don't run; I'll redirect." }`

If the user picks "No" or "Other", stop the skill immediately and do not start Step 1. Do not write any files, do not ask further questions.

## Step 1 — Resolve the feature folder via `feature-resolve` *(main agent)*

**Start the usage window.** Before anything else in this step, invoke `usage-report` via the `Skill` tool with the argument `start feature-plan`, so the final step can report what this run cost. It runs inline, prints nothing, and is a silent no-op when `CLAUDE_CODE_SESSION_ID` is unset — **do not end your turn**, carry straight on with the rest of this step. It sits here rather than in Step 0 deliberately: a declined confirmation must never leave a start marker behind with no report to clear it.

**Load your customisations.** Immediately after the usage window, read the house rules the user recorded for this skill with `/skill-customize feature-plan`. It sits here rather than in Step 0 for the same reason the usage window does: a run the user declined must never have read, announced or applied a customisation first.

**Resolving `${CLAUDE_PLUGIN_DATA}`.**

```text
${CLAUDE_PLUGIN_DATA} is a plugin-config substitution token: Claude Code expands
it inside plugin hook, MCP and LSP command strings, and it is not an exported
environment variable, so a shell that simply reads it almost always gets nothing
back. Resolve the directory yourself, taking the first rule that yields a path:

1. `$CLAUDE_PLUGIN_DATA`, on the chance the environment really does set it.
2. `<config-dir>/plugins/data/<plugin>-<marketplace>`, derived from the running
   skill's own base directory: an installed plugin runs from
   `<config-dir>/plugins/cache/<marketplace>/<plugin>/<version>/skills/<slug>`,
   so `<plugin>` and `<marketplace>` are the two path segments above the version,
   and Claude Code keys the data directory on exactly that pair.
3. The single `<config-dir>/plugins/data/dev-skills*` directory, when `ls` shows
   exactly one. Two of them means a stale second install is present and the rule
   is ambiguous, so it is skipped rather than guessed at.
4. `<config-dir>/plugins/data/dev-skills` — reached only when the plugin is
   running from a working clone rather than an installed copy.

`<config-dir>` is `$CLAUDE_CONFIG_DIR` when that is set, and `~/.claude` when it
is not. A skill's customisation file is then `<extras-dir>/<slug>.extras`.
```

Read `<extras-dir>/feature-plan.extras`.

**A missing file is the ordinary case. Say nothing at all and carry straight on with the rest of this step.** Most projects never customise this skill, and a "no customisations found" line on every run is noise on the common path. The same applies if the file cannot be read for any other reason: carry on without it. A customisation is a preference, and failing to load one never blocks a run.

When the file does exist, treat every `- ` bullet in it as an instruction that applies to this run, on top of everything below. Announce it in one line — `Customisations active: <n> (feature-plan.extras)` — and then actually apply it. Customisations legitimately change defaults, counts, thresholds, tone, formats, which optional behaviours fire, and what you settle yourself instead of asking: how finely stages are cut, how much detail each stage's definition of done carries, how aggressively scaffolding stages are allowed, and how the staged highlights are summarised.

**They never override the *Constraints (non-negotiable)* section at the end of this file.** `/skill-customize` refuses that kind of instruction at write time, so one arriving here means the file was hand-edited. Ignore that bullet, name the constraint it collides with in one line, and carry on with the rest. The file is never permission to make the planning core ask the user questions, plan past a non-empty design §8, or let the subagent commit anything.

The customisations belong to the **main agent**, exactly as the usage window does. The planning subagent never resolves the data directory and never reads the file itself — you loaded it once, here, and you pass the text down in its Step 2 brief. Re-resolving it inside a fresh context is both wasteful and a way for the two agents to end up reading different files.

Parse `$ARGUMENTS` for an explicit version token only — `/feature-plan` does not take requirements text or a description (the description is authoritative from the feature folder; the requirements are authoritative from the design).

- Look for a leading `v<N>` or `version <N>` (case-insensitive; bare `1` does **not** count — only `v1` / `v 1` / `version 1`). If found, record as `explicit_version` and strip from the input. Integer only — no minor versions.
- If `$ARGUMENTS` contains other free-form text (e.g. the user typed feature requirements out of habit), note it for context but do not act on it. Plans don't redefine scope — the design does.

Invoke `feature-resolve` via the `Skill` tool with the argument string:

```
stage=plan[, version=<N>]
```

Include `version=` only if Step 1 captured an `explicit_version`. Do not pass `description=` — plan is always about an existing feature folder, and the resolver derives the description from that folder.

The resolver enforces all of this:

- Without a version arg, it picks the latest `features/feature-v<N>-<desc>/` folder that has a design file but no plan file (Rule C) — exactly the right target.
- If the latest folder already has a plan, the resolver asks the user whether to overwrite in place or target an older version. This is the only way to revise a plan under this plugin (revisions are deliberately dropped from the versioning scheme).
- If no design exists anywhere, the resolver errors and tells the user to run `/feature-design` first. Surface that error verbatim and stop.

This step stays in the main agent deliberately: `feature-resolve` can ask the user questions (authorise an overwrite, pick an older version, choose between template copies), and those must be settled before the subagent — which cannot prompt anyone — is launched.

Parse the resolver's output block. Record `mode`, `version`, `description`, `feature_folder`, `stage_file` (this is where Step 5 writes the plan), `prereq_file` (the design file the subagent must read), and `tracker_file`. Keep the raw block intact — Step 2 pastes it verbatim into the subagent briefing.

If the resolver stops with an error, pass the message to the user verbatim and stop. Do not retry with invented arguments.

**`feature-resolve` runs inline in this turn — do not end your turn when its result block appears.** The `Skill` tool loads it into your own context rather than delegating to a subagent, so the block is a checkpoint in the middle of *your* run, not a hand-off that returns control anywhere. Once you've recorded the fields above, continue straight into Step 2 in the same turn and launch the planning subagent. Stopping here strands the user with a seeded folder, an empty tracker, and no plan. (The Step 2 subagent is the one real delegation in this skill; the resolver is not.)

## Step 2 — Launch the planning subagent *(main agent)*

Everything from reading the design to composing the final summary (Steps 3–10) runs inside one subagent. This keeps the main conversation lean; the cost is that the subagent cannot talk to the user, which Steps 3–10 are written to respect.

Launch **exactly one** subagent with the `Agent` tool — `subagent_type: general-purpose`, default isolation, **not a worktree** (it writes the plan file and tracker into the shared working tree). Launch it and wait for its return; do not run anything else in parallel.

The subagent starts with a fresh context and cannot see this conversation, so its briefing must be self-contained. Pass, as the prompt:

- **Role** — "You are executing Steps 3–10 of the dev-skills `feature-plan` skill in `<absolute cwd>`. You write the plan file, update the tracker, and capture lessons. Your final message is consumed by the main agent, not shown to the user directly."
- **Resolution block** — the Step 1 resolver output verbatim (`mode`, `version`, `description`, `feature_folder`, `stage_file`, `tracker_file`, `prereq_file`, `notes`).
- **Customisations** — the `- ` bullets you loaded in Step 1 from `feature-plan.extras`, copied verbatim, or the single word `none`. Tell it they apply on top of the procedure below but never over the *Constraints (non-negotiable)* section, and that it must not go looking for the file itself — it has no reliable base directory to resolve from, and a second resolution is how the two agents end up reading different files.
- **Procedure** — the full text of Steps 3–10 below **plus** the *Constraints (non-negotiable)* section, copied faithfully — including the plan-file template in Step 5 and the tracker token rules in Step 8. Do not summarise or paraphrase them; fidelity is what keeps subagent runs identical to direct runs.
- **No toolchain claims** — do not state the project's language, package manager, or test runner in the briefing; the subagent derives the runner(s) from the repo's manifests, README, CI config and any previous plan under `features/` (its Step 4). A stale or guessed claim is a misdirection the subagent must spend a grounding pass refuting before it can cite any command.
- **Interaction rule** — it has no user channel: it must never call `AskUserQuestion` or wait for input. Planning-level ambiguity is handled by Step 6's decide-and-record protocol; anything it cannot decide is a halt (below).
- **Halt protocol** — on any blocker (design §8 non-empty, a design-level decision it must not make, a missing prerequisite, a contradiction with the resolution block), it stops where it is and returns a final message starting with `BLOCKED:` plus a one-line reason, followed by the details the user needs (the specific open questions, the decision required, what was and wasn't written). It never flips the tracker's progress bar on a halted run.
- **Git constraint** — it writes files only; it never stages, commits, pushes, branches, or otherwise touches git state.
- **Return contract** — on success, its final message is **exactly** the Step 10 summary block, nothing before or after.

When the subagent returns, verify before relaying:

1. If the message starts with `BLOCKED:`, invoke `usage-report` via the `Skill` tool with `report feature-plan, outcome=halted` (a halted run still cost tokens), then relay the message to the user verbatim and stop — Step 11 does not run, so this is the only place the report fires on a halted run. (For a design-level blocker, the recommendation to the user is a new design version via `/feature-design`.)
2. Otherwise run `test -f <stage_file>` — the plan file must exist. If it doesn't, or the final message isn't the Step 10 block, report the discrepancy to the user instead of relaying a success.
3. If the summary's *Skill-improvement recommendations* line says lessons-capture was unavailable in the subagent, invoke `lessons-capture` via the `Skill` tool (argument `feature-plan`) from the main agent now, and substitute the returned entry into the summary before relaying.

Then continue to Step 11.

**Fallback:** if the `Agent` tool is unavailable in this session, or the user **rejects** the subagent launch, say so in one line and execute Steps 3–10 yourself, in order, under the identical contract — including Step 6's no-clarifying-questions policy, which is a property of the plan stage, not of subagent execution. A rejected launch is a mode override, not an error: never re-attempt the launch.

## Step 3 — Read the design end-to-end *(subagent)*

`Read` the design file at `prereq_file` (from the resolution block in your briefing). Build an internal map of:

- The numbered requirements in §3.
- The components / modules described in §5 (Architecture / components).
- The interfaces, data model, control flow, failure cases, security, performance, observability, compatibility, and testing sections in §5.
- The risks in §7 and the rollout plan in §9.

If §8 (Open questions) of the design is non-empty (anything other than "None — all decisions closed."), halt per the `BLOCKED:` protocol in your briefing — name the specific open items in your return message. The design must be closed via `/feature-design` before planning; do not attempt to plan around them.

If a brainstorm file also lives in `feature_folder` (`feature-storm-v<N>-<description>.md`), `Read` it too — it captures the original product intent and any open questions §8 of the design should have addressed. Cross-check that the storm's intent is reflected in the design before planning.

If the design cites an external document as a mandatory dependency or prerequisite (scan the requirements, architecture, risks, and rollout sections for cited paths or links), `Read` it as well before drafting — a stage that depends on it cannot be made concrete from the citation alone.

## Step 4 — Ground the plan in the codebase *(subagent)*

Use `Read`, `Grep`, and `Glob` to verify the design's assumptions about the existing codebase: do the files/functions/utilities cited in §4 and §5 actually exist? What is already in place vs. what needs to be built? Bound the exploration to what the plan touches.

When the design makes load-bearing claims about an external or sibling dependency — a sibling repo's API, an external tool's return shape or failure behavior — verify them by reading that dependency's source or docs rather than trusting the design prose. Claims about code the design's author does not own are the likeliest to have drifted. When the dependency is an already-installed, version-pinned package, the first check is to introspect the installed copy with the project's own runtime (list the real fields, methods and parameter names), falling back to source or docs only where introspection cannot answer — docs may describe a different release than the one that will run. And when the cited dependency is specified but not yet implemented (a co-developed sibling repo), verify against its design/spec document instead, record the non-implementation as a plan risk, and stage the work against the frozen contract with stubs, deferring live-integration verification to a final gated stage.

**Verify the design's claims, not just its citations.** Confirming that a cited file or symbol *exists* is the weakest available check, and it is the one that keeps passing while the plan inherits a defect. Read the code behind the claim; the classes that most often hide a defect:

- **Names the design says it will add.** For every symbol, file, or key the design says the feature will add, gain, or extend, grep for an existing definition of that exact name. A same-name/different-purpose collision is a Step 7 conflict to raise, not a coincidence to design over. For each helper the design proposes to add, also read the code path it plugs into and check whether an existing mechanism under a different name already delivers the specified observable behaviour — if so, plan reuse, record it as a planning decision, and correct the design in place.
- **Shapes and contracts.** For any wire payload, dict or record literal, response body, or config value the design specifies — or that the feature's new code merely *reads* — diff each field and key against the producer **and** the consumer in the codebase, not against the design's prose. A stale consumer is the trap here: new code piggy-backing on an existing read silently inherits whatever that read already gets wrong. Include the transport in the check — where a client serialises by naming fields explicitly rather than forwarding the object, a newly added field never reaches the wire unless that file is in the relevant stage's *Touches*.
- **Mechanisms the design says already exist.** A runtime behaviour asserted in prose (validation that runs before the body, coercion, retry), a repo-wide guard test or CI gate that a requirement's verification is delegated to, an unpinned push/notify path (event stream, websocket, callback) — locate each on disk and read it before mapping a requirement to it or staging work on top of it. If it does not exist, plan the work and record the gap as a planning decision; if it behaves differently from the prose, record the mismatch. A requirement mapped to a mechanism that lives only in spec text is covered on paper and nowhere else. And a cited runtime mechanism whose trigger or entry symbol has zero call sites outside its own definition does not exist in practice — grep for callers, not just the definition, before mapping a requirement onto it.
- **Anchors and edit targets.** Re-resolve every `path:line` anchor you intend to repeat in the plan — the design was written earlier and line numbers drift with each intervening commit, so correct it or drop the number. And confirm that every file the design's rollout or documentation steps name as an edit target actually exists, so a stage says *create* or *edit* correctly the first time.
- **Symbols the design says it will remove.** For every symbol the design marks deleted, dead, unread, or caller-less, grep its full reference set across source *and* tests before staging the deletion. A surviving caller is a missed requirement site to raise in Step 7; a surviving read falsifies any "this becomes unused" claim the plan would otherwise inherit.
- **Internal consistency of the design's own sections.** The design can contradict itself — an interface sketch declaring an input no described step produces, two sections asserting opposite invariants (one says a component writes a store, another says it never does), prose that violates its own numbered requirement. For every declared signature, name the design component or step that produces each input; for every stated invariant, check no other section asserts its opposite. An input with no producer is an under-specification to close as a planning decision; a contradiction resolves by the precedence rule in Step 7's internal-contradiction case.

Catalogue the project's test directory and naming conventions before drafting — for each new test file the plan will create, name an existing sibling that follows the same pattern (e.g. `<tests-root>/<area>/<existing-sibling-test-file>`). This avoids inventing test paths in Step 5 that you then have to rename in Step 7 once you notice they don't match the project's convention.

**A test location the design names is a proposal, not a fact — confirm it is viable before citing it.** For each test file the plan will create or extend, verify that a test living there can actually run and reach the symbols under test: that the directory's import path resolves to the module under test (watch for per-directory bootstrap files, custom loaders, or path manipulation that only some directories get), that a file named for extension is at the right layer and harness to host the new cases, and that a component the design marks as unit-tested sits in a build target that has a test suite at all. Where it does not hold, choose the substitute location now — relocating the testable logic into a tested target if that is what it takes — and record the choice under *Planning decisions taken*, rather than inheriting an unrunnable path and discovering it at the first red run.

**Greenfield branch (per layer):** if the feature adds tests in a language/runner the repo has no existing suite for — whether the repo is test-less outright or only that layer of a polyglot repo is — waive the sibling-naming requirement for that layer; instead have an early stage of the plan explicitly establish and document that layer's test convention — directory layout, framework/runner command, and any fixture/async setup — and record that choice, rather than inventing a nonexistent sibling path. Layers that do have an existing suite still follow the sibling-naming rule. Before inventing a convention, check whether the design cites a sibling or reference project whose conventions it adopts ("mirrors <other project>"); if it does, read that project's test layout, runner configuration and CI workflow and adopt them, naming it as the convention source in the convention-establishing stage — an inherited, verified convention beats an invented one and is auditable afterwards. Where the repo has no build system at all, confirm which scaffolding tool is actually installed and prove it by executing it once in the scratchpad: run the scaffold, run the proposed test command end-to-end including one deliberately failing test, and transcribe the observed runner command and failure strings into the plan rather than predicting them — reading flags only yields plausible commands, and a generic or assumed tool name fails Step 7's accuracy check at best and Stage 1 at worst.

Also identify the project's primary test framework and runner (read package/build manifests, existing test files, and any CI config). Record the runner command the plan's "run the test" steps will use. If the project uses multiple frameworks for different layers, record which one applies to each area the plan touches.

Ground the rest of the build/run mechanics the stages depend on, not just the test runner:

- Determine how new source and test files are registered with the build system — auto-discovered, or requiring an explicit manifest/project-file entry. If registration is explicit, every file-creating stage must include it as a step, or the new files silently never compile or run.
- If symbols the plan changes feed build targets that have no tests (an app or UI shell, say), record a build-only check command for each; Step 7's working-after-each-stage check must require those targets to keep compiling between stages.
- If a stage introduces a new package or component with its own dependency environment, that stage must provision the environment (and any CI wiring) before its test-run steps, and phrase its "confirm fail" as the behavior gap — a test failing because its environment doesn't exist yet proves nothing.
- Execute each recorded runner and build-only command exactly once before drafting, and record the observed baseline (test count and pass/fail, build exit status) in the plan's development-strategy section. A recorded-but-never-run command is a guess: an unverified or wrongly-flagged command string, and an already-red baseline that would void every stage's "confirm no regressions" step (and which `/feature-implement` halts on anyway), both surface now instead of at the first red run.

For each **shared symbol the design changes** — a constructor or function signature, a widely-used class, a renamed config key — grep its construction/reference count across both source and tests to size the blast radius before staging. That count drives the staging decision (land the change atomically, defer it, or add a backward-compatible shim) and guards against plans that break the suite between stages or bundle an un-reviewably large mechanical edit.

Key the blast-radius check to the *kind* of change — raw reference counts mislead for several common kinds:

- **Changed default value** (no signature change): grep for tests that assert the old default or depend on its behavior; if none do, a high call-site count is not a risk signal.
- **Widened structurally-typed interface** (protocol / abstract base / duck-typed contract): find implementers structurally — classes passed where the type is expected, and test fakes — not just by name-grepping the symbol.
- **New variant on an enum / union / sealed type**: grep for exhaustive switch/match sites over that type; each is a forced same-stage edit — the new variant won't compile (or falls through) until every exhaustive site handles it.
- **New entry in a registry / list that tests enumerate**: grep for tests that iterate or count that collection (the collection name near a length or equality assertion); the stage adding the entry must update those guards.

**Record the dependency evidence the execution schedule needs.** For every stage you will draft, note the files it creates or modifies — including the registration file, lockfile, snapshot/golden file, generated artefact or migration it rewrites, each of which must appear in that stage's *Touches* or Step 5's disjoint-files test cannot see it — the symbols and string-keyed names (endpoint paths, job/event/type names, flag and config keys) it introduces or consumes, the registration points it edits, and any shared test resource its tests bind (a fixed port, a database, a simulator or device, a live service, a global cache or temp path). Step 5's independence rule is decided from this evidence, never from stage titles.

When the design scopes work as **mirroring or paralleling an existing path** — a new variant of an existing family, an analogous handler/pipeline/exporter, a per-kind twin of an existing flow — `grep` and read the existing counterpart before staging, and stage the work as generalising/parameterising the shared code (a kind argument, a loop over kinds, an extracted helper) rather than as a field-swapped copy; name the shared helper in the stage's *Touches* and keep the existing path's tests green within the same stage. The same applies to test scaffolding: a stage adding analog test files reuses or hoists shared fixtures/builders via the project's shared-fixture mechanism instead of re-declaring them per file.

The goal is (a) to produce concrete, executable steps in Step 5, and (b) to surface conflicts between the design and current reality that you will raise in Step 7.

## Step 5 — Draft the staged implementation plan *(subagent)*

The plan is a sequence of **stages**. A stage is a unit of work that ends with a working, tested, mergeable increment — small enough that a reviewer can hold it in their head, large enough to be meaningful. Order stages so that each one builds on the last and leaves the system in a working state.

For every stage that introduces or changes behavior, the steps inside the stage **must follow the test-driven development cycle**:

1. **Write the test first** — concrete test cases for the behavior the stage will deliver. Cite the file path the test will live in.
2. **Run the test and confirm it fails** — record the expected failure mode so the test is proven to actually exercise the new behavior.
3. **Implement the code** — the minimum needed to make the test pass; cite the files/functions to add or modify.
4. **Run the test and confirm it passes** — and run the surrounding test suite to confirm no regressions.

In compiled or statically-checked projects, a stage that introduces a brand-new type or module cannot reach a red *assertion* first — the test target fails to build before any assertion runs. That is a legitimate first red, not a broken cycle: record the build/compile error as the expected initial failure, scaffold the minimal empty API, then re-confirm red as assertion failures before implementing. Write it into the stage's steps as the normal shape for that language rather than re-deriving it as a planning decision on every run.

Not every stage fits the red-first cycle. These stage categories are also sanctioned — label each such stage with its category and a one-line justification; never invent an ad-hoc label:

- **Non-TDD (scaffolding | config-only | integration-verified)** — nothing host-assertable: empty module files, dependency additions, configuration-only edits, or stages verifiable only by a live/integration check. An integration-verified stage must name the concrete verification command or check in its steps.
- **Behaviour-preserving refactor / deletion** — restructures or removes code without changing observable behavior. Discipline: adjust existing tests first, then keep the suite green and the build clean; no new failing test is required.
- **Characterization / guard tests** — behaviour-preservation invariants (parity with a prior implementation, a performance bound) expected to be green before *and* after the change. Each must name the regression it guards; a red here flags a defect in the guarded stage, not a TDD step.
- **Platform-only / UI wiring** — behavior-changing code that cannot run under the host test runner (device/UI layers, platform-conditional code). Extract as much logic as possible into host-tested pure units under full TDD; verify the remaining wiring via build, simulator/device, or a stated manual check.
- **External prerequisite (gated)** — a stage consuming work delivered outside this repo (a sibling repo's feature, a provisioned service, a credential). It opens with a named gate check — a status document and/or a live probe — rather than implementation steps, and requirements delivered externally map in the coverage table to the stage that gates on and consumes them, so the map stays complete without implying out-of-scope work.

A stage may also be **hybrid**, and that is a sanctioned shape rather than an ad-hoc label: full TDD steps for its host-testable portion, plus an *integration-verified remainder* labelled as such and naming the concrete verification command for the rest. The testable-core-plus-platform-edge stage is common, and Step 7 treats an invented label as a defect — so use this form instead of improvising one.

Write the plan to the `stage_file` path from the resolution block in your briefing. In **continue-existing** mode where the resolver's `notes` record an authorised overwrite, edit the existing file in place to match this shape — do not duplicate or branch sections.

```markdown
# <Feature Name> — Implementation Plan v<N>

**Status:** Draft
**Date:** <YYYY-MM-DD>
**Design:** [feature-design-v<N>-<description>.md](./feature-design-v<N>-<description>.md)

## Overview
One paragraph: what is being built, how the plan is staged, how the plan maps to the design.

## Development strategy — Test-Driven Development
Every behavior-changing stage in this plan follows the TDD cycle:

1. **Write the test first.** Add the test(s) that describe the new behavior.
2. **Run the test and confirm it fails.** Capture the failure to prove the test exercises the new behavior.
3. **Write the implementation.** The minimum code needed to satisfy the test.
4. **Run the test and confirm it passes.** Plus the surrounding suite, to catch regressions.

Stages that fit a sanctioned non-red-first category — non-TDD (scaffolding | config-only | integration-verified), behaviour-preserving refactor/deletion, characterization/guard tests, platform-only/UI wiring, external prerequisite (gated) — are labeled with that category and a one-line justification.

## Requirements coverage map
A table mapping every numbered requirement in §3 of the design to the stage(s) that deliver it.

| Design req | Delivered by stage(s) |
| --- | --- |
| R1: <one-line restatement> | Stage 2, Stage 4 |
| R2: ... | Stage 3 |
| ... | ... |

Every design requirement must appear in this table with at least one stage. If you cannot map a requirement, return to Step 4 and find the gap.

## Stages

### Stage 1 — <Short title>
**Goal:** <one sentence — what this stage delivers>
**Design references:** §<n>, §<n> of feature-design-v<N>-<description>.md
**Touches:** <files to create/modify, by path>

**Steps (TDD):**
1. Write test: `<path/to/test_file>` → `<test_name_or_id>` covering <behavior>. Expected initial failure: <one concrete failure mode in this project's test framework, e.g. a missing-symbol/module error, or an assertion that the not-yet-implemented function returns the wrong value>.
2. Run the test — confirm it fails with the expected error.
3. Implement: create/modify `<path>` to <concrete change>.
4. Run the test — confirm pass. Run the surrounding suite — confirm no regressions.

**Definition of done:** <bulleted, checkable>

**Risks specific to this stage:** <only if non-trivial; otherwise "None">

### Stage 2 — <Short title>
<same shape>

### Stage N — <Short title>
<same shape>

## Cross-cutting concerns
Concerns that don't fit cleanly into one stage but must be tracked:
- **Security** — input validation, authz, secret handling decisions taken from design §5 and how they appear across stages.
- **Performance** — limits, indexes, hot-path decisions from design §5.
- **Observability** — logs/metrics/traces added across stages.
- **Compatibility / migration** — how data and callers are handled across stages so the system stays working between merges.

## Verification
End-to-end verification once all stages are complete: how the user confirms the feature works against the acceptance criteria in design §3.

## Risks and open issues
Concrete risks specific to *implementation* (not design risks — those live in the design). Each with a mitigation.

## Planning decisions taken
Planning-level decisions this plan made autonomously because the design did not resolve them (see Step 6's protocol): stage ordering, feature-flag placement, harness/framework selection where the design was silent, concrete file locations. A numbered list, one line each with a short rationale — or exactly: "None — the design resolved every planning-level decision."

## Deviations from the design
Either "None — plan matches design v<N> exactly." or a numbered list of deviations with rationale. Any deviation here is a signal that the design may need a follow-up version; flag the suggestion in the Step 10 summary.

## Execution schedule
Batches run in order; a batch starts only when the previous one has fully landed. Stages inside a *parallel* batch are independent and may be built concurrently; a *serial* batch holds one stage. `/feature-implement` follows this table and demotes any batch it cannot verify to serial.

| Batch | Stages | Mode | Why this mode |
| --- | --- | --- | --- |
| 1 | Stage 1 | serial | establishes the test convention every later stage uses |
| 2 | Stage 2, Stage 3 | parallel | disjoint files, no shared symbol or string-keyed contract, no shared registration point, no shared test resource |
| 3 | Stage 4 | serial | consumes the API introduced by Stages 2 and 3 |

**Critical path:** Stage 1 → Stage 3 → Stage 4 (3 of 4 stages).
```

Compute `<YYYY-MM-DD>` from `date -u +%Y-%m-%d`. Use `v<N>` (integer) in the header — never `v<N>.<M>`.

**The execution schedule.** The *Execution schedule* section groups the stages into batches for `/feature-implement`. Every stage appears in exactly one batch; batches are numbered in the order they run; a batch depends on the whole of the previous one; and a plan with no parallel batch still carries the table, all serial, so the implement skill never has to infer the absence. The aim is the shortest critical path that keeps every stage coherent — the schedule groups the stages Step 5 already cut and never splits, merges or invents a stage to gain parallelism. The *Why this mode* cell of a parallel batch names the evidence, by the test names below; the *Critical path* line lists the longest chain of serial dependencies and its length against the stage count.

**Independence rule.** A batch is *parallel* only when every one of the following tests holds for every pair of stages in it, decided from the evidence Step 4 recorded rather than from stage titles. Any doubt about any test, for any pair, resolves to serial — a serial batch costs wall-clock, a wrongly parallel one costs a broken branch:

1. **Disjoint files** — no file is created or modified by both stages, counting test files, shared fixtures, manifests and project files, registries, lockfiles, snapshot/golden files, generated artefacts and migration files. Side artefacts the implement skill reserves for its main agent (the plan file, the tracker, a changelog or wiki) are excluded, since they never appear in a stage commit.
2. **No symbol or string-keyed dependency** — neither stage calls, imports, extends, or tests a symbol the other introduces or changes, and neither relies on a name the other registers: an endpoint path, a job, event or type name, a flag or config key.
3. **No shared registration point** — neither stage needs an explicit build or manifest entry, exhaustive switch site, enumerated registry, or shared fixture the other also edits.
4. **Same base state** — both stages are green against the previous batch alone, and neither's *confirm fail* step depends on the other's absence.
5. **Category exclusions** — always serial: a scaffolding or convention-establishing stage, a behaviour-preserving refactor of shared code, a stage changing a shared signature (the Step 4 blast-radius set), an external-prerequisite (gated) stage, a stage adding a schema migration, and a stage adding or upgrading a dependency.
6. **Security ordering** — the batch opens no window Step 7's *Security issues* check would reject: a protection never lands later than the code it protects, in the same batch or an earlier one.
7. **No shared test resource** — neither stage's tests bind a fixed port, shared database, simulator or device, live service, or global cache or temp path the other's tests also use; the two suites must be able to run at the same moment.

## Step 6 — Resolve planning-level decisions autonomously *(subagent)*

**You have no channel to the user.** This step replaces the clarifying questions an interactive planner would ask: the plan stage deliberately asks nothing — never call `AskUserQuestion`, never stall waiting for input.

If, while drafting Step 5, you hit a planning-level decision that is **not** resolved by the design and that would meaningfully change the staging or the implementation steps, decide it yourself:

- Prefer the choice that follows the codebase's existing conventions — Step 4's grounding is the evidence base.
- Prefer the reversible option over the one-way door; prefer the ordering that keeps the system working between merges.
- Record **every** such decision as one line with rationale in the plan's *Planning decisions taken* section, and surface the 1–3 most consequential in the Step 10 summary. An unrecorded autonomous decision is a defect — the record is what lets the user veto it after the fact.

Examples of planning-level decisions you decide and record:

- Order of stages when multiple valid orderings exist (e.g. ship the data migration first, or the API first?).
- Whether to land a feature flag in an early stage or skip it.
- Which existing test harness / framework to use when the design didn't specify.
- Concrete file paths when the design described shape but not location.
- Which independent stages to batch in parallel when the schedule could be cut more than one way — record the cut and why, when the choice is not obvious.

Do **not** decide design-level questions. If a gap would change the design itself — scope, requirements, approach, interfaces — halt per the `BLOCKED:` protocol in your briefing and name the decision required; only `/feature-design` can close it. Never silently expand scope in the plan.

## Step 7 — Review the plan and update *(subagent)*

Re-read the draft critically and fix what you find via `Edit` directly in the plan file. Run all of these checks:

- **Design coverage** — every numbered requirement in design §3 appears in the *Requirements coverage map* with at least one stage. Every component in design §5 *Architecture* has at least one stage that creates or modifies it. If anything is missing, add a stage or extend an existing one.
- **TDD discipline** — every behavior-changing, host-testable stage has all four TDD steps in order; the "confirm fail" step records a concrete expected failure (not "it will fail"); every other stage carries one of the sanctioned category labels from Step 5 (non-TDD scaffolding/config-only/integration-verified, behaviour-preserving refactor/deletion, characterization/guard, platform-only/UI wiring, external prerequisite (gated)) with its one-line justification — an unlabeled or ad-hoc category is a defect.
- **Inaccuracies** — every file, function, library, framework, or API cited *as already existing* must actually exist (verify the non-obvious ones with `Read`/`Grep`). For things the plan introduces, the cited path/name must be consistent across stages. Replace or remove anything invented.
- **Conflicts** — does any stage contradict another? Does any stage rely on something an earlier stage hasn't yet introduced? Does any stage break the system between merges? Fix the ordering or split the stage.
- **Intermediate states** — when a stage replaces an existing implementation of the same observable behavior, check whether old and new can coexist; if they cannot, the swap and its test migration must land as one atomic stage, exempt from the stage-size splitting pressure below (record the rationale in the stage). For any requirement the coverage map delivers across multiple stages, state the user-visible behavior after each contributing stage and explicitly decide whether the stages should be bundled into one.
- **Conflicts with the design** — does the plan silently change a decision from the design? If so, either revert to the design or move it to *Deviations from the design* with rationale (flagged in the Step 10 summary). **A factual grounding error in the design is a third case, not a deviation.** When Step 4 shows the design is simply *wrong about existing code* — a symbol it calls unshared that several views use, a module it calls unreachable that a harness already mounts, a drifted anchor — correct the design file in place and record the correction under *Planning decisions taken* with the corrected fact. Reserve *Deviations from the design* for changed scope, requirements, approach, or interfaces: Step 11 keys its recommendation off that section, so filing a one-line fact correction there wrongly recommends against implementing and proposes a whole new design version for something already fixed. Re-ordering or re-grouping implementation stages relative to the design's §9 rollout sequence is **not** a deviation — the plan owns staging order; only changes to scope, requirements, approach, or interfaces count. Likewise, a backward-compatible shim or defaulted parameter introduced only to bound the blast radius sized in Step 4 — leaving the design's interface contract intact — is a planning decision, not a deviation. **An internal contradiction between two design sections is a fourth case.** Resolve it by precedence: a numbered requirement in §3 beats prose or code sketches in §5; where the two readings differ only in *which component performs* an already-specified behaviour, the more operational section wins. Correct the losing section in the design file in place and record the resolution — both readings named — under *Planning decisions taken*, never under *Deviations from the design*. Halt (`BLOCKED:`) only when §3 itself is ambiguous or the readings differ in scope, requirements, or an external interface.
- **Decision log** — every entry in *Planning decisions taken* is genuinely planning-level (staging order, flags, harness, paths). If any recorded decision actually changes scope, requirements, approach, or interfaces, it is design-level — halt per the `BLOCKED:` protocol rather than shipping it in the plan.
- **Security issues** — does any stage introduce a regression in input validation, authz, secret handling, logging of sensitive data, or trust boundaries that the design protected? Does the *order* of stages create a window where the system is insecure (e.g. endpoint live before authz check is wired)? Fix by reordering, adding guard stages, or feature-flagging.
- **Hand-waves** — replace any "TBD", "TODO", "we'll just…", "should be straightforward" with concrete steps or move them to *Risks and open issues* with explicit mitigations.
- **Stage size** — no single stage should be so large that it can't be reviewed in one sitting. Split large stages. Conversely, do not fragment trivially small steps into their own stages. Splitting for size is fine; splitting a stage so its halves can run concurrently is not — that is the schedule reshaping the work, which the next bullet forbids.
- **Schedule soundness** — every stage appears in exactly one batch of the *Execution schedule* and batches are numbered in execution order. Every stage in a parallel batch passes all seven independence tests against each of its siblings — *Disjoint files*, *No symbol or string-keyed dependency*, *No shared registration point*, *Same base state*, *Category exclusions*, *Security ordering*, *No shared test resource* — and the *Why this mode* cell names the evidence. Any pair you cannot clear on every test goes serial. Confirm that no stage was split, merged or added to create parallelism, that a parallel batch opens no window the *Security issues* check above would reject, and that the *Critical path* line is present and consistent with the table.

After edits, do a final pass to confirm:

1. Every design requirement is in the coverage map and tied to a stage.
2. Every behavior-changing stage has the four TDD steps with a concrete "confirm fail" failure mode.
3. Stages are ordered so the system is working and shippable after each one.
4. *Planning decisions taken* either says "None…" or lists only planning-level decisions, each with a rationale.
5. *Deviations from the design* either says "None" or explicitly lists differences with rationale.
6. The *Execution schedule* places every stage in exactly one batch, every parallel batch clears all seven independence tests, and no stage was reshaped to create parallelism.

If any of these still fail, loop on Step 7 until they pass.

## Step 8 — Update the tracker *(subagent)*

The tracker at `tracker_file` already exists from earlier stages. If it's somehow missing (resolver `notes` flagged `tracker_seed: skipped`), defensively copy the plugin template:

```bash
# 1. Prefer the running plugin's own copy: this skill's announced base directory is
#    .../dev-skills/<version>/skills/<slug>, so the template is at <base>/../../templates/.
# 2. Else search — the *dev-skills* form is deliberate, since installed plugins live at
#    .../dev-skills/<version>/templates/ which "*/dev-skills/templates/*" silently misses.
find ~ -path "*dev-skills*/templates/feature-tracker.html" 2>/dev/null
# cp the winner (base-dir copy first; else a plugins/cache/ match at the highest version;
# else a working clone) to <tracker_file>. Copy, never symlink.
```

If no template can be located, skip the tracker update and note it in the Step 10 summary — do **not** fail the whole run.

Apply these edits via the `Edit` tool. For each `{{TOKEN}}`, check it is still literal text in the file. Skip silently if already substituted. Note: the seeded tracker opens with an HTML documentation comment that lists every token name literally, so a bare `{{TOKEN}}` match (or whole-file grep) is non-unique and can match the comment instead of the live markup — scope each check/Edit to the rendered body occurrence (the `panel-plan` section, chip span, bullets `<ul>`, details block, or `<h1>` title), never the comment-block token.

**Header tokens** (only edit if still literal):

- `{{FEATURE_VERSION}}` → `<N>`.
- `{{FEATURE_TITLE}}` → `description` with hyphens replaced by spaces, preserving case.
- `{{FEATURE_SLUG}}` → `feature-v<N>-<description>`.
- `{{GENERATED_AT}}` → today's UTC date.

**Plan section tokens** (this skill owns these — always fill them with real content). Compute the timestamp once via `date -u +"%Y-%m-%d %H:%M UTC"` and reuse the same value for the chip. **If `/feature-storm` or `/feature-design` ran first, these are no longer the literal `{{PLAN_*}}` tokens — the earlier stage rendered them as the placeholder prose `Awaiting /feature-plan` (the chip) and two `<p class="empty">Not yet filled — pending /feature-plan.</p>` blocks (bullets + details). Overwrite those placeholder strings with the real plan content; the skip-if-substituted rule above protects only *other* skills' tokens, never your own Plan panel.**

- `{{PLAN_AT}}` → `Updated <YYYY-MM-DD HH:MM UTC>` (the timestamp chip text — no surrounding HTML).
- `{{PLAN_BULLETS}}` → an `<ul>` of 5–10 plan highlights, one `<li>` per bullet — typically the stage titles plus the *Deviations from the design* line, and one bullet naming the critical path when the schedule has a parallel batch.
- `{{PLAN_DETAILS}}` → free-form HTML rendering the plan in increasing detail, drawn from the file written in Step 5. Cover, in order: the **Overview** paragraph → the **Stages** list (one `<h3>` or `<h4>` per stage with its one-line goal and the files it touches; do not paste the full TDD step list — that's in the .md) → the **Requirements coverage map** as a `<table>` → **Cross-cutting concerns** → **Verification** → **Execution schedule** (the batch table as a `<table>` plus the critical-path line) → **Planning decisions taken** → **Deviations from the design**. Use `<h3>` for top-level section titles, `<h4>` for sub-sections, `<p>` / `<ul>` / `<table>` for content. Order content from highest-level to most detailed so a reader can stop reading at any depth.

**Other tokens** — substitute with the empty placeholder *only if still literal* (most will already be content from earlier stages):

- `{{BRAINSTORMING_AT}}` → `Awaiting /feature-storm`
- `{{BRAINSTORMING_BULLETS}}` / `{{BRAINSTORMING_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-storm.</p>`
- `{{DESIGN_AT}}` → `Awaiting /feature-design` (should never happen — design must exist for plan to run; but defend regardless)
- `{{DESIGN_BULLETS}}` / `{{DESIGN_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-design.</p>` (same caveat)
- `{{IMPLEMENTATION_AT}}` → `Awaiting /feature-implement`
- `{{IMPLEMENTATION_BULLETS}}` → `<p class="empty">Not yet filled — pending /feature-implement.</p>`
- `{{IMPLEMENTATION_DETAILS}}` → `<p class="empty">Not yet filled — pending /feature-implement.</p>`

**Progress bar** (mandatory transition — only fired in this step, after the plan document is written and reviewed; never on a `BLOCKED:` run):

- old_string: `data-stage="plan" data-state="pending"`
- new_string: `data-stage="plan" data-state="complete"`

If the Edit fails, the plan step is already `complete` (backfill on a fully tracked feature) — leave it alone.

Do **not** touch other skills' tokens beyond the empty-placeholder fallback above. Do **not** touch other skills' progress steps.

## Step 9 — Capture lessons *(subagent)*

Invoke the `lessons-capture` skill in this plugin via the `Skill` tool with the single argument `feature-plan`. It runs the reflection protocol, appends a dated entry to `~/.claude/dev-skills/lessons/feature-plan.md`, and returns the entry body for you to paste under the *Skill-improvement recommendations* heading in Step 10.

Do not run the reflection inline — `lessons-capture` is the single source of the protocol for all skills in this plugin. If the `Skill` tool is unavailable in your context, do not inline the protocol either: put the single line `lessons-capture unavailable in subagent — run it from the main agent.` under the *Skill-improvement recommendations* heading in Step 10, and the main agent will invoke it before relaying.

## Step 10 — Compose the staged summary *(subagent — this is your final message)*

Your final message back to the main agent must be exactly this block — no preamble, no trailing commentary. The main agent relays it to the user verbatim (Step 11); it is the only part of your run the user reads.

```
<Created | Revised>: <stage_file path>
**Against design:** <prereq_file path>
**Tracker:** <tracker_file path>

**Feature:** v<N> — <human-readable title>

**Stages**
1. <Stage 1 title> — <one-line goal>
2. <Stage 2 title> — <one-line goal>
...
N. <Stage N title> — <one-line goal>

**Development strategy:** test-first per stage (write test → confirm fail → implement → confirm pass).

**Design coverage:** <N>/<N> requirements mapped.

**Execution schedule:** <m> batches, <n> stages parallel-eligible, critical path <k>/<N> stages.

**Planning decisions:** <"None" or the 1–3 most consequential, one line each — full list in the plan's *Planning decisions taken* section>

**Deviations from design:** <"None" or short list with one-line rationale each>

**Top risks**
- <1–3 implementation risks, each one line>

**Next step:** <e.g. "Begin Stage 1: <title>" — single concrete action>

**Skill-improvement recommendations**
- <single item from Step 9, or the line "No skill-improvement recommendations from this run.">
```

Keep the block under ~35 lines — if the plan has more than 8 stages, group the *Stages* list by phase so the cap still holds. The file is the artifact; the summary is the pointer. If you logged deviations from the design, include on the deviations line the explicit suggestion that the user consider a new feature version via `/feature-design`.

## Step 11 — Relay the summary and offer to chain into /feature-implement *(main agent)*

First, output the subagent's Step 10 summary block to the user **verbatim** — do not compress, rewrite, or annotate it beyond fixing an obvious formatting break. This is the user's only view of the plan run.

**Report the run usage.** Invoke `usage-report` via the `Skill` tool with the argument `report feature-plan, tracker_file=<tracker_file>, feature_version=<version>`, taking both values from this skill's `feature-resolve` block. It prints the run's usage table, appends one line to the usage log and fills this stage's tracker panel. Do this *before* the offer below: on the chain-in branch this skill hands over through the `Skill` tool and never returns to the step, so a report placed afterwards would silently never run. It runs inline — **do not end your turn**, carry straight on.

Then give the user a one-click way to continue into implementation. Call `AskUserQuestion` exactly once:

- **question**: `"Continue with /feature-implement to build this plan stage-by-stage on the current branch?"`
- **header**: `"Run /feature-implement?"`
- **options**:
  - `{ "label": "Yes, run /feature-implement", "description": "Launch the implement skill against the plan just saved. It will write code and create one commit per green stage on the current branch." }`
  - `{ "label": "Not now", "description": "Stop here; the plan is saved." }`

**Which option is Recommended depends on the plan's *Deviations from the design* section** (read it from the summary's **Deviations from design:** line; open the plan file if that line is ambiguous):
- If it says "None — plan matches design v<N> exactly." → mark **"Yes, run /feature-implement"** as Recommended.
- If it lists any deviation → mark **"Not now"** as Recommended instead, and append to its description: `"Consider running /feature-design first to fold the deviations back into the design (as a new feature version) before implementing."` The user can still pick "Yes" if they want to implement against the deviated plan as-is.

If the user picks "Yes, run /feature-implement", invoke the `feature-implement` skill via the `Skill` tool with the single argument `v<version>` (the integer feature version resolved in Step 1). The implement skill's Step 1 parses the version token and delegates to `feature-resolve`, which continues into the same feature folder — no conversation-context lookup involved.

If the user picks "Not now" or "Other", emit exactly one line before stopping:

```
**Next step:** when you're ready, run `/feature-implement v<version>`.
```

Do not skip this step or substitute the AskUserQuestion with prose. The offer is the affordance; rendering it as a question is what makes it one-click. Because `/feature-implement` writes code and commits, the "Not now" path is a perfectly reasonable choice — the user can review the plan first and run the chain later. The "Next step" hint is only emitted on decline.

## Constraints (non-negotiable)

- **No plan without a design.** The plan must reference an existing design under the resolver-returned feature folder. The resolver enforces this; never bypass it.
- **Output path comes from `feature-resolve` only.** Never write to `docs/`, never construct `features/...` paths by hand. Step 1 is the single source of pathing.
- **Integer versions only.** `v<N>` everywhere — no `v<N>.<M>`. The plan version matches the feature version; there is no separate plan minor-versioning.
- **The design's open questions must be empty.** If design §8 has any open question, the run halts (`BLOCKED:`). The plan cannot resolve design ambiguity — only `/feature-design` can.
- **Report the run usage before you stop.** However this run ends — normal completion, a `BLOCKED:` halt, a refusal, or an error surfaced to the user — invoke `usage-report` with `report feature-plan, outcome=halted` before you stop (Step 11's normal path passes `outcome=completed` instead). Step 2 covers the `BLOCKED:` relay; this covers every other exit. The window is the main agent's alone — the planning subagent never opens or closes it.
- **TDD is non-optional for behavior-changing, host-testable stages.** Stages in a sanctioned non-red-first category (Step 5) carry their category label and one-line justification; everything else follows write → fail → code → pass.
- **The planning core never prompts the user.** Steps 3–10 run without `AskUserQuestion` — in the subagent it is impossible, and the policy holds even in the direct-execution fallback. Only Steps 0, 1, and 11 may prompt, and only from the main agent.
- **No silent scope or decision changes.** Divergence from the design lives in *Deviations from the design*; autonomous planning-level choices live in *Planning decisions taken*; both are surfaced in the Step 10 summary. Design-level ambiguity is never decided unilaterally — it halts.
- **Tracker edits are defensive.** Substitute only tokens still literal `{{...}}`; never overwrite content placed by `/feature-storm`, `/feature-design`, or any other skill. The progress bar's `data-stage="plan"` entry is this skill's alone to touch — and only on a successful run.
- **Lessons capture runs every time.** Step 9 always invokes `lessons-capture` from the subagent (or, when the Skill tool is unavailable there, the main agent runs it during Step 2's verification); whether it produces a recommendation or "none this run" is decided by that skill.
- **No symlinks.** If a defensive tracker template copy is needed in Step 8, always copy — never link.
- **Never paste the entire plan into chat.** Step 10's block is staged highlights only, and Step 11 relays it unmodified; the user opens the file for full content.
- **Parallelism never reshapes stages.** The *Execution schedule* groups the stages Step 5 cut; it never splits, merges, or invents a stage to gain parallelism, and any doubt about a pair's independence resolves to serial.
