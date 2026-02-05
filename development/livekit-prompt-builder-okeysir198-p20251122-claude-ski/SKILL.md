---
name: livekit-prompt-builder
description: Guide for creating effective prompts and instructions for LiveKit voice agents. Use when building conversational AI agents with the LiveKit Agents framework, including (1) Creating new voice agent prompts from scratch, (2) Improving existing agent instructions, (3) Optimizing prompts for text-to-speech output, (4) Integrating tool/function calling capabilities, (5) Building multi-agent systems with handoffs, (6) Ensuring voice-friendly formatting and brevity for natural conversations, (7) Iteratively improving prompts based on testing and feedback, (8) Building industry-specific agents (debt collection, healthcare, banking, customer service, front desk).
---

# LiveKit Voice Agent Prompt Builder

Create production-ready prompts for LiveKit voice agents that work seamlessly with text-to-speech systems.

## Quick Start

For most use cases, follow this simple workflow:

1. **Choose a template** from `assets/templates/` that matches your use case
2. **Customize** the template with your specific information
3. **Validate** using `scripts/validate_prompt.py`
4. **Test** with your LiveKit agent
5. **Refine** based on real conversations

## Workflow

### Step 1: Determine Your Agent Type

Select the template that best matches your needs:

**General Purpose:**

- **Basic Assistant** (`basic-assistant.txt`) - Simple conversational agent
  - Use for: General chat, demos, minimal functionality
  - Complexity: Low
  - Tools: Optional

- **Tool-Enabled Agent** (`tool-enabled-agent.txt`) - Agent with function calling
  - Use for: Weather, search, data lookup, single-domain assistants
  - Complexity: Medium
  - Tools: 1-5 tools

- **Customer Service** (`customer-service.txt`) - Support agent with escalation
  - Use for: Help desks, support lines, troubleshooting
  - Complexity: Medium
  - Tools: Lookup, search, escalation

- **Specialist Agent** (`specialist-agent.txt`) - Task-specific agent (reservations, orders, etc.)
  - Use for: Booking systems, order taking, appointments
  - Complexity: Medium-High
  - Tools: Action tools (create, update)

- **Multi-Agent Coordinator** (`multi-agent-coordinator.txt`) - Routes to other agents
  - Use for: Main entry point in multi-agent systems
  - Complexity: Medium
  - Tools: Transfer/handoff tools

**Industry-Specific:**

- **Front Desk Receptionist** (`front-desk-receptionist.txt`) - Professional call routing
  - Use for: Office reception, call centers, front desk operations
  - Complexity: Low-Medium
  - Tools: Transfer, routing, message taking

- **Debt Collection** (`debt-collection-agent.txt`) - Compliant recovery agent
  - Use for: Debt recovery, collections, payment arrangements
  - Complexity: High
  - Tools: Payment processing, sentiment analysis
  - Note: Includes FDCPA/TCPA/CFPB compliance requirements

### Step 2: Customize Your Template

Open your selected template and fill in the placeholders:

**Example - Customizing `basic-assistant.txt`:**

Template:
```
You are [NAME], a friendly voice assistant. You are [TRAIT_1] and [TRAIT_2], with [TRAIT_3].
```

Customized:
```
You are Casey, a friendly voice assistant. You are helpful and patient, with a sense of humor.
```

**Key customization areas:**
- Identity (name, role, personality)
- Domain context (business info, hours, policies)
- Tool descriptions (when and how to use each tool)
- Workflow steps (information collection sequence)
- Boundaries (what agent can't do)

### Step 3: Apply Voice Optimization

Ensure your prompt includes these critical voice optimization rules:

**Required elements:**

```
Keep your responses brief - 1-3 sentences. Respond in plain text only - no emojis, asterisks, markdown, or special formatting. Ask one question at a time.
```

**For agents that mention numbers, prices, or contact info:**

```
Spell out numbers ("fifteen" not "15"). Spell phone numbers digit by digit ("5-5-5, 1-2-3-4"). For URLs, omit "https://" and say "dot" for periods.
```

**For agents with tools:**

```
If a tool call fails, explain the issue simply and suggest a fallback. Summarize tool results in conversational language - don't recite technical IDs or raw data.
```

### Step 4: Validate Your Prompt

Run the validation script to check for common issues:

```bash
python scripts/validate_prompt.py your_prompt.txt
```

The validator checks for:
- Missing identity statement
- Lack of voice optimization rules
- TTS antipatterns (emojis, markdown, special characters)
- Excessive length (>500 words)
- Missing tool error handling
- Number formatting guidance

**Fix any errors** before deploying your prompt.

### Step 5: Test with LiveKit

Deploy your prompt in a LiveKit agent and test with real conversations:

**Test scenarios:**
1. **Happy path** - User provides information smoothly
2. **Interruptions** - User changes topic or interrupts
3. **Tool failures** - Simulate tool errors
4. **Edge cases** - Ambiguous requests, out-of-scope questions
5. **Voice quality** - Listen to TTS output for formatting issues

### Step 6: Refine

Based on testing, refine your prompt:

**Common refinements:**
- Add specific guidance for observed failure modes
- Adjust tone or personality descriptors
- Add examples for complex tool usage
- Tighten response length constraints if agent is too verbose
- Add boundaries for out-of-scope requests

## Key Concepts

### Voice-First Design

Voice agents differ from text chatbots:

**Critical differences:**
- No visual formatting (users can't see bold, lists, etc.)
- Limited user patience (long responses cause frustration)
- TTS limitations (special characters cause problems)
- No "scroll back" (users can't review previous responses)

**Implications for prompts:**
- Always specify plain text only
- Enforce brevity (1-3 sentences typical)
- Spell out numbers and abbreviations
- Ask one question at a time
- Avoid complex structures (lists, tables)

### The Three Essential Sections

Every voice agent prompt should have:

1. **Identity** - "You are [name/role]. You are [personality]."
2. **Voice Rules** - Plain text, brief responses, number formatting
3. **Core Functionality** - What the agent does, tools it uses, workflows it follows

Additional sections (domain context, guardrails, handoffs) add as needed.

### Template vs. Custom Prompts

**Use templates when:**
- Starting a new agent
- Following common patterns (support, booking, etc.)
- Want quick setup with best practices

**Write custom when:**
- Unique use case not covered by templates
- Very specialized domain
- Complex multi-step workflows

Even with custom prompts, reference the templates for voice optimization patterns.

## Progressive Disclosure: When to Load References

Load reference documentation based on your specific needs:

**For all users:**
- Start with templates and this SKILL.md

**Load prompt-components.md when:**
- Building complex prompts from scratch
- Need detailed guidance on specific sections
- Want to understand the "why" behind best practices
- Customizing beyond simple template fill-in

**Load voice-optimization.md when:**
- Encountering TTS formatting issues
- Agent responses sound awkward or unnatural
- Need deep understanding of voice-specific constraints
- Working with multiple TTS providers
- Debugging number, URL, or email pronunciation

**Load tool-integration.md when:**
- Integrating function calling/tools
- Building multi-agent systems with handoffs
- Need patterns for error handling or parameter collection
- Tools aren't being used correctly
- Working with RAG or external data sources

**Load examples.md when:**
- Want to see complete, real-world prompts
- Need inspiration for similar use cases
- Comparing complexity levels
- Learning from production patterns

**Load industry-best-practices.md when:**
- Building agents for regulated industries (healthcare, banking, debt collection)
- Need compliance guidance (HIPAA, FDCPA, TCPA, etc.)
- Working on industry-specific use cases (front desk, customer service, sales)
- Require specialized tone and approach patterns
- Need security or privacy considerations

**Load iterative-improvement.md when:**
- Improving existing prompts based on feedback
- Analyzing test results and conversation data
- Conducting A/B tests on prompt variations
- Establishing metrics and measurement frameworks
- Need systematic approach to prompt refinement
- Want to preserve prompt structure while making improvements

**Strategy:** Start minimal (templates + SKILL.md). Load references only when you hit specific challenges or need deeper guidance.

## Multi-Agent Systems

For systems with multiple agents, design each agent separately:

**Pattern:**

1. **Coordinator/Greeter** - Uses `multi-agent-coordinator.txt`
   - Simple routing logic
   - Minimal conversation
   - Quick transfers

2. **Specialist Agents** - Use `specialist-agent.txt`
   - Each handles one specific task
   - Collects required information
   - Takes action or transfers to next agent

**Key considerations:**
- Each agent should have a single, clear responsibility
- Define handoff criteria explicitly
- Decide what context to pass between agents (full chat history vs structured data)
- Test agent transitions for smoothness

## Common Patterns

### Pattern 1: Simple Conversational Agent

**Template:** `basic-assistant.txt`

**Use for:** Chat, demos, general assistance

**Prompt structure:**
- Identity + personality
- Voice optimization rules
- Optional: specific topics or capabilities

**Example use cases:**
- Demo voice assistant
- Companion chatbot
- General information assistant

### Pattern 2: Information Retrieval Agent

**Template:** `tool-enabled-agent.txt`

**Use for:** Looking up data, answering questions from external sources

**Prompt structure:**
- Identity + domain
- Voice optimization
- Tool descriptions (when to use each tool)
- Result summarization guidance

**Example use cases:**
- Weather agent
- Product lookup
- Knowledge base search
- RAG-enabled assistants

### Pattern 3: Action-Taking Agent

**Template:** `specialist-agent.txt`

**Use for:** Booking, ordering, scheduling, transactions

**Prompt structure:**
- Identity + role
- Voice optimization
- Information collection sequence
- Confirmation before action
- Tool usage for state changes

**Example use cases:**
- Reservation agent
- Order taking
- Appointment scheduling
- Registration

### Pattern 4: Support Agent with Escalation

**Template:** `customer-service.txt`

**Use for:** Help desk, customer support, troubleshooting

**Prompt structure:**
- Identity + tone (empathetic, patient)
- Voice optimization
- Capabilities and tools
- Clear escalation criteria
- Error handling and fallbacks

**Example use cases:**
- Customer support
- Technical troubleshooting
- Account assistance
- Order status lookup

## Troubleshooting

### Issue: Agent uses markdown or special formatting

**Symptoms:** TTS says "asterisk asterisk hello" or skips characters

**Solution:** Ensure prompt includes:
```
Respond in plain text only - no emojis, asterisks, markdown, or special formatting.
```

**Prevention:** Run validation script

### Issue: Responses too long

**Symptoms:** Users interrupt frequently, seem impatient

**Solution:** Add stricter constraints:
```
Keep responses very brief - 1-2 sentences maximum. Ask one question at a time.
```

**Prevention:** Test with real users early

### Issue: Numbers sound awkward

**Symptoms:** "Dollar sign forty-nine point nine nine" or unclear prices/phone numbers

**Solution:** Add number formatting rules:
```
Spell out numbers ("forty-nine ninety-nine" for prices). Spell phone numbers digit by digit ("5-5-5, 1-2-3-4").
```

### Issue: Agent doesn't use tools correctly

**Symptoms:** Tools called at wrong time, missing parameters, no error handling

**Solution:**
1. Add explicit tool usage instructions in prompt
2. Specify when to use each tool
3. Define parameter collection flow
4. Add error handling guidance

**Check:** Load `tool-integration.md` for detailed patterns

### Issue: Agent goes off-topic or out-of-scope

**Symptoms:** Agent tries to handle requests beyond capabilities

**Solution:** Add boundaries and guardrails:
```
You can only help with [specific domain]. For questions about [out-of-scope topics], direct users to [alternative resource].
```

### Issue: Multi-agent transfers feel awkward

**Symptoms:** Abrupt handoffs, lost context, repeated questions

**Solution:**
1. Add transition messages before transfer
2. Define what context passes between agents
3. Ensure previous agent collects minimum required info

**Check:** See multi-agent examples in `examples.md`

## Advanced Topics

### Emotional Expression

For agents that should convey emotion, use descriptive language:

**Good:**
```
When users share good news, respond warmly and enthusiastically. When they express frustration, respond with empathy and patience.
```

**Avoid:** Trying to use emojis, asterisks, or formatting to convey emotion.

**Trust TTS:** Modern TTS systems convey emotion through intonation based on word choice.

### Multiple TTS Providers

Different TTS providers have different characteristics:

- **OpenAI TTS** - Natural, handles most punctuation well
- **Cartesia Sonic** - Fast, low-latency, clear pronunciation
- **Deepgram** - Strong with accents and dialects
- **ElevenLabs** - Highly expressive, personality-driven

**Universal best practices work across all providers:**
1. Plain text only
2. Brief responses
3. Spell out numbers
4. Avoid special characters

Test your specific provider to identify any quirks.

### Handling Sensitive Contexts

For healthcare, finance, or other regulated industries:

**Add explicit constraints:**
```
Never:
- Share customer information without verification
- Provide medical/legal/financial advice
- Process transactions without explicit confirmation
```

**Be security-conscious:**
```
For security, you'll need to verify identity before providing account information.
```

**Escalate appropriately:**
```
For [sensitive issue], immediately transfer to [appropriate specialist].
```

See healthcare and banking examples in `examples.md`.

## Best Practices Summary

1. **Start with templates** - They encode best practices
2. **Keep prompts concise** - Under 300 words when possible
3. **Always include voice rules** - Plain text, brevity, number formatting
4. **Test with real TTS** - Listen to actual output
5. **Validate before deploying** - Use the validation script
6. **One responsibility per agent** - In multi-agent systems
7. **Iterate based on real usage** - Refine after testing
8. **Error handling is critical** - Always include fallback guidance
9. **Confirm before actions** - Especially for state changes
10. **Boundaries prevent confusion** - Clearly define scope

## Resources

**Templates:**

General Purpose:
- `assets/templates/basic-assistant.txt` - Simple conversational agent
- `assets/templates/tool-enabled-agent.txt` - Agent with function calling
- `assets/templates/customer-service.txt` - Support with escalation
- `assets/templates/specialist-agent.txt` - Task-specific workflows
- `assets/templates/multi-agent-coordinator.txt` - Router/greeter agent

Industry-Specific:
- `assets/templates/front-desk-receptionist.txt` - Professional call routing and reception
- `assets/templates/debt-collection-agent.txt` - Compliant debt recovery (FDCPA/TCPA)

**Reference Documentation:**
- `references/prompt-components.md` - Detailed component guide
- `references/voice-optimization.md` - TTS formatting deep dive
- `references/tool-integration.md` - Function calling patterns
- `references/examples.md` - Complete real-world prompts
- `references/industry-best-practices.md` - Industry-specific patterns and compliance
- `references/iterative-improvement.md` - Systematic prompt refinement and testing

**Tools:**
- `scripts/validate_prompt.py` - Validation script

**External Resources:**
- LiveKit Agents Documentation: https://docs.livekit.io/agents/
- LiveKit Prompting Guide: https://docs.livekit.io/agents/build/prompting/
- LiveKit Examples: https://github.com/livekit/agents/tree/main/examples

## Example: Complete Workflow

**Scenario:** Build a pizza ordering agent

**Step 1:** Choose template
- Task-specific with order taking → `specialist-agent.txt`

**Step 2:** Customize
```
You are Marco, an order specialist at Mario's Pizza. You are friendly, efficient, and helpful.

Keep responses very brief - 1-2 sentences. Plain text only, no formatting. Ask one question at a time.

Our menu:
- Margherita: twelve dollars
- Pepperoni: fourteen dollars
- Veggie Supreme: fifteen dollars

Collect in order:
1. Pizza selection - "What pizza would you like?"
2. Size - "What size: small, medium, or large?"
3. Any modifications - "Any special requests or modifications?"
4. Name - "Name for the order?"
5. Phone - "Phone number?"

Confirm: "Let me confirm: [size] [pizza] for [name] at [phone]. Total is [price]. Is that correct?"

Use create_order(pizza, size, modifications, name, phone) after confirmation.

Spell out prices: "fourteen dollars" not "dollar sign fourteen".
Spell phone numbers: "5-5-5, 1-2-3-4".
```

**Step 3:** Validate
```bash
python scripts/validate_prompt.py pizza_prompt.txt
```

**Step 4:** Deploy and test with LiveKit

**Step 5:** Refine based on feedback
- If users often ask about delivery time → Add delivery info to domain context
- If tool fails occasionally → Add error handling for out-of-stock items
- If users interrupt with questions → Add guidance for handling interruptions

## Iterative Improvement

Voice agent prompts improve through continuous refinement based on real-world usage:

### Quick Improvement Workflow

1. **Collect feedback** - Gather test results, user feedback, conversation metrics
2. **Identify patterns** - Look for common issues across multiple conversations
3. **Make targeted changes** - Modify specific sections while preserving structure
4. **Test changes** - Validate improvements with test scenarios
5. **Measure impact** - Compare before/after metrics
6. **Iterate** - Repeat the cycle

### Key Principles

- **Structure preservation** - Make minimal, targeted changes to address specific issues
- **Data-driven** - Use evidence from tests and conversations, not guesses
- **Version control** - Track changes and document reasons
- **A/B testing** - When possible, run old and new versions in parallel
- **Regression testing** - Ensure changes don't break existing functionality

**For detailed guidance:** See `references/iterative-improvement.md`

---

## Industry-Specific Guidance

Different industries require specialized approaches:

**Debt Collection:**
- Empathetic but professional tone
- FDCPA/TCPA/CFPB compliance built-in
- Sentiment-aware escalation
- Payment arrangement workflows

**Healthcare:**
- HIPAA compliance and privacy protection
- Emergency detection and routing
- Professional, caring tone
- Limited scope (no medical advice)

**Banking/Financial:**
- Security-first verification
- Fraud detection awareness
- Regulatory compliance
- Transaction limitations

**Customer Service:**
- Empathetic problem-solving
- Clear escalation criteria
- Knowledge base integration
- Omnichannel awareness

**Front Desk/Reception:**
- Professional greeting frameworks
- Efficient call routing
- Message taking protocols
- After-hours handling

**For detailed patterns:** See `references/industry-best-practices.md`

---

## Getting Started Now

1. **Pick the closest template** for your use case
2. **Copy it** and fill in your information
3. **Run the validator** to catch common issues
4. **Test it** in your LiveKit agent
5. **Collect feedback** and iterate based on real usage
6. **Come back to this skill** when you need to refine or troubleshoot

The templates handle 80% of the work. Focus your customization on domain-specific information, tools, and workflows. Then continuously improve based on real-world performance.
