---
name: structured-outputs-advisor
version: 0.2.1
description: Use PROACTIVELY when users need guaranteed schema compliance or validated tool inputs from Anthropic's structured outputs feature. Expert advisor for choosing between JSON outputs (data extraction/formatting) and strict tool use (agentic workflows). Analyzes requirements, explains trade-offs, and delegates to specialized implementation skills. Not for simple text responses or unstructured outputs.
---

# Structured Outputs Advisor

## Overview

This skill serves as the entry point for implementing Anthropic's structured outputs feature. It helps developers choose between **JSON outputs** (for data extraction/formatting) and **strict tool use** (for agentic workflows), then delegates to specialized implementation skills. The advisor ensures developers select the right mode based on their use case and requirements.

**Two Modes Available:**
1. **JSON Outputs** (`output_format`) - Guaranteed JSON schema compliance for responses
2. **Strict Tool Use** (`strict: true`) - Validated tool parameters for function calls

**Specialized Implementation Skills:**
- `json-outputs-implementer` - For data extraction, classification, API formatting
- `strict-tool-implementer` - For agentic workflows, validated function calls

## When to Use This Skill

**Trigger Phrases:**
- "implement structured outputs"
- "need guaranteed JSON schema"
- "extract structured data from [source]"
- "validate tool inputs"
- "build reliable agentic workflow"
- "ensure type-safe responses"
- "help me with structured outputs"

**Use Cases:**
- Data extraction from text/images
- Classification with guaranteed output format
- API response formatting
- Agentic workflows with validated tools
- Type-safe database operations
- Complex tool parameter validation

## Response Style

- **Consultative**: Ask questions to understand requirements
- **Educational**: Explain both modes and when to use each
- **Decisive**: Recommend the right mode based on use case
- **Delegating**: Hand off to specialized skills for implementation
- **Concise**: Keep mode selection phase quick (<5 questions)

## Core Workflow

### Phase 1: Understand Requirements

**Questions to Ask:**

1. **What's your goal?**
   - "What kind of output do you need Claude to produce?"
   - Examples: Extract invoice data, validate function parameters, classify tickets

2. **What's the data source?**
   - Text, images, API calls, user input, etc.

3. **What consumes the output?**
   - Database, API endpoint, function call, agent workflow, etc.

4. **How critical is schema compliance?**
   - Must be guaranteed vs. generally reliable

### Phase 2: Mode Selection

**Use JSON Outputs (`output_format`) when:**
- ✅ You need Claude's **response** in a specific format
- ✅ Extracting structured data from unstructured sources
- ✅ Generating reports, classifications, or API responses
- ✅ Formatting output for downstream processing
- ✅ Single-step operations

**Examples:**
- Extract contact info from emails → CRM database
- Classify support tickets → routing system
- Generate structured reports → API endpoint
- Parse invoices → accounting software

**Use Strict Tool Use (`strict: true`) when:**
- ✅ You need validated **tool input parameters**
- ✅ Building multi-step agentic workflows
- ✅ Ensuring type-safe function calls
- ✅ Complex tools with many/nested properties
- ✅ Critical operations requiring guaranteed types

**Examples:**
- Travel booking agent (flights + hotels + activities)
- Database operations with strict type requirements
- API orchestration with validated parameters
- Complex workflow automation

### Phase 3: Delegation

**After determining the mode, delegate to the specialized skill:**

**For JSON Outputs:**
```
I recommend using JSON outputs for your [use case].

I'm going to invoke the json-outputs-implementer skill to help you:
1. Design a production-ready JSON schema
2. Implement with SDK helpers (Pydantic/Zod)
3. Add validation and error handling
4. Optimize for production

[Launch json-outputs-implementer skill]
```

**For Strict Tool Use:**
```
I recommend using strict tool use for your [use case].

I'm going to invoke the strict-tool-implementer skill to help you:
1. Design validated tool schemas
2. Implement strict mode correctly
3. Build reliable agent workflows
4. Test and validate tool calls

[Launch strict-tool-implementer skill]
```

**For Both Modes (Hybrid):**
```
Your use case requires both modes:
- JSON outputs for [specific use case]
- Strict tool use for [specific use case]

I'll help you implement both, starting with [primary mode].

[Launch appropriate skill first, then the second one]
```

## Decision Matrix

| Requirement | JSON Outputs | Strict Tool Use |
|-------------|--------------|-----------------|
| Extract structured data | ✅ Primary use case | ❌ Not designed for this |
| Validate function parameters | ❌ Not designed for this | ✅ Primary use case |
| Multi-step agent workflows | ⚠️ Possible but not ideal | ✅ Designed for this |
| API response formatting | ✅ Ideal | ❌ Unnecessary |
| Database inserts (type safety) | ✅ Good fit | ⚠️ If via tool calls |
| Complex nested schemas | ✅ Supports this | ✅ Supports this |
| Classification tasks | ✅ Perfect fit | ❌ Overkill |
| Tool composition/chaining | ❌ Not applicable | ✅ Excellent |

## Feature Availability

**Models Supported:**
- ✅ Claude Sonnet 4.5 (`claude-sonnet-4-5`)
- ✅ Claude Opus 4.1 (`claude-opus-4-1`)

**Beta Header Required:**
```
anthropic-beta: structured-outputs-2025-11-13
```

**Incompatible Features:**
- ❌ Citations (with JSON outputs)
- ❌ Message Prefilling (with JSON outputs)

**Compatible Features:**
- ✅ Batch Processing (50% discount)
- ✅ Token Counting
- ✅ Streaming
- ✅ Both modes together in same request

## Common Scenarios

### Scenario 1: "I need to extract invoice data"
**Analysis**: Data extraction from unstructured text
**Mode**: JSON Outputs
**Delegation**: `json-outputs-implementer`
**Reason**: Single-step extraction with structured output format

### Scenario 2: "Building a travel booking agent"
**Analysis**: Multi-tool workflow (flights, hotels, activities)
**Mode**: Strict Tool Use
**Delegation**: `strict-tool-implementer`
**Reason**: Multiple validated tools in agent workflow

### Scenario 3: "Classify customer support tickets"
**Analysis**: Classification with guaranteed categories
**Mode**: JSON Outputs
**Delegation**: `json-outputs-implementer`
**Reason**: Single classification result, structured response

### Scenario 4: "Validate database insert parameters"
**Analysis**: Type-safe database operations
**Mode**: JSON Outputs (if direct) OR Strict Tool Use (if via tool)
**Delegation**: Depends on architecture
**Reason**: Both work - choose based on system architecture

### Scenario 5: "Generate API-ready responses"
**Analysis**: Format responses for API consumption
**Mode**: JSON Outputs
**Delegation**: `json-outputs-implementer`
**Reason**: Output formatting is primary goal

## Quick Start Examples

### JSON Outputs Example
```python
# Extract contact information
from pydantic import BaseModel
from anthropic import Anthropic

class Contact(BaseModel):
    name: str
    email: str
    plan: str

client = Anthropic()
response = client.beta.messages.parse(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": "Extract contact info..."}],
    output_format=Contact,
)
contact = response.parsed_output  # Guaranteed schema match
```

### Strict Tool Use Example
```python
# Validated tool for agent workflow
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["structured-outputs-2025-11-13"],
    messages=[{"role": "user", "content": "Book a flight..."}],
    tools=[{
        "name": "book_flight",
        "strict": True,  # Guarantees schema compliance
        "input_schema": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "passengers": {"type": "integer"}
            },
            "required": ["destination"],
            "additionalProperties": False
        }
    }]
)
# Tool inputs guaranteed to match schema
```

## Success Criteria

- [ ] Requirements clearly understood
- [ ] Data source identified
- [ ] Output consumer identified
- [ ] Correct mode selected (JSON outputs vs strict tool use)
- [ ] Reasoning for mode selection explained
- [ ] Appropriate specialized skill invoked
- [ ] User understands next steps

## Important Reminders

1. **Ask before assuming** - Don't guess the mode, understand requirements first
2. **One mode is usually enough** - Most use cases need only one mode
3. **Delegate quickly** - Keep advisor phase short, let specialists handle implementation
4. **Both modes work together** - Can use both in same request if needed
5. **Model availability** - Confirm Sonnet 4.5 or Opus 4.1 is available
6. **Beta feature** - Requires beta header in API requests

## Next Steps After Mode Selection

Once mode is selected and you've delegated to the specialized skill, that skill will handle:
- ✅ Schema design (respecting JSON Schema limitations)
- ✅ SDK integration (Pydantic/Zod helpers)
- ✅ Implementation with error handling
- ✅ Testing and validation
- ✅ Production optimization
- ✅ Complete examples and documentation

---

**Official Documentation**: https://docs.anthropic.com/en/docs/build-with-claude/structured-outputs

**Related Skills**:
- `json-outputs-implementer` - Implement JSON outputs mode
- `strict-tool-implementer` - Implement strict tool use mode
