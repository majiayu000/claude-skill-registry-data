---
name: project-init
description: >-
  Setup wizard for an Umbraco package or project. Checks each piece the pipeline relies on
  (solution, CLAUDE.md, .gitignore, memory, plan folders, demo site ports, lint, tests,
  local CMS source and docs clones) and offers to add what's missing, one step at a time.
  Use for a new repo, a repo without CLAUDE.md, or to fill gaps later.
user-invocable: true
argument-hint: [project name, optional]
---

# project-init

Stand up the working files so `feature-explore` and the rest of the pipeline have somewhere
to write. For the Claude-Code-specific layer, you **create structure, not content** — stubs
with headings and decisions to make, never invented decisions. For the solution itself, on a
brand-new package, you don't improvise scaffolding by hand — you defer to a real `dotnet new`
template, the same way you'd defer to a formatter instead of hand-fixing whitespace.

**It runs as a wizard.** Go through the steps below in order. For each one: say what you
found, skip it if it's already there, otherwise ask whether to add it (with the default you'd
pick) and act only on a yes. One question at a time. Re-running the skill later picks up
whatever was skipped, so "not now" is always a fine answer.

| Step | What | Detail |
|---|---|---|
| 1 | Solution | "Step 1: Solution" below |
| 2 | Working files: `CLAUDE.md`, `.gitignore`, README stub, `.claude/memory/`, plan folder | "Step 2: Working files" below |
| 3 | Demo site ports, so worktrees don't collide (only if there's a demo site) | `references/dev-ports.md` |
| 4 | Lint and format | `references/lint.md` |
| 5 | Backend tests | `references/backend-tests.md` |
| 6 | Frontend tests (only if there's a `Client/` frontend) | `references/frontend-tests.md` |
| 7 | End-to-end (e2e) tests | `references/e2e-tests.md` |
| 8 | Local CMS source clone, recorded in `CLAUDE.local.md` | `references/cms-source.md` |
| 9 | Local docs clone, recorded in `CLAUDE.local.md` | `references/docs-source.md` |

## Scope

- IN: for a brand-new package with no solution yet, offering to scaffold the solution itself
  from a real `dotnet new` template (see "Step 1: Solution" below) — **not** hand-rolling a
  solution/test-site yourself. Once there's a solution (whether the template just made one, or
  one already existed): create/update `CLAUDE.md`, `.gitignore`, a `README.md` stub,
  `.claude/memory/`, and the empty `docs/plans/` folder (or whatever path convention the
  interview settles on). Then offer the tooling `feature-build` depends on: per-worktree demo
  site ports, lint and format checks, and backend, frontend and e2e test projects, each set up
  with real tools (`dotnet new`, `npm`) and recorded in `CLAUDE.md`. Last, offer local clones
  of the CMS source and the docs, recorded in the personal `CLAUDE.local.md`.
- OUT: deciding what the project *is* (that's `feature-explore`), architecture
  (`feature-design`), tasks (`feature-plan`). This command does not interview the problem —
  if you're asked "what should this do," stop and point at `feature-explore`. Also out: writing
  solution/project scaffolding by hand — a deterministic template does that job better and
  more consistently than an agent improvising files one at a time.

## Preflight

1. **Re-entrant: if a file already exists, leave it alone.** Report what was already there
   vs. what you created. Never clobber an existing `CLAUDE.md` — if it's missing a section
   this skill would normally add (the plan-folder convention, the pipeline skill list), offer to
   append just that section, and show the diff before writing it.
2. Detect the ground:
   - Code already present → seed `CLAUDE.md` from what's actually there: the CMS version(s)
     targeted (check `Directory.Packages.props` / `.csproj` for an `Umbraco.Cms.Core` package
     reference), the solution/project layout, whether a `Client/` frontend folder exists, the
     test project(s) and their framework. Be factual, no guessing — if something can't be
     detected, leave it `TODO` rather than assuming.
   - Empty dir, and this is a distributable package/add-on (not a single site) → **don't stub
     a solution by hand.** Go to "Step 1: Solution" below first, then come back
     and seed `CLAUDE.md` from what the template generated, the same way as the
     code-already-present branch above.
   - Empty dir, and this genuinely isn't a package (a full Umbraco site, or the template
     doesn't fit — see below) → `CLAUDE.md` gets a stub with the headings below and `TODO`s,
     as before.
   - Regardless of the branch above: detect the trunk branch (`git symbolic-ref
     refs/remotes/origin/HEAD`, falling back to whichever of `main`/`master` exists) and check
     `.claude/settings.json` (project and user level) for an already-configured
     `WorktreeCreate` hook. Both facts go into `CLAUDE.md`'s Feature workflow section — don't
     ask for either unless detection is genuinely ambiguous (e.g. both a default branch and a
     separate long-lived `vN/dev` line exist and it's unclear which one new features should
     branch from).

## Step 1: Solution

Skip this step if a solution (`.slnx` or `.sln`) or project already exists. Otherwise, if
this is a distributable package, ask which way to create the solution. Never install a
template without a yes:

- **`opinionated-package-starter`** (Lotte Pitcher's `dotnet new` template). The default if
  the CMS major it targets fits.
- **The official `Umbraco.Templates`** (`dotnet new umbraco-extension`), for a CMS major the
  starter doesn't cover, or if the user prefers it.
- **Neither**, if the user wants to set it up themselves. Stop the wizard here and pick it up
  on a re-run once a solution exists.

New solutions use the `.slnx` format. If a template creates a `.sln`, offer to convert it
with `dotnet sln migrate`. Leave an existing `.sln` alone unless the user asks.

The starter is the default because it generates the most: the solution, the package project,
a SQLite test site that references the package locally, `Directory.Packages.props`, an
`.editorconfig`, a tag-triggered NuGet release workflow, and doc templates.

1. **Confirm the CMS major this template targets is right for this project.** It follows the
   current Umbraco LTS; check the template's own docs for which major that is, rather than
   assuming. If the
   project needs an older major this template doesn't cover, say so and fall back to the
   official `Umbraco.Templates` package (`dotnet new umbraco-package` / `umbraco-extension`)
   for the base project, then hand-scaffold just the pieces that template doesn't include
   (a test site, `Directory.Packages.props`; `.editorconfig` is step 4) — don't silently
   force a CMS version the project didn't ask for.
2. **Confirm before running** — this creates a whole solution structure, so show the exact
   commands and get a yes first, the same discipline `github-init` uses before creating a
   remote:
   ```bash
   dotnet new install Umbraco.Community.Templates.PackageStarter
   dotnet new umbracopackagestarter -n <PackageName> -an "<Author>" -gu "<GitHubUsername>" -gr "<GitHubRepoName>"
   ```
   From the template's own README — a package id, short name, or parameter can change
   upstream; if `dotnet new install` fails or the short name isn't found,
   check https://github.com/LottePitcher/opinionated-package-starter directly rather than
   retrying the command as-is.
3. Run it, then continue below — seed `CLAUDE.md` from what it just generated (same as the
   "code already present" branch), rather than writing a blank stub.

## Step 2: Working files

### Interview

Almost none. Ask at most:

1. Project name, if not given and not obvious from the folder/solution/`.csproj`.
2. If step 1 is running the `opinionated-package-starter` template: its `-an`/`-gu`/`-gr`
   parameters.
3. The plan-folder path convention (default `docs/plans/<feature-slug>/`, holding `README.md`
   (read-order index), `BRIEF.md`, `ARCHITECTURE.md`, `SPEC.md`, `STORIES.md`, `PLAN.md`,
   `DECISION-LOG.md`, `BUILD-LOG.md` — one file per pipeline phase; offer a
   monorepo/worktree-scoped alternative if the repo already uses worktrees or has more than one
   deployable product in it). Settle the archive path with it (default `docs/archive/`, where
   `feature-close` moves closed plans) and the ideas path (default `docs/ideas/`); don't
   create either folder, the first archive run or idea does.
4. Only if trunk-branch detection above was ambiguous: which branch new features should start
   from and be cut against (see `git-workflow`'s "Branch/worktree per feature" section — this
   is where `feature-build` commits the plan folder and cuts the feature branch/worktree).
5. Only if genuinely ambiguous from the code: which Umbraco CMS major version(s) this targets,
   and whether it ships against SQL Server only or SQL Server + SQLite.

Otherwise stay silent and scaffold.

### Produce

If the `opinionated-package-starter` template just ran, it already produced its own
`.gitignore`, `README.md`, and test site — the re-entrant rule in Preflight means the
templates below won't touch those; they exist for the case where no template was used
(an existing repo, a full site rather than a package, or the template declined/didn't fit).

Copy each template below and fill in its bracketed placeholders from what was detected or
asked in the interview — don't hand-write these from scratch, and don't copy a placeholder
through unfilled:

- **`templates/CLAUDE.md`** → repo root (owned here — re-entrant, append missing sections
  rather than rewrite an existing one).
- **`templates/memory-readme.md`** → `.claude/memory/README.md` (format spec, create once,
  re-entrant).
- **`templates/memory-index.md`** → `.claude/memory/MEMORY.md` (index, create once,
  re-entrant).
- **`templates/project.gitignore`** → `.gitignore`. .NET + (if a frontend exists) Node
  hybrid — the shape real Umbraco product repos actually use, not a hand-picked shortlist.
  Trim the frontend section if this repo doesn't have one. **Don't** add Umbraco runtime
  folders like `App_Data/` or `umbraco/Logs/` by default — a package repo doesn't run Umbraco
  directly, a generated demo site does (already covered by `demos/` in the template). Only add
  them if this repo genuinely *is* a full Umbraco site, not a package. **If this repo is a
  meta/aggregator repo** (a monorepo of pointers to separately-versioned sub-projects), use an
  allowlist-style `.gitignore` (`*` at the top, then `!path/to/each/real/thing`) instead of
  this denylist template.
- **`templates/README.md`** → repo root `README.md` — one-line stub only, owned by a future
  `umbraco-document`-equivalent once one exists; don't write a full README here, that's not
  this skill's job.

**`docs/plans/`** (or the agreed path) — create the empty folder with a `.gitkeep` if the
convention is a fresh folder, so the path exists before the first feature needs it. Don't
pre-create a per-feature subfolder or any of its eight files — `feature-explore` creates
`docs/plans/<feature-slug>/`, its own `BRIEF.md`, and the folder's `README.md` index when the
first real feature starts.

## Steps 3 to 9: Ports, lint, format, tests, CMS source and docs

Each step has its own reference file with what to detect, the default to offer, and how to
set it up. Read only the one for the step you're on. The same rules apply to all of them:

- **Detect first.** If the project already has a tool for this (a linter, a test framework),
  keep it. The defaults are only for a project that has nothing yet.
- **Match the CMS.** The defaults follow what Umbraco CMS itself uses, so Umbraco's own test
  helpers and examples work. Helper package versions match the CMS version the project
  targets (`umbraco-dependencies`' "Which CMS version: the floor").
- **Install, don't hand-write.** Use `dotnet new`, `dotnet add package` and `npm install` so
  versions come from the real feeds. Let them pick the current versions, then pin only where
  the CMS version requires it.
- **No sample tests.** Set up the project and check it builds and runs. Real tests come from
  `bdd-specs` when a feature needs them.
- **Record the commands.** Put each working command in `CLAUDE.md`'s "Build & test" section.
  The `builder`, `reviewer` and `feature-build` smoke step read them from there. Steps 8 and
  9 are the exception: a clone's path is personal, so it goes in `CLAUDE.local.md` instead.
- **Commit nothing.** Leave the changes for the user to review, like every other file this
  skill creates.

## Hand off

End with one line per step (found, added, or skipped), the file list (created vs. skipped vs.
appended-to), the plan-folder path convention settled on, then:
`Suggested next: feature-explore — to define the first feature.`
