---
name: sdlc-init
description: Invoked explicitly by /init-project. Bootstraps or upgrades the SDLC framework in a repository — detects the stack, fills .agent/project-context.yaml, creates the docs/ and .agent/state/ trees, writes the managed project-facts block into CLAUDE.md, and seeds the domain knowledge files. Idempotent and safe to re-run as an upgrade path.
argument-hint: "[--upgrade]"
disable-model-invocation: true
---

# /init-project — bootstrap the SDLC framework

Run once per repository, and again whenever `framework_version` changes.

## Protocol (shared — do not restate here)
Framework assets — `.agent/framework.yaml`, `.agent/steps/`, `.agent/rules/`,
`.agent/gates/`, `.agent/templates/`, `.agent/modules/` — resolve **project-first**: use
the repository's copy when it exists, otherwise `${CLAUDE_PLUGIN_ROOT}/.agent/…`. That is
how one repo can override a single template or rule without forking the framework.
`.agent/project-context.yaml` and `.agent/state/` are **always project-local** — never
read or write them under the plugin root.
1. If `.agent/state/context-cache.md` exists and its `framework_version` matches
   `.agent/framework.yaml`, Read ONLY that file. Otherwise Read
   `.agent/steps/context-loader.md` and execute it, then write the digest back to the cache.
2. Read `.agent/steps/gate.md` and execute it with the phase inputs below.
3. On completion, format output per `.agent/steps/report-footer.md`.
Never copy the contents of those files into this skill.

> **Gate exception.** This skill runs *before* the project has context or state, so it
> skips gate Steps 1, 2 and 2.5 on a first run. Steps 3 (model check) and 4 (checkpoint)
> still apply — this command writes many files.

---

## Step 1 — Detect the situation

Read `.agent/framework.yaml` for `framework_version`.

| Found | Meaning | Action |
|---|---|---|
| No `.agent/project-context.yaml` | fresh install | run all steps |
| Exists, no `framework_version` recorded in state | pre-2.0 install | run in **upgrade** mode |
| Exists, version matches | already current | ask: "Already initialised at {v}. Re-run to repair? (Y/N)" |

In upgrade mode, **never overwrite a filled value.** Add missing keys, report what
changed, and leave the rest.

## Step 2 — Detect the stack

Walk `.agent/framework.yaml` → `stack_detection` in order and look for each manifest.
The first one found decides the primary language; additional manifests mean a polyglot
repository and usually more than one profile.

Read the manifest — the `hint` field says where the useful part is — and infer language,
framework, build tool and test framework. Check
`.agent/framework.yaml` → `ai_detection_signals` too. Then match against the directories
under `.agent/modules/`:

- A matching profile exists → propose it.
- Several apply (e.g. a web framework *and* a message broker) → propose the list, in
  dependency order.
- Any `ai_detection_signals` match → also propose the `ai-llm` overlay.
- **No profile matches** → do not guess. Offer to scaffold a new profile from
  `.agent/modules/_schema.yaml`, and ask the user for the six commands that matter:
  install, test, lint, format check, typecheck, run.

Present the detection and **wait for confirmation** before writing anything:

```
DETECTED
  Language   : {..}
  Framework  : {..}
  Build/test : {..} / {..}
  Profiles   : {ids, in merge order}
  Ticket pfx : {suggested, from the repo or directory name}
  Domains    : {inferred from source subpackages}
Correct? (Y / edit)
```

## Step 2.5 — Confirm the framework assets are reachable

Check that `.agent/framework.yaml` resolves — locally, or under
`${CLAUDE_PLUGIN_ROOT}/.agent/`. Report which:

```
Framework : ${CLAUDE_PLUGIN_ROOT}/.agent  (plugin sdlc-framework v2.0.0)
        or  .agent                        (local checkout — framework repo)
```

If neither resolves, stop: the plugin is not installed and this is not the framework's own
repository. Nothing below can work without the steps, gates, rules and templates.

**Do not copy the framework assets into the target repository.** They resolve from the
plugin root at read time, so copying them creates a second copy that stops receiving
updates — the exact drift this framework exists to prevent. Copy a single file into
`.agent/` only when you deliberately want to override it.

## Step 3 — Create the directory tree

Create, skipping any that exist. These are all **project-owned** — the framework assets
stay in the plugin:

```
docs/product/features   docs/prd        docs/srs         docs/techdocs
docs/testcases          docs/reviews    docs/adr         docs/domain-knowledge
docs/prompts            docs/evals                          <- only when an AI profile is active
specs/bdd
.agent/state/features   .agent/state/evals
.agent/state/runs       .agent/state/archive
```

Also create the test roots named by the merged profile's `layout` if they are missing
(`unit_tests`, `integration_tests`, `acceptance_tests`, and `eval_tests` when AI is on).

## Step 4 — Write `.agent/project-context.yaml`

This file is **always project-local**, even when everything else comes from the plugin.
Copy `.agent/templates/project-context.yaml` (resolved project-first, so normally the
plugin's copy) into the repository at `.agent/project-context.yaml` and fill **every**
`{{PLACEHOLDER}}` from Step 2. Leaving a placeholder behind is a failure of this command, not a task for the
user — an unfilled context file is exactly the state that made the previous framework
generation unusable.

Set `project.ai_product: true` if any AI profile is in `stack_profiles`.

## Step 5 — Write the CLAUDE.md project-facts block

Create `CLAUDE.md` if absent. Then write the managed block:

```
<!-- SDLC:PROJECT-FACTS:BEGIN -->
...§1 Project Overview through §7 Git Conventions, filled with REAL values...
<!-- SDLC:PROJECT-FACTS:END -->
```

Rules:

- **Replace only what is between the markers.** Everything outside is hand-written and
  must survive untouched.
- If the markers are absent but a placeholder-filled or commented-out `§1..§7` block
  exists, convert it in place: uncomment it, fill the real values, wrap it in markers.
- Fill from the code, not from the template's example comments. Read the actual
  exception classes, the actual response wrapper, the actual commands. A project-facts
  block that says `ResourceNotFoundError` while the code defines `NotFoundError` is
  worse than no block, because generators will emit the wrong name with confidence.
- §4 Traceability carries a four-line summary and points at
  `.agent/rules/traceability.md`. Do not duplicate the full rules here.

## Step 6 — Seed domain knowledge

Create if absent (never overwrite):

**`docs/domain-knowledge/business-dictionary.md`** — three tables: Canonical Terms
(term, definition, use instead of), Banned Terms (banned, canonical, why), Status/Enum
Registry (entity, field, allowed values). The context loader enforces the banned list on
every generated word, so an empty file is fine; a wrong one is not.

**`docs/domain-knowledge/core-entities.md`** — per entity: Purpose, Domain, Storage,
Owner service, field table (name, type, required, notes), Business invariants,
Relationships. Seed it from the existing data models if any exist, and say that you did
so, so the user knows to review rather than trust.

## Step 7 — Initialise state

Write `.agent/state/current.yaml` from `.agent/templates/state/current.yaml`:

```yaml
schema_version: 1
framework_version: "{from framework.yaml}"
updated_at: "{ISO8601}"
updated_by: "/init-project"
model_ack: false
active_feature: null
features: {}
next_command: "/feature \"<one-line feature request>\""
notes: "initialised"
```

Create the empty index files with their header rows only:
`findings.tsv`, `trace.tsv`, `trace-waivers.tsv`, `checklist.md`.

Then run the full context loader once and write `.agent/state/context-cache.md`, so the
first real command starts warm.

## Step 8 — Verify and report

Check and report each:

- [ ] `.agent/project-context.yaml` contains no `{{`
- [ ] every path in `paths` exists on disk
- [ ] every id in `stack_profiles` resolves to a directory with a `stack-profile.yaml`
- [ ] each profile satisfies `.agent/modules/_schema.yaml` required keys
- [ ] `CLAUDE.md` contains both markers, and the values inside match the real code
- [ ] `.agent/state/current.yaml` parses and names the framework version
- [ ] `context-cache.md` written

Report per `report-footer.md`. `Gate: n/a`. Next command comes from
`framework.yaml → next_command["init-project"]`.

---

## Boundaries

- Never overwrite a hand-written file. `CLAUDE.md` outside the markers, the domain
  knowledge files, and any filled context value are the user's.
- Never invent a stack profile silently. If nothing matches, ask.
- Do not create example features, sample PRDs, or placeholder documents. An empty
  `docs/` tree is honest; a tree of lorem-ipsum artifacts corrupts the trace index and
  teaches people to ignore the folder.
