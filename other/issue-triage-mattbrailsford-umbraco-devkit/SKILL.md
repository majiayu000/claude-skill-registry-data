---
name: issue-triage
description: >-
  Triages one, several or all untriaged tracker issues: type, code area, duplicates and
  possible security reports, as a report for human review. Once approved, applies `state/*`
  labels and a plain-language comment for the reporter. A `decisions` run walks through
  issues waiting on a maintainer. Use to classify a backlog, or one issue before acting on
  it. Owns the plugin's state labels, its tracker comment format, and its rule for handling
  security reports.
user-invocable: true
argument-hint: [issue ID | ID range | decisions | leave blank for whole tracker]
---

# issue-triage

Read the room on a bug tracker before anyone commits to fixing anything. Classifies, checks
for duplicates, points at the likely code, and flags anything that smells like a security
report — then hands back a report. The tracker is the only record of what's been triaged,
and nothing is written to it until the user says so.

## Scope

- IN: fetch, classify, find the likely code area, duplicate-check, security-flag, report,
  draft a comment for the reporter, and apply the state labels, comments, or closes the user
  approves.
- OUT: any tracker write the user hasn't approved, proving a bug's cause, writing fixes,
  planning a feature. Once a triaged issue turns into real work, hand off to `issue-resolve`.

## Preflight

1. **Resolve the tracker.** Read `CLAUDE.md` for an `## Issue tracker` section (type,
   location, access method). If it's missing, run the interview below and append the section —
   don't guess a tracker or invent an API to call.
2. Note whether the tracker lives in this repo or elsewhere (a separate GitHub repo, a Jira
   project, an Azure DevOps org) — the `Location` line answers that. Every fetch uses it
   explicitly; never assume the tracker is wherever `origin` points.
3. Resolve the access method, in order of preference: an already-connected MCP server for that
   tracker type, else its CLI (`gh` for GitHub, `jira` CLI, `az boards`), else a documented
   REST call. Record whichever one actually worked in `## Issue tracker` so the next run skips
   this detection step.
4. Resolve the state label names: the defaults in State labels below, or the mapping
   `CLAUDE.md` records under `## Issue tracker`. If that section exists but has no `State
   labels` line, ask just the interview's state-labels question and add the line. If the
   mapping has no entry for one of the states, ask about just that state.
5. Resolve which issues this run covers, from the argument:
   - One ID → that issue, whatever its labels. Naming an issue means re-triage it.
   - A range (e.g. `120-135`) → every ID in that range that still exists and is open.
   - `decisions` → every open `state/needs-decision` issue, handled by the Decision run
     below instead of the normal dispatch.
   - No argument → every open issue with no state label, plus:
     - every `state/needs-info` issue the reporter has replied to since the label went on,
       or that has gone quiet for longer than the needs-info timeout;
     - every `state/blocked` issue whose blocker has since closed.

### Interview (only if `## Issue tracker` is missing from `CLAUDE.md`)

Ask in one batch:
1. **Tracker type** — GitHub Issues, Jira, Azure DevOps Boards, or other (name it).
2. **Location** — the repo/project/org identifier, and whether it's the same repo as the
   source code or a separate one.
3. **Access** — is there an MCP server already connected for it, or should this use the CLI or
   a token from the environment?
4. **State labels** — does the tracker already have labels or tags for triage state? If so,
   map them onto the states in State labels below. If not, may this create the default
   `state/*` ones? Creating them is a tracker write, so it waits for a yes.

Append the answers to `CLAUDE.md`:
```markdown
## Issue tracker
- Type: <type>
- Location: <repo/project/org — note explicitly if separate from the source repo>
- Access: <MCP server name | CLI command | REST endpoint>
- State labels: default   <!-- or a mapping, e.g. ready → status/accepted -->
- Needs-info timeout: 30 days
```

## The dedup pre-pass (only when more than one issue is in scope)

Parallel subagents in the same batch can't see each other's output, so run one cheap,
deterministic check first, before spawning anything: pull just the title (and error
text/stack trace, if the tracker's list view shows one) for every issue in scope, and
exact- or near-exact-match them against each other.
This is a literal text comparison, not a judgment call — flag pairs, don't resolve them.
Attach the flag ("possibly a duplicate of #N") to whichever subagent prompt(s) it applies to;
the subagent still investigates and makes the final call, since a matching title or stack
trace is a hint, not a fact.

## Dispatch

**One issue in scope:** dispatch a single `issue-triager` subagent (Agent tool,
`subagent_type: issue-triager`) and wait for its report.

**More than one:** the main thread is the orchestrator. It does not fetch, classify, or judge
any issue itself — it dispatches one `issue-triager` subagent per issue and only aggregates.
Batch the dispatches (parallel Agent tool calls in one message); cap concurrency around 8–10
at a time rather than firing the whole scope at once. For a large whole-tracker run, tell the
user the issue count and the batch plan before starting — a few hundred open issues means a
few hundred subagent calls, and that's worth flagging before it runs.

Every dispatch gets: the issue ID, the tracker's type/location/access method, the repo path,
any dedup-pre-pass hint for that issue, why it's back if it already had a state label (a
reply, the needs-info timeout, or a closed blocker), the "What counts" list from Security
reports below, the "Which state" rules from State labels, and the Tracker comments section.
The triager searches the tracker itself, open and closed, for earlier duplicates. It also
checks whether an open pull request is already linked to the issue (GitHub: the issue's
"Development" links or a cross-reference in its timeline), opened by the reporter or another
outside contributor, and reports it if so.

## Aggregating and reporting

1. Collect every subagent's report.
2. Pull anything flagged as a possible security report into its own short list, handled as
   Security reports below says.
3. Build one combined table for everything else: issue, type, likely area, priority/urgency,
   duplicate-of (if any), recommended action, one-line why (written following
   `plain-writing`). When a triager reports a linked open PR from the reporter or another
   outside contributor, the recommended action is "Review with `pr-review` #<PR>", not a
   state label or fix route — the fix already exists, it hasn't been built yet.
4. Next to each recommended action, show the tracker write it maps to (State labels below):
   the label or close, any type or area label fix the triager found, and the comment the
   triager drafted. A label fix is a tracker write like any other, applied only on approval.
5. Present the table and the security list (if non-empty) to the user. Nothing gets written
   back to the tracker until the user says which recommendations to apply. Then apply exactly
   those, and report what was written.

## Decision run

For issues triage has already sorted, where the only thing missing is the maintainer's call.
No subagents: the notes already hold the facts, so the main thread reads each issue itself.

1. For each issue in scope, read its latest `Notes for the decision` and everything posted
   since: new comments, reaction counts, newly linked duplicates.
2. Show one table: issue, need, size, risks, suggestion, and what's new since the notes. Put
   anything new that changes the picture (a lot more demand, a workaround someone found) in
   the suggestion, and say so.
3. Ask the user for an answer per issue:
   - **Yes** → `state/ready`.
   - **Yes, another way** → `state/ready`, with the other way as what was agreed.
   - **No** → close as not planned.
   - **Not yet** → no change, no comment. It comes back on the next decision run.
4. Draft each answer's label and comment, following Tracker comments below. Apply exactly
   the ones the user approves, as in Aggregating and reporting.

## State labels

The tracker holds triage state, so there's no separate log to commit or keep in sync. An open
issue with no state label is untriaged.

| Label | Means | Set by |
|---|---|---|
| `state/needs-investigation` | Looks real, but nobody has proven it yet | `issue-triage` |
| `state/needs-info` | Waiting on the reporter for detail only they can give | `issue-triage`, `investigate-bug` |
| `state/needs-decision` | Clear, but waiting on a maintainer to agree to it | `issue-triage` |
| `state/blocked` | Can't be fixed here until something outside the project changes | `issue-triage`, `investigate-bug` |
| `state/ready` | Verified and ready to fix | `issue-triage`, `investigate-bug` |
| `state/in-progress` | A fix lane has started | `issue-resolve` |

**Already fixed?** Check this first. If a merged change already fixes the issue, it gets no
state label:

- The fix is in a release that has shipped → close it as fixed, with the "Already fixed"
  comment below naming that version.
- The fix is merged but no release has it yet → leave it open, and draft the "Already
  fixed" comment without the close, naming the change. With no state label it comes back on
  the next run, which is when to check whether the release has shipped.

**Which state.** Pick the first that fits:

1. `state/needs-info` only when the missing piece is something only the reporter can give:
   their steps, versions, setup, data, or what they expected. Don't use it for anything that
   reading the code or trying a repro could answer. That's investigation work, not the
   reporter's. Before asking them to go check something (a log message, a setting, a response
   body), confirm in the code that it's actually there to find. A question built on an
   unchecked assumption ("there's probably something in the log, can you check?") wastes the
   reporter's time if the code never logs it.
2. `state/blocked` when the fix can't happen in this project until something outside it
   changes: a CMS bug with no package workaround planned, or a dependency's release. Link
   what it's waiting on. If a workaround in the package is planned, it isn't blocked.
3. `state/needs-decision` for a feature request, or a change to how something is meant to
   work, that's clear enough to plan but that nobody has agreed to do. Triage doesn't make
   that call. The user can make it while approving the report: yes means `state/ready`, no
   means a close as not planned. The label is for when they don't decide yet.
4. `state/ready` only when there's nothing left to prove or decide. A bug is ready once
   `investigate-bug` has proven its cause, or when the report and the code together leave no
   doubt (a wrong label, a broken link, an error message pointing at the exact line). A
   feature request is ready once it's been agreed and has enough detail to plan.
5. `state/needs-investigation` for any other real-looking bug. When in doubt between this and
   `state/ready`, pick this. `investigate-bug` moves it on: to `state/ready` once the cause
   is proven, to `state/needs-info` if only the reporter can fill a gap, or to a close if it
   isn't a bug.

- An issue carries one state label at a time. Setting one removes the others.
- Duplicates and issues to close don't get a label. Close them with the tracker's own reason
  (duplicate, not planned) where it has one, plus a comment naming the duplicate or the why.
- Every label change and close gets a drafted comment, as Tracker comments below says.
- A `state/needs-info` issue with no reply from the reporter for longer than the
  `Needs-info timeout` in `## Issue tracker` (30 days if it isn't set) gets a drafted close
  as not planned.
- A fixed issue leaves the label set through closing. The close is the record.
- Use the label names recorded in `## Issue tracker` when the project maps these onto its own.
  Never invent a label the tracker doesn't have; create one only with the user's yes.

## Tracker comments

This section is the plugin's one statement of how to write to an issue. `issue-triager`,
`investigate-bug`, and `issue-resolve` all point here.

Triage is also how the reporter hears back. Every label change or close gets one comment,
drafted for the user to approve, with up to two parts, in this order:

1. **For the reporter.** Written following `plain-writing`, for someone who
   uses the package but has never seen its source. Leave it out when someone on the team
   opened the issue. Cut it down to what's new when a maintainer has already told the
   reporter the same thing in a comment; never post a second version of their reply. No file paths, class names, or stack
   frames unless the reporter used them first. Say what was understood, what happens next,
   and what's needed from them, if anything. Thank them where it fits. Never promise a fix
   date or a release.
2. **Notes.** The technical record for whoever picks the issue up next; without it, the
   findings are lost when the chat ends. Each outcome below gives the notes' title and
   fields. Fold the notes away where the tracker can, so the reporter sees one line they can
   skip: on GitHub, a `<details>` block with `<summary><title></summary>` and a blank line
   after it, so the Markdown inside still renders. Where the tracker has no collapsible
   block, use the title as a heading.

Rules for the notes:

- Every field comes from something actually checked. Write "none found" or "not checked"
  rather than leave a field out or guess at it.
- Add only what's new since the issue's last notes. Link back to them rather than repeat
  them.
- They're public even when folded, so leave out roadmap, commercial, or customer detail.

### By outcome

**`state/needs-info`**
- Reporter: exactly what's missing and why it's needed, asked as questions they can answer
  without the code (steps, versions, a screenshot, a log message and where to find it),
  checked as "Which state" says.
- Notes, `Notes for the next look`:
  - **Known so far:** the symptom and setup as reported.
  - **Checked:** what triage or investigation already looked at, and what it ruled out.
  - **Missing:** each question asked, and what its answer would rule in or out.
  - **Likely area:** from a search of the code, or "none found".

**`state/needs-investigation`**
- Reporter: it's been read and will be looked into, but isn't confirmed as a bug yet.
- Notes, `Notes for the investigation`:
  - **Symptom:** expected versus actual, quoting any error word for word.
  - **Where it runs:** CMS version, package version, database, browser, as reported.
  - **Likely area:** from a search of the code, or "none found".
  - **Related:** similar issues, open or closed, and how they differ.
  - **Start with:** the first thing to check, and why.

**`state/needs-decision`**
- Reporter: the request is understood and waiting on a maintainer's decision. Don't hint at
  the answer; the suggestion goes in the notes.
- Notes, `Notes for the decision`:
  - **Need:** what the reporter is trying to do, which may differ from the feature they
    asked for.
  - **Demand:** linked duplicates and related issues, and their reaction counts.
  - **Today:** any workaround, setting, or extension point that already gets close.
  - **Already covered:** whether the CMS or another package does this.
  - **Size:** small, medium, or large, with the code area it would touch.
  - **Risks:** a breaking change, new public API to maintain, work on each supported CMS
    major, a performance cost.
  - **Other ways:** a smaller or different way to meet the need, such as an extension point.
  - **Questions first:** anything to settle before it could be planned.
  - **Suggestion:** do it, do another way, or don't, with the one or two reasons that weigh
    most. Label it as a suggestion; the maintainer decides. Word a "don't" kindly, since the
    reporter can read it.

**`state/blocked`**
- Reporter: what it's waiting on, with a link, and that it moves once that's fixed.
- Notes, `Notes on the blocker`:
  - **Waiting on:** the upstream issue or release, linked.
  - **Why here can't fix it:** the cause, and why it sits outside the project.
  - **Workarounds weighed:** each one, and why it wasn't planned.
  - **Unblocked when:** the version or change to watch for, and how to check it landed.
  - **Then:** what's left to do here once it has.

**`state/ready`**
- Reporter: it's confirmed, what was found in plain terms, and that it's queued for a fix.
  For a feature request, that it's agreed. If it was agreed another way, say plainly what
  will be built instead and why.
- Notes, `Notes for the fix`. For a bug:
  - **Repro:** exact steps, or the test that shows it.
  - **Cause:** the cause, at file and line, and the check that proved it.
  - **Same cause elsewhere:** each place, or "none found".
  - **Suggested fix:** one or two lines, and the test that should guard it.
  - **Size:** a quick fix or the full pipeline, and why.
- For an agreed feature request:
  - **Agreed:** what the maintainer said yes to, and anything they ruled out.
  - **Scope:** what's in and out, and the code area it touches.
  - **Questions left:** anything still to settle while planning.

**`state/in-progress`** (drafted by `issue-resolve`)
- Reporter: work on a fix has started.
- Notes, `Notes on the work`:
  - **Route:** a quick fix or the pipeline, and why.
  - **Where:** the branch, and the plan folder if there is one.
  - **New findings:** anything learned since the ready notes, such as `investigate-bug`'s
    report if it ran just now.

**Fix landed** (drafted by `issue-resolve`)
- Reporter: what changed, in their terms.
- Notes, `Notes on the fix`:
  - **Change:** the commit or PR, linked, and the area it touched.
  - **Verified by:** the repro run through the real entry point, and its result, or "not
    verified end to end" and why.
  - **Guarded by:** the test that now covers it.
  - **Left out:** anything deliberately not fixed, and any follow-up issues.

**Already fixed**
- Reporter: it's fixed, and the version to upgrade to. If no release has it yet, say it's
  fixed and will be in an upcoming release, without promising a date.
- Notes, `Notes on the fix`:
  - **Change:** the commit or PR that fixed it, linked.
  - **Released in:** the version, or "not released yet".

**Duplicate**
- Reporter: a link to the earlier issue to follow instead.
- No notes. Add anything new this report showed to the earlier issue instead.

**Close**
- Reporter: why, kindly. For a support question, answer it or point to the docs or forum.
  For a feature request turned down, give the reason and any workaround that exists today.
- Notes, `Notes on the close`, only when it was looked into:
  - **Checked:** what was tried, such as the setup it failed to reproduce on.
  - **Reopen if:** what new detail would make it worth another look.

**Needs-info timeout close**
- Reporter: there was no reply, so it's closed for now, and replying with the detail will
  reopen it.
- No notes. The needs-info notes already say what's missing.

A security report never gets a comment (Security reports below).

## Security reports

This section is the plugin's one statement of this rule. `issue-triager`, `issue-resolve`,
and `investigate-bug` all point here.

**What counts.** An issue or symptom that reads like a real vulnerability: auth bypass, an
action allowed without permission, data shown to someone who shouldn't see it, injection or
injected script running, secret or credential exposure, remote code execution, a CVE
reference, or similar.

**What to do.**

- Stop. Don't triage, investigate, or fix it as normal work.
- Tell the user, naming the issue but not detailing it, and point them at the
  responsible-disclosure process.
- Never put it in a public commit, PR, comment, or issue, and never draft a public response
  to it. A public reference to an unpatched vulnerability is a leak, not a fix.
- Never quote exploit detail into a report, log, or plan file.
- Never label it, in this tracker or any other public place, and never record it in a file.
  The chat is the only place it appears. With no label, it stays untriaged and gets flagged
  again on the next run, which is the reminder that it's still open.

## Rules

- Read-only against the codebase. The only file this skill writes is, on first run only, the
  `## Issue tracker` section of `CLAUDE.md`. The tracker is written to only as the next rule
  allows.
- Never post a comment, apply a label, or close an issue without the user picking that action
  explicitly — issue by issue, or as a stated "apply all." A draft is the default output, not
  an action.
- If the tracker is unreachable (auth, network, wrong location), stop and say so. Don't triage
  a stale cached copy or guess at an issue's content.

## Hand off

A triaged issue that turns into real work goes to `issue-resolve` next, with its ID. That
picks `quick-fix` or the pipeline, and drafts the tracker reply once the fix lands. A
`state/needs-investigation` issue can go to `investigate-bug` first instead, to prove it
before anyone commits to a fix. An issue with a linked open PR goes to `pr-review` with that
PR number instead — name the skill explicitly, never a generic "review the PR(s)", since a
busy install can drop skill descriptions from the listing and a bare mention won't route. To
work the whole tracker through to ready, `issue-backlog` runs triage, decisions, and
investigations in order. This skill stops at "here's what I'd do," it doesn't start building.
