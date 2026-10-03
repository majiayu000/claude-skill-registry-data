---
name: feature-spec
argument-hint: [feature name or description]
description: Understand an existing feature end-to-end and produce a functional spec in /specs plus a user-facing doc in /docs.
allowed-tools: Read, Write, Grep, Glob, Bash, Agent, AskUserQuestion
---

# Feature Spec

Given a feature in the current repo, produce two deliverables:

1. **`/specs/<feature>.md`** — the comprehensive functional specification.
2. **`/docs/<feature>.md`** — a short, scannable user-facing doc that links into the spec.

Feature target: `$ARGUMENTS`

If `$ARGUMENTS` is empty, use `AskUserQuestion` once to ask what feature to document. Otherwise proceed.

---

## Core principle — functional, not implementation

Both deliverables document **what the feature does for the user**, not how it is built. The redesign (or any future rewrite) should be possible using only these two documents.

**Do include:**
- Roles and what each role can do
- Surfaces (every screen, modal, page, email, notification)
- User-facing behavior for each surface (what the user sees, enters, clicks)
- Business rules (validation, routing, branching, conditionals)
- Post-action effects (what the user and the system see happen after each action)
- Integrations described by **user impact** ("sends the respondent an email", not the email service name)
- Permissions by role
- Entry-point URLs
- Settings the user can toggle and what each one does
- Known constraints, quirks, and limitations

**Do NOT include:**
- File paths, line numbers, module names
- Database collection / table names, field names, schemas
- Function names, service names, class names, RPC names
- Security rule code blocks, config snippets
- Framework specifics (React component names, Firestore rules, etc.)

If an implementation detail is the only way to name a behavior, restate the behavior in plain language. "When the form is submitted, a CRM opportunity is created" — not "the `upsertFormCompletionOpportunity` callable fires."

---

## Step 1 — Scope & orientation

Before reading anything deeply, get the shape of the feature.

1. Confirm the **target branch** to read. Almost always this means the legacy/main implementation, not the in-progress redesign. Ask via `AskUserQuestion` if ambiguous (e.g., "Should I document the feature as it exists on `main`, or the in-progress version on the current branch?").
2. Identify entry points: routes, top-level components, exported callables, cron/triggers. Use `Grep` / `Glob` to find them quickly.
3. Produce a working list of **surfaces** (what a user can see/do) and **roles** (who sees what). Roles usually emerge from permission checks.

At the end of this step you should be able to answer: *"If a stranger asked me to name every screen, email, and URL this feature touches, could I?"* If not, keep scoping.

---

## Step 2 — Understand the functionality (parallel exploration)

Spawn multiple `Agent` (subagent_type: `Explore`) calls in a **single message** to shard the reading across the codebase. This keeps context usable and is dramatically faster than serial reading.

Typical shards (adjust to the feature):
- **Renderer / respondent surface** — what the end user sees and does.
- **Editor / author surface** — what the internal user configures.
- **Assignment / distribution** — how work is handed off between roles.
- **Services & utils** — the business rules (validation, routing, score calculation, field mapping).
- **Backend triggers & callables** — what happens on submit, on create, on status change.
- **Routes, permissions, security rules** — who can reach what.

Each Explore agent should return **structured findings**: surfaces, behaviors, user-facing rules — not file inventories. Remind the agent: "Return behavior, not file paths." Expect ~1 return message per shard.

Reconcile the findings against any existing plan or prior notes. When the plan contradicts the code, trust the code and flag the mismatch in the spec's "Constraints / Quirks" section.

---

## Step 3 — Write `/specs/<feature>.md`

Target a **comprehensive functional reference**. Do not prune — pruning comes later. Typical sections (adjust to fit; omit sections that genuinely do not apply):

1. **Overview & glossary** — the feature in 2-3 paragraphs; every synonym the codebase uses for this feature.
2. **Roles** — every role that can touch the feature and what they can do.
3. **Entry points** — URLs, modals, emails, notifications that open the feature.
4. **Author / builder experience** — step by step, what the internal user sees and configures.
5. **Respondent / consumer experience** — step by step, what the end user sees and does.
6. **Alternate paths** — guest, embed, public, unauthenticated, legacy, admin-override, etc.
7. **Types / variants** — every kind of thing the feature can contain (question types, field types, block types…). Describe by **behavior**, not by enum value.
8. **Conditional logic / rules / routing** — every condition and action, in prose.
9. **Lifecycle / state transitions** — pending → in-progress → completed, draft → published, etc.
10. **Post-action effects** — what automatically happens after each meaningful user action (emails, downstream records, redirects, integrations).
11. **Completion actions / exits** — every way the flow can end and where the user lands.
12. **Reporting / responses view** — what the internal user sees about completed work.
13. **Validation rules** — user-facing: what must be filled, what formats are accepted, what errors show.
14. **Notifications & emails** — each message, its trigger, its audience, its content summary.
15. **Integrations (user impact)** — what each integration *enables the user to do* or *causes to happen*.
16. **Permissions** — role → capability matrix.
17. **Settings reference** — every toggle/option and the behavior it controls.
18. **Constraints, quirks, limitations** — anything the next builder needs to know but won't find in the happy path.

Rules while writing:
- Keep sentences concrete. Name the user, the screen, and the outcome.
- When a behavior is ambiguous or undocumented, **call it out** rather than guess. Mark it `**Open question:** …`.
- When the plan said X but the code does Y, document Y and note the discrepancy.

---

## Step 4 — Write `/docs/<feature>.md`

Short (~100-200 lines), scannable, designed to sit alongside other `/docs/*.md` entries. Purpose: let a newcomer understand what the feature is in 2 minutes and know where to go for depth.

Standard structure:
1. **What this feature is** — 2-3 paragraphs.
2. **Who uses it** — roles, one line each.
3. **Surfaces** — bullet list of every screen/page/email, one line each.
4. **Entry-point URLs** — a table.
5. **What happens on submission / on the main action** — bullet list of effects.
6. **Integrations (user impact)** — one line each.
7. **Link to full spec** — `See [/specs/<feature>.md](../specs/<feature>.md) for the comprehensive specification.`

The docs entry must match the spec's functional framing — do not sneak in implementation details here. If you find yourself writing a function name or collection path, restate it as a user-visible effect.

---

## Step 5 — Verify

Before declaring done:

1. Re-read both files top to bottom.
2. Grep each file for leaked implementation terms (file extensions like `.ts`/`.tsx`/`.jsx`, `collection`, `callable`, `trigger`, framework names). If any slip through, rewrite them as user-facing behavior.
3. Confirm every surface mentioned in the spec appears in the docs entry's surface list (docs is a superset *index*, spec is the deep dive).
4. Confirm the docs entry's spec link path is correct relative to `/docs/`.

Report back with:
- Absolute paths of both created files.
- A one-line summary of what each documents.
- Any **Open questions** flagged in the spec that the user should answer.

---

## Notes

- **Never guess the filename.** Ask the user or derive from the feature name. Common pattern: lowercase, dashed, singular or pluralized to match sibling files (`forms.md`, not `form-feature-final.md`).
- **Never prune during the first pass.** Over-document. Pruning is a later step the user will drive.
- **Never compare to the redesign.** These deliverables describe the existing feature. Redesign-vs-legacy comparisons belong elsewhere.
- **Never include conversation context.** Someone reading these files a year from now must not need to know who asked for them or why.
