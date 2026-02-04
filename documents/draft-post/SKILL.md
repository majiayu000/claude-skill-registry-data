---
name: draft-post
description: Guide the user through creating a blog post draft for Substack (200-500 words) and LinkedIn (100-300 words). Use when user wants to draft a post or share work.
---

# Draft Post Skill

## Purpose
Help users quickly create polished blog posts for Substack and LinkedIn based on their recent work, without spending hours writing and reformatting.

## Instructions

### Introduction Phase
When the user says "Draft a post" or similar, start warmly:
- "Great! Let's draft a post about your work. I'll ask you a few questions to gather the key points, then create three versions: one for Substack, one for LinkedIn, and a restack note for Substack."

### Step 1: Gather Content

Ask each question **one at a time**, wait for the response, then acknowledge before moving to the next:

**Q1: Topic/Work**
- Ask: "What have you been working on that you'd like to write about?"
- Provide example: "For instance: 'I've been setting up a cross-platform agent skills repository' or 'I built a new feature for handling CSV anonymization'"
- If vague, ask follow-up questions for specificity

**Q2: Why Interesting**
- Ask: "What makes this interesting or worth sharing? What problem does it solve or what insight did you gain?"
- Encourage personal perspective: "What excited you about this work or what did you learn?"

**Q3: Key Points**
- Ask: "What are 2-3 key points or takeaways you want readers to understand?"
- Help them identify the most important aspects

**Q4: Technical Details (Optional)**
- Ask: "Are there any specific technical details, links, or resources that should be included?"
- This might include GitHub repos, documentation links, code snippets, etc.

**Q5: Tone/Style**
- Ask: "What tone would you like? (conversational, technical, tutorial-style, reflective, etc.)"
- Default to conversational if they're unsure

## General Formatting (applies to all content)

- Use backticks for inline code (file paths, directory names, commands, variable names, etc.)
- Use code blocks for multi-line code examples
- Do NOT indent paragraphs
- Keep paragraphs left-aligned

### Step 2: Create Substack Draft (250-500 words)

Based on their answers:
1. Draft a Substack post (250-500 words, aim for 300-400)
2. Include:
   - Title (engaging and descriptive)
   - Subtitle (expands on the title, provides context)
   - Engaging opening hook
   - Clear explanation of the work/topic
   - The key points they identified
   - Personal insights or learnings
   - Any technical details or links mentioned
   - Conversational, accessible tone (unless they specified otherwise)
3. Show word count at the end
4. Present the draft clearly with markdown formatting

### Step 3: Get Approval

After showing the Substack draft:
- Ask: "How does this look? Would you like me to revise anything before I create the LinkedIn version?"
- If they want changes, revise and re-present
- If approved, proceed to Step 4

### Step 4: Create LinkedIn Summary (100-150 words)

Once Substack version is approved:
1. Create a LinkedIn summary (100-150 words) based on the approved Substack post
2. This should be:
   - Open with the hook/problem from Substack
   - Present the solution directly and concisely
   - Share personal results/benefits using "I" statements
   - End casually with "In case anyone is interested, I've put [description] on GitHub. Link in the comments."
   - Professional but conversational tone
   - **NO external links in the main post body** (LinkedIn algorithm penalises posts with links)
   - Omit code blocks (can be included in first comment if needed)
3. If there are links (GitHub repo, documentation, etc.):
   - Reference at the end: "In case anyone is interested, I've put [description] on GitHub. Link in the comments."
   - DO NOT include any URLs in the main post body
   - Place the actual URL ONLY in the "First comment" section at the very end
4. Show word count at the end
5. Present the LinkedIn version with the link separated at the bottom

### Step 5: Create Substack Restack Commentary

Once both versions are approved:
1. Create a short restack note (2-4 sentences) for promoting the Substack post on Notes
2. This should:
   - Highlight a "screenshot moment" - the most quotable or compelling point from the post
   - Add your own perspective or why this matters
   - Ask a question or invite engagement
   - Be conversational and authentic
3. Keep it brief and punchy
4. Present the restack commentary

### Step 6: Final Confirmation

- Ask: "Are all three versions ready to go, or would you like any adjustments?"
- Make any requested changes
- Confirm completion when they're satisfied

## Tone & Style
- Be encouraging and efficient
- Don't overthink or over-question
- Move through the process briskly but thoroughly
- Celebrate their work and make the process enjoyable
- Acknowledge their answers warmly before moving on

## When to Use This Skill
- User says "Draft a post", "Write a blog post", "Create an article"
- User wants to share recent work on Substack or LinkedIn
- User mentions wanting to post about something they've done

## Output Format

**Substack Draft:**
```
[Title]
[Subtitle]

[Post content 250-500 words, aim for 300-400]

Word count: [X] words
```

**LinkedIn Summary:**
```
[Post content]

Word count: [X] words

---
First comment (post this after publishing):
[URL links here]
[Optional: code blocks if omitted from main post]
```

**Substack Restack Commentary:**
```
[2-4 sentences highlighting key insight + your perspective + engagement hook]

Use this when restacking your Substack post to Notes.
```

## Notes
- Focus on making the process quick and painless
- The goal is frequent posting, not perfection
- Help them find what's interesting about their work
- Encourage personal voice and insights
