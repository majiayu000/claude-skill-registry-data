---
name: finwiz-ai-minimalism
description: "AI minimalism principles for FinWiz - when to use Python vs AI agents. Use when deciding between AI tasks and Python implementations, or when optimizing costs and performance."
allowed-tools: ["Read", "Edit"]
---

# FinWiz AI Minimalism

**Core Principle**: AI agents are tools, not the alpha and the omega. Use Python for deterministic, rule-based tasks.

## Decision Framework

### Use AI Agents ONLY For

✅ **Analysis requiring reasoning** - Interpreting complex financial data, identifying patterns
✅ **Synthesis of complex information** - Combining multiple data sources with judgment
✅ **Generating insights from unstructured data** - Analyzing news, sentiment, qualitative factors
✅ **Natural language understanding** - Parsing complex text, extracting meaning
✅ **Creative content generation** - Writing analysis narratives, explanations

### Use Python (NOT AI) For

❌ **HTML generation** - Use Jinja2 templates
❌ **Data consolidation** - Use Python functions
❌ **File I/O operations** - Use standard Python file operations
❌ **Calculations and formulas** - Use Python math/numpy
❌ **Data validation** - Use Pydantic models
❌ **Template rendering** - Use Jinja2
❌ **Data transformation** - Use pandas/Python
❌ **Deterministic logic** - Use if/else, loops, functions

## Cost-Benefit Analysis

**Example: Generating 100 HTML reports**

| Approach | Cost | Time | Reliability |
|----------|------|------|-------------|
| AI Agent | $5-10 | 500-1000s | 95% |
| Python Template | $0 | 1-2s | 100% |

**Savings: $5-10 per 100 reports, 500x faster, 100% reliable**

## Evaluation Checklist

Before creating an AI task, ask:

- [ ] Is this task deterministic? (same input = same output)
- [ ] Can this be expressed as a template?
- [ ] Is this just data transformation?
- [ ] Is this a calculation or validation?
- [ ] Can a junior developer implement this in Python?

If you answered YES to any question, **use Python, not AI**.

## Implementation Examples

### ❌ WRONG: Using AI for HTML Generation

```python
@task
def generate_html_report(self) -> Task:
    return Task(
        description="Generate HTML report from JSON data",
        agent=self.reporter(),  # AI agent
        # WRONG: Wasting LLM calls on template rendering
    )
```

### ✅ CORRECT: Using Python Template

```python
def generate_html_report(json_data: dict) -> str:
    """Generate HTML report using Jinja2 template."""
    template = jinja_env.get_template('report.html')
    return template.render(data=json_data)
    # CORRECT: Fast, cheap, testable
```

### ❌ WRONG: Using AI for Data Consolidation

```python
@task
def consolidate_reports(self) -> Task:
    return Task(
        description="Read all crew reports and consolidate them",
        agent=self.aggregator(),  # AI agent
        # WRONG: Wasting LLM calls on file reading
    )
```

### ✅ CORRECT: Using Python Function

```python
def consolidate_reports(file_paths: list[str]) -> ConsolidatedReport:
    """Consolidate crew reports using Python."""
    reports = []
    for path in file_paths:
        with open(path) as f:
            report = CrewReport.model_validate_json(f.read())
            reports.append(report)
    return ConsolidatedReport(reports=reports)
    # CORRECT: Fast, cheap, testable
```

## Benefits of Python Over AI

1. **Cost**: Free vs. LLM API costs
2. **Speed**: Milliseconds vs. seconds
3. **Reliability**: Deterministic vs. probabilistic
4. **Testability**: Unit tests vs. prompt testing
5. **Maintainability**: Code review vs. prompt engineering
6. **Debugging**: Stack traces vs. LLM output inspection

## Implementation Guidelines

### HTML Templates (Jinja2)

- Create professional templates with light/dark mode
- Accept JSON data as input
- Include CSS for responsive design
- Make templates maintainable by developers

### Data Processing (Python)

- Use Pydantic for validation
- Use pandas for data transformation
- Write unit tests for all functions
- Keep functions pure (no side effects)

### File Operations (Python)

- Use pathlib for path handling
- Use context managers for file I/O
- Validate data with Pydantic after reading
- Handle errors gracefully

## Remember

**Be strong, not lazy. Save the project, not your energy.**

Evaluate every AI task critically. If Python can do it, use Python.

When in doubt, choose Python for:

- Template rendering
- Data transformation
- File operations
- Calculations
- Validation
- Deterministic logic

Reserve AI for:

- Complex reasoning
- Natural language tasks
- Creative content
- Unstructured data analysis
