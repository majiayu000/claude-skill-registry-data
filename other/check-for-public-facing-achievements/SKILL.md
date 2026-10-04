---
name: check-for-public-facing-achievements
description: Filter recent ICAIRE Brain updates into evidence-backed achievements suitable for public communications. Use when reviewing stand-up reports or programme updates for externally shareable progress.
---

# Check ICAIRE updates for public-facing achievements

Review current ICAIRE updates and separate externally shareable achievements from internal progress, plans, approvals, and unresolved work.

## Contract Checklist

- Read the relevant recent ICAIRE Brain pages before classifying claims.
- Preserve chronological order and cite the source page for every achievement.
- Include only completed or clearly attained outcomes, not intentions or work in progress.
- Mark claims needing confirmation when publication status, dates, links, names, or partner approvals are missing.
- Do not publish, create campaign items, or update public pages without explicit approval.

## Workflow

1. Define the review scope.
   - Identify the date range, report pages, initiative, or update set.
   - If the scope is ambiguous, use the most recent stand-up reports and state the dates reviewed.
   - Anti-patterns: reviewing stale summaries only, silently expanding the date range, treating report-production work as an ICAIRE achievement.

2. Retrieve and read source pages.
   - Use the owning ICAIRE Brain search and direct page reads.
   - Prefer canonical report, meeting, initiative, and deliverable pages over raw snippets.
   - Capture the exact wording, status, date, and relevant source slug for each candidate claim.
   - Anti-patterns: relying on general memory, inferring completion from a planned milestone, citing only a secondary summary when a canonical page exists.

3. Classify each candidate.
   - `public-facing`: a completed or attained outcome with clear external value, such as participants reached, a portal completed, a call closed, a system built, or content recorded.
   - `internal-only`: attendance, drafting, review, approval queues, task counts, report formatting, internal QA, staffing, or operational blockers.
   - `public-facing with confirmation needed`: externally relevant but missing a publication date, public URL, launch confirmation, final approval, or partner permission.
   - Anti-patterns: turning “near launch” into “launched”, treating “under review” as complete, presenting internal process improvements as public impact.

4. Produce the filtered result.
   - List achievements in chronological order.
   - Use plain language suitable for a communications lead.
   - Keep caveats attached to the claim rather than hiding them in a general disclaimer.
   - Include a short excluded-items note when it prevents overclaiming.
   - Anti-patterns: adding unsupported superlatives, inventing links or dates, removing material caveats for a cleaner narrative.

5. Hand off for content drafting.
   - For each approved candidate, provide a one-line factual basis and the source slug.
   - Flag missing facts needed for a social post, including event dates, guest names, episode titles, URLs, handles, images, and approval owners.
   - Stop before drafting or publishing if the user asked only for filtering.
   - Anti-patterns: publishing directly, fabricating a CTA, tagging partners without approval, treating a draft as approved copy.

## Anti-Patterns

- Do not use internal status as public impact.
- Do not claim a launch, publication, approval, or partner endorsement without source evidence.
- Do not merge separate achievements into one stronger claim unless the sources support the relationship.
- Do not invent public URLs, event dates, guest names, handles, hashtags, images, or approvals.
- Do not send or publish communications.

## Output

Return:

- `Scope reviewed`
- `Public-facing achievements` in chronological order
- `Confirmation needed`
- `Excluded as internal or incomplete`
- `Sources` with ICAIRE Brain slugs
