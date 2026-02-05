---
name: consider
description: |
  Selects and applies mental models for structured problem analysis. Triggers when user asks "why", "what if", "how should we", needs systematic problem-solving, or mentions analyzing a situation. MUST BE USED when comparing options, making decisions, or evaluating trade-offs.
---

<objective>
Analyze problems, decisions, and questions using proven mental frameworks. This skill:
1. Recalls relevant past analyses from memory (if MCP memory available)
2. Classifies problems by type and characteristics
3. Assesses information requirements (local, web, user)
4. Gathers context efficiently using subagent coordination
5. Selects and executes optimal mental model(s)
6. Synthesizes actionable insights
7. Stores analysis to memory for future recall
</objective>

<quick_start>
```
/consider [problem statement]
```

The command will analyze, gather required information, then apply the right model(s).
</quick_start>

<problem_classification>

<problem_types>
| Type | Signals | Description |
|------|---------|-------------|
| DIAGNOSIS | "why", "cause", "root" | Understanding why something happened |
| DECISION | "should I", "decide", "choose" | Choosing between options |
| PRIORITIZATION | "overwhelmed", "too many", "first" | Determining what matters most |
| INNOVATION | "stuck", "nothing works", "assume" | Breaking through barriers |
| RISK | "fail", "risk", "wrong" | Assessing potential failures |
| FOCUS | "focus", "leverage", "important" | Finding highest-impact actions |
| OPTIMIZATION | "simplify", "remove", "reduce" | Improving by subtraction |
| STRATEGY | "strategy", "position", "compete" | Assessing competitive position |
| DELIBERATION | "perspectives", "group", "meeting", "angles" | Exploring from multiple viewpoints |
| SYSTEMIC | "symptoms", "causes", "constraint", "bottleneck" | Complex system diagnosis (TOC) |
</problem_types>

<classification_dimensions>
**Temporal Focus**: PAST | PRESENT | FUTURE
**Complexity**: SIMPLE | COMPLICATED | COMPLEX
**Emotional Loading**: HIGH | LOW
**Information State**: OVERLOAD | SPARSE | CONFLICTING
</classification_dimensions>

</problem_classification>

<approach_selection>

<selection_matrix>
| Problem Type | Focus Area | Primary Model | Supporting Model |
|--------------|------------|---------------|------------------|
| DIAGNOSIS | Root cause | 5-Whys | First Principles |
| DIAGNOSIS | Assumptions | First Principles | Occam's Razor |
| DIAGNOSIS | Simplest explanation | Occam's Razor | 5-Whys |
| DECISION | Time horizons | 10-10-10 | Second-Order |
| DECISION | Tradeoffs | Opportunity Cost | 10-10-10 |
| DECISION | Failure prevention | Inversion | Second-Order |
| PRIORITIZATION | Urgency/importance | Eisenhower Matrix | Pareto |
| PRIORITIZATION | Impact ranking | Pareto | One Thing |
| PRIORITIZATION | Single leverage | One Thing | Pareto |
| INNOVATION | Challenge assumptions | First Principles | Inversion |
| INNOVATION | Flip perspective | Inversion | First Principles |
| INNOVATION | Subtract complexity | Via Negativa | One Thing |
| RISK | Failure modes | Inversion | Second-Order |
| RISK | Consequence chains | Second-Order | Inversion |
| FOCUS | Highest leverage | One Thing | Pareto |
| FOCUS | Vital few | Pareto | One Thing |
| FOCUS | What to eliminate | Via Negativa | Pareto |
| OPTIMIZATION | Remove bloat | Via Negativa | Pareto |
| OPTIMIZATION | Efficiency | Pareto | Via Negativa |
| STRATEGY | Position | SWOT | Second-Order |
| STRATEGY | Competition | SWOT | Inversion |
| STRATEGY | Long-term | Second-Order | SWOT |
| DELIBERATION | Perspectives | Six Hats | SWOT |
| DELIBERATION | Emotions vs logic | Six Hats | 10-10-10 |
| SYSTEMIC | Constraint | TOC | 5-Whys |
| SYSTEMIC | Conflict resolution | TOC | Six Hats |
</selection_matrix>

</approach_selection>

<available_models>

| Model | Best For | Core Question |
|-------|----------|---------------|
| 5-Whys | Root cause analysis | "Why did this happen?" (iterate 5x) |
| 10-10-10 | Decisions with emotional bias | "How will I feel in 10 min/months/years?" |
| Eisenhower | Task prioritization | "Is this urgent AND important?" |
| First Principles | Challenging assumptions | "What is fundamentally true?" |
| Inversion | Risk prevention | "What would guarantee failure?" |
| Occam's Razor | Competing explanations | "Which requires fewest assumptions?" |
| One Thing | Finding leverage | "What makes everything else easier?" |
| Opportunity Cost | Tradeoff analysis | "What am I giving up?" |
| Pareto | Impact prioritization | "Which 20% drives 80% of results?" |
| Second-Order | Consequence analysis | "And then what happens?" |
| SWOT | Strategic position | "Strengths/Weaknesses/Opportunities/Threats?" |
| Via Negativa | Simplification | "What should I remove?" |
| Six Hats | Parallel perspectives | "What are all the angles?" |
| TOC | Systemic root cause + conflict resolution | "What constraint is blocking the system?" |

**Full model templates**: See `references/` directory for complete execution frameworks.

</available_models>

<information_requirements>

<model_information_needs>
| Model | Local Sources | Web Research | User Clarification |
|-------|--------------|--------------|-------------------|
| 5-Whys | Logs, history, docs | Rarely needed | Root symptoms, timeline |
| 10-10-10 | Past decisions | Rarely needed | Values, priorities |
| Eisenhower | Task lists, deadlines | Rarely needed | Urgency criteria |
| First Principles | Technical docs | Industry fundamentals | Core assumptions |
| Inversion | Failure history | Industry failure cases | Success definition |
| Occam's Razor | Available evidence | Rarely needed | Competing hypotheses |
| One Thing | Goals, metrics | Rarely needed | Primary objective |
| Opportunity Cost | Project docs, budgets | Market rates, benchmarks | Budget constraints |
| Pareto | Metrics, analytics | Industry benchmarks | Success metrics |
| Second-Order | Codebase, history | Industry trends, precedents | Time horizon |
| SWOT | Internal docs, capabilities | Market/competitor data | Strategic goals |
| Via Negativa | Current state docs | Best practices | What to preserve |
</model_information_needs>

<information_source_decision>
**Before executing any model, classify each information need:**

| Need Type | Source | Tool/Method |
|-----------|--------|-------------|
| Historical context | Local | Read (logs, docs, git history) |
| Codebase patterns | Local | Task(Explore) with constraints |
| Current metrics | Local | Read analytics, logs |
| Market data | Web | Task + WebSearch |
| Competitor info | Web | Task + WebSearch |
| Industry benchmarks | Web | Task + WebSearch |
| User preferences | User | AskUserQuestion |
| Success criteria | User | AskUserQuestion |
| Constraints/limits | User | AskUserQuestion |
| Technical specs | Local/User | Read docs OR AskUserQuestion |
</information_source_decision>

</information_requirements>

<research_coordination>

When information gathering is needed, use Task tool with structured prompts for token efficiency.

<local_context_gathering>
**For codebase/local file analysis:**

```
@type: AnalyzeAction
about: "[specific question about codebase/docs]"

@return Answer:
- text: string (direct answer, max 200 chars)
- evidence: string[] (file:line references, max 5)
- confidence: string (high|medium|low)

@constraints:
  maxTokens: 2000
  format: JSON object

Return ONLY the specified structure. No preamble or explanations.
```

Use `subagent_type: Explore` with thoroughness based on scope:
- Single file/function: `quick`
- Module/feature: `medium`
- Cross-cutting concern: `thorough`
</local_context_gathering>

<web_research_gathering>
**For market/competitor/industry research:**

```
@type: AnalyzeAction
query: "[specific research query]"

@return ItemList (max 5 items):
- position: integer
- name: string (source name)
- url: string (if available)
- summary: string (max 150 chars, key finding)
- relevance: string (high|medium|low)

@constraints:
  maxTokens: 3000
  format: markdown table

Return ONLY the specified structure. No commentary.
```

Use WebSearch or WebFetch for:
- Current market conditions
- Competitor analysis
- Industry benchmarks
- Recent trends or news
</web_research_gathering>

<parallel_gathering>
**When multiple independent information needs exist:**

Invoke multiple Task calls in a single message:
- Codebase analysis (Task/Explore)
- Web research (Task with WebSearch)
- These run in parallel, reducing latency

**Example parallel invocation:**
```
Task 1: Explore codebase for error handling patterns
Task 2: WebSearch for "industry error handling best practices 2024"
```

Both return focused, structured responses within token budgets.
</parallel_gathering>

</research_coordination>

<combination_patterns>

<serial_chains>
Use when output of one model feeds the next:

**Diagnostic Chain**: 5-Whys → First Principles → Inversion
(find root → verify assumptions → prevent recurrence)

**Decision Chain**: Opportunity Cost → Second-Order → 10-10-10
(what you give up → consequences → time horizons)

**Priority Chain**: Pareto → One Thing → Via Negativa
(vital few → single leverage → remove rest)

**Strategic Chain**: SWOT → Inversion → Second-Order
(position → failure modes → consequences)
</serial_chains>

<parallel_triangulation>
Use multiple lenses simultaneously for validation:

**High-stakes decision**: 10-10-10 + Inversion + Second-Order
**Strategic pivot**: SWOT + First Principles + Opportunity Cost
**Simplification**: Via Negativa + Pareto + One Thing
</parallel_triangulation>

</combination_patterns>

<memory_recall>

**At analysis start, if MCP memory tools are available:**

<step_0_recall>
**Recall Past Context**

Use `mcp__memory__search_nodes` to find relevant prior analyses:

```
search_nodes("{key problem terms}")
```

**Look for:**
- Similar Problem entities (entityType: "Problem")
- Related RootCause entities (entityType: "RootCause")
- Applicable Insight entities (entityType: "Insight")

**If matches found, use `mcp__memory__open_nodes` to get details:**

```
open_nodes(["problem-similar-issue", "insight-relevant-finding"])
```

**Present to user:**
```
## Prior Context (from memory)

**Similar problems analyzed:**
- [problem name]: [key observations]

**Relevant insights:**
- [insight]: [content, outcome]

**Recurring root causes in this area:**
- [root cause]: [occurrence count]
```

**Use prior context to:**
- Suggest models that worked well before
- Highlight root causes that recur
- Avoid repeating failed approaches
- Build on validated insights

**Skip memory recall if:**
- MCP memory tools not available
- User requests fresh analysis
- No relevant matches found
</step_0_recall>

</memory_recall>

<process>

<step_1_analyze>
**Analyze Problem**
- Read problem statement
- Detect signal words (see problem_types table)
- Classify: type, temporal focus, complexity, emotional loading, information state
</step_1_analyze>

<step_2_confirm>
**Confirm Classification**
- Use AskUserQuestion to verify:
  - Problem type classification
  - Focus area within type
  - Any constraints or preferences
- Refine classification based on response
</step_2_confirm>

<step_3_assess_information>
**Assess Information Needs**
For selected model(s), determine:

1. **Available locally?**
   - Conversation history
   - Codebase/project files
   - User-provided documents

2. **Requires web research?**
   - Market/competitor data
   - Industry benchmarks
   - Current trends

3. **Must ask user?**
   - Personal values/priorities
   - Constraints not documented
   - Success criteria
</step_3_assess_information>

<step_4_gather>
**Gather Information**

Execute information gathering based on assessment:

- **Local**: Use Read or Task(Explore) with token constraints
- **Web**: Use Task with WebSearch, structured return format
- **User**: Use AskUserQuestion with specific, focused questions

**Parallel execution**: If needs are independent, invoke multiple Task calls in single message.

**Token budget guidance**:
- Simple lookup: 1000-2000 tokens
- Moderate analysis: 2000-3000 tokens
- Complex research: 3000-5000 tokens
</step_4_gather>

<step_5_execute>
**Execute Model(s)**

With gathered context:
1. Load full model template from `references/[model-name].md`
2. Apply model systematically using template structure
3. For serial chains: complete each model before starting next
4. For parallel triangulation: apply all models, then compare
</step_5_execute>

<step_6_synthesize>
**Synthesize Insights**

Deliver:
- **Key Insight**: Single most important finding (1-2 sentences)
- **Recommended Action**: Specific next step
- **Confidence Level**: High/Medium/Low with reasoning
- **Information Gaps**: What couldn't be determined (if any)
</step_6_synthesize>

</process>

<validation>

**Before proceeding to execution, verify:**

- [ ] Problem type confirmed with user
- [ ] Model selection appropriate for type + focus
- [ ] Information needs classified (local/web/user)
- [ ] Required information gathered with structured responses
- [ ] Token budgets respected in subagent calls
- [ ] No open-ended research (all queries focused)

**Red flags requiring user clarification:**
- Problem fits multiple types equally
- Critical information unavailable
- High emotional loading detected
- Conflicting constraints identified

</validation>

<success_criteria>

Analysis is successful when:
- Problem correctly classified and confirmed
- Required information gathered efficiently (minimal tokens)
- Model(s) applied with full rigor using templates
- Insight is specific and actionable
- Confidence level justified
- User can take immediate action on recommendation

</success_criteria>

<output_format>

## Classification Output Format

For the problem classification section (step 1), use TOON structured format:

```toon
@type: AnalyzeAction
name: problem-classification
object: [problem statement text]
actionStatus: CompletedActionStatus

classification:
primaryType: [DIAGNOSIS|DECISION|PRIORITIZATION|INNOVATION|RISK|FOCUS|OPTIMIZATION|STRATEGY]
temporalFocus: [PAST|PRESENT|FUTURE]
complexity: [SIMPLE|COMPLICATED|COMPLEX]
emotionalLoading: [HIGH|LOW]

signals[N]: [key,signal,words]
```

**Note:** Keep all reasoning, framework selection, model execution, and synthesis as markdown prose. Only use TOON for the structured classification output at the beginning of the analysis.

</output_format>

<references>

Model execution templates (read when applying specific model):
- `references/5-whys.md` - Root cause drilling
- `references/10-10-10.md` - Time horizon analysis
- `references/eisenhower.md` - Urgency/importance matrix
- `references/first-principles.md` - Assumption challenging
- `references/inversion.md` - Failure mode analysis
- `references/occams-razor.md` - Simplest explanation
- `references/one-thing.md` - Leverage identification
- `references/opportunity-cost.md` - Tradeoff analysis
- `references/pareto.md` - 80/20 analysis
- `references/second-order.md` - Consequence chains
- `references/swot.md` - Strategic position
- `references/via-negativa.md` - Improvement by subtraction
- `references/six-hats.md` - Parallel perspective exploration
- `references/toc.md` - Theory of Constraints logical thinking

</references>

<memory_reference>

For memory schema details, see `mcp/memory-schema.md`.

</memory_reference>
