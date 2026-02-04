---
name: Reviewing content governance
description: Reviews content against HMS IT governance standards including style guide, word list, and platform-specific guidelines. Checks voice and tone, word usage, formatting, structure, and compliance with content type requirements. Use when reviewing emails, knowledge base articles, website pages, or documents for style consistency, or when users mention "content review", "style guide check", "governance compliance", "editorial standards", "content quality", or "editorial review".
allowed-tools: ["Read","Grep","Glob","Edit","AskUserQuestion"]
---

<!--
  status: beta
  platforms: ["claude-code"]
  requires: ["access to files for review"]
  tags: ["content", "governance", "review", "style-guide", "quality-assurance", "editorial"]
-->

# Content Governance Review

Reviews content against comprehensive HMS IT content governance standards to ensure consistency, professionalism, clarity, and compliance across all communications.

## Overview

This skill analyzes content against HMS IT's comprehensive governance framework, which includes:

- **Core style guide**: Voice and tone, clarity and conciseness, formatting standards
- **Word list**: 300+ specific usage rules and terminology standards
- **Email guidelines**: Broadcast email composition, subject lines, messaging architecture
- **Knowledge base standards**: Article types, evergreen content rules, metadata requirements
- **Website and internal communications**: Page guidelines, intranet standards, policy templates

The skill identifies issues across multiple dimensions, categorizes them by severity, and can automatically fix many common violations with user approval.

## What you should do

When invoked to review content:

1. **Understand the request**:
   - Determine review mode: Quick Scan (fast, critical only), Comprehensive (complete analysis), or Targeted (specific aspect)
   - If not specified, infer from user's language: "quick check" → Quick Scan, "full review" → Comprehensive, "check word list" → Targeted
   - Identify content type: email, KB article, web page, internal doc, or general documentation

2. **Read the content**:
   - Use Read tool to load the file
   - Note file path for content type clues (/emails/, /kb/, /web/)
   - Scan for structural indicators (subject lines, article metadata, policy format)

3. **Detect content type** (if not obvious):
   - Check file path patterns
   - Look for content structure clues (email salutations, KB article types, SharePoint templates)
   - Use AskUserQuestion only if truly ambiguous after analysis

4. **Consult governance standards**:
   - Core standards: `REFERENCE.md` (style guide, word list)
   - Email-specific: `REFERENCE-EMAIL.md` (subject lines, phishing prevention)
   - KB-specific: `REFERENCE-KB.md` (evergreen content, article types)
   - Web/Internal: `REFERENCE-WEB-INTERNAL.md` (page guidelines, intranet)

5. **Perform review**:
   - **Voice/Tone**: Professional voice, active voice, present tense, no rhetorical questions
   - **Word Usage**: Check against 300+ word list entries, inclusive language, terminology
   - **Formatting**: Sentence case headings, monospace for code, straight quotes, date/time format
   - **Structure**: Paragraph length (≤6 sentences), heading quality, list formatting, parallel phrasing
   - **Platform-Specific**: Apply email/KB/web rules based on content type
   - Categorize each finding: Critical (affects meaning) → Important (consistency) → Minor (polish)
   - Flag auto-fixable issues: word replacements, capitalization, formatting

6. **Present findings**:
   - Organize by category (Voice/Tone, Word Usage, Formatting, Structure, Platform-Specific)
   - Within each category, order by severity (Critical → Important → Minor)
   - For each issue, provide:
     - Line number and context
     - Clear explanation of violation
     - Specific fix recommendation with example
     - Auto-fixable indicator (Yes/No)
   - Summarize: Total issues, breakdown by severity, auto-fixable count

7. **Offer batch fixes** (if auto-fixable issues exist):
   - List all proposed changes with before/after examples
   - Group by type (word list, capitalization, formatting)
   - Request single user approval for entire batch
   - Use AskUserQuestion only for genuinely ambiguous fixes (multiple valid options, context-dependent choices)
   - Apply approved fixes using Edit tool
   - Report summary: "Fixed 15 issues: 8 word list, 4 capitalization, 3 formatting"

8. **Handle manual fixes**:
   - For voice/tone, complex rewrites, and context-dependent issues
   - Provide guidance but don't auto-fix
   - Explain why manual review is needed

**Reference files structure**:
- `REFERENCE.md`: Core style guide and complete word list
- `REFERENCE-EMAIL.md`: Broadcast email standards
- `REFERENCE-KB.md`: Knowledge base article guidelines
- `REFERENCE-WEB-INTERNAL.md`: Website and internal communications
- `governance/`: Complete source files (38 files) for deep reference

## When to Use This Skill

Use this skill when you need to:

- Review content before publication (emails, KB articles, web pages, documentation)
- Ensure compliance with HMS IT governance standards
- Check for style guide violations or inconsistencies
- Validate word usage against the official word list
- Perform quality assurance on communications
- Get editorial feedback on drafts

**Trigger phrases**: "review this content", "check against style guide", "validate governance", "content quality check", "editorial review", "style compliance"

## Content Types Supported

The skill adapts its review criteria based on content type:

1. **Broadcast emails**: Subject lines, messaging architecture, unplanned outage format
2. **Knowledge base articles**: Article type validation, evergreen content, metadata
3. **Website pages**: Page-specific guidelines, strategic initiative content
4. **Internal communications**: Intranet/SharePoint, Teams, policy documents
5. **General documentation**: Core style guide and word list compliance

## Review Modes

The skill offers flexible review depth based on user needs:

### Quick Scan
- Focuses on critical issues only
- Checks voice/tone problems, major word list violations, and serious formatting errors
- Ideal for rapid quality checks before publication
- Typical output: 5-15 high-priority findings

### Comprehensive Review
- Line-by-line analysis covering all governance standards
- Identifies critical, important, and minor issues
- Provides severity ratings and context for each finding
- Typical output: 20-100+ findings depending on content length

### Targeted Review
- Focuses on user-specified areas (e.g., just word usage, just formatting)
- Useful when specific concerns exist or time is limited
- User can request focus on: Voice/Tone, Word Usage, Formatting, Structure, or Platform-Specific

**Default behavior**: The skill automatically selects the appropriate review mode based on user request. For example:
- "Quick check" → Quick Scan
- "Full review" → Comprehensive Review
- "Check the word list" → Targeted Review (Word Usage)

## Workflow

### 1. Content Ingestion
- User provides file path or content to review
- Skill reads and analyzes content structure

### 2. Content Type Detection
- Automatically detects content type from:
  - File path patterns (e.g., `/emails/`, `/kb/`, `/web/`)
  - Content structure (subject lines, article metadata)
  - Explicit user specification

### 3. Review Execution
- Applies appropriate governance rules based on content type
- Checks against multiple dimensions:
  - **Voice and Tone**: Professional voice, appropriate formality, positive language
  - **Word Usage**: Word list compliance, terminology accuracy, inclusive language
  - **Formatting**: Capitalization, monospace/bold/italics usage, dates/times
  - **Structure**: Paragraph length, heading quality, list formatting
  - **Platform-Specific**: Email subject lines, KB article types, metadata

### 4. Present Findings
Findings are organized by:
- **Category**: Voice/Tone, Word Usage, Formatting, Structure, Platform-Specific
- **Severity**: Critical (affects meaning/professionalism) → Important (consistency) → Minor (polish)
- **Location**: Line numbers and context
- **Recommendation**: Specific fix suggestions with examples

### 5. Batch Fix Capability
After presenting findings, the skill offers to automatically fix issues:

**Auto-fixable issues** (can be batched):
- Word list replacements (e.g., "PC" → "computer", "click" → "select")
- Capitalization corrections (sentence case in headings, proper acronym casing)
- Formatting fixes (straight quotes instead of curly quotes, proper date/time format)
- Simple structure improvements (Oxford comma insertion, spacing corrections)

**Manual review required**:
- Voice and tone adjustments (requires judgment and context)
- Complex sentence rewrites (clarity, conciseness)
- Content reorganization (paragraph restructuring, heading improvements)
- Context-dependent word choices

**Batch fix process**:
1. Skill identifies all auto-fixable issues
2. Presents complete list of proposed changes with before/after examples
3. Requests single user approval for batch execution
4. Applies all approved fixes
5. Reports summary of changes made

**When AskUserQuestion is used**:
The skill uses `AskUserQuestion` **only when ambiguity exists during the fix process**, such as:
- Multiple valid fix options (e.g., "either/or" → "either and or" vs "either...or" vs rewording)
- Context-dependent choices (e.g., when "application" might be appropriate vs "app")
- Uncertain content type detection (e.g., could be both email and KB article)

The skill does **not** use `AskUserQuestion` for basic review scope selection if the user's request is clear.

## Finding Categories and Severity Levels

### Voice and Tone
**Critical**:
- Humor or unprofessional language
- Unnecessarily negative framing
- Rhetorical questions instead of statements
- Inappropriate use of "please" or "thank you" (implying optional steps)

**Important**:
- Passive voice where active is clearer
- Future tense instead of present tense/imperative
- Lack of empathy or unhelpful tone

**Minor**:
- Overly formal or stuffy phrasing
- Opportunities to be more direct

### Word Usage
**Critical**:
- Insensitive or non-inclusive terms (blacklist, master/slave, crazy, dummy)
- Incorrect product names or major terminology errors
- Jargon without definition

**Important**:
- Word list violations (PC, click, application vs app)
- Inconsistent terminology
- Latin abbreviations (e.g., i.e., etc.)

**Minor**:
- Unnecessary modifiers (absolutely, actually, basically)
- Roundabout expressions that could be condensed
- Minor redundancies

### Formatting
**Critical**:
- Title case in headings instead of sentence case
- Missing monospace for code, file paths, or commands
- Incorrect bold/italics usage that affects meaning

**Important**:
- Curly quotes instead of straight quotes
- Incorrect date/time format
- Improper acronym capitalization (2fa vs 2FA, vpn vs VPN)

**Minor**:
- Inconsistent spacing
- Missing Oxford commas
- Minor punctuation issues

### Structure
**Critical**:
- Vague or non-descriptive headings
- Tables used for layout instead of tabular data
- Missing heading structure in long content

**Important**:
- Paragraphs longer than 6 sentences
- Lists where prose would be better (or vice versa)
- Non-parallel phrasing in lists or headings

**Minor**:
- Introductory material could be shorter
- Opportunities for better section breaks

### Platform-Specific
**Critical** (Email):
- Vague or non-action-oriented subject line
- Missing required elements (e.g., time zones in outage notifications)

**Critical** (Knowledge Base):
- Temporal/non-evergreen content (e.g., "next month", "recently")
- Incorrect article type classification

**Important**:
- Missing metadata
- Inconsistent template usage

## Output Format Examples

### Quick Scan Output
```markdown
## Content Governance Review: Quick Scan

**Content Type**: Broadcast Email
**Critical Issues Found**: 3
**Auto-fixable**: 2

### Critical Issues

#### Voice and Tone (Line 12)
**Issue**: Rhetorical question found
**Current**: "Wondering how to update your password? Follow these steps:"
**Fix**: "These steps explain how to update your password:"
**Severity**: Critical - Violates professional voice standards

#### Word Usage (Line 23)
**Issue**: Non-inclusive term "blacklist"
**Current**: "Add the sender to your blacklist"
**Fix**: "Add the sender to your blocklist"
**Severity**: Critical - Violates inclusive language standards
**Auto-fixable**: Yes
```

### Comprehensive Review Output
```markdown
## Content Governance Review: Comprehensive

**Content Type**: Knowledge Base Article
**Total Issues Found**: 42
**Critical**: 2 | **Important**: 15 | **Minor**: 25
**Auto-fixable**: 28

### Critical Issues (2)

[Detailed findings with line numbers, context, recommendations]

### Important Issues (15)

[Organized by category: Voice/Tone (3), Word Usage (7), Formatting (3), Structure (2)]

### Minor Issues (25)

[Brief listing with line numbers and quick fixes]

---

**Batch Fix Available**: 28 issues can be automatically corrected.
Would you like me to apply these fixes?
```

## Progressive Disclosure

For detailed reference on specific standards, consult:

- **`REFERENCE.md`**: Core HMS IT style guide and word list (complete reference)
- **`REFERENCE-EMAIL.md`**: Broadcast email-specific guidelines and templates
- **`REFERENCE-KB.md`**: Knowledge base article standards and best practices
- **`REFERENCE-WEB-INTERNAL.md`**: Website and internal communications guidelines
- **`governance/`**: Complete source files organized by category

## Usage examples

For detailed usage examples including:
- Quick email review with auto-fixes
- Comprehensive KB article review with severity breakdown
- Targeted word list checks
- Ambiguous fixes requiring clarification
- Phishing pattern detection
- Structure and formatting checks

See [`EXAMPLES.md`](EXAMPLES.md) for complete walkthroughs with before/after examples and expected outputs.

## Best Practices

1. **Start with Quick Scan**: For time-sensitive reviews, start with Quick Scan to catch critical issues
2. **Comprehensive for publication**: Use Comprehensive Review before final publication
3. **Targeted for specific concerns**: If you know the area of concern, request Targeted Review
4. **Review auto-fixes**: Always review the batch fix list before approving
5. **Manual fixes for voice/tone**: Accept that voice and tone improvements require manual review
6. **Iterative improvement**: Use the skill multiple times as content evolves

## Limitations

- **Context limitations**: The skill cannot fully understand domain-specific context or strategic communication goals
- **Judgment calls**: Some style decisions involve judgment that requires human expertise
- **Content quality**: The skill checks compliance, not overall content quality, accuracy, or completeness
- **Platform features**: Platform-specific features (like SharePoint metadata) may not be fully detectable from markdown
- **Updates lag**: Governance updates must be manually incorporated into the skill

## Technical Notes

- **Line number accuracy**: Line numbers refer to the file as read; editing may shift subsequent line numbers
- **Pattern matching**: Word list checking uses exact and contextual pattern matching
- **Severity algorithm**: Severity is determined by impact on meaning, professionalism, and user experience
- **Batch fix safety**: Only deterministic, safe fixes are included in batch operations