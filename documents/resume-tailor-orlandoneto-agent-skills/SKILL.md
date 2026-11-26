---
license: MIT
name: resume-tailor
description: Tailors a résumé to a specific job description — parses the JD for priorities, reorders and rewrites bullets to match, quantifies achievements, and passes ATS filters. Use when a user is applying to a specific role and wants their résumé to match the JD, or when their bullets are weak ("responsible for...") and need tightening.
---

# Résumé Tailor

A résumé that matches the job description beats a generic one. Not by keyword-stuffing; by showing the exact evidence the hiring team is looking for.

## When to use

- User is applying for a specific role and wants their résumé tuned to that JD.
- Résumé reads generic ("responsible for") and needs punch.
- User has 5+ years of experience and a résumé overflowing onto page 3 — needs cutting.
- ATS-compatibility is a concern (large companies; public sector; many online portals).

## Before you start

Gather:

1. **The job description** — full text, not a summary. Priorities are buried in specific wording.
2. **The current résumé** — ideally in editable form (Markdown, Google Doc, Word). PDF only means you'll retype.
3. **The user's recent work + achievements** that aren't on the résumé yet — often there's a strong story hidden in Slack DMs and project docs.
4. **Which companies they'd be most excited about** — the one where they'll push hardest and get the most value from tailoring.

## Tailoring workflow

1. **Parse the JD.** Separate must-haves, nice-to-haves, culture signals. See [jd-parsing.md](./references/jd-parsing.md).
2. **Audit the current résumé** against the must-haves. What's already there? What's missing? What's there but buried?
3. **Reorder.** Most relevant experience first — within the same role, reorder bullets. Across roles, keep reverse-chronological but consider a summary / highlights section at the top.
4. **Rewrite weak bullets.** Apply STAR (Situation / Task / Action / Result). See [bullet-rewrites.md](./references/bullet-rewrites.md).
5. **Quantify everything possible.** "Improved performance" < "Cut p95 latency 40% (800ms → 480ms)" < "Cut p95 latency 40%, unblocking SLA target for 3M monthly users."
6. **Trim.** One page if <10 years experience, two pages max otherwise. Recent and relevant stays; old and tangential goes.
7. **ATS pass.** Remove fancy formatting, tables, text-in-images, two-column layouts. Single column, clean headers, normal fonts. See [ats-formatting.md](./references/ats-formatting.md).
8. **Generate a short cover letter / email** that leads with the specific reason this role is a match — not a restatement of the résumé.

## Non-negotiable rules

- **Never fabricate.** Achievements, titles, metrics, dates — all real. Fabricated résumés get discovered in reference checks, probation reviews, or worse.
- **Lead every bullet with a verb.** "Led a team of 5..." not "Was responsible for leading..."
- **Quantify every bullet you can.** Numbers, percentages, counts, dollars. "Shipped feature" is weaker than "Shipped feature used by 2,400 users in week 1".
- **Match the JD's vocabulary — where truthful.** If the JD says "partner with stakeholders", use "partnered with stakeholders", not "worked closely with folks".
- **Cut filler sections.** "Objective" / "References available on request" / generic skills lists — delete. Wasted space.
- **One page if possible.** Hiring teams spend 30 seconds on first pass. Two pages means they might not reach page 2.
- **Never use first person.** "Shipped X" not "I shipped X". Not "Yaroslav shipped X" either — implied first person, no pronoun.
- **Never use a photo** (in the US/UK/Canada). In some European countries and APAC it's expected — match local norm.
- **Dates on the right, roles on the left** — makes scanning easy for recruiters.

## Output

- **The tailored résumé** — full document, ready to copy into the user's source.
- **A change log** — what you rewrote, what you cut, what you reordered, and why. So the user can push back on your edits.
- **A short cover email/letter** — optional but almost always worth including.

## References

- [Parsing a JD](./references/jd-parsing.md) — how to extract must-haves, nice-to-haves, and culture signals; common JD patterns.
- [Bullet rewrites](./references/bullet-rewrites.md) — STAR pattern, strong verb lists, quantification tactics, common bullet failures.
- [ATS formatting](./references/ats-formatting.md) — the layout choices that survive parsing, the ones that don't; Word vs PDF; file-naming.
