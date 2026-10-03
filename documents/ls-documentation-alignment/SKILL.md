---
name: ls-documentation-alignment
description: "Run automated repo documentation alignment: discover source truth, audit public/internal docs, refresh generated artifacts, coordinate subagent research, and verify docs in one pass."
metadata:
  version: "1.1"
compatibility: "Python 3.12+, PyYAML, LocalSetup docs_alignment.py adapter. Generic workflow with LocalSetup source-truth defaults."
---

# Documentation alignment

Use this skill when a repo needs documentation brought back into alignment with the code, manifests, CLI commands, assets, generated docs, and current external documentation standards.

## Purpose

- Discover source-of-truth surfaces before editing docs.
- Use subagents for independent repo scouting and current external research when the task is broad.
- Generate a stable inventory, truth map, audit result, asset manifest, and summary.
- Fix supported stale facts in public docs without hand-maintaining volatile counts.
- Keep generated docs owned by the repo generator instead of ad hoc edits.
- Record public-doc ownership through `owner_skill` or `owner_package` frontmatter and fail CI for active framework docs without an owner.
- Leave a reproducible validation trail for future runs.

## Generic workflow

1. Create or resume a run ledger under `.agents/state/<task-slug>/ledger.md`; the controller assigns one Git-bound task slug for every agent and tool to reuse.
2. Inventory the repo: public docs, internal docs, generated docs, skills/workflows, assets, CLI commands, CI, and lifecycle metadata.
3. Map truth sources. For LocalSetup, defaults are `VERSION`, `pyproject.toml`, `ls/config/*.yaml`, `ls/skills/*/SKILL.md`, `ls/workflows/*/workflow.yaml`, generated facts, assets, and CI workflows.
4. Delegate scouts when scope is broad:
   - code truth and generator ownership
   - public docs and stale claims
   - internal/generated docs and lifecycle rules
   - current external documentation standards
   - assets and CI gates
   - skill/workflow package conventions
5. Run the alignment audit and plan. Treat subagent reports as evidence, not completion.
6. Apply generated and supported public fixes. Keep manual-review findings explicit.
7. Regenerate docs artifacts and run validation.
8. Run a final read-only review before claiming completion.

## Commands

Inventory:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . inventory
```

Audit:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . audit
```

Plan:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . plan
```

Apply generated artifacts:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . apply --scope generated
```

Apply supported public-doc fixes:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . apply --scope public
```

Dry-run any write scope:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . apply --scope all --dry-run
```

CI/read-only check:

```bash
uv run --locked python ls/tools/docs_alignment.py --repo-root . check --ci
```

LocalSetup wrapper:

```bash
uv run --locked python ls/tools/localsetup.py --source-root . docs-align check --ci
```

## Outputs

### Release preparation

In the LocalSetup source repository, `localsetup release-docs plan` resolves the
upcoming version and inventories tracked active public documents. `prepare
--verify-baseline --candidate .agents/state/<task-slug>/candidate.json` produces
a scoped model proposal and independent review without applying it. Model authoring is optional. When selected, the protected QC runtime must be
available and an incomplete model proposal cannot be applied. A reviewed source
record with deterministic rendering remains the ordinary fallback; a provider
failure does not block that path.
`apply --candidate ...` is the explicit local write step; `render` updates managed
sections from an existing record. Use `check` after
canonical version/document synchronization and `notes` to render release prose.

Versioned records under `ls/docs/releases/` own the managed `release-summary` and
`release-link` blocks and their matching guides. Edit the record or its owning
generator, not rendered blocks. Preserve historical guides. Semantic review must
cover release claims and complete commands, including required checksum and SBOM
sidecars; a zero-finding static audit alone does not establish semantic accuracy.
Git-backed public inventories exclude untracked files and private state.

Generated artifacts live under `ls/docs/_generated/`:

- `docs-inventory.json`
- `docs-truth-map.json`
- `docs-audit-result.json`
- `docs-asset-manifest.json`
- `docs-alignment-summary.md`

Asset provenance and reference notes live in `assets/README.md` when the asset scope is applied.

## Audit model

The tool reports JSON-first findings for:

- version and generated-facts drift
- stale generated skill taxonomy
- stale skill/workflow counts
- missing lifecycle frontmatter in framework docs
- missing or invalid active-doc ownership frontmatter
- broken relative links and missing image files
- missing image alt text
- unclosed fenced code blocks
- missing managed generated facts blocks

Critical and major findings fail `check --ci`.

## Subagent pattern

For a generic repo, assign scouts before edits:

- `explorer`: map code truth, docs ownership, CI, and assets
- `researcher`: verify current external standards from primary sources
- `worker`: implement bounded fixes after controller verification
- `tester`: run validation commands and summarize failures
- `reviewer`: final read-only review against the run ledger

The controller verifies each report and records checkpoints in the ledger.

## References

- `ls/tools/docs_alignment.py`
- `ls/docs/_generated/docs-alignment-summary.md`
- `ls/docs/OUTPUT_AND_DOC_GENERATION.md`
- `ls/docs/DOCUMENT_LIFECYCLE_MANAGEMENT.md`
- `ls/docs/WORKFLOW_STANDARD.md`

## Documentation Skill Refresh Note

Classification: route docs drift, generated artifact sync, and public documentation alignment here rather than creating a duplicate generic documentation skill.

### Command inventory boundary

The generated inventory's cli_commands lists root `localsetup` command families
from the canonical ls/core/cli_parser.py builder. Collection parses declarations
without importing or executing the target source. Missing, malformed, empty or
nonliteral root declarations fail collection and require an owner update; they
must not silently produce an empty command inventory. A regression check compares
the collected names with the actual argparse root choices.

This field does not enumerate nested subcommands, options, delegated LSCli
commands or their behavior. Audit those against their owning parsers and command
references during comprehensive documentation alignment. A zero-finding report
is not proof that every command contract or current documentation claim is covered.
