---
name: setup
description: This skill should be used when the user asks "what is macstack.json", "set up macstack", "check macstack setup", "verify macstack.json", "explain the macstack standard", or before any other macstack-dev skill runs in a project for the first time. Explains the standard, locates the schema and category registry, and verifies tooling.
---

# MACSTACK Setup & Orientation

macstack.json is the standardized JSON file of the MACSTACK framework (Multi-Agent
Composable Stacks). It lives in **`macstack/` in the project root**, alongside the
working documents (`macstack/macstack.json`) — a bare root `./macstack.json` is a
supported legacy location. It is at once: the business spec (goals, results), the
technical spec (software, entities, interfaces, workflows) and the meta-config from
which project files are scaffolded. `CLAUDE.md` references it — never duplicates it.

## Canonical resources (GitHub-first, bundled fallback)

The standard is hosted on GitHub — always prefer the live copies (they may be newer
than the bundled ones); fall back to the bundled copies offline:

| Resource | Live (canonical) | Bundled fallback |
|---|---|---|
| JSON Schema | `https://raw.githubusercontent.com/macstacks/macstack/main/schema/macstack.schema.json` | `${CLAUDE_PLUGIN_ROOT}/skills/lint/references/macstack.schema.json` |
| Category registry | `https://raw.githubusercontent.com/macstacks/registry/main/software-categories.json` | `${CLAUDE_PLUGIN_ROOT}/skills/lint/references/software-categories.json` |
| Reusable blocks (software passports, entity/trigger/agent templates) | `https://github.com/macstacks/registry` (`software/`, `entities/`, `triggers/`, `agents/`) | — |
| Full examples + reference linter | `https://github.com/macstacks/macstack` (`examples/`, `scripts/lint.py`) | — |

Every macstack.json should start with `"$schema":
"https://raw.githubusercontent.com/macstacks/macstack/main/schema/macstack.schema.json"`
— editors then autocomplete and validate live.

Read the schema's top-level `description` first — it encodes the section order
(result-first): goals → results → processes → triggers → workflows → software →
entities → interfaces → connections → agents → context → resources.

## Core concepts (30 seconds)

- **Result-first**: every stack starts from goals/results in money terms; a process
  without a result is "coding for coding's sake".
- **prototype**: a parent macstack.json (GitHub repo `github:owner/repo` or a local
  absolute path). The child extends/overrides it — merge by `id`.
- **stacks**: organization composition — one `root` stack + `substacks`.
  Cross-stack refs use `<stack-id>:<element-id>`.
- **software[]**: every piece of software with mandatory `category` (registry) and
  `type` (ready_made | constructor | framework | library | custom), strict layers
  (data | logic | interface | infrastructure), `instances[]` with URLs.
- **agents**: `stack_agents` (orchestrate the whole stack, read `.claude/`, may modify
  the stack) and `managed_agents` (model + instructions + tools; invoked via
  interface / workflow / trigger / api).
- **Secrets are NAMES only**: `resources.accesses[]` lists env keys (with `required`
  flag); values live in Infisical.

## The `macstack/` folder

The standard also defines a folder of working documents next to macstack.json —
exactly four subfolders, plus README.md and macstack.json at the root, six
entries in all. The count is a constraint: a specification spread over many
files becomes more tedious to review than the code it describes.

```
macstack/
├── macstack.json            the spec — canonical location
├── README.md                folder contract, rendered from doc-contracts.json   [generated]
├── client/                  what a human writes and the client reads — the source of truth
│   ├── OVERVIEW.md          [client] business logic, goals, invariants, glossary
│   ├── USER-CASES.md        [client] cases per role, versioned
│   ├── UX-UI.md             [client] interface bar — cross-cutting + per-screen, incl. forbidden
│   ├── AUTOMATION.md        [client] roles, role tasks, triggers
│   ├── HANDBOOK.md          [client] how to actually work with the platform, seeded from cases+screens
│   └── OPEN-QUESTIONS.md    §A owed by the client · §B deferred by us
├── generated/                built from a source, never hand-edited
│   ├── ARCHITECTURE.md      how the project is built, generated from macstack.json
│   ├── TEST-CASES.md        how each acceptance bullet is verified, auto | manual
│   └── INDEX.md             generated cases/screens/triggers/coverage tables
├── inbox/                   IMMUTABLE client material · README.md = manifest
└── history/                 journals and records — append-only
    ├── TASKS.md              milestones and tasks — what will be done, in what order
    ├── DECISIONS.md          decision registry (D14, D15 …) → files in decisions/
    ├── CHANGELOG.md          [client] what reached the people who use it, newest first
    ├── ledger.jsonl          append-only, one row per edit, comment and verdict
    ├── deltas/               proposals, not edits
    ├── decisions/            rulings, each with cost-if-wrong
    ├── reviews/              <slug>-conformance.md + its -business.md twin
    └── handoffs/             handoff records
```

`/macstack-dev:start` writes the `## Stack Specification` block into both
`CLAUDE.md` and `AGENTS.md` — the spec must read the same way from Claude Code
and from Codex.

`docs/` stays the ENGINEERING folder (architecture.md, api-conventions.md,
code-style.md, runbooks) — it never moves into `macstack/`.

## Verification steps

1. **Tooling**: `python3 -c "import jsonschema"` (fallback: structural checks only),
   `jq --version`, `gh --version` (needed for `spec-authoring`'s context discovery and
   GitHub prototypes).
2. **Project state**: resolve macstack.json in this order:
   1. `macstack/macstack.json` — canonical.
   2. `./macstack.json` — legacy; works, but say so and offer `/macstack-dev:start`
      (migration mode).
   3. Search upward to the git root (monorepo / nested project).
   - Both 1 and 2 present → **ERROR, never a silent choice** — two specs mean two
     truths; report both paths and stop. The remedy is `/macstack-dev:start`
     (migration mode), which relocates the legacy root file into the folder (or
     `git rm`s it once the moved copy is verified). Never guess which one is
     canonical.
   - Found → validate it (`lint` skill) and report the stage (`lifecycle.stage`).
   - Not found → offer `spec-authoring` — deriving the spec from an existing
     codebase and generating one from scratch are the same skill now.
   - Also check whether `macstack/` and its `client/`, `generated/`, `history/`
     documents exist (`client/OVERVIEW.md`, `USER-CASES.md`, `UX-UI.md`,
     `AUTOMATION.md`, `HANDBOOK.md`, `OPEN-QUESTIONS.md`; `generated/ARCHITECTURE.md`,
     `TEST-CASES.md`, `INDEX.md`; `history/TASKS.md`, `DECISIONS.md`, `CHANGELOG.md`,
     `ledger.jsonl`). If not, offer `documents` to create the folder.
3. **CLAUDE.md link**: check that CLAUDE.md contains a "Stack Specification" section
   pointing to macstack.json. If missing, offer to add:

```markdown
## Stack Specification

The business and technical specification of this project is **`macstack.json`**
(MACSTACK standard, canonical at `macstack/macstack.json`). Read it first: goals →
results → processes → workflows → software → entities → interfaces. What a person
must be able to GET is in `macstack/client/USER-CASES.md`; the folder is mapped in
`macstack/README.md`.

Never write code that contradicts `macstack.json` — change the specification first.

**Keep the folder current. These are triggers, not suggestions:**

| When | Run |
|---|---|
| A task is finished — code merged, behaviour changed | `/macstack-dev:update` |
| The client sent anything: a file, an email, a sentence in chat | `/macstack-dev:intake` |
| The client's answers came back from a review package | `/macstack-dev:review --read <file>` |
| Before promising the client a date, or when asked what is left | `/macstack-dev:plan` |
| You added a collection, route, job or role the documents never mentioned | `/macstack-dev:check --new` |
| Before handing anything to the client | `/macstack-dev:check` |

Never edit `macstack/generated/**` by hand — it is rebuilt and the edit is lost.
Never edit `macstack/client/**` on the client's behalf without a recorded ruling:
their words are the source, and `/macstack-dev:intake` is how a change gets in.
```

The table is the half that matters, and it is the half that was missing. A block
that says only "read this first" produces an agent that reads the folder and lets it
go stale — and a document that reads perfectly while describing yesterday's system is
worse than no document, because it is believed. Naming the trigger and the command
together is what makes "keep the docs current" an instruction instead of a wish.

## Skill routing

| Task | Skill |
|---|---|
| macstack.json for an existing project, or a new stack from scratch — incl. finding plugins/prototypes and worked examples | `spec-authoring` |
| Create the project's working files | `scaffold-project` |
| .infisical.json + .env.prod/.env.dev | `infisical-env` |
| Project rules and slash-command skills | `best-practices` |
| Validation, and "where are we and what next" | `lint` |
| Create/seed the `macstack/` folder, or relocate an existing `docs/` into the new layout | `documents` |
| The heading + bullet-label shape, the pointer bindings and the table budget | `documents` |
| Merge new client material into the folder | `intake` |
| Turn the acceptance bullets into checks | `test-cases` |
| Plan work, or reconcile with the tracker | `planning` |
| Keep the spec, the documents and the code in step | `sync` |
| Record what was built, or cut a release | `journal` |
| Audit the implementation against the documents | `conformance` |
| Package a review for the client | `client-package` |