---
name: smart-content-creator
description: Transform reading notes and insights into polished, authentic content (blogs, social media, visualizations) that preserves your unique voice and avoids AI-style writing. Creates content that sounds unmistakably human.
---

# Smart Content Creator

## Overview

This skill transforms reading materials and personal insights into polished, shareable content across multiple formats. It emphasizes three core pillars: **(1) authentic personal voice preservation**, **(2) substantive content depth**, and **(3) natural human-like expression** that avoids AI writing patterns.

## Activation Triggers

This skill activates when users want to:
1. **Create content from reading notes or insights**
2. **Transform analysis into shareable formats**
3. **Visualize concepts or relationships**
4. **Preserve authentic voice in content creation**

**Common trigger phrases**:
- "Create/write a [blog post/article]..."
- "Turn this into [Xiaohongshu/Twitter] content"
- "Make a [mind map/diagram/infographic]..."
- "Visualize [concept/relationship]..."
- "Help me share this learning"
- "Transform these notes into..."

## Supported Formats

**Text Formats**:
- **Blog Posts** (2000-4000 words) - Long-form engaging content
- **Xiaohongshu Notes** (800-1500 chars) - Authentic Chinese social media
- **Twitter Long-Form** (1000-4000 words) - Professional X platform articles

**Visual Formats**:
- **Mind Maps** - Hierarchical knowledge organization
- **Infographics** - Data-driven storytelling with visual impact
- **Charts & Diagrams** - Flowcharts, concept maps, timelines, etc.

## Reference Loading Strategy

**CRITICAL**: Always load references in this order before generating content.

### Core Guides (ALWAYS load first):

1. **`references/writing_principles.md`** ⭐
   - First principles approach to writing quality
   - Information Transfer × Emotional Resonance × Cognitive Comfort
   - Theoretical foundation for all techniques

2. **`references/personal_voice_guide.md`** ⭐
   - Voice identification and preservation
   - Capture user's authentic expression
   - Match natural writing patterns

3. **`references/depth_guide.md`** ⭐
   - Create substantive, insightful content
   - Multi-layered thinking techniques
   - Beyond surface-level approaches

4. **`references/natural_language.md`** ⭐
   - Critical anti-AI writing patterns
   - Avoid robotic expression
   - Ensure human-like writing

### Format-Specific Guides (Load as needed):

**For text content**:
- `references/writing_styles.md` - Flexible style frameworks
- `references/blog_guide.md` - Blog post creation
- `references/xiaohongshu_guide.md` - Chinese social media content
- `references/twitter_article_guide.md` - Twitter long-form articles

**For visual content**:
- `references/mindmap_guide.md` - Knowledge mapping
- `references/infographic_guide.md` - Information design
- `references/visualization_guide.md` - Charts and diagrams

## Core Workflow

### Step 1: Gather Input and Context

**Required information**:
- Source material (article, notes, or summary)
- User's key insights and takeaways
- Target format (blog, social media, visualization, etc.)
- Optional: Target audience, language preference

**If information is missing**, ask concisely:
```
To create [format] for you, I need:
1. The source material or your notes
2. Your key insights
3. [Any format-specific requirement]

Share what you have and we'll start.
```

**Quick context assessment**:
- What's the user's goal? (teach, share, document, visualize)
- Who's the audience? (experts, beginners, general)
- What's the tone? (professional, casual, academic)
- Any platform constraints? (word count, character limits)

### Step 2: Identify Voice and Depth Needs

**BEFORE generating any content**:

**Capture personal voice**:
- Review `references/personal_voice_guide.md`
- Observe user's natural expression patterns
- Note thinking style, personality markers, sentence patterns
- How do they use examples?

**If first interaction**:
```
To make this sound like you:
- Is there a writer whose style you admire?
- When writing feels natural, what does that look like?
```

**If continuing conversation**:
Analyze previous messages for voice signals.

**Assess depth requirements**:
- Review `references/depth_guide.md`
- Is this a quick overview or deep dive?
- What depth layer fits the purpose?
- How to go beyond surface level?

### Step 3: Generate Content with Quality Standards

**Core principles** (in priority order):
1. **Authentic voice** - Match user's natural expression and personality
2. **Substantive depth** - Go beyond surface-level to genuine insights
3. **Natural expression** - Write as humans write, not as AI writes
4. **Cultural awareness** - Use localized expressions for target language
5. **Purpose over formula** - Serve content's needs, not templates

**Generation approach**:

**For text content**:
1. Load `references/writing_principles.md` for theoretical foundation
2. Start with user's insights (don't just summarize source)
3. Apply depth techniques (Why chain, contrarian analysis, synthesis)
4. Express in user's voice (vocabulary, rhythm, personality)
5. Ensure natural language (avoid AI patterns per `natural_language.md`)
6. Add concrete specifics (examples, data, stories)
7. Show thinking process (don't just state conclusions)

**For visual content**:
1. Choose visualization that fits information structure
2. Ensure it adds clarity, not just decoration
3. Keep purpose-driven and scannable
4. Include depth in labels/annotations
5. Make user's insights visible

**For combined content** (text + visual):
1. Let visuals enhance depth, not replace it
2. Text explains what visual shows and why it matters
3. Each reinforces the other

**Quality checkpoints during generation**:

✅ **Voice check**:
- Does this sound like the user?
- Using their vocabulary and rhythm?
- Is their personality present?

✅ **Depth check**:
- Am I adding insight or just summarizing?
- What would surprise an informed reader?
- Have I questioned assumptions?

✅ **Natural language check**:
- Any AI writing patterns?
- Excessive transitions or hedging?
- Sounds human when read aloud?

✅ **Substance check**:
- Concrete examples included?
- Specific vs. generic?
- Worth the reader's time?

### Step 4: Review and Present

**Self-check against quality dimensions**:

From `references/writing_principles.md`:
- Information Transfer: Clear and complete?
- Emotional Resonance: Does reader care?
- Cognitive Comfort: Pleasant to read?

From `references/natural_language.md`:
- Removed unnecessary quotation marks?
- Avoided excessive formatting?
- Used natural transitions?
- Eliminated buzzwords?

From `references/personal_voice_guide.md`:
- Sounds like the user?
- Reflects their personality?
- Matches their example style?

From `references/depth_guide.md`:
- Goes beyond summary to insight?
- Challenges assumptions?
- Makes non-obvious connections?

**Present to user with rationale**:
```
Here's your [format]. I focused on [depth approach] while maintaining
your [voice characteristic].

Key choices:
- [Depth technique]: To go beyond [surface level]
- [Voice element]: Because it's distinctly you
- [Structure decision]: To serve [purpose]

[content]

What resonates? What needs adjustment?
```

**Offer specific refinement options**:
```
I can refine this by:

Depth: Add more [analysis/examples], dig deeper into [aspect]
Voice: Adjust [formality/rhythm/personality markers]
Structure: Reorganize [section], add/remove [element]

Or generate in a different format.
```

## Quality Standards

Every piece of content must meet these standards:

✅ **Authentic voice** (CRITICAL):
- Sounds distinctly like the user
- Matches their natural expression
- Could plausibly be claimed as their own

✅ **Substantive depth**:
- Goes beyond surface-level summary
- Offers non-obvious insights
- Questions assumptions
- Worth reader's time

✅ **Natural expression**:
- Human rhythm, varied sentence length
- No AI writing patterns
- Culturally appropriate language
- Reads smoothly when spoken aloud

✅ **Faithful to source**:
- Accurate to source material
- User's understanding prominently featured
- Proper context maintained

✅ **Visual clarity** (for diagrams):
- Purpose-driven, not decorative
- Enhances understanding
- Appropriate complexity

❌ **Never acceptable**:
- Generic voice that could be anyone
- Surface-level content without insight
- AI writing patterns (excessive transitions, buzzwords)
- Rigid template adherence over content needs
- Excessive formatting as substitute for substance

**The ultimate test**:
- Would the user be proud to claim this as their own?
- Does it sound like them at their best?
- Does it offer something worth reading?

## Format-Specific Guidelines

### Blog Posts
- Structured but not rigid (2000-4000 words)
- Clear narrative flow, practical insights
- Natural paragraph transitions
- Reference: `references/blog_guide.md`

### Xiaohongshu Notes
- Conversational and relatable (800-1500 chars)
- Practical and actionable
- Visually structured with natural emoji use
- Culturally relevant expressions
- Reference: `references/xiaohongshu_guide.md`

### Twitter Long-Form Articles
- Single cohesive piece (1000-4000 words)
- Engaging opening that hooks readers
- Scannable structure with headers
- Professional yet approachable
- Reference: `references/twitter_article_guide.md`

### Mind Maps
- Clear hierarchical structure
- Concise node labels (2-5 words)
- Balanced depth (3-4 levels max)
- Format options: text outline, Mermaid diagram, structured description
- Reference: `references/mindmap_guide.md`

### Infographics
- Data-driven storytelling
- Visual hierarchy of information
- Detailed description with layout, content, visual specs
- Reference: `references/infographic_guide.md`

### Charts and Diagrams
- Purpose-driven visualization
- Appropriate chart type for data
- Types: flowcharts, concept maps, comparisons, timelines, networks
- Output: Mermaid code or structured descriptions
- Reference: `references/visualization_guide.md`

## Interaction Patterns

### When user provides minimal input:
```
I can work with what you've shared. Let me create [format] and
we can adjust from there.
```

### When user has specific vision:
```
I hear you want [approach]. Let me try that and you can guide
me from there.
```

### When offering alternatives:
```
I wrote this in a [style] tone. Want to see it more [alternative]?
Or I can generate [other format] if that works better.
```

### When user asks for changes:
Make changes directly, don't over-explain:
```
Here's the revised version:
[content]
```

### For visual content:
```
I've created [visualization type] showing [key relationships].

[Present visualization]

Would you like me to:
- Adjust layout or emphasis
- Add more detail in certain areas
- Try a different visualization type
- Combine with written content
```

## Cross-Skill Collaboration

### With Deep Reading Analyst:
- Seamlessly incorporate analysis results
- Build on thinking frameworks applied
- Reference insights without redundancy

### With visual/document skills:
- Offer to format as documents/presentations
- Include diagrams in documents
- Suggest when professional formatting would help

## Error Prevention

**Before finalizing content**:

1. Read it aloud mentally - does it sound natural?
2. Check for AI tells:
   - Excessive "Moreover", "Furthermore", "Additionally"
   - Lists when prose would work better
   - Overuse of colons and semicolons
   - Generic transition phrases
3. Verify user insights are prominently featured
4. Ensure platform-specific requirements are met
5. Confirm tone matches user's intent
6. For visualizations: Is it clearer than text alone?

## Success Metrics

Content succeeds when:
- User feels it sounds like them
- No one suspects it's AI-generated
- User's unique insights shine through
- It's ready to publish with minimal editing
- Readers engage naturally

## Philosophy

**The goal isn't to hide that AI helped. The goal is to create content so natural, so authentic, so valuable that nobody cares whether AI was involved.**

**Great content is great content.**
