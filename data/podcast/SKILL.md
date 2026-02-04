---
name: podcast
description: Creates audio podcasts from text using browser text-to-speech. Use when user mentions podcast, audio conversation, dialogue, spoken content, voice narration, audio book, or text-to-speech generation. Supports multiple speakers with automatic language detection. Zero cost, no API keys, works in browser.
allowed-tools: Read, Write
---

# Podcast Generator

Generates podcast-style audio that plays directly in the browser. Zero cost, no API keys needed.

## Workflow Decision Tree

### User provides formatted dialogue
→ Use existing dialogue as-is if quality is good
→ Refine structure only if flow needs improvement

### User provides article, list, or text content
→ Create dialogue from content (see "Dialogue Creation Process")

### User provides topic only
→ Request source material before proceeding

## Dialogue Creation Process

Follow this two-phase workflow when creating podcast dialogue from content:

### Phase 1: Analyze Source Content

1. **Read source material completely**
2. **Detect language** from content (en, de, fr, es, it, etc.)
3. **Identify key information**: facts, dates, names, numbers, details
4. **Organize by theme**: chronology, category, or logical grouping

### Phase 2: Create Dialogue

1. **Structure conversation**:
   - Host (Speaker 1): ~20% - questions and transitions
   - Expert (Speaker 2): ~80% - factual responses from source
   - Length: as many exchanges as needed to cover all content (typically 10-50+ lines)

2. **Apply TTS formatting**: Read [reference/tts-formatting.md](./reference/tts-formatting.md) for complete rules

3. **Generate JSX file** from template (see "Implementation Steps")

## Information Accuracy

Convert text to audio. Use only source material facts.

**Expert responses:**
- Use only names, dates, numbers, details explicitly stated in source
- Never invent examples, context, or explanations not in source
- Never add interpretations, opinions, or evaluations
- Never explain WHY something happened unless source explains it

**Host phrases:**
- Use neutral transitions: "I see", "Tell me more", "Can you elaborate?"
- Reference previous statements: "You mentioned X - how does that connect to Y?" (when source shows connection)
- Never add new facts, context, or interpretations

## Dialogue Format Guidelines

### Host (Speaker 1) - ~20% of content

- Introduce topic with opening question
- Ask transition questions between topics
- Reference Expert's previous statements: "You mentioned X - can you elaborate?"
- Use conversational acknowledgments: "I see", "Tell me more"
- Never introduce facts not in source

### Expert (Speaker 2) - ~80% of content

- Provide comprehensive factual responses from source material
- Include specific details: names, dates, numbers, locations
- Organize information logically by theme, chronology, or category
- Structure facts narratively using only source material
- Never repeat information already stated
- Never add context or examples not in source

### Natural Conversation Techniques

Use these patterns without adding information:
- Vary question styles: "What happened next?" / "Can you explain that further?" / "Tell me about..."
- Ask follow-up questions based on Expert's previous response
- Expert elaborates when source provides multiple details about a topic
- Clear transitions between sections: "Moving to the next category...", "In the European context..."

### Avoid

- Personal opinions: "I think...", "That's crazy..."
- Value judgments: "amazing", "fascinating", "interesting"
- Humor, irony, jokes
- Rapid back-and-forth after every sentence

## Implementation Steps

When user requests a podcast:

1. **Analyze source content** and create dialogue following format above
2. **Detect language** from content
3. **Read template** from `assets/podcast-template.jsx`
4. **Replace values** in template:
   - `PODCAST_SCRIPT` - your generated dialogue
   - `PODCAST_TITLE` - descriptive title from content
   - `PODCAST_LANGUAGE` - detected language code
5. **Save as JSX file** - Use the Write tool to save the modified template as a `.jsx` file. The file will render as an interactive podcast player.
6. **Recommend Microsoft Edge browser** for best voice quality (250+ Natural voices vs Chrome's 19)

## Technical Reference

### Script Format
```
<speaker1>Host's question or statement.
<speaker2>Expert's response with factual information.
```

### Voice Configuration (automatic)
- Speaker 1 (Host): Pitch 1.05, Rate 0.95
- Speaker 2 (Expert): Pitch 0.88, Rate 0.93

### Platform-Aware Voice Selection

**Platform detection:**
- Automatically detects iOS, Android, Desktop Edge, or Desktop
- Selects best available voices based on platform

**Desktop Edge:**
- Priority: Microsoft Neural/Natural voices (Katja, Conrad, Aria, Guy, etc.)
- 250+ high-quality voices available

**Desktop Chrome:**
- Priority: Google voices (Google UK English Female, Google Deutsch, etc.)
- ~19 voices available (lower quality than Edge)
- Fallback: local system voices

**iOS (Safari/Mobile):**
- Priority: Native Siri voices (Samantha, Anna, Daniel, etc.)
- Best quality on iOS devices

**Android (Chrome/Mobile):**
- Priority: Google TTS voices (Google Deutsch, Google UK English Female, etc.)
- Wavenet voices preferred when available

**Voice assignment:**
- Automatically assigns different voices to Speaker 1 and Speaker 2
- Uses modulo distribution for 3+ speakers
- Ensures distinct voices even with limited availability

### Player Features
- Play/Pause/Resume with full playback control
- Stop to reset to beginning
- Click any transcript line to resume from there
- Progress bar shows current position
- Auto-scroll follows current line

### Technical Constraints
- Keep sentences under 14 seconds (Chrome limitation)
- 350ms pause between speakers
- Microsoft Edge browser provides 250+ high-quality Natural voices (best option)
- Chrome provides only 19 lower-quality voices with utterance bugs
- Firefox has very limited voice support

## Quality Requirements

- **Factual Accuracy**: Expert responses use only source facts
- **Natural Flow**: Avoid rapid back-and-forth, value judgments
- **TTS Compliance**: All text must play without pronunciation errors
- **Zero Hallucination**: No invented examples or context
- **Complete Coverage**: Include all important facts from source
- **No Duplicates**: Each fact appears exactly once
