---
name: brainstorm
description: '[Content] Use when you need to brainstorm as a PO/BA — structured ideation for problem-solving, new product creation, or feature enhancement.'
disable-model-invocation: false
---

> Codex compatibility note:
>
> - Invoke repository skills with `$skill-name` in Codex; this mirrored copy rewrites legacy Claude `/skill-name` references.
> - Task tracker mandate: BEFORE executing any workflow or skill step, create/update task tracking for all steps and keep it synchronized as progress changes.
> - User-question prompts mean to ask the user directly in Codex.
> - Ignore Claude-specific mode-switch instructions when they appear.
> - Strict execution contract: when a user explicitly invokes a skill, execute that skill protocol as written.
> - Subagent authorization: when a skill is user-invoked or AI-detected and its protocol requires subagents, that skill activation authorizes use of the required `spawn_agent` subagent(s) for that task.
> - Do not skip, reorder, or merge protocol steps unless the user explicitly approves the deviation first.
> - For workflow skills, execute each listed child-skill step explicitly and report step-by-step evidence.
> - If a required step/tool cannot run in this environment, stop and ask the user before adapting.

<!-- CODEX:PROJECT-REFERENCE-LOADING:START -->

## Codex Project-Reference Loading (No Hooks)

Codex uses static project-reference loading instead of runtime-injected project docs.
When coding, planning, debugging, testing, or reviewing, open project docs explicitly using this routing.

**Always read:**

- `docs/project-config.json` (project-specific paths, commands, modules, and workflow/test settings)
- `docs/project-reference/docs-index-reference.md` (routes to the full `docs/project-reference/*` catalog)
- `docs/project-reference/lessons.md` (always-on guardrails and anti-patterns)

**Missing/stale context route:** If `docs/project-config.json`, the docs index, `lessons.md`, `CLAUDE.md`, `AGENTS.md`, or any task-required reference doc is missing or stale, auto-run `$project-init` or the narrow setup route (`$project-config`, `$docs-init`, `$scan-all`, `$scan --target=<key>`, `$claude-md-init`) before ordinary project-specific work. If Codex mirrors or `AGENTS.md` are missing/stale, ask the user to run `$sync-codex`; do not auto-run it.

**Situation-based docs:**

- Project structure/architecture/tech-stack/deployment/setup (any layer — backend, frontend, or infra): `project-structure-reference.md`
- Backend/CQRS/API/domain/entity changes: `backend-patterns-reference.md`, `domain-entities-reference.md`
- Frontend/UI/styling/design-system: `frontend-patterns-reference.md`, `scss-styling-guide.md`, `design-system/README.md`
- Spec authoring, `docs/specs/` pathing, or TC format: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`
- Behavior/public-contract changes or spec-test-code sync: `workflow-spec-test-code-cycle-reference.md` plus the spec docs above
- Derived spec indexes/ERDs/reimplementation guides: `spec-system-reference.md` and source Feature Specs under `docs/specs/`
- Integration test implementation/review: `integration-test-reference.md`
- E2E test implementation/review: `e2e-test-reference.md`
- Code review/audit work: `code-review-rules.md` plus domain docs above based on changed files

Do not read all docs blindly. Start from `docs-index-reference.md`, then open only relevant files for the task.

<!-- CODEX:PROJECT-REFERENCE-LOADING:END -->

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:START -->

> **[BLOCKING]** Execute skill steps in declared order. NEVER skip, reorder, or merge steps without explicit user approval.
> **[BLOCKING]** Before each step or sub-skill call, update task tracking: set `in_progress` when step starts, set `completed` when step ends.
> **[BLOCKING]** Every completed/skipped step MUST include brief evidence or explicit skip reason.
> **[BLOCKING]** If Task tools are unavailable, create and maintain an equivalent step-by-step plan tracker with the same status transitions.

<!-- PROMPT-ENHANCE:STEP-TASK-ANCHOR:END -->

## Quick Summary

**Goal:** Facilitate a structured PO/BA brainstorming session via the Double Diamond process (diverge to discover problems and opportunities, then converge to validate and prioritize) to deliver a scored, ranked shortlist of 3-5 candidate ideas — each carrying a problem + value hypothesis, an identified riskiest assumption, and the cheapest validation test designed — so the team commits to the right problem AND the right solution before building, never to a flat unvalidated idea list. The default flow converges to ONE opinionated recommendation; the EXCEPTION is **Multi-Opportunity Discovery mode**, which instead outputs a ranked 3–8-item RICE opportunity map for user multi-select (each selected item becomes a separate PBI downstream).

**Summary:**

- **Main steps (Phases 0→7) — the read-this-if-nothing-else map:** **P0 Session Setup** (ask the user directly to detect scenario + role + how-much-known) → **P1 Problem Framing / Diamond-1 diverge** (POV statement → 5 Whys/Fishbone → JTBD job stories → 5–10 HMW) → **P2 Opportunity Framing / Diamond-1 converge** (OST / Lean Canvas / Blue-Ocean ERRC / Value-Prop Canvas) → **P3 Ideation / Diamond-2 diverge** (SCAMPER → Crazy 8s → Brainwriting 6-3-5 → Impact Mapping → Analogy = 25–40 raw ideas, zero judgment) → **P4 Evaluation / Diamond-2 converge** (Dot Vote → RICE → Kano → 2×2 → MoSCoW = ranked 3–5 shortlist) → **P5 Hypothesis Validation** (Problem + Value card + Riskiest-Assumption Test + cheapest test + Build-Measure-Learn per top-3) → **P6 Decision** (ONE opinionated recommendation + trade-offs) → **P7 Documentation & Handoff**. Multi-Opportunity Discovery mode swaps P6 for a ranked 3–8-item RICE opportunity map.
- Run ask the user directly Phase 0 FIRST to detect scenario (Problem-Solving / New Product / Enhancement / Multi-Opportunity Discovery), role (PO / BA / Mixed), and how-much-is-known — each scenario routes a different technique sequence (see Scenario Cheat Sheets) — why: misclassifying here derails every downstream phase.
- Strictly separate diverge (Phases 1 & 3 — generate, "Yes, and…", zero judgment) from converge (Phases 2 & 4 — narrow, RICE/Kano/MoSCoW scoring); mixing the two modes is the Golden Rule violation that kills idea output.
- Never stop at a raw or flat idea list: every top-3 candidate MUST carry a problem + value hypothesis card, an identified riskiest assumption (RAT), and the single cheapest validation test designed before any build commitment.
- Close with an opinionated decision (Phase 6 — recommend ONE option with trade-offs, not a menu), every claim evidence-backed at >80% confidence, then offer handoff by asking the user directly to `$idea`, `$refine`, `$plan`, etc. — EXCEPT in **Multi-Opportunity Discovery mode**, where convergence RANKS the opportunity map (3–8 RICE-scored items) and hands off via multi-select to a per-opportunity PBI loop instead of picking ONE winner.

**Four Scenarios:**

| Scenario                        | Entry Trigger                                                                     | Primary Methods                                                                |
| ------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Problem-Solving**             | "Something is broken / users complain / metric is bad"                            | 5 Whys → Fishbone → HMW → SCAMPER → Hypothesis RAT                             |
| **New Product**                 | "Greenfield idea / new market / no codebase yet"                                  | JTBD → Lean Canvas → Crazy 8s → Opportunity Scoring → Lean Hypothesis          |
| **Feature Enhancement**         | "Existing product / add capability / improve flow"                                | Opportunity Solution Tree → SCAMPER → Impact Mapping → RICE → Value Hypothesis |
| **Multi-Opportunity Discovery** | "Raw product vision / problem statement spanning multiple distinct opportunities" | JTBD / OST → SCAMPER → RICE opportunity map (3–8 items) → user multi-select    |

**Double Diamond (master meta-framework):**

```
DIAMOND 1: Right Problem          DIAMOND 2: Right Solution
────────────────────────────      ──────────────────────────
Discover ──► Define               Develop ──► Deliver
(diverge)    (converge)           (diverge)   (converge)
```

**Golden Rule:** NEVER evaluate ideas while generating them. Diverge and converge are separate modes. Mixing them kills creative output.

**Be skeptical. Apply critical thinking. Every idea needs a testable hypothesis. Confidence >80% required before recommending.**

---

## Answer this question:

<question>$ARGUMENTS</question>

---

## Phase 0: Session Setup (MANDATORY)

Use ask the user directly to detect scenario, role, and constraints before any technique.

### 0.1 — Scenario Detection

Ask:

1. **"What scenario are we in?"**
    - Problem-solving — something is broken, users struggle, a metric is bad
    - New product — greenfield, no existing product in this space
    - Feature enhancement — existing product, add/improve/remove capability
    - Multi-opportunity discovery — a raw product vision / problem statement spanning MULTIPLE distinct opportunities that should each become a separate PBI (do NOT converge to one — produce a ranked RICE opportunity map for multi-select; see [Multi-Opportunity Discovery Mode](#multi-opportunity-discovery-mode))
    - Mixed — multiple of the above

> **Mode routing:** If the input is a broad vision/problem spanning several distinct opportunities (typically driven by `workflow-idea-to-pbi`'s MULTI-OPPORTUNITY DISCOVERY MODE), select **Multi-opportunity discovery** — it changes Phase 6 convergence from "pick ONE" to "rank a 3–8-item RICE opportunity map for multi-select." All other scenarios keep the single-recommendation default.

2. **"What is the primary role in this session?"**
    - Product Owner — outcome-focused, business value, user outcomes
    - Business Analyst — requirements-focused, process analysis, stakeholder mapping
    - Both PO + BA — full discovery and requirements
    - Developer / Architect — technical feasibility brainstorm

3. **"How much is already known?"**
    - Raw seed — just an intuition or observation
    - Problem confirmed — we know the problem, need solutions
    - Solution direction known — need to evaluate and score options
    - Idea exists — need hypothesis validation only

### 0.2 — Context Loading

- If project codebase exists: read `docs/specs/` to understand domain
- If greenfield: skip codebase reading; rely on user input and web research
- Load `docs/project-reference/domain-entities-reference.md` if entity context needed
- Use `WebSearch` for market/competitor context when scenario = New Product or Enhancement

---

## Phase 1: Problem Framing — Diamond 1 Diverge

**Goal:** Fully understand problem space before jumping to solutions. #1 brainstorming failure: solving the wrong problem.

**Time-box:** 20–45 minutes of session time.

### 1.1 — Problem Statement (POV Format)

Formulate a crisp problem statement BEFORE any ideation:

```
[User/Persona] needs [need/job-to-be-done]
because [insight/root cause/context],
but [current barrier/friction/failure].
```

**Example:**

```
Operators need to quickly identify high-priority orders for action
because peak-season backlogs delay fulfillment,
but the current system shows raw order data with no ranking or comparison.
```

Use ask the user directly to validate:

- "Is this the core problem, or a symptom of a deeper problem?"
- "Who specifically experiences this? How often? What's the cost?"
- "What evidence do we have this problem actually exists?"

### 1.2 — Root Cause Analysis (for Problem-Solving scenario)

Apply one of:

**5 Whys:**

```
Problem: [stated problem]
Why 1: [first cause]
Why 2: [cause of cause 1]
Why 3: [cause of cause 2]
Why 4: [cause of cause 3]
Why 5: [root cause] ← Fix HERE, not at Why 1
```

**Fishbone (Ishikawa) — for systemic problems:**
Spine = problem statement. Bones = 6 cause categories:

- People, Process, Technology, Data, Environment, Policy
- For each bone: ask "What in this category could cause the problem?"

### 1.3 — JTBD (Jobs-To-Be-Done) — for New Product & Enhancement

Replace user stories with job stories to expose real motivation:

**User Story (what):** As an operator, I want to see order totals, so that I can make decisions.

**Job Story (why + context):** When I'm clearing a peak-season backlog with limited time, I want to instantly see which orders need action without opening every record, so I can make fast, defensible decisions before the cutoff.

**Job Story Formula:**

```
When [triggering situation + context],
I want to [motivation / job to be done],
so I can [outcome / expected result].
```

Generate 3–5 job stories covering main user segments. Each story = one opportunity.

### 1.4 — HMW (How Might We) Reframing

Transform problem statements into ideation-ready questions:

**Formula:** "How might we [verb] [object] so that [desired outcome]?"

From the POV statement:

- "How might we **help HR managers rank employees** so that promotion decisions take minutes not days?"
- "How might we **surface hidden top performers** so that managers discover talent they'd otherwise miss?"
- "How might we **reduce bias in performance scoring** so that promotion feels fair to all employees?"

**Rules:**

- Each HMW covers ONE idea direction
- Generate 5–10 HMW questions per problem
- Too broad = "How might we improve HR?" (useless) → too narrow = "How might we add a sort button?" (skip ideation, just build it)
- Sweet spot: one-concept questions that invite multiple solutions

**Output of Phase 1:**

- [ ] Problem statement (POV format)
- [ ] Root cause (5 Whys or Fishbone) — Problem-Solving only
- [ ] 3–5 Job Stories
- [ ] 5–10 HMW questions

---

## Phase 2: Opportunity Framing — Diamond 1 Converge

**Goal:** Narrow problem space to highest-opportunity focus areas before ideating solutions.

### 2.1 — Opportunity Solution Tree (OST) — for Enhancement

Teresa Torres' framework. Maps desired outcome → opportunities → solutions → experiments.

```
Desired Outcome (business metric)
├── Opportunity 1 (unmet user need / pain / want)
│   ├── Solution A
│   └── Solution B
├── Opportunity 2
│   ├── Solution C
│   └── Solution D
└── Opportunity 3 (deprioritized)
```

**Step 1:** State ONE desired outcome (lagging metric the team owns — e.g., "Increase manager satisfaction with review process from 3.2 to 4.0 CSAT")
**Step 2:** Map ALL known opportunities (pains, needs, wants) from research/interviews
**Step 3:** For each top opportunity, generate solution directions (not detailed solutions yet)
**Step 4:** Pick 1–2 opportunities to develop further in Phase 3

### 2.2 — Lean Canvas — for New Product

One-page business model for greenfield ideas (Ash Maurya):

| Block             | Question                              |
| ----------------- | ------------------------------------- |
| Problem           | Top 3 problems being solved           |
| Customer Segments | Who has this problem? Early adopters? |
| Unique Value Prop | Single compelling message             |
| Solution          | Top 3 features (not full spec)        |
| Channels          | How to reach customers                |
| Revenue Streams   | How to make money                     |
| Cost Structure    | Fixed + variable costs                |
| Key Metrics       | One number that measures success      |
| Unfair Advantage  | What can't easily be copied?          |

Fill one canvas per major target segment. Keep it to 20 min — speed is the point.

### 2.3 — Blue Ocean ERRC Grid — for Enhancement or New Product

Eliminate-Reduce-Raise-Create grid (Chan Kim & Mauborgne):

| Eliminate                   | Reduce                            |
| --------------------------- | --------------------------------- |
| Features users never use    | Features that are over-engineered |
| **Raise**                   | **Create**                        |
| Features users want more of | Features no competitor offers     |

**Rule:** Every innovation should have at least ONE item in Create AND one in Eliminate. A product with only Raise entries is incremental — not differentiated.

### 2.4 — Value Proposition Canvas

Connects customer profile to product value:

**Customer Profile:**

- Jobs (functional, social, emotional)
- Pains (frustrations, obstacles, risks)
- Gains (benefits, desires, measures of success)

**Value Map:**

- Products & Services (what you offer)
- Pain Relievers (how you reduce pains)
- Gain Creators (how you produce gains)

**Fit = where Pain Relievers match Pains + Gain Creators match Gains.**

**Output of Phase 2:**

- [ ] OST with 2 selected opportunities (Enhancement)
- [ ] Lean Canvas (New Product)
- [ ] ERRC grid (New Product or Enhancement)
- [ ] Value Proposition fit assessment

---

## Phase 3: Ideation — Diamond 2 Diverge

**Goal:** Generate maximum quantity of solution ideas without judgment. Quality comes Phase 4.

**Critical rule:** NO evaluation in this phase. Every idea is valid. "Yes, and..." not "Yes, but..."

### 3.1 — SCAMPER

Apply each lens to the problem/existing product to generate solution directions:

| Letter               | Prompt                     | Example for order-prioritization feature                      |
| -------------------- | -------------------------- | ------------------------------------------------------------- |
| **S**ubstitute       | What can be replaced?      | Replace manual sorting with AI-assisted ranking               |
| **C**ombine          | What can be merged?        | Combine status + history + SLA risk in one view               |
| **A**dapt            | What can be borrowed?      | Adapt Netflix recommendation to surface priority orders       |
| **M**odify           | What can be scaled/shrunk? | Shrink the review queue to a daily priority check             |
| **P**ut to other use | Different context?         | Use order history for restocking recommendations              |
| **E**liminate        | What can be removed?       | Eliminate the nightly batch — replace with continuous signals |
| **R**everse          | Flip the process?          | Let downstream stages pull orders instead of pushing          |

Generate at least 2 ideas per SCAMPER letter = minimum 14 ideas.

### 3.2 — Crazy 8s (Rapid Visual Ideation)

**Time-box: 8 minutes. 8 ideas. No refinement.**

Process:

1. Fold paper into 8 sections (or create 8 boxes mentally)
2. Sketch one idea concept per box — rough is fine
3. Timer forces quantity over perfection
4. Share and build on sketches

For AI-facilitated sessions:

- AI generates 8 distinct solution directions in 2 minutes
- User picks top 3 to explore deeper
- Each direction = 1 sentence + 1 key differentiator

### 3.3 — Brainwriting 6-3-5

For multi-stakeholder sessions (async-friendly):

- 6 participants, 3 ideas each, 5 rounds
- Each round: read previous ideas → add 3 new ideas OR build on existing
- Result: up to 108 ideas in 30 minutes (works async via shared doc)

For AI-facilitated sessions:

- AI plays all 6 roles across 3 rounds
- Generates ideas from: PO perspective, BA perspective, End User perspective, Dev perspective, Ops perspective, Business perspective

### 3.4 — Impact Mapping

Gojko Adzic's technique. Maps Goal → Actors → Impacts → Deliverables:

```
GOAL: [business outcome with measurable target]
├── ACTOR: Who can help/hinder?
│   ├── IMPACT: How should behavior change?
│   │   └── DELIVERABLE: What feature produces this impact?
│   └── IMPACT: What negative behavior to prevent?
│       └── DELIVERABLE: What reduces this risk?
└── ACTOR: ...
```

**Key insight:** Work backward from GOAL. If a deliverable doesn't trace to an actor behavior change, don't build it.

### 3.5 — Analogical Thinking

"How does [industry X] solve [similar problem Y]?"

| Analogy Source                | Application to HR                      |
| ----------------------------- | -------------------------------------- |
| Spotify Discover Weekly       | Personalized learning recommendations  |
| Uber surge pricing            | Dynamic bonus pool allocation          |
| GitHub PR reviews             | Peer skill endorsement with evidence   |
| Amazon recommendation engine  | Next goal suggestion                   |
| Netflix "because you watched" | "Colleagues like you also achieved..." |

**Output of Phase 3:**

- [ ] SCAMPER grid with 14+ ideas
- [ ] Crazy 8s — 8 solution directions
- [ ] Impact Map (top 2 goals)
- [ ] Analogy-inspired ideas (3–5)
- [ ] Total raw idea count: target 25–40 ideas

---

## Phase 4: Evaluation & Convergence — Diamond 2 Converge

**Goal:** Reduce 25–40 raw ideas to a ranked shortlist of 3–5 candidates for hypothesis testing.

### 4.1 — Dot Voting (First Pass)

Before scoring, do a quick gut-check elimination:

- Each idea gets a ✅ (keep) / ❌ (drop) / 🔄 (merge with another)
- Merge near-identical ideas
- Drop ideas that violate hard constraints (budget, tech, legal)
- Target: reduce to 10–15 candidates

### 4.2 — RICE Scoring

Rank remaining candidates:

```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach:      Users affected per quarter (100 / 500 / 1000 / 5000+)
Impact:     0.25 minimal | 0.5 low | 1 medium | 2 high | 3 massive
Confidence: 0.5 low (gut feel) | 0.8 medium (some data) | 1.0 high (validated)
Effort:     Story Points — 1 trivial | 3 small | 5 medium | 8 large | 13 very large
```

Score all 10–15 candidates. Sort descending. Top 5 = shortlist.

### 4.3 — Kano Model Classification

For each shortlisted idea, classify:

| Category        | Description           | If absent          | If present      | Example          |
| --------------- | --------------------- | ------------------ | --------------- | ---------------- |
| **Must-Be**     | Baseline expectation  | Users angry        | Users neutral   | Login works      |
| **Performance** | More = better         | Users dissatisfied | Users satisfied | Faster load      |
| **Delighter**   | Unexpected value      | Users neutral      | Users delighted | Smart suggestion |
| **Indifferent** | Doesn't matter        | Users neutral      | Users neutral   | Icon colors      |
| **Reverse**     | Some want, some don't | Segment upset      | Segment happy   | Auto-fill        |

**Strategy:** Must-Be → Performance → Delighter. Never skip Must-Be items for Delighters.

### 4.4 — Effort × Impact 2×2

Quick visual triage:

```
HIGH IMPACT
    │  Quick Wins ★    │  Major Projects ⚙️
    │  (do first)      │  (schedule carefully)
────┼──────────────────┼────────────────────
    │  Fill-Ins 📋     │  Money Pits ⚠️
    │  (if time)       │  (avoid or cut)
LOW IMPACT
         LOW EFFORT         HIGH EFFORT
```

Plot each shortlisted idea. Quick Wins = default first picks unless Major Project has strategic necessity.

### 4.5 — MoSCoW for Release Scope

For each idea in the shortlist, assign release priority:

| Priority        | Meaning                            | Threshold                              |
| --------------- | ---------------------------------- | -------------------------------------- |
| **Must Have**   | MVP is broken without it           | Include if >80% of value depends on it |
| **Should Have** | Important but MVP works without it | Include if RICE > median               |
| **Could Have**  | Nice to have, low risk to cut      | Include if effort ≤ 3 SP               |
| **Won't Have**  | Explicitly out of scope this cycle | Document for future                    |

**Output of Phase 4:**

- [ ] Dot-voted shortlist (10–15 ideas)
- [ ] RICE-scored table (top 5 ranked)
- [ ] Kano classification for each shortlisted idea
- [ ] 2×2 matrix placement
- [ ] MoSCoW assignment per idea

---

## Phase 5: Hypothesis Validation

**Goal:** Before committing to build, test riskiest assumptions. 42% of startups fail from no market need — validate before building.

### 5.1 — Problem Hypothesis

```markdown
**We believe** [target users/persona]
**Experience** [specific problem]
**Because** [root cause]
**We'll know this is true when** [validation metric/observable evidence]
```

**Example:**

```
We believe Operators
Experience frustration identifying high-priority orders during peak backlogs
Because order data is fragmented across 3 systems with no unified ranking
We'll know this is true when 3+ operators confirm they spend >2hrs per shift on manual data aggregation
```

### 5.2 — Value Hypothesis

```markdown
**We believe** [feature/solution]
**Will deliver** [specific value/outcome]
**To** [target users]
**We'll know we're right when** [measurable success metric]
```

### 5.3 — Riskiest Assumption Test (RAT)

Identify the ONE assumption whose failure kills the idea:

1. List all assumptions: user behavior, technical feasibility, market demand, business model
2. Score each: `Probability of being wrong (0–1) × Impact if wrong (0–1)`
3. Highest score = Riskiest Assumption
4. Design cheapest possible test to validate/invalidate it **before** full build:
    - User interview (2–3 days)
    - Landing page / fake door test (1 week)
    - Prototype click-through (3–5 days)
    - Concierge MVP (1–2 weeks)
    - Smoke test / pre-sell (2–4 weeks)

### 5.4 — Build-Measure-Learn Loop

For each top idea, define the loop:

```
BUILD: Minimum experiment to test the assumption (not a full product)
MEASURE: One metric that proves/disproves the hypothesis
LEARN: What decision do we make if metric is met / not met?
PIVOT: If hypothesis invalidated — which alternative from Phase 3 do we try next?
```

**Output of Phase 5:**

- [ ] Problem hypothesis card per top-3 idea
- [ ] Value hypothesis card per top-3 idea
- [ ] Riskiest Assumption identified per idea
- [ ] Cheapest test designed
- [ ] Build-Measure-Learn loop defined

---

## Phase 6: Decision & Recommendations

**Goal:** Present a clear, opinionated recommendation with trade-offs. Not "here are all the options" — "here's what we recommend and why."

### 6.1 — Top 3 Options Table

Present final shortlist as a decision table:

| Option   | RICE | Kano        | Effort | Risk   | RAT Test        | Recommendation |
| -------- | ---- | ----------- | ------ | ------ | --------------- | -------------- |
| Option A | 320  | Delighter   | 5 SP   | Medium | 3-day interview | ⭐ Recommended |
| Option B | 180  | Performance | 8 SP   | Low    | Prototype       | Viable         |
| Option C | 90   | Must-Be     | 13 SP  | High   | Pre-sell        | Defer          |

### 6.2 — Recommendation Statement

```
RECOMMENDED: [Option Name]

Why: [1–2 sentences on RICE + Kano + strategic fit]
Risk: [Primary risk + mitigation]
First step: [Cheapest test to validate before full commitment]
Time to validation: [Days/weeks]
```

### 6.3 — Dependency & Sequencing Check

- Does Option A depend on any existing feature/data/service not yet built?
- Can experiments run in parallel?
- What's the critical path to first validated learning?

---

## Multi-Opportunity Discovery Mode

> **Selected in Phase 0.1 when the input is a raw product vision / problem statement spanning MULTIPLE distinct opportunities.** This is an ADDITIONAL mode, not a replacement — every other scenario keeps the single-recommendation default of Phase 6.

**When to use:** the user hands off a broad vision, problem statement, or "explore this whole area" brief where several distinct, independently-shippable opportunities are expected — and each opportunity should become its own PBI downstream. This is the mode `workflow-idea-to-pbi`'s **MULTI-OPPORTUNITY DISCOVERY MODE** drives.

**How convergence differs (the defining difference):** the default flow converges to ONE opinionated recommendation (Phase 6). This mode does NOT. Instead, the SAME convergence techniques (RICE / Kano / 2×2 from Phase 4) are used to **RANK and present a map of 3–8 distinct opportunities** — NOT to pick a single winner. The user then multi-selects which opportunities to develop. Picking one winner here would discard the other PBIs the downstream workflow exists to produce.

**Technique flow:** run Phases 1–4 as normal (problem framing → opportunity framing → ideation → convergence), but in Phase 2 lean on JTBD / Opportunity Solution Tree to surface the FULL opportunity landscape (not a single focus area), and in Phase 4 use RICE / Kano / 2×2 to SCORE and RANK every distinct opportunity rather than collapse to a top recommendation.

**Output contract (must match what `workflow-idea-to-pbi` consumes):**

- An **opportunity map of 3–8 distinct, RICE-scored opportunities**, ranked descending by RICE.
- Documented in **`plans/{plan-dir}/brainstorm-opportunity-map.md`**.
- Each opportunity carries: a one-line problem/value framing, RICE components (Reach × Impact × Confidence / Effort) + RICE score, and (where known) a Kano class — so each can seed a downstream PBI.

```markdown
# Opportunity Map: [Vision/Problem]

| Rank | Opportunity | Problem/Value (1 line) | Reach | Impact | Confidence | Effort | RICE | Kano      |
| ---- | ----------- | ---------------------- | ----- | ------ | ---------- | ------ | ---- | --------- |
| 1    | ...         | ...                    | 1000  | 2      | 0.8        | 5      | 320  | Delighter |
| 2    | ...         | ...                    | ...   | ...    | ...        | ...    | ...  | ...       |
```

**Multi-select handoff:** present the ranked map by asking the user directly with `multiSelect: true` — "Which opportunities should we develop into PBIs?". The selected opportunities feed the **per-opportunity PBI loop** in `workflow-idea-to-pbi` (each selected opportunity → idea → refine → review → story → challenge → DoR → mockup, then a final cross-PBI prioritize). Do NOT author PBIs, specs, or plans inside this skill — the discovery mode's deliverable is the scored, multi-selected opportunity map only.

---

## Phase 7: Documentation & Handoff

### Report Output

Use naming pattern from `## Naming` section in injected context.

Create markdown summary report:

```markdown
# Brainstorm Session Report: [Topic]

## Session Context

- Scenario: [Problem-Solving / New Product / Enhancement]
- Role: [PO / BA / Mixed]
- Date: [YYYY-MM-DD]
- Input: [Original question/problem]

## Problem Statement

[POV format]

## Root Cause Analysis

[5 Whys or Fishbone — if Problem-Solving]

## Job Stories

1. [Job Story 1]
2. [Job Story 2]
3. [Job Story 3]

## HMW Questions

1. How might we...
2. How might we...

## Opportunity Map

[OST or Lean Canvas — per scenario]

## Raw Ideas Generated

[Total count: XX ideas across SCAMPER / Crazy 8s / Impact Mapping]

## Scored Shortlist (RICE)

| Rank | Idea | RICE | Kano | Effort | Priority    |
| ---- | ---- | ---- | ---- | ------ | ----------- |
| 1    | ...  | ...  | ...  | ...    | Must Have   |
| 2    | ...  | ...  | ...  | ...    | Should Have |

## Hypothesis Cards

### Top Recommendation: [Option Name]

- Problem Hypothesis: ...
- Value Hypothesis: ...
- Riskiest Assumption: ...
- Cheapest Test: ...
- Success Metric: ...

## Decision

[Recommendation + rationale]

## Next Steps

- [ ] [First concrete action]
- [ ] [Validation test]
- [ ] [Stakeholder alignment needed]
```

---

## Technique Quick Reference

| Technique                 | Phase | When to Use                        | Time-box |
| ------------------------- | ----- | ---------------------------------- | -------- |
| POV Statement             | P1    | Always                             | 10 min   |
| 5 Whys                    | P1    | Problem-solving scenario           | 15 min   |
| Fishbone                  | P1    | Systemic/complex problems          | 20 min   |
| JTBD / Job Stories        | P1    | New product or enhancement         | 20 min   |
| HMW Questions             | P1    | Always — bridge problem → ideation | 15 min   |
| Opportunity Solution Tree | P2    | Enhancement scenario               | 30 min   |
| Lean Canvas               | P2    | New product scenario               | 20 min   |
| Blue Ocean ERRC           | P2    | Differentiation needed             | 20 min   |
| Value Proposition Canvas  | P2    | Product-market fit unclear         | 25 min   |
| SCAMPER                   | P3    | Always — structured ideation       | 30 min   |
| Crazy 8s                  | P3    | Need quantity fast                 | 8 min    |
| Brainwriting 6-3-5        | P3    | Multi-stakeholder, async           | 30 min   |
| Impact Mapping            | P3    | Outcome-first thinking             | 30 min   |
| Analogical Thinking       | P3    | Novel/creative directions needed   | 15 min   |
| Dot Voting                | P4    | First-pass elimination             | 10 min   |
| RICE Scoring              | P4    | Always for prioritization          | 20 min   |
| Kano Model                | P4    | Feature classification             | 15 min   |
| 2×2 Effort/Impact         | P4    | Visual triage                      | 10 min   |
| MoSCoW                    | P4    | Release scoping                    | 15 min   |
| Problem Hypothesis        | P5    | Always before committing           | 15 min   |
| Value Hypothesis          | P5    | Always before committing           | 15 min   |
| Riskiest Assumption Test  | P5    | Before full build                  | 20 min   |
| Build-Measure-Learn       | P5    | Lean validation                    | 20 min   |

---

## Role-Specific Guidance

### PO Mode (Outcome Focus)

- Lead with: desired business outcome → opportunities → experiments
- Use: OST, Impact Mapping, RICE, Build-Measure-Learn
- Ask: "What behavior change do we need to see in users?"
- Resist: jumping to features before validating the outcome

### BA Mode (Requirements Focus)

- Lead with: stakeholder needs → process gaps → requirements
- Use: BABOK elicitation (interviews, workshops, document analysis), Fishbone, JTBD
- Ask: "What does the system need to do to enable that behavior?"
- Resist: over-specifying before the PO validates the opportunity

### Mixed PO + BA Mode

- PO owns: problem statement, opportunity framing, prioritization, hypothesis
- BA owns: requirements elicitation, acceptance criteria, edge cases, process mapping
- Handoff point: after Phase 4 (scored shortlist) → BA writes acceptance criteria per idea

---

## Collaboration Tools

- `planner` agent — research industry best practices for specific domain
- `docs-manager` agent — understand existing feature constraints and domain context
- `WebSearch` — market/competitor context for new product scenarios
- `docs-seeker` skill — latest documentation for external plugins/APIs
- `visual analysis tooling` skill — analyze visual mockups, screenshots, competitor UIs
- `sequential-thinking` skill — complex problem decomposition requiring structured causal chains
- `web-research` skill — deep market research for greenfield or competitive analysis

---

## Scenario Cheat Sheets

### Scenario A: Problem-Solving

```
1. POV Statement → 2. 5 Whys / Fishbone → 3. HMW Questions
→ 4. SCAMPER on current solution → 5. RICE scoring
→ 6. Problem Hypothesis + RAT → 7. Recommend + cheapest test
```

### Scenario B: New Product

```
1. Job Stories (JTBD) → 2. Lean Canvas → 3. Blue Ocean ERRC
→ 4. HMW Questions → 5. Crazy 8s / Brainwriting
→ 6. Kano Classification → 7. Value Hypothesis + RAT → 8. MVP scope
```

### Scenario C: Feature Enhancement

```
1. Job Stories (JTBD) → 2. Opportunity Solution Tree
→ 3. HMW Questions → 4. SCAMPER on existing feature
→ 5. Impact Mapping → 6. RICE scoring → 7. 2×2 matrix
→ 8. Value Hypothesis + RAT → 9. Recommend + next experiment
```

### Scenario D: Multi-Opportunity Discovery

```
1. Job Stories (JTBD) → 2. Opportunity Solution Tree (FULL landscape, not one focus)
→ 3. HMW Questions → 4. SCAMPER → 5. RICE-score EVERY opportunity
→ 6. Rank into a 3–8-item opportunity map (do NOT pick ONE)
→ 7. Write plans/{plan-dir}/brainstorm-opportunity-map.md
→ 8. ask the user directly multiSelect → hand selected opportunities to the per-opportunity PBI loop
```

> **Key difference from A/B/C:** converge to a RANKED MAP for multi-select, never a single recommendation. See [Multi-Opportunity Discovery Mode](#multi-opportunity-discovery-mode).

---

## Anti-Patterns to Avoid

| Anti-Pattern                                 | Why It Fails                                     | Better Approach                              |
| -------------------------------------------- | ------------------------------------------------ | -------------------------------------------- |
| Jumping to solutions before defining problem | Builds the wrong thing                           | Always complete Phase 1 first                |
| Evaluating ideas while generating them       | Kills creative output, premature closure         | Strict diverge/converge separation           |
| One stakeholder perspective only             | Misses jobs, pains, context                      | Brainwriting from 6 different roles          |
| No hypothesis before building                | 42% of features fail — no market need            | Always write hypothesis + RAT                |
| RICE without confidence score                | Overestimates low-evidence ideas                 | Always include Confidence as a multiplier    |
| Kano ignored — building only Delighters      | Users can't use a delighter with broken Must-Bes | Prioritize Must-Be → Performance → Delighter |
| "Best idea wins" without validation test     | HiPPO bias (Highest Paid Person's Opinion)       | Every top idea needs a RAT test design       |
| Scope creep in ideation                      | Ideas balloon beyond what team can validate      | Timebox each phase strictly                  |
| Treating RICE score as final truth           | RICE is directional, not precise                 | Use RICE + Kano + strategic context together |

---

## Critical Constraints

- **DO NOT implement solutions** — brainstorm and advise only
- **DO validate hypotheses** before endorsing any approach
- **DO prioritize long-term maintainability** over short-term convenience
- **DO consider both technical excellence and business pragmatism**
- **DO produce a scored, ranked shortlist** — never just a flat idea list
- **DO always design the cheapest validation test** — RAT before full spec

---

## Workflow Integration

After brainstorm session concludes, use ask the user directly to present next steps:

| Next Step              | When                                                        | Skill/Workflow          |
| ---------------------- | ----------------------------------------------------------- | ----------------------- |
| `$idea`                | Capture top idea as backlog artifact                        | `idea` skill            |
| `$refine`              | Turn top idea into actionable PBI with AC                   | `refine` skill          |
| `$web-research`        | Need deeper market/competitor research first                | `web-research` skill    |
| `$plan`                | Problem is clear, solution is validated, ready to implement | `plan` skill            |
| `$design-spec`         | UI-heavy idea, need wireframes before spec                  | `design-spec` skill     |
| `$domain-analysis`     | Idea touches domain entities, need model first              | `domain-analysis` skill |
| Continue brainstorming | More scenarios to explore                                   | Stay in this session    |

**Multi-Opportunity Discovery handoff:** when run in discovery mode, do NOT pick a single next step — instead present the ranked 3–8-item RICE opportunity map (written to `plans/{plan-dir}/brainstorm-opportunity-map.md`) by asking the user directly with `multiSelect: true`, then hand the selected opportunities to `workflow-idea-to-pbi`'s per-opportunity PBI loop. `workflow-idea-to-pbi` consumes this opportunity map directly.

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting. This prevents context loss from long sessions.

---

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

<!-- SYNC:critical-thinking-mindset -->

> **Critical Thinking Mindset** — Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
> **Anti-hallucination:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.

<!-- /SYNC:critical-thinking-mindset -->

<!-- SYNC:sequential-thinking-protocol -->

> **Sequential Thinking Protocol** — Structured multi-step reasoning for complex/ambiguous work. Use when planning, reviewing, debugging, or refining ideas where one-shot reasoning is unsafe.
>
> **Trigger when:** complex problem decomposition · adaptive plans needing revision · analysis with course correction · unclear/emerging scope · multi-step solutions · hypothesis-driven debugging · cross-cutting trade-off evaluation.
>
> **Format (explicit mode — visible thought trail):**
>
> 1. `Thought N/M: [aspect]` — one aspect per thought, state assumptions/uncertainty
> 2. `Thought N/M [REVISION of Thought K]: ...` — when prior reasoning invalidated; state Original / Why revised / Impact
> 3. `Thought N/M [BRANCH A from Thought K]: ...` — explore alternative; converge with decision rationale
> 4. `Thought N/M [HYPOTHESIS]: ...` then `[VERIFICATION]: ...` — test before acting
> 5. `Thought N/N [FINAL]` — only when verified, all critical aspects addressed, confidence >80%
>
> **Mandatory closers:** Confidence % stated · Assumptions listed · Open questions surfaced · Next action concrete.
>
> **Stop conditions:** confidence <80% on any critical decision → escalate by asking the user directly · ≥3 revisions on same thought → re-frame the problem · branch count >3 → split into sub-task.
>
> **Implicit mode:** apply methodology internally without visible markers when adding markers would clutter the response (routine work where reasoning aids accuracy).
>
> **Deep-dive:** see `$sequential-thinking` skill (`.claude/skills/sequential-thinking/SKILL.md`) for worked examples (API design, debugging, architecture), advanced techniques (spiral refinement, hypothesis testing, convergence), and meta-strategies (uncertainty handling, revision cascades).

<!-- /SYNC:sequential-thinking-protocol -->

<!-- SYNC:critical-thinking-mindset:reminder -->

**MUST ATTENTION** apply critical + sequential thinking — every claim needs appropriate traced evidence (`file:line` for repo/code claims; source URL or artifact section for research, product, content, and docs claims); confidence >80% to act, <60% DO NOT recommend. Anti-hallucination: never present guess as fact, admit uncertainty freely, cross-reference independently, stay skeptical of own confidence.

<!-- /SYNC:critical-thinking-mindset:reminder -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** apply sequential-thinking — multi-step Thought N/M, REVISION/BRANCH/HYPOTHESIS markers, confidence % closer; see `$sequential-thinking` skill.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- SYNC:ai-mistake-prevention:reminder -->

**MUST ATTENTION** apply AI mistake prevention — verify generated content against evidence, trace downstream references before deleting or renaming, verify all affected outputs, re-read files after context loss, and surface ambiguity before acting.

<!-- /SYNC:ai-mistake-prevention:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

<!-- SYNC:project-protocol-overlay -->

> **Project Protocol Overlay** — Before executing this skill, resolve any PROJECT overlay rules layered onto it: match this skill's name against the `Target` column of the project's skill-protocol index (`docs/project-reference/skill-protocols-reference.md` by default; a `referenceDocs` entry in `docs/project-config.json` overrides the path), taking the most specific matching tier ONLY — exact name > glob > `*`. **That precedence orders overlays against EACH OTHER, never against this skill.** Read ONLY the matched bodies, resolved as `<protocols-dir>/<Name>.md`; a row's Body link is display text, never a read path. A matched body that is missing or malformed is REPORTED and skipped — never reconstructed from the index Description. No index, or no match -> proceed with no overlay, silently. Full contract: `.claude/skills/project-skill-protocol/references/registry.md`.
>
> Overlays are **ADDITIVE ONLY**: they ADD rules on top of this skill's own protocol and NEVER replace, override, disable, or reinterpret a rule it already states — removing every overlay must return this skill to exactly its documented behavior. An overlay is a BRIEF, not an authority escalation: it can NEVER waive a workflow gate, git discipline, a review gate, or a user-confirmation gate. A genuine overlay-vs-skill conflict, or two equally-specific overlays that directly contradict -> surface both to the user; NEVER resolve silently.

<!-- /SYNC:project-protocol-overlay -->

<!-- SYNC:project-protocol-overlay:reminder -->

**MUST ATTENTION** resolve project protocol overlays for this skill BEFORE executing — most specific matching tier only (exact > glob > `*`, which ranks overlays against each other, NEVER against this skill), read only matched bodies at `<protocols-dir>/<Name>.md`; a missing or malformed body is reported, never reconstructed. Overlays are ADDITIVE ONLY (they never replace this skill's own rules) and are a brief, NEVER an authority escalation; an equal-specificity contradiction goes to the user.

<!-- /SYNC:project-protocol-overlay:reminder -->

## Closing Reminders

- **IMPORTANT MUST ATTENTION Goal:** Deliver a scored, ranked shortlist of 3-5 candidate ideas — each carrying a problem + value hypothesis, an identified riskiest assumption, and the cheapest validation test designed — so the team commits to the right problem AND the right solution before building, never to a flat unvalidated idea list.
- **IMPORTANT MUST ATTENTION Main steps (run in order, track each):** P0 Session Setup (detect scenario + role + known) → P1 Problem Framing/diverge (POV → 5 Whys/Fishbone → JTBD → HMW) → P2 Opportunity Framing/converge (OST / Lean Canvas / ERRC / Value-Prop) → P3 Ideation/diverge (SCAMPER → Crazy 8s → Brainwriting → Impact Map → Analogy, 25–40 ideas) → P4 Evaluation/converge (Dot Vote → RICE → Kano → 2×2 → MoSCoW, shortlist 3–5) → P5 Hypothesis Validation (Problem + Value card + RAT + cheapest test + Build-Measure-Learn) → P6 Decision (ONE recommendation) → P7 Documentation & Handoff — why: the skill's own phases are the steps AI most often forgets; re-anchor to them before each phase.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **AI Mistake Prevention:** verify generated content against evidence, trace downstream references, verify all affected outputs, re-read after context loss, surface ambiguity.
- **Critical Thinking:** traced `file:line` proof; confidence >80% to act; never guess.
- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers, confidence closer.

- **MANDATORY IMPORTANT MUST ATTENTION** detect scenario + role + how-much-known by asking the user directly Phase 0 FIRST — each scenario routes a different technique sequence — why: misclassifying scenario derails every downstream phase.
- **MANDATORY IMPORTANT MUST ATTENTION** separate diverge (Phases 1 & 3, generate, "Yes, and…", zero judgment) from converge (Phases 2 & 4, narrow + score) — NEVER evaluate ideas while generating them — why: mixing the two modes is the Golden Rule violation that kills creative output.
- **MANDATORY IMPORTANT MUST ATTENTION** NEVER stop at a raw or flat idea list — every top-3 candidate carries a problem + value hypothesis card, an identified riskiest assumption (RAT), and the single cheapest validation test designed before any build commitment — why: 42% of features fail from no market need; validate before building.
- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting; mark each `completed` immediately, add a final review todo — why: long brainstorm sessions lose context without external task tracking.
- **MANDATORY IMPORTANT MUST ATTENTION** search 3+ existing patterns first — read `docs/specs/` for domain (codebase) or `WebSearch` for market/competitor context (greenfield) before ideating — why: ideas ungrounded in domain or market evidence score on gut feel, not fit.
- **MANDATORY IMPORTANT MUST ATTENTION** cite evidence for every claim, confidence >80% to recommend; RICE Confidence is a multiplier, not optional — why: low-evidence ideas without a Confidence score get over-ranked.
- **MANDATORY IMPORTANT MUST ATTENTION** close with ONE opinionated recommendation + trade-offs (Phase 6) — never a flat menu of options — why: a menu pushes the decision back on the team and invites HiPPO bias. EXCEPTION — **Multi-Opportunity Discovery mode** (selected in Phase 0): do NOT pick ONE; instead RANK a 3–8-item RICE opportunity map, write it to `plans/{plan-dir}/brainstorm-opportunity-map.md`, and hand off by asking the user directly `multiSelect: true` to `workflow-idea-to-pbi`'s per-opportunity PBI loop — why: each opportunity becomes a separate downstream PBI, so collapsing to one would discard the backlog the discovery workflow exists to produce.
- **MANDATORY IMPORTANT MUST ATTENTION** use ask the user directly for all user decisions and handoff routing (`$idea`, `$refine`, `$plan`) — never auto-decide — why: the user owns scenario, prioritization, and next-step choices.

**Anti-Rationalization:**

| Evasion                                         | Rebuttal                                                                                     |
| ----------------------------------------------- | -------------------------------------------------------------------------------------------- |
| "Scenario is obvious, skip Phase 0 detection"   | Misclassified scenario routes the wrong technique sequence. Run ask the user directly first. |
| "Just list the ideas, evaluation can wait"      | A flat idea list is the deliverable failure. Score, rank, and hypothesis-test the top 3.     |
| "Skip the RAT — the idea is clearly good"       | "Clearly good" is HiPPO bias. Design the cheapest test before any build commitment.          |
| "Diverge and converge together to save time"    | Mixing modes kills creative output — the Golden Rule violation. Keep phases separate.        |
| "RICE without Confidence is close enough"       | No Confidence multiplier over-ranks low-evidence ideas. Always score Confidence.             |
| "Already know the domain, skip context loading" | Show `docs/specs/` read or `WebSearch` evidence. No proof = ungrounded ideation.             |

**MUST ATTENTION** Phase 0 scenario detection FIRST · diverge/converge strictly separated · every top-3 idea carries a hypothesis + RAT + cheapest test — these three survive long sessions; re-anchor to them before recommending.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:START -->

## Hookless Prompt Protocol Mirror (Auto-Synced)

Source: `.claude/.ck.json` + `.claude/skills/shared/sync-inline-versions.md` (`:full` blocks) + `.claude/scripts/lib/hookless-prompt-protocol.cjs`

## [WORKFLOW-EXECUTION-PROTOCOL] [BLOCKING] Workflow Execution Protocol — MANDATORY IMPORTANT MUST CRITICAL. Do not skip for any reason.

**Generic portability boundary:** Reusable skills and protocol text stay project-neutral; project-specific conventions are discovered from docs/project-config.json and docs/project-reference/. Apply shared AI-SDD from `shared/sdd-artifact-contract.md`. Read `docs/project-config.json` and `docs/project-reference/docs-index-reference.md`, then open the project reference docs named there. For spec, test-case, behavior-change, public-contract, or `docs/specs/` work, route through the local spec docs named by the docs index: `feature-spec-reference.md`, `spec-system-reference.md`, `spec-principles.md`, and `workflow-spec-test-code-cycle-reference.md` when specs/tests/code must stay synchronized. If either file or a required reference doc is missing or stale, auto-run `$project-init` (or the narrow lower-level route such as `$project-config`, `$docs-init`, `$scan-all`, or `$scan --target=<key>`) before ordinary project-specific work. Any supported AI tool may execute when this shared context and local docs are available.

1. **DETECT:** If the prompt starts with an explicit slash skill/workflow command, execute it directly. Otherwise match the prompt against the workflow catalog and skill list.
2. **ANALYZE:** Choose the best option: execute directly, invoke a skill, activate a standard workflow, or compose a custom step combination.
3. **AUTO-SELECT:** Pick the best option yourself. Do not ask the user to choose between direct execution, skill, standard workflow, or custom workflow.
4. **ACTIVATE:** For a selected workflow, call `$start-workflow <workflowId>`; for a selected skill, invoke that skill; for a custom workflow, sequence custom steps directly; for direct execution, proceed with the task.
5. **CREATE TASKS:** task tracking for ALL workflow/skill/custom steps before execution when the selected path has multiple steps.
6. **PARALLELIZE:** Before executing the task list, tag each task `PAR` (independent inputs + write set disjoint from every other `PAR` task) or `SEQ` (name the blocking dependency), group `PAR` tasks into waves, declare the wave plan, and spawn each wave's sub-agents in ONE message — all-return barrier per wave, fan-out one level deep unless a sub-agent's own definition authorizes further fan-out. Sequential-by-default is a defect when tasks are independent; do not parallelize shared write targets, output-consuming tasks, trivial single-file work, ordering a skill or workflow explicitly fixes, or user-approval gates.
7. **EXECUTE:** Advance per the **Workflow Step Advancement & Parallel Phases** rule in your context instructions — model-driven; a sub-agent completion advances a step identically to an inline call; a parallel-phase group is an all-return barrier (advance only after ALL members return, never serialize it)

## Shared AI-SDD Protocol Markers

Source: `.claude/skills/shared/sync-inline-versions.md`

## SYNC:ai-sdd-artifact-contract

> **AI-SDD Artifact Contract** — Shared spec-driven development rules stay portable and source-owned.
>
> 1. Keep reusable AI-SDD principles in `.claude`; put repository-specific paths, commands, owners, products, and formats in project config/reference docs.
> 2. Preserve cycle: `spec -> plan -> tasks -> implement -> verify -> update spec/docs`.
> 3. Trace every requirement or invariant through decision, task, TC/test, source evidence, and docs/spec update.
> 4. Treat code-to-spec extraction as reference-only until accepted by the canonical spec owner.
> 5. Any supported AI tool may plan, implement, review, or verify with synced context; using multiple tools is optional.
> 6. Update `.claude` source first, then sync generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`. — why: mirrors are generated artifacts; hand-edits are overwritten on the next sync
> 7. If `docs/project-config.json`, root instruction files, or a required project-reference doc is missing or stale, auto-run `$project-init` or the narrow lower-level route before ordinary project-specific work.
>
> **Active reference:** `shared/sdd-artifact-contract.md` in the active skills root.

---

## SYNC:ai-sdd-artifact-contract:reminder

- **MANDATORY** Apply `shared/sdd-artifact-contract.md`; keep reusable AI-SDD in `.claude` and local rules in project docs.
- **MANDATORY** Code-to-spec extraction is reference-only until canonical acceptance; any supported AI tool may execute with synced context.
- **MANDATORY** Update `.claude` source before syncing generated mirrors; do not manually edit `.agents`, `.codex`, or `AGENTS.md`.
- **MANDATORY** Missing or stale project config, root instruction files, or required reference docs route project-specific work through `$project-init` or the narrow setup route automatically.
  **[TASK-PLANNING] [MANDATORY]** BEFORE executing any workflow or skill step, create/update task tracking for all planned steps, then keep it synchronized as each step starts/completes.

## [LESSON-LEARNED-REMINDER] [BLOCKING] Task Planning & Continuous Improvement — MANDATORY. Do not skip.

Break work into small tasks (task tracking) before starting. Add final task: "Analyze AI mistakes & lessons learned".

**Extract lessons — ROOT CAUSE ONLY, not symptom fixes:**

1. Name the FAILURE MODE (reasoning/assumption failure), not symptom — "assumed API existed without reading source" not "used wrong enum value".
2. Generality test: does this failure mode apply to ≥3 contexts/codebases? If not, abstract one level up.
3. Write as a universal rule — strip project-specific names/paths/classes. Useful on any codebase.
4. Consolidate: multiple mistakes sharing one failure mode → ONE lesson.
5. **Recurrence gate:** "Would this recur in future session WITHOUT this reminder?" — No → skip `$learn`.
6. **Auto-fix gate:** "Could `$code-review`/`$code-simplifier`/`$security-review`/`$lint` catch this?" — Yes → improve review skill instead.
7. BOTH gates pass → ask user to run `$learn`.
   **[CRITICAL-THINKING-MINDSET]** Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence >80% to act.
   **Anti-hallucination principle:** Never present guess as fact — cite sources for every claim, admit uncertainty freely, self-check output for errors, cross-reference independently, stay skeptical of own confidence — certainty without evidence root of all hallucination.
   **AI Attention principle (Primacy-Recency):** Put the 3 most critical rules at both top and bottom of long prompts/protocols so instruction adherence survives long context windows.
   **Goal-driven execution:** Define success criteria first, loop until verified, and stop only when observable checks pass.
   **Tests verify intent:** Tests must protect business rules/invariants and fail when the protected intent breaks, not only mirror current behavior.

## Common AI Mistake Prevention (System Lessons)

- **Re-read files after context compaction.** Edit requires prior Read in same context; compaction wipes read state. Re-read before editing.
- **Grep for old terms after bulk replacements.** AI over-trusts find/replace completeness. Grep full repo after bulk edits for missed refs in docs/configs/catalogs.
- **Check downstream references before deleting.** Deletions cascade doc/code staleness. Map referencing files before removal.
- **After memory loss, check existing state before creating new.** Compaction wipes prior-work memory. Query current state to resume — never blindly duplicate.
- **Verify AI-generated content against actual code.** AI hallucinates APIs, class names, method signatures. Grep to confirm existence before documenting/referencing.
- **Trace full dependency chain after edits.** Changing a definition misses downstream consumers. Trace the full chain.
- **When renaming, grep ALL consumer file types.** Some file types silently ignore missing refs (no compile error). Search code, templates, configs, generated files.
- **Trace ALL code paths when verifying correctness.** Code existing ≠ code executing. Trace early exits, error branches, conditional skips — not just happy path.
- **Update docs that embed canonical data when source changes.** Docs inlining derived data (workflows, schemas, configs) go stale silently. Update all embedding docs alongside source.
- **Verify sub-agent results after context recovery.** Background agents may finish while parent compacted — grep-verify output, don't trust assumed completion.
- **Cross-check full target list against sub-agent assignments.** Parallel sub-agents by category miss boundary items. Reconcile union of assignments against target list before proceeding.
- **Sub-agents inherit knowledge only from their agent .md definition — use custom agent types, not built-in Explore.** Tool adoption = permission + knowledge + enforcement (numbered workflow step).
- **Persist sub-agent findings incrementally, not as a final batch.** Long sub-agents hit cutoffs before final write — findings lost. Instruct append-per-section to report file.
- **When debugging, ask "whose responsibility?" before fixing.** Trace caller (wrong data) vs callee (wrong handling). Fix at responsible layer — never patch symptom site.
- **Test failure → record a provisional verdict before trace/edit, then investigate.** Use the full five-way taxonomy: SOURCE-WRONG (production violates intent), TEST-WRONG (assertion/setup is stale), TEST-NOT-OPTIMAL (valid but fragile or low-signal test), ENVIRONMENT-BLOCKED (external state prevents a verdict), or AMBIGUOUS (intent/evidence cannot choose safely). Then trace root cause and triangulate against the governing spec (`docs/specs/**` if one exists) AND source. NEVER weaken an assertion, add a skip, relax a timeout, or change source merely to force green.
- **Grep ALL removed names after extraction/refactoring.** Primary file "done" ≠ secondary files clean. Grep entire scope for every removed symbol before declaring complete.
- **Assume existing values are intentional — ask WHY before changing OR flagging one as a defect.** Pattern-matching as "wrong" skips context. Before changing or reporting any constant/limit/flag/cutoff: read comments, git blame, the CALLER's ordering (the guarantee that makes the value correct usually lives in code running immediately BEFORE the cited line), and 2+ sibling call sites of the same convention. A doc stating WHAT without WHY is missing rationale, not proof of a missing guard — and in a validation pass, an accurate `file:line` citation proves the transcription, never the defect.
- **Verify ALL affected outputs, not just the first.** One build green ≠ all green. Multi-stack changes (backend/frontend/tests/docs) require verifying EVERY output.
- **Evaluate fit before copying a nearby pattern.** Closest example ≠ matching preconditions — verify the new context shares the same constraints, base classes, scope, lifetime.
- **Holistic-first debugging — resist nearest-attention trap.** Don't dive into first plausible cause. List EVERY precondition (config, env vars, paths, DB, endpoints, creds, versions, DI, data). Verify each against evidence (grep/query — not reasoning). Ask "what would falsify this?" — if nothing, it's not a hypothesis. Most expensive failure: going deeper in "obvious" layer while bug sits in layer never questioned.
- **Surgical changes — apply the diff test (context-aware).** Two modes: (1) Bug fix → every line traces to the bug; no restyling; orphan cleanup only for imports YOUR changes made unused. (2) Review/enhancement → implement improvements AND announce as "Enhancement beyond main request: [what]". Never silently scope-creep. Diff test: "Would this line exist if I wasn't asked to do X?" — if no, delete or announce.
- **Surface ambiguity before coding — don't pick silently.** Multiple valid interpretations → present each with effort: "[Request] could mean (1) [N h], (2) [N h]. Which matters?" List scope/format/volume/constraints assumptions first. If simpler path exists, say so. Never silently pick.
- **[MANDATORY FIRST ACTION] ALWAYS activate a suitable skill or workflow BEFORE responding.** Match task against workflow catalog + skill list; invoke via skill invocation or `$start-workflow <workflowId>`. NEVER answer or write code before checking. Skip = protocol violation.
- **Why-Review adversarial mindset — apply when reviewing any plan, decision, or design.** Default SKEPTIC not VALIDATOR: steel-man a rejected alternative, invert each stated reason ("what does it sacrifice?"), stress-test top 2-3 assumptions, run pre-mortem ("ships, fails in 3 months — what breaks?"), surface 1-2 alternatives author missed. Section presence ≠ quality; quality = causal reasoning + concrete mitigations + evidence, not "it's better" or "monitor closely".
- **Front-load report-write in sub-agent prompts for large reviews.** Many-file sub-agents hit budget before final write — findings lost. Design prompts so: (1) report-write is first explicit deliverable, (2) append per-file/section (not batched), (3) scope bounded so reads don't exhaust budget. Truncated mid-sentence with no report file → spawn narrower scope, don't retry same prompt.
- **After context compaction, re-verify all prior phase outcomes before continuing.** Summaries describe intent, not environment state (git index, filesystem, processes). On resume, FIRST audit: git status, re-read modified files, verify filesystem. Every "completed" claim is an untested hypothesis until evidence confirms.
- **OOM/memory: check row count before row size.** Triage: (1) Unbounded query — no DB filter for trigger? Push filter to DB; eliminates OOM. (2) Large rows? Projection reduces proportionally. Row reduction > projection in ROI.
- **Assert the outcome your system OWNS, never the intermediate state your INFRASTRUCTURE owns.** When testing anything asynchronous (queue/broker delivery, retries, background jobs, caches, replication), assert the final business/entity state. NEVER assert the delivery bookkeeping — consume/send status, attempt counts, last-error, row existence or counts in a broker, scheduler, or outbox/inbox table. That bookkeeping lives in shared infrastructure that ANY co-running process (a peer worker, a second replica, a leftover local container) can write, usually under a deterministic shared key, so the assertion silently tests the developer's environment instead of the system: green when run alone, flaky the instant anything else shares that broker + database. Gate question for every assertion: "would this hold no matter WHICH process did the work?" — if no, assert the converged data state instead. Corollary: process-local fault injection and in-process telemetry cannot gate work any process may perform — use them as stress amplifiers (arm → bounded window → disarm → assert convergence), never as preconditions.
- **Keep domain concepts out of generic/shared/infrastructure layers.** Reusable layer (shared library, framework, infra module) must reference NO consumer-specific domain concept — tenant/customer/product IDs, business entities, feature rules. Leak compiles + runs → passes review silently while coupling the "reusable" layer to one consumer. Keep shared type domain-free; push domain fields/logic down into the consumer via subclass/composition. — why: a layer coupled to one consumer's domain is no longer reusable.

<!-- CODEX:SYNC-PROMPT-PROTOCOLS:END -->
