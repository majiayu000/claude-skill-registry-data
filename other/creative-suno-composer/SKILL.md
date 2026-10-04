---
name: creative-suno-composer
description: Create, iterate, or review Suno songs and multi-style albums; turn a concept into copy-ready style/lyric prompts, compare generated audio, and learn from the user's catalog. Use when the user says "Suno prompt", "make a song about X", "design an album", or "review these Suno tracks". NOT for archiving/downloading finished songs (use creative-suno-archive) or publishing them (use creative-youtube-channel).
vault_sync: true
---

# Suno Composer

Create music that carries the user's idea and taste. The working principle is
**minimum sufficient control**: specify what must survive the generation, and
leave the rest open enough for Suno to surprise us.

## Route the request

- **Single song** — develop a brief, lyrics, style prompt, and audition plan.
- **Album / EP** — design the album identity and arc, then develop anchor tracks
  before filling the sequence.
- **Review existing generations** — inspect the exact prompt, lyrics, and audio;
  compare versions and extract reusable lessons.
- **Style or lyric revision only** — preserve the other half unless the user
  asks to reopen it.

By default, deliver copy-ready material. Using Suno itself can consume credits;
generate, extend, remaster, publish, or train a model only when the user has
explicitly asked for that external action.

## Creative stance

1. **Album cohesion does not mean one genre.** Never impose a fixed genre, BPM
   range, language, vocal type, or maximum number of styles. A multi-style album
   can cohere through its thesis, narrative arc, recurring image, rhythmic
   gesture, vocal perspective, production space, transition, or opening/closing
   mirror.
2. **Prompt length follows the control problem.** A familiar pop brief may need
   one compact line. A through-composed, meditative, functional, or unusually
   staged track may need precise dynamic instructions. Remove decorative
   adjectives, not load-bearing direction.
3. **The audio is the result.** A generation is not successful because it
   followed the words on paper. Judge the recording: melody, diction, groove,
   dynamics, emotional truth, and its role in the album.
4. **Taste stays human-owned.** When several versions work, surface the tradeoff
   and let the user's felt response decide. Plays and likes are weak supporting
   signals, never the verdict.
5. **Preserve the strange good part.** Revise around a surprising melody, vocal
   crack, cadence, or production turn that gives a version life; do not polish
   it away merely to satisfy a checklist.

## Build the brief

Before writing, capture only the decisions that materially change the song:

- listener job: what should this song let someone feel, do, remember, or move to?
- source tension or scene: the concrete thing the song keeps returning to;
- point of view and language choice;
- structural mode;
- must-keep words, images, facts, melody, or functional constraints;
- choices intentionally left open to Suno.

Choose a structural mode to fit the song rather than forcing every idea into
verse–pre-chorus–chorus:

- **hook-led** — repetition and melodic recall carry the song;
- **scene-led** — objects, actions, and changes in place carry the emotion;
- **through-composed / movement-led** — development replaces a repeated chorus;
- **meditative / spacious** — silence, drone, recurrence, and restrained change
  are part of the form;
- **functional** — dance cues, warm-up progression, timing, or other real-world
  use is the primary success condition;
- **spoken, bilingual, or hybrid** — code-switching and speech have an emotional
  or dramatic reason, not novelty value.

These are starting shapes, not a closed menu.

## Write the Suno inputs

### Style field

Describe the few sonic relationships that matter. Useful ingredients include:

1. style, era, or hybrid identity;
2. motion or energy curve;
3. the instruments or textures doing the work;
4. vocal delivery and distance;
5. production space or transition;
6. a small number of exclusions only when Suno repeatedly adds the wrong thing.

Compact example:

```text
City pop, 95 BPM; groovy bass, bright synths and snappy drums; intimate
talk-sung vocal; confident, warm, forward-moving.
```

Precise example:

```text
Meditative folk moving through five restrained lifts rather than a pop chorus.
Fingerpicked nylon guitar begins alone; a low drone enters on lift two and one
frame-drum strike marks lift five. Close, clear vocal; the intensity becomes
quieter as the pitch rises. End in unaccompanied room tone, without a climax.
```

Do not turn these examples into defaults. In particular, the catalog already
uses ambient, folk, pop, rock, trip-hop, industrial, jazz, dance, devotional,
spoken, and hybrid forms. Reach beyond recurring `warm / intimate / ambient /
close-mic` language when the concept asks for another world.

### Lyrics field

**Every section tag gets a `(production direction)` line immediately after it.**
This is the standing format for this catalog — do not drop it for brevity. The
direction describes what the arrangement does in that section: instruments,
energy, dynamics, vocal distance, space. Concise but pictorial; one line, in
parentheses, before the first lyric line of the section.

```text
[Verse 1]
(mid-tempo groove with piano lead, crisp drums, shimmering guitars)
Lyrics here...

[Chorus]
(full band lift; pounding drums, handclaps, stacked vocals)
Hook line here...

[Bridge]
(everything drops to voice and bass; half-time feel; room tone audible)
...
```

Sections with different energy must read differently in their direction line —
two choruses that should not be copies get two different directions. The Styles
field describes the song's overall sonic relationships; the per-section
directions carry the arc.

These directions are **steering hints, not guaranteed control syntax**. Suno may
reinterpret a label or sing a parenthetical note, so keep each line short and
free of anything that would be wrong if sung. Verify the audio.

For model-specific capabilities or syntax, verify the current official Suno
documentation first. Do not present the old v4.5 guidance as current; the
catalog already contains v5 and v5.5 generations.

## Lyric review

Review aloud and in the generated recording.

- **Natural order:** would a person say it this way without the melody?
- **Breath unit:** can the singer carry the line without cramming or an awkward
  pause? Chinese 7–10 characters and English 6–10 syllables are useful starting
  ranges, not rules; long or short lines are valid when the phrasing earns them.
- **Scene before aphorism:** a maxim is strongest when the song has first made
  it concrete. The catalog's producer reviews repeatedly found that a line
  reaching for a conclusion can break the lived-in register.
- **Rhyme serves delivery:** do not demand 90% one-rhyme consistency. Use rhyme,
  slant rhyme, consonance, or deliberate non-rhyme according to the voice and
  genre.
- **Hook function:** the hook may be a title, action, sound, image, spoken cue,
  melodic phrase, or returning production gesture; it need not be a conventional
  chorus.
- **Bilingual phrasing:** switch language where thought, character, rhythm, or
  intimacy changes. Remove translations that merely duplicate the previous line.
- **Meaning fidelity:** protect source facts and the user's intended emotional
  boundary. For public work based on private material, deliberately choose
  direct detail, abstraction, or fictionalization rather than leaking specifics
  by accident.

When revising, name the exact problem and change only enough to solve it. One or
two targeted passes are usually more useful than rewriting the whole song.

## Audition generations

If exploration is wanted, generate meaningfully different candidates rather
than repeated clones. A useful starting set is:

- **A — concept-faithful:** preserves the brief with the least intervention;
- **B — stronger musical proposition:** makes the hook, melody, groove, or
  dynamic turn more decisive;
- **C — unexpected but faithful:** changes the sonic world or form while keeping
  the core tension intact.

Two strong candidates may be enough; add a third only when it tests a real
hypothesis. On later rounds, vary one load-bearing dimension at a time so the
result teaches us something.

Listen once without reading, then once with lyrics and prompt visible. For each
candidate record:

- immediate emotional and bodily response;
- the moment remembered after one listen;
- vocal identity and intelligibility;
- groove, tempo feel, and arrangement arc;
- strongest accident worth protecting;
- one failure that actually matters;
- album role and contrast with neighboring tracks;
- decision: keep, revise, repurpose, or reject — with a reason.

For functional music, measure the condition that matters. A dance or warm-up
track needs actual BPM, cue clarity, safe progression, and usable duration; a
meditation track needs real silence/space and loop behavior. A number written in
the prompt is not verification.

## Design a multi-style album

Write a short album bible before drafting every track:

- one-sentence thesis and listener journey;
- opening state, turning point, and closing state;
- two to four cohesion axes chosen for this album;
- recurring images, phrases, sounds, or transitions;
- deliberate contrast plan: where genre, language, tempo, density, or voice
  changes and why;
- no-go list specific to this album;
- track roles and running order;
- two or three anchor tracks to audition first.

Good cohesion axes include concept, narrative, place, season, character,
language progression, recurring field recording, shared harmonic color,
production texture, vocal point of view, dynamic contour, or an opener/closer
callback. Genre is only one possible axis.

Audition the anchor tracks before completing the rest. One should establish the
album's thesis, one should test its widest contrast, and one should reveal the
ending register. Let their audio results recalibrate later briefs. Sequence for
emotional causality and useful contrast, not a mechanical slow-to-fast curve.

## Per-song loop

Album work runs one song at a time, each song in its own note, every note
through the same two gates. This replaced "write the whole bible, then draft
every track" on 2026-09-06, after a 2,500-word spec turned composing into
compliance and the feeling of the early albums went missing.

**The album note is short.** Under ~300 words: a `## 核心句` in the user's own
words (the album has not started until the user has written it), a `## 曲目`
table linking each song note, a `## 整體形狀` of a few lines, and a `## 進度`
checkbox list. A long spec or "creative bible" is an attachment
(`_<album>-製作規格.md`), never the starting point. Model:
`{vault}/70_Media/Music/不识/album.md`.

**One note per song, one song at a time.** Do not pre-write every note. Open
the next song only when the current one has reached `generated`.

**Song note sections**, in this order: `場景` (one sentence) · `Hook` (the line
that cannot be lost) · `歌詞` (every section tag with its production-direction
line) · `Suno 欄位` (Title / Styles / Exclude / sliders, plus a short sound
direction) · `文字檢查` · `生成記錄` · `聽感`. Frontmatter carries `status` and
the catalog fields `suno_url`, `suno_song_id`, `suno_model`, `suno_created`.

**Status — exactly these five, never a new one:**
`draft` → `text-checked` → `generated` → `selected` | `revise` | `shelved`.
`revise` returns the note to `draft`.

**CHECK, before generating.** Run the Lyric review list above (natural order,
breath unit, scene before aphorism, rhyme serves delivery, hook function,
bilingual phrasing, meaning fidelity) plus the album's own no-go list. Write
the result into `## 文字檢查`: one line per item — pass, or what changed — and
the single line most likely to read as false or AI-written, with its fix. A
note without this section is not generated. Status → `text-checked`.

**GENERATE.** One song, one submission: candidate A, concept-faithful. B and C
are generated only after A has been heard and there is a specific hypothesis
to test. Immediately write each clip's URL, id, model and creation time into
`## 生成記錄`. Status → `generated`. Then stop — listening belongs to the user.

**LISTEN, the user's.** Record the user's verdict in `## 聽感` with the
audition fields above; keep / revise / repurpose / reject sets the status.

**Suno through the browser.** The lyrics field is a contenteditable div, not a
textarea. Streaming ~2,500 characters as keystrokes froze the renderer for over
a minute (measured 2026-09-06); one `execCommand('insertText')` call inserts
the text but drops every line break; `insertParagraph` between lines does
nothing. What works (verified 2026-09-06): the editor is Lexical, and a
synthetic paste keeps every line break —
`ed.focus(); const dt = new DataTransfer(); dt.setData('text/plain', text);`
`ed.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}))`
on `div.lyrics-editor-content[contenteditable]`. Clear first with a real
`ctrl+a` + `Delete` keystroke. Styles / Exclude / Title are plain inputs
(`form_input` works); the sliders are `role=slider` elements. The create
form is a server-side draft shared across tabs, so a half-filled form in a
frozen tab reappears in the next one — check the fields before submitting.
Read the song page (`/song/<id>`) after generation: it shows the exact
lyrics, styles, excludes, model and creation time to copy into the note.

## Learn from an existing catalog

When asked to analyze finished work, use the archived evidence instead of
memory. Start with `{vault}/70_Media/Music/_suno-index.json`, album notes,
per-track notes, exact audio, and download/copyright manifests.

Separate three evidence levels:

- **observed:** exact prompt, lyric, audio, model, duration, generation ID, date;
- **selected:** the user's explicit choice, producer verdict, published version,
  or documented rejection reason;
- **inferred:** a pattern across works. Label it as an inference and do not turn
  a single success into a universal rule.

Compare matched pairs when possible: two prompts for one song, a remaster and
original, two vocal versions, or two tracks with the same function. Extract the
smallest lesson that explains the audible difference. Update this skill only
for repeated patterns or explicit standing preferences; keep one-album choices
inside that album's bible.

Current catalog priors to preserve:

- multi-style and multilingual albums are intentional, not drift;
- strong albums often establish a concept, arc, no-go list, and anchor tracks
  before polishing individual songs;
- effective prompts range from compact genre sketches to detailed production
  maps; specificity matters more than brevity;
- hooks, spoken cues, movements, silence, and production motifs can replace a
  literal chorus;
- short conversational lines are common, but strict line-length and rhyme rules
  would erase successful exceptions;
- `warm / intimate / ambient / guitar / piano / reverb` form a recurring home
  palette. Treat it as a signature available to use, not the automatic answer.

## Deliverables

For a single song, normally return:

```text
Title
Core brief
Style
Lyrics
Candidate variation to test (if useful)
What to listen for
```

For an album, normally return:

```text
Album thesis and arc
Cohesion axes
Contrast plan
Track roles / running order
Anchor tracks
No-go list
Per-track briefs and prompts as they are developed
```

When saving a selected generation, preserve the exact Style and Lyrics payloads,
model/version, song ID and URL, creation time, audio path, candidate label,
selection/rejection reason, and any measured functional properties. Keep prompt
intent separate from measured audio fact.

## References

- Catalog index: `{vault}/70_Media/Music/_suno-index.json`
- Style vocabulary (legacy v4.5 reference; vocabulary only, not constraints):
  `{vault}/30_Resources/Technology/Suno AI 曲风参考.md`
- Earlier healing-album workflow (historical evidence, not a universal recipe):
  `{vault}/30_Resources/Technology/洞察疗愈专辑制作经验.md`
- Useful album examples:
  - `{vault}/70_Media/Music/further-assessment/further-assessment.md`
  - `{vault}/70_Media/Music/不识/album.md`
  - `{vault}/10_Projects/YouTube-Music-Channel/songs/temporary-residence-album/_临时居所-Album.md`
  - `{vault}/10_Projects/YouTube-Music-Channel/songs/warwick-album/_Twelve-Moons-Album.md`
  - `{vault}/10_Projects/YouTube-Music-Channel/songs/zero-bias-album/_零偏置-Album.md`
- Current official model reference: `https://help.suno.com/en/articles/11362305`
- Official prompt-in-Lyrics guidance: `https://help.suno.com/en/articles/5782977`
