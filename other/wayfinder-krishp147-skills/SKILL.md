---
name: wayfinder
description: Plan an effort too big for one session as a map of decision tickets (GitHub issue + sub-issues) and resolve them one per session until the way is clear, then hand off to divide.
disable-model-invocation: true
---

Adapted from Matt Pocock's `wayfinder` skill (MIT, see THIRD_PARTY_LICENSES.md); tracker, ticket types, ticket size, research output and the hand-off to `divide` differ.

An idea has arrived that no single session can hold, and the way from here to the **destination** is still fogged. This skill charts that way as a **map** on GitHub Issues, then works its **decision tickets** (questions answered by a decision, not slices of a build) one at a time until nothing is left to decide.

Naming the destination is the first act: it fixes the scope and shapes every ticket. It may be a spec, a decision to lock, or a change such as a data migration. The map fits any domain.

**Target repo** per the `next` skill's `BOARD.md`, Target repo section (`~/.claude/skills/next/` or, as the plugin, `kanban/next/`): resolve `origin` (this skill needs it on GitHub), `-R <o>/<r>` on every `gh` call, and on a fork ask which repo to write to before charting; `<o>/<r>` below is that repo. Effort spanning several repos → ask which one holds the map (the **home**, `<o>/<r>` below; map, tickets and register rows live there), resolve each other repo the same way and list its `<owner>/<repo>` in Notes.

## Plan, don't do

Each ticket resolves a decision; the map is done when the way is clear. The urge to start building means you've reached the map's edge: hand off (see [Hand off](#hand-off)). The map's **Notes** may override this for one effort; absent that, produce decisions, not deliverables.

## Refer by name

Every map and ticket is an issue, so it has a **name**: its title. In anything the human reads, use the name, with the link riding inside it (`[Pick the queue](https://github.com/<o>/<r>/issues/42)`), never a bare `#42`.

## The map

One GitHub issue labelled `wayfinder:map`, the canonical artifact. Its tickets are its **sub-issues** labelled `wayfinder:<type>`; any other sub-issue (a converted issue's existing children) is a build issue, never a ticket. The map is an **index**: it gists each decision and links the ticket that holds it, never restating the detail.

Body (open tickets are not listed; they are open sub-issues, found by query):

```markdown
## Destination

<one or two lines: what reaching the end of this map looks like>

## Notes

<domain; skills every session should call; standing preferences>

## Decisions so far

- [<closed ticket title>](https://github.com/<o>/<r>/issues/<n>): <one-line gist>

## Not yet specified

<!-- fog: in scope, not yet sharp enough to ticket -->

## Out of scope

<!-- ruled beyond the destination; never graduates -->
```

## Tickets

A ticket is a sub-issue of the map whose body is the question, sized to fit one session inside the smart zone (~75K tokens; `hooks/smartzone.py` from this skill set warns at that size when installed, but the figure applies without it):

```markdown
## Question

<the decision or investigation this ticket resolves>

Map: <map link>
```

Each ticket carries exactly one `wayfinder:<type>` label: `research`, `prototype`, `grilling` or `task`. `wayfinder:*` labels are the only labels a map or ticket carries: never `status:*`, never put them on the board. `next`, the `planner` agent and `meta-orchestrator` skip anything labelled `wayfinder:*`.

**Claim** a ticket by assigning it to yourself first, before any work (`gh issue edit <n> -R <o>/<r> --add-assignee @me`), so parallel sessions skip it. Open + unassigned = unclaimed.

**Blocking** uses GitHub's native issue dependencies, so the frontier shows in GitHub's own UI. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed tickets (sub-issues labelled `wayfinder:*` only).

The answer is never in the body; it's recorded on resolution. **Assets** made while resolving (prototypes, long findings): inline in the resolution comment, split over several comments when long; a committed file when the repo tracks that path. Never create a gist without a yes naming its content and destination: a secret gist is readable by anyone with the link. Never link an untracked file (e.g. under an excluded `skilleddocs/`) from GitHub: nobody else can open it.

### GitHub operations

The REST APIs take the issue's numeric `id` (`gh api repos/<o>/<r>/issues/<n> -q .id`), not its number.

```
gh label create wayfinder:<type> --color <hex> --force -R <o>/<r>        # before first use, every label incl. wayfinder:map
gh api repos/<o>/<r>/issues/<map>/sub_issues -X POST -F sub_issue_id=<id> # attach ticket to map
gh api repos/<o>/<r>/issues/<map>/sub_issues                              # list tickets (state, assignees, labels)
gh api repos/<o>/<r>/issues/<n>/dependencies/blocked_by -X POST -F issue_id=<blocker id>
gh api repos/<o>/<r>/issues/<n>/dependencies/blocked_by                   # blockers + their state
```

Colours (fixed so repeats are no-ops; none is a `status:*` colour from `BOARD.md`, so a ticket never reads as a board state): `wayfinder:map` `0052cc`, `wayfinder:research` `1d76db`, `wayfinder:prototype` `f9d0c4`, `wayfinder:grilling` `d93f0b`, `wayfinder:task` `c2e0c6`.

Dependencies API unavailable (404/403) → add a `Blocked by: #<n>` line per blocker to the ticket body and read those lines instead (the one place a bare `#n` is right: it is machine-read, not for the human). Say which mode the map uses in its Notes.

## Ticket types

**HITL** tickets resolve only through a live exchange with the human; never answer their side yourself. **AFK** tickets are driven by the agent alone.

- **Research** (AFK): surface a fact a decision waits on (docs, third-party APIs, knowledge bases, the web). Spawn a `general-purpose` subagent with web search; it returns findings, you post them. Long findings → an asset (see Tickets). No branches.
- **Prototype** (HITL): make a cheap, rough, concrete artifact to react to (outline, stub, sketch UI or logic) when "how should it look/behave" is the question. Its home is an asset (see Tickets); one that needs its own branch is out of scope here: ask the user.
- **Grilling** (HITL): the default. Call the Skill tool with `"grill-docs"`; pass the ticket name, quoted, as the subject and a ticket slug after it, so the transcript is `<date>-<ticket-slug>.md` and grill-docs' register rows cite the ticket in Source. grill-docs has already recorded the decisions: step 4 must not add rows again. The resolution comment gists the answers, linking the transcript only when it is committed.
- **Task** (AFK where possible, else a precise checklist for the human): manual work a decision is blocked on (sign up for a service, get access, move data to see its shape). The one type that *does*; it earns its place by unblocking a decision. Record what was done and any resulting facts (where credentials live, new URLs, row counts). A checklist for the human: post it, keep the ticket claimed and open, and end the session waiting; it resolves (facts recorded, closed) once the human reports it done, in this session if they reply or in a later one.

## Fog of war

Don't chart what you can't see yet. The **Not yet specified** section holds decisions you can tell are coming but can't phrase yet. Resolving a ticket clears fog ahead of it; graduate what's now specifiable into fresh tickets.

**Fog or ticket?** Can you state the question precisely now (not answer it)? Yes → ticket, even if blocked. No → fog. Don't pre-slice fog into ticket-sized pieces; one patch may become several tickets or none.

Not yet specified excludes what's decided, what's ticketed, and what's out of scope.

## Out of scope

The destination fixes the scope. Work beyond it is not fog: it goes in **Out of scope** and never graduates (it returns only as a fresh effort if the destination is redrawn). A ticket found to sit past the destination: **close** it and add one line to Out of scope (gist, why, link). It stays out of Decisions so far.

## Invocation

Two modes. **Never resolve more than one ticket per session**, research excepted.

### Chart the map

User invokes with a loose idea.

0. **Baseline**, as `consult-plan` step 1: open issues, roadmap doc, the decisions doc (found as `grill-docs` does), for every repo in a multi-repo effort (another repo's files from its local clone, else `gh api repos/<owner>/<repo>/contents/<path>`; cite its decisions as `<owner>/<repo> D<k>`). It is the context for every grill below (cite decisions as `D<k>`, or `ADR <n>` in an ADR folder). An open issue already covers this effort → ask now which, act at step 3: **convert** it (relabel `wayfinder:map`, remove every other label, take it off the board (Projects: `gh project item-delete <number> --owner <owner> --id <item>`, item id as in `BOARD.md`; label mode: removing `status:*` is enough), rewrite its body as the map with the old body kept verbatim under a final `## Original issue`; its existing sub-issues (`gh api repos/<o>/<r>/issues/<n>/sub_issues`) stay attached as build issues, labels and cards untouched, listed by name in Notes, and the hand-off's `divide` counts them as existing children) or **close** it once the map exists, with a comment linking the map, and write `Replaces: <its link>` in the map's Notes.
1. **Name the destination.** Call the Skill tool with `"grilling"` to pin it down. It fixes the scope, so settle it first.
2. **Map the frontier.** Grill again, **breadth-first**: across the whole space, surfacing the open decisions and the first takeable steps. **The whole effort fits one session** → no map needed; stop and ask the user how to proceed. No fog is not that: if every decision is specifiable now but together they exceed a session, still make the map (Not yet specified stays empty).
3. **Create the map** (label `wayfinder:map`), or convert the step-0 issue: Destination and Notes filled, Decisions so far empty, fog sketched into Not yet specified.
4. **Create the tickets you can specify now**, attach each as a sub-issue, then wire blocking in a **second pass** (ids must exist first). Write cross-references in that pass too, with real numbers: a placeholder `#<n>` auto-links to an unrelated issue.
5. **Fire research.** One `general-purpose` subagent per new `research` ticket, in parallel; post each one's findings as that ticket's resolution (see Work through the map, step 4).
6. Stop. Charting is one session's work; it hand-resolves nothing.

### Work through the map

User invokes with a map (URL or number), optionally a ticket. Without one, you pick.

1. Load the **map** body only, not every ticket.
2. Choose: the named ticket, else the first frontier ticket in sub-issue order. A named ticket assigned to someone else or blocked → say so and ask before going on. **Claim it** before any work.
3. Resolve it as its `wayfinder:<type>` label says (the body never states the type). Fetch related or closed tickets on demand; call any skills the Notes name.
4. Record: post a **resolution comment** (canonical), **close** the ticket, add a line to the map's Decisions so far. Non-grilling types whose resolution is a decision: if the repo's decisions doc exists (found as `grill-docs` does), also append a row in its format (next `D<k>` or ADR number, source = ticket link); facts stay in the resolution comment. A grilling ticket skips this: `grill-docs` already appended its rows.
5. Add newly surfaced tickets (create, attach, then wire). Graduate fog the answer made specifiable, removing it from Not yet specified. Rule out-of-scope tickets out rather than resolving them. Update or close tickets the decision invalidated.

Other sessions may be working unblocked tickets in parallel: re-read before editing the map body.

## Hand off

When no open tickets and no fog remain, offer `divide` on the map issue to turn the destination into session-sized board issues for `pair` or `meta-orchestrator`. On a yes (this overrides `divide`'s last step, which offers to close the parent later; the map is closed now, not offered):

- pass `divide` the map plus, as the target's detail, the decisions doc rows its tickets produced and each closed ticket's resolution comment (the map is only an index);
- divide says it fits one session → create one board issue at Todo (or reuse one: reopen the issue in the map's `Replaces:` note, else an open one covering it) with `Part of #<map>` and that detail, per `BOARD.md`; it stands in for the children below;
- a roadmap line for the map, or for the issue in the map's `Replaces:` note, gets the children (`#old → #a, #b`, divide's step 5);
- each new issue links back to the map in its body (divide's `Part of #<map>`), and carries no `wayfinder:*` label;
- multi-repo map: run `divide` once per repo, each piece created in the repo it changes (`-R` that repo, its board, its fork rule) with `Part of <o>/<r>#<map>` and, as detail, the home register rows it rests on; `## Handed off` names them as `<owner>/<repo>#a`;
- the map gets a `## Handed off` section listing them by name (divide's task list goes there);
- close the map: its planning is done, whatever happens to the board issues.
