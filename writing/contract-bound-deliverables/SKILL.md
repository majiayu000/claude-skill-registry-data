---
name: contract-bound-deliverables
description: >-
  Assemble a draft to an exact word or character count, required section numbering and citation
  rules. When a submission requires numbered clauses or sources per table row, freeze the admissible
  packet, combine drafts and verify the final document with the brief's counting rule. Not for
  report-claim-audit.
metadata:
  revision: "7"
  areas: "work-management,software-development"
  targets: "runtime-agnostic"
  summary: "meet a measurable brief: freeze the evidence packet, draft in parallel, assemble to the number, verify with the contract's own metric"
  summary_zh: "满足可度量契约：冻结证据包、并行起草、按指定词数/字符数装配、用契约自身的度量脚本验收"
  kind: "entry"
---

# Contract-bound deliverables

## Gates

- Find the owning project. If another writer is active, stop writing, do not commit, and report.
  Do not delete scratch work without file-level migration, reference and active-writer checks.
- Read the measuring rule verbatim before drafting. Apply the owning project's stricter recency
  window. Exclude inadmissible evidence explicitly and rerun a retrieval that used a looser window.
- Freeze the evidence packet as the **only permitted input**. Never invent or elevate evidence.
  Do not rewrite a frozen packet or versioned registry in place after drafts exist.
- Never silently substitute a model; label any direct-authored draft as such and preserve raw
  drafts and honest provenance. Registry entries name secret environment variables, not inline secrets.
- Assemble the final to the number; never re-prompt for it. A separately requested checked draft
  can use bounded same-model passes only with raw receipt and frozen evidence/citations/conditions.
- Verify with the contract's own authoritative metric, then independently measure the written file.
  Enforce both floor and cap. A stale result, private proxy, or provisioning probe is not acceptance.
- Stage explicit paths only; commit and push require separate authorization. Never force or push
  over remote divergence. Do not stage LFS-routed binaries without the LFS client.
- Verify recorded source hashes before commit. Read back every external write.

## 0. Pre-flight

Use this for countable acceptance (length, citation discipline, required numbering). Locate the
existing owner via keywords, history and registry; read its README and plan. Check mtimes and
`git status -s` for concurrent writes; even a same-byte rewrite can be evidence. On conflict read
the newest commit for any explicit handoff. Follow [pre-flight and publishing](references/publish.md).

## 1. Read the acceptance rule before writing a word

- Copy the contract's measuring rule verbatim into your plan: what is counted, what is *included*
  (title? headings? citation markers? reference list?), and the allowed range.
- Note whether the contract names its own authority (for example, "the character count of the file as
  a plain text editor shows it"). That decides the counting convention in step 5.
- **Take the recency window from the owning project, not from the brief's prose.** A brief saying
  "no material older than N years" may have been tightened by the project after earlier rounds (a
  stricter floor, a different start month). Read the project plan's current window and conform to
  the stricter reading. A retrieval round run under the looser interpretation is inadmissible and
  has to be re-run, and its out-of-window hits must be recorded as excluded — not silently dropped,
  and never left in the evidence map where a later draft can cite them.
- Fix the required section schema and numbering up front. Models invent their own numbering and it
  is expensive to retrofit.

## 2. Freeze an evidence packet

Gather sources into one `DELIVERABLE_PACKET` listing each allowed claim, its number/date/model/unit
and provenance, and explicit do-not-use records. Reject untraceable claims; grade installed,
prototype, trial and demonstrated evidence separately; require equally strong support for absence.
For merged evidence, label levels and run number provenance against the union without elevating
summary-level claims. After freeze, append evidence as an addendum with a new QA batch; version the
whole chain for a new deliverable or changed research constraint. Use the
[evidence packet procedure](references/evidence-packet.md) and, for multi-domain retrieval,
[resumable search batches](references/search-route-batching.md).

## 3. Draft in parallel

Give every model the same packet and schema; name drafts by gateway and model id. Rank by
verified numbers, specifics, citations, numbering and wording. Take the skeleton from the most
disciplined draft; good prose never outranks discipline. Add only packet-proven details. Measure
adoption by citation marker and surrounding claim, not keyword. For a new model, use a versioned
registry, check configured routes, capture identity/effort preflight and preserve generation
attribution. When running model drafts, read the
[generation harness](references/model-generation-harness.md) for registry, multi-turn and receipt
rules; follow only the reference for the model's registered transport.

## 4. Assemble to the number

Keep raw outputs intact. Fit the editorial merge with a section-by-section build script measuring
section and total lengths. Keep provenance metadata in a sidecar, not the counted file. For an
existing file, assert each exact replacement matches once before writing any. Cut low-value prose
instead of reference handles: compress titles if needed, but never drop report numbers, URLs or dates.
Log cuts in the sidecar. See [assembly in the evidence packet reference](references/evidence-packet.md).

## 5. Verify, then independently measure

Measure existing artifacts before optimizing. Run the project's measuring/QA script against every
draft and the final; enforce both floor and cap plus every citation, digit, section and wording
requirement. Independently measure the written file and report the exact count. Keep the report;
re-run after artifact or gate changes. If citations change to simple sourcing, enforce no marker
residue. Document whitespace exceptions for captured text; never reformat source to silence QA.
Report provisioned vs probed vs accepted; only the real route with a passing artifact is accepted.
See [verification details](references/evidence-packet.md) and [pitfalls](references/publish.md#pitfalls).

## 6. Publish the deliverable and its evidence

Keep unrelated changes and timestamp-only churn out of the commit. Before any authorized push,
fetch and confirm fast-forward; after publishing, compare the remote SHA and read the files back
through authenticated access, not unauthenticated raw URLs. Keep blocked binaries on disk and
record retention and hashes. Follow [publishing](references/publish.md) for commands, LFS and pitfalls.

## Supporting files

- [Evidence packet](references/evidence-packet.md): schema, provenance, draft comparison, assembly and QA.
- [Search-route batching](references/search-route-batching.md): themed resumable retrieval and date windows.
- [Model generation harness](references/model-generation-harness.md): when running model drafts or
  adding a model to the registry.
- [Pre-flight and publishing](references/publish.md): writer detection, migration, LFS and read-back.
- [Configuration keys](references/configuration-keys.md): keys and defaults; see
  [configuration](references/configuration.md) for resolution order. Project bindings belong in a profile.
