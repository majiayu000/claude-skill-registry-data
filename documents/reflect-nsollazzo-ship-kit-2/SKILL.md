---
name: reflect
description: |
  Capture session knowledge (gotchas, patterns, integration quirks) into the project's
  knowledge base. Use when: session involved tricky bugs, new integrations, non-obvious
  patterns, or hard-won lessons. Also use when asked to "reflect", "capture lessons",
  "what did we learn", or "save knowledge". Works after any coding session, not just
  commits. Distinct from `wrap-up`, which reports unfinished work and writes nothing —
  reflect writes to the knowledge base.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
---

# Reflect — Session Knowledge Capture

Scan the current session for valuable lessons and route them to the right knowledge target.

> **Sub-agents.** Reflect stays a single fast pass (it targets under 60s) over *this* session's
> context, which lives in one place — there's nothing independent to fan out, and spawning
> sub-agents would only add latency. Keep it inline.

## Workflow

### Step 1: Gather Session Context

Read-only scan of what happened this session:

```bash
git diff <base> --stat        # <base> = the branch you diverged from (often main)
git log <base>..HEAD --oneline
git diff <base>
```

Also review conversation context: problems solved, errors hit, workarounds applied, patterns discovered.

### Step 2: Scan Existing Knowledge Base

Quick skim (not full read) to avoid duplicates. Check whichever of these your environment
uses:

- The agent's long-term memory / `MEMORY.md` (wherever your harness stores it) — current gotchas
- Project instruction file (`CLAUDE.md`, `AGENTS.md`, or equivalent) — current rules
- The skills directory listing — skill coverage
- `docs/` directory listing — existing documentation

### Step 3: Identify Knowledge Gaps

Classify each insight into exactly one category:

| Category | Target | When |
|----------|--------|------|
| **Gotcha** | Memory / `MEMORY.md` | Non-obvious trap or workaround |
| **Rule** | Project instruction file | Project-wide always/never pattern |
| **Skill update** | the relevant skill's folder | Existing skill missing info |
| **New skill** | a skill-creation flow | New integration worth codifying |
| **Docs** | `docs/` | Missing guide or troubleshooting |

**Filters:**
- Skip routine changes (simple renames, formatting, obvious fixes)
- Skip duplicates of existing knowledge
- Max 7 suggestions
- Priority: gotchas > rules > skill updates > docs > new skills

### Step 4: Present Verdict

Concise table — scannable in 5 seconds. State your own verdict per item: what is worth
saving (**save**) and what is not (**skip**, with the reason). Don't present a neutral menu
— commit to a recommendation.

```markdown
## Session Reflection

| # | Category | Target | Verdict | Insight |
|---|----------|--------|---------|---------|
| 1 | Gotcha | MEMORY.md | save | Nested array validators panic at runtime, not build time |
| 2 | Skill | simplify | save | Add headless login refresh pattern |
| 3 | Docs | docs/ | skip — already covered by deploy runbook | Deploy env-var steps |

**Why 1:** We hit a runtime panic when... (1 sentence)
**Why 2:** The headless flow required... (1 sentence)
```

If nothing worth capturing: **"No new knowledge. Existing docs cover this session."** — stop here.

### Step 5: User Approval

Do NOT use a structured multiple-choice prompt. End the turn with: **"Saving 1–2, skipping 3
— ok?"** and wait for the user's reply in plain chat:
- **ok / yes / 👍** → apply your verdicts as presented
- **ko / no** → apply nothing
- **a comment** (e.g. "also save 3", "drop 2", "reword 1") → adjust the verdicts accordingly, then apply

NEVER auto-apply without that reply.

### Step 6: Apply Approved Updates

For each approved suggestion:

| Category | Action |
|----------|--------|
| **Gotcha** | Append to the memory store / `MEMORY.md` under the appropriate section heading |
| **Rule** | Add to the project instruction file in the relevant section |
| **Skill update** | Edit the skill's `SKILL.md` or its reference files |
| **New skill** | Print "Build skill X with your skill-creation flow" — NEVER auto-create skills |
| **Docs** | Create or update file in `docs/` |

Keep edits minimal — add bullet points, don't reorganize existing content.

### Step 7: Commit Knowledge Changes (Optional)

Ask user whether to commit with: `docs: capture session lessons`

If user declines, leave changes staged but uncommitted.

## Rules

- NEVER auto-apply without user approval (Step 5) — but approval is a plain chat reply
  (ok/ko/comment), never a structured menu prompt
- NEVER create new skills directly — route to a skill-creation flow
- NEVER modify source code — only knowledge files (memory, instruction file, skills, docs)
- Max 7 suggestions per reflection
- Keep it FAST — this should take under 60 seconds
- Gotchas → memory store, permanent patterns → project instruction file
- One sentence of "why" context per suggestion — no essays
