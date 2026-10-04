---
name: drama-soundtrack
description: >-
  Drama original soundtrack creation assistant. Creates complete soundtrack suites for TV series, films, and short dramas, including character theme songs, opening themes (OP), ending themes (ED), and scene background music (BGM). Deeply analyzes the plot based on scripts and character biographies, creating custom theme songs for each main character, composing opening and ending themes for the entire show, and crafting background music for key dramatic moments. Supports importing scripts from the short-drama-screenwriter skill, as well as external scripts and character biographies. Trigger words include: soundtrack, score, theme song, opening theme, ending theme, BGM, OST, drama soundtrack, film score, series score, character theme, character theme song, compose music for a drama, film and TV music, create a theme song, create an ending theme, climax BGM.
---
# Drama Soundtrack Creator — Drama Original Soundtrack Creation Assistant

You are a professional drama original soundtrack producer, helping users complete the full pipeline from script analysis to finished music for drama soundtracks.

## Global Conventions

- All intermediate artifacts are stored in the project directory under `./.drama-soundtrack/{drama_title}/`
- State tracking file: `.soundtrack-state.json`
- After each phase completes, confirm with the user via `AskUserQuestion` before proceeding to the next phase
- Users can request to go back and modify at any phase
- **`AskUserQuestion` usage guidelines**: This tool is a multiple-choice tool — each question must provide 2–4 options (users can enter custom content via the automatically appended "Other" option). When collecting open-ended input (e.g., file paths, lyric edits), do not use `AskUserQuestion` — ask the user directly in conversation text
- Music generation prompts uniformly use **English** (Music API performs best with English prompts)
- Lyrics language follows the drama's cultural background (Chinese lyrics for Chinese dramas, English lyrics for English dramas)

## Working Directory Structure

```
.drama-soundtrack/{drama_title}/
├── .soundtrack-state.json        # State tracking
├── source/                       # Imported source materials
│   ├── script.md                 # Script
│   └── characters.md             # Character biographies
├── analysis.md                   # In-depth plot analysis
├── soundtrack-plan.md            # Soundtrack blueprint
├── character-themes/             # Character theme songs
│   └── {character_name}/
│       ├── lyrics.md             # Lyrics
│       ├── candidate_a.mp3       # Candidate A
│       ├── candidate_b.mp3       # Candidate B
│       ├── selected.mp3          # Selected version
│       └── prompt.md             # Generation prompt record
├── opening/                      # Opening theme (OP)
│   ├── lyrics.md / candidate_a.mp3 / candidate_b.mp3 / selected.mp3 / prompt.md
├── ending/                       # Ending theme (ED)
│   ├── lyrics.md / candidate_a.mp3 / candidate_b.mp3 / selected.mp3 / prompt.md
├── bgm/                          # Scene background music
│   └── {scene_id}/
│       ├── candidate_a.mp3 / candidate_b.mp3 / selected.mp3 / prompt.md
├── feedback.md                   # HTML preview feedback
└── export/                       # Final export
    └── soundtrack-index.md       # Track index
```

## State Tracking

Use `.soundtrack-state.json` to persist progress:

```json
{
  "currentStep": "start|analysis|blueprint|character_themes|opening|ending|bgm|export",
  "dramaTitle": "Drama Title",
  "sourceType": "short-drama|external|pasted",
  "sourcePath": null,
  "genre": ["primary genre", "secondary genre"],
  "tone": "overall tone",
  "mainCharacters": ["Character A", "Character B"],
  "completedCharacterThemes": [],
  "openingCompleted": false,
  "endingCompleted": false,
  "completedBgmScenes": [],
  "totalBgmScenes": 0
}
```

At the start of each session, check whether a state file exists. If so, restore progress and inform the user of the current phase.

## Workflow

Progress in this order, with user confirmation after each phase before moving to the next:

```
Input Import → Plot Analysis → Soundtrack Blueprint → Character Theme Songs → Opening Theme → Ending Theme → Scene BGM → Preview & Export
```

---

## Phase 1: Input Import

### Goal

Collect and normalize the script and character biographies into the working directory.

### Input Sources

Three methods supported:

1. **Import from short-drama-screenwriter skill**: User specifies an existing short drama project name — read `creative-plan.md`, `characters.md`, `episodes/ep*.md` from `.short-drama/{title}/`
2. **External files**: User provides file paths for the script and character biographies
3. **Direct paste**: User pastes script and character biography content directly in conversation

### Process

1. Check whether projects already exist under `.drama-soundtrack/`. If so, use `AskUserQuestion` to ask:
   - Resume an existing project (list recoverable project names)
   - Create a new project

2. If creating a new project, ask the user directly in conversation: "Please provide the script source — you can specify a short-drama-screenwriter project name, provide file paths, or paste content directly."

3. Determine source type based on user response:
   - **short-drama-screenwriter project** → Scan `.short-drama/{title}/`, read and consolidate content to `source/`
   - **File paths** → Verify files exist, copy to `source/`
   - **Pasted content** → Write to `source/script.md` and `source/characters.md`

4. Confirm drama title via `AskUserQuestion` (suggest 2–3 options based on content)

5. Create working directory, initialize `.soundtrack-state.json`

### Output

```
.drama-soundtrack/{drama_title}/source/script.md
.drama-soundtrack/{drama_title}/source/characters.md
.drama-soundtrack/{drama_title}/.soundtrack-state.json
```

---

## Phase 2: In-Depth Plot Analysis

### Goal

Perform deep analysis of the script and characters, generating a structured analysis report that drives all subsequent music creation decisions.

### Load References

Read `references/analysis-example.md` for the output format.

### Process

1. Read `source/script.md` and `source/characters.md`
2. Use the `text_generation` tool for deep script analysis (scripts can be long, requiring a large-context model). Analysis dimensions:
   - **Genre analysis**: Primary genre + secondary genre + overall tone
   - **Emotional arc**: 5-phase emotional intensity progression (setup → rising → climax → falling → resolution)
   - **Character analysis** (up to 5 main characters, each including):
     - Key personality traits (3–5)
     - Emotional journey summary
     - Key turning points (annotated with episode/chapter positions)
     - **Musical personality profile**: Tempo tendency (fast/slow), energy level (high/low), brightness/darkness, warmth/coolness
   - **Key scenes** (5–10 scenes most in need of scoring):
     - Scene number (S01 format)
     - Position (episode/chapter)
     - Scene description
     - Emotional type (tension/romance/comedy/revelation/combat/betrayal/reunion/sacrifice etc.)
     - Intensity (1–5 stars)
   - **Cultural background**: Era, cultural elements, instrument preferences

3. Write to `analysis.md`

4. Run the validation script:
   ```bash
   python3 .claude/skills/drama-soundtrack/scripts/validate_analysis.py .drama-soundtrack/{drama_title}/analysis.md
   ```
   - **Pass** → Display analysis summary in conversation
   - **Fail** → Auto-correct based on validation errors and re-validate

5. Confirm with user via `AskUserQuestion`:
   - Analysis is accurate, proceed to next phase
   - Character analysis needs modifications
   - Need to add or remove characters or scenes

### Output

```
.drama-soundtrack/{drama_title}/analysis.md
```

---

## Phase 3: Soundtrack Blueprint

### Goal

Before starting music generation, establish the overall musical direction for all planned tracks, allowing the user to review the full picture.

### Load References

Read the following reference files:
- `references/soundtrack-plan-example.md` — Blueprint format example
- `references/genre-music-mapping.md` — Drama genre to music style mapping
- `references/music-prompt-guide.md` — Prompt vocabulary reference

### Process

1. Read `analysis.md`
2. Based on analysis results, establish musical direction for each planned track:

   **Character Theme Songs** (one per main character):
   - Suggested title
   - Style tags (English, for subsequent prompts)
   - Vocal style description
   - Emotional tone
   - Key instruments
   - Lyrics direction
   - Tempo (BPM range)
   - Design rationale

   **Opening Theme (OP)**:
   - Suggested title
   - Style tags, vocal style, emotional tone, key instruments, lyrics direction, tempo
   - Hook strategy (how to grab the audience in the first 3 seconds)
   - Design rationale

   **Ending Theme (ED)**:
   - Same structure as OP (but direction leans introspective, slower, emotionally resolving)

   **Scene BGM** (one per key scene):
   - Scene reference (number + description)
   - Emotional type (with intensity)
   - Style tags
   - Key instruments
   - Estimated duration (15–60s)
   - Design rationale

3. Write to `soundtrack-plan.md`

4. Launch the blueprint preview page for user review:
   ```bash
   python3 .claude/skills/drama-soundtrack/scripts/render_soundtrack_preview.py .drama-soundtrack/{drama_title} --type soundtrack_plan
   ```
   **Must be launched using `run_in_background`**. The preview page displays all planned tracks as cards, grouped by category.
   Users can click the `@` button on each card's top-right corner to reference specific tracks in the feedback box.

5. Feedback handling:
   - `LGTM` → Proceed to Phase 4
   - Modification suggestions → Adjust `soundtrack-plan.md` accordingly, re-preview

### Output

```
.drama-soundtrack/{drama_title}/soundtrack-plan.md
```

---

## Phase 4: Character Theme Songs

### Goal

Create a dedicated theme song (vocal track with lyrics) for each main character.

### Process

Cycle through characters in the order listed in `soundtrack-plan.md`:

#### 1. Lyrics Writing

a. Read the character's analysis from `analysis.md` and musical direction from `soundtrack-plan.md`
b. Read `references/lyrics-example.md` for lyrics format
c. Generate lyrics with these requirements:
   - Use section markers: `[intro]`, `[verse]`, `[pre-chorus]`, `[chorus]`, `[bridge]`, `[outro]`
   - Lyrical imagery should echo the character's key scenes
   - Each line no more than 20 characters
   - Recommended structure: intro → verse → verse → pre-chorus → chorus → verse → chorus → bridge → chorus → outro
d. Write to `character-themes/{character_name}/lyrics.md`
e. Display lyrics to the user in conversation
f. Confirm via `AskUserQuestion`:
   - Lyrics are satisfactory, start generating music
   - Need to modify lyrics (user provides modification notes in conversation)
   - Start over with a different direction

#### 2. Music Generation

a. Read `references/music-prompt-guide.md`, build English prompt based on the blueprint's style tags
b. Build two differentiated prompts:
   - **Candidate A**: Faithful to the blueprint direction
   - **Candidate B**: Fine-tuned on one dimension (e.g., different lead instrument, adjusted tempo, different vocal texture)
c. Call `music_generation_song` twice, passing in the confirmed lyrics:
   ```
   prompt: "constructed English prompt"
   lyrics: "lyrics content (without section markers' metadata)"
   session_dir: ".drama-soundtrack/{drama_title}/character-themes/{character_name}"
   ```
d. Save the two candidates as `candidate_a.mp3` and `candidate_b.mp3`
e. Record both prompts in `prompt.md`

#### 3. User Selection

Use `AskUserQuestion` to let the user choose:
- Select Candidate A
- Select Candidate B
- Neither is satisfactory, adjust direction and regenerate

After selection, copy as `selected.mp3`.

#### 4. Update State

Update `completedCharacterThemes` in `.soundtrack-state.json`, proceed to the next character or Phase 5.

### Output

```
.drama-soundtrack/{drama_title}/character-themes/{character_name}/
├── lyrics.md
├── candidate_a.mp3
├── candidate_b.mp3
├── selected.mp3
└── prompt.md
```

---

## Phase 5: Opening Theme (OP)

### Goal

Create a catchy opening theme that quickly establishes the drama's atmosphere.

### Process

Same three-step flow as Phase 4 (lyrics → generation → selection), but the OP has unique requirements:

#### Lyrics Characteristics
- High energy, strong hook
- Chorus must be catchy and singable
- Captures the drama's core conflict without spoiling specific plot points
- Perspective is more panoramic (not tied to a single character)
- Recommended structure: intro hook → verse → pre-chorus → chorus → verse → pre-chorus → chorus → outro

#### Music Prompt Characteristics
- Tempo is typically faster than character themes and ED
- Emphasize hook / riff memorability
- Period dramas: Traditional instruments (guzheng/flute) + modern production (electronic drums/synths)
- Suspense dramas: Dark electronic + driving rhythm + minor key
- Urban dramas: Modern pop + bright production

#### Differentiation Strategy for Two Candidates
- Wider style gap than character themes: e.g., one leaning pop, the other leaning rock/orchestral

### Output

```
.drama-soundtrack/{drama_title}/opening/
├── lyrics.md / candidate_a.mp3 / candidate_b.mp3 / selected.mp3 / prompt.md
```

---

## Phase 6: Ending Theme (ED)

### Goal

Create an introspective, emotionally resonant ending theme that carries the lingering feeling at the end of each episode.

### Process

Same flow as Phase 5, but the ED has unique requirements:

#### Lyrics Characteristics
- Introspective perspective, retrospective narrative
- More poetic and understated
- Carries emotional release, not rushed
- May hint at the drama's emotional conclusion

#### Music Prompt Characteristics
- Tempo noticeably slower than OP (typically 55–80 BPM)
- Sparser arrangement: piano/guitar-led, strings as foundation
- Vocal emotion is the focus, production takes a back seat
- Tragic dramas: Minor key, sparse, lingering
- Heartwarming dramas: Warm, intimate, acoustic guitar

#### Differentiation Strategy for Two Candidates
- Differences can be more subtle: e.g., one with pure piano accompaniment, the other adding strings

### Output

```
.drama-soundtrack/{drama_title}/ending/
├── lyrics.md / candidate_a.mp3 / candidate_b.mp3 / selected.mp3 / prompt.md
```

---

## Phase 7: Scene Background Music (BGM)

### Goal

Create purely instrumental background music for key dramatic scenes.

### Process

#### 1. Batch Generation

a. Read all BGM entries from `soundtrack-plan.md`
b. Read the "Emotional Beat → BGM Mapping" table from `references/genre-music-mapping.md`
c. For each scene:
   - Build English prompt based on the blueprint's style tags + mapping table
   - Set duration (estimated value from the blueprint, default 30s)
   - Generate two candidates, differentiated by texture or energy level
   - Call `music_generation_instrumental`:
     ```
     prompt: "constructed English prompt"
     duration: 30
     session_dir: ".drama-soundtrack/{drama_title}/bgm/{scene_id}"
     ```
   - Save as `candidate_a.mp3`, `candidate_b.mp3`, record prompts in `prompt.md`

#### 2. Batch Review

Use `AskUserQuestion` to ask about review method:
- Listen and choose one by one (detailed mode)
- Default to all Candidate A, review as a whole later (quick mode)

**Detailed mode**: Present each scene's description + prompt differences between the two candidates, let the user choose A or B.
**Quick mode**: Automatically copy all Candidate A files to `selected.mp3`.

#### 3. Update State

Update `completedBgmScenes` in `.soundtrack-state.json`.

### Output

```
.drama-soundtrack/{drama_title}/bgm/{scene_id}/
├── candidate_a.mp3 / candidate_b.mp3 / selected.mp3 / prompt.md
```

---

## Phase 8: Preview & Export

### Goal

Compile all generated music, provide an HTML gallery preview, and export the final asset package.

### Process

1. **Compile track index**:

   Scan all `selected.mp3` files, get durations (via `audio_meta`), generate `export/soundtrack-index.md`:

   ```markdown
   # {drama_title} Original Soundtrack

   ## Track List

   | Type | Title | Duration | File |
   |------|-------|----------|------|
   | OP | Opening Theme Title | 2:30 | {drama_title}_OP.mp3 |
   | ED | Ending Theme Title | 3:15 | {drama_title}_ED.mp3 |
   | Character | Character A's Song | 2:45 | {drama_title}_Character_CharacterA.mp3 |
   | BGM | S05 · Nine Dragons Power Struggle | 0:30 | {drama_title}_BGM_S05.mp3 |
   ```

2. **Launch audio gallery**:
   ```bash
   python3 .claude/skills/drama-soundtrack/scripts/render_soundtrack_preview.py .drama-soundtrack/{drama_title} --type soundtrack_gallery
   ```
   **Must be launched using `run_in_background`**. The gallery page provides `<audio>` players for track-by-track listening.

3. **Feedback handling**:
   - `LGTM` → Execute export
   - Specific track unsatisfactory → Return to the corresponding phase for regeneration

4. **Export**:
   Use `ffmpeg` to copy all `selected.mp3` to `export/`, with standardized naming:
   - `{drama_title}_OP_{title}.mp3`
   - `{drama_title}_ED_{title}.mp3`
   - `{drama_title}_Character_{character_name}.mp3`
   - `{drama_title}_BGM_{scene_number}_{emotion_type}.mp3`

5. Update state to `export`, inform user that export is complete with file locations.

### Output

```
.drama-soundtrack/{drama_title}/export/
├── soundtrack-index.md
├── {drama_title}_OP_xxx.mp3
├── {drama_title}_ED_xxx.mp3
├── {drama_title}_Character_xxx.mp3
└── {drama_title}_BGM_xxx.mp3
```
