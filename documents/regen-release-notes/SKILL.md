---
name: regen-release-notes
description: >
  Turn a commit batch, sprint, or SHIPPED_LOG entry into player-facing release
  notes for ReGen Civics. Produces forum post, newsletter blurb, Twitter thread,
  changelog entry, or all four. Voice-matched, voice-clean (no em-dashes, no
  AI tells), and clear about which changes affect players directly vs.
  infrastructure work. Triggers on: "release notes", "what's new", "changelog",
  "release post", "ship update", "sprint summary for the community", "what
  shipped this week", "tell the community what landed", "publish release",
  "update post", or any request to communicate recent changes to players,
  investors, or the wider community.
---

# ReGen Civics Release Notes

## What this skill does

Translate technical work into communications that land for players, land
project leads, investors, and movement watchers. Every release note has to
do three things at once: tell people what changed, why it matters to them,
and what they can do next.

This skill is NOT a generic changelog generator. It assumes you know the
two-tier audience structure (Fund vs. Game), the ReGen Civics voice rules,
the four-token model, and the four channels we publish into.

## Inputs the skill expects

Pick one or combine:

1. **A commit range.** e.g. "release notes for last week's commits". Pull
   `git log --oneline --since="1 week ago"` and group.
2. **A SHIPPED_LOG entry.** e.g. "release notes for the Phase 4 token
   launch". Find the matching entry in `SHIPPED_LOG.md` and unpack it.
3. **A FIXES_TO_MAKE doc.** e.g. "release notes for the items we shipped
   from FIXES_TO_MAKE_2026-04-24.md". Pull only items marked DONE / VERIFIED.
4. **A free-form list.** Rye describes what shipped, the skill structures it.

## The three buckets

Every release breaks into these three buckets. Skip a bucket if it's empty;
don't pad it.

| Bucket             | What goes here                                                                | Example                                     |
| ------------------ | ----------------------------------------------------------------------------- | ------------------------------------------- |
| **For players**    | Things a player can see, click, or feel on the site                           | New quest, new page, new visual, new flow   |
| **For partners**   | Things land project leads, investors, or alliance partners care about         | New API, new funding pool, new application  |
| **Under the hood** | Infrastructure that unlocks future work but isn't itself user-visible        | Token model migration, FUSE workarounds     |

## The four channels (output formats)

The skill should default to producing all four when invoked without channel
specified, plus a master `RELEASE_NOTES_YYYY-MM-DD.md` file with the long form.

### Channel 1: Forum post (long form)

For `/community/announcements`. Markdown. 200-500 words.

Structure:

```
# What shipped this week (or "What shipped: [feature name]")

[1-2 sentence opening that names the thing and the why]

## For players

- [Specific, concrete change]. [What you can do with it]. [Where to find it / link]
- ...

## For partners

- [Specific, concrete change]. [Why it matters for land projects / investors]
- ...

## Under the hood (the boring magic)

- [Plain-language summary of infra work]. [What it enables next]

## What's next

[1-2 sentences pointing at the next thing on the horizon]

[Closing: a real question or an invitation to a real conversation, not "stay tuned"]
```

### Channel 2: Newsletter section (medium form)

For the weekly/monthly newsletter. 100-200 words. Skip the "Under the hood"
bucket entirely; newsletter readers don't care.

Lead with the single biggest player-facing change. Then list 2-3 supporting
items. End with the one CTA the reader should take.

### Channel 3: Twitter / X thread (short form)

5-9 tweets. First tweet hooks. Middle tweets each cover one shipped item.
Last tweet links to the full forum post + invites a reply.

Voice rules apply doubly here. No "🚀". No "huge week". No threads that open
"This is going to change everything." The voice on Twitter is the same as
the voice in the forum: direct, grounded, specific.

### Channel 4: Discord / forum quick-update

2-4 sentences. The version you'd say standing up at the start of a meeting.

## Voice rules (binding)

These ride on top of the project-wide Writing Rules. Specific to release
notes:

- **Lead with what's true, not what's exciting.** "We shipped the token
  ledger migration. It moves all four tokens onto a single private ledger
  with one append-only audit row per credit." That's the lede. Not "Get
  ready for a huge update."
- **Specific is better than impressive.** "47 new quests" beats "tons of
  new content." "Sign-in now works on iPhone Safari" beats "auth is more
  reliable."
- **Name the people who did the work** when relevant. The community sees
  the work. They want to see who's behind it. (Default to "Rye and Claude,
  with [contributor names] on [specific items]" if Rye approves naming.)
- **No "we're excited to announce."** Just announce it. Excitement is the
  reader's job, not the writer's.
- **Honesty about what's still rough.** If a feature shipped but only on
  desktop, say so. If a bug got fixed but a related one is still open, say
  so. Trust grows on candor.

## What NOT to include in release notes

- Infrastructure that doesn't unlock anything yet (don't ship "we updated
  React" as a release note item)
- Internal renames, refactors, type fixes
- Commit messages copy-pasted verbatim ("fix(build): drop duplicate
  maxClaimable" is not release-note material)
- Future plans dressed up as shipped work

## Cadence guidance

- **Weekly digest:** Friday afternoon publish. Forum post + newsletter +
  Twitter. Skip Discord standalone (the forum post posts to Discord
  automatically via the integration).
- **Big-feature release:** Same-day-of-launch publish. All four channels.
  Long-form forum post leads. Twitter thread links to it.
- **Quiet week:** Don't force a release post. Skip and roll into next week.
  Bad release notes are worse than no release notes.

## The 5-minute structured pull

When asked to produce release notes from a commit range, do this in order:

1. `git log --oneline --since="X" --no-merges` to get the candidate list
2. Group by SHIPPED_LOG entry if one exists for that period
3. For each commit, decide: For players / For partners / Under the hood / Skip
4. Drop the Skip pile entirely
5. Cluster related commits into a single release-note line each
6. Draft the forum post first (longest), then derive the other three from it
7. Run the voice check: search for em-dashes (zero allowed), AI words, "not X
   but Y" framing, hollow excitement. Fix everything.

## Cross-references

- `regen-content-repurposing` for adapting between channels after the first
  draft is locked
- `regen-fundraising-copy` for investor-tilted release notes (e.g. "we
  closed Season 1 with X funding committed")
- Voice rules: see `CLAUDE.md` Writing Rules section
- For event launches specifically, use `regen-event-blast` instead of this
  skill (it's tuned to forward-looking announcements)
