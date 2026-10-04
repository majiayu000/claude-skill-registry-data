---
description: Score brand compliance of any content against the brand guidelines
---

# Brand Audit

Audit "$ARGUMENTS" for brand compliance. Score how well content, marketing materials, or any output aligns with the established brand guidelines.

## Prerequisites

Read the brand guidelines. The user must specify which brand to audit against:

- If `.metapowers/branding/` contains only one brand directory, use that automatically
- If multiple brands exist, ask the user which brand to audit against
- If no guidelines exist (`05-guidelines.md` not found), tell the user:

> No brand guidelines found. Run the branding workflow first: `/branding:discover <brand>` through `/branding:guidelines <brand>`.

## Process

1. **Read the brand guidelines:**
   - Read `.metapowers/branding/<brand>/05-guidelines.md` for the complete brand rules
   - Read `.metapowers/branding/<brand>/03-verbal.md` for voice and tone details
   - Read `.metapowers/branding/<brand>/04-visual.md` for visual identity details
   - Read `plugins/branding/shared/brand-prism-guide.md` for the scoring framework

2. **Identify what to audit:**
   - "$ARGUMENTS" may be: a file path, a URL, a marketing campaign directory, or a description
   - Read the content to be audited
   - If auditing marketing output, check `.metapowers/marketing/` artifacts

3. **Score each Brand Prism facet (1-5):**

   **Physique (visual elements):**
   - Logo used correctly? Colors within palette? Typography consistent? Imagery matches style?

   **Personality (voice & character):**
   - Tone of voice consistent? Language matches guidelines? Personality reflected in copy?

   **Culture (values):**
   - Brand values communicated? Story consistent? Cultural positioning maintained?

   **Relationship (interaction style):**
   - Communication style appropriate? Touchpoint consistency? Relationship tone maintained?

   **Reflection (target audience):**
   - Target audience correctly addressed? Aspirational messaging aligned?

   **Self-Image (user experience):**
   - Brand promise delivered? Emotional resonance present?

4. **Calculate overall score:**
   - Sum of 6 facets (max 30)
   - Percentage score (out of 100%)
   - Rating: Excellent (90%+), Good (75-89%), Fair (60-74%), Poor (<60%)

5. **Write the audit report** to `.metapowers/branding/<brand>/audit-reports/<date>-<subject>.md` with:
   - **Score Summary** — overall score and rating
   - **Facet Breakdown** — score and rationale per facet
   - **Issues Found** — specific compliance violations
   - **Recommendations** — how to improve compliance
   - **Strengths** — what's well-aligned

## Output

The audit report written to `.metapowers/branding/<brand>/audit-reports/`. Present a summary to the user highlighting:
- Overall compliance score and rating
- Lowest-scoring facet
- Top 3 issues to fix
- Strongest facet
