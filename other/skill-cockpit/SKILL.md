---
name: skill-cockpit
description: Open a local browser cockpit for the agent self-improvement loop - see every installed skill, the new candidate skills, and the blind eval results and adopt/probation/reject decisions for all of them, and start mining, dry runs, full loops, evals and probation rechecks from the page. Use when asked to "show my skills", "open the cockpit", "what did the loop adopt", "show eval results", "manage my skills", or to watch skill-miner / skill-eval-loop runs. Local only, stdlib Python, no cloud.
---

# skill-cockpit

The UX layer over skill-miner and skill-eval-loop. One local page, three questions:
what skills do I have, which new ones are being considered, and did they prove
themselves on my own tasks.

## Start

```bash
lsof -iTCP:7788 -sTCP:LISTEN                 # check the port first
python3 scripts/cockpit.py                    # http://127.0.0.1:7788/
python3 scripts/cockpit.py --port 7790 --forge-root ~/skill-forge \
  --projects ~/.claude/projects --skills-dir ~/.claude/skills --skills-dir ~/.agents/skills \
  --memory ~/.claude/projects/-Users-me/memory --adopt-dir ~/skill-forge/adopted
python3 scripts/cockpit.py --dump             # state JSON, no server (for agents/tests)
```

On a remote box, tunnel it: `ssh -L 7788:127.0.0.1:7788 host`, then open locally.

## What the page shows

- **Evals** - every run in `$FORGE_ROOT/runs`: winner (skill / baseline / tie /
  invalid) with the sample tally (`3–0 of 3`), verify passes per arm (`3/3`) and
  tool errors, gate decision. Sampled runs (`runs/<id>/sN/`) show each sample's
  winner, timings and runner error; a run still being written by forge.sh or a
  timer reads as running, an abandoned one as incomplete. Expand for the
  exact task prompt, the blind judge's reasons, per-criterion winners, the
  production failure it targets, and the probation recheck date.
- **Candidates** - drafted skills (`drafts/`) with their forge status, and scored
  matches from local, getedge, Floom and skills.sh with P(improvement). Any draft
  can be evaluated on an unused brief from the page (`forge.sh --brief --skill-dir
  --samples N`, default 3, optional probation on a tie).
- **Fleet** - installed skills (symlinks de-duplicated) with their latest ledger
  decision, filterable.
- **Failures** - correction themes from `mined/corrections.json` (knowledge gap vs
  generic, with the user's own rule), then mined error clusters (task vs infra), frustration quotes, and the
  heaviest sessions by output tokens. Task clusters can be looped directly.
  "Mine corrections" runs `corrections.py` (one model call; `--memory` maps themes
  to the user's rule files).
- **Jobs** - live log tail of anything the cockpit started.

## Rules

- Binds 127.0.0.1 only, rejects foreign Host headers, and every action needs the
  per-process token embedded in the page (no CSRF against localhost).
- Actions are a fixed whitelist that call the sibling skills' scripts. One job at a
  time, so eval spend stays visible. Evals never overwrite an existing run.
- The cockpit never adopts or deletes skills by itself - `gate.py` and
  `recheck.py` own those decisions, and the ledger records them.
- Scripts are found as siblings (`../../skill-miner/scripts`), then in
  `~/.agents/skills` / `~/.claude/skills`; override with `MINER_SCRIPTS` /
  `EVAL_SCRIPTS`.
