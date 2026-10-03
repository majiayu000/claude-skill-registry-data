---
name: spec
description: Turn a wireframe and everything already agreed into a written spec in traditional agile shape — an initiative broken into epics, epics into user stories with acceptance criteria, and themes as the labels that span them — presented as an interactive drill-down tree the user prunes, edits and annotates in the browser, with a plain-markdown spec generated from it. Use when the user wants a spec, an initiative or epic broken into user stories, acceptance criteria, to formalise what a wireframe or mockup does, or to review and edit a spec visually.
---

A spec in traditional agile shape — the full Atlassian ladder, **initiative → epics → user
stories**, with **themes as the labels that span them** — that opens **collapsed to headlines**:
the initiative's goal, its epics, their story titles; one screen, no scrolling. Click a story for
its acceptance criteria; click a criterion for how it will be verified. Themes are *"large focus
areas that span the organization"* — **tags, not work items**: a catalog shown on the initiative,
toggled onto the stories they span (auditability, performance, compliance). The complaint this
fixes: a spec today is a long document nobody reads.

```
wireframe + product.md + the conversation ──► tree JSON ──► drill-down page ──► edits & notes ──┐
                          ▲                                                                     │
                          └────────── you apply it, reply in notes, regenerate ◄────────────────┘
                                             │
                          specs/YYYY-MM-DD-<feature>.md   ← generated every round
```

**The tree is the spec.** `.vstack/specs/<feature>.json` is the source of truth; the markdown under
`specs/` is generated from it, never edited by hand. **There is no approve/reject** — the user
changes what's wrong, and the change is the feedback.

## 1 · Draft the tree

Read whatever exists — the wireframe (`design/<feature>.html` or wherever it lives),
`specs/product.md`, `specs/requirements.md`, and the conversation. Then write
`.vstack/specs/<feature>.json`:

```json
{
  "feature": "candidate-pipeline",
  "title": "Candidate pipeline",
  "goal": "The epic statement — one sentence on what the user gets.",
  "source": ["design/candidate-pipeline.html", "specs/product.md"],
  "themes": ["Auditability", "Reporting"],
  "epics": [
    { "id": "e1",
      "title": "As a hiring manager, I want to run a role's pipeline in one place, so that no candidate stalls unseen.",
      "stories": [
      { "id": "s1",
        "title": "As a hiring manager, I want to see everyone who applied to a role, so that I can act on every application.",
        "themes": ["Reporting"], "notes": [],
        "note": "Newest application first — the sort is the point, not a detail.",
        "crit": [
          { "id": "c1", "scenario": "Opening a role",
            "given": "Role 42 has applications",
            "when": "I open /roles/42",
            "then": "The top row is the most recent application",
            "and": "", "notes": [] }
        ] }
    ] }
  ]
}
```

The model is **Epic → User story → Acceptance criteria** inside one initiative (`title` + `goal`,
the document itself), with Atlassian's themes spanning it as labels:

- **Epics and user stories are both written as** *"As a [persona], I want to [goal], so that
  [benefit]"*. The story is the experience — what the person wants.
- **There is no separate requirements list.** A requirement that isn't checkable is an opinion, and
  one that is checkable is a scenario — so it goes in `crit`, where `phase-build` will test it.
  Writing both meant writing everything twice and letting the two drift.
- **`note` is the margin** — one optional string per story for the aside that isn't a criterion: a
  constraint, a decision already taken, a thing not to forget. It is never a hiding place for
  behaviour that belongs in `crit`.
- **`crit` are the acceptance criteria, as Gherkin scenarios** — `scenario` names the behaviour;
  `given` / `when` / `then` (and optional `and`) make it checkable with real values, not
  restatements. A criterion you can't write as Given/When/Then isn't done. This is also what
  `phase-build` later tests against. **Cover the flows, not just the demo path**: every story's
  scenarios should span the happy flow, the sad flows (invalid input, refusals, failures), and the
  edge cases (empty, duplicate, boundary). One happy scenario alone is a spec that lies by omission.
- `doc.themes` is the initiative's **theme catalog** — plain labels, edited here, not on the page;
  each story's `themes` array tags it. Keep the catalog short — a theme only one story wears isn't
  spanning anything.
- **No priorities here.** Which stories land first is a phasing decision, and phasing is
  `/vstack:user-story-map`'s job — the spec says *what*, the story map says *when*. Ids are stable —
  never renumber existing ones on a rewrite.
- A small feature is one epic; don't invent a second epic to look thorough. **Keep the first pass
  lean** — the loop is how it gets rich; a bloated v1 wastes the user's first round on deletions.

## 2 · Serve it

```bash
SKILL=<this skill dir>
LIB="$SKILL/../../lib"
DOC=.vstack/specs/<feature>.json
node "$LIB/json-bridge.mjs" serve --json "$DOC" --template "$SKILL/assets/spec-tree.html" --port 7791 --tool spec
```

Start it with **`run_in_background: true`**. It prints the URL (with its token) — tell the user to
open it. Then arm the waiter, carrying the seq the server printed:

```bash
node "$LIB/json-bridge.mjs" watch --json .vstack/specs/<feature>.json --stream --tool spec \
  --seq <the seq printed when the server started>
```

Start it with the **Monitor tool, `persistent: true`**. How the loop behaves — it never exits, one
event per line, the Linked/Unlinked states, the idle close — is
[`contracts/bridge-loop.md`](../../contracts/bridge-loop.md).

`SENT` means an edited tree landed in the JSON; `CLOSED` means the tab went away — say so and
stop serving. **Pass the seq the server printed** — a send that lands between rounds would be
swallowed; use the seq printed by the previous waiter's output.

## 3 · The round

On `SENT`, read the JSON back:

- **Edited text is the new truth.** Titles, criteria, verifies, the goal, priorities, deletions,
  additions — apply them silently. Don't re-litigate a deletion.
- **Notes are clarifications** — the page presents every note as one kind of thing: a question on
  the spec, with a place to answer. A user-written clarification is the user talking to you: answer
  it by **fixing the spec and removing the note**. When something genuinely needs the user's
  decision, leave your own clarification (`who: "agent"` for provenance; the page renders all
  clarifications identically).
- **Prefer multiple choice when asking.** A clarification can carry
  `"options": ["HR owns the list", "Admins only", "Either, behind a permission"]` — the page renders
  them as radio choices and writes the pick into `"answer"`; without options it offers a free-text
  answer line. **An answered clarification is a decision**: apply it and remove the note in the next
  round.
- Rewrite the JSON (the page offers a *Refresh* bar — it never yanks the tree mid-edit), regenerate
  the markdown (§4), and say in a few lines what changed. Don't ask "shall I
  continue?" — the loop is the point.

## 4 · Generate the markdown, every round

`specs/YYYY-MM-DD-<feature>.md` — date fixed on first creation; later rounds update the same file.
Re-running on a feature that already has a dated spec updates that file, never a second one.

```markdown
<!-- Generated from .vstack/specs/<feature>.json — edit on the spec page (/vstack:spec), not here. -->
# Initiative — <title>

<goal>

**Themes:** <theme> · <theme>

## Epic — As a …, I want to …, so that …

### As a …, I want to …, so that …  `<theme>`

**Acceptance criteria**
- **Scenario:** <scenario>
  **Given** <given> · **When** <when> · **Then** <then> · **And** <and>

> <note>          ← only when the story has one
...
```

The header warning matters: this file is an export. A human editing it directly is editing a
generated file, and the next round will overwrite them.

## Notes

- **Never edit `assets/spec-tree.html` or `lib/json-bridge.mjs`** to fit a project — they're the
  engine; only the JSON document is yours. The shell chrome is stamped in from `lib/shell/` — see
  `lib/shell/README.md`.
- The bridge binds `127.0.0.1` and dies when the tab closes (90s grace). Port busy → another spec
  page is up; pass `--port`.
- **The version timeline is kept on disk**, in `.vstack/local/spec/<feature>.history/` —
  one frozen copy per open, send and rewrite. It survives a reload and carries across rounds, so the
  page opens on the whole trail rather than starting from blank. Nothing to run: the bridge records
  it. If the user wants a version back, the bodies are plain JSON files.
- One review is one feature. Several features means several JSON files served one at a time.
- **Works beside any other tooling.** vstack writes `.vstack/` and plain markdown under `specs/`,
  and touches nothing else — no `.specify/`, no other tool's state, no hooks, no config. If the
  project also uses speckit or another spec tool, both coexist: vstack does not own `specs/`, it
  owns only the files it wrote.

## State & handoff

**No `.vstack/pipeline.json`?** You're standalone — everything above still applies. Take the brief
from the user, write the markdown where they ask (default `specs/`), and skip the rest.

- **Read** `.vstack/pipeline.json` → `artifacts.wireframes[]` for the feature's page,
  `artifacts.product` for the constitution. A missing wireframe isn't a blocker — a spec can come
  from conversation alone; say what it's based on.
- **Write** `artifacts.specs[]` (append for a new feature; replace in place for an existing one —
  match on feature, never on array position) and `stage: "spec"`. If the template's
  `design/README.md` inventory exists, fill the feature's *owning spec* cell.
- **Next** — `/vstack:user-story-map` slices the specs into release phases. Offer to run it; don't
  ask whether to continue.
