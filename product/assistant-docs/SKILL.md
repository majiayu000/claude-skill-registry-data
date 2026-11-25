---
name: assistant-docs
description: "Create or update README, API, architecture, changelog, or migration docs, or diagrams of existing code. Use for explicit documentation work or a diagram of existing code."
---

# Write Source-Backed Documentation

## Shared operating guidance

Load [the common outcome guidance and shared stagnation policy](references/operating-guidance.md) for this activity. Keep specialist methods, authority and completion evidence below; single-pass work needs no progress artifact.


Create or update the requested document from source truth. Read the target, project instructions, and relevant code, tests, configuration, git history, or user-provided material first. Keep the requested scope, audience, destination, and existing style. Ask only for material choices that context cannot resolve.

Load only the mode reference needed:

| Request | Reference |
|---|---|
| API documentation | `api-docs.md` |
| Architecture overview or decision | `architecture.md` |
| Diagram of existing code | `architecture.md` |
| README | `readme-gen.md` |
| Release notes | `changelog.md` |
| Upgrade or migration guide | `migration.md` |
| Code explanation | `explainer.md` |
| Revise or edit existing prose | `editing-checklist.md` |

- Back concrete claims with inspected sources. Do not invent features, issue numbers, versions, metrics, roadmap status, or examples. Use real examples or label illustrative ones. Mark unresolved claims for review, including placeholder or unverified text, instead of presenting them as fact.
- Check changed claims against current source and verify documented commands or links when practical. Do not add an unrelated repository-wide freshness audit.
- Prefer canonical links over duplicate prose. Apply [request alignment](references/operating-guidance.md#request-alignment) to the requested reader task: each section has a role for the stated audience and purpose; leave out unrequested sections, filler and decorative content; propose, rather than silently add, material additions the user did not request. For example, "how to install on Windows" adds that section, marks an unverified PowerShell step for review and proposes a troubleshooting section. Use generated markers, XML comments, or diagrams only where the project or request calls for them; a diagram follows the source-backed accuracy and honest render rules in `architecture.md`.
- Keep secrets, tokens, private endpoints, customer data, and internal details out of documents without authorization for that audience. Use local/repo-native sources; external uploads, generators, and installs require authorization.
- For architecture claims, distinguish facts and assumptions. Memory, performance, and extensibility benefits need workload, budget or explicit unknown, measurement method, and failure condition; otherwise mark them for review.

Return the document or changed paths with a concise account of coverage, source evidence, verification, and material review needs. Omit empty safety/status slots. Stop when inaccessible source or unresolved audience/contract wording prevents a trustworthy result.

## Workflow and Structured Consumers

When a call carries feature-preparation evidence or an Architecture Decision Pack, or requests the supported serialized response, load [`contracts/input.yaml`](contracts/input.yaml) and [`contracts/output.yaml`](contracts/output.yaml). Preserve their existing schema v4 field names and no-write recovery. `architecture.md` explains this conditional boundary for any documentation mode.

For existing-system preparation, every carried behavior claim and Product question needs an exact admissible `{evidence_ref, item_id, claim_or_question}` binding. Incomplete, mismatched, stale, or unresolved evidence returns `blocked_incomplete_evidence` with `request_complete_evidence` and no documentation write. A fresh-but-incomplete Pack also returns `blocked_incomplete_pack` with `request_complete_pack`.

Use only a fresh canonical Pack projection and resolve selected design and rationale through its ref, recording `documented_decision_refs` and `architecture_decision_pack_trace`. Missing, stale, or out-of-scope Packs require issue/recovery evidence; never reconstruct or invent their content. Preserve the supplied boundaries, design-pressure checks, type ledger, quality scenarios, and verification/rollback links. Ordinary source-derived documentation does not require a Pack.
