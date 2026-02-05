---
name: build-in-public
description: Generate social media posts for building in public, coding in public, or dev content creation. Activate when user mentions Twitter, X, BlueSky, LinkedIn, Instagram posts about coding, sharing progress, social media content for developers, or wants to share what they built.
version: 1.0.0
---

# Build in Public - Social Media Post Generator

This skill helps developers create engaging social media content from their Claude Code sessions for the #BuildingInPublic and #CodingInPublic communities.

## Capabilities

- Parse Claude Code session transcripts to extract highlights
- Generate platform-appropriate posts for:
  - **Twitter/X**: Short posts (280 chars) and threads
  - **BlueSky**: Short posts (300 chars)
  - **LinkedIn**: Medium-length professional updates
  - **Instagram**: Long-form captions with hashtags
  - **Mastodon**: Medium posts with hashtags
- Track session metrics (files created, commits, bugs fixed, etc.)
- Output both markdown (human-readable) and JSON (for automation)

## When to Activate

Activate this skill when the user:
- Asks to create social media posts about their coding
- Mentions "building in public" or "coding in public"
- Wants to share their progress on Twitter, X, BlueSky, LinkedIn, or Instagram
- Asks for a session summary to share
- Mentions #BuildingInPublic or similar hashtags
- Says things like "I want to tweet about this" or "post this to social media"

## Commands Available

- `/build-in-public:generate` - Generate posts from the current session
- `/build-in-public:preview` - Preview session activity before generating

## How to Generate Posts

When the user wants to create social media content:

1. **Preview first** (optional): Run `/build-in-public:preview` to show them what happened in the session

2. **Generate posts**: Run the generation script:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/generate_posts.py" --output . --json
   ```

3. **Present the best options**: Show the user 1-2 ready-to-post short posts and mention the full file has more options

4. **Offer customization**: Ask if they want to emphasize certain aspects or add custom context

## Post Formats

### Short Posts (Twitter/X, BlueSky)
- Max 280 characters
- Include 1-2 relevant hashtags
- Focus on one key accomplishment
- Use emojis sparingly but effectively

### Threads (Twitter/X)
- 4-6 tweets
- Start with a hook
- End with engagement question
- Each tweet under 280 chars

### Medium Posts (LinkedIn)
- 500-700 characters
- Professional tone
- Bullet points for accomplishments
- Include relevant hashtags at the end

### Long Form (Instagram)
- 1000+ characters
- Storytelling format
- Multiple hashtags (up to 30)
- Include call-to-action

## Output Files

The generator creates:
- `build-in-public_[timestamp].md` - Human-readable posts with all options
- `build-in-public_[timestamp].json` - Structured data for automation tools

## Integration with Publishing Tools

The JSON output can be consumed by automation tools to publish posts. The structure:

```json
{
  "summary": {
    "session_id": "...",
    "project_name": "...",
    "files_created": [...],
    "git_commits": [...],
    ...
  },
  "posts": {
    "short": ["post1", "post2"],
    "thread": ["tweet1", "tweet2", ...],
    "medium": ["linkedin post"],
    "long": ["instagram caption"],
    "hashtags": ["#BuildingInPublic", ...]
  }
}
```

## Tips for Great #BuildingInPublic Content

1. **Be specific**: "Added user authentication" beats "worked on the app"
2. **Show numbers**: "Fixed 3 bugs, created 5 files" is more engaging
3. **Include the struggle**: Bugs fixed = relatable content
4. **End with engagement**: "What are you building?" invites responses
5. **Use relevant hashtags**: Match the tech stack (#Python, #React, etc.)
