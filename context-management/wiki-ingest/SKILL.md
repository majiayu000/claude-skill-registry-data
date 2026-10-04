---
name: wiki-ingest
description: Use when a PDF, URL, transcript, clipping, or raw note must become source-grounded, linked, governed knowledge in an Obsidian vault.
metadata:
  version: "8.1.0"
  updated: "2026-08-18"
  profile: "high-risk"
  assumes: "The source is accessible and the vault root plus write boundaries can be resolved."
  conflicts_with: "Invented provenance, modified immutable sources, unsupported concept promotion, or success claims without post-ingest checks."
---

# Wiki Ingest

<skill_contract>
  <input>Accessible PDF, URL, transcript, clipping, or note plus vault root, topic, provenance, permissions, and lifecycle context.</input>
  <output>Immutable source evidence, linked concept and entity updates, navigation and lifecycle changes, and a verified ingest receipt.</output>
  <done>Touched files pass source, link, block-ref, frontmatter, lifecycle, understanding, and read-after-write checks.</done>
  <non_goals>Fabricated provenance, source mutation, raw-summary dumping, unsupported rule promotion, or unverified completion.</non_goals>

Use STOW: **Source -> Transform -> Organize -> Write-back**. The source is evidence, the concept page is current understanding, and the log is the receipt. Load `references/stow-contract.md` for schemas and lifecycle details.

## Usage Template

Provide: source path/URL/note, vault root, intended topic, permissions, and whether the item came from a clipping queue. Optional: path config, prior canonical source, and desired behavior/skill candidate.

## Workflow

<intake>

1. Verify source existence, type, accessibility, date, and vault identity.
2. Resolve configured directories; record defaults only when no config exists.
3. Classify input as external fact, human experience, internal state, or environment signal.
4. Assign source risk based on primary/secondary/mediated/self-reported status and freshness.
5. Derive a source identity from canonical URL or source id, then hash/title/date
   fallbacks. Search canonical sources, concepts, and entities before creating
   files; record the identity query in the run ledger.

</intake>

<unknowns_gate>

If the source cannot be read, the vault is ambiguous, or provenance cannot be distinguished from mediation, return `NEEDS_INPUT` or `INSUFFICIENT_EVIDENCE`. Never fabricate author, date, URL, hash, source id, transcript text, or primary-source confidence.

</unknowns_gate>

<execute>

`wiki-ingest` owns one evidence-to-candidate transaction: immutable source capture, concept candidate, graph update plan, governance handoff, and clipping transition after verified commit. Cross-corpus deduplication, retrieval/index maintenance, and knowledge-debt queues belong to `knowledge-ops`; health scoring and generalized repair recommendations belong to `wiki-lint`.

1. **Source:** create or identify one immutable source note; preserve raw content and archive locators. Extract 3-7 key insights with stable block references. For concurrent ingest, stage the candidate, recheck the source identity immediately before commit, and promote only one canonical path.
2. **Transform:** separate direct claims, interpretations, contradictions, unknowns, and fast-changing facts. Mark single-source and self-reported claims.
3. **Organize:** update existing entity/concept pages when possible. New concepts require a thesis, mechanism, boundary, counterpoint, source locator, and at least two meaningful links.
4. **Understand:** answer what changed, what causes what, what this source may prove, what could make it wrong, and what reusable action follows. Raw summaries fail this gate.
5. **Navigate:** update the relevant index/map and clipping lifecycle. Machine-owned snapshot blocks remain untouched.
6. **Convert:** queue behavior, creativity, SOP, or skill candidates; apply the promotion gate before changing governed rules.
7. **Write-back:** append evolution timeline and ingest log entries; never
   rewrite historical provenance. Give every machine log entry an idempotency
   key derived from run/batch, operation, canonical source identity, and target;
   a retry must not append the same logical receipt twice.
8. **Verify:** run targeted link, source-ref, frontmatter, block-ref, empty-file,
   navigation, and post-write exact-identity checks over touched files. If a
   concurrent source appears, keep one canonical note, repoint derived links,
   and record reconciliation before claiming completion.

For material promotion or source ambiguity, require independent review and human approval. Prepare a rollback as a file-level diff; rollback may remove derived writes but must not erase original source evidence or logs.

</execute>

<evaluate>

Read touched files after write. Confirm the source exists, locators resolve, concepts pass the understanding gate, links are meaningful, clipping status is accurate, and logs match actual writes. Downgrade the result to partial when any required check is unavailable.

</evaluate>

<retry_policy>

`max_attempts: 2`. Retry only the failed stage after diagnosing path, parser, schema, or link cause. Change strategy before retry; stop on the same signature or `NO_PROGRESS`. Never duplicate source notes as a retry mechanism.

</retry_policy>

<state_contract>

Persist `{run_id, status, attempt, budget, evidence, unknowns, last_error, next_action}` plus source identity/risk, idempotency key, writer lease or compare-and-set evidence, vault fingerprint, resolved paths, touched-file ledger, created block refs, contradictions, reconciliation decisions, candidates, approval, clipping transition owner, and verification receipts. Source and log history are append-only.

</state_contract>

## Failure Protocol

- `NEEDS_INPUT`: source or vault identity is ambiguous; ask one minimal probe.
- `INSUFFICIENT_EVIDENCE`: the material cannot support the requested claim or concept.
- `BLOCKED_PERMISSION`: return proposed writes and paths without claiming mutation.
- `VERIFY_FAILED`: a post-ingest check fails; preserve evidence and repair only the failed stage.
- `NO_PROGRESS`: repeated failure signature after changed strategy; stop and queue review.
- `BUDGET_STOP`: persist coverage and remaining items. `max_attempts: 2`.

## Output Contract

Return `status`, `result` (created/updated/queued files and understanding delta), `evidence` (source and lint receipts), `unknowns`, and `next_action` including approval or rollback when relevant.

## Edge Cases

- A clipping duplicates an existing source: link/archive it and add only new provenance or block locators; do not create a parallel canonical source.
- Two workers discover no exact-URL match and race to create a source: the
  commit-time identity check selects one canonical note; remove only the
  uncommitted/staged duplicate, repoint derived links, and log reconciliation.
- A retry sees its write-back idempotency key in the log: verify the existing
  receipt and return reused/no-op instead of appending another entry.
- A mediated summary contains a precise changing number: preserve the summary, flag the number, and queue primary/current verification before promotion.

## Success Metrics

- Every derived claim traces to an immutable source locator.
- Concurrent retries converge to one canonical source and one logical receipt.
- Concepts add mechanism and boundary, not only summary.
- Touched files pass targeted lint and appear in navigation or an explicit queue.

## Quality Gates

- [ ] Vault, source, and permissions were verified before write.
- [ ] No provenance field or source content was invented.
- [ ] Source identity was checked before and after write; log append was idempotent.
- [ ] Understanding and promotion gates were applied.
- [ ] Independent/approval/rollback controls match the change risk.
- [ ] Post-ingest receipt matches actual filesystem state.

</skill_contract>
