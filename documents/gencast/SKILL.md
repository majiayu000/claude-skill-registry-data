---
name: gencast
description: Auto-invoke gencast to generate podcasts from documents when user mentions podcast, audio, or dialogue generation
allowed-tools: Bash, Read
---

# gencast - Podcast Generation from Documents

Generate conversational podcasts from documents using gencast CLI. ALWAYS uses `--minimal` flag to reduce context usage.

## When to Use This Skill

Auto-invoke when the user mentions:
- "podcast", "generate podcast", "convert to podcast"
- "audio", "convert to audio", "make an audio version"
- "dialogue", "conversation", "generate dialogue"
- "lecture recording", "educational audio"
- Document conversion to spoken format

## How to Use

CRITICAL: ALWAYS include `--minimal` flag in every gencast command to avoid context bloat.

### Basic Pattern

```bash
gencast <input-file> --minimal -o <output.mp3>
```

### With Style and Audience

```bash
gencast document.md --minimal --style educational --audience general -o podcast.mp3
```

### With Planning for Comprehensive Coverage

```bash
gencast document.md --minimal --with-planning --save-plan -o podcast.mp3
```

## Core Workflows

### 1. Check gencast Installation

Before running gencast, verify it's installed:

```bash
which gencast
```

If not found, inform the user:
```
gencast is not installed. Install with: pip install gencast
```

### 2. Validate Input File

Check the input file exists before running:

```bash
if [[ -f "document.md" ]]; then
  gencast document.md --minimal -o podcast.mp3
else
  echo "[ERROR] Input file not found: document.md"
fi
```

### 3. Generate Basic Podcast

Default style (educational) and audience (general):

```bash
gencast lecture.md --minimal -o lecture_podcast.mp3
```

### 4. Generate with Custom Style and Audience

```bash
# Interview style for technical audience
gencast chapter.md --minimal --style interview --audience technical -o chapter.mp3

# Casual style for beginners
gencast intro.md --minimal --style casual --audience beginner -o intro.mp3

# Debate style for academic audience
gencast paper.md --minimal --style debate --audience academic -o paper.mp3
```

### 5. Generate with Planning

For comprehensive coverage of complex documents:

```bash
gencast complex_doc.md --minimal --with-planning --save-dialogue --save-plan -o output.mp3
```

This creates:
- `output.mp3` - The podcast audio
- `output_plan.txt` - The planning document
- `output_dialogue.txt` - The generated dialogue script

### 6. Multiple Input Files

Gencast concatenates multiple inputs:

```bash
gencast chapter1.md chapter2.md chapter3.md --minimal -o full_course.mp3
```

### 7. Custom Voice Selection

```bash
gencast doc.md --minimal --host1-voice nova --host2-voice echo -o podcast.mp3
```

Available voices: alloy, echo, fable, onyx, nova, shimmer (see references/voices.md)

## Minimal Output Format

With `--minimal` flag, gencast only shows:
- Milestones (plan generation, dialogue generation, audio synthesis)
- Final output path
- Duration

No spinners or progress bars - keeps context clean.

## Progress Reporting

After running gencast, report to the user:

```
[OK] Podcast generated

Output: podcast.mp3
Duration: 5m 32s
Style: educational
Audience: general

Additional files:
- podcast_dialogue.txt (if --save-dialogue used)
- podcast_plan.txt (if --save-plan used)
```

## Edge Cases

### PDF Input

PDFs require MISTRAL_API_KEY environment variable:

```bash
if [[ ! -z "$MISTRAL_API_KEY" ]]; then
  gencast document.pdf --minimal -o podcast.mp3
else
  echo "[WARN] PDF input requires MISTRAL_API_KEY environment variable"
  echo "Set with: export MISTRAL_API_KEY=your_key"
fi
```

### Output File Exists

Gencast will overwrite existing files. Warn the user if needed:

```bash
if [[ -f "podcast.mp3" ]]; then
  echo "[WARN] Output file podcast.mp3 already exists and will be overwritten"
fi
gencast doc.md --minimal -o podcast.mp3
```

### No Input Files

```bash
if [[ $# -eq 0 ]]; then
  echo "[ERROR] No input files provided"
  echo "Usage: gencast <input-files> [options]"
  exit 1
fi
```

## Best Practices

1. **Always use --minimal** - Required for context management
2. **Validate inputs first** - Check files exist before running
3. **Provide clear output paths** - Use descriptive names (lecture_01.mp3, not output.mp3)
4. **Save dialogue for review** - Use --save-dialogue for complex topics
5. **Use planning for long documents** - --with-planning ensures comprehensive coverage
6. **Match style to content** - educational for lectures, interview for Q&A, debate for contrasting views
7. **Consider audience level** - beginner vs technical vs academic affects language complexity

## Reference Documentation

- Voice Options: references/voices.md (6 voices with character descriptions)
- Styles and Audiences: references/styles.md (4 styles x 4 audiences matrix)

## User Commands

For explicit invocation, users can use:
- `/gencast:podcast <input> [options]` - Full control over all options
- `/gencast:plan <input>` - Generate planning document only (no audio)

## Examples

### Example 1: Simple Lecture Podcast

```bash
gencast CS101_lecture_notes.md --minimal -o CS101_lecture.mp3
```

### Example 2: Technical Interview Style

```bash
gencast API_documentation.md --minimal --style interview --audience technical --save-dialogue -o API_podcast.mp3
```

### Example 3: Beginner-Friendly Casual Style

```bash
gencast intro_to_programming.md --minimal --style casual --audience beginner -o intro_podcast.mp3
```

### Example 4: Academic Debate

```bash
gencast research_paper.md --minimal --style debate --audience academic --with-planning --save-plan -o research_podcast.mp3
```

### Example 5: Multi-Chapter Course

```bash
gencast week1.md week2.md week3.md --minimal --style educational --audience general -o course_weeks_1-3.mp3
```
