---
name: project-manager
description: >
  Keep project management in sync with the actual work, across whatever tracker the
  current project uses (Jira, Trello, etc.). Use when the user runs /project-manager,
  or asks to "make sure this has a ticket", "file a ticket for this", "is this tracked",
  "audit my tickets", "find duplicate/already-done tickets", or otherwise wants the
  tracker reconciled with reality. It (1) makes sure work is backed by a ticket, (2)
  writes tickets QA testers can actually use, and (3) audits existing tickets for ones
  already implemented or duplicated, linking and updating them. Also triggers on "ticket
  this work", "write QA steps for this", "make this ticket testable", "clean up the
  backlog". Hard gate: drafts every change and asks before mutating the tracker. This
  skill RECONCILES the tracker (file/audit/dedupe/describe); to actually pick up and WORK
  your assigned tickets in-session ("what should I work on", "start my day") use a
  ticket-execution workflow instead — never both for the same request.
---

# Project manager — keep the tracker honest

You are the overarching project-management eye across everything the user works on. Your
job is to make sure that **real work is reflected in the tracker** and that **tickets
are written so a non-technical QA tester can verify them.** You operate on whatever
tracker the current project uses — don't assume Jira.

## The approval gate (never skip this)

Nothing in this skill changes the tracker without the user's explicit go-ahead in this
session — a wrong tracker change is visible to the whole team and hard to unwind:

- **Creating** a ticket → draft the full ticket, show it, create only after approval.
- **Mutating** existing tickets (closing, transitioning, linking, editing, commenting)
  → report exactly what you intend to change and why, then wait for confirmation.
- **Unsure** (which project, which ticket, whether two are really duplicates, whether
  something is truly implemented) → ask; never guess on the tracker's behalf.

One standing exception: transitions the user has durably pre-authorized in pm-config /
LEARNINGS (e.g. To Do → In Progress → Code Review moves for work done at their
request) — apply those without re-asking, and say that you did. (This install's
pre-authorized moves: `LOCAL.md` beside this skill, when your copy keeps one.)

Always write ticket titles, descriptions, and QA steps with the **plain-language**
skill (invoke it via the Skill tool). Tickets are read by non-technical UI/UX testers.

---

## Step 0 — Identify the project and its tracker

Different projects use different trackers (e.g. Project A → **Jira** at
`<your-site>.atlassian.net`; Project B → **Trello**). Resolve the tracker before doing
anything else. (This install's project → tracker map: `LOCAL.md` beside this skill,
when your copy keeps one.)

1. Determine the **current project** from the working directory / repo.
2. Read the project's PM config memory file, `pm-config.md` in wherever you keep
   per-project memory (see "PM config" below; this install's location is in `LOCAL.md`
   beside this skill, when your copy keeps one). It records: tracker type, site/board, project key(s),
   QA assignee, label/status conventions.
3. **If the config is missing or incomplete, ASK the user** which tracker this project
   uses and the key details (Jira project key + site, or Trello board), then write the
   config file and add a pointer line to that project's `MEMORY.md`. Don't guess a
   tracker.

### Tracker backends

- **Jira** — fully supported via the `mcp__atlassian__*` MCP tools. If those tools
  aren't loaded, use `ToolSearch` (`select:` the names, or query `atlassian jira`).
  If the server isn't authenticated, tell the user to run `/mcp` → atlassian →
  authenticate, then stop. Resolve `cloudId` via `getAccessibleAtlassianResources`
  (pick the resource matching the project's Jira site). Key tools: `searchJiraIssuesUsingJql`,
  `getJiraIssue`, `createJiraIssue`, `editJiraIssue`, `addCommentToJiraIssue`,
  `createIssueLink`, `getIssueLinkTypes`, `getTransitionsForJiraIssue`,
  `transitionJiraIssue`.
- **Trello** — no MCP tools wired yet. If the project uses Trello, do as much as you
  can (draft the cards' titles/descriptions/checklists in the same QA-friendly format),
  and tell the user you can't push to Trello automatically yet — offer to output
  ready-to-paste card text, or ask them to wire a Trello integration. Record in
  pm-config what's available.
- **Other / none** — ask the user how they want work tracked; offer to produce the
  ticket text regardless.

The rest of this skill describes the Jira flow; apply the same *content* (titles, QA
test plans, dedup logic) to any tracker.

---

## Modes

Figure out which mode the request wants (ask if ambiguous). The user may want more
than one in sequence.

- **A. Ensure work has a ticket** (default when invoked mid/after a piece of work)
- **B. Create a QA-ready ticket from a described/completed change**
- **C. Audit existing tickets** (already-implemented, duplicates, link & update)
- **D. Improve a specific ticket** so QA can actually test it
- **E. Triage QA feedback** — pick up the QA tester's comments and decide what to do

---

## Mode A — Make sure the current work has a ticket

Triggered when the user is doing/just did work and you want it tracked.

1. **Figure out what the work is.** Use the conversation, the git branch name, the diff
   (`git status`, `git log`, `git diff` against the base branch), and recent commits.
2. **Is it already tracked?** Look for a ticket key in the branch name, commit messages,
   or PR. If found, fetch that ticket and check it actually covers this work; if it's
   thin or out of date, go to Mode D. If none, search the tracker for an existing ticket
   that matches (Mode C's dedup search) before creating a new one.
3. **If genuinely untracked → draft a ticket (Mode B) and confirm** before creating.
4. After creation, note the ticket key back to the user (and suggest including it in the
   branch/PR/commit per their git conventions).

---

## Detailed mode procedures (topic files)

Modes B–E and the release gate live in topic files — read the relevant one:

- **[ticket-writing.md](ticket-writing.md)** — **Mode B** (the QA-ready ticket template) and
  **Mode D** (make a thin/technical ticket QA-ready). The reusable ticket format lives here.
- **[audit.md](audit.md)** — **Mode C** (audit existing tickets: already-implemented,
  duplicates, link & update; report-then-confirm).
- **[qa-feedback.md](qa-feedback.md)** — **Mode E** (triage QA testers' comments) and the
  **QA handoff & release gate** (don't move a ticket to QA/staging before it's live; notify,
  don't reassign).

---

## PM config (per project)

**File:** `<project memory dir>/pm-config.md` — wherever you keep per-project memory
(this install's path: `LOCAL.md` beside this skill, when your copy keeps one). Create on
first run; add a pointer line to that project's memory index (e.g. `MEMORY.md`).

```markdown
---
name: pm-config
description: Project-management tracker config for this project (used by /project-manager)
metadata:
  type: project
---

- **Tracker:** jira | trello | other
- **Site / board:** https://<your-site>.atlassian.net  (or Trello board URL)
- **Project key(s):** e.g. PORTAL
- **QA tester:** <name / account> to assign or add as watcher on new tickets
- **Issue types in use:** Bug, Story, Task, ...
- **Status workflow:** Backlog → To Do → In Progress → In Review → In Staging → Done
- **Label conventions:** <e.g. area labels, "needs-qa">
- **Notes:** anything tracker-specific (custom fields, required fields, components)
```

Keep this current — if you learn a new convention (a required field, the QA assignee,
a label scheme), update the config.

---

## Ticket lifecycle (status follows the work)

A ticket's status must track the work's real state — move it as the work moves, not in
batches later, so the board is trustworthy at any moment. A common convention (this
install's per-project workflow: `LOCAL.md` beside this skill, when your copy keeps one):

- Work starts → **In Progress**.
- PR opens → **Code Review** (also the correct status for merged-but-not-yet-deployed
  work).
- Deployed to staging → **In Staging** — only after the change is actually live there
  (release gate, [qa-feedback.md](qa-feedback.md)); never earlier.

These three forward moves are durably authorized for work done at the user's request.
Other projects: record their workflow in pm-config and follow it the same way.

## Working principles

- **Reconcile with reality, not vibes.** Tie every "implemented/duplicate" claim to
  concrete evidence (code, PR, commit, observed behavior).
- **Write for the tester, not the engineer.** Every ticket must be actionable by
  someone who can't read the code. Plain-language skill is mandatory for the prose.
- **Security by reach.** Multi-role features get explicit "lower tier must not be able
  to…" test bullets — mirror the user's internal-field-route-authority preference.
- **Confirm before mutating.** Drafts for creation, reports for changes. Ask when
  unsure.
- **Honor the user's git/workflow rules** when suggesting branch/PR/commit ticket
  references (own-branch, linear history, no AI attribution).

## Common failure modes — if you're about to do one of these, stop

- **Mutating the tracker without approval.** Any create/edit/transition/link/comment
  you didn't draft-and-confirm this session (and that isn't a durably pre-authorized
  lifecycle move you can name) violates the approval gate. Stop and ask first.
- **Collapsing a list into a count.** "Found 7 duplicates" is unusable — name EVERY
  ticket (key + title) in every report, roster, and audit result. The user requires
  each item enumerated, never summarized to a number.
- **Writing QA steps in engineer jargon.** "Hit the endpoint", "the modal renders",
  file paths in a title — a non-technical tester can't act on any of it. Route all
  tester-facing prose through the plain-language skill; that's what it exists for.
- **Assuming the tracker is Jira.** Different projects use different trackers; resolve
  pm-config (Step 0) before touching anything, and ask when it's missing.
- **Declaring a ticket "already implemented" from its title.** A verdict needs concrete
  evidence (commit/PR/file/observed behavior); without it you have a candidate to ask
  about, not a conclusion.
- **Pulling full descriptions in a broad JQL scan.** On busy projects descriptions blow
  the token budget — request minimal fields (`summary,status,issuetype,labels`) and
  fetch full detail only for the few real candidates.
- **Doing the ticket's work.** If the user wants the ticket implemented, that's a
  ticket-execution workflow's job — this skill only reconciles the tracker.

## Before you call this done

- [ ] Every tracker mutation this session was drafted/reported and approved first (or
      is a pre-authorized lifecycle move you named).
- [ ] Every ticket touched or reported is named by key + title — no collapsed counts.
- [ ] All tester-facing prose went through plain-language: exact navigation, numbered
      steps, expected result, no jargon.
- [ ] Multi-role features carry explicit "lower tier must NOT…" checks.
- [ ] Statuses reflect reality — nothing moved to QA/Staging before it's live.
- [ ] pm-config and LEARNINGS updated with any new convention learned.

## Related skills

- [planning](../planning/SKILL.md): a plan links to the ticket this skill makes sure exists.
- [plain-language](../plain-language/SKILL.md): every ticket title, description and QA step is written in its voice.

## Capturing learnings (session-handoff protocol)

Record reusable PM conventions in `LEARNINGS.md` beside this skill, when your copy
keeps one: per-tracker quirks,
the QA tester's preferences, ticket-template tweaks the user liked, label/field
conventions, recurring dedup patterns. Read before an audit. (Project-specific tracker
facts go in that project's `pm-config.md`, not here.)
