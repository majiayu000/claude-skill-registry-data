---
name: "job-lead-tier2-scoring"
description: "On-demand deep-dive: fetch the real job description for one or more tracker rows (especially LinkedIn/MyJobHelper leads) using Alex's own signed-in browser, and upgrade the row's fit score and gaps from Tier 1 to a full read. Run only when Alex asks, or when he's at his computer."
---

# Job Lead Tier 2 Scoring

The enrichment half of a two-skill pipeline. `job-lead-intake-scan` runs daily and logs new leads with a quick Tier 1 (title-only) score; this skill takes specific rows Alex wants a real answer on, reads the actual job description, and rewrites the row with a properly-sourced score and gaps. Never run this on a fixed schedule — it needs Alex's own computer and browser session, so it only makes sense on demand ("deep-dive JS-00X", "score the LinkedIn rows for real", or similar), or as a periodic manual sweep of everything still tagged Tier 1 when Alex is at his machine and wants to clear the backlog.

## Key files (Google Drive, folder "JobSearch")
- Master resume: `Alex_Example_Resume-Master.docx`, Drive id `<RESUME_FILE_ID>`
- Tracker: `Job_Search_Tracker.xlsx`, Drive id `<TRACKER_FILE_ID>`, sheet "Job Log"

If the linked device is available and the tracker file is confirmed unlocked (not open in Word/Excel on Alex's machine), editing it directly via the device shell is fine and has worked well in practice; otherwise fall back to download/edit/re-upload via the Google Drive connector. Either way, always re-read the row you're about to update immediately beforehand — don't trust a value you saw earlier in the conversation, since intake runs happen in between.

## 1. Figure out which rows to work on
- If Alex named specific row IDs or companies, use those.
- If he asked for "the LinkedIn rows" or similar, read the tracker and find every row whose Notes says "Tier 1 screen" (or equivalent) with a Job Description link pointing at `linkedin.com`.
- If he asked for a general sweep, do all outstanding Tier-1 rows, but check in after the first few if there turn out to be a lot — this is a slower, browser-driven process per row and shouldn't silently run long without Alex knowing the scope.

## 2. Fetching the real JD
- **LinkedIn job-view links** (`linkedin.com/.../jobs/view/<id>/`): WebFetch is blocked by LinkedIn's robots.txt, and the built-in browser has no LinkedIn session of its own (hits the login wall) — use **Claude in Chrome**, which runs in Alex's real, already-logged-in Chrome. Navigate to the URL, then `get_page_text`. The JD body often doesn't appear on the first read (loads asynchronously, or sits behind a "see more" expansion) — wait ~2s and retry once. If it's still not there, the listing may genuinely have no JD on LinkedIn (common on "Promoted by hirer · Responses managed off LinkedIn" postings) — leave that row at Tier 1, note that LinkedIn didn't surface a JD, and move on rather than looping.
- **MyJobHelper and other ATS links** (Greenhouse, Lever, iCIMS, Workday, company career pages): try WebFetch first; fall back to the built-in browser for sites that block fetch (as done for World Travel Holdings' iCIMS postings) — these don't need Alex's personal login, so either browser works.

## 3. Scoring
Score fit 1-10 against Master using the rubric established for the NorthStar Staffing resumes: relevant title/seniority match, required vs. actual years of experience, named tools/methodologies Alex has evidence for in Master, domain/industry match. List the top 3 gaps worded concretely — quote what the JD actually asks for, don't paraphrase vaguely.

## 4. Updating the row
- Update the EXISTING row in place — never create a duplicate. Overwrite Fit Score and Gap 1-3, change the Notes tier-tag to reflect a full JD read, and update Last Updated to today.
- Do not touch Status — leave whatever Alex has set it to (don't reset a row he's already moved to "Read and contemplating" or beyond back to "Need to review").

## 5. End-of-run summary
List which rows were upgraded with their new scores, which couldn't be reached (and why), and how many are still pending if this was a partial sweep.

## Known constraints
- Requires Alex's computer on, Chrome running with the extension, and his own LinkedIn session logged in — if Claude in Chrome isn't reachable, say so plainly and stop rather than trying the built-in browser as a silent substitute (it can't log into LinkedIn).
- Never send email, reply to a lead, or click apply.
- Never advance a row's Status — that stays Alex's call.