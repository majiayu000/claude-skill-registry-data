---
name: blog-to-linkedin
description: This skill should be used when converting technical blog posts (markdown files) into engaging LinkedIn posts that drive traffic and engagement. Use when the user provides a blog post file path or asks to create a LinkedIn post from their blog content.
---

# Blog to LinkedIn Converter

## Overview

Convert technical blog posts into engaging LinkedIn posts that maintain authentic voice, drive engagement, and generate traffic to the full article. This skill analyzes blog content, extracts key insights, and structures LinkedIn posts using proven engagement patterns while adhering to the author's unique writing voice.

## When to Use This Skill

Trigger this skill when:
- User provides a markdown blog post file path and asks to create a LinkedIn post
- User asks to "promote" or "share" a blog post on LinkedIn
- User requests help writing LinkedIn content from their blog
- User mentions creating social media content for a technical article

## Conversion Workflow

### Step 1: Read and Analyze the Blog Post

Read the provided blog post markdown file completely to understand:
- **Main thesis:** What is the core argument or learning?
- **Key insights:** What are the 3-5 most important takeaways?
- **Surprising results:** What metrics, percentages, or outcomes stand out?
- **The story:** What prompted this work? What didn't work first? What was learned?
- **Target audience:** Who would benefit from this content?

**Reference the voice profile** at `references/voice-profile.md` to understand the author's:
- Tone (professional but conversational, educational, humble)
- Perspective (first person for experiences, second person for instruction)
- Common phrases and transitions
- Technical communication style

### Step 2: Identify the Hook

Extract or craft a compelling hook (first 150 characters) that will appear in the LinkedIn feed preview. The hook must:
- Grab attention immediately
- Highlight the most surprising or valuable aspect
- Create curiosity to click "see more"

**Hook patterns to consider** (from `references/linkedin-best-practices.md`):
1. **Specific result:** "Three design changes reduced my context usage from 746k to 262 tokens (99.96%)"
2. **Problem statement:** "I spent 2 weeks building an MCP server that consumed 746k tokens per query"
3. **Counter-intuitive:** "Exposing every API field to your AI makes it less accurate, not more"
4. **Personal discovery:** "While building a YNAB integration, I discovered something surprising about context windows"

Select the pattern that best matches the blog's core insight.

### Step 3: Structure the LinkedIn Post

Follow this proven structure:

**Opening (150-200 characters)**
- Hook: 1-2 sentences with the attention-grabbing insight or problem
- Context: 2-3 sentences explaining what prompted the work
- Thesis: 1 sentence stating what was learned

**Body (800-1,200 characters)**
- **3-5 key points** presented as a scannable list with bullet points (•) or numbers
- Lead with insights, not implementation details
- Include specific metrics and results
- Brief explanation of the most surprising finding
- Use first-person narrative to share the journey

**Close (150-300 characters)**
- Brief summary of what the blog post provides (implementation details, code examples, measurements)
- Link to the blog post
- Soft call-to-action: invitation to discuss or share experiences
- 3-5 relevant hashtags on a separate line

**Total target length:** 1,300-2,000 characters

### Step 4: Apply Voice and Best Practices

**Maintain voice profile characteristics:**
- Professional but conversational tone
- Direct and concise writing
- Humble sharing of discoveries ("I found", "I discovered", "I learned")
- Problem-solver mentality
- Active voice with natural contractions

**Apply LinkedIn formatting:**
- Add blank lines between all paragraphs for mobile readability
- Use bullet points (•) for lists
- Keep sentences punchy and varied in length
- No markdown formatting (LinkedIn doesn't support it)
- Place hashtags at the very end, separated by a blank line

**Optimize for engagement:**
- End with a question to invite comments ("What techniques have you discovered?")
- Create information gap: show results on LinkedIn, explain "how" in the blog
- Use specific numbers and percentages liberally
- Make it skimmable with clear structure

### Step 5: Format and Present the Draft

Present the LinkedIn post in a code block for easy copying:

```
[Full LinkedIn post content here]
```

After the post, provide:
- **Character count** (should be 1,300-2,000 total)
- **Hook validation** (confirm first 150 characters are compelling)
- **Key insights highlighted** (verify 3-5 main points are clear)
- **Engagement elements** (confirm CTA and question are present)

Offer to refine specific sections if needed.

## Reference Materials

### Voice Profile
The `references/voice-profile.md` file contains comprehensive documentation of the author's writing style, including:
- Core voice characteristics and tone
- Structural patterns and content organization
- Common phrases and transitions
- What to avoid

**Load this file into context** at the start of the workflow to ensure authentic voice alignment.

### LinkedIn Best Practices
The `references/linkedin-best-practices.md` file provides detailed guidance on:
- Character limits and formatting constraints
- Hook strategies with examples
- Post structure templates
- Engagement tactics
- Common mistakes to avoid
- Platform-specific adaptations

**Reference this file** when making structural and formatting decisions.

## Quality Checklist

Before presenting the final LinkedIn post, verify:

**Hook & Opening**
- [ ] First 150 characters grab attention and work as standalone preview
- [ ] Core insight or surprising result is stated upfront
- [ ] Context is provided but brief (2-3 sentences)

**Content Quality**
- [ ] 3-5 key points maximum, presented as scannable list
- [ ] Specific numbers and metrics included
- [ ] Personal story/journey is present
- [ ] Focus on insights, not implementation details

**Structure & Formatting**
- [ ] Blank lines between all paragraphs
- [ ] Bullet points (•) used for key insights
- [ ] Total length 1,300-2,000 characters
- [ ] Mobile-readable with visual breaks

**Voice Alignment**
- [ ] Tone matches voice profile (professional but conversational)
- [ ] Uses first person for sharing experiences
- [ ] Direct and concise language
- [ ] Humble and helpful, not promotional

**Engagement Elements**
- [ ] Ends with a question or invitation
- [ ] Link to full blog post included
- [ ] 3-5 relevant hashtags at end
- [ ] Clear value proposition for clicking through

## Common Pitfalls to Avoid

**Content mistakes:**
- Copying the blog introduction verbatim (condense and adapt)
- Burying the most interesting insight below the fold
- Including too much technical implementation detail
- Making it about showcasing work instead of helping others

**Formatting mistakes:**
- Creating walls of text without line breaks
- Forgetting to verify mobile readability
- Weak or generic hook that doesn't stop the scroll
- No clear call-to-action at the end

**Voice mistakes:**
- Being overly enthusiastic or promotional
- Using marketing language instead of authentic voice
- Losing the humble, educational tone
- Not maintaining the problem-solver perspective

## Examples

### Input
Blog post: `/home/user/blog/posts/2025-11-06-build-efficient-mcp-servers.md`

### Output Structure
```
I built an MCP server that used 746,800 tokens for a single query.

That's 3.7x larger than Claude's entire context window. I couldn't even fit the response in a single request.

Here's how I reduced it to 262 tokens (99.96% reduction):

• Filter at the source - Remove unnecessary API fields before sending to the model (65% reduction)
• Pre-aggregate data - Compute summaries in your code, not in the context window (94% reduction)
• Work within constraints - Design workflows that combine available operations creatively

[2-3 sentences explaining the key insight]

[Specific metrics and results]

The full article includes:
→ Real token measurements with tiktoken
→ Code examples for each optimization
→ When to apply each technique
→ Trade-offs and limitations

[Link to blog post]

If you're building MCP servers, start by asking: "What does the model actually need?" Not "What does the API return?"

What context optimization techniques have you discovered?

#AI #ModelContextProtocol #SoftwareEngineering #AITools #ClaudeAI
```

## Tips for Success

**Prioritize the hook:** Spend extra time crafting the first 150 characters. If it doesn't grab attention, nothing else matters.

**Use the 3-point rule:** Even if the blog covers many topics, focus LinkedIn on the 3 most surprising or actionable insights.

**Show, don't tell:** Use specific numbers ("65% reduction") instead of vague claims ("significant improvement").

**Create information gap:** Give enough value in the LinkedIn post to be useful, but save implementation details for the blog to drive traffic.

**Maintain authenticity:** The voice profile exists to ensure LinkedIn posts sound like the author, not like generic AI content.

**Optimize for mobile:** Most LinkedIn users browse on mobile. Blank lines and short paragraphs are essential.
