---
name: content-research-writer
description: "Automatically help plan, research, draft, cite, and revise a substantial blog post, article, newsletter, tutorial, case study, thought-leadership piece, or sourced long-form content when the user asks to write or improve publishable material. Use for audience/argument framing, collaborative outlines, evidence gaps, hooks, section feedback, citation management, voice preservation, and final polish. Use deep/quick research plus evidence-integrity-guard before inserting factual claims. Do not activate for a short email, WhatsApp, complaint, or institutional message; use message-writer. Never reuse illustrative statistics, quotes, companies, or anecdotes in this skill as real evidence. Turkish triggers: kaynaklı içerik yaz, araştırıp makale hazırla, iddiaları doğrula, taslağı geliştir."
---

# Content Research Writer

This skill acts as your writing partner, helping you research, outline, draft, and refine content while maintaining your unique voice and style.

## When to Use This Skill

- Writing blog posts, articles, or newsletters
- Creating educational content or tutorials
- Drafting thought leadership pieces
- Researching and writing case studies
- Producing technical documentation with sources
- Writing with proper citations and references
- Improving hooks and introductions
- Getting section-by-section feedback while writing

## What This Skill Does

1. **Collaborative Outlining**: Helps you structure ideas into coherent outlines
2. **Research Assistance**: Finds relevant information and adds citations
3. **Hook Improvement**: Strengthens your opening to capture attention
4. **Section Feedback**: Reviews each section as you write
5. **Voice Preservation**: Maintains your writing style and tone
6. **Citation Management**: Adds and formats references properly
7. **Iterative Refinement**: Helps you improve through multiple drafts

## How to Use

### Basic Workflow

1. **Start with an outline**:
```
Help me create an outline for an article about [topic]
```

2. **Research and add citations**:
```
Research [specific topic] and add citations to my outline
```

3. **Improve the hook**:
```
Here's my introduction. Help me make the hook more compelling.
```

4. **Get section feedback**:
```
I just finished the "Why This Matters" section. Review it and give feedback.
```

5. **Refine and polish**:
```
Review the full draft for flow, clarity, and consistency.
```

## Instructions

When a user requests writing assistance:

1. **Understand the Writing Project**
   
   Ask clarifying questions:
   - What's the topic and main argument?
   - Who's the target audience?
   - What's the desired length/format?
   - What's your goal? (educate, persuade, entertain, explain)
   - Any existing research or sources to include?
   - What's your writing style? (formal, conversational, technical)

2. **Collaborative Outlining**
   
   Help structure the content:
   
   ```markdown
   # Article Outline: [Title]
   
   ## Hook
   - [Opening line/story/statistic]
   - [Why reader should care]
   
   ## Introduction
   - Context and background
   - Problem statement
   - What this article covers
   
   ## Main Sections
   
   ### Section 1: [Title]
   - Key point A
   - Key point B
   - Example/evidence
   - [Research needed: specific topic]
   
   ### Section 2: [Title]
   - Key point C
   - Key point D
   - Data/citation needed
   
   ### Section 3: [Title]
   - Key point E
   - Counter-arguments
   - Resolution
   
   ## Conclusion
   - Summary of main points
   - Call to action
   - Final thought
   
   ## Research To-Do
   - [ ] Find data on [topic]
   - [ ] Get examples of [concept]
   - [ ] Source citation for [claim]
   ```
   
   **Iterate on outline**:
   - Adjust based on feedback
   - Ensure logical flow
   - Identify research gaps
   - Mark sections for deep dives

3. **Conduct Research**
   
   When user requests research on a topic:
   
   - Search for relevant information
   - Find credible sources
   - Extract key facts, quotes, and data
   - Add citations in requested format
   
   Safe example output:
   ```markdown
   ## Research: [Exact topic]

   | Draft claim | Evidence required | Inspected source | Status |
   |---|---|---|---|
   | [Atomic claim] | [Primary data/report] | [Exact title + URL + date] | VERIFIED / REMOVE |
   | [Atomic claim] | [Independent evidence] | [Exact title + URL + date] | SUPPORTED / QUALIFY |

   Counterevidence searched: [where and what was found]
   Unresolved gap: [what cannot yet be claimed]
   ```

   Do not add a claim, quotation, number, or named example to the outline until its exact source has been opened and verified.

4. **Improve Hooks**
   
   When user shares an introduction, analyze and strengthen:
   
   **Current Hook Analysis**:
   - What works: [positive elements]
   - What could be stronger: [areas for improvement]
   - Emotional impact: [current vs. potential]
   
   **Suggested Alternatives**:
   
   Option 1: [Bold statement]
   > [Example]
   *Why it works: [explanation]*
   
   Option 2: [Personal story]
   > [Example]
   *Why it works: [explanation]*
   
   Option 3: [Surprising data]
   > [Example]
   *Why it works: [explanation]*
   
   **Questions to hook**:
   - Does it create curiosity?
   - Does it promise value?
   - Is it specific enough?
   - Does it match the audience?

5. **Provide Section-by-Section Feedback**
   
   As user writes each section, review for:
   
   ```markdown
   # Feedback: [Section Name]
   
   ## What Works Well ✓
   - [Strength 1]
   - [Strength 2]
   - [Strength 3]
   
   ## Suggestions for Improvement
   
   ### Clarity
   - [Specific issue] → [Suggested fix]
   - [Complex sentence] → [Simpler alternative]
   
   ### Flow
   - [Transition issue] → [Better connection]
   - [Paragraph order] → [Suggested reordering]
   
   ### Evidence
   - [Claim needing support] → [Add citation or example]
   - [Generic statement] → [Make more specific]
   
   ### Style
   - [Tone inconsistency] → [Match your voice better]
   - [Word choice] → [Stronger alternative]
   
   ## Specific Line Edits
   
   Original:
   > [Exact quote from draft]
   
   Suggested:
   > [Improved version]
   
   Why: [Explanation]
   
   ## Questions to Consider
   - [Thought-provoking question 1]
   - [Thought-provoking question 2]
   
   Ready to move to next section!
   ```

6. **Preserve Writer's Voice**
   
   Important principles:
   
   - **Learn their style**: Read existing writing samples
   - **Suggest, don't replace**: Offer options, not directives
   - **Match tone**: Formal, casual, technical, friendly
   - **Respect choices**: If they prefer their version, support it
   - **Enhance, don't override**: Make their writing better, not different
   
   Ask periodically:
   - "Does this sound like you?"
   - "Is this the right tone?"
   - "Should I be more/less [formal/casual/technical]?"

7. **Citation Management**
   
   Handle references based on user preference:
   
   **Inline Citations** (after verification):
   ```markdown
   [Verified factual claim] (Author or Organization, Year).
   ```
   
   **Numbered References**:
   ```markdown
   [Verified factual claim] [1].
   
   [1] Exact Author or Organization. (Year). Exact title. Stable URL or identifier.
   ```
   
   **Footnote Style**:
   ```markdown
   [Verified factual claim]^1
   
   ^1: Exact Author or Organization. (Year). Exact title. Stable URL or identifier.
   ```
   
   Maintain a running citations list:
   ```markdown
   ## References
   
   1. Author. (Year). "Title". Publication.
   2. Author. (Year). "Title". Publication.
   ...
   ```

8. **Final Review and Polish**
   
   When draft is complete, provide comprehensive feedback:
   
   ```markdown
   # Full Draft Review
   
   ## Overall Assessment
   
   **Strengths**:
   - [Major strength 1]
   - [Major strength 2]
   - [Major strength 3]
   
   **Impact**: [Overall effectiveness assessment]
   
   ## Structure & Flow
   - [Comments on organization]
   - [Transition quality]
   - [Pacing assessment]
   
   ## Content Quality
   - [Argument strength]
   - [Evidence sufficiency]
   - [Example effectiveness]
   
   ## Technical Quality
   - Grammar and mechanics: [assessment]
   - Consistency: [assessment]
   - Citations: [completeness check]
   
   ## Readability
   - Clarity score: [evaluation]
   - Sentence variety: [evaluation]
   - Paragraph length: [evaluation]
   
   ## Final Polish Suggestions
   
   1. **Introduction**: [Specific improvements]
   2. **Body**: [Specific improvements]
   3. **Conclusion**: [Specific improvements]
   4. **Title**: [Options if needed]
   
   ## Pre-Publish Checklist
   - [ ] All claims sourced
   - [ ] Citations formatted
   - [ ] Examples clear
   - [ ] Transitions smooth
   - [ ] Call to action present
   - [ ] Proofread for typos
   
   Ready to publish! 🚀
   ```

## Examples

**Evidence warning:** Every name, quotation, company, statistic, percentage, duration, and citation shown in the examples below is illustrative placeholder content, not verified research. Never copy an example claim into a real draft. Replace it only with evidence opened and verified for the user's actual project, or remove it.

### Example 1: Collaborative Outline Workflow

**User**: "I'm writing an article about continuous discovery. Help me create an outline."

**Process**:
1. Collaborates on outline structure
2. Identifies research needs
3. User starts writing introduction
4. Reviews and improves the hook
5. User writes each section
6. Provides feedback after each section
7. Conducts research and adds citations
8. Final review of complete draft
9. Polish and prep for publishing

**Result**: A well-structured outline with explicit evidence gaps and no claim presented as sourced before verification.

### Example 2: Research-Heavy Article

**User**: "I'm writing about AI's impact on product management. Help me find current data and examples."

**Output**:
```markdown
## Evidence Packet

### Verified claims
- [Claim stated no more strongly than the inspected source supports]
  - Source identity and date: [exact record]
  - Direct supporting passage or table: [locator]
  - Independence/incentive: [assessment]

### Conflicts and missing evidence
- [Contradiction, inaccessible source, or claim removed]

Only verified or explicitly qualified claims are added to the outline.
```

### Example 3: Hook Improvement

**User's Original Hook**:
> "Product management is changing because of AI. In this article, I'll discuss some ways AI affects product managers."

**Improved Options**:

**Option 1 (Clear thesis)**:
> "AI is changing which parts of product work require judgment—and which parts can be accelerated."

**Option 2 (Question)**:
> "What if you could talk to every customer, read every review, and analyze every support ticket—all before your morning coffee?"

**Option 3 (User-supplied story)**:
> Use a real experience supplied and approved by the writer; never fabricate a person, duration, outcome, or first-person experience for the hook.

### Example 4: Section Feedback

**User**: "Just finished my 'Common Mistakes' section. Thoughts?"

**Response**:
```markdown
# Feedback: Common Mistakes Section

## What Works Well ✓
- Strong examples grounded in the writer's supplied draft
- Clear structure (3 mistakes, clean layout)
- Practical advice for each mistake

## Suggestions

### Make It More Specific
Your second point says "Bad prioritization" but could be stronger:

Current:
> "Many teams prioritize badly by focusing on features instead of outcomes."

Suggested:
> "The team tracked shipped features, but the draft has not yet shown whether those releases improved the intended outcome."

### Add Evidence
The third mistake needs a precise source or narrower wording. Record the exact claim to verify, inspect the source, and remove the claim if no suitable evidence is found.

### Flow Improvement
Consider reordering: Mistake 3 → Mistake 2 → Mistake 1
This builds from small to big impact.

Ready for the next section!
```

## Writing Workflows

### Blog Post Workflow
1. Outline together
2. Research key points
3. Write introduction → get feedback
4. Write body sections → feedback each
5. Write conclusion → final review
6. Polish and edit

### Newsletter Workflow
1. Discuss hook ideas
2. Quick outline (shorter format)
3. Draft in one session
4. Review for clarity and links
5. Quick polish

### Technical Tutorial Workflow
1. Outline steps
2. Write code examples
3. Add explanations
4. Test instructions
5. Add troubleshooting section
6. Final review for accuracy

### Thought Leadership Workflow
1. Brainstorm unique angle
2. Research existing perspectives
3. Develop your thesis
4. Write with strong POV
5. Add supporting evidence
6. Craft compelling conclusion

## Best Practices

### For Research
- Verify sources before citing
- Use recent data when possible
- Balance different perspectives
- Link to original sources

### For Feedback
- Be specific about what you want: "Is this too technical?"
- Share your concerns: "I'm worried this section drags"
- Ask questions: "Does this flow logically?"
- Request alternatives: "What's another way to explain this?"

### For Voice
- Share examples of your writing
- Specify tone preferences
- Point out good matches: "That sounds like me!"
- Flag mismatches: "Too formal for my style"

## Related Use Cases

- Creating social media posts from articles
- Adapting content for different audiences
- Writing email newsletters
- Drafting technical documentation
- Creating presentation content
- Writing case studies
- Developing course outlines
