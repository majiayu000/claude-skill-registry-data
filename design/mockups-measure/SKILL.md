---
name: mockups-measure
kind: pattern
rule: mockups
description: Pattern of rule mockups. Load before frames are shown to the owner and when a design file is audited — reading the bounds of frames and buttons in one call, overlapping pairs, tops of a row, comparing a file page with the code. Not for a running application — that is the rule browser-verification.
---
<!-- rt-kit v0.34.0 · patterns/mockups-measure.needs-mockups.md · 59ecca950866 · правится надстройкой, не здесь -->

# Measuring a mockup

Pattern of the rule `mockups`. What must be true — the law `docs/constitution/mockups.md`.

## When to use

- The frames of a sheet are about to be shown to the owner.
- A row of cards, a toolbar or a form is drawn at a width other than the desktop one.
- A design file is audited.

## A mockup is measured by node coordinates

A frame in a design tool makes a layout claim, just like a running screen. A look at its screenshot
misses the same things: the buttons of a card row are off one line, or frames on the sheet overlap. Before the
frames are shown to the owner, one call reads the bounds of the sheet's top-level frames and of the
buttons inside them. It prints the overlapping pairs and each row's distinct button tops. Two
values in one row are the defect.

## An audit compares every file page with the code

A file page is a page of the design file, never a page of the application. The audit starts with
one call that lists the file pages and the kit components each draws; a file page with several
components counts for each of them. That list opens the report, and a report without it closes
nothing. Each file page on the list is captured, and the picture is put next to the template and
styles of its components. The question for every file page is one: does the code draw this. Each
drawn shape is then read from the node properties — arc data, corner radii, variable modes — and
compared with the code by numbers. A defect found is searched for across the whole file: it repeats
on other file pages. The report marks every line of the list as compared or as not captured, and
with even one of the second kind the audit stays open.

## Common misses

- **At the tablet width the buttons of a card row stood at different heights, and frames on the
  sheet overlapped.** The owner found both; one call reading node bounds would have shown them.
- **An audit was called finished by inputs, names and the list of variants.** The spinner arc stood
  on four pictures as a sector and was called normal, because nobody asked whether the code draws
  it so.
