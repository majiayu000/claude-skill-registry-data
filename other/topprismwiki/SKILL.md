---
name: topprismwiki
description: Route TopprismWiki enterprise knowledge governance workflows for evidence-aware preview, formal update, query, context, graph, batch status, diagnostics, and source governance. Use when a user asks to update or inspect a governed TopprismWiki knowledge base.
---

# TopprismWiki

TopprismWiki is an evidence-governed knowledge layer for Agentic AI. This
package exposes
one entry skill; the files under `subskills/` are internal modules and must not
be installed or presented as peer Skills.

## Routing

- For approved chat or document updates, read the matching
  `subskills/topprismwiki-formalize-*/SKILL.md` file and use the deterministic
  runner in `scripts/`.
- For formal knowledge queries, read `subskills/topprismwiki-query/SKILL.md`.
- For bounded task context, read `subskills/topprismwiki-context/SKILL.md`.
- For formal or candidate relationships, read `subskills/topprismwiki-graph/SKILL.md`.
- For batches, watermarks, isolates, or health, read
  `subskills/topprismwiki-status/SKILL.md`.
- For source approval, exclusion, readmission, retry, or validation, read
  `subskills/topprismwiki-governance/SKILL.md`.
- For an error, blocked command, or unexplained batch, run `diagnose` and read
  the matching section of `docs/zh-CN/troubleshooting.md` or its English mirror.

Before routing, identify whether the request is read-only, a formal update, a
source-governance action, or a diagnostic request. Read the
[capability matrix](references/capability-matrix.md) and do not present
`adapter-required` or `not-yet-supported` behavior as built in.

Do not present a Workspace candidate, raw message, or document mention as a
formal fact. Formal Vault changes require explicit update intent, a hash-bound
review package, a dry-run, an atomic commit, and post-commit validation. The
agent never edits the Vault directly outside the runner.

Global invariants:

- Formal Vault is the default fact layer; Workspace evidence, candidates and
  raw messages must be labelled and never silently promoted.
- No worker, model or child module writes `vault/wiki` directly. Formal changes
  require a reviewed, hash-bound package and the deterministic Runner.
- Group names, member lists, filenames, co-occurrence and one-off brand
  mentions do not establish customer, project, delivery, adoption or person
  relationships.
- Missing, ambiguous, conflicting or unprocessable evidence is isolated with a
  reason. Do not fill gaps with inference.
- Never expose credentials, raw private evidence or unrestricted absolute paths
  in Markdown, logs, dashboard output or GitHub Issues.

## Runtime

Run commands from the public package or an installed copy of this skill:

```bash
python3 scripts/topprismwiki.py doctor --capability all --project /path/to/wiki
python3 scripts/topprismwiki.py preview --source all --project /path/to/wiki
python3 scripts/topprismwiki.py update --source all --authorized --project /path/to/wiki
python3 scripts/topprismwiki.py query "project status" --project /path/to/wiki
python3 scripts/topprismwiki.py context "prepare a customer review" --budget 6000 --project /path/to/wiki
python3 scripts/topprismwiki.py graph "demo-project" --include-candidates --project /path/to/wiki
python3 scripts/topprismwiki.py batch list --project /path/to/wiki
python3 scripts/topprismwiki.py dashboard build --project /path/to/wiki
python3 scripts/topprismwiki.py diagnose --project /path/to/wiki
```

`preview`, `query`, `context`, `graph`, `status`, `batch`, `dashboard`,
`validate`, and `diagnose` are read-only with respect to the formal Vault.
`retry` and source governance update only private ledgers. `update` is the only
command that may commit reviewed facts, and it requires `--authorized`.

Read [references/architecture.md](references/architecture.md) for data
boundaries and [references/dependencies-and-routing.md](references/dependencies-and-routing.md)
before operating a source-specific workflow. The examples under `examples/`
are synthetic and must not be replaced with real company data in a public
repository.

For installation and the first runnable demo, read
[`docs/en/getting-started.md`](../../docs/en/getting-started.md) or
[`docs/zh-CN/getting-started.md`](../../docs/zh-CN/getting-started.md). For an
error, run `diagnose` and search the matching code in the bilingual
troubleshooting guide.
