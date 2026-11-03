---
name: project-stamp
description: >-
  Scaffold a new managed project inside a kensaiapp instance — create the
  per-project folder tree system/projects/<name>/ (project.md with the Product
  path binding, agari.md, doctrine/, contexts/CONTEXT_PM.md, and the journey/ folders
  nemawashi/ (README + the recommended define-the-product seed + unpicked/ + trail/ + drop/),
  shukuba/ (README + parked/ + trail/), tobiishi/trail/) stamped from the core templates, per
  kensaiapp_structure.md §2. Use this whenever the user wants to start,
  register, scaffold, or set up a new project / product engagement in this
  instance — even if they just say "add a project" or "onboard <product>". It
  is the step that comes BEFORE the CPO session (which authors the PRD and declares the product's
  "done"); this creates the management folder that points at the product. Does
  NOT create the product's docs or code. Do not use for: declaring the product's
  Agari (project-agari), running a change through the pipeline (the chain), or
  first-time instance setup (setup-kensaiapp).
license: MIT
metadata:
  author: Eyal Golan
  category: kensaiapp-setup
  version: "1.15.1"
  created: "2026-07-04"
  risk: safe
  tags: kensaiapp, project, scaffold, setup, structure
---

# project-stamp

Create a new **managed project** — the `system/projects/<name>/` folder that
kensaiapp uses to steer one product through its journey. This is the per-project
slice of the instance structure manifest (`<CORE>/doctrine/setup/kensaiapp_structure.md`,
section **§2. Per-project**). A deterministic helper script does the stamping;
your job is to gather the four inputs and confirm the result.

## Posture

**Role-agnostic, and first.** Scaffolding is plain machinery — it runs in **any**
session, with **no `<role>:` prefix, no loader, no posture** required. Do not adopt a
role to run it, and don't require one; if a session already carries a role (`cpo:` or
otherwise), that's fine, but scaffolding itself is role-free. Its commits are
`Role: Meta`.

It is the **first** step when starting a new project — it comes **before** all product
and role work: before the CPO authors the PRD or declares the Agari, before the PM
opens the journey, before the change pipeline. Nothing about the product's *content* is
decided here; this only creates the folder everything else hangs off. The single
thing that must exist first is the **instance** itself (via `setup-kensaiapp`);
scaffolding a project assumes that's already done. Full flow:
`<CORE>/doctrine/setup/setting_up_a_project.md`.

## What it creates (and what it must not)

Creates, under `system/projects/<name>/`:

```
project.md                       # the load-bearing "Product path:" binding + execution fields
agari.md                         # 上がり — the product's "done" (a declaration, filled later)
doctrine/<name>_doctrine.md         # this project's domain doctrine (stub)
doctrine/ai_responsibility.md       # AI-vs-mechanical boundary for this project (scope = <name>)
journey/nemawashi/README.md         # 根回し — seedbed (folder, one file per idea)
journey/nemawashi/<date>_define-the-product.md  # 根回し — the recommended definition chain, as a seed
journey/nemawashi/unpicked/.gitkeep # 根回し — the candidate pool, empty for a newborn seedbed
journey/nemawashi/trail/.gitkeep    # 根回し — walked-ideas bin (empty)
journey/nemawashi/drop/.gitkeep     # 根回し — killed-ideas bin (empty)
journey/shukuba/README.md           # 宿場 — current station (folder)
journey/shukuba/parked/.gitkeep     # 宿場 — set-down-unreached bin (empty)
journey/shukuba/trail/.gitkeep      # 宿場 — reached-stations bin (empty)
journey/tobiishi/trail/.gitkeep     # 飛び石 crossed-stones bin (empty; active stones are pipeline-authored)
contexts/CONTEXT_PM.md              # the PM's per-project context — a placeholder; the change lifecycle writes it
```

It must **not** create the product's docs or any product code. Those live **with the
product** (manifest §3) and are authored later — never by scaffolding. The project
folder only *points at* the product, by the `Product path:` field.

**The setup seed is a recommendation, not a commitment.** It carries the sequence a
product is defined by as a station checklist, so the seedbed is never empty and the
chain is never re-derived from memory. The stations, their order, and which of them
are runnable today are
`<CORE>/doctrine/setup/setting_up_a_project.md` § "The flow at a glance" — read them
there rather than from this file, which does not own them. The seed is stamped every
time; the owner is free to edit, reorder, or delete it if this product starts
somewhere else. Say that plainly when you show the tree.

All files are stamped from `<CORE>/templates/` (the `<CORE>` token is resolved by
the `resolve_core.py` session hook; the script reads the same `CORE` value).

## Inputs to gather

Ask for what you don't already know. Lead with a recommendation where there's a
sensible default; only the first two are truly required.

1. **Project name / slug** — the folder name under `system/projects/`. Kebab-case,
   no slashes. This also becomes the package slug and the domain-doctrine filename
   (`doctrine/<name>_doctrine.md`).
2. **Placement — internal or external?** This is the *intent* question, and it's the
   one that matters. Ask it in these terms, not in path-shape terms:
   - **internal** → the product lives *inside this instance*. You need no path from
     the user — it defaults to `products/<name>`. (Under the hood this is a relative
     `Product path:`; no directory grant needed.)
   - **external** → the product lives in *its own repo*. Ask **where** — the absolute
     path to that repo. This is the only case that needs a path from the user, and it
     also gets the Claude Code directory grant (see below).

   So: ask internal-or-external first; only when they say **external** do you ask for
   the path. Don't lead with "relative or absolute" — that's the mechanism, not the
   intent. If they say external, ask for the location; don't guess where their repo is.
3. **Execution type** — `headless` (default, `claude -p`) or `docker` (sandboxed runs).
4. **Test command** — default `pytest tests/`. For a product validated another way
   (e.g. a skills product uses `skill-evals`), set it accordingly. For a product with no code
   (only documents), set `none`, since a product with no suite has nothing to run. Where that is not known
   yet, keep the default: `product-card` re-derives the command once the product's documents settle.

## Run it

From the instance root, invoke the scaffolder. `CORE` is already exported into the
shell by the session hook, so the script resolves `<CORE>/templates/` on its own;
pass `--core "$CORE"` explicitly only if you want to be certain.

```bash
# internal — product lives in this instance; path defaults to products/<name>
python3 <CORE>/../skills/interactive-product/.claude/skills/project-stamp/scripts/stamp_project.py <name> \
  --placement internal \
  --execution-type headless --test-command "pytest tests/"

# external — product in its own repo; pass its absolute path
python3 <CORE>/../skills/interactive-product/.claude/skills/project-stamp/scripts/stamp_project.py <name> \
  --placement external --product-path /abs/path/to/product-repo \
  --execution-type headless --test-command "pytest tests/"
```

`--placement` is required — it's the intent you established in the interview. For
`internal`, `--product-path` is optional and defaults to `products/<name>`; for
`external` it's required and must be absolute. The script guards the mismatches
(internal-with-absolute, external-with-relative, external-without-path) with a clear
message (exit 2).

Three more flags fill card lines the interview above does not ask for, and default when omitted:
`--type software|no-code` (default `software`), `--manages "<what>"` (default `none`) and
`--source-material "<line>"` (default `<blank>`). `project-setup` passes all three from its own
interview; a plain stamp can leave them out. The card's `Definition:` line follows from `--type` —
`full` for software, `prd-agari` for no-code — unless `--definition full|prd-agari|none` names it.

The script is **create-if-missing, never overwrite**: if `system/projects/<name>/`
already exists it stops and changes nothing (exit 3). On success it prints the
resolved `<CORE>` and every file it created.

### External products: the directory grant is set automatically

When placement is **external** (the product lives in its own repo), the script
also derives the Claude Code **directory grant** so the pipeline can reach that
repo: it adds the path to `permissions.additionalDirectories` in
`.claude/settings.local.json` (host-local, **gitignored, never committed**). This
is a **merge** — it never clobbers your `allow` list or other keys, creates the
file/key if absent, and is a no-op if the grant is already there. This mirrors the
single-source rule the `setup-kensaiapp` audit uses: `project.md Product path:` is
the source, `additionalDirectories` is the derived grant.

An **internal** product (relative path) needs no grant — the script says so and
skips it. If `settings.local.json` exists but isn't valid JSON, the script warns
and leaves it untouched rather than risk clobbering your overrides — add the grant
by hand in that case.

Because the grant is machine-local, note it in your closing summary so the user
knows a `settings.local.json` change happened (it won't show in `git status`).

### External products: must be a git repo

An external product lives in **its own git repo** — the two-repo
pipeline (routed by `<CORE>/tools/development_path.py`) cuts worktrees and branches there, and the PRD lands
there as its first commit. The scaffolder **checks the product path** and prints a
status line: `product repo OK` if it's already a repo, or
`WARNING: … Run: git init …` if it isn't. Scaffolding the *pointer* still succeeds
either way (the pointer lives in the instance repo) — the check is non-fatal. But
before the CPO authors the PRD, the product path must be a git repo: if the warning
fires, `git init <product-path>` (or have the owner do it), then proceed.

## After scaffolding

1. Show the user the created tree (the script's output is enough).
2. State the next step plainly: **station 1 of the setup seed**, which is a `cpo:`
   session authoring the PRD (`product-prd` → `<product>/docs/PRD.md`), run through
   `<CORE>/launchers/skill/launcher.sh product-prd <name>`. Say that the seed is
   there, that its stations are the recommended path, and that it can be edited
   or deleted. Point the user at `<CORE>/doctrine/setup/setting_up_a_project.md` for
   the full flow, and flag that `agari.md` is a placeholder waiting on station 2.
3. **External product — check the git-repo status line.** If the scaffolder warned
   that the product path isn't a git repo, `git init` it (or have the owner do it)
   before the CPO step — the PRD needs somewhere to commit.
4. **Committing is the user's call** (interactive). Offer to commit the new
   `system/projects/<name>/` folder; don't commit unprompted.

## Reference files

- `scripts/stamp_project.py` — the deterministic scaffolder (stdlib-only). Reads
  the templates, substitutes, writes the §2 tree, guards against overwrite.
