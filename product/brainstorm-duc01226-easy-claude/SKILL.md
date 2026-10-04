---
name: brainstorm
description: '[Content] Use when a workflow step or the user asks for PO/BA brainstorming: new products, feature enhancement, roadmap framing. --mode={roadmap|scope}.'
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

**Goal:** Facilitate evidence-backed PO/BA Double-Diamond ideation that separates problem discovery from solution evaluation and delivers either a validated, ranked 3–5-candidate shortlist with problem/value hypotheses, each riskiest assumption, and cheapest validation test plus one recommendation—or, in **Multi-Opportunity Discovery mode**, a ranked 3–8-item RICE map for user selection—so the team commits to the right problem and solution, never a flat idea list.

**Summary:**

- **Ordered core:** P0 Setup (scenario/role/known + context) → P1 Problem Framing/diverge (POV, 5 Whys/Fishbone, JTBD, HMW) → P2 Opportunity Framing/converge (OST, Lean Canvas, ERRC, Value Proposition) → P3 Ideation/diverge (SCAMPER, Crazy 8s, Brainwriting, Impact Mapping, Analogy; 25–40 ideas) → P4 Evaluation/converge (Dot Vote, RICE, Kano, 2×2, MoSCoW; shortlist 3–5) → P5 Validation (problem/value cards, RAT, cheapest test, Build-Measure-Learn) → P6 Decision (one recommendation) → P7 Documentation/Handoff.
- **Purpose and gates:** Run ask user tool in P0 first; separate diverge from converge; test every top-3 candidate before build; Multi-Opportunity Discovery ranks 3–8 opportunities and uses multi-select.
- **Routing:** Resolve `--mode=roadmap|scope` before P0. Roadmap hands outcome/milestone framing to `$product-roadmap`; scope amends one approved `plans/{plan-id}/scope-brief.md` and stops before scenario/plan work (plans root default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides it).
- **Handoff boundary:** Apply `isLargeIdea`; when true, carry one complete `large_idea_decomposition` block in the owning handoff. Default mode offers user-selected handoff (`$idea`, `$pbi --mode=refine`, `$plan`, etc.); Multi-Opportunity Discovery hands selected items to the per-opportunity PBI loop.

**Workflow:**

1. **Session Setup** — ask user tool detects scenario, role, known context; load domain or market context.
2. **Problem Framing/diverge** — POV, root cause when applicable, JTBD, HMW.
3. **Opportunity Framing/converge** — scenario-specific OST, Lean Canvas, ERRC, Value Proposition.
4. **Ideation/diverge** — SCAMPER, Crazy 8s, Brainwriting, Impact Mapping, Analogy; no judgment.
5. **Evaluation/converge** — Dot Vote, RICE, Kano, 2×2, MoSCoW; rank 3–5 candidates or a 3–8 opportunity map.
6. **Hypothesis Validation** — problem/value cards, RAT, cheapest test, Build-Measure-Learn for top 3.
7. **Decision, Documentation & Handoff** — recommend one option by default; document and route user-approved next steps.

**Key Rules:**

- **Golden Rule:** NEVER evaluate ideas while generating them; diverge and converge stay separate.
- **Evidence:** Every claim and recommendation needs `file:line`, source, or traced evidence; confidence >80% required.
- **Output:** Scored, ranked shortlist with hypothesis validation—never a flat idea list.
- **User decisions:** Use ask user tool for scenario selection, prioritization, and handoff.
- **Technique selection:** Derive the sequence from the detected scenario; use cheat sheets for routing, not a one-size-fits-all checklist.
- **Risk profile:** Content skill; fresh-eyes review, specialist delegation, embedded sub-agent protocols, and recursive fix loops are N/A. Preserve the existing terminal state.

**Four Scenarios:**

| Scenario                       | Entry Trigger                                                                  | Primary Methods                                                                |
| ------------------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Problem-Solving**            | "Something is broken / users complain / metric is bad"                        | 5 Whys → Fishbone → HMW → SCAMPER → Hypothesis RAT                             |
| **New Product**                | "Greenfield idea / new market / no codebase yet"                              | JTBD → Lean Canvas → Crazy 8s → Opportunity Scoring → Lean Hypothesis          |
| **Feature Enhancement**        | "Existing product / add capability / improve flow"                           | Opportunity Solution Tree → SCAMPER → Impact Mapping → RICE → Value Hypothesis |
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

## Roadmap and Scope Modes

Resolve the flag before Phase 0:

| Mode | Purpose | Output / stop condition |
| --- | --- | --- |
| `--mode=roadmap` | Product-level framing for a broad vision or new product | Outcome hypothesis, actors, risks, 3–8 milestone candidates, non-goals, decisions, and evidence proposals; hand off to `$product-roadmap` to write/approve the roadmap artifact (default `docs/product-roadmap.md`; `docsRoots.productRoadmap.path` in `docs/project-config.json` overrides); no code, framework, schema, or timeline |
| `--mode=scope` | Clarify one selected roadmap milestone | Amend the exact selected `plans/{plan-id}/scope-brief.md` (plans root default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides) with in-scope behavior, non-goals, terms, source of truth, risks, decisions, and evidence; stop before `$scenario`/`$plan` |
| default | Standard Double Diamond ideation | Existing idea shortlist or multi-opportunity map flow below |

`--mode=roadmap` still requires owner approval. Use ask user tool for milestone boundaries and lifecycle terms. `$product-roadmap` owns the canonical artifact and selection gate; this mode supplies framing only.

`--mode=scope` MUST resolve an existing scope-brief path from the `$product-roadmap` handoff, `$ARGUMENTS`, or active plan, then amend that file in place. If no stable `plans/{plan-id}/scope-brief.md` exists — plans root default `plans/`, overridable via `docsRoots.plans.path` in `docs/project-config.json` — stop and route to `$product-roadmap`; NEVER create a competing brief or write one under `tmp/reports/`.

Default mode does not route to `--mode=roadmap` merely because the idea is broad. Evaluate:

```text
isLargeIdea = multipleIndependentOutcomes
            || ambiguousOrResearchHeavy
            || releaseScopeDecomposition
            || oversizedPbiThatMustSplit
```

When true, the brainstorm handoff owns this portable block; downstream skills consume it read-only. When all four signals are false, omit the block and roadmap/milestone placeholders. An existing roadmap is context unless the user explicitly chose `--mode=roadmap`.

## Answer this question:

<question>$ARGUMENTS</question>

---

## Phase 0: Session Setup (MANDATORY)

**MUST ATTENTION** Use ask user tool to detect scenario, role, and constraints before any technique.

### 0.1 — Scenario Detection

Ask:

1. **"What scenario are we in?"**
    - Problem-solving — something is broken, users struggle, a metric is bad
    - New product — greenfield, no existing product in this space
    - Feature enhancement — existing product, add/improve/remove capability
    - Multi-opportunity discovery — a raw product vision / problem statement spanning MULTIPLE distinct opportunities that should each become a separate PBI (do NOT converge to one — produce a ranked RICE opportunity map for multi-select; see [Multi-Opportunity Discovery Mode](#multi-opportunity-discovery-mode))
    - Mixed — multiple of the above

> **Mode routing:** A broad vision/problem spanning distinct opportunities (typically from `workflow-idea-to-pbi`'s MULTI-OPPORTUNITY DISCOVERY MODE) selects **Multi-opportunity discovery**. It changes Phase 6 from "pick ONE" to "rank a 3–8-item RICE map for multi-select." All other scenarios keep the single-recommendation default.

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

- Existing codebase: read the business spec root (default `docs/specs/`; `specRoots.business.path` in `docs/project-config.json` overrides) for domain context.
- Greenfield: skip codebase reading; use user input and web research.
- Read `domain-entities-reference.md` under the reference-docs root (default `docs/project-reference`; `docsRoots.projectReference.path` in `docs/project-config.json` overrides) only when entity context is needed.
- Use `WebSearch` for market/competitor context in New Product or Enhancement scenarios.

---

## Phase 1: Problem Framing — Diamond 1 Diverge

**Goal:** Understand the problem space before solutions; the primary brainstorming failure is solving the wrong problem.

**Time-box:** 20–45 minutes.

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

Use ask user tool to validate the framing:

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

- Each HMW covers ONE idea direction.
- Generate 5–10 HMW questions per problem.
- Too broad = "How might we improve HR?" (useless); too narrow = "How might we add a sort button?" (skip ideation, just build it).
- Sweet spot: one-concept questions inviting multiple solutions.

**Phase 1 output (all required):** Problem statement (POV); root cause (5 Whys or Fishbone, Problem-Solving only); 3–5 Job Stories; 5–10 HMW questions.

---

## Phase 2: Opportunity Framing — Diamond 1 Converge

**Goal:** Narrow the problem space to highest-opportunity focus areas before solution ideation.

### 2.1 — Opportunity Solution Tree (OST) — for Enhancement

Teresa Torres' framework: desired outcome → opportunities → solutions → experiments.

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

**Step 1:** State ONE desired outcome (lagging metric the team owns — e.g., "Increase manager satisfaction with review process from 3.2 to 4.0 CSAT").
**Step 2:** Map ALL known opportunities (pains, needs, wants) from research/interviews.
**Step 3:** For each top opportunity, generate solution directions, not detailed solutions.
**Step 4:** Pick 1–2 opportunities to develop in Phase 3.

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

Fill one canvas per major target segment. Time-box to 20 min; speed is the point.

### 2.3 — Blue Ocean ERRC Grid — for Enhancement or New Product

Eliminate-Reduce-Raise-Create grid (Chan Kim & Mauborgne):

| Eliminate                   | Reduce                            |
| --------------------------- | --------------------------------- |
| Features users never use    | Features that are over-engineered |
| **Raise**                   | **Create**                        |
| Features users want more of | Features no competitor offers     |

**Rule:** Every innovation needs at least ONE Create item and one Eliminate item. Raise-only products are incremental, not differentiated.

### 2.4 — Value Proposition Canvas

Connect customer profile to product value:

**Customer Profile:**

- Jobs (functional, social, emotional)
- Pains (frustrations, obstacles, risks)
- Gains (benefits, desires, measures of success)

**Value Map:**

- Products & Services (what you offer)
- Pain Relievers (how you reduce pains)
- Gain Creators (how you produce gains)

**Fit = Pain Relievers match Pains and Gain Creators match Gains.**

**Phase 2 output (all required):** OST with 2 selected opportunities (Enhancement); Lean Canvas (New Product); ERRC grid (New Product or Enhancement); Value Proposition fit assessment.

---

## Phase 3: Ideation — Diamond 2 Diverge

**Goal:** Generate maximum solution quantity without judgment; quality comes in Phase 4.

**Critical rule:** NO evaluation in this phase. Every idea is valid: "Yes, and...", not "Yes, but...".

### 3.1 — SCAMPER

Apply each lens to the problem/existing product; generate solution directions:

| Letter               | Prompt                     | Example for order-prioritization feature                  |
| -------------------- | -------------------------- | --------------------------------------------------------- |
| **S**ubstitute       | What can be replaced?      | Replace manual sorting with AI-assisted ranking           |
| **C**ombine          | What can be merged?        | Combine status + history + SLA risk in one view           |
| **A**dapt            | What can be borrowed?      | Adapt Netflix recommendation to surface priority orders   |
| **M**odify           | What can be scaled/shrunk? | Shrink the review queue to a daily priority check         |
| **P**ut to other use | Different context?         | Use order history for restocking recommendations          |
| **E**liminate        | What can be removed?       | Eliminate the nightly batch — replace with continuous signals |
| **R**everse          | Flip the process?          | Let downstream stages pull orders instead of pushing      |

Generate at least 2 ideas per SCAMPER letter: minimum 14 ideas.

### 3.2 — Crazy 8s (Rapid Visual Ideation)

**Time-box: 8 minutes; 8 ideas; no refinement.**

Process:

1. Fold paper into 8 sections (or create 8 boxes mentally).
2. Sketch one rough idea per box.
3. Let the timer force quantity over perfection.
4. Share and build on sketches.

For AI-facilitated sessions:

- AI generates 8 distinct solution directions in 2 minutes.
- User picks the top 3 to explore.
- Each direction = 1 sentence + 1 key differentiator.

### 3.3 — Brainwriting 6-3-5

For multi-stakeholder, async-friendly sessions:

- 6 participants, 3 ideas each, 5 rounds.
- Each round: read previous ideas → add 3 ideas OR build on an existing idea.
- Result: up to 108 ideas in 30 minutes; works asynchronously in a shared doc.

For AI-facilitated sessions:

- AI plays all 6 roles across 3 rounds.
- Generate from PO, BA, End User, Dev, Ops, and Business perspectives.

### 3.4 — Impact Mapping

Gojko Adzic's technique: Goal → Actors → Impacts → Deliverables:

```
GOAL: [business outcome with measurable target]
├── ACTOR: Who can help/hinder?
│   ├── IMPACT: How should behavior change?
│   │   └── DELIVERABLE: What feature produces this impact?
│   └── IMPACT: What negative behavior to prevent?
│       └── DELIVERABLE: What reduces this risk?
└── ACTOR: ...
```

**Key insight:** Work backward from GOAL. If a deliverable does not trace to an actor behavior change, do not build it.

### 3.5 — Analogical Thinking

Ask: "How does [industry X] solve [similar problem Y]?"

| Analogy Source                | Application to HR                      |
| ----------------------------- | -------------------------------------- |
| Spotify Discover Weekly       | Personalized learning recommendations  |
| Uber surge pricing            | Dynamic bonus pool allocation          |
| GitHub PR reviews             | Peer skill endorsement with evidence   |
| Amazon recommendation engine  | Next goal suggestion                   |
| Netflix "because you watched" | "Colleagues like you also achieved..." |

**Phase 3 output (all required):** SCAMPER grid with 14+ ideas; Crazy 8s with 8 directions; Impact Map for top 2 goals; 3–5 analogy-inspired ideas; 25–40 total raw ideas.

---

## Phase 4: Evaluation & Convergence — Diamond 2 Converge

**Goal:** Reduce 25–40 raw ideas to a ranked 3–5-candidate shortlist for hypothesis testing.

### 4.1 — Dot Voting (First Pass)

Before scoring, run a quick gut-check elimination:

- Each idea gets ✅ (keep), ❌ (drop), or 🔄 (merge).
- Merge near-identical ideas.
- Drop ideas violating hard constraints (budget, tech, legal).
- Target: 10–15 candidates.

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

Use for quick visual triage:

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

Assign release priority to each shortlisted idea:

| Priority        | Meaning                            | Threshold                              |
| --------------- | ---------------------------------- | -------------------------------------- |
| **Must Have**   | MVP is broken without it           | Include if >80% of value depends on it |
| **Should Have** | Important but MVP works without it | Include if RICE > median               |
| **Could Have**  | Nice to have, low risk to cut      | Include if effort ≤ 3 SP               |
| **Won't Have**  | Explicitly out of scope this cycle | Document for future                    |

**Phase 4 output (all required):** Dot-voted shortlist (10–15 ideas); top-5 RICE table; Kano classification; 2×2 placement; MoSCoW assignment per idea.

---

## Phase 5: Hypothesis Validation

**Goal:** Test riskiest assumptions before build commitment. 42% of startups fail from no market need; validate first.

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
4. Design the cheapest possible test to validate/invalidate it **before** full build:
    - User interview (2–3 days)
    - Landing page / fake door test (1 week)
    - Prototype click-through (3–5 days)
    - Concierge MVP (1–2 weeks)
    - Smoke test / pre-sell (2–4 weeks)

### 5.4 — Build-Measure-Learn Loop

Define the loop for each top idea:

```
BUILD: Minimum experiment to test the assumption (not a full product)
MEASURE: One metric that proves/disproves the hypothesis
LEARN: What decision do we make if metric is met / not met?
PIVOT: If hypothesis invalidated — which alternative from Phase 3 do we try next?
```

**Phase 5 output (all required):** Problem and Value hypothesis cards per top-3 idea; Riskiest Assumption per idea; cheapest test; Build-Measure-Learn loop.

---

## Phase 6: Decision & Recommendations

**Goal:** Present one clear, opinionated recommendation with trade-offs—not a menu—so the team knows what to do and why.

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

- Does Option A depend on an unbuilt feature, data source, or service?
- Can experiments run in parallel?
- What is the critical path to first validated learning?

---

## Multi-Opportunity Discovery Mode

> **Select in Phase 0.1 when the input is a raw product vision/problem spanning MULTIPLE distinct opportunities.** This is an additional mode; every other scenario keeps Phase 6's single-recommendation default.

**When to use:** a broad vision, problem statement, or "explore this whole area" brief expects several distinct, independently shippable opportunities, each becoming its own downstream PBI. This is the mode driven by `workflow-idea-to-pbi`'s **MULTI-OPPORTUNITY DISCOVERY MODE**.

**How convergence differs:** the default flow produces ONE opinionated recommendation (Phase 6); this mode does NOT. Use the SAME Phase 4 techniques (RICE / Kano / 2×2) to **RANK and present 3–8 distinct opportunities**, not a single winner. The user then multi-selects opportunities to develop; choosing one would discard downstream PBIs.

**Technique flow:** run Phases 1–4 normally (problem framing → opportunity framing → ideation → convergence). In Phase 2, use JTBD / Opportunity Solution Tree to surface the FULL landscape, not one focus; in Phase 4, use RICE / Kano / 2×2 to SCORE and RANK every distinct opportunity instead of collapsing to one recommendation.

**Output contract (must match what `workflow-idea-to-pbi` consumes):**

- An **opportunity map of 3–8 distinct, RICE-scored opportunities**, ranked descending by RICE.
- Documented in **`plans/{plan-dir}/brainstorm-opportunity-map.md`** (plans root default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides).
- Each opportunity carries: a one-line problem/value framing, RICE components (Reach × Impact × Confidence / Effort) + RICE score, and (where known) a Kano class — so each can seed a downstream PBI.

```markdown
# Opportunity Map: [Vision/Problem]

| Rank | Opportunity | Problem/Value (1 line) | Reach | Impact | Confidence | Effort | RICE | Kano |
| ---- | ----------- | ---------------------- | ----- | ------ | ---------- | ------ | ---- | ---- |
| 1    | ...         | ...                    | 1000  | 2      | 0.8        | 5      | 320  | Delighter |
| 2    | ...         | ...                    | ...   | ...    | ...        | ...    | ...  | ...  |
```

**Multi-select handoff:** present the ranked map with ask user tool and `multiSelect: true`: "Which opportunities should we develop into PBIs?". Selected opportunities feed `workflow-idea-to-pbi`'s **per-opportunity PBI loop** (idea → pbi --mode=refine → review → pbi --mode=story → challenge → DoR → mockup, then final cross-PBI prioritization). Do NOT author PBIs, specs, or plans here; the deliverable is only the scored, multi-selected map.

---

## Phase 7: Documentation & Handoff

### Report Output

Use the naming pattern from the injected `## Naming` section.

Create a Markdown summary report:

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

- Lead with desired business outcome → opportunities → experiments.
- Use OST, Impact Mapping, RICE, and Build-Measure-Learn.
- Ask: "What behavior change do we need to see in users?"
- Resist jumping to features before validating the outcome.

### BA Mode (Requirements Focus)

- Lead with stakeholder needs → process gaps → requirements.
- Use BABOK elicitation (interviews, workshops, document analysis), Fishbone, and JTBD.
- Ask: "What does the system need to do to enable that behavior?"
- Resist over-specifying before the PO validates the opportunity.

### Mixed PO + BA Mode

- PO owns problem statement, opportunity framing, prioritization, and hypothesis.
- BA owns requirements elicitation, acceptance criteria, edge cases, and process mapping.
- Handoff: after Phase 4's scored shortlist; BA writes acceptance criteria per idea.

---

## Collaboration Tools

- `planner` agent — research domain best practices.
- `docs-manager` agent — understand existing feature constraints and domain context.
- `WebSearch` — market/competitor context for New Product scenarios.
- `visual analysis tooling` skill — analyze mockups, screenshots, competitor UIs.
- `$web-research` — deep greenfield or competitive market research, and latest external plugin/API documentation (Context7 MCP optional where configured).

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
→ 7. Write plans/{plan-dir}/brainstorm-opportunity-map.md  (plans root default plans/; docsRoots.plans.path in docs/project-config.json overrides)
→ 8. ask user tool multiSelect → hand selected opportunities to the per-opportunity PBI loop
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

- **DO NOT implement solutions** — brainstorm and advise only.
- **DO validate hypotheses** before endorsing an approach.
- **DO prioritize long-term maintainability** over short-term convenience.
- **DO consider technical excellence and business pragmatism.**
- **DO produce a scored, ranked shortlist**—never a flat idea list.
- **DO design the cheapest validation test**—RAT before full spec.

---

## Workflow Integration

After the session, use ask user tool to present next steps:

| Next Step              | When                                                        | Skill/Workflow          |
| ---------------------- | ----------------------------------------------------------- | ----------------------- |
| `$idea`                | Capture top idea as backlog artifact                        | `idea` skill            |
| `$pbi --mode=refine`  | Turn top idea into actionable PBI with AC                   | `pbi` skill             |
| `$web-research`        | Need deeper market/competitor research first                | `web-research` skill    |
| `$plan`                | Problem is clear, solution is validated, ready to implement | `plan` skill            |
| `$design-spec`         | UI-heavy idea, need wireframes before spec                  | `design-spec` skill     |
| `$domain-analysis`     | Idea touches domain entities, need model first              | `domain-analysis` skill |
| Continue brainstorming | More scenarios to explore                                   | Stay in this session    |

**Multi-Opportunity Discovery handoff:** in discovery mode, do NOT pick one next step. Present the ranked 3–8-item RICE map (write to `plans/{plan-dir}/brainstorm-opportunity-map.md`; plans root default `plans/`, overridable via `docsRoots.plans.path` in `docs/project-config.json`) using ask user tool with `multiSelect: true`, then hand selected opportunities to `workflow-idea-to-pbi`'s per-opportunity PBI loop. `workflow-idea-to-pbi` consumes this map directly.

---

> **[IMPORTANT]** Use task tracking to break ALL work into small tasks BEFORE starting. This prevents context loss from long sessions.

---

<!-- PROTOCOL-GUIDES:START -->

> **Protocol guides** — A hook delivers each protocol's full text when this skill loads. If a protocol's text is not in your context, read its file below before you act on it.

- `sequential-thinking-protocol` — Structured multi-step reasoning with revision, branch and hypothesis markers; planning, debugging or reviewing complex or ambiguous work → .claude/skills/shared/protocols/sequential-thinking-protocol.md

<!-- PROTOCOL-GUIDES:END -->

<!-- SYNC:sequential-thinking-protocol:reminder -->

**MUST ATTENTION** use structured reasoning for complex or ambiguous work, implicitly when visible markers would clutter. Verify hypotheses, revise assumptions, and close with confidence, assumptions, open questions and a concrete next action.

<!-- /SYNC:sequential-thinking-protocol:reminder -->

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:START -->

## Prompt-Enhance Closing Anchors

**IMPORTANT MUST ATTENTION** follow declared step order for this skill; NEVER skip, reorder, or merge steps without explicit user approval
**IMPORTANT MUST ATTENTION** for every step/sub-skill call: set `in_progress` before execution, set `completed` after execution
**IMPORTANT MUST ATTENTION** every skipped step MUST include explicit reason; every completed step MUST include concise evidence
**IMPORTANT MUST ATTENTION** if Task tools unavailable, maintain an equivalent step-by-step plan tracker with synchronized statuses

<!-- PROMPT-ENHANCE:STEP-TASK-CLOSING:END -->

## Closing Reminders

**IMPORTANT MUST ATTENTION Goal:** Facilitate evidence-backed PO/BA Double-Diamond ideation that separates problem discovery from solution evaluation and delivers either a validated, ranked 3–5-candidate shortlist with problem/value hypotheses, each riskiest assumption, and cheapest validation test plus one recommendation—or, in **Multi-Opportunity Discovery mode**, a ranked 3–8-item RICE map for user selection—so the team commits to the right problem and solution, never a flat idea list.
- **IMPORTANT MUST ATTENTION Main steps:** detect scenario/role → frame the problem → frame opportunities → diverge ideas → converge and score → validate hypotheses → decide or rank the opportunity map → document and hand off.
- **IMPORTANT MUST ATTENTION Roadmap mode:** `--mode=roadmap` is explicit-only; it frames outcome-based milestones, risks, non-goals, human decisions, and evidence, then hands off to `$product-roadmap`; it does not choose technology or implementation.
- **IMPORTANT MUST ATTENTION Embedded decomposition:** when any shared `isLargeIdea` signal is true, write the complete five-field `large_idea_decomposition` block in the owning handoff and carry its stable slice IDs into PBIs, stories, mock-ups, and the all-PBI presentation; do not create a default roadmap file.
- **IMPORTANT MUST ATTENTION Scope mode:** `--mode=scope` resolves and amends exactly one approved `plans/{plan-id}/scope-brief.md` in place (plans root default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides), then stops before `$scenario` or `$plan`; it never creates a competing brief.
- **IMPORTANT MUST ATTENTION Main steps (run in order, track each):** P0 Setup (detect scenario/role/known + context) → P1 Problem Framing/diverge (POV → 5 Whys/Fishbone → JTBD → HMW) → P2 Opportunity Framing/converge (OST / Lean Canvas / ERRC / Value Proposition) → P3 Ideation/diverge (SCAMPER → Crazy 8s → Brainwriting → Impact Mapping → Analogy, 25–40 ideas) → P4 Evaluation/converge (Dot Vote → RICE → Kano → 2×2 → MoSCoW, shortlist 3–5) → P5 Validation (problem/value cards + RAT + cheapest test + Build-Measure-Learn for top 3) → P6 Decision (one recommendation, or Multi-Opportunity map) → P7 Documentation/Handoff — why: phase steps are easy to forget in long sessions; re-anchor before each phase.

**Protocols in force (concise digest of the SYNC/shared blocks this skill carries):**

- **Sequential Thinking:** multi-step Thought N/M with REVISION/BRANCH/HYPOTHESIS markers, confidence closer.

- **MANDATORY IMPORTANT MUST ATTENTION** detect scenario + role + how-much-known using ask user tool Phase 0 FIRST — each scenario routes a different technique sequence — why: misclassifying scenario derails every downstream phase.
- **MANDATORY IMPORTANT MUST ATTENTION** separate diverge (Phases 1 & 3, generate, "Yes, and…", zero judgment) from converge (Phases 2 & 4, narrow + score) — NEVER evaluate ideas while generating them — why: mixing the two modes is the Golden Rule violation that kills creative output.
- **MANDATORY IMPORTANT MUST ATTENTION** NEVER stop at a raw or flat idea list — every top-3 candidate carries a problem + value hypothesis card, an identified riskiest assumption (RAT), and the single cheapest validation test designed before any build commitment — why: 42% of features fail from no market need; validate before building.
- **MANDATORY IMPORTANT MUST ATTENTION** break work into small todo tasks using task tracking BEFORE starting; mark each `completed` immediately, add a final review todo — why: long brainstorm sessions lose context without external task tracking.
- **MANDATORY IMPORTANT MUST ATTENTION** search 3+ existing patterns first — read the business spec root (default `docs/specs/`; `specRoots.business.path` in `docs/project-config.json` overrides) for domain (codebase) or `WebSearch` for market/competitor context (greenfield) before ideating — why: ideas ungrounded in domain or market evidence score on gut feel, not fit.
- **MANDATORY IMPORTANT MUST ATTENTION** cite evidence for every claim, confidence >80% to recommend; RICE Confidence is a multiplier, not optional — why: low-evidence ideas without a Confidence score get over-ranked.
- **MANDATORY IMPORTANT MUST ATTENTION** close with ONE opinionated recommendation + trade-offs (Phase 6) — never a flat menu of options — why: a menu pushes the decision back on the team and invites HiPPO bias. EXCEPTION — **Multi-Opportunity Discovery mode** (selected in Phase 0): do NOT pick ONE; instead RANK a 3–8-item RICE opportunity map, write it to `plans/{plan-dir}/brainstorm-opportunity-map.md` (plans root default `plans/`; `docsRoots.plans.path` in `docs/project-config.json` overrides), and hand off using ask user tool `multiSelect: true` to `workflow-idea-to-pbi`'s per-opportunity PBI loop — why: each opportunity becomes a separate downstream PBI, so collapsing to one would discard the backlog the discovery workflow exists to produce.
- **MANDATORY IMPORTANT MUST ATTENTION** use ask user tool for all user decisions and handoff routing (`$idea`, `$pbi --mode=refine`, `$plan`) — never auto-decide — why: the user owns scenario, prioritization, and next-step choices.

**Anti-Rationalization:**

| Evasion                                          | Rebuttal                                                                              |
| ------------------------------------------------ | ------------------------------------------------------------------------------------- |
| "Scenario is obvious, skip Phase 0 detection"    | Misclassified scenario routes the wrong technique sequence. Run ask user tool first. |
| "Just list the ideas, evaluation can wait"       | A flat idea list is the deliverable failure. Score, rank, and hypothesis-test the top 3. |
| "Skip the RAT — the idea is clearly good"        | "Clearly good" is HiPPO bias. Design the cheapest test before any build commitment.   |
| "Diverge and converge together to save time"     | Mixing modes kills creative output — the Golden Rule violation. Keep phases separate. |
| "RICE without Confidence is close enough"        | No Confidence multiplier over-ranks low-evidence ideas. Always score Confidence.      |
| "Already know the domain, skip context loading"  | Show a read of the business spec root (default `docs/specs/`; `specRoots.business.path` in `docs/project-config.json` overrides) or `WebSearch` evidence. No proof = ungrounded ideation. |

**MUST ATTENTION** Phase 0 scenario detection FIRST · diverge/converge strictly separated · every top-3 idea carries a hypothesis + RAT + cheapest test — these three survive long sessions; re-anchor to them before recommending.
