---
name: reuse-first-extend
kind: pattern
rule: reuse-first
description: Pattern of rule reuse-first. Load when what the kit or the base class offers was not enough. What to check before writing your own, how to extend the ready-made, how to declare a one-off deviation with the native-ok marker and when to remove it.
---
<!-- rt-kit v0.34.0 · patterns/reuse-first-extend.md · 253bfb67c0f5 · правится надстройкой, не здесь -->

# The ready-made was not enough

Pattern of the rule `reuse-first`. What must be true — the law
`docs/constitution/reuse-first.md`.

## When to use

A kit component or a base class does not cover the case, and the hand reaches to write one's own
next to it.

## First — check that it is really missing

```bash
grep -n "export" @rt-tools/ui-kit-v2/src/index.ts | wc -l
grep -rn "<similar technique>" libs/admin libs/site --include='*.html' | head
```

The kit is large, and most of its components are in no table. A neighbouring domain is read
whole: a technique that looks new is usually already written — and renamed on a move it stops
being recognised.

Frequent substitutions found by reading: `<prefix>-skeleton` instead of one's own shimmer,
`<prefix>-dialog` instead of one's own veil, `<prefix>-message` instead of one's own
`role="alert"`.

## Extend, do not clone

The missing variant is created **in the kit or in the base class**, and the other screens see it.

```
✗ libs/admin/<domain>/ui/my-dialog/        a clone "almost like the kit one"
✓ @rt-tools/ui-kit-v2/src/lib/components/dialog/   a new variant of the ready-made
```

A clone written next to it takes the edits onto itself and diverges from the original with the
first one. A renamed file and a "similar but own" component are the same departure, only
undeclared.

Before the kit PR is merged, the tree that ordered the edit runs its end-to-end suite against the
packed build of that branch. The build is unpacked over the installed package without touching the
declaration. The kit's own tests do not know the screen it stands on — a dialog over a side panel, a
button whose state the consumer binds — and a defect found after the merge costs a second release.

## One's own primitive — only with the owner's approval

Asked before the first file is written. The same goes for one's own base and one's own inline
style.

## One's own ready-made is declared by a sign

What was created with the owner's approval is seen only by whoever knows of it. So that the next
one does not bypass it, the tree appends a sign to its signs file — the one named by the key
`reuse.signals` in the checks settings:

```json
{
    "key": "<short sign name>",
    "ext": ".ts",
    "mode": "presence",
    "scope": "whole",
    "find": "implements +<the interface the base closes>",
    "cancel": "extends +<the base>",
    "instead": "<the base> — it already holds <what exactly>"
}
```

The scope is declared explicitly. `whole` reads the edit together with the file content and is
taken where the sign judges the structure of the class. Inheritance and the decorator are
declared once and do not land in a spot edit, so a sign without `whole` is always silent. `added`
reads only the added text and is taken where the sign judges the line itself — a raw tag, an own
style.

The cancel `cancel` is mandatory wherever the ready-made can be called lawfully: without it the
sign refuses also the one who has already inherited the base. It is not left empty — a sign
without a cancel is declared without this field at all.

A key matching a package one replaces it: the tree may speak of its own ready-made more precisely
than the package, which never saw it.

## A one-off departure is declared by the marker

```html
<!-- native-ok: the kit has no field with a phone mask, created by task <KEY>-000 -->
<input type="tel" qa-dataid="phone-input" />
```

The `native-ok` marker explains **what exactly the kit lacks**. "These lines were here before"
does not count as a reason: the guard strikes out of the checked text what already lies in the
file, so a refusal means new text.

It stands as a comment on the line above the code or in the line itself — both are lifted. In
markup only the first fits: the formatter spreads a tag whose attributes did not fit the width
limit over lines, and the first attribute always leaves for the line below the tag name. The sign
counts the tag name, that is, the first line, and a marker set as an attribute ends up on the
second and lifts nothing. A short tag the formatter leaves alone — and the marker works exactly
until one more attribute is added to the tag.

Beyond the next line the marker does not reach: it lifts its own case, not the block around it.

The comparison goes without indentation — on a move a block changes its indent while staying the
same code.

## Removing the departure

When the missing appears in the kit, the marker is removed together with the workaround. A
comment justifying a deviation holds that deviation up: as long as the explanation looks
convincing, it is left alone.

## Common misses

- One's own written before reading the kit and the neighbouring domain.
- A clone next to it instead of a new variant of the ready-made.
- A marker set without an explanation of what is missing.
- A marker left after the ready-made has appeared.
- One's own base designed anew instead of carrying over the owner's sample word for word.
