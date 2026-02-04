---
name: new-workflow
description: Generate production-ready Workscript workflow JSON files for the Workscript Agentic Workflow Engine with built-in defensive guards and complexity detection. Use when asked to create workflows, automations, data pipelines, or generate workflow JSON. IMPORTANT - For complex requests that would result in deeply nested or overly complex workflows, this skill will STOP and suggest developing new custom nodes first using /new-node, then return to create a simpler, more linear workflow. All generated workflows include data validation (validateData node) for structured JSON outputs, input guards, array length checks, and error handling edges. Fetches up-to-date node documentation from the Reflection API when available. Outputs validated .json files to the sandbox prompts folder. Also suitable for Claude Code subagents needing to compose workflows programmatically.
---

# Workscript Workflow Generator

Generate valid, production-ready workflow JSON files for the Workscript Agentic Workflow Engine.

**Every workflow MUST include defensive guards to prevent runtime errors.** See [Defensive Guards & Validation](#defensive-guards--validation) section.

## Workflow Generation Process

### Step 1: Understand Requirements

Ask clarifying questions to understand:
- What should this workflow accomplish?
- What is the input data structure?
- What are the expected outputs/side effects?
- Are there error handling requirements?
- Will it need loops, conditionals, or API calls?
- **Does the workflow use AI for structured output?** (Requires JSON validation)
- **Is the input from external sources?** (Requires input validation)
- **Is this domain-specific logic that might be reused?** (May warrant a custom node)

### Step 2: Fetch Node Documentation

**If API server is running**, fetch the compact node manifest:

```bash
curl -s http://localhost:3013/workscript/reflection/manifest/compact | jq .
```

**If API is not running**, start the dev server:

```bash
cd /Users/narcisbrindusescu/teste/workscript && bun run dev
```

Wait for the server to start, then retry the manifest fetch.

**Alternatively**, use the offline reference: [references/node-quick-reference.md](references/node-quick-reference.md)

### Step 2.5: Complexity Assessment (CRITICAL)

**Before designing the workflow, assess if it can be built with existing nodes OR if new nodes should be developed first.**

#### Complexity Red Flags

Stop and consider node development if ANY of these apply:

| Red Flag | Threshold | Example |
|----------|-----------|---------|
| **Nesting depth** | > 3 levels of conditional edges | Validation → Branch → Nested branch → Another branch |
| **Repeated patterns** | Same 3+ node sequence appears twice | Filter → Transform → Validate repeated for different fields |
| **Multi-step atomic operation** | 4+ nodes for one conceptual step | Parse HTML → Extract elements → Filter tags → Build object |
| **Missing domain abstraction** | No node covers the core domain logic | Workflow for "invoice processing" but no invoice-specific node |
| **State juggling** | 5+ state keys for intermediate values | `$.temp1`, `$.parsed`, `$.validated`, `$.mapped`, `$.final` |
| **Workaround patterns** | Using `ask-ai` to avoid building proper logic | "Use AI to determine the category" when rules would suffice |

#### Complexity Assessment Questions

Ask yourself:

1. **Can I describe each workflow step in 1-2 words?**
   - ✅ "Filter active" → "Sort by date" → "Send email" (Simple)
   - ❌ "Parse and extract nested JSON, validate structure, map fields, handle arrays" (Complex - needs a node)

2. **Would a domain expert understand the workflow at a glance?**
   - ✅ User sees: `validateInvoice` → `calculateTax` → `generatePDF`
   - ❌ User sees: 15 nodes doing string manipulation and math

3. **Am I repeating logic that should be encapsulated?**
   - ✅ One `dateTime` node handles all date formatting
   - ❌ Multiple `stringOperations` + `math` + `logic` to achieve the same

4. **Is the workflow solving a generic or specific problem?**
   - Generic (reusable) → Build workflow
   - Specific domain logic → Consider a node

#### When to Pivot to Node Development

**STOP generating the workflow and suggest node development when:**

```
Complexity Score = (nesting_depth × 2) + repeated_patterns + (nodes_for_one_concept - 1) + workarounds

If Complexity Score ≥ 6 → Suggest new node(s)
```

**Example calculation:**
- 4 levels of nesting (4 × 2 = 8)
- 1 repeated pattern (1)
- 5 nodes for "parse invoice" (5 - 1 = 4)
- 1 workaround using AI (1)
- **Total: 14** → Definitely needs new node(s)

#### Node Suggestion Template

When complexity threshold is exceeded, respond with:

---

**⚠️ Complexity Alert: This workflow would be too complex to maintain.**

Based on your requirements, I recommend developing **new node(s)** first:

| Suggested Node | Purpose | Would Replace |
|----------------|---------|---------------|
| `parseInvoice` | Extract invoice data from various formats | 5 nodes (filter + jsonExtract + validate + transform + editFields) |
| `calculateLineItems` | Compute totals, tax, discounts | 4 nodes (loop + math + aggregate + editFields) |

**Benefits of building these nodes:**
1. Workflow becomes **3 nodes instead of 15**
2. Each node is **testable in isolation**
3. Logic is **reusable** across workflows
4. Domain concepts are **explicit** (not buried in JSON config)

**Next steps:**
1. Run `/new-node` to create `parseInvoice` node
2. Run `/new-node` to create `calculateLineItems` node
3. Return here to generate the simplified workflow

Would you like me to proceed with node development first?

---

#### Simplified Workflow Vision

Always show what the workflow WOULD look like with the suggested nodes:

```json
{
  "id": "invoice-processor",
  "name": "Invoice Processor",
  "version": "1.0.0",
  "workflow": [
    { "parseInvoice": { "source": "$.rawData", "format": "auto" } },
    { "calculateLineItems": { "items": "$.invoiceData.lines" } },
    { "generatePDF": { "template": "invoice-template", "data": "$.processedInvoice" } }
  ]
}
```

**Compare to what it would be WITHOUT the new nodes:** (show the 15-node monstrosity briefly)

This contrast helps the user understand the value of investing in node development.

### Step 3: Design Workflow Structure

Based on requirements, identify:
1. **Entry point node(s)** - First node(s) to execute
2. **Data flow** - How data moves through nodes
3. **Branching points** - Where edges are needed (conditionals, error handling)
4. **Sequential steps** - Nodes that should run one after another (use workflow array)
5. **State keys** - What to read (`$.key`) and write
6. **Loop requirements** - Use `nodeType...` suffix for loops

Use patterns from [references/patterns.md](references/patterns.md) as templates.

### Step 4: Generate Valid JSON - FLAT BY DEFAULT

**CRITICAL: Prefer flat, linear workflows. Use edges only for actual branching.**

The workflow array supports sequential execution - nodes run one after another automatically. Reserve edges for:
- **Conditional branching**: `true?`/`false?`, `valid?`/`invalid?`, `found?`/`not_found?`
- **Error handling**: `error?` edges
- **Loop control**: `continue?`/`exit?` with `nodeType...`
- **Multi-way routing**: `switch` node dynamic edges

#### WRONG - Excessive Nesting (Anti-Pattern)

```json
{
  "workflow": [
    {
      "googleConnect": {
        "email": "$.email",
        "success?": {
          "listEmails": {
            "maxResults": 10,
            "success?": {
              "ask-ai": {
                "userPrompt": "Analyze...",
                "success?": {
                  "resource-write": {
                    "content": "$.aiResponse",
                    "created?": {
                      "log": { "message": "Done" }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

**Problems:**
- 5+ levels of nesting
- Hard to read and maintain
- `success?` edges don't add value when next step is unconditional

#### CORRECT - Flat Sequential (Preferred)

```json
{
  "workflow": [
    {
      "googleConnect": {
        "email": "$.email",
        "error?": { "log": { "message": "Connection failed: {{$.error}}" } }
      }
    },
    {
      "listEmails": {
        "maxResults": 10,
        "no_results?": { "log": { "message": "No emails found" } },
        "error?": { "log": { "message": "Failed: {{$.error}}" } }
      }
    },
    {
      "ask-ai": {
        "userPrompt": "Analyze...",
        "error?": { "log": { "message": "AI failed: {{$.error}}" } }
      }
    },
    {
      "resource-write": {
        "content": "$.aiResponse",
        "created?": { "log": { "message": "Created: {{$.writtenResourceId}}" } },
        "updated?": { "log": { "message": "Updated: {{$.writtenResourceId}}" } },
        "error?": { "log": { "message": "Write failed: {{$.error}}" } }
      }
    }
  ]
}
```

**Benefits:**
- Linear, easy to read
- Each node handles its own edge cases
- Sequential flow is implicit

#### WHEN TO USE EDGES FOR CHAINING

Use edges for **actual branching** - when different paths lead to different outcomes:

```json
{
  "workflow": [
    {
      "logic": {
        "operation": "equal",
        "values": ["$.user.role", "admin"],
        "true?": {
          "editFields": {
            "fieldsToSet": [{ "name": "access", "value": "full", "type": "string" }]
          }
        },
        "false?": {
          "editFields": {
            "fieldsToSet": [{ "name": "access", "value": "limited", "type": "string" }]
          }
        }
      }
    },
    {
      "log": { "message": "User {{$.user.name}} has {{$.access}} access" }
    }
  ]
}
```

Here `true?`/`false?` are meaningful branches - they execute different logic.

### Step 4.5: Add Defensive Guards

**Before finalizing, add guards for:**

1. **Input validation at entry point:**
   ```json
   {
     "validateData": {
       "validationType": "required_fields",
       "data": "$.input",
       "requiredFields": ["requiredField1", "requiredField2"],
       "invalid?": { "log": { "message": "Missing required input: {{$.validationErrors}}" } }
     }
   }
   ```

2. **AI response JSON validation** (if using `ask-ai` for structured data):
   ```json
   {
     "validateData": {
       "validationType": "json",
       "data": "$.aiResponse",
       "valid?": { ... },
       "invalid?": { "log": { "message": "AI did not return valid JSON" } }
     }
   }
   ```

3. **Array guards before loops** (if processing arrays):
   ```json
   {
     "logic": {
       "operation": "greater",
       "values": ["$.items.length", 0],
       "true?": { ... },
       "false?": { "log": { "message": "No items to process" } }
     }
   }
   ```

4. **Error edges on all nodes that can fail:**
   ```json
   {
     "nodeType": {
       "config": "...",
       "error?": { "log": { "message": "Operation failed: {{$.error}}" } }
     }
   }
   ```

See [Defensive Guards & Validation](#defensive-guards--validation) for complete patterns.

### Step 5: Validate Workflow

Run the validation script before saving:

```bash
bun /Users/narcisbrindusescu/teste/workscript/.claude/skills/new-workflow/scripts/validate-workflow.ts <workflow.json>
```

The script checks:
- JSON Schema compliance (required fields, patterns)
- Node type existence (all nodeTypes must be registered)
- State setter syntax validity (`$.path` format)
- Edge name format

Exit codes: `0` = valid, `1` = schema errors, `2` = semantic errors

### Step 6: Save to Output Folder

Save validated workflow to:
```
/Users/narcisbrindusescu/teste/workscript/apps/sandbox/resources/shared/prompts/<kebab-case-name>.json
```

**File naming:**
- Use kebab-case matching workflow id
- Examples: `user-registration.json`, `data-pipeline.json`, `email-processor.json`

## Workflow Structure Guidelines

### Flat vs Nested Decision Matrix

| Scenario | Use Flat (Workflow Array) | Use Edges (Nesting) |
|----------|---------------------------|---------------------|
| Sequential operations | YES | NO |
| Error handling only | YES (with `error?` edge) | NO |
| Conditional logic (`if/else`) | NO | YES (`true?`/`false?`) |
| Validation branching | NO | YES (`valid?`/`invalid?`) |
| Database lookup | NO | YES (`found?`/`not_found?`) |
| Switch/routing | NO | YES (dynamic edges) |
| Loops | NO | YES (`continue?`/`exit?`) |

### Template: Flat Sequential Workflow

```json
{
  "id": "kebab-case-id",
  "name": "Human Readable Name",
  "version": "1.0.0",
  "description": "Optional description",
  "initialState": { ... },
  "workflow": [
    { "node1": { "config": "...", "error?": { "log": {...} } } },
    { "node2": { "config": "...", "error?": { "log": {...} } } },
    { "node3": { "config": "..." } }
  ]
}
```

### Template: Branching Workflow

```json
{
  "id": "kebab-case-id",
  "name": "Human Readable Name",
  "version": "1.0.0",
  "initialState": { ... },
  "workflow": [
    {
      "logic": {
        "operation": "equal",
        "values": ["$.condition", true],
        "true?": { "node-for-true": { ... } },
        "false?": { "node-for-false": { ... } }
      }
    },
    { "final-node": { "message": "After branch" } }
  ]
}
```

## API Integration

### Reflection API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/workscript/reflection/manifest` | GET | Full AI manifest with complete documentation |
| `/workscript/reflection/manifest/compact` | GET | Token-optimized manifest (~5000 tokens) |
| `/workscript/reflection/manifest/custom` | POST | Filtered manifest for specific use cases |
| `/workscript/reflection/nodes` | GET | List all nodes with introspection data |
| `/workscript/reflection/nodes/:nodeId` | GET | Complete introspection for specific node |
| `/workscript/reflection/patterns` | GET | Browse workflow patterns library |

### Checking API Status

```bash
curl -s http://localhost:3013/health
```

### Starting Dev Server

```bash
cd /Users/narcisbrindusescu/teste/workscript && bun run dev
```

The API will be available at `http://localhost:3013`.

## Output Requirements

| Requirement | Value |
|-------------|-------|
| Output folder | `/apps/sandbox/resources/shared/prompts/` |
| File extension | `.json` |
| Naming convention | kebab-case (e.g., `my-workflow.json`) |
| Validation | Required before save |
| Schema version | Must be `X.Y.Z` format (e.g., `1.0.0`) |

## Quick Reference

### Required Workflow Fields

| Field | Type | Pattern | Required |
|-------|------|---------|----------|
| `id` | string | `/^[a-zA-Z0-9_-]+$/` | YES |
| `name` | string | min 1 char | YES |
| `version` | string | `/^\d+\.\d+\.\d+$/` | YES |
| `workflow` | array | min 1 item | YES |
| `description` | string | - | no |
| `initialState` | object | - | no |

### Edge Route Types

| Type | Example | Description |
|------|---------|-------------|
| Inline object | `"error?": { "log": {...} }` | Execute next node |
| Array | `"true?": [{ "$.x": 1 }, { "log": {...} }]` | Execute sequence |
| Null | `"false?": null` | End execution / exit loop |

### State Syntax

| Syntax | Purpose | Example |
|--------|---------|---------|
| `$.key` | Full reference (preserves type) | `"items": "$.data"` |
| `{{$.key}}` | Template interpolation (string) | `"message": "Hello {{$.name}}"` |
| `{ "$.path": value }` | State setter | `{ "$.counter": 0 }` |

### Common Edge Names

| Node Type | Edges |
|-----------|-------|
| `math`, `sort`, `editFields` | `success?`, `error?` |
| `logic` | `true?`, `false?`, `error?` |
| `filter` | `passed?`, `filtered?`, `error?` |
| `validateData` | `valid?`, `invalid?`, `error?` |
| `database` | `success?`, `found?`, `not_found?`, `error?` |
| `filesystem` | `success?`, `exists?`, `not_exists?`, `error?` |
| `switch` | `<dynamic>?`, `default?`, `error?` |

## Defensive Guards & Validation

**CRITICAL: All generated workflows MUST include defensive guards to prevent runtime errors.**

### Guard Types

| Guard Type | Node | When to Use |
|------------|------|-------------|
| Input Validation | `validateData` | Before processing user/external input |
| Array Length Check | `logic` | Before iteration or array access |
| Required Fields | `validateData` | Before accessing nested properties |
| JSON Structure | `validateData` | When AI output must be structured JSON |
| Type Check | `validateData` | Before type-sensitive operations |

### Pattern 1: Validate Input Before Processing

Always validate external/user input at workflow entry:

```json
{
  "workflow": [
    {
      "validateData": {
        "validationType": "required_fields",
        "data": "$.input",
        "requiredFields": ["userId", "action"],
        "invalid?": {
          "log": { "message": "Missing required input: {{$.validationErrors}}" }
        },
        "error?": {
          "log": { "message": "Input validation failed: {{$.error}}" }
        }
      }
    },
    {
      "log": { "message": "Processing valid input for user {{$.input.userId}}" }
    }
  ]
}
```

### Pattern 2: Array Length Guard Before Iteration

Check array exists and has items before looping:

```json
{
  "workflow": [
    {
      "logic": {
        "operation": "and",
        "values": [
          { "operation": "greater", "values": ["$.items.length", 0] }
        ],
        "true?": {
          "logic...": {
            "operation": "less",
            "values": ["$.index", "$.items.length"],
            "true?": [
              { "log": { "message": "Processing item {{$.index}}" } },
              { "$.index": "$.index + 1" }
            ],
            "false?": null
          }
        },
        "false?": {
          "log": { "message": "No items to process" }
        }
      }
    }
  ]
}
```

### Pattern 3: Validate AI Response as Structured JSON

**ALWAYS validate AI output when expecting JSON structure:**

```json
{
  "workflow": [
    {
      "ask-ai": {
        "userPrompt": "Extract entities as JSON: {{$.text}}",
        "model": "openai/gpt-4o-mini",
        "systemPrompt": "Return ONLY valid JSON: {\"entities\": [{\"name\": string, \"type\": string}]}",
        "error?": {
          "editFields": {
            "fieldsToSet": [{ "name": "aiError", "value": "$.error", "type": "string" }]
          }
        }
      }
    },
    {
      "validateData": {
        "validationType": "json",
        "data": "$.aiResponse",
        "valid?": {
          "validateData": {
            "validationType": "required_fields",
            "data": "$.parsedJson",
            "requiredFields": ["entities"],
            "valid?": {
              "log": { "message": "AI returned valid structure with {{$.parsedJson.entities.length}} entities" }
            },
            "invalid?": {
              "log": { "message": "AI response missing required fields: {{$.validationErrors}}" }
            }
          }
        },
        "invalid?": {
          "log": { "message": "AI did not return valid JSON: {{$.validationErrors}}" }
        }
      }
    }
  ]
}
```

### Pattern 4: Type Safety Before Operations

Validate types before type-sensitive operations:

```json
{
  "workflow": [
    {
      "validateData": {
        "validationType": "type_check",
        "data": "$.data",
        "typeChecks": [
          { "field": "amount", "expectedType": "number" },
          { "field": "items", "expectedType": "array" },
          { "field": "metadata", "expectedType": "object" }
        ],
        "valid?": {
          "math": {
            "operation": "multiply",
            "values": ["$.data.amount", 1.1]
          }
        },
        "invalid?": {
          "log": { "message": "Type validation failed: {{$.validationErrors}}" }
        }
      }
    }
  ]
}
```

### Pattern 5: Comprehensive Guard Chain

For critical workflows, chain multiple guards:

```json
{
  "workflow": [
    {
      "validateData": {
        "validationType": "required_fields",
        "data": "$.request",
        "requiredFields": ["userId", "email", "payload"],
        "invalid?": {
          "editFields": {
            "fieldsToSet": [
              { "name": "errorType", "value": "MISSING_FIELDS", "type": "string" },
              { "name": "errorDetails", "value": "$.validationErrors", "type": "any" }
            ]
          }
        }
      }
    },
    {
      "validateData": {
        "validationType": "pattern",
        "data": "$.request",
        "patternValidations": [
          { "field": "email", "pattern": "^[^@]+@[^@]+\\.[^@]+$", "errorMessage": "Invalid email format" }
        ],
        "invalid?": {
          "editFields": {
            "fieldsToSet": [
              { "name": "errorType", "value": "INVALID_FORMAT", "type": "string" },
              { "name": "errorDetails", "value": "$.validationErrors", "type": "any" }
            ]
          }
        }
      }
    },
    {
      "validateData": {
        "validationType": "type_check",
        "data": "$.request.payload",
        "typeChecks": [
          { "field": "amount", "expectedType": "number" }
        ],
        "invalid?": {
          "editFields": {
            "fieldsToSet": [
              { "name": "errorType", "value": "TYPE_ERROR", "type": "string" },
              { "name": "errorDetails", "value": "$.validationErrors", "type": "any" }
            ]
          }
        }
      }
    },
    {
      "log": { "message": "All validations passed for {{$.request.userId}}" }
    }
  ]
}
```

### Guard Checklist for Generated Workflows

Before finalizing any workflow, ensure:

- [ ] **Entry validation**: First node validates `initialState` or external input
- [ ] **AI output validation**: Any `ask-ai` response used as structured data is validated with `validateData` (validationType: `json`)
- [ ] **Array guards**: Loops check array length before iteration
- [ ] **Required fields**: Nested property access is guarded by `required_fields` validation
- [ ] **Error edges**: All nodes that can fail have `error?` edges
- [ ] **Type checks**: Operations requiring specific types validate beforehand
- [ ] **Graceful fallbacks**: `invalid?` edges provide meaningful error context

### validateData Node Reference

| Validation Type | Purpose | Required Config |
|-----------------|---------|-----------------|
| `json` | Check if string is valid JSON | `data` |
| `required_fields` | Check fields exist and non-empty | `data`, `requiredFields[]` |
| `type_check` | Verify field types | `data`, `typeChecks[]` |
| `pattern` | Regex validation | `data`, `patternValidations[]` |
| `range` | Numeric bounds | `data`, `rangeValidations[]` |
| `json_schema` | Full JSON Schema | `data`, `schema` |

**State written by validateData:**
- `validationResult`: `{ isValid, timestamp, validationType }`
- `validationErrors`: Array of `{ field, error, value }`
- `parsedJson`: (only for `json` type) The parsed JSON object

## Reference Documentation

- **Complexity Detection**: [references/complexity-detection.md](references/complexity-detection.md) - When to stop and suggest node development
- **Workflow Syntax**: [references/workflow-syntax.md](references/workflow-syntax.md) - Complete JSON structure reference
- **Patterns**: [references/patterns.md](references/patterns.md) - Common workflow patterns with examples
- **Node Reference**: [references/node-quick-reference.md](references/node-quick-reference.md) - All 45 nodes categorized
- **Flat vs Nested Comparison**: [references/flat-vs-nested.md](references/flat-vs-nested.md) - Side-by-side examples
- **Defensive Guards**: See section above for validation patterns

## Scripts

- **Validate**: `scripts/validate-workflow.ts` - Validate workflow JSON
- **Fetch Manifest**: `scripts/fetch-manifest.sh` - Fetch node manifest from API
- **Start Server**: `scripts/start-dev-server.sh` - Start dev server if not running
