---
name: crew-hire
description: Decides how to add a capability to the agent team (role addendum, skill, or new agent) and adds it after the user's one-line OK. Use when the lead pasted the same long instructions into several briefs, or a failure class keeps slipping through.
---

# crew-hire

Run by the lead. `$CREW` is `~/.claude/agent-crew`. The lead proposes; the user approves in
one line; only then is anything written.

## When to hire

Hire only on evidence, never on a hunch:
- the lead pasted the same 300+ words of instructions into 3 or more briefs; or
- a class of failure keeps slipping through (the reviewer or CI finds the same kind of bug again).

State the evidence in the proposal (which briefs, which failures).

## The ladder: use the cheapest rung that works

1. **Role addendum**: a file `.claude/team/roles/<agent>.md` with extra rules for an agent that
   already exists (every agent reads its own addendum). Best for project-specific rules.
2. **Skill**: a `SKILL.md` for a procedure that several agents or sessions repeat. Put it in
   `.claude/skills/<name>/SKILL.md` (project) or `~/.claude/skills/` (every project).
3. **New agent**: only if the job needs its own tools, model or isolation that no existing agent
   has. First look in `$CREW/catalog/` (tester, ui-reviewer, security-reviewer, docs-writer,
   perf-profiler); copy it unchanged instead of writing a new one.

## Limits

- At most **7 active agents**. Over the limit: retire one first (`crew-retire`).
- One-line `description`, written as when to use it.
- A new agent starts as `trial` in `roster.md` and is judged after **3 uses** (kept or retired).

## Steps

1. Write the proposal to the user in at most 6 lines: what, which rung, the evidence, the model
   and effort, the retire criterion. Wait for a one-line OK.
2. Do it:
   - addendum or skill: write the file (addenda are under `.claude/team/`, which the lead may
     write; a project skill is a `coder` job);
   - catalog agent: the `coder` copies `$CREW/catalog/<name>.md` unchanged to
     `.claude/agents/<name>.md` (give it the path); the lead does not write there;
   - new agent: the `coder` writes `.claude/agents/<name>.md` from your brief (frontmatter:
     name, one-line description, tools, model, effort).
3. Add the row to `roster.md` (why, evidence, status `trial`, uses 0, retire criterion) and a
   row to `routing.md` if the agent has its own job type.
4. Run `check-team.ps1 -Project .`. Update `state.md` Index if useful.
