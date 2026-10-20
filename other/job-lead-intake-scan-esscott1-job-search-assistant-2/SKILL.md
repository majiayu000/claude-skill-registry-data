---
name: "job-lead-intake-scan"
description: "Scan Alex's Gmail for new job leads (NorthStar Staffing/Jordan, LinkedIn job alerts, MyJobHelper), screen them for fit, and log new candidates to the Job Search Tracker. Cloud-only — runs on the daily schedule, no computer/browser needed."
---

# Job Lead Intake Scan

Finds new job leads in Alex Example's inbox, does a first-pass fit screen, and logs them to his Job Search Tracker. This is the intake half of a two-skill pipeline: this skill only ever writes rows with status "Need to review" and a Tier tag in Notes — it never advances a status, never emails anyone, never generates a resume, and never opens a LinkedIn job page. Deeper, browser-based JD scoring is a separate skill, `job-lead-tier2-scoring`, run on demand.

Runs daily via a scheduled task (8:00am local time) entirely through the Gmail and Google Drive connectors — by design it must work even when Alex's laptop is off, so never reach for a device or browser tool here.

## Key files (Google Drive, folder "JobSearch")
- Master resume (source of truth for fit-scoring): `Alex_Example_Resume-Master.docx`, Drive id `<RESUME_FILE_ID>`
- Tracker: `Job_Search_Tracker.xlsx`, Drive id `<TRACKER_FILE_ID>`, sheet "Job Log" (scoring-tier legend lives in sheet "Status Guide")
- NorthStar Staffing leads/resumes subfolder: `JobSearch/NorthStar Staffing`

Download the tracker with `download_file_content`, edit with openpyxl, re-upload with `update_file`. Read Master as text via Drive for scoring.

IMPORTANT: when editing the tracker with openpyxl, do not blindly append at `ws.max_row + 1` — this sheet has cell styling pre-applied for hundreds of rows beyond the last real data row, which inflates `max_row` far past the visible data and buries new rows where Alex won't see them (this happened once and had to be fixed). Instead, find the last row that actually has a value in the ID column and use `ws.insert_rows(that_row + 1, amount=N)`, copying the style from the last real data row onto the new rows.

## 1. Look back 7 days, always
Always search a trailing 7-day window (`newer_than:7d`), regardless of how often this skill is actually scheduled to run — if the cron interval is ever widened, a fixed 7-day lookback still won't miss anything, it'll just reprocess a few already-seen emails, which dedup (below) handles for free. Do not narrow the window to match the schedule.

## 2. Gmail sources to scan
- NorthStar Staffing / Jordan: `from:recruiter@example.com`
- LinkedIn single-job alerts: `from:jobalerts-noreply@linkedin.com` — each email is itself a digest of 2-6 job cards (title/company/location, sometimes a salary band), not one job. Parse every card, not just the one in the subject line.
- LinkedIn "similar jobs" recommendations: `from:jobs-noreply@linkedin.com` — lower-signal digests; include but treat as lower priority.
- MyJobHelper: `from:info@alerts.myjobhelper.com` — single-posting alerts, but low-signal/high-noise (many are generic mismatched blasts, e.g. retail "Full Time Assistant"). Screen hard.

Explicitly EXCLUDE other LinkedIn mail that isn't a job posting: `messages-noreply@`, `notifications-noreply@`, `groups-noreply@`, `updates-noreply@`, `editors-noreply@linkedin.com`.

If Alex mentions a new source, add its sender pattern here.

## 3. Screening and scoring (Tier 1, plus opportunistic real fetches)
From the email body alone (title, company, location, salary if shown), judge plausible fit against Alex's background: enterprise/solutions architecture, IT PMO/delivery leadership, technical program/project management, AI enablement and adoption strategy, cloud/infrastructure consulting. Discard obvious non-fits (individual-contributor retail/trades roles, unrelated disciplines) without adding them to the tracker. When unsure, err toward including it.

- **LinkedIn and MyJobHelper leads:** score from the alert content only (this is "Tier 1" — title/company-based, not a real JD read). Never try to open the posting here — LinkedIn blocks WebFetch via robots.txt and requires a signed-in browser this skill doesn't have. That's `job-lead-tier2-scoring`'s job.
- **NorthStar Staffing links and other non-LinkedIn ATS links** (Greenhouse, Lever, iCIMS, Workday, direct company career pages): these don't need Alex's own browser session, so you may attempt a real fetch (WebFetch, falling back to the built-in browser for sites that block fetch, as done for World Travel Holdings' iCIMS postings) and score those with a full JD read — tag those rows as fully-scored rather than Tier 1.

## 4. Dedup before writing
Before adding any row, read the current tracker's Company + Job Title (and Job Description link, if present) and skip anything already logged. Match loosely (same company + substantially same title) since the same LinkedIn job can arrive in more than one digest with different tracking-parameter URLs.

## 5. Writing new rows
- Status is always **"Need to review"**.
- Continue the existing `JS-0xx` ID sequence.
- Fill: Date Found (today), Source, Company, Job Title, Job Description (hyperlink to the posting, or the Gmail message if there's no direct link), Type/Location, Pay Range (if stated), Fit Score, Gap 1-3, Status, Last Updated. Leave Tailored Resume / Resume Created / Date Submitted / Submission Email blank.
- In Next Action/Notes, tag the row "Tier 1 screen" or "full JD" so Alex (and `job-lead-tier2-scoring`) know how much to trust the score. The tracker's "Status Guide" sheet documents this tiering — keep that legend in sync if the logic changes.

## 6. End-of-run summary
Always end with a short summary, never silence: how many new rows were added (one-line list), how many were screened out at Tier 1 and roughly why, and anything flagged as unreachable. If nothing new was found, say so explicitly.

## Known constraints
- Never mark anything "Good fit", "Submitted", or advance a status — this skill only proposes.
- Never send email, reply to a lead, or click apply — read-only scan.
- Never use a device/browser tool here — that dependency belongs entirely to `job-lead-tier2-scoring`.
- Gmail attachments (a JD sent as a raw attachment, not a link) can't be downloaded directly — flag it in Notes for Alex to "Add to Drive" himself.