---
name: mindwork-summary
description: Generate summaries of therapy sessions and journal entries at various lengths and for different audiences. Supports action item extraction, highlights reels, and session prep. Use for quick recaps, sharing with others, or preparing for your next session.
---

# Session & Journal Summarizer

Part of the **mindwork** suite. Condenses sessions and journals into digestible formats for quick reference and sharing.

## What It Does

1. **Condenses** content to requested length
2. **Tailors** output for different audiences
3. **Extracts** action items and highlights
4. **Prepares** you for upcoming sessions

## Key Difference from Analyze

| Skill | Focus | Output |
|-------|-------|--------|
| `analyze` | Deep dive - WHY and HOW | Patterns, themes, insights |
| `summary` | Quick reference - WHAT | Condensed key points |

**Summary gives you the "what happened", analyze gives you the "what it means".**

---

## Length Options

### 1. One-Liner

Single sentence capturing the essence.

**Example prompts:**
> "Give me a one-liner for today's session"
> "Summarize this journal entry in one sentence"

**Output example:**
> "Discussed work anxiety and practiced a new breathing technique for deadline stress."

### 2. Paragraph

3-5 sentences covering key points.

**Example prompts:**
> "Give me a paragraph summary of the last session"
> "Summarize this in a few sentences"

**Output example:**
> "This session focused on recurring anxiety around work deadlines. We explored how perfectionism drives procrastination, and identified a pattern of catastrophizing when projects pile up. I learned a new breathing technique to use before opening stressful emails. Homework: try the technique 3 times this week and journal about it."

### 3. Full Page

Comprehensive summary with sections.

**Example prompts:**
> "Give me a full summary of this session"
> "Detailed summary with action items"

**Output template:**
```markdown
# Session Summary: {Date}

## Main Topics
- Topic 1
- Topic 2

## Key Discussions
- What was explored
- Connections made
- Insights that emerged

## Techniques/Tools
- Technique learned
- How to apply it

## Action Items
- [ ] Homework item 1
- [ ] Homework item 2

## Notable Quotes
- "Meaningful quote from session"

## Emotional Highlights
- Key emotional moment
```

---

## Audience Options

### For Self (default)

Full detail, personal language, includes vulnerable moments.

**Example prompts:**
> "Summarize this session"
> "What happened in today's session?"

### For Therapist

Focus on what happened since last session, what worked/didn't, questions to explore.

**Example prompts:**
> "Create an update for my therapist"
> "Summarize what to tell my therapist"

**Output template:**
```markdown
# Update for Therapist: Since {Last Session Date}

## What I Worked On
- Homework attempted
- Techniques practiced

## What Helped
- What worked well
- Positive observations

## What Was Hard
- Challenges encountered
- Struggles to discuss

## Questions/Topics for Next Session
- Question 1
- Topic to explore
```

### For Sharing

High-level, non-clinical language, focuses on growth and how others can support.

**Example prompts:**
> "Summarize this for my partner"
> "What can I share about today's session?"

**Output example:**
> "Had a good session about work stress. Learning that my perfectionism might actually be causing my procrastination. Trying a new breathing technique this week before checking work emails. Could use support remembering to do it!"

**Guidelines for sharing summaries:**
- Use everyday language, not therapy jargon
- Focus on growth and positive steps
- Include specific ways others can help
- Omit deeply personal or vulnerable details

---

## Special Modes

### Action Items

Extract homework, techniques to try, and next steps.

**Example prompts:**
> "What are my action items from the last session?"
> "List all homework from this month's sessions"
> "What should I be practicing?"

**Output template:**
```markdown
# Action Items

## From {Date} Session
- [ ] Action item 1
- [ ] Action item 2

## From {Date} Session
- [ ] Action item 1
```

**What counts as an action item:**
- Explicit homework from therapist
- Techniques to practice
- Things to notice or track
- Journaling prompts
- Conversations to have
- Behaviors to try

### Highlights Reel

Key quotes, breakthroughs, and emotional moments.

**Example prompts:**
> "Show me highlights from this month's sessions"
> "What were the breakthrough moments?"
> "What were my best quotes from recent sessions?"
> "Highlights from my dream logs this month"

**Output template:**
```markdown
# Highlights: {Period}

## Breakthroughs
- {Date}: Brief description

## Powerful Moments
- Realization or connection

## Key Quotes
- "Something meaningful I said"

## Techniques That Clicked
- Technique that resonated
```

**What counts as a highlight:**
- First-time realizations
- Emotional breakthroughs
- Connections between patterns
- Memorable self-observations
- Moments of growth or self-compassion

### Session Prep

Prepare for your next session with a recap and topics to discuss.

**Example prompts:**
> "Prep me for my session tomorrow"
> "What should I discuss in my next session?"
> "Help me prepare for therapy"

**Output template:**
```markdown
# Session Prep: {Upcoming Date}

## Last Session Recap
- Main topics covered
- Techniques learned
- Homework assigned

## Since Then
- What I practiced
- What came up
- Notable events

## Topics to Consider
- How homework went
- New patterns noticed
- Questions that arose

## Questions I Have
- Specific question 1
- Topic I want to explore
```

**Data sources for session prep:**
1. Last session transcript/analysis
2. Journal entries since last session
3. Previous action items (what's done/not done)

---

## Usage Examples

### Quick Recap
> "One-liner for today's session"

Claude reads the session and returns a single sentence summary.

### Detailed Summary
> "Full summary of transcriptions/2024-01-15-session.md"

Claude generates a comprehensive summary with all sections.

### For Partner
> "Summarize today's session for my partner"

Claude creates a sharing-friendly version without clinical language.

### Action Item Review
> "What action items do I have from the last 3 sessions?"

Claude reads recent sessions and compiles all homework/techniques.

### Monthly Highlights
> "Highlights from January"

Claude reviews all January sessions and extracts breakthroughs and quotes.

### Pre-Session Prep
> "Prep me for tomorrow's session"

Claude compiles last session recap, recent journals, and suggested topics.

### Journal Type Summaries
> "Summarize my dream logs from this week"
> "What themes appeared in my gratitude entries this month?"
> "Give me a one-liner for each anxiety journal entry from January"

Claude filters to the specified journal type and generates summaries with context from the journal description.

---

## Output Location

Summaries can be:
1. **Returned directly** (default) - displayed in conversation
2. **Saved to file** - when user specifies

If saving, use `summaries/` folder:
- `summaries/2024-01-15-session-summary.md`
- `summaries/2024-01-therapist-update.md`
- `summaries/2024-01-highlights.md`

---

## Notes

### Privacy Considerations

**For sharing summaries:**
- Ask before including specific details
- Default to less detail when in doubt
- Never include therapist's direct guidance without consent

### Combining with Other Skills

Summary works well after other skills:
- After `analyze`: "Now give me a one-liner"
- After `progress`: "Summarize the key trends"
- With `insights`: "Summarize my profile for sharing"

### Length Detection

If user doesn't specify length, infer from context:
- "Quick summary" → paragraph
- "Full summary" → full page
- "What happened?" → paragraph
- "Detailed summary" → full page

### Journal Type Handling

When summarizing journals, check `mindwork.yaml` for journal type context:

1. **Match the file path** to a configured journal source
2. **Use the description** to provide context in summaries
3. **Tailor the summary** based on journal type:
   - Dream logs: Focus on imagery, symbols, emotional themes
   - Gratitude entries: Highlight what brought joy, patterns in appreciation
   - Daily reflections: Key mood/events, notable thoughts
   - Anxiety tracking: Triggers identified, coping used

**Include journal type in output:**
```markdown
# Summary: {Date}
**Source**: {journal type description}

{Summary content tailored to the journal type}
```
