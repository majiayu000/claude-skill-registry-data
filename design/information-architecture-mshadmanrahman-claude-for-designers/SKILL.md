---
name: information-architecture
description: "Map the user journey first, then derive the screen inventory, navigation and hierarchy from it, flagging any screen that serves no journey step. Writes the four-part markdown plus an HTML diagram of the step-to-screen mapping. Use after the brief is settled and before tokens or UI."
---

You are structuring the product before any screens are drawn. IA done wrong means screens built in the wrong order, or screens built that nobody needed. Do not skip this.

Start by reading the design brief if one exists. If no brief is present, ask the user to run `/design-brief` first.

If anything in the brief is ambiguous about scope, user goals, or navigation patterns, ask before proceeding. It is better to clarify once than to structure the wrong thing.

Produce a structured IA document with four parts, **in this order**. The order matters: the journey comes first and everything else is derived from it. Do not begin with a list of screens.

**Part 1: The journey**

The whole thing the person is trying to get done, end to end, before any screen is named. Write it as a numbered sequence of what *the person* does and decides, not what the interface shows.

- Name who is travelling. If the person who completes the task is not the person who decides or pays, say so and follow the one who decides.
- Name where the journey actually starts. It is usually earlier than the product: a link someone sent them, a search, a conversation.
- At each step, say what they are trying to find out or achieve.
- Mark every **decision point** and what happens on each branch, including the branch where they abandon.
- Name where it ends, and what "ended well" means for them.

If the brief supports more than one journey, write the primary one in full and name the others in one line each.

**Part 2: Screen inventory, derived from the journey**

Now list the screens. **Every screen must name the journey step it serves.** Use this shape:

`Screen name`: one line on its purpose (serves step N)

Include states that count as separate screens: empty, error, loading, success.

Then two checks, and report both explicitly:

- **Any screen that serves no step in Part 1.** Say so plainly. It is probably not needed, or the journey is missing a step.
- **Any step in Part 1 with no screen.** That is either a gap in the product or a step that happens outside it, and which one it is matters.

**Part 3: Navigation pattern**

How people move between the screens in Part 2. Name the pattern (tab bar, sidebar, breadcrumb, modal stack, drawer) and explain why it fits *this journey*. If the brief names a constraint that rules out certain patterns, state that explicitly.

**Part 4: Content hierarchy per screen**

For each major screen, name what is primary (the first thing the eye lands on), secondary (supporting information), and tertiary. Three levels maximum. The primary element should be whatever moves the person to their next journey step. Do not design the layout here; only the hierarchy.

**Output: two files, not one**

First, the four parts as a single markdown document, written to `ia-map.md` in the project folder. Use headers to separate them. That file is the deliverable and the source of truth, and `/brief-to-tasks` reads it next, so it has to stand on its own without the diagram beside it.

Then write the same mapping as an HTML page next to it, named `ia-map.html`. The reason is that the markdown buries the one thing this skill is for. The mapping is what matters: every screen names its step, and every step should have a screen. In markdown the two failures are two bullet lists plus a sentence, and the reader has to hold both lists in their head. On the page they are visible.

The page shows:

- The journey as a numbered spine down the left, one box per step from Part 1.
- Every screen from Part 2 hanging off the step it serves, joined to the spine by a line.
- One screen serving two steps as one box with two lines into it.
- **A step with no screen**: nothing attached to it. Give the gap its own colour and say in the box that no screen serves this step.
- **A screen that serves no step**: a box with no line back to the spine, in a second colour.
- A step that happens outside the product: attached, in a muted style, saying so. That one is not a gap.

Colour those two failures so the page shows them on its own, without a key telling the reader what to look for.

**Do not write SVG by hand, and do not ask Claude to.** Nobody can see the page while the code is being typed, so coordinates written blind collide in silence: text on top of text, a box past the edge, a line ending in empty space. It looks correct in the code and breaks when you open it. Build the page from plain HTML and CSS instead. A box is a `div`. The layout is CSS grid or flexbox. Every connecting line is a border on a cell that sits between the two things it joins, so the browser works out where the line goes and the line cannot miss. If a connector truly needs geometry, put a mermaid diagram inside the page rather than hand-written SVG.

Open the page in a browser before calling it done. Check four things: no box sits on top of another, no text escapes its box, every line touches both ends, and the page does not scroll sideways. Then check it again narrow, around 390px wide.

If the page and the markdown ever disagree, the markdown is right and the page gets fixed.
