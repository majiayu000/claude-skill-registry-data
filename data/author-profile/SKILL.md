---
name: author-profile
description: Create author profiles via questionnaire or transcript analysis for consistent article voice
---

# Author Profile

Create and maintain consistent author voice across all articles.

## Profile Location

Stored in: `.article_writer/authors.json`

Schema: `.article_writer/schemas/authors.schema.json`

## Two Ways to Create an Author

### Option 1: Manual Questionnaire

Ask questions in conversational groups (2-3 at a time):

#### Identity
1. What name/identifier for this author? (e.g., "mwguerra")
2. Display name? (e.g., "MW Guerra")
3. Professional role(s)?
4. Years/areas of experience?
5. Expertise areas?

#### Languages
6. Primary writing language? (e.g., pt_BR, en_US)
7. Translation target languages?

#### Tone (1-10)
8. Casual (1) vs Formal (10)?
9. Neutral (1) vs Opinionated (10)?

#### Vocabulary
10. Terms readers know (use freely)?
11. Terms to always explain?

#### Style
12. Signature phrases?
13. Phrases to avoid?

#### Positions
14. Strong technology opinions?
15. Topics to stay neutral on?

#### Example
16. Write 2-3 sentences in your voice as example.

### Option 2: Extract from Transcripts

**Use Skill(voice-extractor) for transcript analysis.**

If the author has recordings (podcasts, interviews, videos, meetings):

1. **Prepare transcripts** - Get transcription files with speaker labels
2. **Run analysis**:
   ```bash
   bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/voice-extractor.ts --speaker "Name" transcripts/*.txt
   ```
3. **Review extracted data** - Communication style, phrases, vocabulary
4. **Add identity info** - Name, role, expertise, languages (manual)
5. **Merge** - Combine extracted + manual data

### Option 3: Combined Approach (Recommended)

Best results come from combining both:
1. Extract voice patterns from transcripts
2. Add identity/expertise info manually
3. Review and refine the merged profile

## Author JSON Structure

```json
{
  "id": "author-slug",
  "name": "Display Name",
  "languages": ["pt_BR", "en_US"],
  "role": "Senior Developer",
  "experience": "10+ years",
  "expertise": ["Laravel", "PHP", "Architecture"],
  "tone": {
    "formality": 4,
    "opinionated": 7
  },
  "vocabulary": {
    "use_freely": ["Controllers", "Middleware", "API"],
    "always_explain": ["DDD", "CQRS", "Event Sourcing"]
  },
  "phrases": {
    "signature": ["Na prática...", "Vamos direto ao ponto:"],
    "avoid": ["Simplesmente", "É só fazer..."]
  },
  "opinions": {
    "strong_positions": ["Tests are essential", "Fat models are bad"],
    "stay_neutral": ["Tabs vs spaces", "IDE preferences"]
  },
  "example_voice": "Sample paragraph in author's voice...",
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
      { "trait": "analytical", "percentage": 24.1 }
    ],
    "characteristic_expressions": ["you know", "the thing is"],
    "sentence_starters": ["I think", "So the"],
    "signature_vocabulary": ["approach", "strategy", "implementation"],
    "analyzed_at": "2025-01-15T10:00:00Z"
  },
  "notes": "Additional style notes..."
}
```

## Voice Analysis Fields

When transcripts are analyzed, these fields are populated:

| Field | Description |
|-------|-------------|
| `extracted_from` | Transcript files analyzed |
| `sample_count` | Speaking turns analyzed |
| `total_words` | Total words in analysis |
| `sentence_structure` | Length, variety, question frequency |
| `communication_style` | Traits: enthusiasm, hedging, directness, etc. |
| `characteristic_expressions` | Frequently used phrases/fillers |
| `sentence_starters` | Common ways to start sentences |
| `signature_vocabulary` | Words that characterize the speaker |

## Using Voice Analysis When Writing

When writing articles, use voice_analysis data:

1. **Sentence structure**: Match `avg_length` and `variety`
2. **Tone**: Follow `communication_style` traits
3. **Natural speech**: Sprinkle `characteristic_expressions` naturally
4. **Vocabulary**: Prefer words from `signature_vocabulary`
5. **Sentence starters**: Use patterns from `sentence_starters`

## Multi-Language Workflow

1. Article written in author's primary language (first in array)
2. After completion, translated to other languages
3. Each file named: `{slug}.{language}.md`

Example for author with `["pt_BR", "en_US"]`:
```
content/articles/2025_01_15_rate-limiting/
├── rate-limiting.pt_BR.md    # Primary (written first)
└── rate-limiting.en_US.md    # Translation
```

## Default Author

If article task doesn't specify author:
- First author in `authors.json` is used
- Their language settings apply
- Their voice/tone is followed

## Updating Authors

### Add More Transcript Data

```bash
# Analyze new transcripts for existing author
bun run "${CLAUDE_PLUGIN_ROOT}"/scripts/voice-extractor.ts \
  --speaker "Name" \
  --author-json \
  new_podcast.txt > new_analysis.json

# Merge into existing profile (manually or via command)
```

### When to Update
- New transcript data available
- Writing style evolves
- Feedback indicates tone mismatch
- New expertise develops
