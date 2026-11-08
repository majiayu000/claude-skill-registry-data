---
name: share-lessons
description: "Use when the user got a job (or wraps up or pauses their search) and wants to help future job seekers, says 'share what worked', 'give feedback', 'lessons learned', 'tell the makers', or presses Share what worked in the Celebration panel. A few quick questions, then an anonymous draft with no names, companies, pay or contact details, checked by a script, that the user may post on the project's GitHub page themselves."
---

# /share-lessons: help the next job seeker

Optional and short (about 2 minutes). The user's answers become a few anonymous notes they can post on the project's GitHub page, where the makers read them to improve this workspace for everyone. **You never post anything:** you draft, they read it, and only they post it (ground rule 2). Their files never leave the folder.

## 1. Ask once

Say it plainly, in two sentences: "Want to help people who are where you were? I'll ask 5 quick questions, then draft short notes with no names, companies, pay or contact details. You read them, and only if you want, post them on the project's GitHub page yourself." Add one honest line: "GitHub shows the username of whoever posts, so it's anonymous only in what it says; if you'd rather not be linked, you can keep the notes, or post from a GitHub account without your name. It's public and stays online, so your new employer could read it: many people wait until after their start date." A no is fine: thank them and stop. Don't ask again in this session.

## 2. Five questions (one per message, in their words; any can be skipped)

1. "What made the biggest difference in landing this job (or in your search so far)?"
2. "What would you do differently, or what didn't work?"
3. "Which parts of this workspace helped most, and was anything confusing, missing or broken?"
4. "One tip for someone starting their search today?"
5. "In a few words, your kind of work and country (for example 'nursing, Canada'), so the notes help people like you. Skip it if you'd rather."

Don't probe, and don't ask why they left a job, about health, or anything personal.

## 3. Draft it

Write `history/lessons-draft.md` (their file; never inside the app's folders), in this order, short and in their voice, plain text:

```
Outcome: <got a job / still searching / paused>
Work and country: <their answer to 5, made general>
Search in numbers: <applications band>, <interviews band>, <weeks band>
Used: <Claude Code / Codex / both>, version <VERSION>
What made the difference: ...
What I'd do differently: ...
What helped most in the workspace: ...
Confusing, missing or broken: ...
Tip for someone starting today: ...
```

- **Numbers in bands only**, from `jobs/tracker.csv` (count as the `insights` skill does): applications `1-10`, `11-25`, `26-50`, `51-100`, `over 100`; interviews `0`, `1-2`, `3-5`, `6-10`, `over 10`; weeks from the first application to today `under 4`, `4-8`, `9-16`, `17-26`, `over 26`. Never exact dates, pay, or the offer's terms.
- **Make it anonymous:** no names of people (their own included), employers, schools, recruiters or agencies, towns or cities (a country or a broad region is fine), job titles narrow enough to identify someone (say "a data analyst role", not the team's name), project or product names, emails, phone numbers, links, pay, exact dates, or anything their employers might consider confidential (ground rule 3). Turn specifics into general lessons: "a referral from a former manager" not "Jane at Globex".
- **Could it still point to them?** A rare role, a small country or region and a timeline together can identify someone even with no names. If the combination is that narrow, make it broader (the role family instead of the title, a region instead of a small country, "a few months" instead of a count).
- Keep their meaning; don't add claims they didn't make, and don't polish their criticism away.

## 4. Check it twice

1. Run the privacy check: `bash .claude/skills/share-lessons/scripts/check-anon.sh history/lessons-draft.md` (Windows without bash: `powershell -NoProfile -ExecutionPolicy Bypass -File .claude\skills\share-lessons\scripts\check-anon.ps1 history/lessons-draft.md`). It compares the draft with the names, companies, emails and places in their tracker, contacts and preferences, and looks for emails, phone numbers, links, pay and exact dates. Fix every `found:` line and run it again until it says `ok:`.
2. Then read the draft yourself for what a script can't see (a school, a manager described in words, a one-of-a-kind detail), and fix that too.
3. Show the user the whole draft, with a short list of what you took out or made general ("I left out the company's name and your city"), and end with one question: "Please read it once. Is it ready to post, or should I change or take out anything?" Make their changes, then run the check again.

## 5. Posting is theirs

When they're happy, give them the link and the steps, one at a time; don't open it in a browser or fill it in for them:
1. Open https://github.com/ClarvAI/job-search-hq/issues/new?template=lessons-learned.yml (a free GitHub account is needed; signing up is theirs to do).
2. Copy each part of the draft into the matching box (or the whole draft into the last box), tick the box saying nothing in it identifies anyone, and press **Create**.

Never post it yourself (no `gh`, no API, no browser), and never put the draft into a link. If they'd rather not post, that's fine: the draft stays in `history/` for them, and nothing has left the folder. Add one line to `history/activity.md`: `Lessons-learned draft ready (not posted)`; no content. Thank them warmly either way.

## In Codex

The same steps; the privacy check runs the same way.
