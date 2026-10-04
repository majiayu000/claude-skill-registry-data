---
name: rseng-defensive-coding
description: >-
  Covers defenses against silently wrong research results: validating data at
  boundaries (schemas, assertions, sanity checks), explicit physical units and
  quantities in code (pint/astropy-style), disciplined randomness (explicit
  seeded generators, parallel streams), and fail-loud handling of NaN and
  missing data. Use PROACTIVELY when code ingests external or instrument data,
  when values carry physical units, when randomness enters simulations or
  sampling, or when NaN or missing-data handling is implicit; also when the
  user mentions data validation, unit errors, seeds or silent bugs, or reviews
  analysis code whose failure would be invisible. For floating-point behavior
  and tolerances see rseng-numerical-accuracy; for diagnosing an existing bug
  see rseng-debugging.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Defensive coding for research software

Research code's worst bug is the one that runs to completion: the
unit mismatch, the silently dropped rows, the column shifted by
one, the reused random stream - producing plausible, wrong numbers
that reach a paper. Defensive coding is the discipline of making
wrongness LOUD: validate at boundaries, make implicit physics and
randomness explicit, and prefer a crash today to a correction
notice next year. It complements rseng-numerical-accuracy (float
behavior) and feeds rseng-testing (the checks become tests).

## Validate at the boundaries

Data enters code at boundaries - files, instruments, APIs, user
parameters - and every boundary is a corruption opportunity:

- Schema-check tabular data on ingest: expected columns, dtypes,
  units, ranges, allowed categories, uniqueness of keys
  (pandera-style declarative schemas for DataFrames; JSON Schema
  for configs and records). The schema is executable documentation
  of the data contract (rseng-data-management's data dictionary,
  enforced).
- Sanity-check the science, not just the types: physical ranges
  (no negative concentrations, latitudes within +/-90), plausible
  magnitudes, conservation totals, expected row counts within
  tolerance of yesterday's. Domain assertions catch what dtype
  checks cannot.
- Missing data is a decision, not a default: silent NaN
  propagation and silent row-dropping (the pandas default in many
  operations) are the classic silent killers - count and REPORT
  what was excluded and why, and make exclusion rules explicit
  code (rseng-research-integrity checks this at the manuscript end;
  this skill prevents it at the source).
- Fail loud, fail early: raise on contract violations at ingest
  rather than letting bad data flow downstream; in batch settings
  quarantine-and-log per item (rseng-big-data-processing) - but
  never silently skip.

## Units and quantities

Unit errors are the canonical silent research bug - flagship
missions have died of them:

- Attach units in code, not in comments: a quantity library
  (pint; astropy.units in astronomy) makes units part of the
  value, checked at every operation - adding meters to seconds
  raises instead of publishing.
- Enforce at boundaries even when the core stays plain-numeric
  for performance: convert-and-strip on ingest (asserting the
  expected unit), reattach on output, and document the internal
  convention in ONE place (rseng-scientific-file-formats' metadata
  discipline carries units in the files themselves).
- Degrees vs radians, per-second vs per-minute, and log-vs-linear
  are unit bugs in spirit: name them in variable names or types
  when a full quantity system is overkill (angle_rad,
  rate_per_s).

## Disciplined randomness

- Explicit generators, never global state: create a seeded RNG
  object (numpy's Generator API) and pass it - seeding the global
  makes order-dependent, library-colliding randomness
  (the Scientific Python RNG guidance is the reference).
- Parallel work gets derived streams: spawn per-worker
  generators from a master seed (seed sequences), never the same
  seed in every worker - identical streams across "independent"
  replicates is a silent statistics-destroyer
  (rseng-hpc-computing job arrays included).
- Seeds are provenance: record them with outputs and in configs
  (rseng-reproducibility owns the bookkeeping); stochastic tests
  assert distributions or use fixed seeds knowingly
  (rseng-testing).

## The habit, proportioned

Not every script needs schemas: exploration code needs only the
cheap habits (explicit NaN policy, named units, seeded RNGs);
shared pipelines add ingest validation; published analyses add the
full contract checks in CI (rseng-ci-cd) so drift in upstream data
sources is caught at the pull request, not in the plot. When a
defensive check fires in production, keep it as a regression test -
each catch is a documented failure mode (rseng-trainer's
errors-are-curriculum applies: explain what the check just
prevented).

## Working with this skill

This skill is source-independent: its authority is the tool
documentation and Scientific Python guidance linked below. It is
the prevention layer for the failure modes rseng-research-integrity
hunts post-hoc.

Learn more (verified):
  - https://pandera.readthedocs.io - pandera DataFrame validation
  - https://pint.readthedocs.io - pint physical quantities
  - https://json-schema.org - JSON Schema for configs and records
  - https://docs.astropy.org/en/stable/ - astropy (units module)
  - https://blog.scientific-python.org/numpy/numpy-rng/ -
    Scientific Python guidance on NumPy random number generators

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-big-data-processing - quarantine-and-log at batch scale
- rseng-data-management - data dictionaries the schemas enforce
- rseng-hpc-computing - per-worker RNG streams in parallel jobs
- rseng-numerical-accuracy - float behavior behind silent errors
- rseng-research-integrity - post-hoc hunt for same failures
- rseng-testing - fired checks become regression tests

<!-- related-skills:end -->
