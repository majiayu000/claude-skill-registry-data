---
name: "tailored-resume-builder"
description: "On demand only, never scheduled: when the user says 'build ticked resumes' (tracker rows ticked in Build Resume), names tracker rows, or pastes a job description: picks the most relevant true content from the user's full resume and renders a .docx and PDF of at most 3 pages (or fewer when the user asks) in the user's own resume style (resume-style.md, or the plugin's default), plus a Google Doc of the same resume saved straight to the job's Drive folder. Never invents experience; reports gaps instead. Not for scoring (that's job-fit-rubric), not for editing the master inventory, and not for setting up the resume style (that's job-search-profile)."
---

# Tailored Resume Builder

Turns one job description into one resume of at most 3 pages, or fewer when the user asks for that resume to be shorter ("keep it to 2 pages"), in the user's own look. A 3rd page must be at least half full; otherwise the resume is cut to 2 pages. Shorter is fine: a one- or two-page resume is the right result when the full resume doesn't hold more relevant, true content. It's the last step of the tracker loop: the user ticks Run Tier 2, works through the gaps in the fit report (adding anything true but missing to their full resume and re-ticking to rescore), and when they're done ticks **Build Resume** and asks for "build ticked resumes". The model does the judgment (which true things to show, in what words); `render_resume.py` does the layout from the user's style file, so every resume looks the same and nothing is hand-built. Every build also saves a Google Doc of the resume in the job's Drive folder, so the user has it in Drive whether the build ran in the cloud or on a computer that's since been switched off.

## Key files and systems
- **Profile and tracker:** load the `job-tracker` skill before anything else. It explains how to find the user's job-search profile and tracker, the Build Resume checkbox, the columns this skill writes, and the job files in Drive (`<ID>_JD.md`, the fit reports, the company folder). This skill uses the profile's **Candidate** settings (Full resume, Resume style, Tailored resume prefix) and **Tracker → Local Drive folder**.
- **Content source** (the only source of facts): the full resume named in the profile, found as `job-tracker` describes. It's read-only here; the user edits it. If it isn't found, stop and say so.
- **Look:** the style file named in **Candidate → Resume style**, usually `resume-style.md` in the tracker folder. It's small text, so read it with the Drive connector like any other Markdown file. `default` (or a blank setting) means `default-style.md` in this skill's folder. The format is in `resume-style-format.md` here. If the profile still names a **Resume template** (.docx) instead, use the default style for now, and tell the user to say "set up my resume style" to convert their template. **Never download a .docx through the Drive connector.** It arrives as base64 that has to be copied by hand, which corrupts files.
- **`render_resume.py`** (this folder): `python3 render_resume.py --style <style.md> --content content.json --out <file>.docx --pdf --max-pages <N> --html <file>.html`. `--html` also writes the resume as HTML that Google Drive converts into a Google Doc. It needs `python-docx`; page counting and the PDF need LibreOffice (`soffice`), and `pdfinfo` and `pdftotext` (poppler). It prints JSON with `pages`, `max_pages`, `last_page_fill` (how far down the last page the text reaches, 0-1) and `warnings`, and exits 2 with a reason if the style file, `content.json` or `--max-pages` is invalid.
- **`check_content.py`** (this folder): `python3 check_content.py --inventory <full resume>.md --content content.json`. Checks `content.json` against the full resume: employers, titles and dates match it, every role that ended in the last 15 years is there, no company descriptions, and every role has a line. Prints JSON with `ok`, `errors`, `warnings` and `omitted_old_roles`, and exits 1 when there are errors.
- **`check_doc_text.py`** (this folder): `python3 check_doc_text.py --content content.json --doc <read-back>.md`. Checks that the Google Doc, read back as text, holds every line of `content.json`. Prints JSON with `ok` and `missing`, and exits 1 when lines are missing.
- **Also here:** `extract_style.py`, which `job-search-profile` uses to convert a Word template into a style file. This skill doesn't call it.
- **Evals:** the `resume-*` cases in this plugin's `evals/` folder.

## Procedure
1. **Pick the jobs, their page limit, and each job description.**
   - **"Build ticked resumes":** every tracker row with **Build Resume** ticked, lowest ID first. **Named rows:** exactly those. Build the first 3, then check in before doing more.
   - **Page limit:** 3 pages, unless the user asks for fewer for this resume ("max 2 pages", "keep it to one page"); a limit given with "build ticked resumes" applies to every row in that run. More than 3 is never allowed: if asked, say 3 is the most and use 3.
   - For a tracker row, the JD is the saved `<ID>_JD.md` (`search_files` with `title = '<ID>_JD.md'`). If there isn't one, skip the row, leave it ticked, and report "run Tier 2 first". Don't search for the JD here.
   - **Pasted or attached JD** with no tracker row: use it as given.
   - If there is no usable JD, stop and ask. Never tailor to a job title alone.
2. **Read the full resume and the style file** (see Key files). Save the style text to a scratch file for `render_resume.py`.
3. **Map the job to the inventory.** Load `job-fit-rubric` and build its evidence table: each JD requirement quoted, marked required or preferred, and matched strong, partial or none to a pointer in the full resume. For a tracker row, start from the evidence table in its latest fit report (`title contains '<ID>_fit_r'`, highest run). Keep its requirement list, and check each match against the current full resume, since the user may have edited it since. Use the table as the selection guide: strong matches get the most room, and `none` matches are gaps.
4. **Write `content.json`** (shape below) using only what the inventory supports:
   - Keep every employer, title, location and date exactly as in the inventory. Never change dates, titles, numbers, team sizes, technologies or outcomes.
   - Reword for the JD's vocabulary only when the inventory already says the same thing (e.g. "ATO process" if the inventory says Authority to Operate). Never add a skill, tool, credential, metric or responsibility the inventory doesn't contain, even if the JD asks for it.
   - Headline: a short line matching the target role, built from titles and strengths the user really has. The style decides its capitalisation.
   - Competencies: at most 12, only ones the inventory evidences, ordered by JD relevance.
   - Career highlights: 3 to 5, the strongest matches to the JD's required items.
   - Experience, newest first:
     - Every role that ended within the last 15 years stays. A role that ended more than 15 years ago may be left out, but only when nothing in it is directly relevant to the JD; if it is relevant, keep it.
     - Every role shown has at least one line under it: its summary or a bullet, from the inventory. Never show a bare title.
     - Give the most bullets to the roles that best match the JD, and trim older or less relevant roles to 1-3 lines. Drop a role's summary before dropping a strong bullet, but never take a role below one line.
   - No company descriptions. Each employer gets its name, location and dates only, even when the inventory has a line describing the company. Leave out `description` in `content.json`; `render_resume.py` rejects it.
   - Education and certifications: include as in the inventory. Certification credential IDs are optional; leave them out to save space.
5. **Build:** run `render_resume.py` with `--pdf`, `--max-pages` set to the page limit, and `--html`. Act on every warning before delivering. When trimming, cut in this order: roles that ended more than 15 years ago and aren't relevant to the JD, then the least relevant bullets, then long summaries. Never take a role below one line, and never drop a role that ended in the last 15 years.
   - **Over the limit:** trim, then rebuild until it fits.
   - **Page 3 under half full** (the warning says "trim to 2 pages"): trim to 2 pages and rebuild. Never pad page 3 to reach half. If it can't fit 2 pages without breaking the rules in step 4, stop and say so instead of delivering.
   - **Under the limit:** fine. Use the room for relevant bullets the inventory really has, and never pad with filler to reach a length.
   - **`pages` is null** (LibreOffice isn't available, so the page count can't be checked): keep the content within the limits above, and say in the summary that the page count is unverified. If `last_page_fill` is null on a 3-page build, trim to 2 pages to be safe and say the fill couldn't be checked.
   - **Look at the PDF** (convert its pages to images) to check nothing is broken: dates line up at the right margin, and there's no stray blank page.
6. **Check the content.** Save the full resume's text to a scratch file and run `check_content.py` on it and `content.json`. Fix every error and rebuild until `ok` is true. Note each role in `omitted_old_roles` for the summary. If it warns that the work history isn't in `### Employer | dates` and `#### Title | dates` headings, do those checks by hand. Then, for every bullet, headline, highlight and competency in the output, confirm it traces to a line in the full resume. Fix or remove anything that doesn't. Do not skip this even when running unattended.
7. **Deliver.** Every build produces three files with one name, `<Tailored resume prefix>_<Company>_<Role>`, using the prefix from the profile (e.g. `Jane_Example_Resume_Acme_Corp_Program_Manager`): a Google Doc, a `.docx` and a `.pdf`. If a resume with that name already exists for the job, in any of the three forms, add `_v2`, `_v3` and so on to all three; never overwrite an earlier one. They belong in the job's company folder, `<tracker folder>/<Company_Folder>/` (naming rule in `job-tracker`); find it, or create it with the connector, before saving the first file.

   **The Google Doc, on every run** (cloud or computer):
   1. `create_file` with the name as `title`, `parentId` the company folder's ID, `contentMimeType` `text/html`, and `textContent` the full text of the `.html` file exactly as `render_resume.py` wrote it. Leave conversion on (don't set `disableConversionToGoogleType`), so Drive turns it into a Google Doc. It's text, so it goes through the connector safely; never send it as `base64Content`.
   2. Read it back with `read_file_content` (`includeComments` true), save the returned text to a scratch file, and run `check_doc_text.py` on it and `content.json`. If lines are missing, the HTML changed on its way to Drive: rename that Doc to `<name>_check_failed` and create it once more from the file. If the second one fails too, keep it, list the missing lines, and point the user to the .docx. If the Doc can't be read back, say it wasn't verified.
   3. Google lays out the Doc itself, so it can break pages a little differently from the PDF, and a long date range can wrap. The .docx and PDF are the page-checked versions; say so if the user asks which to send.

   **The .docx and PDF.** **Never upload a .docx or PDF through the Drive connector.** A binary upload has to be copied by hand as base64, which corrupts files. Deliver them one of these ways:
   - **On the user's computer, with a Local Drive folder** (the profile's **Tracker → Local Drive folder** exists on this machine): write the .docx and PDF straight into `<Local Drive folder>/<Company_Folder>/`, creating the folder if needed. Google Drive for desktop syncs them next to the Google Doc.
   - **Otherwise (the cloud, or no Local Drive folder):** hand the .docx and PDF to the user as downloads (in the Claude app, send the files; elsewhere, give their paths). Say that they go in the same folder as the Google Doc.

   Text files still go through the connector. For a pasted JD only, save `<Tailored resume prefix>_<Company>_<Role>_JD.txt` with the job description in the company folder (`create_file` with `textContent`), so it's there if an interview follows. Tracker rows already have `<ID>_JD.md`.

   **For a tracker row:**
   - Write **Tailored Resume**: `=HYPERLINK("<the Google Doc's viewUrl>","<its name>")`. If the Doc couldn't be created, link the PDF instead once it's in Drive (look it up by title with `search_files`, trying for about a minute while it syncs), or write its file name followed by `(syncing to Drive)` or `(download; add to <Company_Folder>/)`.
   - Write **Resume Created** and **Last Updated** (today), then untick **Build Resume** as the last write (`job-tracker` has the rules).
   - If the build failed, is over its page limit, or has a 3rd page under half full, leave the box ticked and say why.
   - If there's no PDF because the page count couldn't be checked, deliver the .docx, refer to it in the row, and say so.
   - Never touch Status or Next Action / Notes.

   **At the start of a run,** replace any `(syncing to Drive)` cell from an earlier run with a link, if the file can now be found.
8. **Tell the user the gaps.** End with the required JD items the inventory has no evidence for. They can then decide whether the inventory is missing something true (and add it to their full resume) or it's a real gap.

## content.json shape
```json
{
  "name": "JANE EXAMPLE",
  "contact": ["phone", "city, state", "email", "linkedin url"],
  "headline": "ROLE-ALIGNED HEADLINE",
  "summary": "2-4 sentences, all true to the inventory",
  "competencies": ["up to 12 short phrases"],
  "highlights": ["3-5 one-sentence achievements"],
  "experience": [
    {"company": "...", "location": "...", "dates": "...",
     "roles": [{"title": "...", "location": "...", "dates": "...", "summary": "optional", "bullets": ["optional if there's a summary"]}]}
  ],
  "education": [{"degree": "...", "school": "..."}],
  "certifications": [{"name": "...", "detail": "issuer, year"}],
  "additional": ["optional lines"]
}
```
Take contact details from the inventory's contact line, not from memory. Give each role its own location and dates as the inventory has them; the renderer shows them only where they differ from the employer's, so a single-role employer's dates appear once. Every role needs a `summary` or at least one bullet.

## Known constraints
- Never invents or inflates anything; gaps are reported, not filled.
- Never edits the full resume, the style file, or any earlier tailored resume. Style changes go through `job-search-profile`.
- Never moves a .docx or PDF through the Drive connector, in either direction. The Google Doc goes through it as HTML text, never as base64.
- Never commits the style file, the inventory, a generated resume or a JD to the repo (it's a public repo).
- Never sends a resume or applies to a job; the user does that.
- Never runs on a schedule. Building a resume is always the user's explicit request.
- Never shows a company description, and never lists a role without at least one line under it.
- At most 3 pages, or the user's lower limit; a 3rd page is at least half full.
- If the inventory can't be found, the style file is invalid, or the output can't be brought within its page limit, say so rather than delivering something off-format.

## End-of-run summary
- Job and files produced: the Google Doc (linked, and whether `check_doc_text.py` passed), the .docx and PDF and where they went (written to the synced folder, or handed over as downloads), page count against its limit (3 by default, or the user's), and which tracker rows were unticked.
- The style used (the user's `resume-style.md`, or the default) and, if the profile still names a Word template, how to convert it.
- Ticked rows skipped, and why (no saved JD, build failed).
- What was emphasized and what was trimmed.
- Older roles left out: each one from `omitted_old_roles`, ended more than 15 years ago and not relevant to the JD.
- Gaps: required JD items with no support in the inventory.
- Anything you couldn't verify, such as the page count.
