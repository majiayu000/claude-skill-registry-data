---
name: explain
description: >-
  Teach one gnarly topic (a bug family, a design constraint, a system) until you genuinely
  understand it: author a verified, layered explainer doc through an isolated investigation, then
  walk it with you one layer at a time, with checkpoints, live repros on challenge, and a decision
  — never a lecture — as the endpoint. Never reads or writes the tracker.
argument-hint: "[topic to investigate | path to an existing explainer doc to run]"
disable-model-invocation: true
effort: max
---

Two modes. If `$ARGUMENTS` names an existing explainer doc, **run** it. If it names a topic, **author** one first, then offer to run it.

$ARGUMENTS

## Author

Delegate the investigation to `sy:explain-author` — an isolated context, so its file reads and repro attempts never enter this session. Seed the prompt with every anchor already in hand: paths, symbols, the commit, the plan/gate/CI finding that made this worth explaining. It writes the doc itself to `<topic>_explainer.md` in the topic's resolved scratch directory (`scratch_dir(<topic-slug>)`) and returns only a compact brief — the resolved doc path, layer count, the one surprising rule, and how many claims are verified versus inferred.

Present that brief as a **Status** update, then close with one **optional suggestion** (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`): walk it here now, or run `claude "/sy:explain <doc path>"` in a new session for a clean slate before something like a merge. Never block on it — proceed either way.

## Run

`references/running.md` owns the walk: one layer per turn, an `AskUserQuestion` checkpoint after each, live repros the moment something is challenged, a decision (not a fact) at the end.

No tracker read or write, at any point — this is about your understanding, not the project record.

Every subagent dispatch resolves its model from config and passes it as the `Agent` invocation's actual model override, per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/model-dispatch.md`; a nested dispatch inherits nothing and must resolve again.
