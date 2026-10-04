---
name: nfr
description: >
  Generate Non-functional Requirements (NFR): performance, security, availability, scalability, compliance, localization. Use on /nfr command, or when the user asks for "non-functional requirements", "NFR", "performance requirements", "security requirements", "SLA", "compliance requirements", "load requirements", "uptime requirements", "regulatory requirements", "GDPR". Sixth step of the BA Toolkit pipeline.
---

# /nfr — Non-functional Requirements

Sixth step of the BA Toolkit pipeline. Generates NFR with measurable metrics.

## Context loading

0. If `00_principles_*.md` exists in the output directory, load it and apply its conventions (artifact language, ID format, traceability requirements, Definition of Ready, quality gate threshold). Pay special attention to section 5 (NFR Baseline) — all listed categories are mandatory for this project.
1. Read `01_brief_*.md`, `02_srs_*.md`, `03_stories_*.md`. SRS is the minimum requirement.
2. Extract: slug, domain, integrations, roles, FR list.
3. If domain supported, load `references/domains/{domain}.md`, section `6. /nfr`. Use mandatory NFR categories for the domain.

## Environment

Read `references/environment.md` from the `ba-toolkit` directory to determine the output directory for the current platform. If the file is unavailable, apply the default rule: if `/mnt/user-data/outputs/` exists and is writable, save there (Claude.ai); otherwise save to the current working directory.

## Interview

> **Follow the [Interview Protocol](../references/interview-protocol.md):** ask one question at a time, present a 2-column `| ID | Variant |` markdown table of up to 4 domain-appropriate options plus a free-text "Other" row last (5 rows max), mark exactly one row (recommended) based on the loaded domain reference and prior answers, render variants in the user's language (rule 11), and wait for an answer before asking the next question.
>
> **Inline context (protocol rule 9):** if the user wrote text after `/nfr` (e.g., `/nfr emphasise security and compliance`), use it as a category hint for which NFR areas to prioritise.

3–7 topics per round, 2–4 rounds.

**Standard alignment:** NFR categories follow **ISO/IEC 25010** Software Quality Model (the international standard for software quality characteristics). Every NFR maps to one of the 8 ISO 25010 characteristics: **Functional Suitability**, **Performance Efficiency**, **Compatibility**, **Usability**, **Reliability**, **Security**, **Maintainability**, **Portability**. Project-specific categories (Compliance, Localisation, Observability) can be added but each must be marked as an extension and explain which ISO 25010 characteristic it derives from.

**Required topics:**
1. **Performance Efficiency (ISO 25010)** — time behaviour (response time, throughput), resource utilisation (CPU, memory, network), capacity (CCU, RPS).
2. **Reliability (ISO 25010)** — availability SLA, maturity (defect rate), fault tolerance, recoverability (RTO/RPO).
3. **Security (ISO 25010)** — confidentiality (encryption at rest and in transit), integrity, non-repudiation (audit trail), accountability (per-user attribution), authenticity (authentication strength).
4. **Compatibility (ISO 25010)** — co-existence (with other systems), interoperability (data exchange formats), browser/OS/device support.
5. **Usability (ISO 25010)** — learnability, operability, accessibility (WCAG level), user error protection.
6. **Maintainability (ISO 25010)** — modularity, reusability, analysability, modifiability, testability (code coverage target).
7. **Portability (ISO 25010)** — adaptability (different environments), installability, replaceability.
8. **Functional Suitability (ISO 25010)** — completeness, correctness, appropriateness — usually covered by FRs but worth a sanity check at NFR time.
9. **SLO and SLI** — what service-level objectives do we commit to externally, and which service-level indicators do we measure internally to track them?
10. **Observability** — what metrics, logs, and traces are mandatory? Retention period for each?
11. **Disaster recovery** — RTO and RPO are not just numbers; what is the *runbook* and how often is it tested?
12. **Data sovereignty** — where can each data class be stored and processed? Cloud regions allowed?
13. **Deprecation policy** — how are NFR thresholds tightened over time, and how is breaking change communicated?

Supplement with domain-specific questions and mandatory categories from the reference.

## Generation

**Slug:** read the `**Slug:**` line from the managed block of `AGENTS.md` (project root, or `../AGENTS.md` if cwd is `output/`) and use it verbatim. See [`../references/slug-source.md`](../references/slug-source.md).

**File:** `06_nfr_{slug}.md`

The full per-NFR field set lives at `references/templates/nfr-template.md` and is the single source of truth. Each NFR carries: ID (`NFR-NNN`), ISO 25010 characteristic, sub-characteristic, description, measurable metric, **acceptance threshold** (the bar that says "we passed"), verification method, source (which stakeholder, regulation, or FR drove this NFR), rationale, priority, and linked FRs / USs / Brief constraints. The artifact carries an FR → NFR coverage matrix and a per-characteristic priority summary at the bottom.

**Rules:**
- Numbering: NFR-001, NFR-002, ...
- Every NFR must have a measurable metric **and** an acceptance threshold. Avoid "the system should be fast."
- Group by ISO 25010 characteristic.
- Domain-specific mandatory categories from the reference are also mapped to ISO 25010 characteristics so the audit trail is consistent.

## Back-reference update

After generation, update section 5 of `02_srs_{slug}.md` with links to specific NFR-{NNN}.

## Iterative refinement

- `/revise [NFR-NNN]` — rewrite.
- `/expand [category]` — add NFR.
- `/clarify [focus]` — targeted ambiguity pass (especially useful for surfacing NFR without measurable metrics).
- `/validate` — mandatory categories covered; every NFR has a metric; links correct.
- `/done` — finalize. Next step: `/datadict`.

## Closing message

After saving the artifact, present the following summary to the user (see `references/closing-message.md` for format):

- Saved file path.
- Total number of NFR generated, grouped by category.
- Confirmation that section 5 of `02_srs_{slug}.md` was updated with NFR links.
- Any categories flagged as missing or lacking measurable metrics.

Available commands for this artifact: `/clarify [focus]` · `/revise [NFR-NNN]` · `/expand [category]` · `/validate` · `/done`

Build the `Next step:` block from the pipeline lookup table in `references/closing-message.md` (row `Current = /nfr`). Do not hardcode `/datadict` here.

## Style

Formal, neutral. No emoji, slang. Terms explained on first use. Generate the artifact in the language of the user's request — see `references/language-rule.md` for what to translate and what stays in English.
