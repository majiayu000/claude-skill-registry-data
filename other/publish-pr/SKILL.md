---
name: publish-pr
description: Use when pushing a branch, opening a pull request, updating pull request metadata, or preparing PR titles and bodies for this repository.
---

# Publish PR

## Rules

- Push or update a PR only when the owner explicitly asks for it.
- After the owner explicitly approves PR creation, open a regular (ready-for-review) PR by default; use a draft only when the owner asks for one.
- Keep the PR title focused on the change itself.
- Do not prefix PR titles with agent labels such as `[codex]`, `[claude]`, or similar. They add noise and are not part of the project change.
- Use one PR for one intent.
- Do not stage unrelated changes.

## PR Body

Include:

- what changed
- why it changed
- notable behavior or workflow impact
- checks run
- known advisory warnings or follow-up items

### Internal links only

A PR title, body, or comment may link only to things **inside this repository**: its own files, branches, commits, issues, and pull requests.

Never write there:

- another repository's issue or pull request, in any form — `owner/repo#123`, a full URL, or a bare autolink
- any external URL at all: upstream projects, docs, model pages, changelogs

A cross-repository reference posts a backlink on the target's timeline and cannot be withdrawn; `/ops/requirements.md` has the reasoning. It has already happened once from this repository.

Upstream references go in files instead — the article, an ADR, a code comment. If a PR body seems to genuinely need an outside link, ask the owner and wait for an answer.

### No AI attribution

No `Co-Authored-By: Claude`, no "Generated with Claude Code", no Claude or AI mention in a title, body, or comment. Commits and pull requests are authored by the owner's git and GitHub identity alone.

## Automated Review Findings

CodeRabbit and similar bots review these PRs. A finding is a suggestion, not an instruction.

Check each one against this repository's own conventions before acting. A finding that contradicts `/ops/style-writing.md` or an established pattern is declined, and the reply says which convention it conflicts with and how widely that convention is used. Empty `alt` on article images is the standing example: it is the documented template and is used on hundreds of images, so a finding asking for descriptive alt text is declined here rather than applied to one page.

Report every finding to the owner with your recommendation. Do not silently accept or silently ignore one.

## Pipeline

The end of the article pipeline in [article-authoring](../article-authoring/SKILL.md). [release-check](../release-check/SKILL.md) comes first.

English wording for the title and body follows [english-reply](../english-reply/SKILL.md).

## Checks Before Publishing

- `git status --short --branch`
- `git diff --check`
- `npm run check` when project files changed
- `npm run build` when content, Eleventy config, nav, or scripts changed
