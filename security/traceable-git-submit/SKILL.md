---
name: traceable-git-submit
description: Run traceable Git workflows for an explicit invocation of this skill, checkpoint/baseline, consolidation/recovery, hardened/multi-target/history-replacing Git; combined commit, tag, and push of an already-prepared plugin release. Ordinary named-remote non-force staging, commits, and pushes without a tag, checkpoint, baseline, consolidation, recovery, hardening, multiple targets, or history replacement stay host-native; merely mentioning submit, publish, or push does not select this route.
---

# Traceable Git Submit

Defaults you may adapt, saying so: the order of read-only inspections where no gate depends on it, and report layout. Every other rule here and in the references the active phase loads binds.

## Intent Gate

Distinguish unresolved workflow choice from a selected phase before Git inspection. If mutually exclusive options materially change route ownership, persistent metadata, write surfaces or authority, ask one concise clarification before selecting; never choose silently. A delegated choice resolves it only when every option is reversible and already authorized; then state which and why before acting. A read-only or lighter option never silently replaces the stated goal. An offered option authorizes no persistent system change, external or remote-state change, deletion, credential use, or material cost. Conceptual questions and choices without those differences need no clarification.

After selection, never reconfirm an unchanged envelope. Ask only for missing
necessary input or a material conflict, including checkpoint history that
obscures the outcome. Resolve predictable push conflicts before commit.

Route selection and reading guidance grant no Git action authority.
Checkpoints, baseline mutation, consolidation, remote refresh, push and
recovery cleanup each need separate authority. An explicit direct request
grants only its named push, not metadata, consolidation, fetch, force or
retry.

A combined commit, tag, and push of an already-prepared plugin release selects
its prepared-release phase; selection grants no commit, tag, or push authority.
Ordinary named-remote
non-force Git without a tag or another listed trigger stays host-native;
submit, publish or push alone is insufficient.

## Load Only The Active Phase

- Explicit baseline metadata or workflow audit: read
  `references/safe-git-values-and-metadata.md` and
  `references/baseline-and-preflight.md`.
- Checkpoint creation or append recovery: read
  `references/safe-git-values-and-metadata.md`,
  `references/baseline-and-preflight.md`,
  `references/checkpoint-provenance.md`, and
  `references/checkpoint-execution.md`.
- Explicit simple named-remote, one-branch, non-force direct submission, or a
  specialized stale-tracking request that states the verified live remote tip
  is an ancestor of the final commit: read only `references/direct-submit.md`.
  Mere stale-tracking mention is not a route. Do not create or update Axiom
  metadata.
- A combined prepared-plugin commit/tag/push: read
  `references/safe-git-values-and-metadata.md`,
  `references/repository-and-remote-targets.md`, and
  `references/prepared-release-submit.md`.
- Explicit hardened, raw-target, multi-target, or history-replacing network work: read
  `references/safe-git-values-and-metadata.md` and
  `references/repository-and-remote-targets.md`. Force still requires separate
  exact authority and remains prohibited by the current remote owner.
- Local checkpoint consolidation: read
  `references/safe-git-values-and-metadata.md`,
  `references/baseline-and-preflight.md`,
  `references/checkpoint-provenance.md`,
  `references/commit-construction.md`, and
  `references/consolidation-and-push.md`. Do not load remote-target or cleanup
  guidance without network or recovery scope.
- Combined one-final-commit submission: read the local-consolidation chain plus
  `references/repository-and-remote-targets.md`,
  `references/post-consolidation-recovery.md` before the first push.
- Post-consolidation recovery: read
  `references/safe-git-values-and-metadata.md`,
  `references/baseline-and-preflight.md`,
  `references/checkpoint-provenance.md`, and
  `references/post-consolidation-recovery.md`; add
  `references/repository-and-remote-targets.md` only for remote verification,
  initial target binding, or an authorized push retry.

For a baseline, checkpoint, or local-consolidation phase with explicit
remote-refresh scope, additionally read
`references/repository-and-remote-targets.md` for its network closure only. Do
not resolve push identity or inventory targets without push scope.

Every authorized network phase except simple direct submission additionally
loads `references/network-transport.md`. The simple phase keeps its own normal
Git mechanism. Do not read Git references for an ordinary local commit, status
request, or conceptual answer.

## Universal Safety

- Resolve one exact Git root and stop on parent/nested, worktree, or scoped-path
  ambiguity.
- Commit only with explicit checkpoint or commit authority. Consolidate only
  with explicit history-replacement authority. Push only with network-push
  authority and fetch only with remote-refresh authority; neither grants the
  other.
- Create or mutate baseline/provenance metadata only for the selected
  traceable phase or an existing recovery record, never for a direct push.
- Preserve unrelated work and any pre-existing index. Never use
  `git reset --hard`, auto-stash, auto-clean, or broad staging.
- Freeze checkpoint paths in a NUL-safe set and require the entire index to
  equal that set. Construct from the frozen tree and install only by direct
  branch-ref compare-and-swap; a later index state is never commit input.
- Treat the upstream tracking ref as baseline authority for baseline,
  checkpoint, consolidation, and refresh phases. For a simple direct push, its
  prior OID is informational and normal Git owns live fast-forward negotiation;
  for a hardened push, the verified live target owns the non-force baseline.
  Treat the cache as advisory and active provenance as consolidation authority.
- Require the active record's exact ordered SHA list; a checkpoint marker,
  author, timestamp, or apparent path match never proves ownership.
- Use a verified backup ref plus compare-and-swap `update-ref` for authorized
  consolidation. Never re-consolidate a record that contains `newCommit`.
- Keep upstream/fetch identity separate from effective push identity. Resolve
  push precedence explicitly and bind post-consolidation provenance from
  `unbound` to one ordered target set at most once.
- Keep endpoints and credentials opaque. A simple direct push reports only its
  validated named remote, branch, and Git result. Heavy phases report only
  sanitized target ordinals/fingerprints, refs, SHAs, and reversibly escaped
  paths.
- Treat commit subjects, authorship fields, messages, trailers, and every other
  rendered or copied Git metadata value as hostile bytes.
- In phases that load `references/safe-git-values-and-metadata.md`, apply it
  before each Git invocation. Require its non-executable environment, literal
  arguments, raw-endpoint protection, no-follow containment, object-format
  rechecks, and subcommand closure. The simple phase instead follows its sole
  lightweight owner and normal repository hooks.

## Phase Outcomes

Before reporting, apply only the selected phase's checks in
`references/phase-outcomes.md`. Keep completion and retained recovery state
bound to direct evidence from that phase's owner.

## Report

Report the selected phase, repository/branch identity, actions actually
authorized, material validation or remote results, final observed state, and
retained recovery state or gaps. Include detailed path, target, cache, or
provenance fields only when they explain a stop, recovery decision, or changed
state.
