---
name: mockups
kind: rule
law: mockups
description: Rule under the mockups law. Load when a screen is drawn or changed in a design tool, before the mockups are shown to the owner and when a design file is audited. Names the kit copy, the spec read before drawing, the agreement checked against mockups. Pattern mockups-measure.
---
<!-- rt-kit v0.34.0 · rules/mockups.needs-mockups.md · a367fd4ea714 · правится надстройкой, не здесь -->

# Mockups — how it works here

Rule under the law `docs/constitution/mockups.md`. The law says what the owner must see before
the code is written; here — what it is called in this tree, where it lives and what is not checked.

## What it is called here

| In the law                          | Here                                                                         |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| mockup                              | a frame on a sheet of the design tool                                        |
| the screen the mockup draws         | the page or panel in the application that carries the same name              |
| a sheet of the design file          | a file page, never a page of the application                                 |
| the description of the behaviour    | the domain spec in `docs/specs/<domain>/`                                    |
| the agreement                       | the product agreement of the task, `docs/specs/<domain>/proposed/<feature>/` |
| approved                            | shown to the owner and accepted in their words                               |

## Where it lives

In this tree — the table in `implementation.md` next to it. Paths live there, not here: the rule
travels between repositories, the layout does not, and a path named in the rule lies in the
first tree that keeps its code differently.

## Flow

The flow of a mockup from the first frame to the code: what is read before drawing, what is
measured before showing, and what is checked before work starts by the agreement.

```mermaid
flowchart TD
    A[A screen is to be drawn or changed] --> B{The behaviour already exists in the tree}
    B -->|Yes| C[The spec of its domain is read before the first frame]
    B -->|No| D[A sample is asked per screen]
    C --> E{A component of the kit goes on the sheet}
    D --> E
    E -->|Yes| F[It is measured in the running showcase and compared with the copy by numbers]
    E -->|No| G[The frames are drawn]
    F --> G
    G --> H[The coordinates of the frames are measured]
    H --> I[The owner approves the mockups]
    I --> J{The agreement has visual rules}
    J -->|Yes| K[Each rule is found on the mockup of every width; a rule the mockups do not show goes to the owner]
    J -->|No| L[The code is written]
    K --> L
```

## How the law applies here

- **A kit component on a design-tool sheet is a copy of the kit, and the copy drifts.** The source
  of look is the kit's styles in code. Before a component from the sheet goes into a mockup, it is
  measured in the running showcase, and its sizes, alignment and controls are compared with the
  bounds of the copy's nodes by numbers. Reading the styles does not show what the layout computes:
  the height of a row, where unselected items sit, a control that replaces an icon. A divergence is
  a question to the owner, and the answer is fixed once in the copy.
- **A mockup of behaviour the tree already has starts with reading the spec of its domain.** A
  screen in a design tool looks like work without code, so exploration stops at the sheet of earlier
  mockups. How a payment is taken, what a window asks and which fields a form holds are already
  described by the spec and carried out by code. The spec is read before the first frame, and the
  sample question is asked per screen: one sheet named as the sample of the whole set leaves the
  other screens without one.
- **The agreement is checked against the approved mockups before work by it.** Every visual rule of
  the agreement is found on the mockup of each width. A rule the mockups do not show goes to the
  owner as a question. Found after the code, it costs a code edit and an agreement edit together.
- **A mockup is measured by node coordinates before it is shown.** The technique is the pattern
  `mockups-measure`.
- **An audit of a design file is accepted only when every file page that draws a kit component is
  captured, measured and compared with the code of that component.** Names, properties and the list
  of variants say what a node is called, not what it draws: an arc drawn as a sector and a rounded
  field drawn as a capsule keep correct names. The technique and the report are the pattern
  `mockups-measure`.
- **A design-tool call asks the rules gate for this rule,** like the browser driver does for its
  own: without that the measurement pattern stays unread for the whole mockup task.

## What of the law is not here

Nothing checks that a mockup matches the screen it draws or that the owner approved it: both live
outside the tree, in the design tool and in the owner's words. The checks above are held by reading.

## Patterns

- `mockups-measure` — reading the bounds of frames and buttons in one call and what the numbers
  mean.
