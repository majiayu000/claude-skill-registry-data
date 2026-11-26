---
name: facebookInspect
description: "The Facebook part of inspect: Facebook's pages, URLs, worked examples (the Marketplace location goal, the likes goal, the West Bank finding), its request docs and what the mouse and recordings taught on Facebook. Read with its shared counterpart, skills/inspect/SKILL.md (the accountBrowser guide), when inspecting a Facebook page."
---

# facebookInspect

The shared way to inspect a page (one launch, one step at a time, readings,
goals and findings) is `skills/inspect/SKILL.md`. This is what only applies
on Facebook.

## The routine on Facebook

```bash
# terminal 1 (or Monitor): the browser stays open until `do stop` or 30 idle minutes
log inspect start --account <a> --url https://www.facebook.com/me 2>&1 | tee <log>

# terminal 2: one step at a time
log inspect do snapshot
log inspect do goto https://www.facebook.com/me
log inspect do click e12 --live        # only when the owner asked
log inspect do stop
```

## Worked examples

A goal, in plain words:

```bash
log inspect start --account <a> --goal "Set the Marketplace location to Bethlehem, Pennsylvania" --detach
```

The goal is judged across the session: on Bethlehem's likes run ("Like 2 to
3 posts"), the first like reads "not reached" (100%) and the second
"reached" (78%).

A finding, as P.E.E.:

```bash
log inspect finding --account <a> --step 04_setlocationBethlehemPa \
  --point "Typing Bethlehem, PA saved the location in the West Bank." \
  --explain "Facebook matched PA to the West Bank, and the account was already in Lima, so the search ranked from Peru."
```

and its fix, once the goal is reached:
`log inspect finding --account <a> --fixes 1 --fix "Typed the state out in full."`

The West Bank step's SubQ reading was about 49,000 tokens.

## Request docs

Rebuild Facebook's request docs after recording or changing a page:
`log capture docs`.

## The mouse on Facebook

- Facebook's page sends requests all the time; the cursor must not freeze
  for them, only for the first ~2.5 s after a navigation.
- The humanMouse recordings (`skills/humanMouse/SKILL.md`) were made with
  `--url https://www.facebook.com/marketplace/`.
