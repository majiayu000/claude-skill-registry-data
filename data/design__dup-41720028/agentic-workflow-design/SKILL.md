---
name: agentic-workflow-design
description: Design multi-agent AI systems including orchestration patterns, tool design, memory management, and error handling for autonomous agents.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Agentic Workflow Design

## When to Use This Skill

Use this skill when:

- **Agentic Workflow Design tasks** - Working on design multi-agent ai systems including orchestration patterns, tool design, memory management, and error handling for autonomous agents
- **Planning or design** - Need guidance on Agentic Workflow Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Agentic AI systems enable LLMs to take autonomous actions, use tools, and orchestrate complex workflows. Effective design requires careful consideration of orchestration patterns, tool interfaces, memory management, and error handling.

## Agent Architecture Patterns

```text
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT ARCHITECTURE SPECTRUM                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SIMPLE ◄────────────────────────────────────────► COMPLEX       │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │ ReAct    │  │ Plan &   │  │ Multi-   │  │ Hierarchical│     │
│  │ Agent    │  │ Execute  │  │ Agent    │  │ Multi-Agent │     │
│  │          │  │          │  │          │  │             │     │
│  │ Think→   │  │ Plan→    │  │ Parallel │  │ Manager→    │     │
│  │ Act→     │  │ Execute→ │  │ Agents→  │  │ Workers→    │     │
│  │ Observe  │  │ Reflect  │  │ Aggregate│  │ Specialists │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │
│                                                                  │
│  Single turn    Multi-turn     Parallel       Complex           │
│  Simple tasks   Complex tasks  Independent    Interdependent    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Orchestration Patterns

### Pattern 1: ReAct (Reason + Act)

```text
┌─────────────────────────────────────────┐
│              ReAct Loop                  │
├─────────────────────────────────────────┤
│                                          │
│  User Query ──► Thought ──► Action       │
│                     │           │        │
│                     │           ▼        │
│                     │      Tool Call     │
│                     │           │        │
│                     │           ▼        │
│                     └─── Observation ◄───┤
│                              │           │
│                              ▼           │
│                    Continue or Respond   │
│                                          │
└─────────────────────────────────────────┘
```

```csharp
public class ReActAgent
{
    private readonly ILlmClient _llm;
    private readonly IToolExecutor _tools;
    private readonly int _maxIterations;

    public async Task<AgentResponse> Run(
        string userQuery,
        CancellationToken ct)
    {
        var scratchpad = new List<AgentStep>();
        var iteration = 0;

        while (iteration < _maxIterations)
        {
            // Generate thought and action
            var response = await _llm.Complete(
                BuildPrompt(userQuery, scratchpad),
                ct);

            var parsed = ParseResponse(response);

            if (parsed.IsFinalAnswer)
            {
                return AgentResponse.Success(parsed.FinalAnswer, scratchpad);
            }

            // Execute action
            var observation = await _tools.Execute(
                parsed.Action,
                parsed.ActionInput,
                ct);

            scratchpad.Add(new AgentStep
            {
                Thought = parsed.Thought,
                Action = parsed.Action,
                ActionInput = parsed.ActionInput,
                Observation = observation
            });

            iteration++;
        }

        return AgentResponse.MaxIterationsReached(scratchpad);
    }

    private string BuildPrompt(string query, List<AgentStep> scratchpad)
    {
        var sb = new StringBuilder();
        sb.AppendLine("Answer the following question using the available tools.");
        sb.AppendLine($"Question: {query}");
        sb.AppendLine();

        foreach (var step in scratchpad)
        {
            sb.AppendLine($"Thought: {step.Thought}");
            sb.AppendLine($"Action: {step.Action}");
            sb.AppendLine($"Action Input: {step.ActionInput}");
            sb.AppendLine($"Observation: {step.Observation}");
            sb.AppendLine();
        }

        sb.AppendLine("Thought:");
        return sb.ToString();
    }
}
```

### Pattern 2: Plan and Execute

```csharp
public class PlanExecuteAgent
{
    private readonly ILlmClient _planner;
    private readonly ILlmClient _executor;
    private readonly IToolExecutor _tools;

    public async Task<AgentResponse> Run(
        string objective,
        CancellationToken ct)
    {
        // Step 1: Generate plan
        var plan = await GeneratePlan(objective, ct);

        var results = new List<StepResult>();

        // Step 2: Execute each step
        foreach (var step in plan.Steps)
        {
            var result = await ExecuteStep(step, results, ct);
            results.Add(result);

            // Check if replanning needed
            if (result.RequiresReplan)
            {
                plan = await Replan(objective, results, ct);
            }
        }

        // Step 3: Synthesize final answer
        return await SynthesizeResponse(objective, results, ct);
    }

    private async Task<ExecutionPlan> GeneratePlan(
        string objective,
        CancellationToken ct)
    {
        var planPrompt = $"""
            Create a step-by-step plan to accomplish:
            {objective}

            Available tools: {string.Join(", ", _tools.GetToolNames())}

            Output format:
            1. [Step description]
            2. [Step description]
            ...
            """;

        var response = await _planner.Complete(planPrompt, ct);
        return ParsePlan(response);
    }

    private async Task<StepResult> ExecuteStep(
        PlanStep step,
        List<StepResult> previousResults,
        CancellationToken ct)
    {
        var context = BuildExecutionContext(step, previousResults);

        var executePrompt = $"""
            Execute this step: {step.Description}

            Context from previous steps:
            {context}

            Use the appropriate tools to complete this step.
            """;

        // Use ReAct-style execution for the step
        var executor = new ReActAgent(_executor, _tools, 5);
        return await executor.Run(executePrompt, ct);
    }
}
```

### Pattern 3: Multi-Agent Collaboration

```csharp
public class MultiAgentOrchestrator
{
    private readonly Dictionary<string, IAgent> _agents;
    private readonly IAgentRouter _router;

    public async Task<AgentResponse> Run(
        string objective,
        CancellationToken ct)
    {
        var conversation = new ConversationHistory();
        var currentAgent = _router.SelectInitialAgent(objective);
        var maxTurns = 20;

        for (var turn = 0; turn < maxTurns; turn++)
        {
            // Current agent processes
            var response = await _agents[currentAgent].Process(
                objective,
                conversation,
                ct);

            conversation.AddMessage(currentAgent, response.Message);

            // Check for completion
            if (response.IsComplete)
            {
                return AgentResponse.Success(response.FinalAnswer, conversation);
            }

            // Check for handoff
            if (response.HandoffTo != null)
            {
                currentAgent = response.HandoffTo;
                continue;
            }

            // Router decides next agent
            currentAgent = _router.SelectNextAgent(conversation);
        }

        return AgentResponse.MaxTurnsReached(conversation);
    }
}

public class SpecialistAgent : IAgent
{
    private readonly string _role;
    private readonly string _expertise;
    private readonly ILlmClient _llm;
    private readonly IToolExecutor _tools;

    public async Task<AgentTurn> Process(
        string objective,
        ConversationHistory history,
        CancellationToken ct)
    {
        var prompt = $"""
            You are a {_role} with expertise in {_expertise}.

            Objective: {objective}

            Previous discussion:
            {history.Format()}

            Contribute your expertise. If you've completed your part or
            need input from another specialist, indicate a handoff.
            """;

        var response = await _llm.Complete(prompt, ct);

        return ParseAgentResponse(response);
    }
}
```

### Pattern 4: Hierarchical Multi-Agent

```csharp
public class HierarchicalOrchestrator
{
    private readonly IManagerAgent _manager;
    private readonly Dictionary<string, IWorkerAgent> _workers;

    public async Task<AgentResponse> Run(
        string objective,
        CancellationToken ct)
    {
        // Manager creates task breakdown
        var taskPlan = await _manager.PlanTasks(objective, ct);

        var completedTasks = new List<TaskResult>();

        while (taskPlan.HasPendingTasks)
        {
            // Get next executable tasks (dependencies satisfied)
            var executableTasks = taskPlan.GetExecutableTasks(completedTasks);

            // Execute in parallel where possible
            var taskResults = await Task.WhenAll(
                executableTasks.Select(t => ExecuteTask(t, completedTasks, ct)));

            completedTasks.AddRange(taskResults);

            // Manager reviews and potentially adjusts plan
            taskPlan = await _manager.ReviewProgress(
                taskPlan,
                completedTasks,
                ct);
        }

        // Manager synthesizes final result
        return await _manager.SynthesizeResult(objective, completedTasks, ct);
    }

    private async Task<TaskResult> ExecuteTask(
        AgentTask task,
        List<TaskResult> context,
        CancellationToken ct)
    {
        var worker = _workers[task.AssignedWorker];

        return await worker.Execute(
            task,
            context.Where(c => task.Dependencies.Contains(c.TaskId)).ToList(),
            ct);
    }
}
```

## Tool Design

### Tool Interface Best Practices

```csharp
public interface IAgentTool
{
    string Name { get; }
    string Description { get; }
    JsonSchema InputSchema { get; }
    JsonSchema OutputSchema { get; }

    Task<ToolResult> Execute(
        JsonElement input,
        ToolContext context,
        CancellationToken ct);
}

public class DatabaseQueryTool : IAgentTool
{
    public string Name => "query_database";

    public string Description => """
        Execute a read-only SQL query against the application database.
        Use for retrieving data needed to answer user questions.
        Only SELECT queries are allowed - no modifications.
        """;

    public JsonSchema InputSchema => new JsonSchema
    {
        Type = "object",
        Properties = new Dictionary<string, JsonSchemaProperty>
        {
            ["query"] = new JsonSchemaProperty
            {
                Type = "string",
                Description = "The SQL SELECT query to execute"
            },
            ["limit"] = new JsonSchemaProperty
            {
                Type = "integer",
                Description = "Maximum rows to return (default: 100)",
                Default = 100
            }
        },
        Required = new[] { "query" }
    };

    public async Task<ToolResult> Execute(
        JsonElement input,
        ToolContext context,
        CancellationToken ct)
    {
        var query = input.GetProperty("query").GetString();
        var limit = input.TryGetProperty("limit", out var l) ? l.GetInt32() : 100;

        // Validate query is SELECT only
        if (!IsSelectQuery(query))
        {
            return ToolResult.Error("Only SELECT queries are allowed");
        }

        try
        {
            var results = await _database.ExecuteQuery(query, limit, ct);

            return ToolResult.Success(new
            {
                row_count = results.Count,
                columns = results.Columns,
                data = results.Rows.Take(20), // Limit response size
                truncated = results.Rows.Count > 20
            });
        }
        catch (Exception ex)
        {
            return ToolResult.Error($"Query failed: {ex.Message}");
        }
    }
}
```

### Tool Result Patterns

```csharp
public class ToolResult
{
    public bool Success { get; init; }
    public object Data { get; init; }
    public string Error { get; init; }
    public Dictionary<string, object> Metadata { get; init; }

    public static ToolResult Success(object data, Dictionary<string, object> metadata = null)
        => new() { Success = true, Data = data, Metadata = metadata ?? new() };

    public static ToolResult Error(string message)
        => new() { Success = false, Error = message };

    public static ToolResult PartialSuccess(object data, string warning)
        => new() { Success = true, Data = data, Metadata = new() { ["warning"] = warning } };
}
```

## Memory Management

### Memory Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT MEMORY SYSTEM                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────┐  ┌───────────────────┐                   │
│  │  WORKING MEMORY   │  │  EPISODIC MEMORY  │                   │
│  │  (Context Window) │  │  (Past Sessions)  │                   │
│  │                   │  │                   │                   │
│  │  - Current task   │  │  - Summaries      │                   │
│  │  - Recent steps   │  │  - Key decisions  │                   │
│  │  - Tool results   │  │  - User prefs     │                   │
│  └───────────────────┘  └───────────────────┘                   │
│                                                                  │
│  ┌───────────────────┐  ┌───────────────────┐                   │
│  │  SEMANTIC MEMORY  │  │  PROCEDURAL MEM   │                   │
│  │  (Knowledge Base) │  │  (Skills/Habits)  │                   │
│  │                   │  │                   │                   │
│  │  - RAG retrieval  │  │  - Tool patterns  │                   │
│  │  - Facts          │  │  - Workflows      │                   │
│  │  - Domain context │  │  - Optimizations  │                   │
│  └───────────────────┘  └───────────────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Memory Implementation

```csharp
public class AgentMemory
{
    private readonly IVectorStore _semanticMemory;
    private readonly IKeyValueStore _episodicMemory;
    private readonly ConversationBuffer _workingMemory;

    public async Task<MemoryContext> Recall(
        string query,
        AgentContext context,
        CancellationToken ct)
    {
        // Retrieve from semantic memory (RAG)
        var semanticResults = await _semanticMemory.Search(
            query,
            topK: 5,
            ct);

        // Retrieve relevant episodic memories
        var episodicResults = await _episodicMemory.GetRelevant(
            context.UserId,
            query,
            limit: 3,
            ct);

        // Get recent working memory
        var recentHistory = _workingMemory.GetRecent(10);

        return new MemoryContext
        {
            SemanticContext = semanticResults,
            EpisodicContext = episodicResults,
            WorkingContext = recentHistory
        };
    }

    public async Task Store(
        AgentStep step,
        StoreOptions options,
        CancellationToken ct)
    {
        // Always add to working memory
        _workingMemory.Add(step);

        // Conditionally add to episodic memory
        if (options.StoreEpisodic && IsSignificant(step))
        {
            await _episodicMemory.Store(new EpisodicMemory
            {
                UserId = step.Context.UserId,
                SessionId = step.Context.SessionId,
                Summary = SummarizeStep(step),
                Timestamp = DateTime.UtcNow,
                Importance = CalculateImportance(step)
            }, ct);
        }

        // Update semantic memory if knowledge gained
        if (step.ProducedKnowledge)
        {
            await _semanticMemory.Upsert(
                step.Knowledge,
                step.KnowledgeMetadata,
                ct);
        }
    }

    public async Task CompactWorkingMemory(CancellationToken ct)
    {
        // Summarize old entries to save context space
        var old = _workingMemory.GetOlderThan(TimeSpan.FromMinutes(30));

        if (old.Count > 5)
        {
            var summary = await SummarizeSteps(old, ct);
            _workingMemory.ReplaceWith(old, summary);
        }
    }
}
```

## Error Handling and Recovery

### Error Handling Patterns

```csharp
public class ResilientAgentExecutor
{
    private readonly IRetryPolicy _retryPolicy;
    private readonly IFallbackStrategy _fallback;

    public async Task<AgentResponse> ExecuteWithRecovery(
        IAgent agent,
        string objective,
        CancellationToken ct)
    {
        var attempts = new List<ExecutionAttempt>();

        for (var attempt = 0; attempt < _retryPolicy.MaxAttempts; attempt++)
        {
            try
            {
                var response = await agent.Run(objective, ct);

                if (response.Success)
                {
                    return response;
                }

                // Agent completed but failed logically
                attempts.Add(new ExecutionAttempt
                {
                    Attempt = attempt,
                    Error = response.Error,
                    Type = ErrorType.LogicalFailure
                });

                // Try self-correction
                var correctedObjective = await AttemptSelfCorrection(
                    objective,
                    response.Error,
                    attempts,
                    ct);

                objective = correctedObjective ?? objective;
            }
            catch (RateLimitException ex)
            {
                attempts.Add(new ExecutionAttempt
                {
                    Attempt = attempt,
                    Error = ex.Message,
                    Type = ErrorType.RateLimit
                });

                await Task.Delay(ex.RetryAfter, ct);
            }
            catch (ToolExecutionException ex)
            {
                attempts.Add(new ExecutionAttempt
                {
                    Attempt = attempt,
                    Error = ex.Message,
                    Type = ErrorType.ToolFailure
                });

                // Try alternative tool or approach
                var fallbackResponse = await _fallback.Handle(
                    objective,
                    ex,
                    ct);

                if (fallbackResponse.Success)
                {
                    return fallbackResponse;
                }
            }
        }

        return AgentResponse.Failed(attempts);
    }

    private async Task<string> AttemptSelfCorrection(
        string objective,
        string error,
        List<ExecutionAttempt> history,
        CancellationToken ct)
    {
        var correctionPrompt = $"""
            The previous attempt to accomplish this objective failed:
            Objective: {objective}
            Error: {error}
            Previous attempts: {string.Join("\n", history.Select(h => h.Error))}

            How should the objective be modified to avoid this error?
            Respond with the corrected objective or "CANNOT_CORRECT" if no correction is possible.
            """;

        var response = await _llm.Complete(correctionPrompt, ct);

        return response.Contains("CANNOT_CORRECT") ? null : response;
    }
}
```

## Agentic Workflow Template

```markdown
# Agentic Workflow Design: [System Name]

## 1. Agent Overview
- **Primary Objective**: [What the agent accomplishes]
- **Autonomy Level**: [Full/Supervised/Assisted]
- **User Interaction**: [Sync/Async/None]

## 2. Architecture Pattern
- **Pattern**: [ReAct/Plan-Execute/Multi-Agent/Hierarchical]
- **Rationale**: [Why this pattern]

## 3. Agent(s) Definition

### Primary Agent
- **Role**: [Role description]
- **Model**: [Model selection]
- **Tools**: [Available tools]
- **Memory**: [Memory configuration]

### Worker Agents (if multi-agent)
| Agent | Role | Tools | Model |
|-------|------|-------|-------|
| [Agent 1] | [Role] | [Tools] | [Model] |

## 4. Tool Inventory

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| [Tool 1] | [Purpose] | [Schema] | [Schema] |

## 5. Memory Strategy
- **Working Memory**: [Configuration]
- **Episodic Memory**: [What to store]
- **Semantic Memory**: [Knowledge base]

## 6. Error Handling
- **Retry Policy**: [Configuration]
- **Fallback Strategy**: [Approach]
- **Escalation**: [When/how]

## 7. Guardrails
- **Action Limits**: [Limits]
- **Approval Requirements**: [When needed]
- **Sandboxing**: [Isolation approach]

## 8. Observability
- **Logging**: [What to log]
- **Metrics**: [What to track]
- **Tracing**: [Span configuration]
```

## Validation Checklist

- [ ] Orchestration pattern selected
- [ ] Agent roles defined
- [ ] Tool interfaces designed
- [ ] Memory strategy planned
- [ ] Error handling implemented
- [ ] Retry policies configured
- [ ] Guardrails established
- [ ] Observability configured
- [ ] Testing strategy defined
- [ ] Human oversight integrated

## Integration Points

**Inputs from**:

- `model-selection` skill → Agent model choices
- `ai-safety-planning` skill → Guardrails requirements
- `prompt-engineering` skill → Agent prompts

**Outputs to**:

- `token-budgeting` skill → Cost estimation
- `hitl-design` skill → Human oversight integration
- Application code → Agent implementation
