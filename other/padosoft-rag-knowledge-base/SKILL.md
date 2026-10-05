---
name: padosoft-rag-knowledge-base
description: >-
  Use this skill when designing or changing the corpus a model retrieves from — the document store, the
  chunk table, identifiers, statuses, the promotion of knowledge into it, the graph of relations between
  documents. Also when the user reports that a document could not be deleted, that the same file was indexed
  twice, that retrieval grounds answers on an outdated or unreviewed page, that two projects collided on an
  identifier, or asks how a model should be allowed to write into the knowledge base. It covers the
  idempotency anchor, canonical typing, the human gate on promotion, trust ordering at retrieval, and the
  delete path. Do not use it for permissions and ingestion trust (padosoft-rag-ingestion-security) or for
  choosing an embedding model.
license: MIT
compatibility: >-
  Stack-agnostic. Examples assume a relational store holding documents and chunks alongside a vector index,
  which is the common shape; the rules about identity, promotion and deletion do not depend on it.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: A model may propose knowledge; only a human promotes it.
  profiles: ai, data
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: rag, knowledge base, canonical, retrieval, chunking, idempotency, promotion, graph, corpus
---

# RAG knowledge base

A corpus is not a folder of files with embeddings next to it. It is a store with an identity contract, a
lifecycle and a trust ordering — and the three defects that follow from not having them are always the
same: the same document indexed twice, a document that cannot be deleted, and an answer grounded on
something nobody approved.

**The rule: a model may propose knowledge; only a human promotes it. And everything the corpus holds carries
its identity, its status and its origin explicitly.**

---

## 1. One idempotency anchor, and everything hangs off it

```text
(tenant or project) + (source path) + (content hash)
```

Re-ingesting the same content is a no-op; changed content is a new version of the same document, not a
second document. Get this wrong and the corpus grows duplicates that all retrieve, so the model sees the
same passage three times and treats the repetition as agreement.

**Normalise the path through one function, and use it everywhere** — ingest, read, delete, the command line
and the HTTP surface alike. This is the rule people break by reimplementing the normalisation inline:

- separators unified, repeated separators collapsed, leading and trailing ones trimmed;
- relative segments **rejected**, not stripped — that is the traversal guard, and the inline version is
  always the one that forgets it;
- an empty result raises, and the caller surfaces it as a validation error rather than swallowing it.

**When ingest and delete normalise differently, a document becomes undeletable.** It was stored under one
spelling and is looked up under another; the delete reports *not found* and is believed. Prove it with a
test that ingests and then deletes the same payload.

## 2. Type the corpus inside the store you already have

Typed documents — a decision, a runbook, a standard, an incident record, a concept — want a stable business
identifier, a status, a priority and their own metadata. Add those as columns on the existing document
table; **do not build a parallel one**.

A second table means a double write and a split source of truth, and every retrieval path then has to know
about both. Nullable columns are cheap, existing consumers keep working, and retrieval keeps one query
surface.

Two consequences to enforce:

- **Identifiers are unique per tenant, never globally.** Two projects should be able to use the same slug —
  a codebase that assumes global uniqueness breaks the moment a second customer arrives.
- **Every query decides, deliberately, which flavour it wants.** A bare query by tenant returns a mix, which
  is right for ingestion and deletion and wrong for grounding. Give the intent a name — a scope — and use it
  instead of rebuilding the condition inline.

## 3. The human gate on promotion

The attractive version of this system is "every agent reads from the knowledge base and writes back to it".
It is also the version that makes the corpus untrustworthy within a month, and unauditable immediately.

Split it into three steps and give the model the first two:

1. **Suggest** — the model extracts candidate knowledge from a transcript, a review, an incident. Returns
   structure. **Writes nothing.**
2. **Validate** — a proposed document is checked against the schema. Returns valid or the list of errors.
   **Writes nothing.**
3. **Promote** — writes the document and queues the indexing. **Only a human or an operator command reaches
   this step.**

Every promotion writes an audit row with the actor, the event and the before and after. And the writer
checks the result of the write: a storage call whose return value is ignored is how a promotion reports
success on an empty file — see **`padosoft-failure-visibility`**.

## 4. Trust ordering at retrieval

Not everything in the corpus deserves the same weight. Rank by **curation**: human-approved above
machine-generated above raw. Give it a numeric priority the reranker can use, so the ordering is a
configuration rather than a branch.

**Curation is not provenance.** Curation asks *has a human vouched for this?*; provenance asks *who wrote
the original?* A human-approved summary of an external email is approved **and** externally authored. Keep
the two fields separate — collapsing them loses the one you will need — and see
**`padosoft-rag-ingestion-security`** for what the second one is for.

Statuses are a lifecycle, not labels: draft, in review, accepted, superseded, deprecated, archived. What
supersedes what is a relation, so a retrieval that returns the superseded version can say so.

## 5. The graph, if you have one

Relations between documents — supersedes, relates to, implements, contradicts — are worth modelling when
answers need to follow them. Two rules keep it from becoming a liability:

- **Every edge carries the tenant**, and the foreign keys are composite so the database refuses a
  cross-tenant edge. When that constraint fires it is a bug to fix, never an error to silence.
- **Deletion cascades.** A hard delete removes the document's nodes and, through the constraint, its edges
  in both directions. Any new delete path calls the one deleter or replicates the cascade — orphaned nodes
  are invisible until a traversal returns something that no longer exists.

## 6. What a chunk has to carry

A chunk is retrieved on its own and read without its document, so it carries what the answer needs to be
checkable: the document identity, the position, the version, and enough of a title or heading path to cite.
A chunk that cannot be traced back to a version of a source is grounding you cannot verify — see
**`padosoft-evidence-boundaries`**.

---

## Gotchas

- **Duplicate documents read as corroboration.** The model has no way to know it is seeing one source three
  times, and a reranker will happily put all three at the top.
- **"Not found" from a delete is believed.** It is the most commonly true-looking wrong answer in this whole
  subsystem.
- **A global unique identifier is a single-tenant assumption** that survives right up to the second customer.
- **Retrieval that ignores status grounds answers on drafts and rejected approaches**, and a rejected
  approach reads exactly like a recommendation once it is out of context.
- **Re-indexing everything to fix one document** is the reflex that hides the identity bug instead of
  exposing it.
- **A metadata block that is parsed at ingestion and never re-validated** drifts from the document it
  describes — see **`padosoft-docs-match-code`**.

## Checklist

- [ ] One idempotency anchor; re-ingesting identical content is a no-op
- [ ] Path normalisation in one function, used by ingest, read and delete alike
- [ ] Relative segments rejected; empty input raises; the caller surfaces it
- [ ] A test that ingests and then deletes the same payload
- [ ] Typed columns on the existing table, not a parallel one
- [ ] Identifiers unique per tenant; no assumption of global uniqueness
- [ ] Every query states which flavour it wants, through a named scope
- [ ] Promotion split into suggest, validate, write — the model stops before the write
- [ ] Every promotion audited with actor and before/after; write results checked
- [ ] Retrieval ranks by curation; curation and provenance kept as separate fields
- [ ] Statuses model a lifecycle, with supersession as a relation
- [ ] Graph edges carry the tenant; deletion cascades through one path
- [ ] Chunks carry enough identity to cite and to verify

## Final report

```
Corpus: <n> documents · <n> chunks · tenants <n>
Identity anchor: <fields> — duplicates found: <n>
Path normalisation: one function? <yes/no> — ingest/delete round-trip tested: <yes/no>
Canonical layer: <columns added / table> · uniqueness scope: <…>
Promotion: suggest <…> · validate <…> · write gated by <human/operator>
Retrieval ordering: <curation field and weights> · provenance kept separate: yes | no
Delete path: cascades <what> · orphans possible: <where>
```
