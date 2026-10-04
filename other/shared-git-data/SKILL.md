---
name: shared-git-data
description: >
  Git for data science — versioning notebooks, datasets, and pipelines.
  DVC, nbstripout, .gitignore, and reproducible data workflows.
  Trigger: When working with git in data science projects, committing notebooks, managing datasets, or setting up a data repo.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "3.0"
  model_tier: T1-ultra-fast
---

# Skill: shared-git-data

Git for data science. Different from code — data needs its own rules.

## Trigger

- Starting a data project and creating the repo
- Committing a notebook and you don't want to push megabytes of outputs
- Should the dataset be in the repo or not?
- You need to version pipelines without versioning heavy data

## Workflow LEND

1. ANALYZE
   ├── Project: analysis, pipeline, dashboard?
   ├── Data: how big? can it go in the repo? (< 100 MB)
   ├── Notebooks: outputs included or stripped?
   └── Collaboration: solo or team?

2. OFFER (Senior Menu)
   ├── A) Standard git — code + clean notebooks + small data (< 100 MB)
   ├── B) Git + DVC — large data versioned outside the repo
   └── C) Git + nbstripout — notebooks without outputs, clean diffs

3. CHOOSE → user confirms

4. EXECUTE
   ├── .gitignore: .venv/, __pycache__/, *.pyc, .env, data/raw/
   ├── nbstripout: `git config filter.nbstripout.extrakeys 'metadata.kernel'`
   ├── DVC: `dvc init && dvc add data/raw/dataset.csv && git add data/raw/dataset.csv.dvc`
   ├── README.md with reproduction instructions
   ├── requirements.txt frozen
   ├── Commits in English US, semantic (feat, fix, chore)
   └── Branch + PR workflow for data pipelines

5. VERIFY
   ├── .gitignore covers what shouldn't be in the repo
   ├── Notebooks can be diffed (no outputs)
   └── A fresh `git clone && pip install` is enough to start

- [ ] Save decisions and changes to Engram (mem_save)
- [ ] Check if README, AGENTS.md, or ARCHITECTURE.md need updating
- [ ] If docs changed → update them in the same PR/commit
