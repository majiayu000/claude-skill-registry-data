---
name: joplin-research
description: Comprehensive guidelines for formatting research artifacts, technical surveys, rundowns, book summaries, and documentation with proper markdown formatting for Joplin notes. This skill should be loaded and followed whenever Joplin is mentioned in a prompt.
---

**When to Use**: Automatically activate this skill whenever:
- User mentions "Joplin" in their request
- User requests markdown artifacts for note-taking
- User requests technical rundowns, summaries, or research documents
- User explicitly requests content following their markdown preferences

**Response**: When returning formatted artifacts:
- Refer to the generated content
- Do not describe formatting rules and other details followed, unless more substantial changes to content have been made

## Core Formatting Principles

### Spacing and Line Break Rules
1. **Heading Spacing**:
   - Two carriage returns (blank lines) BEFORE h2 headings
   - One carriage return (blank line) BEFORE all other headings (h3, h4, h5, h6)
   - CRITICAL: NO extra blank lines after headings
2. **Horizontal Rules**:
   - Remove any extra horizontal rules ("---") under headings other than H3. These are handled by CSS.
   - **NEVER use "---" after h1 or h2 headings** (they already have border-bottom in CSS)
   - **NO other heading levels** (h4, h5, h6) should have horizontal rules.
3. **Content Spacing**:
   - NO extra blank lines within sections unless separating fundamentally different concepts
   - CLI commands follow the same compact formatting as other content
4. **General Rule**: If in doubt, use less spacing rather than more

### Heading Hierarchy & Typography
1. **h1 Headings** - Bitter Serif, 2rem, border-bottom
   - Rarely used. Reserve for document title only in special cases
   - Already has border-bottom in CSS, so NEVER add "---" after it
   - Usually preceded by `>[toc]` tag at start of document if the document is more that 5 pages long
2. **h2 Headings** - Bitter Serif, 1.8rem, border-bottom
   - Main document sections
   - Already has border-bottom in CSS, so NEVER add "---" after it
3. **h3 Headings** - Bitter Serif, 1.5rem
   - Primary section dividers
   - ONLY heading level that gets "---" separator underneath
   - This is where major content sections begin
4. **h4 Headings** - Bitter Serif, 1.25rem
   - Sub-sections within h3 sections
   - Regular markdown, no special formatting
   - Use for subsections within a larger section
5. **h5 Headings** - Bitter Serif, 1.25em
   - Detail-level sections
   - Regular markdown, no special formatting
   - Use for even smaller section headings
6. **h6 Headings** - Sans-serif, 0.9rem, weight 600
   - Rarely used
   - For emphasis or 1-paragraph comments
   - Often used for sub-labels within lists (e.g., `###### [GitHub: Repository](url)`)

### Example Structure:
```markdown
>[toc]
# Main Document Title
First paragraph content starts immediately after heading. Note that h2 already has a border-bottom in CSS, so NO horizontal rule is added.

## Major Section Header
### Major Sub-Section
---
Content starts immediately after the separator line. This is the ONLY heading level that may sometimes get the horizontal rule separator. The presence or absence of "---" should be consistent throughout the document.

<figure class="img-center">
    <img src=":/af5fcef1a0234a36b27c35b519d52e7c" alt="Description">
	<figcaption>Figure 1. This is a comment for an example of how an image should be formatted.</figcaption>
</figure>

#### Subsection
Content starts immediately after heading (one blank line before heading). No horizontal rule for h4.

##### Detail Section
More detailed content here. No horizontal rule for h5.

###### Lower-level Details or Paragraph Header
More content.

### Next Major Sub-Section
Content starts immediately after the separator line. This is the ONLY heading level that may sometimes get the horizontal rule separator.


## Next Major Section
There may be an introductory paragraph here. Then content continues with another section.
```


## Table of Contents

**Format**: Always use blockquote syntax with `>[toc]` at the start of documents
```markdown
>[toc]
# Main Title of Document
## First Major Section
```

**When to Use**:
- Always include for documents longer than 4-5 pages long
- Place at the very beginning of the document
- Single blank line after `>[toc]` before first h2 heading


## Artifact Type Templates
##### 🔥 Research Format Quick Reference
| Request Phrase             | Use Case                   | Typical Output Length |
| -------------------------- | -------------------------- | --------------------- |
| "Technical Survey of..."   | Compare 5-10 similar tools | 2-4 pages             |
| "Technical Rundown of..."  | Deep dive on one tool      | 3-6 pages             |
| "What's New with..."       | Recent updates/changes     | 1/2 page - 1 page     |
| "Book Summary of..."       | Summary of a book          | 2-4 pages             |
| "Article Summary of..."    | Summary of an article      | 2-4 pages             |
| "Whitepaper Summary of..." | Summary of a whitepaper    | 2-4 pages             |


### Technical Rundowns
---
**Trigger**: User specifically requests "Give me a technical rundown of..."
**Use Case**: Software engineering tools, libraries, frameworks, platforms
**Goal**: Condensed material for accelerated learning and technical proficiency

**Structure**:

```markdown
>[toc]

## [Tool/Framework Name]

### Overview
---
**General Information**: Provide context about the entity. How is it different from competitors? Who created it and when? How have adoption rates changed? What is its basic function and purpose? How does it work at a high level (1-paragraph explanation)? What are its key features and capabilities?

**Key Resources**:
- [Official Site](https://...)
- [Documentation](https://...)
- [GitHub Repository](https://...)
- [Community Forum](https://...)

**Advantages & Disadvantages**:
\+ Major advantage over competitors
\+ Another key strength
\+ Unique feature or capability
\- Notable limitation or weakness
\- Area where competitors may excel
\- Potential drawback or concern

### Common Commands
---
- `command syntax`: *Brief description of what it does*
- `another command`: *Its purpose and usage*
- `third command`: *When and why to use it*

### [Additional Detail Section - e.g., Language Support, Pricing, Roadmap, etc]
---
Content about language support.

#### Specific Language Details
Subsection content here.

### [Another Section - e.g., Pricing]
---
Pricing information.

### [Another Section - e.g., Market Position]
---
Market share, GitHub stars, adoption rates.
```

**Required Additional Sections** (when relevant):
- Language support
- Pricing/Licensing
- Security & Deployment (cloud, on-premise, package manager)
- Market share / GitHub stars / rate of adoption
- API flexibility / availability
- Computational requirements
- Integration capabilities


### Technical Surveys
---
**Trigger**: User specifically requests "Give me a technical survey of..."
**Use Case**: Compare 6-12 similar tools in a specific space
**Goal**: Comparison overview of multiple technologies

**Structure**:

```markdown
>[toc]

## [Technology Category Survey]

### Overview
---
Brief introduction to the technology category and why these tools are being compared.

**Comparison Table** (optional):
| Tool | Key Feature | Pricing | Best For |
|------|-------------|---------|----------|
| Tool 1 | Feature | $X | Use case |
| Tool 2 | Feature | $Y | Use case |

### [Tool Name 1]
---
**Background**: When was it created? Who maintains it? How have adoption rates changed recently? Provide context about the entity. How is it different from competitors? What is its basic function and purpose? How does it work at a high level (1-paragraph explanation)? What are its key features and capabilities?

**Key Resources**:
- [Official Site](https://...)
- [Documentation](https://...)
- [GitHub Repository](https://...)

**Advantages & Disadvantages**:
\+ Key advantage
\+ Another strength
\- Notable limitation
\- Area where competitors excel

### [Tool Name 2]
---
[Same structure as Tool 1]

### [Tool Name 3]
---
[Same structure]
```

### Book Summaries
---
**Format**:
```markdown
### [Book Title]

**Author**: [Name]
**Context**: Brief background about the author and why they wrote this book.
**Main Objectives**: Core goals and themes of the book.

### Chapter 1: [Title]
[2-5 sentence summary of key points, arguments, and takeaways]
### Chapter 2: [Title]
[2-5 sentence summary]
[Continue for all chapters]
```

### Article Summaries
---
**Format**:
```markdown
## [Article Title]

**Author**: [Name]
**Source**: [Publication/Website]
**Date**: [Publication date]

### Summary
[Conventional summary providing balanced mix of:]
- Main arguments and thesis
- Key counterarguments or alternative perspectives
- Significant data points or evidence
- Important conclusions or implications

### Key Takeaways
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]
```

### Research Notes
---
**Format**:
```markdown
>[toc]

## [Topic/Research Subject]

### Context & Background
[Overview of the topic, why it matters, current state]

### Key Findings
[Main discoveries or insights organized logically]
#### Finding Category 1
[Details]
#### Finding Category 2
[Details]

### Methodology
[If relevant: how information was gathered or analyzed]

### Implications
[What this means, how it can be applied]

### References
- [Citation 1]
- [Citation 2]
```


## Formatting Special Elements

### Links
**Format**: Always as markdown links with descriptive text
```markdown
- [Official Documentation](https://docs.example.com)
- [GitHub Repository](https://github.com/org/project)
- [Tutorial Series](https://learn.example.com)
```

**For sub-labels within content**:
```markdown
###### [GitHub: Repository](https://github.com/org/project): *Description of what you'll find*
```

### Advantages & Disadvantages
**Format**: Use + and - with proper escaping
```markdown
\+ This is an advantage or positive aspect
\+ Another benefit or strength
\- This is a disadvantage or limitation
\- Another concern or weakness
```
**Why escaping**: The backslash prevents markdown from interpreting + and - as list markers

### CLI Commands
**Format**: Backticks for command, italics for description
```markdown
- `npm install package`: *Installs the specified package*
- `git commit -m "message"`: *Creates a commit with a message*
- `docker build -t name .`: *Builds a Docker image with specified tag*
```

### Code Blocks
**Format**: Standard markdown fenced code blocks with language specification
- Use Fira Code font (automatically applied by CSS)
- Always specify language for syntax highlighting
- Single blank line before and after code blocks

```markdown
```python
def example_function():
    """This is a docstring"""
    return "formatted code"
```
```

**Supported languages**: javascript, python, css, html, bash, typescript, go, rust, java, sql, json, yaml, etc.

### Inline Code
**Format**: Backticks for inline code mentions
```markdown
Use the `useState` hook to manage component state.
```
- Rendered in Fira Code at 12px
- Slight background color for visibility

### Callout Boxes
**Available types**: idea, todo, warning

**Format**:
```markdown
<div class="idea">
<div class="idea-title">Idea</div>
Your idea content goes here. Can include multiple paragraphs, code, lists, etc.
</div>

<div class="todo">
<div class="todo-title">Todo</div>
Your todo content goes here with circular checkmark icon.
</div>

<div class="warning">
<div class="warning-title">Warning</div>
Your warning content goes here with exclamation icon.
</div>
```

**When to use**:
- **Idea**: For insights, suggestions, or creative thoughts
- **Todo**: For action items, tasks, or reminders
- **Warning**: For important cautions, security notes, or critical information

### Blockquotes
**Primary Use**: Table of contents at document start
```markdown
>[toc]
```

**Secondary Use**: General quotes or tips
```markdown
> **Pro tip**: Always validate user input on both client and server side to prevent injection attacks.
```
- Dotted border, 5px border radius
- Light-gray background
- Italic text
- Slightly transparent (0.85 opacity)

### Images
**Format**: HTML image syntax with optional caption that provides css for padding, width, and alignment
When editing existing notes or adding images, images that are formatted as below:
```markdown
![jl.png](:/76cd4725a4e0415c9c36e5fc90c3c19d)
```

 ... should be converted to html:
```markdown
<figure class="img-center">
    <img src="/path/to/image.jpg" alt="Description">
	<figcaption>Figure 1. This is a comment for an example of how an image should be formatted.</figcaption>
</figure>
```

### Tables
**Format**: Standard markdown tables, compact spacing
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| More 1   | More 2   | More 3   |
```
**Best Practices**:
- Use tables for structured data comparison
- Keep column widths reasonable
- Use header row for column labels

### Lists
**Unordered Lists**:
```markdown
- First item
- Second item
  - Nested item (2 spaces indent)
  - Another nested item
- Third item
```

**Ordered Lists**:
```markdown
1. First step
2. Second step
3. Third step
```

**Task Lists**:
```markdown
- [ ] Unchecked item
- [x] Checked item (renders italic with reduced opacity)
- [ ] Another unchecked item
```


## Quality Checklist
Before finalizing any Joplin markdown artifact, verify:

- [ ] `>[toc]` tag present at document start (for h2-headed documents)
- [ ] Two blank lines before h2 headings
- [ ] One blank line before h3, h4, h5, h6 headings
- [ ] "---" separator ONLY under h3 headings (NEVER after h1 or h2)
- [ ] Single blank line between content elements
- [ ] No excessive vertical spacing
- [ ] Links formatted as `- [Text](URL)` or `###### [Source: Title](URL): *description*`
- [ ] Advantages/disadvantages with `\+` and `\-` (escaped)
- [ ] CLI commands as `` `command`: *description* ``
- [ ] Proper heading hierarchy (h2 → h3 → h4 → h5 → h6)
- [ ] Information density maximized
- [ ] Content starts immediately after headings (except for h3 with separator)
- [ ] Code blocks have language specification
- [ ] Callout boxes use proper HTML structure


## CSS-Aware Formatting
Understanding why certain formatting choices are made:

### Why NO horizontal rules after h1/h2?
- h1 and h2 headings already have `border-bottom` styling in CSS
- Adding "---" would create visual redundancy
- The CSS border provides consistent, professional styling

### Why h3 gets horizontal rules?
- h3 doesn't have border-bottom in CSS
- The "---" creates visual separation for major sections
- Maintains consistent visual hierarchy

### Typography Stack
- **Headings (h1-h5)**: Bitter (serif) - Creates visual hierarchy, professional appearance
- **Body text**: Inter (sans-serif) at 14px - Excellent readability for extended reading
- **Code**: Fira Code (monospace) at 12px - Programming ligatures, clear distinction
- **h6**: Sans-serif at 0.9rem - Differentiates from main heading levels

### Color Palette
- **Body text**: Dark gray (#4d4d4d) - High contrast without harsh black
- **Links**: Bright blue (#3486f3) - Clear affordance
- **Code background**: Light gray (#f5f5f5) - Subtle differentiation
- **Callouts**: Color-coded by type (yellow for idea, teal for todo, red for warning)


## Anti-Patterns to Avoid
1. **Horizontal rules after h1/h2**: These headings already have CSS borders
2. **Excessive Spacing**: Multiple blank lines between sections
3. **Wrong Separator Usage**: Using "---" under h2, h4, h5, or h6 headings
4. **Inconsistent Formatting**: Mixing different link styles or bullet formats
5. **Poor Hierarchy**: Jumping from h2 to h5 without intermediate levels
6. **Verbose Descriptions**: Long-winded explanations when concise summaries suffice
7. **Missing Context**: Technical rundowns without advantages/disadvantages or key resources
8. **Unescaped Characters**: Using + and - without backslash escaping in advantage/disadvantage lists
9. **Missing Language Tags**: Code blocks without language specification
10. **Forgetting Table of Contents**: Omitting `>[toc]` from multi-section documents


## Usage Examples
### Example 1: Technical Rundown Request
**User**: "Give me a technical rundown of FastAPI"
**Action**:
1. Activate markdown-formatting skill
2. Create comprehensive technical rundown with `>[toc]`
3. Structure with h2 main title, h3 sections with "---" separators
4. Include Overview, Common Commands, Implementation sections
5. Add advantages/disadvantages with proper escaping

### Example 2: Research Summary for Joplin
**User**: "Summarize this article about neural networks for my Joplin notes"
**Action**:
1. Create article summary with proper metadata
2. Use h3 sections with "---" for Summary and Key Takeaways
3. Include inline code for technical terms
4. Add callout boxes for important warnings or insights

### Example 3: Book Notes
**User**: "Create chapter summaries for 'Clean Code' in Joplin format"
**Action**:
1. Generate book summary with author context
2. Use h3 sections with "---" for each chapter
3. 2-5 sentence summaries per chapter
4. Maintain compact spacing throughout

### Example 4: Technical Survey
**User**: "Give me a technical survey of Python web frameworks"
**Action**:
1. Create comparison with `>[toc]`
2. Optional comparison table at top
3. Each framework gets h3 section with "---"
4. Include advantages/disadvantages for each
5. Add key resources with proper link formatting


## Integration Notes
- **Automatic Activation**: This skill automatically activates when "Joplin" is mentioned or technical documentation is requested
- **User Preferences**: Deeply integrated with user's documented preferences in CLAUDE.md
- **CSS Compatibility**: All formatting choices align with user's custom Joplin CSS (userstyle.css and userchrome.css)
- **Workflow Integration**: Compatible with user's ~/Projects directory structure and research practices
- **Typography Awareness**: Formatting takes advantage of Bitter, Inter, and Fira Code font stack
