---
name: reviewer-roulette
description: Selects exactly one reviewer for a feature branch or pull request, with one backup, using changed files, git history, and the repo ownership map. Use when asked to pick, suggest, assign, or choose a reviewer for a PR, branch, diff, or set of changed files.
compatibility: Cursor-compatible Agent Skill. Requires git.
---

# Reviewer Roulette

## Purpose

The goal is roulette: a single clear reviewer selection (plus one fallback-only backup) instead of a reviewer group, from two signals:

- Git evidence: who recently and historically worked on the changed files.
- Ownership map: the desired ownership state in `docs/ownership-map.md`.

Prefer the ownership map when git evidence is mixed, weak, or mostly reflects old ownership.

## Workflow

1. Load `docs/ownership-map.md`. If it doesn't exist, say so, rely on git evidence alone, and cap confidence at medium.

2. Identify changed files.

   Use the user's base branch or PR target when provided. Otherwise, infer from common defaults:

   ```bash
   git diff --name-only origin/master...HEAD
   git diff --name-only HEAD
   ```

3. Classify the change.

   Map changed files to:
   - feature areas / domains from `docs/ownership-map.md`;
   - software engineering concepts from `docs/ownership-map.md`;
   - cross-cutting risks such as API contracts, database design, testing, CI, or UX.

4. Collect git evidence for the affected files.

   Prefer recent history for current context and use older history only as supporting evidence:

   ```bash
   git log --since='18 months ago' --format='%an <%ae>' -- path/to/file
   git shortlog -sn -- path/to/file
   git blame --line-porcelain path/to/file
   ```

   Normalize aliases from names, usernames, and emails when they clearly refer to the same person. Use
   `docs/ownership-map.md` as the source of truth for known reviewers and GitHub handles.

5. Pick exactly one reviewer and one backup.
   - High confidence: changed files, recent git history, and ownership map agree.
   - Medium confidence: ownership map is clear but git history is mixed, weak, or spread across people.
   - Low confidence: area classification is uncertain or the change spans multiple unrelated ownership areas.
   - Prefer the ownership-map owner unless the changed files are narrowly concentrated in code recently maintained by
     someone else.
   - Do not pick the branch author as reviewer if the author is known or strongly implied by the git evidence.
   - If the mapped owner is the author, fall through to the next best non-author reviewer instead of stopping.
   - Backup is not a second assigned reviewer. It is only the fallback if the selected reviewer is unavailable.
   - Backup should be the mapped backup for the dominant area, unless git evidence clearly points to another listed
     person.

6. Keep output short.

   Return one sentence:

   ```text
   Pick <reviewer> (<github-handle>, <confidence> confidence), backup <backup> (<github-handle>): <short reason>.
   ```

## Example Output

```text
Pick <reviewer> (<github-handle>, medium confidence), backup <backup> (<github-handle>): the change touches alert ingestion and API contracts, and the ownership map is clearer than the mixed file history.
```
