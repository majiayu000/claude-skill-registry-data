---
name: idea-honing
description: Clarify feature ideas through iterative Q&A, recording insights to guide concept development
---

# Idea Honing Skill

## Purpose

Clarify and refine feature ideas through structured questioning. This process helps uncover ambiguities, edge cases, and design considerations before writing the formal concept document.

## When to Use

- User has a rough feature idea but it's not fully formed
- Before writing a concept document
- When a feature idea needs more clarity
- To explore design space and tradeoffs

## Prerequisites

- User has described a rough feature idea
- Feature number and name have been determined (or will be determined)

## Procedure

### 1. Determine Feature Number and Name

If not already determined:

```bash
ls -1d ./docs/features/[0-9][0-9][0-9][0-9]-* 2>/dev/null | tail -1
```

Work with user to choose the next number and a descriptive name.

### 2. Create Planning Directory

```bash
mkdir -p ./planning/NNNN-feature-name
```

### 3. Initialize Idea Honing Document

```bash
cat > ./planning/NNNN-feature-name/idea-honing.md << 'EOF'
# Idea Honing: Feature Name

## Initial Idea

[User's rough description of the feature]

## Questions & Answers

EOF
```

### 4. Generate Initial Questions

Based on the user's rough idea, identify ambiguities and generate questions about:
- Use cases and user workflows
- Scope and boundaries
- Integration points
- Edge cases
- Tradeoffs and constraints
- Success criteria

Create a list of questions to explore.

### 5. Ask Questions ONE AT A TIME

**CRITICAL**: Only ask ONE question at a time.

For each question:
1. Ask the question clearly
2. Wait for the user's answer
3. Discuss and refine the answer if needed
4. Once satisfied, write the Q&A to the document
5. If new ambiguity emerges, add it to your question list
6. Move to the next question

### 6. Update Document After Each Q&A

After each question is answered, append to the document:

```bash
cat >> ./planning/NNNN-feature-name/idea-honing.md << 'EOF'

### Q: [Question text]

**A**: [Answer text]

EOF
```

### 7. Evolve the Process

As you work through questions:
- New ambiguities may emerge - add them as new questions
- Some questions may become irrelevant - skip them
- The process builds on itself organically

**If a question is about existing code behavior** (e.g., "How does X work today?"):
- Note it as needing research
- Continue with other questions
- These will be addressed in follow-up research

### 8. Conclude When Clear

When the feature idea is sufficiently clear:
- Summarize key insights
- Confirm with user that they're ready to write the concept
- The idea-honing document remains in `planning/` for reference

## Validation

Check the idea-honing document:

```bash
# Verify document exists
ls ./planning/NNNN-feature-name/idea-honing.md

# Review content
cat ./planning/NNNN-feature-name/idea-honing.md
```

## Common Issues

**Asking multiple questions at once**: Only ask ONE question at a time. This keeps focus and allows deeper exploration.

**Not recording answers**: Update the document after EACH question is answered, not in batches.

**Stopping too early**: Continue until the user feels confident about the feature scope and approach.

## Next Steps

After idea honing:
1. Use `propose-feature-concept` skill to write the formal concept
2. Reference the idea-honing document when writing the concept
3. The Q&A provides material for the concept's narrative
