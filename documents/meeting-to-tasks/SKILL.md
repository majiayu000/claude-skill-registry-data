---
name: meeting-to-tasks
description: "Reconcile a meeting synthesis or client notes with the codebase and produce a structured task tracking file. Use for \"analyse la synthèse\", \"qu'est-ce qui reste à faire\", \"compare the decisions with the code\", \"what did we decide vs what's implemented\"."
---

# Mission

Bridge the gap between what was *decided* in a meeting and what is *actually built*
in the codebase. The output is a single structured markdown file a developer can
act on immediately — no vague summaries, no duplicating what the meeting doc already says.

The value is in the **cross-check**: finding the delta between decisions and code,
and expressing that delta as clear, actionable tasks.

---

## Step 1 — Ingest the meeting synthesis

Read every source the user provides:
- Meeting synthesis / notes / action items
- Tickets, specs, or follow-up emails if given

Extract three things:
1. **Decisions made** — rules, UX changes, architecture choices, constraints confirmed
2. **Explicit action items** — who does what, by when
3. **Implicit rules** — things said casually ("it shouldn't even be possible to select
   that") that imply a behavior but weren't formally written as rules

Keep a mental note of which items are *in-code* concerns vs. *organizational* concerns
(e.g., "contact Caroline for a test session" is not a code task).

---

## Step 2 — Analyze the codebase

Don't rely solely on what the user tells you — actually look at the code to confirm
what's there. Use Glob and Grep to find the relevant files, then read them.

For each decision/action item from Step 1, ask: **"Is this already in the code?"**

Look for:
- The feature/behavior itself (UI element, function, validation, field)
- The correct *shape* of implementation (e.g., a field exists but the label is wrong,
  or a value is hardcoded when it should be dynamic)
- Anything that contradicts the meeting decision (old behavior that should have been removed)

Classify each item:
- **✅ Done** — implemented correctly, confirmed in code
- **☐ À faire** — not present in code at all
- **🔄 Partiel** — exists but incomplete, misnamed, wrong behavior, or missing a constraint

---

## Step 3 — Write the task document

Save the output to `[project-docs-dir]/taches-[project-slug]-[YYYY-MM-DD].md`.
If a logical docs folder exists (like `prototype/docs/`), use it. Otherwise save
next to the synthesis file.

### Document structure

```markdown
# Tâches [Project Name] — Suite synthèse [date]

**Source :** [synthesis filename or meeting description + participants]
**Statut document :** En cours

---

## T-01 — [Imperative task title]

**Fichier(s) :** `path/to/file` (line ~N if relevant)
**Action :** What exactly needs to change. Be specific enough that another developer
             could implement it without asking questions.
**Règle / Contexte :** Why this change exists — the decision or rule from the meeting
                        that drives it. Quote directly if useful.
**Statut :** ☐ À faire | ✅ Fait | 🔄 Partiel — [explanation of what's missing]

---

[repeat for each task]

---

## Tâches hors code (organisationnelles)

| # | Tâche | Responsable | Deadline |
|---|---|---|---|
| H-01 | ... | ... | ... |

---

## Règles implicites à confirmer

List any behaviors inferred from casual remarks or context that weren't formally
validated. Format as: **[Rule description]** — *Basée sur :* "[quote]" — *À confirmer :* [question]
```

### Numbering and ordering

- Code tasks: `T-01`, `T-02`, … — ordered by impact/dependency (blocking tasks first)
- Non-code tasks: `H-01`, `H-02`, … — people tasks, org tasks, to-be-validated items
- Mark tasks that are already done (✅) so the document shows full coverage, not just gaps

### Tone and length

- Keep each task self-contained. A developer reading T-03 shouldn't need to read T-01
  to understand what to do.
- File paths and line numbers make the document dramatically more useful — include them
  when you've confirmed them in the code.
- Don't pad. If a task is two sentences, it's two sentences.

---

## What makes a good task vs. a bad one

**Good:** "Remove `placeholder="8.0"` from `#m-te-heures` (index.html:254) and `#m-tm-heures`
(index.html:285). The field must start empty — a pre-filled placeholder leads users
to skip entering their actual value."

**Bad:** "Fix the hours field default value issue as discussed."

The difference: the good version tells you *where*, *what*, and *why*. The bad version
just restates the meeting problem.

---

## Edge cases

**Multiple synthesis files / tickets:** Merge them. One task document covers all sources.
Note the source per task if origins differ.

**No codebase access:** If you can only read the synthesis (no repo), produce a task
doc based on the decisions alone, mark all statuses as "À confirmer (code non analysé)",
and note this at the top.

**Task already done mid-conversation:** If the user implemented something during the
conversation before you ran this skill, mark it ✅ and add a brief note of what was changed.

**Ambiguous scope:** If a decision could mean two different things in code, list both
interpretations under "Règles implicites à confirmer" rather than guessing.
