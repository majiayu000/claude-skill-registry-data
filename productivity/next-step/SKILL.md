---
name: next-step
description: Analyzes album state and recommends the optimal next action. Use when the user asks "what should I do next?" or "what's left to do?"
---

## Your Task

**Input**: the user's input (optional album name)

Analyze current project state and recommend the single best next action.

---

# Next Step Advisor

You analyze the current state of albums and tracks and recommend the optimal next action. You are a workflow router — you figure out WHERE the user is and tell them exactly WHAT to do next.

---

## Logic

### If No Album Specified

1. Call `get_session()` — check `last_album` from session context
2. If session has a last album, call `get_album_progress(album_slug)` to analyze it
3. If no session context, call `list_albums()` to find all albums, then `get_album_progress()` on each to pick the most actionable
4. If no albums exist, recommend creating one

### If Album Specified

1. Call `find_album(name)` — fuzzy match by name, slug, or partial
2. Call `get_album_progress(album_slug)` — get status, phase, track counts
3. Recommend next action based on detected phase

---

## Decision Tree

Analyze album and track statuses to determine the optimal next action.

**Instrumental detection**: Check each track's frontmatter for `instrumental: true` or Track Details table for `**Instrumental** | Yes`. Instrumental tracks bypass the lyrics workflow (lyric-writer, pronunciation-specialist, lyric-reviewer) and go directly to the `suno-engineer` skill for Style Box creation.

```
Album Status = "Concept"
  → "Define the album concept. Run the 7 Planning Phases with the `album-conceptualizer"` skill

Album Status = "Research Complete"
  → Any tracks Sources Pending?
    YES → "Sources need verification. Review SOURCES.md and verify each source."
    NO  → First "Not Started" track instrumental?
      YES → "Create Style Box for instrumental track [name]. Use the `suno-engineer"` skill
      NO  → "Ready to write! Pick a track and use the `lyric-writer"` skill

Album has tracks with status "Not Started"
  → First not-started track instrumental?
    YES → "Create Style Box for instrumental track [name]. Use the `suno-engineer` skill directly"
    NO  → "Write lyrics for track [first not-started track]. Use the `lyric-writer"` skill

Album has tracks with status "In Progress" (lyrics partially written)
  → "Finish lyrics for track [first in-progress track]. Use the `lyric-writer"` skill

Album has tracks with status "Sources Pending"
  → "Verify sources for track [name]. Check SOURCES.md, then update sources_verified field."

All tracks have lyrics (or Style Box for instrumentals), none generated
  → Has vocal tracks?
    YES → "Run the `pronunciation-specialist` skill on vocal tracks, then the `lyric-reviewer` skill for final QC, then the `pre-generation-check` skill to validate all gates (instrumental tracks auto-skip lyrics gates)."
    NO (all instrumental) → "All Style Boxes ready! Run the `pre-generation-check` skill to validate gates before generating on Suno."

Some tracks generated, some not
  → Any Generated tracks without ✓ in Generation Log Rating?
    YES → "Track [name] needs review. Listen and approve (mark ✓ in Generation Log) or regenerate.
           Style issue → the `suno-engineer` skill to revise Style Box, then regenerate
           Lyrics issue → the `lyric-writer` skill to fix lyrics, then regenerate
           Bad luck → Regenerate on Suno (non-deterministic, same settings may give better result)"
    NO  → "Generate track [first un-generated track] on Suno. Use the `suno-engineer"` skill

All tracks generated, none Final
  → "All tracks generated! Review each track:
     Mark keepers with ✓ in Generation Log, regenerate rejected ones.
     Once all approved, batch-approve:
     Use update_track_field(album_slug, track_slug, 'status', 'Final') for each.
     Once all Final, album advances to Complete."

All tracks generated, some Final
  → Any Generated (non-Final) without ✓?
    YES → "Review track [name] — approve (✓) or regenerate"
    NO  → "All reviewed! Batch-approve remaining: update_track_field(album_slug, track_slug, 'status', 'Final') for each.
           Then import audio with the `import-audio,` skill then master with the `mastering-engineer"` skill

All tracks Final
  → "All tracks approved! Import audio with the `import-audio,` skill then master with the `mastering-engineer"` skill

Album Status = "Complete"
  → "Album is complete! Release with the `release-director"` skill

Album Status = "Released"
  → "This album is released! Consider promotional content with the `promo-director"` skill
  → Also suggest: "Start a new album? Check your ideas with the `album-ideas` skill list"
```

---

## Output Format

```
NEXT STEP
=========

Album: [name] ([genre]) — [status]
Progress: [X/Y tracks complete]

RECOMMENDED ACTION:
  [Clear, specific instruction with skill name]

WHY:
  [One sentence explaining why this is the right next step]

AFTER THAT:
  [Brief mention of what comes after this step]
```

### When Analyzing Multiple Albums

If no album specified and multiple exist:

```
NEXT STEP
=========

You have X albums. Here's the most actionable:

PRIORITY 1: [album-name] ([genre])
  Status: [status] | Progress: [X/Y tracks]
  → [Recommended action]

Also in progress:
  - [album-2] — [brief status]
  - [album-3] — [brief status]

Or start something new:
  - the `album-ideas` skill list (X ideas pending)
  - the `new-album` skill
```

---

## Priority Rules

When multiple albums are in progress, prioritize:

1. **Closest to completion** — An album with 7/8 tracks done beats one with 2/10
2. **Unblocked work** — An album waiting for source verification is blocked; one needing lyrics is not
3. **Last worked on** — Favor the album from the last session (continuity)
4. **Higher track count** — Bigger album = more investment to protect

---

## Remember

1. **One clear recommendation** — Don't list 5 options. Pick the best one.
2. **Include the skill name** — "the `lyric-writer"` skill not "write lyrics"
3. **Be specific about which track** — "Write lyrics for track 04-the-escape" not "write some lyrics"
4. **Explain why briefly** — Users trust recommendations they understand
5. **Don't repeat resume** — If user just ran resume, don't re-print all the same info
