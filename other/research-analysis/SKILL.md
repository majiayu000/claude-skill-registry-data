---
name: research-analysis
description: "Use when initializing, adding, updating, deleting, or linting a package's state-backed Analysis view, or when distilling an evidence-backed insight into a package Rule."
argument-hint: "<subcommand: init | add-insight | add-rule | lint> [args]"
allowed-tools: Bash(python *), Read, Grep, Glob
---

# research-analysis

## Purpose

`/research-analysis` manages the records behind a package's existing Analysis page. It owns two
editorial decisions:

1. whether an experimental result supports a mechanism-level Insight;
2. whether that Insight warrants a reusable package Rule.

The records live in unified research state. The browser page under `.research/interface/` is a
derived view and must never become a store.

## Authority and storage

Authority runs in this order:

1. the user's request and explicit payload;
2. the management schema and EventStore policy;
3. the trust and interface rules shipped by `/research-dashboard`;
4. this skill's editorial contract.

The relevant data is:

| Concept | Authoritative representation |
| --- | --- |
| Analysis enabled | `Package.pages[]` contains `"analysis"` |
| Insight | `Learning` aggregate `<pkg>::learning::<insight-id>`, plus the package's `analysisInsights[]` projection fields |
| Package Rule | `Rule` aggregate `<pkg>#<slug>` with `level=package`, `kind=lesson` |
| Evidence | `provenance` and any typed evidence reference recorded with the Learning or Rule |
| Human view | `.research/interface/packages/<package-slug>/analysis.html`, rebuilt by `lib.interface` |

All mutations use `skills/research-op/scripts/research_op.py`, except `init`, whose small helper commits
the package page-selection event through the same management layer. Do not edit
`.research/state/events.jsonl`, `.research/state/current.json`, or anything below
`.research/interface/`.

## Boundary

- `results.html` answers what happened. Its rows come from verified run results.
- Analysis answers why it happened and what should be remembered.
- Insights and Rules require an explicit editorial decision. Fact propagation does not create them.
- An Insight is a non-binding Learning. A Rule is binding package memory and needs stronger evidence.
- A package Rule is not a `methodsTried` verdict row. The two records answer different questions.
- Terminal packages are frozen. If `research-op` rejects a mutation, surface the rejection instead of
  patching the rendered page.

## Preflight

Confirm that the versioned research root and target Package exist:

```bash
test -f .research/VERSION
python skills/research-op/scripts/research_op.py \
  show package <package-id> --workspace .
```

If the Package is missing, use `/research-package`. If the workspace is legacy
or unversioned, stop; automatic migration is unsupported. The generated
interface is not an execution prerequisite.

## Operations

### `init <package-id>`

New Packages include Analysis in their standard page set. Use `init` only to
repair an older Package whose state-backed `pages[]` omitted it:

```bash
python skills/research-analysis/scripts/init_analysis_page.py \
  --workspace . \
  --package-id <package-id>
```

The command appends `"analysis"` to `Package.pages[]` through a
`PackageMutationApplied` event. It is idempotent and marks the interface stale;
the Dashboard or next static-page request rebuilds the projection.

### `add-insight <package-id> <insight-id>`

Record one evidence-backed Insight through the `analysis-insight` facade:

```bash
python skills/research-op/scripts/research_op.py \
  --workspace . \
  --pkg <package-id> \
  --op insert \
  --target analysis-insight \
  --payload '{
    "id":"<kebab-case-id>",
    "title":"<short title>",
    "lead":"<observed pattern>",
    "reading":"<what the evidence shows>",
    "mechanism":"<why it happened>",
    "provenance":".research/experiments/<pkg>/<experiment>/<run>/result.json"
  }'
```

Required fields:

- `id` or `slug`;
- `title`;
- at least one of `lead`, `reading`, or `mechanism`;
- `provenance` that identifies the evidence.

The gateway records a `Learning` and updates the package's renderer-facing `analysisInsights[]`
fields in the same operation. Use `--op update` with the same stable `id` to revise it. Use
`--op delete` with `{"id":"<id>","reason":"<why>"}` for an explicit correction.

The interface renders each Insight as a closed `<details>` block. Text fields are HTML-escaped.
Raw HTML is not part of the current Insight payload contract.

### `add-rule <package-id> <slug>`

Distill an existing Insight into a package Rule only when finalized result evidence supports a
general lesson:

```bash
python skills/research-op/scripts/research_op.py \
  --workspace . \
  --pkg <package-id> \
  --op insert \
  --target rule \
  --payload '{
    "level":"package",
    "kind":"lesson",
    "slug":"<kebab-case-slug>",
    "title":"<short title>",
    "text":"<standalone rule prose>",
    "rationale":"insight-<insight-id>",
    "addedAt":"<YYYY-MM-DD>"
  }'
```

The Rule text must stand on its own and remain plain text. Put thresholds, named subjects, and other
binding details in `text`; put the supporting Insight id in `rationale`. `research-op` rejects a
lesson when the package has no finalized result evidence.

### `lint <package-id-or-all>`

Lint the authoritative state:

```bash
python skills/research-analysis/scripts/lint_analysis.py \
  --workspace . \
  --package-id <package-id>

python skills/research-analysis/scripts/lint_analysis.py \
  --workspace . \
  --all
```

The linter checks:

- Analysis is enabled in `Package.pages[]`;
- Insight ids are unique kebab-case ids;
- every Insight has a title, content, and provenance;
- active lesson Rules contain plain text;
- each lesson Rule cites an Insight that exists for the package.

It does not parse or mutate rendered HTML.

## Human layout contract

The current Analysis page keeps the existing human layout:

1. Rules appear first as a numbered list.
2. Insights follow as closed, collapsible cards.
3. The interface renderer supplies the empty placeholders.
4. The package navigation and shared CSS remain owned by `/research-dashboard` and
   `lib.interface`.

`skills/research-package/templates/analysis.html` is the single layout template. This skill does not
carry or write a second page template.

## Visualization boundary

[references/viz-templates.md](references/viz-templates.md) records the approved visual language for a
future typed visualization field. The current `analysis-insight` facade accepts text fields and does
not render arbitrary HTML. Do not paste a visualization into `.research/interface/` or smuggle raw
HTML into state. Until the schema and renderer gain a typed visualization payload, place the finding
in `reading` and `mechanism`, with the result artifact in `provenance`.

## Inspection

Inspect the stored records through bounded queries:

```bash
python skills/research-op/scripts/research_op.py \
  show learning '<package-id>::learning::<insight-id>' --workspace .

python skills/research-op/scripts/research_op.py \
  show rule '<package-id>#<rule-slug>' --workspace .
```

After any accepted mutation, confirm that the automatic interface rebuild
succeeded, then run the state linter. A clean lint is silent and exits with
status 0.

## Final response

Report:

- the operation and package id;
- the committed event ids;
- the Learning or Rule aggregate id;
- the lint result;
- whether the interface rebuild succeeded;
- the next decision, if one remains.

## Bundled resources

- `scripts/init_analysis_page.py`: enables Analysis in Package state.
- `scripts/lint_analysis.py`: validates the state contract.
- `templates/rule-bullet.html`: package Rule payload reminder.
- `references/viz-templates.md`: frozen visualization layout reference, not a mutation path.
