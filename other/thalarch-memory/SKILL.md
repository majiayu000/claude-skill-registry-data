---
name: thalarch-memory
description: >
  Retrieves, classifies, validates, and optionally persists compact durable knowledge so future tasks
  can reuse verified experience without treating memory as current truth. Use when prior project
  decisions, recurring failures, user-authorized workflow preferences, or general engineering lessons
  could materially improve a task. Separates IGNORE/SESSION/PROJECT/GENERAL memory, revalidates
  load-bearing memories against current evidence, prevents sensitive-data and chain-of-thought
  persistence, and prefers small retrieval capsules over context dumps.
---

# Thalarch Memory

Memory is a **retrieval aid**, not an authority layer. Current user/repository/runtime evidence wins.

Core invariant: **current repository/runtime evidence wins over retrieved memory**.

## 1. Four memory classes

Classify every candidate before persistence:

- `IGNORE` — task noise, obvious facts, duplicated information, weak guesses, transient logs;
- `SESSION` — useful only for the active task/session; keep in the evidence ledger, not durable storage;
- `PROJECT` — stable knowledge specific to one repository/product, such as invariants, commands,
  architecture decisions, regressions, design rules, or integration contracts;
- `GENERAL` — transferable engineering knowledge that is useful beyond one repository.

Do not promote a memory merely because it was expensive to discover.

## 2. Authority and freshness

Retrieved memory has trust level `MEMORY` until checked.

Before a memory drives a load-bearing decision:

1. identify what current fact it predicts;
2. verify that fact against current repository/runtime/primary-source evidence when practical;
3. compare project/version/environment scope;
4. reject or retire the memory if current evidence contradicts it.

A stale project memory must never override current source, manifests, tests, dependency versions, or
runtime observations.

## 3. Persistence gate

Durable persistence requires all of the following:

- the lesson is useful again;
- evidence and provenance are recorded;
- scope is explicit;
- transfer conditions and counterexamples are known enough to avoid blind reuse;
- no secret, credential, private chain-of-thought, raw personal data, or unnecessary sensitive data
  is included;
- a durable sink is authorized by the user/project/host.

By default, do **not** mutate a repository merely to save memory. Use `thalarch-project-brain` only
when project-local durable memory is authorized.

`GENERAL` memory is stricter than `PROJECT` memory. A single anecdotal success should normally remain
project-scoped or a generalization candidate until it is supported by a stable mechanism/contract,
multiple independent cases, or explicit human curation.

## 4. Memory record

A useful durable record is compact and inspectable:

```text
TITLE
SCOPE: PROJECT | GENERAL
KIND: invariant | decision | regression | diagnostic | failure-pattern | workflow | design-rule
PROJECT: optional stable project key
TRIGGER: when retrieval is useful
LESSON: concise reusable statement
EVIDENCE: what proved it
SOURCE: path/commit/run/doc reference when available
TRANSFER: conditions where it applies
COUNTEREXAMPLE: when it must not be applied
CONFIDENCE: evidence-derived, not rhetorical confidence
LAST_VERIFIED: timestamp/commit/version when available
STATUS: active | retired
TAGS: small retrieval vocabulary
```

Do not store private reasoning traces. Store decisions and evidence.

## 5. Retrieval protocol

Before meaningful work where history is likely to help:

1. form a narrow retrieval query from task + subsystem + failure mode;
2. search project memory first, then general memory only when useful;
3. retrieve a small top set, not the whole store;
4. remove duplicates and low-similarity results;
5. revalidate any load-bearing item;
6. inject a compact capsule into `thalarch-context`.

Use this capsule:

```text
MEMORY USED
- <lesson> — scope/evidence/freshness

MEMORY REJECTED
- <lesson> — stale, contradictory, wrong scope, or insufficient evidence
```

Silence is better than irrelevant retrieval.

## 6. Contradictions and retirement

Never silently overwrite history when a lesson stops being true.

- current evidence contradicts memory → mark/retire it;
- a new version narrows applicability → update scope/version metadata;
- two memories conflict → keep both out of the active capsule until current evidence resolves them;
- repeated weak retrievals → prune or retag rather than expanding the prompt.

## 7. Sensitive-data boundary

Do not persist:

- passwords, tokens, keys, secrets, auth cookies;
- full private emails/messages/logs when a non-sensitive lesson is sufficient;
- health, financial, identity, or other sensitive personal data unless a separate authorized product
  memory system explicitly governs that data;
- private chain-of-thought or hidden reasoning;
- copied third-party proprietary content when a short derived lesson is sufficient.

Project memory should describe engineering facts, not become a surveillance archive.

## 8. Portable local store

When an opt-in local durable store is appropriate, this skill includes:

`scripts/memory_store.py`

It provides a standard-library SQLite store with `init`, `add`, `search`, `list`, and `retire`
commands. It is a portability fallback, not a requirement: prefer a host-native memory/RAG provider
when one is available and authorized.

The script deliberately accepts only durable `PROJECT` or `GENERAL` entries. `SESSION` belongs in the
current ledger. `GENERAL` insertion requires stronger evidence and explicit generalizability.

## 9. Completion discipline

Do not claim that the model has been retrained because memory was added. Memory improves retrieval
and continuity around the base model; it does not change the model weights.

Report memory-assisted conclusions with the same evidence discipline as any other conclusion.
