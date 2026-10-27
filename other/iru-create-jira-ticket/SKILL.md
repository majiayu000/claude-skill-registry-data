---
name: iru-create-jira-ticket
description: "Invoke as `/iru-create-jira-ticket` or `/iru-create-jira-ticket <short description>`. Drafts and files a Jira ticket ready for the `/iru-issue`, `/iru-plan`, `/iru-code` flow: explores the codebase, asks purpose, context, epic, files (attached), due date and importance, then files via Jira MCP after confirmation. Needs a Jira MCP tool. Use to turn an idea, bug report or request into an actionable ticket."
model: sonnet
---

# Create Jira Ticket

Turn a rough idea, bug report, or request into a well-formed Jira ticket — grounded in the real codebase, with a
clear purpose statement and whatever supporting context the user has — so it's immediately actionable by the
`/iru-issue` or `/iru-plan` skills. This skill only files a ticket; it does not branch, plan, or write code.

This is the Jira equivalent of `iru-create-github-issue` — same shape, but sourced through Jira MCP tools instead of
the `gh` CLI, and with Jira's project/issue-type model instead of GitHub labels.

This skill is for new tickets only — not for tickets that already exist (nothing to file), and not for work that
should be tracked as a GitHub issue instead (use `iru-create-github-issue`).

## Step 1 — Confirm Jira MCP tooling is available

Unlike GitHub (which has the `gh` CLI as a reliable fallback), there is no ubiquitous Jira CLI — this skill depends
entirely on a connected Jira MCP integration.

- Search for it: `ToolSearch` with a query like "jira issue" or "jira ticket".
- If one or more Jira MCP tools are found, note what they support (creating issues, listing projects, listing
  issue types, fetching issues by key, **uploading/adding an attachment to an existing issue**) — later steps
  rely on whichever of these are actually available. The attachment capability specifically drives whether
  Step 4/Step 8 can attach provided files directly to the ticket, or must fall back to describing/inlining them.
- If none are found, tell the user plainly that this environment has no Jira connection and this skill has no
  fallback for filing one without it, then stop. Suggest `iru-create-github-issue` instead if the work should be
  tracked on GitHub.

## Step 2 — Explore the codebase

Run `Skill({skill: "iru-explore"})` with no argument — there is no ticket yet, so this is a general orientation pass,
not one narrowed to a specific area. Skip this if general codebase exploration already happened earlier in this
same conversation and looks reasonably current; reuse it instead of repeating the work.

This grounds later steps in the real architecture, conventions, and tech stack (per `iru-explore`'s own "Tech stack"
report) so the ticket can reference concrete files/modules instead of vague descriptions, and so its acceptance
criteria fit how the codebase actually behaves today.

## Step 3 — Ask for the purpose of the task

Ask the user directly, in plain conversational text (not `AskUserQuestion` — the answer is inherently open-ended,
not a choice among fixed options): what problem this ticket should solve or what capability it should add, why it
matters, and any acceptance criteria they already have in mind. If the skill was invoked with a short description
argument, treat that as a starting point and ask only for what it leaves unclear (e.g. the "why," or what "done"
looks like) rather than re-asking everything from scratch.

Wait for the user's reply before continuing — the rest of the ticket is drafted around this purpose.

## Step 4 — Ask for additional context

Ask the user (again as a plain, open-ended question) whether they have any of the following, making clear all of
it is optional:

- **Linked URL(s)** — design docs, discussions, external references, prior art.
- **Attached file(s) or documents** — screenshots, logs, specs, mockups (local paths).
- **Related ticket(s) or issue(s)** — in this Jira project, another project, or a linked GitHub repository, that
  this depends on, relates to, or duplicates.
- **Epic** — an optional Jira epic this ticket belongs to.

Gather whatever is provided:

- **URLs**: fetch each with `WebFetch` and note the key points worth folding into the ticket — don't just link
  them blind if their content materially shapes scope or acceptance criteria.
- **Files/documents**: `Read` each local path (this tool also handles images and PDFs) and summarize what it
  shows that's relevant to the ticket — this grounds the Context/Acceptance criteria sections. Don't stop at a
  summary, though: unlike GitHub, Jira's own REST API has a native attachment endpoint
  (`issue/{key}/attachments`) that accepts any file type, so if Step 1 found a Jira MCP tool that exposes it,
  plan to actually attach every one of these files to the ticket once it exists — record the local paths here
  for Step 8 to upload, since attaching requires the ticket's key and the ticket isn't created until then. If no
  attachment-capable Jira MCP tool is available, fall back the same way `iru-create-github-issue` does when it
  can't reach GitHub's own upload mechanism: embed small text-based files (logs, `.md`/`.txt`, config, diffs,
  short specs — comfortably under a couple hundred lines) directly in the description's References section
  inside a collapsible block, and for anything else (images, PDFs, large/binary files) just describe it in
  References without an actual attachment, telling the user plainly that this Jira connection can't upload
  files.
- **Related Jira tickets**: confirm each with the connected Jira MCP tools (fetch by key: summary, status, URL) so
  the reference in the drafted description is accurate — don't take the user's key on faith without checking it
  resolves to what they mean. A related **GitHub** issue, if mentioned, can be confirmed with `gh issue view
  <id> --json number,title,url,state` if `gh` is available; otherwise just record the reference as given.
- **Epic**: if the user gives one, confirm it with the connected Jira MCP tools (fetch by key: summary,
  description, status, labels/components, and URL) so it's a real epic and not a typo'd key. Then explore it the
  same way `iru-explore` explores an epic found for an existing ticket: read its description in full and, if the
  Jira MCP tools support listing an epic's child tickets, fetch those too (summary and status are enough unless
  one's description is clearly load-bearing) — an epic frequently carries the overall goal, cross-cutting
  constraints, or sibling tasks already completed or planned that should shape how this new ticket is scoped,
  not just a label to attach. Note what it adds for Step 7's draft. This epic will be assigned to the new ticket
  as its parent/epic link when it's created in Step 8 — if fetching it fails (no permission, deleted, not found),
  tell the user and ask whether to proceed without it or provide a different key.

**Also delegate to the `iru-jira-custom-context` skill** for anything organization-specific beyond the above —
that skill is an explicit extension point for whatever extra questions or lookups this Jira instance/organization
needs (a required custom field, team/component ownership, a customer/account, an affected environment, a
compliance/security classification, etc.) without this skill having to hardcode them:

```
Skill({skill: "iru-jira-custom-context", args: "<the task's stated purpose from Step 3>"})
```

Fold whatever it returns into the draft the same way as the other optional context above (Step 7). If it reports
nothing was provided (its own default catch-all question declined, or every extended question skipped as
optional), proceed without it — this call is never a blocker, and if the skill itself isn't installed in this
repository, skip it entirely and continue as if it had returned nothing.

If the user has none of the context above, and `iru-jira-custom-context` returns nothing either, proceed with
just the purpose from Step 3 — this step is not a blocker.

## Step 5 — Ask for due date and importance

Ask the user two more things before drafting — both help whoever triages or picks up the ticket later:

- **Due date**: ask plainly (in open-ended text, not `AskUserQuestion`) whether there's a deadline or target date
  for this work, making clear it's optional. Normalize whatever they give to an absolute date (e.g. "next Friday"
  → the actual date) for the drafted ticket. If they have none, omit it from the draft entirely rather than
  inventing one.
- **Importance**: ask via `AskUserQuestion`, since this is a fixed choice, presenting all four levels — **Trivial**,
  **Minor**, **Important**, **Blocking** — but mark whichever applies as the recommended default rather than
  leaving all four unweighted:
  - **Minor** is the default recommendation for an ordinary task.
  - **Blocking** is the default recommendation instead when Step 3's purpose or Step 4's context describes a bug
    or incident actively affecting a production environment — language like "production," "prod," "outage,"
    "down," "customers affected," or "data loss," combined with broken/incorrect existing behavior (the same
    "fails," "crash," "broken," "error when…" signal words used elsewhere in this pipeline to detect a bug).
  This is guidance for the recommended option, not a silent assignment — always let the user confirm or pick a
  different level. If they decline to pick (e.g. via "Other"), record importance as "not specified" rather than
  applying the Minor default silently.

## Step 6 — Determine the target project and issue type

Jira tickets need a project and an issue type — unlike GitHub, where any issue lands in the one repository
already in context.

- **Project**: if the current conversation already established a Jira project (e.g. a prior `/iru-explore PROJ-123`
  or `/iru-issue PROJ-123` in this session), offer it as the default. Otherwise, if the Jira MCP tools support listing
  accessible projects, fetch that list and ask the user via `AskUserQuestion` to pick one (with a sensible default
  if only one project is accessible). If projects can't be listed, ask the user directly for the project key.
- **Issue type**: decide bug vs. feature/task, using the same signal words `iru-issue`'s own classification step
  uses: language describing broken/incorrect existing behavior ("fails," "crash," "broken," "incorrect," "error
  when…") → `Bug`; language describing new, not-yet-existing capability ("add," "support for," "new,"
  "implement," "as a user I want…") → `Story`/`Task`/`New Feature` (whichever label this Jira instance uses).
  If the Jira MCP tools support listing a project's available issue types, fetch that list and match against it —
  don't invent an issue type name the project doesn't actually have configured. If the classification is
  genuinely ambiguous, or issue types can't be listed, ask the user via `AskUserQuestion` to pick.
- **Labels/components** (optional): if the user's stated purpose or additional context clearly implicates an
  existing label or component (check via the MCP tools if listing is supported), note it for Step 8; otherwise
  omit rather than guessing.

## Step 7 — Draft the ticket

Compose:

- **Summary**: a concise, imperative one-liner describing the change (e.g. "Add retry support to the HTTP
  client," "Fix list item move detection on drag cancel").
- **Description**, structured as:
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
      Step 4's context, and the epic's context if one was explored. Pick exactly one level from: very easy, easy,
      medium, hard, very hard, extreme, impossible — then state it plus a one-line rationale (e.g. "medium —
      touches two existing classes with clear precedent elsewhere in the codebase, no new dependencies"). Use
      judgment based on the concrete codebase evidence, not a formula; reserve "impossible" for something that
      genuinely isn't achievable as stated (e.g. it contradicts a hard technical constraint uncovered in Step 2),
      not just "very hard."
  - **References** — any URLs and confirmed related-ticket/iru-issue links from Step 4; omit if none were
    provided. If an epic was confirmed in Step 4, name it here too (key, summary, and a one-line note of what
    context it added), separately from ordinary related tickets since it's also an assignment, not just a
    reference. For files/documents from Step 4: if they'll be attached via Jira MCP tools once the ticket
    exists, add a short placeholder line per file ("attached: filename.ext") rather than embedding or linking
    anything yet — the real attachment happens in Step 8 and shows up in the ticket's own Attachments panel. If
    no attachment-capable tool is available, use Step 4's fallback instead: the inline collapsible block for
    small text files, or a plain description for anything else.
  - Anything `iru-jira-custom-context` returned in Step 4: fold each label/value pair it reported in as its own
    line, either under **Task details** if it reads like a property of the ticket (team, environment, customer)
    or under **References** if it reads like supporting material — whichever fits the specific pair better. Omit
    this entirely if it returned nothing.

Show the full drafted summary, description, project, issue type, and — if one was given — the epic it will be
assigned to, to the user before taking any action. If Step 4 planned any real attachments (not just the inline/
described fallback), list those file paths too, so the user sees exactly what's about to be uploaded to the
ticket alongside everything else.

## Step 8 — Confirm and create

Filing a ticket is visible to everyone with access to this Jira project — never do it without explicit
confirmation. Ask the user via `AskUserQuestion`:

- **Create the ticket now** (recommended once the draft looks right).
- **Edit the draft first** — take their edits, update the draft, and re-ask.
- **Don't create it** — stop here; the draft itself is the deliverable.

If they confirm creation, use the connected Jira MCP tool(s) from Step 1 to create the ticket with the project,
issue type, summary, description, any labels/components determined above, and — if one was confirmed in Step 4 —
the epic link/parent field set to that epic's key (the classic "Epic Link" field, or `parent` in team-managed/
next-gen projects, whichever this Jira instance's create-issue tool expects). Capture the created ticket's key
and URL from the tool's response.

If ticket creation fails (e.g. a required field this Jira instance enforces wasn't supplied), surface the exact
error to the user rather than retrying blindly, and ask how to proceed (supply the missing field, or stop).

Once the ticket exists, upload every file Step 4 flagged for real attachment (the attachment-capable-tool path,
not the inline/described fallback) using the connected Jira MCP tool(s), targeting the newly created ticket's
key. Do this one file at a time so a single failure doesn't need to be diagnosed against a batch: if uploading a
particular file fails (wrong MIME type, size limit, permission issue), note that file's error, keep uploading
the rest, and report every failure in Step 9 rather than silently dropping it. Files handled by Step 4's fallback
(already inlined in the description, or already described in References) need no further action here.

## Step 9 — Report

Give the user the ticket key and URL, and tell them the ticket is now ready to be picked up: `/iru-issue <key>` to
kick off branch creation, exploration, planning, implementation, and PR creation in one pass, or `/iru-plan <key>`
alone if they'd rather just get an implementation plan first. If any file failed to attach in Step 8, list which
ones and why, rather than letting a partial attachment failure pass unmentioned.
