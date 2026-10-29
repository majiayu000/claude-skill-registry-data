---
name: extract-lessons
description: Harvest a finished session for anything that would help beyond this one project, decide honestly where each piece belongs, and put it there. Most sessions yield nothing, and saying so is the correct outcome. Separates a project detail from a general trap, routes real findings to the right skill as a pull request, spots when a cluster of homeless lessons means a new skill is needed, and recognises when a body of knowledge is its own domain and belongs in a separate repo rather than bloating this one. Use at the end of a session, when the user asks whether anything is worth pulling into The Last Mile or another toolkit, or says "anything useful from this", "extract the lessons", "add this to the toolkit".
---

# Extract lessons

Anyone running several projects wants the toolkit to get better from each one.
This turns a finished session into whatever small, general thing it actually
produced, and most often that is nothing.

This is not `improve-skill`. That one fixes a skill that misbehaved. This one
looks for knowledge the toolkit does not have yet.

## The rule that makes this worth running

**The default outcome is nothing, and that is a success.** A skill that finds
something every time fills a public repo with one project's anecdotes, and the
next person reads them as advice. Expect to extract from maybe one session in
four. If you find yourself reaching, stop.

## 1. List the candidates

From the session, write down every thing learned, in one line each. Include the
mistakes, which are usually the best material. Do not filter yet.

Then, for each one, answer the only question that matters first:

> **Would this still be true for an app that is not this one?**

If no, it belongs in the project's own rules file (`CLAUDE.md` or `AGENTS.md`)
and nowhere else. Write it there and strike it off. This removes most of the
list, and removing it is the point.

## 2. Apply the evidence bar

What is left has to survive a second test, and it is stricter than it looks.

**Extract these:**

| Kind | Why it survives | Example shape |
| --- | --- | --- |
| A platform fact | Checkable by anyone, today | "A photo post takes a title capped at 90 characters AND a separate description. A video takes one caption" |
| A trap, with its mechanism | The reader can recognise it before it costs them | "Fine on a desktop preview and wrong on the phone means the platform is drawing its own UI over your image, not cropping it" |
| Arithmetic or a method | Produces the reader's own answer, not yours | "Never pay a cost per thousand views above your own revenue per thousand views. Compute it as revenue over installs, times installs per thousand views" |
| An exact invocation that works | Saves an hour of the next person's life | "`yt-dlp -U` fails for a pip install. Use `<that python> -m pip install -U yt-dlp`" |

**Do not extract these:**

- **"This worked for us."** Six posts, one campaign, one account. A result is not
  a method, and a stranger acting on your anecdote is the harm this bar exists to
  prevent.
- **Anything still contested.** If the session ended with two sources disagreeing
  and no measurement settling it, it is not knowledge yet. Leave it in the
  project's research notes.
- **Anything that only makes sense with your numbers in it.** If stripping the
  project's metrics leaves nothing, there was nothing.

A useful phrasing test: could you write it as a trap or a formula with **no
reference to your app at all**? If not, it fails.

## 3. Find each survivor a home

| The lesson is... | Goes to |
| --- | --- |
| A correction to how an existing skill behaves | `improve-skill`. Stop, run that instead. |
| New knowledge an existing skill should carry | That skill, as an added step, trap or table row. |
| Orphaned, and the only one of its kind | A one line note in the relevant skill's references, or nowhere. **Do not build a skill for one lesson.** |
| Orphaned, and part of a cluster of three or more related orphans | A new skill. See step 4. |

**When several lessons have nowhere to live, that is the finding.** It means the
toolkit has a gap, not that the lessons are weak. Say so plainly rather than
forcing them into the nearest skill that half fits.

## 4. A new skill, or a different repo

Before writing a new skill, ask what the cluster is actually about.

**This repo is about getting an app shipped and found.** A cluster inside that
subject becomes a skill here.

**A cluster that is its own domain does not.** Content marketing, hiring,
fundraising, customer support: each is a field with its own practice, and
absorbing one into a shipping toolkit makes both worse. The honest move is to
say: "this is three skills' worth of a different subject, it wants its own
repo." Then stop and let the user decide. **Never create a repo unprompted.**

Two signals that it is a separate domain rather than a skill here:

- Somebody could want this toolkit and not want that one at all.
- Explaining the cluster needs vocabulary this repo's other skills never use.

If it IS a skill here, write it the way the others are written: a short
description that says when to use it, numbered steps, tables over prose, and the
honest limits stated in the skill rather than discovered by the user.

## 5. Strip the project out

The repo is public. Before anything is committed, remove:

- The app's name, the user's name, handles, URLs and repo paths
- Every metric: revenue, user counts, view counts, conversion rates
- Screenshots, file paths and command output that identify the project
- Anything a competitor would find interesting

The lesson has to stand with all of that gone. If it does not, it was step 2's
"only makes sense with your numbers in it" and should not have reached here.

## 6. Open the pull request

1. Add one line under the unreleased heading in `CHANGELOG.md`.
2. Add the skill to the table in `README.md` if it is a new one.
3. Run `node scripts/validate.mjs` and fix what fails. It checks, among other
   things, that no Markdown file contains a long dash.
4. Commit only what you changed, push the branch, open a pull request following
   `.github/pull_request_template.md`.

If you cannot push to the repo, fork it and open the pull request from there.

## 7. Tell the user

A few lines, and be specific about what you threw away:

- What you extracted, and where it went.
- **What you considered and rejected, and why.** This is the most useful half.
  "Four things looked like lessons and were one project's results" tells the user
  their session was normal, not empty.
- The pull request link.
- If a cluster suggested a new repo, say so as a question, not a decision.

Then note that the project picks the change up on its next sync, and that the
synced copy under `.claude/skills/` must never be edited by hand.
