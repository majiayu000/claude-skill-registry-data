---
name: ddd-strategic-design
description: Guide for DDD strategic design - analyzing domains through structured questioning, conducting stakeholder interviews (PM/domain experts/users), and producing Bounded Context analysis, Context Maps, and Ubiquitous Language. Use when user needs help understanding domain boundaries, planning domain interviews, or structuring DDD strategic artifacts.
---

# DDD Strategic Design

## Overview

This skill guides Domain-Driven Design strategic analysis through systematic questioning and interview planning. It helps extract domain knowledge from chaotic inputs, structure interviews with different stakeholders, and produce standard DDD strategic outputs.

## Workflow

### Phase 1: Input Diagnosis

When user provides unclear or mixed information about a system:

1. **Identify what you have**: Analyze the input type (code, documents, verbal description, requirements)
2. **Identify what's missing**: Determine gaps in domain understanding
3. **Ask clarifying questions** to establish:
   - Business context and goals
   - Key user roles and workflows
   - System boundaries and constraints
   - Existing pain points or complexity

**Questioning principles:**
- Start broad, then narrow down
- Ask one question at a time to avoid overwhelming
- Use "why" to uncover business rules
- Use "what if" to discover edge cases
- Use "who" to identify stakeholders and their needs

### Phase 2: Domain Exploration

Guide domain discovery through progressive questioning:

1. **Identify core business concepts**: What are the key entities, events, and processes?
2. **Find natural boundaries**: Where do terms mean different things? Where do teams/processes separate?
3. **Discover business rules**: What constraints, validations, or policies exist?
4. **Map workflows**: How do different parts of the system interact?

**Red flags for context boundaries:**
- Same term with different meanings in different areas
- Different teams owning different parts of workflow
- Independent change cycles
- Different data consistency requirements

### Phase 3: Interview Planning

When user needs to interview stakeholders, generate targeted question sets:

**For Product Managers** - See `references/pm-questions.md`:
- Business goals and priorities
- Success metrics
- Roadmap and constraints

**For Domain Experts** - See `references/expert-questions.md`:
- Business rules and terminology
- Edge cases and exceptions
- Domain constraints and invariants

**For End Users** - See `references/user-questions.md`:
- Actual workflows and pain points
- Task sequences and decision points
- Desired outcomes

### Phase 4: Synthesis and Output

Transform gathered knowledge into DDD artifacts:

1. **Bounded Context Analysis** - Document each context's purpose, boundaries, and responsibilities
2. **Context Map** - Visualize relationships between contexts using standard DDD patterns
3. **Ubiquitous Language** - Create glossary of domain terms with precise definitions

See `references/output-templates.md` for detailed formats and examples.

## Iterative Refinement

Domain understanding evolves. After initial analysis:
- Identify remaining ambiguities
- Suggest follow-up questions
- Validate assumptions with stakeholders
- Refine boundaries based on new insights

## References

This skill includes interview question templates and output format guides:

- `references/pm-questions.md` - Question framework for Product Manager interviews
- `references/expert-questions.md` - Question framework for Domain Expert interviews  
- `references/user-questions.md` - Question framework for End User interviews
- `references/output-templates.md` - Templates for Bounded Context analysis, Context Map, and Ubiquitous Language

