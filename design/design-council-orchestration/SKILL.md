---
name: design-council-orchestration
description: Convene 11 role-specialized Claude agents to debate technical decisions in parallel, with the invoking Claude acting as CEO
triggers:
  - convene the design council
  - run a design debate
  - get the council together for this decision
  - council review of this architecture
  - spawn the design council
  - need a cross-functional design review
  - debate this with the full council
  - convene council to review
---

# Design Council Orchestration

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Design Council is a Claude Code plugin that spawns 11+ independent Claude agents in parallel, each with a specialized role (principal-engineer, security-engineer, product-manager, etc.), to debate cross-cutting technical decisions. The invoking Claude acts as CEO, orchestrating the debate and writing binding decisions.

Unlike single-context reviews, each seat runs in its own context with no shared history. Disagreement is structural, not simulated. Seats argue via direct peer DMs (`SendMessage`), not sequential turns through the CEO.

**Key difference from other patterns**: This isn't prompt engineering within one context — it's multi-agent orchestration with genuine parallelism and independent reasoning.

## Installation

```bash
# Add the plugin marketplace
/plugin marketplace add sjsyrek/claude-plugins

# Install design-council
/plugin install design-council@sjsyrek
```

To pin a specific version:

```bash
git clone https://github.com/sjsyrek/design-council.git
cd design-council
git checkout v0.2.0
/plugin marketplace add .
/plugin install design-council@sjsyrek
```

## When to Use

**Invoke when BOTH conditions hold:**

1. Decision crosses **≥2 specialist domains** (e.g., security + performance + UX)
2. Output must **survive handoff** (decision log, tracker items, execution plan)

**Natural trigger phrases:**
- "Convene the council to review this API design"
- "Get the design council together for this architecture"
- "Council debate: pagination strategy for this endpoint"
- "Run a design review on the caching layer"

**Do NOT invoke for:**
- Simple bug fixes (single domain)
- Library/tool selection (→ use direct research)
- Pure exploration without deliverable
- Questions answerable by one specialist

**Token economics**: Expect 10–20× the cost of single-context review. The council earns its cost on decisions that would otherwise ship with blind spots.

## Execution Phases

### Phase 0: Plan Card (Pre-Flight)

Before any agents spawn, the CEO shows a confirmation card:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DESIGN COUNCIL PLAN

Mode: DEBATE
Roster (8 seats):
  • principal-engineer     [opus]
  • platform-engineer      [sonnet]
  • security-engineer      [sonnet]
  • test-engineer          [sonnet]
  • performance-engineer   [sonnet]
  • product-manager        [opus]
  • technical-writer       [opus]
  • qa-engineer            [sonnet]

Budget:
  ~180k tokens (cached brief saves ~9k × 8)
  ~4–7 min wall-clock (3 debate rounds)

Opening prompt:
  "Should the /search endpoint paginate with
   cursor tokens or offset/limit?"

Reply: go | swap X for Y | drop X | add X | abort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**You control the roster here:**

```bash
# Accept as-is
go

# Swap models
swap principal-engineer for sonnet

# Add a seat
add domain-expert

# Remove a seat
drop ui-ux-designer

# Cancel
abort
```

### Phase 1: Brief Assembly

The CEO gathers constraints **once** into `~/.claude/councils/<slug>/brief.md`:

- `CLAUDE.md` constraints
- Referenced specs / ADRs
- Project memory (including beads if detected)
- **Skill self-audit**: greps auto-memory for entries about design-council itself — memory wins over skill text (real failures > documentation)

Every seat's spawn prompt points to this path → **prompt cache hits across all spawns** (~7–12k tokens saved per 8-seat council).

### Phase 2: Parallel Spawn

CEO spawns all seats in **one multi-tool-call message**:

```typescript
// Conceptual — the CEO does this automatically
await Promise.all([
  Agent({
    name: "principal-engineer",
    run_in_background: true,
    team_name: "design-council-2026-05-17-pagination",
    model: "claude-opus-4",
    prompt: `You are the principal-engineer seat.
    
Brief: file://~/.claude/councils/pagination/brief.md

Four delivery rules:
1. Handshake: DM "READY: principal-engineer" within 10s
2. Cross-talk: SendMessage only (never Execute)
3. Final verdict: via SendMessage to CEO
4. Idle summary: <100 chars

Opening question:
Should /search paginate cursor or offset?`
  }),
  Agent({ name: "security-engineer", ... }),
  Agent({ name: "platform-engineer", ... }),
  // ... 5 more
]);
```

### Phase 2.5: Handshake Verify

CEO counts incoming `READY: <seat-name>` DMs, checks for empty `tmuxPaneId`s (silent spawn failures), remediates, and emits:

```
HANDSHAKE: 8/8 ok | verdict=PROCEED
```

If any seat fails to spawn:
- CEO attempts one re-spawn
- On second failure: drops seat, logs it, proceeds with reduced roster

### Phase 3: Opening Verdicts

Each seat posts its opening verdict via `SendMessage` to CEO:

```
From: security-engineer
To: CEO

CONCERNS

Offset pagination leaks record counts (DoS vector).
Cursor tokens must be HMAC-signed with rotation.
Need rate-limit strategy regardless of choice.
```

Verdicts:
- `APPROVE` — no blocking concerns
- `CONCERNS` — issues that need resolution
- `BLOCK` — showstopper (requires CEO arbitration or escalation)

### Phase 4: Cross-Talk (Peer DMs)

**Review mode**: skips cross-talk by default (seats → CEO only).

**Debate mode**: CEO routes disagreements to direct seat-to-seat DMs:

```typescript
// CEO orchestration (automatic)
if (security.verdict === "CONCERNS" && platform.verdict === "APPROVE") {
  SendMessage({
    from: "CEO",
    to: "security-engineer",
    text: "DM platform-engineer: they approved offset. Argue your HMAC requirement."
  });
  
  SendMessage({
    from: "CEO", 
    to: "platform-engineer",
    text: "security-engineer has concerns about offset. Respond to their HMAC point."
  });
}
```

Seats then argue directly:

```
From: security-engineer
To: platform-engineer

Your offset approval ignores enumeration risk.
Without signed cursors, scrapers can walk the
entire dataset. Do you have a mitigation?
```

```
From: platform-engineer  
To: security-engineer

Rate limiting is orthogonal to pagination style.
Offset + jittered delays caps enumeration to
same ROC as cursor. Offset is simpler to cache.
```

**Hard cap: 3 rounds.** CEO forces convergence or arbitration.

### Phase 5: Arbitration + Decision Log

For unresolved disagreements, CEO writes **binding decisions** (3–5 sentences engaging both sides):

```markdown
## Decision: Cursor pagination with signed tokens

security-engineer's enumeration concern is valid
and not fully mitigated by rate limiting (jitter
still allows sequential walks). platform-engineer's
caching argument applies to both schemes via
`cache_token` param. **Adopt cursor pagination
with HMAC-SHA256 signed tokens (rotate key daily).**

Deferred: Rate limit strategy (filed as BEAD-127).
```

**Escalations** (to user):
- Strategic tradeoffs (e.g., "ship fast vs. correct")
- Budget / resourcing
- Legal / compliance
- Cross-team dependencies

CEO emits draft log to chat:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DECISION LOG (DRAFT)

Reply: save | amend "<changes>" | discard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 6: Persist + Teardown

On `save`:

```bash
# Decision log
~/.claude/councils/2026-05-17-pagination/log.md

# Structure
---
slug: pagination
date: 2026-05-17
mode: DEBATE
roster: [principal-engineer, security-engineer, ...]
primary-tracker-id: BEAD-126  # if beads detected
linked-tracker-ids: [BEAD-127]
status: resolved
---

# Opening Prompt
Should /search paginate cursor or offset?

# Resolved Disagreements
...

# Arbitration Decisions
...

# Execution Plan
File ownership:
- src/api/search.ts → platform-engineer context
- src/auth/tokens.ts → security-engineer context
- tests/api/search.test.ts → test-engineer context
```

CEO then:
- Broadcasts shutdown via `SendMessage`
- Calls `TeamDelete` (removes shared task list)
- Cleans up Brief artifact

## Roster Configuration

### Default 11 Seats (Dynamic Sizing)

```yaml
core:
  - principal-engineer    # Architecture synthesis (opus)
  - platform-engineer     # Infra / deployment (sonnet)
  - integration-engineer  # API contracts / compat (sonnet)
  - test-engineer         # Test strategy (sonnet)
  - qa-engineer           # Quality gates (sonnet)
  - security-engineer     # Threat model (sonnet)
  - performance-engineer  # Latency / throughput (sonnet)
  - product-manager       # User impact / scope (opus)
  - ui-ux-designer        # Interface / flows (sonnet)
  - accessibility-specialist  # A11y / WCAG (sonnet)
  - technical-writer      # Docs / clarity (opus)

opt-ins:
  - devops-engineer       # CI/CD / observability
  - finops-engineer       # Cloud cost / budget
  - legal-compliance      # GDPR / SOC2 / licensing
  - domain-expert         # Named SME (you provide context)
  - historian             # Past decisions / ADRs
```

**Automatic pruning** (Phase 0):
- No UI → drop `ui-ux-designer`, `accessibility-specialist`
- Internal tool → drop `security-engineer`, `platform-engineer`
- Pure backend → drop `ui-ux-designer`

**Adding seats in plan card**:

```bash
# Add domain expert
add domain-expert

# CEO will prompt you for context:
# "What domain? Provide 2–3 sentence brief."
```

### Model Assignment

**Default strategy**:
- **Opus**: synthesis-heavy (`principal-engineer`, `product-manager`, `technical-writer`, `historian`)
- **Sonnet**: analytical (`test-engineer`, `performance-engineer`, `security-engineer`)

**Override triggers**:
- "High quality bar" → all Opus
- "Ship to production" → all Opus
- Plan card manual swap: `swap security-engineer for opus`

## Beads Integration (Tracker System)

When [beads](https://github.com/gastownhall/beads) is detected (`.beads/` exists OR `bd` on `$PATH`):

**Phase 1 (Brief)**:
```bash
# CEO runs automatically
bd memories       # → brief.md
bd ready          # → brief.md (active context)
bd show <id>      # → brief.md (if user referenced a bead)
```

**Phase 4 (Defer)**:
```bash
# CEO translates DEFER decisions to tracker items
bd create \
  --title "Implement rate limiting for /search" \
  --type task \
  --parent BEAD-126 \
  --context "From design-council-2026-05-17-pagination: security-engineer raised enumeration concern"
```

**Phase 6 (Teardown)**:
```bash
# Close primary bead under debate
bd close BEAD-126 --force  # if dependency inversion flagged

# Log tracker IDs in frontmatter
primary-tracker-id: BEAD-126
linked-tracker-ids: [BEAD-127, BEAD-128]
```

**Without beads**: deferred items remain prose in decision log. Protocol is strictly additive.

## Advanced Patterns

### Stop Early

```bash
# At any phase
stop the council
```

CEO broadcasts shutdown, saves partial log with `status: halted`, cleans up.

### Review Mode (No Cross-Talk)

```bash
# User invocation
"Council review of PR #47 (no debate)"
```

CEO skips Phase 4 cross-talk. Seats → CEO verdict only. Faster, cheaper, good for conformance checks.

### Implementation Handoff

After decision log saves, spawn **execution agents** with `isolation: "worktree"`:

```typescript
// CEO provides this in execution plan
await Agent({
  name: "implement-cursor-pagination",
  isolation: "worktree",
  model: "claude-sonnet-4",
  prompt: `Implement cursor pagination per design-council-2026-05-17-pagination.

Decision log: file://~/.claude/councils/2026-05-17-pagination/log.md

File ownership (avoid conflicts):
- src/api/search.ts (yours)
- tests/api/search.test.ts (yours)

DO NOT TOUCH:
- src/auth/tokens.ts (security-engineer's impl)

Brief: file://~/.claude/councils/pagination/brief.md`
});
```

Worktree isolation prevents merge conflicts. See `references/implementation-handoff.md` in the plugin source for full playbook.

### Memory Self-Audit Pattern

**Why it matters**: If you've used design-council before and hit a failure (e.g., "security seat always blocks on offset pagination"), that failure lands in auto-memory. Phase 1 greps for `design-council` memories and **overrides skill text** with ground truth.

Example:

```markdown
# In auto-memory
2026-05-10: design-council: security-engineer seat
over-indexes on HMAC signatures. For internal APIs,
skip security seat unless user data is involved.
```

Phase 1 brief will now include:

```
MEMORY OVERRIDE (from 2026-05-10):
  Skip security-engineer for internal APIs unless
  user data involved. Prior councils over-rotated
  on HMAC signatures.
```

This is automatic. Memory always wins.

## Observability (Split-Pane Mode)

**Tmux / iTerm2**: Each seat renders in its own pane. Watch debates live.

```json
// settings.json (Claude Code)
{
  "teammateMode": "auto"  // or "tmux" to force
}
```

**Without split-pane terminal**: Seats share main pane. Cycle with Shift+Down.

This is a Claude Code harness feature, not plugin-required.

## Common Issues

### Silent Spawn Failures

**Symptom**: Phase 2.5 reports `HANDSHAKE: 6/8 ok | verdict=DEGRADED`

**Cause**: `TeamCreate` + `Agent` race on shared task list initialization.

**Remediation** (automatic):
1. CEO retries failed seats once
2. On second failure: drops seat, logs it, proceeds

**User action**: Check `~/.claude/councils/<slug>/log.md` for `degraded-roster: [security-engineer]`. If critical seat dropped, re-run with `add security-engineer`.

### Token Budget Overrun

**Symptom**: Debate stalls mid-round, costs spike.

**Cause**: Deep research by one seat (e.g., `performance-engineer` running benchmarks).

**Fix**:
1. Say "stop the council"
2. Review partial log
3. Re-run in **review mode** (skips cross-talk)

**Prevention**: Use review mode for conformance checks, debate mode for novel decisions.

### Deferred Items Lost

**Symptom**: Phase 5 decision says "DEFER: <item>" but no tracker created.

**Cause**: No tracker system detected (no beads, no `bd` on `$PATH`).

**Fix**: Manually file from decision log prose:

```bash
# From log.md
# Deferred: Implement rate limiting

bd create \
  --title "Implement rate limiting for /search" \
  --context "From design-council-2026-05-17-pagination"
```

**Prevention**: Install beads or integrate another tracker (see `references/tracker-integration.md`).

### Prompt Cache Misses

**Symptom**: Token costs higher than predicted.

**Cause**: Brief modified between spawns (5-minute cache window).

**Fix**: Don't edit `~/.claude/councils/<slug>/brief.md` during Phase 2 spawn.

## Performance Characteristics

| Metric | Review Mode | Debate Mode (3 rounds) |
|--------|-------------|------------------------|
| Wall-clock | 2–3 min | 4–7 min |
| Tokens | 60–90k | 150–250k |
| Seats (typical) | 4–6 | 6–11 |
| Cache savings | ~5k × seats | ~9k × seats |

**Parallelism**: Wall-clock ≈ slowest seat, not sum of seats.

## Configuration Files

### Brief Artifact

```bash
~/.claude/councils/<slug>/brief.md

# Contents
- CLAUDE.md constraints
- Referenced specs
- Memory overrides
- Beads context (if detected)
```

**Lifecycle**: Created Phase 1, read by all seats, deleted Phase 6 teardown.

### Decision Log

```bash
~/.claude/councils/<yyyy-mm-dd>-<slug>/log.md

# Frontmatter
---
slug: pagination
date: 2026-05-17
mode: DEBATE
roster: [principal-engineer, ...]
primary-tracker-id: BEAD-126
status: resolved
---
```

**Lifecycle**: Persists after teardown. User artifact space.

## Code Examples

### Invoking from Code

```typescript
// In a TypeScript project
// User says: "convene council to review this cache layer"

// CEO automatically:
// 1. Reads current file context
// 2. Assembles brief from CLAUDE.md + memory
// 3. Shows plan card
// 4. On "go": spawns roster
```

### Custom Seat Brief (domain-expert)

```bash
# User: add domain-expert
# CEO: "What domain? Provide brief."

# User:
PostgreSQL query optimization. We're deciding
between materialized views vs. incremental
aggregates. Expert should eval EXPLAIN plans.
```

CEO injects this into domain-expert spawn prompt:

```
You are domain-expert (PostgreSQL query optimization).

Context: Eval materialized views vs. incremental
aggregates. Review EXPLAIN plans in brief.

Brief: file://~/.claude/councils/cache-layer/brief.md
```

### Execution Plan Format

```markdown
# Execution Plan

## Phase 1: Cursor Token Implementation
Owner: platform-engineer context
Files:
  - src/api/search.ts
  - src/types/pagination.ts

## Phase 2: HMAC Signing
Owner: security-engineer context  
Files:
  - src/auth/tokens.ts
  - src/auth/rotation.ts

## Phase 3: Integration Tests
Owner: test-engineer context
Files:
  - tests/api/search.test.ts
  - tests/auth/tokens.test.ts

## Merge Strategy
Worktree per phase. Merge order: 1 → 2 → 3.
Conflict expected: src/api/search.ts (line 47, imports).
Resolution: Accept Phase 2 (security adds token import).
```

## Environment Variables

No secrets required. All state in `~/.claude/councils/` (user artifact space).

If integrating a custom tracker (not beads):

```bash
export COUNCIL_TRACKER_CMD="jira"  # Default: bd
export COUNCIL_TRACKER_CREATE_ARGS="create --project DESIGN"
```

See `references/tracker-integration.md` for adapter contract.

## Version Compatibility

- **Claude Code**: v0.9.0+ (requires `TeamCreate`, `Agent.run_in_background`)
- **Beads**: v0.3.0+ (optional, for tracker integration)
- **Tmux**: 3.0+ (optional, for split-pane observability)

## Further Reading

- **Implementation handoff playbook**: `references/implementation-handoff.md` in plugin source
- **Tracker integration**: `references/tracker-integration.md`
- **Changelog**: `CHANGELOG.md`

---

**License**: MIT  
**Source**: https://github.com/sjsyrek/design-council
