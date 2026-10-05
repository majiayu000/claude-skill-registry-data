---
name: resume
description: Search briefs, erp tasks, erp notes and the wiki for prior context on a topic in one `search_all` call, then pick up a thread or start fresh. Trigger on:- resume, continue prior work, what do we know about, any prior work on, pick up where we left off.
disable-model-invocation: true
argument-hint: "[topic or system; omit to take the most recent brief]"
allowed-tools: mcp__erp-local__search_all, mcp__brief-local__get_brief, mcp__brief-local__send_brief, mcp__brief-local__complete_brief, mcp__erp-local__get_task, mcp__erp-local__get_note, mcp__erp-local__get_upcoming, mcp__wiki-local__get_doc, mcp__wiki-local__get_entity
model: claude-sonnet-5
---

Orient a session against everything already known about a topic, before doing work that
may re-derive it.

## When to use this

- Starting substantive work on a system that has history — invoked explicitly, since the
  sweep costs a round-trip.
- Continuing from a handoff brief (the original use; still the default with no argument) —
  no sweep, just the most recent brief.
- Skip for a self-contained one-off, or a topic that plainly has no prior work.

## Procedure

1. **Derive terms** — from the argument, or from the user's opening request, take 2–3
   search terms: the system or host name, the component, the problem word. `search_all`
   matching is typo- and word-order-tolerant but **not** synonym-aware, so include the
   obvious synonym — `dnsmasq` and `DHCP` are still two terms, not one (synonym
   expansion is deferred, erp task #167).

   **No-argument path** — with no topic, skip the sweep entirely: `get_brief` the most
   recent brief, confirm the pick-up in one line (step 6), and continue from its next
   step. Steps 2–5 are the topic-search path only.

2. **Sweep** — one `search_all(query, limit=15)` call. It spans briefs, erp tasks, erp
   notes and the wiki, and returns ranked shortlist rows (never full bodies); each row's
   `ref` is the literal follow-up call to read that item. Pass `get_upcoming` alongside
   only when the topic is home-infra and you need due-date context the search rows lack.

3. **Dedupe** — the same fact often sits in two stores (a task linked to a wiki doc).
   Collapse rows sharing a `thread` into one line. Ranking is server-side.

4. **Present a shortlist** — at most 5–7 rows, numbered: store, title, date, one line of
   gist. Then stop and ask: pick a row, or start fresh.

5. **Branch:**
   - **Pick** — read the item named by the row's `ref` (`get_task` / `get_note` /
     `get_brief` / `get_doc` / `get_entity`). Resolve the references it names (paths,
     URLs, commits) before acting. Continue from its stated next step; don't redo
     decisions it records. For a brief, follow its "suggested skills" section.
   - **Nothing found, or fresh** — say so in one line and start the work clean. An empty
     sweep is a valid outcome, not a dead end.

6. **Confirm before proceeding** — one line on what you're picking up and the next
   action, so the user can redirect if it's the wrong thread.

## Constraints

- Read-only. The one exception: a brief that was picked up and finished is
  `complete_brief`d, as before.
- Never act on a shortlist row without the user picking it — present, then wait.
- Don't widen a found thread's scope. It says what it says; new work is new work.
- No fabricated gist. If a row's content wasn't read, the gist is its title.

## Done criteria

- `search_all` swept and deduped by thread (topic mode), or the most recent brief taken
  directly (no-argument mode).
- A shortlist presented and a thread picked, or "nothing relevant / starting fresh"
  stated explicitly.
- The next action confirmed in one line before work begins.
