---
name: enforcing-output-formats
description: >
  Enforces industry-standard formatting conventions for every output type,
  even when not explicitly requested. Activates on any request to produce
  a song, lyric sheet, script, screenplay, email, letter, memo, legal document,
  resume, recipe, chord chart, lead sheet, tablature, lesson plan, press release,
  invoice, brief, pitch deck outline, interview transcript, meeting minutes,
  style guide, or any other structured deliverable with a known professional
  format. Also triggers on: format this correctly, fix the formatting, proper
  format, industry standard, how should this look, lyric sheet, song structure,
  script format, screenplay format, business letter, cover letter, formal memo,
  legal brief, or any output where implicit format conventions exist.
version: "1.0.0"
---

# Enforcing Output Formats

Apply the correct industry-standard format for every output type — even when
the user doesn't ask for it. If a known format exists, use it. Never default
to markdown when the output type has its own convention.

---

## Decision Tree

```
What is being produced?
  ├─ Song / Lyrics ──────────────── Lyric sheet format (see SONGS)
  ├─ Script / Screenplay ────────── Industry script format (see SCRIPTS)
  ├─ Business document ──────────── Document format by subtype (see DOCUMENTS)
  ├─ Music notation reference ───── Lead sheet / chord chart (see MUSIC NOTATION)
  ├─ Legal / Formal ─────────────── Formal document format (see LEGAL/FORMAL)
  ├─ Communication ──────────────── Email / letter / memo format (see COMMS)
  └─ No known convention ────────── Use markdown with clear hierarchy
```

---

## SONGS — Lyric Sheet Format

### Required Elements
- **Header block** (top of page):
  ```
  TITLE
  Artist / Writer: [name]
  Key: [key]   Tempo: [BPM or feel descriptor]   Genre: [genre]
  ```
- **Section labels**: ALL CAPS, left-justified, in brackets. No `---` dividers.
  Valid labels: `[INTRO]`, `[VERSE 1]`, `[PRE-CHORUS]`, `[CHORUS]`,
  `[VERSE 2]`, `[BRIDGE]`, `[OUTRO]`, `[HOOK]`, `[REFRAIN]`, `[INTERLUDE]`
- **One blank line** between sections. No blank lines within a section.
- **Duet / multi-voice notation**: Speaker label as ALL CAPS prefix on the line,
  followed by colon. Underlayer / harmony gets `(under)` suffix.
  ```
  KYLE: You learned this from me
  KINSLEY (under): It ends with me
  BOTH: It ends with me
  ```
- **Stage/production directions**: Italicized in parentheses, on their own line.
  ```
  *(quiet, no production)*
  ```
- **Repeated sections**: Write `[CHORUS — repeat]` rather than rewriting the
  full chorus unless lyrics differ.
- **No markdown bold, no `---` dividers, no bullet points** anywhere in the lyric sheet.

### Section Order Convention
Standard pop/rock structure:
`INTRO → VERSE 1 → PRE-CHORUS → CHORUS → VERSE 2 → PRE-CHORUS → CHORUS → BRIDGE → FINAL CHORUS → OUTRO`

Do not insert a second PRE-CHORUS without a CHORUS between them.
Do not stack two BRIDGES.

### Example — Correct Lyric Sheet
```
IT ENDS WITH ME
Writer: Kyle Rosebrook
Key: Am   Tempo: Slow burn   Genre: Alt-folk / confessional

[INTRO]
*(low, no instrumentation)*
I said calm down.
You still hear it.
So do I.

[VERSE 1]
I said calm down
Glass sweating on the counter
Watching the game like the score mattered
Like you weren't in the room

[PRE-CHORUS]
You were six years old
Taking notes I didn't know I was leaving

[CHORUS]
You learned this from me
How to make yourself invisible
How to wait it out and call that
Handling it

[OUTRO]
KYLE: It ends with me
KINSLEY (under): It ends with me
BOTH: It ends with me
```

---

## SCRIPTS — Screenplay / Stage / Podcast

### Screenplay (Film/TV)
- Scene headings: `Loxihart. LOCATION — DAY` (all caps, no quotes)
- Action lines: present tense, flush left, double-spaced between blocks
- Character cues: centered, all caps, 3.5" from left
- Dialogue: centered block, under character cue
- Parentheticals: centered, under character cue, in parens — use sparingly
- Transitions: `CUT TO:` / `FADE TO:` — right-justified, all caps

### Podcast / Audio Script
- Header: Show name, episode number, title, runtime estimate
- Speaker labels: `[KYLE]` left-justified before each block
- Stage directions in `*italics*` on own line
- `[MUSIC: brief description]` for audio cues
- `[PAUSE 2s]` for intentional beats

---

## DOCUMENTS — Business / Professional

### Email
```
To: [recipient]
Subject: [subject line — specific, not vague]

[Body — no indented paragraphs, single line break between grafs]

[Name]
[Title / context if needed]
```

### Formal Letter / Cover Letter
```
[Full Name]
[Address]
[Date]

[Recipient Name]
[Title]
[Organization]
[Address]

Dear [Name]:

[Body — block format, no indentation, single space between grafs]

Sincerely,

[Signature block]
```

### Memo
```
MEMORANDUM

TO:      [recipient(s)]
FROM:    [sender]
DATE:    [date]
RE:      [subject — specific]

[Body — block paragraphs, no indentation]
```

### Press Release
```
FOR IMMEDIATE RELEASE
[or: EMBARGOED UNTIL [date]]

HEADLINE IN ALL CAPS OR TITLE CASE

Subhead in sentence case if needed.

[CITY, Date] — [Lead graf: who, what, when, where, why in first two sentences]

[Body grafs]

[Boilerplate: "About [Company]" graf]

###    [end mark — always three pound signs]

Contact:
[Name]
[Email]
[Phone]
```

---

## MUSIC NOTATION REFERENCE

### Lead Sheet
- Title, composer, key signature, time signature at top
- Chord symbols above melody line
- Lyrics below staff (or in lyric-only version: below chord symbols)
- Repeat signs and section markers follow standard notation

### Chord Chart (Nashville Number System)
```
TITLE — Key of [X]

[INTRO]  | 1 | 1 | 4 | 5 |

[VERSE]
| 1 | 1 | 4 | 4 |
| 1 | 1 | 5 | 5 |
```

### Tablature
- 6 lines, low E at bottom
- Fret numbers on strings, rhythm notation above when needed
- Open = 0, X = muted

---

## LEGAL / FORMAL

### Contract / Agreement
- Party definitions before operative clauses
- Defined terms capitalized throughout
- Numbered sections: 1.0, 1.1, 1.1.1
- Signature block at end: name, title, date, signature line

### Legal Brief (US)
- Caption (case name, court, docket) at top
- Statement of facts before argument
- Argument headers in ALL CAPS or bold
- Conclusion section required
- No contractions, no first person

---

## COMMS — Miscellaneous

### Meeting Minutes
```
[ORGANIZATION / PROJECT]
Meeting Minutes — [Date]
Attendees: [list]
Facilitator: [name]

AGENDA ITEMS
1. [Item] — [decision/outcome/owner]

ACTION ITEMS
- [Task] | Owner: [name] | Due: [date]

Next meeting: [date / TBD]
```

### Recipe
```
TITLE
Yield: [servings]   Prep: [time]   Cook: [time]

INGREDIENTS
[amount] [unit] [ingredient]
...

INSTRUCTIONS
1. [Step]
2. [Step]

NOTES
[Optional storage, substitutions, tips]
```

---

## Enforcement Rules

1. **Always apply the correct format** — do not default to markdown prose
   when a structured format exists.
2. **Never mix formats** — don't put `---` markdown dividers in a lyric sheet.
   Don't put lyric section labels in a business letter.
3. **If format is ambiguous** — state the assumed format at the top:
   `Formatting as: [format type]. Let me know if you need a different convention.`
4. **Partial outputs still use correct format** — if only writing one section
   of a larger document, still use the correct labels and structure for that section.
5. **Revisions inherit the original format** — if editing existing work, match
   the format already established, don't revert to markdown.

---

## Self-Verification Checklist

Before outputting any structured deliverable:
- [ ] Identified the output type
- [ ] Applied the correct format from this skill (not markdown defaults)
- [ ] No format-mixing (no `---` in lyric sheets, no bullets in scripts, etc.)
- [ ] Multi-voice / duet notation correct if applicable
- [ ] Section order follows the convention for the type
- [ ] Header block present if required by the format
- [ ] Stated format assumption if type was ambiguous

---

## CLAIMS
- [SOURCED] Lyric sheet conventions follow standard Nashville/publishing industry format
- [SOURCED] Screenplay format follows WGA/Final Draft industry standard
- [SOURCED] US business letter block format is standard professional convention
- [GENERATED] The section order rule (no double PRE-CHORUS without intervening CHORUS) is
  derived from standard song structure convention, not a written specification
- ! If Kyle uses a DAW or publisher that requires a different lyric format, this
  skill's lyric conventions should be updated to match

## GAPS
- Does not cover: tablature beyond basic structure, Nashville Number System edge cases,
  non-US legal formats, academic citation formats (MLA/APA/Chicago), medical records,
  technical specifications (RFC, API docs — those have their own skills)
- Multi-language lyric sheets (bilingual notation) not addressed
- Film vs. TV screenplay format differences not fully differentiated
