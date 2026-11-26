---
name: reference-image-library
description: "Use when auditing or deduping a reference-image library."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [images, assets, canon, dedupe, generation]
    related_skills: [studio-universe, studio-workflows, image-model-craft]
---

# Reference image libraries

Every generation pipeline accumulates images: **canon sources** (the ground truth for a character or
product), **retouches** of those sources, and **derived plates** (crops made for one reference slot).
A request to "clean up the duplicates" usually arrives at a folder that looks redundant and is not.

## When to Use

- A folder of character, product or set images is called out as "full of duplicates" or "too big".
- A reference image must be renamed, moved, re-encoded or deleted, and something may depend on its path.
- Deciding whether two near-identical files are the same artwork.
- Someone wants the library reduced to "one sheet per character/product" and you need to say what that
  actually costs.
- Someone wants to know whether one reference strategy beats another (sheet vs crops) and you need a
  comparison that can actually be judged.

## Order of work

1. **Inventory before opinions.** Size, dimensions and hash every file; group by directory
   (`character`, `product`, `set`). Report the total so the user knows whether the problem is even
   size.
2. **Find the consumers of every path.** A file is only deletable if nothing names it.
3. **Prove duplication or disprove it.** Native-resolution comparison, never a thumbnail.
4. **Then** propose: delete genuine duplicates / re-encode heavy files / restructure. These are three
   different jobs with different blast radii; do not bundle them into one answer.

## Paths are load-bearing keys

Before renaming, re-encoding or deleting anything, find every consumer:

```bash
# structured pointers (registry, manifest, catalog)
grep -rn '<filename>' registry.json PLATES.md <library>/*/*.md
# saved/generated specs: runtime state that fails later, at regeneration time
grep -ohE '[a-z0-9/_-]+\.(png|jpg|jpeg|webp)' /path/to/storage/*/spec-*.json | sort | uniq -c
# code that resolves a spec's reference list, and existence assertions in tests
grep -rn 'references' packages/*/src/*.ts | grep -i 'map\|resolve'
grep -rn '\.png\|\.webp' packages/*/test/*.ts | grep -i 'exist'
```

Two failure shapes to expect, both silent:

- **Specs store paths, and they outlive the folder.** A moved plate fails at render time, weeks later,
  with an error that names the plate and not the rename.
- **A test asserts existence.** A registry entry plus an `existsSync` check turns a cleanup into a red
  suite; that is a feature — it is the only thing that catches the break before a render does.

## Proving duplicates

```bash
shasum -a 256 a.png b.png                 # byte-identical? almost never
compare -metric RMSE a.png b.png null:    # native resolution, same pixel dimensions
```

Read native-resolution RMSE as: **≈0.00–0.02** the same artwork (a retouch, a re-encode, one region
painted over); **≥0.25** different artwork, however alike the filenames are.

Two methods that lie on this data, both tried:

- **RMSE on squashed 64×64 thumbnails.** Crops of one figure and different characters collapse to
  the same smudge, and non-square sheets are distorted by the resize — every pair looks related.
- **dHash / perceptual hashes on multi-panel sheets.** 9×8 hashing over a five-panel character sheet,
  or a PNG with alpha, returns "same artwork" across _different characters_.

Check dimensions before concluding too: two files at the same 2048×1152 are candidates for being the
same sheet; `350×225` beside `512×1152` is a face crop beside a full-body crop — a derivation chain,
not duplication.

## What the cleanup actually is

- **Genuine duplicates** — same artwork, same role: delete the redundant copy and update every
  pointer in one commit.
- **Derived crops** — only removable if the references that use them are rewritten too; usually keep
  them. Per-character file counts of 5–8 are normal for canon + retouch + 3–4 slots.
- **Encoding weight** — the usual real problem. PNG sheets at 2048×1152 run 2–2.7 MB; WebP q92 at the
  same dimensions is ~92% smaller, while PNG recompression saves only ~5%. Convert, then update
  every path holder, and record that a lossy file is no longer the canon source.

```bash
magick sheet.png -strip -quality 92 sheet.webp     # ~92% smaller
```

### Execute the re-encode in an order that cannot lose art

Converting is the easy half. Do it as one pass with the old file still on disk until the new one
verifies:

```bash
# per file: convert, then compare pixel dimensions before deleting anything
magick "$f" -strip -quality 92 "${f%.*}.webp"
sips -g pixelWidth -g pixelHeight "$f"   "${f%.*}.webp"   # must be identical
rm "$f"
```

Then, in the same commit, rewrite every consumer: registry/manifest, the plates doc, character docs,
the test fixtures, and the saved specs under project storage. Finish by running the existence test
and a resolution sweep — the sweep is the real proof, the rewrite script's own counter is not.

Three things that break the rewrite:

- **Counting replacements undercounts.** Counting unique basenames per file reports 7 when 15 paths
  changed. Count occurrences, and trust only a sweep that resolves every path in the registry and
  every spec's `references` list.
- **Compound fields are not broken paths.** A `derived_from` of `"a.webp + b.webp"` splits into two
  valid files; a naive existence check reports the whole string missing. Split on `+` before
  validating, or you will "fix" a correct registry.
- **A lossy source does not get a second lossy pass.** Re-encoding the only photoreal ground truth
  (a JPEG photo) stacks a second generation of loss on the reference every render depends on. Leave
  it, and say in the plates doc why it is the one exception.

## One shape per character folder

Once a strategy is settled, make every folder read the same way — the point of the cleanup is that
a future reader opens any character and finds the same slots:

```
<character>/
  PROMPT.md        canon: prompt block(s), rules, failure modes
  turnaround.webp  the render reference — front, three-quarter, profile, back, head
  photoreal.jpg    visual ground truth for a photoreal register, where one exists
```

Three rules keep a rename from breaking the pipeline:

- **A rename is a registry change.** The compiler resolves a character's canon by the `bible` path in
  the registry and extracts marker-to-marker blocks from that file, so renaming a canon doc without
  repointing the registry turns every compile into `MARKER_NOT_FOUND`. Rename and repoint together,
  then run the compile/fixture suite — it is the only proof the markers still land.
- **A photoreal source is not a spare copy of the sheet.** A sheet is a cel render reference; a
  photoreal source is what a photoreal frame is checked against. Uniform naming, yes; deleting the
  photo because "the sheet covers it" leaves that register with no reference at all.
- **Historical records keep their old paths, annotated.** A generation record listing the inputs it
  actually used stays accurate after those inputs are retired: add a one-line note that the paths are
  historical instead of rewriting them, and never feed such a record to an existence sweep that then
  "fixes" a correct file.
- **Uniform names cost the filename, so refer to the folder.** Once every character carries
  `turnaround.webp`, a log line, an error message or a grep result that prints the basename prints
  four identical strings and tells you nothing about which character broke. Print and ask for
  `character-c/turnaround.webp`, and when a skill logs attached references, log the parent segment too.
- **An adopted sheet is a registry change, not a copy.** Dropping the chosen render into the folder
  leaves it invisible: the compiler attaches what the registry names. Set the sheet's reference slot
  (`plates.turnaround` here) in the same change, retire the crop or plate that fed it, repoint any
  spec or fixture that named the retired path, and run the existence test — a sheet nobody attaches
  looks exactly like a working library.
- **A missing sheet is generated with the canon attached, then chosen by the user.** When the ask
  needs art that does not exist (a character whose only source is a photo or a face crop), render
  candidates with that character's existing references attached — a verbatim prompt with no
  references drifts, and the drift is then baked into the canon. In the studio image skill that means
  `--ref <bible path>` (repeatable, `--prompt` only; a spec carries its own references). Render two
  candidates at 2K and hand over both; adopting a single self-chosen candidate is the same error as
  scoring them. A user who says "candidate 1 for all" has judged in seconds — two per character is
  enough, and re-rolling is cheaper than arguing. Record the chosen render's prompt and inputs in the
  character folder so the sheet is reproducible.

## Testing a reference strategy

"One sheet per character will work better" is a hypothesis, and a good one — but it is settled by
renders the user judges, not by argument.

Call the two sides **variant A** and **variant B** in anything a human reads. "Arm", "n=1" and
"confound" are trial jargon; the first reply will be _what do you mean by arms_, and the vocabulary
then costs more attention than the result. The discipline survives plain words: one variable,
labelled pairs, a sealed key, and an honest note on what the run does not prove. Keep both arms alive while you test: the old crops and the
new sheet. Deleting the plates first makes the test unfalsifiable.

Design the comparison so the only difference is the reference set:

- **Same prompt per pair**, compiled from the same spec fields, so the arm is the only variable.
- **Single-character frames and group shots.** Singles isolate identity; groups expose whether a
  reference that carries several characters' worth of detail actually holds across two or three of
  them. Two or three group compositions are enough to see a trend.
- **Neutral concepts.** Test on plain staging the user does not care about, never on a concept they
  are still developing — a bad render then reads as a verdict on their idea instead of the arm.
- **Blind the pairs.** Give each pair a scene code with the arm shuffled (`P7-A` / `P7-B`), deliver a
  contact sheet, and keep the mapping until the user has judged. Recording the order biases the
  judgement and invites the agent to "confirm" it. Inline the thumbnails as base64 data URIs in the
  page: a `::preview` frame does not resolve relative `src` paths, so `<img src="code.jpg">` renders as
  alt text and reads as "I can't see your images".
- **Make the verdict come back through a channel you can read.** The page is the viewing surface, not
  the ballot box: a form inside a preview frame can submit and arrive with no payload. Ask for the
  picks in chat (`s1 X, s3 Y, s5 no preference`) and keep the sealed mapping in a file, so a lost
  verdict costs one question instead of a re-run. Treat picks numbered `s1…s7` as row order — say
  which scene each number is when you ask.
- **Verify the shuffle is balanced, not merely random.** A per-scene coin flip can land the same arm
  on the left in six of seven rows, which makes position collinear with arm — a left-side preference
  then reads as an arm win. Count the split after shuffling and re-draw (or alternate deterministically)
  until each arm occupies the left about half the time. With an unbalanced draw, report the position
  split alongside the tally, as the check that the verdict is not a side artefact.
- **Match the reference count, or say the confound out loud.** Two crops per character against one
  sheet per character varies _how many_ references as well as _which_, so a win cannot distinguish
  "sheets are better" from "fewer references are better". Either hold the count constant or state the
  confound in the result — do not quietly attribute it to the sheet.
- **Check the model's reference cap before a multi-character scene.** qwen-image-2.1-turbo accepts at
  most four references and returns HTTP 400 at six, so a three-character frame with two crops each
  cannot run. Cap references per character, and note in the result when a scene had to be re-run at a
  lower count — otherwise that arm quietly changed definition mid-test.
- **One render per scene is directional.** Seven scenes judged once each is a signal, not a rate; say
  so. Repeats are the only thing that turns "5 of 6" into something that survives a second look.
- **Say the cost up front.** A render count times per-render price (the response `usage.cost`, ~2¢ for
  a 2K qwen render) — a 14-render pass is ~$0.26, which is cheap enough that the user will say yes.
- **Report coverage, not scores.** What to report is model, size, cost, and the sealed mapping after
  the verdict; never a quality claim about either arm.

## Pitfalls

- **Never judge the images, or pick a winner.** The user decides quality; the agent establishes
  facts (dimensions, hashes, references, sizes). A cleanup request is not an invitation to score art.
- **"There are duplicates" is a hypothesis.** Disprove it with a measurement and say so plainly —
  agreeing with a wrong premise is how canon art gets deleted.
- **One file per slot is a design decision, not bloat.** A face-only crop exists so a reference cannot
  contradict an outfit assigned elsewhere; a combined plate exists because the renderer has one
  reference slot. Flattening that is a pipeline change requiring new art, not a deletion.
- **A character whose only source is a photo or a crop has no turnaround to keep.** Check what exists
  before agreeing to "one sheet each": the ask may imply generating art.
- **When two sheets compete for one role, do not pick one.** Two multi-angle sheets of the same
  character at the same dimensions are different artwork, not duplicates — which one is _the_ sheet is
  a taste call the user owns. Report both with dimensions and what each is derived from, name it as the
  one decision only they can make, and offer to re-roll rather than choosing for them.
- **Do the size win and the canon change separately.** Offer the re-encode (no art lost) as its own
  decision, so the user can take most of the benefit without touching canon.
- **Back up before a bulk move.** A `git bundle` plus an rsync of the working tree costs seconds and
  is the difference between a revert and a rebuild.
- **A user's own cleanup is an event to re-verify, not a finished state.** They delete files directly in
  the library folder; the registry keeps its pointers and the existence test fails on the next run —
  the test is the detector, so run the resolution sweep and the suite immediately after anyone
  hand-edits the folder, and repair the pointers before touching anything else. Reconciling the prose
  is part of the same repair: a table, or an "attach X for photoreal" instruction, that names a file
  which is gone reads as authority and sends the next render into a missing path.
- **Deleting a source silently retires a register.** Removing the only photoreal reference because
  "we are cel only now" is a different decision from removing a duplicate: say which register is left
  with nothing to be checked against, in the plates doc and in the character's own canon.

## Reference

- `templates/turnaround-sheet-prompt.md` — starter prompt, flags and hand-over protocol for
  generating a missing multi-angle sheet from a character's existing canon.
- `references/reference-ab-test.md` — harness mechanics: plan/mapping files, the render loop, the
  blind judging page (inline images, why relative paths fail), and how to report the tally.
