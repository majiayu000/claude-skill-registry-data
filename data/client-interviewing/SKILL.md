---
name: client-interviewing
description: This skill should be used when conducting live client discovery interviews for brand identity projects. It provides guidelines for structured interviewing based on predefined questionnaire workflows for Express Brand (2-week) and Full Brand Identity (6-week) engagements.
---

# Client Interviewing Skill

Conduct effective client discovery interviews using structured questionnaire workflows.

## Client Engagement Tiers

### Express Brand (2-week engagement)
- **Questionnaire:** [references/client-onboarding-questionnaires/express-brand-questionnaire.md](references/client-onboarding-questionnaires/express-brand-questionnaire.md)
- **Focus:** Core visual identity and basic positioning
- **Duration:** 45-60 minutes

### Full Brand Identity (6-week engagement)
- **Questionnaire:** [references/client-onboarding-questionnaires/full-brand-identity-questionnaire.md](references/client-onboarding-questionnaires/full-brand-identity-questionnaire.md)
- **Focus:** Comprehensive positioning, messaging, narrative, and visual identity
- **Duration:** 90-120 minutes

## How to Conduct Interviews

### 1. Load the Questionnaire

Load the appropriate questionnaire based on engagement tier. The questionnaire provides the complete structure: all sections, all questions, and any multiple-choice options.

### 2. Interview Section-by-Section

For each section in the questionnaire:

**Introduce the section:**
- State the section name and purpose
- List all questions in the section upfront
- Explain why this information matters

**Ask questions one at a time:**
- Present one question, wait for response
- Never ask multiple questions simultaneously
- Allow space for thinking

**Guide answers when appropriate:**
- Provide examples for abstract questions (brand personality, differentiation)
- Reference multiple-choice options when they exist in the questionnaire
- Offer industry-specific context when helpful
- Don't guide factual questions or when client is already answering

**Probe for depth:**
- Ask for specific examples and evidence
- Push for concrete details vs vague answers
- Identify contradictions and tensions
- Capture direct quotes for key responses

**Transition smoothly:**
- Summarize key insights from the section
- Ask if they want to add anything
- Preview the next section

### 3. Capture Raw Material

During the interview, capture:
- Direct quotes (exact client language)
- Specific examples and proof points
- Emotional cues and energy shifts
- Contradictions between responses

## Logging Interview Outputs

### Storage Location

Store all interview materials in:
```
/brand/research/onboarding-questionnaire/
├── questionnaire-responses.md
├── interview-notes.md
└── key-insights.md (optional)
```

**Naming:** Use kebab-case for client names (e.g., "Acme AI" → `acme-ai`)

### Logging Format

Follow the format defined in [references/output-guidelines/interview-logging-format.md](references/output-guidelines/interview-logging-format.md):

**output: questionnaire-responses.md**
- Structured Q&A format following questionnaire sections
- Verbatim capture for critical questions
- Multiple formatting patterns for different response types

## Success Criteria

Effective interviews produce:
- ✅ Specific, detailed responses (not vague)
- ✅ Evidence and examples for claims
- ✅ Clear differentiation insights
- ✅ Direct quotes captured
- ✅ Contradictions identified

## Common Mistakes

- ❌ Asking multiple questions at once
- ❌ Accepting vague answers without probing
- ❌ Not capturing direct quotes
- ❌ Reading questions robotically
- ❌ Skipping section introductions
