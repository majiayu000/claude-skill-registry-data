---
name: voice-extractor
description: Extract voice patterns from transcripts - speaking style, phrases, vocabulary for authentic author profiles
---

# Voice Extractor

Extract authentic voice characteristics from transcripts to enhance author profiles.

## Purpose

Transform transcript data (podcasts, interviews, meetings, videos) into actionable writing guidelines that capture an author's authentic voice, making AI-generated content sound natural and personal.

## When to Use

- Author has recordings/transcripts of themselves speaking
- Want to capture authentic speaking patterns
- Need to enhance a manually-created author profile
- Building a new author profile from scratch using transcripts
- Refining an existing profile with more data

## Workflow

### 1. Prepare Transcripts

Accept transcripts in these formats:
- Plain text: `Speaker: text`
- Timestamped: `[00:01:23] Speaker: text` or `59:54 Speaker: text`
- Bracketed: `[Speaker]: text`
- WhatsApp: `[17:30, 12/6/2025] Speaker: text`
- SRT subtitles: Standard subtitle format

**If user provides audio/video without transcript:**
Suggest transcription services:
- YouTube auto-captions (downloadable)
- Otter.ai, Descript
- OpenAI Whisper (local)
- Rev.com

### 2. Run Analysis

```bash
# List speakers in transcript
bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/voice-extractor.ts --list-speakers transcript.txt

# Extract for specific speaker
bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/voice-extractor.ts --speaker "Name" transcript.txt

# Multiple transcripts (more data = better profile)
bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/voice-extractor.ts --speaker "Name" t1.txt t2.txt t3.txt

# Output JSON for direct merging into authors.json
bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/voice-extractor.ts --speaker "Name" --json transcript.txt
```

### 3. Enhance Author Profile

The extracted data enhances these author fields:

| Extracted Data | Maps To |
|---------------|---------|
| Communication style | `tone.formality`, `tone.opinionated` |
| Characteristic expressions | `phrases.signature` |
| Sentence starters | `phrases.signature` |
| Signature vocabulary | `vocabulary.use_freely` |
| Speaking style | `notes` |

### 4. Manual Enhancement

After automated extraction, read transcript samples to identify:

- **Unique phrases**: Catchphrases missed by frequency analysis
- **Humor style**: Sarcasm, self-deprecation, wit patterns
- **Story structure**: How they set up anecdotes
- **Cultural markers**: Regional expressions, analogies
- **Topic emphasis**: What makes them animated

## What Gets Extracted

### Sentence Structure
- Average sentence length
- Variety (short/moderate/long/complex)
- Question frequency

### Communication Style
- Enthusiasm (love, amazing, awesome)
- Hedging (maybe, perhaps, I think)
- Certainty (definitely, absolutely)
- Empathy (understand, appreciate)
- Directness (need to, must, bottom line)
- Storytelling (so, and then, eventually)
- Analytical (because, therefore, however)

### Characteristic Expressions
- Fillers: "you know", "I mean", "like", "right"
- Hedgers: "kind of", "sort of", "I guess"
- Emphatics: "honestly", "literally", "definitely"

### Vocabulary
- Signature words used frequently
- Vocabulary richness percentage

## Integration with Author Profile

### New Author from Transcript

```bash
# 1. Extract voice data
/article-writer:author analyze --speaker "John" transcripts/*.txt

# 2. Review and confirm extraction
# Claude will show extracted patterns

# 3. Add identity info
/article-writer:author add
# Answer: name, role, expertise, languages

# 4. Merge voice data
# Claude will combine extracted + manual data
```

### Enhance Existing Author

```bash
# 1. Extract from new transcripts
/article-writer:author analyze --speaker "John" --author-id mwguerra new_podcast.txt

# 2. Review changes
# Claude shows what will be updated

# 3. Confirm merge
# Voice analysis data added to existing profile
```

## Output Format

### JSON Output (for merging)

```json
{
  "voice_analysis": {
    "extracted_from": ["podcast_ep1.txt", "interview.txt"],
    "sample_count": 156,
    "total_words": 12450,
    "sentence_structure": {
      "avg_length": 14.5,
      "variety": "moderate length, conversational",
      "question_ratio": 12.3
    },
    "communication_style": [
      { "trait": "enthusiasm", "percentage": 28.5 },
      { "trait": "analytical", "percentage": 24.1 },
      { "trait": "directness", "percentage": 18.7 }
    ],
    "characteristic_expressions": [
      "you know",
      "I think",
      "the thing is",
      "at the end of the day"
    ],
    "sentence_starters": [
      "I think",
      "So the",
      "And then",
      "But the"
    ],
    "signature_vocabulary": [
      "actually",
      "basically",
      "approach",
      "strategy",
      "implementation"
    ],
    "analyzed_at": "2025-01-15T10:00:00Z"
  },
  "suggested_updates": {
    "tone": {
      "formality": 5,
      "opinionated": 7
    },
    "phrases": {
      "signature": ["you know", "the thing is", "at the end of the day"]
    },
    "vocabulary": {
      "use_freely": ["approach", "strategy", "implementation"]
    }
  }
}
```

### Markdown Report

```markdown
# Voice Analysis: John Smith

*Analyzed 156 speaking turns, 12,450 words*

## Speaking Style
- **Sentence length**: Moderate (~14 words avg)
- **Questions**: Uses questions occasionally (12%)
- **Vocabulary richness**: 45% unique words

## Communication Style
- **Primary**: Enthusiastic (28%)
- **Secondary**: Analytical (24%)
- **Tertiary**: Direct (19%)

## Characteristic Expressions
- "you know" (used 45x)
- "I think" (used 38x)
- "the thing is" (used 22x)

## Sentence Starters
- "I think..." (28x)
- "So the..." (19x)
- "And then..." (15x)

## Signature Vocabulary
**actually** (67x), **basically** (45x), **approach** (34x)

---

## Recommendations for Author Profile

Based on this analysis:
- Set formality to 5 (conversational but professional)
- Set opinionated to 7 (confident, uses "I think" but states opinions)
- Add signature phrases: "you know", "the thing is"
- Use vocabulary freely: approach, strategy, implementation
```

## Quality Indicators

Good voice analysis needs:
- **100+ speaking turns** for reliable patterns
- **5,000+ words** for vocabulary analysis
- **Multiple contexts** (different topics/conversations)

Low data warning:
```
⚠️ Limited data: Only 23 speaking turns found.
   Results may not fully represent speaking patterns.
   Consider adding more transcripts.
```

## References

- [TRANSCRIPT-FORMAT-EXAMPLES.md](references/TRANSCRIPT-FORMAT-EXAMPLES.md)
- [VOICE-PROFILE-TEMPLATE.md](references/VOICE-PROFILE-TEMPLATE.md)
