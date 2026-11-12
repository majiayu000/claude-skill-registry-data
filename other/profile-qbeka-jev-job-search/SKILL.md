---
name: profile
description: Check or change the candidate profile, the standing answers, the drafts and the voice guide. Use when the user says /profile, when a form answer looked wrong, or when their details changed. For a first run use /setup instead.
model: claude-sonnet-5-5
effort: high
---

# /profile: check or change the candidate's data

If `data/profile.json` does not exist, this is a first run: use the
`/setup` skill instead.

1. Run `npx jev doctor`. A schema error names the field to fix.
2. Ask what the user wants to change, or which answer on a form was wrong.
3. Make the change in the right place:

   | What was wrong | Where to change it |
   |---|---|
   | A detail about the person: contact, education, dates, work authorization | the matching field in `data/profile.json` |
   | A claim in a written answer, or a missing one | `facts`, `experience` or `projects` in `data/profile.json` |
   | How a recurring question is answered (relocation, text messages, notice period, pay, history) | `answers` in `data/profile.json` |
   | How written answers sound | `data/voice.local.md` |
   | The starting draft for a common open question | `data/bank.json` |

   The full list of questions the profile answers is in
   [../setup/questions.md](../setup/questions.md).
4. Run `npx jev doctor` again, then rehearse the form that was
   wrong: `npx jev apply --dry <job id>`.

Things to know:

- Any change to the profile, the drafts or the voice guide makes the tool
  forget its remembered answers, so the next run asks Claude again with the
  corrected facts. That is on purpose.
- Anything not in `facts`, `experience`, `projects` or `answers` will never
  appear in an application.
- These files are git-ignored. Never commit them.
