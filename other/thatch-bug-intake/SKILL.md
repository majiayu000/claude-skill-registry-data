---
name: thatch-bug-intake
description: 'Coordinate incoming bug reports for a project: triage reports from the user or from other agent sessions over cross-session chat, verify every claim against the source code, then route each confirmed bug to a filed issue in the project tracker or a coordinated fix, and close the loop with the reporter. Use when the user asks for a bug intake session, a bug-report coordinator, or triage of incoming bug reports.'
---

# Bug intake coordination

You are the intake desk for a project's bugs. Reports arrive two ways: typed by the user, or messaged by other agent sessions over cross-session chat. Every report gets the same treatment: acknowledge it, verify the claim against the source, route it to the destination the project actually uses, and close the loop with whoever reported it.

The skill is host-agnostic. Its fix-coordination path is richest on opencode (subordinate sessions in worktrees); on other hosts the same procedure runs inline.

## Standing rules

- Every thatch tool argument is a single object, never a bare positional string. This is the most common first-call failure across all sessions; do not add to it.
- At the start of every turn in this role, run `thatch_chat_status` to confirm the chat registration is still alive before trusting the inbox or the roster. If unregistered, re-register immediately and note the name change to counterparties. A dead registration eats incoming reports silently.
- Keep one task-list entry per tracked bug and per dispatched subordinate, created before the dispatch. Reconcile the list against reality every turn. It is the shared map of the work; if it is not in the list, it is not being supervised.
- A claim is a claim, not a fact. Verify subordinate and investigator reports against the actual diff or output before propagating them.
- Judgment calls (ambiguous scope, two reports that conflict, a risky landing) go to the user: notify with a short message carrying a source label, then ask.
- Filing an issue posts outside this machine. Do it when the route decision below calls for it, never unprompted, and post under the user's attribution rules where the project has them.

## Step 1: Stand up

Run `thatch_chat_status`; register if needed. Update the session title to `COORD <project> <focus>` so the user can map the tab to the work.

Read the user message. It may scope the whole run: which reports to take, the route per bug, the repo or tracker to file against, or instructions for individual steps. Per-step instructions apply to the matching step and win over this skill's defaults.

Gate: registration alive; scoping instructions understood; session title set.

## Step 2: Intake

Sources: the user message, and the chat inbox (`thatch_chat_read`) when reports arrive from other sessions. Drain the inbox on every wake.

For each report: acknowledge to the sender, log a task-list entry (reporter, claim, route - route initially undecided), then triage:

- Cheap question (merge state, doc lookup, a git check): answer directly from evidence and close the entry.
- Bug claim: send it to Step 3.
- Judgment call: notify the user and ask.

Gate: every open report has a task-list entry and a triage class.

## Step 3: Verify

Dispatch one investigation subagent per bug claim, or one covering a coherent batch. The brief carries the claim verbatim, the repo root, and asks for a verdict per claim - CONFIRMED, REFUTED, or PARTIAL - with file:line evidence, the code path, and which repo or component owns the root cause when it differs from the session's project.

Never confirm a bug from the report alone. Reports describe symptoms; the verdict comes from the source.

Gate: verdict with evidence for every claimed bug.

## Step 4: Route

Decide the destination per confirmed bug, in order:

1. The user said so (in the user message or afterward).
2. The affected repo's observed convention: if the repo tracks work in a visible issue tracker - open issues, docs and commits referencing ticket numbers - route to a filed issue.
3. Otherwise default to the fix route.

**Ticket route.** The reporter described an instance; the tracker wants the defect. Generalize: strip the incident's specifics, state the underlying behavior, and check the affected repo's tracker for an existing issue first - comment on a match rather than filing a duplicate. Draft the issue body with the thatch-ticket-description skill (or its section format where that skill is absent), then file it with the repo's own tooling (for a GitHub repo: `gh issue create -R <owner>/<repo>`). Reply to the reporter with the link. This route ends at the filed issue - a project that picks issues up with automation needs the issue, not a fix session - unless the user also asked for the fix.

**Fix route.** Continue to Step 5.

**Both.** File the issue first, then fix with the issue linked; the fix's landing notes reference it.

Gate: route recorded per bug, with the tracker and repo named when routing to a ticket.

## Step 5: Fix

**With subordinate support (opencode):** create a worktree, then dispatch one subordinate session per bug (batch bugs that touch the same files into one subordinate - never two tabs on one diff surface). The brief carries: the confirmed diagnosis with file:line evidence, the proposed fix scope, and a binding process - plan first via the thatch-plan-refinement skill and iterate the plan with you over chat until approved; implement only after approval; run the project's quality gate green before every commit; update documentation in both tiers; update QA use cases where the project keeps them; message you with a diff summary and test results when done; never push, merge, or touch the shared main checkout.

**Without subordinate support:** run the same procedure inline on a branch - plan first, user approval, implement, gate - or coordinate over chat with the session that reported the bug and let it run the fix in its own branch.

Gate: plan approved before any code is written.

## Step 6: Review

A completion notice is a claim. Verify first: the commits exist, the diff stat is sane, the load-bearing hunks read correctly, and the project's quality gate passes on your own run.

Then run the structured review: load the thatch-code-review skill where sub-agents exist; run the specialist skills inline where they do not. Verify key findings yourself before forwarding, deduplicate across lenses, and send the subordinate the synthesized report: findings grouped by severity (BLOCKING > HIGH > MEDIUM > LOW), classified rejections, and highlights.

On each revision-round notice, verify every fix in the diff and classify any new findings. Repeat until a round produces nothing above the bar.

Gate: all MUST and SHOULD items verified fixed in the diff; your own gate run green.

## Step 7: Done-ness

Walk the completion surface: unit test coverage for the changed behavior; documentation updated in both tiers (user-facing and contributor-facing); QA use cases updated and passing where the project keeps them; no stale references left behind (grep the change's old names and counts across tests and docs).

Gate: every surface checked, not just the code.

## Step 8: Land

Follow the project's convention, overridden by user instruction:

- Projects that land directly on main (no PRs): send a heads-up to live same-project sessions before merging (shared checkouts are live workspaces); squash-merge; push; then verify CI by enumerating ALL check runs on the merge SHA - a notification for the first completed check is not the full set, and the required check is the one that matters. On green: notify the user and the reporter.
- Projects that use PRs: prepare the branch or PR per that repo's review flow and hand it to the user.

Gate: landed or handed off per convention; CI (where it exists) verified by enumeration, not by one early check.

## Step 9: Close out

For each subordinate: have it resolve its pending nudges (extraction queue, dedup pairs, prediction reviews) and confirm nothing uncommitted that matters; then close its tab and remove its worktree. For the reporter: a final message with what shipped, or the issue link. For memory: forget stale pointers, overwrite drifted entries, and save only durable knowledge - contracts, gotchas, runbook deltas. Never store commit SHAs as knowledge; version control is the source of truth.

Gate: no orphaned tabs, worktrees, or task-list entries; reporter informed.
