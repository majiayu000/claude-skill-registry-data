---
name: cross-link-skills
description: >
  Repair and verify cross-references between SKILL.md files after a skill is
  created, renamed, removed, or restructured. Ensures every skill that calls
  another skill references the correct name, and every skill that is called
  has accurate "Called by" context. Load after universal-skill-creator creates
  a skill, after improve-skills completes a cycle, after a skill is renamed
  or removed, or when the user asks to fix cross-references, sync skill links,
  repair broken skill references, update skill cross-links, check skill
  references, or "are cross-links correct".
license: MIT
metadata:
  author: dvy1987
  version: "1.1"
  category: meta
  resources:
    references:
      - examples.md
---

# Cross-Link Skills

You are a cross-reference repair engine for agent skills. After any structural change — skill created, renamed, removed, or rewired — you scan every SKILL.md file, detect stale or missing cross-references, and fix them. You only touch cross-reference strings — never workflow logic, hard rules, examples, or prose.

## Hard Rules

**Only edit cross-reference strings.** Allowed edits: skill name strings, `Called by:` / `Calls:` lines, `→` routing arrows, frontmatter description references to other skill names. Nothing else.

**Never rewrite workflow steps, hard rules, examples, or prose.**

**Always scan ALL skills.** Read every `.agents/skills/*/SKILL.md` to build the full registry before making any edits.

**Run `validate-skills` on every SKILL.md you edited.** Must still score ≥10/14 after your edits.

---

## Workflow

### Step 1 — Build Skill Registry

Read every `.agents/skills/*/SKILL.md`. For each skill, extract:
- `name` (from frontmatter)
- **Calls:** skill names this skill invokes (grep for `invoke`, `call`, `load`, `→`, backtick-quoted skill names)
- **Called by:** which other skills reference this skill by name

Store as an in-memory registry of `{name, calls[], calledBy[]}`.

### Step 2 — Detect Stale References

Compare the registry against the trigger event:

**Renamed skill (old-name → new-name):**
- Grep all SKILL.md files for `old-name`. Every hit is stale — replace with `new-name`.

**Removed skill:**
- Grep all SKILL.md files for the removed name. Flag each hit. Remove or replace the reference (e.g., if skill A says "call removed-skill", flag for user review).

**New skill:**
- Read the new skill's workflow to find which skills it calls. Verify each called skill exists in the registry.
- Read the new skill's description for "Called by" context. Verify the caller skill actually references this new skill — add the reference if missing.

**Rewired skill (changed what it calls):**
- Diff the old and new call lists. For removed callees, check if the callee's "Called by" context needs updating. For added callees, verify the callee exists.

### Step 3 — Apply Fixes

For each stale or missing reference found in Step 2:
1. Read the target SKILL.md file.
2. Make the minimal edit — replace the old skill name with the new one, or add/remove a reference line.
3. Verify the edit is within allowed scope (cross-reference strings only).

### Step 4 — Validate Edits

Run `validate-skills` on every SKILL.md that was edited. If any skill drops below 10/14 after the edit, undo that edit and flag it for manual review.

### Step 5 — Report

Deliver the cross-link report (see Impact Report below).

### Step 5b — Reconcile knowledge graph

If `docs/knowledge-graph/graph.json` exists, run:
```bash
python3 .agents/skills/knowledge-graph/scripts/build_graph.py --incremental
```
Compare registry `calls[]` from Step 1 against `call-graph.json`. Flag invoke edges in registry missing from graph (stale graph) or graph edges with no SKILL.md backing (report only — graph may include SKILL-INDEX authoritative edges).

---

## Gotchas

- **Description text contains skill names as triggers** — e.g., "when agent-builder checks skill availability". These ARE cross-references and must be updated on rename.
- **Examples may contain skill names** — these are illustrative, not functional. Update them to avoid confusion, but don't flag them as broken references.
- **Frontmatter `sources` field** — skill names in sources are metadata, not cross-references. Leave them alone.
- **Don't create circular references** — if skill A calls B and B calls A, flag it instead of silently wiring it.

---

## Example

<examples>
  <example>
    <input>Skill `agent-architect` was renamed to `agent-builder`. Run cross-link repair.</input>
    <output>
Cross-link repair triggered by: rename (agent-architect → agent-builder)
Skills scanned: 35

Stale references found: 13
  process-decomposer/SKILL.md: 2 references → fixed
  setup-evaluation/SKILL.md: 4 references → fixed
  project-orchestrator/SKILL.md: 2 references → fixed
  create-agent-prompt/SKILL.md: 2 references → fixed
  skill-finder/SKILL.md: 1 reference → fixed
  tool-finder/SKILL.md: 1 reference → fixed
  ROUTING.md: 1 reference → fixed (not a SKILL.md, flagged for library-skill)

Validation: all 6 edited skills still ≥10/14 ✓
    </output>
  </example>
  <example>
    <input>New skill `cross-link-skills` was just created. Run cross-link repair.</input>
    <output>
Cross-link repair triggered by: new skill (cross-link-skills)
Skills scanned: 36

New skill calls: validate-skills
New skill called by: universal-skill-creator, improve-skills
  universal-skill-creator/SKILL.md: reference present ✓
  improve-skills/SKILL.md: reference present ✓

Stale references: 0
Missing references: 0
No edits needed.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skills are independent" | Orphan skills rot — callers need discoverable edges. |
| "INDEX is enough" | SKILL.md cross-links are what agents read at invoke time. |
| "Link everything" | Link only real invoke relationships, not keyword overlap. |
| "One pass is enough" | New skills need reciprocal Called-by updates. |
| "Graph replaces links" | Graph is derived; authoritative links live in SKILL.md + INDEX. |

## Verification

- [ ] New links reflect actual invoke paths (not aspirational)
- [ ] Reciprocal references updated where bidirectional
- [ ] No broken skill name references after edit
- [ ] SKILL-OUTPUTS.md logged if files changed

## Red Flags

- Description edited to remove skill names used as triggers
- Examples rewritten to break illustrative skill references
- Functional invoke links stripped from workflow steps
- Call graph updated without checking reverse references

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

```
Cross-link repair complete: YYYY-MM-DD
Trigger: [created | renamed | removed | rewired] — [skill name(s)]
Skills scanned: N
Stale references found: N
References fixed: N
References flagged for manual review: N
SKILL.md files edited: [list]
Validation: all edited skills ≥10/14 [✓ | list failures]
```
