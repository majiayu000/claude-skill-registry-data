---
name: brand-collections-uefn
description: Recognizing which official Fortnite Game Collection (brand island — TMNT, LEGO, Fall Guys, Star Wars, KPop Demon Hunters, Squid Game, The Walking Dead Universe, Rocket Racing, and any new one Epic adds later) a project is built on, from folder names, device classes, and template names actually found in it. Read this during project-bootstrap's A1 (structure mapping) whenever the project's assets/devices/folders look brand-themed. Also covers the procedure for capturing markers for a brand not covered yet, straight from a real project, into the second brain.
---

# Recognizing UEFN brand collections

Epic partners with major franchises ("Game Collections") to ship exclusive prefabs, galleries,
and sometimes custom devices for building themed "brand islands" — see [Epic's own Game
Collections index](https://dev.epicgames.com/documentation/fortnite/game-collections-in-fortnite).
This skill is about recognizing, from what's actually IN a project (folder names, device classes,
template names), which collection it's built on — useful for `project-bootstrap`'s structure map
(A1) and for `SPEC.md` to say something more specific than "uses some branded assets."

## How to use this

During A1, if the project's Content Browser folders, placed device classes, or the project
template name look brand-themed (a folder or device with a name that isn't generic Fortnite/UEFN
terminology), check `references/known-brand-markers.md` for a match before guessing:

- **Match found, strong confidence**: note it plainly in `SPEC.md` ("this project appears to be
  built on the <Brand> Game Collection, based on <the specific folder/device/template that
  matched>").
- **Match found, weak confidence** (a collection with only a name-level marker, no confirmed
  folder/device signature yet — see the table's confidence column): note it as a *guess to
  confirm with the owner*, not a fact — false positives are possible with a name-only match.
- **Looks brand-themed but no match at all**: this is a real gap in the table — see
  `references/first-use-recognition-procedure.md` for how to fill it in from THIS project, so
  the next one with the same brand gets recognized automatically.

This is a heuristic aid, never a blocker: if nothing about a project looks brand-themed, don't
go looking for a match that isn't there.

## References
- `references/known-brand-markers.md` — the marker table itself (folder names, device class
  names, template/prefab naming patterns) for every collection currently known, with a confidence
  level per collection (strong = confirmed technical markers, weak = name-only, from marketing-
  level public docs, not yet confirmed against a real project).
- `references/first-use-recognition-procedure.md` — what to do when a project looks brand-themed
  but doesn't match anything in the table yet: how to capture real markers from that project and
  get them into the vault (and, from there, into future runs of `project-bootstrap`).

Read only what you need — the marker table for a routine A1 pass, the capture procedure only when
you've actually hit an unrecognized brand.
