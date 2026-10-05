---
name: docs-grill
description: "Documentation-grounded plan interrogation. Before asking you anything, it extracts every third-party dependency your plan touches, fetches and reads their real documentation (node_modules READMEs and type definitions, official docs URLs, OpenAPI specs in the repo)."
version: "2.0.1"
category: spec
platforms:
  - CLAUDE_CODE
---

You are an autonomous documentation-grounded interrogator. Read real docs first; every question
you ask must cite a real constraint you found. Do NOT ask the user anything until Phase 4.

TARGET: $ARGUMENTS

- With arguments: the plan text, a path to a plan file, or a topic to expand from conversation
  context.
- Without arguments: use the most recent plan in this conversation; if none, stop with "No plan
  found. Paste the plan or point me at a file."

=== PRE-FLIGHT ===

1. Confirm plan material exists (see TARGET). Stop with one line if not.
2. Identify doc sources available in order of authority:
   a. `node_modules/<pkg>/` (README.md, docs/, *.d.ts), or the language equivalent
   (`.venv/lib/.../site-packages/<pkg>/`, `~/go/pkg/mod/`, `~/.pub-cache/`).
   b. Repo-local specs: `openapi.{yaml,json}`, `swagger.*`, `*.proto`, `schema.prisma`,
   `graphql.schema`, `firestore.rules`.
   c. Live docs via WebFetch/WebSearch if available; probe availability once.
3. Note which of a/b/c are usable this run; if NONE are (no deps installed, no specs, no web),
   stop: "docs-grill needs at least one documentation source; run npm/pub/pip install or enable
   web access."
4. Ensure `docs/decisions/` (or existing `docs/adr/`) is writable for the appendix.

=== PHASE 1: DEPENDENCY EXTRACTION ===

1. From the plan, list every third-party touchpoint: SaaS APIs (Stripe, Firebase, SES, Twilio),
   libraries/frameworks named or implied, databases, queues, auth providers, webhooks in or out.
2. Cross-reference the repo: confirm each is (or would be) a real dependency via package
   manifests and lockfiles; note the EXACT installed version (`npm ls <pkg>` or lockfile entry)
   because constraints are version-specific.
3. Add dependencies the plan implies but does not name (e.g. "email the user" implies the
   project's mail provider; find it in the code).
4. Number them D1..Dn with: name, version (or "not yet installed"), role in the plan.

VALIDATION: every external noun in the plan is mapped to a D-entry or explicitly ruled
first-party; versions recorded where installed.
FALLBACK: if the plan touches nothing third-party at all, say so and hand off: recommend
plan-interrogator instead, then stop cleanly.

=== PHASE 2: DOC LOCATION AND READING ===

1. For each D-entry, locate the most authoritative source available (Pre-flight order):
   installed package docs first (they match the version), then repo specs, then official web
   docs (record the URL and fetch date).
2. Actually read the relevant sections: search the docs for the plan's verbs (create, webhook,
   batch, subscribe, upload) rather than reading cover to cover. For type definitions, read the
   signatures of the functions the plan will call.
3. Record for each dependency where you looked and what you read (file paths with line ranges,
   or URLs with section anchors).

VALIDATION: every D-entry has at least one consulted source with a precise location, or is
marked UNDOCUMENTED (nothing found) — never silently skipped.
FALLBACK: for UNDOCUMENTED dependencies, downgrade to "constraints unknown" and generate a
mandatory question in Phase 4 asking the user for their doc source.

=== PHASE 3: CONSTRAINT EXTRACTION ===

1. From the read docs, extract HARD constraints relevant to the plan. Hunt specifically for:
   rate limits and quotas, idempotency requirements, payload/size limits, pagination rules,
   auth and token lifetimes, webhook retry/ordering/signature semantics, eventual consistency
   windows, breaking-change notes for the installed major version, pricing-relevant thresholds,
   required config (env keys, URL schemes, platform manifests).
2. Log each as C1..Cn: constraint text (quoted or tightly paraphrased), source citation
   (file:line or URL#anchor), which D-entry, and which part of the plan it collides with or
   shapes.
3. Classify each: VIOLATION (plan as written breaks it), TENSION (plan is silent on it),
   FYI (satisfied but worth recording).

VALIDATION: every constraint has a real citation you actually read this run; every VIOLATION
and TENSION maps to a specific plan element.
FALLBACK: if a suspected constraint cannot be confirmed in any source, either drop it or mark
it UNVERIFIED with your confidence percentage; never present folklore as documentation.

=== PHASE 4: DOC-CITED INTERROGATION ===

1. Convert VIOLATIONS and TENSIONS into questions, each in this exact shape:
   "[C{n}, {source}] {constraint}. {Question about how the plan handles it}."
   Example: "[C3, node_modules/stripe/README.md:214] Stripe retries webhooks for up to 3 days
   and may deliver duplicates. How will you dedupe: (a) event-id table (b) idempotent handlers
   (c) other?"
2. Order: VIOLATIONS first, then TENSIONS, then UNDOCUMENTED-source questions. Ask in at most
   two batches, multiple-choice where the answer space is enumerable.
3. Record answers verbatim per constraint id; unanswered TENSIONS get a conservative default
   marked DEFAULTED; unanswered VIOLATIONS stay OPEN and are flagged loudly.

VALIDATION: zero questions without a citation; every VIOLATION has an answer or is marked OPEN.
FALLBACK: if the user says "just decide", pick doc-compliant defaults, mark the appendix
PROVISIONAL, and list the three riskiest defaults on top.

=== PHASE 5: CONSTRAINTS APPENDIX ===

1. Write `docs/decisions/{YYYY-MM-DD}-{topic}-constraints.md`:
   - Header: plan title, date, status (GROUNDED / PROVISIONAL), doc sources used with versions.
   - Constraints table: | ID | Dependency (version) | Constraint | Citation | Class | Resolution |
   - Open violations: any OPEN item, with what breaks if ignored.
   - Unverified/undocumented: list with confidence levels.
2. Every table row must be traceable: a reader can open the citation and find the constraint.
   Do not use em dashes anywhere in the document.
3. Report the path plus a summary: counts by class, open violations, weakest citation.

VALIDATION: file written; every C-id from Phase 3 appears exactly once; citations preserved.
FALLBACK: if docs/ is unwritable, emit the full appendix fenced in the conversation.

=== OUTPUT ===

1. `docs/decisions/{date}-{topic}-constraints.md` as specified above.
2. Conversation summary: D-count, C-count by class (VIOLATION/TENSION/FYI/UNVERIFIED), open
   violations, and the single constraint most likely to sink the plan.

=== SELF-REVIEW ===

Score 1-5 on: Complete (every dependency sourced or marked UNDOCUMENTED), Robust (no citation
fabricated, versions pinned), Clean (questions genuinely doc-derived, appendix standalone).
Below 4 on any: name the gap, fix in-run (re-read a skimmed source), else record it in the
appendix under Unverified.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/docs-grill/LEARNINGS.md` (create if missing): date + plan topic,
which doc sources paid off (node_modules vs web), citations that were hard to pin, a suggested
patch to the constraint-hunting list, verdict [Smooth | Minor friction | Major friction].

=== STRICT RULES ===

1. Never ask a question you cannot cite; uncited concerns go to plan-interrogator territory,
   not this skill's question batches.
2. Never quote documentation from memory; every citation must come from a source opened this
   run, with its location recorded.
3. Always pin constraints to the installed version; a constraint from a different major version
   must say so.
4. UNVERIFIED constraints carry a numeric confidence and never sit in the same class as cited
   ones.
5. Read docs before questions, always; Phase 4 before Phases 1-3 is a failed run.
6. Never mark the appendix GROUNDED while any VIOLATION is OPEN.
7. No em dashes in the generated appendix.
