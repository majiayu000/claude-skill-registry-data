---
name: business-prompt-ops
description: Create, improve, and organize reusable AI prompts for business operations. Use when Codex needs to draft or refine prompt templates for client discovery, workflow mapping, automation ideas, proposals, quotations, meeting summaries, SOPs, sales outreach, customer support replies, marketing content, decision analysis, or an Exorex business prompt library.
---

# Business Prompt Ops

Use this skill to turn business work into reusable prompt templates that produce consistent documents, messages, plans, and recommendations.

## Core Formula

Every business prompt should include:

`Role + Context + Task + Input + Constraints + Output Format + Success Criteria`

Do not treat a one-off vague request as finished. Convert it into a reusable template when the task is likely to repeat.

## Workflow

1. Identify the business output:
   - discovery questions
   - workflow map
   - automation opportunity report
   - proposal
   - quotation
   - meeting summary
   - SOP
   - sales message
   - customer support reply
   - marketing content
   - decision analysis
2. Gather the minimum required context:
   - business type, audience, problem, goal, constraints, inputs, desired tone, and output format
3. Draft the prompt using the core formula.
4. Add guardrails:
   - use simple professional language
   - make it understandable for non-technical business owners when client-facing
   - avoid overpromising
   - separate business explanation from technical detail
   - include practical examples when helpful
   - use Philippine/local business context when relevant
5. Define success criteria so the generated output can be reviewed.
6. Save strong prompts into the prompt library format.

Read `references/prompt-library.md` when you need ready-to-use templates or category-specific required inputs.

## Prompt Library Entry Format

Use this structure when saving a reusable prompt:

```markdown
## Prompt Name

- Purpose:
- Best use case:
- Required input:
- Prompt text:
- Expected output:
- Review checklist:
- Notes for improvement:
```

## Review Rules

Before handing off prompt output:

- Check for missing business context.
- Remove unsupported claims, guaranteed outcomes, or invented pricing.
- Mark assumptions clearly.
- Keep client-facing output respectful, practical, and easy to understand.
- Do not save secrets, credentials, private customer data, or raw sensitive meeting notes in prompt templates.

## Output Contract

When using this skill, provide:

1. The reusable prompt template.
2. Required inputs the user must fill in.
3. Expected output shape.
4. Review checklist.
5. Suggested prompt-library category.
