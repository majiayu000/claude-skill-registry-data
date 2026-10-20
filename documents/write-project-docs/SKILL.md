---
name: write-project-docs
description: >-
  Load this skill when writing a complete docs set under docs/: quickstart, guides, concepts, API
  reference, examples, troubleshooting. Trigger on "document this project", "write the docs for
  this library", "build out the docs folder". Not for a README refresh.
argument-hint: "[project-path]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Reads the target project's files and, when present, its git history through the git CLI on PATH
  (`git -C <root> log`, `git tag`). Without git or without history it still runs: "Added in"
  markers come from CHANGELOG.md alone, and commit-sourced design rationale is skipped. Checking
  samples needs the project's own runtime (Python and venv, Node, …); without it samples are marked
  not run. Writes Markdown only and installs no docs framework.
license: Apache-2.0
---

# Write Project Docs

Produce a docs set that a newcomer can use in five minutes and an experienced user can mine for
every feature and the reason behind it. The balance does not come from trimming words. It comes
from **giving every page exactly one job**, so each page can go to its own extreme: the quickstart
as short as possible, the reference as complete as possible, the concepts as deep as needed.

This skill owns the target, the survey, the page plan, the front pages, and the final link pass.
Every other page type is delegated to the skill that owns it. Every page, whoever writes it,
follows `${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` ("the standard" below). Read it before
step 3. Each delegated skill reads the same file.

## Procedure

### 1. Resolve the target

- **A path was given** (skill argument or in the request): that directory is `<root>`. Resolve it
  to an absolute path and confirm it exists and holds a project (a manifest such as
  `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, or a source tree).
- **No path given:** `<root>` is the current working directory.

Every read is from `<root>`. Every git command is `git -C <root> …`. Every write goes under
`<root>/docs/`, plus the one README link in step 6 and the docs framework's nav config. Nothing is
written into the workspace the agent happens to be running in when `<root>` is somewhere else.

Checking a sample must not leave files behind in `<root>`. Install from a copy of `<root>` into a
scratch environment: a virtualenv for Python, a scratch project running `npm install <copy>` for
Node, given its own `package.json` first (`npm init -y`) so npm does not walk up and install into a
parent directory. Delete the copy afterwards. Never leave `build/`, `*.egg-info`, `node_modules/`,
a lockfile, or a cache directory in `<root>`.

### 2. Survey

Read before planning. Record the answers in a survey table in the session. The table stays in the
conversation: pass `<root>` as the argument to each delegated skill, which reads audience, scope,
prerequisites, and sources from the table instead of re-deriving them.

| Question                                                                                            | Where to look                                                                                    |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| What kind of project? (library, CLI, HTTP API / SaaS, service, app)                                 | Manifest, entry points, route files, `Dockerfile`                                                |
| Who reads the docs, and which audience is primary? (callers, operators, contributors)               | The request, the project kind, deploy files                                                      |
| What is the public surface, roughly how big?                                                        | Package exports, routes, CLI definitions, env reads — `write-api-reference` does the exact count |
| How is it installed and run? What must a reader have first (runtime versions, access, credentials)? | Manifest, README, `Makefile`, CI config, `.env.example`, auth code                               |
| What does a first working result look like?                                                         | README, `examples/`, the simplest test that exercises the public API                             |
| What are the core ideas a user must hold?                                                           | Public class and type names, repeated terms in docstrings and errors                             |
| Where does design rationale live?                                                                   | ADRs, `ARCHITECTURE.md`, decision logs, PR/commit bodies, `CHANGELOG.md`                         |
| Release history?                                                                                    | `git -C <root> tag --sort=-creatordate`, `CHANGELOG.md`                                          |
| What docs exist already, and is a docs framework configured?                                        | `docs/`, `mkdocs.yml`, `conf.py`, `docusaurus.config.*`, `astro.config.*`                        |
| Known limitations and failure modes?                                                                | Raised errors, `TODO`/`NotImplementedError`, issue templates, README caveats                     |

### 3. Plan the page set

Map the survey onto the layout of standard §1, annotated here with who writes what. **Cut every
page that has no real content**: no `migration.md` without a breaking release in history, no
`examples/` without a runnable example, no `operations/` for a library. A design record under
`docs/` (ADRs, decision logs) stays where it is and is linked, not restyled (standard §1). An empty
section costs the reader a click and trust.

```text
docs/
├── index.md          # front page: what it is, one code sample, where to go next  (this skill)
├── why.md            # why X, X vs alternatives, when NOT to use it, limitations   (this skill)
├── guide/            # getting-started (the quickstart), how-to/, troubleshooting
│                     #                                           (write-guides-and-runbooks)
├── operations/       # the operator's runbook, OP-NN pages       (write-guides-and-runbooks)
├── concepts/         # the mental model + why it is built this way   (write-concept-docs)
├── reference/        # every public item, exhaustively               (write-api-reference)
├── examples/         # complete runnable programs, EX-NN-<name>.md   (this skill)
└── migration.md      # per-major-version upgrade steps               (this skill)
```

Write the plan as a table, **Page | Mode | The one question it answers | Source**, and hold it in
the session. Modes are the seven names of standard §2. A page that needs two modes is two pages. A
page whose question you cannot state in one line is not planned yet.

**Existing docs:** edit in place and fill gaps. Map each existing page to a mode, keep its path,
and add only the missing pages. Never relocate or duplicate existing pages into the layout above.
When a docs framework is configured, add every new page to its nav config (`nav:` in `mkdocs.yml`,
`sidebars.*`, `toctree`) in the same pass.

### 4. Run the pipeline

Run in order. Reference comes first because every other page links into it. The front pages come
last because they link to everything. Links to pages planned but not yet written are fine along the
way: step 6 checks them. Each delegated skill returns its rows and open items instead of its own
report, and this skill merges them into the one report at the end.

| #   | Pages                                 | Delegate to                                                                                                                        | Gate before next step                                                                        |
| --- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1   | `docs/reference/`                     | Invoke the Skill tool with skill="ceh-documentation:write-api-reference" — pass `<root>` and the survey table                      | Every surface item counted in its coverage check has an entry, or is listed as an open item  |
| 2   | `docs/concepts/`                      | Invoke the Skill tool with skill="ceh-documentation:write-concept-docs" — pass `<root>`, the survey table, the reference page list | Each concept page has a "Why it works this way" section with a cited source, or an open item |
| 3   | `docs/guide/`, `docs/operations/`     | Invoke the Skill tool with skill="ceh-documentation:write-guides-and-runbooks" — pass `<root>`, the audience, and the brief below  | Getting-started reaches a working result; every how-to ends in a verify step                 |
| 4   | `docs/examples/`, `docs/migration.md` | this skill — see below                                                                                                             | Each example ran, and its shown output is what it printed                                    |
| 5   | `docs/why.md`, `docs/index.md`        | this skill — see step 5                                                                                                            | Index links every section; no page unreachable from it                                       |
| 6   | Link pass                             | this skill — see step 6                                                                                                            | Zero broken relative links                                                                   |

**Brief for `write-guides-and-runbooks`:** its `docs/guide/` and `docs/operations/` mean
`<root>/docs/guide/` and `<root>/docs/operations/`. Write `operations/` only when the project is
deployed and operated, never for a library. Its `getting-started.md` _is_ the site quickstart: the
shortest path to a first working result for the **primary audience** (for a library, install to
first call; for a hosted API, the caller's first request, not the server install), at most 7 steps,
no options, each optional knob replaced by a link to its reference entry. The system overview and
the settings list are not guide pages here: they live in `concepts/` and
`reference/configuration.md`. How-to pages cover the tasks from the survey, show the handful of
options that task needs, and link to `docs/reference/` for the rest. Troubleshooting entries are
headed by the literal error text a user will search for, each linking to the error's reference
entry, or to the reference entry of the input that causes it. A term that needs explaining links to
its concept page instead of explaining it inline.

**Examples:** only programs that already exist in the repo (`examples/`, runnable snippets from
tests) and that you ran successfully. An example that did not run is cut, not marked. This skill
never writes new example programs. When the repo has none worth a page, skip `examples/` and add an
open item telling the user to run `/ceh-documentation:write-examples` (a feature tour plus
copy-paste recipes under `<root>/examples/`), then rerun this step. Do not invoke it yourself. Each
page:

```text
# EX-01 — <What it builds>
[← Examples](index.md)
<One line: what the program does and which feature it shows.>
## Code        — the full program, one fenced block
## Run it      — the command, then Expected output
## Draws on    — bullets linking the guide and reference pages it uses
---
<footer>
```

Name each page `examples/EX-NN-<name>.md`, with an `examples/index.md` hub. A single example folds
into a how-to instead.

**Migration:** one section per **breaking release**, newest first: a major version, a release the
changelog or a commit marks breaking (`BREAKING`, `!:`), or, before 1.0, a minor version whose
changes make existing calls fail or return different results. A post-1.0 minor that changes output
without being marked breaking gets a `_Changed in <version>: …_` marker and a concept-page note,
not a migration section. A release that only added things gets nothing here. Each section gives
what broke, the before/after code, and the "why" link to its concept or decision. Link
`CHANGELOG.md` for everything smaller. Never copy the changelog into the docs.

### 5. Write the front pages

`docs/index.md` fits on one screen. Its code sample is copied from getting-started and must run on
its own: inline placeholder values (`<your-api-key>`) instead of variables set in an earlier step.
When one already exists, merge into this shape: keep its sentences that are still true, and add a
route line for every extra audience (a "**Deploying it?**" line for operators). Drop every link
whose target was cut, and every line left with no link. A section written as one file links to that
file (`concepts.md`, not `concepts/index.md`):

````markdown
# <Project>

<One sentence: what it is and who it is for.>

```<lang>
<the smallest real usage — 10 lines or fewer, copied from getting-started>
```

- **New here?** [Get started](guide/getting-started.md) — a working result in minutes.
- **Doing a specific task?** [Guides](guide/index.md)
- **Deploying or operating it?** [Operations](operations/index.md)
- **Want to understand how it works and why?** [Concepts](concepts/index.md)
- **Looking up a function, flag, or setting?** [Reference](reference/index.md)
- **Want a whole working program?** [Examples](examples/index.md)
- **Choosing between tools?** [Why <Project>](why.md)
- **Upgrading?** [Migration](migration.md) · [Changelog](link)
````

`docs/index.md` has no breadcrumb. `docs/why.md` and `docs/migration.md` open with
`[← Docs home](index.md)`. Once `docs/index.md` exists, give every section hub its
`[← Docs home](../index.md)` breadcrumb (standard §4).

`docs/why.md` is for someone deciding whether to adopt: the problem it solves, what it does
differently (link the concept page carrying each claim), a comparison with named alternatives only
where the repo or its docs make the comparison, **when not to use it**, and **Known limitations**
with the workaround where one exists. Claims come from the code and the survey, never from
marketing adjectives.

### 6. Run the link pass and consistency check

- Every page is reachable from `docs/index.md` in at most two clicks (design records under `docs/`
  excepted: they hang off the concept pages that cite them).
- Every relative link resolves to a file that exists, and every `#anchor` to a heading that exists
  (standard §6). Check mechanically, not by eye: list every link target ending in `.md` and test
  that the file and heading exist.
- Every page follows the anatomy of standard §4, whichever skill wrote it. The pass is where drift
  between skills gets caught.
- An idea is explained once, in its home mode, and linked everywhere else. Collapse any second
  explanation into a link.
- One term per concept across every page. The reference name wins when two pages disagree.
- Code samples are copied from something that ran, or marked `[VERIFY: …]`.

Then add one line to `<root>/README.md`, directly under its title and tagline, unless it already
links the docs: `Documentation: [docs/index.md](docs/index.md)`. Make this edit here rather than
through a README-maintenance skill: those gate on code changes and diff the last commit, neither of
which fits a docs-only change. The README stays the storefront, the docs are the manual.

## Page budgets

| Page                       | Budget                                      | Why                                                       |
| -------------------------- | ------------------------------------------- | --------------------------------------------------------- |
| `index.md`                 | One screen                                  | It routes; it does not teach                              |
| `guide/getting-started.md` | At most 7 steps, zero options               | Every option is a place to stall                          |
| How-to page                | One task, ≤ 2 screens                       | Longer means two tasks                                    |
| Concept page               | ≤ 2 screens                                 | Longer means two concepts                                 |
| Reference page             | Unbounded, but one module/resource per page | Completeness is its job; findability comes from structure |

## Rules

- **Never invent.** Every command, flag, default, signature, and rationale comes from the code, its
  history, or a design record. Anything unverified is marked `[VERIFY: …]` in place and listed
  under **Open items** in the report.
- **Markdown only.** Do not install or configure a docs generator. If none is configured, name the
  fitting one for the stack in the report (MkDocs or Sphinx for Python, Starlight or Docusaurus for
  TypeScript, an OpenAPI renderer for HTTP APIs): the Markdown written here is its input.
- **Stay inside `<root>/docs/`**, plus the one README link and the docs framework's nav config.
- **Do not commit.** The caller decides what lands. If the environment requires a branch before
  editing, create one; still do not commit.

## Output

End with the report of `${CLAUDE_PLUGIN_ROOT}/references/docs-standard.md` §10, covering every page
in the set, the delegated skills' rows merged in: one report for the whole run. Put three lines
above the table: pages written / updated / cut, the reference coverage line in the form of standard
§10, and a generator recommendation when no reference generator is wired into the docs build.

## Stop conditions

- The given path does not exist or holds no project → stop and say so. Never document the current
  workspace in its place.

## Hands off to

- Invoke the Skill tool with skill="ceh-documentation:write-api-reference" to write
  `docs/reference/` (pipeline row 1).
- Invoke the Skill tool with skill="ceh-documentation:write-concept-docs" to write `docs/concepts/`
  (pipeline row 2).
- Invoke the Skill tool with skill="ceh-documentation:write-guides-and-runbooks" to write
  `docs/guide/` and `docs/operations/` (pipeline row 3).
- New example programs belong to `/ceh-documentation:write-examples`, which the user runs. This
  skill only reports the gap.
