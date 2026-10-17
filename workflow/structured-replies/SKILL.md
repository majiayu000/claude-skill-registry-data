---
name: structured-replies
description: Shape assistant replies. Simple questions → terse direct answer, freeform. Complex / multi-topic / process answers → open with headlines + one-line summaries, optionally an ASCII visual (diagram, mockup, table, flow) when order or layout matters, then short detail sections that each say what was understood, how it was done, and (when non-obvious) why. Use only when the user names this skill or asks for this reply style.
disable-model-invocation: true
---

# structured-replies

Apply on EVERY reply. The first decision is always: simple or complex?

## Decide first

- **Simple** — one topic, fits in a sentence or short paragraph. Skip the scaffold. Answer directly. No headlines, no summary block, no ASCII. Freedom.
- **Complex** — multiple topics, a process, a plan, a comparison, a change with several moving parts, anything the reader will scroll. Apply the structure below.

When unsure, lean simple. The user can always ask for more.

## Structure for complex replies

1. **Headlines + one-line summaries** at the top. Each topic gets one bullet: bold title + ≤1 sentence hook. The reader should be able to stop here and still grasp the shape.
2. **ASCII visual** when explaining a process or layout — diagram, mockup, table, flow, sketch in a fenced block. Use it when temporal order, structure, or relationships matter. Skip when prose is clearer.
3. **Detail sections**, one per headline, in the same order. Each section is brief and uses these labels:
   - **Understood** — mirror the request back in one line so expectations align before diverging.
   - **How** — the actual answer / steps / change.
   - **Why** — include only when the reason is non-obvious or a tradeoff was made.

Bullets beat paragraphs. Code blocks for code. No filler. No closing summary that repeats the top.

## Example

User: *"Help me set up CI for my Node project — tests, lint, deploy on tag."*

A well-structured reply looks like this:

---

### Summary
- **Workflow file** — One GitHub Actions YAML at `.github/workflows/ci.yml`.
- **Jobs** — `test` and `lint` on every push; `deploy` only when a `v*` tag is pushed.
- **Secrets** — `NPM_TOKEN` (or deploy creds) added under repo settings.

### Pipeline shape
```
   push                         tag v*
    │                             │
    ▼                             ▼
 ┌──────┐   ┌──────┐         ┌────────┐
 │ test │──▶│ lint │   ───▶  │ deploy │
 └──────┘   └──────┘         └────────┘
```

### Workflow file
- **Understood:** one CI file covering tests, lint, and tagged deploys.
- **How:** three jobs in `ci.yml`, gated by `on.push` and `on.push.tags`.
- *(code block here)*

### Secrets
- **Understood:** the deploy job needs auth that local devs already have.
- **How:** Settings → Secrets → Actions → add `NPM_TOKEN`.
- **Why:** tag-triggered deploys run on GitHub runners with no local credentials.

---

## Notes

- The "Understood" line is the cheapest insurance against shipping the wrong thing — use it whenever the request had any ambiguity.
- Don't pad a simple answer to look thorough. Brevity is the feature.
- An ASCII visual is a tool, not a tax. Skip it if prose says it faster.
