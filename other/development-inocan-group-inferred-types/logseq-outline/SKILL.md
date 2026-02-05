---
name: logseq-outline
description: Format any content as a Logseq-compatible outline using nested bullets (no markdown headers, no bold). Works in both Claude Code and Claude Desktop.
---

# Logseq Outline Formatting Skill

Format notes, lists, or any structured content as Logseq-compatible outlines. Uses nested bullet points (outline hierarchy) instead of markdown headers, with plain text styling.

## When to Use This Skill

Use this skill when the user needs to format content for Logseq:
- Structured notes or outlines
- Research summaries
- Reading lists
- Project documentation
- Meeting notes
- Any hierarchical content for import into Logseq

**Key indicator phrases:**
- "Format this for Logseq"
- "Create a Logseq outline"
- "Make this Logseq-compatible"
- "Save this to paste into Logseq"
- "Format as an outline" (when context suggests Logseq)

## Core Formatting Philosophy

**Logseq uses outline hierarchy, not markdown headers.**

- ✓ Use nested bullet points with tabs/spaces for indentation
- ✓ Use plain text throughout (no bold, no italics unless semantically required)
- ✓ Use proper markdown links for URLs
- ✓ Organize by nesting depth, not visual styling
- ✗ Never use `#` markdown headers
- ✗ Never use bold (`**text**`) for emphasis
- ✗ Never use horizontal rules (`---`)

## Universal Logseq Formatting Rules

### Structure

**Hierarchy through nesting only:**
```
- Top Level Item
	- Second Level Item
		- Third Level Item
			- Fourth Level Item
```

**Never use headers:**
```
❌ WRONG:
# Main Topic
## Subtopic

✓ CORRECT:
- Main Topic
	- Subtopic
```

### Text Styling

**Plain text only:**
```
❌ WRONG:
- **Important Item**
- *Emphasized point*

✓ CORRECT:
- Important Item
- Emphasized point
```

**Exception:** Use bold/italics only when semantically meaningful (e.g., book titles, technical terms), not for visual emphasis.

### Links

**Use proper markdown links:**
```
✓ CORRECT:
- Item with link: [Link Text](https://example.com)
- Reference: [Document Name](file:///path/to/file.pdf)
```

### Lists and Sub-items

**Use consistent indentation:**
```
- Main point
	- Supporting detail
		- Further detail
		- Another detail
	- Another supporting detail
- Next main point
```

## What NOT to Include

**Avoid these common mistakes:**

- ❌ **No markdown headers** (`#`, `##`, `###`) - use nested bullets instead
- ❌ **No bold styling** (`**text**`) for emphasis - use plain text
- ❌ **No summary sections** at the end (no totals, no statistics)
- ❌ **No horizontal rules** (`---`) for section breaks
- ❌ **No item counts** ("Total: 23 items") at the end
- ❌ **No meta-commentary** ("Organized by themes", "Sources include...")

## Output Format by Environment

### Claude Desktop

**Create a markdown artifact** containing the Logseq-formatted outline.

- Use artifact format for easy copying
- User can copy and paste directly into Logseq
- No file system access needed

### Claude Code

**Save to file and open in BBEdit** for review.

**Steps:**
1. **Location:** Save to Desktop
   - Path: `/Users/niyaro/Desktop/`
2. **Filename:** Descriptive name with topic
   - Format: `Topic_Name_Outline.md`
   - Example: `Research_Notes.md`
3. **Extension:** Always use `.md` (markdown)
4. **Open in editor:**
   - Command: `bbedit /path/to/file.md`
5. **Confirm to user:** Report filename and location

**Example:**
```bash
# Save file
cat > /Users/niyaro/Desktop/Research_Notes.md <<'EOF'
- Research Topic
	- Key Points
		- Point 1
		- Point 2
	- Next Steps
		- Action 1
		- Action 2
EOF

# Open in BBEdit
bbedit /Users/niyaro/Desktop/Research_Notes.md
```

## Common Use Cases

### Use Case 1: Research Notes

**User request:** "Create a Logseq outline of my research notes"

**Output structure:**
```
- Research Project: [Topic]
	- Background
		- Key concept 1
			- Definition
			- Examples
		- Key concept 2
			- Definition
			- Examples
	- Findings
		- Finding 1
			- Evidence
			- Source
		- Finding 2
			- Evidence
			- Source
	- Next Steps
		- Action item 1
		- Action item 2
```

### Use Case 2: Reading List

**User request:** "Make a Logseq-formatted reading list"

**Output structure:**
```
- Reading List: [Topic]
	- Must Read
		- Book Title, Author (Year)
			- Why read: reason
			- Length: X pages
		- Another Book, Author (Year)
			- Why read: reason
	- Recommended
		- Book Title, Author (Year)
			- Why read: reason
	- Optional
		- Book Title, Author (Year)
```

### Use Case 3: Meeting Notes

**User request:** "Format these meeting notes for Logseq"

**Output structure:**
```
- Meeting: [Date] - [Topic]
	- Attendees
		- Person 1
		- Person 2
	- Discussion Points
		- Topic 1
			- Decision: action decided
			- Owner: person responsible
		- Topic 2
			- Decision: action decided
	- Action Items
		- Item 1 (Owner: Person)
			- Due: date
		- Item 2 (Owner: Person)
```

### Use Case 4: Project Plan

**User request:** "Create a Logseq outline for my project"

**Output structure:**
```
- Project: [Name]
	- Goals
		- Goal 1
		- Goal 2
	- Milestones
		- Phase 1: [Name]
			- Task 1
			- Task 2
		- Phase 2: [Name]
			- Task 3
			- Task 4
	- Resources
		- Resource 1
		- Resource 2
	- Risks
		- Risk 1
			- Mitigation: plan
```

## Converting Existing Content

### From Markdown with Headers

**Input:**
```markdown
# Main Topic

## Subtopic 1
Content here

## Subtopic 2
More content
```

**Output:**
```
- Main Topic
	- Subtopic 1
		- Content here
	- Subtopic 2
		- More content
```

### From Bold-Heavy Format

**Input:**
```markdown
- **Section 1**
  - **Point 1:** Details
  - **Point 2:** More details
```

**Output:**
```
- Section 1
	- Point 1: Details
	- Point 2: More details
```

### From Flat List to Hierarchy

**Input:**
```
- Item 1
- Item 1a (related to Item 1)
- Item 1b (related to Item 1)
- Item 2
- Item 2a (related to Item 2)
```

**Output:**
```
- Item 1
	- Item 1a
	- Item 1b
- Item 2
	- Item 2a
```

### From Numbered Lists

**Input:**
```
1. First main point
   1.1 Sub-point
   1.2 Another sub-point
2. Second main point
```

**Output:**
```
- First main point
	- Sub-point
	- Another sub-point
- Second main point
```

## Quality Checklist

Before delivering Logseq-formatted content, verify:

- [ ] Uses nested bullets (tabs/indentation), not headers
- [ ] No bold styling except when semantically required
- [ ] All links use proper markdown format `[text](url)`
- [ ] No summary sections at the end
- [ ] No horizontal rules or visual separators
- [ ] **Claude Code only:** File saved to Desktop with `.md` extension
- [ ] **Claude Code only:** File opened in BBEdit for user review
- [ ] **Claude Code only:** Confirmed filename and location to user

## Examples

### Complete Research Notes Example

```
- Embodied Cognition Research Notes
	- Core Concepts
		- Embodiment
			- Definition: Cognitive processes are deeply rooted in the body's interactions with the world
			- Key theorists: Lakoff, Johnson, Varela
		- Grounded Cognition
			- Definition: Mental representations are grounded in sensory-motor experiences
			- Key theorists: Barsalou
	- Key Studies
		- Lakoff & Johnson, 1980. Metaphors We Live By
			- Main argument: Abstract concepts structured by bodily experiences
			- Example: "Argument is war" metaphor
		- Varela et al., 1991. The Embodied Mind
			- Main argument: Mind emerges from body-environment interaction
			- Approach: Enactivist perspective
	- Applications
		- Education
			- Gesture-based learning
			- Physical manipulation in math education
		- Robotics
			- Embodied AI systems
			- Sensorimotor grounding
```

### Complete Project Plan Example

```
- Website Redesign Project
	- Objectives
		- Improve user experience
		- Increase conversion rate by 20%
		- Mobile-first design
	- Timeline
		- Phase 1: Research (Weeks 1-2)
			- User interviews
			- Competitor analysis
			- Requirements gathering
		- Phase 2: Design (Weeks 3-5)
			- Wireframes
			- Mockups
			- User testing
		- Phase 3: Development (Weeks 6-10)
			- Frontend development
			- Backend integration
			- QA testing
		- Phase 4: Launch (Week 11)
			- Deployment
			- Monitoring
			- Iteration
	- Team
		- Designer: Jane
		- Developer: John
		- PM: Sarah
	- Budget
		- Design: $10,000
		- Development: $25,000
		- Total: $35,000
```

## Important Notes

- **Universal skill:** Works in both Claude Code and Claude Desktop
- **Environment-aware output:** Artifacts for Desktop, files for Code
- **Plain text focus:** Logseq handles styling; content structure matters most
- **No summaries:** Logseq users can create their own summaries/queries
- **Nesting depth:** No theoretical limit, but 3-4 levels is most readable
- **Flexibility:** Can format any hierarchical content, not just specific types

## Related Skills

- **zotero-mcp:** For formatting bibliographies with Zotero-specific metadata and translations
- **zotero-tagging:** For tagging Zotero items after bibliography generation

---

**Remember: Logseq uses outline hierarchy, not visual styling. Structure through nesting, not through headers or bold text.**
