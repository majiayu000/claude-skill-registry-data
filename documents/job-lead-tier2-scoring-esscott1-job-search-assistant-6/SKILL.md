---
name: "job-lead-tier2-scoring"
description: "Cloud-only, cron-friendly: for tracker rows still tagged Tier 1, search the open web and fetch the real JD from company/ATS pages (never LinkedIn directly), then score and update the row. Rows it can't resolve get flagged in Notes recommending job-lead-manual-jd-lookup."
---

# Job Lead Tier 2 Scoring (web-search based)

The enrichment half of a two-skill pipeline. `job-lead-intake-scan` runs daily and logs new leads with a quick Tier 1 (title-only) score; this skill takes rows still tagged Tier 1, tries to find the *real* job description via open web search, and rewrites the row with a properly-sourced score and gaps. It never opens LinkedIn itself and never touches a browser or the linked device, so it can run entirely unattended (a scheduled task) or on demand. A separate skill, `job-lead-manual-jd-lookup`, exists for the rows this skill can't resolve (LinkedIn postings with no JD body, sites that block fetch/search) and requires Alex's own computer - it is run by Alex, not called automatically from here.

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

When run as a scheduled task there is no linked device by definition, so always use the cloud path in that case.

## 1. Figure out which rows to work on
- If Alex named specific row IDs or companies, use those.
- If he asked for "the LinkedIn rows" or similar, read the tracker and find every row whose Notes says "Tier 1 screen" (or equivalent) and has no "Full JD read" tag yet.
- On a scheduled run, or a general sweep, do all outstanding Tier-1 rows that don't already carry a "Tier 2 (web search) attempted" note from today (dedup against same-day re-runs), but check in (or, on schedule, just note it in the end-of-run summary) if there turn out to be a lot - each row costs a few search+fetch calls.
- Skip any row already tagged "Full JD read" - don't re-score it.

## 2. Finding the real JD - web search only, no browser
For each row:
1. Build a search query from Company + exact Job Title, quoted (e.g. `"Acme Corp" "Senior Widget Architect" job description`). Add a distinguishing detail (location, req/job number if visible in the LinkedIn URL slug or the row) if the title alone is generic.
2. Prefer, in this order: (a) the company's own careers page, (b) a direct ATS posting (`job-boards.greenhouse.io`, `jobs.lever.co`, iCIMS, Workday, `careers.<company>.com`), (c) a job-board mirror (Indeed, BuiltIn, ZipRecruiter, dreamworkhq, freehire, Monster, Dice, TheMuse, JobRight, Lensa, CareerBuilder, etc.) only if (a)/(b) aren't found or don't fetch cleanly.
3. WebFetch the most promising 2-3 candidate URLs, asking for responsibilities, required qualifications, and preferred qualifications verbatim. If one comes back empty (JS-rendered SPA with no server-rendered text), a 403, or says the posting is closed/filled, move to the next candidate rather than retrying the same URL.
4. **Never fetch a `linkedin.com/jobs/view/...` URL directly** - WebFetch is blocked by LinkedIn's robots.txt regardless of how the search led there. If every candidate outside LinkedIn fails, that's this skill's dead end for the row (see step 4).
5. Stop after 2-3 solid attempts per row - this is meant to be a fast automated pass, not an exhaustive hunt.

## 3. Scoring
Score fit 1-10 against Master using the established rubric: relevant title/seniority match, required vs. actual years of experience, named tools/methodologies Alex has evidence for in Master, domain/industry match. List the top 3 gaps worded concretely - quote what the JD actually asks for, don't paraphrase vaguely.

## 4. Updating the row
- Update the EXISTING row in place - never create a duplicate. Never touch Status - leave whatever Alex has set it to.
- Do the research for all rows first, then apply every row update in a single save (one upload, one new file ID), not one save per row.
- If the JD lists pay and the row's Pay Range is blank, fill it in. Put the source URL in Notes so job-lead-manual-jd-lookup and Alex can find it.
- If the posting turns out to be closed or filled, say so in Notes and suggest Alex set Status to Closed (don't set it yourself); don't recommend a manual lookup for it.
- **If a usable JD was found:** overwrite Fit Score and Gap 1-3, set Notes to `"Full JD read (job-lead-tier2-scoring, web search) - JD from <domain of the source URL>."`, and set Last Updated to today.
- **If no usable JD could be found after trying the candidates in step 2:** do NOT touch Fit Score or Gap 1-3 (leave the existing Tier 1 score standing). Instead update Notes to record the attempt and point at the manual fallback, e.g.: `"Tier 2 (web search) attempted <date> - no fetchable JD found off LinkedIn ([reason: e.g. no non-LinkedIn source found / sources blocked or JS-rendered / posting appears filled]). Tried: <domains tried>. Recommend running job-lead-manual-jd-lookup (needs Alex's browser) to check the LinkedIn posting or blocked sites directly."` Still update Last Updated to today so Alex can see this was recently touched.

## 5. End-of-run summary
Always end with a short summary, never silence:
- Rows upgraded to a full JD read, with their new scores.
- Rows flagged for manual lookup, with why (one line each).
- How many are still pending if this was a partial sweep.

## Known constraints
- Cloud-only by design: never use a device/browser tool here, and never attempt LinkedIn directly - that's `job-lead-manual-jd-lookup`'s job.
- Never send email, reply to a lead, or click apply - read-only research.
- Never advance a row's Status - that stays Alex's call.
- Safe to run unattended on a schedule since every tool it uses (WebSearch, WebFetch, the Drive connector) works without Alex present or any interactive approval.