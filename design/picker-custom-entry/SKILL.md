---
name: picker-custom-entry
description: "Custom-entry fix for pickers with no way to add a choice (Select, Popover list, DropdownMenu). Use when building or touching any choice control (tier, category, tag, status, owner), `pnpm check:picker-add` names a file, running Pattern Patrol P13, or the user says 'no way to add my own' or 'why can't I type a new one'."
---

# picker-custom-entry — every picker takes new input (P23)

> "We have to annihilate the UIs that offer options but don't allow custom entry
> because those are the ones that lose the platform the best users. Right now, I
> got inspired to update something and the moment I went in to assign a tier, I
> got a pop up that forced me to choose from the shitty options I had in front of
> me. So instead of our system getting significantly better because I took the
> initiative to add something, our system was too arrogant and cocky and didn't
> want my opinion. … No one will ever know that it was one stupid popover that
> caused us to leave. But it's these platform level breaks that destroy
> everything. It's the lazy coding agent who builds a popover with a drop down,
> but is too lazy to include an add feature."
> — Arman, 2026-08-23

**The moment a person wants to teach the system something is the highest-value
moment in the whole product.** Refusing it converts an advocate into silent
churn, and nobody ever files a ticket saying so.

Doctrine: **THE PLATFORM POLICY** `common-docs/policies/no-dead-ends.md`
(promoted 2026-09-18 from P23 in the SEO keyword decisions; P11 is its "platform-governed" exception). Detector: `pnpm check:picker-add`.
Out of scope: choosing WHAT a picker should offer — that is the feature's own
doctrine.

## THE LAW

Any UI that offers a set of choices must let the person add one on the spot.
Typed text becomes a real value and is **selected immediately**. A dropdown with
no "+ Add" is a defect, not a simplification.

## The required shape

1. **A type-ahead, not a bare list.** When the typed text matches nothing, the
   control offers `Create "what you typed"` — never make them retype it into a
   different box. (matrx-frontend reference implementation:
   `components/ui/creatable-picker.tsx`; guard `pnpm check:picker-add`.)
2. **The add affordance lives OUTSIDE the scrolling list**, so a search that
   matches nothing cannot hide the one thing they came to do.
3. **Call the vocabulary's ONE existing write path.** Never hand-roll a second
   creation path beside the editor's — that is the defect this law's own sweep
   had to fix in its first run. In the keyword system that path is
   `quickAddDimensionValue` (`seo.gsc_quick_add_value`) for dimension values and
   `saveValueVocabulary` (`seo.gsc_save_value_vocabulary`) for levels/bands.
4. **Select it immediately.** Creating and then leaving the picker empty is the
   same dead end wearing a different hat.
5. **Say what was created and where it now lives**, with a door to the editor
   that owns that vocabulary (THE DOOR LAW — no dead ends).
6. **More than a name? Collect it, never guess it.** A level needs a threshold;
   a dimension needs at least two choices or the classifier is forced to stamp
   its only value on everything. Hand the typed text to a small dialog that asks
   for the rest — `AddLevelDialog` / `AddDimensionDialog` are the worked pair.

## P11 — the ONE exception, and it is still never a dead end

A **platform-shared vocabulary** (one every tenant reads the same way) is
governed centrally, so the control genuinely cannot widen it. It must then:

- **say so, in the control**, in the DB's own sentence (these refusals carry a
  message written for a non-technical reader — surface it verbatim), and
- **offer the local-override path** — "make this your own dimension" — as a
  live affordance, not a suggestion in prose.

A picker that just greys out, or fails silently, has broken P23 harder than one
with no add button at all.

## Genuinely exempt — a closed set the person could not extend in principle

- **Engine capability enums**: how a matcher matches (whole word / contains /
  exact), a comparison operator, a sort direction. Test: does each option map
  1:1 to a code branch? If adding an option would require writing code, it is
  not a vocabulary.
- **Time ranges** and other closed natural sets.
- **Pickers of existing records created elsewhere** (a site, an org) where
  inline creation genuinely belongs on that record's own surface — and even
  then, prefer an inline create when the record is cheap to make.

"It would be awkward to build" is never on this list.

## Fixing one (Tier M recipe)

1. Identify the vocabulary and find its ONE write path (grep the editor that
   already creates these rows — never invent a second).
2. Replace the closed control with the type-ahead + create footer.
3. If creation needs more than a name, add the small collect-the-rest dialog and
   pass the typed text through as its initial value.
4. Select the new value, invalidate every cache that renders that vocabulary,
   and toast what was created + a door to its editor.
5. `pnpm type-check`, then verify LIVE: type a brand-new name, add it, see it
   selected, confirm the row in the database, and remove the test value.
6. Re-run `pnpm check:picker-add` — the file must drop off the list.

## Anti-patterns

- **A door to the management page is NOT an add affordance.** Arman, 2026-09-18,
  on `ContextItemPicker`: "people don't know what a 'Context Item' is when they're
  in the scopes screen but when they're here, they see it in practice and so this
  is the time to allow them to create one the right way and we're squandering it."
  A `+` that opens `/organizations/…/context-items` in a new tab satisfies the
  detector's regex and the 2026-08-30 P13 run certified exactly that on
  `ScopeContextTargetPicker` — it is still the dead end. The record is created
  HERE, through its one write path (`CreateOrgModal` with `initialName`,
  `createScopeType`, `ContextItemAddForm` inline), and selected. A door is the
  "manage" companion, never the substitute.
- **The picker is inside a blocking modal.** A focus-trapping `Dialog` around a
  picker makes every door a dead end (the window it opens is unreachable). The
  host becomes a `WindowPanel`; a modal is for a yes/no, never for a workbench.

- A second write path beside the vocabulary's editor "because it was easier here".
- An "+ Add" that navigates away and loses what they typed.
- Creating the row but leaving the picker on its placeholder.
- Silently refusing a platform vocabulary (P11) instead of offering the override.
- Clearing a `check:picker-add` finding with an allowlist entry you approved
  yourself — exceptions are human-owned.
