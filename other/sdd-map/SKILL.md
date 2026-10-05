---
name: sdd-map
description: >
  Produce a deterministic, read-only evidence map of the repository for SDD Composy
  (languages, manifests, commands, modules, boundaries, staleness) and publish the
  context bundle only on request. Use before a PRD or TechSpec, or when the map is
  stale — 'mapear o repositório', 'atualizar o contexto do código', 'what does this
  codebase look like for SDD'. Do NOT use for architecture decisions, code review,
  or repository exploration without an SDD workspace.
metadata:
  version: 0.1.0
---

# SDD Map

Create or inspect the SDD Composy codebase map. The bundled `scripts/sdd_map.py` helper owns
traversal, secret exclusion, deterministic serialization, and atomic publication; this skill owns
scope, approval, interpretation, and downstream routing.

Language: before writing human-facing prose, run `scripts/sdd_language.py <repo-root>` and use the persisted language; on `not_initialized`, return it with `next_action: run_init`. Localization rules: `references/language.md`.

## Inputs

- Repository root: the current repository unless the user supplies another real directory.
- Optional output directory: inside the repository, default `.planning/sdd-composy/context`.
- Optional request to publish. A scan is observation-only; publishing is the only permitted
  write and is limited to the context bundle.

Do not execute commands discovered in manifests, and do not modify source files, governance
files, task artifacts, or architectural plans.

## Procedure

1. Resolve and validate the repository root and output directory without changing files.
2. Run the read-only scan and present its JSON result, preserving `source_commit`,
   `mapped_commit`, `observation_only`, confidence, observed languages, manifests, commands,
   modules, boundaries, domain evidence, and staleness. Commands in the result are evidence
   only; never run them.

   ```sh
   python3 "<plugin-root>/scripts/sdd_map.py" --repo-root <repository-root> [--output-dir <context-dir>]
   ```

3. Only when the user explicitly requests publication, repeat with `--write` (and the exact
   `--output-dir` when supplied). Publication writes only `codebase.json`, `project.md`,
   `stack.md`, `domain.md`, and `pitfalls.md` under the context directory. Report those paths
   and the recorded source commit.
4. Check `staleness.stale`. A stale prior map is not valid downstream evidence: report the
   previous and current commit and refresh before routing. A missing or unknown commit is an
   uncertainty to report, not permission to invent one.
5. Route a fresh map to the next approved lifecycle stage: PRD first, then STORIES, TECHSPEC,
   and TASKS as applicable. Those stages interpret the evidence under their own human gates;
   a map never turns file observations into unapproved architecture.

## Read when

- `references/mapping.md` — publishing the bundle, or interpreting the output schema and
  staleness record.

## Output

Return the helper JSON or a faithful summary, publication status, output paths, source commit,
the `observation_only` field, staleness status, and the next lifecycle stage.

Safety: Do not commit, push, or publish. Do not read or expose `.env`, credentials, tokens, private keys, certificates, or fleet environment files. Full contract: `references/safety.md`.
