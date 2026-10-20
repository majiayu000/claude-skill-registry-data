---
name: "job-tracker"
description: "Shared tracker contract for the job-search skills, not run on its own: job-lead-intake-scan, job-lead-tier2-scoring, job-lead-manual-jd-lookup, tailored-resume-builder and job-tracker-cleanup load it before reading or writing the Job_Search_Tracker Google Sheet. Defines which columns each skill owns, how rows are found, added and updated, the Score Tier values, the Run Tier 2 and Build Resume checkboxes, the per-job JD and fit-report files in Drive, the Archive tab, and canonical_url.py for dedup."
---

# Job Tracker

The single definition of the Job Search Tracker and how skills touch it. Each job-search skill loads this before its first Sheets call and follows it exactly. It doesn't decide what to write (that's the calling skill's job); it decides where and how.

## Files in this skill
- `canonical_url.py`: reduces a job link to its canonical form, the dedup key. Run `python3 <this skill's directory>/canonical_url.py <url> [<url> ...]`. It prints a JSON array of `{"input", "canonical"}`; `canonical` is `""` for links that aren't a posting or can't be resolved without following them.
- `test_canonical_url.py`: checks the rules (`python3 -m pytest -q` in this directory).

## The job-search profile
Everything specific to a user (their name, files, tracker, target roles, location, email sources and housekeeping settings) is in **`job-search-profile.md`** in their Google Drive. The `job-search-profile` skill defines its format and is the only skill that writes it; every other skill reads it first and never assumes a value it doesn't find there.
- **Find it** with `search_files`: `title = 'job-search-profile.md'`, then read it as **Reading Markdown files** below describes.
  - **None found:** stop and say "No job-search profile found. Say 'set up my job search' to create one."
  - **More than one:** stop and list them; ask the user to keep one (`job-search-profile` resolves this).
- **Read it as written:** each setting is a `- Key: value` line under a section heading; Email sources and Career sites are tables. A section that isn't there (an older profile may have no Career sites) counts as empty. A blank value a skill needs is a stop, not a guess. Name the setting in the summary: `Profile setting "Location → Home area" is blank; say "update my job search profile"`.
- The settings each skill relies on:

| Setting | Used by |
|---|---|
| Candidate → Full resume | every skill that scores, and the resume builder |
| Candidate → Resume style, Tailored resume prefix; Tracker → Local Drive folder | tailored-resume-builder |
| Tracker → Sheet ID, Sheet name, Folder ID | every skill (finding the tracker and the job folders) |
| Tracker → Time zone | every skill that writes a date |
| Target roles | intake screening, and `title_seniority` in `job-fit-rubric` |
| Location | `work_arrangement` in `job-fit-rubric` |
| Email sources, Career sites, Never scan, Housekeeping → Career site leads per run | job-lead-intake-scan |
| Housekeeping → Archive after days | job-tracker-cleanup |
| Housekeeping → Tier 2 rows per run | job-lead-tier2-scoring |

## Finding the tracker
- Open the sheet by the profile's **Sheet ID** with the Sheets connector; its `spreadsheetId` is used for every Sheets call. If that fails, search for it: `title = '<Sheet name>' and mimeType = 'application/vnd.google-apps.spreadsheet' and parentId = '<Folder ID>'`.
  - Exactly one result: use it, and mention in the summary that the profile's Sheet ID is out of date.
  - No result: stop and report it. Never create a tracker here; `job-search-profile` does that with the user's agreement.
- **The full resume** is the file named in **Candidate → Full resume**, in the profile's tracker folder: `title = '<Full resume>' and parentId = '<Folder ID>'`. Read it as **Reading Markdown files** below describes. If it isn't found, stop and say so.
- **Reading Markdown files** (the profile, the full resume, saved JDs and fit reports): use the Drive connector's `download_file_content` and base64-decode the result. `read_file_content` can return an empty result for a Markdown file created in the last few minutes, which is exactly when a rescore or a resume build reads a JD file another run just wrote.
- Tabs: "Job Log" (one row per active job), "Status Guide" (status meanings, the scoring legend, and `COUNTIF` totals), and "Archive" (stale rows moved out of the Job Log by job-tracker-cleanup; created on its first run).

## Columns
Find every column by its header text on each run, never by letter: the user may add, move or hide columns. If a column a skill needs is missing, stop and report `Tracker is missing the "<header>" column`. Don't create it or write the value somewhere else.

| Header | Written by | Contents |
|---|---|---|
| ID | intake | `JS-` and a number, at least three digits: one more than the highest number already used (see **Adding rows**) |
| Date Found | intake | Date the row was logged (today), `YYYY-MM-DD` |
| Source | intake | The **Source** label, from the profile's Email sources or Career sites, of where the lead came from |
| Company, Job Title | intake | From the email; a truncated title (ending in `...`) stays as the email shows it |
| Job Description | intake; Tier 2 skills | `=HYPERLINK("<url>","View posting")`. The canonical URL when there is one, otherwise the Gmail message. A Tier 2 skill may replace a Gmail-message link with the JD URL it found, and never replaces a posting link |
| Type / Location | intake; Tier 2 skills fill it if blank | As stated (e.g. `Remote`, `Austin, TX (hybrid)`) |
| Pay Range | intake; Tier 2 skills fill it if blank | As stated, only if stated |
| Fit Score (1-10) | intake, Tier 2 skills | The `score` from `job-fit-rubric`'s `score.py`, unchanged |
| Score Tier | intake, Tier 2 skills | One of the values in **Score Tier values** below |
| Gaps | intake, Tier 2 skills | Format defined in `job-fit-rubric` |
| Fit Report | Tier 2 skills; intake when it reads a full JD | `=HYPERLINK("<Drive URL of the latest fit report>","r<n>: <score>")` (see **Job files in Drive**) |
| Run Tier 2 | **The user ticks**; Tier 2 skills untick | Checkbox. Ticked means "score this row against the real JD and the current resume" |
| Build Resume | **The user ticks**; tailored-resume-builder unticks | Checkbox. Ticked means "build a tailored resume for this row" |
| Status | **The user**; intake writes `Need to review` on new rows only | Dropdown. No skill ever changes it after that |
| Next Action / Notes | **The user only** | No skill writes here |
| Contact / Referrer | The user; intake when the source's profile notes say it's a recruiter | The recruiter's name, written as on earlier rows from that source |
| Tailored Resume, Resume Created | tailored-resume-builder | `=HYPERLINK("<URL of the tailored resume's Google Doc>","<its name>")`; without a Google Doc, a link to the PDF, or the file name followed by `(syncing to Drive)` or `(download; add to <Company_Folder>/)`; date built |
| Date Submitted, Submission Email | The user | |
| Last Updated | every skill that writes the row | Today, `YYYY-MM-DD` |
| Source Email | intake | `=HYPERLINK("https://mail.google.com/mail/u/0/#all/<Gmail message id>","Email")`. Blank for a lead from a career site |
| Gmail Message ID | intake | The Gmail message id the lead came from. Blank for a lead from a career site |
| Email Received | intake | Date the email arrived (its Gmail date, in the profile's time zone), `YYYY-MM-DD`. Blank for a lead from a career site |
| Score Breakdown | intake, Tier 2 skills | How the score was reached: `<source> \| <breakdown string from score.py>` (formats below) |
| Tier 2 Date | Tier 2 skills; intake when it reads a full JD | Date of the last Tier 2 attempt, whatever the outcome |
| Canonical URL | intake | Plain text output of `canonical_url.py`, blank if it returned `""`. The dedup key |

Never write anything a row's owner column doesn't list for your skill. In particular, no skill writes **Status** (after the first write of a new row) or **Next Action / Notes**.

## Score Tier values

| Value | Meaning | Set by |
|---|---|---|
| `T1` | Scored from the alert email only; no JD read. Capped at 8 | intake |
| `T2` | Scored against the full JD, found by web fetch | intake (direct company or ATS links), job-lead-tier2-scoring |
| `T2-manual` | Scored against the full JD, read in the user's browser | job-lead-manual-jd-lookup |
| `T2-pending-manual` | Tier 2 web search found no usable JD. The T1 score stands until job-lead-manual-jd-lookup runs | job-lead-tier2-scoring |
| `T2-no-jd` | Manual lookup confirmed there's no JD anywhere reachable. The T1 score stands and the row isn't flagged again | job-lead-manual-jd-lookup |
| `T2-closed` | The posting is closed or filled. The user decides whether to set Status to Closed | either Tier 2 skill |

### Score Breakdown formats
- T1: `Alert email | <breakdown>`, or `Career site listing | <breakdown>` for a lead from a career site
- T2: `JD: <full JD URL> (web search) | <breakdown>` (intake writes `(intake fetch)`)
- T2-manual: `JD: <full JD URL, or "LinkedIn direct"> (browser) | <breakdown>`
- A rescore adds the run and the previous score inside the brackets: `JD: <full JD URL> (web search, rescore r3, was 6) | <breakdown>`.
- An attempt that didn't produce a new score keeps the old breakdown after a note: `<note> | <previous breakdown>`, where the note is e.g. `Tier 2 web search 2026-10-14: no JD off LinkedIn (sources JS-rendered). Tried: acme.com, builtin.com`, `Manual lookup 2026-10-14: LinkedIn shows no JD body, no other source`, or `Posting closed per acme.com 2026-10-14`.
- A JD that came as an email attachment: `JD is an email attachment; add it to Drive | <breakdown>`.

## The Run Tier 2 checkbox (the human gate)
Tier 2 scoring costs several searches and fetches per row, so it runs only on rows the user picks:
1. The user ticks **Run Tier 2** on any rows they want scored against the real JD, usually after sorting by Fit Score.
2. job-lead-tier2-scoring runs on a schedule and processes only ticked rows (or rows the user names in an on-demand run).
3. When a row is finished, whatever the outcome (`T2`, `T2-pending-manual` or `T2-closed`), the skill writes its results, sets **Tier 2 Date** to today, and then unticks **Run Tier 2** as the last write for that row. If a run stops partway through, the row stays ticked and the next run retries it.
4. **Re-ticking is a rescore.** If the row already has a saved JD (`<ID>_JD.md`, below), job-lead-tier2-scoring scores that same JD against the current full resume, keeping the previous run's requirement list, and doesn't search the web again. This is how the user checks whether a resume edit closed a gap; they can re-tick the same row as often as they like. To force a fresh fetch (the posting changed), they trash `<ID>_JD.md` first.

## The Build Resume checkbox
Building a tailored resume is on demand only, never scheduled:
1. When the user is done iterating on a row's gaps, they tick **Build Resume**.
2. They then ask for "build ticked resumes" (or names rows). tailored-resume-builder processes only ticked or named rows.
3. A row needs a saved JD (`<ID>_JD.md`). If it has none, the builder leaves the box ticked and reports "run Tier 2 first".
4. After the resume files are saved, the builder writes **Tailored Resume**, **Resume Created** and **Last Updated**, then unticks **Build Resume** as the last write. Re-ticking builds a new version; earlier versions are never overwritten.

## Checkbox cells
Sheets returns checkbox cells as the strings `TRUE` and `FALSE`. Untick by writing the boolean `false` with `update_values`. Write `false` into Run Tier 2 and Build Resume for every new row.

## Job files in Drive
Each job that gets a full JD read has files in a folder for its company, so the JD stays fixed while the user iterates and every scoring run is kept.
- **Folder:** `<tracker folder>/<Company_Folder>/` (the profile's **Folder ID**), where `<Company_Folder>` is the Company cell with every run of characters other than letters and digits replaced by `_`, and leading or trailing `_` removed (`PwC (US)` → `PwC_US`, `Acme Corp.` → `Acme_Corp`). Find it with `search_files`: `title = '<Company_Folder>' and mimeType = 'application/vnd.google-apps.folder' and parentId = '<Folder ID>'`. Create it with `create_file` (`mimeType` folder) if it's missing.
- **Write once, never edit.** The Drive connector can create files but can't change their content. Create every file with `create_file`: `parentId` the job's folder, `contentMimeType` `text/markdown`, `disableConversionToGoogleType` true, and the text in `textContent`. Never replace or trash an existing job file; that's the user's call.
- **Find job files by title**, not by folder: IDs are unique. `title = '<ID>_JD.md'` for the JD; `title contains '<ID>_fit_r'` for fit reports, taking the highest run number.

**`<ID>_JD.md`**: the job description, written once, the first time any skill reads a full JD for the row:
```
# <ID> <Company>: <Job Title>
Source: <JD URL, or "LinkedIn direct (browser)">
Fetched: <YYYY-MM-DD> by <skill name>

<the JD's responsibilities, required and preferred qualifications, and any location, pay and arrangement details, verbatim as read>
```

**`<ID>_fit_r<n>_<YYYY-MM-DD>.md`**: one new file per scoring run against that JD (`r1` for the first):
~~~
# <ID> <Company>: <Job Title>, fit run r<n>
Score: <score> (<Score Tier>), was <previous score> in r<n-1>    (leave out "was …" in r1)
Breakdown: <breakdown from score.py>
JD: <ID>_JD.md · Resume: <full resume file> last modified <its modifiedTime date>

## Changes since r<n-1>
- <requirement, short>: <old evidence> → <new evidence>
(or "First run." in r1, or "No changes." when nothing moved)

## Gaps
| Requirement | Type | Evidence | Resume evidence |
(every requirement marked none, then partial; required before preferred)

## Met
| Requirement | Type | Resume evidence |
(every requirement marked strong)

## Evidence table
```json
<the job-fit-rubric evidence table exactly as passed to score.py>
```
~~~
After creating it, write the row's **Fit Report** link to the new file's `viewUrl`.

## Reading
- `get_values` on `'Job Log'!A1:AZ`. Row 1 is the header.
- `get_values` returns what a cell displays, so a `HYPERLINK` cell reads as `View posting` or `Email`. Use **Canonical URL** for matching rather than the link cells. To see a link's target, read that cell with `get_spreadsheet` (`includeGridData` true, field `sheets.data.rowData.values.userEnteredValue`).

## Writing
- **Find rows by ID** at the moment you write, never by a row number remembered from earlier. The user may sort or filter between your read and your write. Re-read the row just before writing and confirm its ID matches.
- **Update** with `update_values` on only the cells your skill owns in that row (A1 ranges such as `'Job Log'!J14:K14`, one range per run of adjacent cells). Never rewrite whole rows or the whole sheet.
- **Links** go in with `update_formulas`. Never store a link that still has a tracking query: LinkedIn email links carry a one-time sign-in token (`otpToken`). Always write the canonical URL for LinkedIn.
- **Dates** are `YYYY-MM-DD` text, and "today" is today in the profile's time zone.
- **Status Guide** totals are `COUNTIF` formulas. Never write numbers over them. When the tiers or the rubric change, the legend on that tab is updated in the same change.

## Adding rows
New rows go at the **top** of the Job Log, newest first, so the latest leads are what the user sees on opening the sheet.
1. **Number them.** The next ID is one more than the highest `JS-` number in the ID column of the Job Log **and** the Archive, whatever order the rows are in (the user may have sorted them). An archived ID is never reused. Number a run's new leads oldest email first, so the newest lead gets the highest ID.
2. **Insert them under the header** with `insert_dimension`: `dimension` ROWS, `startIndex` 1, `endIndex` 1 + the number of new rows, `inheritFromBefore` **false**, so they copy the formatting, dropdown and checkboxes of the first data row below them rather than the header's.
3. **Fill them newest first:** the highest ID in row 2, then descending. Use `update_values` and `update_formulas`, and write all of a run's new rows in one pass.

If the Job Log has no data rows yet, insert under the header the same way and set the Status dropdown and the checkbox validation on the new rows yourself.

## Dedup
Before adding a lead, check it against the Job Log, the Archive tab (if there is one), and the leads already accepted in this run. A job that was archived stays archived; it isn't logged again.
1. Run `canonical_url.py` on the lead's posting link. If the result isn't `""` and matches an existing **Canonical URL**, it's a duplicate.
2. Otherwise, the same company and substantially the same title is a duplicate. A truncated title such as `Senior Projec...` matches any title it's the start of. Rows logged before the Canonical URL column existed are caught this way, and so is the same job reached two ways (an alert email's link and the company's career site).

## The Archive tab
Rows the user never acted on are moved here by job-tracker-cleanup after the profile's **Archive after days** (30 by default), so the Job Log stays reviewable.
- **Columns:** the Job Log's headers, then **Archived On** (`YYYY-MM-DD`). Columns are matched **by header text**, never by position, because the Job Log can gain columns after the Archive was made. A header the Job Log has and the Archive lacks is added to the Archive before **Archived On**; Archive columns are never removed or reordered.
- **Order:** most recently archived at the top, under the header.
- **Moving rows:** only job-tracker-cleanup moves rows between the tabs, always in one `update_spreadsheet` batch tied to the revision it read (`writeControl.requiredRevisionId`), so a row is never lost or duplicated halfway.
- **Read-only for everything else:** other skills read the Archive for dedup and ID numbering, and never write to it. A skill asked to score or build a resume for an archived row says it's archived and suggests restoring it.
- Nothing is ever deleted from the Archive.

## Failure rules
- If a Google Sheets call fails because the connector isn't available or authorized, stop and report "Google Sheets connector unavailable". Don't fall back to downloading or uploading an .xlsx, or to editing a copy on the user's computer.
- If a write fails partway through a row, report which ID and which cells, and don't retry blindly. Re-read the row first.

## Known constraints
- This skill defines the contract; it never runs on its own and never decides what a score or status should be.
- Only `job-search-profile` creates a tracker, and only when the user agrees. If it's missing, every other skill stops and says so.
- Nothing user-specific is written in this skill; it all comes from the job-search profile.
