---
name: context-pack
description: "Builds bounded, export-authorized context packs for worker handoff or review."
---

# Context Pack

Use this skill when the agent needs to package repository context for another
agent, a long review, an architecture handoff, or an external LLM session.

The preferred external tool is Repomix when it is already available or the user
explicitly asks for it. Use `repomix --compress` for architecture handoffs,
large reviews, and external LLM sessions when compressed structure is more
useful than full implementation detail. Otherwise, use repository-native
commands such as `rg`, `git ls-files`, targeted file reads, and structured
summaries.

## When To Use

Use for:

- large repository handoff;
- architecture or migration planning;
- multi-agent review setup;
- bug reports that require a bounded source bundle;
- sharing code context outside the current session.

Avoid for:

- tiny tasks where direct file reads are clearer;
- repositories containing unreviewed secrets;
- user requests to dump private source into an external service without review.
- small implementation/debugging tasks where `rg`, symbol lookup, and targeted
  file reads produce better evidence than a repository pack.

For an explicit fresh-agent handoff, select original `pocock.handoff`; for
long-task compression, select original `context.context-compression` from the
opt-in `context-continuation` group. Read complete author instructions rather
than substituting a source pack for their procedure. The owner's compact
state template and freshness policy are in `templates/task-resume-checkpoint.md`
and `docs/task-continuation.md`. A checkpoint is not an export authorization.

## Context Selection

Include:

- an explicit allowlist of relevant source files;
- tests touching the behavior;
- public configuration and dependency manifests;
- route, schema, API, migration, or build files needed to understand the task;
- a short file tree and rationale.

Exclude:

- `.env`, auth, tokens, private keys, credentials;
- generated caches, build artifacts, lockfiles unless dependency resolution is
  part of the task;
- vendored or third-party code unless directly relevant;
- unrelated large files.

Resolve paths and symlinks before collection; reject files outside allowed
roots. Record the goal, base commit, uncommitted state, included file paths and
sha256 hashes, exclusions, and output hash. Check those hashes before reuse;
changed input makes a pack stale. A clean base commit alone is insufficient.
For a working snapshot, record whether each file differs from that commit.

## Repeated Worker Context

For repeated authorized requests, prepare a stable prefix with the opt-in
`scripts/context-cache.py` helper described in
[Context Cache](../../docs/context-cache.md). Keep the current task, patch and
volatile results after the stable prefix. Preserve complete selected author
text and check actual source hashes before reuse, including local changes.
Bind cache scope to the project and authorization boundary; changing a route,
scope or source invalidates reuse. A local identity does not prove a provider
hit or authorize export. Report hits only from returned usage metadata and keep
missing counts unknown. Verify the actual host adapter before activation.

## Repomix Workflow

If `repomix` is available and appropriate:

```bash
repomix --help
```

Prefer `--compress` for architecture or handoff context. Use the uncompressed
form when exact implementation details matter. Verify the installed version's
include/exclude flags or file-list support, then export only the allowlist;
never rely on the tool's default repository-wide scope. Inspect the produced
pack, not only the input filters, before sending it to a worker.

Repomix has no project initialization step. Before writing a pack, check whether
the requested output already exists and whether source files changed since it
was generated. Reuse an existing pack only when its scope and freshness match
the current request.

Prefer a user-requested path or a clearly generated local path for packs. Do not
leave a repo-local pack silently: report the path, scope, and whether it should
remain untracked.

If `repomix` is unavailable, produce a manual context pack:

```markdown
# Context Pack
## Goal
## Repository Facts
## Relevant Files
## Key Snippets
## Validation Commands
## Open Questions
```

## Safety

- Run or reuse secret scanning before exporting a pack outside the local
  machine.
- Run or reuse runtime-boundary checks before exporting a pack outside the local
  machine.
- Read-only access is not permission to export code. Verify destination and
  allowed data before export; use synthetic data for integration smoke tests.
- Do not copy HOME, the parent environment, auth configuration, private client
  repositories, or conversation history into a worker pack. Supply only
  necessary non-secret launch variables; use the destination provider's
  normal secret mechanism when explicitly authorized.
- Prefer summaries over full files when the recipient only needs architecture.
- Label generated context as stale once source files change.
- Pass task contents through stdin or a supported file, not shell interpolation
  or a large command-line argument. A worker receives the pack or a sanitized
  snapshot, never unrestricted access to the parent repository.

## Optional Flat-Data Encoding Experiment

Keep canonical JSON as the machine contract and raw artifact. A compact table
encoding such as ANAL is only an optional model-facing view of homogeneous
flat records, never a global replacement for JSON or the worker protocol.

Before adoption, round-trip strings, numbers, booleans, null, empty and missing
values, delimiters, quotes, newlines and Unicode without losing fields or
types. Reject unsupported nested objects/arrays; do not flatten them silently.
Measure the actual corpus with an explicitly named tokenizer, including format
instructions and decoding overhead, and compare task accuracy as well as size.
Bytes are not tokens; a tokenizer proxy is not provider billing evidence.
If losslessness or end-to-end quality is unverified, leave the encoding as an
experiment and continue passing JSON. Preserve failing fixtures and results.

## Output

Report:

- pack target path or summary;
- included/excluded scope;
- secret/runtime boundary check;
- token or size concerns when known;
- remaining context gaps.

Measure bytes separately from tokenizer-derived tokens. For comparisons, keep
the tasks and included scope equivalent; record calls, elapsed time, available
usage and cost per worker, parent tokens separately, and unknown values. Do not
claim token or cost savings from byte counts alone. Preserve raw evidence and
return compact findings using `subagent-result-merge`.
