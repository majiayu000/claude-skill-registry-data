---
name: field-agent-documentation
description: Comprehensive template and guidelines for documenting Field Agents including technical specifications, system prompts, tool specifications, user interactions, and standardized documentation structure
---

# Field Agent Documentation Standards

This skill provides a complete template and best practices for creating professional, comprehensive documentation for Field Agents. Following these standards ensures consistency, clarity, and ease of use across all agent documentation.

## When to Use This Skill

Use this skill when you need to:
- Create documentation for a new Field Agent
- Standardize existing Field Agent documentation
- Write system prompts with best practices
- Define tool specifications and naming conventions
- Structure user prompts and interaction patterns
- Document agent architecture and technical details

## Documentation Structure Overview

Complete Field Agent documentation should include these sections in order:

```markdown
1. Basic Information (metadata, links, status)
2. Team Structure (owners, contributors)
3. Purpose & Functionality (description, value, users)
4. Usage Scenarios (use cases, examples)
5. Technical Specifications (model, settings, parameters)
6. Dependencies & Integration (requirements, data sources)
7. Agent/Sub-Agent Details (per-agent specifications)
8. System Prompt (detailed agent instructions)
9. Tools (function specifications and schemas)
10. Input/Output Format (data structures, formats)
11. User Prompts (interaction patterns, guided flows)
12. Development Roadmap (milestones, phases)
13. Demo (examples, videos, recordings)
```

---

## Section 1: Basic Information

This section provides essential metadata about the agent.

### Template

```markdown
# [Agent Name]

## Basic Information

| Item | Details |
|------|---------|
| **Project Name** | [Clean, self-explanatory, immutable name] |
| **Type** | Field Agent |
| **Interface Type** | TD Workflow / Chat / Slack / API |
| **GitHub Repo Link** | [Repository URL] |
| **Status** | Development / Staging / Production |
| **Version** | [Semantic version: MAJOR.MINOR.PATCH] |
| **Last Updated** | [YYYY-MM-DD] |
| **Agent Instance** | [Cloud provider: instance ID] |
| **Agent Link** | [Direct link to agent] |
| **One-Pager Slide** | [Link to overview presentation] |
| **Demo Video** | [Link to demonstration recording] |
| **Demo Talk-Track** | [Link to demo script] |
```

### Best Practices
- **Project Name**: Choose a clear, descriptive name that won't change
- **Status**: Keep status current (Development → Staging → Production)
- **Version**: Use semantic versioning (1.0.0, 1.1.0, 2.0.0)
- **Links**: Ensure all links are accessible to target audience

---

## Section 2: Team Structure

Document who is responsible for the agent.

### Template

```markdown
## Team Structure

| Role | Assignee |
|------|----------|
| **Product Owner / Main Architect** | [Name, Email] |
| **Additional Contributors** | [Names, Roles] |
| **Support Contact** | [Team/Channel] |
```

### Best Practices
- Include contact information for support
- List all contributors for accountability
- Update when team changes occur

---

## Section 3: Purpose & Functionality

Explain what the agent does and why it matters.

### Template

```markdown
## Purpose & Functionality

### Description
[Brief 2-3 sentence description of what the agent performs and its core functionality]

### Key Capabilities
- **Integration 1**: [What it integrates with and how]
- **Integration 2**: [What it integrates with and how]
- **Core Feature**: [Primary capability description]

### Business Value
[Explain the business value this agent delivers. What problems does it solve? What ROI does it provide?]

### Target Users
- **Primary**: [Job roles/personas who will use this most]
- **Secondary**: [Additional users who may benefit]

### Potential Applications
[Detailed description of who will use this agent and in what contexts]
```

### Example

```markdown
## Purpose & Functionality

### Description
Customer Segmentation Agent analyzes customer data to automatically identify behavioral segments using RFM (Recency, Frequency, Monetary) analysis and predictive modeling.

### Key Capabilities
- **Database Integration**: Connects to Treasure Data customer databases
- **Segmentation Algorithms**: RFM, K-means clustering, behavioral scoring
- **Visualization**: Generates interactive Plotly charts and segment distributions

### Business Value
Enables marketing teams to identify high-value customer segments 10x faster than manual analysis, improving campaign targeting accuracy by 35% and increasing ROI on marketing spend.

### Target Users
- **Primary**: Marketing Managers, CRM Analysts, Customer Success Teams
- **Secondary**: Data Analysts, Business Intelligence Teams

### Potential Applications
Marketing teams use this agent to create targeted campaigns, CRM teams identify at-risk customers for retention programs, and analysts explore customer lifetime value patterns.
```

---

## Section 4: Usage Scenarios

Provide concrete examples of how the agent is used.

### Template

```markdown
## Usage Scenarios

### Primary Use Case
[Describe the most common use case with a step-by-step example]

**Example:**
1. User asks: "[Sample user query]"
2. Agent performs: "[What the agent does]"
3. Agent returns: "[What the user receives]"

### Additional Use Cases
1. **Use Case Name**: [Description and benefit]
2. **Use Case Name**: [Description and benefit]
3. **Use Case Name**: [Description and benefit]

### Example Scenarios

#### Scenario 1: [Name]
**Context**: [When this scenario applies]
**User Input**: "[Example user query]"
**Agent Output**: [What the agent provides]
**Outcome**: [Business result]

#### Scenario 2: [Name]
[Follow same structure]
```

---

## Section 5: Technical Specifications

Define the technical configuration of the agent.

### Template

```markdown
## Technical Specifications

| Item | Details |
|------|---------|
| **Agent Name** | [Name - use `[Sub]` prefix for sub-agents] |
| **Model Name** | Claude 4 Sonnet ⭐ (Recommended) / Claude 3.5 Sonnet / Claude 3 Haiku |
| **Max Tool Iterations** | [Number - controls resource consumption] |
| **Temperature** | [0-1, where 0 = deterministic, 1 = creative] ⭐ Recommended: 0 |
| **Max Tokens** | [Output token limit] |
| **Timeout** | [Execution timeout in seconds] |
```

### Model Selection Guide

**Claude 4 Sonnet (Recommended)** ⭐
- Best for: Most production Field Agents
- Benefits: Highest performance, more output tokens, better reasoning
- Use when: You need reliability and comprehensive outputs

**Claude 3.5 Sonnet**
- Best for: Alternative to Claude 4, similar capabilities
- Benefits: Strong performance, widely tested
- Use when: Claude 4 not available or testing compatibility

**Claude 3 Haiku**
- Best for: Lightweight, fast-response tasks
- Benefits: Lower cost, faster execution
- Use when: Simple queries, real-time requirements, budget constraints

### Temperature Guide

| Temperature | Behavior | Best For |
|-------------|----------|----------|
| **0** ⭐ | Deterministic, consistent answers | Most Field Agents, production use |
| **0.3** | Slight variation, mostly consistent | Agents needing minor creative variation |
| **0.7** | Balanced creativity and consistency | Content generation with some flexibility |
| **1.0** | Maximum creativity, varied outputs | Creative writing, brainstorming agents |

**Recommended**: Use temperature **0** for Field Agents to ensure consistent, reliable outputs.

### Max Tool Iterations

Controls how many times the agent can execute tools before stopping.

```markdown
- **Low (5-10)**: Simple agents with few tool calls
- **Medium (15-20)**: Most Field Agents with moderate complexity
- **High (25-30)**: Complex agents requiring multiple data sources and iterations
```

**Best Practice**: Start with 15-20, increase only if agent needs more steps.

---

## Section 6: Dependencies & Integration

Document all external requirements and integrations.

### Template

```markdown
## Dependencies & Integration

### Required Data Sources
| Data Source | Purpose | Access Requirements |
|-------------|---------|---------------------|
| [Database/Table] | [What data is used] | [Permissions needed] |

### Integration Points
| Integration | Type | Purpose |
|-------------|------|---------|
| [System/API] | [REST/GraphQL/SDK] | [What it's used for] |

### Prerequisites
- [ ] Access to [database/system]
- [ ] Permissions: [specific permissions]
- [ ] API keys configured: [which APIs]
- [ ] Dependencies installed: [libraries/tools]

### Dependencies on Other Systems
- [None] OR [List dependent workflows, features, product permissions]
```

### Example

```markdown
## Dependencies & Integration

### Required Data Sources
| Data Source | Purpose | Access Requirements |
|-------------|---------|---------------------|
| `customer_db.transactions` | Transaction history for RFM analysis | Read access to customer_db |
| `customer_db.profiles` | Customer demographic data | Read access to customer_db |

### Integration Points
| Integration | Type | Purpose |
|-------------|------|---------|
| Treasure Data Trino | SQL Query | Data extraction and analysis |
| Plotly | Visualization Library | Chart generation |

### Prerequisites
- [ ] Access to `customer_db` database
- [ ] Permissions: Read access on customer tables
- [ ] API keys configured: None required
- [ ] Dependencies installed: Plotly for visualizations

### Dependencies on Other Systems
- Requires Treasure Data instance with Trino query engine
- No dependencies on external workflows
```

---

## Section 7: Agent/Sub-Agent Details

Provide detailed specifications for each agent and sub-agent.

### Template

```markdown
## Agent Details: [Agent Name]

| Item | Details |
|------|---------|
| **Agent Name** | [Name] or **[Sub] [Name]** for sub-agents |
| **Model Name** | Claude 4 Sonnet ⭐ |
| **Max Tool Iterations** | [Number] |
| **Temperature** | 0 ⭐ |
| **Purpose** | [What this specific agent does] |
| **Invocation** | [How this agent is called] |

### Sub-Agents
If this agent uses sub-agents, list them:

- **[Sub] Sub-Agent Name**: [Purpose and when it's invoked]
```

### Best Practices
- Use `[Sub]` prefix for sub-agents to distinguish from main agents
- Document invocation patterns (how/when sub-agents are called)
- Specify different configurations if sub-agents use different models

---

## Section 8: System Prompt

The system prompt is the most critical element - it defines agent behavior.

### System Prompt Structure Template

```markdown
## System Prompt: [Agent Name]

# [Agent Name]

[Brief one-line description of agent role and purpose]

# Role

The agent's role and responsibilities:
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

# Goal

[Detailed description of what the user receives when the agent is executed and what the agent aims to achieve]

## Basic Principles

High-level workflow:
1. [Step 1: What happens first]
2. [Step 2: What happens next]
3. [Step 3: Final steps]
4. [Step 4: Output delivery]

## Available Tools

### [Tool Category/Purpose]

**Tool**: `tool_name_in_snake_case`
**Purpose**: [Brief purpose of this tool]
**Input**: [What inputs the tool consumes]
**Output**: [What outputs the tool returns]

### [Next Tool Category]

**Tool**: `another_tool_name`
**Purpose**: [Brief purpose]
**Input**: [Input parameters]
**Output**: [Return values]

## Task Flow

### Task 1: [Tool Name] [required = true, mandatory_start = true]

**Execution**:
call_<tool_name>[required = true, mandatory_start = true]

**Steps** [sequential=true]:
1. [Detailed step-by-step pseudo-logic]
2. [What the tool should do]
3. [How to handle results]
4. [Error handling]

**Output Format**:
[Describe or show sample output format]

### Task 2: [Next Tool] [required = false]

[Follow same structure]

## Checklist (Optional)

If applicable, provide a validation checklist:
- [ ] [Validation item 1]
- [ ] [Validation item 2]
- [ ] [Validation item 3]
```

### System Prompt Best Practices

#### 1. Tool Naming Conventions ⭐

**Use snake_case with descriptive names:**

✅ **Good Examples:**
```
verify_database_access
list_columns_customer_db
query_sales_data
calculate_rfm_scores
generate_segment_visualization
fetch_customer_transactions
```

❌ **Bad Examples:**
```
verify          # Too vague
list            # What are we listing?
query           # Query what?
verifydbaccess  # Hard to read, no separators
listColumns     # Should be snake_case
```

**Naming Pattern**: `[action]_[object]_[context]`
- **Action**: verify, list, query, calculate, generate, fetch, create, update
- **Object**: database, columns, data, scores, visualization
- **Context**: customer_db, sales, rfm, etc.

#### 2. Reduce Hallucination with Detailed Logic

Provide explicit pseudo-logic instead of general instructions:

✅ **Good - Explicit Logic:**
```markdown
### Task 1: Query Customer Data

**Steps** [sequential=true]:
1. Call `verify_database_access` with database name
2. If access is denied, return error message: "Database access denied. Please check permissions."
3. If access is granted, call `list_columns_customer_db` to retrieve schema
4. Validate that required columns exist: ['customer_id', 'revenue', 'last_purchase_date']
5. If columns missing, return error: "Required columns not found: [list missing columns]"
6. If columns exist, call `query_sales_data` with filters:
   - WHERE last_purchase_date >= DATE_SUB(CURRENT_DATE, INTERVAL 365 DAY)
   - AND revenue > 0
7. Return result set in JSON format
```

❌ **Bad - Vague Instructions:**
```markdown
### Task 1: Query Customer Data

Query the customer database and get the data we need.
```

#### 3. Specify Sequential vs. Parallel Execution

```markdown
**Steps** [sequential=true]:
# Tasks must execute in order - each depends on previous

**Steps** [parallel=true]:
# Tasks can execute simultaneously - no dependencies
```

#### 4. Include Sample Output Formats

```markdown
**Output Format**:
\```json
{
  "status": "success",
  "segments": [
    {
      "segment_name": "Champions",
      "customer_count": 1250,
      "avg_revenue": 5200.00,
      "characteristics": {
        "recency_score": 5,
        "frequency_score": 5,
        "monetary_score": 5
      }
    }
  ],
  "total_customers_analyzed": 5000,
  "execution_time_ms": 2341
}
\```
```

---

## Section 9: Tools

Document each tool/function specification.

### Template

```markdown
## Tools

### Tool: `tool_name_in_snake_case`

| Item | Details |
|------|---------|
| **Function Name** | `tool_name_in_snake_case` |
| **Function Description** | [Brief description of what this function does] |
| **Target** | Knowledge Base / Agent / External API |
| **Target Function** | List Columns / Query Data / Search Schema / Custom |

#### Input Format
\```json
{
  "parameter1": "value1",
  "parameter2": "value2"
}
\```

#### Output Format
\```json
{
  "result": "data",
  "status": "success"
}
\```

#### Example Usage
\```
User: "Get customer segments"
Tool Call: query_customer_segments({"min_revenue": 1000})
Tool Response: {"segments": [...], "total": 5}
\```

### Tool: `next_tool_name`

[Follow same structure for each tool]
```

### Tool Target Types

**Knowledge Base Tools:**
- **List Columns**: Retrieve schema information
- **Query Data (Trino SQL)**: Execute SQL queries
- **Search Schema**: Find tables/columns (avoid if possible - can be slow)

**Agent Tools:**
- **Sub-Agent Call**: Invoke another agent and return results
- **Custom Function**: Execute custom Python/JavaScript code

### Best Practices for Tool Documentation
1. **Match names** between system prompt and tool specification exactly
2. **Use snake_case** consistently
3. **Provide examples** of inputs and outputs
4. **Document errors** and how the tool handles them
5. **Specify data types** for all parameters

---

## Section 10: Input/Output Format

Define how users interact with the agent and what they receive.

### Template

```markdown
## Input/Output Format

### Input Format

**Language Request**: [Natural language or structured format]

**Sample Dialogue**:
\```
User: "[Example user query]"
Agent: "[Agent's clarifying question if needed]"
User: "[User's response]"
\```

**Optional Parameters**:
- `parameter_name`: [Description, constraints, default value]
- `another_parameter`: [Description, constraints, default value]

### Output Format

**Output Type**: HTML / Plotly Graph / Markdown / JSON / Summarized Text

**Sample Output**:
[Show representative example of what the user receives]

### Sample Conversation Flow

\```
User: "Analyze my customer segments for Q4 2024"

Agent: "I'll analyze your customer segments. I can use RFM analysis, behavioral clustering, or both. Which would you prefer?"

User: "Both"

Agent: [Executes analysis]

Agent Output:
# Customer Segmentation Analysis - Q4 2024

## RFM Segments
[Table showing segments]

## Behavioral Clusters
[Visualization showing clusters]

## Key Insights
- [Insight 1]
- [Insight 2]
\```
```

### Output Format Options

| Format | Best For | Example |
|--------|----------|---------|
| **HTML** | Structured presentation with formatting | Reports, dashboards, formatted tables |
| **Plotly Graph** | Data visualizations | Charts, graphs, interactive visualizations |
| **Markdown** | Text-heavy content with structure | Analysis summaries, documentation |
| **JSON** | Programmatic consumption | API responses, data pipelines |
| **Summarized Text** | Quick insights | Executive summaries, key findings |

---

## Section 11: User Prompts

User prompts guide the conversation and capture necessary information.

### Template

```markdown
## User Prompt: [Prompt Name]

| Item | Details |
|------|---------|
| **User Prompt Name** | [Descriptive name indicating purpose] |
| **Purpose** | [What this prompt accomplishes] |

### User Prompt Text

\```
Step 1: [First question or instruction]
- Option A: [Description]
- Option B: [Description]
- Option C: [Description]

Step 2: [Next question based on previous answer]
[Continue step-by-step flow]

Step 3: [Final configuration]
[Gather remaining details]
\```

### Advanced Settings

**Pre-Configuration Checklist**:
- [ ] [Configuration item 1]
- [ ] [Configuration item 2]
- [ ] [Configuration item 3]

**System Prompt Override** (if applicable):
[Explain if/when system prompt can be customized by users]

### Sample Conversation

\```
Agent: "Welcome! I can help you with customer segmentation. What would you like to do?
1. Analyze existing segments
2. Create new segments
3. Compare segment performance"

User: "Analyze existing segments"

Agent: "Great! Which time period should I analyze?
- Last 30 days
- Last quarter
- Last year
- Custom date range"

User: "Last quarter"

Agent: "Analyzing your customer segments for Q3 2024..."
[Proceeds with analysis]
\```
```

### User Prompt Best Practices

1. **Step-by-step flow**: Guide users through complex tasks incrementally
2. **Clear options**: Provide specific choices rather than open-ended questions
3. **Context**: Explain what each option does and why they'd choose it
4. **Validation**: Include checks to ensure user input is valid
5. **Defaults**: Suggest sensible defaults for common use cases

---

## Section 12: Development Roadmap

Track the agent's development milestones and future plans.

### Template

```markdown
## Development Roadmap

### Milestones

| Phase | Date | Deliverables | Status |
|-------|------|--------------|--------|
| **Planning** | [Date] | Requirements, architecture design, team formation | ✅ Complete |
| **Development** | [Date] | Core functionality, tools, system prompt | ✅ Complete |
| **Testing** | [Date] | Unit tests, integration tests, user testing | ✅ Complete |
| **Deployment** | [Date] | Production deployment, documentation, training | 🔄 In Progress |
| **Enhancement** | [Date] | Feature additions, optimizations, feedback integration | 📅 Planned |

### Future Enhancements
- [ ] [Planned feature 1]
- [ ] [Planned feature 2]
- [ ] [Planned feature 3]
```

---

## Section 13: Demo

Provide examples and demonstrations of the agent in action.

### Template

```markdown
## Demo

### Input Example

\```
User Query: "[Realistic example user input]"

Context:
- [Relevant context or prerequisites]
\```

### Output Example

\```
[Show exactly what the agent returns]

[Include visualizations, formatted output, or screenshots]
\```

### Video Recording

**Demo Video**: [Link to recording]
**Duration**: [Length]
**Covers**: [What the demo shows]

### Live Demo Access

**Demo Environment**: [Link if available]
**Test Credentials**: [If applicable]
**Sample Data**: [Link to sample data for testing]
```

---

## Complete Documentation Example

Here's a concise example applying all the templates:

```markdown
# Customer RFM Segmentation Agent

## Basic Information

| Item | Details |
|------|---------|
| **Project Name** | Customer RFM Segmentation Agent |
| **Type** | Field Agent |
| **Interface Type** | Chat |
| **Status** | Production |
| **Version** | 1.2.0 |
| **Model** | Claude 4 Sonnet |
| **Temperature** | 0 |

## Purpose & Functionality

### Description
Automatically segments customers using RFM (Recency, Frequency, Monetary) analysis to identify high-value segments and at-risk customers.

### Business Value
Enables 10x faster customer segmentation, improving campaign targeting by 35% and increasing marketing ROI.

## System Prompt: RFM Agent

# Customer RFM Segmentation Agent

Analyzes customer transaction data to create actionable segments.

# Role
- Query customer transaction databases
- Calculate RFM scores for each customer
- Assign customers to segments based on scores
- Generate visualizations and insights

# Goal
Provide marketers with clear customer segments and actionable insights for targeted campaigns.

## Available Tools

### Database Access
**Tool**: `verify_database_access`
**Purpose**: Verify user has access to customer database
**Input**: Database name
**Output**: Access status (granted/denied)

### Data Retrieval
**Tool**: `query_customer_transactions`
**Purpose**: Retrieve customer transaction history
**Input**: Database, table, date range
**Output**: Transaction records with customer_id, date, amount

### RFM Calculation
**Tool**: `calculate_rfm_scores`
**Purpose**: Calculate Recency, Frequency, Monetary scores
**Input**: Transaction data
**Output**: RFM scores per customer

### Visualization
**Tool**: `generate_segment_chart`
**Purpose**: Create Plotly visualization of segments
**Input**: Segment data
**Output**: Plotly JSON chart specification

## Task Flow

### Task 1: Verify Access [required = true, mandatory_start = true]

**Steps** [sequential=true]:
1. Call `verify_database_access` with customer database name
2. If access denied, return error and stop
3. If access granted, proceed to Task 2

### Task 2: Retrieve Transaction Data [required = true]

**Steps** [sequential=true]:
1. Call `query_customer_transactions` with date range (default: last 365 days)
2. Validate minimum 100 records returned
3. If insufficient data, warn user and ask to expand date range
4. Proceed to Task 3

### Task 3: Calculate RFM [required = true]

**Steps** [sequential=true]:
1. Call `calculate_rfm_scores` with transaction data
2. Assign scores 1-5 for Recency (days since last purchase)
3. Assign scores 1-5 for Frequency (number of purchases)
4. Assign scores 1-5 for Monetary (total revenue)
5. Create segments based on score combinations:
   - Champions: RFM 5-5-5
   - Loyal: RFM 4-5-4 or 5-4-5
   - At Risk: RFM 2-3-3 or 3-2-3
   - Lost: RFM 1-1-1
6. Proceed to Task 4

### Task 4: Generate Output [required = true]

**Steps** [parallel=true]:
1. Call `generate_segment_chart` to create visualization
2. Format summary statistics
3. Compile key insights

**Output Format**:
\```json
{
  "segments": [
    {"name": "Champions", "count": 1250, "avg_revenue": 5200},
    {"name": "Loyal", "count": 2100, "avg_revenue": 3100}
  ],
  "chart": { "plotly_json": "..." },
  "insights": ["45% of revenue from Champions (25% of customers)"]
}
\```
```

---

## Best Practices Summary

### Documentation Do's ✅
- Use clear, descriptive tool names in snake_case
- Provide detailed pseudo-logic in system prompts
- Include sample inputs and outputs for every tool
- Keep documentation updated with code changes
- Use semantic versioning
- Include visual examples and demos
- Document error handling explicitly

### Documentation Don'ts ❌
- Don't use vague tool names (verify, list, query)
- Don't write generic system prompts without details
- Don't skip example conversations
- Don't forget to update version numbers
- Don't leave links broken or outdated
- Don't omit dependencies or prerequisites
- Don't publish without demo/video

---

## Quick Reference: Tool Naming

| Purpose | Good Name | Bad Name |
|---------|-----------|----------|
| Verify database access | `verify_database_access` | `verify` |
| List columns from customer DB | `list_columns_customer_db` | `listColumns` |
| Query sales data | `query_sales_data` | `query` |
| Calculate RFM scores | `calculate_rfm_scores` | `calcRFM` |
| Generate visualization | `generate_segment_chart` | `makeChart` |

---

By following this comprehensive documentation template, your Field Agent documentation will be clear, consistent, and professional, making it easy for users to understand, deploy, and use your agents effectively.
