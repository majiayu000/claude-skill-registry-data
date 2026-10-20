---
name: "job-lead-tier2-scoring"
description: "Cloud-only, cron-friendly (every 2-4 hours): for tracker rows the user has ticked in the Run Tier 2 column, or rows they name, search the open web and fetch the real JD from company/ATS pages (never LinkedIn directly), save it to Drive, then score and update the row. Re-ticking a row rescores its saved JD against the user's current resume without searching again. Does nothing when no row is ticked. Rows it can't resolve are marked T2-pending-manual for job-lead-manual-jd-lookup."
---

# Job Lead Tier 2 Scoring (web-search based)

The enrichment stage of the pipeline. `job-lead-intake-scan` logs new leads daily with a quick Tier 1 (title-only) score. The user reviews them and ticks **Run Tier 2** on the rows worth a closer look. This skill takes only those rows, finds the *real* job description via open web search, saves it, and rewrites the row with a properly sourced score, gaps and a full fit report. When the user adds something to their resume and re-ticks the row, it rescores the saved JD so they can see whether the gap closed. It never opens LinkedIn and never touches a browser or the linked device, so it can run unattended on a schedule or on demand. Rows it can't resolve are left for `job-lead-manual-jd-lookup`, which needs the user's own computer and is run by the user, never called from here.

## Key files and systems
- Tracker: load the `job-tracker` skill with the Skill tool before any Sheets call. It defines how to find the tracker, the columns this skill owns, the Score Tier values, the Run Tier 2 checkbox, and the job files in Drive (`<ID>_JD.md` and the fit reports). Follow it exactly.
- Scoring: load the `job-fit-rubric` skill before setting any Fit Score. It holds the evidence-table format and `score.py`.
- **The full resume** (found as `job-tracker` describes, from the profile's **Candidate → Full resume**) is the only evidence used for scoring. It holds all of the user's experience, not a two-page selection, so score against the whole file. Read-only for these skills; the user edits it. If it isn't found, stop and report that.

## 1. Pick the rows
- **On demand, with rows named** (IDs or companies): use exactly those, ticked or not.
- **Otherwise** (the scheduled run, or "run Tier 2"): every row whose **Run Tier 2** reads `TRUE`, lowest ID first, at most the profile's **Tier 2 rows per run** (10 if blank). Ticked rows beyond that stay ticked for the next run.
- If nothing is ticked, stop right after reading the tracker and report "No rows ticked for Tier 2". Don't load the resume or search for anything.
- Never pick rows on your own. An unticked Tier 1 row stays Tier 1 until the user ticks it, however promising it looks.

## 2. Rescore or first read
For each picked row, look for its saved JD: `search_files` with `title = '<ID>_JD.md'`.
- **Found: this is a rescore.** Read it (as `job-tracker` **Reading Markdown files** describes), and read the latest fit report (`title contains '<ID>_fit_r'`, highest run number). Skip step 3; don't search the web. Go to step 4. If the JD exists but no fit report does (an earlier run stopped partway), build the evidence table fresh and write `r1`.
- **Not found: this is a first read.** Find the JD (step 3). When you get one, create `<ID>_JD.md` in the job's folder before scoring (`job-tracker` **Job files in Drive** has the format).

## 3. Finding the real JD (web search only, no browser)
For each first-read row:
1. Build a search query from Company + exact Job Title, quoted (e.g. `"Acme Corp" "Senior Widget Architect" job description`). Add a distinguishing detail (location, or a req/job number from the row) if the title alone is generic. If the title is truncated (`Senior Projec...`), search on the company and the words you have.
2. Prefer, in this order: (a) the company's own careers page, (b) a direct ATS posting (`job-boards.greenhouse.io`, `jobs.lever.co`, iCIMS, Workday, `careers.<company>.com`), (c) a job-board mirror (Indeed, BuiltIn, ZipRecruiter, dreamworkhq, freehire, Monster, Dice, TheMuse, JobRight, Lensa, CareerBuilder, etc.) only if (a)/(b) aren't found or don't fetch cleanly.
3. WebFetch the most promising 2-3 candidate URLs, asking for responsibilities, required qualifications, and preferred qualifications verbatim. If one comes back empty (a JS-rendered page with no server-rendered text), a 403, or says the posting is closed/filled, move to the next candidate rather than retrying the same URL.
4. **Never fetch a `linkedin.com/jobs/view/...` URL directly.** WebFetch is blocked by LinkedIn's robots.txt regardless of how the search led there. If every candidate outside LinkedIn fails, that's this skill's dead end for the row (step 5).
5. Stop after 2-3 solid attempts per row. This is meant to be a fast automated pass, not an exhaustive hunt.

## 4. Scoring
Load the `job-fit-rubric` skill and follow it. In short:
1. **Judgment:** build its evidence table in `tier2` mode: every requirement quoted from the JD, marked required or preferred, with full-resume evidence strong / partial / none, plus title/seniority (against the profile's Target roles) and work arrangement (against the profile's Location).
2. **Arithmetic:** run its `score.py` on the table. The `score` it returns is the Fit Score, unchanged. If it looks wrong, fix the table, not the number.

**On a rescore,** start from the evidence table in the latest fit report. Keep its `requirements` entries exactly as they are (same text, same required/preferred), and judge each one's `evidence` and `resume_evidence` again against the current full resume. Re-judge `title_seniority` too; keep `work_arrangement` unless the JD says otherwise. Holding the requirement list fixed means a changed score comes from the user's resume edits, not from reading the JD differently.

`score.py` caps any job that needs a move the user won't make at 3.

Write the 3 biggest gaps into the Gaps cell in the format defined in `job-fit-rubric`.

## 5. Updating the row
Do the research for all picked rows first, then write the updates row by row, re-finding each row by ID just before writing it (`job-tracker` **Writing**). Update the existing row in place; never create a duplicate.

- **Scored (first read or rescore):** first create the next fit report, `<ID>_fit_r<n>_<date>.md` (`r1` on a first read, one higher than the latest on a rescore), with the score, the changes since the last run, the gaps and the evidence table (format in `job-tracker`). Then write Fit Score, Gaps, **Fit Report** (link to the new file) and **Score Breakdown**:
  - First read: **Score Tier** `T2`, Score Breakdown `JD: <full JD URL> (web search) | <breakdown from score.py>`. Fill Pay Range and Type / Location if they're blank and the JD states them. If Job Description links only to the Gmail message, replace it with the JD URL.
  - Rescore: leave Score Tier as it is (`T2` or `T2-manual`: where the JD came from hasn't changed). Score Breakdown keeps its source and adds the run: `JD: <source> (<web search or browser>, rescore r<n>, was <previous score>) | <breakdown>`.
- **No usable JD after the candidates in step 3:** leave Fit Score and Gaps as they are (the Tier 1 score stands). Set **Score Tier** `T2-pending-manual` and put the attempt in front of the existing breakdown: `Tier 2 web search <date>: no JD off LinkedIn (<reason: no non-LinkedIn source found / sources blocked or JS-rendered>). Tried: <domains> | <previous breakdown>`.
- **The posting is closed or filled:** leave the score, set **Score Tier** `T2-closed`, and note it: `Posting closed per <domain> <date> | <previous breakdown>`. Don't set Status; the user decides.

Then, for every outcome, set **Tier 2 Date** and **Last Updated** to today, and finally untick **Run Tier 2** (write `false`). Unticking last means a run that stops partway leaves the row ticked for the next run.

## 6. End-of-run summary
Always end with a short summary, never silence:
- Rows scored `T2` on a first read, with old → new Fit Score.
- Rows rescored, with old → new Fit Score and the requirements whose evidence changed (or "no change").
- Rows marked `T2-pending-manual`, with why (one line each), and a reminder that `job-lead-manual-jd-lookup` picks them up when the user is at their computer.
- Rows marked `T2-closed`.
- How many ticked rows are still waiting for the next run.

## Known constraints
- Cloud-only by design: never use a device/browser tool here, and never attempt LinkedIn directly. That's `job-lead-manual-jd-lookup`'s job.
- Only rows the user ticked or named. Never sweep the tracker.
- Never change Status, and never write Next Action / Notes.
- Never send email, reply to a lead, or click apply. Read-only research.
- Never set a Fit Score that didn't come from `job-fit-rubric`'s `score.py`.
- Never edit, replace or trash a JD file or fit report. Each run creates a new fit report; the JD file is written once.
- Safe to run unattended on a schedule: every tool it uses (WebSearch, WebFetch, the Drive and Sheets connectors) works without the user present or any interactive approval, and an empty queue costs one tracker read. A rescore uses no web search at all.
