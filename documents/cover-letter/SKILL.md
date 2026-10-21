---
name: cover-letter
description: Write and render a cover letter for one posting.
disable-model-invocation: true
---

# /cover-letter

Files: `templates/`, `scripts/`, `docs/`, `examples/` and `routines/` are in the method root, `${CLAUDE_PLUGIN_ROOT}` (the clone holding this skill when that is not replaced by a path); every other relative path is in the workspace, the current folder. Before acting on the person's behalf, read `profile.md`, `docs/rules.md` and the workspace `rules.md`; the workspace one wins on conflict.

Input: a posting URL or pasted posting text, plus optionally the CV version to base it on. Output: `cover-letters/<company>-<role>.md` and its PDF, rendered by `scripts/render.mjs`. The markdown contract is `templates/cover-letter.md`: frontmatter with sender, recipient, place, date, subject, greeting and signoff, then plain paragraphs.

## Gather

1. Read the CV version `profile.md` names for this market. When it fails the approval check in `/cv` ("Approval"), stop and tell the person to approve it through `/cv`.
2. Read the posting. Pull out: the exact role title, the team or product, the three things they ask for most, one sentence worth quoting back, the city or remote setup, the company's legal name and address if shown, the hiring contact's name if shown.
3. If the posting is in the tracker, read the JobCubby application for anything already said to this company (salary figure, earlier contact).

## Write

Three paragraphs, each with one job, two or three sentences each. Keep the whole letter under 300 words, in the language of the posting. Two structures; pick by what the person knows about the company.

**Default structure**:

1. **Who I am and what I want to take care of.** Name, role and years from the profile (the main stack first, in the profile's order), then what in their product I would take care of, in their vocabulary.
2. **Why we are a match, with evidence.** Two results from the CV with numbers, chosen to mirror what they ask for, and how I work (what I put emphasis on).
3. **Their words and the next step.** "You write that ..." with one line from the posting and that it attracted me; where I would join (their city or remote, as the posting says) and when I can start; how to reach me and thank you.

**Problem-first structure**, when there was a call with the hiring manager or an `/outreach` conversation (their words are in the JobCubby description):

1. **I know your problem.** Refer to the conversation and name the challenge in their exact words.
2. **I have solved it before.** The one result from my career that proves it, with a number, then one more. What I bring to the table, not what I like about myself.
3. **Let's talk.** I would like to discuss this in person, thank you, how to reach me.

Then: greeting to the named person ("Dear First Last") or the team, signoff from the frontmatter.

**Email application**, for postings that only accept applications by mail: a plain mail, not a rendered letter. Subject: "Application as <exact title>". Body: greeting to the named person or "<Company> Team"; one line of who I am (title and years from the profile, stack in the profile's order) and that I am applying for <title> found on <source>; one or two sentences of proof matching their asks; that the CV is attached; thank you and that I look forward to discussing how I can contribute. Attach the CV version for the market as PDF. It goes out through `scripts/mail.mjs` from the account in `.mail.env`, with the body saved as `cover-letters/<company>-<role>.txt` and the CV as `--attach`; the exact command is in `docs/sweep-events.md`.

## Render and record

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/render.mjs" cover-letters/<company>-<role>.md
```

Check the PNG: one page, header matches the CV header. If `.data.git/` exists, run `"${CLAUDE_PLUGIN_ROOT}/scripts/data" save "cover letter <name>"`. Then in JobCubby add a timeline event on the application ("Cover letter written, file cover-letters/<name>.pdf") and, if the application is new, create it with the letter path in the description.
