---
name: tailor
description: Write a resume, and optionally a cover letter, for one or more queued jobs from the user's profile. Use when the user says /tailor, "tailor my resume for this job", "write a cover letter for", or wants the application to carry a resume written for the posting. Every claim is checked against the profile before the PDF is made.
model: claude-sonnet-5-5
effort: high
---

# /tailor: a resume and a cover letter written for one job

The CLI does the writing. Run from the repo root:

```
npx jev tailor <job id> [<job id> ...] [--cover] [--fresh] [--open]
```

It asks the writer for a one-page resume (and, with `--cover`, a one-page
cover letter) built from the profile and the posting, checks every number
and every capitalized name in the draft against the profile, renders the
PDFs through the runner's own Chrome, and keeps them in
`documents/tailored/<Company>_<Role>_<job id>/`: `resume.pdf`, `resume.md`, `cover.pdf`,
`tailored.json`.

A job id comes from `queue` or `log`. A draft that claims what the profile
does not say is refused with the claims named; fix the profile with
`/profile` if the claim is true, and run again.

## Using the documents in an application

- `apply --tailor` writes the resume for each job and attaches it instead of
  the profile's resume file.
- `apply --cover` also writes a cover letter wherever a form has a box for
  one, and uploads it or pastes it. Without `--cover`, a form that requires a
  cover letter is still skipped, as the profile says.
- `coverLetter: "when_asked"` in `data/profile.json` makes every `apply`
  behave as if `--cover` was given.

## Templates

The PDFs come from the template in use: the stock one, or one the user
registered with `npx jev templates --add <folder> --name <name>` and chose
with `--use <name>`. `npx jev templates` lists them. A template is a folder
with `resume.html` and `cover.html` in the small placeholder language the
README's "Custom resume and cover letter templates" section describes.
Registering runs a test print; a template that fails is not kept.

## What you check before the user sends anything

Open `resume.md` and the cover letter text and read them. The rule is the
project's: nothing about the candidate that the profile does not say. If a
sentence reads as a stretch, tell the user which one and run again with
`--fresh` after the profile is fixed. Never edit the PDF or the JSON by
hand to get a claim in.
