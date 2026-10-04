---
name: understand
description: '[Process] Use when a developer needs to understand and judge scoped work: a change set, subsystem, decision, plan or concept — flow, rationale, trade-offs, testing. Bugs: investigate --mode=debug; one feature''s code flow: investigate.'
disable-model-invocation: false
---

> Codex compatibility note:
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Host-native execution: Codex runs a skill by loading its `SKILL.md` instructions and executing the required steps with available tools. No separate `Skill` tool is required; a loaded skill is already activated.
> - Source vs execution: prefer the registered `.agents/skills/<name>/SKILL.md` for Codex execution. `.claude/**` remains the canonical authoring source; reading it for a registry or source inspection does not switch this session to Claude Code.
> - Capability check: interpret Claude tool names through the active host before declaring a blocker. Continue when Codex can perform the required operation; stop and ask only when the actual capability is unavailable, naming the step and evidence. Host-native execution is not a protocol deviation and needs no extra approval.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - Use ask user tool to ask user.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, steps follow the guided contract in `$start-workflow` (gate steps fixed; other steps may flex with a logged reason); report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.
<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Teach developers to review and judge any scoped work—not merely accept it—by showing what changed, how it flows, which stories/rules it protects, where to start, why this solution, alternatives/trade-offs/impact, how to test and demo it, decision levers, and written challenges, in a full report whose scope changes group count, not sections.

**Summary:** Read this if nothing else. Explain whatever the prompt names, at **ANY scope** — one decision, one subsystem, a 60-file change set, or the whole project — and leave the reader able to judge it. Scope flexes by growing the number of **understanding groups**; the report contract never flexes. Main steps, in order:

1. **RESOLVE scope** from the prompt (bare `$understand` → current tasks + working-tree changes). State it in one line; on ambiguity infer and proceed, **never ask**.
2. **LOAD the three contracts** — `report-template.md` · `diagram-catalog.md` · `review-path.md`.
3. **SIZE the target → a scope tier S0–S4** from files · capabilities · contexts, and announce the tier.
4. **DECOMPOSE into understanding groups** (≥2 from tier S2) — each explainable on its own, ≤8 files / ≤2000 diff-lines — and load `references/scale-protocol.md` at tier ≥ S2.
5. **BREAK THE WORK INTO TASKS before the first deep read** — the current task list first, then one task per group plus the fixed spine tasks; exactly one `in_progress`; a group task completes only when its block is **on disk**.
6. **GATHER the six inventories**, per group — diagram sources · stories + REAL test IDs · route classification · concepts · option space · demo & run evidence — **delegating to read-only investigation skills** (`$investigate`, `$investigate --mode=debug`, `$graph-code --mode=trace`) when a direct read cannot fill one.
7. **ORDER on two axes** — narrative leverage (governs §5–§10) and contract-inward route (governs §4). Never conflate them.
8. **OPEN the report before writing section one** — **ONE file at every tier**; at ≥2 groups the spine region sits at the top of that file and one `# G{n}` block is appended per group, in the same file.
9. **ACCUMULATE group by group** — investigate → analyze → append that group's block → update the spine ledger → complete the task. Never hold the report in context, never batch the write.
10. **SYNTHESIZE across groups** — the group map, the group order, cross-cutting trade-offs and blast radius, the whole-scope challenge.
11. **SUMMARIZE in chat** — plus the report path, plus anything dropped — and append the index line. Never quiz, never block.

**Deliverable:** a full review guide written to `tmp/reports/understand-{YYMMDD}-{HHmm}-{slug}.md` (git-ignored working artifact), **plus** an in-chat executive summary — and the report path whenever a file was written (Step 3 delivers every section in chat instead when it finds no git-ignored directory for the report). It reads **high level first, detail later**, opening with the summary and then the four parts:

- **§0 — Detailed Summary:** the read-only-this section — what the change is, what you need to know, where to start, and the one thing to double-check. Written LAST, from the finished sections.
- **Part I — Orient:** §1 What Was Done · §2 Visual Map · §3 User Stories & Business Rules — the picture and the business, before any code.
- **Part II — Route:** §4 Review Path — where to start reading, in what order, and what to answer at each stage.
- **Part III — Depth:** §5 Concepts You Need · §6 How It Works · §7 Why This Solution · §8 Options Considered · §9 Trade-offs Accepted · §10 Impact & Blast Radius.
- **Part IV — Prove & Push Back:** §11 Test & Demo · §12 Your Call · §13 Challenge This.

Section shape and authoring rules: `references/report-template.md`. Diagram contract: `references/diagram-catalog.md`. Route contract: `references/review-path.md`.

**Scope is prompt-driven — flexible for all cases:**

- **Default (bare `$understand`, no target named):** explain the **current working context** — the active tasks (the current task list) and the working-tree changes (`git diff`), plus any active plan or `$watzup` summary. "Here's what we're working on, what changed, and why."
- **Targeted (prompt names something):** explain exactly that — a plan, a change set/PR, a subsystem, a single design decision, a concept, a bug, "why X over Y". Read the prompt, derive the target, gather only that material.
- **Ambiguous:** **do NOT ask** — infer the most likely target (default to the current working context), state the assumption in one line, and proceed.

**Workflow:** Resolve scope/style/contracts → size and decompose the target → create tasks before deep reading → gather six evidence inventories → order narrative, review route, and groups → open and incrementally write the one report → teach every section and synthesize → summarize in chat and close without a quiz or loop.

**Key Rules (the contract — read these first):**

- **DERIVE SCOPE FROM THE PROMPT.** What to explain is whatever the developer asked about; if they asked nothing specific, default to the current tasks + changes in context. Never force a fixed agenda.
- **NO MODE — ALWAYS THE FULL REPORT.** There is no `--mode`, no light variant, no summary-only path, no opt-out. Every invocation produces every section, every mandatory diagram, and the review path. Scope flexes; the contract does not.
- **ANY SCOPE — SIZE IT, THEN GROUP IT.** Every run sizes its target into a scope tier (Step 0.4) before reading it, and every target above tier S1 is decomposed into **understanding groups** — explainable units, each carrying its own answers. A bigger target buys **MORE GROUPS, never FEWER SECTIONS**: "too big to explain properly" is the one conclusion this skill may never reach. — why: the failure mode of a large target is a report that silently thins into a summary, which is exactly the description-instead-of-teaching failure the skill exists to prevent.
- **BREAK THE WORK INTO TASKS BEFORE THE FIRST DEEP READ.** the current task list first (resume, never duplicate), then one task per group plus the fixed spine tasks, exactly one `in_progress`, and a group task completes **only when its block is on disk**. — why: the gather-and-write phase is where long runs die, and a task list built afterwards records nothing about where it stopped.
- **DELEGATE THE GATHERING, NEVER THE TEACHING.** When read + grep + trace cannot fill an inventory, invoke the repo's own **read-only** investigation skills (`$investigate` to locate and explain existing behavior, `$investigate --mode=debug` for a live defect's cause, `$graph-code --mode=trace` / `$graph-code --mode=blast-radius` for reach) and feed their output in as INPUT — re-verified against `file:line` before it becomes a report claim. NEVER delegate to a skill that mutates files or issues findings/verdicts, and never let a delegate author a section. — why: this skill emits no findings and mutates nothing; a delegate must not smuggle either in, and a claim that passed through another skill is still a claim you must be able to cite.
- **ACCUMULATE ON DISK, NEVER IN CONTEXT.** Open the report before writing section one; append per section and per group; update the ledger as each block lands; synthesize the scope-wide sections **from the written blocks**, never from memory. A report held in context until the end is a report one cutoff away from nothing. — why: partial results on disk beat complete results that never got written.
- **TEACH, COACH, AND ROUTE — the developer must be able to JUDGE, not just follow.** A description of what the code does is a FAILED run. Teaching = the reader could re-derive the design. Coaching = the reader is handed the levers and the counter-arguments needed to disagree on evidence. Routing = the reader knows which file to open first, what to check there, and what they must be able to answer before moving on.
- **ALL SECTIONS, AT EVERY SCOPE TIER.** Part I What Was Done → Visual Map → User Stories & Business Rules; Part II Review Path; Part III Concepts → How → Why-this-solution → Options-considered → Trade-offs → Impact; Part IV Test & Demo → Your-call → Challenge-this. Every report includes all sections, mandatory diagrams, and review stages regardless of scope tier.
- **DIAGRAMS ARE MANDATORY, AND DERIVED — NEVER DRAWN FROM EXPECTATION.** §2 always carries a system flowchart, a domain ERD, and a sequence diagram per main flow, each built from a graph trace, a read call site, or an existing spec diagram. A mandatory diagram that cannot be derived degrades to a **stated blocker** — never to silence, never to an empty fence, and never to plausible-looking invented nodes. Contract: `references/diagram-catalog.md`.
- **REAL IDs ONLY — NEVER INVENT A TEST CASE.** Every `TC-*` / test ID in §3 and §11 is one that actually exists in the specs or the test code. A story or case with no test says _"no test covers this"_ and is recorded as a coverage gap. A fabricated case ID is worse than an admitted gap: it retires a risk that is still live.
- **ALTERNATIVES ARE MANDATORY, WITH PROS AND CONS EACH.** Every significant decision lists ≥2 alternatives beyond the chosen one — each with specific pros, specific cons, cost-to-switch-later, and the disqualifying reason — or an explicitly argued statement that the option space is genuinely empty. The chosen option MUST list real cons too. Generic pros/cons ("cleaner", "faster") are a failed section. Label each option `[deliberated]` (weighed during the work) or `[reconstructed]` (surfaced now, after the fact) — **NEVER invent a deliberation that did not happen.**
- **PROVOKE THINKING IN WRITING — NEVER INTERROGATE.** The report MUST end with rhetorical challenge prompts, a named weakest link, and a pre-mortem, so the reader pressure-tests the work. These are **written provocations, not tool calls**: NEVER use ask user tool, NEVER quiz or ask for teach-back, NEVER wait for an answer, NEVER gate anything on a reply. Provoke on paper; the developer answers at their own pace or not at all. On an ambiguous target, still do not ask — infer, state the assumption, proceed.
- **STANDALONE, NEVER BLOCKS.** This skill can be invoked directly or as a wrap-up handoff from `$watzup`. It teaches and ends; it never traps the developer in a loop or prevents commit/workflow progress.
- **EXPLAIN THE WHOLE SCOPE, LEAD WITH THE NON-OBVIOUS.** Cover everything in the resolved scope, but order by leverage — open with the highest-blast-radius, highest-future-change-cost, most-surprising parts; treat boilerplate/CRUD/mechanical edits briefly. Depth is the goal; ordering is the optimization.
- **READ-ONLY on code & plans; writes ONLY git-ignored working artifacts.** This skill never edits source, plan, or doc files. Its only write targets are git-ignored working artifacts — the teaching report at `tmp/reports/understand-{YYMMDD}-{HHmm}-{slug}.md` and the resumable index at `tmp/understand/{branch}-index.md` (see Step 3) — never in `.claude/`, the source tree, `docs/`, or any git-tracked path. When an artifact's candidate directories are all git-tracked it writes **nothing there** and reports the skip (Step 3): the constraint is what holds, never a fixed count of files.
- **NO SECRET VALUES, ANYWHERE.** Diagrams, stage tables, and run/demo commands name the setting, the file, and the class of check — never a credential, token, key, connection string, or customer identifier. Secrets render as `<redacted:…>` placeholders from the moment they would enter context (Step 1 inventory 6), not at write time.

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

---

# Understand — Prompt-Driven Review Guide, Teaching & Coaching Explainer

You are a **teacher, a coach, and a router**, in that order.

- **As a teacher** you make the human deeply understand what happened: the motivation, the technical concepts they need, the mechanics, the business logic, the edge cases. You name a concept before you use it. You go first principles before jargon, concrete before abstract, and you offer an analogy for anything genuinely dense. You **draw** it before you describe it — a picture orients a reader in seconds that prose cannot in paragraphs.
- **As a coach** you make the human able to _judge_ it: you lay out the options that existed and what each would have cost, you name what the decision paid for and what it paid with, you hand over the levers they'd pull to change it, and you write down the sharpest questions a hostile reviewer would ask — so they can push back on evidence instead of rubber-stamping AI output.
- **As a router** you make the human able to _review_ it: you tell them which file to open first and why, what to check there, what a red flag looks like, and what question they must be able to answer before moving to the next group. A route is **directive**, not explanatory — "open these three files; you should be able to state the invariant before you continue", never "the domain layer is important".

> **The bar:** a developer who reads the report could (a) re-derive the design themselves, (b) argue for a different option and say what it would cost, (c) name the weakest part of the work, and (d) sit down and review the change in the right order without asking anyone where to start. Anything less is a description, not teaching.

**One-way, never interrogating.** You do the teaching and the provoking; the developer reads. The challenge questions in §13 are **rhetorical and written down** — you never call ask user tool, never quiz, never ask for teach-back, and never wait for or gate on a reply.

## Step 0 — Resolve Scope and Plan the Report (do this first, cheaply)

1. **Derive the scope from the prompt.** Read what the developer actually asked and pick the target:

   | Prompt signal                                                 | Scope to explain                                                                                                                                                                  |
   | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | Bare `$understand`, no target named                           | **Default: current working context** — active tasks (the current task list) + working-tree changes (`git diff --name-only` + untracked) + active plan / latest `$watzup` summary if present. |
   | Names a change set / PR / "what I just did" / "these changes" | The diff and its rationale.                                                                                                                                                       |
   | Names a plan / "the approach" / "before we build"             | The active plan: problem, approach, rejected alternatives, risks, phase order.                                                                                                    |
   | Names a subsystem / file / feature / "how does X work"        | That code path — read the files (optionally a graph trace as a stale-able hint), explain the flow.                                                                                                             |
   | Names a single decision / "why X over Y"                      | That decision and its trade-offs.                                                                                                                                                 |
   | Names a concept / bug / error                                 | That concept or root cause.                                                                                                                                                       |
   | Ambiguous / multiple plausible targets                        | **Do NOT ask.** Infer the most likely target (default to current working context), state the assumption in one line, and proceed.                                                 |

   State the resolved scope in one line before continuing (e.g. `Explaining: current working changes (3 files) + active task #42`).

2. **Load all three contracts.** Read them before gathering — the shape of the report determines what you must collect, so improvising it from memory guarantees a thin section:

   | Reference                       | Supplies                                                                                                                                                             |
   | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `references/report-template.md` | The section skeleton, the four parts, the options/pros-cons table format, the provenance labels, and the pre-write self-check |
   | `references/diagram-catalog.md` | Which diagrams are mandatory, how each is derived from real evidence, the provenance marking, size discipline, and what to emit when one genuinely cannot be derived |
   | `references/review-path.md`     | The layer taxonomy, the deterministic ordering algorithm, the context-inclusion rule, and the eight fields every review stage must carry                             |

   **If a contract file is missing** (a partial distribution, a vendored copy, an incomplete mirror sync), **degrade — never silently, and never by skipping the work it governs.** Say which file is absent in one line — *"`references/diagram-catalog.md` not found — running on the inline contract; diagram derivation detail unavailable"* — and fall back to the inline contract in this file: the mandatory diagram set and provenance rule at the §2 row of the section table, the eight-field stage rule at the §4 row, and the section order + code-free forms below. The report is still owed in full; only the elaboration is lost. This is the same rung every other input in this skill ends on (diagram sources, stories/TCs, route classification, run commands, write location) — a stated blocker, never a silent gap.

3. **Size the target BEFORE you read it (cheap signals only — this step costs seconds).** Count, do not estimate: in-scope **files** (`git diff --name-only` + untracked, or a glob of the named area), distinct user-facing **capabilities/flows**, distinct **modules / bounded contexts** (`docs/project-config.json` → modules), and **changed lines** where a diff exists. Read the tier off the table — **first row whose trigger matches, top-down, highest tier first** (promote before dispatch if subsequent decomposition exceeds the selected tier; a point request does not override measured scale) — and announce it in one line (`Scope: S3 · Large — 63 files, 9 capabilities, 4 modules → 8 groups`).

   | Tier | Trigger (first match wins) | Understanding groups | Report shape | How the work runs |
   | --- | --- | --- | --- | --- |
   | **S4 · Program** | Whole repo · multi-service · "explain the project" | Grouped per context, nested | One file | Group agents in waves → context synthesizers → spine |
   | **S3 · Large** | > 40 files **OR** > 6 groups | 6–12 | One file | One sub-agent per group, **every group spawned in ONE wave**, front-loaded fragment writes |
   | **S2 · Multi** | ≥ 10 files **OR** ≥ 2 capabilities/flows/contexts | 2–6 | One file | **Gather fans out** — one read-only gather agent per group, all in ONE wave; orchestrator authors inline from the returns |
   | **S0 · Point** | One file, one decision, one concept, one error | 1 | One file | Inline, section by section |
   | **S1 · Small** | < 10 in-scope files, one capability | 1 | One file | Inline, section by section |

   > The thresholds are the framework's existing map-reduce ladder (`SYNC:systematic-review-batching`: < 10 sequential · ≥ 10 batch · > 6 categories or > 40 files hierarchical), **adopted deliberately** so `understand` and the review skills never partition the same target two different ways. What differs is only the unit and the output: this skill batches by **explainable group** and emits **teaching**, never findings. — why: a developer who runs both skills on one change should meet the same boundaries twice, not two competing maps.

   Scope tier determines how many groups exist, where the report lives, and how the work is dispatched. It NEVER removes a section, a mandatory diagram, or a review stage. S0 is a legitimate, common outcome; so is S4.

4. **Decompose into understanding groups, then break the work into TASKS — before any deep read.**

   - **A group is an explainable unit** — its own §1–§13 are answerable about it alone, its name has no "and" in it, and it fits ≤ 8 files **or** ≤ 2000 diff-lines. Decomposition axis, first rung yielding ≥2 cohesive groups: **module/bounded context** → **capability/story cluster** → **end-to-end flow** → **layer slice** (horizontal sweeps only) → **directory** (last resort, labelled *"structural grouping — not a conceptual boundary"*). MUST ATTENTION record which rung you landed on — the reader calibrates on it exactly as on a grep-derived route. Tier S0/S1 → exactly one group, and this collapses to the classic single-file report with zero overhead.
   - **[BLOCKING] Create the task list BEFORE gathering.** the current task list FIRST — an interrupted or compacted run **resumes its tasks, never duplicates them**. Then create one task per group plus the fixed tasks: *size & decompose · scope-wide gather · open report + ledger · {one per group} · cross-group synthesis · chat summary + index · contract self-check*. Exactly one `in_progress`; transition it before the work and `completed` immediately after the evidence exists. **A group task completes ONLY when that group's block is on disk** — evidence is the path plus the sections it carries, never a summary in context. At S0/S1 still create one task per report part (I·II·III·IV). — why: a run that dies mid-report must show the reader exactly where it stopped, at every size.
   - **Decompose to the FINEST unit that still explains something.** Do not stop at the coarsest split that clears the group tests — a group holding 8 loosely-related files is two groups pretending to be one, and it serialises work that could have run concurrently. Push down the decomposition axis one more rung whenever the result still yields cohesive, individually-explainable groups. More, smaller groups = more parallel width and a finer resume point; the ≤12-per-level guard and the nesting rule bound the count. — why: decomposition width IS the parallelism budget — a target split into 3 groups can never run 8-wide, no matter how many agents are available.
   - **[BLOCKING at S2+] Tag every task `PAR` or `SEQ`, then declare the waves — BEFORE dispatching any of them.** `PAR` = its inputs do not include another pending task's output AND its write target is disjoint from every other `PAR` task; everything else is `SEQ` and must name the dependency that forces it. The fixed task set classifies the same way on every run:
   - **S2 never assigns fragment ownership:** gather agents return bounded evidence only and the orchestrator authors the one report. Fragment paths begin at S3+.

     | Task | Mode | Why |
     | --- | --- | --- |
     | size & decompose | `SEQ` | every other task consumes its group set |
     | scope-wide gather · open report + ledger | `PAR` | one is read-only, the other writes only the report skeleton — disjoint targets |
     | {one per group} | **`PAR` — the main wave** | each group reads its own file list and writes its OWN fragment; no shared write target |
     | cross-group synthesis | `SEQ` | consumes every group block |
     | chat summary + index · contract self-check | `SEQ` | consume the finished report |

     Announce it in one line before the first spawn — `Parallel plan: wave 1 = [scope gather, open report+ledger] · wave 2 = [G1…G8] · SEQ = [synthesis, summary, self-check] (each consumes the whole wave)` — then spawn **every member of a wave in ONE message**, never dripped one per turn, and honour the barrier: advance only after EVERY member returns. — why: a declared wave is checkable; an undeclared one silently degrades into the sequential run it was meant to replace.

   > **Scale Protocol** — grouping algorithm and the three group tests · group ordering (contract-inward at group altitude) · the exact task set · the accumulation ledger and write order · resumability after a cutoff · sub-agent fan-out rules at S3+ · caps and the no-silent-truncation rule · the degradation ladder.
   >
   > **At tier ≥ S2, MUST ATTENTION READ `references/scale-protocol.md` now** — before gathering. At S0/S1 skip it; one group needs none of it. Missing file → degrade exactly as in item 3: say so in one line and run on the inline rules above.

## Step 1 — Gather the Material

Gather **only** what the resolved scope needs:

- **Current working context (default):** the current task list for active tasks; `git diff --name-only` (+ untracked via `git ls-files --others --exclude-standard`) for the change set; the active plan and latest `$watzup` summary if they exist. Extract: what's being worked on, what changed, why, new behavior.
- **A plan:** read the plan files (`plan.md` + `phase-*.md` from the Plan Context / configured plans dir). Extract: problem, chosen approach, rejected alternatives, design decisions, risks, phase order.
- **A subsystem / feature / "how does X work":** read the relevant files to map the call/flow chain (optionally `python .claude/scripts/code_graph trace <file> --direction both --json` as a stale-able hint). Extract: entry points, data flow, key invariants.
- **A single decision / "why X over Y":** the relevant code + its rationale (comments, git blame, the plan's alternatives section).

Keep gathering proportional to scope — don't read the whole repo to explain one decision.

**Portable discovery — resolve locations, never hardcode them.** Read `docs/project-config.json` (and the project-reference docs it points to) for source roots, spec/feature-doc location, test locations, and run commands. This skill runs on repos it has never seen; a hardcoded framework path is a guess wearing a citation. Where a source is absent, walk the degradation ladder stated per inventory below and **record which rung you landed on** — the reader calibrates on it.

**Delegate the GATHERING when a direct read cannot fill an inventory — never delegate the TEACHING.** Read + grep + trace fills most inventories. When it does not — you cannot locate the relevant files in an unfamiliar repo, the mechanics of an existing feature need a real investigation, a live defect's cause is unknown — invoke the repo's own read-only investigation skills and feed their output into the inventories below. Every section of the report is still authored **here**.

| The gather step needs… | Invoke | Feeds |
| --- | --- | --- |
| Where the relevant files even are, across a large or unfamiliar codebase | `$investigate` | Step 0.5 group decomposition + each group's file list |
| How an existing feature or subsystem actually works, beyond what one read shows | `$investigate` | §6 How It Works · §7 Why This Solution · §5 Concepts |
| The root cause of a live, un-fixed defect | `$investigate --mode=debug` | §6 · §8 candidate causes with evidence for and against |
| The call/flow chain and its reach | `$graph-code --mode=trace` · `$graph-code --mode=blast-radius` | §2 D1/D3 · §10 Blast Radius · Step 2 Axis A |
| Which spec owns a capability, when finding it is itself the problem | `$spec [mode=index]` | §3 stories + REAL `TC-*` IDs · §11 cases |

1. **Read-only delegates ONLY.** NEVER invoke a skill that mutates files or issues findings/verdicts (`$fix`, `$changes-review`, `$code-quality-review`, `$why-review`, `$plan --mode=execute`) — this skill emits no findings and mutates nothing outside its own git-ignored artifacts, and a delegate must not smuggle either in through the back door.
2. **MUST ATTENTION delegate on evidence of need — NEVER by reflex.** Try read + grep + trace first, within the group's budget. Announce each delegation in one line and record it in the report header — `Delegated: $investigate — G3 mechanics` — why: the reader calibrates on the provenance chain exactly as they do on a grep-derived route.
3. **A delegate's output is INPUT, never a finished section.** Re-verify every claim you carry forward against `file:line` before it becomes a claim in the report; a `TC-*` ID that arrives through a delegate is still one you must have read yourself. The anti-hallucination bar does not relax by passing through another skill.
4. **At tier S3+, delegation happens INSIDE the group's sub-agent**, never in the orchestrator — why: delegating from the orchestrator pulls a whole investigation transcript back into the one context the grouping exists to protect.

**Then gather the six things a description-only pass always skips.** Each feeds a named section; a skipped inventory produces a thin section, which the Step 4 gate will reject.

1. **Diagram sources (feeds §2).** Collect the evidence each mandatory diagram is built from: `python .claude/scripts/code_graph trace <file> --direction both --node-mode file --json` for the component map; an existing spec `erDiagram` (lift it verbatim — the cheapest correct source) else the entity/model class fields else the migration/schema files for the domain model; the flow entry points and their handler chains for the sequences. Note any entity carrying a `status`/`state`/`phase` field, a lifecycle enum, or a transition guard — that, and only that, fires the state diagram. _Ladder:_ graph trace → grep + read the call sites → spec/plan text → **state the blocker**. Never a fifth rung of invention.
2. **Story & test-case inventory (feeds §3, and §11's cases).** Identify the **main** user-facing capabilities in scope — the "As a … I want … so that …" the change delivers — and for each, the business rule or invariant it protects and where that rule is enforced (`file:line`). Then collect the **real** cases that prove it: spec `TC-*` IDs and/or the integration/unit/e2e `it`/`[Fact]` test names and scenarios. **Use the actual IDs — never invent case numbers.** Reconcile the union of spec TCs and test-code cases; a story with no case is a coverage gap to report, never a gap to fill with a plausible ID. _Ladder:_ specs → tests → PBIs/release notes/commit messages → the diff itself.
3. **Review-path classification (feeds §4).** Assign every in-scope file to a layer bucket per `references/review-path.md` (contracts/API · domain · application · persistence · integration · UI · tests · config/generated), then walk **one hop outward** and admit the unchanged files a reviewer needs in order to judge the changed ones — the invariant owner, the interface satisfied, the base-class contract, the governing spec/TC. Mark every such file as context, not as a change. _Ladder:_ graph trace → grep of imports/references, in which case the emitted route must carry its approximation label.
4. **The concept inventory (feeds §5).** List every technical concept, pattern, or mechanism a reader must hold in their head to follow the flow — CQRS, optimistic concurrency, debounce, idempotency key, event sourcing, memoization, whatever is actually in play. Keep every load-bearing one — however many that is, with no maximum; drop decoration. For each, find where it is visible in this codebase (`file:line`) so the concept is taught against real code, not in the abstract.
5. **The option space (feeds §8).** For each significant decision, reconstruct what ELSE could have been done. Sources, in order of strength:
   - the plan's rejected-alternatives section, ADRs under the ADR root (default `docs/adr/`; a `docsRoots.adr.path` entry in `docs/project-config.json` overrides the path), PR/commit messages, code comments saying "instead of"/"we tried";
   - `git log`/`git blame` on the touched lines — a prior implementation IS an alternative, and its removal is evidence;
   - **3+ sibling patterns already in this codebase** solving the same shape of problem differently (grep/glob) — the strongest alternatives are the ones the repo already demonstrates;
   - the framework/library's other supported approach for the same job;
   - your own engineering judgement — the approach a competent engineer would have reached for first.

   **[ANTI-HALLUCINATION]** Mark each option `[deliberated]` only when you have evidence it was actually weighed during the work. Everything else is `[reconstructed]` — surfaced now, for the developer's judgement. NEVER dress a reconstruction up as a deliberation; a fabricated decision history is worse than none.

6. **Demo & run evidence (feeds §11).** Collect the project's own test/run commands from `docs/project-config.json`, the seed/fixture paths that stage a scenario, and — per main case — how the domain **stores or changes** the data that makes the case work: the persisted field/column/table, the entity or migration that owns it, and the rule that consumes it to produce the outcome (`file:line` each). Read the code; do not infer persistence from names. A display-only case states _"no storage change"_ and describes the computed representation instead. _Ladder:_ `project-config.json` → the CI workflow's own commands → the test runner's manifest (`package.json` scripts, `*.csproj`, `Makefile`) → **state that you could not resolve a command** rather than guessing one.

   > **[SECURITY]** Record every command in **placeholder form**. Environment variables, connection strings, tokens, keys, and customer identifiers are referenced by NAME and rendered `<redacted:…>` — never by value. This is the point where a secret would first enter context, so it is the point that must refuse it.

## Step 2 — Order the Material (two different axes — do not conflate them)

You will explain the **whole** resolved scope. Two orderings come out of this step, and they answer different questions:

**Axis A — narrative depth order (which topics get the most words).** Order by leverage; open with what matters most, compress the rest:

- **Blast radius:** assess by grep/read of callers on the key files in scope (optionally `$graph-code --mode=blast-radius` or `python .claude/scripts/code_graph trace <file> --direction both --json` as a stale-able hint). High upstream/downstream reach → explain first and in most depth.
- **Future-change-cost:** decisions expensive to reverse later (schema, public contract, cross-service message, shared/framework layer) → high priority.
- **Surprise:** anything a competent engineer would NOT guess from the task description — a non-obvious trade-off, a preserved edge case, a "we did X instead of the obvious Y because Z" → call these out explicitly.

Boilerplate, generated code, and mechanical renames get a one-line mention, not a deep dive. Nothing in scope is silently omitted — but depth follows leverage.

**Axis B — review route order (which files a human opens first).** Order **contract-inward**, per `references/review-path.md`: start at the layer that defines _meaning_ (API contract, then domain invariants), walk outward through application → persistence → integration → UI, tests last, config/generated collapsed into one final skim. Blast radius is the **tie-break between peers here, not the primary axis**.

**When the two disagree, each governs its own output — never borrow one for the other.** A shared utility with the widest blast radius leads Axis A: it gets the deepest explanation in §6 and §10. It does NOT lead Axis B: a route that opens with a util file drops the reviewer into mechanism before they know what the change is supposed to _mean_, and they cannot tell a correct edit from an incorrect one. The entity that owns the invariant leads the route even when its reach is small. Axis A orders §5–§10; Axis B orders §4.

**At multi-group scale both axes run INSIDE each group, and a third ordering appears ABOVE them: the group order.** Groups are ordered contract-inward at group altitude — the group owning the shared contract or domain invariant first, then dependencies before dependents, cycles broken at the weakest edge and said out loud, peers tie-broken by blast radius, and the ungrouped remainder (config, generated, boilerplate) collapsed into one final skim group. That single ordering governs three things at once — the task order, the write order, and the spine's group route — so they can never disagree (`references/scale-protocol.md` §2).

## Step 3 — Open the Teaching Report (write incrementally, never in one final batch)

> **[HARD RULE] Write ONLY git-ignored working artifacts — NEVER inside `.claude/`, the source tree, `docs/`, or any git-tracked path.** This skill mutates no source, plan, or doc file.

Two artifacts, different jobs:

| Artifact | Path | Job |
| -------- | ---- | --- |
| **Teaching report** (the deliverable) | `tmp/reports/understand-{YYMMDD}-{HHmm}-{slug}.md` — **one file, at every tier** | The full review guide the developer keeps, re-reads, and argues with. Matches the framework-wide report convention. Directory resolved by the rules below — the plans root (default `plans/`; a `docsRoots.plans.path` entry in `docs/project-config.json` overrides the path) is git-ignored in this repo, but that is verified, never assumed. |
| **Understanding index** (resumability) | `tmp/understand/{branch}-index.md` | Append-only one-line-per-session log: date · scope · report path · one-line takeaway. Makes a branch's learning history browsable. Use `temp/…` if the project already uses `temp/`; create the `understand/` subdir if absent; `{branch}` = current branch with `/` → `-`. **The `-index` suffix is load-bearing:** `$investigate --mode=explain` owns `tmp/understand/{branch}.md` for a different, multi-section Problem/Solution/Impact format (`investigate/SKILL.md:247`) — sharing the directory is intended, sharing the file would interleave two incompatible shapes. |

**Create the report file BEFORE writing the first section**, then append section by section as you produce it. **Append-per-section is mandatory, not advisory.** The report is long and the diagrams are the expensive part — a long run that dies mid-way must leave the finished sections on disk. Never hold the whole report in context and write once at the end.

**At ≥2 understanding groups the report is a SPINE REGION plus one BLOCK per group, all inside that ONE file** — the tier changes how many groups exist and how the work is dispatched, never how many files come out. Layout, spine skeleton, block skeleton, and the >12-group nesting rule are owned by `references/report-template.md` → *Scaled report layout*. Do not improvise a second layout, and do not re-split the file for size.

**Write order is fixed:** spine FIRST — header, resolved scope + tier, the group ledger with every row `pending`, and **reserved stub headings** for the scope-wide sections → then group by group in the Step 2 group order (investigate → analyze → write that group's block → update its ledger row to `written` with its path and one-line takeaway → complete that task) → then fill the reserved scope-wide stubs **from the written blocks** → then the chat summary and the index line. NEVER hold more than the current group in context; read a finished block back from disk when you need it again. — why: the scope-wide sections belong at the top but can only be written last, and reserving them keeps the file coherent at every intermediate moment.

**After a cutoff, compaction, or resume:** the current task list → read the ledger → **verify every `written` row against the filesystem** (the file exists AND carries its sections; an absent or truncated block resets to `pending`) → re-read the contracts → continue at the first unfinished group. NEVER restart a finished group, and never re-derive a written block from memory (`references/scale-protocol.md` §5).

> **[NO SILENT TRUNCATION]** If any cap, budget, or interruption leaves part of the resolved scope uncovered, name what was deferred or dropped **in the spine AND in the chat summary** — *"G7–G9 (integration layer, 22 files) deferred — not covered by this report."* — why: bounded coverage that reads as complete coverage makes the reader retire a risk nobody examined.

**Resolving the write location (the HARD RULE above is absolute — a tracked path is never an option):**

1. **Resolve a directory PER ARTIFACT — the report and the index succeed or fail independently.** Report candidates, in order: the directory `docs/project-config.json` names for reports/working artifacts **IF it names one** (the project's own map beats a hard-coded default — but most configs name none; absent the key, fall straight through and NEVER map some other key onto the role), then `tmp/reports/`. Index candidates: `tmp/understand/` (or `temp/understand/` when the project already uses `temp/`).
2. **Take the FIRST candidate that is git-ignored**, creating it if absent — never a hard-coded name, and never the first candidate merely because it is first. If an earlier candidate was skipped because it is tracked, say so in one line — *"configured directory `{X}` is git-tracked; using `{Y}` instead"* — so a project never silently loses its own configuration.
3. **If NO candidate for an artifact is git-ignored**, do not write **that artifact** — every candidate path is tracked, and the HARD RULE above admits no exemption. **Report:** deliver every section in chat and report the blocker in one line — *"No git-ignored working directory — add the plans root (default `plans/`; path from `docsRoots.plans.path` in `docs/project-config.json`) to your git-ignore to get the report as a file."* **Index:** skip the append and say so once — *"Understanding index skipped — `tmp/` is not git-ignored."* The teaching is never withheld; only the file is. This mirrors `watzup`'s pattern of reporting a blocker rather than silently degrading.

**HTML output (on request).** When the caller asks for HTML, also write the same report as self-contained HTML next to the `.md` (`understand-{YYMMDD}-{HHmm}-{slug}.html`, same directory and HARD RULE), reusing the styling of `.claude/skills/watzup/references/session-report-template.html` — inline CSS, no external assets. Then open it with `node .claude/scripts/open-report.cjs <path>`, which opens nothing in CI or headless sessions and always exits 0. The `.md` stays the deliverable Step 5 summarizes; the chat names both paths.

## Step 4 — Teach, Coach & Route: the Report (the deliverable)

Follow `references/report-template.md` for the skeleton, the options table, the provenance labels, and the self-check; `references/diagram-catalog.md` for §2; `references/review-path.md` for §4. Every section is mandatory for every scope tier. Cite `file:line` for every concrete claim, and state confidence where a claim rests on inference.

The report runs **high level first, detail later** — the summary, then four parts:

| § | Section | What you MUST deliver |
| --- | --- | --- |
| 0 | **Detailed Summary** | The read-only-this section, and the first thing in the file: the purpose in one sentence, the change in one paragraph in **behavior** terms, a **what-you-need-to-know** bullet per load-bearing item — key mechanic, business rule at stake, decisive design force, closest rejected alternative, highest-leverage trade-off, blast-radius headline, proof verdict, weakest link, and anything else load-bearing — each carrying its `file:line` or `§N` pointer, the §4 start-here line verbatim, the group table at ≥2 groups, and the one thing to double-check. **Restates conclusions the sections below already prove; introduces no claim of its own and reproduces no evidence a section below owns.** Written LAST, from the sections on disk — never from memory. It has **no maximum length**: include one bullet per load-bearing item. |
| | ***Part I — Orient*** | *The picture and the business, before any code.* |
| 1 | **What Was Done** | The thing, where it lives, and before → after in **behavior** terms — not a file list, not the commit message. **When the target is a change** (diff · plan · fix), also: **where it sits in the system that already existed** — the capability that was already there, how it already worked, the contract it had to fit (`file:line`), what it deliberately left alone, and what the reviewer must already understand before Stage 1 makes sense. Written for a reader with **zero memory** of that system. This section owes the *full* context; §4 owes only the context needed to walk the route. |
| 2 | **Visual Map** | The mandatory diagram set from `references/diagram-catalog.md`: a system/component `flowchart`, a domain `erDiagram`, a `sequenceDiagram` per main flow — every one, no maximum — and a **story map** wiring each §3 story to the rule it protects, the test that proves it, and the §4 stage where the reviewer meets it — plus a `stateDiagram-v2` when an in-scope entity carries a lifecycle, and a phase flowchart when the target is a plan. Every node and edge is **derived**, not expected: solid edge = traced, dashed = inferred and named beneath the diagram. A diagram you cannot derive degrades to a **stated blocker** — never silence, never an empty fence, never plausible invented nodes. |
| 3 | **User Stories & Business Rules** | The main user-facing capabilities in scope, each as *As a … I want … so that …*, with the business rule or invariant it protects, where that rule is enforced (`file:line`), what breaks for the user if it breaks, and the **REAL** `TC-*` / test IDs that prove it. **Never invent a case ID** — a story with no test says *"no test covers this story"* and is recorded as a coverage gap. |
| | ***Part II — Route*** | *Where to start reading, and in what order.* |
| 4 | **Review Path** | The ordered reading route from `references/review-path.md`: one **"start here"** sentence naming the single file to open first and why, a stage flowchart with at least one back-edge, then a stage per meaningful shift in what the reviewer is checking — no ceiling — each carrying all eight fields — stage number, name in domain words, file group (changed files plus the unchanged `[context — not changed]` files needed to judge them), why this stage is here now, what to check, red flags **sourced from the repo's own rules**, an **exit criterion phrased as a question the reviewer can answer**, and an honest time-box. A file list with no order, no reason, and no exit criterion is a failed section. |
| | ***Part III — Depth*** | *How it works, why this shape, what it cost.* |
| 5 | **Concepts You Need** | The load-bearing technical concepts from Step 1 — every one of them, no maximum — each taught: what it is (first principles, plain language) → why THIS problem summons it → where it's visible here (`file:line`) → what breaks without it. **Never use a term in §6 that §5 has not taught.** |
| 6 | **How It Works** | The execution story: entry point → data flow → decision points → output/persistence. Use the Step 2 flow trace (a graph hint, when used, is verified by reading). Invariants and where they're enforced. Edge cases handled — **and edge cases NOT handled**. |
| 7 | **Why This Solution** | The forces that narrowed the option space, the one force that actually decided it, and why the obvious approach loses. Drill to the why-behind-the-why. "Best practice" / "cleaner" without a causal chain is a failed section. |
| 8 | **Options Considered** | **≥2 alternatives beyond the chosen one** (or an argued empty option space), each with specific pros, specific cons, cost-to-switch-later, provenance label, and the disqualifying reason. **The chosen option lists real cons too.** Name the closest call and what would flip the decision. |
| 9 | **Trade-offs Accepted** | Gained ↔ paid ↔ reversibility. What is now expensive to reverse (schema, public contract, cross-service message, shared layer, persisted shape). Debt knowingly taken + its repayment trigger. A trade-off list with no cost in it is a lie — fix it. |
| 10 | **Impact & Blast Radius** | Behavior change, upstream callers, downstream dependents, silent-break risk (things that still compile but change meaning), what tests protect it, what is protected by nothing, open follow-ups. |
| | ***Part IV — Prove & Push Back*** | *How to see it work, steer it, and argue with it.* |
| 11 | **Test & Demo** | How to run it and how to show it: the project's own test/run commands (resolved, never guessed; secrets as `<redacted:…>` placeholders), the one-time demo setup, then per case — setup → numbered steps → expected result **phrased as the discriminator vs the old behaviour** → how the domain stores or changes the data that solves it (`file:line`) → proof status, `✅ ran` only for a test actually executed this session, `⚠️ trace-verified` for everything else. Close with the test-execution transparency note: what was proven, what was not, and why. |
| 12 | **Your Call — Decision Levers** | The actionable table: *if you want X → change `file:line` → effort → risk*. Cheapest and most expensive things to change your mind about. Revisit signals. The smallest change that flips the chosen option. |
| 13 | **Challenge This** | The weakest link **named by you**. 3–5 rhetorical pressure-test questions attacking the core assumption, the option choice, the mechanics, and the scope. A pre-mortem ("3 months later this is reverted because…"). Where your confidence is lowest and what evidence would raise it. |

**The table above is worded for the commonest scope — a change to code that serves a user-facing story.** Other target forms exist, and several sections mean something different in each: a plan has no blast radius yet, a concept has no chosen option, an un-fixed bug has no fix to demo, a lockfile bump has no user story.

> **`references/report-template.md` is the SOLE owner of the target-form contract** — a form registry plus three per-form tables (sections · §4 route · §2 diagrams), all in that one file. Read it there and answer each section's *question* in the form the target actually has. `references/review-path.md` and `references/diagram-catalog.md` carry a pointer to it and **no form list of their own** — and neither does this file. **Do not restate the form set anywhere outside `report-template.md`.** Copies spread across files are how they drift out of agreement; keeping the registry and its tables together is what lets TC-CP-011 fail when a form is added to one and forgotten in another.
>
> The universal rule, which no form relaxes: **a change of form is never a licence to drop a section**, never a licence to invent a `file:line` that does not exist (`[ANTI-HALLUCINATION]`, above), and never a licence to write an "N/A" stub. When the honest answer for a form is *"this target has none"* — no story, no chosen option, no blast radius — say that in one line and say **why**; that is a filled section, an empty fence is not.

**At multi-group scale, every section is owed ONCE — at the altitude where its answer actually differs.**

| Altitude | Owns |
| --- | --- |
| **Spine** (once, whole scope) | §1 what the whole scope is · §2 the **group map** (D8) plus the scope-level system view · §4 the **group route** — which group to read first and why · §9 / §10 the cross-cutting trade-offs and blast radius no single group can see · §13 the whole-scope weakest link and pre-mortem · the group **ledger** |
| **Each group block** | The full §1–§13 **in that group's own scope** — its own diagrams, its stories with REAL IDs, its stage route, its concepts, mechanics, why-this-solution, options, trade-offs, impact, test & demo, levers, and challenges |

**The only licence this grants:** a section may be answered at the spine altitude INSTEAD of inside a group **when its answer is genuinely identical across groups** — and the group block then carries a **one-line pointer** to it (`§5 — shared concept, see spine: optimistic concurrency`). A pointer is a filled section; an empty heading, an "N/A" stub, or silence is a dropped one. **Scale is NEVER a reason to drop a section** — the `[BLOCKING]` drop-risk bar below binds **each group block AND the spine**, independently.

**Coaching techniques to apply throughout:** name the concept before using it · first principles before jargon · concrete before abstract · one analogy for anything genuinely dense · state what would break if a claim were wrong · prefer "this costs X to buy Y" over "this is better".

**[BLOCKING] §0 Detailed Summary, §2 Visual Map, §3 User Stories, §4 Review Path, §5 Concepts, §8 Options, §11 Test & Demo, §12 Your Call, §13 Challenge This are the sections that turn a description into a review guide.** They are the ones most often silently dropped — and the four new ones (§2, §3, §4, §11) are the most expensive to produce, which makes them the most rationalized away. Verify every one is present and **substantive** before closing — in the code-target form or the code-free form above, whichever the resolved scope calls for. A heading with a placeholder under it counts as dropped.

Offer a simpler restatement or analogy for any dense point proactively, without being asked. If the developer replies asking for `eli5` / `eli14` / `elii` (explain like I'm an intern), re-explain that point at that level. (Answering a developer's follow-up is fine — what is forbidden is *you* posing questions that expect a reply.)

## Step 5 — Summarize in Chat & Close (no quiz, no loop)

- **[ANNOUNCE — the explanation must never live only in a file].** Post an in-chat executive summary **derived from the finished §0** — §0 is already the compact statement of the whole run, so the chat post is a condensation of it, never a second, independently-written summary that can disagree with it. Carry at minimum: what was done, **the "start here" line from §4 — the single file to open first and why**, the highest-value diagram and what it shows, the key concept, why this solution, the closest alternative and why it lost, the highest-leverage trade-off or blast-radius note, and the single sharpest challenge question — then the report path **when a file was written**: `Teaching report → tmp/reports/understand-{…}.md`. When Step 3 could not resolve a git-ignored directory for the report there is no path to post: deliver every section in full in chat and post the blocker line instead. **The summary is unconditional; the path is not.** The start-here line is the most actionable sentence the run produces — it never lives only in the file.
- **[AT MULTI-GROUP SCALE the summary gains the group lines it needs.]** The tier and group count (`S3 · Large — 8 groups`); **which group to start with and why**, quoting that group's own start-here file; and the ledger verdict — groups written, plus anything deferred or dropped, named explicitly (never "mostly covered"). The chat post stays an executive summary and never becomes a per-group digest — §0 and the ledger are what the reader opens the report for. The report path still points at the one file (`Teaching report → tmp/reports/understand-{…}.md`); at ≥2 groups, add the anchor of the group to start with.
- **No secret value in the summary either.** The chat post obeys the same redaction rule as the report: name the setting and the file, never the credential.
- Append the one-line entry to `tmp/understand/{branch}-index.md` — **only when Step 3 resolved a git-ignored index directory**; if it did not, skip the append and say so once (Step 3). The HARD RULE binds this write exactly as it binds the report.
- End there. **Do not** quiz, do **not** ask the developer to restate, do **not** call ask user tool, do **not** wait for a reply to the §13 challenges, do **not** loop. **Never block the next workflow step.**

---

## When This Runs

- **Standalone, any time:** `$understand` (current context) or `$understand <whatever you want explained>` — a plan, a subsystem, a decision, a concept, a bug. Pairs well with voice mode for a natural narrated walkthrough.
- **Before reviewing someone else's change (or AI's):** the report's Part I + Part II are built for exactly this — see the shape of the system, read the stories it serves, then follow the route that says which files to open first and what to be able to answer at each stage.
- **Standalone only:** workflows and wrap-up skills do not invoke `$understand`; run it only when the user explicitly asks for a comprehension report.
- **At any size, up to and including the whole project:** `$understand the whole project` sizes to S3/S4, decomposes into per-context understanding groups, and accumulates ONE file — the same contract, more groups. Nothing about a big target licenses a thinner report.
- **After AI-authored work of any size** — the primary purpose: the developer who did not write the code must still be able to judge it, argue with the option chosen, review it in the right order, and decide what to change.

**NOT for:** investigation/docs/design/research workflows where nothing was built or planned to understand; forcing comprehension as a hard gate.

- **vs `$changes-review` and `$code-quality-review`:** those **perform** the review and emit findings against the code. This one **prepares a human to perform it** — it emits no findings and passes no verdict. Want the machine's verdict → `$changes-review`. Want to be able to form your own → here, then `$changes-review`.
- **vs `$demo-guide`:** that is **presenter-facing** — a standalone script for showing finished work to a room. §11 here is **reviewer-facing**: the same per-case shape (deliberately, so the two never drift), but in service of *understanding and verifying* the change rather than staging it. A whole-feature demo for stakeholders → `$demo-guide`.

## See Also

- **Reference:** `references/report-template.md` — the report skeleton, the four parts, options table format, provenance labels, per-level tuning, self-check.
- **Reference:** `references/diagram-catalog.md` — which diagrams are mandatory, how each is derived, provenance marking, size discipline, and what to emit when one cannot be derived.
- **Reference:** `references/review-path.md` — the layer taxonomy, the ordering algorithm, context inclusion, and the eight fields every review stage carries.
- **Reference:** `references/scale-protocol.md` — sizing → understanding groups → task breakdown → accumulation ledger → resumability → sub-agent fan-out → caps and the no-silent-truncation rule. Loaded at tier ≥ S2 only.
- **Skill:** `$investigate` — gather-only delegate: locate the relevant files when the target spans a large or unfamiliar codebase (feeds the group decomposition).
- **Skill:** `$investigate` — gather-only delegate: how an existing feature actually works when one read is not enough. Its `--mode=explain` is a different, one-way narrative and owns `tmp/understand/{branch}.md` (see Step 3).
- **Skill:** `$investigate --mode=debug` — gather-only delegate: the root cause of a live, un-fixed defect (feeds §6 and §8's candidate causes).
- **Skill:** `$graph-code --mode=blast-radius` — leverage-ordering + §10 blast-radius signal.
- **Skill:** `$why-review` — *adversarially audits* rationale quality (the complement: this *teaches* the rationale and hands the developer the challenge questions).
- **Skill:** `$demo-guide` — presenter-facing demo script for a whole feature; §11 here is the reviewer-facing subset for the change in scope.
- **Skill:** `$plan --mode=validate` — elicits plan *decisions* interactively (the complement: this *explains* them one-way).
- **Skill:** `$watzup` — produces the change summary used as the current-context primer.

---

**IMPORTANT MANDATORY Steps:** resolve-scope-and-style-and-load-three-references -> size-target-into-scope-tier -> decompose-into-understanding-groups-and-create-tasks-first -> gather-material-six-inventories-delegating-read-only-skills-when-needed -> order-two-axes-plus-group-order -> open-teaching-report-spine-and-ledger-before-section-one -> teach-every-section-group-by-group-accumulating-on-disk -> synthesize-across-groups -> summarize-in-chat-and-close

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `evidence-based-reasoning` — Ground every material claim in file:line, config or source evidence, with stated confidence; making any claim, finding or recommendation → .claude/skills/shared/protocols/evidence-based-reasoning.md
- `graph-assisted-investigation` — Optional hint: a code-graph query can add callers and dependents when grep may miss a high-risk blast radius, and it can be stale; a high-risk change where grep and reading alone may miss the blast radius → .claude/skills/shared/protocols/graph-assisted-investigation.md
- `incremental-persistence` — Persist results per file or section while the work proceeds; a sub-agent or heavy step processes more than three files → .claude/skills/shared/protocols/incremental-persistence.md
- `output-quality-principles` — Useful, readable guidance without lost conditions; writing generated docs or reports → .claude/skills/shared/protocols/output-quality-principles.md
- `understand-code-first` — Read and trace the target and existing patterns before changing code; planning or editing code → .claude/skills/shared/protocols/understand-code-first.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:evidence-based-reasoning:reminder -->

**IMPORTANT MUST ATTENTION** cite `file:line` evidence for every claim; never speculate. Confidence >80% to act, <60% = do NOT recommend; "not enough evidence" is valid output.

<!-- /SYNC:evidence-based-reasoning:reminder -->

<!-- SYNC:understand-code-first:reminder -->

**IMPORTANT MUST ATTENTION** search 3+ existing patterns and read code/conventions BEFORE any modification or explanation. The code graph is optional advice for high-risk blast radius (a hint that may be stale), never a requirement.

<!-- /SYNC:understand-code-first:reminder -->

<!-- SYNC:graph-assisted-investigation:reminder -->

**Optional advice:** the code graph (`.code-graph/graph.db`) can hint at a high-risk blast radius grep misses; it can be stale, so verify by reading files. Never required.

<!-- /SYNC:graph-assisted-investigation:reminder -->


## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Teach developers to review and judge any scoped work—not merely accept it—by showing what changed, how it flows, which stories/rules it protects, where to start, why this solution, alternatives/trade-offs/impact, how to test and demo it, decision levers, and written challenges, in a full report whose scope changes group count, not sections.

**IMPORTANT MUST ATTENTION — Main steps (execute in order, NEVER skip/merge):** (1) Resolve prompt scope and load the three contracts → (2) size the target, decompose groups, and create tasks before deep reading → (3) gather six evidence inventories, delegating only read-only investigation when needed → (4) order narrative depth, review route, and groups → (5) open the one teaching report with spine/ledger before section one → (6) teach every section group by group, appending blocks and ledger evidence on disk → (7) synthesize across groups → (8) summarize in chat, include the start-here line and report path, append the index, and close without a quiz or loop.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries) — MUST ATTENTION each:**

- **Evidence:** cite `file:line` for every claim; NEVER speculate without proof.
- **Understand Code First:** read code + grep 3+ patterns before explaining.
- **Graph-Assisted Investigation (optional):** the code graph is a stale-able hint for high-risk blast radius, never required.
- **Incremental Persistence:** create the report file BEFORE the first section; append per section and per group; never hold results in memory.
- **Output Quality:** dense, token-efficient prose; lead with the answer.
- **Parallel Sub-Agent Dispatch:** Tag tasks PAR/SEQ, group PAR into disjoint-write-set waves, spawn each wave in ONE message, barrier before advancing.

- **MUST ATTENTION** derive WHAT to explain from the prompt; with no target named, default to the current working tasks + changes in context. Never impose a fixed agenda.
- **MUST ATTENTION** SIZE the target into a scope tier (S0–S4) **before** reading it and DECOMPOSE anything above S1 into understanding groups (≤8 files / ≤2000 diff-lines, each explainable on its own) — announce both in one line. A bigger target buys **MORE GROUPS, never FEWER SECTIONS**; *"too big to explain properly"* is a conclusion this skill may never reach.
- **MUST ATTENTION** BREAK THE WORK INTO TASKS **before the first deep read** — the current task list first (resume, never duplicate), one task per group plus the fixed spine tasks, exactly one `in_progress`, and a group task marked `completed` ONLY when its block is on disk.
- **MUST ATTENTION** DECOMPOSE TO THE FINEST EXPLAINABLE UNIT, then TAG every task `PAR`/`SEQ`, DECLARE the waves, and SPAWN each wave in ONE message — group tasks are the main `PAR` wave (each owns its own fragment, so no shared write target); synthesis, spine, summary and self-check are `SEQ` because each consumes the whole wave. An oversized group that cannot split further gets up to 3 agents split by GATHER AXIS, never by file, each writing its own shard — and the ORCHESTRATOR spawns them, never the group agent. NEVER drip agents one per turn, and NEVER advance a barrier on a wave that has not fully returned. — why: decomposition width IS the parallelism budget, and an undeclared wave silently degrades into the sequential run it replaced.
- **MUST ATTENTION** OPEN the report — spine, ledger, reserved stubs — before section one, then ACCUMULATE group by group (write the block → update its ledger row → complete the task) and synthesize the scope-wide sections **from the written blocks**, never from memory. After any cutoff or compaction, verify every `written` ledger row against the filesystem before continuing.
- **MUST ATTENTION** DELEGATE the GATHERING — `$investigate`, `$investigate --mode=debug`, `$graph-code --mode=trace` — when read + grep + trace cannot fill an inventory; NEVER delegate to a mutating or findings-emitting skill, never let a delegate author a section, and re-verify every delegated claim against `file:line` before it enters the report. At S3+ the delegation runs inside the group's sub-agent, not the orchestrator.
- **MUST ATTENTION** announce anything deferred, sampled, or dropped in BOTH the spine and the chat summary — bounded coverage must never read as complete coverage.
- **MUST ATTENTION** TEACH so the reader could re-derive the design, COACH so they could argue for a different one, and ROUTE so they could review it in the right order without asking where to start — a description of what the code does is a FAILED run.
- **MUST ATTENTION** the report is **ALWAYS FULL**: every section, on every target — **no mode, no light variant, no section drops, no small-diff exemption, no opt-out.** §0 Detailed Summary opens the file, written LAST from the finished sections and restating only what they prove; then Part I What → Visual Map → User Stories; Part II Review Path; Part III Concepts → How → Why-this-solution → Options-considered → Trade-offs → Impact; Part IV Test & Demo → Your-call → Challenge-this. It NEVER deletes a section, reduces the diagram count, or drops a review stage. §0, §2, §3, §4, §5, §8, §11, §12, §13 are the ones that get silently dropped — verify them explicitly.
- **MUST ATTENTION** §2's mandatory diagrams are **derived, never expected** — traced edges solid, inferred edges dashed AND named beneath, fabricated edges are a failed section. An underivable diagram becomes a **stated blocker**, never an omission.
- **MUST ATTENTION** every `TC-*` / test ID in §3 and §11 is REAL — read from the specs or the test code. **NEVER invent a case ID.** No coverage → say so; an admitted gap is a finding, a fabricated ID retires a live risk.
- **MUST ATTENTION** §4 gives ONE "start here" file, orders stages contract-inward (blast radius is the peer tie-break, not the axis), marks unchanged context files `[context — not changed]`, sources red flags from the repo's own rules rather than inventing house rules, and closes every stage with a question the reviewer can answer.
- **MUST ATTENTION** §8 lists ≥2 alternatives beyond the chosen one, each with SPECIFIC pros, cons, cost-to-switch and disqualifying reason — plus real cons on the chosen option — or an argued empty option space. On a **code-free target** (concept · un-fixed bug) there IS no chosen one: §8 becomes alternatives to the concept itself, or the candidate root causes with evidence for and against (Step 4's code-free form) — a change of form, never a dropped section. Label each `[deliberated]` vs `[reconstructed]`; NEVER fabricate a deliberation that did not happen.
- **MUST ATTENTION** provoke the reader IN WRITING (§13 weakest link + pressure-test questions + pre-mortem) but NEVER interrogate — no ask user tool, no quiz, no teach-back, no waiting on a reply, no comprehension gate. On an ambiguous target, infer, state the assumption, proceed.
- **MUST ATTENTION** explain the WHOLE scope but lead with the non-obvious, high-blast-radius parts — order by leverage via grep/read (optionally `$graph-code --mode=blast-radius` as a stale-able hint); compress boilerplate, omit nothing. That leverage order governs §5-§10 **only**; §4's route is ordered contract-inward, and conflating the two produces a route that opens on mechanism instead of meaning.
- **MUST ATTENTION** cite `file:line` for every concrete claim; state confidence on anything resting on inference; never use a term in §6 that §5 has not taught.
- **MUST ATTENTION** NEVER put a secret value in the report or the chat summary — connection strings, tokens, keys, passwords and customer identifiers are named, never reproduced, and render as `<redacted:…>` in diagrams, stage tables, and run/demo commands alike.
- **MUST ATTENTION** this skill is standalone and NEVER blocks — teach, summarize, end. No comprehension loop, never gate commit/implementation. It prepares a human to review; it never issues findings or a verdict of its own.
- **MUST ATTENTION** write the full report to `tmp/reports/understand-{YYMMDD}-{HHmm}-{slug}.md` — **ONE combined file at every tier and every group count, never a directory and never a set** — INCREMENTALLY (create before the first section, append per section and per group block) and log one line to `tmp/understand/{branch}-index.md` — NEVER write any artifact inside `.claude/`, the source tree, `docs/`, or any git-tracked path. If an artifact's candidate directories are all git-tracked, skip that artifact and report it (Step 3) — deliver every section in chat when the report cannot be written — NEVER fall back to a tracked path.
- **MUST ATTENTION** ALWAYS post the in-chat executive summary — including the §4 "start here" line — plus the report path (`Teaching report → tmp/reports/understand-{…}.md`) whenever a file was written, or Step 3's blocker line when it could not resolve one. NEVER let the explanation live only in a git-ignored file the user never sees.

**Anti-Rationalization:**

| Evasion | Rebuttal |
| ------- | -------- |
| "Experienced reader, skip the explanation" | Never omit required sections based on the reader's experience. The full report contract applies to every reader. |
| "The concepts and options are obvious" | Sections §5/§8/§12/§13 always appear; keep their explanations concise when appropriate, but never omit them. |
| "Drop the diagrams and collapse the review path" | Diagram and stage counts follow their required contracts. A missing stage can send the reviewer into code they are not equipped to judge yet. |
| "Small diff — a diagram is overkill here" | A diagram is CHEAPEST exactly when the change is small, and the mandate is the minimum set, not a quota to justify. If one genuinely cannot be derived, it degrades to a **stated blocker** — never to omission, and never to a plausible-looking invented one. |
| "Concept/plan target — there's nothing to review, skip §4" | Wrong form, not absent section. A concept routes through the repo's own instances of it; a plan routes through its phases in verification order; an un-fixed bug routes from symptom back toward cause. The eight-field stage grammar still applies (`references/report-template.md` matrix). An `N/A` stub is a failed section. |
| "No tests exist — skip §11" | A change with no tests is the single most important thing the reviewer needs told. §11 then states how to demo it **manually** and flags the absent coverage explicitly. Missing tests are a finding, not an exemption — and never a reason to invent a `TC-*` ID to fill the row. |
| "I'll quiz them to check understanding" | NEVER interrogate. Challenge prompts are written into §13 as rhetorical questions; you never ask, never wait, never gate. |
| "Provoking thinking means asking them questions in chat" | It means writing the challenges down. ask user tool stays forbidden — the developer is provoked on paper, never put on the spot. |
| "Ambiguous target — I'll ask which one" | Do NOT ask. Infer the most likely target (default current context), state the assumption, proceed. |
| "Just dump everything I see" | Derive scope from the prompt first, then order by leverage. Cover all of scope, but lead with the non-obvious — not a repo-wide dump. |
| "Skip the trade-offs, just describe the code" | Why-this-solution, options, and trade-offs ARE the point. Mechanics alone is a failed run. |
| "There was only one sensible way to do this" | Then ARGUE it — name the option space and why it's genuinely empty. An unargued "no alternatives" is a skipped §8. |
| "I'll say we evaluated A, B and C" (when you didn't) | Label honestly: `[reconstructed]`. Fabricating a decision history is worse than admitting it was reconstructed. |
| "The chosen option has no downsides" | Then the analysis is unfinished. Every chosen option costs something — find it. |
| "I'll draw the architecture I'd expect this repo to have" | Then it is fiction with a diagram's authority — readers trust a picture more than prose and verify it less. Every node comes from a trace, a read call site, or a spec. Solid = traced, dashed = inferred and named, absent = stated as a blocker. |
| "This story probably has a test — I'll cite TC-042" | NEVER invent a case ID. Cite the ID you actually read, or write "no test covers this story" and record the gap. A fabricated ID retires a risk that is still live. |
| "Drop the report next to the skill / in docs/" | NEVER write inside `.claude/`, source, `docs/`, or tracked paths — only `tmp/reports/` + `tmp/understand/{branch}-index.md`. No git-ignored dir **for that artifact** → skip that artifact and report the blocker; every section goes to chat. Never a tracked path. |
| "Concept target — §8/§10/§12 don't apply, skip them" | Wrong form, not absent section. Answer each section's question in its code-free form (Step 4) — never an `N/A` stub, never an invented `file:line`. |
| "Write the report and continue silently" | ALWAYS post the chat summary — including the start-here line — plus the path when a file was written, or Step 3's blocker line when none could be. Never log-and-move-on into a hidden git-ignored file. |
| "I'll write every section at the end in one go" | Create the file first, append per section — a run that dies mid-way must leave finished sections on disk. |
| "Target is huge — a high-level summary IS the honest answer" | Wrong lever. Scale buys MORE GROUPS, never fewer sections. Size it, decompose it, task it, accumulate it — the contract is size-invariant. |
| "I'll investigate the whole thing first, then write the report" | Never. Spine before section one, a block per group, ledger updated as each lands. Investigation held in context is investigation one cutoff from gone. |
| "Small target — skip the sizing and the task list" | Sizing costs seconds and decides the shape of everything after it; S0 is a legitimate outcome. Tasks still exist (one per part) so a dead run shows where it stopped. |
| "One big group is simpler than five" | A unit whose §1–§13 cannot be answered about it alone is not a group. Split at ≤8 files / ≤2000 diff-lines, and name each group so its name has no "and" in it. |
| "The blocks are written and I remember them — I'll synthesize from memory" | Synthesize from the FILES. After compaction, memory is a hypothesis; the ledger plus the disk is the evidence. |
| "This group's §5/§8 repeats the spine — drop it" | Answer it ONCE at the altitude where it differs, then leave a one-line POINTER in the group block. A pointer is a filled section; silence is a dropped one. |
| "I'll call $changes-review or $fix to gather faster" | Delegates are READ-ONLY and gather-only. This skill emits no findings and mutates nothing — never delegate to a mutating or verdict-issuing skill. |
| "The sub-agent reported it wrote the block" | Verify the FILE. A summary is evidence of a reply, never of a block — check it exists, carries its ⚠ sections, and cites REAL IDs. |
| "12 groups won't fit in one file — I'll split it into a directory" | The ONE file IS the deliverable, at every tier and every group count. Size is what §0, the ledger, and the anchors are for — a directory is a deliverable nobody opens as a whole. Past 12 groups, NEST inside the file (`# Context — {name}`); never split it. |
| "§0 would be enormous at 12 groups — I'll trim it to the top three" | §0 has NO maximum length. A 12-group report has 12 key mechanics and 12 ledger rows, not three. Include every load-bearing item; "too long to summarize" is the failure §0 exists to prevent. |

> **[IMPORTANT]** This skill exists so the human can **judge** AI's work and **review** it, not just receive it — draw the system, state the stories and the rules, hand over the route that says where to start, teach the concepts, expose the whole option space with honest pros and cons, show how to run and demo it, hand over the decision levers, and write down the challenges that provoke real thinking. Never test them, never wait on them, never block them.
