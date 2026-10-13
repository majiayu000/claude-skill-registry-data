---
name: story-slicing
description: Slice epics and oversized stories into independently deliverable vertical slices. Analyzes the codebase to ground sizing in real complexity. Applies Richard Lawrence's 9 splitting patterns and INVEST criteria. Includes agent-native equivalents of Jira Intelligence features — work breakdown, story enhancement, comment summarization, edge case generation, dependency detection, NL-to-JQL, and story point estimation — no Jira Premium required.
triggers:
  - "slice this story"
  - "split this epic"
  - "story is too big"
  - "how do I break this down"
  - "story slicing"
  - "vertical slice"
  - "story splitting"
  - "this won't fit in a sprint"
  - "break down this feature"
  - "story too large"
  - "independent stories"
  - "story points too high"
  - "improve this ticket"
  - "summarize this ticket"
  - "what are the edge cases"
  - "find dependencies in these stories"
  - "estimate this story"
  - "turn this into JQL"
audience: manager, engineer, qa
---

# Story Slicing

## Context

Large stories and epics are the #1 cause of missed sprint commitments, deferred feedback, and integration risk. The fix is not to "try harder" — it's to slice differently. Most teams slice horizontally by technical layer (UI story, API story, DB story) — a glorified waterfall that produces nothing shippable until all layers are done. Vertical slicing cuts end-to-end through all layers, delivering a thin but complete and usable increment after every sprint.

This skill combines:
- **Richard Lawrence's 9 story splitting patterns** — the most widely used framework in agile coaching
- **INVEST criteria** — the acceptance test for every slice
- **Codebase analysis** — grounds sizing in real complexity, not guesses
- **Jira MCP** — creates child stories directly from the analysis

---

## Vertical vs Horizontal Slicing

| | Horizontal (❌ avoid) | Vertical (✅ target) |
|---|---|---|
| **How it slices** | By technical layer or skill | End-to-end through all layers |
| **Example** | "Design story", "Backend story", "QA story" | "User can log in with email/password (happy path)" |
| **Demo-able at sprint end?** | No — each slice is incomplete alone | Yes — working feature, even if limited |
| **User feedback possible?** | No | Yes |
| **INVEST-compliant?** | No (not Valuable, not Independent) | Yes |
| **Risk** | Integration crunch at end | Caught early |

> **The sandwich analogy (nextagile.ai):** Horizontal = separating the bun, lettuce, patty, tomato into layers. Vertical = cutting the whole sandwich into smaller sandwiches — each one complete and edible.

---

## Step 1 — Codebase Analysis (Agent-Driven)

Before slicing on paper, analyze the codebase to understand the *real* cost of each slice.

### What to scan

**Service/module boundaries:**
```bash
# Understand the architecture
find . -name "*.service.*" -o -name "*.controller.*" -o -name "*.handler.*" | head -30
find . -name "routes.*" -o -name "router.*" | head -20
ls src/ services/ modules/ packages/ apps/ 2>/dev/null
```

**API surface (how many endpoints does this feature touch?):**
```bash
grep -rn "@Get\|@Post\|@Put\|@Delete\|@Patch\|router\.\(get\|post\|put\|delete\)" src/ --include="*.ts" --include="*.js" | grep -i "<feature_keyword>"
```

**Schema / migration impact:**
```bash
ls db/migrations/ migrations/ prisma/migrations/ 2>/dev/null | tail -10
grep -rn "ALTER TABLE\|CREATE TABLE\|addColumn\|createTable" migrations/ db/ 2>/dev/null
```

**Test coverage surface:**
```bash
find . -name "*.test.*" -o -name "*.spec.*" | xargs grep -l "<feature_keyword>" 2>/dev/null
```

**Cross-cutting concerns (auth, logging, feature flags):**
```bash
grep -rn "featureFlag\|isEnabled\|authorize\|@Guard\|middleware" src/ --include="*.ts" | grep -i "<feature_keyword>"
```

### Complexity signals

Use the scan to estimate the slice's real cost:

| Signal | Low complexity | High complexity |
|--------|---------------|-----------------|
| Services touched | 1 | 3+ |
| New API endpoints | 0–1 | 3+ |
| Schema changes | None | New table / multi-column |
| Auth/permission changes | None | New role or scope |
| New test files needed | 1–2 | 5+ |
| Cross-service calls | None | Sync or async integration |
| Feature flag needed | No | Yes (phased rollout) |

> **Key insight:** A story that touches 3 services, adds 4 endpoints, and requires a schema migration is almost certainly 2–3 sprints of work. Slice it before estimation, not during.

---

## Step 2 — INVEST Check on the Input Story

Before splitting, evaluate whether the input story/epic fails INVEST — this tells you *what kind* of split is needed.

| INVEST | Check | Failure → Split by |
|--------|-------|--------------------|
| **Independent** | Can this be built without waiting for another story? | Workflow steps or spike first |
| **Negotiable** | Are details still open? | That's fine — don't over-specify |
| **Valuable** | Does this deliver user-perceivable value alone? | Role or happy-path split |
| **Estimable** | Can the team give a rough size? | Spike story needed first |
| **Small** | Fits in ≤ half a sprint? | Apply splitting patterns below |
| **Testable** | Do we know what "done" looks like? | Acceptance criteria split |

---

## Step 3 — Richard Lawrence's 9 Splitting Patterns

Apply these in order. Use the first pattern that produces independently valuable stories.

### Pattern 1 — Workflow Steps
Split by the sequential steps a user takes through a workflow.

```
Original: "As a user, I can manage my account"
→ S1: User can update their profile photo
→ S2: User can update personal information
→ S3: User can change their password
→ S4: User can delete their account
```
✅ **Best for:** Large features with a clear user journey. Each step is usable independently.

---

### Pattern 2 — Happy Path / Alternate Paths
Implement the happy path first, then error cases and edge cases as follow-on stories.

```
Original: "User can log in with email and password"
→ S1: User can log in with valid credentials (happy path)
→ S2: System shows error for invalid credentials
→ S3: System validates email format
→ S4: System validates password complexity
→ S5: System supports 500 concurrent logins within 3s (performance story)
```
✅ **Best for:** Any story with multiple acceptance criteria — especially validation, error handling, and performance. Most reliable pattern.

---

### Pattern 3 — CRUD Operations
Split by Create, Read, Update, Delete — each is independently valuable.

```
Original: "User can manage products in the catalogue"
→ S1: User can view the product catalogue (Read)
→ S2: User can add a new product (Create)
→ S3: User can edit a product's details (Update)
→ S4: User can archive a product (Delete/soft-delete)
```
✅ **Best for:** Admin panels, dashboards, data management features.

---

### Pattern 4 — Data Types / Complexity
Build for the simplest data case first, then add complex variants.

```
Original: "User can send messages to other users"
→ S1: User can send a plain text message
→ S2: User can send a message with an image attachment
→ S3: User can send a message with a file attachment
→ S4: User can send a message with inline code formatting
```
✅ **Best for:** File uploads, rich content editors, multi-format APIs.

---

### Pattern 5 — Business Rules
Each distinct business rule becomes a story.

```
Original: "Apply discount at checkout"
→ S1: 10% discount applied for loyalty members
→ S2: Promo code discount applied at checkout
→ S3: Bulk discount applied for orders over $500
→ S4: Stacked discounts follow precedence rules
```
✅ **Best for:** Pricing engines, approval workflows, compliance rules.

---

### Pattern 6 — Roles / User Types
Implement for the primary user role first, then extend to other roles.

```
Original: "Users can view the analytics dashboard"
→ S1: Viewer role can see their own team's analytics
→ S2: Manager role can see all teams' analytics
→ S3: Admin role can export analytics to CSV
```
✅ **Best for:** RBAC features, multi-tenant products, permission systems.

---

### Pattern 7 — Platform / Interface Variations
Ship on one surface first, then extend.

```
Original: "Users can complete checkout"
→ S1: Checkout works on web (desktop)
→ S2: Checkout is responsive on mobile web
→ S3: Checkout available as native mobile app flow
```
✅ **Best for:** Multi-platform products. Don't wait for all platforms before shipping any.

---

### Pattern 8 — Defer Performance / Quality Constraints
Implement correctness first; meet performance/SLA targets as a follow-on story.

```
Original: "Search returns results in < 200ms"
→ S1: Search returns correct results (no SLA)
→ S2: Search results return in < 200ms under load (performance spike + optimization)
```
✅ **Best for:** Any story mixing functional and non-functional requirements. NFRs should be explicit stories, not hidden acceptance criteria.

---

### Pattern 9 — Spike (Investigation Story)
When the team can't estimate because of unknowns, create a time-boxed spike first.

```
Original: "Integrate with Stripe for payments" (team has never used Stripe)
→ Spike: Investigate Stripe integration — auth flow, webhook setup, test mode — 2-day timebox
  → Outcome: ADR + estimated stories for the real implementation
→ S1–SN: (defined after spike)
```
✅ **Best for:** New technology, third-party integrations, uncertain architecture. **Spikes are not features** — cap them at 2 days, and always produce a written output.

---

## Step 4 — Evaluate Each Slice

Run every proposed slice through this checklist before accepting it:

```
□ Independent — can be built and released without another story being done first
□ Valuable — a real user or stakeholder benefits; it's not "just the backend"
□ Demo-able at sprint end — can be shown working in a sprint review
□ Testable — acceptance criteria are written (Given/When/Then)
□ Sized ≤ half a sprint — a team of 2 could finish it in 2–3 days
□ No horizontal layer split — not "Frontend only" or "API only"
□ Happy path is separate from error paths (if large enough to warrant it)
□ Performance / NFR constraints are a separate story (if non-trivial)
```

**Red flags — reslice if any are true:**
- "We can't demo this until the other story is done" → dependency, recombine or reorder
- "This is just the API, the UI is next sprint" → horizontal slice
- "This covers all the edge cases" → split off error paths and edge cases
- "This is the whole feature" → almost certainly too big

---

## Story Output Template

For each slice, produce:

```
## Story: <title>

**As a** <role>
**I want** <action>
**So that** <value>

**Why this slice:** <which splitting pattern was applied and why>

**Codebase impact (from analysis):**
- Services touched: <list>
- New endpoints: <list or none>
- Schema changes: <list or none>
- Cross-cutting: <auth changes, feature flags, etc.>
- Estimated test files: <N>

**Acceptance Criteria:**
- [ ] Given <context>, When <action>, Then <outcome>
- [ ] Given <context>, When <action>, Then <outcome>

**Definition of Done check:**
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Acceptance criteria verified
- [ ] No regressions in <related area>
- [ ] Documentation updated (if user-facing)

**Size estimate:** <XS / S / M — if M, consider splitting further>
**Dependencies:** <none / blocked by Story X>
**INVEST score:** I✅ N✅ V✅ E✅ S✅ T✅
```


## Jira Intelligence Commands

This skill pairs with **`jira-intelligence`** — a standalone skill with 7 agent-native commands that replicate Jira Premium AI features without a license:

| Command | Trigger |
|---------|---------|
| Work Breakdown | *"Break this epic into stories"* |
| Story Enhancement | *"Improve this ticket / rewrite this story"* |
| Comment Summary | *"Summarize this ticket / TLDR this thread"* |
| Edge Case Generator | *"What are the edge cases for this story?"* |
| Dependency Detector | *"Find dependencies / which stories are blocking each other?"* |
| Story Point Estimator | *"Estimate this story"* |
| NL → JQL | *"Turn this into JQL"* |

> Invoke `jira-intelligence` directly for any of the above. When slicing a full epic, this skill chains into `jira-intelligence` automatically for work breakdown and point estimation.

## Anti-Patterns Reference

| Anti-pattern | Problem | Fix |
|---|---|---|
| Layer split (UI / API / DB as separate stories) | Nothing ships until all layers done | Use workflow or happy-path split instead |
| "Include all edge cases" | Story is actually 3 stories | Happy path first, edge cases follow |
| Technical task as story | "Create the DB schema" delivers no user value | Embed in a real story or use a spike |
| Mega spike | "Research the whole feature" — no clear output | Cap at 2 days, define the written output |
| Split by team member | "Alice does frontend, Bob does backend" | Pair or mob; don't slice by person |
| Premature performance NFR | "Returns in < 200ms" baked into functional story | Defer performance as a follow-on story |

---

## Agent Instructions

When applying this skill, the agent should:

1. Ask for the epic/story text, or fetch it from Jira via MCP
2. **Scan the codebase** using the patterns in Step 1 to assess real complexity
3. Run the INVEST check on the input to identify what type of split is needed
4. Apply the first applicable splitting pattern(s) from the 9 patterns
5. Evaluate each proposed slice against the Step 4 checklist
6. Output all slices using the Story Output Template, including codebase impact per slice
7. Flag any slices that still seem too large and suggest the next split
8. If MCP is available, create the child stories in Jira under the parent epic

---

## References

- Richard Lawrence & Peter Green: [The Humanizing Work Guide to Splitting User Stories](https://www.humanizingwork.com/the-humanizing-work-guide-to-splitting-user-stories/)
- NextAgile: [Vertical Slicing and Horizontal Slicing](https://nextagile.ai/blogs/agile/vertical-slicing-and-horizontal-slicing/)
- Bill Wake: [INVEST in Good Stories](https://xp123.com/invest-in-good-stories-and-smart-tasks/)
- Mike Cohn: [User Stories Applied](https://www.mountaingoatsoftware.com/books/user-stories-applied)
- Martin Fowler: [Feature Branch](https://martinfowler.com/bliki/FeatureBranch.html) — on shipping small increments safely
- LeadDev: [Breaking down work for faster delivery](https://leaddev.com/agile-other-ways-working)
