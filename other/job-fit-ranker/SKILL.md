---
name: job-fit-ranker
description: Use when a user provides a careers website, job list, or job descriptions and wants roles extracted, filtered for campus-recruitment eligibility, compared with a resume, and ranked with evidence. Optimized for Chinese ATS sites and AI, Agent, RAG, backend, and algorithm roles.
---

# Job Fit Ranker

Rank real openings against verified candidate evidence. Do not treat keyword overlap as proof of experience.

## Inputs

Obtain the careers URL or JD text and the candidate resume/profile. Ask only for missing information that could change eligibility or the top-ranked result.

Read the shared [candidate contract](../../shared/references/candidate-profile-schema.md), [job record](../../shared/references/job-record-schema.md), [scoring contract](../../shared/references/fit-scoring.md), [role families](../../shared/references/role-families.md), and [output contract](../../shared/references/output-contracts.md). For Chinese recruiting systems, also read [ATS patterns](../../shared/references/chinese-ats-patterns.md).

## Workflow

1. Inspect the official careers source. Search, paginate, or open job details as needed. Prefer official current postings over aggregators.
2. Normalize title, company, location, job type, cohort, degree, major, language, responsibilities, requirements, source URL, and posting status.
3. Separate explicit requirements from inferred preferences. Record unavailable fields as `unknown`.
4. Apply hard eligibility checks before scoring. Never conceal an unmet cohort, degree, graduation, location, or language constraint.
5. Map every positive match to resume evidence. Give no credit for unsupported keywords.
6. Score with the shared rubric and rank roles. Break close ties by core-capability evidence, then engineering delivery.
7. Return a concise shortlist plus rejected roles that failed hard requirements.

## Output

Use the table and decision format in [ranking-output.md](references/ranking-output.md). Emit one shared Job Record per requisition, include direct job links, and state which page coverage was inspected and whether the list may be incomplete.

## Guardrails

- Do not apply, submit, or create accounts.
- Do not invent candidate credentials or job requirements.
- Do not rank a closed or unverifiable posting above a verified active posting.
- If a site blocks access, report the limitation and analyze user-provided JD text instead.
