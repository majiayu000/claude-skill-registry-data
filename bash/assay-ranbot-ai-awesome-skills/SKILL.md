---
name: assay
description: Run assay on a web page you just wrote or changed. It opens the page in a real browser, drives every control, and reports where the page contradicts itself. Local browser checks without an LLM API key
category: Document Processing
source: antigravity
tags: [python, javascript, react, api, claude, ai, llm, template, document, security]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/assay
---


# Assay

## Overview

A page you have just written has no tests yet. `assay` serves the page locally, opens it in a real Chromium browser through Playwright, finds every control on it, uses all of them, and reports where the page contradicts itself. There is no LLM API key requirement. Browser behavior can vary with application state, timing, browser version and network dependencies; repeated results are evidence only for the tested environment.

Use this skill after you create or change a web page, to run assay on that page and report the one line it prints. The skill reports the result and does not change code because of it unless you ask.

## When to Use This Skill

- Use when you have just created an HTML page and want to know whether its controls work before you move on.
- Use when you changed a page, or the JavaScript or CSS that a page loads, and want to confirm the page still holds together.
- Use when the user asks you to check, QA, or smoke-test a local web page.
- Run it once at the end, after the last edit, on each page you changed. Do not run it while you are still making changes.

## How It Works

### Step 1: Install the CLI once

Install assay from PyPI. The package is named `assay-ui` and the command it installs is `assay`.

```bash
pip install assay-ui
```

It needs Python 3.10 or newer. On the first run assay downloads the Chromium build Playwright uses.

### Step 2: Run assay on the page you changed

Point assay at the page itself and ask for the one-line summary.

```bash
assay <the page you changed> --one-line
```

Point it at a file such as `todo.html` or `dist/index.html`. A folder also works and opens the `index.html` inside it. The page is often a folder or two above the file you edited, so a change to a script or stylesheet still means running assay on the page that loads it. assay needs no LLM API key; initial browser installation and page dependencies may use the network. A small page takes seconds, and a busy one can take a minute or more.

### Step 3: Report the one line assay printed, verbatim

Put assay's output, word for word, as the last thing in your reply. It is already one line, or one line and a short list. Do not summarize it, reformat it, add to it, or write your own version.

A clean run looks like this, with assay's own numbers and wording.

```text
assay: checked todo/todo.html, 8 checks, nothing flagged.
```

A run that flagged something looks like this, followed by a short list.

```text
assay: checked notes/index.html, 12 checks, 4 flagged:
```

Report the line whether it flagged anything or not. Without it, the reader cannot tell a clean page from a check that never ran.

If the command did not run, say so in your own words, name the page, and quote what the shell actually printed. Never describe a check that did not happen as one that passed, and never guess at a cause.

### Step 4: Report the finding and stop

Report what assay found and stop. Do not edit code in response to a finding in the same reply. If the user then asks you to fix it, fix it.

## Examples

### Example 1: A page that checks out clean

**User:** I added a to-do list at `todo/todo.html`. Does it work?

```bash
assay todo/todo.html --one-line
```

```text
assay: checked todo/todo.html, 8 checks, nothing flagged.
```

Report that line as the last thing in the reply, and do not change the page.

### Example 2: A page where assay flagged something

```bash
assay notes/ --one-line
```

```text
assay: checked notes/index.html, 12 checks, 4 flagged:
  - draw on canvas twice, then press Undo twice: it reacted one press late
```

Report the whole line and its short list, say that a finding is a place to look rather than a confirmed bug, and wait for the user to ask before changing anything.

### Example 3: The command did not run

```bash
assay dist/index.html --one-line
```

```text
assay: error: dist/index.html does not exist
```

Say that assay did not run, name the page, and quote the message. Do not report a check that never happened as one that passed.

## Best Practices

- ✅ Run assay once, at the end, on each page you changed.
- ✅ Point it at the built page, such as `dist/index.html`, not at a source template.
- ✅ Print assay's one line exactly as it came out, as the last thing in your reply.
- ✅ When assay flags something, treat it as a place to look and wait to be asked before changing code.
- ❌ Do not run assay while you are still editing the page.
- ❌ Do not summarize, reword, or invent the result, and never report a check that did not run as one that passed.

## Limitations

- assay will not build your project. Point it at built output. Given a source tree, it says so and names the command to run, and it will not run `npm install` for you, because installing dependencies executes their setup scripts.
- assay checks one page. It does not crawl, so run it on each page you changed.
- assay cannot check intent. A control that runs but does the wrong thing usually is not caught, because ass
