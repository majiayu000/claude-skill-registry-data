---
name: release-notes
description: Generates human release notes between two versions by reading full git commit context and enriching it with external sources such as Jira issues or GitHub PRs. Use when asked for changelog or release notes between versions/tags.
compatibility: Cursor-compatible Agent Skill. Requires git and python3. Network access is needed only when external data sources are used.
---

# Release Notes

## Purpose

Generate polished, human-readable release notes between two versions using full git history and optional external metadata sources.

Default behavior:

- Balanced tone (not too short, not too verbose)
- Include tracked (ticket/PR-linked) and untracked commits
- Never skip meaningful PR-linked changes just because Jira metadata is missing
- Output sections: Features, Bugfixes, Internal Improvements
- Prefix each bullet with short source links when available (Jira/PR)
- Return text unless file editing is explicitly requested
- Read full commit context (subject, body), not just one-line commit messages

## Inputs

- End version/tag (required, example: `11.29.0`)
- Start version/tag (optional, example: `11.28.2`)
  - If omitted, resolve previous version automatically from git refs.
- Optional external source credentials (only for enabled sources):
  - `ATLASSIAN_BASE_URL` (example: `https://company.atlassian.net`)
  - `EMAIL`
  - optional: `JIRA_TOKEN`
  - optional: `GITHUB_TOKEN`
  - stored in `.agents/skills/release-notes/release-notes-secrets.env`

## Workflow

1. Resolve refs for range

- Prefer explicit refs like `versions/web-app/<version>`.
- Verify end ref exists.
- If start version is not provided, infer it semantically:
  - Enumerate refs/tags in the same release stream as the end ref (for example `git tag -l "versions/web-app/*"`).
  - Parse semantic versions and pick the nearest lower version than the end version.
  - Use that as the start ref.
  - If no lower version exists, fail with a clear message asking for explicit start version.
- Verify inferred/provided start ref exists.

2. Read commit history with full context

- Use `scripts/collect_commit_context.py` to collect:
  - subject
  - full body
  - `jira_keys` extracted from each commit message
- Keep:
  - tracked commits (contain issue/PR identifiers)
  - untracked commits (no external identifier)

3. Enrich from external sources (optional, source-specific)

- Jira source is currently implemented:
  - `scripts/sources/fetch_jira_issues.py`
  - Input: commit JSON from `collect_commit_context.py`
  - Output: same commit list with `jira_issues` metadata per commit
  - If `JIRA_TOKEN` is missing, script returns input commits unchanged (with empty `jira_issues`)
  - If `JIRA_TOKEN` is set, requires `ATLASSIAN_BASE_URL` and `EMAIL`
  - Resolves `CLOUD_ID` from `ATLASSIAN_BASE_URL`
- GitHub PR source is implemented:
  - `scripts/sources/fetch_github_prs.py`
  - Input: commit JSON from `collect_commit_context.py` (or Jira-enriched JSON)
  - Output: same commit list with `github_pr` metadata per commit (`title`, `description`, etc.)
  - If `GITHUB_TOKEN` is missing, script returns input commits unchanged (with `github_pr=null`)
- Continue even when some source lookups fail; note missing metadata.

4. Categorize changes

- Source metadata indicates bug fix -> Bugfixes
- Source metadata indicates feature/story/epic -> Features (unless clearly internal-only)
- Tooling/refactor/infrastructure/convention work -> Internal improvements
- PR-linked commits without Jira:
  - still include if they have meaningful product or engineering impact
  - classify from PR title/description/branch context (do not drop due to missing Jira)
- Untracked commits:
  - `fix/*` or `bugfix/*` patterns usually Bugfixes
  - `feature/*` patterns usually Features unless tooling-only
  - formatting/conventions/test infra/refactors usually Internal improvements

5. Write notes in human language

- Do not just copy issue/PR titles.
- Use descriptions when available to capture intent and impact.
- Group related items into themes.
- Keep user-facing impact first, technical detail second.
- Add short drill-down links at the beginning of each bullet when available:
  - Prefer `[Jira: PZ-12345](...)` for Jira-tracked work
  - Prefer `[PR #1234](...)` for GitHub PR context
  - If both are available, include both, with Jira first
  - If Jira is unavailable but PR exists, include PR-only link and keep the item
  - Keep links compact and at the very start of the bullet so they are easy to remove

## Output Format

```markdown
# Release Notes <toVersion>

## Features

- [Jira: PZ-12345](https://.../browse/PZ-12345) [PR #1234](https://github.com/<owner>/<repo>/pull/1234) Add support for ....
- [PR #1231](https://github.com/<owner>/<repo>/pull/1231) Improve ....

## Fixed Bugs

- [Jira: PZ-12000](https://.../browse/PZ-12000) Fix ....

## Internal Improvements

- [PR #1204](https://github.com/<owner>/<repo>/pull/1204) Refactor ....
```

## Quality Bar

- Keep claims grounded in commit and source evidence.
- Prefer full commit context over branch-name guesses.
- Mention uncertainty when classification is ambiguous.
- Keep secrets out of outputs (never print tokens).
- Prefer concise, outcome-focused wording.

## References

- Workflow examples: [references/examples.md](references/examples.md)
- Jira auth troubleshooting: [references/jira-troubleshooting.md](references/jira-troubleshooting.md)
- Scripts:
  - `scripts/collect_commit_context.py`
  - `scripts/sources/fetch_jira_issues.py`
  - `scripts/sources/fetch_github_prs.py`
