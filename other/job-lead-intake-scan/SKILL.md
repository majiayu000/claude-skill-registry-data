---
name: "job-lead-intake-scan"
description: "Scan the user's job sources from their job-search profile for new job leads: job-alert email in Gmail (job alerts, recruiters, job boards) and the company career sites they watch. Screen leads against their target roles and location, and log new candidates to their job tracker with a canonical link and a Tier 1 score. Cloud-only: runs on a daily schedule, no computer or browser needed."
---

# Job Lead Intake Scan

Finds new job leads in the user's inbox and on the company career sites they watch, does a first-pass fit screen, and logs them to their job tracker. This is the intake stage of the pipeline: this skill only ever writes new rows with status "Need to review". It never changes an existing row's status, never emails anyone, never generates a resume, and never opens a LinkedIn job page. The user then ticks **Run Tier 2** on the rows worth a closer look; `job-lead-tier2-scoring` (cloud, web search, scheduled) scores those against the real JD, and anything it can't reach goes to `job-lead-manual-jd-lookup` (the user's own browser, on demand).

Runs daily on a schedule, entirely through the Gmail, Google Drive and Google Sheets connectors plus web search and web fetch for career sites. It must work when the user's computer is off, so never reach for a device or browser tool here.

## Key files and systems
- **Profile and tracker:** load the `job-tracker` skill with the Skill tool before anything else. It explains how to find and read the user's **job-search profile** and their tracker, the columns this skill owns, how to add rows, dedup, and the job files in Drive. Follow it exactly. This skill uses the profile's **Email sources**, **Career sites**, **Never scan**, **Housekeeping → Career site leads per run**, **Target roles**, **Location**, **Candidate → Full resume** and **Tracker → Time zone**.
- **Scoring:** load the `job-fit-rubric` skill before setting any Fit Score. It holds the evidence-table format and `score.py`.
- **The full resume** (found as `job-tracker` describes) is the only evidence used for scoring. It holds all of the user's experience, not a two-page selection, so score against the whole file. Read-only for these skills; the user edits it. If it isn't found, stop and report that.

## 1. Choose the email search window
This window applies to email only. Career sites (step 3) are read as they are now on each run, and dedup skips what's already logged.
- Normally search a trailing 7-day window (`newer_than:7d`), whatever the schedule. If the schedule is ever widened, a fixed 7-day lookback still won't miss anything; it just reprocesses a few emails, which dedup handles.
- **Catch-up after a gap:** read the newest **Email Received** in the tracker (rows from career sites have none). If it's more than 7 days ago (runs failed or were paused), search from that date instead (`after:YYYY/MM/DD`), up to 30 days back. Work through the emails oldest first. If the run can't finish, write the rows found so far; the next run picks up from the new newest Email Received. Say in the summary that this was a catch-up run, with the window.

## 2. Email sources to scan
Search Gmail for each sender in the profile's **Email sources** table (`from:<Sender>`), and use the **Source** label on the rows it produces. Each source's **Notes** say how to read its emails: follow them. Skip anything from a sender listed under **Never scan**.
- If both **Email sources** and **Career sites** are empty (or missing), stop and say so; there's nothing to scan.
- If Email sources is empty but there are career sites, skip this step.
- If the Gmail connector isn't available, still scan career sites (step 3), and say in the summary that email was skipped and the Gmail connector needs connecting.

Formats this skill already knows, for sources whose notes don't say otherwise:
- **LinkedIn job alerts** (`jobalerts-noreply@linkedin.com`): each email is a digest of 2-6 job cards (title, company, location, sometimes a salary band), not one job. Parse every card, not just the one in the subject line.
- **LinkedIn "jobs you may be interested in"** (`jobs-noreply@linkedin.com`): lower-signal digests; include them but screen harder.
- **LinkedIn mail that isn't a posting** (`messages-noreply@`, `notifications-noreply@`, `groups-noreply@`, `updates-noreply@`, `editors-noreply@linkedin.com`): never a lead, even if the profile doesn't list it under Never scan.
- **Job-board digests whose links are click-trackers** (for example MyJobHelper): titles are often truncated (`Senior Projec...`) and the links can't be resolved, so those rows have no Canonical URL and link to the Gmail message. Screen hard; many are generic blasts.
- **Recruiter emails:** usually one role per email, often with a direct company or ATS link.

When the user mentions a new source, the change belongs in their profile (`job-search-profile`), not in this skill.

## 3. Career sites to scan
For each row in the profile's **Career sites** table (skip this step if there are none), read the current listings by its **Method**:
- **`feed`:** fetch the URL and read each posting's title, location and posting URL, and its posted or updated date if given.
- **`page`:** fetch the URL and read the job titles, locations and posting links. If the listing is split into pages, read at most the first 3.
- **`search`:** run one web search per Target roles role family, with the row's `site:` scope (for example `site:acme.example-ats.com/careers "enterprise architect"`). Keep results that are posting pages on that host.

Then:
- Use the row's **Source** label for every lead from it, and its posting URL as the lead's link.
- Screen, score and dedup each listing exactly like an email lead (steps 4 and 5). A listing that already gives the full job description (many feeds do), or a posting page you fetch, is a full-JD read and follows the full-JD rules in step 4.
- **Cap:** add at most **Career site leads per run** new rows per site (15 if the setting is blank). Take the closest matches first. The rest aren't logged yet, so the next run picks them up; say how many were held back.
- **A site that can't be read** (an error, a login page, an empty shell built by JavaScript, no posting links): skip it and report it in the summary as `Careers: <Company> could not be read (<what happened>); say "update my job search profile" to re-test it`. Never fall back to a browser. A site with no matching postings today isn't a failure.

## 4. Screening and scoring (Tier 1, plus opportunistic real fetches)
From the email or listing alone (title, company, location, salary if shown), judge plausible fit against the profile's **Target roles** (Role families, Seniority, Adjacent roles). Discard leads that match **Never interested** or are plainly outside the target roles, without adding them to the tracker. When unsure, err toward including it.

- **LinkedIn and click-tracker leads:** score from the alert content only (Tier 1: title and company, not a real JD read). Never try to open the posting here. LinkedIn blocks WebFetch through robots.txt and needs a signed-in browser this skill doesn't have. Finding the real JD is `job-lead-tier2-scoring`'s job once the user ticks the row.
- **Direct company or ATS links** (Greenhouse, Lever, iCIMS, Workday, company career pages, often from recruiters): these don't need the user's browser, so you may fetch the JD with WebFetch and score those with a full JD read. If the site blocks WebFetch, leave the row at Tier 1; the user can tick it for Tier 2.

**Setting the Fit Score.** Every score comes from the `job-fit-rubric` skill; never estimate one by feel.
- Tier 1 rows: build the evidence table in `tier1` mode (title/seniority and work arrangement from the alert email) and run its `score.py`.
- Full-JD rows: build the `tier2` table from the fetched JD and run `score.py`.
- Work arrangement matters even at Tier 1. It's judged against the profile's **Location**, and `score.py` caps any job needing a move the user won't make at 3. Log those rows anyway (don't discard them) so the user can see them; the low score keeps them out of the way.

## 5. Dedup before writing
Follow **Dedup** in `job-tracker`: run `canonical_url.py` on every accepted lead's posting link, then skip any lead whose canonical URL, or company and title, is already in the tracker (including its Archive tab) or already accepted earlier in this run. The same LinkedIn job often arrives in several digests with different tracking links; the canonical URL is what makes them match. The same job found both in an alert email and on the company's career site has two different URLs, so it's the company-and-title rule that catches it.

## 6. Writing new rows
Add rows as `job-tracker` describes (at the top, newest first, one pass). For each new row write:
- **ID** (the next number, per `job-tracker`), **Date Found** (today), **Source** (the profile's label), **Company**, **Job Title**, **Type / Location**, **Pay Range** (if stated).
- **Email Received**: the Gmail message's date in the profile's time zone, not today. **Gmail Message ID** and **Source Email** (hyperlink to that message) for the email the lead came from. Leave all three blank for a lead from a career site.
- **Canonical URL** from `canonical_url.py` (blank if it returned `""`).
- **Job Description**: `=HYPERLINK("<canonical URL>","View posting")`, or the Gmail message link if there's no canonical URL. For a career-site lead, the posting URL itself if `canonical_url.py` returned `""`. Never the raw LinkedIn email link, which carries a one-time sign-in token.
- **Fit Score**, **Gaps** (format per `job-fit-rubric`), **Score Tier** and **Score Breakdown**:
  - Tier 1: `T1`, `Alert email | <breakdown from score.py>` (`Career site listing | …` for a career-site lead).
  - Full JD fetched: `T2`, `JD: <JD URL> (intake fetch) | <breakdown>`, and **Tier 2 Date** today. Also save the JD as `<ID>_JD.md` and create `<ID>_fit_r1_<date>.md` in the job's folder (formats in `job-tracker` **Job files in Drive**), and write the **Fit Report** link.
- **Run Tier 2** and **Build Resume**: `false`. **Status**: `Need to review`. **Last Updated**: today.
- **Contact / Referrer**, when the source's notes say it's a recruiter: the recruiter's name, written as on earlier rows from that source.
- Leave Next Action / Notes, Tailored Resume, Resume Created, Date Submitted and Submission Email blank.

A JD that arrives as a Gmail attachment (not a link) can't be downloaded here. Score the row at Tier 1 and start its Score Breakdown with `JD is an email attachment; add it to Drive`.

## 7. End-of-run summary
Always end with a short summary, never silence:
- The email search window (and whether it was a catch-up run), or that email was skipped and why.
- New rows per source, including each career site, and any career site that couldn't be read or had leads held back by the cap.
- How many new rows were added, as a one-line list with their Fit Scores, strongest first.
- How many leads were screened out at Tier 1 and roughly why, and how many were skipped as duplicates.
- Anything that couldn't be processed, including any profile setting that was blank.
If nothing new was found, say so explicitly.

## Known constraints
- Never change an existing row's Status, and never write Next Action / Notes. Those are the user's.
- Never tick Run Tier 2; choosing what gets a full JD read is the user's call.
- Never send email, reply to a lead, or click apply. This is a read-only scan. On career sites, never sign in, submit a form, or create an account or job alert.
- Never use a device or browser tool here. That dependency belongs entirely to `job-lead-manual-jd-lookup`.
- Never set a Fit Score that didn't come from `job-fit-rubric`'s `score.py`.
- Never write the profile. Changes to sources, roles or location go through `job-search-profile`.
