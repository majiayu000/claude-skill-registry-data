---
name: rseng-legacy-code
description: >-
  Covers working safely with inherited research code: characterization tests
  before any change, incremental modernization of untested scripts, recovering
  intent from code without documentation, and deciding between refactor,
  rewrite and retire. Use PROACTIVELY when asked to change code that has no
  tests, and when the user inherits a codebase from a departed researcher,
  mentions legacy or untested code they are afraid to touch, or wants to
  change code that has no tests. (Migrating off commercial platforms like
  MATLAB, IDL or SAS to open alternatives is rseng-open-source-migration; this
  skill supplies the characterization-test safety net it builds on.)
license: CC-BY-4.0
metadata:
  version: 0.2.0
---

# Working with legacy research code

Research software outlives its authors' contracts. The typical legacy
situation is a working but untested codebase whose author has left,
whose behavior IS the specification, and whose results current papers
still depend on. The prime directive: preserve today's behavior first,
improve structure second, change behavior only deliberately and
visibly. In research code a silent behavior change is worse than a
crash - it can corrupt published results downstream.

## First contact with an inherited codebase

Before changing anything:

1. Get it running. Capture the exact environment that works (versions,
   OS, data paths) in a lockfile or container while it still runs
   anywhere (rseng-reproducible-environments) - the running environment
   is itself endangered knowledge.
2. Snapshot everything: commit the code as-is to version control,
   including generated files and local tweaks, before any cleanup
   (rseng-version-control-review). Tag it as the reference state.
3. Recover intent from what exists: papers that used the code, commit
   messages, variable names, comments in any language, old emails or
   READMEs. Write down what you learn as documentation NOW
   (rseng-documentation) - you are the next person who will forget.
4. Map the danger zones: which outputs feed publications, which parts
   are dead code, which parts everyone fears. Effort goes where
   published results depend on correctness.

## Characterization tests: the safety net

Legacy code has no tests, so the first tests do not check that the
code is RIGHT - they pin down what it currently DOES:

1. Run the code on representative inputs and capture the outputs.
2. Turn each captured run into an automated test asserting today's
   output (golden-master / snapshot testing). For floating-point
   results, assert within tolerances, and record the tolerance
   decision.
3. Only then start changing code, keeping the characterization tests
   green after every step.

When a characterization test later fails on purpose (a bug fix changes
results), update it explicitly and record the scientific justification
in the commit and changelog - that changed number may need to reach
users of previous results (rseng-publishing-releasing). The rseng-testing
skill covers the mechanics; the discipline here is: no refactoring
without a pinned baseline.

## Incremental modernization

Never big-bang rewrite what you cannot yet test. Work in small,
reversible steps, each one commit-sized (rseng-version-control-review):

- Strangler pattern: wrap the legacy core behind a clean interface,
  route new work through the interface, and replace the inside
  piece by piece while the outside stays stable.
- Seams first: to test an untestable function, introduce the smallest
  change that lets you inject inputs or observe outputs (extract a
  function, parameterize a hard-coded path) - then test, then
  refactor.
- One concern per pass: formatting-only commits, then dead-code
  removal, then restructuring. Never mix behavior changes into
  cleanup commits - reviewers must be able to trust that a "cleanup"
  diff changes nothing.
- Add modern hygiene as you touch things, not wholesale: linting and
  CI on the files you changed (rseng-code-quality, rseng-ci-cd) rather
  than a repository-wide reformat that destroys git blame.

## Language and stack migrations

For Fortran-to-Python, MATLAB-to-Python, Python 2-to-3, IDL and
similar migrations:

- Migrate by module with the characterization tests as the contract:
  old and new implementations must agree on the pinned outputs within
  stated tolerances before the old one is deleted.
- Consider wrapping instead of translating: mature Fortran/C numeric
  cores are often best kept and called from a modern interface
  (f2py, ctypes, Rcpp) - translation risk is highest exactly where
  the code is most optimized.
- Expect floating-point differences across languages, compilers and
  BLAS implementations; decide tolerances scientifically, with the
  domain expert, not by loosening until tests pass.
- Record the migration in the project history and cite the original
  authors - the old code is a research contribution
  (rseng-citation-metadata).

## Refactor, rewrite or retire

Make the decision explicit and write it down
(rseng-management-planning):

- Refactor when results still matter and the code mostly works -
  the default choice.
- Rewrite only with characterization tests as the acceptance
  criterion, and keep the legacy version runnable until parity is
  proven.
- Retire when nothing current depends on it - but archive properly
  rather than delete: a tagged release plus a public archive keeps
  the record citable (rseng-publishing-releasing; Software Heritage
  archives source code for exactly this purpose).

## Working with this skill

This skill is source-independent: it encodes established legacy-code
practice (characterization testing, seams, strangler migration)
applied to research software.

Learn more (verified):
  - https://refactoring.com - Fowler's refactoring catalog and book
  - https://archive.softwareheritage.org - universal source code
    archive, for preserving and citing retired research code

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-archiving - retire path ends in archive
- rseng-documentation - recording recovered intent
- rseng-open-source-migration - commercial-platform exits build on this
- rseng-reproducible-environments - capture the working environment first
- rseng-testing - characterization test mechanics
- rseng-version-control-review - small reversible cleanup commits

<!-- related-skills:end -->
