---
name: specify
description: |
  "/specify", "specify", "요구사항 정의", "requirements", "스펙 잡기",
  "뭘 만들어야 하는지", "기획 정리", "인터뷰해서 스펙"
  Turn a goal into structured requirements through systematic interview.
  Three phases: Interview → Extract → Cross-check.
  Writes requirements.md in the cli format (consumed by /blueprint).
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
  - Skill
validate_prompt: |
  Must produce or preserve a valid <spec_dir>/requirements.md with only type,
  goal, and non_goals in frontmatter. Requirement IDs must use R-B*, R-U*, and
  R-T* only, and every sub-requirement must include given/when/then.
  For brownfield-extension, brownfield-refactor, and hybrid specs, qa-log.md
  must either have where.research_done: true or record an explicit research skip
  / fallback reason in ## Research.
  After Phase 2, reqs-business.md, reqs-interaction.md, reqs-tech.md, and
  cross-check.md must exist. cross-check.md must keep ## Dedup Log before
  ## Cross-Check Report.
  Phase 4.2 decisions must be persisted in qa-log.md ## Resolutions as CC-N
  entries. Final Open Decisions must be promoted from qa-log.md ## Open Items
  and deferred CC-N resolutions.
  Unless explicitly skipped, metrics/specify-events.jsonl and performance.md
  must be produced so slow /specify runs can be analyzed after the fact.
---

# specify: Goal → Requirements via Systematic Interview

## Invocation Modes (v1.6.0-sr.7)

`/specify` accepts the following invocation patterns. They are pre-processed before Phase 0 begins.

### Bare invocation — Smart Router

`/specify` with no arguments inspects local state and routes:

| State | Action |
|---|---|
| No `<spec_dir>` exists, no goal in input | Ask the user for a goal, then proceed to `init` flow |
| `<spec_dir>` exists with incomplete `qa-log.md` | **Resume** from last recorded phase |
| `<spec_dir>` exists with completed `requirements.md` and `spec_inbox.json` empty (or absent) | Print `status` summary (coverage + open decisions) and stop |
| `<spec_dir>` exists with `spec_inbox.json` containing N items | Print "🔔 N items pending" and offer reflect/expand options via AskUserQuestion |
| Multiple candidate `spec_dir`s under `.sr-harness/specs/` | AskUserQuestion to pick one |

The router only chooses *which* flow to run — it does not change Phase 0–4 internals. If the user passes an explicit goal string, treat as `init` regardless of state.

### `--quick` flag

`/specify --quick "<goal>"` runs an abbreviated interview suitable for skeleton v0 specs:

- **Phase 1 cap**: max **2 questions per active node** regardless of `depth_calibration` (deep → standard, standard → light cap).
- **Inline drills**: disabled. Treat all "vague qualifier" / "hidden assumption" signals as Open Items instead of drilling.
- **Gap audit**: each axis runs gap-auditor exactly once. CONTINUE verdict auto-promotes remaining AMBIGUOUS items to `## Open Items` and the axis is treated as sufficient.
- **Phase 2 extractors**: still run, but on a smaller qa-log → naturally faster.
- **Final audit**: skipped. Cross-check (Phase 3) catches inter-axis issues.

Use `--quick` for early exploration, prototypes, and toy projects. Re-run without `--quick` (or use future `/specify expand <axis>`) to deepen any axis.

### `-context @<file>...` flag — Context-First lite

`/specify -context @docs/idea.md [-context @notes/meeting.md ...]` injects pre-existing documents as the primary source for Mirror + Phase 1 default answers.

Pre-processing:
1. Read each `@<file>`. Concatenate up to 50K tokens; if larger, summarize each file via a single Pre-Fill Agent call.
2. Stash combined context as `<spec_dir>/context-bundle.md` once `spec_dir` is decided in Step 0.3.
3. In Step 0.1 Mirror generation, prefer extracted goal/non_goals/sr_* fields from the context bundle over keyword inference. Mark each extracted field with `source: from-context-doc` and `lineage: <file>:<line-range>` in qa-log.md frontmatter.
4. In Phase 1, when forming AskUserQuestion options, use the context bundle as the "tentative answer" for Default-First (see Question Construction below). Show `[from idea.md:42-58]` provenance in the option `description`.

`-context conversation` (literal token, not `@`) injects the current conversation history as a context source. Off by default; user must opt-in.

Combinable: `--quick` + `-context` is the fastest path — context fills most fields, the abbreviated interview asks only what is left.

## Overview

Transform a vague goal into structured, traceable requirements through:
0. **WHERE Grounding** — establish project type, situation, ambition, and risk modifiers
0.5. **Context Research** (brownfield only) — scan existing codebase before asking the user
1. **Interview** — systematic Q&A across Business/Interaction/Tech axes (depth-calibrated by WHERE)
2. **Extract** — parallel requirements extraction by domain experts
3. **Cross-check** — conflict/gap/duplicate detection
4. **Confirmation** — user accepts assumptions + final `requirements.md` committed in cli format

## Handoff contract

The final deliverable is `<spec_dir>/requirements.md` in the format that `/blueprint` consumes:
- Frontmatter: `type` (greenfield|feature|refactor|bugfix), `goal`, `non_goals[]`
- Body: flat list of `## R-X<num>:` parent requirements, each with nested `#### R-X<num>.Y:` sub-requirements carrying `given/when/then`
- `X` in the ID is axis code: **B**=Business, **U**=Interaction (user), **T**=Tech
- Optional `## Open Decisions` section with `### OD-N:` blocks

All intermediate files (qa-log.md, reqs-business.md, reqs-interaction.md, reqs-tech.md, cross-check.md) stay in `<spec_dir>/` for traceability but are NOT read by /blueprint.

## Path Conventions

- `${baseDir}` — the directory containing this `SKILL.md` (i.e., `skills/specify/`). Resolves to the same path whether the skill is loaded from the repo or from a plugin marketplace cache.
- `<spec_dir>` — the per-spec output directory (default `.sr-harness/specs/{spec-name}/`). Decided in Step 0.3.
- All template references in this file use `${baseDir}/templates/*` and never repo-root paths.
- Metrics helper path: `${baseDir}/../../scripts/specify-metrics.mjs`

## Performance Metrics

`/specify` records lightweight wall-clock metrics so slow runs can be diagnosed after the session. The metrics are not consumed by `/blueprint`; they are diagnostic artifacts only.

Write metrics to:

- `<spec_dir>/metrics/specify-events.jsonl` — raw event stream
- `<spec_dir>/performance.md` — summary report with bottleneck and improvement candidates

Use this helper:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> <phase> <event> --label "<label>"
node "${baseDir}/../../scripts/specify-metrics.mjs" report <spec_dir> > <spec_dir>/performance.md
```

Record these events:

| Moment | Command shape |
|---|---|
| Phase start | `mark <spec_dir> phase0 phase_start --label "WHERE Grounding"` |
| Phase end | `mark <spec_dir> phase0 phase_end --label "WHERE Grounding"` |
| AskUserQuestion before/after | `mark <spec_dir> phase1 ask_user_start/end --label "<axis or gate>"` |
| gap-auditor before/after | `mark <spec_dir> phase1 gap_audit_start/end --label "<business|interaction|tech|final>"` |
| extractor before/after | `mark <spec_dir> phase2 agent_start/end --label "<business-extractor|interaction-extractor|tech-extractor>"` |
| research agent before/after | `mark <spec_dir> phase0.5 agent_start/end --label "<code-explorer|docs-researcher|refactor-impact>"` |

At the end of Phase 4.4, generate the report:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" report <spec_dir> > <spec_dir>/performance.md
```

Interpretation rules:
- `ask_user_*` duration includes user wait time. If that dominates, the bottleneck is workflow friction, not model work.
- `gap_audit_*` count identifies audit loops. Repeated loops usually mean Phase 1 questions are too broad or depth thresholds are too strict.
- `phase0.5` dominance usually means KB cache miss, stale KB re-scan, or over-broad code exploration.
- `phase2` dominance usually means extractor agents are not effectively parallel or one extractor has a prompt/output bloat issue.

## Phase 0: WHERE Grounding

The **WHERE** is the combination of current situation and intended scope. It calibrates how deep the interview goes on each axis — without it, every project gets the same heavyweight treatment, which over-engineers toys and under-specs production systems.

### Step 0.1: Mirror + SR Context Detection

#### SR-Harness: Parse user input for project context

Before generating the mirror, scan the user's input (description + keywords) to infer SR-Harness project context. This replaces the need for a separate product/module selection step.

**Keyword inference rules use confidence, not single-token matching.**

| Context | High-confidence signals | Generic signals (never enough alone) | Inference rule |
|---|---|---|---|
| `sr_product: spx` | `spx`, `core-driver`, `core-nav*`, `core-local*`, `core-task`, `core-docking` | `robot`, `driver`, `navigation` | High signal present -> infer `spx` |
| `sr_product: sarics-nx` | `sarics`, `관제`, `sarics-nx` | `dashboard`, `frontend`, `backend`, `be`, `fe` | High signal present -> infer `sarics-nx`; generic-only needs 2+ signals and mark as `(estimated)` |
| `sr_product: cross-product` | SPX high signal + SARICS high signal, `ros bridge`, `관제-로봇` | `bridge`, `integration` | High signal pair -> infer `cross-product`; generic-only stays null |
| `sr_profile: driver` | `core-driver`, `uart`, `can`, `wheel`, `bms`, `sensor`, `lift` | `hw`, `hardware`, `driver` | High signal present -> infer `driver`; generic-only needs 2+ signals and mark as `(estimated)` |
| `sr_profile: ros-node` | `core-nav*`, `core-local*`, `core-task`, `core-docking`, `nav2`, `amcl`, `ekf`, `rclpy`, `rclcpp` | `node`, `topic`, `action`, `service` | High signal present -> infer `ros-node`; generic-only needs 2+ signals and mark as `(estimated)` |
| `sr_profile: cross-product` | `sarics` + `spx`, `ros bridge`, `관제-로봇` | `bridge`, `sync`, `api` | High signal present -> infer `cross-product` |
| `sr_profile: infra` | `simulation`, `simulator`, `infra` | `테스트`, `tool`, `도구` | High signal present -> infer `infra`; generic-only needs 2+ signals and mark as `(estimated)` |
| `sr_profile: web` | `sarics` with no SPX signal | `dashboard`, `frontend`, `backend` | SARICS high signal -> infer `web`; generic-only stays null |
| `sr_ros_version: ros2` | `ros2`, `rclpy`, `rclcpp`, `humble`, `iron`, `colcon` | - | High signal present -> infer `ros2` |
| `sr_ros_version: ros1` | `ros1`, `rospy`, `roscpp`, `noetic`, `catkin` | - | High signal present -> infer `ros1` |

Confidence handling:
- **high**: domain-specific signal present. Infer automatically.
- **medium**: 2+ generic signals, or a generic signal plus a related domain-specific signal. Show `(estimated)` in the mirror and let the user correct it during confirmation.
- **low**: only 1 generic signal. Leave as `null`.

Generic words such as `node`, `service`, `topic`, `action`, `dashboard`, `backend`, `tool`, and `테스트` appear in many domains. Do not use them alone to set SR context.

**`sr_modules` extraction** — populate the array by normalizing matched module tokens. KB-first lookup (Phase 0.5) and KB Save (Step 4.5) iterate this array, so it must be filled whenever the user names specific SPX/SARICS modules.

| Token (case-insensitive) | Normalized module name |
|---|---|
| `core-driver`, `wheel`, `bms`, `led`, `io`, `lift`, `sensor manager` | `core-driver` |
| `core-localization`, `core-local`, `localization`, `amcl`, `ekf` | `core-localization` |
| `core-task`, `task scheduler`, `mission scheduler` | `core-task` |
| `core-navigation`, `core-nav`, `nav2`, `move_base`, `planner` | `core-navigation` |
| `core-docking`, `docking` | `core-docking` |
| `sarics-be`, `sarics backend`, `관제 backend` | `sarics-be` |
| `sarics-fe`, `sarics frontend`, `관제 frontend`, `dashboard` (only when `sarics` co-occurs) | `sarics-fe` |

Rules:
- Multiple modules can be detected — append all matches.
- If no module token matches, leave `sr_modules: null` (NOT `[]`) so Phase 0.5 / Step 4.5 skip cleanly.
- Sub-component tokens (`wheel`, `bms`, etc.) collapse to their parent module — they are not separate modules.

If `sr_product` or `sr_profile` is not detectable at medium or high confidence, leave as `null` — do not ask; the interview (Phase 1 Tech axis) will naturally surface it.
If only `sr_ros_version` is ambiguous and `sr_profile` is `ros-node` or `driver`, batch a single ROS version question into the mirror confirmation below.

#### Mirror template

Present your understanding using this template:

```markdown
**Mirror — Here's what I understood**

**Understanding:**
<1–2 sentences paraphrasing the user's request in your own words. Not a verbatim echo.>

**Goal:**
- <bullet 1: concrete outcome>

**Non-Goal (explicitly out of scope):**
- <bullet 1: exclusion — at least one must be inferred by you, not stated by user>

**Ambiguous (scope-level unknowns):**
- <ambiguity about what "done" means, what's included, or who the user is>

**Detected context:** <sr_product> / <sr_modules> / <sr_ros_version>
(omit this line if nothing was detected)
```

Then confirm via AskUserQuestion.

**If `sr_ros_version` is ambiguous** (sr_profile is `ros-node` or `driver` but ROS version not in input): batch the ROS version question together with the mirror confirmation in one AskUserQuestion call.

```
AskUserQuestion(
  questions: [
    {
      question: "Does this match your intent?",
      options: [
        { label: "Approve", description: "Proceed to WHERE grounding" },
        { label: "Revise", description: "Fix goal/non-goal/scope" }
      ]
    },
    {
      question: "Which ROS version?",   // only if sr_ros_version ambiguous
      options: [
        { label: "ROS2 (Humble/Iron)", description: "colcon, rclpy/rclcpp, lifecycle nodes" },
        { label: "ROS1 (Noetic)", description: "catkin, rospy/roscpp, rostopic" }
      ]
    }
  ]
)
```

**If `sr_ros_version` is already clear**: single-question confirmation only.

**Rules:**
- At least one Non-Goal and one Ambiguous item must be **inferred** by you — a pure echo is a violation
- Ambiguous items are **scope-level** only ("what are we building / for whom / done when?"), NOT tech choices
- Max 2 revision rounds. If still unclear, proceed and record residual ambiguities for Phase 1
- On Approve: extract `goal`, `non_goals`, and all detected `sr_*` fields for qa-log.md

### Step 0.2: PROJECT_TYPE + SITUATION + AMBITION (batched AskUserQuestion)

Use **one AskUserQuestion call with 3 questions batched**:

```
questions: [
  {
    question: "What kind of thing are you building?",
    header: "Project type",
    options: [
      { label: "User-facing app", description: "Web, mobile, or desktop app with end-user UI" },
      { label: "API / Service", description: "Backend API, data pipeline, or background service" },
      { label: "Dev tool / Library", description: "CLI tool, SDK, library, automation script" },
      { label: "Infrastructure", description: "Infra change, deployment config, platform work" }
    ]
  },
  {
    question: "What's the current codebase situation?",
    header: "Situation",
    options: [
      { label: "Greenfield", description: "Brand new project, no existing code" },
      { label: "Brownfield extension", description: "Adding to an existing codebase, minimal changes to what's there" },
      { label: "Brownfield refactor", description: "Reworking existing code; structural changes expected" },
      { label: "Hybrid", description: "New module inside existing project, both new and integration work" }
    ]
  },
  {
    question: "What's the ambition level?",
    header: "Ambition",
    options: [
      { label: "Toy / Experiment", description: "Days of work, personal/internal, failure acceptable" },
      { label: "Feature / MVP", description: "1-2 weeks, real users, core functionality only" },
      { label: "Product", description: "Long-term, external customers, reliability and security matter" }
    ]
  }
]
```

### Step 0.2b: Risk Modifiers (multiSelect AskUserQuestion)

Some projects are "small but dangerous" — a toy that handles real money, a refactor that touches a public API. Risk modifiers catch these cases by forcing relevant axes to `deep` regardless of Ambition.

```
questions: [
  {
    question: "Select any that apply to this project (pick none if none apply):",
    header: "Risk factors",
    multiSelect: true,
    options: [
      { label: "Sensitive data", description: "Handles PII, payments, health, secrets, or regulated data" },
      { label: "External exposure", description: "Accessible from public internet or external customers" },
      { label: "Irreversible ops", description: "Migrations, destructive actions, public contract changes" },
      { label: "High scale", description: "High traffic, large data volumes, or strict latency targets" }
    ]
  }
]
```

If the user picks none, proceed with base calibration. Otherwise, modifiers will escalate specific nodes to `deep` in Step 0.4.

### Step 0.3: Spec Name & Output Setup

- Determine **spec name** (kebab-case, e.g., `user-dashboard`)
- Decide `spec_dir`: default `.sr-harness/specs/{spec-name}/`
- **Pre-flight templates before starting the interview**. Verify these files exist under the specify skill directory:
  - `${baseDir}/templates/qa-log.md`
  - `${baseDir}/templates/reqs-axis.md`
  - `${baseDir}/templates/requirements.md`
  - `${baseDir}/references/research-prompts.md`
  - `${baseDir}/../../scripts/specify-metrics.mjs`
  If any template is missing, abort immediately with a clear message. Do not begin the interview and risk losing hours of Q&A at Phase 4.
- **Bootstrap via cli** — creates the directory AND writes a `requirements.md` stub with the correct frontmatter so /blueprint can read it later:
  ```bash
  sr-harness-cli req init <spec_dir> --type <greenfield|feature|refactor|bugfix> --goal "<one-line goal>"
  ```
  Map `WHERE.SITUATION` → `--type`:
  - `greenfield` → `greenfield`
  - `brownfield-extension` → `feature`
  - `brownfield-refactor` → `refactor`
  - `hybrid` → `feature` (or `refactor` if structural churn dominates)
  The stub is overwritten at Phase 4.3 once the interview is complete. If `<spec_dir>/requirements.md` already exists from a prior run, skip `req init` and proceed (the user is re-running specify on the same spec).
  - **`type` rerun check**: when `<spec_dir>/requirements.md` exists, read its frontmatter `type` and compare with the new SITUATION→type mapping above. If they differ, halt and ask the user whether to keep the existing `type` (and ignore the new SITUATION) or rewrite it (and treat the spec as a Full re-interview per Phase 4.3).
- Read the Q&A log template from `${baseDir}/templates/qa-log.md`
- Initialize `<spec_dir>/qa-log.md` only when it does not already exist.
  - If `<spec_dir>/qa-log.md` exists, keep it unchanged, treat the run as a resume/re-run, and append new Q&A under a dated `## Re-run` or `## Re-interview` section when needed.
  - If it does not exist, create it with spec name, goal, non-goals, and the WHERE context filled in.
- **Resume mismatch check** — when `<spec_dir>/qa-log.md` exists, compare the existing `where:` frontmatter against the new Mirror result. If any of the following changed, halt and ask the user:
  - `goal` differs (semantic difference, not whitespace)
  - `non_goals` set differs
  - `situation` / `ambition` differ
  - `sr_product` / `sr_profile` / `sr_modules` differ from non-null existing values
  ```
  AskUserQuestion(
    question: "Existing qa-log.md describes a different scope than the new mirror. How to proceed?",
    options: [
      { label: "Update WHERE", description: "Overwrite frontmatter with new mirror result; keep prior Q&A under ## Re-interview" },
      { label: "Keep existing", description: "Discard new mirror; resume with prior WHERE context" },
      { label: "Fresh spec", description: "Abort — user will use a different spec_dir" }
    ]
  )
  ```
  - **Update WHERE**: write new mirror values to frontmatter, append a `## Re-interview` section with the date, continue Phase 0.4.
  - **Keep existing**: discard new mirror result, restart Phase 0.1 from existing frontmatter values.
  - **Fresh spec**: abort; the user will rerun `/specify` with a different `spec_dir`.
  Include SR-Harness fields if detected in Step 0.1:
  ```yaml
  where:
    situation: <brownfield-extension|greenfield|...>
    ambition: <toy|feature|product>
    risk_modifiers: []
    sr_product: <spx|sarics-nx|cross-product|other|null>
    sr_modules: [<module>, ...]   # null if not detected
    sr_ros_version: <ros1|ros2|null>
    sr_profile: <web|driver|ros-node|cross-product|infra|null>
    sr_raw_input: "<user's original input text>"
  ```

After `<spec_dir>` is known and pre-flight passes, start Phase 0 metrics:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase0 phase_start --label "WHERE Grounding"
```

### Step 0.4: Derive Axis Depth Calibration

Combine SITUATION × AMBITION × RISK_MODIFIERS to assign each taxonomy node a depth level (**light**, **standard**, or **deep**). Apply rules in order — later rules escalate, never downgrade.

**Step A — SITUATION base**:
- **Greenfield** → TECH.ARCH/DATA standard
- **Brownfield extension** → TECH.ARCH **deep**, TECH.COMPAT **deep**; BUSINESS.WHO **light**
- **Brownfield refactor** → TECH.ARCH **deep**, TECH.COMPAT **deep**, TECH.DATA **deep**
- **Hybrid** → blend Greenfield + Extension rules

**Step B — AMBITION modulation**:
- **Toy** → TECH.SECURITY **light**, BUSINESS.RISK **light**, INTERACTION.ACCESS **light**. Keep INTERACTION.JOURNEY/HAPPY standard.
- **Feature/MVP** → default standard; only honor deeps from Step A.
- **Product** → TECH.SECURITY **deep**, INTERACTION.ACCESS **deep**, BUSINESS.RISK **deep**, TECH.COMPAT **deep**.

**Step C — RISK_MODIFIERS escalation (override Step B downgrades)**:
- **sensitive-data** → TECH.SECURITY **deep**, TECH.DATA **deep**
- **external-exposure** → TECH.SECURITY **deep**, INTERACTION.ACCESS **deep**
- **irreversible** → BUSINESS.RISK **deep**, TECH.COMPAT **deep**
- **high-scale** → TECH.INFRA **deep**, TECH.ARCH **deep**

**Examples**:
- User-facing + Greenfield + Toy + no modifiers → light SECURITY/RISK/ACCESS, standard elsewhere
- User-facing + Greenfield + Toy + sensitive-data → SECURITY/DATA escalated to **deep** (small-but-dangerous)
- API-service + Brownfield-refactor + Product + external-exposure → virtually everything deep

**Project-type notes** — PROJECT_TYPE doesn't change calibration numbers, but it changes what each INTERACTION node *means* (the interaction-extractor reads project_type for lens selection).

**Step D — SR Profile override (SR-Harness only, apply after Step C)**:

Apply only when `where.sr_profile` is set. These escalate on top of Step C — never downgrade.

| sr_profile | Escalation | Additional interview nodes activated |
|---|---|---|
| `driver` | TECH.INFRA **deep** | `TECH.HW_INTERFACE`: UART/CAN/SPI protocol, baud rate, packet format, timeout/retry, E-Stop |
| `ros-node` | TECH.ARCH **deep**, TECH.COMPAT **deep** | `TECH.ROS_INTERFACE`: topic/service/action names, msg types, QoS, lifecycle, tf frames |
| `cross-product` | TECH.ARCH **deep**, TECH.COMPAT **deep**, BUSINESS.RISK **deep** | `TECH.INTEGRATION`: REST↔ROS bridge protocol, latency SLA, reconnect; `TECH.SAFETY`: E-Stop propagation |
| `web` | no change (Step A–C apply normally) | — |
| `infra` | BUSINESS.WHO **light**, INTERACTION all **light** | — |

Write the derived calibration into `qa-log.md` frontmatter as `depth_calibration:` so Phase 1 and the gap-auditor can read it.

When Step 0.4 finishes, close Phase 0:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase0 phase_end --label "WHERE Grounding"
```

## Phase 0.5: Context Research (brownfield only)

**Skip this phase entirely if `where.situation == greenfield`.** Run it for `brownfield-extension`, `brownfield-refactor`, and `hybrid`.

Why: brownfield work depends on existing code that the user may not fully remember. Asking the user "what's the architecture?" when the codebase is right there is wasteful and unreliable. Scan the code first, then interview them on decisions — not facts.

Record Phase 0.5 start/end:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase0.5 phase_start --label "Context Research"
# ... after research consolidation or explicit Re-use skip
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase0.5 phase_end --label "Context Research"
```

### Re-run cache check

Before any KB lookup or agent dispatch, read `<spec_dir>/qa-log.md` if it exists.

If `where.research_done: true`, ask the user whether to reuse or refresh:

```
AskUserQuestion(
  question: "Existing research is already recorded for this spec. Reuse it or scan again?",
  options: [
    { label: "Re-use", description: "Keep the existing Research section and skip research agents" },
    { label: "Re-scan", description: "Run research agents again and append fresh findings" }
  ]
)
```

- **Re-use**: preserve the existing `## Research` section and skip this phase.
- **Re-scan**: run this phase again; append a dated `### Re-scan` subsection instead of deleting previous findings.
- A blank template `## Research` heading does **not** count as cached research. If `research_done: false`, proceed to KB lookup or agent dispatch even when the heading already exists.
- If recovering a legacy `qa-log.md` without `research_done`, treat the section as cached only when it contains non-comment, non-whitespace content.

### SR-Harness: KB-first lookup

Run this check BEFORE dispatching agents. If `where.sr_modules` was detected in Step 0.1:

1. Read `.sr-harness/knowledge/index.yaml`
2. **Classify each module in `where.sr_modules`** (in-memory, no user prompts yet):
   - Not in index.yaml → mark `agent_scan` (fall through to dispatch)
   - In index.yaml + `commit_sha` match `git rev-parse HEAD` in `source.path` → mark `kb_loaded` (load KB files: `common` + `ros2`/`ros1` if present, skip agent scan)
   - In index.yaml + `commit_sha` mismatch → mark `kb_stale` (collected for batched prompt below)
3. **Batched MISMATCH prompt** — if any modules are `kb_stale`, ask the user once with one question per stale module (max 4 per AskUserQuestion call; chunk if more):
   ```
   AskUserQuestion(
     questions: [
       {
         question: "KB for {module-A} is outdated (stale commit). How to proceed?",
         options: [
           { label: "Use existing", description: "Load KB files as-is, mark kb_loaded" },
           { label: "Re-scan now", description: "Run /knowledge scan {module-A}, then load result" },
           { label: "Skip", description: "Fall through to agent dispatch" }
         ]
       },
       // ... one question per stale module (chunk into multiple calls if more than 4)
     ]
   )
   ```
   Apply the user's answer per module:
   - Use existing → `kb_loaded`
   - Re-scan now → invoke `/knowledge scan {module}` via the knowledge skill, then reload the KB and mark `kb_loaded`
   - Skip → `agent_scan`

   If `/knowledge scan {module}` fails, is unavailable, or the user aborts it, do not abort `/specify`. Mark that module as `agent_scan`, add `KB re-scan failed: {module} — {reason}` to `qa-log.md` `## Research`, and continue with agent dispatch.
4. If **all** modules are `kb_loaded` → skip "Dispatch subagents in parallel" entirely. Write KB content into `qa-log.md` `## Research` section directly.
5. If **some** modules are `kb_loaded` (and others are `agent_scan`) → still dispatch agents, but inject the following constraints into each agent prompt:
   - **Exclude already-known modules**: list `kb_loaded` modules with note "이미 KB로 처리됨 — 스캔 제외"
   - **Scope to remaining modules only**: agent should investigate only the not-loaded modules
   - Example prompt suffix: `"제외 대상 (이미 KB 로드됨): spx-driver. 조사 대상: core-navigation"`
   Write KB content for `kb_loaded` modules + agent findings for the rest into a unified `## Research` section.

### Dispatch subagents in parallel

Read `${baseDir}/references/research-prompts.md` and dispatch the listed prompts:

- **Relevant Code Explorer** → `code-explorer`
- **Toolchain Explorer** → `code-explorer`
- **Docs Researcher** → `docs-researcher`

For `brownfield-refactor` specifically, add:

- **Refactor Impact Explorer** → `code-explorer`

When some modules were already loaded through KB, apply the prompt constraint from `research-prompts.md` so agents exclude `kb_loaded` modules and scan only `agent_scan` modules.

For each dispatched research agent, record `agent_start` immediately before dispatch and `agent_end` after its result is received. Use labels `code-explorer:relevant`, `code-explorer:toolchain`, `docs-researcher`, and `code-explorer:refactor-impact`.

### Consolidate into `qa-log.md` → `research:` section

Write findings into `qa-log.md` under a new top-level heading `## Research` (before the axis sections). Include:
- Existing architecture summary (1-3 sentences)
- Relevant files/modules (with file:line anchors)
- Toolchain (build/test/lint)
- Existing constraints or conventions discovered
- Potential impact surface (for refactors)

Also add `research_done: true` to the `where:` frontmatter block so later phases can rely on it.

### Interview uses research as baseline

During Phase 1, when asking Tech axis questions:
- Reference the research findings ("I see you use Vite + TypeScript — is that still the target?" instead of "what's your build tool?")
- Only ask the user for **decisions** (what they want) and **intent** (why), not **facts** (what exists — we already found those)

## Phase 1: Interview

Record Phase 1 start/end:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase1 phase_start --label "Interview"
# ... after final audit SUFFICIENT and Proceed gate
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase1 phase_end --label "Interview"
```

### Interview Protocol

You are the interviewer. Ask questions **one axis at a time**, following this taxonomy:

```
Axis 1: BUSINESS    — WHO, WHY, WHAT, SUCCESS, SCOPE, RISK
Axis 2: INTERACTION — JOURNEY, HAPPY, EDGE, STATE, FEEDBACK, ACCESS
Axis 3: TECH        — ARCH, DATA, INFRA, DEPEND, COMPAT, SECURITY
```

**The INTERACTION axis is consumer-generic.** Reinterpret nodes based on `where.project_type`:

| project_type | JOURNEY | HAPPY | FEEDBACK | ACCESS |
|--------------|---------|-------|----------|--------|
| user-facing | User entry → outcome | Core UI flow | Visual/audio reactions | Permissions, a11y |
| api-service | Consumer integration flow | Canonical API call | HTTP responses, errors | Auth, rate limits |
| dev-tool | Install → invoke → result | `--help` / canonical use | stdout+exit codes | Install, platform |
| infrastructure | Operator procedure | Green deploy path | Dashboards, alerts | RBAC, IAM |

EDGE/STATE are universal: failures & conditional behavior apply everywhere.

### Depth -> Question Guidelines

Use the `depth_calibration:` frontmatter from `qa-log.md` to decide minimum interview depth. The gap-auditor must use the same thresholds when judging coverage.

| depth | Minimum questions per active node | Inline Drill (Type A) | Post-Audit Drill (Type B) |
|---|---:|---|---|
| `light` | 1 | Optional | Optional |
| `standard` | 2-3 | Required on first ambiguity signal | Required when gap-auditor flags ambiguity |
| `deep` | 4+ | Required for every ambiguity signal | Required; a single shallow answer is usually CONTINUE |

If an SR profile activates additional nodes such as `TECH.ROS_INTERFACE`, `TECH.HW_INTERFACE`, `TECH.INTEGRATION`, or `TECH.SAFETY`, apply the same depth table to those nodes.

### SR Extra Node Recording

When SR profile activates extra Tech nodes, append their headings under `## Axis: Tech` in `qa-log.md` after `### SECURITY`. Use the same Q/Drill/status recording format as built-in nodes.

| Active node | Heading to add |
|---|---|
| `TECH.ROS_INTERFACE` | `### ROS_INTERFACE` |
| `TECH.HW_INTERFACE` | `### HW_INTERFACE` |
| `TECH.INTEGRATION` | `### INTEGRATION` |
| `TECH.SAFETY` | `### SAFETY` |

The gap-auditor must receive these active nodes in the taxonomy checklist and include them in coverage calculations.

### Late SR Profile Surface

When `where.sr_profile` was `null` after Step 0.1 but Tech-axis answers reveal SR context (e.g., user mentions ROS topics, UART protocol, ros bridge), update it mid-interview rather than waiting for the final audit:

1. Update `where.sr_profile` (and `sr_modules` / `sr_ros_version` if newly clear) in `qa-log.md` frontmatter.
2. Re-run **Step 0.4 Step D** against the updated `sr_profile` — escalate `depth_calibration` for the affected nodes (e.g., `ros-node` → TECH.ARCH/COMPAT deep, plus activate `TECH.ROS_INTERFACE`).
3. Dispatch **gap-auditor** immediately on the Tech axis (do not wait for the normal end-of-axis trigger). The auditor will flag the now-`deep` nodes as AMBIGUOUS or MISSING if the existing Q&A is shallower than the new threshold.
4. Convert the auditor's AMBIGUOUS list into Inline/Post-Audit drills as usual.

This prevents under-spec when SR context surfaces late, without the heavyweight cost of a Re-calibration log.

### Question Rules

**PRIMARY: Use AskUserQuestion tool for all interview questions.**
Free-text prompting should only be a fallback when options genuinely cannot be enumerated.

Before every AskUserQuestion call, record `ask_user_start`; immediately after the user answers, record `ask_user_end`. Use the current axis or gate as the label, e.g. `business`, `tech`, `phase2-gate`, `final-preview`.

#### Why AskUserQuestion

- Directly implements **Recognition over Recall** — user picks from concrete options
- Options with `description` field show consequences/trade-offs per choice
- "Other" is auto-added — user can always override with custom answer
- Supports **batching** (1-4 questions per call) — pair related questions together
- `multiSelect: true` for non-exclusive choices

#### Batching Guidance

**Batch when**:
- Questions are within the same axis node and mutually informative (e.g., WHO + WHAT)
- Questions are orthogonal and won't confuse the user (e.g., STATE + FEEDBACK)
- User has already given broad context and is ready for several specifics

**Do NOT batch when**:
- A later question's options depend on the answer to an earlier one (ask sequentially)
- The first question is a depth drill that may trigger more drills (go one-at-a-time)
- User seems uncertain — a single focused question is less overwhelming

Max 4 per call (tool limit). Default: batch 2-3 related questions per turn.

#### Question Construction

Each AskUserQuestion option must have:
- `label`: 1-5 words (what the user picks)
- `description`: the consequence/implication of this choice
- First option gets "(Recommended)" suffix only when you genuinely have a recommendation

#### Default-First Pattern (v1.6.0-sr.7)

Before composing options, **always attempt to derive a tentative answer** from one of these sources, in priority order:

1. `<spec_dir>/context-bundle.md` (when `-context` flag was used)
2. Phase 0.5 Research findings (`qa-log.md` `## Research`)
3. KB content loaded for `where.sr_modules`
4. WHERE context defaults (situation × ambition × sr_profile)
5. Sensible engineering defaults for the project_type

When a tentative answer can be derived, structure the question as **Recognition + Verification**, not Recall:

```
question: "Confirm the tentative answer or override?"
header: "<topic>"
options: [
  { label: "Confirm: <tentative>", description: "Use the value above. Source: <where it came from>" },
  { label: "Modify", description: "Provide a different value via Other" },
  { label: "Skip", description: "Leave as uncertainty zone — revisit during /blueprint or later" },
  { label: "Other concrete option", description: "..." }
]
```

The "Skip" option is required whenever the user is unlikely to know the answer (Tech axis details, security thresholds, etc.). It records the node as `status: assumption` with confidence `low` and adds an Open Item, instead of forcing speculation.

When **no** tentative answer can be derived honestly, fall back to standard option construction. Do NOT fabricate a default just to satisfy the pattern.

Provenance: when the tentative answer comes from a context document, include `[from <file>:<lineX-Y>]` in the description so the user sees the origin.

**Example** (batched):
```
questions: [
  {
    question: "Who is the primary user?",
    header: "Primary user",
    options: [
      { label: "Senior developers", description: "Power users; expect depth + customization" },
      { label: "Junior developers", description: "Learning users; expect guidance + safe defaults" },
      { label: "Both equally", description: "Dual-mode UX; complexity to serve both" }
    ]
  },
  {
    question: "What's the success signal?",
    header: "Success metric",
    options: [
      { label: "Team-wide adoption", description: "Qualitative; hard to measure" },
      { label: "Daily active use", description: "Quantitative DAU; needs tracking" },
      { label: "Time saved per task", description: "Efficiency metric; baseline needed" }
    ]
  }
]
```

### Depth Drill: Two Mechanisms

Drills happen at two distinct moments, with different judges. Both are required.

#### Type A: Inline Drill (You judge, in real time)

**When**: Immediately after an AskUserQuestion answer arrives.

**How**: Scan the selected option + any "Other" free-text for these signals. If present, the NEXT AskUserQuestion is a drill on the same node.

| Signal | Example answer | Drill question |
|--------|---------------|----------------|
| **Vague qualifier** | "fast", "easy", "simple", "good UX" | AskUserQuestion with concrete thresholds as options (e.g., "<1s", "<3s", "<10s") |
| **Hidden assumption** | "obviously X", "of course Y" | AskUserQuestion surfacing the assumption ("does X always hold? What if not?") |
| **Multiple interpretations** | A term that could mean 2+ things (e.g., "admin") | AskUserQuestion listing each interpretation as an option |
| **New stakeholder** | Mentions a role not yet covered | Add a new node under the current axis, AskUserQuestion about their perspective |

Inline drills are fast and subjective — you catch the obvious ones on the spot.

#### Type B: Post-Audit Drill (gap-auditor judges, end of axis)

**When**: After an axis ends, gap-auditor returns verdict=CONTINUE with an AMBIGUOUS list.

**How**: The auditor's AMBIGUOUS list tells you exactly which nodes still need drilling. Convert each AMBIGUOUS item into an AskUserQuestion targeting that specific ambiguity, then continue until gap-auditor returns SUFFICIENT.

Post-audit drills are systematic — they catch what inline judgment missed.

#### Why Both

Type A is a fast first-pass filter; Type B is the safety net. Relying on only Type A means subjective blind spots slip through. Relying on only Type B means needlessly long axis rounds because trivially fixable ambiguities aren't caught early.

#### When Free-Text Is Acceptable

Only use free-text Q&A (no AskUserQuestion) when:
- The answer is genuinely open-ended (e.g., "describe your current workflow")
- You cannot construct 2+ distinct options honestly
- The question is exploratory to find option candidates for the next round

#### Handling "I Don't Know" — Tentative Judgment + Open Decision

Users will sometimes not know the answer (especially on Tech axis, or when the PM doesn't know implementation details). Don't let the interview stall.

When the user's answer is "I don't know / not sure / up to you / whatever works" (either by Other free-text or by tone):

1. **Make a tentative judgment**: Pick the reasonable default based on the WHERE context, existing research findings, and what experienced engineers would typically choose.
2. **Log it as an assumption**: Record in `qa-log.md` with `status: assumption` and include the reasoning in `> blockquote`.
3. **Add to Open Decisions**: Append an entry to `## Open Items` in qa-log.md with:
   - The undecided question
   - Your tentative judgment
   - Why this decision can be deferred (or why it might need revisiting)
4. **Tell the user**: "I'll go with {X} for now, logged as an open decision. You can revisit it later."

Don't re-ask the same question. Move on. The Phase 4 Confirmation will let the user review and override any tentative judgment.

**Example**:
```
Q: What authentication method?
User: "Dunno, whatever works"
→ Tentative: "Given brownfield-extension + sensitive-data, I'll assume existing SSO integration"
→ Log as assumption with status: assumption
→ Add to Open Items: "OD: auth method (tentative: SSO based on existing system)"
→ Continue to next question
```

#### Recording Answers

Update `qa-log.md` after each exchange using the template format:
- `#### Q:` for the question, `> blockquote` for the answer (include the selected option label + any free-text)
- `##### Drill:` for depth follow-ups
- Mark each with `status: resolved | ambiguous | assumption`

### Gap Audit Triggers

Dispatch the **gap-auditor** agent at these specific moments:

1. **End of axis** (required) — after you believe an axis is complete, before moving to the next
2. **Stuck on axis** (early check) — after 3 consecutive AskUserQuestion turns on the same axis without moving forward.
   "Without moving forward" means the last 3 turns added no new `status: resolved` entry to `qa-log.md`; `status: ambiguous` and `status: assumption` do not count as progress.
3. **Final audit** (required) — after all 3 axes look done, before transitioning to Phase 2

Do NOT call gap-auditor after every AskUserQuestion turn — that's wasteful. Call it at boundaries.

### Gap Audit Flow

Each call:
1. Write current Q&A state to `qa-log.md` first
2. Increment `audit_counts.{business|interaction|tech|final}` in `qa-log.md` frontmatter before dispatch.
3. **v1.6.0-sr.7 — Single-shot audit (default)**: each axis runs gap-auditor exactly once. If the verdict is CONTINUE, do **not** loop. Instead, automatically promote the auditor's AMBIGUOUS list to `## Open Items` (each as `status: ambiguous`) and treat the axis as sufficient for completion purposes. Record `audit_counts.{axis}: 1` and proceed.

   Rationale: repeated audit loops were the dominant Phase 1 cost (per `12_specify-pipeline-review.md` H-1 and `15_specify-redesign-living-spec.md` §3). Open Items are now first-class — `/blueprint` and `/execute` are expected to surface them through `spec_inbox.json` (Living Spec) or via Open Decisions in `requirements.md`.

   Legacy multi-loop behavior is available via `--strict` flag (max 5 loops + circuit breaker AskUserQuestion). The opt-out exists for high-risk product specs; default is single-shot.

   Multi-loop (legacy `--strict`) circuit breaker:
   ```
   AskUserQuestion(
     question: "The {axis} audit has looped 5 times without reaching SUFFICIENT. Continue interviewing or accept the remaining gaps as open decisions?",
     options: [
       { label: "Continue interviewing", description: "Run another audit/interview loop for this axis" },
       { label: "Accept and move on", description: "Convert remaining gaps into Open Decisions and proceed" }
     ]
   )
   ```
   - **Continue interviewing**: allow one more audit loop and increment the count.
   - **Accept and move on**: record each unresolved gap under `## Open Items` in `qa-log.md` as `status: assumption` or `status: ambiguous`, then treat the axis as sufficient for completion purposes.
4. Dispatch **gap-auditor** with:
   - Full `qa-log.md` content
   - Which axis just completed (or "final" for the full audit)
5. Read the verdict:
   - **CONTINUE** → ask the agent's suggested questions (use AskUserQuestion)
   - **SUFFICIENT** → move on
6. **You do NOT decide completion yourself** — only gap-auditor can say SUFFICIENT, except for the explicit circuit-breaker "Accept and move on" path above.

Record `gap_audit_start` immediately before dispatch and `gap_audit_end` after the verdict is read. Use the audited axis as the label.

### Interview Completion

All 3 axes must receive **SUFFICIENT** verdict, AND the final audit must also return **SUFFICIENT**. A circuit-breaker "Accept and move on" answer counts as sufficient only for the specific axis/final audit where the user accepted the residual gaps.
Update `qa-log.md` frontmatter: `status: complete` with final coverage scores.

Before entering Phase 2, show a short interview summary and ask for confirmation:

```
AskUserQuestion(
  question: "Proceed to requirements extraction?",
  options: [
    { label: "Proceed", description: "Run the three extractor agents now" },
    { label: "Add more", description: "Return to the selected axis, add more Q&A, then run final audit again" }
  ]
)
```

If **Add more**, ask which axis needs more detail, continue Phase 1 for that axis, run the axis audit and final audit again, then return to this gate.

## Phase 2: Requirements Extraction

Record Phase 2 start/end:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase2 phase_start --label "Requirements Extraction"
# ... after all extractors and post-processing complete
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase2 phase_end --label "Requirements Extraction"
```

Run 3 agents **in parallel**:

1. Read `${baseDir}/templates/reqs-axis.md` template
2. Read `where.sr_profile` from `qa-log.md` frontmatter
3. Dispatch simultaneously:
   - **business-extractor** agent with: qa-log.md content + template
   - **interaction-extractor** agent with: qa-log.md content + template
   - **tech-extractor** agent with: qa-log.md content + template + SR profile boundary context (see below)
4. Write outputs to:
   - `.sr-harness/specs/{spec-name}/reqs-business.md`
   - `.sr-harness/specs/{spec-name}/reqs-interaction.md`
   - `.sr-harness/specs/{spec-name}/reqs-tech.md`

Record `agent_start` for each extractor before dispatch and `agent_end` after each result is received. This lets the report identify whether a single extractor dominates Phase 2.

### Phase 2 Post-processing

Before Phase 3, run a lightweight deterministic dedup pass across the three reqs files:

1. Compare sub-requirements by normalized `given` + `when` + `then`.
2. If two items are structurally identical, keep the more specific axis item:
   - Tech-specific implementation/interface detail wins over generic Interaction wording.
   - Interaction workflow detail wins over generic Business wording.
   - Business intent stays when it expresses value/success criteria rather than behavior.
3. Remove only exact structural duplicates. Do not resolve semantic overlap here; leave that for Phase 3.
4. Create `<spec_dir>/cross-check.md` with the fixed section structure below and write the `## Dedup Log` section. Always create this file even when no duplicates are removed (write `_No duplicates removed._` under `## Dedup Log`).

### `cross-check.md` Section Structure (fixed)

The file MUST contain exactly these top-level sections in this order, and each phase writes only the section it owns:

```markdown
# Cross-Check

## Dedup Log
<!-- Phase 2 owns this section. List removed duplicates as bullet items: source ID → kept ID, reason. -->

## Cross-Check Report
<!-- Phase 3 owns this section. List CONFLICT / GAP / DUPLICATE / OPEN_QUESTION / ASSUMPTION items, each with a stable issue ID (CC-1, CC-2, ...). -->
```

Write rules:
- **Phase 2** creates the file with both section headings and fills only `## Dedup Log`. The `## Cross-Check Report` heading is left present but body empty.
- **Phase 3** reads the file, preserves `## Dedup Log` verbatim, and replaces the body of `## Cross-Check Report` with discovery results. Phase 3 NEVER touches `## Dedup Log`.
- After Phase 3 the file is **immutable** until next Supplement axis / Full re-interview cycle.

### SR-Harness: tech-extractor boundary context injection

When `where.sr_profile` is set, append the following to the tech-extractor prompt:

**sr_profile == `driver`** — HW↔Driver↔ROS boundary:
```
Apply boundary decomposition per interface layer:
Each sub-requirement must be separated into: HW communication | Driver processing | ROS interface.
Do NOT mix HW protocol details and ROS topic names in a single sub-req.
Example boundary: UART packet send (R-T1.1) ↔ /cmd_vel subscriber (R-T1.2) ↔ timeout E-Stop (R-T1.3)
```

**sr_profile == `ros-node`** — Node↔Node (topic/service/action) boundary:
```
Apply boundary decomposition per ROS interface:
Each sub-requirement must be separated by publisher side ↔ subscriber side (or client ↔ server).
Include: topic/service/action name, message type, QoS setting, and success/failure condition per side.
Example boundary: /navigate_to_pose action client (R-T1.1) ↔ global planner server (R-T1.2) ↔ local planner cmd_vel (R-T1.3)
```

**sr_profile == `cross-product`** — REST↔ROS Bridge↔ROS boundary:
```
Apply boundary decomposition across three layers: SARICS side | Bridge | SPX side.
Each cross-system interaction needs sub-reqs on all three sides.
Example boundary: POST /api/missions (R-T1.1) ↔ bridge dispatch (R-T1.2) ↔ /mission_request ROS publish (R-T1.3)
```

If `sr_profile` is `web`, `infra`, or null: use standard v2 boundary decomposition (API↔UI etc.).

## Phase 3: Cross-Check

Record Phase 3 start/end:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase3 phase_start --label "Cross-Check"
# ... after cross-check.md is written
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase3 phase_end --label "Cross-Check"
```

1. Read all 3 reqs files
2. Detect issues across axes:
   - **CONFLICT**: requirements that contradict each other across axes
   - **GAP**: something mentioned in one axis but missing in others
   - **DUPLICATE**: same requirement expressed differently
3. Read existing `<spec_dir>/cross-check.md` (created by Phase 2 Post-processing). Preserve `## Dedup Log` verbatim.
4. Replace the body of `## Cross-Check Report` with discovery results:
   - List each issue with the requirement IDs involved
   - Collect all `confidence: low` and `open_questions` items from extractor outputs
   - Collect all assumptions the extractors made (items inferred but not directly sourced from Q&A)
   - Assign a stable issue ID to each item (`CC-1`, `CC-2`, ...) — IDs are sequential within this report and do not collide with prior runs.

After Phase 3 writes the report, `cross-check.md` is **immutable** until a Supplement axis or Full re-interview cycle starts (see Phase 4.3). Resolution state belongs in the final `requirements.md` draft and its `## Open Decisions` section, never in `cross-check.md`.

## Phase 4: User Confirmation & Finalization

Record Phase 4 start/end:

```bash
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase4 phase_start --label "Confirmation"
# ... after requirements.md is written
node "${baseDir}/../../scripts/specify-metrics.mjs" mark <spec_dir> phase4 phase_end --label "Confirmation"
```

Before writing the final `requirements.md`, surface everything to the user for explicit acceptance. This prevents assumptions from silently becoming "requirements."

### Step 4.1: Present Cross-Check Summary

**Data sources** (read each before composing the summary):
- `<spec_dir>/cross-check.md` `## Cross-Check Report` → Conflicts, Open Questions, Assumptions
- `<spec_dir>/reqs-business.md` / `reqs-interaction.md` / `reqs-tech.md` → Confirmed Requirement counts per axis
- `<spec_dir>/qa-log.md` frontmatter `where.non_goals` → Out of Scope list

Show the user a concise summary grouped into:

```
## Final Confirmation

### Confirmed Requirements
{count by axis: Business N, Interaction N, Tech N}

### Conflicts to Resolve ({count})
- {ID pair}: {conflict description}
  → Options to resolve

### Open Questions ({count})
- {ID}: {question} (axis: {axis})

### Assumptions to Accept ({count})
- {ID}: {assumption the extractor made} — accept / reject / replace

### Out of Scope (Non-Goals)
- {items from where.non_goals}
```

### Step 4.2: Resolve via AskUserQuestion

For each CONFLICT and ASSUMPTION, use AskUserQuestion with options (typically: accept / reject / modify / defer).

For OPEN QUESTIONS: either answer them now (free-text or AskUserQuestion) or explicitly defer them to the open_decisions list.

Apply resolutions to the in-memory requirements draft AND persist a one-line audit entry in `qa-log.md` per resolution so the work survives session compaction:

- **accept**: keep the requirement or assumption in the final draft.
- **reject**: remove or rewrite the affected requirement.
- **modify**: apply the user's replacement text, then re-show the affected requirement.
- **defer**: add an entry to the final `## Open Decisions` section.

**Persist resolution per decision** — immediately after the user answers an AskUserQuestion in this step, append one line to `qa-log.md` `## Resolutions`:

```
- CC-{N}: {accept | reject | modify | defer} — {short note or replacement text reference}
```

The `## Resolutions` section is created on first append if missing. This is the durable record; the in-memory draft is rebuilt from `cross-check.md` + this list on resume.

**Resume rule** — if Phase 4 resumes after interruption (compaction, crash, or `/specify` re-entry on the same `spec_dir`):
1. Read `cross-check.md` `## Cross-Check Report` for the full CC-N list.
2. Read `qa-log.md` `## Resolutions` for already-resolved CC-N entries.
3. Only ask about CC-N IDs that appear in (1) but not in (2).
4. Rebuild the requirements draft by replaying the `## Resolutions` list against `reqs-*.md`.

### Step 4.3: Preview final requirements

After all conflicts and assumptions are resolved, show the full requirements list before writing to disk:

```
[specify] Final Requirements Preview

Type: greenfield | Goal: "<goal>"
Non-goals: <list>

## R-B1: <title>
  - R-B1.1: <sub title>
    given: ... | when: ... | then: ...
  - R-B1.2: ...

## R-U1: <title>
  - R-U1.1: ...

## R-T1: <title>
  - R-T1.1: ...

Summary: {N} parent reqs, {M} sub-reqs (B:{b} U:{u} T:{t})
Open Decisions: {count or "none"}
```

Then ask:
```
AskUserQuestion(
  question: "Finalize these requirements?",
  options: [
    { label: "Approve", description: "Write requirements.md and finish" },
    { label: "Edit", description: "Modify specific requirements before writing" },
    { label: "Re-interview", description: "Go back to interview for missing coverage" }
  ]
)
```

If **Edit**: ask which requirements to change, apply edits, re-show preview. Max 3 rounds.
If **Re-interview**: choose one explicit path:

| Path | Use when | Re-run scope | File handling |
|---|---|---|---|
| **Supplement axis** | The gap is isolated to one axis | Reopen that axis in Phase 1 -> rerun that axis extractor -> rerun Phase 3 -> return to Phase 4 | Overwrite only the affected `reqs-{axis}.md`; keep the other two reqs files |
| **Full re-interview** | The goal/scope was misunderstood or multiple axes are invalid | Phase 1 full interview -> Phase 2 all extractors -> Phase 3 -> Phase 4 | Delete `reqs-*.md` and `cross-check.md`; keep `qa-log.md` and append a `## Re-interview` section |

Never mix old and new extractor outputs for an axis. Any axis that receives new Q&A must have its extractor rerun before Phase 3.

### Step 4.4: Write Final `requirements.md`

Only after user has explicitly approved the preview:

1. Read `${baseDir}/templates/requirements.md` template (cli format)
2. Overwrite `<spec_dir>/requirements.md` (replacing the stub created by `sr-harness-cli req init` at Phase 0.3). Final shape:
   ```markdown
   ---
   type: greenfield | feature | refactor | bugfix
   goal: "<one-line goal>"
   non_goals:
     - "<item>"
   ---

   # Requirements

   ## R-B1: <parent title>
   - behavior: <one-sentence system behavior>

   #### R-B1.1: <sub title>
   - given: <precondition>
   - when: <trigger>
   - then: <expected outcome>

   #### R-B1.2: ...

   ## R-U1: <Interaction requirement parent>
   ...

   ## R-T1: <Tech requirement parent>
   ...

   ## Pre-work

   - [ ] <action> (blocking)
   - [ ] <action> (non-blocking)

   ## Open Decisions

   ### OD-1: <title>
   - context: <why undecided>
   - options: [<A>, <B>]
   - impact: <what is blocked>
   ```
3. **ID rules** (must match `/blueprint`'s expectations):
   - Parent: `## R-X<num>:` at H2, where `X` is axis code (`B`=Business, `U`=Interaction, `T`=Tech)
   - Sub: `#### R-X<num>.Y:` at H4 with `given/when/then` lines
   - No axis grouping headings in the body (flat list); axis is encoded in the ID letter
4. **Frontmatter** carries only `type`, `goal`, `non_goals[]`. Do NOT add extra keys like `spec`, `phase`, `date`, `total_requirements` — those broke with cli's frontmatter format.
5. Pre-work is optional — include only when the interview surfaced actions the user must complete before execution (e.g., "get API key", "run migration"). Use this exact checkbox format:
   ```markdown
   ## Pre-work

   - [ ] <action text> (blocking)
   - [ ] <action text> (non-blocking)
   ```
   Allowed markers are exactly `(blocking)` and `(non-blocking)`. `/execute` gates only on unchecked `(blocking)` items; `(non-blocking)` items are reported but do not block execution.
6. Open Decisions is optional — omit the section if no unresolved decisions.
   - **Open Items → Open Decisions promotion**: items recorded in `qa-log.md` `## Open Items` (interview scratchpad) plus any `defer` resolutions from Step 4.2 are the source. Assign sequential `OD-N` IDs and write each as one entry in this section. The two names refer to the same concept at different stages — `Open Items` is the in-flight scratch, `Open Decisions` is the final consumed-by-`/blueprint` form.
7. Generate `<spec_dir>/performance.md` using the metrics helper.
8. Confirm completion with the user, showing final file path + next step: `/blueprint <spec_dir>/`, and mention the top bottleneck from `performance.md`.

### Step 4.5: KB Save (SR-Harness only)

Run only when `where.sr_modules` is set. Execute after Step 4.4 completes.

For each module in `where.sr_modules`:
1. Open `.sr-harness/knowledge/{product}/{module}.md` — skip if file does not exist
2. Identify new patterns discovered during this session (interface changes, naming conventions, constraints)
3. Locate the `## Accumulated Learnings` section by heading text (NOT by number — number is profile-dependent: §7 for non-driver, §9 for driver). Append a new bullet:
   ```
   - {date} [specify] {pattern summary}
   ```
4. Update `index.yaml`: set `scanned_at` to today's date (do NOT update `commit_sha` — that is only updated by `/knowledge scan`)

## Output Files

All outputs go to `<spec_dir>/` (default `.sr-harness/specs/{spec-name}/`):

| File | Phase | Description | Consumed by |
|------|-------|-------------|-------------|
| `requirements.md` | 0.3 (stub) / 4.3 (final) | Requirements in cli format (frontmatter + flat `## R-X` / `#### R-X.Y` with GWT) | `/blueprint` |
| `qa-log.md` | 1 | Full interview transcript | audit/traceability only |
| `reqs-business.md` | 2 | Axis extraction scratch | merged into requirements.md |
| `reqs-interaction.md` | 2 | Axis extraction scratch | merged into requirements.md |
| `reqs-tech.md` | 2 | Axis extraction scratch | merged into requirements.md |
| `cross-check.md` | 2 / 3 | Dedup log plus immutable conflict/gap/duplicate audit record | confirmation traceability only |
| `metrics/specify-events.jsonl` | 0-4 | Raw timing events for phase and operation analysis | diagnostic only |
| `performance.md` | 4.4 | Timing summary with bottleneck and improvement candidates | diagnostic only |

**Only `requirements.md` is load-bearing for downstream skills.** The other files are internal scratch/audit — /blueprint does not read them.

## CLI Dependency

- `sr-harness-cli req init <spec_dir> --type <t> --goal "<g>"` (Phase 0.3) — creates dir + requirements.md stub
- `node "${baseDir}/../../scripts/specify-metrics.mjs" ...` (Phases 0-4) — records timing diagnostics and writes `performance.md`
- No other cli commands are called directly by /specify. Phase 4.3 overwrites `requirements.md` directly via Write tool.
- Phase 0.5 may invoke the `/knowledge scan {module}` skill when the user chooses "Re-scan now" for stale KB. If that skill call fails or is aborted, fall back to agent scan for the module and record the fallback in `qa-log.md` `## Research`.

## Agents Used

| Agent | Phase | Purpose |
|-------|-------|---------|
| `gap-auditor` | 1 | Interview coverage validation |
| `business-extractor` | 2 | Business req extraction |
| `interaction-extractor` | 2 | Interaction req extraction (project-type-aware) |
| `tech-extractor` | 2 | Tech req extraction |
