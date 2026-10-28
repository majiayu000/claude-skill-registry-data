---
name: chatter-scout
description: Sweep the web for new chatter on a topic, skip what earlier runs already saw, verify what is left, and write one ranked, cited findings file to feed a blog post or a digest email.
disable-model-invocation: true
argument-hint: "A topic or profile slug (omitted: the repo's only profile)"
allowed-tools: "WebSearch WebFetch"
compatibility: "Needs jq on PATH"
model: sonnet
effort: medium
---

# Chatter Scout

Run one scouting pass on a topic, then offer next steps. Output is one findings file; nothing is drafted, sent, or published unless the user picks that next step. Safe to re-run: the seen-ledger keeps every run from resurfacing what an earlier one reported.

Cost is the design constraint. The lead (this skill) does no bulk searching or page reading; it writes briefs, runs the ledger script, ranks, and writes the file. Searching fans out to cheap sweepers; page reading goes only to candidates that survive the ledger.

## Files (in the target repo)

- **Profile** `docs/chatter/<topic-slug>/profile.md`: the lens, sources, and watchlist. Format and bootstrap rules: [PROFILE-FORMAT.md](PROFILE-FORMAT.md).
- **Ledger** `docs/chatter/<topic-slug>/seen.json`: JSON array of normalized URLs already judged. Only [scripts/filter-seen.sh](scripts/filter-seen.sh) reads or writes it; it never removes an entry.
- **Findings** `.scratch/chatter/<topic-slug>/<YYYY-MM-DD>.md`: this run's output. A second run on the same day appends `-2`, `-3`.
- **Legacy log** `docs/intel/chatter-log.md`: the layout before profiles. Step 1 imports it once; nothing writes to it.

## Steps

1. **Resolve the topic.** `$ARGUMENTS` is a profile slug or free text. Slugify free text and match it against `docs/chatter/*/profile.md`. No argument: use the only profile; if there are zero or several, list them and stop. No profile for the topic: bootstrap one per PROFILE-FORMAT.md. If `seen.json` does not exist and `docs/intel/chatter-log.md` does, import the old log first: pipe every URL in it (`grep -oE 'https?://[^ )>\]]+'`, as a JSON array) to `filter-seen.sh add`, and note the count and the log's newest date for the recap. Earlier runs reported those items, so a missing ledger never means nothing was reported before. *Done when* one profile is loaded and today's date is known from the environment.
2. **Load what is already covered.** If the profile has `covered:` globs, collect the title (and tags, if any) from each file's frontmatter, one line each. Do not read bodies. *Done when* you hold a covered-titles list (possibly empty).
3. **Sweep.** Dispatch one sweeper per profile source group (watchlist included), at most 5, **in parallel** (in Claude Code with this plugin installed, `subagent_type=leek-skills:chatter-sweeper`; in plain Claude Code, `general-purpose` with `model: haiku`; elsewhere, any sub-agent on the cheapest model the harness offers, or run the groups inline one after another). Each brief carries: today's date, `window_days`, the Lens, Buckets, and Ignore sections verbatim, that one group's sources, queries, and notes, and the **Sweeper** section of [BRIEFS.md](BRIEFS.md). Nothing else. *Done when* every sweeper has returned its JSON array.
4. **Drop what the ledger has seen.** Concatenate the arrays and pipe them through `bash <skill-dir>/scripts/filter-seen.sh filter docs/chatter/<slug>/seen.json`. Then drop, by title, anything a covered title already covers, or that an earlier findings file for this topic already reported under another URL (an index, mirror, or syndicated copy of the same item; read only those files' `##` headings and **Source** lines): a genuinely new development in a covered story (new ruling, new data, new state) stays. Move any item dated before the window (non-evergreen buckets) to an **Older than window** list: it skips verification, and the findings file names it so the user can pull it back in. If more than 15 survive, keep the 15 that best fit the Lens, taking day-dated items before undated ones: an undated item takes a slot only when no dated item fits. *Done when* at most 15 new candidates remain; if none remain, skip to step 6.
5. **Verify.** Split the survivors into batches of about 5 and dispatch one verifier per batch **in parallel** (in Claude Code, `subagent_type=leek-skills:chatter-verifier`; in plain Claude Code, `general-purpose` with `model: sonnet`; elsewhere, a sub-agent on a mid-tier model, or inline). Each brief carries: today's date, `window_days`, the Lens, Buckets, and Ignore sections, the batch, the profile's fetch notes, and the **Verifier** section of BRIEFS.md. A candidate the verifier marks `unreachable` stays `unreachable`, including a page whose text it could not read. The lead does not fetch it or extract that text. *Done when* every candidate has a verdict.
6. **Rank and write.** Keep verdict `keep` and `community`. Rank by fit to the Lens first, then freshness (for non-evergreen buckets), then how many concrete facts the item carries. Take the top `max_items`; the rest go under **Also seen**. Write the findings file in the format below. *Done when* the file exists.
7. **Update the ledger.** Pipe a JSON array of every URL with verdict `keep`, `community`, `off-topic`, `stale`, or `thin`, plus every **Older than window** URL, to `filter-seen.sh add`. Leave `unreachable` out so a later run retries it. *Done when* the script reports its `added` count.
8. **Recap** in 3–6 lines: groups swept, candidates found, new after the ledger, kept; the single strongest item; the findings path; and, if the profile was bootstrapped, that it needs review.
9. **Offer next steps.** End every run, a zero-keep run included, with 2–4 concrete options inside one question (`AskUserQuestion` where available: one single-select question, the options being the next steps; otherwise one numbered list in chat): for example draft a post or digest from item N, pull back an **Older than window** item, widen the window and re-run, or stop. Act only on the answer. *Done when* the user picked one.

Never write to the profile after it exists, and never edit an earlier findings file.

## Findings format

```markdown
# Chatter: <topic>, <YYYY-MM-DD>

Swept <n> groups · <n> candidates · <n> new · <n> kept. Purpose: <blog | digest | both>.

## 1. <title>
- **Bucket:** <bucket> · **Date:** <YYYY-MM-DD, or "undated"> · **New this week:** yes | no
- **Source:** <publication> <URL>
- **Summary:** 1–2 lines.
- **Facts:** the specific numbers, dates, names, and citations the item hangs on.
- **Why it matters:** 1–2 lines against the Lens.
- **Angle:** for blog, the search query or headline it could win; for digest, the one line a reader acts on.
- **Action:** watch | respond | build | share | write
- **Confidence:** verified | community (unverified sentiment, not fact)

## Also seen
- <title>, <URL>: one line.

## Older than window
- <title>, <URL>, <date>: one line. Not verified; ask to pull one back in.

## Rejected
<n> off-topic · <n> stale · <n> thin · <n> unreachable (retried next run)
```

With no kept items, write the header line, `No new relevant chatter.`, and the **Older than window** list if it has entries.
