---
name: logo
description: Design a logo or mark through reference study, generated concept rounds, and a browsable contact sheet the user picks from. Use "/logo new <brief>" to start, "/logo round <dir>" to rebuild a sheet, "/logo ship <dir>" to emit final assets.
user-invocable: true
argument-hint: "new <brief> | round <dir> | refine <concept-id> | ship <dir>"
allowed-tools: Bash(node *, uv run *, python3 *, curl *, mkdir *, cp *), Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, AskUserQuestion
---

# Logo Skill

You are designing a mark. The user picks; you generate, render, and narrow.

## Path Variables

- `SKILLS_DIR` = this skill's directory (where `SKILL.md` lives)
- `SCRATCH` = the session scratchpad directory, or `$(mktemp -d)` if none is
  given. **Concepts and contact sheets never go in the user's repo** — only the
  final chosen assets do

## Dispatch

- `new <brief>` → follow [explore.md](explore.md) from the top
- `round <dir>` → rebuild and serve the contact sheet for `<dir>` (step 4 of
  explore.md). Use when concepts changed and you want a fresh look
- `refine <concept-id>` → re-enter explore.md at the refinement round with that
  concept as the seed
- `ship <dir>` → follow [ship.md](ship.md) to emit final assets
- anything else → list the subcommands above and stop

## Requirements

- **Node** for the contact sheet. No dependencies
- **`uv`** only if you bake typeface outlines (`outline.py` pulls `fonttools`
  and `uharfbuzz` on demand). Purely geometric marks do not need it
- A way to view a rendered page. The sheet is served over HTTP precisely so a
  headless browser can reach it

---

## Non-negotiables

These are not style preferences. Each is here because skipping it produced a
visibly worse result, and they are ordered by how much damage they do.

### 1. Study real work before generating anything

Generating first and looking at references later does not work. Asked for *N*
concepts cold, you will produce *N* samples from one distribution — the same
monoline geometric stroke drawing, wearing *N* hats. It reads as generic because
it *is* the generic default, and it is the house style of every automated logo
tool.

Breadth has to come from outside. [references.md](references.md) is the step
that supplies it. Do not skip it because the brief seems obvious.

### 2. Render it and look before showing it to anyone

You cannot judge a mark from its path data. Build the contact sheet, open it,
and look at the pixels before presenting.

This is not a formality. Real bugs that survived review-by-reading: a letter
whose stem was missing its top half, a subtitle whose ascenders punched through
the word above it, a mark sized so small beside its wordmark that it read as a
bullet point. All three were obvious in a browser and invisible in the markup.

### 3. Judge at 16px

The sheet renders every concept at 16px for a reason. That is the size a favicon
is actually used at, it is the size that eliminates candidates, and it is the one
nobody looks at until the thing ships.

What it reliably decides:

- **Solid fills survive; strokes close up.** A stroked ring at 16px fills in
- **Detail is a liability.** A 10-stroke CJK glyph at 16px is texture, not a
  character. Two of them is a smudge
- **Silhouette beats interior.** A circle among square favicons is identifiable
  even when nothing inside it resolves

### 4. Never bake in an assumption about the person

If a mark depends on a fact about the user — what their name means, which
characters it is written with, what a symbol signifies in their culture — **ask
before building it**, with AskUserQuestion.

You will otherwise produce a confident, polished, well-executed artefact built on
a guess, and the guess will not be visible in the output. A name that sounds like
a common word usually is not one.

### 5. Use real typeface outlines, not hand-rolled letterforms

Hand-drawn geometric letters look like a template and carry bugs. Bake outlines
from a real face with `SKILLS_DIR/scripts/outline.py` and freeze them as path
data: correct contrast and kerning, no webfont request, no flash of fallback
type.

The trade: baked outlines fix the string. If the wordmark text might ever be
localised or edited, say so at the time — it has to stay live text.

### 6. Decide colour by comparison, not theory

Put candidate palettes side by side in the sheet and look. Two colours that are
defensible individually can fight when adjacent — near-complementary pairs
especially. The fix is usually not a different hue but removing one from the
pairing.

### 7. The user picks, at every gate

Never advance a round on your own taste. Present, recommend with reasons, and
wait. Say plainly which candidates you would cut and why — an opinion is useful,
a decision is not yours.

---

## Anti-patterns

| Smell | What it actually means |
| ----- | ---------------------- |
| Every concept shares one skeleton | You produced one concept, *N* times. Go do the reference study |
| All strokes, uniform weight | The generated default. Try solid fills, real type, or no mark at all |
| A mark for its own sake | Plenty of strong identities are type plus one colour. "No mark" is a candidate |
| Judging from the SVG source | You have not seen it. Build the sheet |
| A concept that needs its name explained | If it needs explaining it is not reading. The 16px column is the test |

## Tooling

| Need | Command |
| ---- | ------- |
| Contact sheet + local server | `node SKILLS_DIR/scripts/gallery.mjs <dir> [--port N] [--title T] [--no-serve]` |
| Bake typeface outlines to paths | `uv run --with fonttools --with uharfbuzz python SKILLS_DIR/scripts/outline.py` |

`outline.py` reads a JSON job list on stdin and writes JSON on stdout. Source
faces come from `LOGO_FONT_DIR` (default `.fonts`), or a job may name an absolute
path. See [ship.md](ship.md) for the job shape and the traps.
