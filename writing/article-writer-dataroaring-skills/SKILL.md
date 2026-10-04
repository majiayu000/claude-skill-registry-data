---
name: Article Writer & Reviewer
description: This skill should be used when the user asks to "write an article", "help me write a blog post", "draft a technical article", "review my article", "check my writing", "improve this draft", "give me writing feedback", "find a topic", "what should I write about", or mentions "writing coach". Provides comprehensive guidance including topic selection, 15 writing skills, and reviewer collaboration from "Writing for Developers".
---

# Technical Article Writing Coach

A writing coach skill that guides users through writing and reviewing technical articles using the methodology from "Writing for Developers" by Piotr Sarna & Cynthia Dunlop.

## When to Use This Skill

- User wants to write a new technical article or blog post
- User wants feedback or review on an existing draft
- User asks for writing guidance or coaching
- User mentions improving their technical writing

## Topic Selection (Before Everything)

**The 3 Ps Test** - Does your topic meet at least one?
- **Proud of** - Accomplishments you're eager to show off
- **Pained by** - Challenges that caused constant headaches
- **Passionate about** - What gets your blood racing

If you're not personally proud, pained, or passionate about the topic, the blog post won't yield great results.

See `references/topic-selection.md` for topic idea sources and testing methods.

## The 15 Writing Skills

Apply these skills in order based on the user's stage:

### Pre-Writing Phase

**1. Goal Definition** - Before writing, establish:
- "The goal of this article is to..." (never published)
- "My perspective is interesting because..." (never published)
- Who is the target reader? What do they already know?
- What should they think or do differently after reading?

**2. Pattern Selection** - Match content to the right structure:

| Content Type | Pattern |
|-------------|---------|
| Finding/fixing a tricky bug | Bug Hunt |
| Migrating to new language/framework | Rewrote It in X |
| Significant technical project | How We Built It |
| Hard-won wisdom from experience | Lessons Learned |
| Opinion on industry direction | Thoughts on Trends |
| Educational content with product | Non-markety Product |
| Performance data/comparisons | Benchmarks |

### Writing Phase

**3. Evidence-Based Claims** - Support every statement:
- "Impressive performance" → Show benchmark numbers
- "X is better than Y" → Show code comparison
- "It's difficult" → Explain specific challenges

**4. Conversational Voice** - Write authentically:
- Use "I/we" for author, "you" for reader
- Contractions are fine
- Share frustrations, mistakes, what you don't know
- See `references/human-voice.md` for avoiding AI-sounding writing

**5. Single-Idea Paragraphs** - Keep it clear:
- One idea per paragraph
- If out of breath reading aloud, sentence is too long
- Replace weak "to be" verbs with action verbs

**6. Scannability** - Make it easy to read:
- Headings every 2+ scrolls
- Bold key points
- Use lists and tables
- No massive paragraph blocks

**7. Show Don't Tell** - Use concrete examples:
- Code snippets (legible, syntax-highlighted)
- Diagrams for architecture/flow
- Specific numbers, not vague claims

**8. Actionable Writing** - Don't make reader think:
- Replace "it depends" with specific conditions
- Give decision criteria, not requirements lists
- Provide recognition signals, not abstract descriptions
- Answer "How do I know when?" for every claim
- See `references/actionable-writing.md` for transformation examples

### Review Phase (The 3 F's)

**9. Facts Check** - For each arguable statement:
- Is it supported by evidence?
- Are there specific numbers, code, benchmarks?
- Would a skeptical reader trust this?

**10. Focus Check** - For every paragraph:
- Does this advance the stated goal?
- Can this be cut without losing value?
- Is there off-topic rambling?

**11. Flow Check** - Overall structure:
- Logical progression from start to end?
- Smooth transitions between sections?
- Would a reader get lost anywhere?

**12. Component Review** - Check each element:
- **Title**: Short (<60 chars)? Keywords upfront? Intriguing?
- **Introduction**: States what reader gets? Why your perspective matters?
- **Headings**: Descriptive and scannable?
- **Ending**: Ties up nicely? Clear path forward?
- **Code**: Legible? Syntax highlighted? Copy-pasteable?
- **Visuals**: Helpful? Properly sized?

**13. Pattern-Specific Review** - Apply criteria for chosen pattern:
- See `references/pattern-reviews.md` for detailed criteria

**14. Pre-Publish Verification** - Technical checks:
- Title renders well in template
- All links work
- Code is legible and copy-pasteable
- Images properly sized
- Keywords in meta description
- URL is clean and includes keywords

**15. Self-Review Test** - Final questions:
- Would I share this if someone else wrote it?
- Can a skeptical reader trust my claims?
- Does every section advance my stated goal?
- Is the key takeaway clear within first few paragraphs?

## Human Voice Check (Avoiding AI-Sounding Writing)

When reviewing, check for these AI red flags:
- Unusually dense/consistent metaphors throughout
- Overly flowery, consistently ornate prose
- Lack of specific technical details
- Artificial emotional arc (curiosity → challenge → triumph)
- No genuine personal anecdotes with specific details
- **Excessive em dashes (—)** - Multiple per paragraph is a classic AI tell

### Em Dash Warning

Em dashes are a major AI-writing red flag. Limit to 1-2 per entire article.

**Fix:** Replace em dashes with periods, commas, or parentheses:
- ❌ "The system—which handles millions—was failing"
- ✅ "The system handles millions of requests. It was failing."

To sound human:
- Include specific, idiosyncratic details from real experience
- Let voice vary naturally (not perfectly consistent)
- Admit mistakes, uncertainties, frustrations
- Share what you were thinking/feeling at key moments
- Include at least one self-deprecating comment

**Test:** Would a close friend recognize your personality in this writing?

See `references/human-voice.md` for detailed guidance and examples.

## Working with Reviewers

**Selecting reviewers:**
- Technical reviewer (knows subject matter)
- Clarity reviewer (unfamiliar with topic - catches assumptions)

**Preparing reviewers:**
- Provide background on goal and target reader
- Specify what feedback you want
- Highlight sections you're uncertain about

**Responding to comments:**
- Address every comment (even if just "noted")
- Don't argue with every suggestion
- Consider feedback, don't just react

See `references/working-with-reviewers.md` for detailed guidance.

## Workflow for Writing New Articles

When user wants to write a new article:

1. **Ask Goal Definition questions** (Skill 1):
   - What is the goal of this article?
   - Why is your perspective interesting/unique?
   - Who is your target reader?
   - What should they do differently after reading?

2. **Help select pattern** (Skill 2):
   - Based on their content, recommend appropriate pattern
   - See `references/patterns.md` for detailed pattern guides

3. **Guide drafting** (Skills 3-8):
   - Ensure claims have evidence
   - Check voice is conversational
   - Verify structure is scannable
   - Make content actionable (not abstract)

4. **Review draft** (Skills 9-15):
   - Apply the 3 F's: Facts, Focus, Flow
   - Check components
   - Apply pattern-specific review

## Workflow for Reviewing Existing Articles

When user has a draft to review:

1. **Read the draft** to understand content and pattern

2. **Apply the 3 F's** (Skills 9-11):
   - Facts: Flag unsupported claims
   - Focus: Identify off-topic sections
   - Flow: Check logical progression

3. **Component Review** (Skill 12):
   - Evaluate title, intro, headings, ending, code, visuals

4. **Pattern-Specific Review** (Skill 13):
   - Consult `references/pattern-reviews.md`

5. **Provide actionable feedback**:
   - Prioritize most impactful improvements
   - Give specific suggestions, not vague criticism

## Coaching Prompts

Use these when user is stuck:

**Stuck starting:**
> "Don't worry about the introduction. Start with the most interesting technical part. What's the one thing you most want to share?"

**Too much content:**
> "Go back to your goal statement. Does this paragraph advance that goal? If not, cut it."

**Doubts expertise:**
> "You're the world's expert on YOUR specific experience. Share what you learned, what surprised you, what you'd do differently."

**Wants perfection:**
> "There's no value in letting a technical article age in a dark cellar. Get it published before industry shifts make it less relevant."

## Additional Resources

### Reference Files

For detailed guidance, consult:
- **`references/topic-selection.md`** - The 3 Ps test, topic idea sources, testing topics
- **`references/patterns.md`** - Detailed guide for each blog post pattern
- **`references/pattern-reviews.md`** - Pattern-specific review criteria
- **`references/writing-skills-complete.md`** - Full skills reference
- **`references/actionable-writing.md`** - Transform abstract → actionable content
- **`references/human-voice.md`** - How to sound human, not AI-generated
- **`references/native-english-style.md`** - Sentence optimization, clarity, and native English style
- **`references/seo-metadata.md`** - Keywords, title tags, meta descriptions, URLs, Open Graph
- **`references/visual-code-presentation.md`** - Headings, images, code examples, tables
- **`references/working-with-reviewers.md`** - Selecting, preparing, and responding to reviewers

### Examples

Working examples in `examples/`:
- **`examples/goal-definition.md`** - Example goal definition exercise
- **`examples/review-checklist.md`** - Practical review checklist
