---
name: light-citation
description: Verify scholarly references and claim-citation support for Light stage 10. Use when auditing a manuscript, claim map, bibliography, DOI/arXiv/PMID/ISBN/URL, BibTeX/CSL, citekeys, chimeric or fabricated citations, retraction/correction alerts, or preparing a canonical citation registry for typesetting. Builds provenance-preserving inventories, confirms metadata with independent authoritative sources, distinguishes CONFIRMED/CONFIRMED-MISSING/UNAVAILABLE/UNRESOLVED, records Crossref update direction, and emits the citation gate plus delivery artifacts.
---

# Citation — stage 10

Make every author-used reference traceable, real, correctly identified, and
honestly connected to the claim it is supposed to support. Treat formatting,
metadata existence, publication-integrity facts, and semantic support as four
different questions.

Read [`citation-resource-map.md`](citation-resource-map.md) before a full
manuscript audit. Read
[`references/registry_contract.md`](references/registry_contract.md) before
producing or consuming the canonical registry. Read
[`references/locator_audit.md`](references/locator_audit.md) before judging
claim support.

## Stage contract

- Consume paper-writing's `light.paper_claims.v1`, exact claim/source locators,
  current claim text hashes, reviewer-bound citation-support hashes,
  manuscript, figures/tables, supplement, and reference candidates.
- Reuse literature-search provenance as input evidence; independently verify
  the references the author actually keeps.
- Emit `light.citation_registry.v1`, BibTeX, CSL JSON, source-level evidence,
  failure records, claim-edge review, citekey audit, and
  `light.findings.v1(producer=citation)`.
- Keep stage 10's only critical gate `citation_verify`: confirmed missing works
  and chimeric citations. Metadata conflicts, unavailable sources, claim
  relevance, formatting, and publication-update alerts are warn/skip.
- Fix citation failures inside stage 10. `ROUTES` has no key 10; never invent a
  back-edge.
- Hand `references.bib`, `citekey-audit.json`, registry and `delivery.json` to
  typesetting. Typesetting compiles and checks keys; it does not re-decide
  authenticity. `delivery.json` must declare `status` and per-deliverable
  `sha256:` hashes so typesetting can reject stale or edited handoffs.

## Non-negotiable rules

1. Never invent a reference, DOI, author, year, venue, citekey, locator or
   support verdict.
2. Never call a network failure, rate limit, 5xx, authentication failure, or
   index miss “this work does not exist.”
3. Assign `CONFIRMED-MISSING` only when DOI Registration Agency explicitly
   reports non-existence and Crossref plus DataCite both return 404/410.
4. Assign `CONFIRMED` only when registration metadata and at least one
   independent field source confirm the work. Otherwise retain
   `UNAVAILABLE` or `UNRESOLVED`.
5. Preserve every source's title/authors/year/venue/identifier value. Select
   canonical fields from the registration agency; never use fuzzy matching to
   overwrite the original citation.
6. Treat a real DOI paired with conflicting title/authors/year as a possible
   chimeric citation. Multi-core-field conflict is critical; one ambiguous
   field mismatch is a warning for manual review.
7. Read publication updates in the correct direction: the affected original
   carries Crossref `updated-by`; the notice carries inverse `update-to`.
8. Record retraction/correction/expression-of-concern facts and alerts, then
   hand integrity judgment and wording to research-ethics. Do not rebuild its
   ethics gate.
9. Never equate metadata confirmation or “A cites B” with “B supports claim
   C.” `SUPPORTS` requires a locator-backed semantic review.
10. Keep the core path local/free or public/no-key. OpenAlex and keyed
    Semantic Scholar are optional coverage enhancements; commercial managers,
    institutional databases, and browser plugins are never required.

## Execute the author workflow

### 1. Inventory every reference occurrence

Use the claim map, manuscript, figures/tables and supplement together:

```bash
python scripts/citation_registry.py \
  --claim-map claim_plan.json \
  --draft paper.tex \
  --figure figure_notes.md \
  --supplement supplement.md \
  --refs-spec citation_input.json \
  --out-dir citation-delivery
```

Preserve `claim_id`, exact claim, claim locator, artifact path, occurrence
locator, citekey and raw identifier. Use
[`templates/citation_input.json`](templates/citation_input.json) when the
project has no reference spec.

### 2. Normalize without erasing versions

Normalize DOI, arXiv, PMID, ISBN and URL. Deduplicate exact works. Keep arXiv,
accepted manuscript, versioned dataset and published DOI as explicit versions
under one work only when the inputs establish the relationship. If not
established, keep them separate and mark the relationship unresolved.

### 3. Verify with independent sources

```bash
python scripts/verify_refs.py \
  --spec citation_input.json \
  --self-author Smith \
  --out verify.json
```

Use Crossref or DataCite as the registration source. Use PubMed, Semantic
Scholar, or configured OpenAlex as the independent field source. Keep each
endpoint, HTTP status, outcome, timestamp and returned fields in
`source_evidence`，并保存实际参与判定的 normalized-field SHA-256。Crossref polite-pool
email、OpenAlex/Semantic Scholar key 只用于请求，绝不写入 endpoint、registry 或日志。

Interpret status exactly:

| Status | Meaning | Action |
|---|---|---|
| `CONFIRMED` | registration source + independent field source | eligible for canonical BibTeX/CSL |
| `CONFIRMED-MISSING` | DOI RA explicit non-existence + Crossref/DataCite 404 | critical; replace or delete |
| `UNAVAILABLE` | transport/rate/auth/5xx prevents lookup | retry or use another free source |
| `UNRESOLVED` | partial evidence or second source incomplete | investigate; do not call verified |

### 4. Resolve field conflicts and chimeras

Compare the author's cited title, authors and year against registration
metadata. Inspect `field_conflicts` source by source. Keep the user's raw
citation unchanged until a human resolves the conflict.

Treat these as chimeric critical:

- real identifier plus conflicts in at least two of title/authors/year;
- title matches but the cited author list adds an author absent from the
  registered work.

Treat a single title translation, subtitle, year-online/year-print difference,
author omission or ordering issue as metadata warning unless corroborating
evidence establishes a chimera.

### 5. Record publication updates

Inspect `publication_updates`. Confirm relation direction with both the
affected work and notice DOI when the alert matters. Record type, notice DOI,
source and direction. Send those facts to research-ethics; do not label a
correction notice itself retracted because it has `update-to`.

### 6. Audit claim↔citation support

Use
[`templates/claim_citation_review.json`](templates/claim_citation_review.json)
and the original full text:

- `supports`: the cited locator supports the claim as written;
- `partial`: only a narrower statement is supported;
- `related_only`: same topic, but not evidence for this proposition;
- `unsupported`: the source contradicts or does not support it;
- `review_required`: full text/locator/reviewer is missing.

Each review must record `access`, a real non-placeholder `source_locator`,
`source_evidence_sha256`, `reviewer`, an already-occurred ISO `reviewed_at`, and
`reviewed_claim_sha256` for the exact claim text that was reviewed. The registry
also emits the current `claim_text_sha256`; the two hashes must match, otherwise
the review is stale and is downgraded to `REVIEW_REQUIRED`. `SUPPORTS` without
those fields, with a future `reviewed_at`, with a template/absolute/escaping
locator, or with a mismatched claim hash is downgraded to `REVIEW_REQUIRED` by
the registry/gate; metadata-only access can never support a claim. If access is only `ABSTRACT_ONLY`, `SUPPORTS` also requires
`support_scope=ABSTRACT_EXPLICIT` or `abstract_claim_explicit=true`; otherwise
the registry/gate downgrades it to `REVIEW_REQUIRED`. Check direction,
population, intervention, comparator, metric, time, modality, causal strength
and scope. Change the claim or citation when related-only or unsupported. Do
not promote an abstract-level heuristic to final support.

Normalize the four gates explicitly before delivery:

```bash
python scripts/citation_four_gate.py \
  --registry citation-delivery/citation-registry.json --as-of 2026-07-05
# 或仅调试模板合约:
python scripts/citation_four_gate.py \
  --input templates/citation-four-gate.example.json --as-of 2026-07-05
```

The public template is intentionally `UNKNOWN` and must exit 1. A later gate
can never repair an earlier failure: existence → identity → directed
publication status → locator-backed claim support. Prefer `--registry` so the
four-gate records are derived from the canonical registry rather than a hand
copied template. `ABSTRACT_ONLY` may be
direct only when the declared claim is explicitly present in the abstract;
metadata alone never supports a claim. Retracted work may document historical
record but cannot silently support a current conclusion.

### 7. Generate and audit delivery

Run the registry online after inputs are complete:

```bash
python scripts/citation_registry.py \
  --claim-map claim_plan.json --draft paper.tex \
  --refs-spec citation_input.json --online \
  --out-dir citation-delivery

python scripts/citekey_audit.py \
  --tex paper.tex --bib citation-delivery/references.bib --json
```

Only confirmed, non-chimeric works enter generated BibTeX/CSL. Preserve every
failure and unresolved review in separate artifacts. The generated
`delivery.json` is `DELIVERED` only when `citation-failures.json` and
`claim-citation-review.json` are empty and the citekey audit is OK; otherwise
it exposes `ERROR` or `REVIEW_REQUIRED`. Use `doi_to_any.py` for one-off DOI
content negotiation and formatting, not as proof of semantic support.

### 8. Run the gate and stage checkpoint

```bash
python scripts/citation_verify_gate.py \
  --registry citation-delivery/citation-registry.json \
  --tex paper.tex --bib citation-delivery/references.bib \
  --report citation_findings.json

python ../light-orchestrator/scripts/run_checkpoint.py \
  --file .light/passport.yaml --stage 10 \
  --findings citation_findings.json --write --ts <ISO-8601>
```

Expect `citation_verify_gate.py` to return exit 1 on a critical finding.
Repair the registry root cause, rebuild all derived artifacts, rerun the gate,
then rerun the same stage-10 checkpoint. Deliver only after the checkpoint
passes and passport records `delivered`.

## Script map

| Script | Responsibility |
|---|---|
| `citation_registry.py` | inventory, normalization, version grouping, verification orchestration, claim edges, registry/BibTeX/CSL/evidence/failure/delivery |
| `verify_refs.py` | authoritative multi-source fields, honest status machine, source evidence, conflicts, chimeras, Crossref update direction |
| `citation_verify_gate.py` | stage-10 findings producer; exit 1 on confirmed missing/chimeric |
| `citekey_audit.py` | manuscript ↔ `.bib` key audit; reused by typesetting |
| `doi_to_any.py` | DOI content negotiation and citation-format output |
| `verify_citation_edge.py` | paper A→B open-index relation; never claim support |
| `citation_four_gate.py` | ordered existence/identity/update/support contract with purpose-aware retraction handling; can derive records directly from `light.citation_registry.v1` |

## Resource boundaries

- `citation-resource-map.md`: executable order and resource tiers.
- `references/registry_contract.md`: machine artifact semantics.
- `references/locator_audit.md`: human semantic-support protocol.
- `references.md`: API/style/reference-manager details; load only the relevant
  section.
- `templates/*`: author input and review contracts.
- `assets/citation_checklist.md`: final human checklist.
- `docs/competitors/citation.md`: R1 evidence and comparative claims, not an
  execution guide.

## Completion check

- [ ] Inventory includes claim map, manuscript, figures/tables, supplement and
  reference spec provenance where present.
- [ ] DOI/arXiv/PMID/ISBN/URL are normalized; versions remain visible.
- [ ] Every confirmed work has registration plus independent source evidence.
- [ ] Every unavailable/unresolved source is honestly labeled.
- [ ] No confirmed-missing or chimeric work remains.
- [ ] `updated-by` direction is correct; notices are not inverted.
- [ ] Every core claim citation has a locator-backed review; related-only is not
  called support; every `SUPPORTS` edge has source evidence SHA-256, reviewer,
  non-future reviewed_at, matching `claim_text_sha256`/`reviewed_claim_sha256`
  and non-metadata access, with no template/absolute/escaping locator.
- [ ] Four-gate order passes; abstract/full-text access and historical/direct purpose are explicit.
- [ ] Four-gate input came from `--registry` unless there is a documented reason to use a hand-written fixture.
- [ ] Registry, BibTeX, CSL, evidence, failures, claim review and citekey audit
  were generated from one canonical state.
- [ ] `delivery.json` records status plus `sha256:` hashes for every
  deliverable consumed by typesetting.
- [ ] citation gate and stage-10 checkpoint pass.
- [ ] typesetting consumed the delivered BibTeX/citekeys.
