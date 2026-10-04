---
name: author-roadmap
description: Draft /roadmap's plan over the vertical slices /shape produced — for each slice estimate its effort, resolve its dependency_notes (plus shared functionalities and those functionalities' spine depends_on) into concrete depends_on slice ids, and propose a value order. Writes a draft only (plan-draft.yaml in STM), never the live model and never the final order numbers. Under direct-model-write (ADR 026) this draft IS the manifest data the play's keyed persist consumes — this skill writes no model file — the coherent order (compute_plan.py) and the in-place spine write (persist_roadmap.py) are the play's deterministic scripts, not this skill.
version: 0.3.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob
---

# author-roadmap

Reads the vertical slices /shape produced across all shaped domains and supplies the
three things a plan needs that a script cannot:

- **effort** — a size estimate per slice (your judgment, read from what the slice
  bundles and the ICE it references).
- **resolved dependencies** — turn each slice's free-text `dependency_notes`, its shared
  functionalities, and those functionalities' ICE `depends_on` into concrete
  `depends_on` slice ids.
- **value order** — a most-valuable-first preference over the slices, used only to break
  ties between slices that don't depend on each other.

It writes a **draft only** (`plan-draft.yaml`). It does NOT assign the final `order`
numbers, does NOT enforce the topological sort, and does NOT detect cycles — those are
deterministic and belong to the play's `compute_plan.py`. This skill supplies effort,
dependencies, and preference; the script turns them into a coherent, dependency-correct,
global order.

**Direct-model-write (ADR 026, `standards/rules/direct-model-write.md`).** This skill writes
NO model file — not the spine `_spine.yaml`, not a grounding doc, nothing under
`product-os/`. `plan-draft.yaml` is a non-model STM artifact: it is the manifest data the
play's keyed persist (`persist_roadmap.py`, via `compute_plan.py`'s `plan.json`) later
applies to the live spine slices in place. The containment split holds trivially here —
the LLM (this skill) touches no shared file; the deterministic keyed script owns the sole
shared file (`_spine.yaml`). Emit the draft and stop.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `snapshot_path` | yes | The `snapshot.json` the play captured — every slice across every domain, with its id, domain_ref, bundled functionality_refs, and dependency_notes. The authoritative list of what to plan. |
| `product_base` | yes | From config — to read each slice's functionalities (their `functionality.md` grounding + the spine `depends_on` on their functionality entries) for effort + dependency judgment. |
| `out_path` | yes | Where to write `plan-draft.yaml` under STM. |
| `stm_base` | yes | From config. |

## Procedure

The effort, the dependency resolution, and the value preference are yours; the data
discipline is non-negotiable.

1. **Read the slices.** From `snapshot.json`, take every slice (across all domains).
   Note its bundled functionalities and its `dependency_notes`.

2. **Resolve dependencies.** For each slice, decide which OTHER slices it must follow,
   from: its `dependency_notes`, functionalities it shares with another slice, and the
   `depends_on` on those functionalities' spine entries. Emit them as concrete `depends_on`
   slice ids. Do NOT invent a dependency the notes/grounding don't support.

3. **Estimate effort.** Size each slice (e.g. S / M / L, or points) from what it bundles
   and the functionality docs it references. Every slice gets an effort.

4. **Propose a value order.** Order the slices most-valuable-first against the product's
   goals. This is only the tie-breaker — the script will still put dependencies first.

5. **Write the draft.** Emit `plan-draft.yaml` at `out_path` in exactly this shape:

```yaml
plan:
  value_order:                 # ids, most valuable first (tie-break only)
    - <slice-id>
    - <slice-id>
  slices:                      # one entry per slice
    - id: <slice-id>
      effort: "M"              # your size estimate (non-empty)
      depends_on: [<slice-id>] # resolved slice deps (ids); [] if none
```

## Boundaries

### NEVER
- Assign the final `order` numbers, run the topological sort, or detect cycles — that is
  `compute_plan.py`'s deterministic job.
- Edit a slice's composition (name, outcome, functionalities, acceptance_intent) or its
  `dependency_notes` — those are /shape's. You only read them.
- Write the live model, or anything other than `plan-draft.yaml` at `out_path`.
- Invent a dependency with no basis in the notes, shared functionalities, or ICE.

### ALWAYS
- Cover every slice in the snapshot: each gets an effort and a `depends_on` (possibly
  empty), and appears in the value order.
- Keep effort non-empty for every slice.
- Return the draft path, not its contents.
