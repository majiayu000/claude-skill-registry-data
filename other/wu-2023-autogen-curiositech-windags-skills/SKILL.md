---
license: Apache-2.0
name: wu-2023-autogen
description: Framework for building multi-agent conversation systems with customizable LLM-powered agents
category: Research & Academic
tags:
  - multi-agent
  - conversation
  - llm-agents
  - orchestration
  - code-generation
---

# AutoGen Multi-Agent Conversation Design

## When to Use This Skill

Load this skill when facing:
- Coordination complexity where multiple LLMs, tools, or human experts need orchestration
- Rigid control flows using brittle state machines or hard-coded orchestration
- Monolithic agents handling validation, execution, safety, and domain expertise simultaneously
- Human-AI integration requiring smooth transitions between autonomous and collaborative modes
- Tasks needing iterative refinement, debugging, or progressive problem-solving

## DECISION POINTS

**Agent Topology Selection:**
```
IF task has clear sequential stages
├─ THEN use static group chat with predefined speaker order
├─ SET termination condition based on final stage completion
└─ CONFIGURE each agent for specific stage responsibility

IF task complexity varies at runtime
├─ THEN use dynamic speaker selection
├─ IMPLEMENT speaker selection based on message content analysis
└─ ALLOW topology to adapt based on conversation context

IF validation/safety required
├─ THEN add adversarial critic/safeguard agents
├─ POSITION them to intercept before execution
└─ GIVE them veto power in conversation flow

IF human involvement varies
├─ THEN design human agents with configurable backends
├─ SUPPORT autonomous → supervised → collaborative modes
└─ MAINTAIN same conversational interface across modes
```

**Failure Recovery Strategy:**
```
IF one-shot generation fails repeatedly
├─ THEN add executor agent providing error feedback
├─ DESIGN conversation loop: attempt → error → refinement
└─ CAPTURE execution results as conversational messages

IF safety violations occur
├─ THEN implement safeguard agent with conversation veto
├─ POSITION before any execution or external communication
└─ ESCALATE violations as conversation messages requiring resolution

IF coordination breaks down
├─ THEN examine conversation history as execution trace
├─ IDENTIFY where message patterns deviated from expected
└─ ADJUST agent prompts or termination conditions, not orchestration code
```

## FAILURE MODES

**Monolithic Agent Syndrome**
- *Symptom*: Single agent handling execution + validation + safety through complex prompts
- *Detection*: Agent prompts exceed 500 tokens or contain multiple "Also, make sure to..." clauses
- *Fix*: Decompose into specialized agents coordinating through conversation

**Central Orchestrator Trap**
- *Symptom*: Controller code that must understand every agent's internal capabilities
- *Detection*: Orchestration logic contains agent-specific conditionals or capability mapping
- *Fix*: Make agents conversable; let coordination emerge from message-passing patterns

**Human-as-Special-Case**
- *Symptom*: Separate code paths for human vs autonomous operation modes
- *Detection*: If/else branches checking for human participation before different execution flows
- *Fix*: Treat humans as agents with configurable backends using same conversational interface

**Brittle Control Flow**
- *Symptom*: Hard-coded conversation sequences breaking when requirements change
- *Detection*: Speaker order defined in code rather than conversation context or natural language rules
- *Fix*: Use dynamic speaker selection or natural language control flow specifications

**Conversation History Blindness**
- *Symptom*: Agents making decisions without sufficient conversation context
- *Detection*: Repeated questions about information already discussed or contradictory responses
- *Fix*: Configure conversation history visibility based on agent role and responsibility

## WORKED EXAMPLES

**Example 1: Code Generation with Validation**

*Scenario*: Generate Python function with safety validation and execution testing

*Novice Approach*: Single agent with complex prompt handling generation + validation + execution
*Expert Approach*: Three-agent conversation with specialized roles

```
Initial Setup:
- ProgrammerAgent: Generates code based on requirements
- CriticAgent: Reviews code for safety and correctness
- ExecutorAgent: Runs code and reports results

Conversation Flow:
1. Human: "Create a function to process user file uploads"
2. ProgrammerAgent: [Generates initial code with basic file handling]
3. CriticAgent: "Security concern: no input validation for file types or size limits"
4. ProgrammerAgent: [Revises with validation and size checks]
5. ExecutorAgent: "Code executed successfully. Test cases passed. No security violations detected."
6. TERMINATION: All agents confirm completion

Key Decision Points Navigated:
- Critic intercepted unsafe code before execution
- Executor provided concrete feedback enabling iterative refinement  
- Human stayed in loop without separate orchestration logic
```

**Example 2: Dynamic Research Task**

*Scenario*: Multi-step research requiring different expertise levels

*Initial Message*: "Analyze the impact of quantum computing on cryptocurrency security"

*Agent Topology Decision*:
- Complexity varies by subtopic → Use dynamic speaker selection
- Multiple domains required → Deploy specialized expert agents
- Human oversight needed → Include human agent with veto capability

*Conversation Trace*:
```
1. ResearchCoordinator: "Breaking this into quantum algorithms, cryptography, and economic impact"
2. QuantumExpert: [Detailed analysis of Shor's algorithm threat timeline]
3. CryptoExpert: "Post-quantum cryptography migration challenges: [technical details]"
4. EconomicAnalyst: [Market impact assessment]
5. Human: "Focus more on near-term practical implications"
6. ResearchCoordinator: [Adjusts research scope based on human feedback]
7. QuantumExpert: [Provides 5-10 year timeline analysis]
... [conversation continues with dynamic speaker selection based on expertise needs]
```

*What Expert Catches vs Novice Misses*:
- Expert: Recognizes when to shift speakers based on conversation content analysis
- Novice: Would try to pre-plan speaker order or use single "research agent"
- Expert: Sees human feedback as conversational input that naturally redirects agent focus
- Novice: Would implement separate human oversight as orchestration layer

## QUALITY GATES

Task completion requires all conditions verified:

- [ ] Agent specialization: Each agent has single, clear responsibility (no agent handles >2 concerns)
- [ ] Conversation history: All agents receive appropriate conversation context for their role
- [ ] Termination signals: Clear, testable conditions for conversation completion defined
- [ ] Failure recovery: Error cases flow through conversation rather than breaking system
- [ ] Human integration: Human participation uses same interface as AI agents
- [ ] Message coherence: Each conversation turn advances toward task completion
- [ ] Role separation: Computation (agent responses) distinct from control flow (speaker selection)
- [ ] Feedback loops: Validation/correction cycles built into conversation pattern
- [ ] Scalability: Adding new agent capabilities doesn't require orchestration code changes
- [ ] State management: Conversation history serves as complete system state

## NOT-FOR BOUNDARIES

**Use different skills for:**
- Single-agent tasks → Use `llm-prompting` or `tool-integration` skills instead
- Real-time systems requiring <100ms response → AutoGen conversation overhead too high
- Batch processing with no interactive requirements → Use `workflow-orchestration` instead
- Simple API integration → Use `service-integration` patterns instead
- Deterministic algorithms → Use traditional programming rather than conversation-based coordination

**Delegate when:**
- Task requires guaranteed deterministic outcomes → Use rule-based systems
- Conversation history would exceed token limits → Use `memory-management` skill for optimization
- Integration with existing workflow engines → Use `system-integration` skill for adapter patterns
- Performance optimization needed → Use `distributed-systems` skill for efficient coordination protocols