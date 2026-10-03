---
name: postmortem
layer: method
description: At the close of an epic (or a difficult issue), post a postmortem roundup comment — what went well, what was hard (backed by evidence), and 1–3 concrete proposals to improve the skills/flows — then offer to turn accepted proposals into their own `workflow`-labeled tasks, and end with a `🔭 Next` handoff (a paste-ready next-session prompt + the next epic to start). Use at epic close, after the "verify the whole thing" rollup, or when asked to "do a retro", "postmortem this epic", "what did we learn", "how do we improve the workflow".
allowed-tools: mcp__github__issue_read, mcp__github__add_issue_comment, mcp__github__issue_write, mcp__github__sub_issue_write, mcp__github__list_issues, mcp__github__search_issues, mcp__github__list_commits, Read, Bash
---

# Postmortem — learn from the epic, tighten the loop

Turns a just-finished epic (or a difficult issue) into a short, honest **retro
comment on the epic**, plus an offer to spin the good ideas into tracked
`workflow` tasks. The point isn't ceremony — it's that **the loop only gets
tighter if we feed each run's friction back into the skills and flows**. See
epic #403.

This runs **after** the `github-tasks` "## 🧪 Verify the whole thing" rollup
(verify = *does it work?*) and **before** the epic is closed (postmortem =
*how did building it go, and how do we improve?*).

## When to use
- **Default:** at epic close, once all sub-issues have merged.
- A single **difficult issue** worth a retro on its own (lots of blocks, re-work).
- On ask: "do a retro / postmortem on #NN", "what did we learn".
- **Skip** for a trivial chore — not every issue needs a retro.

## What it produces
A single **comment on the epic** (`add_issue_comment`) with three sections, and
— on your go-ahead — one or more new issues labelled `workflow`.

## Step 1 — Resolve scope
- Input is an **epic number** (default) or a single issue number.
- Read it + its children: `issue_read` (`get`, `get_sub_issues`). Note which
  children merged cleanly vs. needed re-work.

## Step 2 — Mine the difficulty signals (evidence, not vibes)
For each child issue (and its PR), pull what the available tools can give. Each signal
below lists **how** to get it and how **precise** it is — be honest about the gaps, and
**never imply a measurement you didn't make**.

| Signal | How to get it (GitHub MCP) | Precision |
|---|---|---|
| **Time-in-progress** | `get_sub_issues` → per child `created_at` → `closed_at` | rough (proxy for build effort) |
| **Sign-off rounds** | `issue_read get_comments` on the child's PR → count revisions on the `<!-- ui-proposal:* -->` / `<!-- schema-review:* -->` sticky thread + review replies | good (markers are explicit) |
| **Asked-for-help / blocks** | `get_comments` → count `@`-mention + "blocked" comments; `get_labels` → is `status:blocked` still on it | good for *count* |
| **Blocked duration** | not exposed directly (label add/remove timestamps aren't in these MCP methods) → approximate from the gap between the blocking comment and the resuming comment | weak — **state it's an approximation** |
| **Re-work / commit churn** | `list_commits` on the PR branch → many "fix"/"oops" rounds = friction | available now |
| **Fix-bot attempts** | the `claude/issue-*` retry count (from #336 watch-to-merge) | only when #336 is live → say "n/a" otherwise |
| **Reopens** | `issue_read get` per child → reopened-after-close | approx |

Aggregate into **3–5 "what was hard" lines**, each tied to a specific child + its signal.
Prefer a few true signals over a complete-looking guess; where a signal is unavailable,
write "n/a (not measurable with current tooling)" rather than inventing a number.

## Step 3 — Write the roundup comment
Keep it terse and human-first (the `github-tasks` two-audience convention). Three
sections:

- **✅ What went well** — what was smooth / worth keeping. Name it concretely.
- **⚠️ What was hard** — the friction, each line tied to a signal or a specific
  issue (e.g. *"#NN sat blocked 3 days waiting on a sibling; the schema gate took
  2 revision rounds"*).
- **🔧 Proposals (1–3)** — concrete, actionable changes to a **skill / agent /
  flow** that would remove that friction next time. Each proposal = a candidate
  `workflow` task with a one-line "why".
- **🔭 Next** — the handoff (composed in Step 6): the next epic to start + a
  paste-ready next-session prompt. End the roundup with this so it's the first
  thing visible when the epic is reopened.

**Lead the comment with a machine-readable marker** so automation can detect that
this epic has had its postmortem without parsing the prose. Put it on the very
first line (it's an HTML comment — invisible in the rendered view, present in the
raw body via the API):

```
<!-- postmortem:done epic=#NN -->
```

The "ready to close vs needs postmortem" labeller (#763, `label-ready-epics.mjs`)
greps the epic's comments for `postmortem:done`: present ⇒ `status:ready-to-close`,
absent ⇒ `status:needs-postmortem`. Use the real epic number for `#NN`.

Post it with `add_issue_comment` on the epic.

**Flip the labels immediately (don't wait for the daily cron).** Right after posting,
add `status:ready-to-close` and remove `status:needs-postmortem` on the epic
(`issue_write` / label tools) so the review queue updates *now* — `label-ready-epics`
stays as the daily safety net. The epic is then closeable by the owner simply commenting
**`/close-epic`** on it (`close-epic-on-comment.yml` closes it, gated on the
`status:ready-to-close` label, #856) — surface that in the `🔭 Next` handoff so they know
the one-gesture close is available.

## Step 4 — Dedup against existing follow-ups, then offer to turn proposals into work

**First, dedup — don't mint duplicates.** Before proposing anything new, search for an
existing home for each proposal: an open follow-up / "harden X" **epic** or issues that
already capture it. Use `search_issues` with the proposal's keywords (and `label:epic`),
and check the source epic's own linked follow-ups. If a proposal is already tracked,
**link to that issue/epic in the roundup instead of opening a new one**; add only a
*genuinely-new* proposal to that epic as a sub-issue (`sub_issue_write`). The roundup
should state, per proposal, **where it's tracked** (existing #NN, or "new").

> Why this matters: the #274 dogfood found its proposals already lived in epic #291 —
> the right move was to link #291, not open parallel `workflow` issues.

Then ask the human (plain): *"Open the remaining (untracked) proposals as `workflow`
tasks?"* On a yes, for each accepted, **not-already-tracked** proposal create an issue
with `issue_write`:
- Labels: **`workflow`** + **`meta:agents`** + one `type:*` (usually `type:chore` or `type:feat`).
- Body: the proposal as a small **hypothesis** (what we change, why, how we'll know it helped). Reference the source epic.
- If several relate, group them under a small tracking parent via `sub_issue_write`.

Don't open issues the human didn't accept; don't pad with filler — 1–3 real ones beat ten
generic ones; and **never open a `workflow` issue that duplicates an existing follow-up
epic** — link it instead.

## Step 5 — Propagate the change to neighbouring issues

The epic's decisions often land on *other* tickets — a sibling epic, a consumer, something it
supersedes. Tell them, so nobody works around a change they didn't know happened.

- **Find neighbours:** issues/PRs referenced by the epic, its sub-issues, and their PR bodies;
  plus a keyword `search_issues` on the change (reuse the Step-4 dedup search).
- **Open neighbour → always comment:** one line of *what changed for you* + the link
  (e.g. "#515's release now wires to this App — see #NN"). This is how live work wires *into* the
  change instead of around it.
- **Closed neighbour → comment ONLY if the change supersedes/contradicts what it decided** — a
  terse "superseded / updated by #NN" forward-pointer for later archaeology. **Never** for mere
  topical relevance (dead-ticket noise).
- Keep it to the genuinely-affected few — a couple of true cross-links beat ten tangential
  mentions (same spirit as the Step-4 dedup). Each comment carries the `🤖` provenance header and
  is informational (won't trip agent-resume triggers).

## Step 6 — Hand off the next session (the `🔭 Next` block)

A postmortem must not dead-end — it points at what to do next, so there's no "now what?" gap
between sessions (#615). Compose a **`🔭 Next` block** and include it as the closing section of
the Step-3 roundup (so it's visible the moment the epic is reopened), **and echo the same block in
your chat reply** so it can be pasted straight into a new session.

1. **Pick the next epic.** From the initiative tree this epic belongs to (e.g. the `[Initiative]`
   parent) and the open `label:epic` list, choose the most sensible next one:
   - prefer an **unblocked sibling under the same initiative** (no open `Blocked-by:`), then the
     highest-priority open flow epic;
   - skip epics already in progress with an owner.
   State the choice + a one-line **why**. If there's **no obvious next epic**, say so and offer
   2–3 candidates rather than guessing.
2. **Emit a paste-ready prompt.** A fenced block a human can drop into a fresh session, containing:
   - **CONTEXT (done, don't redo):** 2–4 lines — what this epic delivered + any live state the next
     session needs (branch, preview URL, an open PR left as a testbed).
   - **NEXT:** the chosen issue `#NN` + its full URL, and "read it first, then propose a short plan".
   - **RULES:** ISSUE-FIRST · `/commit` skill, reference `(#NN)` · PRs not direct-to-`main` · never
     touch `packages/` without approval · deploy STAGING only.
3. **Post + echo.** The `🔭 Next` block is the last section of the roundup comment (Step 3); repeat
   it verbatim in the chat reply.

Then **report:** the epic comment URL, the `workflow` issues opened (with URLs), the neighbour
issues cross-linked, and the chosen next epic. This closes the learning loop *and* opens the next —
the proposals are on the board, the change is wired to everything it touches, and the next session
has a runway.

## Conventions & gotchas
- **After verify, before close.** Don't close the epic until the postmortem is
  posted (the `github-tasks` epic-close walk-up sequences this).
- **Headless = no dialogs.** If running unattended, post the roundup + proposals
  and @mention the owner rather than blocking on a prompt; the owner converts
  proposals to issues by replying.
- **Bot-comment filter.** The roundup is informational; it should not itself
  trip the agent-resume triggers (`resume-on-comment.yml` ignores bot authors).
- **Signals are best-effort.** Prefer a smaller, true set of evidence over a
  complete-looking but guessed one.
- **Dedup first.** A proposal already owned by a follow-up/hardening epic gets a
  link in the roundup, not a fresh `workflow` issue (proven by the #274 dogfood,
  whose learnings already lived in #291).
