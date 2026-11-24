---
name: sciwrite-manuscript
description: >
  Structure a scientific paper section by section — tables and figures, Results,
  Methods, Introduction, Discussion, Abstract — following Stanford's Writing in
  the Sciences. Use this skill whenever someone is writing, drafting, planning,
  restructuring or reviewing any part of a research paper, journal article,
  conference paper or thesis chapter: "help me with the introduction", "how do I
  structure the discussion", "is my abstract missing anything", "my results
  section is too long", "what order should I write the sections in", "does this table
  look right", "where should the limitations go". Also use it when someone asks
  what belongs in a given section, or which verb tense a section takes. Use it
  together with sciwrite-prose, which handles sentence-level editing once the
  structure is settled. Do NOT use it for grant proposals or review articles
  (sciwrite-proposals) or for lay summaries and press material
  (sciwrite-outreach).
---

# Structuring a scientific manuscript

A paper is not written in the order it is read. This skill covers what belongs in
each section, in what order to build them, and how to tell whether a draft
section is doing its job.

Answer in whatever language the user writes to you in; course examples stay in
their original English.

---

## The writing order

Build the manuscript in this sequence. It is not arbitrary — each step makes the
next one easy, and skipping ahead is why people find writing painful.

1. **Tables and figures.** Not shells or rough drafts: a finished, polished set.
   They contain the story of the paper, and until you know what that story is you
   cannot frame anything else.
2. **Results.** Falls straight out of the tables and figures.
3. **Methods.** Could be written at any time — it is a play-by-play of what you
   did — but it sits naturally here.
4. **Introduction.** Written after the story is nailed down, because only then do
   you know how to frame the question.
5. **Discussion.** The hardest and most open-ended; easier once everything else
   exists.
6. **Abstract.** Always last. *Abstract* means *to pull out*, and you are pulling
   from sections that now exist.

When someone asks "where do I start", the answer is almost always the tables and
figures, even if they came expecting to talk about the introduction.

---

## What each section owes the reader

Keep this table in mind; go to `references/sections.md` for the full treatment of
whichever section is actually on the table.

| Section | Its one job | Shape | Voice |
|---|---|---|---|
| Tables & figures | carry the story; stand alone | one clear point each, progressing | — |
| Results | summarise the tables at a *higher level* | trends and relationships, table cited in parentheses | active |
| Methods | be the recipe | subsections; diagrams where possible | passive fine, jargon fine |
| Introduction | set up one question | cone: known → unknown → aim → approach | active |
| Discussion | answer that question, then broaden | inverted cone: answer → context → limitations → so what | active |
| Abstract | stand alone | background → aim → methods → key results → conclusion → implication | active |

**Verb tense, one rule for all of them.** Past tense for completed actions — the
experiments, the analyses, what you and others found. Present tense for what is
still true as the reader reads: *Figure 1 shows*, *the data suggest*, *the
findings confirm*. Both appear in the same paragraph routinely.

---

## Reviewing a draft section

Read the section against the checks below before doing any sentence-level work —
a beautifully edited Results section that recites the table is still wrong.

**Results.** Is it reading the table aloud, number by number? That is the
signature failure. Does it waste a sentence saying *Table 1 shows the
characteristics of the groups* instead of launching into the finding? Does it
justify statistical choices that belong in Methods, or interpret findings that
belong in Discussion? Is the treatment-versus-control comparison foregrounded?
Are negative results reported?

**Methods.** Could someone replicate this? Is it broken into subsections a skimmer
can navigate? Is there a protocol or flow that would be clearer as a diagram or
table? Is the ethics statement present, if needed?

**Introduction.** Count the paragraphs — more than five means it has drifted into
a literature review. Is there an explicit statement of aim or hypothesis, in
findable words? Does it review the *specific link* being studied, or the two
topics separately? Does it summarise prior work at a high level, or walk through
studies one by one? Does it leak results or implications?

**Discussion.** Does the first sentence answer the question the introduction
asked? Does it start with limitations (it should not)? Does it discuss things
that were never measured? Are the limitations specific to *this* study, or
boilerplate that would fit any paper? Does the last paragraph restate the finding
and leave a take-home message? Does anyone outside the immediate field learn why
this matters?

**Abstract.** Does it stand alone? Does it carry the implication sentence — the
*why should I care* — or stop at the conclusion? Does it use the same explicit
aim phrasing as the introduction? Do its numbers match the body?

**Tables and figures.** Three horizontal rules and no vertical ones? Units on
every variable? Significant figures the measurement actually supports? Acronyms
defined inside the table or legend? Does each one make a single clear point? Are
significance markers unambiguous about which comparison they refer to? Is the
same data presented twice, once as a table and once as a figure?

---

## Tools

```bash
# The scripts ship in sciwrite-prose/scripts/. Find that skill wherever it was
# installed: plugin, `npx skills add` (project or global), or a manual copy.
SCIWRITE=$(for d in "${CLAUDE_PLUGIN_ROOT:-.}/skills" .claude/skills .agents/skills \
                    ~/.claude/skills ~/.agents/skills; do
  [ -f "$d/sciwrite-prose/scripts/prose_audit.py" ] && { (cd "$d/sciwrite-prose/scripts" && pwd); break; }
done)

python "$SCIWRITE/extract_text.py" paper.tex
python "$SCIWRITE/extract_text.py" paper.tex --section introduction
python "$SCIWRITE/numeric_consistency.py" paper.tex
python "$SCIWRITE/keyword_consistency.py" paper.tex
```

If `$SCIWRITE` comes back empty, the sciwrite-prose skill is not installed: do
these checks by reading, and tell the user that
`npx skills add dvdsosa/scientific-writing-skills` adds the scripts.

`extract_text.py` maps the sections of a `.tex`, `.docx` or `.md` file, so you
can pull the Discussion without anyone pasting it. Run the consistency checks
whenever a whole manuscript is in play: numbers that disagree between abstract
and body, or a group renamed between Methods and Results, are what a reviewer
notices first and what an author never sees.

---

## Helping someone write a section from scratch

Ask for the material before offering structure. For an introduction you need to
know what is established, what the gap is, and what they asked — and it is common
that the gap has not been articulated yet, in which case that is the real work
and the writing is easy afterwards.

For a Results section, ask for the tables and figures. If they do not exist yet,
say so plainly: writing Results before the figures are settled means writing it
twice.

Draft in their voice, not a generic one, and follow the prose rules from
`sciwrite-prose` as you write — active voice, no throat-clearing, keywords
repeated exactly.

---

## Output

For a section review:

```
## <Section> review

<Two or three sentences: does this section do its job, and what is the single
biggest structural problem?>

### Structure
<Against the checks above. What is missing, what is in the wrong section,
what order the paragraphs should be in.>

### Specific fixes
<Original → revision, for the passages that carry the structural problem.>

### Consistency
<Numbers, terminology, acronyms — only if there is something to report.>
```

When the section is sound, say so and move to prose-level work rather than
inventing structural objections.

---

## Reference files

| File | Read it when |
|---|---|
| `references/sections.md` | working on any specific section — the full rules, with worked examples per section |
| `references/tables-figures.md` | building or reviewing tables and figures; deciding table vs figure |
| `references/worked-examples.md` | you want a model of a good section, or of the same section done badly |
| `references/oceanography-sections.md` | the paper reports ocean transports, hydrographic sections or cruise data |

For sentence-level editing once the structure holds, use **sciwrite-prose**. For
deciding how to spend the writing time in the first place, use
**sciwrite-process**.
