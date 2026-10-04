---
name: start
description: "Use when the user does not remember a skill's name, wants the list of exo skills in plain words, or names a goal and wants exo to pick. Not for a session's own routing rules, which route-skills owns and loads by itself."
argument-hint: "[goal or spec-path]"
disable-model-invocation: true
---

# Start

One door for a user who does not remember a skill's name. The enemy is a pick handed back for the user to type, or a list nobody reads before falling back to doing the work by hand. The overcorrection is a question when only one route fits the goal.

## No goal

- Relay the two tables in `references/cheat-sheet.md` as the whole reply, rows unchanged, because they line up only as written.

## With a goal

1. **Match.** Read every skill's `description` for the triggers that fit the stated goal.
   - A path to a spec file, or a spec or big wish to build, picks `spec` with that path or wish as its argument.
   - Start runs nothing after `spec`, which offers `build` once the brief is written.
   - `route-skills` is never a pick.
2. **Two routes, different work.** A goal that leaves open whether behavior stays or changes fits a behavior-keeping and a behavior-changing skill.
   - Run nothing before the answer, because the wrong pick does work the answer undoes.
   - Ask one question per `../route-skills/references/question.md`.
3. **Several fit.** Pick the one, ordering by `route-skills`' "When several fire" section.
4. **None fits.** Follow `route-skills` step 2 and do the work without a skill.
5. **Run.** Call the picked skill through the Skill tool in this turn with the goal as its argument, before any edit or write.
   - Tell the user no command to type, because they already typed one.
   - A skill carrying `disable-model-invocation` cannot be called that way: name the exact command to type instead, such as `/exo:remember <goal>`.
6. **Chain.** Each stage's handoff carries the run on to `ship`: add no stop, summary or question between stages, because the stage's next-stage question is the user's one choice.

## References

| File | Read it when |
|---|---|
| `references/cheat-sheet.md` | `/exo:start` with no goal. |

## Judgment

- A goal naming a skill outranks a close description match: "run the plan" picks `build` even when another description reads close.
