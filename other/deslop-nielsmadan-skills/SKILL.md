---
name: deslop
description: Copy-edit text to strip AI/LLM writing tells ("slop") and make it read as human-written — overused words (delve, showcase, robust), significance-inflation phrases ("stands as a testament to", "plays a pivotal role"), scene-setting openers ("in today's fast-paced world"), hedging, em-dash overuse, rule-of-three, and "it's not X, it's Y" parallelism. Use when asked to "deslop", "de-slop", "remove AI tells", "make this sound less like AI/ChatGPT", "make this sound human", or copy-edit a draft (.md, .txt, prose, emails, docs) that reads as machine-generated.
argument-hint: "[file path or pasted text] [--report] [--all]"
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Deslop

Copy-edit text to remove LLM writing patterns so it reads as human-written.

## The core idea

Slop is text engineered to *sound* authoritative while saying little: inflated
vocabulary, formulaic significance-frames, reflexive hedging, and mechanical
structure. The job is **not** find-and-replace from a synonym table — that just
makes *differently* robotic text. The job is to **delete the inflation and
force a concrete specific**, while preserving the author's meaning and voice.

Three rules that override everything else:
1. **Density, not isolated words.** One "crucial" on a page is fine. Act on
   clusters and reflexive use.
2. **Don't over-edit.** Legitimate uses stay; voice and meaning are preserved;
   no facts change. When in doubt, lighter edit + flag it.
3. **Prose only.** Never edit inside fenced blocks, inline code, commands,
   paths, URLs, link targets, or YAML frontmatter. A literal `underscore` in a
   naming rule and `--not --remotes` in a git invocation are not tells.

## Flags

- `--report` — detect and list tells with locations; do **not** rewrite. Use
  when the author wants to edit themselves.
- `--all` — include the low-signal word hits the detector hides on reference
  docs.
- Default — rewrite the text, removing tells, then summarize what changed.

## Workflow

### Step 1: Get the text and mode

- **File path in the prompt** (`.md`, `.txt`, etc.) → read it.
- **Text pasted in the conversation** → operate on that.
- **Neither** → ask the user to paste the text or give a path. Don't proceed
  without input.
- `--report` present → detection-only mode (Step 4 only).

### Step 2: Read the full catalog

Read `references/patterns.md`. It holds the word lists, phrase lists,
structural tells, and — critically — section 4 "What NOT to touch". Don't skip
it; the anti-over-editing guidance is half the skill.

### Step 3: Run the detector for coverage

```bash
python3 scripts/flag.py <file>        # or:  cat file | python3 scripts/flag.py -
```

It masks code, then scans the prose for known tells and prints each with a line
number and category, plus stance-word echoes and em-dash density. It
**over-flags on purpose** — every hit is a *candidate*, not a verdict. Use it so
nothing is missed in long text; then judge each in context yourself. (For pasted
text, write it to a scratch file first, or just scan by eye against the catalog
for short passages.)

It reports a **genre** on the first line, which sets how hard to look:

- **reference** — docs that state behavior (CLI pages, API references, config
  guides). The vocabulary is fixed by the subject, so single-word puffery hits
  carry almost no signal and are hidden; `--all` shows them. What matters here
  is punctuation density, filler, and echoes.
- **persuasive** — pages making a case (landing pages, comparisons, READMEs,
  announcements, instructions written to convince). Everything applies. This is
  where the judgment pass earns its keep.

Override with `--genre` when the detector guesses wrong. A page that argues
inside a reference site is persuasive whatever the surrounding directory.

### Step 3b: Project vocabulary

Every codebase has terms of art the catalog also lists as tells — a *harness*
that is a test harness, a *comprehensive* mode that is a mode name, a literal
*unlock*. Suppress them once instead of re-judging them every run:

```
# .deslopignore at the repo root — one term per line, # comments allowed
harness
comprehensive
```

The nearest `.deslopignore` walking up from the file is used, merged with a
machine-wide `$XDG_CONFIG_HOME/deslop/ignore` (default
`~/.config/deslop/ignore`) for terms that recur across every project. `--ignore
a,b` adds more for one run. Suppressed hits are reported as a count, never
silently — if that count is large, the list may be hiding a real tell.

**Offer to add a term** when you dismiss the same word as a term of art twice in
one pass. Don't edit the ignore file without asking.

### Step 4: Edit (or report)

**Report mode (`--report`):** present the detector's findings grouped by
category, add any structural/tonal tells the script can't catch (rule-of-three,
both-sides non-conclusions, copula avoidance, over-bolding), and stop. Don't
rewrite.

**Default (rewrite) mode:** for each candidate, decide in context:
- **Delete** the inflation when it adds nothing ("plays a pivotal role in" →
  state what it does, or cut). This is the most common fix.
- **Replace** with a concrete specific or a plain word when one fits — but
  **vary** replacements; don't turn every "delve" into "explore".
- **Keep** legitimate/technical/literal uses and intentional voice.
- **Restructure** the tics: collapse rule-of-three to one precise word, undo
  "not X, it's Y" to the positive claim, restore normal punctuation for
  overused em-dashes, turn copula-avoidance ("serves as") back into "is",
  cut reflexive "In conclusion"/"Overall" wrap-ups.
- **Break stance echoes.** When one evaluative word carries the framing three or
  more times ("an *honest* look" … "taking the survey *honestly*" … "the
  *honest* flip side"), the text is asserting a judgment it is already
  demonstrating. Keep the one instance that does work and cut the rest — don't
  reach for synonyms, which just relocates the tic.

Preserve formatting that helps; convert reflexive bolding/emoji-bullets/
over-headed text back to prose where prose reads better.

**Em-dash density is relative to the author, not absolute.** The detector's
3/1000 threshold is a prompt to look, not a target. A writer whose own notes run
at 15/1000 is using dashes as voice; the same rate in a page written for
strangers reads as a tic, because the reader has no baseline for it. Sample a
few documents the author wrote for themselves before deciding a count is high,
and trim toward the reader rather than toward zero.

### Step 5: Output

- **File input:** apply edits and show a concise diff (or write a `*.deslopped`
  copy if the user prefers not to overwrite — ask if unsure for important
  files).
- **Pasted input:** return the cleaned text.
- Then add a short **changelog**: what categories you cut/changed, and — just as
  important — **what you deliberately left** and why (e.g. "kept 'robust' — it's
  the statistical term of art here"). This builds trust and surfaces judgment
  calls for the user to override.

## Examples

### Example 1: Rewrite a draft file

User: "deslop blog-draft.md"

1. Read `blog-draft.md` and `references/patterns.md`.
2. `python3 scripts/flag.py blog-draft.md` → 18 candidates, em-dashes 4.1/1000.
3. Edit: cut the "In today's fast-paced world" opener; "stands as a testament
   to" → "shows"; collapse "powerful, flexible, and intuitive" → "flexible";
   undo two "it's not X — it's Y" constructions; restore commas for 5 of 7
   em-dashes; keep one literal "landscape" (about hiking).
4. Show diff + changelog noting the literal "landscape" was kept.

### Example 2: Report only

User: "run deslop --report on this" + pasted text

Write text to a scratch file, run `flag.py`, present findings grouped by
category with line refs, add the structural tells the script misses, and stop —
no rewrite.

### Example 3: A docs directory

User: "deslop the user docs"

1. Run `flag.py` over each file. Most come back `genre: reference` with nothing
   flagged — say so plainly rather than manufacturing edits.
2. The comparison page comes back `genre: persuasive`, with `3× honest/honestly`.
   Read it: the page asserts even-handedness three times while already
   demonstrating it. Cut two, keep the one carrying weight.
3. Two suppressed hits were `harness`, a term of art in this repo — offer a
   `.deslopignore` entry so the next run doesn't re-raise them.
4. Report per file, and name the files you changed nothing in.

### Example 4: Pasted paragraph

User: "make this sound less like ChatGPT: <paragraph>"

Scan against the catalog (short enough to skip the script), rewrite removing
the tells, return the cleaned paragraph + a one-line note on the main changes.

## Troubleshooting

### The rewrite reads flattened / lost the author's voice
**Cause:** Over-editing — mechanical removal of every flagged word, including
ones that carried tone or precision.
**Solution:** Re-read section 4 of `references/patterns.md`. Act on density, not
every hit; keep intentional register; prefer deleting *empty* inflation over
swapping *every* word. Offer a lighter pass.

### The detector flagged a legitimate word (literal "landscape", "robust" in stats)
**Cause:** The script over-flags by design; it can't see context.
**Solution:** Keep the legitimate use and note it in the changelog. The script
is a coverage net, not a judge — you decide. If the same word is a term of art
in this codebase and will recur on every run, offer to add it to
`.deslopignore` rather than re-judging it each time.

### The report is all noise on a reference doc
**Cause:** Running with `--all`, or a genre misdetection on a page that is
mostly prose about a command surface.
**Solution:** Drop `--all` and trust the demotion. Single-word puffery is close
to meaningless where the vocabulary is fixed by the subject — on that kind of
page the real signals are echoes, filler, and punctuation density.

### Replacements themselves sound like AI
**Cause:** One-to-one synonym swapping across the whole text creates a new tell
(every "delve" → "explore").
**Solution:** Vary word choice, or — better — delete the inflated frame and
state the concrete point. The catalog's guiding principle is deletion over
substitution.

### Nothing flagged but it still reads like AI
**Cause:** The real signal is structural/tonal (formulaic arcs, both-sides
non-conclusions, even paragraph rhythm, vague claims), which a word list can't
catch.
**Solution:** Apply section 3 of the catalog by judgment: vary sentence length,
land conclusions on a position, replace vague claims with specifics, break the
intro-body-summary template.
