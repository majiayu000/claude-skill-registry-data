---
name: write-examples
description: >-
  Load this skill when writing runnable example programs under examples/: a feature tour and
  copy-paste recipes, each run before it is kept. Trigger on "write examples for this project", "add
  usage examples", "the examples are missing or broken".
argument-hint: "[project-path]"
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Runs every example with the target project's own runtime and package manager (Python with its
  venv or uv, Node or Bun, cargo, go, …) and needs whatever services the examples call (a local
  server, a database). Without the runtime the examples are still written but reported as not run.
  Recipes with their own dependencies need network access to fetch them into a throwaway
  environment (`uv run --with`, `bunx`, a temp venv).
license: Apache-2.0
---

# Write Examples

An example has two readers, and they want opposite things:

- **The newcomer** wants to see, in a few minutes, what the project does and how its most important
  features feel to use. They read the example, run it, and read the output.
- **The integrator** already chose the project and is wiring it into their own app, service, or
  script. They want a block they can copy whole, change two values in, and trust.

One file cannot serve both well: a tour stays short by skipping error handling and configuration,
and a recipe earns its trust by including exactly those. So this skill writes two tracks under
`<root>/examples/` and never mixes them in one file. Every file is **run before it is kept**. An
example that does not run is worse than none: it is the first thing a new user copies.

## Procedure

### 1. Resolve the target

- **A path was given** (skill argument or in the request): that directory is `<root>`. Confirm it
  holds a project (a manifest such as `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, or
  a source tree).
- **No path given:** `<root>` is the current working directory.

If `<root>/examples/` already exists, read it first. Fix what is broken and add only what is
missing. Never move or rename an existing example that runs: READMEs, docs, and issues link to
those paths. List it in the index under the track it fits, and put only new files in the layout
below. Never delete a user's example without listing it in the report.

### 2. Survey the public surface

Examples use the project the way an outsider does, so learn the outsider's view first:

| Question                                                                 | Where to look                                                                               |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| What kind of project is it: library, CLI, HTTP API, SDK, service?        | Manifest, entry points, `bin`/`scripts`, route definitions                                  |
| What is the public import path or command name, and how is it installed? | Package name in the manifest, `__init__`/`index` exports, README install line               |
| Which features matter most?                                              | README feature list, docs quickstart, the most-tested public functions, CLI subcommands     |
| What does a caller have to configure?                                    | Constructor parameters, env vars read (`.env.example`, settings code), required credentials |
| What fails in normal use and how does the caller see it?                 | Public exception or error types, HTTP error bodies, CLI exit codes                          |
| How does the project's own code call itself?                             | Tests that exercise the public API: the most reliable source of correct, current usage      |

Rank the features. **The tour gets the top three to five**, chosen by how many users need them, not
by how interesting they are to build. A feature that almost every user touches (create the client,
make the core call, read the result) outranks a clever advanced one.

### 3. Plan the two tracks

Write the plan as a short table before any code: file, track, the feature or integration it shows,
and the one line it will print. Then write the files.

```text
examples/
├── README.md                 # index: both tracks, how to run, what each file shows
├── tour/
│   ├── 01-<first-result>.<ext>    # shortest path to a first working result
│   ├── 02-<core-feature>.<ext>
│   └── 03-<core-feature>.<ext>
└── recipes/
    ├── <integration-name>.<ext>   # one integration scenario per file
    └── ...
```

Use the project's language and file extension. A CLI project writes shell scripts. An HTTP API
writes `curl` scripts plus one client in the language its users most likely use. If the ecosystem
lays examples out differently by convention (Rust's flat `examples/*.rs` run by
`cargo run --example`, Go's one `package main` per `examples/<name>/` directory), follow the
convention and keep the two tracks as a name prefix (`tour_01_...`, `recipe_...`) instead of
subfolders. Examples are programs, not tests: do not write them as Go `Example*` functions or
doctests, because a user must be able to run and copy each one as a standalone program.

**Examples run against the working tree, but integrators install the latest release.** Compare the
public surface the examples use against the latest release tag
(`git -C <root> describe --tags --abbrev=0`, then the changelog). If an example relies on something
unreleased, say so at its top and in the index, so nobody copies code their installed version
cannot run.

### 4. Write the tour

The tour answers "what does this do, and what does it feel like to use?" in as few lines as
possible.

- **One feature per file, numbered in reading order.** `01` is always the shortest path to a first
  working result. Each later file assumes only what an earlier file showed.
- **Twenty to forty lines each.** If a feature needs more, it is two features or a recipe.
- **Default everything.** No options beyond what the feature needs to run. Each skipped option is
  something the reader can find in the reference, not something they have to understand now.
- **Print what matters.** The output is half the lesson: print the result in a form that shows what
  happened (`created user usr_abc123`), not a raw object repr.
- **One comment per non-obvious step, explaining why, not what.** A tour is read more than run.
- **No setup the reader cannot see.** If the example needs a running server or a sample file, the
  file creates it or the first lines say exactly how to start it.

### 5. Write the recipes

A recipe answers "how do I put this in my own project?" The test for every line: **would the
integrator have to change it or add to it before it is safe to ship?** If yes, fix the recipe.

- **Self-contained.** It imports only the project's public path and the standard library, or
  dependencies the recipe declares in a header comment with an install line. Never import from the
  repo's internals, test helpers, or other example files.
- **Configuration from the environment, never hard-coded.** Read secrets and endpoints from env
  vars with the names the project documents. Fail with a clear message when one is missing. A
  project that takes no secrets or endpoints skips this rule. Do not invent env vars for it.
- **Handle the failures the project really raises.** Catch the project's public error types at the
  boundary and show the one sensible response (retry, log and skip, return an error). Never a bare
  catch-all that swallows the error. A project with no failure mode worth handling skips this rule.
- **Clean up.** Close clients, connections, and files the way the project intends (context manager,
  `defer`, `finally`, `using`).
- **Shaped like the caller's code, not a script.** Put the integration in a function or class the
  user can lift out whole, with a small `main` guard below it that runs it. The lifted part must
  not depend on the guard. A recipe that is config rather than code (a CI step, a compose service,
  a shell alias) is instead the complete block to paste, with nothing around it.
- **Marked edit points.** Every value the integrator is expected to change carries a comment:
  `# change: your bucket name`. There are few of them. If there are more than three, the recipe is
  doing too much.
- **Scenario-named.** Name files after what the user is building (`retry-on-rate-limit`,
  `fastapi-dependency`, `ci-step`, `batch-import-from-csv`), never after the API they call.

Pick recipes from the integrations the survey found: the frameworks the project mentions, the
callers its own tests simulate, the questions in issues or the README FAQ. Three to six is typical.
A recipe no real user would need is a tour step or nothing.

### 6. Run every example

Run each file exactly the way `examples/README.md` will tell the reader to, from a clean shell in
`<root>`, using the project's own toolchain (`uv run`, `bun run`, `cargo run --example`, `go run`,
`bash`). Capture the output. Then act on the result:

- **It ran and printed what the file claims:** keep it. Put its real output in the README, with
  values that change on every run (IDs, timestamps, durations) shown as they printed once and noted
  as varying. Never show a secret the run printed.
- **It failed:** fix the example, never the project. If the failure reveals a real bug in the
  project, stop editing that example, keep it out of the README, and report the bug.
- **It cannot run here** (needs paid credentials, an external service, hardware): keep it only if
  it is a recipe the survey showed users need. Mark it in the README as `not run: <reason>` and
  list it in the report. A tour example that cannot run is cut. The tour exists to be run.
- **Output that is not text** (a UI, an image, a written file): check the program exits cleanly and
  the artifact exists or builds, and say in the report how you checked it. You cannot confirm it
  looks right.

### 7. Write `examples/README.md`

The index is the page a new user opens first, so it states the order and the one command per file:

````markdown
# Examples

<One sentence: what these show and the version or commit they were run against.>

## Setup

```bash
<the one install or sync command>
```

## Tour — learn the main features in order

| File                                            | Shows                                   | Run                                        |
| ----------------------------------------------- | --------------------------------------- | ------------------------------------------ |
| [01-first-request.py](tour/01-first-request.py) | Create a client and make the first call | `uv run examples/tour/01-first-request.py` |

## Recipes — copy into your own project

| File                                                     | Use it when                      | Change            |
| -------------------------------------------------------- | -------------------------------- | ----------------- |
| [retry-on-rate-limit.py](recipes/retry-on-rate-limit.py) | Your app calls the API in a loop | `API_KEY` env var |
````

A table cell cannot hold a code block, so put tour output after the tables, in an `## Output`
section with one `###` heading per file and its output in a `text` block. If the project has a
`docs/` set, link from `examples/README.md` to it.

## Rules

- **Never change the project to run an example.** A recipe's extra dependencies (a web framework,
  an HTTP client) go into a throwaway environment: `uv run --with <pkg>`, `bunx`, a temp venv.
  Never add them to the project's manifest or lockfile: integrators install the released project,
  so an example that needs project edits misleads them.
- **Never run against production or a real account.** An example that writes, deletes, sends, or
  bills runs only against a local or test instance. Start it yourself if the project can run one
  (the dev server, a compose file) and stop it afterwards. If the only reachable target is live, do
  not run the example. It counts as cannot run here.
- Keep the example files free of generated output, and never commit secrets used to run them.
- Never mix the tour and recipe tracks in one file.

## Output

Files under `<root>/examples/` in the layout of step 3. End with a table of every example file:
track, what it shows, and whether it ran (`ran`, `not run: <reason>`, `cut: <reason>`). After it,
list anything the user must act on: project bugs found, examples that need credentials to verify,
and pre-existing examples changed or left alone.

## Stop conditions

- The given path holds no project → stop and say so. Never write examples for the workspace
  instead.
- A failing example reveals a real bug in the project → stop editing that example and report the
  bug.

## Hands off to

- Leave documenting the examples in `docs/` to `ceh-documentation:write-project-docs`, which picks
  them up from `examples/`.
