---
name: changelog
description: Create or update user-facing changelog entries, or set up GitHub Actions to generate PR changelog entries.
disable-model-invocation: true
---

# Changelog

Use when explicitly asked to create or update a changelog, assess whether a change deserves an entry, or set up changelog automation in a repository.

For entry work, follow this file. Read [GitHub Actions setup](references/github-actions.md) only when asked to create or change the automation. An entry request does not authorize installing a workflow, publishing a release, pushing commits, or changing repository settings.

## Establish the repository contract

Inspect the repository instructions, existing changelog entries, contribution and release guidance, and any generator or fragment consumer. Reuse the existing location, format, categories, ordering, language, and validation command. Edit source fragments rather than generated output when a generator owns the changelog.

Identify the intended audience. For a library or developer tool, public API and CLI consumers are users; contributor-only implementation work is not automatically user-facing.

Resolve the requested scope from the conversation and repository state: a PR, branch diff, commit range, local changes, or release. For a PR, read its title, body, labels, and complete diff against the base. Use `gh` when available. For local work, include the relevant staged, unstaged, and untracked files without disturbing unrelated edits. Do not invent a comparison base, release version, date, or PR number when that information is required but unavailable.

For a create or update request, if no changelog Markdown file exists, create `CHANGELOG.md` at the repository's documented location, or at the repository root when none is documented. Reuse an existing `changelog.md` or other filename casing rather than creating a duplicate. If a generator owns the file, create it through that generator. An assessment-only request does not authorize file creation.

When there is no existing format, initialize the file with an `Unreleased` section and only the categories needed from Added, Changed, Deprecated, Removed, Fixed, and Security. If no entry qualifies, leave `Unreleased` empty rather than inventing content. Do not introduce a generator dependency for a single entry. If the repository needs a release or fragment policy beyond this default, settle that choice before wiring automation.

## Decide whether an entry belongs

Default to no entry unless the evidence supports a concrete change for the intended audience. Read the authoritative feature-gate definitions and affected call paths when release availability is relevant. A flag name, default value, or PR title alone does not establish who can use a feature.

Skip work that only changes:

- Tests, CI, builds, internal tooling, or contributor documentation.
- Implementation structure, naming, or types without observable behavior changes.
- Dependencies without an identified user-visible effect.
- Staff-only, developer-only, disabled, or otherwise unreleased behavior.
- Preparatory infrastructure that no released user-facing path reaches.

A newly introduced flag is not evidence of a shipped feature. Conversely, an existing gate does not disqualify a change available to the intended users. For mixed PRs, describe only the eligible public behavior. Customer documentation corrections, public API type fixes, and dependency fixes can qualify when their user impact is established.

If availability or impact remains uncertain, skip the speculative entry and state the uncertainty. If required evidence could not be retrieved, report that blocker rather than treating a failed lookup as proof that no entry is needed. Honor the repository's explicit skip labels.

## Write or update

Describe what users can now do, what behaves differently, or what failure is fixed. Prefer a short, concrete sentence over an implementation summary. Include breaking changes and migration actions when supported by the diff.

Do not expose internal codenames, flag names, staff/dev surfaces, or unreleased plans. If an entry only makes sense when those details are included, reconsider whether it belongs. Follow any security disclosure policy; a changelog request does not authorize disclosing an embargoed vulnerability.

Search the relevant unreleased section or PR fragments before adding an entry. Update an existing entry about the same change rather than duplicating it, preserving deliberate human wording and unrelated entries. Do not delete a human entry merely because the automated criteria would skip it; flag the discrepancy. Do not rewrite released history unless the user requested that correction.

Use the repository's fragment schema when present. For the optional JSON convention described in the automation reference, a PR fragment is `changelog/unpublished/<PR_NUMBER>.json` with exactly these fields:

```json
{
  "type": "fixed",
  "description": "Keep the selected file visible after refreshing the file list."
}
```

Allowed types for this convention are `added`, `changed`, `fixed`, and `removed`. Do not impose this schema on an existing changelog system. Without a PR number, use the repository's local-fragment naming convention or the Markdown default, not a fabricated number.

## Finish

Run the existing changelog validator or generator checks when available. Otherwise, check the changed entries for format, category, duplicate coverage, and support in the diff. For JSON, parse it and validate its exact schema; successful parsing alone is insufficient.

Finish with the entry and location, or the reason for skipping or being blocked. Distinguish an unpublished entry from a published release. For automation work, use the reference's completion criteria.
