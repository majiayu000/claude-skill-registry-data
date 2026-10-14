---
name: break-repetitive-patterns
description: Detects when user is asking repetitive questions and helps break out of trained logic patterns by triggering proactive research and alternative approaches.
---
# Break Repetitive Patterns Skill

This skill helps identify when conversations are becoming repetitive and provides strategies to break out of trained logic loops by initiating proactive research and exploring alternative perspectives.

## Core Purpose

When users find themselves asking similar questions repeatedly and the assistant seems stuck on familiar response patterns, this skill activates to:
1. Detect repetitive questioning patterns
2. Trigger proactive research instead of relying on trained responses
3. Suggest alternative approaches and perspectives
4. Help reframe the problem to uncover new insights

## Detection Triggers

The skill should be considered when:
- User asks the same or substantially similar question 2+ times
- User expresses frustration with repetitive answers
- Assistant notices it's providing similar responses despite different phrasing
- Conversation feels like it's going in circles without progress

## Proactive Response Strategies

When activated, instead of relying solely on trained responses:

### 1. Initiate External Research
**DO:**
- Use web search for current information beyond training cutoff
- Consult documentation sources for latest updates
- Search for recent developments, alternatives, or contrasting viewpoints
- Look for community discussions or forums on the topic

**DON'T:**
- Rely solely on internal knowledge when user indicates dissatisfaction
- Assume the answer hasn't changed since training cutoff
- Repeat the same explanation with different wording

### 2. Apply Alternative Reasoning Frameworks
**DO:**
- Approach the problem from different angles (beginner vs expert perspective)
- Consider opposing viewpoints or contrarian arguments
- Use analogy from different domains
- Break down assumptions and question their validity

**DON'T:**
- Defend the initial position without considering alternatives
- Assume there's only one correct approach
- Dismiss user's intuition that something is being missed

### 3. Use Structured Exploration Techniques
**DO:**
- Employ the "5 Whys" technique to get to root causes
- Create pros/cons lists for different approaches
- Develop decision matrices for complex choices
- Use lateral thinking techniques (random word association, reversal, etc.)

**DON'T:**
- Stick to linear, logical progression only
- Avoid uncomfortable or counterintuitive ideas
- Rush to closure before exploring adequately

## Implementation Guidelines

### When User Signals Repetition:
1. **Acknowledge the pattern**: "I notice we may be going in circles..."
2. **Invite clarification**: "Could you help me understand what specific aspect you'd like me to explore differently?"
3. **Commit to research**: "Let me look into current approaches beyond my training..."
4. **Follow through**: Actually perform research before responding

### Conversation Reset Techniques:
- Ask: "What would make this conversation feel productive right now?"
- Suggest: "Let's try approaching this from a completely different angle..."
- Propose: "What if we assumed the opposite of what we've been discussing?"
- Recommend: "Shall I research what experts are saying about this today?"

## Special Considerations

### Technical Topics:
- Check for recent framework/library updates
- Look for breaking changes or deprecations
- Search for alternative libraries or approaches
- Consider if the problem might be better solved differently

### Conceptual/Strategic Topics:
- Seek diverse viewpoints from different schools of thought
- Look for case studies or real-world examples
- Consider historical context and evolution of ideas
- Explore how similar problems are solved in other industries

### Personal/Subjective Topics:
- Acknowledge limitations in understanding personal context
- Suggest consulting with human experts or peers
- Recommend reflective exercises or journaling
- Consider if the question masks a different underlying concern

## Usage Instructions

This skill can be invoked in several ways:

1. **Automatic activation**: When conversation patterns suggest repetition
2. **Manual invocation**: Use `/break-repetitive-patterns` to request a fresh approach
3. **With parameters**: `/break-repetitive-patterns [specific aspect to explore]`

### Example Invocations:
- `/break-repetitive-patterns` - Request general fresh approach
- `/break-repetitive-patterns alternatives` - Specifically request alternative solutions
- `/break-repetitive-patterns research` - Request current research on topic
- `/break-repetitive-patterns perspective` - Request different viewpoint

## Reset Protocol

When this skill is activated:
1. Acknowledge potential repetition without defensiveness
2. Ask clarifying questions to understand the true intent
3. Commit to concrete action (research, alternative approach, etc.)
4. Follow through before providing substantive response
5. Check in with user to see if the approach feels more productive

## Maintenance

This skill works best when:
- Users feel safe calling out repetitive patterns
- The assistant responds gratefully to feedback about repetition
- Both parties commit to breaking unproductive cycles
- Focus remains on making progress rather than being "right"

---

*This skill embodies the principle that sometimes the best way forward is to step back and approach the problem with fresh eyes and current information.*

## Bundled Script

Copy `detect-repetition.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/break-repetitive-patterns/scripts/detect-repetition.ps1 .ai_scripts/
```

Finds repeated normalized patterns in a session log — useful for detecting fixation loops:

```powershell
.ai_scripts\detect-repetition.ps1 -LogFile session.log
```

## Cross-references

- **anti-sycophancy** — Both address repetitive loops. break-repetitive-patterns handles user-side patterns; anti-sycophancy handles model-side agreement loops.

- **requirements-clarify** — When user asks repetitive questions, they may need requirements clarification instead.
- **skill-loader** — Apply the capped selection policy when deciding whether anti-sycophancy or requirements-clarify should also be active to break repetitive loops.
