---
name: admin-nav-item
kind: pattern
rule: navigation
description: Pattern of rule navigation. Load when creating an admin menu item, a section with a panel or a new section address — one declaration per item and route, the flag of a section without a screen, address nesting, a hint on an unavailable item. Not for the record edit panel — pattern entity-aside.
---
<!-- rt-kit v0.34.0 · patterns/admin-nav-item.md · 2db80c3581c2 · правится надстройкой, не здесь -->

# A menu item and a section address

Pattern of the rule `navigation`. What must be true — the law
`docs/constitution/navigation.md`.

## When to use

- An admin menu item or a section with a panel is created.
- A new screen appears that needs an address.
- An item has to be shown while there is no screen under it yet.

## One declaration per item and route

The menu declaration is data: addresses, dictionary keys, rights and the section flag. It lives
in `libs/admin/common/container/util` and serves as the source of both the items and the route
gating. A second declaration next to the routes would drift from the first, and the result would
be "the item is not visible, but the page opens".

The declaration imports no `shell`: otherwise the graph closes into a cycle and
`npm run check:layers` stops.

## An item without a screen

Declared **without rights and without an address**: a right opens the screen, and there is no
screen. It is visible to everyone all the while. When the screen appears, the flag is removed and
the rights are added; nothing else in the declaration needs editing.

The caption is visible, a press does nothing, the hint explains why. The carrier of the hint is
a wrapper around the button, and the item itself is switched off by `aria-disabled`, not by the
native `disabled`: a natively disabled button takes no focus, and from the keyboard the
explanation is unreachable.

`aria-disabled` always goes with a paired style rule `[aria-disabled='true']` — the browser does
not draw this attribute itself. Such an item has no click handler at all.

## The address repeats the section

Everything that stands in a section lies under its segment: a screen from "Settings" — under
`/settings`. The nesting is done in `apps/admin/src/app/app.routes.ts` through `children` of the
section segment; the domain's `shell` is mounted inside. No lib of its own is needed for a
section.

Highlighting of the active section is counted by address prefix, and no list of exceptions is
kept for it.

## Domain data comes into the header by a token

Unread counters are declared by an interface and an `InjectionToken` in
`libs/admin/common/container/util`, and the composition root (`provideAdminEnvironment`) ties
the token to the implementation. Only the root gets rights to a foreign lib — by one line in its
boundaries config.

The sign reaches the kit as a predicate by the item id, not as a field of its own in the
declaration: a domain section is named by the id of its item.

## Common misses

- A second declaration of rights next to the routes.
- A section with a panel that was given an address of its own: only items have addresses, and a
  section is visible if at least one item inside is visible.
- Walking only the top row when looking for the owner of an address: sections are walked
  together with the items of their panels, otherwise a nested screen is left without gating.
- A hint on an available item: it repeats the caption next to it word for word and adds nothing.
- `<prefix>PopoverTrigger` not set explicitly: the popup directive opens by press by default, and
  two neighbouring elements of one row behave differently.
- An address move without editing the end-to-end tests: they walk by addresses, and the run goes
  red.
- An icon picked as "similar": a missing one is added to the sprite and to
  `<prefix>-icon-names.ts`. The name of a present icon is copied from the kit icon file as is: some
  names carry the `ico-` prefix and most do not.

## The highlight is given by the router, not computed from the address

A section of this tree. The menu here is drawn by the kit top row, and it hands the highlight of
the current item to the router: an item carries the section address, and the one lit is the one
whose address is open. Computing it oneself — as a derivation over router events, the way the
shell did before the menu moved into a row — means answering the question about the address a
second time and diverging from the first answer on the very first address with a parameter or an
open panel.

- **An item declares an address, not a «current» flag.** There is no `active` field in the
  declaration at all: putting one there means starting a second source of truth about the open
  section.
- **No exception list for the highlight is started.** A panel address lives in a separate outlet
  and does not change the section address, so an open panel does not knock the highlight off.
- **The narrow layout of the row is started by the kit.** On a narrow screen the inline row hides
  whole, and the same items open by a button — the application header writes no narrow layout of
  its own.
