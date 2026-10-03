---
name: adopt
description: Bootstrap Plumbline into an existing project — lay the Plumbline/ machinery and Planning/ skeleton non-destructively, detect and fill Stack/Commands from the real code, and record where the project's spec docs live so architect can ingest them. The brownfield counterpart to scaffold. Run once at onboarding.
version: 1.0
---

## Contract terms — read first

Before anything else, read your slice of the Plumbline contract at **`${CLAUDE_PLUGIN_ROOT}/terms/adopt.md`** — generated from the root `TERMS.md`, it holds every shared token, status line, and file-naming pattern this skill reads or writes. Reproduce them **verbatim**. **If you cannot load it, stop and report; do not guess the contract.**

---

## When to use this skill
- Onboarding an **existing** codebase to Plumbline — real code is already here, but there's no Plumbline structure (`Planning/` + `CLAUDE.md`) yet.
- The brownfield counterpart to `scaffold`. `scaffold` starts an empty project; `adopt` wraps Plumbline around one that already exists.

**Not for greenfield** (use `scaffold`) and **not for a project already on Plumbline** (`Planning/` + `CLAUDE.md` present — just run the normal flow). Run once, at first onboarding.

The guiding rule: **adopt is non-destructive.** It adds Plumbline's own folders and a contract; it never moves, rewrites, or deletes the project's existing code or docs. The project's spec docs stay exactly where they are — adopt only records where they are so `architect` can read them.

---

## What it creates

The same skeleton `scaffold` lays — `Planning/{specs,reference}` + the single `Plumbline/` machinery folder — added *alongside* the existing project. The difference is everything adopt can **fill from the real code** instead of leaving pending:

- **Stack and Commands** — a brownfield project already has a real test command and a stack. adopt detects them and writes them into `CLAUDE.md` (not `[pending — architect]`). This is the whole advantage of adopting over scaffolding: the contract is complete from the start.
- **History mode** — if the root is already a git repo, History is `git`; otherwise ask, defaulting to `git`.
- **Spec source location** — the path(s) where the project's existing spec/requirement/design docs live, recorded for `architect` to ingest.

---

## Step 1 — Confirm this is a brownfield adoption

List the project root and classify it:

- **Already on Plumbline** — `Planning/` and `CLAUDE.md` both present → **stop.** Nothing to adopt; tell the caller to run the normal flow (`architect` for a new feature).
- **Empty / greenfield** — no real source code, no build files → **stop and point at `scaffold`.** adopt is for projects that already have code.
- **Brownfield** — real source code present, but no `Planning/` + `CLAUDE.md` → proceed.

Never overwrite an existing file at any step. If a partial Plumbline structure exists, fill only what's missing.

---

## Step 2 — Locate the project's spec docs

Ask the caller: **where are this project's spec / requirement / design docs stored?** Accept a folder, a glob, or a set of files (e.g. `docs/specs/`, `spec/`, `requirements/`, `README.md`, an ADR folder). If the caller already told you, confirm it exists.

- If the project genuinely has **no** spec docs, record that — `architect` (adapt mode) will then derive specs from the **code alone**, which is weaker (behavior without stated intent). Note it as a risk for the human, don't block on it.
- Do **not** read or rewrite these docs here. adopt only records the location; ingesting them is `architect`'s job in Step 6.

---

## Step 3 — Detect the stack and the real commands

Read the project's own build/config files to learn the stack and, above all, the **real test command** and run/demo command. Do not invent them — a made-up test command poisons every downstream stage. Look at, as they apply:

- **Python** — `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements.txt`, `tox.ini`, `pytest.ini`
- **JS/TS** — `package.json` (`scripts.test`, `scripts.start`)
- **Go** — `go.mod` (`go test ./...`); **Rust** — `Cargo.toml` (`cargo test`); **Ruby** — `Gemfile`, `Rakefile`; **JVM** — `pom.xml`, `build.gradle`
- A `Makefile`, `justfile`, or CI config (`.github/workflows/*`) often names the canonical test invocation

Confirm the test command actually runs if you can. If the stack or test command is ambiguous or you find none, **ask the caller** rather than guessing — this is the one field that must be real.

---

## Step 4 — Lay the skeleton (non-destructive) and init history

Create any missing folders — `Planning/specs/`, `Planning/reference/`, and `Plumbline/{blueprints,decisions,inspect,deviations,surveys,walkthrough,homeowner}` — following the same **What it creates** conventions as `scaffold` (self-labeling `.gitkeep` lines in git mode). Touch nothing that already exists.

**History mode.** If the root is already a git repo, History is `git` — do **not** re-init; the project has its own history. Just add the new skeleton and commit it (message like `Adopt: add Plumbline structure + contract`). If it is not a git repo, ask; default `git` (then `git init` as scaffold does), or `none` if the caller declines git.

---

## Step 5 — Write CLAUDE.md, filled from detection

Create `CLAUDE.md` from **`${CLAUDE_PLUGIN_ROOT}/skills/scaffold/contract-template.md`** (the canonical contract — the same one scaffold uses; do not re-invent it). Unlike scaffold, **fill Stack and Commands from Step 3's detection** — a brownfield project has real ones. Set:

- **Project name / identity** — from the repo (folder name, `package.json` name, `pyproject` name).
- **Shell/OS** — the environment you're running in.
- **Stack** and **Commands** — the detected stack, test command, and run command. Only leave a field `[pending — architect]` if you genuinely could not detect it and the caller couldn't supply it.
- **History Mode** — from Step 4.

If `CLAUDE.md` already exists, append only missing sections — never touch existing content.

---

## Step 6 — Record the handoff (do not invoke architect)

adopt does not write specs, and — like every Plumbline stage — **it never invokes the next stage itself.** Coordination is by convention, not by call: adopt records what architect will need and reports a status; the **caller** (a human, or an orchestrator) runs architect next. Do not spawn a subagent from here.

Record for the handoff:
- the **spec source location** from Step 2 (or "none — derive from code"),
- the project root.

When the caller later runs **architect** in *adapt mode* against that source, architect reads the existing docs and the code as raw material and writes clean Plumbline specs — with tagged `**Done when:**` items — into `Planning/specs/`, leaving the originals untouched as reference. That ingest is what turns a described project into a Plumbline-verifiable one — but it is architect's job, on the caller's turn, not yours.

---

## Step 7 — Report

State:
- what was detected (stack, test command, run command) and what — if anything — was left `[pending]`,
- the spec source location recorded,
- the folders created vs. already present,
- the History mode.

Then tell the caller the next step: **run `architect` in adapt mode** against the recorded spec source to ingest specs into `Planning/specs/`, then `foreman` → `builder` → `inspector` as usual.
