---
name: review-code-tickets
description: "Find a code spec's Halt risks before a run: a reader that never wrote the tickets checks every one against the spec, the step permissions and the order, and reports each risk with quoted evidence and a fix or a spec-gap question. Takes /code-tickets' drafts or a spec's published sub-issues, as /review-code-tickets <repo> <n>."
disable-model-invocation: true
---

Finds the **Halt risks** ([`runner/GLOSSARY.md`](../../../runner/GLOSSARY.md)) in a code spec's tickets before the runner meets them. The reviewer never wrote the tickets, so a ticket its writer reads as clear still gets read **cold**, the way an implement step reads it: this session when it wrote none of them, else a fresh sub-agent on the session's model.

The review reports and never edits. Inside `/code-tickets` the writer acts on the report by its own step; run standalone, this skill acts on it by step 4.

## 1. Pin the input

The input is one of:

- **Drafts**: the scratchpad folder of ticket files `/code-tickets` hands over, one per ticket in the local-ticket template, with the spec's repo and number.
- **A published spec**: `/review-code-tickets <repo> <n>`. Read the spec with `npm run issue:read -- <repo> <n> --body --comments`, which also lists its sub-issues; read each sub-issue with `npm run issue:read -- <its repo> <m> --body --comments`. Read the edges, and what has landed or started, from `npm run runner -- status <owner/repo> <n>`: its `Landed`, `Current` and `Waiting` lines.

A ticket that has landed or is current is **report-only**: its risks are reported, and no fix is offered for it.

Done when the spec body, every ticket body and every blocking edge are in hand, and the report-only tickets are named.

## 2. Pick the reviewer

One reviewer takes up to 10 tickets. Past 10, split them into parts of up to 10, in ticket order, one reviewer per part.

- **This session reviews** when it wrote none of the tickets and there are 10 or fewer. Follow the brief below as your own, from what step 1 gathered.
- **Fresh sub-agents review** otherwise, one per part, and when this session wrote the tickets, as it always has inside `/code-tickets`. Each runs on the session's model with no `model` override, in the foreground. Each prompt gives the spec body, the ticket bodies, the edges and the brief below, and nothing of how the tickets were written.
- **The order pass runs past 10 tickets**, when no reviewer saw them all. Each part also returns, for each ticket, the files it changes and any gate or tier row it adds; then the order causes (4 and 9) are checked alone, from those lists, every title and every edge, by this session when it wrote none of the tickets, else by one more fresh sub-agent.

Before step 3, check each finding against the evidence it quotes, and correct or drop, saying so, any that doesn't hold.

<brief>

You are reviewing a code spec's tickets before the runner runs them. A **Halt risk** is a line in a ticket, or a gap in the ticket order, that would make a run Halt. Find every one.

**Read the current permissions yourself, every time; never work from memory of them:**

- `docs/claude-code-guardrails.md`, sections "The hooks and the project agent" and "The Bash sandbox": the step write rule, what the tier gate does in a step, and what the box denies. An Edit or Write inside the workspace passes, protected paths included; a Bash write under the workspace's `.claude/hooks` or `.claude/skills` (a `git rm`, `mv`, `chmod`, `sed -i`) fails in the box.
- `docs/targets-and-gates.md`, "Which tier an action is in": a tier-3 action is refused in a step.
- `runner/src/Workflow/code/implementStep.ts` and `runner/src/stepPrompts.ts`, the implement step's prompt lines: what a step may not do with branches, issues and blockers.
- `docs/agents/planning.md`, "Ticket size".

Resolve every path a ticket names, or implies by naming a skill, doc or symbol, to the file it lands on, symlinks followed: the rule applies to where the write lands, not to the name. Grep the names each ticket changes to count its files.

**The causes**, each with a Halt it once raised:

1. **Size**: over ~10 files changed, or over the ticket budget by `planning.md`'s estimate. (#597 split twice.)
2. **A live run a step can't make**: a criterion needs a command against a live target the ticket doesn't name, or one the gate refuses. (#221–#228 required a `dev:gen:configs` run.)
3. **A contradiction**: the ticket against itself, the spec, the existing tests or the implement step's rules. (#481 asked for 3 tries with 3 waits; #541 asked for `git branch -d`, which the step's rules forbid.)
4. **A gate change not yet on master**: the ticket runs a script, or uses a tier row, that a ticket of this spec adds; the gate loads from master, so a step sees it only once that ticket lands and the run relaunches. (#492 needed its own new `freeScripts` entry.)
5. **A denied write**: a write outside the workspace, `$TMPDIR` or `/tmp`, into `.git`, or a Bash write the box denies. (#561 `git rm` under `.claude/hooks`; #491 wrote `.runner/*.facts.json`.)
6. **A GitHub write the step can't make**: editing another issue's body, closing an issue, changing a triage label, or creating an issue. (#157 backlinked onto other issues.)
7. **A gap in the ticket's own rule**: an undefined term, a case the rule must decide but leaves open, or a guarantee the criteria claim but nothing enforces. (#250 left `clasp_config_auth` undefined; #227's `--force` had no address for a tab's own trait.)
8. **A hand check the gate refuses**: "check by hand once" or "first confirm" through a command a step can't run. (#470's `claude -p --model haiku` check.)
9. **An order gap**: two tickets editing the same files with no edge between them, or a ticket that needs another's output without being blocked by it. (#596 failed checks after #597 changed a message it asserted.)

**The specificity bar.** A ticket leaves the implementer every choice the code, the design docs and the code style settle, as `docs/agents/planning.md`'s "Ticket size" rule says, because the implement step "carr[ies] on with the reading the ticket best supports when the work can go on without it". Under cause 3 or 7, report only a contradiction, an undefined term, or a case the ticket's rule leaves open. A ticket with no file paths, names or shapes, or no "how", is as `/code-tickets` means it to be.

**Return**, for each Halt risk:

- the ticket, and the line quoted verbatim, or the edge that's missing
- the cause, by number
- the Halt it would raise: `denied-tool`, `gated-action` or `spec-ambiguity` blocker, Split Halt, or Failure Halt
- the evidence: the permission, spec or code line it conflicts with, quoted with `file:line`
- one of: **fix**, the change to the ticket or its edges, true to the spec; **spec gap**, the question only the developer can answer, which the spec leaves open; or **interactive split**, the part only a `ready-for-interactive` ticket can do

End with each ticket you found no risk in, by number. Under 300 words per five tickets.

</brief>

Done when the review, or every part and the order pass, has reported, and every sub-agent finding is checked.

## 3. Report

Present the Halt risks in three lists: fixes, spec gaps and interactive splits. Each list is ordered by ticket, and report-only tickets are marked. Then name the tickets with no risk, and give a count for each list.

For drafts, stop here and hand the report back to `/code-tickets`.

## 4. Act on it, standalone

1. **Spec gaps first**: put them to the developer as one round in the [`grilling`](../grilling/SKILL.md) format, each with a recommended answer. The answers can turn a gap into a fix or an interactive split. When an answer settles what the spec should have said, add a line saying so to the spec's body.
2. **Fixes and splits**: list each edit you would make (a ticket body, a blocking edge, a label, or a new `ready-for-interactive` ticket) and get the developer's one yes for the list. Then make them by the [issue tracker doc](../../../docs/agents/issue-tracker.md)'s operations. Make none on a report-only ticket. A new ticket's edges go through cause 9 like any other's before the list goes to the developer: it is blocked by each ticket whose output its work needs, and blocks each ticket that needs its output.

Done when every spec gap has an answer, every approved edit is made, and the edits made are listed with links.
