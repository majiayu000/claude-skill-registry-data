---
name: ascii-design
description: Use when explaining a system in plain text with diagrams — a PR body, a code comment, a README, a terminal doc, an ADR, a commit body, a Slack post, a design note. Produces monospace-grid diagrams on a three-tier character contract (pure ASCII / box-drawing / emoji badges), with shape carrying kind, left-gutter tags carrying subsystem, lanes carrying owner, and two typographic registers so a reader can always tell the code from your narration. Ships a linter that fails on width shear, tier violations, and off-grid junctions. Pick this over narrative-diagram when the output must survive as text — no HTML, no Mermaid, no renderer.
---

# ASCII design system

The plain-text counterpart to [`narrative-diagram`](../narrative-diagram/SKILL.md). Same doctrine —
shape carries kind, a second channel carries subsystem, lanes carry owner, prose and symbols never
share a face, a legend sits above the diagram it explains, a plain-language notes list closes the
doc. The medium is different, so the mechanics are: the renderer is a monospace grid you lay out by
hand, and the failure mode is not a mermaid parse error but a diagram that silently shears apart in
somebody else's terminal.

## The core discipline

*One cell, one column.*

Width is not a style question here. A single double-width glyph shifts the rest of its line one cell
right, so the box that was square arrives at a colleague's terminal as a parallelogram, and nothing
in your own viewer will have told you. The tier contract and the lint script both exist to make that
class of failure impossible to ship rather than merely unlikely.

## Rules

### Tier contract

1. **Declare a tier and never mix down.** Three character tiers, each with a stated compatibility
   contract. Pick the *lowest* tier that carries the meaning, then use only that tier's characters.

   | Tier | Character set | Safe in | Use for |
   |---|---|---|---|
   | **A** — ASCII | `+ - \| / \ < > ^ v ( ) [ ] { } . ' * = : #` | everything: code comments, logs, `git log`, email, any terminal, any font | source-embedded diagrams, commit bodies, anything that might be grepped or re-indented |
   | **B** — box-drawing | Tier A plus U+2500–U+259F (`─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ━ ┃ ┏ ═ ║ ╔ ╭ ╰ ┈ ╌ █ ▌`) | any UTF-8 terminal or Markdown renderer with a real monospace font | the default for docs, READMEs, PR bodies, design notes |
   | **C** — badges | Tier B plus a small fixed emoji set, **left gutter only** | Slack, GitHub Markdown, chat | scannable status lists where a reader triages before reading |

2. **A badge line carries no box art, and a diagram line carries no badge.** Almost every emoji is
   East-Asian **Wide**, and inside a GitHub or Slack code fence the actual advance width varies by
   platform — 1.5 cells here, 2 there. So a badge cannot be trusted to hold a column, which rules it
   out of anything that has to line up. Tier C badges annotate **list rows**, where each line stands
   alone and a width shift moves only that row's own text:

   ```
   🟢  merged            41 units
   🟡  waiting on a PR   12 units
   🔴  failed             3 units
   ```

   Inside a diagram, the same channel is carried by a bracketed Tier A tag in the left gutter
   (`[ok]`, `[wt]`, `[er]`) — fixed width, same meaning, no assumption. This is why Tier C is an
   addition for a *different kind of artifact*, not a richer way to draw the same diagram.

3. **Geometric shapes and arrows (`▶ ◀ ▲ ▼ → ← ↑ ↓ ◆ ●`) are East-Asian *Ambiguous*.** They are one
   cell in a Latin locale and two cells in a CJK-configured terminal — the worst class of character,
   because it renders correctly on your machine and shears on a colleague's. Tier B arrowheads are
   `>` `<` `^` `v` (Tier A characters, deliberately). Reserve `▶`/`▼` for Tier C, where you have
   already accepted a rich-text renderer.

   Box-drawing is formally Ambiguous too, which is the one width assumption Tier B does make. It is
   accepted on a specific argument: a picture built entirely of box-drawing scales as a unit, so a
   viewer that doubles them doubles every line together and the picture still holds. One `→` in a
   line of Latin text doubles alone and shears that line only. Tier A is the only tier that assumes
   nothing; drop to it whenever the diagram will live somewhere you cannot see.

### Shape carries kind

4. **A shape means one kind of thing, consistently across every diagram in the doc.** This is the
   channel a reader decodes first, so overloading it costs the most. The grammar, Tier B on the
   left, its Tier A degradation on the right:

   ```
    step / method call        actor, class, service      external boundary
    ┌──────────────────┐      ┏━━━━━━━━━━━━━━━━━━┓       ╔══════════════════╗
    │ evaluate()       │      ┃ Orchestrator     ┃       ║ GitHub           ║
    └──────────────────┘      ┗━━━━━━━━━━━━━━━━━━┛       ╚══════════════════╝
    +------------------+      +==================+       #==================#

    datastore / table         observed event             narration, no symbol
    ┌──────────────────┐      ( minion.merged )          ╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╮
    ├──────────────────┤      ( . . . . . . . )          ┊ nobody is coming ┊
    │ medusa_batches   │                                 ╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╯
    └──────────────────┘                                 . . . . . . . . . .
   ```

   The datastore's tell is the **shelf** — a `├───┤` rule directly under the top edge, the way a
   table header reads. The narration capsule is **dashed and never filled**, so an assertion you are
   making is visibly not a thing that exists in the code.

   An ORM model is both a class and a table, so pick by what the diagram is about and hold it for
   the whole doc: heavy when you are drawing objects that call each other, the shelf when you are
   drawing rows and columns. Drawing the same model both ways in one doc tells the reader the shape
   means nothing.

5. **Decisions are gate rows, not diamonds. The diamond is the bug.** A text diamond costs five
   lines to say one word and cannot hold a real label. Write the condition once with a `?`, then fan
   the answers out on the outbound edges — the same information, three lines, and the branch labels
   land where the reader's eye already is.

   ```
   BAD                       GOOD
        .                    <> stack_on_blocker?
      .   .                     |
    . one? .                    +-- exactly one blocker --> stack on it
      .   .                     |
        .                       +-- none, or 2+ ---------> wait for merge
   ```

   `<>` is the gate marker in every tier. It has no Tier B upgrade: `◆` is Ambiguous, and a gate row
   is exactly where a width shift would drag every branch label out of alignment.

### Registers

6. **Two typographic registers, and never one.** Text has no bold and no color, so the register
   split from `narrative-diagram` rule 12 has to be carried by case, delimiters, and column. The
   failure this prevents: every line in the box is lowercase prose in the same face, so a real method
   name, a table name, and a sentence you invented all look identical, and the reader cannot tell the
   map from the commentary.

   - **Symbols** — a real, greppable identifier — go bare, exactly as they appear in the source, with
     their call parens: `stack_on_blocker()`, `PR_OPEN_PHASES`, `medusa_work_units`. Never reword,
     never pluralize, never drop the namespace when it disambiguates.
   - **Narration** — your prose — goes on its own line inside the box, indented one space and led by
     `*`, lowercase, no terminal period. The lead is ASCII in every tier: `·` is the prettier choice
     and it is East-Asian Ambiguous, so on a colleague's terminal it takes two cells and pushes the
     box's closing wall out of column.
   - A box with narration and no symbol is a **dashed capsule** (rule 4), not a solid one.

   ```
   ┌────────────────────────────────┐
   │ stack_on_blocker()             │  <- symbol: greppable, verbatim
   │  * picks the one branch to     │  <- narration: led, indented, mine
   │    fork from, or nothing       │
   └────────────────────────────────┘
   ```

7. **Never let authored prose sit flush against a symbol on the same line.** If they must share a
   line, the symbol comes first and the narration follows after ` * `, never before. A reader
   scanning the left column should see only real names.

### Layout

8. **Lanes carry the owner.** Group steps by who executes them, one labelled column or one labelled
   band. A round trip back into an earlier lane is the single most valuable thing a diagram can show,
   and it is invisible without lanes.

   ```
   Orchestrator          │ WorkUnit             │ GitHub
   ──────────────────────┼──────────────────────┼─────────────────────
    evaluate()           │                      │
        │                │                      │
        └──────────────> │ dependencies_        │
                         │ satisfied?           │
                         │      │               │
        <────────────────┴──────┘               │
    dispatch_unit()      │                      │
        └────────────────┼─────────────────────>│ open PR
   ```

9. **Gutter tags carry the subsystem or status.** A bracketed two-letter tag (`[pl]`, `[ex]`,
   `[db]`) at the far left, before the box art, one per line. One tag means one subsystem, reused
   identically in every diagram in the doc — the same discipline as reusing one hex per subsystem in
   a colored diagram. Never invent a tag for a single use. Emoji badges are the Tier C form of this
   channel and are confined to list rows by rule 2; they never appear beside box art.

10. **Flow is top-down by default; left-right only when the chain is short and linear.** Vertical
    scales — a fourteen-state machine reads fine as a column and is unusable as a row that wraps.
    Wrapping is the hard failure mode of text diagrams: a wrapped line does not degrade, it becomes
    noise. Hard-cap every diagram line at **80 display columns** for anything that lands in a code
    comment or a terminal, 100 for a Markdown doc.

11. **Align on a column grid, not by eye.** Pick box widths from a small set (say 20 / 28 / 36
    columns) and reuse them, so parallel boxes line up and edges run straight. Ragged widths are the
    single most common tell of a hand-drawn diagram that nobody checked.

12. **The unit is title, legend, diagram — and the doc closes with notes.** Same as
    `narrative-diagram` rules 5 and 8, with one addition the medium forces: a text diagram gets
    pasted into a ticket, a chat, or a review comment stripped of everything around it, so those
    three lines travel together or the diagram arrives unreadable. The legend belongs directly above
    the diagram it explains rather than once at the top of a long doc, and it names only the channels
    that diagram actually uses. The doc then closes with three to six plain sentences a reader who
    skipped every diagram could still act on: what is new, what you deliberately left out, and what
    is true in production but not visible in the picture.

## Legend strips

Two rows, matching the two channels the reader must decode. Keep the chips shaped like the thing they
describe, so the legend teaches the grammar rather than just labelling it.

```
kind    ┌ step ┐   ┏ actor ┓   ╔ external ╗   ├ store ┤   ( event )   ╭┈ note ┈╮
reads   symbol_name()  verbatim from source     *  narration, mine, not the code
```

## Badge set

*Tier C list rows only. Inside a diagram this channel is the bracketed tag in the left gutter.*

| Badge | Tag | Means |
|---|---|---|
| 🟢 | `[ok]` | succeeded, satisfied, merged |
| 🔴 | `[er]` | failed, refused, aborted |
| 🟡 | `[wt]` | waiting, blocked, queued |
| 🔵 | `[rn]` | running now |
| ⚪ | `[na]` | not applicable, skipped by design |
| 🗄 | `[db]` | a database write |
| 🌐 | `[ex]` | leaves the process: network, GitHub, k8s |
| ⚠️ | `[!!]` | a trap: the thing that surprises readers here |
| 🆕 | `[nu]` | new in this change |

Nine is the ceiling, and reaching for a tenth is usually the signal that one artifact is carrying
two stories and wants to be split rather than extended.

## Worked example

`references/worked-example.md` renders a dense, heavily commented Rails model (`Medusa::WorkUnit`)
in this system, and is the only place all four channels appear in one doc: status ladder, stacking
decision as a gate row, lane diagram, notes list.

`references/worked-example-timeline.md` renders a quantity-over-time trace (a game's line-tension
fight) with threshold crossings, aligned input/timer band rows, and a gate row for the outcome —
the shape to copy when the story is a value moving against limits rather than steps in a flow.

`references/worked-example-render.md` renders a render-pipeline guide (Project Zomboid's
isometric frame) with spatial pictures on the tile grid, nested depth-axis spans, a bar chart,
tilesheet strips, and a two-lane Java/Lua timeline — the shape to copy when the story is where
things sit, what occludes what, and in what order they paint.

`references/glyphs.md` is the character inventory per tier, with the width class of every character
and the Tier A degradation of every Tier B form.

## Generating a diagram

Prefer generating over typing. A hand-laid box can shear the moment someone lengthens a label;
a generated one computes its own width and cannot.

```
SHAPE=~/.claude/skills/ascii-design/scripts/shape.py
python3 $SHAPE box "text" --title NAME --kind store
python3 $SHAPE graph spec.json --tier b
```

`box` wraps and frames one block of text. `table`, `frame`, `tree`, and `seq` cover the shapes that
are not flows, and are described below. `graph` takes a JSON spec of nodes and edges, layers it
top-down by longest path, centres each layer, and routes orthogonal edges that merge into real tees
where they meet — run `shape.py demo` for a spec to copy. `gate` builds a rule-5 gate row from a
condition and a list of answers, putting every arrowhead on one column. `rows` emits badge list
rows. `--kind` selects the shape grammar from rule 4 (`step`, `actor`, `external`, `store`, `note`),
and `--tier a` re-renders the identical layout in pure ASCII.

An edge that skips a layer takes its own margin column rather than dropping straight through the box
in between, where it would be swallowed and vanish from the picture.

### The other four generators

Not every picture is a flow. `table` takes `{"rows": [[cell, ...], ...]}` and sizes each column from
its content — `--header` rules off the first row, and `"aligns": ["l", "r"]` right-aligns the
columns you name, which is what numbers want. `frame` puts a block of text in a box, with
`--numbers` for a line-number gutter, so a code excerpt can sit in a diagram without the reader
losing where it starts and ends. `tree` turns an indented outline into branches, taking the
indent from the text itself so any consistent unit works, and treating a dedent past every open
level as a new root. It draws two ways. `--style indent` runs down the page, which suits a file
listing or anything with long labels. `--style right` puts the root on the left and centres every
parent on the span of its children, which is the one to reach for when the shape of the hierarchy
is the point:

```
        ┌─Android
        │                 ┌─Lubuntu
        │        ┌─Ubuntu─┼─Kubuntu
──Linux─┼─Debian─┤        └─Xubuntu
        │        └─Mint
        ├─Centos
        └─Fedora
```

`seq` reads `Actor -> Actor: message` a line at a time (`<-` points the other
way), stands each actor up as a column, and widens the gaps until every label fits its own span:

```
┌──────────┐                      ┌─────────┐
│ Renderer │                      │ Browser │
└──────────┘                      └─────────┘
      │       BeginNavigation()        │
      ├────────────────────────────────>
      │       CommitNavigation()       │
      <────────────────────────────────┤
```

Actors stand in first-seen order, so `A -> C` before `B -> C` puts C in the middle. Reorder by
mentioning the actors in the order you want them read. Arrowheads are ASCII `>` and `<` rather than
the `▶` a renderer would use, because those are East-Asian Ambiguous and would shear the lifelines.

### Styling

A kind is what a thing *is*; a border is what it looks like. Every kind has a default border, and
`--border` (or `"border"` on a node) overrides the look without touching the meaning — pick from
`single`, `bold`, `double`, `rounded`, `dashed`, `ascii`. Two more per-box switches: `--shadow`
casts a `░` under the right and bottom edges, and `--titlebar` sets the title into the top edge as
`╭─ Title ──────╮` instead of giving it a row inside the box.

Override the border only when the diagram is decorative or the kinds are already carried some other
way. In a diagram that means something, rule 4 is doing real work and repainting a `store` as
`double` says "external boundary" to the reader whatever you intended.

`"groups"` wraps a run of siblings in a titled container:

```json
{"groups": [{"title": "Your Home WiFi", "nodes": ["iphone", "robot"],
             "border": "rounded", "shadow": true}]}
```

Wires cross a container wall rather than being blocked by it, and a shadow never breaks a wire that
passes through it. A container can only wrap nodes that share a layer, and says so rather than
guessing: if one member is downstream of another, or of a node outside the group, there is no row
the container could occupy, and the fix is to the flow rather than to the grouping.

Siblings in a layer share a width and a height, which is rule 11 enforced rather than trusted. It
also removes a specific misreading: a short sibling closing on the same row where a taller one draws
an inner rule looks like one box with something hanging off it. `--ragged` gives back the natural
widths; the shared height is not optional.

Before printing, the generator grades its own output with the linter below and exits 1 if anything
fires, so it cannot hand you a diagram the checker would reject.

Diagrams go to stdout and the width report to stderr, so `shape.py graph g.json 2>/dev/null` pastes
straight into a doc. That report always names the Tier B bet in cells: how far the picture would
shear for a reader in a CJK locale, where the box art doubles and the Latin text inside it does not.

Hand-editing generated output puts you back on the hook for the grid. Change the spec and re-run.

## Checking a diagram

Column drift is not something the eye is good at, which is the whole reason this script exists.

```
python3 ~/.claude/skills/ascii-design/scripts/ascii-lint.py FILE --tier b
```

It extracts fenced blocks (`--raw` for a whole file) and fails on characters outside the declared
tier, a badge sharing a line with box art, lines over the column cap (`--cols`, default 100; pass 80
for anything headed into a code comment), tabs, trailing whitespace, CRLF, an unclosed box edge, a
junction one column off its lane wall, and a branch arrowhead that misses the column its siblings
share. Those last two are the ones worth having a machine for: a rule that drifted one column during
an edit is invisible to a reader and unmissable to a column scan.

Finding no blocks is itself an error, so a path typo or an unfenced diagram cannot come back looking
like a pass. Exit zero means the diagram will not shear; whether it communicates is still your eyes.

## Common pitfalls

- **Mixing tiers inside one diagram.** A `+---+` box beside a `┌───┐` box reads as two different
  kinds of thing, because rule 4 says shape means kind — you have accidentally said something.
- **A badge on a diagram line.** Its advance width is not yours to predict, and it is the one
  failure that is invisible to the author, because it renders correctly in the editor you wrote it
  in. Badges annotate list rows; diagrams get the bracketed tag.
- **An unfenced diagram.** The `*` narration lead turns into an emphasis marker, the pipes in a lane
  diagram can start a table, and the next formatter in the chain reflows the rest. Fence every
  diagram, including in a commit message where fencing is only a convention.
- **Using `→` because it looks nicer than `->`.** It is Ambiguous width, so the improvement is
  local to your locale and the shear it causes is not.
- **Prose in the symbol register.** Writing `checks if deps are ok` where a real method name goes
  destroys the reader's ability to grep the diagram back into the codebase. If there is no symbol,
  it is a dashed capsule.
- **Trailing whitespace inside boxes.** Invisible on screen, and it makes every future diff of that
  diagram noisy for reasons the next reader cannot see.
