---
name: blog-voice-review
description: |
  Review blog content for authentic voice and tone. Checks if content sounds like Fabio's conversational, honest technical writing style.
  Trigger phrases: "voice", "voice review", "tone", "sounds like me", "authentic", "check voice", "voice check"
allowed-tools: Read
---

# Voice & Tone Review

## Quick Checks
- First person? ("I've been", "my experience")
- Conversational? (like talking to a colleague)
- Honest about limitations?
- Personal experience vs generic advice?
- Any English idioms that confuse non-native speakers?

## Red Flags
- Overly formal language
- Generic examples ("Let's say you have...")
- Claims without personal context
- Marketing speak
- Phrases like "leverage", "utilize" instead of "use"

## Title & Clickbait Check
Watch for clickbait patterns in titles:
- Excessive superlatives ("worst", "best", "ultimate")
- Manufactured urgency or drama
- Promising more than the content delivers
- "You won't believe..." or similar hooks

**Good titles:**
- Honest about scope ("one of my bad habits" not "my worst habit")
- Clear about what the post covers
- Personal and specific
- No artificial drama

## Style Guide
For detailed voice guidelines, see `style-guide.md`

## Process
1. Read the content
2. Flag issues with brief explanation
3. Don't rewrite - let author fix in their voice

## Response Format
Keep it conversational:

```
This section feels generic - you mention "users might want" but where's YOUR experience? 

Also caught an idiom: "hit the ground running" might confuse non-native speakers. Try more direct language.

The technical explanation is great though - clear and accessible.
```
