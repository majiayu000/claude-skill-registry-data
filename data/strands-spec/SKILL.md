---
name: strands-spec
description: "Expert guidance for creating strands-cli workflow specifications (YAML/JSON). Use when creating, modifying, or troubleshooting strands-cli specs for: (1) Multi-step agent workflows (chain, routing, parallel, graph patterns), (2) Tool configuration (python_exec, http_request, custom tools), (3) Runtime and provider setup (Bedrock, OpenAI, Ollama), (4) Input/output handling and templating, or (5) Debugging validation errors"
---

# Strands Workflow Spec Creation Skill

Expert guidance for building production-ready strands-cli workflow specifications.

## Core Principles

1. **Declarative Over Imperative**: Define *what* the workflow should do, not *how* to execute it
2. **Schema-First**: All specs validate against `strands-workflow.schema.json` (JSON Schema Draft 2020-12)
3. **Progressive Loading**: Start simple, add complexity only when needed
4. **Safe by Default**: Always include budgets, retries, and validation

## When to Use This Skill

Load this skill when you need to:
- Create a new strands-cli workflow from scratch
- Add new patterns (chain, parallel, routing, etc.) to existing specs
- Configure tools, runtime providers, or telemetry
- Debug schema validation errors
- Optimize workflow performance or token usage

## Quick Start Template

```yaml
version: 0
name: "my-workflow"
description: "Brief description of what this workflow does"

runtime:
  provider: bedrock  # or openai, ollama
  model_id: "anthropic.claude-3-sonnet-20240229-v1:0"
  region: "us-east-1"
  budgets:
    max_tokens: 100000
    max_duration_s: 300

agents:
  main-agent:
    prompt: "Your clear, specific instructions here"

pattern:
  type: chain  # Start with chain, evolve to other patterns
  config:
    steps:
      - agent: main-agent
        input: "Task description"

outputs:
  artifacts:
    - path: "./output.txt"
      from: "{{ last_response }}"
```

## Progressive Loading Strategy

**DO NOT load all reference files at once.** Instead:

1. **Start here** for basic workflow structure and patterns
2. **Load `patterns.md`** when working with specific orchestration patterns (chain, routing, parallel, etc.)
3. **Load `tools.md`** when configuring custom tools or troubleshooting tool execution
4. **Load `advanced.md`** for context management, telemetry, security features
5. **Load `examples.md`** for real-world workflow patterns and templates
6. **Load `troubleshooting.md`** when debugging validation errors or runtime issues

## Essential Workflow Elements

### 1. Runtime Configuration

```yaml
runtime:
  provider: bedrock          # REQUIRED: bedrock | openai | ollama
  model_id: "..."            # Model identifier (provider-specific)
  region: "us-east-1"        # Required for Bedrock
  temperature: 0.7           # 0.0-2.0 (default: 0.7)
  max_tokens: 2000           # Per-message limit
  budgets:                   # Prevent runaway costs
    max_tokens: 100000       # Total token budget
    max_duration_s: 600      # Timeout in seconds
    max_steps: 50            # Max agent invocations
```

**Provider Quick Reference:**
- **Bedrock**: Requires `region`, uses AWS credentials (fully supported)
- **OpenAI**: Requires `OPENAI_API_KEY` env var (fully supported)
- **Ollama**: Requires `host: "http://localhost:11434"` (fully supported)

### 2. Agent Definition

```yaml
agents:
  agent-name:
    prompt: |
      Clear, specific instructions.
      Use {{ variables }} for dynamic content.
    tools: ["python_exec", "http_request"]  # Optional
    runtime:                                 # Optional overrides
      temperature: 0.3
      max_tokens: 4000
```

**Prompt Best Practices:**
- Be specific about expected output format
- Include examples when format is complex
- Reference template variables with `{{ var_name }}`
- Keep prompts focused on single responsibility

### 3. Pattern Selection

Choose based on your coordination needs:

| Pattern | Use Case | Complexity |
|---------|----------|------------|
| `chain` | Sequential steps, each builds on previous | ⭐ Simple |
| `routing` | Dynamic agent selection based on input | ⭐⭐ Medium |
| `parallel` | Independent tasks executed concurrently | ⭐⭐ Medium |
| `workflow` | DAG with dependencies, parallel where possible | ⭐⭐⭐ Complex |
| `graph` | State machines with loops and conditionals | ⭐⭐⭐⭐ Advanced |
| `evaluator-optimizer` | Iterative refinement with quality gates | ⭐⭐⭐ Complex |
| `orchestrator-workers` | Dynamic task delegation | ⭐⭐⭐⭐ Advanced |

**All 7 patterns are fully implemented and production-ready.** Start with `chain`, migrate to complex patterns only when needed.

### 4. Inputs and Variables

```yaml
inputs:
  required:
    topic: string                # Shorthand syntax
  optional:
    format:
      type: string
      description: "Output format"
      default: "markdown"
      enum: ["markdown", "json", "yaml"]
```

Use variables in prompts and artifacts:
```yaml
prompt: "Research {{ topic }} and output as {{ format }}"
```

### 5. Outputs

```yaml
outputs:
  artifacts:
    - path: "./artifacts/result.md"
      from: "{{ last_response }}"           # Last agent output
    - path: "./artifacts/trace.json"
      from: "{{ $TRACE }}"                  # Full execution trace
```

**Template Variables:**
- `{{ last_response }}` - Most recent agent output
- `{{ steps[0].response }}` - Chain step output (0-indexed)
- `{{ tasks.task_id.response }}` - Workflow task output
- `{{ $TRACE }}` - Complete execution trace

## Common Validation Errors

### Error: "Property 'version' is required"
**Fix:** Add `version: 0` at top level

### Error: "Property 'pattern.type' must be one of..."
**Fix:** Use valid pattern type: `chain`, `routing`, `parallel`, `workflow`, `graph`, `evaluator-optimizer`, `orchestrator-workers`

### Error: "Agent 'xyz' not found in agents"
**Fix:** Ensure agent referenced in pattern is defined in `agents:` section

### Error: "Invalid provider"
**Fix:** Use `bedrock`, `openai`, or `ollama`

## Performance Optimization

1. **Agent Caching**: Reuse agents across steps with same configuration
2. **Model Client Pooling**: Same provider/model/region shares HTTP client
3. **Parallel Execution**: Use `parallel` or `workflow` patterns for independent tasks
4. **Token Budgets**: Set realistic limits to avoid runaway costs
5. **Context Compression**: Enable `context_policy.compression` for long workflows

## Next Steps

Once you understand this core structure:

1. **For pattern details**: Load `Skill("strands-spec/patterns")`
2. **For tool configuration**: Load `Skill("strands-spec/tools")`
3. **For advanced features**: Load `Skill("strands-spec/advanced")`
4. **For examples**: Load `Skill("strands-spec/examples")`
5. **For debugging**: Load `Skill("strands-spec/troubleshooting")`

## Schema Validation

Always validate before execution:
```bash
uv run strands validate my-workflow.yaml
```

Or use inline schema reference:
```yaml
# yaml-language-server: $schema=./strands-workflow.schema.json
version: 0
# ...
```

## Minimal Working Example

```yaml
version: 0
name: "hello-world"

runtime:
  provider: bedrock
  model_id: "anthropic.claude-3-sonnet-20240229-v1:0"
  region: "us-east-1"

agents:
  greeter:
    prompt: "Say hello to {{ name }}"

inputs:
  required:
    name: string

pattern:
  type: chain
  config:
    steps:
      - agent: greeter
        input: "Greet the user"

outputs:
  artifacts:
    - path: "./greeting.txt"
      from: "{{ last_response }}"
```

Run with:
```bash
uv run strands run hello-world.yaml --var name="World"
```
