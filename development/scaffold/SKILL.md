---
name: scaffold
description: Create a new project from an architecture document — directory structure, boilerplate (README, CLAUDE.md, AGENTS.md, .gitignore, package manifest, linter+formatter config, Dockerfile if applicable, CI workflow, tests directory), per-component stubs with real interfaces, `.aicp/state.yaml` for AICP tracking, git init + first commit. Project must be immediately runnable. Distinct from `scaffold-subagent` (creates a sub-agent inside an EXISTING fleet) and `scaffold-monorepo` (multi-package). Loads when the operator says "scaffold the project", "create the project from architecture", "generate boilerplate from docs/architecture.md", "stand up <project-name>".
argument-hint: <project-name> [path-to-architecture-doc]
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: high
---

# scaffold

The "architecture doc → runnable repo" skill. Reads `docs/architecture.md` (or operator-named source), creates the directory tree + boilerplate trio (README / CLAUDE.md / AGENTS.md) + package manifest + per-component stubs + tests + CI + Docker + state file, initializes git. The output is a project that can be cloned, set up, and run before a single feature is written. Distinct from `scaffold-subagent` (sub-agent in fleet) and `scaffold-monorepo` (multi-package monorepo).

## Trigger phrases (when to load this skill)

Load when the conversation matches any of:

- **Direct verb**: operator says "scaffold the project", "create the project", "stand up <name>", "generate the boilerplate", "build the skeleton from architecture".
- **Lifecycle gate**: an `architecture-propose` produced a fresh architecture doc; operator wants to translate it to a working repo.
- **Sister-project bootstrap**: a fleet-class new project (e.g., a new `nnrt-*` variant or a new sister project) needs initial structure.
- **Replatforming**: existing project being rebuilt from a re-proposed architecture (rare; usually paired with `evolve-migrate`).

Do NOT load when:

- Adding a sub-agent to an existing fleet — load `scaffold-subagent`.
- Multi-package layout from day 1 — load `scaffold-monorepo`.
- An existing project just needs a missing piece (CI, Docker, deps) — load the specific `foundation-*` skill.
- Architecture doesn't exist yet — load `architecture-propose` first; this skill scaffolds AGAINST architecture.
- Project exists; want to reorganize — load `refactor-architecture`.

## Operations

This skill has 4 named operations. Execute in order — each gates the next.

### Operation 1: Read architecture + check preconditions

**Trigger**: skill loaded; operator named project + (optional) architecture doc.

**Process**:

1. Resolve inputs:
   - Project name: from `$0` arg.
   - Architecture path: from `$1` arg, default `docs/architecture.md`.
2. Read the architecture document. Extract:
   - **Components/layers** with their responsibilities.
   - **Stack**: language, framework, runtime, infra targets.
   - **Module breakdown**: what packages/modules will exist.
   - **First milestone(s)** if listed (often informs "what to scaffold first").
3. Check destination preconditions:
   ```bash
   pwd
   ls <project-name>/ 2>/dev/null && echo "DESTINATION EXISTS"
   git rev-parse --is-inside-work-tree 2>/dev/null   # are we already in a repo?
   ```
   Three valid scenarios:
   - **New directory next to current**: scaffold creates a sibling directory.
   - **Bootstrap into empty current dir**: rare; only if explicitly authorized.
   - **Inside existing repo (sub-project)**: scaffold creates a subdirectory.
   Reject silently overwriting any existing directory.
4. Verify the architecture is COMPLETE enough to scaffold:
   - At minimum: stack named, components named, module structure named.
   - If architecture is sketchy, surface gaps to operator BEFORE scaffolding — partial scaffolds are worse than waiting (`architecture-review` may be the right next step).
5. Identify which sister-project conventions apply (if applicable):
   - AICP fleet projects share AGENTS.md/CLAUDE.md/SOUL.md trio convention.
   - DSPD projects use Plane integration.
   - openfleet uses standing-orders.yaml.

**Quality bar (Operation 1 done when)**:

- [ ] Project name + architecture path resolved.
- [ ] Architecture parsed: stack, components, modules captured.
- [ ] Destination scenario classified (sibling / current / subdir).
- [ ] No silent overwrite — existing destination flagged for explicit operator decision.
- [ ] Architecture completeness verified (or gaps surfaced for `architecture-review`).
- [ ] Sister-project conventions identified if applicable.

### Operation 2: Create directory tree + manifest

**Trigger**: Operation 1 inputs validated.

**Process**:

1. Create top-level structure:
   ```
   <project>/
   ├── README.md
   ├── CLAUDE.md
   ├── AGENTS.md
   ├── .gitignore
   ├── <package-manifest>     # pyproject.toml / package.json / Cargo.toml / go.mod
   ├── Makefile               # mirror common ops as targets
   ├── .env.example
   ├── docs/
   │   └── architecture.md    # copy or link the source doc
   ├── <src>/                 # language-conventional dir (aicp/ or src/ or ...)
   │   └── <component>/       # one per architecture component
   ├── tests/
   ├── .aicp/
   │   └── state.yaml
   ```
2. Create `<src>/<component>/` for each architecture component, with:
   - `__init__.py` (or equivalent) with module docstring naming the component's responsibility.
   - One stub file with the named interface(s) — type signatures, docstrings, `raise NotImplementedError`.
   - Companion `tests/test_<component>.py` with one trivially-passing smoke test.
3. Generate the package manifest with the right minimum (Python example):
   ```toml
   [project]
   name = "<project>"
   version = "0.0.1"
   description = "<from architecture summary>"
   requires-python = ">=3.11"
   dependencies = [<from architecture stack>]

   [project.optional-dependencies]
   dev = ["pytest", "ruff", "mypy"]
   ```
4. Generate `.gitignore` for the language + AICP conventions (`.env`, `.aicp/state.yaml` if state is operator-private, `__pycache__/`, etc.).
5. Generate `Makefile` with: `install`, `test`, `lint`, `run`, plus project-specific targets implied by architecture.

**Quality bar (Operation 2 done when)**:

- [ ] Top-level files exist with REAL content (not "TODO").
- [ ] One directory per architecture component, each with stub + test.
- [ ] Package manifest dependencies match architecture stack.
- [ ] `.gitignore` covers language + secrets + state.
- [ ] Makefile has install + test + lint + run as minimum.

### Operation 3: Author the agent-context trio + foundational config

**Trigger**: Operation 2 tree built.

**Process**:

1. **README.md** — operator/contributor-facing:
   - Project name + one-line description.
   - Quick-start: setup commands that ACTUALLY WORK.
   - Architecture summary (3-5 sentences) + link to `docs/architecture.md`.
   - How to run, how to test, how to build.
2. **CLAUDE.md** — Claude Code-specific (per AICP convention; sister projects have own conventions):
   - Project Identity Profile (type / domain / scale / phase).
   - Mission summary.
   - Architecture diagram (text or ASCII) + key principles (3-5).
   - Tech stack (one paragraph).
   - Project structure (table mapping packages to responsibilities).
   - Pointers to depth (link to `docs/architecture/_index.md` or equivalent if needed).
3. **AGENTS.md** — universal cross-tool context:
   - Hard rules (4-6 bullets the project never violates).
   - Stage gates (if architecture has milestones).
   - Quality gates (lint clean, tests pass, type-check clean before commit).
   - Common commands.
   - Conventions (file naming, commit format).
4. **.aicp/state.yaml** — initial state:
   ```yaml
   project: <name>
   phase: scaffolded
   created: <date>
   architecture: docs/architecture.md
   active_task: null
   recent_handoffs: []
   ```
5. **CI workflow** (`.github/workflows/ci.yml` or equivalent):
   - Lint stage, test stage, build stage. Each mirrors a Makefile target so dev/CI run identical commands.
6. **Dockerfile** + **docker-compose.yaml** if architecture calls for containerization (defer to `foundation-docker` if absent — don't generate Docker for non-containerized projects).

**Quality bar (Operation 3 done when)**:

- [ ] README has working setup instructions (verified by reading them, not just authored).
- [ ] CLAUDE.md identity profile correctly populated from architecture.
- [ ] AGENTS.md hard rules + quality gates are project-specific, not generic.
- [ ] state.yaml exists with project name + phase + architecture link.
- [ ] CI workflow runs lint + test + build (or explicit "no CI for this scope").
- [ ] Docker present only if architecture calls for it.

### Operation 4: Init git + smoke + announce

**Trigger**: Operation 3 boilerplate authored.

**Process**:

1. Initialize git:
   ```bash
   cd <project>
   git init
   git config init.defaultBranch main
   ```
2. Run install + test smoke to prove the scaffold actually runs:
   ```bash
   make install 2>&1 | tail -20
   make test 2>&1 | tail -20
   make lint 2>&1 | tail -10
   ```
   All three must exit 0. If any fail, the scaffold is INCOMPLETE — fix before proceeding.
3. Make the initial commit:
   ```bash
   git add .
   git commit -m "scaffold: initial structure from <architecture-doc>"
   ```
4. Announce to operator:
   - "Scaffolded `<project>` at `<absolute-path>`."
   - "Smoke green: install + test + lint all pass."
   - "Next: load `foundation-deps` to wire actual dependencies, OR `feature-document` to start the first feature, OR `pm-plan` to translate architecture into milestones."
   - State the recommended NEXT skill explicitly.

**Quality bar (Operation 4 done when)**:

- [ ] Git initialized with `main` as default branch.
- [ ] `make install + test + lint` all exit 0.
- [ ] Initial commit made with message naming the architecture source.
- [ ] Operator told absolute path of new project.
- [ ] Operator told the specific next skill.

## Gotchas (known failure modes — read before doing)

### Gotcha 1: Scaffolding into an existing directory silently

Operator runs scaffold; destination already exists with operator's prior work-in-progress. Skill writes over README, CLAUDE.md, package manifest, etc. Operator's work is gone — it was unsaved or only-locally-committed.

**The rule**: Operation 1 step 3 — if destination exists with content, STOP and surface to operator. Three valid resolutions: (1) abort, (2) explicit "overwrite, I have a backup", (3) target a sibling directory. Never silently overwrite.

### Gotcha 2: Stub interfaces that don't match the architecture's vocabulary

Architecture says "Router resolves request to backend via tier_map." Stub generated as `class RequestResolver:` with no mention of tier_map or backend. Future implementation has to either rename or carry duplicate vocabulary; either way the architecture-to-code mapping is broken from day 1.

**The rule**: Operation 2 step 2 reads the architecture's NAMING and uses those exact names. If architecture says "Router", the stub class is `Router`, not `RequestResolver`. The naming carries semantic content; renaming silently makes the code drift from the doc.

### Gotcha 3: README setup instructions that don't work

Skill writes `make install` in README quick-start. Operator clones, runs `make install`, gets "no such target" because the Makefile uses `pip install` and never defined `install:`. Setup fails on the first thing a new user tries.

**The rule**: Operation 3 step 1 reads-its-own-instructions before claiming done. Operation 4 step 2 actually runs them. If the instructions don't work in operation 4's smoke, the scaffold is incomplete — fix and retry. The README is a contract; broken contracts erode trust immediately.

### Gotcha 4: Generating Docker / CI / database / auth that the architecture didn't ask for

Architecture is a single-file Python script tool. Skill generates Dockerfile, docker-compose, GitHub Actions, PostgreSQL connection scaffolding, and auth middleware because "every project has these". Operator now has 600 lines of unused config to maintain.

**The rule**: Operation 3 step 6 — generate Docker / CI / database / auth ONLY if architecture explicitly calls for them. The default is "absent". For ambiguous cases, generate the SIMPLEST version that matches the architecture's statement, and defer richer foundations to the specific `foundation-*` skill (`foundation-docker`, `foundation-ci`, `foundation-database`, `foundation-auth`).

### Gotcha 5: First commit is 600 files of "TBD"

Skill generates 50 component stubs, all `raise NotImplementedError`. Initial commit is "scaffold: initial structure" but reads as a graveyard — every file is empty. Future operator can't tell which stubs are real-skeleton vs accidentally-empty.

**The rule**: Operation 2 step 2 — every stub has REAL content: the responsibility (docstring), the interface (type signatures), and the failure mode (`raise NotImplementedError("not yet implemented for milestone M0X")`). The interface tells the next session WHAT to implement; the milestone reference tells WHEN. A stub without these is filler, not a scaffold.

## Reference exemplars

The Extension Standards reference exemplars for skills are the second brain's `model-builder` and `wiki-agent` skills — see `~/devops-solutions-research-wiki/skills/`. This skill follows their structure: trigger phrases, multiple named operations, per-operation Process + Quality bar, Gotchas with detection + rule + reasoning. For scaffold ARTIFACTS specifically, AICP itself was scaffolded into its current shape over Stages 1-5; the [docs/architecture/_index.md](../../../docs/architecture/_index.md) detail tree is an example of architecture-driven layout the scaffold output should be ready to evolve into.

## Domain context

This skill operates in the **backend-ai-platform-python** domain. AICP convention is the AGENTS.md + CLAUDE.md + (per-agent) SOUL.md trio for context-management; sister fleet projects use the same trio. State tracking via `.aicp/state.yaml`. Python projects default to Python 3.11+ (StrEnum era), pyproject.toml, ruff for linting, pytest for testing, ruff format for formatting. Sister projects (openfleet, dspd, nnrt) may use different stacks (TypeScript / Plane integration / NLP pipelines) — this skill respects whatever the architecture names. Brain (~/devops-solutions-information-hub) connection is bootstrapped if architecture calls for it — that's via `tools.gateway` adoption, not in this skill's scope to set up.

## Related skills

| Skill | When | Why distinct |
|-------|------|--------------|
| scaffold-subagent | Add a sub-agent to an EXISTING fleet | Sub-agent within fleet; this skill bootstraps a top-level project |
| scaffold-monorepo | Multi-package monorepo from day 1 | Multi-package; this skill is single-project |
| architecture-propose | Propose architecture from idea | Produces input for this skill; this skill scaffolds against it |
| architecture-review | Review an architecture for gaps | Pre-scaffold gate; this skill assumes architecture is reviewed |
| foundation-deps | Wire actual deps post-scaffold | Specific concern; this skill generates the manifest stub |
| foundation-docker | Container infrastructure | Specific concern; this skill generates Docker only if architecture asks |
| foundation-ci | CI pipeline tailored to stack | Specific concern; this skill generates CI minimally |
| foundation-testing | Full test framework setup | This skill generates test stubs; foundation-testing fills the framework |
| pm-plan | Forward planning post-scaffold | Plans against this skill's output |
