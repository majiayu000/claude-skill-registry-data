---
name: check-article
description: Check whether article/hug-flow.md, the verbatim copy of the published HuG Flow post, is missing anything or out of date given the current repo content, and report what the post needs. Use when the user types /check-article, and right before the CHANGELOG.md chunk of every pull request in this repo.
---

# Check the article against the repo

`article/hug-flow.md` is published to <https://julienberanger.com/hug-flow>
by CI when it changes on `main`. The repo is the source of truth: the
question is **is the post missing anything, or still saying something the
repo has changed?**

This skill reports only. It never edits, stages or commits. Fixes always
go to `article/hug-flow.md`, never to the repo files it was compared with.

## Order

1. `git diff --name-only main...HEAD` (plus uncommitted changes): check
   the files this pull request changed first. That is where drift comes from.
2. Then walk the whole map below. Read both sides in full; don't sample.
3. Then any tracked file not in the map (`git ls-files`): if it adds or
   changes something the post describes, or should describe, it's a finding.

## Map

| Repo                                              | Article                                                       |
| ------------------------------------------------- | ------------------------------------------------------------- |
| `README.md` intro, `package.json` `description`   | Frontmatter `title`, `description`                            |
| `README.md` intro                                 | Intro, between the title and Motivation                       |
| `README.md` Motivation                            | Motivation                                                    |
| `README.md` Get started, `SETUP.md`               | Get started                                                   |
| `README.md` What it looks like                    | What it looks like                                            |
| `spec/hug-flow.md`, header table to §11           | Official spec, character for character                        |
| `examples/julien/README.md` intro and Files       | My own setup intro                                            |
| `examples/julien/CLAUDE.md`                       | My own setup, `CLAUDE.md` code block, character for character |
| `examples/julien/skills/super-app-issue/SKILL.md` | My own setup, intake skill summary and link                   |
| Further reading in the spec and examples README   | Further reading                                               |

## Expected differences

Don't report these:

- In Official spec: headings one level lower, relative links turned into
  absolute `https://github.com/julienbrg/hug/...` URLs, and the spec's title
  and Further reading left out.
- In the intro: the README's "Human-Gated Flow" subtitle and its line
  pointing to the article left out.
- In Get started: links to repo files written as plain text or absolute URLs.
- The rest of `examples/julien/README.md` (Stack, lifecycle mapping,
  enforcement layer, coverage, known deviations) and
  `examples/julien/settings.json` and `repo-settings.sh`: the article links
  to `examples/julien` instead of quoting them.
- First person ("I", "my setup") in the article vs neutral wording in the repo.
- Wording that points to a file in the repo where the article quotes it
  inline ("Here it is as I use it").
- Markdown formatting that prettier applies to the repo but not to `article/`
  (table padding, list markers, emphasis style) when the text is the same.

## Report

If the post is up to date, say so in one line.

Otherwise, one table, most important first:

| Repo | Article | Missing or outdated |
| ---- | ------- | ------------------- |

Give the repo location as a clickable `path:line` and the article location
as `§n` plus a short quote (or "nowhere" when it's missing). Then propose
the edit to `article/hug-flow.md` as the next chunk, to go through the
usual review loop.
