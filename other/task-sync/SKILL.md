---
name: task-sync
description: Reconciles a planning-side task list against the engineering tracker it mirrors. Reads both, diagnoses the ways they have drifted apart — unfiled, duplicated, wrong parent, broken link, resurrected, field mismatch, off the tracker's own template — and then proposes, waits for approval, and only then writes. Nothing is written automatically. Where the read cannot be exhaustive it says so in the coverage line rather than implying it saw everything. Filing or updating one task belongs to /pm:task-publish. Triggers - "/pm:task-sync", "reconcile the tasks", "sync notion and github", "일감 동기화해줘", "노션 깃헙 맞춰줘", "정합화 돌려줘".
allowed-tools: AskUserQuestion, Bash, Agent, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-query-data-sources, mcp__claude_ai_Notion__notion-update-page, mcp__plugin_github_github__issue_read, mcp__plugin_github_github__issue_write, mcp__plugin_github_github__sub_issue_write, mcp__plugin_github_github__list_issues, mcp__plugin_github_github__search_issues
---

# task-sync — reconcile the planning list against the engineering tracker

**Part of a plugin.** The scripts this skill runs ship beside it under `${CLAUDE_PLUGIN_ROOT}`. If that path does not resolve, this file was installed on its own — stop and say the plugin itself is needed (`claude plugin install pm@byjunyoung`), rather than improvising what the scripts do.

Brings a planning-side task list and the engineering tracker that mirrors it back to the same state, every run. This is not a bulk create: it reads both sides, diagnoses how they drifted, and writes only **after** a proposal has been approved. **Nothing is written automatically.**

Where `task.mirror.type` is `none` there is no second side and nothing to reconcile. Say so and stop — that is the correct answer for a single-tracker team, not an error.

## Configuration

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/resolve-config.py --name pm-conventions.yaml \
  --need task.record.ref,task.link_property --authored task.contract.level,task.progress_source
```

With a mirror, `task.mirror.ref` belongs on that list too. A `null` named on stderr is a config gap, not a tracker problem — `/pm:setup` writes it. Stop on it rather than reconciling against a side that was never named.

## What "correct" means — every verdict rests on these

- **Matching runs on `task.link_property` and nothing else** — the property on the record holding the ticket's url, one to one. A back-link written in the ticket *body* is not trusted: it can point at a source that was already discarded, and that is exactly how past mis-matches, duplicates and resurrections happened.
- **The unit is one record to one ticket.** Where `task.hierarchy.parent_kind` is set, records map to tasks *under* a parent. **A parent relationship is never changed automatically** — propose it, report it, and change it only on an explicit approval.
- **Fields have owners.** `task.field_owner` says which side wins for each. A field not listed there is reported as a difference and left alone. "Two-way" means reading both sides to reconcile *existence, closure and duplication* — it does not mean copying every field back and forth.
- **Closed means closed.** A closed ticket, whatever the reason, and an archived record, are both terminal. **A terminal pair is never recreated.** Archive rather than delete on the planning side, so the id survives.
- **The backlog boundary** is whatever `task.status_map` maps the initial status onto. No milestone means backlog; a milestone arrives when work starts, at the level `task.hierarchy.milestone_on` names.
- **The version a task is tied to is the mirror's, copied rather than decided.** Where `task.properties.version` names a record property, it holds the milestone the task's ticket sits under, read at the level `task.hierarchy.milestone_on` names — under `parent`, the parent's milestone, with a task's own ignored and reported as the policy drift it is. A milestone the tracker uses as a backlog bucket is copied by name like any other: whether that counts as a version is the rule document's call, and a record that says *backlog* tells a reader more than a blank one. No milestone at all writes `task.properties.version_unset`. **Which records carry one:** every open record, filed or not, and every filed record whatever its state — a finished ticket's milestone is history worth keeping. A closed record that never had a ticket stays blank, because a placeholder on finished work reads as a decision still pending
- **Where `task.policy.doc` names a rule document, read it before the first write of the session.** It holds the tracker's own conventions, and where it disagrees with a default here or in the config, **it wins**. It is also what tells this skill which of the two rules below are live on this tracker. The mirror's adapter says how to fetch it; with the key null there is no such document.
- **The tracker's own template is what a ticket's shape is judged against**, where `task.template` names one. Read it with the rule document, before the first write. A ticket filed before the template existed, or by hand, or by an older version of these skills, sits there with headings nobody will revisit — the contract writer leaves everything it does not own byte for byte, so no later run reaches them. **This skill is the only thing that looks.** It looks and it reports; the sections hold prose somebody wrote, and rewriting them from here would be the bulk edit this whole design refuses.
- **Closing is not always this skill's to do.** Where the rules gate closing a parent on a person's sign-off — a comment, an approval, a named role — a close from here is reverted by whatever enforces them, and the reopen carries no record of why it was closed. Report it, say who can close it, and leave it open.
- **A ticket the tracker's own automation closed is not a decision.** Rules that close a ticket for going stale, or for breaking a convention, say nothing about whether the work is still wanted. The rule document names how such a close is marked; those never drive a record to closed on their own.
- **How far along a task is gets counted, never estimated.** Where `task.progress_source` is `contract`, the only progress figure either side may carry is the ticked fraction of the contract checklist — the one number that already exists on both sides of an approval. Dates come from the day something happened: the column moved, the first box was ticked, the last one was. **With `task.progress_source` null, or the property unnamed in `task.properties`, these diagnoses do not run at all** — a blank field is not a drift when nothing was configured to fill it, and a percentage invented to fill a gap is worse than the gap.

## When NOT to invoke

- Filling one record's context table → `/pm:task-draft`
- Filing or updating one task → `/pm:task-publish`
- Writing the requirements → `/pm:prd`

## The cycle

### 0. Scope

Ask, or take it from the argument.

- **everything** — the whole list. For whoever administers it
- **mine** — filtered to one assignee

**A narrower scope is safer.** Most of the damage this skill could do is to someone else's task, and scope is what prevents it.

### 1. Scan (zero writes)

Read both sides in full where the tools allow it.

- **The mirror** — list every task and parent with title, status, milestone and url, and which parent each task sits under — where `task.properties.version` is named, that parent is where a task's version is read. Confirm open or closed separately where the board's status and the ticket's state can disagree. **A board listing can truncate without saying so** — compare the row count against the limit you asked for, and treat equal counts as a partial read
- **The record side** — query the task list for title, project, group, priority, status, assignee, the link property, and `task.properties.version` where one is named

**Where an exhaustive query is not available**, fall back to search plus fetch: enumerate candidates with several differently-worded queries, dedupe, fetch each, and **keep only the rows whose parent really is the task list** — a search will happily return a sub-page or a row from another database. For a large list, fan the fetches out to sub-agents that each return compact JSON, so the main context stays clear.

**Then say what that cost you.** A relevance-ranked search has no "that was all" signal, so rows that matched none of the queries are simply missing, with nothing to indicate it. Misses are structural.

Wrongly *creating* or *closing* something is normally not, because duplicate detection reads the mirror and every write waits for approval — **but that protection is only as good as the mirror read.** Where the mirror listing truncated, a ticket that exists but was not returned reads as `unfiled`, and the proposal is to create the duplicate. So a partial read on the mirror side downgrades every `unfiled` finding to a candidate: confirm each one against the mirror directly before it goes in the proposal. So:

- **The coverage line in the result is mandatory** — how the read was done, and whether it was exhaustive
- **Where full reconciliation actually matters**, ask for an export of the task list and re-run against the file

Match each record to its ticket by the link property. Never match on the ticket body.

The calls for each side are in its adapter — read both before scanning. They also carry what each tool cannot do, which is what the coverage line reports.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.record.type} --role record
python3 ${CLAUDE_PLUGIN_ROOT}/_common/scripts/lib/adapter.py --name pm-conventions.yaml --kind trackers --type {task.mirror.type} --role mirror
```

It prints the file to read — the bundled one, or yours from `adapters.dirs` where you drafted one. **Exit 3 means no adapter exists for that type.** Stop and say so; `/pm:setup` drafts one from the tools connected on this machine. Do not improvise the calls. **Exit 4 means the adapter exists but answers for the other side** — a mirror-only file asked for the record, say. Stop the same way; 3b drafts the side that is missing. Say what it means in the person's words — "this tool isn't supported yet; `/pm:setup` can add it from what's connected here" — never the exit code or the file path.

### 2. Diagnose — a rule broken is a drift

| Kind | How it shows | What is proposed |
|---|---|---|
| Unfiled | Link property empty, status not terminal, project mapped | Create the ticket |
| Duplicate | The same task filed twice in the mirror | Keep one, close the rest, consolidate the link |
| Parent | Task orphaned, multi-parented, or under the wrong one | Offer the right parent — **never change it silently** |
| Broken link | The link property points at a dead or wrong ticket | Re-infer the pair from title and content, then correct the link |
| Resurrected | Ticket closed but record still open | Reconcile to closed. **Do not recreate.** Closed by the tracker's own automation rather than by a person → ask first, and say which rule closed it |
| Ahead of the mirror | Record terminal, ticket still open | **Report, propose nothing.** Where `field_owner.status` is `mirror`, this is what a finished spec waiting on engineering looks like — the normal state, not a drift. Only raise it when the ticket has been open long enough to look forgotten |
| Record deleted | Ticket exists, record gone | Ask. Work may be in progress, so never auto-close |
| Field mismatch | The owning side disagrees with the other | Correct toward `task.field_owner` |
| Progress stale | The record's progress differs from the ticked fraction of the contract checklist, or is blank where the ticket has one | Correct the record toward the checklist. **Where the checklist is the stale one** — boxes ticked before the work behind them actually finished — say which, and ask. Copying a number that was never true is how a task reads as done twice |
| Schedule blank | Work has started and no start date, or the pair is terminal and no end date — on either side | Fill it from the evidence: the day the column moved or the first condition was ticked, the day the last one was. **Never today's date**, which records only when this happened to run |
| Schedule past | The end date has gone by and neither side is terminal | **Report, propose nothing.** A date that slipped is a decision somebody has to make, and moving it here makes the slip disappear instead of surfacing it |
| Version stale | The record's version differs from the milestone resolved for its ticket, or is blank where it should carry one | Correct the record toward the mirror. **Never the other way** — a milestone is moved on the tracker, where the people planning the release can see it, and a version edited on the record is exactly what this row exists to catch. A parent whose milestone moved shows here once for every task under it; they go in one batch. **A value the record's property cannot hold is reported rather than written** — adding the option is a schema change somebody should make where they can see the whole list. **And judge a milestone that looks wrong for the ticket by the ticket's project label, never by its title** — a title naming one product on a ticket filed under another is the ordinary case, not a drift, and only where the label disagrees as well is it worth asking before the copy. Only runs where `task.properties.version` is named |
| Policy | Milestone on the wrong level, or a label the rules require that the ticket does not carry | Correct per `task.hierarchy`, and per the rule document where one is configured. **A label the tracker does not have is reported, never created** |
| Reads as internals | A title, or a sentence a person acts on, written in the vocabulary of the system rather than of the people who act on it | **Report, and name the way out.** `/pm:task-publish` rewords one ticket with a person watching. The same reword across a list is a bulk edit of sentences other people wrote, on one approval |
| Off template | The ticket's headings are not the template's — a section missing, a section the template never had, a different order | **Report, and name the way out.** `/pm:task-publish` fixes one ticket with a person watching. This skill does not, because the same edit across a list would rewrite a hundred tickets on one approval |
| Held by the rules | The tracker's enforcement has flagged the ticket — a violation, a decision it is waiting on | **Report, propose nothing.** It is waiting on a person, and that person is usually not the one running this |

### 3–4. Propose → approve, in two tiers

Group the proposed changes by how much damage a wrong one would do.

- **Confirmed one at a time** — creating, closing, deleting, merging duplicates, changing a parent, handling a deleted record. Each gets its own preview and its own "go"
- **Confirmed in a batch** — plain field updates such as a title, a priority or a version. One preview, one "go"

Only what was approved goes to step 5.

### 5. Apply

Run the approved changes and nothing else.

**Creating follows the same rules as `/pm:task-publish`** — the parent is resolved and confirmed rather than assumed, the ticket carries the configured title and labels, read once for whether the people who will act on it can read it too, the milestone lands on the level `task.hierarchy.milestone_on` names, and the link property is written back afterwards. A project with no entry in `task.label_map.project` is skipped, not guessed at.

This skill writes only a minimal ticket body and **does not add a link back to the record** — that is `/pm:task-publish`'s job, done with a person in the loop. Where such a link is already in the body, leave it: it is not used for matching and it is not removed either.

**An off-template finding is never applied here**, whatever was approved elsewhere in the run. It is in the table so that a drift nothing else can see gets seen. The list is what a person works through afterwards, one ticket at a time, with `/pm:task-publish` — which offers exactly this edit, with its own preview, its own "go", and a question for every piece of content that has to move. Turning the same list into a batch is how a hundred tickets get rewritten on one approval, and the difference between the two is the person who is watching.

**The contract is left empty here**, whichever level `task.contract.level` names. Done conditions and a QA checklist are drafted from the spec and the design with somebody watching, which is the opposite of what a bulk reconciliation is for — a plausible condition nobody agreed to gets built. `task.contract.allow_tbd` does not gate this path: closing the gap between two lists is this skill's job, writing the contract is not. Report every ticket created here as still needing `/pm:task-publish`, so an empty contract is visible rather than assumed filled.

### Result

```
[reconciled]
read      : {how} · coverage: {N rows surfaced, exhaustive or not}
created {n} · relinked {n} · resurrection blocked {n} · duplicates merged {n}
field-synced {n} · version-synced {n} · progress-synced {n} · skipped {n} · errors {n}
reported only: off template {n} · reads as internals {n} · held by the rules {n} · ahead of the mirror {n} · schedule slipped {n}
```

The coverage line comes first on purpose. A count with no coverage reads as "everything is now consistent", which is the one claim this skill cannot make on a partial read.

## Constraints

- **No automatic writes.** Diagnose → propose → approve → apply, always in that order
- **Never change a parent on your own.** Propose it and wait
- **Never recreate a terminal pair.** That is the resurrection this design exists to stop
- **Never close a parent where closing is gated on somebody's sign-off.** Name who can, and stop there
- **Never read an automated close as a cancelled task.** Ask, and say which rule closed it
- **Never rewrite a ticket's body to match a template.** The difference is reported and the person is pointed at `/pm:task-publish`, which does it one ticket at a time. This skill sees the drift precisely because nothing else does, and that is a reason to be careful with it, not licence
- **Never invent a mapping.** An unmapped project, priority or assignee is skipped and reported
- **Never write a version the tracker does not show.** The record copies the milestone; it does not propose one
- **Never state coverage you did not have.** Where the read was best-effort, the result says so
