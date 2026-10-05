---
name: padosoft-rag-ingestion-security
description: >-
  Use this skill when content is brought into a corpus that a model will read — a connector to a document
  store, a mailbox, a ticket system, a wiki, an upload, a crawl — and whenever the question is who may see
  what came in. Also when the user reports that an assistant surfaced a document somebody should not have
  seen, asks how to mirror the source's permissions, worries about content written by outsiders reaching a
  tool call, or needs personal data kept out of an index. It covers the ingestion contract, permission
  mirroring that fails closed, authorship provenance, the indirect-injection chain, and redaction before
  embedding. Do not use it for choosing an embedding model, for retrieval quality, or for the shape of the
  corpus itself (padosoft-rag-knowledge-base).
license: MIT
compatibility: >-
  Stack-agnostic. Written for a multi-tenant assistant with pluggable connectors and a vector store; the
  reasoning applies to any pipeline that turns somebody else's documents into grounding.
metadata:
  version: 0.1.0
  author: Padosoft
  summary: The ingestion contract records what a document is, not where its authority comes from.
  profiles: ai, api
  scope: project
  repository: https://github.com/padosoft/skills
  keywords: rag, ingestion, connectors, acl, oversharing, provenance, prompt injection, pii, redaction
---

# RAG ingestion security

Ingestion looks like a data problem and is an authorisation problem. **The contract records what a document
*is* — path, title, type, tenant — and not where its authority comes from.** There is nowhere to put the
fact that it was shared with three people, so it arrives readable by everyone with access to the corpus.

That is oversharing, and it is the headline failure of enterprise assistant rollouts. The second failure
shares its cause: nothing records **who wrote** the content either.

---

## 1. Mirror the source's permissions, or say that you did not

A connector reports **what the source said**; it never decides who may read. The distinction is the design.

```text
principals (type + external id + allow/deny)
inherits_from_parent: bool      folder or space inheritance
complete: bool                  false = the source truncated the list
```

The host maps external principals to internal subjects — by verified address, directory link, group
mapping. That resolution depends on directory state the connector does not have, which is why it is not the
connector's job.

**And it will sometimes fail**: an external collaborator, a group the directory does not know, a truncated
list.

## 2. Unmapped access fails closed. This is the load-bearing rule

**A document whose access could not be fully mapped must not fall back to corpus-wide visibility.** That
fallback is exactly the bug this whole design exists to remove, and it is the tempting shortcut every time.

Store it in a restricted state — readable only by the owner of the connector installation — until an
operator triages it. **This makes some documents invisible that were visible yesterday. That is the point,
not a regression**, and saying so up front is what keeps it from being reverted in the first week.

## 3. Mirrored permissions have to be revoked, not only granted

- Keep the **origin** of every permission row: mirrored from the source, or set by hand. A re-sync
  reconciles the mirrored ones and must not destroy an operator's manual grant.
- **When a source removes a share, the reconciliation deletes the mirrored row.** A mirror that only ever
  adds is a slow leak, and it leaks in the direction nobody is watching.
- Record an unresolved principal **as an unresolved principal** rather than discarding it. The row is the
  evidence that access was intended for somebody, and it is what an operator triages later.
- Deny wins over allow, wherever both apply.

## 4. Authorisation belongs inside the query

The retrieval path is a hot path, and it does not call your policy object. Push the allow-list into the
query — the same predicate the rest of the application uses — so retrieval gets authorisation **for free
and by construction** rather than as a filter somebody remembered to add after the results came back.

A decision made after retrieval is a decision that can be skipped by the next code path that queries
directly. See **`padosoft-tenant-isolation`**.

## 5. Provenance: who wrote this, and do we trust them?

```text
trusted-internal · untrusted-external · machine-generated
```

Most connectors bring in content written inside the organisation. **A mailbox connector brings in content
written by anyone who can send an email.** That message becomes a document, the document becomes chunks, the
chunks become grounding — and the same platform exposes tools an agent can call. That is a complete
**indirect-injection chain**: attacker-controlled text reaching a tool-calling context, with no boundary
between the two ends.

- **Ship the label before the enforcement.** A provenance column and a contract method are cheap, and they
  immediately answer a question nobody can answer today: *how much of our corpus is externally authored?*
  Labels without enforcement are still worth having — they make the enforcement testable before it exists.
- **Then enforce the asymmetry**: an untrusted chunk may be **quoted in an answer** and must **never
  influence a tool call**. A tool invocation whose arguments derive from untrusted grounding needs an
  explicit policy or a human confirmation. See **`padosoft-agent-host-boundaries`**.
- **Provenance is not curation tier, and collapsing them loses information.** Curation asks *has a human
  vouched for this?*; provenance asks *who wrote it?* A human-approved page summarising an external email is
  **both** approved and externally authored, and both facts matter at different moments.

## 6. Personal data: redact before embedding

Once a value is in the vector store it is in every backup, every index and every answer. So the redaction
runs **at ingestion, before the embedding**, not at display time.

- **Deterministic surrogates**, so the same value always yields the same token and search still works — a
  search for a person's ticket still matches.
- **Two strategies**: one-way masking, and reversible tokenisation with a vault. The vault is **per tenant,
  with a per-tenant salt**, so the same value in two tenants produces different tokens and nothing
  correlates across them.
- **One redaction core for every ingestion path.** A pipeline path and a direct path that redact separately
  will diverge, and the contract *no raw personal data in the index* has to be path-independent.
- **Redact the chunk, not the source.** The original stays as the idempotency anchor and keeps its metadata
  parseable — see **`padosoft-rag-knowledge-base`**.
- **A dry run uses the one-way strategy**, so a preview never writes to the vault.
- **Re-identification is a privileged, audited operation**, and stricter still when exposed as a tool a
  model can call. Every unmask and every denied attempt writes an immutable audit row that records **counts,
  never the values**.

## 7. Extending the contract without stranding anybody

The ingestion contract is public API for every connector, including the ones other people wrote.

- **Add optional capability interfaces**, never a required argument. A connector implementing neither
  behaves exactly as before.
- Carry the new data in the **extension channel that already exists** — the metadata map — written and read
  through helpers, so no call site handles the key by hand.
- **An optional trailing parameter is not additive for implementers.** Callers are fine; a class that
  *implements* the interface with the old signature fails at declaration time, before any of its code runs.
  That is the compatibility you were trying to preserve, broken by the mechanism chosen to preserve it. See
  **`padosoft-contract-changes`**.

---

## Gotchas

- **Nothing in the code is wrong when oversharing happens.** The contract simply had nowhere to put the
  permission, so no reviewer sees a mistake.
- **A connector that reads permissions but ingests them as "allow everyone" on failure is worse than one
  that reads none**, because it looks solved.
- **The retrieval path is the one that skips the policy**, every time, in every codebase.
- **A summary of untrusted content inherits its provenance**, and a human approving the summary does not
  change who wrote the original.
- **Determinism in redaction is a privacy trade**: identical surrogates make search work and make frequency
  analysis possible. Per-tenant salting is what keeps it acceptable.
- **The audit trail of a re-identification must not contain what was re-identified.**

## Checklist

- [ ] The connector reports principals and completeness; it makes no access decision
- [ ] Unmapped or truncated access fails **closed**, into a restricted state with an owner and a triage path
- [ ] Permission rows carry their origin; re-sync reconciles mirrored rows without destroying manual ones
- [ ] Revocation implemented and tested, not only granting
- [ ] Authorisation enforced inside the retrieval query
- [ ] Provenance tier assigned at ingestion; labels shipped before enforcement
- [ ] Untrusted grounding may be quoted, never influence a tool call without policy or confirmation
- [ ] Provenance kept separate from curation tier
- [ ] Redaction before embedding, deterministic, one core for every path, chunk not source
- [ ] Vault per tenant with a per-tenant salt; re-identification privileged and audited without values
- [ ] Contract extended by optional capability interfaces; no implementer stranded

## Final report

```
Connectors: <n> — with ACL mirroring: <n> · with provenance: <n>
Unmapped policy: <what happens> · documents currently restricted-unmapped: <n>
Revocation: implemented | not (leak direction: <…>)
Enforcement: in-query | post-filter (where)
Provenance: labels <shipped?> · enforcement <phase> · untrusted corpus share: <%>
Redaction: strategy <…> · vault <per-tenant salt?> · paths covered: <list>
Contract changes: <what was added, and how implementers stay valid>
```
