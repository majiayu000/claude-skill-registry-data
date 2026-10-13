---
name: balance-check
description: "Analyzes balance constraints. Game: balance data, formulas, progression, degenerate strategies, and economy imbalances. Product: quotas, rate limits, pricing tiers, permissions, workflow friction, retry/backoff settings, and operational budgets."
argument-hint: "[system-name|path-to-data-file]"
user-invocable: true
allowed-tools: Read, Glob, Grep
agent: economy-designer
---

## User Guide

- When to use: Analyzes balance constraints. Game: balance data, formulas, progression, degenerate strategies, and economy imbalances. Product: quotas, rate limits, pricing tiers, permissions, workflow friction, retry/backoff settings, and operational budgets.
- Inputs: Command arguments: `/balance-check [system-name|path-to-data-file]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before checking balance:
- `design/cdd/game-concept.md` -> **[Game]** keep the existing game balance workflow: formulas, economy, damage, progression, resource curves, difficulty, and player power gates.
- `design/cdd/product-concept.md` -> **[Product]** run a product balance check: quotas, rate limits, pricing tiers, permissions, workflow friction, retry/backoff settings, queue limits, default configuration, and operational budgets.
- If unclear, ask whether the target is game balance or product rule/resource balance.

Game balance examples remain authoritative for game projects. Product checks must be added beside them, not substituted for them.
## Phase 1: Identify Balance Domain

Determine the balance domain from `$ARGUMENTS[0]`:

- **Combat** → weapon/ability DPS, time-to-kill, damage type interactions
- **Economy** → resource faucets/sinks, acquisition rates, item pricing
- **Progression** → XP/power curves, dead zones, power spikes
- **Loot** → rarity distribution, pity timers, inventory pressure
- **File path given** → load that file directly and infer domain from content

**[Product] Product balance domains:**
- **Quotas / Rate limits** -> request budgets, burst limits, retry/backoff, queue depth, concurrency caps
- **Pricing / Plan tiers** -> included usage, overage rules, feature gating, account limits, free-trial limits
- **Permissions / Roles** -> role capability spread, privilege escalation risk, default access, approval friction
- **Workflow friction** -> number of steps, decision points, error recovery, manual handoffs, repeated data entry
- **Operational budgets** -> p95 latency, memory, cold start, storage, throughput, background job duration
- **File path given** -> load that file directly and infer whether it defines product constraints, config defaults, pricing, permissions, or workflow limits

If no argument, ask the user which system to check.

---

## Phase 2: Read Data Files

Read relevant files from `assets/data/` and `design/balance/` for the identified domain.
Note every file read — they will appear in the Data Sources section of the report.

**[Product] Read product constraint sources:**
- Config and defaults: `config/**/*`, `.env.example`, `*.example`, `*.sample`
- API/CLI contracts: `docs/api/**/*`, `docs/cli/**/*`, OpenAPI files, command help docs, SDK examples
- Product design docs: `design/cdd/*.md`, `design/ux/*.md`, `design/cdd/product-concept.md`, `design/cdd/module-index.md`
- Architecture and operational docs: `docs/architecture/*.md`, `docs/reference/<stack>/VERSION.md`, deployment notes, runbooks
- Production evidence: `production/qa/**/*`, `production/releases/**/*`, support/incident notes if present

---

## Phase 3: Read Design Document

Read the CDD for the system from `design/cdd/` to understand intended design targets,
tuning knobs, and expected value ranges. This is the baseline for "correct" behaviour.

**[Product] Product baseline:**
Read the CDD for the module or workflow from `design/cdd/` and extract:
- User Promise or JTBD target
- API/CLI/UI contract and primary workflow
- Data model, permissions, configuration, and integration constraints
- Acceptance criteria and operational budgets
- Any explicit plan tier, quota, retry, latency, storage, or migration values

---

## Phase 4: Perform Analysis

Run domain-specific checks:

**Combat balance:**
- Calculate DPS for all weapons/abilities at each power tier
- Check time-to-kill at each tier
- Identify any options that dominate all others (strictly better)
- Check if defensive options can create unkillable states
- Verify damage type/resistance interactions are balanced

**Economy balance:**
- Map all resource faucets and sinks with flow rates
- Project resource accumulation over time
- Check for infinite resource loops
- Verify gold sinks scale with gold generation
- Check if any items are never worth purchasing

**Progression balance:**
- Plot the XP curve and power curve
- Check for dead zones (no meaningful progression for too long)
- Check for power spikes (sudden jumps in capability)
- Verify content gates align with expected player power
- Check if skip/grind strategies break intended pacing

**Loot balance:**
- Calculate expected time to acquire each rarity tier
- Check pity timer math
- Verify no loot is strictly useless at any stage
- Check inventory pressure vs acquisition rate

**Product quota/rate-limit balance:**
- Compare default limits against expected user journey and API/CLI usage.
- Check for plan tiers where an upgrade path is impossible, exploitative, or operationally unsafe.
- Verify retry/backoff values avoid thundering herd behavior and do not make normal users wait longer than the product promise allows.
- Identify one setting that dominates all others, such as a global cap that makes per-endpoint limits meaningless.

**Product permission balance:**
- Map roles to capabilities and flag roles that are too broad or too narrow.
- Check default permissions for least privilege and reasonable first-use flow.
- Verify approval gates do not block the core workflow unnecessarily.
- Flag privilege escalation paths and dead-end states.

**Product workflow-friction balance:**
- Count steps, handoffs, repeated fields, confirmations, and error-recovery loops in the primary workflow.
- Check whether friction is intentional protection or accidental drag.
- Compare workflow effort against the Product Concept user promise and JTBD.
- Flag any required step with no user-visible value, no risk reduction, and no compliance need.

**Product operational-budget balance:**
- Compare p95 latency, cold start, memory, storage, and job-duration budgets against architecture docs and production evidence.
- Flag budgets inherited from defaults with no evidence.
- Identify overly loose budgets that hide reliability failures and overly tight budgets that would create unnecessary engineering cost.

---

## Phase 5: Output the Analysis

For game projects, use the existing format below.

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [HEALTHY / CONCERNS / CRITICAL ISSUES]

### Outliers Detected
| Item/Value | Expected Range | Actual | Issue |
|-----------|---------------|--------|-------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```

For product projects, use this equivalent format:

```markdown
## Product Balance Check: [Module / Workflow / Constraint]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [HEALTHY / CONCERNS / CRITICAL ISSUES]

### Constraint Outliers
| Constraint | Intended Range / Promise | Actual | Issue |
|------------|--------------------------|--------|-------|

### Workflow Friction
| Step / Limit | User Value | Risk Reduced | Friction Cost | Verdict |
|--------------|------------|--------------|---------------|---------|

### Operational Budget Analysis
| Budget | Target | Evidence | Issue |
|--------|--------|----------|-------|

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|---------------|--------|

### Values That Need Attention
[Specific quotas, limits, defaults, roles, retries, or budgets with rationale]
```

---

## Phase 6: Fix & Verify Cycle

After presenting the report, ask:

> "Would you like to fix any of these balance issues now?"

If yes:
- Ask which issue to address first (refer to the Recommendations table by priority row)
- Guide the user to update the relevant data file in `assets/data/` or formula in `design/balance/`
- After each fix, offer to re-run the relevant balance checks to verify no new outliers were introduced
- If the fix changes a tuning knob defined in a CDD or referenced by an ADR, remind the user:
  > "This value is defined in a design document. Run `/propagate-design-change [path]` on the affected CDD to find downstream impacts before committing."

If no:
- Summarize open issues and suggest saving the report to `design/balance/balance-check-[system]-[date].md` for later

End with:
> "Re-run `/balance-check` after fixes to verify."

**[Product] Product fix cycle:**
- If the fix changes an API/CLI contract, run `/propagate-design-change` on the affected CDD and update docs/examples before implementation.
- If the fix changes a quota, plan tier, retry value, permission, or default configuration, update the relevant CDD/ADR and add regression or contract evidence in `production/qa/`.
- If the fix changes an operational budget, re-run `/perf-profile` or the relevant CI/load evidence collection before marking the Product balance issue resolved.
