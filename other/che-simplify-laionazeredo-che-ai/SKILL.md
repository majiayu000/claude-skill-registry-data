---
name: "che-simplify"
description: "Produces a SIMPLIFICATION PLAN for something already planned or implemented (epic, task graph, gh-stack plan, module, codebase area). Applies the Simplicity Bias (engineering-contracts §1) with the GOALS held fixed: it classifies every element as essential or accidental complexity, then proposes the smallest plan that still meets the goals — merging slices, deferring items, collapsing PR layers, removing unearned abstractions. Output is a spec-shaped plan plus a decision trail. NEVER a verdict (that is che-code-review) and NEVER a pure explanation (that is che-explain)."
---

# Che — Simplify (plan reduction under fixed goals)

> **SHARED REFERENCES (CANONICAL — do NOT duplicate the body here):**
> - Simplicity Bias + essential vs accidental complexity: `engineering-contracts` §1
> - LEAN/YAGNI overengineering scanner (L1-L13): `che-scope-checker` skill
> - Vertical-slice model: `che-plan` skill
> - Reading an existing plan (comprehension only): `che-explain` skill

This is a SPEC written **in reverse**: the input is something already planned or built, and the change
is a **reduction**, not a new feature. The output is a plan — not code.

---

## §0 PURPOSE

Reduce an existing plan (or an implemented area) to the smallest version that still meets the GOALS.
Cut accidental complexity; keep essential complexity; record every cut.

---

## §1 INPUT (pick one)

- A task graph (`task_graph.md`), a gh-stack plan (`gh_stack_plan.md`), a SPEC, or a codebase area.
- The **GOALS** — mandatory. Without fixed goals there is nothing to simplify against.

---

## §2 THE INVARIANT

**The GOALS are fixed.** Everything else is a candidate for reduction. A cut that breaks a goal is
**scope removal**, not a simplification, and it needs explicit user approval — never a silent cut.

---

## §3 PROCESS

1. **Restate the goals verbatim** (from the plan / ticket / user). No goals → stop and ask.
2. **Inventory** every element: subtask, module, abstraction, PR layer, dependency, config.
3. **Classify each element** as **Essential** (a goal demands it) or **Accidental** (we added it:
   premature abstraction, unearned generality, defensive completeness). Use `engineering-contracts`
   §1 and the `che-scope-checker` L1-L13 scanner.
4. **Propose the reduced plan**: merge slices, defer accidental items, collapse PR layers, drop
   abstractions that have fewer than two present cases.
5. **Decision trail**: for every cut → what, why, the risk if the cut is wrong, and whether it is
   reversible.

---

## §4 HARD RULES

- **Never cut essential complexity** — a goal-demanded element is not a candidate.
- **Classification is mandatory and explicit** — no silent deletions.
- **Every cut is reversible or flagged** — an irreversible cut needs explicit user approval.
- **Goals are quoted, not paraphrased** — so the reduction can be audited against them.
- **The output is a plan** — not a verdict (`che-code-review`) and not an explanation (`che-explain`).

---

## §5 OUTPUT

Write the plan as a **worktree artifact** — never inside the worktree, never the fallback:

1. Resolve the storage env FIRST (without it, `che output_path` falls back to a folder inside the Che
   repo): `eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"`
2. Resolve the path: `SIMPLIFY_PLAN="$(che output_path report simplify-plan "$RELATED_ID" workspace md)"`
   → `$CHE_WORKSPACE_SHARED/reports/<related_id>/<YYYYMMDD-HHMMSS>-simplify-plan.md`
3. Write it with the content on **stdin** (the helper reads stdin, not an argument):
   `che write_file_atomic "$SIMPLIFY_PLAN" <<'PLAN_EOF' … PLAN_EOF`.

> **Never** write it under `specs/` — `che-act` discovers the approved SPEC via `specs/**/*.md` and
> would mistake the plan for one.

- `decisions.log` entry via `che decision_append`: `SIMPLIFY_PLAN` (elements, essential, accidental,
  cuts, path).
- Sections: Goals (verbatim) · Inventory · Essential vs Accidental table · Reduced plan ·
  Decision trail · Deferred by design.

---

## §6 WHAT IT IS NOT

- **Not `che-explain`** (comprehension) · **not `che-code-review`** (verdict) · **not `che-refactor`**
  (that one changes code, this one changes plans) · **not a licence to drop requirements**.
