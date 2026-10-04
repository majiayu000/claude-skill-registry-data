---
name: rseng-notebooks
description: >-
  Covers engineering discipline for computational notebooks: execution-order
  and hidden-state pitfalls, restart-and-run-all hygiene, keeping notebooks in
  version control with jupytext, testing notebooks with nbval-style execution
  checks, parameterizing and batch-running them with papermill, refactoring
  mature notebook code into importable modules, and deciding what belongs in a
  notebook versus a package. Use PROACTIVELY when a project contains .ipynb
  files, when the user works in Jupyter or similar notebooks, mentions
  notebook reproducibility, testing, version control or parameterization, when
  a notebook has grown into the de-facto pipeline, or when notebook results
  must become citable, reviewable artifacts.
license: CC-BY-4.0
metadata:
  version: 0.1.0
---

# Notebook engineering

Notebooks are where most research computing happens - and their
superpower (interactive, stateful, out-of-order execution) is
exactly their reproducibility hazard. The discipline is not "stop
using notebooks"; it is knowing what notebooks are FOR
(exploration, narrative, teaching) and applying engineering at the
point where a notebook turns into infrastructure without anyone
deciding it should. The
CodeRefinery Jupyter lesson teaches the same split.

## Hidden state: the core hazard

A notebook's on-screen code and its kernel's actual state can
disagree: cells run out of order, deleted cells leave live
variables, and a figure can come from code that no longer exists.
Working rules:

- Restart-and-run-all IS the test: before trusting, committing or
  sharing any notebook, restart the kernel and run top to bottom.
  A notebook that only works in one execution order is broken -
  fix the order now, while you still remember it.
- Keep cells re-runnable: no cell should break when run twice
  (guard appends, recreations, cumulative mutations); avoid
  mutating a variable across distant cells - derive new names
  instead.
- Definitions up top: imports, parameters and configuration in the
  first cells; a parameters cell makes intent explicit and enables
  parameterization later.
- Watch execution counts: out-of-sequence numbers in a "final"
  notebook are the tell (rseng-version-control-review reviewers can
  see them too).

## Version control that works

Raw .ipynb diffs are JSON noise with embedded outputs:

- Pair notebooks with a script/markdown twin via jupytext: the
  text twin is the reviewable, diffable, mergeable source; the
  .ipynb carries outputs locally.
- Decide the output policy explicitly: strip outputs before
  commit (clean diffs, smaller repos - a pre-commit hook
  automates it) OR commit executed notebooks deliberately as
  result records (rseng-reproducibility's compendium may want
  exactly that); mixing the two policies in one repo confuses
  everyone.
- Large embedded outputs (images, tables) are the notebook form
  of committed data - the same instincts apply
  (rseng-data-management).

## Testing and automation

- Execution tests: run notebooks in CI and fail on errors
  (nbval-style pytest integration checks stored outputs too;
  plain execution via papermill or nbconvert catches rot). A
  notebook that no longer runs is the most common form of
  repository decay (rseng-ci-cd; budget-conscious: run on reduced
  data - rseng-green-computing).
- Parameterize with papermill: a tagged parameters cell turns a
  notebook into a callable with arguments - the honest bridge
  from "notebook" to "batch job" (sweeps via rseng-hpc-computing
  job arrays or rseng-workflows without abandoning the notebook
  form).
- Environments: a notebook without a pinned environment is a
  screenshot; keep the kernel's environment in the repository's
  lockfile (rseng-reproducible-environments) and Binder-ready when
  sharing is the goal (rseng-reproducibility).
- Seeds and data paths follow the same rules as any code
  (rseng-defensive-coding) - notebooks get no exemption from
  provenance.

## The graduation path

Notebooks accumulate load-bearing code; the move is extraction,
not rewrite:

- When a function is used twice, or another notebook copies it,
  extract it to a module in the repository and import it - the
  notebook keeps the narrative, the module gets tests
  (rseng-testing) and design (rseng-software-design). Autoreload
  during development keeps the loop tight.
- When a notebook IS the pipeline (runs nightly, feeds a paper),
  graduate the computation to scripts/workflow stages
  (rseng-workflows) and keep a thin notebook as the exploratory
  window onto results.
- The notebook that remains is the good kind: narrative analysis,
  figures with their reasoning, teaching material
  (rseng-trainer) - prose and code interleaved doing what neither
  does alone (rseng-science-communication for the storytelling
  layer).

## Working with this skill

This skill is source-independent: its authority is the Jupyter
ecosystem tooling and the CodeRefinery lesson linked below.

Learn more (verified):
  - https://jupyter.org - Project Jupyter
  - https://jupytext.readthedocs.io - jupytext notebook/text
    pairing
  - https://github.com/computationalmodelling/nbval - nbval
    notebook validation
  - https://papermill.readthedocs.io - papermill parameterization
  - https://coderefinery.github.io/jupyter/ - CodeRefinery
    Jupyter lesson

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-hpc-computing - papermill batch sweeps on clusters
- rseng-reproducibility - executed notebooks as deliberate result records
- rseng-science-communication - narrative layer of analysis notebooks
- rseng-scientific-visualization - figure-producing notebook cells
- rseng-trainer - notebooks as teaching material
- rseng-version-control-review - jupytext twins make diffs reviewable

<!-- related-skills:end -->
