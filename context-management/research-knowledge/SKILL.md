---
name: research-knowledge
description: Retrieve existing results, ideas, examples, counterexamples, and corrections across a research campaign, sibling repositories, and shared literature. Build bounded task context, maintain internal-writeup packets, and audit stale extractions. Use at campaign start or resume and before substantial new work or novelty claims.
---

# Research Knowledge

Use the configured shared knowledge index to recover prior work before developing another proof,
experiment, or route. The sources remain authoritative; search results and extracted cards are
navigation and reusable summaries, not independent proof certification.

## Start or resume

1. Run `python3 scripts/research_knowledge.py sync` from the campaign repo. Configuration is found
   through `.research-knowledge.json`, `RESEARCH_KNOWLEDGE_CONFIG`, or the shared library binding.
   An explicit `--config /path/to/knowledge/workspace.json` also works. Inspect coverage issues.
   Let sync finish using the tool's running-process/polling support; do not kill it with a few-second
   process timeout. First builds and migrations can take minutes; progress is printed to stderr.
2. Run `python3 scripts/research_knowledge.py context --campaign . --task 'current question'` and
   actually read its output. Rebuild this context after compaction or a change of research direction.
   `--budget` uses conservative UTF-8 byte units to bound token use without a model dependency;
   increase it when necessary. The output lists omitted records and marks partial raw excerpts.
   Keep the campaign profile short: current conventions and source pointers, not an appended history
   of rounds. Pin the authoritative current packet and retrieve history selectively. If profile/task
   text exceeds its share of the budget, context explicitly omits the whole profile while preserving
   retrieved evidence. Read the full profile with `profile --campaign ID` when needed; do not
   repeatedly trim a few characters while leaving an oversized historical summary.
3. Search the proposed claim and its failure mechanism with
   `python3 scripts/research_knowledge.py search 'terms' --campaign .`. Campaign synonyms and
   related sibling repos influence ranking; global sources remain available. Search reformulations
   too. For precise evidence, use `inspect RESULT_ID` and open the linked original statement/proof.

Compare hypotheses, quantifiers, conventions and conclusions before importing a result. Corrections,
refutations and superseding cards accompany known IDs; uncurated archive corrections can still
require direct searches. An empty result or incomplete index does not establish novelty. When the
registry is unavailable, use targeted `rg` searches of campaign and sibling sources and report the
coverage limit. Use `shared-literature` for external paper acquisition and identity reservations.

Use `status` to diagnose retrieval trouble: it cheaply reports index age, schema/registry status,
coverage issues and a running writer. Readers can query the previous committed snapshot during sync;
returned hits check source drift and corrections. The default lock allowance is 300 seconds; use
`--lock-timeout 600 sync` when a longer wait fits the task budget. Check helper versions if a campaign
copy lacks these commands. Repair or finish synchronization before treating retrieval as unavailable;
do not launch duplicate rebuilds or repeat unchanged short timeouts. Do not remove a shared lock or
terminate another campaign's job. If the checkout/index is actually unavailable or cannot be repaired
within scope, record the failure and coverage limit before using direct-source retrieval. That is
an exceptional recovery path, not the normal campaign startup. Retrieval failure never establishes
that a mathematical result is absent.

## Maintain reusable findings

Use `python3 scripts/research_knowledge.py sources` to identify configured source repositories,
subjects, input types, and ownership. The shared registry supports manuscript/text sources and
structured JSON collections. Register new authoritative sources and their mappings in the artifact
workspace; consult the owner's existing schema and ownership map before choosing what to index.

For structured knowledge, update records in their owning database, preserve stable IDs, scope,
source status and proof/citation links, run that database's validators, then run shared `sync` and
`audit`. Do not create a second editable packet for each existing database record. Keep authored
proofs in their declared owner and exclude generated catalogue copies when the originals are
indexed. An imported `established` status reports the source's assessment, not a new proof review.

Register substantial internal writeups under `writeups` in the artifact workspace's registry. Use
`python3 scripts/research_knowledge.py packet WORK_ID` to create their shared literature packets.
After meaningful source changes, use `packet WORK_ID --refresh`. This fingerprints explicit TeX
inputs and registered extra sources and refreshes unreviewed extraction candidates; it preserves
curated result cards and hand-written overviews. Declare nonliteral dependencies explicitly.

Inspect candidates against their original statements, definitions and proof status. Add precise
Markdown cards under the packet's `results/` directory, following the schema in the CLI guide.
Preserve assumptions, aliases, source fingerprints/anchors, evidence status and extraction review
separately. Record useful examples, counterexamples, ideas and failed approaches as well as theorems.
Link `uses`, `corrects`, `refutes` and `supersedes` relations by stable result ID. New wording is not
new mathematics; reuse IDs and source links rather than creating independent copies of one result.

Run `packet WORK_ID --refresh` to render a managed overview after editing cards, then `sync` and
`audit`. A changed source does not automatically validate an old extraction: review it before
updating its fingerprint. Audit reports include stale sources, broken relations, duplicate IDs,
registered works without packets, and standalone TeX candidates awaiting registration.
Commit curated packets/configuration in the artifact workspace and source changes in their owner.
The SQLite index is a disposable ignored cache. Keep project names and mappings out of generic skills.

## Optional specialists

When delegation is authorized and useful, add `--role historian`, `--role literature`, or
`--role transfer` to the context command. Give that output and a bounded question to the specialist.
The command produces a brief; it does not spawn an agent or authorize delegation. Require source IDs,
applicability, corrections and search limitations in the return. Reconstruct expertise from durable
profiles and records rather than relying on a subagent remembering earlier sessions.

Full CLI and card examples live in `docs/research-knowledge.md` in the tools workspace. Keep workflow
instructions brief in campaign ledgers; link the maintained result map and source owners.
