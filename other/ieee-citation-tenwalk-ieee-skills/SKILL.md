---
name: ieee-citation
description: >-
  Format references and in-text citations to IEEE style, and prepare Index Terms and IEEEtran
  bibliography setup. Use this whenever the user needs to "format references in IEEE", "fix my
  bibliography", "convert these citations to IEEE", "make a .bib for IEEEtran", "number my
  citations", "参考文献改成 IEEE 格式", "整理引用", or asks how in-text numbered citations and the reference
  list should look for an IEEE journal. Also covers Index Terms and EDICS selection ("选 EDICS",
  "Index Terms 怎么写"). Never fabricate DOIs, page numbers, volumes, EDICS codes, or any
  bibliographic field — flag missing metadata instead.
---

# IEEE Citation and Reference Formatting

Use this skill to turn raw references, a `.bib` file, DOIs, or a messy bibliography into correct
IEEE-style entries and in-text citations, and to set up Index Terms and the IEEEtran bibliography.

## Core stance

- **Never fabricate metadata.** Do not invent a DOI, volume, issue, page range, year, or venue.
  If a field is missing, output `[MISSING: volume]` (or similar) and ask the user, or leave the
  BibTeX field empty rather than guessing.
- **Order by first appearance**, not alphabetically. IEEE numbers references `[1], [2], ...` in
  the order they are first cited in the text; the reference list follows that same order.
- **Abbreviate journal and conference names** per IEEE (e.g., *IEEE Transactions on Pattern
  Analysis and Machine Intelligence* → *IEEE Trans. Pattern Anal. Mach. Intell.*). If unsure of
  an abbreviation, flag it rather than inventing one.
- **Defer to the target journal's Author Kit** where it differs (some allow DOIs, some omit them;
  some want month, some do not).

## When to open extra files

| File | Open when |
|---|---|
| [references/ieee-reference-format.md](references/ieee-reference-format.md) | Formatting any reference entry (journal, conference, book, chapter, thesis, online, standard, patent, preprint) or in-text citations |
| [references/ieeetran-latex.md](references/ieeetran-latex.md) | Setting up IEEEtran: `\bibliographystyle{IEEEtran}`, `.bib` entry types/fields, `\cite` usage, Index Terms, EDICS, common BibTeX pitfalls |

## Quick rules (most common needs)

- **In-text:** square brackets, on the line (not superscript): "as shown in [3]". Group as
  "[1], [2]" or a range "[4]–[7]". Cite in numerical order at each point.
- **Do not use the number as a noun:** prefer "the method of [12]" / "Smith *et al.* [12]" over
  "in [12], they...".
- **Author names:** initials then surname — "J. K. Author". Up to six names; for more, list the
  first followed by "*et al.*".
- **One reference = one list entry**, numbered in brackets, hanging indent in IEEEtran (automatic).

## Workflow

1. **Collect** the references (text, `.bib`, DOIs). Identify the type of each (journal,
   conference, book, ...).
2. **Map citation order:** scan the manuscript for first-appearance order; renumber accordingly.
3. **Format each entry** using `references/ieee-reference-format.md`; abbreviate venue names.
4. **Flag gaps:** mark any missing/uncertain field; never fill by guess.
5. **In-text pass:** ensure every `[n]` resolves, ordering is by appearance, and there are no
   orphan or unused entries.
6. **Output** the formatted list (and a `.bib` if the user uses LaTeX), plus a list of flags.

## Output format

1. `References:` the numbered IEEE-formatted list (plain text), or a `.bib` block for IEEEtran.
2. `In-text notes:` any citation-order or phrasing fixes needed in the body.
3. `Flags:` every missing or uncertain field the author must verify.
4. (If requested) `Index Terms:` 5–8 alphabetical terms.
5. (If submitting to CL or another EDICS journal) `EDICS:` the best-fitting category code(s) from
   the journal's current list — never invent a code; tell the user to confirm against the live list.
