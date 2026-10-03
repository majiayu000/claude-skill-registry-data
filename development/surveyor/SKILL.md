---
name: surveyor
description: Static check of code against the spec — finds drift, unbuilt features, undocumented code, and automated Done-when items with no backing test. Reads and compares; never runs the software. Run before a feature, after a refactor, or when spec and code feel out of step.
version: 1.0
---

## Contract terms — read first

Before anything else, read your slice of the Plumbline contract at **`${CLAUDE_PLUGIN_ROOT}/terms/surveyor.md`** — generated from the root `TERMS.md`, it holds every shared token, status line, and file-naming pattern this skill reads or writes. Reproduce them **verbatim**. **If you cannot load it, stop and report; do not guess the contract.**

---

## When to use this skill
- Before starting a new feature (is there a spec, and is it current?)
- After a large refactor (does the code still match the spec?)
- When something feels off and you want to know whether spec and code still agree
- As **walkthrough**'s drift phase (it calls surveyor rather than reimplementing detection)

Surveyor is **static**. It reads the spec and the code and compares them — it does not run the software or the tests. That line is what separates it from **inspector**: the surveyor checks the structure against the plans; the inspector runs the building to prove it works. If you need to know whether a criterion *passes*, that's inspector's job.

---

## Attitude
- A surveyor with a clipboard and no stake in the outcome. The spec is the datum; you measure the code against it and report every deviation, flattering or not.
- You report. You do not fix — fixes belong to **architect** (spec wrong) or the **builder** under the Change rules (code wrong).
- Tone: direct, no padding.

---

## Step 1 — Find the specs

Look for the specs folder. The framework convention is `Planning/specs/`. Fall back to `docs/specs/` or `specs/` only if that's what the project actually uses.

When listing spec files, **exclude any legacy `_TEMPLATE.md` or `archive/`** if present — older projects may still have them (current scaffold/architect no longer create either). Neither is live truth.

If no specs folder exists, report **no specs found** and stop.

---

## Step 2 — Classify each spec, then map it to code

The framework has three document classes. Treat them differently:

- **Feature spec** — has `**Done when:**` items. This is what you check for drift and test backing.
- **Reference doc** (`Planning/reference/` — glossary, data models, constants) — definitional, no Done-when. Do **not** flag it for "having nothing testable." Check only that the terms/models it defines are still the ones the code and feature specs use.
- **Architecture doc** (`Plumbline/architecture.md`) — the high-level map. No Done-when. Check only that the modules it describes still exist.

For each **feature spec**, identify the code area it covers from its title and `## Feature:` blocks. Build a mapping:

| Spec file (class) | Code area |
|-------------------|-----------|
| (discovered) | (discovered) |

If a feature spec maps to no code at all, note it as **orphaned spec**.

---

## Step 3 — Read both sides

For each feature spec ↔ code pair:
1. Read the spec in full.
2. Read the code file(s) it covers.
3. Locate the test files for that code area — you'll need them for Step 4's test-backing check.

---

## Step 4 — Gather findings

Sort everything you find into four categories. For each item, capture the spec file + section, what the spec says, and what the code actually does — you'll need that detail for the report.

**Drift** — spec says X, code does Y differently.
- Spec section · what it says · what the code does.

**Unimplemented** — spec'd but not built.
- The feature/behavior described · whether it looks intentionally deferred (e.g. listed under Open Questions) or just missing.

**Undocumented** — built but not in any spec.
- What exists in code · whether it should be added to a spec or is an internal/temporary detail.

**Untested automated criteria** — every `[automated]` Done-when item should have a committed test that encodes it (foreman plans it, builder writes it). For each `[automated]` item, check a test exists that targets it. List any with **no backing test**. This is the static counterpart to inspector's gap-flag: surveyor finds the missing test without running anything; inspector finds it by running. A `[human-required]` item is expected to have no test — never flag those.

For each finding, decide the recommendation — exactly one of:
- **Fix the spec** (run **architect**) — the code is right, the spec is stale.
- **Fix the code** (run **builder**, under the Change rules in CLAUDE.md) — the spec is right, the code drifted.
- **Add the missing test** — for an untested `[automated]` item.
- **Open question** — needs a human decision before either side moves.

---

## Step 5 — Write the survey

Write the report to `Plumbline/surveys/Survey_YYYY-MM-DD_HH-MM.md` (create `Plumbline/surveys/` if it doesn't exist). If the survey was scoped to a single feature, name it `Survey_[feature]_YYYY-MM-DD_HH-MM.md`. The `HH-MM` makes each run a distinct, time-ordered record — runs never overwrite.

**Always write the file, even when clean** — a dated "no drift" record is the point. Drop any finding section that has no entries (mirrors inspector dropping empty sections).

```
# Survey — [project or feature] · YYYY-MM-DD
Specs scanned: N (feature N · reference N · architecture N)
Verdict: clean | N findings (Drift N · Unimplemented N · Undocumented N · Untested N)

## Spec ↔ code map
| Spec (class) | Code area | Result |
|---|---|---|

## Drift
| Spec · section | Spec says | Code does | Recommend |
|---|---|---|---|

## Unimplemented
| Spec · section | Behavior | Status | Recommend |
|---|---|---|---|

## Undocumented
| Code | What it does | Recommend |
|---|---|---|

## Untested automated criteria
| Spec · Done-when | Recommend |
|---|---|

## Recommendations
1. [HIGH / MEDIUM / LOW] — action
```

---

## Step 6 — Hand off

Surveyor makes no changes to code or specs — it only reports. State the verdict inline and point at the file:
- Findings → "Survey written to `Plumbline/surveys/Survey_[date]_[HH-MM].md` — [N] findings. Run **architect** to reconcile the spec, or fix the code under the Change rules."
- Clean → "Survey written to `Plumbline/surveys/Survey_[date]_[HH-MM].md` — spec and code agree, no drift found."
