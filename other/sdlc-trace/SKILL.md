---
name: sdlc-trace
description: Invoked explicitly by /trace. Audits traceability across specifications, code and tests — every use case has a feature file, every scenario a tagged implementation and a verifying test — recomputes scenario hashes to detect stale specs, rebuilds the trace index, and writes one finding per violation.
argument-hint: "[FEAT-ID]"
disable-model-invocation: true
---

# /trace — traceability audit

This is where the trace tags stop being a convention and start being enforced.

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

**Phase inputs** — no phase of its own; runnable at any point. Outputs
`{{paths.trace_index}}` and rows in `{{paths.findings}}`. Read-only over the repository:
skip gate Step 4 (CHECKPOINT).

---

## Step 1 — Delegate to `trace-auditor`

Hand the audit to the `trace-auditor` agent. It runs `Read, Grep, Glob` only, on a small
model: the work is mechanical pattern matching over the whole repository, and it is the
one agent that can safely scan everything precisely because it cannot write.

Give it the resolved paths, the merged profile's `traceability` and `trace_tags`, and the
scope (a FEAT-ID, or the whole repository when no argument is given).

## Step 2 — Rebuild the index

Write `{{paths.trace_index}}` from the agent's `index_rows`, tab-separated:

```
scenario_id	uc_id	feat_id	requirement_ids	spec_hash	feature_file	impl_refs	test_refs	test_types	prompt_ref	status
```

The index is **derived**. Regenerate it wholesale; never hand-patch a row. What people
maintain is the tags in the source files — asking them to maintain a derived file is how
it stops matching reality and starts being ignored.

TSV rather than JSON or a markdown table: one line per fact, greppable, minimal diffs, no
quoting rules to remember when someone does need to read it in a pull request.

## Step 3 — Apply waivers

Read `{{paths.trace_waivers}}`. A row there suppresses its rule for its scenario, and the
index status becomes `waived`.

**An expired waiver is not honoured.** Report it as `major`. A waiver with no expiry
date is a permanent hole nobody revisits, which is why the column is required.

## Step 4 — Report violations

Apply the T1–T10 table from `.agent/rules/traceability.md` exactly — do not invent extra
rules and do not soften the listed severities.

The one that drives the loop is **T8 STALE-SPEC**: a scenario whose recomputed
`spec_hash` differs from the stored one means the code and tests behind it were built
against a different specification. Everything downstream of it is suspect until
regenerated. Report which artifacts those are, and suggest `/sdlc --blast {FEAT-ID}` to
see the scope before spending anything on regeneration.

For AI features, **T9 EVAL-GAP** catches a prompt version in the registry with no eval
set or no recorded run — a prompt whose quality has never been measured, which is the
whole failure mode the AI branch of this framework exists to prevent.

Report as a table: code, severity, scenario, location, detail. Then a coverage summary:

```
TRACE — {scope}
  Scenarios   : {n}
  Implemented : {n} ({pct})
  Tested      : {n} ({pct})
  Verified    : {n} ({pct})
  Stale       : {n}
  Violations  : {b} blocker / {m} major / {i} info
```

## Step 5 — Write findings

One row in `{{paths.findings}}` per T1–T9 violation, with a `route_to`:

| Code | route_to | Why |
|---|---|---|
| T1 ORPHAN-IMPL | `code` | the tag names a scenario that does not exist |
| T2 MISSING-IMPL | `code` | specified behaviour was never built |
| T3 MISSING-TEST | `tests` | built behaviour was never verified |
| T4 BAD-SOURCE | `code` | the tag points at a path that does not resolve |
| T5 UNTAGGED-ENTRYPOINT | `code` | changed entry point with no trace tag |
| T6 DANGLING-REQ | `srs` | a requirement no scenario covers |
| T7 ORPHAN-UC | `srs` | a use case with no specification |
| T8 STALE-SPEC | `srs` | the specification moved under its implementation |
| T9 EVAL-GAP | `techdoc` | a prompt version with no eval set or no recorded run |

Without a `route_to` the loop router cannot act on the finding, so it would sit in the
file forever.

## Step 6 — Record

Update the feature's `findings_open` counts and `current.yaml`. This command runs no gate
of its own; its results feed G4, G5b and G6.

---

## Boundaries

- **Do not add or fix trace tags.** Report the gap; `/gen-code` and `/unittest` fix it.
  A tool that silently tags code to make its own audit pass audits nothing.
- Do not create waivers. Only a person does that, with an owner and an expiry.
- Do not infer a link from a filename that merely looks related. A missing tag is a
  finding — guessing produces a trace index that is a comforting lie, which is strictly
  worse than an honest gap.
- Do not normalise mismatched ids. `PTK-001-UC1-SC1` and `PTK-001-UC1-SC01` are different
  identifiers and the difference is the finding.
