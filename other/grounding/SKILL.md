---
name: grounding
description: >-
  Use before writing, reviewing, or debugging any code that uses a specific ML
  model (DINOv3, SAM 2, Whisper, Qwen3-Embedding, SigLIP 2…), whenever a
  model-provenance archive for it exists locally. Loads that archive's real
  source — checkpoint ids, API signatures, preprocessing constants, training
  recipe — so the code is written from the model's actual code instead of
  training-time recall, then mechanically checks the result. Triggers include
  "load DINOv3 and extract features", "fine-tune SAM 2 on my data", "why does
  this checkpoint 404", "review this inference script", or any coding task
  naming a model that has been harvested.
allowed-tools: Bash, Read, Grep, Glob
---

# Grounding

`model-provenance` harvests a model's real code, papers, and checkpoint
metadata once. This skill is what every later session does with it: read the
archived source *before* writing code, so the checkpoint ids, class names,
preprocessing constants, and recipe come from the model's actual source rather
than from recall.

That distinction is the whole point. Your memory of a specific model is
plausible and lossy in a way that is hard to notice: checkpoint ids that look
exactly right and 404, a class name borrowed from a neighbouring model, a
normalization constant from the previous version, an argument that was renamed
a release ago. All of it reads as confident, correct code. The archive is the
only thing on this machine that can settle those questions, so consult it first
and check against it after.

## Workflow

### 1. Find the archive

```bash
scripts/load_archive.py "<model name>"
```

Name matching is fuzzy — `DINOv3`, `dinov3`, and `"SAM 2"` all resolve. It
prints the archive path, `notes.md`'s outline, the captured checkpoint ids with
their gated/license status, and what the archive is missing.

`scripts/load_archive.py --list` shows every archive on this machine.

**If there is no archive**, this skill has nothing to offer. Say so plainly and
pick one:

- Run `model-provenance` to harvest the model first — right when the code
  matters, or the model is obscure, or a wrong checkpoint id costs a long
  download.
- Proceed from memory, having *told the user* that the model's details are
  ungrounded and that checkpoint ids and API signatures may be wrong.

Never quietly fall back to memory. An ungrounded answer that looks identical to
a grounded one is the failure this skill exists to prevent.

### 2. Read before writing

Read `notes.md` first, in full. It is the synthesis: architecture, training
recipe, variant table, I/O contract, versions and license, a working inference
snippet, and known gotchas — every claim cited to a file and line.

Then read only what the task needs, following `notes.md`'s citations:

| The task turns on | Read |
|---|---|
| which checkpoint to load | the variant table, then `hub/<checkpoint>/info.json` for the revision sha, license, and gated status |
| input preprocessing | `hub/<checkpoint>/preprocessor_config.json`, and the I/O contract section |
| tokenization or a chat template | `hub/<checkpoint>/tokenizer_config.json` |
| output shapes and semantics | the I/O contract section, then the model definition in `key_code/` |
| the training objective or losses | the training-recipe section, then the train loop in `key_code/` |
| why upstream code does something | the pinned clone under `code/` |

Don't read the whole archive. Some run to 30MB+, and `notes.md` plus two cited
files is normally the entire answer.

Treat `notes.md`'s `## Unverified` section as exactly that: leads, not facts.

### 3. Write the code

Take checkpoint ids, class names, function signatures, argument names, and
numeric constants from what you just read. Where the paper and the shipped
checkpoint disagree, the `hub/` config wins for inference — the paper describes
what was trained, the config describes what was released.

Cite the archive in comments where a value would otherwise look arbitrary:

```python
# mean/std from hub/facebook__dinov3-vitb16-pretrain-lvd1689m/preprocessor_config.json
```

A future reader — including you — needs to know which numbers came from the
real source and which were chosen.

If the archive genuinely does not answer something, say so and mark it, rather
than filling the hole with a plausible value. A flagged gap gets checked; an
invented constant does not.

### 4. Check what you wrote

```bash
scripts/check_grounding.py --model "<model name>" <files you wrote or changed>
```

It pulls the Hub repo ids and model-specific symbols out of your code and
verifies each appears in the archive, exiting non-zero on any miss. This catches
the two failures that survive careful writing: a checkpoint id that looks right
and does not exist, and a class name from a different model in the same family.

An `UNGROUNDED` line is normally a real error — find the correct identifier in
the archive. Occasionally it is real but newer than the harvest, in which case
confirm it upstream and tell the user the archive is stale.

The check is narrow on purpose. It ignores general library APIs, so a clean run
means those identifiers exist, not that the code is correct.

## The archive is read-only

Never write into `~/.claude/model-provenance/<slug>/`. Not experiment results,
not "this worked for me", not debugging notes, not a fixed version of a snippet.
The archive records what the model's source said at harvest, and it is shared by
every project on this machine — mixing one experiment's findings into it
corrupts that for everything else. Session findings belong in the project or the
chat.

Filling a genuine gap in the original harvest — a missing paper, an
un-extracted repo — is `model-provenance`'s job, not this skill's.

## Incomplete archives

Older archives predate parts of the harvest, and `load_archive.py` reports what
is absent. Work with what is there and say what is missing:

- **No `notes.md`** — no synthesis was written. Read `key_code/MANIFEST.md` and
  the source directly. You are reading raw code rather than a cited summary, so
  hold claims to what you can point at.
- **No `hub/`** — checkpoint metadata was never captured, so ids are not
  verified here. `notes.md`'s variant table is the next best source; confirm any
  id against the Hub before writing it into code that downloads weights.
- **Nothing but `code/`** — treat it as a pinned clone and read it as source.

An incomplete archive still beats memory. Say which parts are grounded and which
are not.
