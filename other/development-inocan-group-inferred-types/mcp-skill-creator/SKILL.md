---
name: mcp-skill-creator
description: Meta-skill for creating workflow-optimized skills from MCP servers. Use when users want to create a custom skill that integrates one or more MCP servers into a specialized workflow. The user provides MCP server configurations and describes their work scenario (workflow, preferences, SOPs), and this skill generates a new skill with optimized scripts following Anthropic's MCP + code execution best practices.
---

# MCP-Powered Skill Creator

This meta-skill creates workflow-optimized skills from MCP servers using code execution patterns inspired by [Anthropic's MCP engineering practices](https://www.anthropic.com/engineering/code-execution-with-mcp).

## Core Concept

Transform MCP servers into specialized, personalized workflow skills by:

1. **Progressive Disclosure**: Generate code APIs for MCP tools, loaded on-demand (not all upfront)
2. **Context Efficiency**: Process data in execution environment, minimize token usage
3. **Workflow Optimization**: Combine MCP calls with parallel execution, filtering, control flow
4. **Personalization**: Embed user preferences, SOPs, and domain knowledge into the skill

## When to Use This Skill

Use this skill when a user wants to:
- Create a custom skill from one or more MCP servers
- Optimize a workflow that involves multiple MCP tool calls
- Build reusable automation scripts for specific work scenarios
- Capture personal SOPs and preferences into a skill

## ⚠️ IMPORTANT: Before You Start

**ALWAYS check and install dependencies FIRST before doing anything else:**

```bash
python3 -c "import mcp; print('✓ MCP SDK is installed')" 2>/dev/null || pip3 install mcp --break-system-packages
```

**Automatic Installation Process:**
1. First, check if MCP SDK is installed
2. If not installed, **automatically install it** using `pip3 install mcp --break-system-packages`
3. Verify installation succeeded before continuing
4. Then proceed with skill creation

**DO NOT ask the user to manually install dependencies** - you should handle this automatically as part of the skill creation process.

**Why this matters**: The introspector and generated scripts require the `mcp` package. Installing it upfront ensures a smooth workflow.

## Skill Creation Process

Follow these steps to create an MCP-powered skill. This process combines programmatic MCP infrastructure generation with LLM-driven skill design, following skill-creator principles.

### Overview of Steps

0. **Prerequisites** - Install required dependencies
1. **Gather Input** - Collect MCP servers and workflow description from user
2. **Generate MCP Infrastructure** - Use scripts to introspect servers and create wrappers (programmatic)
3. **Understand the Workflow** - Analyze user's scenario with concrete examples (LLM-driven)
4. **Plan Skill Contents** - Determine what scripts, references, and guidance to include (LLM-driven)
5. **Implement the Skill** - Write workflow scripts and SKILL.md with embedded preferences (LLM-driven)
6. **Package and Deliver** - Create distributable .skill file

### Step 0: Prerequisites (Automatic)

**You should automatically check and install the MCP SDK if needed:**

```bash
python3 -c "import mcp; print('✓ MCP SDK is installed')" 2>/dev/null || pip3 install mcp --break-system-packages
```

**Process:**
1. Check if MCP SDK is already installed
2. If not, install it automatically with `pip3 install mcp --break-system-packages`
3. Verify installation succeeded
4. Inform the user that dependencies have been installed

**Why needed**: The introspector and generated scripts use the `mcp` package to connect to MCP servers.

**DO NOT ask the user to manually install** - handle this automatically as part of the workflow.

### Step 1: Gather Input

Before starting, collect the following from the user:

**MCP Server Configurations** (required):
```json
{
  "mcp_servers": [
    {
      "name": "server-name",
      "command": ["npx", "-y", "@modelcontextprotocol/server-..."]
    }
  ]
}
```

**Workflow Description** (required):
- Clear description of the workflow steps
- Can be numbered list, sequential narrative, or structured steps
- Example: "First I visit the official website, then check ProductHunt, then search Twitter/Reddit, finally generate a report"

**User Preferences** (optional):
- How they like to work
- What data they prioritize
- Quality standards
- Example: "I prefer quantitative metrics over qualitative descriptions"

**Standard Operating Procedures** (optional):
- Company-specific practices
- Domain knowledge
- Best practices
- Example: "Always verify information from at least 3 sources"

If user provides a single configuration file, parse it to extract these components.

### Step 2: Generate MCP Infrastructure (Programmatic)

This step generates the MCP client infrastructure and tool discovery utilities.

#### 2.1 Introspect MCP Servers

Use `scripts/mcp_introspector.py` to discover available tools:

```bash
# Create MCP config file in skill directory
echo '{
  "servers": [
    {
      "name": "filesystem",
      "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  ]
}' > <skill-dir>/mcp_config.json

# Run introspection
python scripts/mcp_introspector.py <skill-dir>/mcp_config.json introspection.json
```

This produces a JSON file with all available tools, their parameters, and descriptions.

#### 2.2 Generate MCP Client and Tool Discovery

Use `scripts/generate_mcp_wrappers.py` to create the infrastructure:

```bash
python scripts/generate_mcp_wrappers.py introspection.json <skill-dir>
```

This creates:
- `scripts/mcp_client.py` - **Working** MCP client with proper connection management
- `scripts/list_mcp_tools.py` - **Dynamic tool discovery** (Progressive Disclosure)
- `scripts/tools/<server>/` - (Optional) Type-safe wrappers for each tool

**Generated structure**:
```
<skill-dir>/
├── mcp_config.json           # Server configuration
├── scripts/
│   ├── mcp_client.py         # ✅ Working implementation
│   ├── list_mcp_tools.py     # 🆕 View tool docs on-demand
│   └── workflows/            # (You'll create these)
│       └── your_workflow.py
```

#### 2.3 How to View MCP Tool Documentation

**Progressive Disclosure** means tools are discovered on-demand, not pre-loaded. Three ways to view docs:

1. **Dynamic Query** (Recommended):
   ```bash
   cd <skill-dir>/scripts
   python list_mcp_tools.py
   ```
   Shows all available tools with parameters and descriptions.

2. **Generate Static Reference**:
   ```bash
   python list_mcp_tools.py > references/mcp_tools_reference.txt
   ```
   Save for offline reference.

3. **In SKILL.md**:
   List only the most commonly used tools, full docs available via method 1 or 2.

**Key Insight**: You don't need wrapper files for each tool. Just use `call_mcp_tool()` directly:
```python
from mcp_client import call_mcp_tool

result = await call_mcp_tool('filesystem', 'search_files', {
    'path': '/path',
    'pattern': 'myfile'
})
```

### Step 3: Understand the Workflow (LLM-Driven)

Now analyze the user's workflow description to understand what this skill needs to accomplish. Similar to skill-creator's Step 1.

**Ask clarifying questions if needed**:
- "What specific data sources do you use?"
- "How do you handle cases where data is missing?"
- "What does the final output look like?"
- "Are there any steps that must happen sequentially vs in parallel?"

**Identify workflow characteristics**:
- Which steps are data fetching operations (candidates for parallelization)
- Which steps are data processing (candidates for execution environment filtering)
- Which steps have complex control flow (loops, conditionals, polling)
- What intermediate state needs to be preserved

**Example Analysis**:

User says: "I research products by checking the official site, ProductHunt, Twitter, and Reddit, then create a report"

Analysis:
- 4 data fetch operations (parallel opportunity)
- 1 aggregation step (data filtering opportunity)
- 1 output generation (report creation)
- Sequential dependency: Fetch all → Aggregate → Generate report

### Step 4: Plan Skill Contents (LLM-Driven)

Based on the workflow analysis, determine what to include in the skill. Follow skill-creator principles.

#### 4.1 Decide on Scripts vs Guidance

**Create scripts when**:
- Same code would be rewritten repeatedly
- Complex workflow with multiple MCP calls
- Parallel execution can improve performance
- Data filtering reduces context usage significantly
- Polling/monitoring patterns

**Use text guidance when**:
- Workflow varies significantly each time
- Simple single-tool operations
- User needs flexibility in approach
- Context helps more than code

#### 4.2 Plan Script Structure

For each workflow script to create, determine:

**Script purpose**: What part of the workflow does it handle?

**MCP tools needed**: Which tools from which servers?

**Optimization patterns**: 
- Parallel execution: `asyncio.gather()` for independent fetches
- Data filtering: Process in execution environment before returning
- Control flow: Loops, conditionals, error handling
- State persistence: Save intermediate results to filesystem

**Parameters**: What inputs does the script need?

**Output**: What does it return? (Prefer summaries over full data)

#### 4.3 Plan SKILL.md Structure

Determine what goes in SKILL.md:

**Essential**:
- Workflow overview (user's mental model)
- When to use each script
- User preferences (embedded as guidance)
- SOPs (embedded as procedural instructions)
- Available MCP tools (reference, not full docs)

**Optional references/**:
- Detailed MCP tool catalog
- Complex schemas or API documentation  
- Additional examples
- Troubleshooting guides

### Step 5: Implement the Skill (LLM-Driven)

Now create the actual skill files. This is where you write code and documentation.

#### 5.1 Write Workflow Scripts

For each planned script, create `scripts/workflows/<script_name>.py`:

**Follow these patterns from Anthropic's MCP best practices**:

**Pattern 1: Parallel Fetch + Aggregate**
```python
async def research_pipeline(product_url: str, product_name: str) -> dict:
    """Complete research workflow with parallel data gathering"""
    
    # Parallel fetch from multiple sources
    official_task = google_devtools.fetch_page(product_url)
    twitter_task = x_com.search_tweets(f'"{product_name}"')
    reddit_task = reddit.search_discussions(product_name)
    
    # Execute concurrently (3x faster than sequential)
    official, twitter, reddit = await asyncio.gather(
        official_task, twitter_task, reddit_task
    )
    
    # Filter and aggregate in execution environment
    # (keeps raw data out of context)
    key_features = extract_features(official, top_n=10)
    sentiment = analyze_sentiment([twitter, reddit])
    highlights = extract_highlights(twitter + reddit, top_n=5)
    
    # Return summary (not full data)
    return {
        'key_features': key_features,
        'sentiment': sentiment,
        'highlights': highlights,
        'source_count': len(twitter) + len(reddit)
    }
```

**Pattern 2: Polling/Monitoring**
```python
async def wait_for_deployment(channel: str, keyword: str, timeout: int = 300):
    """Poll Slack channel for deployment completion"""
    start = time.time()
    
    while time.time() - start < timeout:
        messages = await slack.get_channel_history(channel, limit=10)
        
        if any(keyword in m['text'].lower() for m in messages):
            return {'status': 'complete', 'message': messages[0]}
        
        await asyncio.sleep(10)
    
    return {'status': 'timeout'}
```

**Pattern 3: Bulk Processing**
```python
async def sync_contacts(sheet_id: str, crm_object: str):
    """Sync contacts from sheet to CRM (privacy-preserving)"""
    
    # Load data once
    contacts = await google_sheets.get_sheet(sheet_id)
    
    # Filter in execution environment (not in context)
    valid = [c for c in contacts if validate_email(c['email'])]
    
    # Batch update (PII never enters model context)
    results = []
    for batch in chunked(valid, batch_size=50):
        batch_results = await asyncio.gather(*[
            crm.update_record(crm_object, contact)
            for contact in batch
        ])
        results.extend(batch_results)
    
    # Return summary only
    return {
        'processed': len(valid),
        'successful': sum(1 for r in results if r['success'])
    }
```

**Key Principles for Scripts**:
- Use `async`/`await` for IO-bound MCP calls
- Combine related operations into single scripts
- Filter/aggregate data before returning to model
- Return summaries, not raw data
- Include type hints and docstrings
- Add helper functions for data processing

#### 5.2 Write SKILL.md

Create the SKILL.md following skill-creator structure, with MCP-specific additions.

**YAML Frontmatter**:
```yaml
---
name: <skill-name>
description: <Brief description of workflow + when to use + MCP servers involved>
---
```

**Body Structure**:

```markdown
# [Skill Name]

[Overview of what this skill does]

## Prerequisites

This skill requires the MCP SDK. **The scripts will automatically check and install it if needed.**

If you want to manually verify or install:

```bash
python3 -c "import mcp; print('✓ MCP SDK ready!')" 2>/dev/null || pip3 install mcp --break-system-packages
```

**Why needed**: This skill uses MCP tools to [brief explanation of what MCP servers do]. The workflow scripts require the `mcp` package to connect to MCP servers.

**Note**: When you run any workflow script, it will automatically check for MCP SDK and display a helpful error message if not installed.

## Workflow Overview

[User's workflow steps in their own language]

[USER PREFERENCES - Embedded as guidance]
When using this skill:
- [Preference 1]
- [Preference 2]

[SOPs - Embedded as procedural instructions]
Standard procedure:
1. [SOP step 1]
2. [SOP step 2]

## Quick Start

**Before running workflows, ensure MCP SDK is installed** (see Prerequisites above).

[Simple example of using the main workflow script]

## Available Workflows

### [Primary Workflow Script]

**Use when**: [Scenario]

**Location**: `scripts/workflows/<script>.py`

**Usage**:
```python
from scripts.workflows import workflow_name
result = await workflow_name(params)
```

**Optimizations**:
- Parallel execution of [X] data sources
- Context-efficient data filtering  
- [Other optimizations]

[Repeat for other workflow scripts]

## MCP Tools Available

[Brief overview of integrated MCP servers]

### [Server Name]

**Tools**: [Count] available

**Location**: `scripts/tools/[server]/`

**Key tools**: [List 3-5 most relevant]

**Discovery**: Use `ls scripts/tools/[server]/` to see all tools

[Repeat for each server]

## Advanced Usage

[Guidance on combining scripts, customization, etc.]

## Performance Notes

[Context optimization benefits, speedups from parallelization]
```

**Critical**: Embed user preferences and SOPs directly into the workflow guidance, not as separate sections. They should inform HOW to use the skill.

**Example of embedded preferences**:
```markdown
## Workflow Overview

This skill automates product research with the following steps:

1. Official website analysis
2. Community feedback gathering
3. Report generation

**Research approach**: Always prioritize quantitative metrics (user counts, ratings) over qualitative descriptions. Recent information (last 6 months) is valued over older reviews. Cross-reference official claims against community feedback to identify contradictions.
```

#### 5.3 Create References (If Needed)

Only create `references/` files if SKILL.md would exceed 500 lines or if there's detailed reference material that doesn't belong in the main workflow.

Possible reference files:
- `references/mcp_tools.md` - Detailed catalog of all MCP tools
- `references/schemas.md` - Data schemas for APIs
- `references/examples.md` - Additional usage examples

### Step 6: Package and Deliver

Once the skill is complete:

1. **Review the skill structure**
   - SKILL.md is clear and under 500 lines
   - Scripts are tested (or marked as TODO)
   - User preferences are embedded
   - MCP tool wrappers are generated

2. **Package the skill**
   ```bash
   python /mnt/skills/public/skill-creator/scripts/package_skill.py <skill-dir>
   ```

3. **Provide to user**
   - Share the .skill file
   - Explain key workflows
   - Highlight personalized aspects (preferences, SOPs)

## Key Differences from Standard Skill-Creator

This meta-skill extends skill-creator with MCP-specific capabilities:

### 1. MCP Infrastructure (Unique)

**Standard skill-creator**: You manually write scripts or provide instructions

**MCP skill-creator**: Programmatically generates type-safe tool wrappers from MCP servers, enabling progressive disclosure

### 2. Optimization Focus

**Standard skill-creator**: General workflow guidance

**MCP skill-creator**: Specific optimization patterns (parallel execution, data filtering, control flow, privacy)

### 3. Personalization Depth

**Standard skill-creator**: Domain knowledge in references/

**MCP skill-creator**: User preferences and SOPs embedded directly into workflow guidance

## Best Practices

### When to Create Scripts vs Text Guidance

**Create scripts for**:
- End-to-end workflows with 3+ steps
- Operations that benefit from parallelization
- Data processing that should happen in execution environment
- Polling/monitoring patterns
- Bulk operations

**Use text guidance for**:
- Ad-hoc tool usage
- Workflows with high variability
- Simple single-tool operations
- Exploratory tasks

### Embedding User Preferences

❌ **Don't**: Create separate "User Preferences" section
✅ **Do**: Weave preferences into workflow guidance

Example:
```markdown
## Workflow Overview

This skill follows your research methodology:
1. Start with official sources (per your SOP)
2. Gather community feedback in parallel
3. Cross-reference claims (highlighting contradictions as you prefer)
4. Generate report with quantitative metrics emphasized
```

### Optimization Patterns

Always consider these opportunities when analyzing workflows:

**Parallel Execution**: Any independent fetch operations
**Data Filtering**: Processing that reduces data size
**Control Flow**: Loops, conditionals, error handling  
**State Persistence**: Long-running or resumable workflows
**Privacy**: Sensitive data that shouldn't enter context

## Example: Product Research Skill

**User Input**:
```
MCP Servers: puppeteer, twitter, reddit
Workflow: Research products by visiting official site, checking ProductHunt, 
          searching Twitter/Reddit, then creating markdown report
Preferences: Quantitative metrics > qualitative, recent info > old
SOPs: Start with official sources, cross-reference claims, cite sources
```

**Generated Skill**:

`SKILL.md`:
```markdown
---
name: product-research-workflow  
description: Automated product research integrating official sources and community platforms
---

# Product Research Workflow

Research internet products efficiently by gathering data from official sources 
and community platforms, with emphasis on quantitative metrics and recent information.

## Workflow Overview

This skill implements your standard research process:

1. **Official Source Analysis**: Visit product website and extract key features, 
   pricing, and positioning (per your SOP: always start with official sources)

2. **Community Intelligence**: Gather feedback from ProductHunt, Twitter, and Reddit 
   in parallel (optimized for speed)

3. **Cross-Reference**: Identify contradictions between official claims and community 
   feedback (your preference for critical analysis)

4. **Report Generation**: Create comprehensive markdown report with quantitative 
   metrics emphasized (ratings, user counts, pricing comparisons)

## Quick Start

```python
from scripts.workflows import product_research_pipeline

report = await product_research_pipeline(
    product_url='https://example.com',
    product_name='ExampleApp'
)
```

## Available Workflows

### product_research_pipeline

**Use when**: Researching any new internet product or SaaS tool

**Optimizations**:
- 3x faster via parallel social media gathering
- Context-efficient: processes 1000s of posts, returns top 10 insights
- Recent info prioritized (last 6 months)

[... rest of SKILL.md with embedded preferences and SOPs ...]
```

`scripts/workflows/product_research_pipeline.py`:
```python
async def product_research_pipeline(product_url: str, product_name: str):
    # Official source
    official = await puppeteer.fetch_page(product_url)
    
    # Parallel community research (3x faster)
    twitter, reddit, ph = await asyncio.gather(
        twitter_mcp.search_tweets(f'"{product_name}"', recent_days=180),
        reddit_mcp.search(product_name, time_filter='6months'),
        producthunt_mcp.get_product(product_name)
    )
    
    # Filter in execution env (user preference: quantitative focus)
    metrics = extract_quantitative_metrics(official)
    sentiment = calculate_sentiment_score([twitter, reddit, ph])
    recent_feedback = filter_recent(twitter + reddit, days=180)
    contradictions = find_contradictions(official, recent_feedback)
    
    # Return summary (not raw data)
    return {
        'official_metrics': metrics,
        'sentiment_score': sentiment,
        'recent_mention_count': len(recent_feedback),
        'contradictions': contradictions[:5],
        'top_praise': extract_top_feedback(recent_feedback, 'positive', 3),
        'top_complaints': extract_top_feedback(recent_feedback, 'negative', 3)
    }
```

## References

For detailed MCP optimization patterns and examples:
- `references/mcp-best-practices.md` - Comprehensive guide to MCP + code execution
- `references/quick-start.md` - Step-by-step tutorial
- `references/example-config.json` - Complete configuration example
