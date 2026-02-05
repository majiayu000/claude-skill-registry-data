---
name: video-to-article
description: Use this skill when the user wants to convert a lecture, presentation, or talk video into text formats (transcript, outline, or article). Trigger when user mentions processing video recordings, creating transcripts from lectures, or generating articles from recorded presentations.
allowed-tools: Bash, Read, Write, AskUserQuestion, Glob
---

# Video to Article Conversion Workflow

This skill automates the conversion of lecture/presentation videos into various text formats including transcripts, outlines, and article drafts.

## Workflow Overview

1. **Setup Folder** - Create properly named folder if needed
2. **Validate Input Metadata** - Check for README.md with required frontmatter
3. **Extract Audio** - Convert video to MP3 using ffmpeg
4. **Transcribe** - Generate text transcript using ElevenLabs API
5. **Process Text** - Create progressive text refinements

## Step 0: Folder Setup (if starting from scratch)

If user is starting a new talk/lecture conversion and no folder exists yet:

Create folder using format: `YYYY Title of Talk`

After creating folder, navigate into it and proceed with workflow.

## Step 1: Validate Metadata

Look for `README.md` in the current directory with these frontmatter fields:

- `title` - Lecture/presentation title
- `speaker` - Speaker name
- `date` - Presentation date (YYYY-MM-DD)
- `lang` - Presentation language (e.g., "english", "czech", "spanish")
- `abstract` - Brief description
- `slides` - Link to slides (or file path)
- `video` - Optional: link to video

### If README.md is Missing or Incomplete

Use the AskUserQuestion tool to collect missing information:

```
- What is the lecture title?
- Who is the speaker?
- What date was this presented?
- What language is the presentation in?
- Brief description or abstract?
- Link to slides or presentation file?
```

Create or update README.md with collected information.

## Step 2: Find or Download Video File

### Check for Local Video

Look for video file in current directory:

- Common patterns: `*.mp4`, `*.mov`, `*.avi`, `*.mkv`
- If multiple found, ask user which to process

### If No Local Video Found

Ask user if they have a YouTube URL using AskUserQuestion tool:

- "Do you have a YouTube URL for this talk?"
- If yes, collect the YouTube URL
- If no, ask for local video file path

### Download from YouTube (if URL provided)

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/video-to-article/scripts/download-youtube.sh <youtube-url>
```

This downloads the video as `video.mp4` in medium quality (720p max).

**Requirements**: User needs yt-dlp installed. If missing, show:

```
Install yt-dlp:
- pip install yt-dlp
- brew install yt-dlp (macOS)
- sudo apt install yt-dlp (Ubuntu/Debian)
```

## Step 3: Extract Audio

Check if `audio.mp3` already exists. If not:

Run the extract-audio.sh script using the plugin root variable:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/video-to-article/scripts/extract-audio.sh <video-file>
```

This creates `audio.mp3` in the current directory.

## Step 4: Transcribe Audio

Check if `generated-transcript.txt` already exists. If not:

### Map Language to ISO Code

Convert the `lang` field from README.md to the appropriate ISO 639-1 language code for ElevenLabs API. Use your knowledge of language codes to map language names to their two-letter codes (e.g., "english" → "en", "czech" → "cs", "spanish" → "es").

### Run Transcription

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/video-to-article/scripts/transcribe-audio.sh <language-code>
```

## Step 5: Generate Text Outputs

### Execution Protocol

Before generating content, complete these steps in order:

1. **List all required outputs** - Read and acknowledge the complete list below
2. **Check which files already exist** - Use file existence checks for each output
3. **Read all existing source files** - Load transcript, outline, key-ideas as context
4. **Confirm which outputs need generation** - Explicitly state which files are missing
5. **Only then begin generation** - Generate missing files one by one

### Required Outputs

Generate all of these files:

1. `generated-transcript-cleaned.md` - Cleaned transcript
2. `generated-transcript-readable.md` - Readable transcript
3. `generated-transcript-outline.md` - Content outline
4. `generated-key-ideas.md` - Key takeaways
5. `generated-article-formal.md` - Explanatory blog post (long-form, narrative)
6. `generated-article-direct.md` - Scannable technical brief (concise, bullets)

**Note:** Outputs 5 and 6 are two different article variants with distinct styles and audiences. Generate both.

**Workflow:**

- Check file existence for all files above
- Automatically generate any missing files without asking user
- Skip files that already exist (inform user which were skipped)
- Don't declare completion unless all files exist
- Don't ask user if they want to generate missing files - just generate them
- Generate both article variants (formal and direct) - they serve different purposes

### Idempotent Generation Strategy

This process is idempotent - running the skill multiple times will only generate missing files, never overwrite existing ones:

1. **Check each output file before generating** - Use file existence checks
2. **Skip files that already exist** - Inform user which files are being skipped
3. **Generate only missing files** - Don't overwrite existing content
4. **Use existing files as context** - When generating later outputs (like key-ideas), read all available previous outputs for context

Example: If only `generated-key-ideas.md` is missing:

- Read existing: `generated-transcript-cleaned.md`, `generated-transcript-readable.md`, `generated-transcript-outline.md`
- Generate: `generated-key-ideas.md` using the existing files as context
- Skip: All other outputs

This allows users to:

- Resume interrupted workflows
- Generate only specific missing outputs
- Re-run safely without data loss

### Output 1: Cleaned Transcript

**File:** `generated-transcript-cleaned.md`
**Input:** `generated-transcript.txt`
**Check:** Skip if file exists

Convert the transcript into a more readable form by dividing it into paragraphs and adding headings.

**Instructions:**

- Do not change the content, except for obvious typos
- Do not change the tone of voice - if the speaker uses informal language, keep it
- Remove filler words like "Eh", "Ehm", "Um", "Uh"
- Remove comments related to the transcription itself, or rewrite them elegantly if possible (e.g., "(laughter)" or "(2 second pause)")
- Respond in {lang} language - maintain the same language as the original transcript

The cleaned transcript should preserve the speaker's authentic voice while being easier to read and follow.

### Output 2: Readable Transcript

**File:** `generated-transcript-readable.md`
**Inputs:** `generated-transcript.txt` and `generated-transcript-cleaned.md`
**Check:** Skip if file exists

You have two inputs:

1. The first text contains the direct transcript of a lecture
2. The second text contains a better structured version of this transcript

The slides are available here: {slides}

Create a more readable text from this transcript:

**Instructions:**

- Preserve the style, but optimize for reading comprehension
- Fix typos, repetitions, and improve stylistic clarity
- Shorten where it doesn't affect the message
- Make it flow naturally for readers while keeping the speaker's voice
- Respond in {lang} language - the output must be in the same language as the input

The goal is to make the content accessible to readers while maintaining the essence of the spoken presentation.

### Output 3: Outline

**File:** `generated-transcript-outline.md`
**Inputs:** Cleaned and readable transcripts
**Check:** Skip if file exists

From the provided transcript inputs, create an outline of what was discussed.

**Instructions:**

- List the main ideas and messages with very brief content
- Use bullet points for clarity
- Focus on key takeaways and core concepts
- Keep descriptions concise - just enough to understand the point
- Respond in {lang} language - the outline must be in the same language as the source material

This outline should serve as a quick reference guide to the presentation's structure and main points.

### Output 4: Key Ideas

**File:** `generated-key-ideas.md`
**Inputs:** Cleaned and readable transcripts (or all available generated files if running incrementally)
**Check:** Skip if file exists

From the provided transcript inputs, extract the key ideas, tips, and main concepts.

**Instructions:**

- Focus on interesting insights, actionable tips, and core concepts
- Unlike the outline, don't follow chronological order - prioritize importance
- Exclude generic or procedural content
- Each idea should have a brief description explaining why it matters
- Use bullet points or numbered list
- Respond in {lang} language - the output must be in the same language as the source material

This should capture the most valuable takeaways someone would want to remember from the talk.

### Output 5: Explanatory Blog Post

**File:** `generated-article-formal.md`
**Inputs:** All previous outputs (or all available generated files if running incrementally)
**Check:** Skip if file exists

Create a traditional blog post with complete explanations and smooth narrative flow.

**Target audience:** General readers discovering the topic, browsing casually
**Reading context:** Website visitors who have time and want full understanding

**Instructions:**

- Write in complete, flowing sentences with careful transitions
- Provide context and background before diving into details
- Use storytelling elements to maintain engagement
- Example opening: "V průběhu posledního roku jsme zaznamenali značné změny..." (Czech) or equivalent
- Explain why concepts matter, not just what they are
- Guide readers through ideas with clear signposting
- Respond in {lang} language - the article must be in the same language as the source material

**Style characteristics:**

- Narrative structure with introduction, development, conclusion
- Welcoming tone that assumes less prior knowledge
- Longer paragraphs with descriptive language
- Educational approach that builds understanding step-by-step

### Output 6: Scannable Technical Brief

**File:** `generated-article-direct.md`
**Inputs:** All previous outputs (or all available generated files if running incrementally)
**Check:** Skip if file exists

Create a condensed, high-signal article optimized for rapid scanning and information extraction.

**Target audience:** Technical readers or busy professionals who skim content
**Reading context:** Newsletter, Slack/Discord shares, or quick reference

**Instructions:**

- Lead with short, declarative statements - skip warm-up sentences
- Frontload key information in each paragraph
- Heavy use of bullets, numbered lists, and visual breaks
- Example opening: "AI modely: radikální skok za rok." (Czech) or equivalent
- Cut all filler words, hedging, and obvious statements
- Dense information - every sentence earns its place
- Respond in {lang} language - the article must be in the same language as the source material

**Style characteristics:**

- Telegraphic style - fragments are encouraged when clearer
- Bullets and lists dominate over prose paragraphs
- Assumes reader familiarity with domain
- Optimized for 2-minute skim, not 10-minute read

## Summary

After completion, inform the user which files were:

- **Skipped** (already existed)
- **Generated** (newly created)

Example output:

```
Workflow complete!

Skipped (already exists):
- audio.mp3
- generated-transcript.txt
- generated-transcript-cleaned.md
- generated-transcript-readable.md
- generated-transcript-outline.md

Generated:
- generated-key-ideas.md
- generated-article-formal.md
- generated-article-direct.md

All outputs in <language> language.
```

If everything was generated fresh, simply list all outputs under "Generated".

## Error Handling

- **Missing ffmpeg**: Prompt user to install ffmpeg
- **Missing API key**: Prompt user to set ELEVENLABS_API_KEY
- **Transcription errors**: Show error message and suggest checking API key/quota
- **Script not found**: Use absolute paths to skill scripts directory
