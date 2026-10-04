---
name: gaia-bot-curate
description: >
  Curate Gaia bot crawler branches into real-skill catalog entries and clean up
  processed bot/* branches. Use when the user says: "process bot branches",
  "curate the crawl output", "clean up bot proposals", "run bot curation",
  "merge the crawler results", "review bot/* branches", "ingest crawler data",
  or explicitly types /gaia-bot-curate. Also triggers when the user asks to
  review pending `bot/*` branches, turn crawler JSON proposals into registry
  nodes, decide which crawled skills to accept vs reject, or batch-add skills
  from an automated crawl run. This skill handles the full pipeline: fetch
  remote bot branches, triage proposals, run `gaia dev` mutations, validate,
  open a PR, and delete consumed bot branches.
---

# gaia-bot-curate

Turn remote `bot/*` crawler branches into curated `registry/nodes/` entries via `gaia dev` commands, then clean up the processed branches and open a PR.

The guiding principle: bot crawlers cast a wide net. Your job is quality filtration — accept only concrete skill implementations with enough signal, reject or defer everything else, and never let a bad state land in the registry.

## Workflow

### 1. Start clean

```bash
git fetch --all --prune
```

Create `review/meta/<short-crawl-slug>` from `origin/main`. Never merge bot branches directly — crawl output needs human-in-the-loop filtration before touching the registry.

### 2. Collect and deduplicate bot payloads

List remote crawler branches:
```bash
git for-each-ref refs/remotes/origin/bot
```

For each branch, find its added proposal files:
```bash
git diff --name-only $(git merge-base origin/main <branch>)..<branch> -- proposals
```

Write raw payload copies and a compact deduplicated candidate JSON to `/tmp`. Also write `/tmp/gaia-bot-crawl-skill-names-<date>.md` with: source branch, proposal file, candidate ID, name, evidence URL, and duplicate source refs. Deduplicate by proposal `id`; fall back to normalized lowercase `name` when `id` is absent.

Keep payloads outside the repo so the review branch stays registry-only.

### 3. Dispatch narrow triage agents

Split candidates by source type (`github`, `vscode-marketplace`, `huggingface`, or other). Give each triage agent only its relevant `/tmp` candidate JSON subset — not full raw payloads or unrelated history. Ask for structured output per candidate: `id`, `name`, `contributor`, `url`, optional `sourceRepo` and `mapsToGaia`, and a `reason` field.

Narrow context keeps triage agents fast and prevents one noisy source from polluting judgement on another.

### 4. Accept, reject, and analyze

**Accept** a candidate when it is a concrete skill implementation: a workflow artifact, model capability page, reputable package, or documented tool with real usage evidence.

**Require needs-evidence (defer)** for MCP servers, API connectors, and tool extensions unless they include a specific agent playbook (e.g., `AGENTS.md`, `CLAUDE.md`, `.claude/skills/`, or documented autonomous agent workflows). The presence of a server does not demonstrate skill mastery; a playbook does.

**Fusion analysis** — for each accepted item, ask: does it combine multiple basic capabilities in a novel way? If so, propose a new Fusion (`type: fusion`) rather than shoe-horning it into an existing generic. Combinations like `web-scrape + browser-automation` warrant their own taxonomy node.

**Demerit assignment** — apply demerits only at Level 3★ (Evolved) or higher. Below that threshold, leniency serves registry growth. Assign a demerit only when it breaks the "Install Anywhere" promise for a typical developer:
- `heavyweight-dependency`: requires massive local infrastructure (e.g., full Airflow stack, 10 GB+ Docker images)
- `niche-integration`: restricted to a non-portable OS or IDE (e.g., Windows-only Visual Studio extension)

If a high-level skill is demerit-free, it is a strong Named Promotion candidate.

**Named promotion** — if the item has a clear playbook and high quality, propose it as a Named Skill in `registry/named/`. Verify the `links.github` URL uses `blob/<branch>/subpath` format (not a bare repo root or `tree/` URL). Without a valid blob URL, submit at 1★ (Awakened) — this is a hard rule from META.md §2.4, not a soft fallback to 2★. A missing blob link is evidence of insufficient curation signal.

### 5. Integrate via `gaia dev` commands

The `gaia dev` mutation verbs are the only sanctioned way to write to `registry/`. Direct file edits skip timeline logging and break schema integrity — if you find a gap where the CLI can't do what you need, file an issue tagged `CLI` + `tech-debt` and stop.

**Generic (starless) nodes:**
```bash
gaia dev add "Skill Name" --id <id> --type basic --description "..."
```
Generic skills have no `--level` flag; they are rank-less taxonomy entries.

**Named skills:**
```bash
gaia dev add "Skill Name" --id <id> --named --contributor <user> --generic-ref <ref> --status awakened
```
Named skills always start as `awakened`. A human reviewer later promotes to `named` and calibrates stars (2★–6★). Do not hand-set `title` or `catalogRef`.

**Evidence, calibration, and wiring:**
```bash
gaia dev evidence <id> "<url>" --type <type>        # attach evidence
gaia dev calibrate <id> "<star>"                    # set/adjust star level after evidence
gaia dev link <target-id> <prereq-id-1>,<prereq-id-2>  # wire prerequisites
gaia dev reclassify <id> <type>                    # change skill type if needed
gaia dev update-named <contributor/skill> --status awakened  # patch named-skill frontmatter
gaia dev rm <id>                                   # remove a skill added in error
```

When batching multiple adds, pass `--no-build` on each and run `gaia dev build` once at the end to avoid redundant regeneration.

### 6. Clean remote bot branches

Delete consumed bot branches only after the `/tmp` snapshot exists and the review branch contains the curated result. This ordering ensures the crawl data is never lost even if something goes wrong post-deletion.

```bash
git push origin --delete <bot-branch>
git ls-remote --heads origin <bot-branch>  # confirm deletion
```

### 7. Verify and publish

```bash
gaia dev docs
gaia dev validate
./.venv/bin/pytest tests/test_validate.py tests/test_real_skill_catalog.py tests/test_registry_layout.py
git diff --check
```

Review `git diff --name-only origin/main`. A `review/meta` branch must not touch `packages/`, `src/`, or `registry/schema/`. If pre-commit hooks inject package or version churn, restore out-of-scope files from `origin/main`, rerun verification, and amend with `--no-verify` only after manual validation passes.

Push the review branch and open a PR. The PR description should cover:
- PR URL and temp snapshot path
- Accepted skill count, broken down by source type
- Rejected and `needs-evidence` counts with representative reasons
- Validation command outcomes
- Remote bot branches deleted
