---
name: whats-next
description: >-
  Load this skill when the user asks what to do next or which skill or agent fits their situation:
  read the request and the repo, then suggest the installed skills or agents that fit, and run
  none of them. Trigger on "what's next", "what should I do now", "which skill do I use".
argument-hint: "[what you want to do]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# What's next

Advise the user which installed skill or agent to use next, and run nothing. Done when the user
has one to three suggestions, each with the exact way to start it, and the choice is left to them.

## Procedure

1. Take the goal from the request or the argument. When there is none, read the situation, using
   read-only commands only:
   - in a git repo: `git status`, the current branch, and `git log --oneline -10`
   - the lifecycle handoff files, each of which marks a stage reached: `product/BUSINESS_PLAN.md`
     (Shape done), `product/plans/*.md` (a plan not `built` is in flight), `product/ARCHITECTURE.md`
     (built), `product/EVIDENCE.md` (proven)
   - the newest file in `.agents_workspace/handoff/`, if any, for work a past session left open
2. Collect the candidates: every skill and agent in this session's listings, any plugin's, plus
   each user-only skill in the table below whose plugin `claude plugin list` shows as enabled.
3. If the request and the repo still leave the goal open, ask one round with `AskUserQuestion`: at
   most four questions, each with a recommended answer. With no human present, skip the question,
   assume the most likely goal, and say so in the answer.
4. If no installed candidate fits, run `claude plugin list --available --json`. Its `available`
   array holds only plugins not yet installed, each with `pluginId`, `description`, and
   `marketplaceName`. Match the descriptions against the goal and keep at most two, looking first
   at plugins whose `name` starts with `ceh-`, then at other marketplaces the user added, and at
   `claude-plugins-official` last. Mark each "not installed", with
   `claude plugin install <pluginId> --scope <user|project|local>` and then `/reload-plugins` as
   the way to start it. Leave the scope to the user, recommending `project`: `user` turns the
   plugin on in every folder, and a committed `project` scope turns it on for everyone who clones
   the repo.
5. Answer in the Output format and stop.

## Rules

- Run nothing: no Skill tool call, no subagent dispatch, no install, no file write. The user
  chooses what runs, so a suggestion that starts itself takes that choice away.
- Suggest an installed skill or agent first, and a plugin to install only through step 4. Never
  name a plugin from memory, which may be stale or not in any marketplace the user added. When
  step 4's command fails, point to the install guide,
  https://raw.githubusercontent.com/cheneeheng/ceh-claude-code-library/main/docs/GETTING_STARTED.md.
- Rank by fit to the moment, not by breadth: the skill whose trigger matches what the user is about
  to do comes first.
- Give the reason for each suggestion from what was read ("`product/plans/auth.md` exists and no code
  matches it yet"), never a generic one ("planning is useful").

## User-only skills

These set `disable-model-invocation: true`, so they never appear in the session's skill listing.
Suggest one only when its plugin is enabled.

| Skill                                       | Start it                                                    | When it fits                                                                                              |
| ------------------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `ceh-coding-conduct:refactor-repo`          | `/ceh-coding-conduct:refactor-repo [module-or-path]`        | A whole codebase or module has grown complex and should shrink, not one branch's diff                     |
| `ceh-orchestration-lab:orchestrate`         | `/ceh-orchestration-lab:orchestrate [model] [task]`         | Experimental: run a coding task as a supervised loop, with cheaper implementer subagents doing every edit |
| `ceh-orchestration-lab:plan-then-implement` | `/ceh-orchestration-lab:plan-then-implement [model] [task]` | Experimental: run a coding task as one complete plan handed to one cheaper implementer subagent           |

## Output

```markdown
| #   | Suggestion                  | Why now                               | Start it                          |
| --- | --------------------------- | ------------------------------------- | --------------------------------- |
| 1   | `<plugin>:<skill or agent>` | <the fact read that makes it fit now> | `/<plugin>:<skill> <args>` or ask |

Read: <what the advice rests on, one line>. Assumed: <the goal, if it was assumed>.
```

For an agent, "Start it" is the request that makes Claude dispatch it, such as "ask the
bulk-reader agent which files call X". For a plugin from step 4, "Suggestion" is
`<plugin> (not installed)` and "Start it" is the install command plus `/reload-plugins`.
