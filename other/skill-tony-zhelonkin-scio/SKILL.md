---
# =============================================================================
# CANONICAL SKILL FRONTMATTER (Scio toolkit conventions)
# =============================================================================
# Allowed top-level keys (Claude Code / Desktop skill loader schema):
#   name, description, license, allowed-tools
# Any other top-level key fails the validator. Cross-references and caveats go
# in the body, not the frontmatter: `## Prerequisites`, `## When not to use`,
# `## See also`.
#
# Validate with:
#   python skills/skill-creator/scripts/quick_validate.py skills/<this-skill>/
#
# NOTE: `name` below is the placeholder `SKILL_IDENTIFIER`. The validator WILL
# fail on this until you rename the skill — that is intentional (it forces you
# to pick a real kebab-case name). Every other field should already validate.
# =============================================================================

name: SKILL_IDENTIFIER
# ^ kebab-case, matches the directory name exactly. Pattern: ^[a-z0-9-]+$
#   Examples: `scvi-basic`, `pycistopic-atac-topic-modeling`, `anndata`

description: "[Tool or method name] — [one-line function, dash-joined]. Use when [specific trigger condition, e.g. a data type, a user phrase, a workflow stage]. For [adjacent case] use [other-skill-name]."
# ^ The SINGLE most important field. It's the only thing the model sees during
#   skill selection. Conventions from audited library:
#     - Start with the TOOL or METHOD NAME (scanpy, SCENIC+, scVI, MrVI, ...)
#     - Follow with an em-dash and a one-line function summary
#     - Give a concrete "Use when" trigger — specific, not generic
#     - Give 1-2 "For X use other-skill" pointers (disambiguates from siblings)
#     - 2-4 sentences, ≤350 chars (`scio lint --check toolkit` enforces the cap),
#       including the trigger keywords that should activate it
#     - NO angle brackets `<` `>` anywhere (validator rejects them — use square
#       brackets `[...]` for placeholders above, or just write plain prose)
#     - If the text contains a raw colon, wrap the whole string in double quotes
#       OR use a YAML block scalar (`description: |`)

license: MIT
---

# [Skill Title — Human-Readable, Not Kebab-Case]

## Overview

Two to four sentences answering: what problem does this skill solve, who needs it, and what is the headline differentiator from adjacent skills. Keep it scannable — this is the first thing a reader sees after the frontmatter.

**When to use this skill:**
- [Concrete trigger 1 — e.g. a specific data type, pipeline stage, or user intent]
- [Concrete trigger 2]
- [Concrete trigger 3]

**When NOT to use this skill:**
- [Anti-case 1] → use `other-skill.md`
- [Anti-case 2] → use `other-skill.md`

---

## Decision Tree

```
Faced with [situation]?
│
├─ [Condition A]  →  use this skill
├─ [Condition B]  →  use alternative-skill
└─ [Condition C]  →  no skill needed, write ad-hoc code
```

*Decision tree is OPTIONAL for `tier: simple`, REQUIRED for `standard` and `rich`.*

---

## Quick Start

Minimal working example — the shortest path to a visible, verifiable result.

```python
# 5-15 lines. Imports, load data, one or two core calls, a print/plot.
import <library>

result = <library>.do_the_thing(input_data)
print(result.shape)   # or similar observable
```

**Verify it worked:**

```python
# Assertions that catch the most common failure modes.
# Prefer observable properties (shape, dtype, obs/var keys, plot appears)
# over silent "it didn't error".
assert result.shape[0] > 0, "Empty output — check input filtering"
assert "expected_key" in result.obs.columns, "Missing expected annotation"
```

---

## Progressive Depth

*This three-level structure is REQUIRED for `standard` and `rich` tiers; `simple` tier can use a flat "Basic Usage" section instead.*

### Basic Usage

Core functionality covering ~80% of real use. Sensible defaults. Plain code, no parameter tuning — just what the typical user needs to get a reasonable result.

### Intermediate Usage

Parameter tuning, alternative approaches, performance considerations. Cross-reference `references/<topic>.md` for deep treatments rather than inlining them here.

### Advanced Usage

Edge cases, customization, integration with other tools. Point to `references/<topic>.md` and `scripts/<helper>.py` rather than duplicating long content in SKILL.md.

---

## Verification Checklist

After running this skill, confirm:

- [ ] **Observable check:** [a concrete assertion, e.g. "`adata.obsm['X_latent']` has shape `(n_obs, n_latent)`"]
- [ ] **Biological plausibility:** [a domain-specific check, e.g. "known marker genes separate expected cell types in UMAP"]
- [ ] **Output integrity:** [a structural check, e.g. "no NaNs in the latent representation"]

For automated verification: `python checks/check_<thing>.py` *(rich tier only)*

---

## Common Pitfalls

### Pitfall: [Short, memorable name]

- **Symptom:** What the user sees when this goes wrong (error message, weird plot, silent corruption).
- **Cause:** The underlying reason — usually an assumption the user didn't know was being made.
- **Fix:** Concrete code or action that resolves it.

### Pitfall: [Next one]

- **Symptom:** ...
- **Cause:** ...
- **Fix:** ...

*Aim for 3-6 pitfalls covering the most-hit real-world failures. Tabular form is also acceptable when the fix fits in one cell — see `chromvar-motif-accessibility` for an example.*

---

## Resources

- **Docs:** https://example.org/docs
- **Paper / tutorial:** https://example.org/tutorial
- **Repository:** https://github.com/org/repo

*Prefer primary sources (official docs, original papers). Avoid link rot — don't cite blog posts unless authoritative.*

---

## When not to use

- Do not use for [case]. Use [other-skill] instead.
- Do not use on [data condition, e.g. log-normalized counts]. [Preferred tool or preprocessing step] is required.

---

## See also

Each entry is `` - `skill-name` — Relationship; purpose ``: a short relationship
label (`Prerequisite`, `Next step`, `Alternative`, `Downstream consumer`,
`Sibling convention`, ... — pick the word that names the *edge*, not the
target's job) followed by a semicolon and one clause saying what the target
skill actually does for/against this one. Don't let the purpose clause just
restate the relationship word (e.g. avoid `Voter; voter for X` — say what
kind of vote). Keep it to one line per entry.

- `related-skill-a` — Prerequisite; produces the input this skill consumes
- `related-skill-b` — Next step; consumes this skill's output for [task]
- `related-skill-c` — Alternative; use instead when [condition]
- `related-skill-d` — Sibling convention; shares [contract/house style] with this skill
