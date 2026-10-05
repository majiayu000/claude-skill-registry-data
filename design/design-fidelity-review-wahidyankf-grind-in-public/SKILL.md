---
name: design-fidelity-review
description: >-
  Guides judging a rendered page against cited design ground truth: reading the live render rather than component
  source, citing the source a difference departs from, telling finding kinds apart, and judging practice with evidence.
when_to_use: >-
  Use when reviewing whether a running user-facing surface matches its approved design and sound visual practice, or
  when deciding whether a visual difference is a finding.
compatibility: Requires a running surface in a real browser and read access to the approved designs and token layer.
---

# Design Fidelity Review

Design-Fidelity Pass owns the ground-truth sources, the coverage, what each finding records, and what the pass leaves
alone. Enumerated Coverage owns the element and shared-control sweeps, Design Tokens and Accessibility own the values a
render must honour, and
[Plan UI Design](../../../repo-governance/conventions/plans-organization-policy/016-plan-ui-design.md) owns how approved
designs are carried. This skill covers the reviewer's judgement.

## The Render Is the Evidence

Judge what the browser resolved: computed values, rendered geometry, and the state on screen. A stylesheet can be
correct and still render wrong through an override, the cascade, or a missing dark token; it can also look wrong and
render right. Deciding a finding by reading component source substitutes a different check for this one.

Record the viewport class, theme, locale, and state with every observation. A difference seen in one of them exists only
there until it is checked in the others.

## Cite Before Recording

Complete one sentence before writing anything down: the render shows this, and that source says otherwise. The source is
a named design and frame, a token role, a named primitive, or a published guideline. When that half of the sentence
cannot be filled, the observation is preference, not a finding. An optional external design that was never supplied is
never a finding either.

## Tell the Kinds Apart

| Observation                                                             | Kind                                |
| ----------------------------------------------------------------------- | ----------------------------------- |
| a value no token defines, or a token used outside its role              | token fidelity                      |
| an element that departs from the selected design at a declared viewport | design fidelity                     |
| a hand-built control where the design names a primitive                 | primitive reinvention               |
| failing contrast, invisible focus, or an undersized target              | accessibility                       |
| weak composition where no design speaks                                 | practice                            |
| a control that acts on one surface and does nothing on another          | behaviour, for the exploratory lens |

The last row belongs to [Exploratory Testing](../exploratory-testing/SKILL.md); raising it here double-counts it.

## Judge Practice by Measurement

Each practice dimension has evidence a second reviewer can repeat:

- **Hierarchy:** the primary content or action is the most prominent element at first glance, at each viewport.
- **Alignment:** edges and baselines are shared; measure the offset rather than eyeballing it.
- **Spacing and density:** gaps come from the spacing scale, related items sit together, and nothing crowds past the
  target sizes.
- **Typography:** sizes come from the type scale, with no truncation or overflow in the longest locale.
- **Colour:** only token roles appear, and each state uses its own role.
- **Consistency:** the same component shows the same recorded values on every surface.
- **Balance:** no composition turns lopsided at one breakpoint.

## Sweep Before Browsing

Run the consistent-styling sweep before free inspection, so the list of what gets checked is not shaped by what caught
the eye. An unstyled native control beside its styled counterpart elsewhere is the typical catch. Dark themes, the
longest locale, and the narrowest viewport are where fidelity most often breaks, so they are never the ones skipped.

## Observe Only

Change nothing shared or live. Use synthetic data, stop a destructive flow at its confirmation step, and fix nothing
found.
