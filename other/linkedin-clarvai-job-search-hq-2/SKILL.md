---
name: linkedin
description: "Improve the user's LinkedIn profile (headline, About, experience bullets, skills, Open to Work settings) consistent with their master resume. Use when the user asks about their LinkedIn profile or how recruiters find them."
---

# /linkedin

1. Ask the user to paste their current headline, About, and experience sections (or use `/import-linkedin` data if present). Don't browse LinkedIn yourself.
2. Draft, from `profile/master-resume.md` only (field limits and what shows before "see more": `references/linkedin-facts.md`):
   - **Headline** (≤ 220 chars, target role title first; only the start shows in search): role targets + proof, e.g. "Operations Analyst | Process Improvement & Supply Chain | Cut fulfillment time 20% at a 3PL | Excel, SQL, Lean" (fictional; build the user's from their real facts and target roles).
   - **About** (120–200 words, first person, plain; role and best proof point in the first two lines): what they do, 2 proof points with numbers, what they're looking for (target roles and start timing from `preferences.md`), how to reach them.
   - **Experience:** 2–3 bullets per role, consistent with the resume (LinkedIn can be slightly more narrative), using the plain job titles people in the field search for.
   - **Skills:** top 10 to add in order of target-role relevance, taken from the master resume and `knowledge/field/resume-keywords.md`, only if true. Suggest which 5 to show as "top skills" in About and which to link to each job.
   - **Featured:** one project, portfolio piece, or write-up (non-confidential; nothing from a past employer beyond what's already public).
3. Settings advice: Open to Work (if employed, "recruiters only"; otherwise either setting is fine; details and evidence in `references/linkedin-facts.md`). If they're employed and searching quietly, tell them first to turn off **Share profile updates** before pasting in changes, and keep the headline about their work, not "open to opportunities" (`knowledge/searching-while-employed.md`). Then: job titles and locations matching `preferences.md`, a professional photo, custom URL, "Connect" kept as the main profile button, and the alumni tool on their school's LinkedIn page to find people.
4. Run `truth-checker`, then `voice-editor`. Give the user copy-ready text section by section for them to paste in themselves (never edit LinkedIn for them).
