---
name: skill-audit
description: Explicit workflow for auditing Claude/Codex skill behavior, implementation, or historical autonomous routing. Invoke only with /skill-audit in Claude or $skill-audit in Codex; never load automatically.
disable-model-invocation: true
---

# Skill audit

Run this workflow only after `/skill-audit` in Claude or `$skill-audit` in
Codex. If it loads without the tool's explicit command form, do not apply it.

Use the request and `$ARGUMENTS` to select one mode:

- **Targeted audit:** inspect one or more named skills, their resources, or a
  proposed keep, split, merge, or hardening change.
- **Invocation audit:** reconstruct historical Codex skill use, separate
  explicit from autonomous use where the evidence permits, then audit the most
  important autonomous routes.

Do not use this skill for a broad agent-configuration audit, an ordinary code
or documentation review, or a single unexplained routing incident. Those belong
to `config-audit`, the relevant code or document audit, and `diagnose`,
respectively.

## Authorization and evidence

Default to read-only. Apply changes only when `--accept` is present or the user
explicitly asks to fix or improve the audited skills. Limit edits to
high-confidence, scope-preserving changes and their directly required tests,
metadata, and documentation.

Do not present reconstructed invocation counts as native telemetry. This
collector uses supported rollout reads and announcements, not native invocation
telemetry. Report the evidence window, confidence, coverage gaps, and ambiguous
cases.

## Targeted audit

1. Resolve every target exactly. Use `bin/agent-skill` when available. If a
   skill has Claude and Codex copies, inspect both unless the request narrows
   the tool.
2. Read `SKILL.md`, inventory its directory, and open only the resources needed
   for the audit.
3. Read [references/artifact-audit.md](references/artifact-audit.md) and apply
   its behavior-focused checklist.
4. In normal mode, report findings without modifying files.
5. In accepted fix mode, keep intended pairs synchronized, run focused checks
   and realistic positive and near-miss evaluations, inspect the diff and
   status, and commit only the scoped change when repository rules require it.

## Invocation audit

1. Record a UTC cutoff before reading any target skill. Prefer the timestamp of
   the request that started the audit; otherwise record the current time.
2. Read [references/invocation-audit.md](references/invocation-audit.md).
3. Run `scripts/audit_invocations.py` from this skill directory against a
   fixed session root and cutoff. Use JSON output when another check will
   consume the results.
4. Reconcile totals, inspect every ambiguous high-frequency case, and rank
   skills by confirmed autonomous invocations. Do not force uncertain evidence
   into the autonomous bucket.
5. Audit the highest-impact routes with the targeted workflow. Test fresh-agent
   should-trigger and should-not-trigger prompts before changing descriptions
   or invocation policy.
6. Report the inventory results separately from the skill-quality findings so
   a reader can distinguish observed use from your judgment.

## Completion report

For a targeted audit, lead with impact-ranked findings, then state strengths,
the smallest coherent revision, and verification. For an invocation audit,
lead with counts by classification and confidence, then coverage limits,
ambiguous evidence, prioritized routing findings, and verification.

After accepted fixes, include the changed files, commit hash, checks performed,
and any deferred recommendations. Preserve unrelated worktree changes.
