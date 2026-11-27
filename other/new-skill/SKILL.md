---
name: new-skill
description: "Use when a project thread repeated a multi-step procedure, a Lessons line hit Seen: 3x, or a propose_skills card comes to mind. Gets the skill into claude-setup as a PR, never as an account skill."
---

# New skill: idea to PR

A saved `propose_skills` card becomes an account skill: a second rule source outside git, no PR, no gate,
loaded in every thread of every project and paid for in tokens every turn. The hook refuses the tool
(`global/rule-guard.mjs`). The idea itself is welcome, so it goes into claude-setup like any other change.

## Is it a skill?

- A procedure done twice or more, with several steps: a skill (Anthropic: procedures are skills).
- A rule ("always X", "never Y"): one line in `CLAUDE.md`, or in its home from `docs/MAP.md`. Not a skill.
- A one-off: a Lessons line, nothing else.

## Steps

1. **Prior art.** Search `docs/MAP.md`, `.claude/skills/` and `config/ecc.json`. A fit gets extended, never doubled.
   Never edit vendored skills (the ECC set, impeccable, ponytail, web-interface-guidelines).
2. **Write** `.claude/skills/<name>/SKILL.md` in the format `scripts/check.mjs` checks: `description` up to 200
   characters, third person, trigger case first, containing "Use ..." (check.mjs enforces these two); keep the body short, detail in files one
   level down. Only what Claude does not already know. Anthropic's `skill-creator` helps with the draft.
3. **Eval first.** `evals/<case>/prompt.md` plus `graders/criteria.md` (see this skill's `evals/`): one case that
   should fire it and one that should not. `claude plugin eval` (laptop) compares with and without the skill.
4. **Place it.** Cross-project: symlink it from `mods/setup-skills/skills/` (flow, review, UI, legal, money) or
   `mods/setup-domains/skills/` (games, video, social, stores). A plugin skill links only skills of its own
   plugin; repo files go in as text, `claude-setup/<path>`. `.claude/settings.json` plugin lists do not load in cloud threads.
5. **Ship.** Thread with the GitHub App: `add_repo` claude-setup, branch `claude/skill-<name>`, one commit per skill,
   batched into the next claude-setup push (`docs/github-rules.md`). Without it: patch to
   `/mnt/project-files/<project>/batch/claude-setup/`, a `Batched: <path>` line, and the coordinator carries it.
   The PR body needs `Prior art:`, `Lessons:` and the `claude plugin details` token numbers before and after.
6. **Gate.** The normal five checks, plus: the description fires on 3 example sentences and stays silent on 3 others.
