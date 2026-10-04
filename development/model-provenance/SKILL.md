---
name: model-provenance
description: >-
  Use when the user names a specific ML model (e.g. DINOv3, SAM 2, Whisper,
  Qwen2-VL) and wants its real/official code, training recipe, or papers
  found, verified, or archived locally for grounded coding. Triggers include
  "find the real code for this model", "harvest DINOv3", "store the model's
  code and papers locally", "archive the training/inference code", "set up a
  local source-of-truth / reference archive for a model", or any request that
  future coding against a model be grounded in its actual source instead of
  training-time memory.
---

# Model Provenance

Given a model name, produce a local, verified, self-contained archive of its
**actual** code and papers, then register a memory so all future work on that
model reads the real source instead of guessing.

## When NOT to use
- The user wants to *run/train* the model now, and an archive already exists →
  use the `grounding` skill, which reads this archive and checks the code
  against it. This skill builds the archive; `grounding` spends it.
- A generic literature review with no specific model → use research/deep-research.

## Output layout (the "safe folder")

**Always archive to the global root `~/.claude/model-provenance/<model-slug>/`,
never inside the current project.** The archive is a machine-wide source of
truth shared by every project (the memory in step 8 points other repos at this
absolute path), so it must not live under any one project's working dir and must
not be committed to a project's git history. Do **not** ask for or accept a
per-project location; if the user wants a copy in their project, symlink it
after the fact. Expand `~` to the real `$HOME` in every path you write down.
Slugify the exact variant: `DINOv3` → `dinov3`, `SAM 2` → `sam2`.

```
~/.claude/model-provenance/<model-slug>/
├── code/         # full git clones — canonical repo first, key community repos
├── key_code/     # extracted train loop, model def, inference; + MANIFEST.md
├── papers/       # <slug>.pdf + <slug>.metadata.json (title/authors/abstract/bibtex)
├── hub/          # per official checkpoint: config/preprocessor/tokenizer/chat-template,
│                 # model card, revision sha, license+gated status — metadata, never weights
├── SOURCES.md    # provenance manifest: every repo+paper+checkpoint, commit pin, WHY canonical
└── notes.md      # synthesis: architecture, recipe, I/O contract, variants, how to run
```

**Reuse what's already there.** Before doing any network work, check whether
`~/.claude/model-provenance/<slug>/` already exists. If it does, treat the
existing archive as the starting point and only fill gaps — do not re-clone,
re-extract, or re-download artifacts that are already present and valid. Each
step below states its own skip condition. If the user explicitly asks to
refresh, delete the relevant subdir(s) first, then re-run those steps.

**Write the archive once, at harvest; never pollute it with usage.** The
archive captures a model's source *as gathered the first time*. When a later
session reads it to write code for some experiment, that experiment's working
notes, results, debugging observations, or "what worked for me in exp-xx" do
**NOT** get written back into the archive — they belong in the project or the
chat. The only writes to an existing archive are (a) filling a genuine gap in
the original harvest (a missing paper, an un-extracted repo) or (b) an explicit
user-requested refresh. Nothing session- or experiment-specific is ever added,
and no file under the archive is edited to record how the model was used.

**Safety:** this skill archives code; it never executes cloned repos, installs
their dependencies, or runs their scripts. Reading and copying only.

## Workflow

Track these as todos. Steps 1–2 are high-judgment (do them inline / with an
agent); steps 3–6 are mechanical; step 7 is the synthesis; steps 8–9 are
required, not optional polish.

### 0. Check for an existing archive
```bash
ls -la ~/.claude/model-provenance/<slug>/ 2>/dev/null && \
  cat ~/.claude/model-provenance/<slug>/SOURCES.md 2>/dev/null
```
If the archive already exists and `SOURCES.md` covers the canonical repo + the
papers the user wants, this skill is mostly done: report what's there, run the
step 9 verification, and only re-enter the steps below for whatever is missing
or stale. A fresh archive starts at step 1.

### 1. Discover candidates
Confirm the exact model variant with the user if ambiguous (DINOv3 vs DINOv2).
Fan out searches across web, GitHub, Hugging Face, and arXiv.
See `references/discovery.md` for the exact queries and APIs. Collect a candidate
list of repos and papers — do not commit to one yet.

### 2. Verify the canonical source
Do not trust the top GitHub result. Score candidates with the verification
rubric in `references/discovery.md` (author-org match, paper→repo link, HF paper
page link, HF card, fork check). For non-obvious cases, dispatch a
subagent to cross-check author affiliations against repo ownership and report
which repo is official with evidence. Decide:
- the **canonical** repo (required), and
- optionally 0–2 **community** repos worth archiving (clearer impls), labeled as such.

### 3. Create the archive + clone
Create the folder layout, then clone into `code/` and **pin the commit**:
```bash
ROOT=~/.claude/model-provenance/<slug>
mkdir -p "$ROOT"/{code,key_code,papers,hub}
# skip if already cloned (idempotent re-runs)
[ -d "$ROOT/code/<repo>" ] || git -C "$ROOT/code" clone --depth 1 <canonical-repo-url>
# record the exact commit for reproducibility
git -C "$ROOT/code/<repo>" rev-parse HEAD
```
Use `--depth 1` for speed unless the user wants full history. If the user named
a specific revision (e.g. SAM 2.1) and the repo has a matching release tag,
clone that tag (`--depth 1 --branch <tag>`) instead of bare HEAD — HEAD of an
active repo may already be past it (see discovery.md, "Version drift"). If the
repo dir is already present, keep it (note its pinned commit) rather than
re-cloning.

### 4. Extract key code
`scripts/` paths below are relative to **this skill's directory** (the base
directory announced when the skill loads), not the project. For each cloned
repo, pull the high-signal train/inference/model/config files:
```bash
scripts/extract_key_code.py "$ROOT/code/<repo>" --out "$ROOT/key_code"
```
Skip a repo whose files are already under `key_code/` with a current
`MANIFEST.md` unless the clone changed. This writes `key_code/MANIFEST.md`
(including the source commit). Skim it; if
the training loop or model def is missing (unusual layout), locate it by hand
and copy it in. Config-heavy repos are capped at 50 files per category
(`--max-per-category`); overflow is listed in the manifest but not copied.

### 5. Download papers
For each paper (primary + method-defining predecessors — see discovery.md):
```bash
scripts/fetch_paper.py <arxiv-id-or-url> --out "$ROOT/papers"
```
Accepts an arXiv id (`2304.07193`), an `/abs/` or `/pdf/` URL, or a direct PDF
URL (`--name <slug>` to set the filename). Writes the PDF + a metadata sidecar
with bibtex. Skip any paper whose `.pdf` + `.metadata.json` already exist in
`papers/` and pass the step 9 `%PDF` check.

### 6. Capture Hub checkpoint metadata
The released checkpoint's own config files are the ground truth for *using*
the model, and they routinely disagree with the paper (input resolution,
normalization constants, chat template). For each **official** checkpoint the
user will code against (1–5, from the lab's HF org — the reverse arXiv lookup
in discovery.md surfaces them):
```bash
scripts/fetch_hub_meta.py <org/checkpoint-id> --out "$ROOT/hub"
```
Fetches metadata only, never weights: `config.json`,
`preprocessor_config.json` / `tokenizer_config.json` (incl. chat template),
`generation_config.json`, the model card, plus `info.json` with the revision
sha, license, gated status, and the weight-file inventory (names + sizes).
Gated repos still yield `info.json` + model card; the script reports the
misses — record them in `SOURCES.md` ("config gated; accept license at <url>
to fetch"). Skip checkpoints already under `hub/` with an `info.json`.

### 7. Write SOURCES.md and notes.md
- **`SOURCES.md`** — the provenance ledger. For every repo: URL, pinned commit,
  canonical|community label, and the one-line evidence for why it's canonical.
  For every paper: title, arXiv id, local filename. For every checkpoint:
  repo id, revision sha, license, gated status.
- **`notes.md`** — read `key_code/`, `hub/`, and the papers and synthesize the
  doc future-you reads first. Required sections:
  - **Architecture overview** and the **training recipe** (objective, losses,
    key hyperparameters, data).
  - **Variant table** — every official checkpoint: HF repo id, params,
    input size / context length, embedding dim, and which variant the paper's
    headline numbers used. Hallucinated checkpoint ids are the most common
    grounding failure; this table is the antidote.
  - **I/O contract** — input preprocessing (resolution, normalization
    constants, tokenization / chat template) and output semantics (pooled vs
    CLS token, shapes, logits vs embeddings), cited to `hub/` configs or
    `key_code/`. Where paper and shipped checkpoint disagree, the `hub/`
    config wins for inference — cite both.
  - **Versions & license** — minimum library versions the model class needs
    (e.g. which `transformers` release added it), the license, and gated
    status (a future session must know before writing a download that 401s).
  - **How to run inference** — concrete, grounded in the model card snippet
    or a `key_code/` entrypoint.
  - **Reference numbers** — 1–2 benchmark figures from the paper/model card a
    future session can sanity-check its integration against.
  - Optionally **Gotchas** (≤5 bullets) — known pitfalls from the repo's
    pinned/top issues or paper-vs-code mismatches, each cited to an issue URL
    or file:line.

  Hold every section to this bar:
  - **Every factual claim carries a citation to its source** — a
    `key_code/<file>:<line>` (line or range) or `hub/<checkpoint>/<file>` for
    code/config, a paper `§section` for a paper claim. A hyperparameter, layer
    name, loss term, default, or API signature written without a line/section
    reference does not belong here.
  - **No claims from memory, no false or aspirational claims.** If the archived
    source does not state it, do not write it. Anything you cannot verify
    against a file goes under an explicit `## Unverified` heading, marked as
    such — never mixed into the grounded sections as if it were confirmed.
  - It is a **map into the real files, not a replacement** for them: quote and
    point at exact lines; do not paraphrase from recall. When code and paper
    disagree, note both with citations rather than picking silently.

### 8. Register the mandatory-read memory  ← required
So future sessions ground coding in the real source, write a memory file (see
the memory instructions in the system prompt) and index it in `MEMORY.md`:

- `type: reference`, name `model-src-<slug>`. If this memory already exists,
  update it in place rather than creating a duplicate.
- Body must state the **absolute path** to the global archive (expand `~`, e.g.
  `/home/<user>/.claude/model-provenance/<slug>`) and an explicit rule:

  > **Before writing or reviewing any code involving `<model>`, use the
  > `grounding` skill against `<abs-path>`. Read `<abs-path>/notes.md` and the
  > relevant files under `<abs-path>/key_code/` and `<abs-path>/hub/` first.
  > Ground all APIs, layer names, checkpoint ids, preprocessing constants, and
  > the training recipe in that archived source — do not rely on memory for this
  > model. The archive is a read-only reference: never write experiment or usage
  > notes into it.**

- Link related models with `[[model-src-...]]` (e.g. DINOv3 → `[[model-src-dinov2]]`).
- Add the one-line pointer to `MEMORY.md`:
  `- [<model> source archive](model-src-<slug>.md) — MUST read before coding <model>`

This is what makes the archive *binding*: the pointer loads every session, and
the memory's recall makes reading the real code mandatory rather than optional.
The `grounding` skill is the procedure a later session follows to do it —
resolve the archive, read the cited files, then check the code it wrote against
them.

### 9. Verify the archive  ← before reporting
Run these checks; fix anything that fails rather than reporting around it:
- every `papers/*.pdf` starts with `%PDF` (`head -c4`) and has a matching
  `.metadata.json` sidecar. If a PDF fails the check (HTML error page), delete
  it and re-fetch from an alternate source (arXiv `/pdf/` URL, the paper's
  project page); if it still fails, remove the junk file and record the miss
  in `SOURCES.md` instead;
- `key_code/` contains at least a model definition plus a train **or**
  inference file, and `MANIFEST.md`'s source commit matches the pin in
  `SOURCES.md`;
- `SOURCES.md` has a pinned commit and one-line canonical evidence for every
  repo in `code/`, and a repo id + revision sha + license/gated status for
  every checkpoint in `hub/`;
- `hub/` holds an `info.json` for at least the primary official checkpoint (or
  `SOURCES.md` records why none exists), and every non-gated checkpoint's
  `config.json` parses as JSON;
- `notes.md` has the required sections (variant table, I/O contract,
  versions & license, reference numbers) and its claims are cited: spot-check
  that hyperparameters, layer names, and API signatures carry a
  `key_code/<file>:<line>`, `hub/<checkpoint>/<file>`, or paper `§` ref, that
  the cited lines actually say what's claimed, and that anything uncertain sits
  under `## Unverified` rather than in the grounded sections;
- the archive contains no experiment/usage notes — only first-harvest source and
  its factual ledger;
- the memory file exists and `MEMORY.md` contains its pointer line.

## Final report to the user
State where the archive lives, the canonical repo + pinned commit, what was
extracted, the papers saved, the checkpoints captured (with license/gated
notes), and that the mandatory-read memory is registered.
Flag anything uncertain (e.g. "could not find official training code; archived
the most-trusted community impl").
