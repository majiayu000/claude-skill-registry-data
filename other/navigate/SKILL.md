---
name: navigate
description: "Artifact status + multi-phase orchestration. Scan what exists, check freshness, compose and track complex workflows across sessions. Not for skill routing (the agent does that proactively)."
argument-hint: "'status' or 'orchestrate [goal]'"
allowed-tools: Read Grep Glob Bash
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "3.0.0"
  budget: fast
  estimated-cost: "$0.03-0.10"
promptSignals:
  phrases:
    - "what skills should i use"
    - "which skill"
    - "where do i start"
    - "project status"
    - "what skills do we have"
  allOf:
    - [which, skill]
  anyOf:
    - "navigate"
    - "skill"
    - "workflow"
    - "status"
  noneOf: []
  minScore: 6
routing:
  intent-tags:
    - artifact-scan
    - staleness-check
    - project-status
    - workflow-planning
  position: utility
  produces:
    - workflow-plan.md
  consumes: []
  requires: []
  defers-to: []
  parallel-with: []
  interactive: false
  estimated-complexity: medium
---

# Navigate

*Meta — Utility. Artifact awareness and multi-phase orchestration.*

**Core Question:** "What exists, and how do I track a complex workflow across sessions?"

> **Note:** Skill routing (matching a user's goal to the right skills) is the agent's job — it reads skill descriptions and proposes matches proactively on every response. Navigate does NOT route. It provides artifact state awareness and persistent workflow tracking that the agent can't do implicitly.

---

## Two Modes

### Status
**When:** Argument is `status` or user asks "what exists", "what's stale", "what do I have"

Scan `.agents/` **and the canonical top-level folders** (`brand/`, `architecture/`, `research/`), then report. Single-pass, no sub-agents.

1. **Scan** every `.md` file in:
   - `.agents/` (pipeline artifacts — including `.agents/meta/`)
   - `brand/`, `architecture/`, `research/` (canonical records)

   For each, read frontmatter to extract `skill:`, `date:`, `status:`, `version:`. Missing fields = `—`. Most meta-skill artifacts (`.agents/meta/`) are ephemeral analysis outputs — report them but weigh them lightly in recommendations. Exception: `meta/review-chain-report.md` is consumed by `/ship` as a review gate, so treat it as a real dependency when ship is in the workflow. Also scan `.agents/meta/out-of-scope/` — report count of out-of-scope decisions and flag any whose "Revisit if" conditions may now be met.

2. **Report** as a table sorted by date (newest first), with a `Location` column distinguishing `.agents/` pipeline outputs from top-level canonical records. Mark **STALE** if `date:` > 30 days old.

```
| Artifact | Location | Skill | Date | Age | Status |
|----------|----------|-------|------|-----|--------|
| product-context.md | research/ | icp-research | 2026-03-15 | 13d | ok |
| system-architecture.md | architecture/ | system-architecture | 2026-03-10 | 18d | ok |
| solution-design.md | .agents/ | solution-design | 2026-02-10 | 46d | STALE |
```

If none of the scanned folders exist or all are empty, say so.

3. **Recommend** the one or two skills that unblock the most, using the dependency graph below. Don't dump a flat list of everything missing — trace the graph, find the root blocker.

### Orchestrate
**When:** Argument starts with `orchestrate` or user asks for a full workflow plan

1. Scan `.agents/` + `brand/` + `architecture/` + `research/` for existing artifacts (same as Status step 1)
2. Check `.agents/meta/out-of-scope/` — if the goal overlaps with a prior out-of-scope decision, surface it: "This was previously scoped out because [reason]. Revisit condition: [condition]. Proceed anyway?"
3. Classify the goal, match to skills using the skill registry, check dependencies, identify parallel tracks
4. Produce a `workflow-plan.md` artifact with phases, checkpoints, and progress tracking
5. Return the plan + instructions for Phase 1

**Continuation:** Run `/navigate orchestrate` again (no new goal) to validate current phase, update progress, and recommend next phase.

---

## Orchestrate Output Format

```markdown
---
skill: navigate
version: 1
date: [today]
status: in-progress
goal: "[user's goal]"
---

# Workflow: [Goal Title]

## Phases

### Phase 1: [Name]
- [ ] /[skill] -> [artifact]
**Decisions:**
- Mechanical: [auto-decided, not surfaced]
- Taste: [auto-decided, surfaced at checkpoint]
- User Challenge: [must ask before proceeding]
**Checkpoint:** [validation criteria]

### Phase 2: [Name]
- [ ] /[skill] -> [artifact]
**Decisions:**
- [same format]
**Checkpoint:** [validation criteria]

## Status
Current phase: 1
Next action: Run `/[first-skill] [context]`
```

---

## Decision Classification

In Orchestrate mode, classify decisions within each phase into three types:

| Type | Behavior | Examples |
|------|----------|---------|
| **Mechanical** | Auto-decide silently — obvious from context, low risk | "Use the ORM already in the codebase", "Follow existing naming conventions" |
| **Taste** | Auto-decide but surface at phase checkpoint for user review | "Chose polling over WebSockets because latency requirements are relaxed", "Picked 3 personas instead of 2" |
| **User Challenge** | Always ask — never assume | "Should we support mobile?", "Which pricing tier to target?", "Build vs buy for auth?" |

**How to classify:**
- If the codebase, spec, or prior artifacts answer it → **Mechanical**
- If you have a defensible recommendation but the user might disagree → **Taste**
- If it's expensive to reverse, subjective, or has business implications → **User Challenge**

**In the workflow plan**, annotate each phase:
```
### Phase 2: Architecture
- [ ] /system-architecture -> system-architecture.md
**Decisions:**
- Mechanical: tech stack (matches existing codebase)
- Taste: DB schema normalization level — will default to 3NF, surface at checkpoint
- User Challenge: self-hosted vs managed DB — must ask before proceeding
```

**At phase checkpoints**, present Taste decisions as a batch: "I made these calls — confirm or override before I continue." User Challenges block the phase until answered.

## Checkpoint Validation

Between phases in orchestrate mode:

1. **Existence** — required artifacts exist
2. **Freshness** — `date` field < 30 days
3. **Completeness** — valid frontmatter present
4. **Status** — `final` preferred; `draft` triggers warning

```
Phase [N] Checkpoint: PASS / WARNING / BLOCKED
```

---

## Cross-Project Mode (--cross-project)

When invoked with `--cross-project`:

1. Scan `.agents/` in current directory AND sibling skill repo directories
2. Report unified table with **Project** column
3. Trace cross-project dependencies
4. Recommend highest-impact action across ALL projects

---

## Dependency Graph (Canonical)

Artifacts are **optional save-points**, not mandatory pipeline gates. The graph shows what CAN flow between skills, not what MUST exist on disk. Conversation context from the current session is equally valid.

```
product-context.md <- /icp-research
|-> market-research.md <- /market-research --+
|-> problem-analysis.md <- /problem-analysis -+
|                                             +-> solution-design.md <- /solution-design
|                                             |   |-> targets.md <- /funnel-planner -> experiment-*.md
|                                             |   |-> mkt/imc-plan.md <- /imc-plan -> mkt/content/ -> mkt/*.humanized.md
|                                             |   +-> system-architecture.md <- /system-architecture
|                                             |       +-> tasks.md <- /task-breakdown
|                                             |           +-> (execute) -> meta/review-chain-report.md <- /review-chain
|                                             |               +-> ship-report.md <- /ship
|                                             |                   +-> deploy-verify-report.md <- /deploy-verify
|-> /discover (conversation context or spec.md) --+
|-> design/brand-system.md <- /brand-system
+-> product/flow/*.md + product/flow/index.md <- /user-flow --> system-architecture.md, tasks.md
```

---

## Priority Table

When recommending next action. Note: if discover ran in the current session, its decisions are in conversation context — no spec.md file is required.

| If missing/stale | Run | Because |
|------------------|-----|---------|
| `product-context.md` | `/icp-research` | 12+ downstream skills depend on it |
| `market-research.md` or `problem-analysis.md` | `/market-research` or `/problem-analysis` | Feed into `/solution-design` |
| `solution-design.md` | `/solution-design` | Architecture, funnel, comms need it |
| No clarity on what to build (no conversation or spec) | `/discover` | Need alignment before architecture |
| `system-architecture.md` | `/system-architecture` | Can't decompose without design |
| `tasks.md` | `/task-breakdown` | Needs architecture first |

---

## Pre-Built Workflow Templates

### Technical Build
**Triggers:** "build the app", "implement", "code it"
```
Phase 1: /discover (interactive conversation — optionally saves spec.md)
Phase 2: /system-architecture -> system-architecture.md
Phase 3: /task-breakdown -> tasks.md
Phase 4: (execution, /review-chain after critical tasks)
Phase 5: /code-cleanup + /technical-writer (parallel)
Phase 6: /ship -> ship-report.md
Phase 7: /deploy-verify -> deploy-verify-report.md
```

### Full Product Launch
**Triggers:** "launch", "new product", "go to market"
```
Phase 1: /icp-research -> product-context.md
Phase 2: /market-research + /problem-analysis (parallel)
Phase 3: /solution-design -> solution-design.md
Phase 4: /brand-system + /imc-plan + /funnel-planner (parallel)
Phase 5: /user-flow -> product/flow/<flow-name>.md (once per flow)
Phase 6: /discover (interactive conversation)
Phase 7: /system-architecture -> system-architecture.md
Phase 8: /task-breakdown -> tasks.md + execution (/review-chain after critical tasks)
Phase 9: /ship -> ship-report.md
Phase 10: /deploy-verify -> deploy-verify-report.md
Phase 11: /content-create + /copywriting -> mkt/content/
Phase 12: /lp-optimization + /seo (parallel)
```

### Strategy Sprint
**Triggers:** "strategy", "what should we build", "prioritize"
```
Phase 1: /icp-research -> product-context.md
Phase 2: /market-research + /problem-analysis (parallel)
Phase 3: /solution-design -> solution-design.md
Phase 4: /funnel-planner -> targets.md
Phase 5: /experiment -> experiment-*.md
```

### Content Campaign
**Triggers:** "content campaign", "marketing campaign"
```
Phase 1: /icp-research -> product-context.md
Phase 2: /imc-plan -> mkt/imc-plan.md
Phase 3: /content-create -> mkt/content/
Phase 4: /copywriting -> mkt/content/*.copy.md
Phase 5: /humanize -> mkt/content/*.humanized.md
```

### Landing Page
**Triggers:** "landing page", "conversion page"
```
Phase 1: /icp-research -> product-context.md
Phase 2: /brand-system -> design/brand-system.md
Phase 3: /copywriting -> mkt/content/*.copy.md
Phase 4: /lp-optimization -> mkt/lp-optimization.md
Phase 5: /humanize -> mkt/content/*.humanized.md
```

### Architecture Decision
**Triggers:** "debate the tech stack", "which approach", "compare options"
```
Phase 1: /discover -> scope the decision (interactive)
Phase 2: /agent-room debate -> meta/agent-room-report.md
Phase 3: /system-architecture -> system-architecture.md
```

---

## Anti-Patterns

- **Dumping a flat list** — Trace the graph, find the root blocker. Don't list every missing artifact equally.
- **Ignoring artifact state** — Don't recommend `/icp-research` when `product-context.md` is 3 days old.
- **Skipping dependency tracing** — Don't recommend `/task-breakdown` when `system-architecture.md` doesn't exist.
- **Treating templates as rigid** — Skip phases where fresh artifacts exist.
- **Using navigate for skill routing** — The agent proposes skills proactively. Navigate is for artifact status and orchestration only.

## Chain Position

Meta skill — scans artifact state and recommends the highest-impact next skill to run. Start here when unsure what to do next.
