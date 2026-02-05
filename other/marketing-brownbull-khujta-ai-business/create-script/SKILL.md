---
name: create-script
description: Transforms content into a voiceover-ready script optimized for Chatterbox TTS. Use when the user provides ANY content for voiceover - URLs, raw text, video scripts, notes, or asks to "create a script" for audio.
license: Apache-2.0
compatibility: Requires web fetching capability (for URLs) and LLM processing. No external scripts needed.
metadata:
  author: chatterbox
  version: "4.0"
---

# Create Script

Transforms ANY content into a natural, engaging voiceover script.

## When to use this skill

**USE THIS SKILL** when the user:
- Provides raw text/content and wants a voiceover (e.g., "do voiceover on this: [content]")
- Provides a video script, notes, or outline to convert to audio
- Shares a URL to convert to audio narrative
- Says "create a script" or "make this into a voiceover script"
- Provides content with timestamps, bullet points, or formatting to clean up

**IMPORTANT**: If the user provides content AND says "voiceover" or "then voiceover", use THIS skill FIRST to create the script file, THEN use the `voiceover` skill to generate audio.

## How to execute this skill

### Step 1: Determine the output filename

Ask yourself: What should this script be named?
- **Prioritize the URL slug** if provided (e.g., for `https://example.com/journal/entry-001`, use `entry-001.txt`)
- Use a descriptive name based on the content if no URL is present (e.g., `opencode_skills_video.txt`, `cooking_tutorial.txt`)
- Default to `article.txt` only if no better name is apparent
- The user may specify a filename - use it if provided

### Step 2: Transform the content

Apply these transformations to the content:

1. **Clean up structure**: Remove timestamps, bullet points, section headers, and visual cues
2. **Rewrite for speech**: Convert written style to conversational spoken style
3. **Keep acronyms concise**: Do NOT expand common acronyms (e.g., keep "AI" instead of expanding to "Artificial Intelligence") unless explicitly necessary for clarity. Chatterbox TTS handles common acronyms naturally.
4. **Convert symbols**: % → "percent", $ → "dollars", & → "and", etc.
5. **Remove visual references**: Cut "click here", "see image below", "as shown above"
6. **Add paralinguistic tags** sparingly where natural:
   - ✅ SUPPORTED: `[sigh]`, `[chuckle]`, `[laugh]`
   - ❌ NOT SUPPORTED: `[pause]`, `[breath]` (Chatterbox ignores these)
7. **Ensure flow**: Create natural transitions, opening hook, satisfying conclusion

### Step 3: Save the script

Save the transformed content to the project's working directory as `[filename].txt`

### Step 4: Report back

Tell the user:
- The filename you saved to
- Word count (helps estimate voiceover duration)
- Any paralinguistic tags added
- Remind them the file is ready for the `voiceover` skill

## Example Usage

### Example 1: Raw text provided
User: "Create a script from this and then voiceover: [paste of video script with timestamps]"

1. Clean up the content (remove timestamps, format for speech)
2. Add 1-2 `[chuckle]` tags where natural
3. Save to descriptive filename like `video_script.txt`
4. Tell user the script is ready
5. **Then proceed to use the `voiceover` skill** (user said "then voiceover")

### Example 2: URL provided
User: "Create a script from https://example.com/article"

1. Fetch the URL content
2. Transform following the guidelines above
3. Save to `article.txt` or a descriptive name
4. Report back to user

## Output Format

The script should:
- Read naturally when spoken aloud
- Use short, digestible sentences
- Have paragraph breaks for natural pauses
- Be saved as a `.txt` file in the project's working directory
