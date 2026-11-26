---
vendored_from: https://github.com/BESSER-PEARL/uml-drawing-skill
name: uml-drawing
description: >
  Put a correct UML class diagram — as an embeddable image — into your docs.
  Use this skill whenever the user wants to add, draw, embed, or export a UML
  class diagram for a README, design doc, wiki, slide, or `.md` spec: it
  builds a structurally-correct model (classes, attributes, associations,
  inheritance, multiplicities) — from a description or from existing code the
  agent reads — and delivers it either as B-UML code embedded in the document
  or as a rendered SVG/PNG image (the agent can render it itself with a single
  call to BESSER's headless SVG endpoint, or export it from the BESSER web
  editor). Trigger on
  "embed a UML diagram", "add a class diagram to the README", "draw the data
  model", "diagram my code", "export the diagram as an image/SVG/PNG", or any
  request for a diagram that should both look right and stay accurate. The diagram is
  code — for building models in depth defer to bes …
license: Apache-2.0
compatibility:
  - claude-code
  - cursor
  - cline
  - windsurf
  - copilot
metadata:
  author: BESSER-PEARL
  version: "0.1.0"
  repository: https://github.com/BESSER-PEARL/uml-drawing
triggers:
  - uml-drawing
  - uml
  - drawing
---

# Embed a correct UML diagram in your docs

Agents are constantly asked to "add a diagram" to documentation — and they
routinely get the modeling subtly wrong (invalid multiplicities, arrows
reversed, inheritance backwards) or hand back a code block that never
renders as a picture. This skill produces a **correct** class diagram and a
**real embeddable image**.

## Scope

- **Class diagrams only**, for now — classes, attributes, associations,
  multiplicities, inheritance. Other UML diagram types (state machines,
  object, sequence, activity, …) are out of scope for this skill.
- **Always through BESSER B-UML.** Every diagram is built as a B-UML
  `DomainModel` first, then delivered. Going through the model is what makes
  the diagram correct *and* reusable as code.

### Where it can start

- **A description** — the user explains the domain; the agent writes the model.
- **Existing code** — the agent reads the source and builds the B-UML model
  from its structure. (There is no automatic code scanner; the *agent* does
  the modeling from what it reads — it is not a one-click importer.)
- **A supported into-B-UML path** — PlantUML, Draw.io, or a UI mockup.

### Two ways to deliver

Model once, then deliver as **embedded B-UML code** (Deliver A) or a
**rendered image** (Deliver B) — both from the same model, so they never
disagree. Pick by context (a design doc that should stay runnable → code; a
README that should show a picture → image), or provide both. Details in the
Deliver sections below.

**Where it lands.** If the user names a target document (a README, a design
doc), embed into that file. If they name none — or ask for a standalone diagram
of a repo/system — default to delivering a **new self-contained `.md`** (e.g.
`docs/<model>.md`): the rendered image (Deliver B) and/or the B-UML code
(Deliver A), plus a line or two explaining what the diagram shows. That turns a
bare "diagram my repo" into a committable document rather than a loose SVG.
When you create a new file, say where you put it (and offer the alternative —
embed into an existing doc instead — if that may be what they wanted).

## Workflow

```
1. Build the B-UML model — from a description, from existing code the agent
   reads, or via a supported into-B-UML path (PlantUML / Draw.io / mockup)
2. model.validate()  → confirm it is structurally correct

Then deliver one (or both):

  A) Embed the code:  drop the DomainModel Python into a fenced block in the .md
  B) Embed an image:  POST the model to BESSER's headless SVG endpoint (one
     HTTP call — no browser), save the returned SVG (e.g. docs/img/data-model.svg),
     embed  ![Data model](docs/img/data-model.svg)

3. When the model changes, update the model and re-deliver — one source of truth
```

## 1. Build the model

A correct diagram starts from a correct model. The minimal shape:

```python
from besser.BUML.metamodel.structural import (
    DomainModel, Class, Property, Multiplicity,
    BinaryAssociation, Generalization, StringType, IntegerType,
)

publication = Class(name="Publication", attributes={Property(name="title", type=StringType)})
book   = Class(name="Book",   attributes={Property(name="pages", type=IntegerType)})
author = Class(name="Author", attributes={Property(name="name", type=StringType)})

book_is_a = Generalization(general=publication, specific=book)   # Book is a Publication

# A Book is written by 1..* Authors; an Author writes 0..* Books
written_by = Property(name="writtenBy", type=author, multiplicity=Multiplicity(1, "*"))
writes     = Property(name="writes",    type=book,   multiplicity=Multiplicity(0, "*"))
book_author = BinaryAssociation(name="book_author", ends={written_by, writes})

model = DomainModel(
    name="Library",
    types={publication, book, author},
    associations={book_author},
    generalizations={book_is_a},
)
assert model.validate()["success"]
```

Naming: no spaces, no hyphens. For everything beyond this minimal shape —
enumerations, all multiplicity/composition patterns, association classes,
generalization sets, methods, validation details — read
**`references/class-diagram.md`** (bundled with this skill). For non-class
model types (object, feature, deployment, OCL, …), see the BESSER platform's
`besser-user` skill.

> **Importable form — required for both delivery paths.** Write every
> `Class(...)`, `BinaryAssociation(...)`, and `Generalization(...)` as an
> **explicit top-level assignment**, exactly as shown above. BESSER's importer
> (used by the SVG endpoint and by the editor's Import) reads the file's
> *structure* — it does **not** execute it — so relationships built inside a
> helper function or a loop are invisible: the classes import but the
> associations silently vanish. One literal statement per relationship.
>
> Because the importer never runs the file, `model.validate()` is **not**
> executed on the render path — you do not need BESSER installed to render via
> the endpoint. Keep the `validate()` call for when you *do* have BESSER locally
> (and before generating code); it is a no-op for the endpoint, not a
> requirement.

Where the model comes from:
- **From a description** — write it as above.
- **From existing code** — read the source and translate its structure
  (classes, fields, relationships, inheritance) into the B-UML model. The
  agent does the modeling; there is no automatic code scanner.
- **From PlantUML / Draw.io / a UI mockup** — use the matching into-B-UML
  conversion (available via the BESSER platform), then continue.

Now deliver it one of two ways.

## Deliver A — embed the B-UML code in the doc

Drop the model straight into a fenced ` ```python ` block in the `.md`. It is
correct, `validate()`-checked, re-runnable, and importable into the editor.
Best when the document should carry the model itself (a design doc, a spec):

````markdown
## Data model

```python
# (the DomainModel from above)
```

This B-UML model is the source of truth for the domain — `validate()`-checked,
and the input to any BESSER generator.
````

## Deliver B — embed a rendered image

The model becomes a real picture through BESSER's renderer, so the image
always matches the model. Two ways — pick by whether you want it hands-off or
hand-tuned.

### B1. Render it automatically (default) — one HTTP call, no browser

BESSER exposes a headless **B-UML → SVG** endpoint. The agent POSTs the model
`.py` file and gets an SVG back — no editor, no manual steps, nothing for the
user to click:

```bash
curl -X POST https://editor.besser-pearl.org/besser_api/get-svg \
  -F "buml_file=@data-model.py;type=text/x-python" \
  -o docs/img/data-model.svg
```

The endpoint parses the B-UML, auto-lays it out, and returns `image/svg+xml`.
Save it into the repo and embed:

```markdown
![Data model](docs/img/data-model.svg)
```

- The model file must be in **importable form** (see the callout in §1) — the
  same form the editor imports. Class diagrams only.
- Layout is automatic. When the placement matters, hand-tune it with B2.
- Save the `.py` as **UTF-8 without a BOM** — a leading byte-order mark makes
  the endpoint reject the file (HTTP 400).
- Omit enum-literal `default_value=...` in a model you render here — the
  endpoint currently fails on it (HTTP 500). It is fine for code generation; a
  plain enum used as an attribute type renders fine.
- A non-200 response is a small JSON error, not an SVG (`{ "detail": ... }`) —
  check the status before saving.

### B2. Hand-tuned export from the editor (when layout matters)

Open https://editor.besser-pearl.org, **Import** the `.py` (choose the
**B-UML** format), drag boxes and route lines to taste, then **Export** and
pick a format:

- **SVG** — sharp at any size; best for docs and the web.
- **PNG** — transparent background.
- **PNG (white background)** — for surfaces that need an opaque image.

Save into the repo and embed it the same way. (The editor can also export the
model as **B-UML** or **JSON** — those are the model, not an image.)

Either way, SVG and PNG render everywhere Markdown images do — GitHub, GitLab,
docs sites, wikis, slides — with no plugin.

## Keep it from drifting

Whichever mode you choose, the **model** is the source of truth. When
requirements change, update the model and re-deliver (re-paste the code, or
re-export the image) — never hand-edit an exported SVG/PNG, it is generated.

## The payoff beyond a picture

Because the diagram is a real B-UML model, the *same* artifact can generate
working code — Python classes, SQL, a FastAPI backend, Django, React, and
more. A diagram you drew to explain the system can become the system. To
generate code from it, defer to the **besser-generators** skill.

## When to reach for related skills

- **Building models in depth** (enums, inheritance, methods, OCL, object /
  feature / deployment / NN / quantum models) → the **besser-user** skill.
- **Generating code** from the model → the **besser-generators** skill.
- **Errors** (import/validation/editor issues) → the **besser-troubleshooting** skill.
