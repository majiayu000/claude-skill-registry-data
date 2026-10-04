---
name: enterprise-architecture
description: >-
  Unified enterprise & software architecture skill grounded in four open-source standards —
  C4 + Structurizr DSL, ArchiMate 3.x, TOGAF ADM, and arc42 + ADRs (MADR). Use it whenever the
  user wants to: produce architecture diagrams as code (C4 context/container/component,
  Structurizr, PlantUML, Mermaid); write architecture docs or decision records (arc42,
  ADRs/MADRs, design docs); review or assess a design against quality attributes and EA
  principles; or model an enterprise (capabilities → applications → technology, app landscapes,
  portfolio rationalization). Trigger it even when no framework is named — e.g. "draw the
  architecture of this service", "give me a container diagram", "write an ADR for choosing
  Kafka", "is this design sound?", "map our capabilities to apps", "document my architecture
  in arc42", "create an HLD or LLD", "assess this design against ISO 25010 / quality
  attributes", "produce a solution design". Do NOT trigger it for writing
  application code or REST endpoints, IaC / cloud deployment (Terraform, Kubernetes), database
  or ER schema design, code-level UML or sequence diagrams, reviewing a pull request, or API
  reference docs.
---

# Enterprise Architecture

A practical toolkit for doing real architecture work the way open-source EA standards
intend it — diagrams as code, documentation as code, decisions as records, and a single
traceable model underneath. It unifies four complementary frameworks so you reach for the
right tool at the right altitude instead of forcing everything into one notation.

## The mental model: four frameworks, four altitudes

These frameworks are not competitors — they answer different questions. Knowing which one
fits the question is most of the skill.

| Framework | Question it answers | Altitude | When to reach for it |
|---|---|---|---|
| **C4 model** | "How is *this software system* structured?" | System → code | A single system/service: context, containers, components |
| **ArchiMate** | "How does the *whole enterprise* hang together?" | Business → app → tech | Capabilities, app landscapes, cross-system flows |
| **TOGAF ADM** | "How do we *deliver* an architecture change?" | Process/governance | Running an architecture engagement end-to-end |
| **arc42 + ADRs** | "How do we *write it down* so others understand & decisions stick?" | Documentation | Documenting a system; recording a decision |

A useful rule of thumb: **C4 zooms into one system, ArchiMate zooms out to the
enterprise, TOGAF is the *method* for changing it, and arc42/ADR is how you *narrate* it.**
They compose: an arc42 doc embeds C4 diagrams and links ADRs; a TOGAF engagement produces
ArchiMate models and ADRs as deliverables.

## How to use this skill

1. **Pick the mode** (below) from what the user is asking for. If ambiguous, ask one
   short clarifying question rather than guessing — architecture work is expensive to redo.
   If the question is *which framework / how should we approach this* rather than a request
   for an artifact ("is TOGAF worth it?", "Zachman vs TOGAF?", "how do we structure this
   effort?"), read `references/choosing-frameworks.md` and answer with a grounded
   recommendation that routes into the right mode.
2. **Read the matching reference file(s)** in `references/` before producing output. They
   contain the real notation, element catalogs, templates, and gotchas. Do not work from
   memory of the standards — load the reference so the output is correct and idiomatic.
3. **Produce diagrams/docs as code**, default to text formats that live in Git and render
   anywhere. Save artifacts to files when the user has a repo/workspace; otherwise emit
   inline.
4. **Keep one source of truth.** When elements recur across diagrams/docs, give them
   stable IDs and reuse them (see *Traceability* below). Don't redraw the same box with a
   different name in two places.

## The four modes

### Mode 1 — Diagram (diagrams as code)
*Triggers: "draw / diagram / visualize the architecture", "C4 container diagram",
"Structurizr workspace", "show the components".*

- For a **single software system**, use **C4** → read `references/c4-structurizr.md`.
  - Default output: **Structurizr DSL** when the user wants a reusable model that
    generates multiple views; **Mermaid** when they want something that renders inline
    immediately (chat, GitHub, Markdown docs); **PlantUML (C4-PlantUML)** when they're
    already in a PlantUML/Kroki toolchain.
  - Produce views in order of altitude: System Context → Container → Component (→ Code
    only if explicitly asked; it's usually noise). Stop at the level that answers the
    question.
- For **cross-system / enterprise** views, use **ArchiMate** → read `references/archimate.md`.
- Respect good-diagram hygiene from the reference: 5–20 elements per view, every external
  dependency shown, consistent naming, a title and a legend.

### Mode 2 — Document (docs & decisions as code)
*Triggers: "document this system", "write an ADR / decision record", "arc42 docs",
"design doc / RFC for X".*

- **Whole-system documentation** → arc42. Read `references/arc42.md`. Use the
  discover → generate → validate loop and the detail-level knob (LEAN / ESSENTIAL /
  THOROUGH) so you write the right amount, not a 40-page tome nobody reads.
- **A single decision** → ADR/MADR. Read `references/adr-madr.md`. Capture the context and
  the *options considered with trade-offs*, not just the chosen answer — the value of an
  ADR is the reasoning a future reader can't reconstruct.
- Embed diagrams (Mode 1) rather than describing visuals in prose. Link ADRs from the
  relevant arc42 section (§9 Decisions).

### Mode 3 — Review / assess
*Triggers: "review my architecture", "is this design sound?", "assess this against best
practice", "what are the risks in this design?".*

- Read `references/review-rubric.md`. Assess against **quality attributes** (the ISO/IEC
  25010 set: performance, security, reliability, maintainability, etc.) and EA principles,
  not personal taste.
- Output **severity-categorized findings** (Critical / Major / Minor / Suggestion), each
  with *evidence* and a *concrete remediation*, then a **verdict**
  (Approved / Approved-with-changes / Needs-revision). Avoid vague praise; an unhelpful
  "looks good" is worse than nothing.
- Where a finding implies a fix, hand off to the right mode (e.g. "record this as an ADR",
  "redraw the container diagram to show the queue").

### Mode 4 — Model the enterprise
*Triggers: "map our business capabilities", "application landscape", "capability → app →
technology", "enterprise architecture model", "rationalize our app portfolio".*

- This is the big-picture mode. Use **ArchiMate** for the model
  (`references/archimate.md`) and **TOGAF ADM** for the method/structure of the engagement
  (`references/togaf-adm.md`).
- Work top-down through the layers: **Strategy/Motivation → Business (capabilities,
  processes, services) → Application (apps, services, data) → Technology (nodes,
  platforms)**, then draw the *realization* links between layers (which app realizes which
  capability; which node hosts which app). The cross-layer links are the whole point — a
  capability map with no realization links is just a list.
- For portfolio rationalization, add a TIME / quality assessment per application
  (Tolerate / Invest / Migrate / Eliminate) — see the TOGAF reference.

## Traceability — keep one model under everything

Give every architectural element a **stable, human-readable ID** and reuse it across
diagrams, docs, and ADRs. This is what turns a pile of pictures into an actual model.

- Recommended ID scheme (URN-style): `ea:{org}:{system}:{kind}:{name}`
  - e.g. `ea:acme:checkout:container:payment-api`, `ea:acme:enterprise:capability:billing`
  - `kind` ∈ person, system, external, container, component, capability, app, node,
    decision …
- When a repo/workspace exists, persist these in an `architecture/` folder (one file per
  significant artifact, or a Structurizr workspace as the model-of-record) so they're
  diff-able and greppable. Reference the same ID from the arc42 doc and the ADRs.
- Before inventing a new element, check whether it already exists under another name and
  reuse the ID. Two names for one thing is the most common EA documentation defect.

## Validation

After generating diagrams or docs, sanity-check them. For cross-artifact consistency
(IDs referenced but never defined, building blocks named in prose but missing from
diagrams, quality goals with no scenario, ADRs not linked from any doc), run:

```
python scripts/ea_lint.py <path-to-architecture-dir-or-file>
```

It reports issues grouped by severity. Treat its output as advisory review feedback, not a
hard gate — explain findings to the user rather than silently "fixing" their intent.

## Output conventions

- **Diagrams**: fenced code blocks with the right language tag (` ```mermaid `,
  ` ```plantuml `, or Structurizr DSL in ` ```text `/a `.dsl` file). One view per block,
  each with a one-line caption stating what it shows and for whom.
- **Docs**: Markdown, headings matching the standard's section structure. Diagrams as
  separate `.puml`/`.dsl` files referenced from the doc when a repo exists; inlined
  otherwise.
- **Always state which framework and view** you're producing, so the user learns the map.
  Part of this skill's job is to make the user fluent in the frameworks, not just hand them
  artifacts.

## Reference files (load as needed)

| File | Load when |
|---|---|
| `references/c4-structurizr.md` | Any C4 diagram; Structurizr DSL; Mermaid/PlantUML C4 |
| `references/archimate.md` | ArchiMate views; enterprise/cross-system modeling (Modes 1 & 4) |
| `references/togaf-adm.md` | Running/structuring an architecture engagement; portfolio (Mode 4) |
| `references/arc42.md` | Whole-system documentation (Mode 2) |
| `references/adr-madr.md` | Writing a decision record (Mode 2) |
| `references/review-rubric.md` | Reviewing/assessing an architecture (Mode 3) |
| `references/choosing-frameworks.md` | "Which framework should I use?", framework comparisons, EA-approach strategy questions |

Templates live in `assets/templates/`; the consistency linter in `scripts/ea_lint.py`.
