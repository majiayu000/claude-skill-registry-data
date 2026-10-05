---
name: split-docs
description: "Split one oversized Markdown reference document into a progressive-disclosure tree - a curated index page plus one file per section - without altering a byte of prose. Use when a single doc has grown too large to read whole (a multi-hundred-line architecture spec, PRD, catalogue, or reference), when asked to split, shard, or break up a doc into sections, when each row of a table or list should become its own file, when converting a monolith-plus-stale-digest pair into an index-plus-sections layout, or when a digest has drifted from the doc it summarizes. Verifies byte-faithfulness by concatenation and repairs inbound and outbound links repo-wide. Do NOT use for authoring new documentation content (that is make-docs), for choosing a Diataxis type, for splitting source code, or for editing prose during the move."
metadata:
  author: Serghei Iakovlev
  version: "1.2"
  category: documentation
---

# Splitting a Large Doc into a Progressive-Disclosure Tree

A reference doc that has grown past a few hundred lines is read whole every time any part of it is relevant, which wastes context and buries the section that matters. The fix is to split it into one file per top-level section under a sibling directory, and replace the original with a curated index that routes a reader to the one section their task touches.

The hard constraint is that this is a *move*, not a *rewrite*. Section prose must survive byte-for-byte; only the index is new writing. Three failure modes recur and all are silent:

1. Dropped or reordered bytes during extraction.
2. Outbound links inside the moved sections that break because the section files now sit one directory deeper than the original.
3. Inbound links from elsewhere in the repo that pointed *into* the doc by section anchor (`thedoc.md#some-heading`), left dangling because that anchor no longer exists in the doc - it moved to a section file.

This skill makes all three verifiable instead of hoped-for. The third is the easiest to miss and the most damaging, because the dangling links sit in *other* files, often ones an agent never reopens during the split.

A frequent variant: the doc travels with a hand-written digest (`*-digest.md`, `*-summary.md`) that has drifted out of date. The digest's job - route a reader to the right part - is exactly what the new index does, so the digest is deleted after the split, not carried forward.

This document uses one example doc to keep the commands concrete, but nothing here is specific to it: it applies equally to an architecture spec, a PRD, or any long reference. Set the two variables below once and the rest is doc-agnostic.

## When this applies

Run it when a single Markdown reference doc is too large to read whole and the request is to break it up. It generalizes across doc types. If the repo holds several monolith-plus-digest pairs (for example an architecture spec and a PRD, each with its own digest), each is a separate application of this same procedure.

It does not apply to authoring new prose (`make-docs`), to picking a Diataxis quadrant, or to splitting code. If the task involves rewriting or improving the prose while moving it, stop - that breaks the byte-faithful contract and needs a different approach the user should approve first.

## Choose the cut level before tiling

The split level is not always `##`. Cut at the level where each output file is one coherent subject.

When top-level headers are *containers* rather than subjects - a `## Direct competitors` holding five `### Vendor` entries, a `## Endpoints` holding twelve `### GET /path` entries - cutting at `##` collapses every subject into one file and defeats the split. Map both levels before deciding:

```bash
grep -nE '^## '  "$SRC"
grep -nE '^### ' "$SRC"
```

If a `##` section holds several `###` subjects, cut at `###` and let the container header become a directory. The container's own lines - its header and the blank after it - are lifted into structure exactly as the preamble is lifted into the index, so step 4 must account for them or the concat diff will not close.

## Two modes: move and transform

Most of a split is a **move**: prose travels byte-for-byte and the concat diff proves it.

Some of it is a **transform**: a section is a table or list whose *rows* are the subjects, and each row becomes a file. Transform output is new bytes in a new arrangement, so the concat diff structurally cannot cover it.

Declare the mode of every section before extracting. Transformed sections are excluded from the concat gate and get the replacement gates below instead. A transform that was not declared is a transform that was not verified.

### Replacement gates for transformed sections

The byte gate proves nothing was lost. In transform mode you prove the same thing three narrower ways, all in code, none by eye:

1. **Field containment.** Every field of every source row appears verbatim in the file it became. Assert it and fail loudly.
2. **Uniqueness.** No subject owns two output files. The same slug appearing in two directories means the transform manufactured a duplicate.
3. **Count.** Output files equal source rows minus declared exclusions, and every exclusion is logged by name.

Gate 2 earns its place on its own. It is the only one that catches a subject that exists both as a transformed row *and* as a full section elsewhere in the same document - and field containment will happily pass while that happens, because the text was copied faithfully into a file that should not exist.

### Tombstone rows are pointers, not subjects

A row struck through (`~~Name~~`), or whose cells read *moved*, *promoted*, *superseded*, *see above*, or set the reference field to `N/A`, is a redirect the author left for readers following an old citation. It is not a subject.

Turning one into a file resurrects something deliberately retired. Skip these rows explicitly, and print each skip so the count in gate 3 reconciles.

## Adding metadata during the move

Prepending YAML frontmatter to each output file is additive, so it does not break the byte-faithful contract - but it does break the *gate*, because the concatenation no longer matches the snapshot. Re-run the gate with frontmatter stripped:

```bash
strip() { awk 'BEGIN{n=0} /^---$/{n++; if(n<=2) next} n>=2{print}' "$1"; }
diff <(sed -n '<first-section-line>,$p' /tmp/_split_original.md) \
     <(for f in <output files in document order>; do strip "$f"; done)
```

**Every derived metadata value must appear verbatim in the source it describes.** Extract each value from the prose, then assert the extracted string is present before writing it, and abort the build if it is not.

Dates are where this bites. A timestamp the source never states is invented metadata, and one commit later invented metadata is indistinguishable from recorded metadata - it will be trusted, reported, and acted on. Where the source says nothing, write the null the schema defines. Never a plausible guess, never the file's mtime, never today's date.

## When the target is another repository

The procedure is unchanged; two steps widen.

**Step 5 loses its relative anchor.** Links that resolved inside the old repository do not resolve from the new one. Rewrite them as absolute URLs, or as whatever runtime-resolved path variable the consuming host provides. Check the destination's existing convention first and match it - a tree carrying two link forms is worse than either one.

**Step 8 runs in both repositories.** The source repo still holds references to content that is no longer there, and those are now cross-repo references rather than broken relative paths. Sweep both trees.

## Procedure

### 1. Snapshot the original before touching anything

Set the source and target as variables so every later command is doc-agnostic, then copy the source to a scratch path. Every later check diffs against this snapshot, so it must be taken before the first edit.

```bash
SRC=docs/the-doc.md     # the oversized doc to split (e.g. docs/architecture.md, docs/PRD.md)
DIR=docs/the-doc        # sibling directory that will hold one file per section
cp "$SRC" /tmp/_split_original.md
wc -l "$SRC"            # record the line count
```

### 2. Map the top-level section boundaries

List the headers at the split level (usually `##`) with their line numbers. These are the cut points; the count is how many section files you will produce.

```bash
grep -nE '^## ' "$SRC"
```

Decide the per-file naming up front: zero-padded ordinal plus a slug from the heading (`01-<slug>.md`, `02-<slug>.md`) keeps the directory sorted in document order. Create the target directory (`mkdir -p "$DIR"`).

### 3. Tile the file by header into section files

Extract each section as the byte range from its header line up to (but not including) the next header line. Drive it from the boundary line numbers in step 2 - do not hand-retype prose. Run `sed -n 'START,ENDp' "$SRC"` for each range, writing to the matching section file. The first section starts at the doc's first `##`; anything above it (title, preamble) belongs in the index, not a section file. For the last section, end at `$` so a missing trailing newline does not truncate it.

Extract every section before editing either the snapshot or the live file, so the line numbers stay valid.

### 4. Verify byte-faithfulness by concatenation

This is the gate that makes the split trustworthy. Concatenate the section files in order and diff against the snapshot. The only legitimate difference is the title and preamble lifted into the index (the lines above the first `##`).

```bash
diff <(sed -n '<first-##-line>,$p' /tmp/_split_original.md) <(cat $(ls "$DIR"/*.md | sort))
```

Investigate every diff line. A diff hunk in the *middle* of a section means dropped or duplicated content - fix the tiling and re-run. Do not proceed until the only diff is the lifted preamble (or run the diff against the original from the first section line, as above, for a clean empty result).

Three things change what "in order" and "the only difference" mean, and each is covered above:

- **Container headers**, when cutting below `##`. Include them in the concatenation from wherever you parked them, or the diff will not close.
- **Transformed sections.** Exclude them from this gate and run their replacement gates instead - the concat diff cannot judge rearranged bytes.
- **Added frontmatter.** Re-run the diff with it stripped.

### 5. Repair outbound relative-link depth, then sweep every link

Section files now live one directory deeper than the original, so every relative link that pointed *outside* the doc's own directory needs one extra `../`. A link to `decisions/0008.md` from the old `$SRC` becomes `../decisions/0008.md` from `$DIR/05-*.md`. Links *within* the new tree (section to section, including same-file `#anchor` links) do not change.

Do not trust a hand-built list of links to fix - that is exactly where one gets missed (a single doc can hold more escaping links than you expect). After repairing, sweep *all* relative links across the new files and confirm each resolves:

```bash
grep -rnoE '\]\(([^)]+)\)' "$DIR" | grep -v '://'   # every non-http link
```

For each hit, check the target exists from the section file's location (`test -e` against the resolved path, or open it). A link that does not resolve is either an unrepaired depth (`../` missing) or over-repaired (one `../` too many). The grep sweep, not the edit plan, is the source of truth for which links exist.

### 6. Author the index fresh from each section's current content

Replace the original file with an index page. Derive each section's summary by reading that section file *as it now stands* - do not port descriptions from the old digest or an outdated table of contents, which may describe content that has since moved or changed. Open each section, write its row from what is actually there.

Match the repo's existing index house-style: study a sibling index (for example `docs/README.md` or a `decisions/README.md`) and reuse its table shape and column semantics. A routing index typically carries a short preamble, an optional orientation paragraph, and a table whose columns name each section, what it covers, and when a reader should open it. State, near the top, that the section file wins when the index summary and the section disagree - the index is a map, not a second source of truth. Follow the project's writing rules (sentence-case headings, punctuation conventions, banned words, em-dash bans) the same as any other doc edit.

### 7. Delete a now-redundant digest, after confirming it holds nothing unique

If a `*-digest.md` / `*-summary.md` accompanied the original, the new index supersedes it. Before deleting, diff its content against the section files and the new index to confirm it carries no information that exists nowhere else. If it holds a unique line, fold that into the right section or the index first; then delete. Removing it stops a second stale artifact from accumulating drift.

### 8. Find and repair every inbound reference, repo-wide

This is the step that is most often under-done. Other files point *at* the doc you just split: agent context files, other docs, ADRs, reference pages, even source comments. Search the whole repo, not just `*.md`, and not just the doc's own directory.

```bash
DOCNAME=$(basename "$SRC")          # e.g. architecture.md
SECTIONS=$(basename "$DIR")         # e.g. architecture
EXC="--exclude-dir=node_modules --exclude-dir=.next --exclude-dir=$SECTIONS"
grep -rn "$DOCNAME" . $EXC                                  # by file name
grep -rnE "${SECTIONS}[[:space:]]+(section[[:space:]]+)?§?[0-9]" . $EXC  # by short name + section
```

The second grep matters because a reference like `architecture §11C.1` or `architecture section 20` names the doc by its short name with no `.md`, so the first grep never sees it. Adjust `${SECTIONS}` to whatever short name prose actually uses for this doc.

Each hit takes a different repair, and two traps make a clean-looking sweep wrong. Classify every hit, repair it, and verify it resolves, following [references/inbound-references.md](references/inbound-references.md); open that file before touching the first hit.

## Validation

The split is correct when all of these hold:

- The order-preserving `cat` of section files diffs clean against the pre-split snapshot, save for the preamble lines lifted into the index and any container headers lifted into directory structure. Where frontmatter was added, the diff was re-run with it stripped.
- Every section is declared either move or transform, and no transformed section was fed to the concat gate.
- Every transformed section passed field containment, uniqueness, and count, with each excluded row logged by name.
- No subject owns more than one output file anywhere in the tree.
- Every value written into frontmatter appears verbatim in the source it describes; fields the source does not state are null, not guessed.
- The all-links grep sweep over the new tree resolves every relative link from its file's location - none missing a `../`, none with one too many.
- Every inbound reference repo-wide that resolves through a section - anchor link or section reference naming the split doc - has been repointed to the owning section file and resolves, or is a deliberately-left historical artifact you have named.
- Every bare `§N` reference of ambiguous source has been judged a same-doc self-reference (left) or a reference into the split doc (repointed) on evidence, not rewritten blind.
- Any broken inbound references inside edit-protected files have been surfaced to the user with the file list and an explanation, not silently skipped.
- The index is built from the current section content, follows the repo's index house-style, and names the section files as authoritative on conflict.
- No `*-digest.md` survives carrying information absent from the sections or index.

## Anti-patterns

The failure modes this procedure exists to prevent are listed in [references/anti-patterns.md](references/anti-patterns.md). Read it before the first extraction, and again before declaring the split done.
