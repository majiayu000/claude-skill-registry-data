---
name: write-tickets
description: Single entry point for turning a design, plan, PRD, or in-chat spec into either a single GitHub Issue or a parent epic with child issues. Use when the user wants to create, review, or improve any ticket destined for a coding agent or another developer to pick up. Covers atomic issues, bug reports, technical tasks, spikes, and epic breakdowns using tracer-bullet vertical slices. Output is AFK-ready by default — written so a coding agent days later can produce the right work without the original chat context.
model: opus
effort: high
---

Two shapes of work:

1. **Atomic issue** — one user story, bug, technical task, or spike. Use the workflow in this file.
2. **Epic + child issues** — a design / plan / PRD broken into independently-grabbable vertical slices. Use the workflow in **[references/epic-breakdown.md](references/epic-breakdown.md)**.

Every ticket body must be **AFK-ready** by default — durable enough that a coding agent picking it up days later, with no access to the original chat context, can produce the right work. The principles are in **[references/agent-brief.md](references/agent-brief.md)** and they apply to atomic issues and epic children alike.

- Be extremely concise and sacrifice grammar for the sake of concision. Write the issue body to be easy to understand and read (3rd grader level language). Clear and concise.
- Run the workflow as a skeptical, iterative collaboration with the user

---

## Tracer-bullet vertical slices

Every ticket — atomic or child of an epic — is a **thin vertical slice** cutting through every relevant layer (schema, API, UI, tests, docs) end-to-end. Not a horizontal layer cake.

| Bad (horizontal by layer) | Good (vertical by behaviour) |
|---|---|
| Issue 1: Build all schema | Issue 1: Password reset path (schema + API + UI + test) |
| Issue 2: Build all APIs | Issue 2: Password change path (schema + API + UI + test) |
| Issue 3: Build all UIs | Issue 3: Password complexity rules (validation + UI hint + test) |
| → Nothing shippable until all complete | → Each issue shippable on its own |

Rules:

- Each slice delivers a narrow but **complete** path. A completed slice is demoable or verifiable on its own.
- Prefer many thin slices over few thick ones.
- Documentation-only slices are valid (e.g. an ADR + `CLAUDE.md` note). They follow the same rules.
- **Size**: 1–2 days for one developer end-to-end (implementation, tests, review, fixes). If it can't fit, it's an epic — use **[references/epic-breakdown.md](references/epic-breakdown.md)**.

---

## Work-readiness: AFK vs HITL

Every ticket carries one of two tags in its body, right under the title:

- **AFK** (Away From Keyboard) — a Claude Code agent can implement and merge this without human interaction. All decisions are resolved; acceptance criteria are testable; scope is clear.
- **HITL** (Human In The Loop) — requires human judgment during implementation: architectural decision, design review, UX trade-off, or security call.

Prefer AFK where possible. If a ticket is HITL, note *why* in one line (e.g. "HITL — needs design review before shipping", "HITL — schema trade-off needs product input").

Format goes in the issue body, not as a label:

    **Work-readiness:** AFK

    or

    **Work-readiness:** HITL — <reason>

---

## Interactive Workflow

1. **Identify the type** — story, bug, task, spike, or epic — and whether the user is drafting fresh, improving an existing ticket, or reviewing.
2. **Walk through the AFK body sections** in `agent-brief.md` § Body template — Purpose, Current/Desired behaviour, Key interfaces, Acceptance criteria, Out of scope, References. Defer type-specific fields to the per-type template.
3. **Challenge red flags**: missing impact, vague language, untestable AC, and size — break down if >2 days, combine if <30 min. Acceptance-criteria rules live in `references/agent-brief.md` § Acceptance criteria.
4. **Iterate** until the ticket passes the *Ready for Development* test: a developer unfamiliar with the context could complete it without asking questions.
5. **Apply [agent-brief.md](references/agent-brief.md)** (durability, behavioural, testable AC, explicit out-of-scope), then emit the matching template:
   - Story → [story-template.md](references/story-template.md)
   - Bug → [bug-template.md](references/bug-template.md)
   - Task → [task-template.md](references/task-template.md)
   - Spike → [spike-template.md](references/spike-template.md)
   - Epic → [epic-template.md](references/epic-template.md), then break down via [epic-breakdown.md](references/epic-breakdown.md)

---

## Publish gate

Before creating the issue, confirm:

- [ ] `## Purpose` is filled — not "TBD" or restating the title.
- [ ] Blockers are documented (`Blocked by #N` if any).
- [ ] No open questions in your head — if there are, surface them in chat first.
- [ ] Work-readiness tag (AFK/HITL) reflects honest assessment, not aspiration.

---

## Publishing to GitHub Issues

You author; you do **not** run `gh` yourself. Once the body is final, write it to a file and **delegate publishing to the `github-issue` agent** (`subagent_type: github-issue`) — it creates the issue, adds it to the repo's linked Project board, sets the fields, and runs the validation gate, returning distilled refs + the verdict so the verbose tracker output stays out of your context. For an atomic issue, hand it the title, body file, labels, milestone, and the field plan (Status/Start/Target). For an epic + children, follow **[references/epic-breakdown.md](references/epic-breakdown.md)** § Publish — same one-call handoff with the ordered child list and number-token bodies.

The GitHub-specific spec the agent implements — project field table, sub-issue mechanics, "Related tickets" conventions — lives in **[references/github-publishing.md](references/github-publishing.md)**. Read it so your field plan and body files match what the agent expects.

---

## Post-publish validation gate

The bundled validator is a **hard gate** — it audits body sections and the board's fields (including the roadmap-driving Start date / Target date) against the per-type requirements in `scripts/rules.ts`. The `github-issue` agent runs it as the final step of publishing (`validate-ticket.ts <issue-number>` for one ticket, `--epic <P>` for an epic + every sub-issue in one pass) and loops until exit 0, returning the verdict.

Gate on the agent's reported result before declaring the work done. A **content** failure (missing section, weak AC — exit 1, often a missing Start/Target date) comes back to you: fix the body file or field plan and re-delegate, passing the existing issue numbers so the agent edits in place rather than re-creating. Exit 2 means the board could not be read (gh auth / API change / a renamed field) — an environment problem to surface, not a body fix.
