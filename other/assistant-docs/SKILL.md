---
name: assistant-docs
description: "Create or update README, API, architecture, changelog, or migration docs. Use for explicit documentation work."
---

# Documentation Generator

## Contracts

| File | Purpose |
|---|---|
| [`contracts/input.yaml`](contracts/input.yaml) | doc_type, scope, source_files[], format, conditional feature-preparation evidence and architecture_decision_pack |
| [`contracts/output.yaml`](contracts/output.yaml) | files_updated[], evidence_sources[], doc_coverage, review_items[], safety_notes[], conditional feature-preparation and Architecture Pack traces |

- `doc_type` and `scope` are required; `source_files` and `format` are inferred when absent
- `files_updated` entries include path, change_type (created/modified), and description
- `review_items` is non-empty when docs contain inferred, stale, conflicting, or audience-sensitive claims needing confirmation
- Any existing-system feature-preparation document requires exact admissible evidence-row bindings `{evidence_ref, item_id, claim_or_question}` for every behavior claim and carried Product question. Incomplete or mismatched evidence returns `blocked_incomplete_evidence` with `request_complete_evidence` and no documentation write; a fresh-but-incomplete Pack additionally returns `blocked_incomplete_pack` with `request_complete_pack`.
- Infer `architecture_design_mode` and conditional `architecture_decision_pack_status`. A current Pack requires the compact canonical `architecture_decision_pack` projection; resolve selected design and rationale through its current canonical ref and record them in `documented_decision_refs`. Missing, stale, and out-of-scope Pack states require issue/recovery evidence and an `architecture_decision_pack_trace` outcome. Never reconstruct, infer, or invent a missing or stale Architecture Decision Pack.

Migration note: v4 replaces the v3 `feature_preparation_evidence_refs: string[]` transport with exact `{evidence_ref, item_id, claim_or_question}` bindings in the input and validated output trace. v3 consumers must migrate each carried behavior claim or Product question to its exact canonical evidence row; broad artifact-only refs are rejected and return no-write recovery. v3 adds feature-preparation completeness for ordinary and Pack-backed documentation. v2 consumers must treat `blocked_incomplete_evidence` and `blocked_incomplete_pack` as no-write recovery, and provide admissible feature-preparation evidence refs before documenting behavior claims or carried Product questions. Existing v2 behavior keeps files_updated required/non-empty for ordinary and current-Pack documentation, but permits omission for typed no-write recovery. Pack projections require non-empty boundaries and exact five-concern design-pressure coverage; v1 consumers must adapt before accepting v2.

Covers the developer's documentation weakness by generating accurate, maintainable docs from code.

Core principle: **docs should be generated from truth (code), not written from memory.**

## Goal

Produce documentation that is accurate, maintainable, and traceable to source evidence.

## Success Criteria

- Every concrete claim is backed by code, git history, existing docs, or user-provided source material.
- When documenting an applicable architecture decision, the document resolves selected design and rationale from the fresh Architecture Decision Pack reference, records their documented decision refs, and preserves facts versus assumptions, semantic type/primitive-boundary rationale, and falsifiable quality verification rather than rewriting generic design claims.
- Pack-backed architecture docs return `architecture_decision_pack_trace`: `documented` carries source Pack/decision/evidence refs; missing, stale, and out-of-scope states record only recovery action and review trace, never invented refs.
- Review-needed items identify inferred or stale claims instead of silently presenting them as fact.
- The selected doc mode, scope, output files, evidence, and remaining gaps are explicit.

## Constraints

- Do not invent features, issue numbers, versions, metrics, roadmap status, or examples to make docs sound stronger.
- Ask every material question when missing audience, scope, target file, doc type, or architecture claim changes the output and cannot be inferred; group questions by topic with why, risk if guessed, and a safe default where available rather than enforcing a numeric quota.
- If evidence is weak, write generic wording with placeholders or mark the claim for review.
- Prefer local files, repo-native commands, and git history as documentation truth. Do not call external documentation generators, SaaS analyzers, or upload proprietary code without explicit approval.
- Do not include secrets, tokens, private endpoints, customer data, or internal-only details unless the target document is explicitly approved for that audience.

## Available Modes

| Mode | File | When to use |
|---|---|---|
| **API Docs** | `api-docs.md` | Endpoints, services, public interfaces |
| **Architecture** | `architecture.md` | System overview, component relationships, data flow |
| **README** | `readme-gen.md` | Project README from codebase analysis |
| **Changelog** | `changelog.md` | Release notes from git history |
| **Migration Guide** | `migration.md` | Breaking changes, upgrade steps |
| **Code Explainer** | `explainer.md` | Deep explanation of specific code for learning |

## Mode Selection

```
Input arrives
    │
    ├─ "document the API" / "API docs"      → api-docs.md
    ├─ "architecture doc" / "system design"  → architecture.md
    ├─ "update readme" / "write readme"      → readme-gen.md
    ├─ "changelog" / "release notes"         → changelog.md
    ├─ "migration guide" / "upgrade guide"   → migration.md
    ├─ "explain this" / "doc this code"      → explainer.md
    └─ ambiguous                             → ask user
```

When the request is clear enough to choose a mode and scope from local context, proceed without ritual questions and record any assumptions in **Review needs**.

## General Protocol

For all modes:

1. **Read the code first** — never generate docs from assumptions
2. **Read existing docs and project instructions** — README, docs index, AGENTS/CLAUDE/CONTRIBUTING, changelog, API specs
3. **Match existing style** — if the project has docs, follow their conventions
4. **Verify accuracy** — every claim in the doc must be traceable to code, tests, config, git history, or user-provided source
   - For existing-system feature preparation, resolve `feature_preparation_evidence_status` before drafting; incomplete evidence is a no-write recovery even when no Architecture Decision Pack applies.
5. **Use real examples only** — examples must come from actual code/tests or be explicitly labeled as illustrative
6. **Mark generated sections** — use `<!-- generated by assistant-docs -->` comments only where the project accepts generated markers
7. **Record review needs** — list inferred, stale, or audience-sensitive claims instead of burying uncertainty

## Output

Return:
- **Status** - created, updated, reviewed, or no changes needed.
- **Files** - paths changed with a one-line description for each.
- **Evidence** - source files, APIs, tests, configs, commits, or examples used as documentation truth.
- **Coverage** - what the documentation now covers and what remains out of scope.
- **Review needs** - inferred claims, stale areas, audience-sensitive claims, conflicts, or open questions needing user confirmation.
- **Safety notes** - any redactions or sensitive/internal details intentionally omitted.

## Staleness Detection

When entering a project, check for stale docs:

```
>> Scanning documentation freshness...
   README.md: last updated 45 days ago, 3 new features since
   API.md: references endpoints that no longer exist
   CHANGELOG.md: missing entries for last 2 releases
```

Report staleness to user. Offer to update.

## Output Quality

- Use the project's existing doc format (markdown, XML docs, etc.)
- For .NET: generate XML doc comments for public APIs when the project uses them
- For APIs: include request/response examples from tests, fixtures, schemas, or clearly labeled illustrative data
- For architecture: include Mermaid diagrams only if the project already accepts Mermaid or the user approves; otherwise use text outlines
- For architecture decisions: do not claim memory, performance, or extensibility benefit without a workload, budget/explicit unknown, measurement method, and failure condition; point to the verification evidence or mark the claim for review.
- Keep docs concise — verbose docs don't get read
- Prefer links to existing canonical docs over duplicating content

## Anti-Patterns

- **Don't document obvious code** — `/// Gets the user` on `GetUser()` adds nothing
- **Don't hallucinate features** — only document what exists in code
- **Don't create docs the project doesn't need** — a 50-line script doesn't need architecture docs
- **Don't duplicate** — if info exists elsewhere, link to it
- **Don't leak sensitive context** — redact secrets, tokens, private endpoints, and customer data
- **Don't treat stale docs as truth** — code/config/tests/git/user-provided source outrank old docs

## Stop Rules

- Stop and ask every material, non-discoverable question only when the missing answer changes audience, scope, target artifact, public contract wording, or verification; group them by topic and keep them concise.
- Stop and report gaps when required source files, git history, or docs cannot be accessed.
- Do not finalize docs until changed claims have source evidence or are clearly marked for review.
