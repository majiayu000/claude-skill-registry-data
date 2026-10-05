---
name: changelog-writer
description: >
  Write external-facing changelog and release note entries in a pithy, tastefully sassy,
  occasionally clever voice that makes software updates fun to read without burying what
  actually shipped. Use this skill whenever someone asks to write, draft, or review a
  changelog entry, release notes, "what's new" post, or product update announcement for
  end users. Also trigger when someone pastes a list of shipped features/fixes and wants
  them turned into public-facing copy, or asks to make a changelog "less boring," "more fun,"
  or "not sound like corporate speak."
version: 1.0.0
audience: external
---

# Changelog Writer

Writes external, end-user-facing changelog entries with personality — modeled on what
Slack, Basecamp, Linear, Raycast, and Tumblr do well: voice and confidence first, jokes
used sparingly and only in service of the fact, never replacing it.

**This skill is for external/end-user changelogs.** If the audience is internal engineering
or the changelog needs to double as a searchable technical record (breaking changes, API
versioning, migration notes), this tone is the wrong trade — use a precise, Stripe-style
format instead and skip this skill.

**Reference files:**
- `references/voice-examples.md` — annotated examples of the tone done well (Slack, Basecamp,
  Tumblr, Raycast, Linear) and done badly, for calibration
- `references/draft-format.md` — the full spec for the intermediate draft format the scripts parse

**Scripts** (in `scripts/`) — run these against every draft before presenting a final version:
- `check-all.mjs` — runs everything below and gives one pass/fail report
- `check-structure.mjs`, `check-sass-budget.mjs`, `check-voice.mjs`, `check-length.mjs`, `check-cadence.mjs`

---

## Workflow

1. **Gather the raw material.** Get the list of what actually shipped — feature names, what
   changed, any tickets/PRs. If it's vague ("we improved search"), ask what specifically changed
   before writing anything. A joke can't rescue an entry with no real content behind it.
2. **Group by theme, not by ticket.** Five related tweaks become one entry. Assign each entry
   a `category` (`New`, `Improved`, or `Fixed`) and a stable `id` (a slug from the feature name,
   not a sequence number — this is what makes the rule IDs and scripts useful over time, since
   entries can be tracked and diffed release over release).
3. **Draft every entry in the structured format** described in `references/draft-format.md`.
   Write the whole draft this way first — plain field-by-field — before making it pretty.
   This is what makes the entry checkable by script instead of just vibes.
4. **Run `node scripts/check-all.mjs <draft-file>`.** Fix every FAIL. Read every WARN and use
   judgment — WARNs are things worth a second look, not always things to change.
5. **Re-run until clean**, then convert the structured draft into the final published prose
   (see "Rendering the final version" below).
6. **Present the finished changelog**, not the structured intermediate format — the field
   labels are a drafting tool, not something an end user should ever see.

---

## The building blocks (rule reference)

Every rule below has a stable ID. The scripts check the ones marked **[scripted]**; the rest
are judgment calls a script can't reliably make — apply them yourself when drafting.

### Entry skeleton — `STRUCT-*`

- **STRUCT-01** *(scripted)* — Headline is mandatory. Plain statement of what shipped, no pun
  required. Whoever's skimming has to get this in one glance.
- **STRUCT-02** *(scripted)* — So-what is mandatory for `New`/`Improved` entries (optional,
  can collapse into the headline for `Fixed`). One sentence on why this matters to the reader,
  written like you're telling a friend, not pitching a feature.
- **STRUCT-03** *(scripted)* — Receipt is mandatory for `New`/`Improved` entries. The actual
  detail: what changed, what to click, what's different. Always plain English, never vague
  ("various improvements" fails this check).
- **STRUCT-04** — Hook is optional and the only piece allowed to be cut. Better no joke than
  a forced one.

### Sass budget — `SASS-*`

- **SASS-01** *(scripted)* — One bit per entry, max. If the headline already lands a joke, the
  hook stays quiet.
- **SASS-02** *(scripted)* — Zero jokes near security, billing, data loss, outages, or anything
  users would be upset about. Straight talk only. This is a hard rule, not a style preference.
- **SASS-03** *(scripted, batch-level, warn only)* — Not every entry needs a bit. If most entries
  in one release have a hook, personality has stopped being special.

### Voice — `VOICE-*`

- **VOICE-01** *(scripted)* — No corporate buzzwords or press-release phrasing ("we are pleased
  to announce," "leverage," "seamless experience," "blazing fast" — say the actual number instead).
- **VOICE-02** *(scripted, warn only)* — Use contractions. Formal constructions read stiff.
- **VOICE-03** *(scripted)* — No clichéd pun templates (egg-cellent, purr-fect, fin-tastic,
  and the like — swap-a-word-for-a-similar-sounding-word puns that are worn out regardless of
  the feature) and no lampshading ("get it?", "pun intended", a winking emoji). If a joke has
  to announce itself, it already failed.
- **VOICE-04** *(judgment only, not scripted)* — The "two truths, one phrase" test: a pun is
  only good if its second meaning is also literally true of what shipped, not just wordplay
  that happened to be available. A script can't know what's true about the feature, so this
  one's on you. See `references/voice-examples.md` for the full breakdown.

### Length — `LEN-*`

- **LEN-01** *(scripted)* — `Fixed` entries: ~30 words total across all filled fields. Should
  read in one breath.
- **LEN-02** *(scripted)* — `New`/`Improved` entries: 4 sentences max combined across all fields.
- **LEN-03** *(scripted)* — No single field over 40 words. If it needs a paragraph, the feature
  is confusing, not the changelog.

### Cadence / metadata — `CAD-*`

- **CAD-01** *(scripted)* — Category must be `New`, `Improved`, or `Fixed`. Nothing fancier —
  the categories aren't where the personality goes.
- **CAD-02** *(scripted, warn only)* — Every entry needs a unique, stable id (a slug, not a
  sequence number), so entries can be tracked release over release.
- **CAD-03** *(judgment only)* — Ship an entry every release, even a boring one. Consistency is
  what earns the reader's trust that the funny ones are worth reading.

---

## Rendering the final version

Once a draft passes `check-all.mjs` clean, convert each entry from the structured fields into
one flowing changelog entry:

```
## [Headline, possibly rewritten as a title]
[Hook, if present — one line, woven in naturally] [So-what, one line] [Receipt, the actual detail]
[CTA, if present]
```

Group entries under `New`, `Improved`, `Fixed` headers, in that order. Don't show the reader
`headline:` / `hook:` / etc. labels — those are scaffolding for the check, not part of the
output.

**Example — structured draft:**
```
### ENTRY id=bulk-actions category=New sass=hook
headline: Bulk actions have entered the chat.
hook: You can now select every unread thread at once.
sowhat: Stop clicking the same checkbox forty times.
receipt: Select multiple conversations from the inbox and archive, tag, or reassign them in one action.
cta: none
### END
```

**Rendered as:**
> **Bulk actions have entered the chat.** Select every unread thread at once instead of
> clicking the same checkbox forty times — archive, tag, or reassign a whole batch in one go.

---

## Common failure mode to watch for

The most common way this goes wrong isn't "not funny enough" — it's overwritten. Every entry
trying too hard, reader fatigue setting in by the third one. When in doubt, cut the hook before
you cut the receipt. The fact always survives; the bit is expendable.
