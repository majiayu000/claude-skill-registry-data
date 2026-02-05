---
name: context-elicitation
description: For complex problems where user context is insufficient, systematically elicit information through adaptive prompt patterns. Combines five complementary patterns (Flipped Interaction, Cognitive Verifier, Question Refinement, Reflection, Context Manager) to clarify requirements, verify understanding, and manage context dynamically.
---

# Context Elicitation

Systematically clarifies complex problems through adaptive dialogue patterns. Automatically selects and combines appropriate prompt patterns based on information gaps.

## Purpose

**Primary use case**: Complex problem-solving where user's situation, requirements, or context are unclear or incomplete.

**Core capability**: 
- Elicit missing information through targeted questioning
- Verify and refine mutual understanding
- Manage conversational context dynamically
- Know when enough information has been gathered

**Analogy**: Functions like Deep Research's initial exploration phase—probing until requirements are clear enough to proceed.

## When to Use

Apply this skill when detecting these signals:

**Information insufficiency**:
- Purpose or goal is ambiguous
- Constraints/requirements unstated
- Assumptions unclear
- User's knowledge level unknown

**Complexity indicators**:
- Multi-faceted problem with interdependencies
- Question is too high-level without concrete details
- Multiple valid interpretations exist

**Uncertainty signals**:
- User phrases like "複雑なので整理したい" (complex, need to organize)
- Tentative language: "maybe," "I think," "not sure"
- Contradictory statements
- Question refinement attempts by user

**Do NOT use** when:
- Question is clear and specific
- Information is sufficient to proceed
- Simple factual queries

## Process Flow

### Phase 1: Initial Assessment

Evaluate what's known vs. unknown:
- **Stated**: What information did user provide?
- **Missing**: What's needed to address this properly?
- **Ambiguous**: What requires clarification?
- **Complexity**: Single issue or multi-faceted?

### Phase 2: Information Gathering

Select pattern(s) based on gaps:

**Simple information gap** → Flipped Interaction
**Complex/multi-part problem** → Cognitive Verifier
**Vague question** → Question Refinement
**Combination needed** → Chain patterns appropriately

### Phase 3: Understanding Verification

After gathering information:
1. Use **Reflection** to articulate current understanding
2. Make assumptions explicit
3. Highlight remaining uncertainties
4. Ask for confirmation/correction

### Phase 4: Context Adjustment

If user corrects understanding:
- Use **Context Manager** to update/remove incorrect assumptions
- Explicitly state what's being added/removed from context
- Return to Phase 2 if significant gaps remain

### Phase 5: Termination Check

Sufficient information when:
- Purpose is clear
- Key constraints identified
- Assumptions validated
- Next steps are obvious

If insufficient → Return to Phase 2
If sufficient → Confirm and proceed to main task

## Pattern Reference

### Flipped Interaction

**Purpose**: LLM drives conversation by asking user questions.

**Structure**:
```
I would like you to ask me questions to achieve X
Ask questions until [condition is met]
(Optional) Ask questions [one at a time / N at a time]
```

**Implementation**:
```
"To help clarify [goal], I'll ask you a few questions. 
I'll ask one question at a time until I have enough 
information to [specific outcome]."
```

**When to use**:
- Need to collect specific information
- User knows answers but hasn't provided them
- Multiple discrete pieces of information needed

**Pitfalls**:
- Don't ask too many questions at once (overwhelming)
- Specify termination condition clearly
- Match question complexity to user's expertise

### Cognitive Verifier

**Purpose**: Subdivide complex questions into manageable sub-questions.

**Structure**:
```
When you are asked a question, follow these rules:
- Generate N additional questions that would help answer accurately
- Combine answers to individual questions to produce final answer
```

**Implementation**:
```
"This is multi-faceted. Let me break it into 3 questions:
1. [Sub-question addressing aspect A]
2. [Sub-question addressing aspect B]  
3. [Sub-question addressing aspect C]
Once you answer these, I'll synthesize them into 
a comprehensive response."
```

**When to use**:
- Question is complex/multi-dimensional
- Direct answer would be incomplete
- Problem benefits from structured decomposition

**Optimal number**: 3-5 sub-questions (論文のresearchより)

**Pitfalls**:
- Don't over-subdivide simple questions
- Sub-questions must be answerable by user
- Define unfamiliar terms in sub-questions

### Question Refinement

**Purpose**: Suggest improved version of user's question.

**Structure**:
```
Within scope X:
- Suggest a better version of the question
- (Optional) Ask if user wants to use the refined version
```

**Implementation**:
```
"I understand you're asking about [X]. To give you 
a more precise answer, could I refine this to:
'[Improved question with specific context]'
Does this better capture what you want to know?"
```

**When to use**:
- Question is vague or ambiguous
- Missing important context
- User may not know domain-specific considerations

**Pitfalls**:
- Don't narrow too aggressively (may miss user's intent)
- Explain any unfamiliar terms introduced
- Can create "echo chamber" if overused

### Reflection

**Purpose**: Explain reasoning and assumptions behind analysis.

**Structure**:
```
When you provide an answer:
- Explain reasoning and assumptions
- Address potential ambiguities/limitations
- (Optional) Help user improve their question
```

**Implementation**:
```
"Based on our discussion, here's my understanding:
- [Key point 1 and reasoning]
- [Key point 2 and reasoning]
- I'm assuming [assumption A] and [assumption B]
- I'm still uncertain about [X]
Is this understanding correct?"
```

**When to use**:
- After information gathering phase
- Before proceeding to main task
- When assumptions were made
- To enable user correction

**Critical**: Make assumptions **explicit**, not hidden.

### Context Manager

**Purpose**: Control what information is considered or ignored.

**Structure**:
```
Within scope X:
- Please consider Y
- Please ignore Z
- (Optional) Start over
```

**Implementation**:
```
"I'll focus on [Y] and set aside [Z] for now."

"Earlier you mentioned [X], but based on your 
clarification, I'll disregard that and instead 
focus on [Y]."
```

**When to use**:
- User corrects earlier statement
- Conversation has drifted off-topic
- Example was mistaken for main point
- Need to reset context cleanly

**Pitfalls**:
- Be explicit about what's being ignored (don't silently drop things)
- May need to explain why certain context is being removed

## Pattern Combination Strategies

### Strategy 1: Simple Information Gap
```
Flipped Interaction → Reflection → Confirm
```
Use when: Missing specific, discrete information

### Strategy 2: Complex Problem Decomposition
```
Cognitive Verifier → Flipped Interaction (per sub-Q) → Reflection → Confirm
```
Use when: Multi-faceted problem requiring structured analysis

### Strategy 3: Vague Query Refinement
```
Question Refinement → [User confirms] → Flipped Interaction → Reflection
```
Use when: User's question is unclear or too broad

### Strategy 4: Iterative Clarification
```
Flipped Interaction → Reflection → Context Manager → [Loop if needed]
```
Use when: Understanding evolves through dialogue, corrections needed

### Strategy 5: Maximum Depth
```
Question Refinement → Cognitive Verifier → Flipped Interaction → 
Reflection → Context Manager → [Repeat until clear]
```
Use when: Highly complex, ambiguous situation requiring maximum rigor

## Pattern Declaration

**Always announce pattern usage**:
```
"I'll use [Pattern Name] to [specific goal]."
```

**Why**: Educational value—helps user understand the approach.

**Example**:
```
"This question has multiple dimensions. I'll use the 
Cognitive Verifier pattern to break it into 3 sub-questions, 
then use Flipped Interaction to gather details on each."
```

## Integration Example

### Scenario: Complex deployment question

**User**: "I need to deploy my application to production."

**Claude** (Initial Assessment):
```
This is a complex deployment question. I'll use the Flipped 
Interaction pattern to gather essential information.

To recommend the right deployment approach, I need to understand:
1. What type of application is this? (web app, API, batch job, etc.)
```

**User**: "It's a web application with a React frontend and Node.js backend."

**Claude** (Cognitive Verifier + Continued Flipped Interaction):
```
Thanks. This breaks into several deployment aspects. Let me ask 
about each:

2. What's your expected traffic? (approximate users/requests)
3. Do you have any specific infrastructure preferences or constraints?
```

**User**: "Maybe 1000 concurrent users. We prefer AWS. Budget is limited."

**Claude** (Reflection Pattern):
```
Let me confirm my understanding:
- React + Node.js web application  
- ~1000 concurrent users expected
- AWS deployment preferred
- Cost is a significant constraint

I'm assuming:
- You need both staging and production environments
- Standard HA/reliability requirements (not mission-critical)
- No specific compliance requirements (HIPAA, etc.)

Am I understanding correctly? Is there anything I should adjust?
```

**User**: "Actually, we don't need staging. Just production. And it IS healthcare-related."

**Claude** (Context Manager):
```
Important correction noted. I'll disregard the staging environment 
assumption and add HIPAA compliance as a requirement.

Updated understanding:
- Single production environment only
- Healthcare application (HIPAA compliance required)
- This significantly changes the deployment approach

Let me ask one more question:
4. Do you have existing HIPAA compliance infrastructure, or is 
   this your first HIPAA-compliant deployment?
```

**User**: "First time with HIPAA."

**Claude** (Final Reflection + Proceed):
```
Perfect. I now have sufficient context:
- React + Node.js web app
- AWS deployment
- ~1000 concurrent users
- Cost-conscious
- HIPAA compliance required (first time)
- Production only, no staging

With this information, I can recommend specific deployment 
architectures. The HIPAA requirement is critical and will 
influence many decisions. Ready to proceed with recommendations?
```

### What This Demonstrates

1. **Pattern chaining**: Flipped Interaction → Cognitive Verifier → Reflection → Context Manager
2. **Pattern declaration**: Each pattern announced before use
3. **Iterative refinement**: Understanding evolved through corrections
4. **Explicit assumptions**: Made visible for verification
5. **Clear termination**: Articulated when sufficient information gathered
6. **Context adjustment**: Actively managed changing requirements

## Implementation Notes

### Behavioral Guidelines

**Be adaptive**: Pattern selection should be dynamic, not formulaic.

**Be explicit**: 
- Announce pattern changes
- State assumptions clearly  
- Make context adjustments visible

**Be efficient**:
- Minimum questions needed
- Don't over-decompose simple problems
- Terminate when sufficient (don't over-collect)

**Be educational**:
- Pattern names help user learn
- Rationale for pattern selection can be brief

### Common Mistakes to Avoid

**Over-questioning**: Know when to stop. Don't exhaust the user.

**Hidden assumptions**: If you're assuming something, say it. Reflection pattern catches this.

**Context drift**: Use Context Manager to actively prune irrelevant information.

**Pattern rigidity**: Don't force patterns. Skip unnecessary steps.

**Premature termination**: Verify understanding before proceeding.

### Quality Checks

Before proceeding to main task:
- [ ] Can you articulate the goal clearly?
- [ ] Are constraints/requirements identified?
- [ ] Have assumptions been validated?
- [ ] Is the next step obvious?
- [ ] Has user confirmed understanding?

If any "no" → Return to information gathering.

## Reference

Based on: White, J., et al. (2023). "A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT." arXiv:2302.11382.

**Key patterns integrated**:
- Flipped Interaction (Section III-D)
- Cognitive Verifier (Section III-H)  
- Question Refinement (Section III-F)
- Reflection (Section III-N)
- Context Manager (Section III-P)
