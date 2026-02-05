---
name: id-generator
description: Generate intelligent session IDs based on detected content source type.
  Analyzes ContentSummary and creates meaningful IDs (podcast-xyz, transcript-abc, etc.).
---

# ID Generator Skill

Expert at generating meaningful session IDs based on content source type and characteristics.

## What This Skill Does

- Reads ContentSummary JSON with detectedSource field
- Analyzes source type and main topic/theme
- Generates human-readable, meaningful session ID
- Returns ID with confidence score and rationale
- Enables reusable content identification

## ID Generation Process

Follow these 5 steps:

### Step 1: Validate Input
- Confirm ContentSummary has required fields
- Check if detectedSource field exists
- Note the content's main topic/headline/category

### Step 2: Analyze Source Type
- Review detectedSource value (podcast, transcript, article, youtube, twitter, text, other)
- Consider content characteristics:
  - **Podcast**: Audio transcript with timestamps, speaker markers, conversational flow
  - **Transcript**: Conversational content, dialogue, timestamps, multiple speakers
  - **Article**: Written structure, sections, headlines, formal tone
  - **YouTube**: Video description, channel info, timestamps
  - **Twitter**: Social media context, short-form, engagement metrics
  - **Text**: Unstructured thoughts, raw content, raw notes
  - **Other**: Any other content type

### Step 3: Extract Topic Keywords
- Identify main topic from headline, category, or keyThemes
- Select 1-2 most significant keywords
- Avoid generic terms, prefer specific subject matter
- Examples: "healthcare", "ai", "python", "productivity"

### Step 4: Generate Base ID
- Format: `{source-type}-{date}-{topic}`
- Source prefix from detectedSource (lowercase)
- Date in YYYY-MM-DD format
- Topic as 1-2 words (hyphen-separated, lowercase)
- Example: `podcast-2024-12-08-ai-healthcare`

### Step 5: Quality Check & Return
- Ensure ID is lowercase, hyphen-separated
- Validate length (20-50 characters preferred)
- Return JSON with:
  - `contentId`: Generated ID
  - `detectedSource`: Confirmed source type
  - `sourceConfidence`: 0.0-1.0 confidence in source detection
  - `rationale`: Brief explanation of why this source type

## ID Generation Rules

### Source-Based Naming
- **Podcast**: `podcast-{date}-{topic}`
- **Transcript**: `transcript-{date}-{topic}`
- **Article**: `article-{date}-{topic}`
- **YouTube**: `youtube-{date}-{topic}`
- **Twitter**: `tweet-{date}-{topic}`
- **Text**: `text-{date}-{topic}`
- **Other**: `content-{date}-{topic}`

### Topic Selection
- Extract from headline (first 2-3 words)
- If headline too generic, use category or first keyTheme
- Avoid articles (a, the, and, or)
- Use only letters, numbers, hyphens
- Maximum 3 words

### Date Handling
- Use current date in YYYY-MM-DD format
- Or extract from context field if content has original date
- Format consistently

### Examples
```
Input: Podcast about AI in Healthcare (2024-12-08)
Output: podcast-2024-12-08-ai-healthcare

Input: Whisper transcript of React conference talk (2024-12-07)
Output: transcript-2024-12-07-react-conference

Input: Article on productivity hacks (2024-12-06)
Output: article-2024-12-06-productivity-hacks

Input: YouTube tutorial on Python (2024-12-05)
Output: youtube-2024-12-05-python-tutorial
```

## Output Format

Return structured JSON:
```json
{
  "contentId": "podcast-2024-12-08-ai-healthcare",
  "detectedSource": "podcast",
  "sourceConfidence": 0.95,
  "rationale": "Audio transcript with speaker markers, timestamps, and conversational flow indicates podcast source."
}
```

## Important Rules

- Always return valid JSON
- Confidence score reflects certainty in source detection (0.5-1.0 typical range)
- Rationale should be brief (1-2 sentences)
- ID must be unique and reusable
- Never include spaces or special characters (except hyphens)
- Generate ID even if source confidence is moderate (>0.5)
- Prefer readable IDs over random strings
- Keep ID length under 60 characters when possible
