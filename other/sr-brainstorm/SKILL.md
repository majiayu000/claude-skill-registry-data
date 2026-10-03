---
name: sr-brainstorm
description: >
  Phase 1 of the SRS workflow. User gives a project topic → AI runs a deep,
  categorized brainstorm (5 mandatory rounds) to fully understand actors,
  features, scope boundary, tech constraints, and business rules before
  writing anything.
---

# sr-brainstorm

Goal: fully understand the project before a single word of spec is written.
Do NOT write spec, plan, or SRS in this session.

---

## Step 0 — Topic Intake

Receive topic from user. Do NOT ask questions yet.

Identify:
- Domain (e-commerce | healthcare | fintech | SaaS | internal tool | mobile | other)
- Scale signals (MVP | startup | enterprise | unknown)
- Any constraints already mentioned

Echo back:
```
Topic:   {topic}
Domain:  {domain}
Scale:   {scale}
Slug:    {kebab-case name for projects/{slug}/}
```

Confirm slug with user before proceeding. If topic is too vague to form a slug, ask.

---

## Step 1 — Load Domain Questions

Load `.codex/skills/srs-workflow/references/brainstorm-guide.md`.
Select the question bank matching the detected domain.

---

## Step 2 — Round 1: Actors & Users

Ask the user with concrete role options (not open-ended).

Ask about:
- Primary end users (with examples from the domain)
- Secondary users / supporting roles
- Admin / back-office roles
- External systems / third-party integrations

Wait for answer. Record each confirmed actor as:
```
[ACTOR] {name}: {description} | access level: {read/write/admin}
```

---

## Step 3 — Round 2: Core Features

Ask the user. Present a feature checklist derived from domain + topic.

For each feature cluster offer sub-options. Example for e-commerce:
- Authentication: (A) email+password (B) OAuth (C) both (D) SSO enterprise
- Catalogue: (A) simple products (B) configurable SKUs (C) bundles (D) subscriptions

Mark each selection as [CONFIRMED]. Infer likely missing features — ask to confirm or reject.

Wait for answer.

---

## Step 4 — Round 3: Scope Boundary

Ask the user. Present a two-column table:

| IN Scope (proposed) | OUT Scope (proposed) |
|---------------------|----------------------|
| {feature A}         | {feature X}          |

Ask user to move items between columns or add new ones.

**HARD BLOCK:** Do not proceed without explicit in/out boundary confirmed by user.

Wait for answer.

---

## Step 5 — Round 4: Technical Constraints

Ask the user:
- Tech stack (present common options for the domain)
- Hosting (cloud provider / on-premise / hybrid)
- Existing systems to integrate (with yes/no options)
- Security & compliance (GDPR | HIPAA | PCI-DSS | SOC2 | none)
- Performance targets (show numeric examples: < 200ms | < 500ms | < 1s)
- Timeline / budget signals

Wait for answer.

---

## Step 6 — Round 5: Business Rules & Edge Cases

Ask the user:
- Roles and permissions model (RBAC | ABAC | simple owner/member | custom)
- Data ownership and retention rules
- Key failure scenarios the system must handle gracefully
- Pricing / billing logic (if applicable)
- Regulatory requirements beyond what's already captured

Wait for answer.

---

## Step 7 — Completeness Check

After Round 5, self-check against this list. Any gap = add a follow-up question NOW:

- [ ] Every actor has name + description + access level
- [ ] Every feature in IN scope has been confirmed (not just inferred)
- [ ] OUT scope list is explicit (minimum 3 items)
- [ ] At least one numeric NFR target per: Performance / Availability / Security
- [ ] At least one business rule per feature cluster
- [ ] Compliance requirements stated (even if "none")
- [ ] Integration points listed (even if "none")

If ANY box is unchecked: ask a targeted follow-up round before proceeding.

---

## Step 8 — Save Brainstorm Output

Write `projects/{slug}/brainstorm.md`:

```markdown
# Brainstorm: {project name}
Date: {date}

## Topic
{user's original topic verbatim}

## Domain / Scale
{domain} / {scale}

## Actors
{list with [ACTOR] entries}

## Confirmed Features (IN Scope)
{confirmed list}

## OUT of Scope
{explicit list}

## Technical Constraints
{answers from Round 4}

## Business Rules
{answers from Round 5}

## NFR Baselines
{confirmed numeric targets, or [TBD] with context}

## Open Items
{anything still unresolved — will become [TBD] tags in spec}
```

---

## Step 9 — Handoff

Output:
```
Brainstorm complete.

Project: {name}   Slug: {slug}
Actors:  {count}
Features confirmed (IN scope): {count}
OUT scope items: {count}
Open items: {count}

Saved: projects/{slug}/brainstorm.md

Next: $sr-spec → writes the full spec from this brainstorm
```
