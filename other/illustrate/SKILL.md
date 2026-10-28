---
name: illustrate
description: Before drawing or prompting any figure for a FrontierJS document, page or README — a diagram, an SVG, a Mermaid fence, a painted image, a chart — fill the eleven-line brief here, pick the kind, and route to its renderer. Use when a page is long enough that a paragraph and one picture might replace it, and before shrinking a page on the strength of a figure.
---

# Illustrate

**The brief is the craft; the drawing is execution.** Everyone who explains for a living decides the claim, the reader and the viewpoint before a mark is made, and most run a written check on the result (`IDEAS/illustration.md` § 2, with the sources). This skill is that brief for an agent, and the measurement that says whether the figure earned its place. Where the brief lives, and why, is `FJS-D1498`.

## When a picture can stand in for a page

Larkin & Simon's condition: a picture beats the prose only where the prose would make the reader *search or compute*. **A flow, a boundary crossed, a state that changes, two options compared: draw it. A list of facts, a definition, a policy: a diagram of a list is a list.** Say which the subject is before filling the brief.

## Three kinds, each with an owner

Roam's question picks the kind: *what/who* is an illustration, *how*, *where* and *when* a mechanism, *how much* a chart.

| Kind | Answers | Renderer | Owner |
| ---- | ------- | -------- | ----- |
| **Illustration** | *what a thing is* — a Gate, a Surface, a Stressor | an image model, painted, no lettering | `brand/IMAGERY.md` |
| **Mechanism** | *how it works* — a call crossing the bridge, the hook pipeline, a write announced | hand SVG up to about eight parts, D2 compiled to SVG above that, committed as `.svg` beside the doc; a Mermaid fence only where the reader is GitHub's renderer, a `README.md` (`FJS-D1499`) | this skill, until `brand/README.md` § Diagrams exists (`FJS-D1500`) |
| **Chart** | *how much* | SVG from data | the `dataviz` skill |

A mechanism figure draws the vocabulary's metaphor and coins none: `VOCABULARY.md` and `brand/README.md` § 1 already did the mining (three terrains, the surveyor, the bridge, the gate ladder). The frontier metaphor is allowed to be literal in a picture and nowhere in a feature name.

## The brief

Fill it in order, one line each, before a line is drawn or a prompt sent. **A field that will not fit in one line says the figure is not ready**, and a mechanism that cannot be drawn at one level with every arrow labeled is a finding about the mechanism: file it in `ISSUES.md` and stop drawing (Hohpe's test).

1. **Claim** — one sentence; it becomes the caption and the `aria-label`. Written first.
2. **Reader** — one named reader and what they already hold.
3. **Question** — who/what, how, where, when or how much. This picks the kind.
4. **Kind and renderer** — from the table above.
5. **Viewpoint and level** — one abstraction level; which realm or realms; what is deliberately off the page.
6. **Parts and relations** — at most seven named parts; every arrow carries its verb: `writes`, `refuses`, `announces`.
7. **The difference** — when comparing, the one edge each option adds or removes.
8. **Metaphor** — source → target, taken from `VOCABULARY.md`; what it highlights and what it hides. Illustration only.
9. **Encoding** — what each color, line style and size means; one hue for the thing under discussion and `currentColor` for the rest.
10. **Cut** — what was left out and why.
11. **Check** — the list below, answered yes.

The brief is kept: for an `.svg` it goes in a comment at the top of the file, for a painted image in the `<name>.prompt.txt` sidecar `brand/IMAGERY.md` § 8 already asks for, for a chart in the figure's `<figcaption>` and the commit.

## Rendering, by kind

- **Mechanism.** Load the `artifact-diagramming` skill for the mechanics: depict the mechanism not its name, one figure one claim, `<figcaption>` and `aria-label` carry the claim, `currentColor` so it reads in both themes. Count the parts first; above about eight, write D2 source and compile, since a hand-written SVG degrades with every part added (SVGenius, `IDEAS/illustration.md` § 3). Neither `d2` nor `mmdc` is installed here; a compile step says what it needs.
- **Illustration.** Paste `brand/IMAGERY.md` § 3's scene base, append the brief's claim as the subject line, add the realm and figure lines from § 4, and grade the result against § 8. No lettering in the image: the page sets the type.
- **Chart.** Load the `dataviz` skill and hand it the brief's claim and encoding.

## The check

Every line true at the size the figure will be used at.

- [ ] Title, type, scope and key present; every part named; every arrow labeled, its direction matching the label; every color, shape, line style and size with one stated meaning (Simon Brown's C4 checklist).
- [ ] Labels sit on the part they name, never in a legend; nothing decorative survives (Mayer).
- [ ] The caption states the claim, not the subject (Zelazny).
- [ ] The output parses. A figure that renders is not proof of a valid file, the same way a clean compile is not proof of valid JS (Invariant 15):

```sh
python3 -c "import sys, xml.etree.ElementTree as E; E.parse(sys.argv[1])" path/to/figure.svg
```

## The proof a figure replaced a page

**The measurement is a cold reader; the word count is the result.** Hand a fresh session the paragraph and the figure only, and ask it the questions the long page answers. Where it answers them, the page shrinks to claim, figure, cost paragraph and a link to the long page, which stays where it is. Where it cannot, the brief missed a part: go back to field 6, not to the drawing.

The paragraph and the figure divide the work: the figure carries the structure, the caption states the claim, the paragraph says what it costs and where it breaks, which is `brand/README.md` § 5's house voice already.
