---
name: "job-lead-intake-scan"
description: "Scan Alex's Gmail for new job leads (NorthStar Staffing/Jordan, LinkedIn job alerts, MyJobHelper), screen them for fit, and log new candidates to the Job Search Tracker. Cloud-only — runs on the daily schedule, no computer/browser needed."
---

# Job Lead Intake Scan

Finds new job leads in Alex Example's inbox, does a first-pass fit screen, and logs them to his Job Search Tracker. This is the intake stage of a three-skill pipeline: this skill only ever writes rows with status "Need to review" and a Tier tag in Notes — it never advances a status, never emails anyone, never generates a resume, and never opens a LinkedIn job page. Real-JD scoring happens later in `job-lead-tier2-scoring` (cloud, web search, can run unattended), and anything it can't reach goes to `job-lead-manual-jd-lookup` (Alex's own browser, on demand).

Runs daily via a scheduled task (8:00am local time) entirely through the Gmail and Google Drive connectors — by design it must work even when Alex's laptop is off, so never reach for a device or browser tool here.

## Key files (Google Drive, folder "JobSearch", folder id `<JOBSEARCH_FOLDER_ID>`)
- Master resume (source of truth for fit-scoring): `Alex_Example_Resume-Master.docx`, Drive id `<RESUME_FILE_ID>`. These skills only read it, so its ID is stable.
- Tracker: `Job_Search_Tracker.xlsx`, sheets "Job Log" and "Status Guide" (the scoring-tier legend lives in "Status Guide"). **Never hardcode the tracker's file ID.** It changes every time the tracker is saved from the cloud (see "Saving the tracker" below), so always look it up by name.

## Finding the current tracker
Call the Drive connector's `search_files` with:
`title = 'Job_Search_Tracker.xlsx' and parentId = '<JOBSEARCH_FOLDER_ID>'`
- The exact-title match deliberately skips older copies, which are renamed `Job_Search_Tracker (superseded ...).xlsx`.
- Exactly one result: that's the tracker. Note its `id`, `fileSize` and `modifiedTime`.
- No result: stop and report it. Don't create a new tracker.
- More than one: an earlier save didn't finish its rename step. Use the one with the latest `modifiedTime`, say so in the end-of-run summary, and leave the other one alone for Alex to sort out.

`read_file_content` on the tracker gives a quick text view of every row (handy for dedup and for picking rows to work on). For edits you need the real .xlsx (below).

## Saving the tracker
**Preferred: Alex's computer is linked.** Edit the synced copy in his connected JobSearch folder in place through the device shell, after checking it isn't open in Excel (`lsof`/`fuser`). Google Drive for desktop syncs the change into the same Drive file, so the file ID and link don't change.

**Cloud path (scheduled runs, or no linked device).** The Drive connector can change a file's title or folder but not its contents, so saving means uploading a replacement file:
1. Right before editing, repeat the lookup above and confirm `modifiedTime` hasn't changed since you read the tracker. If it has, someone saved in between: download again and redo your edits on the new copy. (If you uploaded the tracker yourself earlier in this same session and its `modifiedTime`/`fileSize` are unchanged, you can edit the local file you uploaded instead of downloading.)
2. Download with `download_file_content`, write the base64 to disk, decode it, and confirm the decoded byte count equals the Drive `fileSize` before trusting it. Edit with openpyxl. Always re-read the specific rows you're about to change from this fresh copy; don't trust values seen earlier in the conversation.
3. Keep the workbook lean. Never pre-style empty rows beyond the data: the original tracker had hundreds, which bloated it until it couldn't be round-tripped at all. After saving, recompress the .xlsx with zip level 9.
4. Base64 the saved file with `base64 -w0`. To read it back, `fold -w 1000` it and Read it about 16 lines at a time, since Read truncates one long line. Pass it to `create_file` as one continuous string with **no line breaks**, because the connector rejects base64 that contains newlines. For anything over ~25K characters, first Write the exact string you're about to send to a scratch file and compare its sha256 with the real base64. Only upload once they match.
5. Call `create_file` with title `Job_Search_Tracker.xlsx`, `parentId` set to the JobSearch folder id, `contentMimeType` `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, and `disableConversionToGoogleType` true.
6. Check that the returned `fileSize` equals your local file's size. `read_file_content` can return empty text for a few minutes after an upload while Drive indexes the file; that is not corruption.
7. Only after step 6 passes, rename the previous copy with `update_file` to `Job_Search_Tracker (superseded YYYY-MM-DD HHMM).xlsx`. Never trash or delete it; Alex cleans those up himself.
8. In the end-of-run summary, give Alex the new file's link, because his old link now opens the superseded copy.

**Size limit.** The whole base64 string has to go out in a single tool call, which gets unreliable beyond roughly 45-50K characters (a workbook of about 35KB). If the tracker grows past that, don't attempt the cloud upload. Stop, report the size, and recommend running on Alex's computer (device path above) or moving Closed/Rejected rows into a separate archive workbook.

- NorthStar Staffing leads/resumes subfolder: `JobSearch/NorthStar Staffing`

### Adding rows
When inserting into "Job Log", don't append at `ws.max_row + 1`: if the sheet carries styling beyond the real data, `max_row` is inflated and new rows get buried where Alex won't see them (this happened once). Find the last row that actually has a `JS-0xx` value in the ID column and use `ws.insert_rows(that_row + 1, amount=N)`, copying the style from that last real row. Make the Job Description cell a real hyperlink (text "View posting"), and update the "Need to review" and "Total" counts on the Status Guide sheet. Make all of a run's additions in one save, because every cloud save creates a new file.

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

- **LinkedIn and MyJobHelper leads:** score from the alert content only (this is "Tier 1" — title/company-based, not a real JD read). Never try to open the posting here — LinkedIn blocks WebFetch via robots.txt and requires a signed-in browser this skill doesn't have. Finding the real JD is `job-lead-tier2-scoring`'s job (web search off LinkedIn), with `job-lead-manual-jd-lookup` as the browser fallback.
- **NorthStar Staffing links and other non-LinkedIn ATS links** (Greenhouse, Lever, iCIMS, Workday, direct company career pages): these don't need Alex's own browser session, so you may attempt a real fetch with WebFetch and score those with a full JD read (if the site blocks WebFetch, leave the row at Tier 1 - `job-lead-tier2-scoring` or `job-lead-manual-jd-lookup` will pick it up) — tag those rows as fully-scored rather than Tier 1.

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
- Never use a device/browser tool here — that dependency belongs entirely to `job-lead-manual-jd-lookup`.
- Gmail attachments (a JD sent as a raw attachment, not a link) can't be downloaded directly — flag it in Notes for Alex to "Add to Drive" himself.