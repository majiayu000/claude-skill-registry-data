---
name: sync
description: This skill should be used when the user says "sync the spec", "the client corrected the roles", "the spec and the documents disagree", "update macstack.json after the code changed", "reconcile the spec with reality", when lint reports rule 12.22, after anyone edits AUTOMATION.md or UX-UI.md, and as stage 3 of /macstack-dev:update and /macstack-dev:reconcile. Owns ONE file — it reconciles macstack.json against the client's documents on one side and the code on the other, and edits nothing else. For bringing the DOCUMENTS themselves up to date with the code, use the reconcile skill instead.
---

# Reconcile the spec with the documents and with the code

`macstack.json` sits between two things that both change without asking it: the
documents a client corrects, and the code a developer writes. This skill compares it
against each and reports every disagreement.

The two halves are not symmetrical and must not be run as one blur.

## The business half — documents → spec

`client/AUTOMATION.md`, `client/UX-UI.md` and `client/OVERVIEW.md` are **authored**: a
human writes them and the client corrects them. The business half of `macstack.json` is
the same facts in machine form.

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sync/references/sync-spec.py" macstack
python3 "${CLAUDE_PLUGIN_ROOT}/skills/sync/references/sync-spec.py" macstack --apply
```

Dry run by default. `--apply` writes only what it can write safely.

| From the documents | To the spec |
|---|---|
| roles, what they see and may do | `roles[]` |
| role tasks with their gates | `processes[].tasks[]` |
| triggers: name, type, schedule and the other settings | `triggers[]` name, type, config — the document's `source` bullet is derived from the `type` and has no field in the spec |
| which workflow answers which trigger | `workflows[]` name, triggers, implements |
| screens and their addresses | `interfaces[]` id, name, path, roles |
| goals and high-level processes | `goals[]`, `processes[]` |

**Changes:** values of items it matched — a task's gate, a trigger's schedule, a
screen's path, a role's sentence.

**Refuses:** creating or deleting anything. A new entity needs an **id**, and an id is a
decision: workflows, tests and prose all reference it. A machine that invents one is a
machine that silently orphans every reference the next time somebody renames the entity.
New and missing entities are reported; a human gives them ids.

This is also why a **rename shows up as one addition and one removal**. In v1 the
documents carried no ids at all and the two were genuinely indistinguishable. In v2 the
entity heading carries the id, so a rename of the *title* is now detectable and applied
— but a change of the *id* is still an addition plus a removal, and the report says so
rather than guessing.

## The technical half — code → spec

Not derivable from any client document and never written by the tool above: where a
workflow lives in the code, what engine runs it, which entities and software exist, what
is actually implemented. Those are the architect's, measured against the code.

Walk the project and compare:

- software, versions and instances against the manifests and compose files
- workflows against the files `workflows[].source` names (schema rev 15: the path from
  the project root to where the workflow lives in code) — a path that no longer resolves
  is an error, not a warning
- entities against the schema or the generated types
- infrastructure the code has and the client documents never will — a file store, a delivery
  log, a queue worker — gets `technical: true` on its `software[]`, `entities[]` or
  `workflows[]` record (schema rev 14), not silence and not a place in a client document
- interfaces against the routes
- `resources.accesses` against `.env.example`, and regenerate `.env.example` from the
  spec, never the other way round: the spec holds names, the env file holds values, and
  a round trip in the wrong direction leaks one into the other
- `context.plugins` against the plugins actually enabled

Update `status` fields to what the code says. This is the one place `status` is allowed
to move without a human, because it is a measurement rather than an intention.

**Do not update `reviewed` dates here.** A sync proves the spec matches the code; it
says nothing about whether the client documents still describe the product. That is
`conformance`.

## Then

Regenerate the derived artifacts through `documents` — `ARCHITECTURE.md`, `INDEX.md`,
`README.md` — reconcile `lifecycle.open_questions` and `needs_from_client` pointers
against `client/OPEN-QUESTIONS.md`, and run `lint`.

Commit the spec **together with** the code change it describes. A spec updated in a
later commit is a spec that was wrong for the length of a review.

## When to run

After the client returns a package, after anyone edits the authored documents, after a
task is finished (`/macstack-dev:update` calls this), as stage 3 of
`/macstack-dev:reconcile`, and before a release. Lint calls
the business half too: a spec that disagrees with the document the client signed off on
is the failure this whole folder exists to prevent.