---
name: seam-model
kind: skill
status: ready
provenance:
  principles:
  - P082
  - P030
  - P107
  - P027
  - P138
  - P025
  - P131
  claims:
  - C00067
  - C00072
  - C00073
  - C00068
  - C00069
  - C00080
  - C00081
  - C00086
  - C00082
  - C00083
  source_anchors:
  - 1d83dc6f489c-c0003
  - 1d83dc6f489c-c0004
  authored_from_digest: 5509e88d558c59abd744256f036ad993fecba2d919c69a56567a530fa7eb1d64
---

# Seam model

## Purpose

Find and exploit **seams** — places where you can alter the behaviour of a program without
editing in that place — so a hard-to-test dependency can be replaced under test while the
source code stays identical in production and test (P082). Every seam has an **enabling
point**: a separate place where you decide which behaviour the seam uses. Seeing code in
terms of seams reveals existing testing opportunities and shows how to structure new code
for testability (P030).

## When to use

- You need to replace a hard-to-test dependency to get code under test.

Do **not** apply when no behaviour substitution is needed to test the code.

## Procedure

1. **Locate the place whose behaviour must change under test** (the call to the blocking
   collaborator).
2. **Identify the seam type available**, each mapping to a build step that turns text into
   running code:
   - **Preprocessing seam** — behaviour altered before compilation (macro/preprocessor).
     Available only in languages with a preprocessing build step (C/C++).
   - **Link seam** — behaviour altered at link/reference resolution, whose enabling point
     lives outside the source in the build/link configuration (P027).
   - **Object seam** — behaviour altered by which object is used: pass the collaborator in as
     a parameter (enabling point is the argument list) or override a method in a testing
     subclass (P107).
3. **Locate the enabling point** for the chosen seam — the separate place where you decide
   which behaviour is used. The enabling point must be outside the seam itself so production
   and test source stay identical (P082).
4. **Prefer object seams in object-oriented code (P138).** Reserve the less-explicit link and
   preprocessing seams for when the language leaves no object seam; value object seams over
   link and preprocessing seams, which do little to improve design (P025).
5. **Substitute** the test behaviour (typically a fake) through the enabling point and
   confirm production code is unchanged. In particularly nasty legacy code, modify as little
   as possible, using the seams the language offers to work around fragile areas (P131).

## Inputs

- The blocking call site and the language/build toolchain (determines available seam types).

## Output

A named seam type at the blocking dependency, its enabling point, and the substitution to
make there — with object seams preferred unless the language forces otherwise.

## References

- `sensing-and-separation` — why you are inserting the seam (sensing vs separation).
- `dependency-breaking-techniques` — concrete techniques (Extract Interface, etc.) that open
  object seams.

## Provenance

Derived from principles P082 (seam + enabling point), P030 (see code in seams), P107 (object
seam via parameter/override), P027 (link seam), P138 (choose seam type), P025 (value object
seams), and P131 (minimal edits in nasty code). Source is distillation-only; paraphrased, not
quoted.
