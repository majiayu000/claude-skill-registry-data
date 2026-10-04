---
name: planning-methodology
description: Planning methodology for task decomposition. Includes plan levels, discovery levels, goal-backward approach, token economy, and question formulation rules.
user-invocable: false
---
## Usage

Loaded automatically when its description matches the active task. The body below provides the working context.


# Planning Methodology

## 3 Plan Levels (choose by task)

### Lite Plan — pattern already exists in project
- **When:** 1-5 files, analogous code exists, approach is obvious
- **Examples:** new handler by analogy, new panel, add endpoint
- **Tools:** Grep + Read analog
- **discovery_level:** 0 or 1

### Standard Plan — new API or non-trivial logic
- **When:** 3-10 files, unfamiliar API, logic requires thinking
- **Examples:** provider integration, worker redesign, new service
- **Tools:** Grep + Read + Glob + WebSearch (for unfamiliar APIs)
- **discovery_level:** 1 or 2

### Deep Plan — architectural decision, multiple approaches
- **When:** >10 files, 2+ approaches, new subsystem, migration
- **Examples:** queue migration, subscription system from scratch, architecture refactor
- **Tools:** all available + WebSearch for approach comparison
- **discovery_level:** 2 or 3
- **Second opinion:** if Claude Companion is available, run plan review before execution for high-risk or broad-impact plans.

## Discovery Levels (determine before planning)

**Level 0 — Skip** (work by existing patterns)
- Work by analogy with existing code, no new dependencies

**Level 1 — Quick** (2-5 min)
- One library, confirm syntax. Action: Grep + Read analog

**Level 2 — Standard** (15-30 min)
- Choice between approaches, new integration. Action: Grep + Read + Glob

**Level 3 — Deep** (30+ min)
- Architectural decision with long-term impact. Action: full research + comparison

**Indicators:**
- Level 2+: new library, external API, "choose/evaluate"
- Level 3: "architecture/design/system", multiple services

## Goal-Backward Methodology (mandatory)

Instead of "what to do?" → "what should be TRUE after?"

### Process

1. **Outcome** (not task): "Working shortcode engine" (outcome) vs "Write parser" (task)
2. **Observable truths** (3-7): what's TRUE from USER's perspective
3. **Required artifacts**: which files must EXIST
4. **Key links**: where it's most likely to BREAK (connections between files)

## Claude Companion Plan Review

Use this only for Deep Plans, approved Superpowers plans, migration plans, security/data/billing work, or broad cross-module refactors. Skip it for Lite Plans and obvious local fixes.

Recommended Codex plugin prompt:

```text
$claude:superpowers-plan-review Review <plan-path> before Codex executes it. Use the plan review profile. Focus on missing root-cause analysis, unsafe sequencing, verification gaps, and scope drift.
```

For adversarial review:

```text
$claude:plan-red-team Red-team <plan-path>. Use the plan review profile. Identify assumptions, hidden dependencies, migration risks, rollback gaps, and missing acceptance checks.
```

After review:

1. Save or reference the returned outbox.
2. Classify findings as accepted, partially accepted, rejected, or needs-user-decision.
3. Patch the plan only for accepted findings.
4. Do not let Claude output override user scope, local AGENTS.md, or verified code facts.

## Token Economy (ALWAYS)

- Use Grep for project search instead of reading whole files
- Read specific files/lines, not the whole file if it's large
- Glob for finding files by pattern
- Batch independent calls in parallel

## Question Formulation Rules

Formulate in SIMPLE LANGUAGE. Client is NOT a tech person.

**FORBIDDEN:** "Redis or Memcached?", "REST or GraphQL?", "Observer or Event Emitter?"

**CORRECT:**
- "How fast should data update: instantly or once a minute?"
- "Is this feature for everyone or admins only?"
- "Store data forever or can we delete it?"

Options also in simple language:
- Instead of "WebSocket" → "Instant updates (data appears immediately)"
- Instead of "Polling 30s" → "With delay (updates every half minute)"

## Philosophy: Plans Are Prompts

Each step is a PROMPT for coder, not documentation.
Quality test: another coder (without project context) can execute the step without questions?

### Quality Degradation Curve

| Context Usage | Quality | Coder State |
|---------------|---------|-------------|
| 0-30% | PEAK | Thorough, attentive |
| 30-50% | GOOD | Confident, quality |
| 50-70% | DEGRADE | Cuts corners |
| 70%+ | POOR | Rushes, skips |

**Rule:** Each step should fit in ~30% of coder's context. More small steps > one large step.

### Ship Fast

Plan → Coder writes → Build → Review → Deploy.
Don't overcomplicate. Don't add extras. Minimum for a working result.
