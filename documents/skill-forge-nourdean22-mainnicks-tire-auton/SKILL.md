---
name: skill-forge
description: Use when creating a new skill, when an existing skill never loads, does not fire or fires on the wrong prompts, when its description, trigger or routing needs rewriting, or when turning a workflow or runbook into a skill for this repo. Wraps the official skill-creator with this repo's evidence gates. Not for changing the steps or wording inside an existing skill's body (edit that file directly), compiling a book, doc or transcript into a cited package (source-to-skill), proposing skill edits after a session (session-observer), or running, listing or auditing skills (skill-fire-audit).
triggers: new skill, create a skill, skill never loads, does not fire, fires on wrong prompts, description rewrite, trigger rewrite, routing, runbook into a skill, skill-creator, trigger queries, held-out score, baseline, write a skill
---

# skill-forge

The official skill-creator drafts and evaluates a skill. On its own it leaves this repo's gates open: in the baseline run, a skill
made by following it alone failed 6 repo gates ([evals/baseline.md](evals/baseline.md)). Its text puts the workspace beside the skill
in `.claude/skills/`, its trigger queries are invented, no held-out set is kept, and nothing shows the skill loads by name. Config prose
does not cause invocation (`skill-fire-audit`): the description plus a working load are the only routing. A skill or policy edit Nour
asked for in words merges on green through the manager (monorepo-manager step 15); one made on agent initiative is a proposal
that waits for him. The global `writing-skills` skill gives the TDD doctrine for
skills; when it and this one both load, follow these gates.

Tooling: [scripts/forge.mjs](scripts/forge.mjs) (`check`, `mine`, `split`, `verify-origins`, `score`, `prove`; no dependencies).
Why each gate exists, with the incident behind it: [references/gates.md](references/gates.md). Trigger queries, step by step:
[references/trigger-evals.md](references/trigger-evals.md).

## Procedure

1. **Gate.** `find-skill` and `prior-art-grep` first: grep `.claude/skills`, `docs/UPSTREAMS.md`, `docs/skill-proposals.md`. A skill that
   exists gets edited, not duplicated. A skill compiled from a book, transcript or doc enters through `source-to-skill`: run its
   `scaffold.mjs` FIRST (it refuses a slug directory that already holds other files), then continue here from step 2.
   Rewriting an existing skill's description: its baseline rows are the prompts that misfired, and steps 7 and 8 use `check --existing`
   (and `--git`). Changing only the steps or wording inside its body is not this skill: edit the file directly.
2. **Baseline first.** Run the task WITHOUT the skill, at least once fresh plus any recorded incident, and write `evals/baseline.md`
   from the template in [references/gates.md](references/gates.md). If the task does not fail without the skill, stop: you do not need one.
   Commit the baseline ALONE, before `SKILL.md` exists (for an existing skill: before the first commit on the branch that changes it), and
   do not edit it afterwards: `forge.mjs check --git` (`--existing --git` for an existing skill) verifies both on the branch (a squash
   merge erases the order).
3. **Draft with the official skill-creator.** Invoke `anthropic-skills:skill-creator`; never edit the plugin copy, updates overwrite it.
   Where it conflicts with this repo, the repo wins: the workspace goes in the scratchpad (never `<name>-workspace` beside the skill);
   the layout is flat `.claude/skills/<slug>/`; the description starts "Use when", names what the skill is NOT for, stays under 1,024
   characters with no angle brackets, and states triggers rather than summarising the procedure. Skip its description-optimizer
   scripts on Windows (they report a clean score for a crashed run, see [references/trigger-evals.md](references/trigger-evals.md)); use step 4.
4. **Trigger queries from real data.** Mine real prompts, paraphrase them, label them, then fix the held-out split by hash. Tune the
   description on the train score; score the held-out rows ONCE with the final description and put every miss in the PR body
   ([references/trigger-evals.md](references/trigger-evals.md)). Never tune on the held-out rows.
5. **Skeptic pass.** A separate read-only agent (`lane-research`) tries to refute the skill, using the brief in
   [references/gates.md](references/gates.md). Record each finding in `evals/skeptic.md` under `## Findings`, ending the line with a
   full stop, semicolon or colon and then `fixed`, or with `rejected: <why>` or `none found after trying: <what>`. Fix what is real before you score again.
6. **Invocation proof.** After the description is final: `node .claude/skills/skill-forge/scripts/forge.mjs prove .claude/skills/<slug> --model haiku`
   starts a fresh `claude -p` session, asks the Skill tool for the skill by its exact name, and writes `evals/invocation.json`, bound to the
   description's hash. Any later description edit makes it stale; run it again.
7. **Conventions check, last.** `node .claude/skills/skill-forge/scripts/forge.mjs check .claude/skills/<slug>` must exit 0: name equals the
   directory, "Use when" description with a "Not for" clause, every bundled file linked from `SKILL.md` by its exact relative path
   (a file named only in prose is never read), no eval-tool leftovers, and the baseline, queries, skeptic record and invocation proof
   present and well formed. A compiled skill also passes `scripts/skill-compiler/validate.mjs`; `check` runs it. It does not parse YAML:
   quote a description that contains a colon and a space.
8. **Register.** Update the skill count and the routing line in `CLAUDE.md` (a 60-line cap, so edit in place), then
   `node scripts/agent-os/check-adapters.mjs` and `node scripts/agent-os/verify.mjs`. The PR body carries the baseline summary, the
   held-out score with its misses, the skeptic findings and the invocation receipt. Run `check <dir> --git` (`--existing --git` for an
   existing skill) on the branch before the squash; the manager repeats it.

## Never

- Edit the plugin's skill-creator, or hand-edit a held-out flag (`forge.mjs split --write` assigns it).
- Commit raw transcript text: this repo is public. `mine` redacts and `check` rejects common private shapes (emails, phone and ID numbers,
  addresses, IPs, domains, paths, tokens), but a name cannot be detected: read every query.
- Relabel an invented query as mined. `origin: "written"` is honest; at least a third of the queries must carry a real `tx:` id, and
  `forge.mjs verify-origins` proves on your machine that each one exists as a prompt YOU typed (a headless `claude -p` run, including this
  tool's own score runs, does not count).
- Call a skill done on a green `check` alone: step 6 is the proof it loads, and the held-out score is the proof it routes.
