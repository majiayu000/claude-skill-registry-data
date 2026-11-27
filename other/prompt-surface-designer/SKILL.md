---
name: prompt-surface-designer
description: "Designs the input experience for chat and agent surfaces - empty states, starter prompts, capability discovery, input affordances, follow-up suggestions, and first-run onboarding - with a capability inventory, starter-prompt scoring, and a blank-box risk assessment. Use when designing a new chat or agent interface; users stare at an empty prompt box and leave; writing starter prompts or suggested follow-ups; or improving discovery of what an assistant can do."
---

# Prompt Surface Designer

> A blank text box is the hardest interface ever shipped. Design what surrounds it.

## What this skill is

A workflow for designing everything around the prompt input of a chat, copilot, or agent surface. It starts from an inventory of what the system can actually do well, then designs the empty state, starter prompts, input affordances, follow-up suggestions, and first-run experience so users discover high-value capabilities and form accurate expectations. It treats the prompt box as a product surface, not a text field.

## What it solves

- Users who do not know what to ask, try one generic question, and leave
- Starter prompts that showcase demo tricks instead of the jobs users actually have
- Capabilities users never discover because they live only in documentation
- Inputs that force users to type context the system already has or could gather
- Follow-up suggestions that are generic ("Tell me more") rather than the next useful step
- First-run onboarding that tours the interface instead of getting the user to a first success

## When to invoke

- Designing a new chat, copilot, or agent entry point
- Analytics show high empty-state abandonment or short first sessions
- Writing or refreshing starter prompts and suggested follow-ups
- Launching new capabilities that users need to discover
- Adding attachments, context pickers, or structured inputs to a chat surface

## Phase 1: Build the capability inventory

List what the system can do, scored on reliability and user value. Discovery should promote only what works.

| Capability | Example request | Measured success rate | User value (1-5) | Frequency of need (1-5) |
|-----------|-----------------|----------------------:|-----------------:|------------------------:|
| Summarize a thread | "Summarize this customer thread" | 94 percent | 4 | 5 |

```
Promotion score = Success rate x User value x Frequency
Promote only capabilities with success rate at or above 85 percent
```

Also record **known limits**: what users are likely to ask that the system cannot do well. These become expectation-setting copy.

## Phase 2: Assess blank-box risk

Score the surface to decide how much scaffolding it needs:

| Factor | Low risk (1) | High risk (3) |
|--------|-------------|---------------|
| User familiarity with AI tools | Daily users | First-time users |
| Breadth of capability | Narrow, obvious purpose | Broad, general-purpose |
| Context awareness | Knows the user's current object or page | No context |
| Cost of a bad first result | Trivial | Damages adoption |

```
Blank-box risk = sum of factors (4-12)
4-6: light scaffolding (placeholder text, 2-3 starters)
7-9: moderate (contextual starters, capability hints, examples)
10-12: heavy (guided first task, structured entry, templates)
```

## Phase 3: Design the empty state and starter prompts

Empty state components, in order of importance:
1. **Context line** - what the assistant can see right now ("Working with: Q3 pipeline report")
2. **Starter prompts** - 3-4 tappable requests
3. **Capability hint** - one line on scope and one known limit
4. **Placeholder text** - a concrete example, not "Ask me anything"

Score each candidate starter prompt (0-2 each, keep those scoring 8 or more of 10):

| Criterion | 2 points if |
|-----------|-------------|
| Real job | Maps to a frequent task from research or logs |
| Reliable | Uses a capability above the success threshold |
| Contextual | References the user's current object, role, or data |
| Teaches | Reveals a capability the user would not guess |
| Specific | Concrete enough that the output is predictable |

Rotate starters by context (page, role, recent activity), not at random. Include at least one starter that shows a non-obvious capability.

## Phase 4: Design input affordances

Reduce what users must type and remember:

| Affordance | Use when |
|-----------|----------|
| Context chips (current file, selection, page) | The system can attach context automatically |
| Attachment and mention ("@" for people, files, records) | Users need to point at specific objects |
| Slash commands or action menu | Repeated structured tasks exist |
| Mode or scope selector | Distinct behaviors (search vs. draft vs. act) need different expectations |
| Structured fields | Required parameters (date range, recipient) are often omitted |
| Prompt editing and resend | Users iterate on the same request |
| Voice or paste-friendly input | Long-form or mobile input |

Show what context is attached before sending, and let users remove it.

## Phase 5: Design follow-up suggestions

Follow-ups should advance the job, not prolong the chat. Generate them from:
- **Next step in the workflow** - "Draft the reply to this customer"
- **Refinement of this output** - "Make it shorter", "Use the 2025 pricing"
- **Adjacent capability** - "Create a task from these action items"

Rules: 2-3 suggestions maximum, specific to the output just produced, and never a suggestion the system would likely fail at.

## Phase 6: Design first-run onboarding

Aim for a first successful outcome within 60 seconds:

| Step | Purpose |
|------|---------|
| Set expectations | One sentence on what it does well and one thing it does not |
| Guided first task | Pre-filled, high-reliability request using the user's own data |
| Show control | Point out edit, retry, and undo on the first result |
| Seed the next session | One suggestion for something to try next time |

Measure: time to first successful output, second-session return rate, and percent of users who use 3 or more distinct capabilities in the first week.

## Output

- Capability inventory with promotion scores and known limits
- Blank-box risk score and scaffolding level
- Empty state spec with context line, starter prompts, and placeholder copy
- Starter prompt scoring table and rotation rules
- Input affordance spec
- Follow-up suggestion rules and examples
- First-run onboarding flow with success metrics

## Operating rules

**Always**
- Promote only capabilities that clear a measured reliability threshold
- Make starter prompts contextual to the user's current work
- Show what context the system has before the user sends
- State one known limit alongside capabilities
- Measure time to first successful output

**Never**
- Use "Ask me anything" as the only guidance
- Showcase demo-friendly prompts that do not match real jobs
- Offer follow-ups the system is likely to fail
- Run an interface tour in place of a first real success
- Hide attached context the model will use
