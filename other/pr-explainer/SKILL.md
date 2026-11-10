---
name: pr-explainer
zh_name: "PR 说明"
en_name: "PR Explainer"
emoji: "🔍"
description: "A pull request explained for reviewers: what changed and why, a before and after, risks and the test plan, and a guided tour of the files, drawn from the branch commits and diff."
en_description: "A pull request explained for reviewers: what changed and why, a before and after, risks and the test plan, and a guided tour of the files, drawn from the branch commits and diff."
category: doc
scenario: engineering
tags: ["pull request", "pr", "code review", "changes", "diff", "engineering"]
triggers:
  - "pr explainer"
  - "explain this pr"
  - "pull request description"
  - "explain my changes"
  - "review guide"
  - "walk me through this branch"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - typography-hierarchy
      - color
      - accessibility-baseline
  platform: desktop
  scenario: engineering
  preview:
    type: html
    entry: index.html
  design_system:
    requires: false
  example_prompt: "Explain the current branch as a pull request for reviewers: what changed and why, a before and after, risks and how it was tested, and a tour of the files in the order to review them."
---

# PR Explainer

**Intent.** Helps a reviewer understand a change in five minutes and review it in the right order. It is a guide to the diff, not a copy of it.

## Ground it

Write only what the sources say. Gather them yourself before writing a word:

- `git log --oneline <base>..HEAD` and `git diff --stat <base>...HEAD` (base: `main` unless the user says otherwise);
- `git diff <base>...HEAD -- <path>` for the files that matter, and the tests that changed;
- if `gh` is available and a PR exists, `gh pr view --json title,body,files,commits` and linked issues.

Keep the list of files, commits and refs you read: they go in a **Sources** section at the bottom of the page and in `sources` when you register (`register_open_design_artifact` with kind `html`). If something the document needs isn't in the sources, ask the user, or mark it plainly as an open question. Never invent numbers, dates, names or quotes.

## Structure

1. **Header:** PR title, branch → base, author, number of commits and files, `+added −removed`.
2. **In one paragraph:** what this changes and why, for someone who won't read further.
3. **Before and after:** the behaviour before and after, side by side. For UI changes, screenshots: render the before and after with the export tool and embed the images. For other changes, a short example (a command and its output, an API call).
4. **Risks:** what could break, and how the change guards against it.
5. **How it was tested:** the tests added or changed (by name), and manual checks.
6. **Review tour:** the files in the order to review them, grouped (core logic first, then call sites, then tests, then generated or mechanical changes), each with one line on what to look for. Mechanical changes (generated files, renames) are listed together so reviewers can skim them.
7. **Sources:** the commit range and the files read.

## Design

- One readable column (`max-width` 720–780px), body 16–17px with line-height 1.55–1.65, generous space between sections. It must read well on a phone: tables sit in an `overflow-x: auto` wrapper, nothing has a fixed width wider than the screen.
- Style from the active design system (`--bg`, `--surface`, `--fg`, `--muted`, `--border`, `--accent`); status colours are the only extra colours (green for accepted/done, amber for proposed/in progress, red for rejected/high severity, grey for superseded).
- Headings are short labels; the content does the talking. Code, paths and commands in a monospace face, with `overflow-wrap: anywhere` so long paths wrap on phones.
- Finish with `check_open_design_artifact` and fix every error at desktop and mobile width.
