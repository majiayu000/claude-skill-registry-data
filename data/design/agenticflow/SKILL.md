---
name: agenticflow
description: This skill enables you to design, build, and validate AgenticFlow automation workflows from natural language requirements. Use this when users mention AgenticFlow, automation workflows, or want to integrate external services (Gmail, Slack, Shopify, CRM systems, etc.) into automated processes. You can transform user requirements into production-ready workflows with both standard nodes and MCP integrations.
license: Complete terms in LICENSE.txt
---

# AgenticFlow Workflow Builder

## 🎯 When to use this skill

Use this skill when users want to:
- Create automation workflows from natural language descriptions
- Integrate external services (Gmail, Slack, HubSpot, Shopify, Google Sheets, etc.)
- Build AI-powered automation with web scraping, data extraction, or content generation
- Automate business processes across multiple platforms
- Design workflows mixing standard nodes with 2,500+ MCP integrations

**Key Capability:** You can transform natural language like "I need to monitor competitor prices and alert my team on Slack" into a complete, production-ready workflow.

---

## ⚡ Performance Optimization - Use Local Files First!

**CRITICAL:** This skill contains ALL necessary data locally. Minimize API calls to improve performance.

### 📁 Complete Local Data Available

**Node Type Data (139 nodes):**
- `references/official_node_types.json` - Complete API data, ready to parse
- `references/node_types.md` - Human-readable, categorized by function
- `references/complete_node_types.md` - Full schemas with all fields

**Workflow Examples (78 templates):**
- `references/examples/workflows/*.json` - Real production workflows

**Agent Examples (8 templates):**
- `references/examples/agents/*.json` - Pre-built agent configurations

### 🎯 When to Use API vs Local Files

**USE LOCAL FILES (No API call needed):**
- ✅ Browsing available nodes → `references/node_types.md`
- ✅ Getting node field details → `references/complete_node_types.md`
- ✅ Finding similar workflows → `references/examples/workflows/`
- ✅ Understanding MCP actions → `references/mcp_integrations.md`
- ✅ Learning workflow patterns → `references/workflow_guide.md`

**USE API CALLS (Only when required):**
- ⚠️ **Validating workflow → `agenticflow_validate_workflow()` - REQUIRED before creation**
- ⚠️ **Creating workflow → `agenticflow_create_workflow()` - Only after validation passes**
- ⚠️ Health check → `agenticflow_health_check()` - Optional
- ⚠️ Searching nodes → `agenticflow_search_node_types()` - Only if local search insufficient

### 💡 Recommended Workflow

```
User Request
     ↓
Load LOCAL guides & references (NO API calls)
     ↓
Design complete workflow using local data
     ↓
Build workflow JSON structure
     ↓
API CALL 1: agenticflow_validate_workflow() ← REQUIRED validation
     ↓
Validation passed? → Yes → Continue
     ↓ No → Fix errors and validate again
API CALL 2: agenticflow_create_workflow() ← Create after validation
     ↓
Return workflow link to user
```

**Result:** Typically 2 API calls needed (validate + create) - Prevents broken workflows!

---

## 📚 Complete Documentation Structure

This skill provides a comprehensive system for building workflows:

### Core Guides (Start Here)

1. **`guides/01_workflow_creation_process.md`** - Complete 7-phase workflow creation process
   - Health check → Discovery → MCP Integration → Configuration → Pre-building → Building → Validation
   - Step-by-step instructions for each phase
   - Visual workflow diagrams and patterns
   - **Load this first** when user requests a new workflow

2. **`guides/02_node_selection_strategy.md`** - Choose the right nodes for any requirement
   - All 139 nodes organized by use case
   - Decision flow charts
   - Connection requirements and cost considerations
   - Output field reference
   - **Load when** deciding which nodes to use

3. **`guides/03_mcp_integration_guide.md`** - Complete MCP integration reference
   - 2,500+ service integrations
   - Action patterns by category (CRM, Communication, E-commerce, etc.)
   - Hybrid workflow patterns
   - Connection setup instructions
   - **Load when** user mentions external services

4. **`guides/04_technical_requirements.md`** - Field requirements and common fixes
   - Complete node structure requirements
   - Common errors and solutions
   - Template variable syntax
   - Validation checklist
   - **Load when** building or debugging workflows

### Reference Documentation

5. **`references/node_types.md`** - Quick reference for 139 node types
   - Organized by 12 functional categories
   - Descriptions and key fields
   - **Load for** quick node browsing

6. **`references/complete_node_types.md`** - Full API schemas
   - Complete input/output schemas for all nodes
   - Exact field requirements
   - **Load for** detailed field information

7. **`references/mcp_integrations.md`** - MCP service catalog
   - Popular actions by category
   - Integration patterns
   - **Load for** MCP integration details

8. **`references/workflow_guide.md`** - Design patterns and best practices
   - Hybrid workflow patterns
   - Parallel processing
   - Input schema design
   - **Load for** workflow architecture patterns

### Examples

9. **`references/examples/workflows/`** - 78 real workflow templates
   - Content creation, marketing, research, e-commerce, events
   - **Load for** similar workflow examples

10. **`references/examples/agents/`** - 8 pre-built agent templates
    - Social media, sales, e-commerce, SEO, events, design, support, research
    - **Load for** agent configuration examples

---

## 🚀 Quick Start: Natural Language to Workflow

### The 7-Phase Process

Follow this systematic approach for every workflow:

#### Phase 1: Health Check
```javascript
// Only call API if needed (e.g., validating connection or checking workspace)
// Otherwise skip to save API calls - all node data is in local files
agenticflow_health_check() // OPTIONAL - only if validating connection
```

#### Phase 2: Discovery
1. Analyze user's natural language request
2. Ask clarifying questions if needed
3. **Use LOCAL files first** - NO API calls needed:
   - Load `guides/02_node_selection_strategy.md` for node selection
   - Reference `references/node_types.md` for browsing nodes
   - Check `references/examples/workflows/` for similar patterns
4. **Only use API calls** when:
   - Searching for specific node type: `agenticflow_search_node_types()`
   - Need absolute latest node list: `agenticflow_list_node_types()`
   - Creating/validating workflow: Required for these operations

#### Phase 3: MCP Integration Analysis
1. Identify external services mentioned
2. Check if MCP integration needed
3. Load `guides/03_mcp_integration_guide.md` if using MCP
4. Plan action names and instructions

#### Phase 4: Configuration Planning
1. Design data flow between nodes
2. Map template variables
3. Plan input schema with UI metadata
4. Show visual workflow diagram to user

#### Phase 5: Pre-Building
1. Structure complete workflow JSON
2. Validate all required fields
3. Load `guides/04_technical_requirements.md` for validation
4. Document MCP connections needed

#### Phase 6: Building
1. **REQUIRED:** Validate workflow first using `agenticflow_validate_workflow()`
2. **Check validation results** - Fix any errors before proceeding
3. **Only after successful validation:** Create workflow using `agenticflow_create_workflow()`
4. Provide direct workflow URL
5. Include clear setup instructions

**CRITICAL:** Never create a workflow without validating first! This prevents creating broken workflows.

#### Phase 7: Validation & Documentation
1. Validate workflow structure
2. Document MCP setup requirements
3. Provide usage instructions
4. Note limitations and best practices

**Detailed instructions for each phase:** Load `guides/01_workflow_creation_process.md`

---

## 💡 Core Principles

### Think Expansively
AgenticFlow connects to **2,500+ services** through MCP, not just built-in nodes. When users ask about automation:
1. Consider standard nodes AND MCP integrations
2. Design hybrid solutions when needed
3. Never limit yourself to just standard nodes

**Example:**
- User: "Monitor competitor prices and alert team"
- Solution: `web_scraping` → `llm` (analysis) → `SLACK-SEND-MESSAGE` (MCP)

### Hybrid Workflow Design
Mix standard nodes with MCP for powerful automations:
- **Standard nodes** for: AI processing, web scraping, data extraction
- **MCP integrations** for: Gmail, Slack, HubSpot, Shopify, Google Sheets, etc.

### Natural Language First
Transform user requirements directly into workflows:
1. Understand the goal
2. Break into logical steps
3. Select appropriate nodes
4. Connect data flow
5. Build and validate

---

## 🎨 Common Workflow Patterns

### Pattern 1: Data Collection + AI Processing + Distribution
```
Web Scraping → LLM Analysis → Multi-Channel Output
    ↓               ↓                 ↓
  Research    Extract Insights    Email + Slack + Sheets
```

### Pattern 2: External Service Integration
```
MCP Data Source → AI Processing → MCP Action
      ↓                ↓               ↓
  HubSpot CRM    Analyze Leads    Send Campaigns
```

### Pattern 3: Content Generation Pipeline
```
User Input → LLM Generation → Image Creation → Multi-Platform Publishing
               ↓                    ↓                    ↓
         Text Content        Visual Assets     LinkedIn + Twitter + FB
```

**Full patterns with code:** Load `references/workflow_guide.md`

---

## 📖 Resource Loading Strategy

Load documentation strategically based on current phase:

### Planning Phase
1. `guides/01_workflow_creation_process.md` - Overall process
2. `guides/02_node_selection_strategy.md` - Choose nodes
3. `references/node_types.md` - Browse available nodes

### MCP Integration Phase
1. `guides/03_mcp_integration_guide.md` - MCP setup
2. `references/mcp_integrations.md` - Service catalog

### Building Phase
1. `guides/04_technical_requirements.md` - Field requirements
2. `references/complete_node_types.md` - Detailed schemas

### Learning from Examples
1. `references/examples/workflows/` - Similar workflows
2. `references/examples/agents/` - Agent configurations

**Don't load everything at once** - Load based on what you need for the current phase.

---

## 🔧 Key Technical Points

### Node Structure (CRITICAL)
```javascript
{
  "name": "node_name",              // Required: unique string
  "node_type_name": "exact_type",    // Required: exact from API
  "input_config": {},                // Required: object (never null)
  "output_mapping": {},              // Required: {} not null
  "connection": ""                   // Required: "" not null
}
```

### Template Variables
```javascript
{{node_name.content}}              // LLM output
{{node_name.response}}             // Search/API output
{{node_name.scraped_content}}      // Web scraping output
{{node_name.output}}               // MCP action output
{{input_parameter}}                // User input
{{__app_connections__['uuid']}}    // MCP connection
```

### MCP Action Format
```javascript
{
  "node_type_name": "mcp_run_action",
  "input_config": {
    "action": "SERVICE-ACTION-NAME",     // All caps with hyphens
    "input_params": {
      "instruction": "Clear instruction with {{variables}}"
    }
  },
  "connection": "{{__app_connections__['connection-uuid']}}"
}
```

**Complete technical details:** Load `guides/04_technical_requirements.md`

---

## ✅ Workflow Creation Checklist

Use this for every workflow:

**Before Building:**
- [ ] Health check completed (`agenticflow_health_check()`)
- [ ] Requirements fully understood (asked clarifying questions)
- [ ] Node types identified (checked available nodes)
- [ ] MCP services planned (documented which connections needed)
- [ ] Data flow mapped (template variables planned)
- [ ] Input schema designed (with UI metadata)

**During Building:**
- [ ] All required fields included
- [ ] Template variables correct ({{node_name.field}})
- [ ] Connection fields proper format ("" or UUID)
- [ ] No null values (use {} for objects, "" for strings)
- [ ] Node names unique and descriptive

**Before Creating (REQUIRED):**
- [ ] **Validation API called** - `agenticflow_validate_workflow()`
- [ ] **Validation passed** - No errors or warnings
- [ ] **Errors fixed** - If validation failed, fix and re-validate

**After Building:**
- [ ] Workflow created successfully (only after validation)
- [ ] Direct link provided to user
- [ ] MCP setup documented
- [ ] Usage instructions clear
- [ ] Limitations noted

---

## 🎓 Learning Path

### For Simple Workflows (1-3 nodes)
1. Load `guides/01_workflow_creation_process.md`
2. Follow Phases 1-7
3. Reference `guides/02_node_selection_strategy.md` for nodes
4. Check `references/examples/workflows/` for similar examples

### For MCP Workflows (External Services)
1. Load `guides/01_workflow_creation_process.md`
2. Load `guides/03_mcp_integration_guide.md`
3. Review MCP action patterns for the service category
4. Follow connection setup instructions

### For Complex Workflows (5+ nodes)
1. Load `guides/01_workflow_creation_process.md`
2. Load `references/workflow_guide.md` for patterns
3. Design data flow carefully with template variables
4. Use `guides/04_technical_requirements.md` for validation

---

## 🚨 Common Pitfalls to Avoid

1. **Don't use `null`**: Use `{}` for objects, `""` for strings
2. **Exact node type names**: Must match API exactly (case-sensitive)
3. **Template variables**: Use `{{node.field}}` not `${node.field}`
4. **Output fields**: Different nodes have different output fields (.content, .response, .output)
5. **Required fields**: Check `references/complete_node_types.md` for each node type
6. **MCP connections**: Document setup requirements for users

---

## 🎯 Success Criteria

A successful workflow should:
- ✅ Transform user's natural language request into working automation
- ✅ Have all required fields properly configured
- ✅ Use template variables correctly for data flow
- ✅ Include clear setup instructions (especially for MCP)
- ✅ Provide direct workflow link
- ✅ Document any limitations or prerequisites

---

## 📞 Quick Reference

**Most Important Files:**
- `guides/01_workflow_creation_process.md` - THE process
- `guides/02_node_selection_strategy.md` - Choose nodes
- `guides/03_mcp_integration_guide.md` - MCP integrations
- `guides/04_technical_requirements.md` - Field requirements

**Most Useful References:**
- `references/node_types.md` - Node browsing
- `references/complete_node_types.md` - Field details
- `references/examples/workflows/` - Real examples

**Quick Actions:**
- Health check: `agenticflow_health_check()` - OPTIONAL, only if validating connection
- Search nodes: Use `references/node_types.md` first, API search only if needed
- List nodes: Use `references/official_node_types.json` - all 139 nodes locally available
- **Validate workflow: `agenticflow_validate_workflow({...})` - REQUIRED before creation**
- **Create workflow: `agenticflow_create_workflow({...})` - Only after successful validation**

**Data Source Priority:**
1. **LOCAL FIRST** - Use references/* files (saves API calls)
2. **API ONLY WHEN** - Creating, validating, or need latest data

---

## Keywords

AgenticFlow, automation workflows, workflow design, MCP integrations, external services, API automation, workflow validation, workflow building, natural language to workflow, AI automation, Gmail integration, Slack integration, HubSpot integration, Shopify automation, web scraping, data extraction, content generation
