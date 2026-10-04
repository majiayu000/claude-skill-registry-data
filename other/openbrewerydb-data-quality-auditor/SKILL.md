---
name: openbrewerydb-data-quality-auditor
description: Audit OpenBreweryDB source CSV data quality and prepare issue-ready findings. Use when asked to inspect the openbrewerydb/openbrewerydb dataset for structural, identity, completeness, geospatial, or brewery-status problems without changing dataset files.
---

# OpenBreweryDB Data Quality Auditor

Perform read-only audits of the source CSVs in a local `openbrewerydb/openbrewerydb` checkout. Produce an issue-ready report by default; never fix records, open implementation PRs, or write in the dataset repository.

## Non-negotiable boundaries

- Treat the dataset checkout as read-only. Do not create reports, temporary files, branches, commits, or any other files inside it.
- Never edit CSVs or generated artifacts. Report proposed corrections rather than applying them.
- Never run `npm`, `npm install`, an npm script, another package manager's equivalent, or an upstream script implementation. Do not reproduce an upstream mutating workflow.
- Use only read-only inspection commands and the bundled stdlib helper. Put any explicitly requested saved output outside the dataset checkout.
- Do not open an issue or pull request and do not implement a fix. The deliverable is Markdown ready for the user or maintainer to paste into an issue.

## Workflow

1. Ask for the local dataset root if it is unknown. Confirm it contains `data/`; do not modify or sync the checkout.
2. Select one or more modes: `structural`, `identity`, `completeness`, `geospatial`, or `status`. Read `references/audit-checks.md` for definitions and triage rules.
3. Run the helper from this skill directory, with the dataset path as an argument. It reads the live brewery type enum from `src/config.ts` as text without executing upstream code. Markdown is the issue-ready default:

   ```bash
   python3 scripts/audit_dataset.py /path/to/openbrewerydb --mode structural --mode identity
   python3 scripts/audit_dataset.py /path/to/openbrewerydb --format json
   ```

   With no `--mode`, all modes run. The helper reads `data/**/*.csv` recursively and writes only to stdout.
4. Review findings against the live CSV rows. Do not claim an automatic heuristic is a confirmed defect. Group related rows and retain file, row, ID, severity, and confidence.
5. For status findings, follow `references/status-verification.md`. Status is not established by CSV values alone and requires current external evidence.
6. Before finalizing each issue candidate, search open issues and pull requests in `openbrewerydb/openbrewerydb` for the ID, brewery name, source file, and defect type. Use read-only GitHub access, for example:

   ```bash
   gh issue list --repo openbrewerydb/openbrewerydb --state open --search '"<brewery name>" OR "<id>"' --limit 100
   gh pr list --repo openbrewerydb/openbrewerydb --state open --search '"<brewery name>" OR "<id>"' --limit 100
   ```

   Inspect plausible matches with `gh issue view` or `gh pr view`. If `gh` is unavailable, use GitHub web search and disclose the limitation if neither can be used. Link related items and mark duplicates or already-addressed findings rather than proposing a new issue.
7. Format the result with `references/issue-report-template.md`. Include scope, commands/modes, evidence, affected rows, related open issues/PRs, and a non-mutating suggested resolution. Separate confirmed defects from items needing maintainer review.

## Reporting rules

- Prefer a small, evidence-backed issue over a bulk dump of weak signals.
- Use source-relative paths and one-based physical CSV row numbers.
- Treat missing IDs as review items because pending contributor rows may intentionally lack IDs.
- Never infer that `(0, 0)`, a duplicate-looking identity, or an old web listing is conclusively wrong without corroboration.
- State that no dataset files were changed and no npm or upstream implementation was run.

## References

- Audit definitions and severity guidance: `references/audit-checks.md`
- Issue-ready output structure: `references/issue-report-template.md`
- Status evidence and conflict handling: `references/status-verification.md`
