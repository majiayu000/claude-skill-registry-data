---
name: nick-saban
description: >
  Sets up and audits the Claude Code harness for a project: CLAUDE.md,
  .claude/rules, skills, subagents, settings.json permissions, hooks,
  verification loop. Commands: kickoff (scaffold new setup),
  check-playbook (score an existing one), scouting-report (last scorecard),
  adjust (fix bloat/misplaced instructions), drill (turn advisory prose into
  real hooks/permissions/CI), decline (record an accepted risk), gameplan
  (work order with acceptance criteria before building), watch-film (check a
  diff against that order for scope creep/weakened tests/false claims). Use
  for setting up Claude Code, or on: "Claude ignores my CLAUDE.md", "it's huge
  and still misses things", "it said done but ran nothing", "it changed files
  I didn't ask about", "it weakened a test to pass", "rule, skill, or hook?",
  "is my setup any good". Not for code quality (code-audit), test coverage
  (test-assessment), one-off prompt wording (genie-proof-prompts), new skill
  authoring (skill-creator), or compacting a conversation (handoff).
---

# Nick Saban

A playbook is the durable, repo-wide agent operating system: `CLAUDE.md`, `.claude/rules/`, `.claude/skills/`, `.claude/agents/`, `.claude/settings.json` permissions, hooks, and the verification loop. This skill builds one, scores one, and fixes what it finds — plus a separate, lighter-weight pair of commands for contracting and checking one specific change.

`kickoff` · `check-playbook` · `scouting-report` · `adjust` · `drill` · `decline` · `gameplan` · `watch-film`

## Doctrine

Five beliefs every command holds. They're short on purpose — read them every time, and load a reference file when you need the procedure behind one.

1. **The lowest sufficient rung.** Every requirement in a playbook belongs on exactly one rung of the enforcement ladder — prose, scoped rule, skill, hook, permission, CI gate, or test — and it belongs on the *lowest* one that actually holds. Prose is cheap to write and easy to ignore. A failing test cannot be ignored. Moving a requirement down the ladder isn't extra rigor for its own sake — it's closing the gap between what you told the agent and what actually happens.
2. **Detected, never asserted.** Nothing in this system marks itself done. `adjust` and `drill` change the repo; they never touch a finding's status. Only the next `check-playbook` gets to close a finding, by observing that whatever it was detecting no longer happens. This is the same principle Doc 2 makes about verification-as-autonomy, applied recursively to this skill's own claims about itself — if this skill asserted its own fixes worked, it would be exactly the kind of unverified completion claim it exists to catch.
3. **A finding you can't write a consequence for isn't a finding.** "This is bad practice" is an opinion. "This means formatting drifts across sessions because nothing runs the formatter" is a finding. If you can't name the concrete way this bites the user, don't raise it — or keep digging until you can.
4. **Declined is a first-class answer.** Some standing risks are deliberate trade-offs the user already made with full knowledge. Recording that once, by signal, with a reason, is a legitimate outcome — not a failure to fully "fix" the repo. A system that re-flags a decision every single pass trains people to stop reading it.
5. **Context is a budget.** Every line in `CLAUDE.md` is paid for on every single session, forever. Deleting a line that isn't earning its keep is a fix in its own right, not a smaller version of a fix.

## Setup

Read `.claude/nick-saban/registry.json` once, at the start of the turn, if it exists. Don't re-read it between commands in the same turn — nothing in this skill mutates it mid-command except the command that's actually running.

## Commands

| Command | Category | Description | Reads | Writes | Reference |
|---|---|---|---|---|---|
| `kickoff` | Set up | Scaffold a playbook for a project that has none | repo probe | `CLAUDE.md`, `.claude/**`, `audits/001.json` | `references/kickoff.md` |
| `check-playbook` | Assess | Inspect and score the existing playbook | source, prior record, waived | `audits/NNN.json`, `registry.json` | `references/check-playbook.md` |
| `scouting-report` | Assess | Scorecard, delta since last pass, open backlog, orders | registry, records, orders | — | `references/scouting-report.md` |
| `adjust` | Resolve | Restructure the instruction layer | record @ rungs `prose`/`scoped-rule`/`skill` | `CLAUDE.md`, `.claude/rules/`, `.claude/agents/` | `references/adjust.md` |
| `drill` | Resolve | Convert advisory prose into executable enforcement | record @ rungs `hook`/`permission`/`ci`/`test` | `.claude/hooks/`, `settings.json`, CI | `references/drill.md` |
| `decline` | Resolve | Record a finding as a deliberate, accepted choice | record | `waived.json` | `references/decline.md` |
| `gameplan` | Contract | Write a work order with acceptance criteria bound to real commands | repo, `verificationSurface` | `orders/<slug>.md` | `references/gameplan.md` |
| `watch-film` | Contract | Check a diff against its work order | order, `git diff` | order frontmatter, `orders/<slug>.attest-N.json` | `references/watch-film.md` |

## Routing

1. **No argument** → load `references/routing.md` and present its evidence-based menu. Never auto-run a command just because one is due — a bare invocation means "what should I do?", not "do the obvious thing."
2. **Explicit or clearly implied command** → load its reference file and follow it exactly, including its "stops at" boundary.
3. **Otherwise** (general "how's my setup" or "help me with Claude Code here" energy, no command implied) → treat it as a request to understand the current state and default to `check-playbook`.
4. **Aliases** — route silently, no need to mention the alias resolved: `init` / `setup` / `scaffold` → `kickoff` · `check` / `score` / `status` → `check-playbook` · `prove` → `watch-film` · `order` / `brief` → `gameplan` · `accept` / `ignore` / `waive` → `decline`.
5. **Genuinely ambiguous — ask once, then proceed:** `verify` could mean `check-playbook` (verify the setup) or `watch-film` (verify a change). `fix` could mean `adjust` (rewrite the text) or `drill` (make it enforced). `review` could mean either playbook command or a different skill entirely (see the boundary sentence in this skill's description). One short clarifying question, then go.

## State

State lives in the user's project at `.claude/nick-saban/`, committed to the repo, one instance per project — two repos share nothing. It is **state, not source**: no command inspects, scores, or raises a finding about anything under that path; commands only read and write it exactly per their declared Reads/Writes above.

Full schema, the closed detector registry, the enforcement-ladder rung enum, and the write rules that keep the record trustworthy across passes: `references/state.md`. Read it before running `kickoff` or `check-playbook` for the first time in a session — those are the two commands whose correctness depends on getting the schema exactly right.
