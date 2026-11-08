---
name: resume-review
description: "Tough, specific review of the user's master resume or a tailored resume, then fixes with their OK. Use when the user asks for resume feedback, wants their resume improved, wants their GitHub, portfolio or publications reflected in it, or before a big application push."
---

# /resume-review

Usage: `/resume-review [job folder to review a tailored version]` (or just ask in plain English).

1. Target: `$ARGUMENTS` (a job's `resume.md`) or, if blank, `profile/master-resume.md` + the original resume file in `profile/` (`resume-original.<ext>`), if present.
2. Run the `recruiter-reviewer` agent for a 6-second-skim read and an ATS read. Add your own pass (evidence and sources behind these checks: `references/what-recruiters-check.md`):
   - **Top third:** reading only the name, the summary line (if any) and the first section, would a recruiter know what the user does, at what level, and one result? If not, that's fix #1.
   - Every bullet: action verb + what they did + measurable result? Flag bullets with no result and ask the user for the number (don't invent one); scale or before → after also count. For "Responsible for…" lines, ask what changed because they were there.
   - Lead with the strongest numbers already in the master resume (money saved or earned, % improvements, time cut, scale).
   - Cut weak or old items for tailored versions (e.g., an old class project or early job unless relevant).
   - Consistency: dates, punctuation, tense, bullet style, capitalization of terms and tools, section order.
   - Keywords for the user's target roles (from `knowledge/field/resume-keywords.md`, or the target postings if that file still says `STATUS: not generated`) present where true, and only if true.
   - Missing: a summary line (optional), links; for students and new grads (`career_stage` in preferences), a GPA decision.
   - **Length and format for their country and stage** (`home_base` and `career_stage` in preferences): see the reference file; one page is a US early-career norm, not a world rule.
   - **ATS:** check what really breaks (columns, tables, text boxes, headers/footers, images, odd headings) and unexplained gaps. Don't chase "ATS scores"; "software rejects most resumes" is a myth.
3. Show the top 10 fixes ranked by impact, each with before → after. Ask which to apply. Apply approved ones to the file you reviewed: for a tailored resume, edit that job's `resume.md`, re-check the changes (`truth-checker`, then `voice-editor`), rebuild its `resume.html`, and remake the PDF if one exists (`/tailor-resume` step 8); for the master resume, re-read `profile/master-resume.md` right before editing, change only the approved lines (the user will see a permission prompt; that's intentional), and add one line to `history/activity.md`. Never cut content from the master resume because it doesn't fit one job; offer master-resume changes separately.
4. **Public work (optional).** If the user asks you to look at their GitHub, portfolio, publications or other public work, or the master resume's contact lines link to such a page and a section looks thin (few projects; no publications for an academic), offer once to read it and suggest real work the resume leaves out: `references/public-work.md`. Nothing from it goes in without the user's yes.
