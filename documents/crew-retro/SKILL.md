---
name: crew-retro
description: Periodic retrospective of the agent team. Measures real token cost with the ledger, updates routing Evidence and roster uses, prunes the team files under their line caps, proposes hires and retirements, and offers generic lessons upstream. Use when the session-start hook says the retro is due.
---

# crew-retro

Run by the lead. `$CREW` is `~/.claude/agent-crew` (Windows: `$HOME\.claude\agent-crew`).
Edit only `.claude/team/` files other than `PROJECT.md` yourself; a change to `PROJECT.md` (or any
project file) is a `coder` job. Be short: this is housekeeping, not a report.

## 1. Measure

Run the ledger for the period since the last retro (read `last_retro` in `roster.md`; if
it says `never`, use the whole history):

```
powershell -NoProfile -File "$HOME\.claude\agent-crew\scripts\ledger.ps1" -Project . -Since <date> -Format md
```

Add `-Alias old=new` for agents that were renamed. The ledger gives, per agent type, model
and effort, the spawn counts and the **share of usage** (each row's cost weighted by model
price, divided by the total; this is what matters under subscription limits). Report shares
by default. Add `-Mode cost` and report dollars only if PROJECT.md or USER.md says the user
pays per token. A warning "unknown model family" means a model the price file does not know:
tell the user to add its family to `~/.claude/team/prices.local.json` (README, Models). Remember: `subagent_tokens` in notifications is a
context size, not spend; only the ledger is spend.

Also read the lead's own rows (main session, not subagents) in the ledger output or the session
transcript usage: the typical context size per turn and how often it was compacted. Report both in
one line. If the evidence says the window is wrong (contexts stay far below it and never compact:
lower it; compacted several times in a short span and lost state: raise it; stay within
100000-400000), edit `.claude/team/session.json` yourself (`lead_compact_window`, `reason`, `updated`)
and tell the user in one line. No pull request and no approval: the session-start hook copies the
value into `.claude/settings.local.json` at the next session start. If the user set their own value
(env var, `/autocompact`, user settings) the hook leaves it alone; `check-team` says which wins.

## 2. Update the evidence

- `routing.md` "Evidence": add one line per useful measurement or finding (what was tried,
  cost, result). Change a routing row only if the evidence supports it, and tell the user
  in one line.
- `roster.md`: set each agent's `Uses` from the ledger spawn counts; set `trial` agents with
  3 or more uses to `kept` or flag them for retirement.

## 3. Prune under the caps

Caps: `state.md` 50 lines, `routing.md` 150, `roster.md` 80. For each file over its cap, or
holding old items: move knowledge to its cold home instead of deleting it.
- finished work: delete from `state.md`;
- hazards and conventions that are stable: `PROJECT.md` (a coder job);
- how the project works: the project's own docs (a coder job);
- agent-specific rules: `.claude/team/roles/<agent>.md`;
- old evidence lines: merge several into one rule under "Learned rules", drop the rest.

## 4. Team changes

Look at the roster against the ledger. Propose, do not do:
- hire: via the `crew-hire` skill (same 300+ word paste in 3+ briefs, or a failure class
  that keeps slipping through);
- retire: via the `crew-retire` skill (0 spawns in 5 merged features or redundant).
Ask the user for a one-line OK for each.

## 5. Generic lessons

List lessons that are not about this project (rules about delegation, cost, briefs, hooks,
models). Compare with `$CREW/docs/RULES.md` and skip ones already there. If there are any, propose an upstream pull request to
`exaltedo2/agent-crew`: show the user the lessons stripped of costs, names, paths and any
project content (one line each). After a one-line OK, hand it to the `coder` with that text
as the task (a branch in a clone of agent-crew, never `main`). If the user says no, drop it.

## 6. Finish

Write the current ISO timestamp into `.claude/team/.last-retro` and into `roster.md`
`last_retro:`. Run `check-team.ps1 -Project .` and fix violations. Tell the user in at most
8 lines: cost headline (top agent types), what you pruned, what you propose.
