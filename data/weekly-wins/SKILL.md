---
name: weekly-wins
description: A one-page weekly debrief of what you and your team did this week against last week, built from git, your agent chats and whatever metrics you track, bottom line first. Use when you say "weekly debrief", "weekly one pager", "what did we do this week", "week in review", "what changed since last week", "status for the team meeting" or "BLUF of the week".
---

# Weekly debrief

One page the user can put in front of a partner, team or manager each week. **It is a debrief of what happened
this week, compared with last week: the bottom line first, then what went right, then the experiments and how
each went.** It never asks for decisions, recommends bets or says "decide today". If the user wants a decision,
use `help-me-decide` instead.

**Window: the last 7 days, compared with the 7 days before.** Use a different window only when the user names one.
The first run has no earlier page, so say it sets the baseline. Lead with what was done and what is working.
Show this week's numbers with last week's beside them for comparison, and use a before and after only to prove
that a specific change worked (for example "after the new signup page: 3.0 to 4.4 signups a day").

## 0. Set it up once (ask on the first run, then reuse)

Ask only what you cannot find yourself, and save the answers in a short `weekly-wins.config.md` next to where
the pages are kept, so later weeks need no questions:

- **Scope.** What the debrief covers (for example the whole company, marketing and sales, one product, or one
  team) and what to leave out (side projects, pure engineering, and so on).
- **Who reads it.** The audience sets the depth and the words.
- **Repos.** The git repos whose commits count as this scope's work.
- **Metrics.** Where the numbers live: an analytics export, a dashboard, a database query, a spreadsheet, a
  billing or store console, a CSV the user drops in, or a skill such as `grow-my-revenue` or
  `mission-control`. If the user has none, the page runs on git and chats only and says so.
- **Where pages go.** A folder for the weekly pages, and whether they may be committed. If any metric is private
  (money, customers, anything the user would not post publicly), keep that folder out of git and tell the user.

## 1. This week's numbers

Pull each metric for this week and last week from the sources in the config. Run slow pulls in the background.

- **Count things from the live source or git, never from a mid-chat message.** A chat may say "11 items" when the
  repo holds 24.
- If a source did not refresh, say which and leave its tile out. Never guess or fill in a number.
- Keep each number with its label, its unit and its date range.

## 2. What happened this week

1. Run the collector from this skill's folder and read its output whole:

   ```bash
   python3 -I gather.py --since <7 days ago, YYYY-MM-DD> --repo <repo> [--repo <repo> ...] \
     [--topic "<words that mark this scope's chats>"] [--skip "<words that mark chats to leave out>"] \
     --out <scratch>/week.txt
   ```

   It reads local agent chat transcripts (Claude Code and Codex folders by default; pass `--chats <folder>` for
   others) and git, and prints this week's chats with their first asks and last answers, plus commit counts for
   this week and last week and this week's commit log. It sends nothing anywhere.
2. Read the chats that matter in full (the `resume-any-chat` skill helps find one by title). Newer numbers beat
   older ones. If two chats disagree, use the one that says it corrected the other.
3. Add what the chats and git do not hold, when the user has the tools connected: shipped releases, merged pull
   requests (`gh pr list --state merged --search "merged:>=<date>"`), posts and their reach, emails or newsletters
   sent, places the product went live (stores, directories, listings), and replies or messages worth noting from
   the inbox (read only). Never claim praise or results you did not find.
4. Read last week's page so its "Still running" items get their result this week.

## 3. Write

If you have them, load `make-it-sell`, then `sound-human` last.

Tone: **positive and confident, never defensive, anxious or cautious.** Lead with what went right. What isn't
working is stated plainly as fact, in one short list, never as worry. Every fact right, every claim backed by data.

- **Headline:** the week's biggest true win, with its number.
- **Bottom line:** three short paragraphs. What we did this week, what is working (with numbers against last
  week), and what the week produced (releases, features, content, customers, whatever the scope counts).
- **What's working:** up to 8 tiles. Each shows this week's number, last week's beside it, and a short note on what
  drove it.
- **What we got right:** 4 to 6 numbered wins, each a bold label plus one sentence with its numbers.
- **Experiments:** one table per area the scope has (for example product, sales, reach), with columns when,
  experiment, what happened (with numbers) and a result tag: Worked, Shipped, Learned, Running, Growing, Baseline
  set, Live early. No warning-colored tags. Include last week's "Still running" items with their result.
- **Still running** and **What hasn't worked yet** side by side. Each "hasn't worked" line says what we did about
  it, when we did something.
- **Footer note:** which chats, repos and metric sources it came from, any caveat a number needs (for example
  "before fees" or "excludes refunds"), and the exact dates of both windows.

No em dashes, no colon reveals, no recap at the end.

## 4. Publish

- Write the page as one HTML file named `<YYYY-MM-DD>-weekly-debrief.html` in the pages folder from the config.
  Copy last week's page for layout and tone when one exists, so the weeks look alike.
- If your agent can publish private pages (for example Claude's Artifacts), also publish it as a **new** page each
  week so every week keeps its own link, and remind the user it stays private until they share it.
- Do not commit it if it holds private numbers. Tell the user where the file is.
