---
name: wiki-lint
description: Use when an Obsidian wiki needs a reproducible health audit for structure, provenance, links, understanding, lifecycle, and promotion readiness.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "stateful"
  assumes: "The vault is readable and configured paths can be discovered or supplied."
  conflicts_with: "Mutating immutable source notes, silently deleting content, or reporting health without scan evidence."
---

# Wiki Lint

<skill_contract>
  <input>Vault root, path configuration, audit scope, exclusions, prior baseline, and explicit repair authorization if any.</input>
  <output>A reproducible, severity-ranked wiki health report with file-level evidence, debt queues, and bounded repair proposals.</output>
  <done>All twelve checks record scope and receipts, findings are reproducible, and report-only mode leaves content unchanged.</done>
  <non_goals>Silent deletion, immutable-source mutation, unapproved repair, semantic rewrite, or health claims without scan evidence.</non_goals>

Audit the wiki as a governed knowledge graph. Report prioritized, reproducible findings; make no content mutation unless separately authorized.

## Usage Template

Provide: vault root, optional path config, audit scope, prior report, and whether repairs are authorized. Default to report-only.

## Workflow

<intake>

Resolve configured source, concept, entity, clipping, daily, system, and log paths. Record scan timestamp, file count, exclusions, and prior baseline. Fail closed if the supplied path is not the intended vault.

</intake>

<unknowns_gate>

If the vault root or path semantics are ambiguous, return `NEEDS_INPUT` before scanning or writing. Missing optional directories are findings; inaccessible required directories are `BLOCKED_PERMISSION`.

</unknowns_gate>

<execute>

Run twelve checks and preserve file-level evidence:

1. required frontmatter and stable identifiers;
2. broken wikilinks and unresolved embeds;
3. source references and block locators;
4. orphan concepts and isolated entities;
5. duplicate titles or semantic duplicates;
6. stale notes and unresolved contradictions;
7. single-source or weak-provenance claims;
8. concept structure and understanding-gate integrity;
9. clipping archive and source lifecycle;
10. permission, immutable-source, and human-approval boundaries;
11. daily-loop receipts and flywheel write-back;
12. V8.1 promotion-gate readiness for proposed rules.

Classify `P0` integrity loss, `P1` broken provenance/navigation, `P2` debt, and `P3` improvement. Prefer deterministic checks; label semantic judgments separately.

</execute>

<evaluate>

Re-scan a sample of findings, deduplicate root causes, and compare counts with the prior baseline. A report is invalid if paths, scan scope, or reproduction details are absent. If repair was authorized, run the relevant check again after each bounded repair.

</evaluate>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus vault fingerprint, scan scope, finding ledger, severity counts, baseline delta, authorized repairs, and receipts. Never overwrite the prior report.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: vault identity or configured path semantics are unclear.
- `BLOCKED_PERMISSION`: required files cannot be read or an authorized report cannot be written.
- `VERIFY_FAILED`: a finding cannot be reproduced; downgrade or remove it.
- `BUDGET_STOP`: scan budget ends; return coverage and the unscanned queue rather than a whole-vault claim.

## Output Contract

Return `status`, `result` (severity-ranked findings and health summary), `evidence` (paths, checks, counts, samples), `unknowns` (coverage gaps), and `next_action` with owner and cheap verification.

## Edge Cases

- A concept is intentionally unlinked during drafting: classify it as debt with age/context, not a P0 defect.
- A source note has malformed metadata but is immutable: report the issue and propose an overlay/index repair; do not edit the source.

## Success Metrics

- Every P0/P1 finding is reproducible from a path and check.
- Coverage, exclusions, and baseline delta are explicit.
- Repair recommendations preserve provenance and include a cheap check.

## Quality Gates

- [ ] Vault identity and scan scope are verified.
- [ ] Deterministic and semantic findings are separated.
- [ ] No immutable source was changed without authorization.
- [ ] Report-only versus repair mode is explicit.

</skill_contract>
