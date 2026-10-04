---
name: rseng-open-source-migration
description: >-
  Covers migrating research code from commercial, license-bound platforms to
  open source alternatives: MATLAB to Octave or Python/NumPy, IDL to Python,
  SAS/SPSS/Stata to R or pandas, Mathematica to SymPy/Julia, and the
  platform-specific pitfalls (indexing, copy semantics, toolbox equivalents,
  numerical parity). Use when the user wants to leave MATLAB, IDL, SAS, SPSS,
  Stata, Mathematica, LabVIEW or another proprietary platform, asks for an
  open or free alternative to commercial scientific software, can no longer
  afford or access a license, or needs collaborators without licenses to run
  the code. (The characterization-test safety net and general inherited-code
  discipline are rseng-legacy-code.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Migrating from commercial platforms to open source

Research code locked to a commercial platform has a structural
problem: every user, collaborator, student, reviewer and CI runner
needs a license, and reproducibility acquires an expiry date tied to
a vendor. Migration to open alternatives removes the toll booth and
makes the work FAIR in practice (rseng-fair-software) - but a naive
"translate the syntax" migration produces subtly wrong science. The
discipline: pin behavior first, choose the target honestly, migrate
incrementally with numerical parity as the acceptance test. The
general safety net (characterization tests, strangler migration)
lives in rseng-legacy-code; this skill adds the platform-specific
knowledge.

## Before migrating: pin the baseline

While the commercial license still works, capture everything the
migration must reproduce (this window may not stay open):

- Run the original on representative inputs and save inputs and
  outputs as the golden baseline (rseng-legacy-code's
  characterization tests).
- Record the platform version, toolbox versions and settings that
  produced the baseline.
- Export data OUT of proprietary formats now: .mat to HDF5-based or
  open formats, SAS/SPSS/Stata files to open tabular formats
  (rseng-scientific-file-formats) - data freedom precedes code
  freedom, and readers for proprietary formats are better used
  while a licensed installation can verify the export.

## Choosing the target

- MATLAB, two honest paths: GNU Octave runs most plain MATLAB with
  minimal changes - the low-cost exit when the goal is simply
  license freedom; Python/NumPy/SciPy is the larger move that buys
  ecosystem, packaging (rseng-project-scaffolding) and hiring, at the
  cost of a real port. Choose Octave for frozen-but-must-run code,
  Python for code with a future. (Simulink has no clean open
  equivalent - flag it as the hard part early.)
- IDL: Python is the community-standard destination (astronomy's
  stack - astropy and friends - exists precisely from this
  migration).
- SAS/SPSS/Stata: R (statistical depth, native model objects) or
  pandas/statsmodels; verify statistical defaults match - the same
  named procedure can use different degrees-of-freedom or contrast
  conventions, which is a science difference, not a bug.
- Mathematica: SymPy for symbolic work, Julia for symbolic-numeric
  blends.
- LabVIEW and instrument control: Python instrument stacks are the
  destination, but hardware interfaces make this a re-engineering
  project, not a translation.
- Whatever the target, check whether the field already has an open
  reimplementation of the domain workflow before porting line by
  line (rseng-software-reuse) - many "migrations" should be
  adoptions.

## Translation pitfalls (where silent wrongness lives)

The famous ones an agent must actively check, not discover:

- Indexing: MATLAB/Octave/R/Julia are 1-based, column-major;
  NumPy is 0-based, row-major. Every hand-translated index and
  every reshape/flatten is a suspect until tested.
- Copy semantics: MATLAB copies on assignment; NumPy slices are
  VIEWS - in-place modification after translation corrupts data
  that MATLAB code safely mutated.
- Broadcasting and implicit expansion rules differ in edges;
  element-wise vs matrix operators (.* vs *) invert their
  defaultness between MATLAB and NumPy.
- Toolbox calls map to ecosystems, not functions: Signal Processing
  Toolbox to scipy.signal, Statistics Toolbox to statsmodels/scipy.
  stats, Image Processing to scikit-image - map the WORKFLOW to the
  library's idiom instead of reimplementing the MATLAB function
  signature.
- Numerical defaults: solvers, tolerances, RNG algorithms and seeds
  differ across platforms; identical seeds do NOT give identical
  streams, so statistical results match in distribution, not
  bitwise (rseng-numerical-accuracy sets the tolerance discipline,
  rseng-reproducibility the seed bookkeeping).
- Automatic translators (MATLAB-to-Python converters and similar)
  produce a starting draft at best: un-idiomatic, license-check the
  output, and every translated function still needs its parity
  test. Interop bridges (oct2py running Octave from Python) are
  better used as migration scaffolding - call the old
  implementation module by module while the new one grows - than as
  a destination.

## Migration as a project

1. Inventory and rank: which scripts/functions matter, which are
   dead; migrate the load-bearing path first.
2. Module-by-module with parity gates: port a module, run both
   implementations against the baseline inputs, assert agreement
   within scientifically justified tolerances, only then delete or
   bypass the original (strangler pattern - rseng-legacy-code).
3. Adopt the target's ecosystem hygiene as you go: environments and
   lockfiles (rseng-reproducible-environments), tests
   (rseng-testing), CI without license servers - the ability to run
   tests on every commit is a migration dividend
   (rseng-ci-cd).
4. Keep a translation log: mapping decisions, tolerance
   justifications, known behavior differences - the scientific
   record of the migration (rseng-documentation), and cite the
   original code's authors (rseng-citation-metadata).
5. Announce the migration to users with a compatibility note
   (rseng-science-communication) and license the freed code properly
   (rseng-licensing) - opening the platform without opening the
   license wastes the trip.

## Working with this skill

This skill is source-independent: it encodes community migration
practice between scientific computing platforms. The generic
legacy-code safety net is rseng-legacy-code; this skill is its
commercial-platform specialization.

Learn more (verified):
  - https://octave.org - GNU Octave
  - https://numpy.org/doc/stable/user/numpy-for-matlab-users.html -
    NumPy for MATLAB users (official mapping guide)
  - https://scipy.org - SciPy ecosystem
  - https://github.com/blink1073/oct2py - oct2py Octave-Python
    bridge
  - https://www.sympy.org - SymPy symbolic mathematics
  - https://julialang.org - Julia
  - https://pandas.pydata.org - pandas
  - https://docs.astropy.org/en/stable/ - Astropy (the IDL-exodus
    ecosystem)

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-legacy-code - characterization tests and strangler pattern
- rseng-licensing - license the freed code
- rseng-numerical-accuracy - parity tolerances across platforms
- rseng-reproducible-environments - target-ecosystem pinning as you go
- rseng-scientific-file-formats - exporting proprietary data formats first
- rseng-software-reuse - adopt an existing open reimplementation

<!-- related-skills:end -->
