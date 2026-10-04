---
name: redesign-templates
description: Redesign the resume and cover letter templates into your own house style. Changes typography, palette, and layout while holding the ATS constraints fixed, then proves the result still compiles and still extracts. Run any time; not a pipeline stage.
argument-hint: "[a direction: a palette, a font, a reference PDF, or nothing]"
license: MIT
---

# Redesign Templates

Change how the documents look without changing what a machine reads out of them.

`templates/resume.tex` and `templates/cover_letter.tex` ship in one house style. It is a defensible style and it is not the user's. This skill produces a variant they own.

**Every `templates/...` path in this file is relative to the plugin, not to the workspace.** They are read from there and never written back to there; the variant goes in the user's own directory. Resolve them against the directory this skill file was itself loaded from — that works on every harness, where a harness-specific plugin-root variable does not.

**Arguments:**
- `$1` — optional. A direction: a palette, a font family, a reference PDF or image, an adjective. With nothing, interview for it.

**Announce at start:** "Redesigning the resume and letter templates. The ATS rules are fixed; everything visual is open. I'll compile and check the extraction before and after."

## The One Thing That Makes This Skill Dangerous

A redesign is judged by eye and graded by a parser. Those are different judges, and the second one never reports back.

A two-column layout, a sidebar of icons, a header block, a skills table: each of these looks better to a person and reads worse to an ATS, and the failure is silent. Nothing errors. The PDF looks correct. The extracted text has the dates in one column and the employers in another, and the candidate never learns that this is why nobody called.

So this skill holds a fixed set of constraints and changes everything else. The constraints are listed below, and they are not preferences.

## Fixed Constraints

These do not move, whatever the user asks for. If the user asks for one of them anyway, say once what it costs and then do what they decided — it is their application. Record the override in a comment at the top of the file so the next run of this skill does not silently revert it.

1. **Single column for content.** Multi-column layouts get read in the wrong order, and the resulting text interleaves two unrelated streams. This is the single most damaging change available in this skill.
2. **No tables carrying content, no text boxes, no icons carrying meaning.** An icon that replaces the word "Email" removes the word "Email" from the extracted text. A phone glyph is not a phone number.
3. **Contact details in the body, never in `\header` or `\footer`.** Roughly a quarter of ATS drop header and footer content entirely, and the dropped field is the one they would have called.
4. **Standard section headings.** "Work Experience", not "Where I've Been". The parser matches on the string.
5. **Month and year on every role.** A year-only date makes tenure ambiguous, and an ambiguous tenure gets resolved against the candidate.
6. **Selectable text.** No content rendered as an image, no font that fails to embed a usable ToUnicode map. Test this rather than assuming it; see Phase 4.
7. **The two documents stay a matched pair.** Same palette, same fonts, same header treatment. They are the only two things in the application a screener sees side by side.

Everything else is open: typeface, weight, color, rule weight, spacing, margins, section order, the shape of a role entry, whether links are colored, how emphasis works.

## Phase 1: Read What Exists

Read both templates before proposing anything. Read the header comment blocks specifically — they carry the reasoning for choices that look arbitrary from the body, and a redesign that "cleans up" a load-bearing decision is the most likely way this skill does damage.

Check whether the user has already redesigned once: a house-style comment that differs from the shipped one, or a variant in the workspace. Extend that rather than starting over. Two competing house styles in one workspace is worse than either of them.

Then compile both, as they are, and keep the output. That is the before state, and without it there is nothing to compare a regression against.

## Phase 2: Get The Direction

If `$1` gave a direction, work from it. Otherwise ask, in one batch:

1. **A reference.** A document whose look they want, a website, a brand, a PDF. Concrete beats adjectival: "like the Stripe docs" is workable, "modern and clean" is not.
2. **Constraint or freedom.** Is there an employer, industry, or region with an expectation to meet? A conservative field punishes a design that a design field rewards.
3. **Color, or none.** A single accent is the default here and it is the safest interesting choice. Ask whether they will ever print this in black and white, because an accent that carries meaning disappears when they do.
4. **Fonts they can actually install.** A font the user does not have is a hard XeLaTeX error rather than a warning. See Phase 3.

Do not ask more than this. The rest is a decision to make and show, not a question to ask.

## Phase 3: Design

Change the preamble, not the body. The body of both templates is placeholder prose that teaches the structure, and rewriting it turns a redesign into a rewrite the user did not ask for. Where a design change requires a new command, add the command and use it; do not inline the styling at each call site, because the next redesign then has to find every one of them.

### Typography

Pick at most two families: one for text, one for the mono details. A third family reads as indecision at any size.

Body size between 9.5pt and 11pt. Below 9.5pt a reader over forty stops reading and does not tell you that is why. Above 11pt the document runs long for reasons that are not content.

### Fonts must degrade

**Every font the template names gets an `\IfFontExistsTF` fallback to something that ships with a normal system.** This is not defensive politeness. A missing font in XeLaTeX aborts the build, so a template naming a font the user has not installed does not look wrong, it does not exist. The shipped templates fall back to DejaVu; keep that pattern.

The shipped house fonts are vendored in the plugin's `assets/fonts/` and installed by `python3 scripts/install_fonts.py`. A font the user picks in this skill is not, so it has to come from somewhere. Ask where before designing around it: a Google Font they will install, a licensed font already on their machine, or a system font. A typeface nobody can install is a design that renders as DejaVu everywhere except the machine it was drawn on.

Name the real font first, the fallback second:

```latex
\IfFontExistsTF{Your Font}{%
    \setmainfont{Your Font}[UprightFont={* Regular}, BoldFont={* Bold}]
}{%
    \setmainfont{DejaVu Sans}
}
```

Then verify both paths. Phase 4 says how.

### Color

One accent. Two accents means every use of either has to justify which one, and the answer is usually that it was whichever was nearer in the file.

Check the accent against a white background at text size, not at heading size. A copper or a mid-blue that reads well at 21pt can drop below usable contrast at 10pt. Darken the link color relative to the accent if it fails — the shipped templates carry a separate `accentink` for exactly this, and that is the pattern to copy rather than a one-off.

### Density

Density is a real variable and it is the one users most often get wrong in both directions. A dense layout fits more evidence per page and reads as harder work. A loose layout reads as confident and runs longer. Neither is correct in the abstract. Ask what the user is optimizing for, then make the margins, `\linespread`, and list spacing agree with the answer instead of arriving at density by accident.

## Phase 4: Prove It

A redesign is not done when it looks right. Run all four checks and report every one, passing and failing both. A check that only reports failures is indistinguishable from a check that did not run.

**1. It compiles, on both font paths.**

```bash
latexmk -xelatex -interaction=nonstopmode resume.tex && latexmk -c
```

Then compile again with the named fonts unavailable, to exercise the fallback. The fallback branch is the one nobody tests and the one that runs on every machine except the author's. On Linux, a scratch fontconfig pointing at only the fallback family does this without uninstalling anything:

```bash
FONTCONFIG_FILE=/path/to/fallback-only.conf latexmk -xelatex resume.tex
```

If that is not available, at minimum read the fallback branch and confirm every family it names is one that ships with the system.

**2. The extraction is still correct.**

```bash
pdftotext resume.pdf - | less
```

This is the check the whole skill exists for. Read the output, do not glance at it. Specifically:

- Every role's employer, title, location, and dates appear together and in order. Interleaving here is the two-column failure and it is the one to look for first.
- Contact details are present. If the email or phone vanished, they moved into a header.
- Section headings appear as text.
- No content is missing entirely. Anything rendered as an image extracts as nothing at all.

**3. Nothing is an image.** If the extracted text is empty or nearly empty, the document rendered as graphics and every ATS will score it zero. This is rare and it is total.

**4. Page count did not run away.** Report the before and after count for both documents. A redesign that pushed the resume from two pages to three has made a content decision disguised as a style decision, and the user should get to make that one deliberately.

## Phase 5: Hand Off

Write the result to the workspace, not over the plugin's templates. The plugin directory is a checkout that gets replaced on the next update, and an edit there disappears without warning. Put the variant in the user's own workspace and tell them the path.

Record the house style at the top of both files, in the same comment block the shipped templates use: the fonts and where to get them, the palette with hex values, the density decision and what it was for, and any fixed constraint the user chose to override with the reason they gave. That block is what makes the next redesign an edit rather than an archaeology exercise.

Show the user:

- Both PDFs, before and after
- The four check results, each one stated
- Page counts, before and after, per document
- Anything they asked for that hit a fixed constraint, and what was done instead

## Anti-Patterns

- **Do not redesign the body prose.** The placeholder text in both templates teaches the structure and carries the reasoning. Changing the preamble is a redesign; changing the body is a different skill the user did not run.
- **Do not add a second column because the content does not fit.** Content that does not fit is a content problem. A two-column resume that fits is a resume that no longer parses, which is a worse outcome than a three-page one that does.
- **Do not name a font without a fallback.** The template stops building on every machine that lacks it, and the user finds out during an application rather than now.
- **Do not judge the result from the PDF alone.** The PDF is what a human sees, and a human is the second reader. Read the extracted text before calling it done.
- **Do not edit the plugin's `templates/` in place.** It is a checkout. The next plugin update overwrites it and the user's design is gone with no error and no diff.
- **Do not carry a style across from a reference without checking the constraint list.** Most attractive resume templates on the internet violate at least one of the seven fixed constraints, and the ones that look best usually violate the first.
