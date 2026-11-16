---
name: python-workspace
description: Use when several Python distributions live in one repository — creating the workspace root, or admitting a member to it. Covers the root project as a container with no runtime code of its own, the shared-library versus runnable-member split, the two-sentence admission test a new member passes, in-repository dependency edges the packaging tool resolves rather than path hacks, tooling values settled once at the root, one container profile per runnable member, and the task-runner targets that sync every member, type-check and test each member from its own directory, apply migrations where members share a store, and launch each member from its own directory. Everything here is about members, never about what is inside one, so a member of any internal layout needs the same root. One distribution on its own needs none of it; a member's own layout and data access belong to that member's architecture skills, and whether a proposed member is a boundary at all is `coupling`. - Also when asked for a monorepo, a uv workspace, a `packages/` and `services/` layout, a root `Makefile` target, or a `docker compose` profile per runnable member.
---

# Workspace — the root for several distributions in one repository

One-shot bootstrap for a repository holding several distributions: the runnable ones plus the library
packages they depend on. Run once per repository; adding the Nth member afterward is just a new member
directory, not a re-run of this skeleton.

**The rules below are about members, not about what is inside one.** A member's own internal layout is
its architecture's business — `hex-architecture`, in the `pyhouse-hex` plugin, for a hexagonal member;
`flat-layered`, in the `pyhouse-flat` plugin, for a flat one — and this root is the same either way.

## When to use vs. neighbours

- The architecture family of the members going into the workspace is not settled →
  `architecture-choice` decides hexagonal versus flat per distribution; nothing here depends on the
  answer.
- Where members share a store, what its owning library holds → `persistence` for the rules, and for
  the files the member family's data-access skill or the project's own layout.
- Adding one member's internal layout — its layer or role packages, its clients, its work units → not
  this skill, use that member's architecture skill.
- Choosing a runnable member's trigger → the member family's entrypoint skill (`flat-entrypoint`, in the
  `pyhouse-flat` plugin, is one).
- What the linter, the type checker and the line length are set to, and how dependencies are declared
  → `python-toolchain`; this root is only where those values are written, once. The interpreter floor
  behind them is `python-style`'s.
- Which runtime libraries a member's roles bring → the member family's setup skill
  (`hex-project-setup`, in the `pyhouse-hex` plugin, is one, and the flat family's is
  `flat-project-setup`, in the `pyhouse-flat` plugin).
- Where members share a store, the pytest plugin module the root `addopts` loads, and the fixtures
  inside it → the member family's integration-setup skill (`flat-test-integration-setup`, in the
  `pyhouse-flat` plugin, or `hex-test-integration-setup`, in `pyhouse-hex`).
- Building a single standalone distribution with no siblings and no shared store → not this skill; it
  needs no workspace root at all. Its own architecture skill lays its package skeleton, including the
  data-access role — neither assumes anything above the distribution.
- Whether a proposed member is a boundary at all — its encapsulated knowledge and change vectors →
  `coupling`.
- What goes inside a runnable member's `Dockerfile`, and the build context it admits →
  `python-container-image`; this root places the file and runs it from compose.
- The repository-wide grep firewall in `tests/test_architecture.py` → `test-architecture-rule`.

## Template — uv workspace, Docker Compose and Make

```
myrepo/
├── pyproject.toml            # workspace container + shared tooling config; NO runtime code
├── Makefile
├── docker/                   # only where a runnable member runs in a container
│   ├── local.compose.yaml    # development — what every make target drives
│   └── compose.yaml          # deployment template — registry images, resource limits
├── tests/
│   └── test_architecture.py  # repository-wide grep firewall
├── packages/                 # only where members share a library
│   └── myschema/             # a library the runnable members depend on
└── services/
    └── myapp/                # one runnable distribution per directory
```

**A library that drags a heavy dependency in is not the same member as one that does not** — a member
that only wants the logging setup should not inherit a schema library's driver and migration tool. The
second cross-cutting helper is the signal for a second `packages/` member, not a bigger first one; a
repository whose members share nothing has no `packages/` at all.

Root `pyproject.toml` — `python-toolchain`'s tables, written here once and whole, plus:

```toml
[project]
name = "myrepo"
version = "0.1.0"
requires-python = ">=3.13"

[tool.uv.workspace]
members = ["packages/*", "services/*"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Its `pythonpath` lists only what this root loads (below), and `packages/*` is a member group only
where members share a library.

The test configuration is whole here and nowhere else (rule 6): `python-toolchain`'s block, with
`testpaths` naming each run's own `tests/`. **Each member's suite runs from that member's directory, with
the member as the runner's root** (rule 10), and the root's own `tests/` runs from the root — the `test`
target below does both. A member's tests import their own support (`tests.unit.fakes`, `tests.helpers`)
under a name that resolves to that member's tree, and one run over the whole repository cannot give them
that: with the root as the runner's root, `pythonpath = ["."]` makes `tests` the repository's own
directory and no member's, and listing every member's directory instead lets the first one listed
shadow every other member's `tests`. Under `python-toolchain`'s `--import-mode=importlib` the runner's root decides what `tests`
names, while a `pythonpath` entry resolves against this file, so the root block carries no `.`.

The root project is a **workspace container plus shared tooling config, with no runtime code of its
own**. Nothing importable lives at the root; every line of shipped code sits inside a member.

**The tooling values above are the project's to choose; what the workspace fixes is that they are chosen
once, at the root, and inherited.** A member never restates them — a second `line-length` in a member's
`pyproject.toml` is how two halves of one workspace start disagreeing about what a diff should look like.
The full tool tables and the choice of line length are `python-toolchain`'s, the interpreter floor
`python-style`'s; the workspace's part is only that they are written here, once.

Each member's `pyproject.toml` declares its workspace dependencies explicitly — here
`services/myapp/pyproject.toml`:

```toml
[project]
name = "myapp"
version = "0.1.0"
dependencies = ["myschema"]  # only where members share a library

# only where members share a library
[tool.uv.sources]
myschema = { workspace = true }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

The member carries no `requires-python` and no tool configuration of its own: the root settles both,
and a member that restates the floor is the first half of a workspace that disagrees with itself
(rule 6).

`docker/local.compose.yaml`:

```yaml
name: myrepo

services:
  myapp:
    build:
      context: ..
      dockerfile: services/myapp/Dockerfile
    profiles: ["myapp"]
```

**Pin `name:` explicitly.** Without it compose names the project after the directory holding the
file — `docker/` — and every volume is recreated under a new prefix the first time someone runs it
from a different path.

A runnable member's `Dockerfile` sits in that member's directory and builds with the repository root
as its context, which is what `context: ..` above names.

**One compose profile per runnable member**, named after the member, and each such profile also pulls in
the datastores it depends on. That is what makes `--profile myapp` bring up exactly what one member needs
and nothing else.

`Makefile`:

```makefile
.PHONY: install lint fmt typecheck test verify run-myapp

install:
	uv sync --all-packages

lint:
	uv run ruff check

fmt:
	uv run ruff check --fix
	uv run ruff format

typecheck:
	for member in packages/* services/*; do [ -d $$member/src ] || continue; (cd $$member && uv run mypy --config-file $(CURDIR)/pyproject.toml src $$(find tests -name '*.py' 2>/dev/null | grep -q . && echo tests)) || exit 1; done
	uv run mypy tests

test:
	for member in packages/* services/*; do [ -d $$member/tests ] || continue; (cd $$member && uv run pytest --rootdir .; rc=$$?; [ $$rc -eq 0 ] || [ $$rc -eq 5 ]) || exit 1; done
	uv run pytest

verify: lint typecheck test

run-myapp:
	cd services/myapp && uv run python -m myapp
```

Two details in there are load-bearing. `uv sync --all-packages` is needed because a bare `uv sync`
syncs only the root project and leaves every member's dependencies uninstalled. And `run-*` targets
`cd` into the member directory first: where a member's settings, and a shared library's that reads its
own stem, resolve their dotenv files relative to the process working directory, a member launched from
the repository root reads none of them. The `test` loop skips a member with no `tests/` directory and accepts pytest's
exit status 5 — nothing collected — from one whose `tests/` holds none yet, and stops on any other failure.
The `typecheck` loop is rule 10 applied to the type checker. The root's `[tool.mypy]` table is
`python-toolchain`'s as written for one distribution — its `src`, `tests` and `.` resolve against the
directory the checker runs from — and it is passed explicitly, so the member's own `pyproject.toml` is
never taken for it. The loop passes `tests` only where the member has Python files under it.

**Where members share a store, add what serves it — and nothing above changes.** The compose file gains
the datastore as a service whose `profiles` name every runnable member that uses it, on a named volume,
its image pinned per `python-toolchain` rule 12. The Makefile gains a `migrate` target, the only
sanctioned way schema changes reach a database, which `cd`s into the owning library before running
the migration tool (rules 3 and 4). The store's test fixtures live in a pytest plugin module beside
that library's own tests — `packages/myschema/tests/myschema_testing.py` — loaded by
`-p myschema_testing` in `addopts` and
`packages/myschema/tests` in the root block's `pythonpath`, which resolves against the root file and so
holds in every member's run. Every member loads that one module rather than a copy, and each member's
run starts its container once. What goes inside that module is the member family's integration-setup
skill's, and the loop-scope lines it needs are `python-toolchain`'s; this root owns only the two settings
that load it. Infrastructure with its own schema owner — a workflow engine, a metrics store
— gets its own datastore and its own named volume, never the members' database.

## Other bindings

- **Another workspace tool in place of uv.** Poetry path dependencies, PDM local sources, Pants and
  Bazel all express the same two things: the member list declared once at the root, and each member
  pinning its in-repository dependencies through an edge the tool itself resolves. The member-glob syntax,
  the lock file and the sync command change; rules 1–10 do not. Rule 5 is the one to carry over
  literally — whatever the tool, the edge is *declared*, never faked with a path insert.
- **Another task runner in place of Make, another container runtime in place of Compose.** `just`,
  `invoke` and `nox` give the same one-discoverable-command-set-at-the-root property; a dev Kubernetes
  cluster or Tilt gives the same per-member profile. What must survive either swap: one command syncs
  *every* member and not only the root, each member's suite and type check run with that member as root,
  each runnable member still starts from its own directory, one
  command applies migrations wherever members share a store, and a cleanup command names what it
  destroys instead of sweeping the project.

## Rules

1. **One workspace; libraries and runnable members never share a group.** One group holds libraries with no entrypoint of their own —
   only where members share a library, and a repository whose members share none has no such group;
   the other holds runnable distributions, one directory per deployable. `packages/*` and `services/*`
   are this example's names for them. Never put runnable code in the library group or shared library
   code in the runnable one, and never runtime code in the root project, which is a container: code
   that has no member gets one. A library member declares itself typed (`python-packaging` rule 13);
   the untyped-package override is never the fix for a member, because it turns every import of it
   into `Any`.
2. **A new member is admitted with two sentences, not just a directory.** Before creating the
   directory, the change that adds it names the member's **encapsulated knowledge** — the tables it
   owns, the upstream it speaks, the vocabulary it defines, none of which another member may assume —
   and two or three **change vectors**: plausible changes that would touch *only* this member. A member
   whose knowledge cannot be named is a category word, not a boundary; one whose every change vector
   drags a sibling along is drawn in the wrong place. The reasoning is `coupling`'s; the check costs two
   sentences and is the cheapest boundary test available.
3. **Exactly one member owns a shared store's schema and its migration history, and it is a library
   member.** Two members defining tables over one store means two migration histories over one schema,
   and the second one to run decides what the first one's tables look like. So the owner sits in the
   library group, every dependant declares an edge to it, and a grep firewall enforces that no runnable
   member constructs a statement of its own (`test-architecture-rule`). The flat family states the
   same ownership obligation from a member's side, under `flat-persistence`, in the `pyhouse-flat`
   plugin.
4. **One migration history per store is applied by one command, and that command runs from the member
   that defines the schema** — a `make migrate` target that `cd`s into the owning member. What makes the
   working directory load-bearing is a property of members, not of storage: a migration run from inside
   a *dependant* resolves its connection settings from that member's environment and working directory,
   so two members can apply one migration history to two different databases and neither of them
   notices.
5. **A member declares its in-repository dependencies as edges the packaging tool resolves** —
   `[tool.uv.sources]` under uv — never a path hack, a `sys.path` append, or a copy-pasted module. A
   dependency the packaging tool cannot see is one the installer, the type checker and CI each resolve
   differently, and the disagreement surfaces as an import error on somebody else's machine.
6. **Tooling values are settled once at the root and inherited, never re-argued in a member.** Line
   length, the interpreter floor (whose value is `python-style`'s), the lint target, the test-runner
   configuration: the *values* are the project's to choose, and what the workspace fixes is that they
   live in one file. A member overrides one only for a genuine per-package exception, and never the test-runner's own configuration block —
   declaring it in a member moves the configuration file down to that member, and every path the
   test configuration carries then resolves against a directory nobody wrote it for.
7. **Runnable members never import each other.** Two of them needing the same code means that code
   belongs in a library member. A deployable-to-deployable import is what turns a workspace of
   independent deployables into one program.
8. **Where a member resolves settings files against the working directory, it is launched from its own
   directory** — `cd services/<member> && uv run python -m <member>`, which is what `make run-<member>`
   does. A member's settings, and a shared library's that reads its own stem, then resolve their dotenv
   files against the process working directory, so a member started from the repository root silently reads
   none of them. Migrations and syncs have no such restriction.
9. **A cleanup command names what it destroys.** It removes the one volume or artifact it is for, never
   everything the project holds — `docker compose down -v` drops every volume, application data
   included.
10. **Each member's test suite and its type check run with that member as the tool's root**, from the
    member's own directory, and the repository's own tests run from the root. A member's tests import
    their own support under a name that resolves to that member's tree; a single run from the root
    resolves that name to the repository's directory or to whichever member it finds first, and a
    member's suite then imports another member's support or none — or, for the type checker, meets two
    members' support under one module name and refuses to check either.

## Hard stops

- Only one distribution will ever exist → stop, this is a single-distribution project and it needs no
  workspace root; its own architecture skills lay its packages and its data access. Sharing a datastore
  is one reason members end up in one repository, not the test of whether they belong there — a
  repository of libraries and CLIs that share no store needs every rule here except the ones about a
  schema owner.
- Asked for a member's internal layout — its layer or role packages, its clients, its work units → stop,
  use that member's architecture skill (`hex-architecture`, in `pyhouse-hex`, or `flat-layered`, in
  `pyhouse-flat`), or the project's own layout where neither applies.
- The members' architecture family is not settled → stop, use `architecture-choice`, once per member.
- Asked whether a proposed member is a boundary at all → stop, use `coupling`; rule 2 is the check this
  skill runs once that is settled.
