---
name: propose-rule
description: "Proposes a change to the baseline rules, hooks, settings or skills as an issue in the skills repository or as a message to the user, without ever editing the installed baseline. Use when a correction recurs, a guardrail is missing or wrong, or a skill needs updating."
---

# propose-rule

Turn a correction into a baseline change proposal. Never apply it locally.

## When to use

- The user corrects or overrides the same thing twice.
- A guardrail is missing, too loud, or fires wrongly.
- A skill is wrong, outdated or missing.

## Steps

1. Name the trigger: what happened, how often, in which repository.
2. Classify the target: `rules/baseline.md` for something that must hold always,
   `skills/<category>/<name>` for domain knowledge, `hooks/` for something a hook can check
   mechanically.
3. Draft the final wording in bullets, ready to paste into the target file.
4. State the effect: what it blocks, what it allows, the false positive risk for a hook.
5. Decide the destination: read the source checkout path from
   `~/.config/agent-skills/state.json` and its git remote.
6. Current repository's remote owner matches that owner: open an issue there with
   `gh issue create -R <owner>/skills`, carrying trigger, wording, target and effect.
7. Owner differs, or the state file is missing: write the proposal in the answer to the user
   instead.
8. State unreadable: ask the user which path to take.
9. Report where the proposal landed.

## Template

```markdown
## Trigger
- <what happened, how often>
## Target
- rules/baseline.md | skills/<category>/<name> | hooks/<script>
## Proposal
- <final wording, bullets>
## Effect
- blocks:
- allows:
- false positive risk:
```

## Guardrails

- Never edit the installed baseline, never change the skills repository directly unless the user
  explicitly asks for a pull request.
- One proposal per change.
- Destination decided by remote ownership, never guessed.
