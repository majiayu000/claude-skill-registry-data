---
name: draft-section
description: Incremental content drafting skill that writes specific sections within existing scaffolds. Supports drafting 1 section at a time or batch-drafting multiple sections with user control. Each operation stays under 10k tokens to avoid context compacting.
allowed-tools: Read, Grep, Glob, Write, Edit, Skill
---

# Section Drafter

## Overview

This skill drafts actual content for chapter sections within existing scaffolds, including:
- **Full-prose content** tailored to the part type and topic
- **Mermaid diagrams** (1-2 per section via mermaid-diagrams skill)
- **Code examples** formatted ≤80 chars wide
- **Cross-references** to related chapters
- **Quality validation** before output

**Key Benefits**:
- **Incremental drafting**: Write 1 section at a time with user review between
- **Context efficient**: ~8-10k tokens per section (no compacting issues)
- **Part-aware strategies**: Different writing approaches per part type
- **Quality-focused**: Built-in validation checks before output
- **User control**: Draft today, review tomorrow, iterate at your pace

## Critical Principles

### 1. Incremental Over Batch

**⚠️ IMPORTANT**: This skill prioritizes user control. Don't batch-draft entire chapters unless explicitly requested. Default to one section at a time so users can:
- Review each section before moving on
- Provide feedback and corrections
- Maintain quality and consistency
- Avoid rework from compounding errors

### 2. Strategy Over Templates

Different part types require different writing strategies:

- **Part 1 (Foundations)**: First-principles teaching - explain concepts from scratch, build understanding progressively
- **Part 2 (Playbook)**: Practical workflows - actionable steps, concrete deliverables, working with Claude Code
- **Part 3 (Patterns & Tools)**: Pattern documentation - problem/solution format, when to use, examples
- **Part 4 (Example)**: Narrative walkthrough - show actual project decisions, prompts used, lessons learned

### 3. Quality Over Speed

Each drafted section must pass quality checks:
- Content matches placeholder guidance
- Diagrams enhance understanding (not decorative)
- Code examples are practical and formatted correctly
- Cross-references are accurate and relevant
- Tone matches target audience (accessible to vibecoders, valuable to CTOs)

## When to Use This Skill

Invoke this skill when you need to:
- Draft content for specific sections within an existing scaffold
- Write one section and pause for user review
- Batch-draft multiple related sections
- Complete remaining sections in a chapter

**Prerequisites**:
- Chapter scaffold must exist (created by scaffold-chapter skill)
- Context files available: `brief.md`, `requirements.md`, `design.md`
- Related chapters available for cross-referencing

## Workflow

### Step 1: Read Context

Before drafting, read necessary context:
- [ ] Read the chapter scaffold to understand structure and placeholder guidance
- [ ] Read `/home/testa/agentic-coding-book/planning/brief.md` (for book vision)
- [ ] Read `/home/testa/agentic-coding-book/planning/requirements.md` (for requirements)
- [ ] Optionally read related chapters (for cross-references)

**Why**: These files provide the strategic context, requirements, and related content for accurate drafting.

### Step 2: Identify Target Section(s)

Determine which section(s) to draft based on user request:

**Modes**:
1. **Single section**: Draft one specific section (e.g., "Introduction")
2. **Multiple sections**: Draft several specified sections (e.g., "Key Concepts" + "Practical Application")
3. **Remaining sections**: Draft all sections not yet written

**Parse the scaffold** to identify:
- Which sections already have content vs placeholders
- What the placeholder guidance says for each section
- Which sections are requested by the user

### Step 3: Select Content Strategy

Based on the part number, select the appropriate writing strategy:

#### Part 1: First Principles Teaching Strategy

**Goal**: Explain concepts from scratch, accessible to beginners

**Approach**:
- Start with relatable scenarios or problems
- Build understanding progressively (simple → complex)
- Use analogies and comparisons
- Provide concrete examples
- Avoid jargon or define it clearly
- Include diagrams to visualize concepts

**Structure per section**:
- **Introduction**: Hook with problem, establish relevance
- **Key Concepts**: Define terms, explain principles step-by-step
- **Practical Application**: Show how to apply concepts
- **Common Pitfalls**: What mistakes to avoid
- **Summary**: Key takeaways
- **Further Reading**: Related chapters and external resources

#### Part 2: Practical Workflow Strategy

**Goal**: Provide actionable, step-by-step guidance

**Approach**:
- Focus on deliverables and outcomes
- Provide specific prompts for Claude Code
- Include "what good looks like" criteria
- Show concrete examples from planning/ directory
- Address common questions and edge cases
- Link to Part 3 patterns where relevant

**Structure per section**:
- **Overview**: Where this fits in 6-week journey
- **Prerequisites**: What must be complete first
- **The Process**: Step-by-step with actionable items
- **Working with Claude Code**: Specific prompts and tips
- **Deliverables**: What artifacts are produced
- **Example**: Complete walkthrough
- **Common Questions**: FAQ
- **Next Steps**: What comes next

#### Part 3: Pattern Documentation Strategy

**Goal**: Provide reusable reference material

**Approach**:
- Problem-first: explain what issue this solves
- Solution-focused: mechanics and implementation
- Include concrete code examples
- Provide "when to use" / "when NOT to use" guidance
- Cross-reference related patterns
- Include checklists for quick reference

**Structure per section**:
- **Overview**: One-paragraph summary
- **The Problem**: What issue does this solve? Symptoms?
- **The Solution**: How it works, implementation steps
- **Example**: Code, diagrams, walkthrough
- **When to Use / When NOT to Use**: Clear guidance
- **Related Patterns**: Cross-references
- **Checklist**: Quick reference
- **Further Reading**: External resources

#### Part 4: Example Narrative Strategy

**Goal**: Show real project execution with decisions and learnings

**Approach**:
- Tell the story chronologically
- Show actual prompts used with Claude Code
- Include real code snippets and their evolution
- Reveal decision-making process (why not just what)
- Share lessons learned and surprises
- Make it personal and authentic

**Structure per section**:
- **Where We Are**: Project state and timeline
- **The Challenge**: What needs to be solved
- **The Approach**: Planning and execution with Claude
- **Code Highlights**: Key snippets with explanation
- **Lessons Learned**: Insights and takeaways
- **What's Next**: Tease next chapter

### Step 4: Draft Content

For each section being drafted:

1. **Read the placeholder guidance** - understand what content belongs here
2. **Apply the part-appropriate strategy** - use the right writing approach
3. **Write full-prose content** - not bullet points, full paragraphs
4. **Include diagrams** where they enhance understanding (1-2 per section)
5. **Add code examples** where relevant, formatted ≤80 chars wide
6. **Insert cross-references** to related chapters
7. **Match the tone** - accessible to vibecoders, valuable to CTOs

**Content Guidelines**:
- **Paragraph length**: 3-6 sentences (not too dense)
- **Section length**: 200-500 words per subsection (varies by topic)
- **Code blocks**: Include descriptive comments, use proper syntax highlighting
- **Diagrams**: Use mermaid-diagrams skill to generate, include alt text
- **Cross-references**: Use markdown links with descriptive text
- **Tone**: Conversational but professional, teaching-focused

### Step 5: Generate Diagrams

For each diagram needed:

1. **Identify diagram opportunities** - concepts that benefit from visualization
2. **Choose diagram type**:
   - **Flowchart**: Processes, workflows, decision trees
   - **Sequence diagram**: Interactions, API flows
   - **Component diagram**: Architecture, system structure
   - **State diagram**: State machines, lifecycle
   - **ER diagram**: Data models, relationships
   - **Gantt chart**: Timelines, project phases

3. **Invoke mermaid-diagrams skill**:
   - Provide clear description of what to visualize
   - Specify diagram type
   - Request alt text for accessibility

4. **Save diagram reference** in content:
   ```markdown
   [Placeholder: Mermaid diagram showing X]

   ```mermaid
   [diagram code from mermaid-diagrams skill]
   ```

   *Figure X.X: [Diagram description with alt text]*
   ```

### Step 6: Format Code Examples

For each code example:

1. **Write practical code** - not toy examples, real-world patterns
2. **Format ≤80 chars wide** - for print readability
3. **Add descriptive comments** - explain non-obvious parts
4. **Use proper language tags** - for syntax highlighting
5. **Include context** - what this code does and why

**Example**:
```python
# Validate EARS requirement format
def validate_ears(requirement: str) -> bool:
    """Check if requirement follows EARS notation.

    Args:
        requirement: The requirement text to validate

    Returns:
        True if valid EARS format, False otherwise
    """
    ears_patterns = [
        r'^WHEN .+ the system shall .+',  # Event-driven
        r'^WHILE .+ the system shall .+', # State-driven
        r'^WHERE .+ the system shall .+', # Optional
        r'^IF .+ THEN .+ shall .+',       # Conditional
        r'^The system shall .+'           # Ubiquitous
    ]

    return any(
        re.match(pattern, requirement)
        for pattern in ears_patterns
    )
```

### Step 7: Add Cross-References

For each section, identify opportunities to link to related chapters:

**Cross-reference patterns**:
- **Prerequisites**: "See [Chapter X](link) for background on..."
- **Deep dives**: "For detailed information, refer to [Pattern Y](link)"
- **Related concepts**: "This relates to [Concept Z](link) from Part 1"
- **Forward references**: "We'll explore this further in [Chapter N](link)"

**Format**:
```markdown
See [Chapter 3: Architecture Principles](../part1-foundations/03-architecture-principles.md)
for the foundational concepts behind this pattern.
```

### Step 8: Quality Validation

Before finalizing drafted content, verify:

**Content Quality**:
- [ ] Addresses placeholder guidance completely
- [ ] Follows part-appropriate strategy
- [ ] Tone is accessible yet professional
- [ ] No jargon without definitions
- [ ] Examples are concrete and practical

**Technical Accuracy**:
- [ ] Code examples are syntactically correct
- [ ] Code is formatted ≤80 chars wide
- [ ] Diagrams accurately represent concepts
- [ ] Cross-references point to existing files
- [ ] Requirements traceability maintained

**Completeness**:
- [ ] Section fully written (not partial placeholder)
- [ ] Diagrams included where beneficial
- [ ] Code examples where relevant
- [ ] Cross-references to related content
- [ ] Alt text for all diagrams

**Formatting**:
- [ ] Markdown syntax is valid
- [ ] Headings follow hierarchy (##, ###, ####)
- [ ] Code blocks have language tags
- [ ] No trailing whitespace
- [ ] Consistent with existing content

### Step 9: Update Chapter File

Replace the placeholder section with drafted content:

**Use Edit tool** to replace:
```markdown
## Section Name

[Placeholder: Guidance text]
```

with:
```markdown
## Section Name

[Full drafted content with diagrams, code, cross-references]
```

**Confirm successful update** and report to user.

### Step 10: Batch Mode (Optional)

When drafting multiple sections:

1. **Process sections sequentially** (not in parallel)
2. **Keep context under 25k tokens total**
3. **Pause for user review** after each 2-3 sections
4. **Report progress** clearly

**Batch output**:
```
Drafted sections:
✓ Introduction (450 words, 1 diagram)
✓ Key Concepts (620 words, 2 diagrams, 1 code example)
✓ Practical Application (540 words, 1 code example)

Remaining sections:
- Common Pitfalls
- Summary
- Further Reading

Ready to continue? Or would you like to review first?
```

## Drafting Modes

### Mode 1: Single Section

**User**: "Draft the Introduction section for book/part1-foundations/01-renaissance-developer.md"

**Process**:
1. Read scaffold
2. Identify Introduction section
3. Read placeholder guidance
4. Apply Part 1 strategy
5. Draft content
6. Generate diagrams if needed
7. Validate quality
8. Update file

**Output**: Introduction section fully drafted, report completion

### Mode 2: Multiple Sections

**User**: "Draft 'Key Concepts' and 'Practical Application' sections for book/part1-foundations/03-architecture-principles.md"

**Process**:
1. Read scaffold
2. Identify both sections
3. Draft each sequentially
4. Update file with both sections
5. Report completion

### Mode 3: Remaining Sections

**User**: "Draft all remaining sections in book/part2-playbook/04-requirements-writing.md"

**Process**:
1. Read scaffold
2. Identify sections with only placeholders
3. Draft each sequentially
4. Pause every 2-3 sections for user review
5. Continue until complete

### Mode 4: Iterative Refinement

**User**: "Improve the 'Example' section in book/part3-patterns-tools/specifications/ears-notation.md - add more concrete code examples"

**Process**:
1. Read existing content
2. Identify what needs improvement
3. Draft enhanced version
4. Replace existing content
5. Report changes

## Best Practices

1. **One section at a time by default** - let user review before continuing
2. **Match placeholder guidance** - the scaffold tells you what to write
3. **Use part-appropriate strategy** - teaching vs workflow vs pattern vs narrative
4. **Visualize concepts** - diagrams enhance understanding
5. **Show, don't just tell** - concrete examples over abstract explanations
6. **Cross-reference generously** - connect concepts across parts
7. **Format for print** - 80-char code width, readable paragraphs
8. **Validate before output** - quality over speed

## Integration with Other Skills

**Upstream** (before drafting):
- **scaffold-chapter skill**: Creates the structure this skill fills in

**Parallel** (during drafting):
- **mermaid-diagrams skill**: Generates diagrams for content

**Downstream** (after drafting):
- Manual editing and refinement
- CI/CD validation scripts
- User review and iteration

## Performance Targets

- **Single section**: 10-15 minutes, ~8-10k tokens
- **Multiple sections (2-3)**: 25-35 minutes, ~20-25k tokens
- **Full chapter**: Multiple sessions with user review between

## Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Drafted content too generic | Re-read placeholder guidance, make content specific to chapter topic |
| Code examples too complex | Simplify to essential patterns, add more comments |
| Section too long | Break into subsections, use bullet points for lists |
| Cross-references broken | Verify file paths, use relative links |
| Diagram doesn't add value | Remove it, or rethink what should be visualized |
| Tone too academic | Rewrite with conversational style, use "you" |

## Example Invocations

See [EXAMPLES.md](EXAMPLES.md) for detailed examples of using this skill across all four parts.

## Output Format

For each drafted section, report:

```
✓ Drafted: book/part1-foundations/01-renaissance-developer.md - Introduction
  - Words: 450
  - Diagrams: 1 (skill distribution)
  - Code examples: 0
  - Cross-references: 2 (to Ch 2, Ch 5)
  - Quality: Passed validation
  - Status: Ready for user review
```

## Notes

- This skill writes **content**, not structure (structure is from scaffold-chapter)
- Each drafted section should be **complete and polished**, not rough drafts
- User should **review each section** before continuing to next
- Diagrams are **generated during drafting**, not as separate step
- Quality validation is **built-in**, not optional
- Context efficiency is **critical** - keep operations under 10k tokens per section
