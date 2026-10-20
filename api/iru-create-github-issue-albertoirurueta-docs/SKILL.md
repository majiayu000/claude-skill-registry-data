---
name: iru-create-github-issue
description: Draft and file a new GitHub issue that is ready to be picked up by the `/iru-issue`, `/iru-plan`, `/iru-code` flow. Runs the `iru-explore` skill first to ground the issue in the actual codebase, then asks the user for the purpose of the task to be implemented, then asks for additional context (linked URLs, attached files/documents, related issues), then asks for the task's due date (optional) and importance (trivial/minor/important/blocking), and folds whatever is provided into the issue body. Any provided file/document is not just read for context but actually attached to the created issue — small text files are embedded inline, larger or binary files (images, PDFs, etc.) are uploaded as release assets and linked, since GitHub's API has no direct issue-attachment endpoint. Classifies the issue as bug/feature/enhancement from the stated purpose and matches it against this repository's actual label set, drafts a title and body (Summary, Context, Acceptance criteria, Task details — due date, importance, and an estimated task difficulty from very easy to impossible based on everything gathered — References), and shows the draft for confirmation before filing it with `gh issue create` (or GitHub MCP tools if `gh` is unavailable). Invoke as `/iru-create-github-issue` or `/iru-create-github-issue <short description>`. Stops early if this repository isn't hosted on GitHub. Use when the user has an idea, bug report, or request that needs to become a well-formed, actionable GitHub issue before `/iru-issue` or `/iru-plan` can pick it up — not for issues that already exist (nothing to file) or repositories on Bitbucket/Azure DevOps/TFS/Jira (no issue-filing target this skill supports).
model: sonnet
---

# Create GitHub Issue

Turn a rough idea, bug report, or request into a well-formed GitHub issue — grounded in the real codebase, with a
clear purpose statement and whatever supporting context the user has — so it's immediately actionable by the
`/iru-issue` or `/iru-plan` skills. This skill only files an issue; it does not branch, plan, or write code.

## Step 1 — Confirm this repository is hosted on GitHub

This skill is GitHub-specific (unlike `iru-explore`/`iru-issue`, which support multiple hosts) — verify before doing any
other work:

- If `iru-explore` already ran earlier in this conversation, reuse its `Repository host: ...` finding instead of
  re-detecting.
- Otherwise, get the remote URL (`git remote get-url origin`, falling back to `git remote -v` or whichever remote
  the current branch tracks) and check it matches `github.com` or a GitHub Enterprise Server domain.
- If the host is something else (Bitbucket, Azure DevOps/TFS) or there's no remote configured at all, tell the
  user plainly that this skill only files GitHub issues, and stop — don't attempt a different platform's
  equivalent or guess at one.

## Step 2 — Explore the codebase

Run `Skill({skill: "iru-explore"})` with no argument — there is no ticket yet, so this is a general orientation pass,
not one narrowed to a specific area. Skip this if general codebase exploration already happened earlier in this
same conversation and looks reasonably current; reuse it instead of repeating the work.

This grounds later steps in the real architecture, conventions, and tech stack (per `iru-explore`'s own "Tech stack"
report) so the issue can reference concrete files/modules instead of vague descriptions, and so its acceptance
criteria fit how the codebase actually behaves today.

## Step 3 — Ask for the purpose of the task

Ask the user directly, in plain conversational text (not `AskUserQuestion` — the answer is inherently open-ended,
not a choice among fixed options): what problem this issue should solve or what capability it should add, why it
matters, and any acceptance criteria they already have in mind. If the skill was invoked with a short description
argument, treat that as a starting point and ask only for what it leaves unclear (e.g. the "why," or what "done"
looks like) rather than re-asking everything from scratch.

Wait for the user's reply before continuing — the rest of the issue is drafted around this purpose.

## Step 4 — Ask for additional context

Ask the user (again as a plain, open-ended question) whether they have any of the following, making clear all of
it is optional:

- **Linked URL(s)** — design docs, discussions, external references, prior art.
- **Attached file(s) or documents** — screenshots, logs, specs, mockups (local paths).
- **Related issue(s)** — in this repository or elsewhere, that this depends on, relates to, or duplicates.

Gather whatever is provided:

- **URLs**: fetch each with `WebFetch` and note the key points worth folding into the issue — don't just link them
  blind if their content materially shapes scope or acceptance criteria.
- **Related issues**: confirm each with `gh issue view <id> --json number,title,url,state` (or GitHub MCP tools if
  `gh` is unavailable) so the reference in the drafted body is accurate — don't take the user's number on faith
  without checking it resolves to what they mean.

If the user has none of these, proceed with just the purpose from Step 3 — this step is not a blocker.

### Files/documents: read for context, then actually attach them

`Read` each local path (this tool also handles images and PDFs) to summarize what it shows that's relevant to the
issue — this grounds the Context/Acceptance criteria sections. But don't stop at a summary: GitHub's REST API and
`gh` CLI have no endpoint to attach an arbitrary file to an issue the way the web UI's drag-and-drop does (this is
a known, long-standing gap — see `cli/cli#12960`), so getting the actual file into the issue takes one of two
paths depending on the file:

- **Small, text-based files** (logs, `.md`/`.txt`, config, diffs, short specs — say, comfortably under a couple
  hundred lines): embed the file's actual content directly in the drafted issue body (Step 7's References
  section) inside a collapsible `<details><summary>filename.log</summary>` block wrapping a fenced code block of
  the full file content, closed with `</details>`. No upload needed — the real content lives in the issue text
  itself, not just a paraphrase of it.
- **Everything else** (images, PDFs, screenshots, large files, or any binary): upload it as a release asset and
  link the resulting stable URL in the issue body — `gh release upload` is the one officially supported `gh`
  mechanism that accepts an arbitrary file and hands back a durable download URL, regardless of file type:
  - Check whether a release already exists to host these: `gh release view issue-attachments --json tagName`.
  - If it doesn't exist yet, this is the first file of this kind in the repository — ask the user via
    `AskUserQuestion` before creating it, since a new release is visible to everyone with repository access:
    **Create a dedicated `issue-attachments` release to host uploaded files (recommended — reusable for every
    future issue created this way)** / **Skip uploading — just describe these files in the issue body without
    attaching them**. If they decline, keep the existing summarize-only behavior for these files and skip the
    rest of this step.
  - If they confirm, create it once: `gh release create issue-attachments --title "Issue attachments" --notes
    "Storage for files attached to issues via /iru-create-github-issue." --notes-file -` (or a plain `--notes`
    string) — do not attach any repository ref/tag content beyond what `gh` creates by default.
  - Upload each file: `gh release upload issue-attachments <path>` (add `--clobber` only if re-uploading a file
    with a name that's already present and you intend to replace it, not for a new file with a new name — if two
    different files share a filename, rename one locally before upload so both survive). Get each asset's
    download URL from the command's own output, or `gh release view issue-attachments --json assets` afterward.
  - Note the filename → URL mapping for use in Step 7's References section: an image (`![filename](url)`) so it
    renders inline, anything else as a plain link (`[filename](url)`).
  - If `gh` is unavailable, search for GitHub MCP tools that can create a release and upload an asset
    (`ToolSearch` "github release"); if none exist either, fall back to describing the file in the body without
    attaching it, and say so plainly to the user rather than silently dropping the attachment.

## Step 5 — Ask for due date and importance

Ask the user two more things before drafting — both help whoever triages or picks up the issue later:

- **Due date**: ask plainly (in open-ended text, not `AskUserQuestion`) whether there's a deadline or target date
  for this work, making clear it's optional. Normalize whatever they give to an absolute date (e.g. "next Friday"
  → the actual date) for the drafted issue. If they have none, omit it from the draft entirely rather than
  inventing one.
- **Importance**: ask via `AskUserQuestion`, since this is a fixed choice, to pick one of:
  - **Trivial** — cosmetic or nice-to-have, no real urgency.
  - **Minor** — worth doing, but low impact if it slips.
  - **Important** — meaningfully affects users or the project; should be prioritized in the normal course of work.
  - **Blocking** — actively blocking other work, a release, or a user; needs prompt attention.
  Only pre-select a recommended default if the purpose (Step 3) or context (Step 4) clearly implies one (e.g. a
  bug described as breaking existing functionality leans toward Important/Blocking); otherwise present all four
  with no default and let the user choose. If they decline to pick (e.g. via "Other"), record importance as "not
  specified" rather than guessing on their behalf.

## Step 6 — Classify the issue and pick a label

Decide whether this is a bug or a feature/enhancement, using the same signal words `iru-issue`'s own classification
step uses: language describing broken/incorrect existing behavior ("fails," "crash," "broken," "incorrect," "error
when…") → bug; language describing new, not-yet-existing capability ("add," "support for," "new," "implement,"
"as a user I want…") → feature/enhancement.

Check which labels this repository actually has: `gh label list --json name,description`. Match the
classification against whatever labels exist (e.g. `bug`, `enhancement`, `feature`) — don't invent a label name
that isn't in that list. If nothing matches closely, or the classification is genuinely ambiguous, ask the user
via `AskUserQuestion` to pick from the repository's actual label list (this is now a concrete decision among known
options, unlike Steps 3-4's open-ended questions).

## Step 7 — Draft the issue

Compose:

- **Title**: a concise, imperative one-liner describing the change (e.g. "Add retry support to the HTTP client,"
  "Fix list item move detection on drag cancel").
- **Body**, structured as:
  - **Summary** — the purpose and motivation from Step 3, in the user's own terms.
  - **Context** — grounded in Step 2's exploration: the relevant existing files/modules/classes and how they
    currently behave, so whoever picks this up (including a future `/iru-explore`/`/iru-plan` run) starts oriented
    instead of cold.
  - **Acceptance criteria** — a short bulleted list, if the user gave any in Step 3 or they can be reasonably
    inferred from the purpose; omit this section entirely rather than inventing criteria that weren't discussed.
  - **Task details** — a short bulleted list combining Step 5's answers with your own assessment:
    - **Due date**: the date from Step 5, or omit this line entirely if none was given.
    - **Importance**: the level chosen in Step 5 (trivial/minor/important/blocking), or "not specified."
    - **Estimated difficulty**: your own assessment of how hard this task is to implement, grounded in everything
      gathered so far — Step 2's exploration (how much of the codebase it touches, whether it needs new
      abstractions or unfamiliar frameworks/dependencies, how many files/modules are affected), Step 3's purpose,
      and Step 4's context. Pick exactly one level from: very easy, easy, medium, hard, very hard, extreme,
      impossible — then state it plus a one-line rationale (e.g. "medium — touches two existing classes with
      clear precedent elsewhere in the codebase, no new dependencies"). Use judgment based on the concrete
      codebase evidence, not a formula; reserve "impossible" for something that genuinely isn't achievable as
      stated (e.g. it contradicts a hard technical constraint uncovered in Step 2), not just "very hard."
  - **References** — any URLs, confirmed related-issue links, and the actual attached files from Step 4: inline
    collapsible blocks for small text files, `![filename](url)`/`[filename](url)` links for anything uploaded to
    the `issue-attachments` release, or plain summaries for files the user chose not to attach; omit this section
    entirely if Step 4 gathered nothing.

Show the full drafted title and body to the user before taking any action.

## Step 8 — Confirm and create

Filing an issue is visible to everyone with access to the repository — never do it without explicit confirmation.
Ask the user via `AskUserQuestion`:

- **Create the issue now** (recommended once the draft looks right).
- **Edit the draft first** — take their edits, update the draft, and re-ask.
- **Don't create it** — stop here; the draft itself is the deliverable.

If they confirm creation:

- Write the body to a temp file (avoids shell-quoting issues with multi-line Markdown) and run:
  ```bash
  gh issue create --title "<title>" --body-file <path> --label "<label>"
  ```
  Omit `--label` if Step 6 found no matching label. If `gh` is not installed/authenticated, search for GitHub MCP
  tools instead (`ToolSearch` "github issue") and use those to create the issue with the same title, body, and
  label.
- Capture the created issue's number and URL from the command's own output (or `gh issue view --json number,url`
  immediately after, if the create output didn't surface it).

## Step 9 — Report

Give the user the issue number and URL, and tell them the issue is now ready to be picked up: `/iru-issue <number>`
to kick off branch creation, exploration, planning, implementation, and PR creation in one pass, or `/iru-plan
<number>` alone if they'd rather just get an implementation plan first. If Step 4 created the `issue-attachments`
release, mention that too — it's a repo-visible artifact the user may not expect, and it will be reused (not
recreated) by future runs of this skill.
