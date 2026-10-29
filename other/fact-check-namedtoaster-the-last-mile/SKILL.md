---
name: fact-check
description: Re-check stated facts about the App Store, Google Play and app tools against the current official pages, update each fact's status and date, fix broken source links, and report what changed. Works on a project's rules file and docs, or on The Last Mile's own traps and facts (one topic or all of them). Use when the user says "check the facts", "is this still true", "re-verify the traps", "store rules changed", or before a store submission.
---

# Fact check

Facts about stores and tools go stale quietly. This skill re-reads the official page
behind each fact and records what it found, so every status means what it says.

## Pick the target

- **Inside a user's project:** the facts their rules file and docs state about the
  stores and their tools (fees, tester counts, target API levels, review guidelines,
  console steps). Ask which files if it is not obvious. Only check statements that
  claim an outside rule or number; skip the project's own decisions.
- **In The Last Mile repo or a fork:** every file in `skills/ship/references/`
  (traps, facts, stacks, domains, payments, levels, rulebooks) and the factual
  claims in `skills/ship/SKILL.md`, including console steps. The user may name one
  topic ("Google Play testing", "account deletion") or ask for everything. An open
  "Re-check facts" issue names the files whose sources changed; start there.

List the entries you will check and how many there are before starting.

## Status meanings

Use the same three statuses as the traps reference:

- **Checked YYYY-MM-DD (official page opened and read):** the page was opened today
  and a sentence on it supports the entry.
- **From experience:** it happened to a real app, but no official page states it.
- **Needs a human:** the answer sits behind a console login no automation can read.
- **Seen on screen YYYY-MM-DD:** the user's own console screen showed it (a
  screenshot or pasted text). The live screen beats a saved page: when they
  disagree, record what the screen showed, note that the official page lags, and
  keep the page as the source for anything it still states correctly.

In `facts.md` the status lives in the **Last checked** column: a date means Checked,
otherwise write "From experience" or "Needs a human".

## Check each entry

1. **Open the source page.** Fetch the page itself. A search snippet or summary is
   not enough. If the page will not load (blocked, login wall, timeout), use these
   in order and say which one you used:
   - **The Last Mile's saved copy.** A weekly job saves a text copy of every page the
     ship references cite. Read `sources/index.json` in The Last Mile
     (`https://raw.githubusercontent.com/namedtoaster/the-last-mile/snapshots/sources/index.json`,
     on the `snapshots` branch), find the URL, and read `sources/<file>` from the same branch.
     GitHub is reachable from cloud sessions by default, so this needs no settings.
     The copy counts as the page opened on its `fetched` date: set **Checked
     <fetched date> (saved copy of the official page)**. If `fetched` is more than a
     month old or the entry has an `error`, say so.
   - Another route to the same page: a different fetch tool, or the page in another
     language on the same official site.
   - A search with results limited to the official domain. That is a lead: an entry
     read only this way is **Not yet checked**, per `CONTRIBUTING.md`.
   If all of these fail, leave the status as it was. If the block comes from the
   session's network rules, name the host in one line at the end of the report, as
   an optional fix; never make the user change settings to get an answer.
2. **Find the supporting sentence.** Quote it word for word in your notes. If the
   entry has no source, search the official docs (Apple, Google, Expo, the tool's own
   site) for one. Blogs, forums and other repos are leads, never sources.
3. **Decide:**
   - The page supports the entry: set **Checked** with today's date.
   - The page contradicts it: write the corrected wording, show the old and new text
     with the quoted sentence, and wait for the user to agree before changing it.
   - No official page states it: keep or set **From experience**.
   - It sits behind a console login: set **Needs a human**, with what to look for.
4. **Fix the link.** If the link is broken or redirects, replace it with the current
   official URL. Point it at the exact rule: use the anchor for the guideline section
   (for example `#5.1.1v`) or the specific help article, not a home page. Open the
   new link to confirm it lands on the rule.

## Console steps

Steps through a console (App Store Connect, Play Console, RevenueCat, a registrar)
are facts too, and the most likely to drift. Before giving or writing any:

- Read the saved copy of the vendor's page for that screen, and give the steps in
  its words. Say which steps come from the page and which from memory.
- Name the fields the user will see in order, so a missing or extra field shows up
  at once. When the user reports a different screen, ask for the exact text or a
  screenshot, correct the reference the same day, and mark it **Seen on screen**.
- One wrong step usually means the page is old: re-check the other steps from the
  same page before carrying on.

## Hard rules

- Never upgrade a status from memory. Checked needs a page opened today.
- Never set a date on an entry you did not open.
- Do not soften an entry that the page contradicts; correct it or flag it.
- Change only the status, date, link and, once agreed, the wording. Keep each
  entry's shape (see `CONTRIBUTING.md`, "Adding a trap", in The Last Mile).
- Plain words in any wording you write. No long dashes.

## Report

Reply in chat with a short table, one row per entry checked:

| Entry | Old status | New status | What changed |
| --- | --- | --- | --- |
| Testers for a new personal account | Checked 2026-07-02 | Checked 2026-10-11 | Nothing |
| Account deletion in the app | Checked 2026-07-02 | Checked 2026-10-11 | Link now points at the guideline anchor |

Then:

- Proposed rewrites, each with the old text, the new text and the quoted sentence.
- Pages that would not load, and entries marked **Needs a human**, so the user knows
  what is still unconfirmed.
- The edits made, as a list of files.

Keep it short. Rows where nothing changed can be grouped into one line if there are
many.

## When to run it

- **Before a submission:** the ship skill should run this on the traps that apply to
  the release (iOS, Android, or both) before preparing the submission.
- **When a rule seems to have moved:** a rejection names a guideline the traps do not
  match, or the user hears a store rule changed.
- **When a saved copy changes:** the weekly snapshot job
  (`.github/workflows/snapshot-sources.yml`) commits every page whose text changed.
  A changed or failed page opens a "Re-check facts" issue naming the reference files
  that cite it; run this skill on those files and close the issue with the result.

## Done when

Every entry in scope has been opened or reported as not loadable, every status and
date in the files matches what was found today, and the user has seen the table.
