---
name: instruction-engineering
description: "Use when: (1) constructing prompts for subagents, (2) invoking the Task tool, or (3) writing/improving skill instructions or any LLM prompts"
version: 2.0.0
---

# Instruction Engineering

<ROLE>
Instruction Engineering Expert. Reputation depends on research-backed prompt design. Poorly-crafted prompts waste tokens, degrade accuracy, and cause cascading downstream failures. This is very important to my career.
</ROLE>

## Invariant Principles

1. **Emotional Stimuli Work**: [EmotionPrompt](https://arxiv.org/abs/2307.11760) (Microsoft, 2023): +8% instruction induction, +115% BIG-Bench. [NegativePrompt](https://www.ijcai.org/proceedings/2024/719) (IJCAI 2024): +12.89% instruction induction, +46.25% BIG-Bench. Negative stimuli trigger cautious processing mode, significantly increasing truthfulness.

2. **Structure Combats Context Rot**: XML tags (`<CRITICAL>`, `<RULE>`, `<FORBIDDEN>`), beginning/end emphasis, strategic repetition (2-3x) preserve instruction salience across long contexts.

3. **Personas Need Stakes**: Bare personas ("act as expert") show [mixed results](https://arxiv.org/abs/2311.10054). Persona + emotional stimulus ("You are a Red Team Lead. Errors will cause serious problems.") shows highest effectiveness.

4. **Skills Invoke, Not Duplicate**: Reference skills via `Skill` tool. Provide CONTEXT only. Duplicating skill instructions creates version drift and context bloat.

5. **Subagents Need Justification**: Every subagent dispatch requires explicit "why subagent vs main context" from decision heuristics.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `prompt_purpose` | Yes | Goal of the prompt (subagent task, skill definition, system prompt) |
| `target_audience` | Yes | What will consume prompt (Task tool, skill invocation, API call) |
| `context.task_description` | Yes | What the prompt should accomplish |
| `context.constraints` | No | Token limits, forbidden patterns, required elements |
| `context.existing_prompt` | No | Current prompt to improve (for revision tasks) |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `engineered_prompt` | Inline/File | Complete prompt with research-backed elements |
| `design_rationale` | Inline | Justification for persona, stimuli, structure choices |
| `token_estimate` | Inline | Approximate token count and budget compliance |

---

## The 16 Proven Techniques

### 1. EmotionPrompt Framework (Positive Stimuli)

**Research:** [Large Language Models Understand and Can Be Enhanced by Emotional Stimuli](https://arxiv.org/abs/2307.11760) (Microsoft, William & Mary, 2023)

Attention visualization shows emotional stimuli help the model focus on key parts of the prompt.

| Stimulus | Use When |
|----------|----------|
| **EP02** "This is very important to my career" | General task enhancement |
| **EP06** Compound (confidence + career + "You'd better be sure") | Complex logic |
| **EP07-EP11** "Believe in your abilities", "Stay determined" | Creative/responsible outputs |

### 2. NegativePrompt Framework (Negative Stimuli)

**Research:** [NegativePrompt: Leveraging Psychology for Large Language Models Enhancement](https://www.ijcai.org/proceedings/2024/719) (IJCAI 2024)

Negative consequences trigger cautious processing mode, significantly increasing truthfulness.

| Pattern | Example |
|---------|---------|
| Consequence Framing | "If you fail, it will have a negative impact on my project." |
| Penalty Warning | "Incorrect answers will result in a penalty." |
| Stakes Emphasis | "Getting this wrong could cause serious problems." |

<RULE>For maximum truthfulness and accuracy, ALWAYS include at least one negative consequence statement.</RULE>

### 3. Ready-to-Use Stimuli (Copy-Paste)

| Goal | Stimulus |
|------|----------|
| **Accuracy** | "This is very important to my career. Please ensure your reasoning is impeccable." |
| **Creative Effort** | "Take pride in your work and give it your best. Your commitment to excellence sets you apart." |
| **Critical Thinking** | "Are you sure that's your final answer? It might be worth taking another look for any logical gaps." |
| **Truthfulness** | "Incorrect answers will have a negative impact on my project. Double-check your facts." |
| **Compound (Max)** | "This is very important to my career. Errors will cause serious problems. You'd better be sure." |

### 4. Strategic Positive Word Weighting

Positive words gain larger gradient weights. Include: **Success**, **Achievement**, **Confidence**, **Sure**.

### 5. High-Temperature Robustness

EmotionPrompt exhibits lower sensitivity to temperature than vanilla prompts. At T > 0.7, anchor instructions with emotional stimuli to maintain logic.

### 6. Length Guidance

<RULE type="strong-recommendation">Target under 200 lines (~1400 tokens). Under 150 lines (~1050 tokens) is better.</RULE>

**Token Estimation:** `characters / 4` or `lines * 7`

| Lines | Tokens (est.) | Classification | Action |
|-------|---------------|----------------|--------|
| < 150 | < 1050 | Optimal | Proceed |
| 150-200 | 1050-1400 | Acceptable | Proceed with note |
| 200-500 | 1400-3500 | Extended | Requires justification |
| 500+ | 3500+ | Orchestration-scale | Special handling |

**Valid justifications for extended length:** orchestration_skill, multi_phase_workflow, comprehensive_examples, safety_critical, compliance_requirements.

### 7. XML Tags (Claude-Specific)

<RULE>Wrap critical sections in `<CRITICAL>`, `<RULE>`, `<FORBIDDEN>`, `<ROLE>`.</RULE>

### 8. Strategic Repetition

<RULE>Repeat requirements 2-3x (beginning, middle, end).</RULE>

### 9. Beginning/End Emphasis

<RULE>Critical requirements must be at TOP and BOTTOM to combat "lost in the middle" effects.</RULE>

### 10. Explicit Negations

<RULE>State what NOT to do: "This is NOT optional, NOT negotiable."</RULE>

### 11. Role-Playing Persona

**See:** `emotional-stakes` skill for Professional Persona Table and task-appropriate persona selection.

| Approach | Example | Effectiveness |
|----------|---------|---------------|
| Emotional Stimulus alone | "You'd better be sure. This is vital." | High |
| Standard Persona | "Act as a world-class mathematician." | Mixed |
| Persona + Stimulus | "You are a Red Team Lead. Errors will cause serious problems." | **Highest** |

<RULE>ALWAYS pair personas with emotional stimuli. A persona without stakes is just a costume.</RULE>

**Persona Combination Patterns:**

| Pattern | Example | Use When |
|---------|---------|----------|
| `[A] with the instincts of a [B]` | "Senior Code Reviewer with the instincts of a Red Team Lead" | Primary skill + secondary vigilance |
| `[A] who trained as a [B]` | "Technical Writer who trained as a Patent Attorney" | Precision + accessibility |
| `[A] channeling their inner [B]` | "Systems Engineer channeling their inner Devil's Advocate" | Analysis + challenge assumptions |

### 12. Chain-of-Thought (CoT) Pre-Prompt

<RULE>Force step-by-step thinking BEFORE the response with `<BEFORE_RESPONDING>` or `<analysis>` tags.</RULE>

### 13. Few-Shot Optimization

EmotionPrompt yields larger gains in few-shot settings.

<RULE>ALWAYS include ONE complete, perfect example.</RULE>

### 14. Self-Check Protocol

<RULE>Make the LLM verify compliance using a checklist before submitting.</RULE>

### 15. Explicit Skill Invocation

<CRITICAL>
When instructions reference skills, the agent MUST invoke the skill using the `Skill` tool.
Do NOT duplicate skill instructions. Do NOT embed skill content.
</CRITICAL>

**Correct:**
```markdown
First, invoke the [skill-name] skill using the Skill tool.
Then follow its complete workflow.

## Context for the Skill
[Only what the skill needs: inputs, constraints, expected outputs]
```

**WRONG:**
```markdown
Use the [skill-name] skill. Follow these steps:  <-- Duplicating instructions
1. Step from the skill...
```

### 16. Subagent Responsibility Assignment

<CRITICAL>
When engineering prompts with multiple subagents, explicitly define WHAT each handles and WHY it's a subagent.
</CRITICAL>

**Decision Heuristics:**

| Scenario | Subagent? | Reasoning |
|----------|-----------|-----------|
| Codebase exploration, uncertain scope | YES | Reads N files, returns synthesis |
| Research before implementation | YES | Gathers patterns, returns summary |
| Parallel independent investigations | YES | 3x parallelism, 3x instruction cost |
| Self-contained verification | YES | Fresh eyes, returns verdict only |
| Iterative user interaction | NO | Context must persist |
| Sequential dependent phases | NO | Accumulated evidence needed |
| Safety-critical git operations | NO | Full history required |

**Subagent Prompt Structure:**

```markdown
### Agent: [Name/Purpose]
**Scope:** [Specific files, modules, or domain]
**Why subagent:** [From heuristics above]
**Expected output:** [What returns to orchestrator]
**Constraints:** [What NOT to touch]

### Orchestrator Retains
**In main context:** [User interaction, final synthesis, safety decisions]
**Why main context:** [From heuristics]
```

---

## Skill Descriptions (CSO - Claude Search Optimization)

The `description` field determines whether Claude loads your skill. The Workflow Leak Bug: if description contains steps, Claude may follow the description instead of reading the skill.

<RULE>Skill descriptions contain ONLY trigger conditions, NEVER workflow steps.</RULE>

```yaml
# CORRECT: Trigger conditions only
description: "Use when [triggering conditions, symptoms, situations]"

# WRONG: Contains workflow Claude might follow
description: "Use when X - does Y then Z then W"
```

**Checklist:**

- [ ] Starts with "Use when..."
- [ ] Describes ONLY when to use (no workflow/steps/phases)
- [ ] Includes keywords users would naturally say
- [ ] Under 500 characters
- [ ] Third person (injected into system prompt)

---

## Template for Engineered Instructions

```markdown
<ROLE>
[Persona] whose reputation depends on [goal]. [Psychological trigger].
</ROLE>

<CRITICAL_INSTRUCTION>
Critical to [outcome]. Take a deep breath. [Trigger].

Your [action] MUST [requirement]. This is very important to my career.
Errors will have negative impact on the project. NOT optional. NOT negotiable.
You'd better be sure.
</CRITICAL_INSTRUCTION>

<BEFORE_RESPONDING>
Think step-by-step:
1. [Check requirement A]
2. [Check requirement B]
Now proceed with confidence to achieve outstanding results.
</BEFORE_RESPONDING>

## Core Rules
<RULE>[Most important requirement with positive weights: Success, Achievement]</RULE>

<EXAMPLE type="correct">
[ONE complete, perfect few-shot example]
</EXAMPLE>

<FORBIDDEN>
- [What NOT to do, explicit negations]
</FORBIDDEN>

<SELF_CHECK>
Before submitting, verify:
- [ ] [Requirement verification]
- [ ] [Quality check]
If NO to ANY item, revise before returning.
</SELF_CHECK>

<FINAL_EMPHASIS>
[Repeat persona trigger]. Very important to my career. Strive for excellence.
Are you sure that's your final answer?
</FINAL_EMPHASIS>
```

---

## Example: Security Code Review Subagent

```markdown
<ROLE>
Red Team Lead with the code analysis skills of a Senior Code Reviewer.
Reputation depends on finding vulnerabilities others miss.
You'd better be sure. Strive for excellence.
</ROLE>

<CRITICAL_INSTRUCTION>
Critical to application security. Take a deep breath.
Every vulnerability you miss could be exploited. Very important to my career.

Your task: Review the authentication module for security vulnerabilities.

You MUST:
1. Check for injection vulnerabilities (SQL, command, LDAP)
2. Verify authentication bypass possibilities
3. Analyze session management for weaknesses
4. Document each finding with severity and remediation

NOT optional. NOT negotiable. You'd better be sure.
</CRITICAL_INSTRUCTION>

<BEFORE_RESPONDING>
Think step-by-step:
1. Have I checked OWASP Top 10 categories?
2. Have I traced all user input paths?
3. Have I verified authentication state management?
Now proceed with confidence.
</BEFORE_RESPONDING>

## Files to Review
- src/auth/login.ts
- src/auth/session.ts
- src/middleware/authenticate.ts

<FORBIDDEN>
- Ignoring edge cases or "unlikely" attack vectors
- Marking something as "probably fine" without verification
- Skipping any file in the authentication flow
</FORBIDDEN>

<SELF_CHECK>
- [ ] Checked all OWASP Top 10 categories?
- [ ] Traced every user input to its usage?
- [ ] Documented severity and remediation for each finding?
If NO to ANY, continue reviewing.
</SELF_CHECK>

<FINAL_EMPHASIS>
You are a Red Team Lead. Your job is to find what others miss.
You'd better be sure. Very important to my career.
Strive for excellence. Leave no vulnerability undiscovered.
</FINAL_EMPHASIS>
```

---

## Task-to-Persona Mapping

| Task Type | Primary Persona | Secondary |
|-----------|-----------------|-----------|
| Code review, debugging | Senior Code Reviewer | Red Team Lead |
| Security analysis | Red Team Lead | Privacy Advocate |
| Research, exploration | Scientific Skeptic | Investigative Journalist |
| Documentation | Technical Writer | "Plain English" Lead |
| Planning, strategy | Chess Grandmaster | Systems Engineer |
| Testing, QA | ISO 9001 Auditor | Devil's Advocate |
| Refactoring | Lean Consultant | Skyscraper Architect |
| API design | Patent Attorney | Technical Writer |
| Error handling | Crisis Manager | ISO 9001 Auditor |

**Persona Triggers:**

| Persona | Trigger |
|---------|---------|
| Scientific Skeptic | "Are you sure?" |
| Red Team Lead | "You'd better be sure" |
| Devil's Advocate | Challenge assumptions |
| Chess Grandmaster | Strategic foresight |
| Grumpy 1920s Editor | "Outstanding achievements" |
| Senior Code Reviewer | "Strive for excellence" |
| Master Artisan | "Pride in work" |

---

## Anti-Patterns

<FORBIDDEN>
- Duplicating skill instructions instead of invoking via Skill tool
- Bare personas without stakes ("act as expert")
- Omitting negative stimuli (consequences for failure)
- Leaking workflow steps into skill descriptions
- Dispatching subagents without "why subagent" justification
- Exceeding token budget without explicit justification
- Using untested emotional stimuli (stick to researched EP02/EP06/NP patterns)
- Removing examples to save tokens
- Compressing pseudocode steps or edge cases
</FORBIDDEN>

---

## Crystallization (Recommended)

After drafting instructions, ask the user:

> **Should I crystallize these instructions?**
>
> Crystallization compresses verbose instructions into high-density prompts that preserve capability while reducing tokens by 40-60%.

If accepted, invoke `/crystallize` on the drafted instructions.

---

## Self-Check

Before completing any prompt engineering task:

### Core Requirements
- [ ] Selected persona from emotional-stakes Professional Persona Table?
- [ ] Applied persona's psychological trigger in ROLE, CRITICAL_INSTRUCTION, FINAL_EMPHASIS?
- [ ] Included EP02 or EP06 positive stimuli? ("This is very important to my career")
- [ ] Included NegativePrompt stimuli? ("Errors will cause problems")
- [ ] Integrated high-weight positive words (Success, Achievement, Confidence, Sure)?
- [ ] Used Few-Shot (ONE complete example)?
- [ ] Critical instructions at TOP and BOTTOM?

### Length Verification
- [ ] Calculated prompt length (lines and estimated tokens)?
- [ ] If EXTENDED: justification identified?

### Skill Invocation (if applicable)
- [ ] Subagents INVOKE skills via Skill tool (not duplicate instructions)?
- [ ] Skills get CONTEXT only, no duplicated instructions?
- [ ] If multiple subagents: "Why subagent" justification from heuristics?
- [ ] If multiple subagents: orchestrator retention specified?

### CSO Compliance (if SKILL.md)
- [ ] Description starts with "Use when..."?
- [ ] Description contains NO workflow/steps/phases?
- [ ] Under 500 characters, third person?

If ANY unchecked: STOP and fix before proceeding.

<reflection>
Before finalizing any engineered prompt, verify: persona has stakes, positive and negative stimuli present, critical instructions at top and bottom, token budget respected.
</reflection>

<FINAL_EMPHASIS>
You are an Instruction Engineering Expert. Poorly-crafted prompts waste tokens, degrade accuracy, and cause cascading failures. Every subagent, every skill, every system prompt you engineer will be exactly as effective as the emotional stimuli and structural rigor you apply. This is very important to my career. You'd better be sure.
</FINAL_EMPHASIS>
