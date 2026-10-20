---
name: "job-lead-manual-jd-lookup"
description: "On-demand, requires Alex's computer: for tracker rows job-lead-tier2-scoring flagged as unreachable by web search (LinkedIn postings with no JD body, sites that block fetch), read the real JD using Alex's own browser session and update the row."
---

# Job Lead Manual JD Lookup

The manual-fallback half of the Tier 2 pipeline. `job-lead-tier2-scoring` runs cloud-only (web search + WebFetch, no browser) and handles most rows; anything it can't get a JD for - most commonly a LinkedIn posting with "Promoted by hirer / Responses managed off LinkedIn" and no JD body, or a site that blocks WebFetch entirely (JS-rendered career page, 403, a mirror site that needs interactive access) - it flags in the row's Notes rather than guessing. This skill picks up exactly those flagged rows and uses Alex's own logged-in browser to get the real text. It exists as its own skill (rather than a fallback branch inside job-lead-tier2-scoring) specifically so Alex can run it himself, on demand, whenever he's at his machine - it must never run unattended, since it depends on a live browser session and, for some sites, one-time interactive site-access approval that nobody is present to grant on a schedule.

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

This skill needs Alex's computer anyway, so the device path is the normal one here; use the cloud path only if the synced folder isn't reachable from the device shell.

## 1. Figure out which rows to work on
- If Alex named specific row IDs or companies, use those.
- Otherwise, read the tracker and find every row whose Notes contains a job-lead-tier2-scoring recommendation to run this skill (look for "job-lead-manual-jd-lookup" or "Tier 2 (web search) attempted" in Notes) and that hasn't already been upgraded to "Full JD read".
- If there are a lot, do the first few and check in before continuing - this is a slower, browser-driven process per row.

## 2. Fetching the real JD
- **LinkedIn job-view links** (`linkedin.com/.../jobs/view/<id>/`): use **Claude in Chrome**, which runs in Alex's real, already-logged-in Chrome (load its tools via ToolSearch first if deferred). Navigate to the URL, then `get_page_text`. The JD body often loads asynchronously or sits behind a "see more" expansion - wait ~2s and retry once. If it's still not there, the listing genuinely has no JD on LinkedIn (common on "Promoted by hirer / Responses managed off LinkedIn" postings) - leave the row's score as-is, note that LinkedIn confirmed no JD, and move on rather than looping.
- **Other blocked sites** (a mirror or career page job-lead-tier2-scoring found but couldn't fetch - 403, JS-rendered, or needs a login): use the **built-in browser**. It will likely need one-time site access - call `request_access` for that site (scope "site" is fine so it doesn't ask again, or "once" if Alex would rather approve each time) and retry. If Alex declines or doesn't respond to an access prompt, don't push - note that the site couldn't be accessed and move to the next row.
- Start from the candidate URLs job-lead-tier2-scoring already tried (check the row's Job Description link and Notes) before searching fresh - no need to redo its web search from scratch unless those leads are dead ends too.

## 3. Scoring
Same rubric as job-lead-tier2-scoring: fit 1-10 against Master - title/seniority match, required vs. actual years of experience, named tools/methodologies Alex has evidence for, domain/industry match. Quote the JD's actual wording for the top 3 gaps, don't paraphrase vaguely.

## 4. Updating the row
- Update the EXISTING row in place - never duplicate. Never touch Status.
- If you end up on the cloud path, batch all row updates into a single save rather than one upload per row.
- If a usable JD was found: overwrite Fit Score and Gap 1-3, set Notes to `"Full JD read (job-lead-manual-jd-lookup, browser) - <LinkedIn direct / site name>."`, and set Last Updated to today.
- If the posting genuinely has no JD anywhere reachable (LinkedIn confirmed empty and no other source exists), leave the score as-is but update Notes to say so plainly (e.g. `"Manual lookup attempted <date> - LinkedIn confirmed no JD body, no other source found. Still Tier 1."`) and Last Updated to today, so it doesn't get re-flagged forever.

## 5. End-of-run summary
List which rows were upgraded with their new scores, which still couldn't be reached (and why), and how many are still pending if this was a partial sweep.

## Known constraints
- Requires Alex's computer on and reachable: Chrome running with the extension for LinkedIn rows, and/or the desktop app's built-in browser for other blocked sites. If neither is reachable, say so plainly and stop rather than silently falling back to WebFetch (which is exactly what already failed upstream in job-lead-tier2-scoring).
- Never run this on a schedule - it depends on live interactive access (browser session, and possibly a site-access approval) that nobody is present to grant unattended.
- Never send email, reply to a lead, or click apply.
- Never advance a row's Status - that stays Alex's call.