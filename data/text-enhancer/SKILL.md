---
name: text-enhancer
description: Enhance professional and technical text with grammar correction, clarity improvements, and
  factual verification. Triggers on "enhance" or "polish" commands. Integrates with AWS Documentation
  and Obsidian to verify technical accuracy and find relevant context. Preserves author's authentic
  style while improving readability and impact.
---

# Text Enhancer

This skill provides comprehensive text enhancement for professional communications, technical documentation,
blog posts, Obsidian notes, and other written content.

## When to Use This Skill

Activate this skill when the user requests to:

- "Enhance [text]"
- "Polish [text]"
- "Check and enhance [text]"

## Core Enhancement Workflow

### 1. Identify Content Type and Context

First, determine the text type and intended context:

**Common content types:**

- Blog posts (technical, public-facing)
- IT handbook pages (technical documentation)
- Slack messages (internal, informal-to-professional)
- Emails (professional correspondence)
- Obsidian notes (personal knowledge management, markdown)
- Presentations or reports

**Context inference:**

- Examine the text to infer likely context (audience, formality, purpose)
- If context is ambiguous or not explicitly provided, suggest the inferred context and ask for confirmation
- Always explicitly confirm context before proceeding with enhancement

**Example:**

> "This appears to be a technical blog post for external readers. Is this correct, or is this content
> for internal documentation?"

### 2. Search for Related Context

Before enhancing, gather relevant context:

**For Obsidian notes:**

- Use `obsidian_simple_search` or `obsidian_complex_search` to find similar notes
- Look for related concepts, previous writing on the topic, or style patterns
- Use findings to maintain consistency with existing notes

**For AWS-related content:**

- Identify any AWS services, features, or technical claims mentioned
- Use `search_documentation` to verify current AWS capabilities
- Use `read_documentation` to check specific technical details
- Flag any outdated or incorrect AWS information

### 3. Apply Enhancement Guidelines

Perform comprehensive enhancements following these principles:

**Grammar and vocabulary:**

- Correct all grammar errors
- Fix vocabulary mistakes
- Improve word choice for precision and clarity

**Clarity and flow:**

- Restructure sentences for better readability
- Improve logical flow between ideas
- Break up overly complex sentences
- Add transitions where helpful

**Conciseness (default preference):**

- Keep text concise and direct
- Remove unnecessary words and filler
- Allow modest expansion (10-20%) only when it significantly improves clarity
- Never add length just to make text appear more substantial

**Impact optimization:**

- Strengthen weak phrases
- Make key points more prominent
- Improve professional tone while maintaining authenticity

### 4. Style Preservation (Critical)

Maintain the author's authentic voice and specific style preferences:

**Mandatory style rules:**

- NEVER use em dashes (—) - this is a red flag for AI-generated text
- PREFER colons (:) instead of em dashes for clarification or elaboration
- Use natural, straightforward, authentic language
- Avoid buzzwords and marketing speak
- Avoid unnecessary adjectives and filler words
- Keep sentences digestible and easy to understand
- Maintain direct, honest tone without sugar-coating

**Preserve existing patterns:**

- Maintain the author's sentence structure preferences (short vs. explanatory)
- Keep consistent terminology the author uses
- Respect the author's voice and communication style
- Don't impose a "corporate" or overly formal style unless requested

**Formality matching:**

- Professional communications: formal but not stiff
- Internal Slack: conversational but professional
- Technical docs: clear and precise
- Personal notes: authentic and natural

### 5. Verify Factual Accuracy

Check technical and factual claims:

**Technical verification:**

- For AWS-related claims, use AWS Documentation MCP to verify
- For other technical claims, flag if uncertain and suggest verification
- Note when information might be outdated

**Questionable assumptions:**

- Flag claims that seem speculative without supporting evidence
- Note logical inconsistencies or gaps
- Identify areas where more context might be needed

**Flag format:**

```text
⚠️ Technical note: [specific concern]
```

### 6. Identify Ambiguities and Missing Context

Ask clarifying questions when:

- Key terms are ambiguous
- Target audience is unclear
- Technical depth needed is uncertain
- Context would significantly change the enhancement approach
- Multiple interpretations are equally valid

Keep questions focused and specific. Avoid overwhelming with many questions at once.

### 7. Structural Improvements

Suggest structural changes when they would significantly improve the text:

- Reordering sections for better flow
- Adding or removing subheadings
- Breaking up long paragraphs
- Adding lists for complex enumerations (when appropriate)

Note: Author prefers full text over bullet points except for code snippets, specifications, and examples.

## Output Format

Present the enhanced text in an artifact with:

1. **Enhanced version** - The improved text
2. **Key changes summary** - Brief bullet list of major improvements made
3. **Technical flags** - Any factual concerns or verification notes (if applicable)
4. **Clarifying questions** - Any ambiguities requiring user input (if applicable)
5. **Related notes** - Links to similar Obsidian notes found (if applicable)

Keep the summary outside the artifact for easy reference.

## Tool Integration

### AWS Documentation MCP

When text contains AWS service references:

```text
1. search_documentation: Find relevant AWS documentation
2. read_documentation: Verify specific technical claims
3. Flag discrepancies between text and official documentation
```

### Obsidian MCP

When enhancing Obsidian notes:

```text
1. obsidian_simple_search: Find notes with similar keywords
2. obsidian_complex_search: Find notes with specific patterns/tags
3. obsidian_get_file_contents: Read similar notes for context
4. Use findings to maintain consistency across notes
```

## Examples of Style Preferences

**❌ Avoid (AI tells):**

- "The system leverages cutting-edge technology—ensuring optimal performance"
- "This revolutionary approach—which transforms the landscape—delivers value"
- Overuse of adjectives: "incredibly powerful," "absolutely essential"

**✅ Prefer:**

- "The system uses proven technology: this ensures consistent performance"
- "This approach transforms how we work: it reduces complexity and improves reliability"
- Direct statements: "powerful," "essential"

## Enhancement Intensity

Default to substantial enhancement that:

- Makes all necessary corrections
- Significantly improves clarity and flow
- Maintains concise length (modest growth acceptable)
- Preserves authentic style and voice

If the text is already strong, make minimal changes and note this in the summary.
