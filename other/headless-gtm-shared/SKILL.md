---
name: headless-gtm-shared
description: >
  Reference module for the Headless GTM chain, not a skill to invoke. Holds the
  record contract every chain skill reads and writes (CONVENTIONS.md) plus the
  Python helpers they import (common.py, schema.py). Installed alongside the
  chain so those imports and references resolve; read CONVENTIONS.md when you
  need the JSONL record shape, the runs/ layout, or the cost-gate rules.
---

# `headless-gtm-shared` - the chain's record contract and helpers

This folder is a library, not a skill. Nothing invokes it directly. It ships as
a skill folder for one reason: the `SKILL.md` marker is what makes skill
installers copy a directory, and every chain skill depends on this one.

## What is in here

| File | What it is | Who uses it |
|---|---|---|
| `CONVENTIONS.md` | The chain contract: JSONL records, additive per-stage fields, the `runs/<run-id>/` layout, deviation logging | Every chain skill references it; read it before changing any output format |
| `common.py` | `.env` loading, the >$10 cost gate, output-dir resolution, run slugs, run metadata | Imported by the chain scripts |
| `schema.py` | `ProspectRecord` construction and the CSV/JSON writers | Imported by the discovery scripts |
| `requirements.txt` | The full dependency list for the chain, mirrored at the repo root | `pip install` |

## If you are reading this because an import failed

A script exited with `cannot find headless-gtm-shared/common.py`. The skill was
copied out without this folder. Copy `skills/headless-gtm-shared/` next to the
skill that failed, so the layout is:

```
<skills-dir>/
├── headless-gtm-shared/          <- this folder
├── 02-apify-maps-discover/
└── ...
```

The `npx skills add` installer picks this folder up on its own. Only a manual
single-folder copy can miss it.

## Two rules worth knowing before you edit anything here

- **`common.load_env()` never overwrites an exported variable.** A real shell
  export or a secrets manager always beats a `.env` on disk. The loader only
  fills in what is missing.
- **`common.resolve_out_dir()` writes under the current working directory**, not
  under the skill. An installed skill is a read-only package; client output
  belongs in the project you are working in.
