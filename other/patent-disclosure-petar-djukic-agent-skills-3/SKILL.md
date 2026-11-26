---
name: patent-disclosure
description: >-
  Write and evaluate invention disclosures a patent professional can file.
  Guides the full workflow: claim drafting, prior-art search, the
  eleven-section disclosure written in the recommended order, and a
  four-axis self-assessment (novelty, non-obviousness, commercial value,
  subject-matter eligibility) with target scores. Domain-independent; a
  per-project context file supplies the technology domain, prior-art
  starting points, and commercial material. Triggers: patent disclosure,
  invention disclosure, patentability, is this patentable, prior art
  search, claim drafting, four-axis, Alice/Mayo, patent claim, IP
  disclosure, file a patent.
---

# Patent disclosure

This skill turns an invention into a disclosure that survives a patent
professional's four-axis evaluation. It is domain-independent: everything
domain-specific comes from a project context file, never from the skill.

## Where things live

- **Framework:** `references/four-axis-framework.md` — the four
  evaluation axes with targets, plus detectability.
- **Writing guide:** `references/section-guide.md` — the eleven sections,
  the problem-statement formula, the writing order, style rules.
- **Patterns:** `references/patterns-and-antipatterns.md` — claim
  anatomy, four strong patterns, five anti-patterns with fixes.
- **Register:** `references/technical-register.md` — anthropomorphic and
  casual vocabulary with technical replacements, the term-of-art
  exception, the companion-disclosure independence rule.
- **Skeleton:** `assets/disclosure-template.md` — the section scaffold to
  copy for a new disclosure.
- **Gate:** `assets/checklist.md` — the patentability checklist and the
  self-assessment rubric with target scores.

## Domain context (required input)

Look for `patent-context.md` in the working directory (or a file the user
names). It supplies what the skill deliberately does not contain:

- the technology domain and its terminology
- pointers to the project's architecture documents
- known competitors and prior-art starting points (assignees to search)
- relevant standards bodies and any standardization plans
- scenario, roadmap, and commercial material for Sections 5.3 and 9

If the file is absent, ask the user for the domain and any known prior
art in one question, then proceed with generic search strategies. Never
invent commercial figures, expert names, or competitor claims — every
Section 9 fact traces to the context file or the user.

## The workflow

### 1. Claim first

Draft (or receive) the claim and treat it as the north star: enumerate
its limitations, confirm each is an intentional technical element, and
verify material exists to support every one. Offer the three-scope ladder
(broad / medium / narrow) from the framework reference.

### 2. Prior-art search

Follow the search strategy in the framework reference. For academic
literature, delegate to the `update-references` skill — build arXiv and
Scholar queries from the claim's defining terms; results land in
`references.yaml` and feed Section 3.C. Patent databases (Google Patents,
Espacenet, the US Patent and Trademark Office, the World Intellectual Property
Organization) and standards bodies are searched directly, with
assignees from the context file. Record the closest prior art explicitly.

### 3. Write in the recommended order

Problem (4) → Summary (5) → Details (6) → Context (2) → Prior art (3) →
Detectability (7) → metadata (8-11). Copy `assets/disclosure-template.md`
as the scaffold and follow `references/section-guide.md` per section.
Check each major claim/description against the patterns reference — if a
passage matches an anti-pattern, apply its fix before moving on.

### 3b. Register sweep

After Sections 5-6 are drafted, sweep them against
`references/technical-register.md`. Components perform operations; they
do not ask, hold, hand off, or stand up. Replace conversational verbs
with the role-precise technical verb (asks → queries for discovery,
requests for a consumer), strip hand/body and motion metaphors, and
delete idioms in favour of the named mechanism. Apply the term-of-art
exception before each replacement: vocabulary the governing standard
uses stays. Related disclosures follow the companion-disclosure
independence rule — no "builds on" or "borrows from" language anywhere.

### 4. Self-assessment

Run `assets/checklist.md`: every checkbox, then the rubric. Score each
axis honestly against its target. **Do not report the disclosure as ready
while any score is below target** — name the failing axis and the
specific revision required, and iterate.

### 5. Prose pass

Run the `filter-tells` skill on the finished disclosure. The overlap is real:
marketing vocabulary ("revolutionary", "cutting-edge") fails both filter-tells's
venue-jargon check and this skill's own style rules; undefined coinages
fail both Prompt 8 and the claim-support check. Fix what both flag once.
The register sweep (step 3b) is complementary, not redundant: filter-tells does
not flag "asks", "hands to", or "lets" — those are unremarkable in
articles and only wrong in the patent register.

### 6. Report

Deliver: the disclosure file, the rubric with scores, the closest prior
art identified, and the open risks (lowest-scoring axis, any claim
element with thin support, detectability concerns).

## Dependencies

None beyond the repo's standard tooling. Prior-art literature search uses
`update-references` (PyYAML; arXiv needs no key, Scholar needs the
SerpAPI key). The prose pass uses `filter-tells`.
