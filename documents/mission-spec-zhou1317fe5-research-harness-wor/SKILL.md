---
name: mission-spec
description: Use when a mission starts from a natural-language request, a draft canonical spec, or a Markdown document without mission frontmatter and the agent must discuss requirements, write an approvable spec, record explicit approval, and hand the approved document to execution.
---

# Mission Spec

Own requirement discussion and the `draft -> approved` spec transition. Do not implement the work and do not write a separate implementation plan.

Declare: `使用 mission-spec skill，讨论并生成可批准的 canonical spec。`

## Workflow

1. Read the request and the relevant repository context.
2. If `lite-arch-recall` is installed, run it only before a genuine architecture-bearing decision (hard-to-reverse system boundary, data ownership, protocol, persistence, or cross-module control-flow choice) against applicable `docs/adr/` records. Ordinary model/module iteration, hyperparameter changes, experiment setup, bug fixes, and CSV bookkeeping do not trigger ADR recall.
3. Ask one question at a time only while a material goal, constraint, scope boundary, or acceptance condition remains unresolved.
4. Present alternatives only when real alternatives exist. Recommend one and state concrete tradeoffs.
5. Once the design is determined, write a draft to `docs/specs/<YYYY-MM-DD>-<topic>.md`. Register its task pointer using the lifecycle command below so preparation survives compaction.
6. Run `python scripts/validate_spec.py <spec> --allow-uncommitted-approved` and fix every error.
7. Use explicit approval of the exact draft, or an existing explicit user delegation that covers this task and its decisions. For delegated approval, record the user's source reference and scope, set `approval_mode: delegated` and `approval_source`, and continue without asking again. Do not infer delegation from positive discussion or permission for another task.
8. After approval, set `status: approved` and add the current RFC 3339 `approved_at` timestamp with timezone. Do not change the approved body in the same edit.
9. For a genuine architecture-bearing decision, run installed `lite-arch` and print its required three-line decision block before creating, amending, superseding, or skipping an ADR. Do not create ADRs for ordinary scientific iterations or routine implementation choices.
10. Commit the approved spec and any draft ADR created by the optional gate before execution. Then run `validate_spec.py` without the allow flag to prove the approved file is committed and unchanged from `HEAD`.
11. Route the committed spec to `mission-approved-doc`, unless the user explicitly chooses ordinary direct implementation.

## Canonical format

Use exactly one scalar frontmatter block:

```yaml
---
mission: spec
status: draft
created: YYYY-MM-DD
---
```

After approval:

```yaml
---
mission: spec
status: approved
created: YYYY-MM-DD
approved_at: YYYY-MM-DDTHH:MM:SS+08:00
---
```

Required sections:

- `Goal`
- `Scope`
- `Design`
- `Acceptance Criteria`

Add `Non-goals`, `Alternatives`, `Compatibility`, `Security`, `Rollout`, or `Rollback` only when they carry real information.

The validator accepts unique scalar fields `mission`, `status`, `created`, `approved_at`, plus optional `approval_mode` and `approval_source`. Existing four-field specs remain valid. `approval_mode` is `explicit` (default) or `delegated`; delegated approval requires a nonempty source reference and a description of its scope in the body. Nested values, arrays, aliases, tags, duplicate keys, invalid dates and extra frontmatter blocks remain invalid.

## Approval integrity

- Explicit approval applies to the exact draft the user saw. Delegation applies only within the user's stated task and scope.
- A later content change needs renewed approval. If existing delegation covers that change, revalidate and record the new `approved_at` under the same source; otherwise return to draft and request approval for the concrete changed content.
- A later session may trust an approved spec only when `validate_spec.py` confirms that it exists in `HEAD` and the working copy is unchanged.
- Never infer approval from positive discussion, implementation permission for another artifact, or a previous version of the document.

## Recoverable task pointer

After creating the draft, run from the project root:

```bash
python .agents/harness/workflow/mission_state.py register --task-id <SpecID> --spec docs/specs/<file>.md --source-ref <user-source-ref>
```

When the user changes task boundaries, add `--replaces <old-task-id> --reason <reason>` to register the new pointer and retire the old task in one write. Do not use replacement for intentionally parallel tasks. `issues/.missions.json` records task identity and lifecycle, not CSV row progress or scientific outcomes.
This local control file is Git-ignored so code branch changes cannot restore an old active pointer. Keep it with the current workspace when transferring an interrupted task.

## Writing boundary

Run `humanizer-zh` on prose before presenting or committing the spec. Do not let it rewrite frontmatter, code identifiers, paths, commands, dates, or machine-checked fields.

`mission-spec` produces and approves the spec. `mission-approved-doc` maps an approved spec into execution artifacts. `mission-csv-execute` owns execution state. Keep those responsibilities separate.
