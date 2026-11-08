---
name: leonardo
description: Draw the way Leonardo da Vinci drew — a study sheet, a notebook folio, a red-chalk or silverpoint study, a machine cutaway, a storm of vortices — in his real materials and page-logic, generated with the make-art engine and anchored on fifteen of his actual (public-domain) sheets. Use when you say "Leonardo", "da Vinci", "like his notebooks", "a codex page of X", "draw this as one of his study sheets", "sanguine", "silverpoint", or wants a design, diagram, or illustration in that hand. Also a reading guide to his notebooks (Richter's 1883 public-domain translation) for "what did Leonardo say about shadow / trees / water". This is a TASK skill; the engine is `make-art`.
---

# leonardo — his hand, his page, his materials

Not "Renaissance sketch style." Leonardo's sheets have a specific material language and a
specific *page logic*, both measured here off fifteen real drawings listed in
`sheets/CREDITS.md` (where each one is and what was read off it). Run
`python3 scripts/fetch_sheets.py` once to download them from Wikimedia Commons; they are the
style anchors `plate.py` attaches.

**Always label the output** as made in his manner, never as his. Don't use his name to sell
something in customer-facing copy.

## What his sheets actually are (the measured language)

Read off the sheets. Every STEM in `prompts/` is a paraphrase of this list.

- **The page is a working page, never a picture.** Several studies of one thing at different
  scales share a sheet: a main study, sections and cutaways, a detail, a tiny diagram lettered
  *a b c*, an abandoned first attempt left faint. Nothing is centred. Text wraps around the
  drawings, some lines with a thin leader pointing in (fetus sheet, shoulder sheet).
- **Left-handed hatching.** Shadow is parallel strokes running upper-left → lower-right (`\\`),
  close-set, curving with the form, denser where the form turns from the light. He hatches the
  *ground behind* a form to push it forward (skull, Vitruvian's legs). Cross-hatching is rare.
- **Sections and transparency.** A skull sawn in half; a womb opened like a fruit; a machine
  drawn with its casing gone. His way of explaining a thing is to cut it.
- **Motion as hair.** Water, cloud, smoke, wind are nested spirals of dozens of fine parallel
  arcs (the Deluge). Hair and beard are long rhythmic waves (Turin self-portrait).
- **Six material modes**, and they don't mix on one sheet:
  | mode | what it is | the anchor sheets |
  |---|---|---|
  | `ink` | pen + brown iron-gall ink over faint black chalk, brown wash in the deep shadow; the anatomy and machine sheets | shoulder, fetus, flying machine |
  | `codex` | a notebook folio that is mostly *writing*, with diagrams sitting in the text | Arundel opening, Atlanticus 307v, Vitruvian |
  | `chalk` | red chalk (sanguine), one pigment, sfumato modelling | Turin self-portrait, grotesque heads |
  | `silverpoint` | metalpoint on a coloured prepared ground (blue-grey or pink-buff), lead-white heightening | woman's hands, horses |
  | `linen` | brush + grey tempera on prepared linen, pure tone, no line | seated drapery |
  | `deluge` | pen + ink + wash storm/landscape, vortices and hooked strokes | Deluge, 1473 Tuscan landscape |
- **The paper is a character.** Cream-to-buff laid paper aged to ochre at the edges, foxing,
  brown stains, a torn corner, show-through from the verso. The real sheets also carry a
  crowned-ER collector's stamp and inventory numbers — **those are the museum's, not his; never
  ask for them and probe every plate for an invented one** (the engine has forged a real artist's signature unasked; see `make-art`).
- **Mirror script.** Small, even, right-to-left, same ink as the drawing, in blocks. On the
  working pages (`ink`, `codex`) it's most of the surface. The chalk, metalpoint and linen
  studies mostly have **no writing at all** — don't add it where he didn't.

## Step 1 — decide the mode and the aspect before writing a word

The mode is the whole look, so it's the first decision, and it's usually forced by the brief:
a mechanism or an anatomy → `ink`; a page of reasoning with a big diagram → `codex`; a
portrait, a tree, a face → `chalk`; hands, animals, anything about touch and light →
`silverpoint`; cloth → `linen`; weather, water, a valley → `deluge`.

Aspect: `3:4` is a folio and the default; `4:3` for a landscape sheet; `codex` sheets are
always `3:4`. He never drew a 16:9.

**Ask one question if the brief is a subject and nothing else:** working page or finished
study? It sets mode (`ink`/`codex` vs the rest), writing (on vs off) and how many studies share
the sheet. Everything else — aspect, anchors, size — is mine to decide.

## Step 2 — write the SUBJECT as studies, not as a picture

The prompt is STEM (fixed per mode) + SUBJECT (the only variable) + NOTES (per mode) + TAIL
(fixed). `scripts/plate.py` assembles it and attaches the mode's anchor sheets:

```bash
python3 scripts/plate.py --mode ink --aspect 3:4 --size 2K \
  --out art/<slug>/candidates/r1/1-<name>.png \
  --subject "A study sheet dissecting …: one large main study …; beside it three smaller
             studies — …; a tiny diagram in the corner showing …, points lettered a, b, c."
python3 …/plate.py --list-modes          # modes, their default writing, their anchors
python3 …/plate.py … --dry-run           # print the assembled prompt, spend nothing
```

The SUBJECT that works is a *list of studies on one sheet*, each with its scale and view:
"one large main study of X seen three-quarters from above with Y cut open; beside it three
smaller studies — A alone, B in section, C seen from below; a tiny diagram in the corner
showing Z, points lettered a, b, c." Write a picture ("an espresso machine on a table") and
you get an illustration on old paper, which is the standard failure. 

Draft at `2K` (~$0.13); spend `4K` only on the pick. The engine needs network access (`make-art`).

## Step 3 — read the plate against the sheets, then fix the prompt, not the plate

Look at every plate at full size beside its anchor sheet. The three things that actually go wrong, in order of how often:

1. **The writing leak.** Told to write "Renaissance Italian mirror handwriting", the engine
   wrote *"Reall bennifsance Italian mirror Italian mirror right to left"* — my instruction,
   mirrored, along the bottom of an otherwise perfect silverpoint sheet. Told the notes were
   about a piston, it wrote "Piston seal" and "Mechanical advantage" in plain English. **Never
   describe the writing in words it can copy, and never let the SUBJECT's nouns sit near a
   caption slot.** `prompts/notes-*.txt` now says the hand is illegible *by design* and forms no
   word in any language; that cut the leak from a whole sentence to two or three half-English
   labels per `ink` sheet, and to zero on `none`. So: modes without writing default to `none`;
   an `ink`/`codex` sheet with `margin` notes needs a read for leaked English and a re-roll
   (or a crop) if a word survives. Leaks land next to the small studies — check there first.
2. **Right-handed hatching.** The engine hatches `/` about as often as `\\`, whatever the STEM
   says. When the sheet has no legible writing, `--flip` mirrors it horizontally and the
   hatching becomes his; check that the composition survives being reversed (a lettered
   diagram will not — its letters flip). Don't fight this in the prompt; it doesn't listen.
3. **Cartoon foliage.** First red-chalk birches came back as scalloped cloud-lobes. The chalk
   STEM now says foliage is *a mass of tone built from short flicked strokes, never outlined
   lobes*, and the SUBJECT should say "the leaf-masses as soft tone" rather than naming leaves.
   Same rule generalises: name the *tone* you want, not the object the engine has a cliché for.

Then the standard `make-art` probes: edges (these plates are meant to show the sheet's own
torn edges against nothing — that is the design, not a border to trim), and corners for an
invented stamp or signature.

## Step 4 — land it

A folder `art/<slug>/` with a README, finals numbered by rank, `candidates/`, `prompts/`.
`plate.py` writes `<out>.prompt.txt` beside every plate, so the prompts folder is free.

## Reading him (the other half of the persona)

His notebooks are public domain in J.P. Richter's 1883 arrangement (*The Notebooks of Leonardo
da Vinci*, free on Project Gutenberg), in twenty-two books by subject. When the job is *what did he think*
— about shadow, trees, water, how to study, the grotesque, flight — read the book, quote the
paragraph number, and don't improvise. The lines that bear directly on drawing, attested in the book on the practice of painting (Richter paragraph numbers):

- **522.** *"When you draw take care to set up a principal line which you must observe all
  throughout the object you are drawing; every thing should bear relation to the direction of
  this principal line."* — the one rule for a SUBJECT paragraph too.
- **502.** A master who trusts memory over drawing from nature is *"graced with extreme
  ignorance, inasmuch as these effects are infinite."* — why the sheets are studies, plural.
- **523.** The glass-pane method: draw on glass with *"a brush or red chalk"*, trace to paper,
  *"afterwards transfer it onto good paper"* — his own account of the transfer chain that
  ends in pouncing (**628**, the panel recipe: *"Then pounce and outline your drawing finely"*).
- **540.** *"When you draw from nature stand at a distance of 3 times the height of the object."*
- **529.** *"How the mirror is the master [and guide] of painters"* — check a drawing against
  the mirror image of the thing. The reason `--flip` is a legitimate move and not a cheat.

A famous line that isn't in the notebooks isn't his until you find it there. His voice when
not instructing — the fables, the prophecies, the letters asking to be paid — is in books
19–21 and is drier and funnier than the reputation.

## References

- Engine, flags, the paste-to-disk trick, the border probe: `make-art`. Method for a spread off
  one reference: `image-riff`. This skill is a third layer: a fixed language with modes instead
  of a language read off a pasted image.
- `sheets/CREDITS.md` — provenance of the fifteen anchors (all public domain, Wikimedia Commons);
  `sheets/meta.json` is the raw Commons record used by `fetch_sheets.py`.
