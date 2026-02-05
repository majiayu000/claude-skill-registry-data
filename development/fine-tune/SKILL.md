---
name: fine-tune
description: Use when you need to fine-tune(ファインチューニング) and optimize LangGraph applications based on evaluation criteria. This skill performs iterative prompt optimization for LangGraph nodes without changing the graph structure.
---

# LangGraph Application Fine-Tuning Skill

A skill for iteratively optimizing prompts and processing logic in each node of a LangGraph application based on evaluation criteria.

## 📋 Overview

This skill executes the following process to improve the performance of existing LangGraph applications:

1. **Load Objectives**: Retrieve optimization goals and evaluation criteria from `.langgraph-master/fine-tune.md` (if this file doesn't exist, help the user create it based on their requirements)
2. **Identify Optimization Targets**: Extract nodes containing LLM prompts using Serena MCP (if Serena MCP is unavailable, investigate the codebase using ls, read, etc.)
3. **Baseline Evaluation**: Measure current performance through multiple runs
4. **Implement Improvements**: Identify the most effective improvement areas and optimize prompts and processing logic
5. **Re-evaluation**: Measure performance after improvements
6. **Iteration**: Repeat steps 4-5 until goals are achieved

**Important Constraint**: Only optimize prompts and processing logic within each node without modifying the graph structure (nodes, edges configuration).

## 🎯 When to Use This Skill

Use this skill in the following situations:

1. **When performance improvement of existing applications is needed**

   - Want to improve LLM output quality
   - Want to improve response speed
   - Want to reduce error rate

2. **When evaluation criteria are clear**

   - Optimization goals are defined in `.langgraph-master/fine-tune.md`
   - Quantitative evaluation methods are established

3. **When improvements through prompt engineering are expected**
   - Improvements are likely with clearer LLM instructions
   - Adding few-shot examples would be effective
   - Output format adjustment is needed

## 📖 Fine-Tuning Workflow Overview

### Phase 1: Preparation and Analysis

**Purpose**: Understand optimization targets and current state

**Main Steps**:

1. Load objective setting file (`.langgraph-master/fine-tune.md`)
2. Identify optimization targets (Serena MCP or manual code investigation)
3. Create optimization target list (evaluate improvement potential for each node)

→ See [workflow.md](workflow.md#phase-1-preparation-and-analysis) for details

### Phase 2: Baseline Evaluation

**Purpose**: Quantitatively measure current performance

**Main Steps**: 4. Prepare evaluation environment (test cases, evaluation scripts) 5. Baseline measurement (recommended: 3-5 runs) 6. Analyze baseline results (identify problems)

**Important**: When evaluation programs are needed, create evaluation code in a specific subdirectory (users may specify the directory).

→ See [workflow.md](workflow.md#phase-2-baseline-evaluation) and [evaluation.md](evaluation.md) for details

### Phase 3: Iterative Improvement

**Purpose**: Data-driven incremental improvement

**Main Steps**: 7. Prioritization (select the most impactful improvement area) 8. Implement improvements (prompt optimization, parameter tuning) 9. Post-improvement evaluation (re-evaluate under the same conditions) 10. Compare and analyze results (measure improvement effects) 11. Decide whether to continue iteration (repeat until goals are achieved)

→ See [workflow.md](workflow.md#phase-3-iterative-improvement) and [prompt_optimization.md](prompt_optimization.md) for details

### Phase 4: Completion and Documentation

**Purpose**: Record achievements and provide future recommendations

**Main Steps**: 12. Create final evaluation report (improvement content, results, recommendations) 13. Code commit and documentation update

→ See [workflow.md](workflow.md#phase-4-completion-and-documentation) for details

## 🔧 Tools and Technologies Used

### MCP Server Utilization

- **Serena MCP**: Codebase analysis and optimization target identification

  - `find_symbol`: Search for LLM clients
  - `find_referencing_symbols`: Identify prompt construction locations
  - `get_symbols_overview`: Understand node structure

- **Sequential MCP**: Complex analysis and decision making
  - Determine improvement priorities
  - Analyze evaluation results
  - Plan next actions

### Key Optimization Techniques

1. **Few-Shot Examples**: Accuracy +10-20%
2. **Structured Output Format**: Parsing errors -90%
3. **Temperature/Max Tokens Adjustment**: Cost -20-40%
4. **Model Selection Optimization**: Cost -40-60%
5. **Prompt Caching**: Cost -50-90% (on cache hit)

→ See [prompt_optimization.md](prompt_optimization.md) for details

## 📚 Related Documentation

Detailed guidelines and best practices:

- **[workflow.md](workflow.md)** - Fine-tuning workflow details (execution procedures and code examples for each phase)
- **[evaluation.md](evaluation.md)** - Evaluation methods and best practices (metric calculation, statistical analysis, test case design)
- **[prompt_optimization.md](prompt_optimization.md)** - Prompt optimization techniques (10 practical methods and priorities)
- **[examples.md](examples.md)** - Practical examples collection (copy-and-paste ready code examples and template collection)

## ⚠️ Important Notes

1. **Preserve Graph Structure**

   - Do not add or remove nodes or edges
   - Do not change data flow between nodes
   - Maintain state schema

2. **Evaluation Consistency**

   - Use the same test cases
   - Measure with the same evaluation metrics
   - Run multiple times to confirm statistically significant improvements

3. **Cost Management**

   - Consider evaluation execution costs
   - Adjust sample size as needed
   - Be mindful of API rate limits

4. **Version Control**
   - Git commit each iteration's changes
   - Maintain rollback-capable state
   - Record evaluation results

## 🎓 Fine-Tuning Best Practices

1. **Start Small**: Optimize from the most impactful node
2. **Measurement-Driven**: Always perform quantitative evaluation before and after improvements
3. **Incremental Improvement**: Validate one change at a time, not multiple simultaneously
4. **Documentation**: Record reasons and results for each change
5. **Iteration**: Continuously improve until goals are achieved

## 🔗 Reference Links

- [LangGraph Official Documentation](https://docs.langchain.com/oss/python/langgraph/overview)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
