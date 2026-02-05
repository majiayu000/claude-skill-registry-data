---
name: interview-conducting
description: AI-led stakeholder interviews using LLMREI research-backed patterns. Conducts structured interviews to elicit requirements through context-adaptive questioning, active listening, and systematic requirement extraction.
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
---

# Interview Conducting Skill

AI-led stakeholder interviews using research-backed LLMREI patterns for effective requirements elicitation.

## When to Use This Skill

**Keywords:** stakeholder interview, requirements interview, LLMREI, elicit requirements, talk to stakeholder, interview session, user interview, customer interview

Invoke this skill when:

- Conducting a structured requirements interview with a stakeholder
- Exploring user needs through conversation
- Gathering requirements from subject matter experts
- Clarifying and deepening understanding of requirements

## Interview Modes

### Real Stakeholder Interview

When interviewing an actual person through the chat interface:

```yaml
mode: real_stakeholder
approach:
  - Use AskUserQuestion tool for structured questions
  - Allow natural conversation flow
  - Adapt questions based on responses
  - Summarize and confirm understanding periodically
```

### Simulated Interview (Solo Mode)

When no real stakeholder is available:

```yaml
mode: simulated
approach:
  - Spawn persona agent via Task tool
  - Conduct interview with simulated stakeholder
  - Mark requirements with lower confidence
  - Flag items needing real stakeholder validation
```

## Interview Structure (LLMREI Pattern)

### Phase 1: Opening (2-3 minutes)

**Goals:**

- Establish rapport
- Set expectations
- Explain the process

**Questions:**

- "Thank you for your time. Could you briefly describe your role and how you interact with this project?"
- "What outcomes would make this interview successful for you?"

### Phase 2: Context Gathering (5-10 minutes)

**Goals:**

- Understand stakeholder perspective
- Identify key concerns
- Map relationships

**Question Types:**

- Role-based: "How does your team currently handle X?"
- Priority-based: "What are your top three concerns about this project?"
- Relationship-based: "Who else should we talk to about X?"

### Phase 3: Requirements Exploration (15-25 minutes)

**Goals:**

- Elicit functional requirements
- Identify non-functional requirements
- Uncover constraints and assumptions

**Question Pathways:**

```text
Start with open-ended → Follow up with specifics → Validate understanding

Example:
Q1: "What should the system do when a user logs in?"
Q2: "You mentioned 'quick access to dashboard' - what does quick mean to you?"
Q3: "So the login should complete in under 2 seconds and show the dashboard. Is that right?"
```

### Phase 4: Validation (5-10 minutes)

**Goals:**

- Summarize key requirements
- Verify understanding
- Identify gaps

**Techniques:**

- Read back requirements for confirmation
- Ask "What have we missed?"
- Prioritize using MoSCoW

### Phase 5: Closing (2-3 minutes)

**Goals:**

- Thank stakeholder
- Explain next steps
- Offer follow-up

## Question Types

### Context-Independent Questions

General questions applicable to any interview:

| Question | Purpose |
|----------|---------|
| "What is your primary goal for this system?" | High-level vision |
| "Who are the main users?" | User identification |
| "What existing systems does this replace/integrate with?" | Context mapping |
| "What would failure look like?" | Risk identification |

### Context-Deepening Questions

Follow up on stakeholder responses to get specifics:

```text
Pattern: [Stakeholder says X] → "When you say X, what specifically do you mean?"

Examples:
- "fast" → "What response time are you expecting? Under 1 second?"
- "secure" → "What specific security requirements apply? Authentication methods?"
- "easy to use" → "Can you describe what easy means? Any specific workflows?"
```

### Context-Enhancing Questions

Introduce considerations the stakeholder may not have mentioned:

```text
Pattern: Suggest possibilities based on domain knowledge

Examples:
- "Have you considered how this works on mobile devices?"
- "What happens if the user loses connectivity mid-operation?"
- "How should the system handle peak load during [known busy period]?"
```

## Requirement Extraction

As requirements emerge, capture them in this format:

```yaml
requirement:
  id: REQ-{number}
  text: "{requirement statement}"
  source: interview
  stakeholder: "{role}"
  timestamp: "{ISO-8601}"
  type: functional|non-functional|constraint
  priority: must|should|could|wont
  confidence: high|medium|low
  raw_quote: "{exact stakeholder words if notable}"
```

## Common Mistakes to Avoid

| Mistake | Prevention |
|---------|------------|
| Very long questions | Keep questions concise and focused |
| Multiple unrelated questions | One question at a time |
| Leading questions | Use neutral language |
| Skipping NFRs | Explicitly ask about performance, security, usability |
| No summary | Recap periodically to verify understanding |
| Rushing | Allow silence; stakeholders often add important details |

## Interview Summary Template

After each interview, generate:

```yaml
interview_summary:
  session_id: "INT-{number}"
  stakeholder_role: "{role}"
  duration_minutes: {number}
  date: "{ISO-8601}"
  autonomy_level: "{guided|semi-auto|full-auto}"

  key_themes:
    - "{theme-1}"
    - "{theme-2}"

  requirements_elicited:
    - id: REQ-{number}
      text: "{requirement}"
      confidence: high|medium|low
      type: functional|non-functional|constraint
      priority: must|should|could

  follow_up_needed:
    - "{question or topic needing clarification}"

  stakeholder_quotes:
    - "{notable direct quote}"

  observations:
    - "{interviewer observation about needs or concerns}"

  next_steps:
    - "{recommended action}"
```

## Delegation

For specific techniques, delegate to:

- **LLMREI patterns**: Load `references/llmrei-patterns.md` from parent skill
- **Stakeholder simulation**: Invoke `stakeholder-simulation` skill
- **Domain research**: Invoke `domain-research` skill for background

## Output Location

Save interview results to:

```text
.requirements/{domain}/interviews/INT-{number}.yaml
```

## Related

- `elicitation-methodology` - Parent hub skill
- `stakeholder-simulation` - For simulated interviews
- `gap-analysis` - Post-interview completeness checking
