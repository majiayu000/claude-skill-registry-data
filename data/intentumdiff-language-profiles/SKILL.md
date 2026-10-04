---
name: intentumdiff-language-profiles
description: >-
  The per-language diff-tuning layer that sits above the parser — how IntentumDiff decides, for
  each language, what counts as a stable identity key, what surfaces as a meaningful change, and
  what is scaffold noise to suppress. Use this whenever a diff is wrong for a specific language:
  a real change reported as noise (or vice versa), parameter/label "leakage", a changed
  entity suppressed, an anonymous-move false positive, or a bad label on a statement/command.
  It covers the profile families in `src/intentumdiff/analysis/*_profiles.py` (statement, keyed,
  resource, path, query, language/functional-entity) and how they feed matching + presentation
  grouping. Most of the repo's per-language test failures live here. Read intentumdiff-engine for
  the diff/grouping pipeline and intentumdiff-parsers for the grammar layer beneath this; new
  authoritative logic ultimately belongs in the Rust core.
---

# IntentumDiff — Language / statement / keyed profiles

Above the raw parser (which produces a `SemanticNode` tree) sits a **per-language tuning layer**
that tells the matcher and the presentation stage how to treat that language's node types. Get
this wrong and the *same* diff engine produces noise for one language and precision for another.
This is where most per-language quality bugs — and most of the repo's failing snippet/profile
tests — actually live.

> Boundary note: these profiles currently live in the Python `analysis/` test-oracle. New
> authoritative behavior belongs in the Rust core (see `intentumdiff-architecture`); use the
> Python profiles to reproduce, characterize, and pin behavior, and to decide the correct Rust
> fix. Changing a `.py` profile needs no maturin rebuild; the Rust equivalent does.

## The profile families — now Rust-authoritative

> **Migration status (#57 / #90 / #82):** the profile families were ported to the Rust
> core, which is now **authoritative** for profile-label enrichment — **there is no Python
> fallback** (readiness #90). Fix profile behavior in the Rust module; the deleted Python
> modules are gone, and the surviving Python ones are shrinking remnants, not the source of
> truth. Rust homes below.

| Family (langs) | Rust home (authoritative) | Python status |
|---|---|---|
| statement (asm, bash, delphi, …) | `crates/rust-core-host/src/statement_keys.rs`, `entity_anchors.rs` | **`statement_profiles.py` DELETED** (#91) |
| keyed data (json, yaml, …) — key-path match, `keyed_data_key` | `crates/rust-core-host/src/keyed_data.rs` | `keyed_profiles.py` retained only for guardrails' keyed identity helpers; its enricher is dead |
| path/segment (css, scss, html, xml, mdx) | `crates/rust-core-host/src/html_path.rs`, `xml_schema.rs` | **`path_profiles.py` DELETED** (#91) |
| query (sql dialects) | `crates/rust-core-host/src/sql_profile.rs` | **`query_profiles.py` DELETED** (#91) |
| resource (hcl/puppet) — identity by type + title | *pending port* | **`resource_profiles.py` — the last live Python enricher (#90 remaining sub-task)** |
| functional-entity / function-valued decl | in the Rust core (anchors/entity matching) | `language_profiles.py` catalogs |

Note: `RESOURCE_PROFILE_LANGUAGES` still includes `dockerfile`, but dockerfile keying is
Rust-served; only hcl/puppet still route through the Python resource enricher.

## The core tuning knobs (see `StatementProfile`)

A profile classifies a language's node types into three roles — this is the lever for almost
every per-language fix:

- **`keyed_node_types`** — the stable *identity* of a node (used to match old↔new). Wrong keys →
  false moves / renames, or a changed entity matched to the wrong sibling.
- **`review_node_types`** — node types that, when changed, are **meaningful** and should surface.
  Too narrow → a real change (e.g. a changed `FORM`) is dropped/suppressed as noise.
- **`scaffold_node_types`** — structural boilerplate to **suppress** (e.g. `program`,
  `compound_statement`, `command_name`). Too broad → real content leaks in as noise; too narrow
  → scaffold churn floods the diff.

Keyed/resource profiles instead expose a `*_key(node)` function (semantic key path / resource
type+title) and a `build_parent_map` so identity is content-based, not positional.

## How this maps to the failing tests (worked examples — `tests/unit/test_snippet_gap_regressions.py`, `test_profile_hardening.py`)

Each of these is a profile-tuning gap, not a generic engine bug:
- **bash** `greet "$NAME"` shows as an extra label → a `command`/argument node is keyed/reviewed
  when it should be scaffold, or the command label extraction is wrong.
- **delphi** `WriteLn(Multiply(2,3))` label missing / `Alpha`→`Alpha changed` MODIFICATION not
  scoped to its routine → statement keying/scoping in the Delphi profile.
- **abap** a changed `FORM` suppressed as stable noise → the form node type isn't in
  `review_node_types` (or is over-matched as stable).
- **dart / elixir** parameter additions (`identifier('x')`/`('y')`, `additive_expression('name')`)
  leak as ADD/DELETE → params/body scaffold not suppressed; anchor on the signature.
- **perl** named subroutines reported as anonymous moves → identity key doesn't capture the sub
  name, so the matcher treats them as anonymous.
- **puppet** resource titles/parameters not used as identity → resource profile key.

Fix pattern: reproduce with the real engine, inspect the node types the parser emits for the
snippet, then adjust the language's profile (keyed vs review vs scaffold, or the key function) so
identity and meaningfulness match human intent. Add/adjust the fixture and re-run.

## Reproduce & verify

```python
from intentumdiff.differ import SemanticDiffer
diff = SemanticDiffer().diff_strings(old, new, "x.sh", language_hint="bash")
for c in diff.changes: print(c.change_type, (c.new_node or c.old_node).node_type, c.description)
for g in diff.change_groups: print(g.kind, g.metadata.get("reason"))
```
Inspect the actual `node_type`s the parser emits (that's the vocabulary your profile must
classify), then tune. `tests/unit/test_snippet_gap_regressions.py` and `test_profile_hardening.py`
pin per-language behavior; keep them green. Many are currently red — see
`docs/BACKLOG.md` "Known pre-existing test failures". Fixing them authoritatively means the Rust
core's equivalent per-language handling, with the Python profile as the parity oracle.
