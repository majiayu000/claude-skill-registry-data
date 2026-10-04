---
name: "Red: Doc"
description: "Adversarial review of a document written as the colleague trying to kill it, aimed at one or two named readers"
when_to_use: "Before a document goes in front of people: find what gets it rejected, on the terms of the specific readers who will reject it. Also for a hostile pass over your own draft."
model: opus
effort: high
metadata:
  glyph: ᛟ
  family: red
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write", "Bash(python3:*)", "Bash(git:*)", "Bash(mkdir:*)", "Bash(ls:*)", "Bash(rg:*)", "Bash(grep:*)", "Bash(wc:*)", "Bash(python3 \"$HOME\"/.claude/library/scripts/red-personas.py:*)"]
argument-hint: "<target> [persona] [persona] [-- what else would kill it]"
---

# Sabotage a document

The methodology itself (persona resolution, the nine-field schema, field
ordering, the report skeleton, discipline rules, refine-then-save) lives in
`~/.claude/library/references/red/methodology.md`. Read it now and execute it;
this file adds only what is unique to the document path.

## Step 1: Parse `$ARGUMENTS`

**Target is required; persona is not.** A target with no target is nothing to
run at all. Exception: the single literal invocation `/red-doc personas` (no
other arguments) prints the roster and stops: that is a deliberate roster
lookup, not an incomplete review request.

If the target is missing, do not guess and do not fall back to the document
most recently discussed. Print tersely and stop:

```
Usage: /red-doc <target> [persona] [persona] [-- failure conditions]
Missing: target
```

Once a target is present: positional, in this order.

```xml
<arguments>
    <positional n="1" name="target" required="true">
        Path to the document under review (.html, .md, .txt, anything readable).
        An @-mention resolves to its path.
    </positional>
    <positional n="2,3" name="personas" required="false">
        Resolved per the methodology's Step 1/1a/1b/1c, via
        `python3 "$HOME"/.claude/library/scripts/red-personas.py` called with
        `--scope doc`. **Default: `goblin`** when none is named — Jason's own
        review stance, scoped to both doc and branch.
    </positional>
    <positional n="4+" name="failure-conditions" required="false">
        Free text: extra information about what would make this specific
        document fail. Anything after a bare `--`, or any remaining argument
        that is not persona-shaped (a short capitalised name then a colon).
        Fold it into every pass, and give it its own section when it introduces
        criteria the standing sections do not already cover.
    </positional>
</arguments>
```

`/red-doc personas` prints the roster from the personas file and stops.

## Step 2: Read the target and its sources

Read the target in full. Then find what it rests on and read that too: the
spike doc, ADR, migration, schema or roadmap it cites, plus anything in the
repo that would confirm or refute a load-bearing claim. Every number the
document leans on is a claim to check.

Two things come out of this pass:

- **Verified findings**, marked ✅ in the report. Only ever applied where you
  read the source and the mismatch is real.
- **Source-only information**, which is how you catch what the document
  withholds. The strongest findings in this format are usually a figure the
  document quotes without the identifier that makes it damning.

## Step 3: Mechanical pass

```bash
python3 ~/.claude/library/scripts/slop-scan.py <target> --top 6
```

Counts house-rule breaches, contrastive couplets, first-person density, hedge
boilerplate, intensifiers, LLM lexicon, borrowed weight, triads, numeral-style
clashes and verbatim repetition, with line numbers. (`--strict` is the gate
mode the commit-msg hook and the prose skills use: house rules only, exit 1 on
a hit. This pass wants the full report, not the gate.)

The scan produces candidates, never findings. Read each hit in context before
it enters the report, and drop the ones where the construction is doing real
work. A count is only evidence when the repetition is the point: "the same
rhetorical move 23 times" is a finding, "uses the word actually" is not.

## Step 4: The passes

Run each of these over the whole document, plus the persona-pass from the
methodology. Keep going until a full pass turns up nothing new. Never pad: an
item you cannot quote does not exist.

### AI slop

Each entry needs **evidence** (verbatim), **where** (section), and **why it is
slop**. The why is the part that convinces; it names the tell, meaning what the
passage reveals about how the text was produced. Categories that carry weight:

- **Layer gaps.** The difference between edited and unedited parts of the
  document. Zero em dashes in the prose and nine in the headers proves the
  style pass touched paragraphs only. Comma soup where dashes were stripped
  without the restructuring the rule demands. A lone Americanism that no
  spellchecker flags.
- **Rhetorical defaults.** The contrastive couplet manufactures insight by
  rejecting a claim nobody made. Twenty-three instances of one construction
  across 3,000 words is local optimisation with no memory of the previous
  paragraph's cadence. Five triads shows a container shape being filled,
  whatever the real count was.
- **Epistemic theatre.** Hedges landing on the safe claims whilst the
  load-bearing numbers go bare. Six-significant-figure counts implying a
  measurement programme the document admits it never ran.
- **Generation artefacts.** A metaphor reused as though it were established.
  Register alternating block by block. Stock aphorisms doing the work of an
  argument.
- **Slop that is also wrong.** The strongest items in this section are the ones
  where the tell is simultaneously a factual error; say so, and cite both.

### Self-indulgence

Passages doing something for the author rather than the reader. Vanity
statistics no claim rests on. Sections about work that is not happening.
Announcements of the document's own importance. The same sigh twice, sections
apart. Integrity narration, where a method note is written as a character
reference. Pre-emptive self-defence against criticism nobody made. Restraint
boasts. Anecdotes told three times in one section.

### Named failure conditions

Only when positional 4 supplied criteria the sections above do not already
cover. Same evidence discipline.

## Step 5: The report

Follow the methodology's report skeleton. Title is `Sabotage dossier:
{filename}`. Evidence sections are, in order: Section 1 AI slop evidence
(`A1`, `A2` …), Section 2 self-indulgent bits (numbered), then the per-persona
sections and named failure conditions per the shared skeleton.

## Step 6: Refine, then save

Follow the methodology's refine-then-save protocol.
