---
name: github-init
description: >-
  Sets up the GitHub repo for a new Umbraco package: README, LICENSE, CONTRIBUTING.md, a bug
  report template and a Dependabot config. Use when a project has no `origin` remote yet and
  is about to go public.
user-invocable: true
argument-hint: [optional repo name]
---

# github-init

Stand up the GitHub remote for a new Umbraco package and make its first impression a good
one. Deliberately lighter than a generic open-source bootstrap checklist — see "What this
skips, and why" below.

## Preflight

1. **Refuse if a remote already exists.** `git remote -v` — if `origin` points at github.com,
   stop and tell the user. Suggest `gh repo view` / `gh repo edit` instead.
2. **`gh auth status`** — refuse if not logged in; tell the user to run `gh auth login`.
3. Read context: `CLAUDE.md`, the feature plan folder(s) if any exist, any existing `README.md`,
   `LICENSE`, `CONTRIBUTING.md`, `.github/` — never overwrite without consent.

## Interview (ask in one batch)

1. **Repo name** — propose one derived from `CLAUDE.md` (kebab-case, short). Offer 2–3
   options if the obvious name is ambiguous.
2. **Visibility** — public or private.
3. **License** — propose with a one-line reason each: **MIT** (most permissive, standard
   default for an Umbraco package or add-on) or **Apache-2.0** (adds an explicit patent
   grant, worth it if the package is likely to see corporate adoption). Recommend MIT unless
   there's a specific reason to want the patent grant.
4. **Owner** — personal account vs. an org, only if `gh auth status` shows the user belongs
   to one.

## The bar — what gets built before the first push

### README.md — real, never boilerplate

A boilerplate README is anything matching: just the project name and a one-liner; contains
`TODO`, `Lorem ipsum`, or the literal `project-init` stub text; no installation, no usage, no
example. If the current README trips this, **refuse to push** and offer to write a real one
from `templates/README.md` — fill in every placeholder, don't copy one through unfilled.

Pull the pitch and supported-versions line from `CLAUDE.md` — never invent them. If
`CLAUDE.md` doesn't have them yet, send the user to `project-init` first.

### CONTRIBUTING.md — one file, short, honest

Minimum sections: prerequisites + how to get the project running locally (one command if
possible), how to run tests, where the coding conventions live (point at `CLAUDE.md`, don't
repeat it), and how to propose a change (issue first vs. PR first — link `git-workflow`'s
commit-format section). If the project supports more than one CMS major at once, add the
branch-naming rules `git-workflow` describes (`vN/feature/…`, `vN/release/…`, etc.). 60–150
lines is plenty; don't split this into multiple files the way a large flagship project might.

### LICENSE — real SPDX text

`gh repo create ... --license <id>` drops in the canonical text — don't hand-write it or
fudge the year/holder.

### One issue template — bug report only, plus contact links instead of more forms

`.github/ISSUE_TEMPLATE/bug_report.yml`, structured like a real, large open-source Umbraco
project's (its actual field set, not a generic guess): a required "which version" field, a
required bug-summary textarea, an optional "specifics" textarea (URL it happens on, browser,
screenshots/videos), a required "steps to reproduce," and a required "expected result /
actual result." Ask for each field's `description` to include a short hint ("write the
*exact* version, example: `10.1.0`") — it measurably improves what people fill in.

`config.yml` — copy from `templates/config.yml`, filling in the real Discussions/security
links for this project.

A contact link that redirects feature ideas to a discussion, and another that redirects
security reports to wherever that actually gets handled, is a better fit for a small package
than either a second structured issue-request template or a standalone `SECURITY.md` — see
"What this skips" below.

### Dependabot config — locked dependencies ignored from day one

`.github/dependabot.yml`, built from `umbraco-dependencies`' "Dependabot" section and its
template. Without it, Dependabot's security updates still open PRs, including ones for
dependencies the CMS decides, and nothing groups the dev-only noise. Fill the ignore list
from what this project actually references, checked against the CMS at the package's floor.
If the project carries more than one CMS major, add a `target-branch` copy of each entry per
extra line.

## What this skips, and why

This is intentionally lighter than a generic "professional open-source repo" checklist,
because real Umbraco package repos don't carry the extra weight:

- **No `SECURITY.md`.** Route reports via the `config.yml` contact link above instead, to
  wherever the disclosure process actually lives (a centralized page for something Umbraco-
  scale; an email address in `CONTRIBUTING.md` for a typical package). A dedicated file
  saying the same thing a contact link already says is redundant.
- **No separate feature-request issue *form*.** A contact link redirecting to a discussion
  is the pattern to copy, not a second structured `.yml` template.
- **No `CODE_OF_CONDUCT.md` by default.** Add one only once the project has a meaningfully
  sized outside contributor base — an unused template file is worse than no file.

## Behavior

1. Run the interview.
2. Audit existing files. For each one missing or boilerplate, stop and draft it with the
   user — never push first and fix later.
3. **README boilerplate gate.** Re-read the README right before creating the remote. If it
   still trips the boilerplate detector, refuse and offer to rewrite.
4. Create the remote:
   ```bash
   gh repo create <owner>/<name> \
     --<visibility> \
     --license <spdx-id> \
     --source . \
     --remote origin \
     --description "<one-line from README>" \
     --push
   ```
5. After push: confirm the description on github.com matches the README's pitch, print the
   URL.

## Rules

- Never push a boilerplate README. Refuse, draft, then push.
- Don't fabricate a description — pull it from the README's one-liner.
- Never set `origin` to a different remote without explicit consent.
- Never make a repo public if the interview said private, and vice versa.

## Hand off

Report: remote URL, license + visibility + owner, files created, anything skipped and why.
Suggested next: `git-workflow` for the first commit/PR once there's something to ship. When
Dependabot PRs start arriving, `dependency-review` works through them.
