---
name: trace-incident
description: Traces a production symptom to its cause and produces a minimal hotfix plan at .workflow/incident-<slug>/sdd.json with a timeline. Use when something is broken in production now.
---

# trace-incident

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

The entry is a **symptom** — an error, an alert, a user report — not a ticket.
Speed matters, which is exactly why the discipline does not loosen: a hotfix
built on a guess extends the incident.

## Steps

1. **Write down the symptom first**, before touching code. What is observed,
   since when, affecting whom, and how it was noticed. This becomes the timeline
   in `.workflow/incident-<slug>/incident.md`, and it is what stops the
   investigation drifting to a more interesting problem than the real one.

2. **Separate stopping the bleeding from fixing the cause.** They are two
   changes. Decide explicitly which one you are doing now. A rollback, a flag
   flip or a config change often beats a code fix as the immediate step — say so
   if it does. A mitigation that is not code needs no `sdd.json`: record it as a
   timeline entry in `incident.md` — what was done, when, by whom, and the
   effect. `route incident-<slug>` lists it as the `mitigate` step.

3. **Trace it, do not guess it.** Follow the symptom to the code path with the
   strongest search available: `../../shared/code-search.md`.
   Then read the actual lines. Every step of the chain from symptom to cause
   needs a `file:line` you have read.

4. **Label the confidence.** A plausible cause you cannot demonstrate is a
   hypothesis, and calling it one is not weakness — it is the difference between
   a fix and a second incident. Say what would confirm it: a log line, a metric,
   a reproduction.

5. **Plan the smallest fix.** `.workflow/incident-<slug>/sdd.json`, persona
   `incident-responder`, shape in
   `../plan-change/references/sdd.md`. Nothing tidied,
   nothing renamed, nothing upgraded. `rollback` states the user-visible state
   during and after, not just "revert the commit".

6. **Audit it anyway.** `sdd audit incident-<slug>`. Urgency is when a wrong
   citation is most likely and most expensive. A missing handover is reported
   as pending, not failed: it is owed before the PR, not before the hotfix, and
   `pr check --key` refuses until it is written.

7. **The regression test ships with the fix**, not after. A hotfix without one
   is how the same incident happens twice. If it genuinely cannot be written
   before the fix goes out, say so explicitly and name the follow-up.

8. **Close the timeline.** Detection, cause, fix, verification, and what would
   have caught this earlier. Each step of the chain in `incident.md` cites as
   `` `path:line` — `the line` ``; `cite check .workflow/incident-<slug>/incident.md`
   must pass. Then hand off to `implement-change`.

## Rules

- **The symptom is the scope.** Other problems found on the way get written
  down as follow-ups, not fixed in this change.
- **Never widen a permission or disable a check to make it work.** That trades
  an outage for an incident of a different kind.
- **Say what you did not verify.** Under time pressure the honest gap is worth
  more than a confident guess.
- **Production access is the user's.** Ask for logs, metrics or a query result;
  do not reach for production yourself.
