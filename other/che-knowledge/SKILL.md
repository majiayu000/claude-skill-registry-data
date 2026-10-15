---
name: "che-knowledge"
description: "Create and evolve the project's durable knowledge base: glossary.md (vocabulary) plus <domain>/conventions.md (observed practice per domain). Evidence-based, previewed as a dry-run diff and gated by keep/alter/revert before every write. Invoked at phase boundaries by che-architect, che-archeology, che-spec and che-act, or standalone via /che-knowledge."
---

# Che Knowledge — project vocabulary + per-domain conventions

> **SHARED REFERENCES (CANONICAL — DO NOT DUPLICATE body here):**
> - Engineering contracts (precedence 1-18, DbC, Simplicity Bias): `engineering-contracts` skill
> - Path resolution + storage contract: `che` CLI — `eval "$(che compute_paths "$WORKTREE_ROOT" "$SESSION_ID" --cwd "$PWD")"`
> - Domain rulebooks (human playbooks): `domains/<domain>/profile.md` + `domains/<domain>/playbook.md`
> - CLI surface: `che capabilities --json --command "knowledge apply"`

## §0 PURPOSE

Che already keeps **structural** knowledge (`project_profile.md`, `architecture.md`) and **strategic**
knowledge (`roadmap.md`, `product_context.md`). It did not keep the **observed** knowledge of *how this
project actually works* — the vocabulary and the conventions people already follow. This skill owns
that, as two artifact families under the project folder (never inside the user worktree):

| Artifact | Path | Scope |
|---|---|---|
| Glossary | `~/.che-workspaces/<slug>/glossary.md` | one per project |
| Conventions | `~/.che-workspaces/<slug>/<domain>/conventions.md` | one per domain |

## §1 WHEN IT RUNS (phase boundaries)

- **Bootstrap (learning):** `che-architect` and `che-archeology` — when a project's intent/architecture is
  being established, seed the domains in play from observed evidence.
- **Consume + propose:** `che-spec` (planning) and `che-act` (execution) — load the relevant domain's
  conventions, apply them, and propose additions when the work reveals or contradicts one.
- **Standalone:** `/che-knowledge` for an explicit refresh of a domain.

## §2 PREFLIGHT

1. **Project slug is mandatory.** It is never inferred from the working directory. If the user did not
   supply one, ASK for it. No worktree binding is required — the knowledge base is project-scoped.
2. Confirm the project exists: `che knowledge show --project <slug>` fails with `UNKNOWN_PROJECT` when it
   does not.

## §3 THE THREE VERBS

```bash
che knowledge show    --project <slug> [--domain <domain>]   # read (inventory or one domain)
che knowledge scaffold --project <slug> --domain <domain>     # write the 11-section skeleton (idempotent)
che knowledge apply   --project <slug> --ops <json|@file|->    # preview a change set (dry-run default)
che knowledge apply   --project <slug> --ops @ops.json --no-dry-run --confirm   # write it
```

## §4 OBSERVATION ROUTINE (what evidence to read)

Read the repository, not your assumptions. Useful, evidence-based sources per domain:

- **engineering** — git history + merged PR titles/bodies, review comments, `AGENTS.md` / `CONTRIBUTING.md`,
  linter/formatter config, test framework + scripts, CI workflow files, commit message shapes.
- **devops** — IaC layout, container manifests, pipeline definitions, environment promotion, runbooks.
- **product** — ticket/issue conventions, requirement templates, prioritisation labels, roadmap docs.
- **business** — pricing/commercial rules, compliance docs, contracts/SLAs.
- **design** — design tokens, component naming, accessibility target, handoff contract.

A convention is only recorded when it is **observed**, and the `Evidence & Sources` section records where.
When the host repo's own rules differ from a general default, the repo wins.

## §5 CHANGE SETS (ops)

`--ops` accepts inline JSON, `@path/to/file.json`, or `-` for stdin. A change set is an object with
`glossary` and/or `conventions` lists. Glossary ops: `insert` | `update` | `delete` (term identity is
case-insensitive). Conventions ops: `update_topic` | `insert_topic` (identified by topic title).

Every operation is validated against the current documents **before anything is written**: inserting an
existing term/topic, or updating/deleting a missing one, fails with `KNOWLEDGE_CONFLICT` and leaves the
file untouched. A malformed change set fails with `KNOWLEDGE_INPUT_INVALID`.

## §6 THE GATE (non-negotiable)

1. Build the change set and **preview it** — `che knowledge apply` (dry-run) prints a unified diff and
   writes nothing.
2. **Show that diff to the user** and ask **keep / alter / revert**.
   - **keep** → re-run with `--no-dry-run --confirm`.
   - **alter** → edit the ops and re-preview.
   - **revert** → stop; nothing was written.
3. After a successful apply, record it on the audit trail:
   `che decision_append <worktree> "KNOWLEDGE" "<op> <target>"`. The CLI writes the document; the skill
   owns the decision log, because it is the layer that has the bound worktree.
4. NEVER hand-edit `glossary.md` or `conventions.md` — every write goes through `che knowledge apply`.
5. If there is no knowledge yet and nothing new to record, this step is a **no-op**: skip it silently.

## §7 NON-GOALS

- No database or RAG index of conventions; no continuous background inference (phase boundaries only);
  no per-worktree glossary; no web UI; no translation of the documents; no CI enforcement — the
  knowledge is **consumed by the agent**, not imposed by a machine gate.
