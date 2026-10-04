---
name: rseng-reproducibility
description: >-
  Covers end-to-end computational reproducibility: making a project's results
  regenerable with one command, determinism and seed discipline, research
  compendium structure, replication packages for papers, Binder-launchable
  repositories, artifact evaluation and reproducibility badges. Use
  PROACTIVELY when the user wants results others can reproduce, prepares a
  replication package or artifact submission, mentions reproducibility,
  research compendia, Binder or badges, asks why results differ between runs
  or machines, or is about to publish results whose regeneration path is
  untested. (Pinning environments: rseng-reproducible-environments; pipeline
  automation: rseng-workflows; run-level lineage: rseng-provenance.)
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Computational reproducibility

Reproducibility is the ability of someone else - including the
author in six months - to regenerate the results from the code and
data. It is not one practice but a stack: pinned environments
(rseng-reproducible-environments), scripted pipelines (rseng-workflows),
versioned data (rseng-data-management) and controlled randomness,
assembled so that ONE documented command rebuilds the results. This
skill owns the assembly and its verification; the layers below have
their own skills. The bar to aim for: a stranger with the repository
and the README reproduces the paper's numbers without emailing
anyone.

## The one-command bar

- Everything scripted, nothing manual: any step a human performs by
  hand (a click, a copy, an "then edit line 12") is a reproduction
  failure waiting to happen. Encode the full path from raw data to
  final figures/tables in a workflow or top-level script
  (rseng-workflows).
- One entry point, documented: `make reproduce`, `snakemake all` or
  ./run.sh - named in the README with expected runtime and resource
  needs. Long-running steps get cached intermediates so partial
  reruns are practical.
- Outputs land in generated directories, mapped to the paper:
  which script makes Figure 3 must be answerable from the repo
  (a results/README or a figures manifest).
- Configuration explicit: every parameter that shaped the published
  results lives in versioned config files, not command-line lore or
  notebook cell edits.

## Determinism and honest nondeterminism

- Seed discipline: explicit RNG objects seeded from configuration,
  never global unseeded randomness; derive per-worker streams from a
  master seed for parallel runs; record seeds with outputs - a seed
  is provenance.
- Know the nondeterminism you cannot remove: thread scheduling,
  parallel reduction order, GPU kernels and library versions
  legitimately perturb low-order bits (rseng-numerical-accuracy).
  State the expected variability ("results match to 1e-6; figures
  identical") instead of claiming bit-identity you have not tested.
- Sort the unordered: filesystem listings, dict/set iteration and
  parallel completion order differ across runs; sort before anything
  result-bearing.

## The research compendium

Structure the repository as a compendium - the recognized shape for
reproducible research projects: data (raw read-only, processed
generated), code, environment specification, outputs, and a README
tying them together with the one command. Conventions and examples
live at research-compendium.science. For projects headed
to review, the compendium IS the replication package.

## Replication packages and artifact evaluation

When results support a paper:

- Assemble the package: frozen code version (tagged release -
  rseng-publishing-releasing), data or scripted data retrieval with
  checksums (rseng-data-management), pinned environment, run
  instructions with runtimes, and a manifest mapping outputs to
  paper claims.
- Deposit, do not just link: an archival repository with a DOI
  (Zenodo-class) is the durable home; a git URL alone does not meet
  artifact-availability bars (ACM's artifact badging explicitly
  requires archival deposit for its Available badge).
- Target the venue's checklist when one exists (artifact evaluation
  tracks, journal data editors); rseng-software-peer-review covers
  review-side mechanics and CODECHECK-style independent execution.
- Declare AI involvement in producing the results in aidecl.yaml
  (rseng-ai-declaration) - reproducibility and provenance are the same
  promise at different layers.

## Binder: reproducibility others can click

repo2docker builds a runnable image from a repository's standard
environment files; mybinder.org hosts it so anyone can run the
analysis in a browser without installing anything. Make a repo
Binder-ready by keeping environment files canonical (no
requirements drift), test the build locally with repo2docker before
adding the badge, and expect image builds to rot as dependencies
move - pin versions and re-test at releases
(rseng-reproducible-environments). For compute-heavy work, Binder
demos a subset; the full run documents its HPC path
(rseng-hpc-computing).

## Verify before you claim

Reproducibility untested is reproducibility absent:

- Clean-room test: fresh clone on a machine (or container) that
  never ran the project, follow only the README, compare outputs to
  the published ones with stated tolerances. This finds the
  undeclared dependency and the hardcoded path every time.
- Automate the claim where affordable: a CI job that runs the
  pipeline on reduced data and compares key numbers keeps the
  reproduction path from rotting between releases (rseng-ci-cd).
- Independent reruns (a colleague, a CODECHECK, a ReproHack-style
  event) are the strongest evidence - and normal practice, not an
  audit to fear.

## Working with this skill

This skill is source-independent: its authority is the community
reproducibility guidance and tooling linked below. It assembles what
rseng-reproducible-environments, rseng-workflows and rseng-data-management
provide layer by layer.

Learn more (verified):
  - https://research-compendium.science - research compendium
    conventions and examples
  - https://mybinder.org - Binder
  - https://github.com/jupyterhub/repo2docker - repo2docker
  - https://codecheck.org.uk/ - CODECHECK independent execution

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - declaring AI involvement in results
- rseng-archiving - depositing the package with a DOI
- rseng-data-management - versioned data with checksums
- rseng-numerical-accuracy - stating expected run-to-run variability
- rseng-publishing-releasing - tagged frozen release for the package
- rseng-software-peer-review - CODECHECK-style independent reruns

<!-- related-skills:end -->
