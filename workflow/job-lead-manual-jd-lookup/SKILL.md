---
name: "job-lead-manual-jd-lookup"
description: "On-demand, requires the user's computer: for tracker rows marked T2-pending-manual (job-lead-tier2-scoring couldn't reach the JD by web search: LinkedIn postings with no JD body, sites that block fetch), read the real JD using the user's own browser session and update the row."
---

# Job Lead Manual JD Lookup

The manual fallback of the Tier 2 pipeline. `job-lead-tier2-scoring` runs cloud-only (web search + WebFetch, no browser) on the rows the user ticks. When it can't get a JD (most commonly a LinkedIn posting with "Promoted by hirer / Responses managed off LinkedIn" and no JD body, or a site that blocks WebFetch: a JS-rendered career page, a 403, a mirror that needs interactive access), it marks the row `T2-pending-manual` rather than guessing. This skill picks up exactly those rows and uses the user's own signed-in browser to get the real text. It's a separate skill so the user can run it themselves, on demand, when they're at their computer. It must never run unattended: it depends on a live browser session and, for some sites, a one-time site-access approval that nobody is present to grant on a schedule.

## Key files and systems
- Tracker: load the `job-tracker` skill with the Skill tool before any Sheets call. It defines how to find the tracker, the columns this skill owns, the Score Tier values and the job files in Drive. Follow it exactly.
- Scoring: load the `job-fit-rubric` skill before setting any Fit Score. It holds the evidence-table format and `score.py`.
- **The full resume** (found as `job-tracker` describes, from the profile's **Candidate → Full resume**) is the only evidence used for scoring. It holds all of the user's experience, not a two-page selection, so score against the whole file. Read-only for these skills; the user edits it. If it isn't found, stop and report that.

## 1. Pick the rows
- If the user named specific row IDs or companies, use those.
- Otherwise, every row whose **Score Tier** is `T2-pending-manual`, lowest ID first.
- If there are more than 5, do the first 5 and check in before continuing. This is a slower, browser-driven process per row.

## 2. Fetching the real JD
- **LinkedIn job-view links** (`linkedin.com/jobs/view/<id>/`, the row's **Canonical URL**): use **Claude in Chrome**, which runs in the user's real, already-signed-in Chrome (load its tools via ToolSearch first if deferred). Navigate to the URL, then `get_page_text`. The JD body often loads asynchronously or sits behind a "see more" expansion; wait ~2s and retry once. If it's still not there, the listing genuinely has no JD on LinkedIn (common on "Promoted by hirer / Responses managed off LinkedIn" postings). Don't loop.
- **Other blocked sites** (the domains listed in the row's Score Breakdown as tried by job-lead-tier2-scoring: 403, JS-rendered, or needs a login): use the **built-in browser**. It will likely need one-time site access. Call `request_access` for that site (scope "site" is fine so it doesn't ask again, or "once" if the user would rather approve each time) and retry. If the user declines or doesn't respond to an access prompt, don't push; note that the site couldn't be accessed and move to the next row.
- Start from what job-lead-tier2-scoring already tried before searching fresh. There's no need to redo its web search unless those leads are dead ends too.

## 3. Scoring
Load the `job-fit-rubric` skill and follow it, exactly as `job-lead-tier2-scoring` does: build the `tier2` evidence table from the JD you read, run its `score.py`, and use the returned `score` unchanged as the Fit Score. Jobs needing a move the user won't make are capped at 3. Write the 3 biggest gaps into the Gaps cell in the format defined in `job-fit-rubric`.

## 4. Updating the row
Write each row with the Sheets connector, re-finding it by ID just before writing (`job-tracker` **Writing**). Update it in place; never duplicate.
- **A usable JD was found:** first save it as `<ID>_JD.md` in the job's folder, then create the first fit report, `<ID>_fit_r1_<date>.md` (formats in `job-tracker` **Job files in Drive**). Saving the JD means later rescores run in the cloud through job-lead-tier2-scoring, with no browser. Then write Fit Score, Gaps, **Fit Report** (link to the new report), **Score Tier** `T2-manual`, **Score Breakdown** `JD: <full JD URL, or "LinkedIn direct"> (browser) | <breakdown from score.py>`. Fill Pay Range and Type / Location if they're blank and the JD states them.
- **No JD anywhere reachable** (LinkedIn confirmed empty and no other source exists): leave the score as it is, set **Score Tier** `T2-no-jd`, and note it: `Manual lookup <date>: LinkedIn shows no JD body, no other source | <previous breakdown>`. The row then isn't picked up again.
- **The posting is closed or filled:** set **Score Tier** `T2-closed` with `Posting closed per <site> <date> | <previous breakdown>`. Don't set Status.
- **Couldn't access the site** (the user declined access, or the browser wasn't reachable): leave the row as `T2-pending-manual` and unchanged, and list it in the summary.

For every row you changed, set **Tier 2 Date** and **Last Updated** to today, and write `false` to **Run Tier 2** if it's ticked.

## 5. End-of-run summary
List which rows were upgraded with old → new scores, which were marked `T2-no-jd` or `T2-closed`, which still couldn't be reached (and why), and how many `T2-pending-manual` rows are left.

## Known constraints
- Requires the user's computer on and reachable: Chrome running with the extension for LinkedIn rows, and/or the desktop app's built-in browser for other blocked sites. If neither is reachable, say so plainly and stop rather than silently falling back to WebFetch (which is exactly what already failed upstream in job-lead-tier2-scoring).
- Never run this on a schedule. It depends on live interactive access (a browser session, and possibly a site-access approval) that nobody is present to grant unattended.
- Never send email, reply to a lead, or click apply.
- Never edit, replace or trash a JD file or fit report.
- Never change Status, and never write Next Action / Notes.
