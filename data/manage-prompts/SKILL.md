---
name: manage-prompts
description: MUST INVOKE this skill when creating focused prompts in .prompts/prompts/ and multi-stage chains in .prompts/metaprompt/. Create, audit, and maintain all types of prompts including standalone prompts and meta-prompts for AI-to-AI workflows.
---

# Objective

Create effective prompts for both direct execution and multi-stage AI-to-AI workflows. This skill handles standalone prompts and meta-prompts (chains where outputs from one prompt become inputs for the next).

# Prompt Categories

## Single Prompts

Standalone prompts for direct execution by users or agents.

- **Analysis**: Examine and interpret information, extract insights
- **Generation**: Create new content or artifacts
- **Review**: Quality checks, validation, critique
- **Transformation**: Conversion, extraction, summarization
- **Q&A**: Answer specific questions
- **Creative**: Brainstorming, ideation, problem-solving

## Meta-Prompts

Multi-stage prompt chains for Claude-to-Claude communication where outputs feed into subsequent prompts.

- **Research Prompts**: Gather information, analyze options, produce findings
- **Plan Prompts**: Create implementation roadmaps and strategies
- **Do Prompts**: Execute tasks, produce artifacts
- **Refine Prompts**: Improve existing prompts with versioning

# Output Structure

## Single Prompts

```
.prompts/prompts/
├── {number}-{name}.md    # The prompt file
└── SUMMARY.md             # Summary of created prompt
```

## Meta-Prompts

```
.prompts/metaprompt/
├── {number}-{topic}-{purpose}/
│   ├── {number}-{topic}-{purpose}.md  # The prompt file
│   ├── {topic}-{purpose}.md            # Output file (for Research/Plan)
│   ├── completed/                      # Archive after running
│   └── SUMMARY.md                      # Required: executive summary
```

# Prompt Numbering

Auto-increment from existing prompts:
```bash
# Single prompts
find .prompts/prompts -name "*.md" | wc -l

# Meta-prompts
find .prompts/metaprompt -type d -name "*-*" | wc -l
```

# Key Methodology

## Hybrid XML/Markdown Structure

**XML Containers** (Use Sparingly - max 3-5 tags):
- `<context>` - Large data dumps or background info
- `<workflow>` - Non-negotiable step sequences
- `<constraints>` - Negative constraints (NEVER/MUST NOT)
- `<output_format>` - Machine-parseable responses

**Markdown** (Most Content):
- Instructions and guidance
- Explanations and descriptions
- Examples and demonstrations

**Critical Rules**:
- Limit to 3-5 XML tags maximum
- Never nest XML tags
- Reserve XML for highly structured workflows

## Prompt Creation Steps

### Single Prompts

1. **Understand the Task**: What inputs, outputs, context?
2. **Select Type**: Analysis, Generation, Review, etc.
3. **Apply Structure**: XML for containers, Markdown for instructions
4. **Include Examples**: Concrete examples where helpful
5. **Add Verification**: How to confirm successful output

### Meta-Prompts

1. **Design the Chain**: Research → Plan → Do sequence
2. **Structure Each Prompt**: Use hybrid XML/Markdown
3. **Set Dependencies**: Reference previous outputs with `@` syntax
4. **Add YAML Frontmatter**: Include confidence, dependencies, questions
5. **Create SUMMARY.md**: Required for each prompt in the chain

## Chaining Patterns

- **Sequential**: Each prompt depends on previous output
- **Parallel**: Multiple prompts run simultaneously
- **Mixed**: Parallel layer feeds into sequential step

# Reference Files

## Single Prompts

- `references/prompt-types.md` - Detailed type guidance
- `references/single-prompt-templates.md` - Template patterns
- `references/optimization-guide.md` - Quality improvement

## Meta-Prompts

- `references/research-patterns.md` - Research prompt structure
- `references/plan-patterns.md` - Plan prompt structure
- `references/do-patterns.md` - Do prompt structure
- `references/refine-patterns.md` - Refine prompt structure
- `references/metadata-guidelines.md` - YAML frontmatter requirements
- `references/summary-template.md` - SUMMARY.md structure
