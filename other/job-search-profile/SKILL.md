---
name: "job-search-profile"
description: "On demand: sets up or updates the user's job-search profile, job-search-profile.md in their Google Drive. It holds their name, full-resume file, tracker sheet and folder, target roles, location and relocation rules, job sources (job-alert email senders and company career sites), housekeeping settings, and the look of their tailored resumes (resume-style.md, converted once from a Word template they attach). Use it the first time someone sets up the job-search plugin ('set up my job search'), and whenever they change something in chat ('add a job alert sender', 'search for openings at Acme', 'watch https://careers.example.com/jobs', 'I'd relocate to Austin now', 'my tracker moved', 'set up my resume style', 'make my resume headings navy'). Interviews the user for anything missing, checks the Gmail connector, and finds and tests career sites. The other job-search skills read the profile; they never write it."
---

# Job Search Profile

Every job-search skill in this plugin works from one file: **`job-search-profile.md`** in the user's Google Drive. It plays the part a CLAUDE.md plays for a codebase: plain Markdown that this skill writes and keeps current, and that the user can also edit by hand. Nothing about a particular user is written into the skills themselves; it all comes from here.

This skill creates the profile by interviewing the user, and updates it whenever they tell Claude something changed.

## Key files and systems
- **The profile:** a plain-text Markdown file named exactly `job-search-profile.md`, stored in the user's job-search folder. It's found by name (`search_files` with `title = 'job-search-profile.md'`), so its location never has to be configured. Drive search can't filter out trashed files, so this skill never leaves a trashed file with that name (see step 4).
- **Google Drive connector** to find, read, create, rename and trash files. Read the profile with `download_file_content` and base64-decode it: `read_file_content` can return an empty result for a Markdown file created in the last few minutes. **Google Sheets connector** to check the tracker. **Gmail connector** to confirm email senders. **Web search and web fetch** to find and test career sites.
- **`job-tracker` skill:** load it for the tracker's tab and column layout when checking or creating a tracker.
- **The resume style:** `resume-style.md` in the same folder, the look of the user's tailored resumes (step 7). Its format is `resume-style-format.md` in the `tailored-resume-builder` skill's folder, which sits next to this skill's folder. That folder also holds `extract_style.py` (drafts a style file from a Word template), `render_resume.py` (builds a resume from a style file, used here for previews) and `default-style.md`.

## The profile format
Keep this exact structure. Each setting is a `- Key: value` line under its section, so both people and skills can read it; add a short comment in parentheses after a value when it helps. Leave a value blank rather than inventing one.

~~~
# Job search profile

Maintained by the job-search-profile skill. You can edit it by hand: keep the
section headings and the "- Key: value" lines, and change the values.

Last updated: <YYYY-MM-DD>

## Candidate
- Name: <full name, as it should appear on file names>
- Full resume: <file name of the full career history in the job-search folder, e.g. Full-Resume.md>
- Resume style: <resume-style.md, or "default" for the plugin's default look>
- Tailored resume prefix: <file-name prefix for tailored resumes, e.g. Jane_Example_Resume>

## Tracker
- Sheet name: <Google Sheet name, e.g. Job_Search_Tracker>
- Folder: <Drive folder path, e.g. My Drive/Job Search>
- Folder ID: <filled in by this skill>
- Sheet ID: <filled in by this skill>
- Time zone: <IANA time zone used for dates, e.g. America/Denver>
- Local Drive folder: <optional: where this folder appears on the user's computer, if Google Drive for desktop syncs it>

## Target roles
- Role families: <comma-separated, e.g. enterprise architecture, technical program management>
- Seniority: <e.g. senior, lead, principal, manager>
- Adjacent roles: <roles that count as a partial title match>
- Never interested: <roles or industries to discard at Tier 1>

## Location
- Home area: <metro area and state or country>
- Home ZIP: <postal code the commute is measured from; optional>
- Max commute (miles): <one-way distance the user will travel to an office, e.g. 35>
- Commutable to: <optional: cities or areas to treat as commutable regardless of distance>
- Remote: <yes / no>
- Relocation: <no / yes / only to: <places>>

## Email sources
| Source | Sender | Notes |
|---|---|---|
| <label written to the Source column> | <sender address> | <how to read these emails: one job or a digest, how reliable, link quirks> |

## Career sites
| Source | Company | URL | Method | Notes |
|---|---|---|---|---|
| <label written to the Source column, e.g. Careers: Acme> | <company name> | <listing page, feed or site: scope> | <page / feed / search> | <the ATS if known, the human careers page for a feed, filters in the URL, quirks> |

## Never scan
- <sender addresses that look like job mail but aren't postings>

## Housekeeping
- Archive after days: <30>
- Tier 2 rows per run: <10>
- Career site leads per run: <15>
~~~

Email sources and Career sites are both optional, but intake needs at least one source to scan. A profile written before Career sites existed simply has no such section; skills treat a missing section as empty.

## 1. Find the profile
Search Drive for `title = 'job-search-profile.md'`.
- **One found:** read it (`download_file_content`, decoded) and go to step 3.
- **None found:** if a `job-search-profile.previous.md` exists, an earlier update stopped partway: tell the user, read that file as the current profile, and finish the update from step 4. Otherwise this is a new setup: go to step 2.
- **More than one:** stop and list them with their folders and modified dates (one may be a copy the user trashed by hand). Ask which one is current; never pick one yourself.

## 2. Interview a new user
Ask one section at a time, in the order of the format above, and confirm each section before moving on. Offer an example for every question, and accept "skip" for anything optional (Adjacent roles, Never interested, Never scan, Notes).
- **Candidate:** the name, then the full-resume file. If they don't have a Markdown full resume yet, explain it's one file with their whole career history (every role, project, certification and tool, not a two-page selection), that every score is judged against it, and that the more complete it is the fewer false gaps they'll see. Suggest a name such as `Full-Resume.md`. Derive the tailored resume prefix from the name (`Jane_Example_Resume`) and show it. Then set up the resume style (step 7).
- **Tracker:** ask for the Google Sheet's name and the Drive folder it's in (or should go in). For now the tracker is always a Google Sheet. Then follow step 5. Ask whether they use Google Drive for desktop on this computer; if so, ask where this folder appears on disk (for example `C:\Users\<name>\Google Drive\My Drive\Job Search`, or a folder they chose). If this session can see the computer's files, check the path exists and holds the profile or tracker folder's files before writing it as **Local Drive folder**. Skills use it only when they run on that computer, to read and write job files directly instead of through the Drive connector.
- **Target roles and Location:** ask in plain language ("What kinds of roles are you looking for, and at what level?", "Where do you live?", "What's your ZIP code?", "How many miles, one way, would you commute to an office?", "Would you relocate? If so, where?") and turn the answers into the profile's lines. Read them back.
- **Job sources:** follow step 6. It covers Email sources, Career sites and Never scan.
- **Housekeeping:** offer the defaults (archive after 30 days, 10 Tier 2 rows per run, 15 career-site leads per site per run) and change them only if asked.

Then show the whole profile and ask the user to confirm before writing it (step 4).

## 3. Update an existing profile
When the user tells you something changed (in this conversation or in a request that loaded this skill), change only the lines it affects, and keep everything else exactly as it is, including the user's own wording and comments. If a request is ambiguous ("add Indeed"), ask the one question needed ("Which sender address do Indeed alerts come from?"). Show the changed lines as before → after and confirm, then write the file (step 4).

A request about the look of tailored resumes ("set up my resume style", "make the headings navy", "use Garamond", "use this template instead") follows step 7.

A request that adds a job source ("add Indeed alerts", "search for openings at Acme", "watch https://careers.example.com/jobs") follows step 6 for that one source. "Stop watching Acme" removes its Career sites row; show it before → after like any other change.

Also use this step for a review: if asked "show my job search profile", read it back section by section and point out anything blank or inconsistent (for example Relocation "only to" with no places).

## 4. Write the profile
The Drive connector can create, rename and trash files but can't change a file's contents, so an update replaces the file:
1. If a profile exists, rename it to `job-search-profile.previous.md` with `update_file` (`title`).
2. Create the new `job-search-profile.md` with `create_file`: `parentId` the tracker's folder ID, `contentMimeType` `text/markdown`, `disableConversionToGoogleType` true, the full text in `textContent`, and **Last updated** set to today.
3. Read it back with `download_file_content`, decode it, and check that it matches what you meant to write.
4. Rename the previous copy to `job-search-profile.replaced-<YYYYMMDD-HHMM>.md`, then trash it with `trash_file`. Renaming first means no trashed file ever carries a name this skill searches for. Drive keeps trashed files for 30 days, so the user can still recover it.

If step 2 or 3 fails, rename the previous copy back to `job-search-profile.md` and report the failure.

`resume-style.md` is written the same way, with its own names (`resume-style.previous.md`, `resume-style.replaced-<YYYYMMDD-HHMM>.md`) and `contentMimeType` `text/markdown`.

## 5. Check the tracker
1. Find the folder: search for the folder name (`mimeType = 'application/vnd.google-apps.folder'`), following the path the user gave from the top. If there's more than one match, ask which. Record its **Folder ID**.
2. Find the sheet in that folder: `title = '<Sheet name>' and mimeType = 'application/vnd.google-apps.spreadsheet' and parentId = '<Folder ID>'`. Record its **Sheet ID**.
3. If it exists, open it with the Sheets connector and check it has a **Job Log** tab with the headers `job-tracker` lists. Report any missing headers. Don't add them without asking.
4. If the folder or sheet doesn't exist, tell the user and ask whether to create it. Create only with an explicit yes. Then create the folder if needed (`create_file`, `mimeType` folder), and create the sheet in it (`create_file`, `mimeType` `application/vnd.google-apps.spreadsheet`, `parentId` the folder). Rename its first tab to **Job Log**, and write the headers in the order `job-tracker` lists them. Add the Status dropdown and the two checkbox columns' validation, freeze row 1, and add a **Status Guide** tab with each status, what it means and a `COUNTIF` count of rows in that status.

## 6. Job sources
Ask first: "Where do you want to find openings: job-alert emails, specific companies' career sites, or both?" Set up each kind the user picks. They can add more any time later.

### Email
1. **Check for a mail connector.** Email is read through the Gmail connector: see whether its tools (`search_threads`, `get_thread`) are available in this session.
   - **Gmail is available:** go on to 2.
   - **Another mail connector but not Gmail** (for example Outlook): say that email scanning supports Gmail only for now. Offer career sites instead, or adding the Gmail connector if the alerts also reach a Gmail account.
   - **No mail connector:** explain that intake reads job-alert email through the Gmail connector, and how to add it: in Claude, **Customize → Connectors → Gmail**, then connect the Google account the alerts arrive in. Offer to carry on with the rest of setup and come back later with "add my email sources". Leave Email sources empty until a sender can be confirmed; never write a sender you couldn't check.
2. **Ask which job-alert emails they get** (LinkedIn job alerts, recruiter mail, job boards, a company's own alerts). For each, find a recent example in Gmail, confirm the sender address with the user, and write a one-line note on how to read it (one job per email or a digest of several, any link quirks). If no example turns up, say so and ask whether to add the sender anyway.
3. **Never scan:** if they use LinkedIn alerts, suggest adding LinkedIn's non-posting senders (`messages-noreply@`, `notifications-noreply@`, `groups-noreply@`, `updates-noreply@`, `editors-noreply@linkedin.com`).

### Career sites
For each company the user names, or careers URL they give ("search for openings on https://careers.example.com/jobs", "search for openings at Acme"):
1. **Find the listing page.**
   - **A URL:** use it as given.
   - **A company name:** search the web for its official careers page (`<company> careers jobs`). Prefer the company's own domain or the applicant-tracking board its careers page links to (Greenhouse, Lever, Workday, iCIMS, Ashby, SmartRecruiters and the like). Never use a job aggregator or a LinkedIn page. Company names collide, so show the URL you found and ask the user to confirm it's the right company. If results disagree, show the candidates and let the user choose.
2. **Test how it can be read from the cloud.** Intake runs on a schedule with no browser, so try these in order and record the first that works as **Method**:
   - **`feed`:** the board is on an applicant-tracking system with a public job feed that a plain GET returns: Greenhouse `https://boards-api.greenhouse.io/v1/boards/<board>/jobs`, Lever `https://api.lever.co/v0/postings/<company>?mode=json`, Ashby `https://api.ashbyhq.com/posting-api/job-board/<board>`, SmartRecruiters `https://api.smartrecruiters.com/v1/companies/<company>/postings`. Fetch it and check it lists postings. Put the feed URL in **URL** and the human careers page in **Notes**.
   - **`page`:** fetch the listing page and check that it shows real job titles with links to postings, not just a search box or an empty shell built by JavaScript. If the site puts its search in the URL (for example `?q=architect&location=Columbus`), build that URL from Target roles and Location, test it again, and record it.
   - **`search`:** neither works, which is common on JavaScript-only boards such as many Workday sites. Run a web search `site:<careers host and path> <a role keyword>` and check that some results are posting pages on that host. Record the scope as **URL** (`site:acme.example-ats.com/careers`); intake adds role keywords from Target roles. Note in **Notes** that results depend on the search index and can lag the site by days.
   - **None works:** say that this site can't be read without a browser. Suggest the company's own job-alert email sign-up, which many career sites offer; once alerts arrive, add the sender as an email source. Don't add the row.
3. **Write the row:** Source `Careers: <Company>`, Company, URL, Method and Notes. Show it before → after, confirm, and write it (step 4).

Then ask whether there are more companies to watch.

## 7. Resume style
Tailored resumes take their look from `resume-style.md`, a short text file of fonts, sizes, colours, margins and layout, so no Word file ever has to pass through the Drive connector. It's made once, from a Word template the user already likes, or the user takes the plugin's default.

1. **Ask:** "Do you have a Word resume template whose look you want your tailored resumes to have? Attach the .docx here, or say no to use the plugin's default style."
2. **Get the .docx as a real file.**
   - **Attached to this conversation:** use the attached file.
   - **On the user's computer, with a Local Drive folder:** read it from disk if they name it there.
   - **Never download a .docx through the Drive connector.** It arrives as base64 that has to be copied by hand, which corrupts files. Ask them to attach it instead.
3. **Convert:** `python3 <tailored-resume-builder folder>/extract_style.py <template.docx> --out <scratch>/resume-style.md`. It prints a report of what it guessed, how, and with what confidence, and what it can't carry over. On exit 2, say the file couldn't be read as a Word resume and offer the default style.
4. **Preview with the user's own content.** Make a small `content.json` from the full resume only:
   - the name and contact line;
   - a headline from their current title;
   - two or three sentences of summary;
   - six competencies and two highlights;
   - the two most recent roles, with up to three bullets each.

   Never invent anything for a preview. Run `render_resume.py --style <scratch>/resume-style.md --content content.json --out preview.docx --pdf`. If a PDF came out, turn its first page into an image (`pdftoppm -png -r 80 -f 1 -l 1 preview.pdf preview`) and show it. Otherwise give the .docx as a download, and say the preview couldn't be rendered here.
5. **Check with the user.**
   - List the low-confidence guesses from the report, and ask about each.
   - List everything under "Not carried over" (pictures, text boxes, columns, header or footer content, uncommon fonts), so nothing is lost silently.
   - Ask whether the preview looks right.
   - Apply their changes ("make the headings navy", "dates after the title") by editing the style file's lines in the documented format, and re-render.
6. **Save** `resume-style.md` to the tracker folder (step 4) only after they confirm, and set **Candidate → Resume style** to `resume-style.md`.
7. **No template:** set Resume style to `default`, and show a preview of `default-style.md` with their content. If they want to adjust the default, copy it to their own `resume-style.md`, then edit and save it as above.

**Later changes:**
- "make the section headings navy", "use Garamond", "put the dates after the title": change only those lines of their `resume-style.md`, show before → after, preview, and save.
- "use this template instead", with an attachment: convert again from item 3 above.
- The original .docx isn't needed after conversion. Don't upload, copy or keep it.

A profile written before this step has **Resume template: <file>.docx** instead of Resume style. Offer to convert that template once (asking the user to attach it), and replace the line with **Resume style** when the style file is saved.

## 8. End-of-run summary
- Whether the profile was created, updated or only reviewed, and where it is.
- The lines that changed, before → after.
- For each career site added, the Method found and what the test returned (for example "page: 12 postings listed").
- Anything still blank that other skills will need. For example, intake has nothing to scan without at least one email source or career site, and scoring needs Target roles and Location.
- If email was skipped because the Gmail connector isn't connected, how to add it.
- If the resume style was set up or changed: the style used (converted from which template, or the default), what wasn't carried over, and that tailored resumes will use it from now on.
- For a new setup, what to do next: put the full resume in the folder, then schedule the daily intake task (and Tier 2 and weekly cleanup) in the Claude app.

## Known constraints
- The only files this skill writes are `job-search-profile.md` and `resume-style.md`, plus a tracker or folder the user explicitly asked it to create.
- Never moves a Word file through the Drive connector, and never uploads or keeps the user's template; it's converted once and set aside.
- Never invents profile values. If the user hasn't said it, it stays blank and is listed in the summary. A career site's URL is written only after the user confirms it.
- Testing a career site only reads it. Never sign in, apply, create an account, or sign up for job alerts on the user's behalf.
- Never deletes a profile outright; an update trashes the previous copy only after the new one is written and checked.
- Never changes the user's other files: not the full resume, not the tracker's rows, not job files.
- The profile holds personal details. It stays in the user's Drive and is never copied into a repository, an issue or a public page.
