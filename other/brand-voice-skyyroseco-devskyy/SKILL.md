---
name: brand-voice
description: Build a source-derived writing style profile from real posts, essays, launch notes, docs, or site copy, then reuse that profile across content, outreach, and social workflows. Use when the user wants voice consistency across writing work without generic AI tropes. Do NOT use for drafting the content itself — that is article-writing / content-engine; this skill only produces the reusable VOICE PROFILE they consume.
origin: ECC
---

# Brand Voice

Build a durable voice profile from real source material, then use that profile everywhere instead of re-deriving style from scratch or defaulting to generic AI copy.

## When to use

- the user wants content or outreach in a specific voice
- writing for X, LinkedIn, email, launch posts, threads, or product updates needs a consistent register
- adapting a known author's tone across channels
- the existing content lane needs a reusable style system instead of one-off mimicry

**When NOT to use:**

- the deliverable is the article/post itself and a confirmed profile already exists — go straight to `article-writing` / `content-engine`
- the user wants a one-off tone tweak on a single sentence — just edit it
- no real source material exists and the user declines the documented defaults — a profile invented from imagination is worthless (see Failure modes)

## Inputs

Required before starting — **absent input = stop and ask, never proceed on imagination**:

1. **5–20 real samples** of the target voice, strongest first:
   1. recent original X posts and threads
   2. articles, essays, memos, launch notes, or newsletters
   3. real outbound emails or DMs that worked
   4. product docs, changelogs, README framing, and site copy
2. For the **SkyyRose founder voice**, the canonical repo sources are
   `docs/brand/collection-stories.md` and `docs/brand/corey-questions.md` — verbatim founder
   language, locked canon. Read them; do not paraphrase from memory.
3. The **goal** the profile serves (launch copy, outbound, social) — it changes what to extract.

Do not use generic platform exemplars as source material. If zero samples exist and no
documented default applies, deliver "no profile derivable — need sources", not a guess.

## Procedure

1. Gather 5 to 20 representative samples. Prefer recent material over old unless the user says
   the older writing is more canonical.
2. Separate "public launch voice" from "private working voice" if the source set clearly splits.
3. If live X access is available, pull recent original posts before drafting. Checked
   2026-07-28: no `x-api` skill is installed in `.claude/skills/` or `~/.claude/skills/`
   `[repro]` — so this step means an actual API call or an operator-supplied export, not a
   skill handoff. No access → work from the samples you have and say the X lane is uncovered.
4. Extract, per sample set:
   - rhythm and sentence length
   - compression vs explanation
   - capitalization norms
   - parenthetical use
   - question frequency and purpose
   - how sharply claims are made
   - how often numbers, mechanisms, or receipts show up
   - how transitions work
   - what the author never does
5. Write the profile using the exact schema in
   [references/voice-profile-schema.md](references/voice-profile-schema.md) — every source in
   the Source Set is a real path or URL that was actually read this session.
6. Render one short sample paragraph under the profile and run the Verification checks on it
   before declaring the profile usable.

## Output contract

Produce a reusable `VOICE PROFILE` block that downstream skills consume directly
(schema: `references/voice-profile-schema.md`). Keep it short enough to reuse in session
context. The point is operational reuse, not literary criticism.

### Affaan / ECC defaults

If the user wants Affaan / ECC voice and live sources are thin, start here unless newer source
material overrides it: direct, compressed, concrete · specifics, mechanisms, receipts, and
numbers beat adjectives · parentheticals qualify or narrow · capitalization is conventional ·
questions are rare and never bait · tone can be sharp, blunt, skeptical, or dry · transitions
feel earned.

# Verification

Every check can return "no". A check that errors is a dead gate, not a pass (bug-230) —
`grep` on a missing file exits 2, not 1; treat exit 2 as "re-run with a real path".

1. **Profile completeness** — the schema's required fields exist:

```bash
grep -cE '^(Author|Goal|Confidence):' voice-profile.txt
```

   **PASS:** prints `3`, exit 0. Fewer = incomplete profile, do not hand it downstream. `[repro]`

2. **Trope scan** — render one sample paragraph under the profile, then:

```bash
grep -nEi 'excited to share|no fluff|not [a-z]+, just|game.chang|cutting.edge|revolutionary|rapidly evolving' sample-draft.md
```

   **PASS:** exit 1 (zero matches). Exit 0 = a banned trope survived; rewrite the sample AND
   tighten the profile's "never does" list. `[repro]`

3. **Source reality** — every entry in the profile's Source Set resolves: repo paths via
   `ls <path>` (exit 0), URLs via `curl -sI <url> | head -1` (HTTP 200). **PASS:** all resolve.
   A source that cannot be opened gets deleted from the profile, not kept. `[repro]` / `[live]`

Prove check 2 can fail before trusting it: feed it one line containing "Excited to share",
confirm exit 0, restore (rule 3 of the authoring standard — done once, observed, in the worked
example below).

## Worked example

Real run, 2026-07-28, deriving the SkyyRose founder voice. Source read from the repo:
`docs/brand/collection-stories.md` (line 79: `"Hurts" is not a theme. It is the bloodline that
raised the founder.` `[repo]`). Two test drafts written to the session scratchpad:

```bash
$ grep -nEi 'excited to share|no fluff|not [a-z]+, just|game.chang|cutting.edge|revolutionary|rapidly evolving' draft-bad.md
1:Excited to share our new drop. No fluff, just heat.
$ echo $?
0        # RED — the gate catches the tropes, proving it can fail

$ grep -nEi 'excited to share|no fluff|not [a-z]+, just|game.chang|cutting.edge|revolutionary|rapidly evolving' draft-good.md
$ echo $?
1        # GREEN — zero matches on the rewritten draft
```

Both outputs observed this session `[repro]`. The good draft kept the canon line ("The Love
Hurts hoodie carries the bloodline story.") and dropped both tropes.

## Failure modes

| Failure | What it looks like | Rule |
|---|---|---|
| Profile from memory | "I know the founder's voice" with no sources read this session | Same defect shape as bug-096 (hallucinated brand canon): plausible ≠ sourced. Stop; read the canon docs |
| Mixed collection voices | "bloodline" language applied to Black Rose | Each collection has its own canon — `docs/brand/collection-stories.md` is the SOT; never substitute one collection's voice for another |
| Unfalsifiable sign-off | "matches the voice" with no check that could have said no | bug-287: tag the claim. "Trope scan exit 1 `[repro]`" is a verdict; "sounds right" is not |
| Dead gate read as pass | grep exits 2 (file missing), agent reports "clean" | bug-230 fail-open. Exit 1 is clean; exit 2 is a broken gate — fix the path and re-run |
| Repo-tracked fingerprints | personal voice profile committed without being asked | Persistence rule: save to the requested workspace/memory surface only; never repo-track personal voice data unasked |

### Hard bans — delete and rewrite on sight

fake curiosity hooks · "not X, just Y" · "no fluff" · forced lowercase · LinkedIn
thought-leader cadence · bait questions · "Excited to share" · generic founder-journey filler ·
corny parentheticals

## Persistence and downstream use

- Reuse the latest confirmed `VOICE PROFILE` across related tasks in the same session.
- Durable artifact requested → save in the requested workspace location or memory surface.
- This skill is the canonical voice source for `content-engine`, `crosspost`,
  `article-writing`, `marketing-campaign`, and outbound across X, LinkedIn, and email. If
  another skill has a partial voice-capture section, this skill's profile wins.
