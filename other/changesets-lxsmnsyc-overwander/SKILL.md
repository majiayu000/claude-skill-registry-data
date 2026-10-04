---
name: changesets
description: >
  Every change ships with a changeset. The bump level says what kind of change
  it is: `patch` for something that already existed and now behaves differently,
  `minor` for something that did not exist before, `major` only with the
  maintainer's explicit approval. Keep the description short and to the point,
  a list when it covers several things. Applies to every task that touches this
  repository, without being asked.
---

This repository releases through [changesets](https://github.com/changesets/changesets). Writing one is part of finishing the work, not a step somebody has to ask for.

## What gets one

A changeset describes what changed **against `main`**, not what changed against
the last commit.

A branch often introduces something and then corrects it a few commits later.
Nobody reading `CHANGELOG.md` ever saw the broken version, so that correction
gets **no changeset of its own**. Amend the feature's own changeset instead, if
it now claims something untrue.

The test is one question: did the behaviour being fixed ever reach `main`? A fix
for something players have today, or anything `main` does not have at all, gets a
changeset as usual.

## The bump level

The question is not how big the change looks or how visible it is on screen. It is **whether the thing existed before**.

**`patch`.** Something that already existed now behaves differently. A bug fixed, a number retuned, a rendering path rewritten, a screen relaid, a performance win. All of these are `patch` however different the result looks. A rendering change that alters what a player sees is still a fix.

**`minor`.** Something exists now that did not exist before. A new weather, a new item, a new ability, a new NPC, a new screen, a new field on a record that callers can set. If a player or a developer could not have reached it yesterday and can today, it is `minor`.

**`major`.** Ask first. Never write one on your own judgement. Say what you think warrants it and let the maintainer decide.

The two questions are worth keeping separate, because a single change often does both. Adding a fourth rarest sky is `minor`; retuning the threshold that decides how often the existing three appear is `patch`. When one changeset covers both, take the higher of the two.

## The file

A markdown file in `.changeset/`, named in kebab-case as a short sentence about the change rather than as a ticket or a component: `held-rather-than-hovered.md`, `nests-wait-for-babies.md`, `four-corners-of-the-sky.md`.

```markdown
---
'overwander': minor
---

One line saying what is true now.
```

The package is always `overwander`.

## The prose

**Keep it short.** One line for one change. A changeset is a changelog entry, not a summary of the work: it says what is true now and stops. Resist explaining the reasoning, the trade-offs or what it replaced.

Where a change covers several things, use a list rather than paragraphs, one line each:

```markdown
---
'overwander': patch
---

- Evolution rows on a shiny catch sheet no longer show the ordinary coat.
- A gifted species nobody has met draws a silhouette instead of Missingno.
```

Write for someone reading `CHANGELOG.md`, not someone reading the diff. Name the behaviour, not the file or the function.

The repository's usual prose rules apply: **no em-dashes**, plain sentences, no build-up. Wrap around 80 columns like the files already there.

Where a change touches world generation, say so on its own line, because it changes what every existing player sees.

## Before concluding one is missing

The release step folds every changeset into `CHANGELOG.md` and empties `.changeset/`, so a directory holding only `README.md` and `config.json` does not mean the work went unrecorded. Check `CHANGELOG.md` before writing a second one for something already shipped.
