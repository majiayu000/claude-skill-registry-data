---
name: triage-task
description: Reads a ticket from Jira or Azure DevOps and writes .workflow/<KEY>/triage.json. Use when asked what to work on, to pick up a ticket by key, or to understand its description, comments and blocking links.
---

# triage-task

All tracker access goes through one command. Never construct JQL, WIQL, URLs or
field lists — the provider builds them from the resolved context.

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

## Steps

0. **Key given?** Go straight to step 2: `start <KEY>` resumes as well as
   starts. With no key, `status` lists every ticket with work in flight and
   the one command that moves each on.

1. **No key given** — `task list`. Four columns, newest first. Show them and ask
   which one, unless the request already names one.

   No tracker in this repo? `task new "title" --type bug|feature|chore|support`
   records it in the local backlog and everything downstream works unchanged.
   Only local contexts accept it; `wb` says so if the repo has a real tracker.

2. **Pick it up** — `start <KEY>`. Reads the ticket into
   `.workflow/<KEY>/triage.json` and prints its text, puts the checkout on the
   ticket's branch, and ends with the route and the one next command. Rerun it
   any time: it is a no-op that says where the ticket stands. To read without
   branching, or deeper, use `task get <KEY>` — depth 1 by default: the task,
   plus one line per linked item.

   - Use `--depth 0` when the ticket is self-contained and links do not matter.
   - Use `--depth 2` only when a blocker or a parent decides the approach. It
     fetches bodies for blocking and hierarchy links, never for `relates`.

   **Light path** (the route says so): no plan, no other skill, no `status`.
   Make the change and a test that covers it, then
   `finish <KEY> -m "<type>: <summary>" --commit`. It runs the suite, the
   regression check and the message check itself, so do not run them first;
   on a pass it commits exactly the checked files. If it says the work
   outgrew the path, continue with `plan-change`.

3. **Go deeper only where it pays** — the `_expand` list names what exists but
   was not included. Pass a handle back **verbatim**:
   `task get <KEY> --expand comments:all`. Do not compose handles; anything not
   in `_expand` is rejected.

4. **Check `_unmapped` and `_truncated`** if present. `_unmapped` means the
   tracker had a link type or field this version does not model — say so rather
   than guessing what it meant. `_truncated` means content was capped, and
   names the handle that would retrieve it.

5. **Report gaps before planning.** If the ticket lacks acceptance criteria, a
   reproduction, or a decision someone else owns, list those questions plainly.
   A blocked-by link that is not Done is a gap, not a detail. Write them to
   `.workflow/<KEY>/questions.md` and say the ticket is not ready to plan.

## Rules

- Report what the ticket says, not what it probably means. Missing information
  is a finding to report, never a blank to fill.
- Quote the `key` in every claim so later steps can check it.
- One tracker per context, resolved automatically. If `wb` reports no context,
  relay its fix lines — do not guess a project or a URL.

Next, on the standard route: `plan-change` reads the artifact this produced.
