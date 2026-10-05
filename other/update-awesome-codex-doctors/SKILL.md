---
name: update-awesome-codex-doctors
description: Add, refresh, reclassify, or retire entries in the Awesome Codex Doctors catalog and leave a verified, merge-ready repository change. Use for catalog maintenance and contribution preparation, not for diagnosing the user's local Codex installation.
---

# Update Awesome Codex Doctors

Maintain the catalog as reviewed data, not an automatically accepted search dump.

## Establish the change

Identify whether the request adds a project, refreshes metadata, changes classification, marks a project archived, or removes a false positive. Do not mix unrelated repository cleanup into the contribution.

Find the repository root containing `data/github-snapshot.json`, `METHODOLOGY.md`, and `scripts/render.py`. When invoked from this repository, the root is two directories above this skill folder.

Before editing, read:

- `METHODOLOGY.md` for scope and chart rules;
- `CONTRIBUTING.md` for evidence and safety requirements;
- `data/github-snapshot.json` and `CATALOG.md` for duplicates;
- [references/catalog-schema.md](references/catalog-schema.md) for field semantics.

## Search local data before the web

Normalize the candidate repository as `owner/name`. Search the snapshot and catalog for its full name, URL, renamed repository, fork, mirror, and closely overlapping project. Update an existing record instead of adding a duplicate.

Only then inspect current external evidence:

1. Open the GitHub repository and its README; do not rely on a search snippet.
2. Verify that it addresses OpenAI Codex rather than a medical app built with Codex or a match caused by the owner's username.
3. Verify purpose, platform, delivery form, read-only/repair/cleanup behavior, files touched, backup or dry-run claims, license, releases, archived state, creation time, and recent activity.
4. For claims about official Codex behavior, use current official OpenAI documentation or the `openai/codex` source/release that supports the claim.
5. Record uncertainty instead of guessing. Use `unverified` only when the candidate is plausibly relevant and retaining it helps future review.

External metadata changes quickly. Refresh it from GitHub during the contribution rather than copying stale values from an older table.

For a structured refresh pass, run `python scripts/discover.py` to produce `data/discovery-candidates.json` and review that candidate list before editing the snapshot.

## Edit the source of truth

Edit `data/github-snapshot.json`; do not hand-edit generated catalog rows or the SVG curve.

- Preserve the existing JSON field names and chronological project ordering.
- Update `generated_at` to the actual snapshot date.
- Recompute `counts` from the project records.
- Keep manual classifications (`scope`, `specialty`, `skill_or_plugin`) evidence-based.
- Set `state_change_risk`, `dry_run_support`, `backup_support`, and `evidence_count` from evidence, using `unknown` when unresolved.
- Write both `description` and `description_zh` as concise, factual answers to “What does this one do?” Distinguish similarly named Doctors by their concrete problem surface, platform, or delivery form; do not copy promotional prose or repeat generic wording.
- Do not remove a project solely because a transient network check fails.

The chart is a discovery curve based on repository `created_at`, not popularity. Never alter dates or classifications to make the curve look stronger.

## Generate and verify

From the repository root:

```bash
python scripts/discover.py
python scripts/render.py
python skills/update-awesome-codex-doctors/scripts/audit_catalog.py .
git diff --check
```

The audit checks schema, counts, uniqueness, repository URL consistency, timestamps, risk/confidence fields, and generated files. Resolve failures rather than bypassing them.

Review the final diff. It should normally contain the source snapshot plus generated `README.md`, `README.zh-CN.md`, `CATALOG.md`, `data/catalog.json`, and `assets/community-growth.svg`; include methodology changes only when the contribution changes policy or headline counts.

## Leave a merge-ready result

Summarize:

- projects added, updated, reclassified, archived, or removed;
- sources opened and any remaining uncertainty;
- safety-relevant findings;
- validation commands and results;
- the files changed.

Do not commit, push, open a pull request, merge, or alter repository settings unless the user explicitly requests that external action. When requested, use the user's existing Git identity and repository conventions; do not invent credentials or authorship.
