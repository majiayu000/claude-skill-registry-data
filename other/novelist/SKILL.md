---
name: novelist
description: "Use when drafting, editing, or reviewing chapters of The Old Songs of Aevoria narrative fiction series. Loads the series' complete author voice guide (three registers, house rules, diction), character dialogue voices for all five Book One ensemble members, anaphoric tic prevention patterns, the series canon firewall, and chapter structure conventions. Also activates when the user asks to write fiction, check prose against voice guidelines, maintain cross-chapter consistency, enforce character voice boundaries, or do a consistency pass across multiple chapters. Proactively flag any deviations from established voice."
allowed-tools: Read Write Edit Grep Glob
argument-hint: [chapter-path|chapter-name|"check all"|paste-text]
---

# Novelist — The Old Songs of Aevoria

Target: **$ARGUMENTS**

Scope: chapter path → edit that chapter | chapter name (e.g. "Ch 14") → find and edit | "check all" → sweep all chapters for voice/conformance issues | paste text → review against voice

**Always reference these companion files when you need deeper guidance:**
- `Novels/Style_Sheet.md` — full author voice rules (binding, read before any drafting)
- `Novels/00 Series Outline/Files/Old_Songs_of_Aevoria_MASTER_REFERENCE.md` — series bible including character dialogue voices section 16, canon firewall section 8, lore alignment section 9

---

## 1. The Voice at a Glance

**One-line definition:** A Memory-Keeper's told legend — oral-mythic but intimate, looking back across ages, so every scene carries the ache of hindsight; warm in heart, spare in word, kinetic when blood is drawn.

**POV & tense:** First person, Elowen, past tense. Two Elowens in one voice (young-Elowen living the scene, elder-Elowen telling it). Never head-hop.

### Three Registers

1. **Narration** — clear, propulsive, told-tale rhythm. Moves the story. Carries the world in lived texture, never lore-dumps.
2. **Reflection** — lyrical, brief, faintly aphoristic, always elder-Elowen's hindsight. One or two sentences, rarely a paragraph. Used to close scenes.
3. **Action** — short verbs, motion, no metaphor mid-strike. Sentences shorten. Lyric drops entirely until the blood is still.

Never blend all three in one breath. Move between them; let the seams show as rhythm.

### House Rules (Sentence Level)

1. **Restraint is the default.** State grief plainly and stop. Trust white space. Understatement lands harder than melodrama.
2. **Motif as memory.** Recurrence is craft made literal — plant, echo, pay off.
3. **Earn the mythic through the personal.** Cosmology only ever arrives *felt*, through one person in one moment. No lore for its own sake.
4. **Wound first, world second.** Every scene presses on a character's wound.
5. **Concrete over abstract.** A name, a hand on bark, a wound that closes wrong — not "loss," "grief."
6. **Earnest, never cynical.** Honor, sacrifice, and love are real and they cost.
7. **Tragedy is permitted.** The joy means something only because loss is allowed to stay lost.

### Diction

- No anachronism, no modern idiom, no meta. Timeless-mythic register, not medieval-cosplay. No "thee/thou."
- No profanity — consistent with an elven Memory-Keeper's voice.
- Avoid purple: no piled adjectives, no three metaphors where one will do. Restraint *is* the elven beauty.
- Keep dialogue tags simple ("said"). Let voice, not adverbs, carry character.

### The Seam

The voice's key move: elder-Elowen's hindsight bleeding into a young scene. Aim for one such seam per chapter — the line where present-tense knowledge and past-tense feeling intersect.

Format: always **italicized** to distinguish from young-Elowen narration. Never a full paragraph. One or two sentences. Usually closes a scene or precipitates a register shift.

> *"I was young. I still believed a thing kept was a thing saved."*

**Violation alert:** If the seam is not italicized, that is a formatting violation. If the seam runs longer than 3 sentences, it is a register violation (prose has slipped into pure reflection and stopped telling the story).

---

## 2. Anaphoric Tic Prevention

**The tic:** Starting sentences with the same grammatical structure in rapid succession without deliberate purpose. The specific patterns to watch:

- "It was ___." / "It had been ___."
- "He had ___." / "She had ___."
- "There was ___." / "There were ___."
- "This was ___." / "That was ___."
- "And it ___." / "And she ___." / "And he ___."

**The rule:** If a paragraph has 3+ sentences starting with the same structure, the first may be deliberate but the rest are the tic. Rewrite for variety — shift to subject-verb-first, invert clauses, or merge sentences.

**Allowed exceptions** (deliberate rhetorical devices, not the tic):
- A triple anaphora for deliberate emphasis ("She had walked out of monsters untouched. She had walked out of the wild miles unscathed. She had walked out of the thing that had run Corwin through.") — only when the repetition *builds* meaning
- The "But that is the rest of the song" refrain — a deliberate chapter-closing device
- The "That's not right" type — a single natural contraction is fine

**The test:** Read the paragraph aloud. If the repeated rhythm feels unconscious rather than purposeful, rewrite.

---

## 3. Character Dialogue Voices

Each character speaks with a distinct register. The ensemble differentiates by **contraction use, sentence length, question-asking tendency, naming habit, and formality level.**

### Corwin — *Formal-archaic*

| Trait | Rule |
|---|---|
| Contractions | **None.** Always "I am," "I have," "I do not," "it does not," "you are," "there is," "I was not" |
| Sentence length | Bimodal — very short answers or very long speeches |
| Patterns | Anaphoric lists, categorical pronouncements, parallelism across clauses |
| Anti-patterns | No "all right," "don't worry about it," "forget I said anything," "I heal fast" |

**Do NOT write:** "I'm looking for fragments. I've been looking a long time. It doesn't mean anything."
**Write:** "I am looking for fragments. I have been looking a long time. It signifies nothing."

### Brannoc — *Colloquial-storyteller*

| Trait | Rule |
|---|---|
| Contractions | Frequent and natural ("you've," "I'll," "it's," "don't") |
| Sentence length | Medium-long, accumulative. Most talkative character |
| Patterns | Calls people "elf"/"human" (never names); drops subjects ("Heard it before"); mini-stories; punchy declarations; dwarven exclamations |
| Anti-patterns | No formal archaisms, no philosophical chains |

**Write:** "Your elf's got a voice that does things."

### Wren — *Warm-declarative*

| Trait | Rule |
|---|---|
| Contractions | Appropriate for warmth ("I'll," "you're," "I'm," "that's") |
| Sentence length | Short to medium. Direct declarative sentences |
| Patterns | Names people directly; triadic warmth repetition ("I'm sorry about... I'm sorry about..."); affirms ("I like it," "that's what matters"); fragments ("Packed. Ready.") |
| Anti-patterns | Do NOT write Wren asking one-word questions — that is Elowen's signature |

### Elowen (spoken dialogue) — *Interrogative-echo*

| Trait | Rule |
|---|---|
| Contractions | Moderate ("don't," "I'm," "you've") |
| Sentence length | Very short. Fragments and one-word questions |
| Patterns | One-word questions ("Why." x4, "Where." "What."); echoes speakers back ("Before it broke."); interrogative mode (most lines are questions); rarely names conversation partner |
| Anti-patterns | Her spoken voice must be simpler than her internal narration. Must not match internal voice's lyricism |

**Elowen asks:** "Why." / "Where is it." / "How do you know that."
**Elowen echoes:** "Before it broke." / "And the Quiet is the aberration."

### Maelis — *Laconic-ritual*

| Trait | Rule |
|---|---|
| Contractions | Mixed — uses "you're"/"I'm" casually but full forms ("does not") for important statements |
| Sentence length | Very short. 5-12 words typical |
| Patterns | Ultra-laconic; practical justification in threes; full negatives for gravity; repetition for emphasis |
| Anti-patterns | No long explanations, no casual dismissals, no philosophical chains |

**Do NOT write:** "I'm not sure that's a good idea because we haven't scouted the area yet and we don't know what's out there."
**Write:** "I do not like it. We have not scouted. That is reason enough."

### Register Boundary Rules

1. **Corwin never uses contractions** — not even in emotion. Weight and cadence carry intensity, not informality.
2. **Elowen's spoken dialogue is simpler than her narration.** They must not match.
3. **Brannoc's dropped subjects and type-naming are his alone.**
4. **Wren's triadic warmth repetition is hers alone.**
5. **Maelis's full negatives in important statements** distinguish him from Brannoc and Wren.

---

## 4. Canon Firewall

The series draws **only** on native Aevoria pantheon and cultures:

| Allowed | Excluded entirely |
|---|---|
| Radiant Queen, Stonefather, Verdant Mother, Flame-Mother, Ash-Father | Aeor, the Calamity, Exandria, dimensional rift |
| Spoken-memory, resonance/geomancy, tide/storm, fire-shaping | Aeorian Echo, Eclipse Day, cascade, Heart of Winter, White Maw |
| Nullwood, Tharundor, sunken/coastal peoples, Emberlands | Any current campaign-era NPC, location, organization (including Northwatch Wardens) |
| Novel-specific geography (Thistlebrook, Karrendeep, Greymarch, Haldren's Ford) | The Aeorian ruins, Salsvault |

### Subtle / Edge-Case Violations

Some violations hide behind description instead of proper names. Flag these:

| Description that sounds safe | What it actually references | Why excluded |
|---|---|---|
| "the flying city" | Aeor | Exandrian geography |
| "the day the sky split open" | Eclipse Day | Exandrian event |
| "that war of gods" | The Calamity | Exandrian event |
| "the icy heart beneath the glacier" | Heart of Winter | Exandrian location |
| "the guild of monster-hunters in the north" | Northwatch Wardens | Campaign-era organization |
| "the rift in the sky" | The Echo / dimensional rift | Exandrian phenomenon |
| "the white beast that sleeps in winter" | White Maw | Exandrian entity |
| "the inn at the crossroads" | Waystone Inn | Campaign-era location |
| "the inn at Four Corners" / "the old stone inn" / "the wayfarer's rest" (if intended to be Waystone Inn) | Waystone Inn | Campaign-era location |

### Violation Severity

- **Hard violation:** Proper name directly used (Aeor, Eclipse Day, etc.). Must be replaced before the chapter can ship.
- **Soft violation:** Descriptive reference to an excluded element (see table above). Must be flagged and replaced.
- **Edge case:** A name that coincidentally overlaps but has different in-world referent (e.g. if a novel inn is called "the Stone's Rest" — that's fine, it's novel-specific geography). When in doubt, flag and ask.

If a passage references an excluded element (hard or soft), flag it and suggest the native replacement. Do not edit without approval.

---

## 5. Chapter Structure

Every chapter file must have YAML frontmatter:
```yaml
---
series: "The Old Songs of Aevoria"
title: "The Chapter Title"
label: "Chapter One"  # or "Interlude"
sort_order: 1  # numeric, 9.5 for interlude
part: 1  # 1, 2, or 3
type: chapter  # or "interlude"
---
```

Formatting conventions:
- Chapter headings: `### Chapter One — The Title`
- Scene breaks: `---` (three dashes) on its own line
- Chapter-end marker: `*[End of Chapter One. Continues — Chapter Two: The Next Title.]*`
- End of Part: `*[End of Chapter Twenty-Two — End of Part Two.]*`

---

## 6. Verification Checklist

Before claiming a chapter is done, verify:

- [ ] **Voice:** No anaphoric tic (3+ same-structure sentence starts in any paragraph). Scan for "It was"/"He had"/"She had"/"There was" chains.
- [ ] **Character voices:** Corwin uses zero contractions. Elowen's speech is simpler than her narration. No character could swap lines with another without sounding wrong.
- [ ] **Canon:** No excluded pantheon/geography/events. Only native Aevoria references.
- [ ] **Frontmatter:** YAML present with all required fields.
- [ ] **Formatting:** Scene breaks use `---`. Chapter-end markers present. No stray markdown.
- [ ] **Restraint:** No purple prose, no piled adjectives, no modern idiom, no profanity.
- [ ] **The seam:** At least one elder-Elowen hindsight line, **italicized**, bleeding into a young scene. Not more than 3 sentences. Not a full paragraph of reflection.

For "check all": spawn one subagent per chapter, each running the full checklist. Aggregate results.

Invoke `skill-self-review novelist` at completion.
