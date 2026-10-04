---
name: wayfinder
description: >
  Chart a too-big effort as a shared map of decision tickets on the Gaia headquarters
  issue tracker, then resolve them one at a time until the way to the destination is
  clear. Use when someone says: "this is too big for one session", "chart a map",
  "wayfinder map", "plan this effort", "what do we need to decide first", "open a
  wayfinder", "work the map", "what's on the frontier", or /wayfinder. Covers any
  gaia-research org repo — gaia-skill-tree, gaia-research, gaia-skill-heaven and beyond
  — but every map and every ticket lives on ONE tracker: gaia-research/gaia-skill-tree.
  This is cartography (planning an effort as decisions), NOT triage of an existing
  backlog — for that use /gaia-triage.
disable-model-invocation: true
---

# wayfinder (Gaia)

This is the Gaia expression of Matt Pocock's `wayfinder` skill. Upstream is deliberately
tracker-agnostic: it says *"the issue tracker should have been provided to you… consult
the tracker doc's 'Wayfinding operations' section for how THIS repo expresses them."*

**This file is that document.** Upstream owns the method; this file pins down the
mechanics — where maps live, how tickets are created and nested, how blocking is
expressed, how the frontier is queried, how a ticket is claimed, how a resolution is
recorded. Read the upstream SKILL.md for the method
([mattpocock/skills → engineering/wayfinder](https://github.com/mattpocock/skills/blob/main/skills/engineering/wayfinder/SKILL.md));
read this for how Gaia does it.

Wayfinder is **cartography**: planning an effort too big for one agent session as a map
of *decision* tickets, worked one at a time until nothing is left to decide. It is not
backlog hygiene and not issue resolution — see [Not this skill](#not-this-skill).

---

## 1. Headquarters — one tracker, many repos

**Every map and every ticket lives on the `gaia-research/gaia-skill-tree` issue tracker,
regardless of which repository the resulting code lands in.** There is no second map
tracker, and a map is never split across repos.

```bash
export GAIA_HQ=gaia-research/gaia-skill-tree      # headquarters — all wayfinder issues
```

Why: a map's whole value is that one issue holds the low-resolution view of an entire
effort. Efforts here routinely cross repo boundaries — a Skill Heaven benchmark decision
made in `gaia-research` changes door code in `gaia-skill-heaven` and registry vocabulary
in `gaia-skill-tree`. A map fragmented across three trackers is not a map.

### Target-repo tagging

A ticket in HQ can point at work landing anywhere in the `gaia-research` org. Say where,
on the ticket body, as the **first line**:

```markdown
**Target repo:** `gaia-research/gaia-skill-heaven`
```

Use a repo's full `owner/name`. Multiple targets are allowed (one line, comma-separated);
`n/a` is valid for a pure-decision ticket that lands no code anywhere. Minimum supported
scope is the big three:

| Target repo | What lands there |
|---|---|
| `gaia-research/gaia-skill-tree` | registry, CLI, site, curation, HQ itself |
| `gaia-research/gaia-research` | research lab, benchmarks, ledger, reports, Next.js site |
| `gaia-research/gaia-skill-heaven` | product monorepo — engine + per-harness doors |

Any other `gaia-research/*` repo is fair game; the convention is deliberately open-ended,
and nothing beyond the string needs to change to extend it.

**Cross-repo linking is by URL, not by number.** `#1648` inside an HQ issue resolves to
HQ. When referring to an issue or PR in another repo, write the full
`gaia-research/<repo>#<n>` form or a full URL — a bare number silently points at the
wrong repo.

---

## 2. Wayfinding operations (the tracker contract)

This is the section upstream defers to. Everything here is verified against the live map
**[Wayfinder map: Trust Magnitude recalibration backlog (post-Yggdrasil III)](https://github.com/gaia-research/gaia-skill-tree/issues/1636)**
(#1636), which is the reference implementation. Read it before charting your first map.

### 2.1 Create the map

One issue, labelled `wayfinder:map`, titled `Wayfinder map: <destination in a phrase>`.

```bash
gh issue create --repo "$GAIA_HQ" \
  --title "Wayfinder map: <destination in a phrase>" \
  --label "wayfinder:map" \
  --body-file map-body.md
```

Use `--body-file` with real newlines (repo convention — escaped `\n` in `--body` produces
a mangled issue). Verify after creating:

```bash
gh issue view <n> --repo "$GAIA_HQ" --json body --jq .body
```

The body uses upstream's five sections **exactly**, in this order — `## Destination`,
`## Notes`, `## Decisions so far`, `## Not yet specified`, `## Out of scope` — and ends
with the pointer line:

```markdown
---

Frontier tickets are linked below as they're created (see this issue's timeline / linked issues).
```

The map is an **index**: `Decisions so far` gists each closed ticket in one line and links
it; the detail lives in the ticket, never restated on the map. #1636's Notes section shows
the local register — it carries measured numbers, named root causes, and founder rulings,
because those are what every session working that map must load first.

### 2.2 Create a child ticket

Two passes: create, then nest. Titles are sentences that state the decision, not nouns
(`Determine cause of garrytan/gstack suite-component uniform undercount (16 skills, -3.67 each)`,
not `gstack undercount`).

```bash
gh issue create --repo "$GAIA_HQ" \
  --title "<the decision, stated>" \
  --label "wayfinder:research" \
  --body-file ticket-body.md
```

Ticket body:

```markdown
**Target repo:** `gaia-research/<repo>`

Part of #<map> (Wayfinder map).

**Blocked by:** #<n>, #<m>          <!-- omit the line entirely when unblocked -->

## Question this ticket answers
<the decision or investigation, stated so a fresh session can act on it cold>

## How to resolve
<the concrete route: commands, files, who to ask>

## Not this ticket
<the adjacent thing a reader will assume is in scope and isn't>
```

`## Question this ticket answers` is upstream's `## Question`; on a `task` ticket, title it
`## Decision this ticket resolves` (as #1648 does) — a task ticket earns its place by
unblocking a decision, and naming the decision keeps that honest.

### 2.3 Nest it under the map (hierarchy)

**Hierarchy is GitHub native sub-issues.** Verified working on #1636 — 6 sub-issues,
6/6 closed, `sub_issues_summary` reported by the API. Do not use task-list checkboxes for
hierarchy; they do not produce the parent/child relation.

Sub-issues take the child's **issue id**, not its number:

```bash
# resolve the child's id, then attach it to the map
CHILD_ID=$(gh api repos/$GAIA_HQ/issues/<child-number> --jq .id)
gh api --method POST repos/$GAIA_HQ/issues/<map-number>/sub_issues -f sub_issue_id=$CHILD_ID
```

Agents on the GitHub MCP server use `sub_issue_write` with `method: "add"` (`issue_number`
= the map, `sub_issue_id` = the child's id, again *not* its number).

### 2.4 Blocking — body convention, not a native edge

**Use the body convention. Verified, and it is a fallback, not a preference.**

Upstream prefers a tracker's native dependency relationship because it renders the frontier
visually. We do not have a usable one here:

- The GitHub MCP toolset these agents run on exposes sub-issue writes and nothing for issue
  dependencies — there is no blocked-by verb to call.
- `gh` ships no `gh issue dependency` command; reaching the REST dependency endpoints means
  hand-rolled `gh api` calls that the org's app installation does not currently answer.
- The live map #1636 wires no native blocking edges; its ordering is carried in prose.

So blocking is a line in the ticket body:

```markdown
**Blocked by:** #1643, #1600
```

Rules: HQ-relative `#<n>` (blockers are always HQ tickets — a blocker in another repo means
that work needs its own HQ ticket); one line, comma-separated; **omit the line entirely when
nothing blocks** — an empty or `none` value makes the frontier query below unreliable.
When a blocker closes, the blocked ticket does not update itself; the session that closes
the blocker edits the line, dropping the closed number, and deletes the line when it empties.

**Re-check this before trusting it.** If GitHub issue dependencies become reachable from
`gh` or the MCP server, they supersede the convention and this section should be rewritten
rather than kept alongside:

```bash
gh api repos/$GAIA_HQ/issues/1636/dependencies/blocked_by   # 404/403 ⇒ convention still stands
gh issue --help | grep -i depend                            # empty ⇒ convention still stands
```

### 2.5 The frontier query

The **frontier** is the open, unblocked, unclaimed children of the map. Because blocking is
a body convention, the query is two steps: ask GitHub for open unassigned children, then
filter on the `Blocked by:` line.

```bash
MAP=1636
gh api repos/$GAIA_HQ/issues/$MAP/sub_issues --jq \
  '.[] | select(.state=="open") | select(.assignee==null) | "\(.number)\t\(.title)"' |
while IFS=$'\t' read -r n title; do
  blockers=$(gh issue view "$n" --repo "$GAIA_HQ" --json body --jq \
    '.body | capture("(?m)^\\*\\*Blocked by:\\*\\* (?<b>.*)$").b // ""')
  open_blockers=0
  for b in $(echo "$blockers" | grep -o '[0-9]\+'); do
    [ "$(gh issue view "$b" --repo "$GAIA_HQ" --json state --jq .state)" = "OPEN" ] &&
      open_blockers=$((open_blockers+1))
  done
  [ "$open_blockers" -eq 0 ] && printf 'FRONTIER  #%s  %s\n' "$n" "$title"
done
```

Take the **first** frontier ticket in order unless the user named one.

### 2.6 Claiming

**Assign the ticket to yourself before any work** — the assignee *is* the claim, and an
open unassigned child is by definition unclaimed. Concurrent sessions work the same map.

```bash
gh issue edit <n> --repo "$GAIA_HQ" --add-assignee "@me"
```

Claim first, then read. A session that reads for ten minutes and then claims has raced.

### 2.7 Resolution

Four steps, in this order:

```bash
# 1. post the answer as a resolution comment
gh issue comment <n> --repo "$GAIA_HQ" --body-file resolution.md

# 2. close the ticket
gh issue close <n> --repo "$GAIA_HQ" --reason completed

# 3. append a one-line context pointer to the map's "Decisions so far"
gh issue edit <map> --repo "$GAIA_HQ" --body-file updated-map.md

# 4. drop this number from any "Blocked by:" line that names it
```

The map line takes the shape #1636 uses — **name**, number, gist, and where the work
landed:

```markdown
- **#1643 (closed):** Fixed the role-stripping regression — `role` no longer stripped from `buildMergedSkillMap()`. Landed in #1647 → `dev/yggdrasil-iii-newmeta` (`ff9ba51`). → #1648.
```

Refer to tickets **by name** in everything a human reads (narration, comments, the map's
prose). A wall of `#42, #43, #44` is illegible. The number rides inside the name; it never
stands in for it.

Then graduate any fog the answer sharpened into fresh tickets, clearing each graduated
patch from `Not yet specified`. If the answer shows a ticket sits past the destination,
**close it and add one line to `Out of scope`** — it never appears in `Decisions so far`,
which records only the route actually walked.

### 2.8 Labels

| Label | Meaning |
|---|---|
| `wayfinder:map` | The map issue itself. Exactly one per effort. |
| `wayfinder:research` | AFK — read docs/APIs/local resources to surface a fact a decision waits on. |
| `wayfinder:prototype` | HITL — build a cheap rough artifact to react to. |
| `wayfinder:grilling` | HITL — conversation. The default ticket type. |
| `wayfinder:task` | Manual work that must happen before a decision can be made. |

Every ticket carries exactly one `wayfinder:<type>` label. Stack ordinary repo labels on
top freely — #1637 is `tech-debt` + `wayfinder:task`, #1643 is `tech-debt` +
`wayfinder:task` + `trust-model`. Priority (`P0`–`P4`) is optional on a map ticket and
means what `/gaia-triage` says it means.

All six are declared in `.github/labels.yml`. **Never create a wayfinder label ad hoc** —
`labels-sync.yml` reconciles from that file with `skip-delete: false` on every push to
`main`, so an undeclared label is deleted off live issues at the next sync.

---

## 3. Charting and working a map

Upstream owns this; the short version, with the Gaia-specific hooks.

### Chart the map (one session, resolves nothing)

1. **Name the destination.** `/grilling` + domain modelling. The destination fixes the
   scope, so it is settled first.
2. **Map the frontier** breadth-first. If no fog surfaces — the whole journey fits one
   session — **stop and say so**; you don't need a map.
3. **Create the map** on HQ (§2.1): Destination and Notes filled, Decisions-so-far empty,
   fog sketched into `Not yet specified`.
4. **Create the tickets you can specify now** (§2.2), nest them (§2.3), then wire
   `Blocked by:` lines in a **second pass** — issues need numbers before they can name
   each other.
5. **Fire research subagents** for each `wayfinder:research` ticket, in parallel.
6. **Stop.** Charting hand-resolves nothing.

### Work through the map

1. Load the map — the low-res view, not every ticket body.
2. Run the frontier query (§2.5), take the first ticket, **claim it** (§2.6).
3. Resolve it. Zoom into closed tickets on demand; call the skills the map's `## Notes`
   names.
4. Record the resolution (§2.7).
5. Graduate fog; rule out-of-scope work out of scope.

**Never resolve more than one ticket per session**, except research tickets, which
parallelise.

**Fog or ticket?** The test is whether you can state the question precisely *now*, not
whether you can answer it now. Sharp-but-blocked ⇒ ticket. Not yet sharp ⇒ fog.

---

## 4. Gaia house rules that bind a map

- **Decisions of record live in `gaia-research/founder/RATIFICATION.md`**, not on the map.
  A ticket whose resolution changes a ratified decision does not edit RATIFICATION.md by
  itself: the delta rides the implementing PR (D9), and the resolution comment says so.
- **Programmatic-first.** A `wayfinder:task` ticket that mutates the registry resolves
  through `gaia dev` verbs. Hand-editing `registry/nodes/` is forbidden; so is
  hand-editing a `trustMagnitude` number. #1636's Notes say this out loud, and that is the
  pattern to copy.
- **A map is not a sprint.** `gaia-skill-tree`'s sprint-completeness rule bans closing a
  sprint by filing its own remainder as follow-ups. A map is the opposite artifact: it is
  *supposed* to keep graduating fog into new tickets. Do not use a map to launder a
  sprint's unfinished work — if it was in the sprint's scope, it stays in the sprint.
- **Founder rulings settle scope.** #1636 records one inline ("no separate Wayfinder ticket
  for this batch, #1600 stays the tracker"). Record rulings on the map where they change
  scope; that is what keeps the next session from re-litigating.
- **Frontend work stays human-gated.** A map ticket cannot merge a gated frontend PR.
  Resolving the decision is in scope; merging is not.

---

## Not this skill

| You want to | Use |
|---|---|
| Plan an effort too big for one session as decisions | **this skill** |
| Sort, size, prioritize, link, and assign an existing backlog | `/gaia-triage` |
| Take one triaged issue end-to-end to a merged PR | `/gaia-issue-resolver` |
| Rank registry skills needing review | `/gaia-meta-audit` |

Wayfinder charts unknowns. Triage sorts knowns. Keep them apart: a map that fills with
already-specified build slices has stopped being a map.
