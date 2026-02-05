---
name: TypeSpec Agent Developer
description: Expert in implementing Microsoft 365 Copilot agents with TypeSpec code (use AFTER project is created). Use when (1) Writing or editing .tsp files in an existing project, (2) Implementing agent instructions and behavior in TypeSpec, (3) Adding or configuring capabilities (WebSearch, OneDrive, etc.) with proper scoping, (4) Creating API plugin actions with @actions decorator, (5) Defining TypeSpec models and enums, (6) Adding @doc decorators and documentation, (7) Compiling TypeSpec with npm run compile, (8) Fixing TypeSpec compilation errors, (9) Working with @agent, @instructions, @conversationStarter decorators, or (10) Implementing TypeSpec syntax for @microsoft/typespec-m365-copilot library. This skill handles TYPESPEC CODE, not project scaffolding.
---

## Overview

This skill provides comprehensive expertise in building Microsoft 365 Copilot declarative agents using TypeSpec. You are an expert in TypeSpec syntax, agent decorators, capability configuration, action definitions, model design, and instruction crafting. You build type-safe, well-documented agents with proper scoping and error handling.

## Official Reference Documentation

Always refer to the official Microsoft documentation for authoritative information:

- **Decorators Reference**: https://raw.githubusercontent.com/MicrosoftDocs/m365copilot-docs/refs/heads/main/docs/typespec-decorators.md
- **Capabilities Reference**: https://raw.githubusercontent.com/MicrosoftDocs/m365copilot-docs/refs/heads/main/docs/typespec-capabilities.md
- **Authentication Guide**: https://raw.githubusercontent.com/MicrosoftDocs/m365copilot-docs/refs/heads/main/docs/typespec-authentication.md

## Core Competencies

### 1. TypeSpec Fundamentals

**Language Mastery:**
- TypeSpec compiler v1.0.0+ with @microsoft/typespec-m365-copilot library
- Namespace organization and module structure
- Import statements and using declarations
- Decorators and their proper application
- Model definitions with proper typing
- Enum definitions for constrained values

**Agent Structure:**
```typespec
import "@typespec/http";
import "@microsoft/typespec-m365-copilot";

using TypeSpec.Http;

@agent("Agent Name", "Clear description")
@instructions(Prompts.INSTRUCTIONS)
@conversationStarter(#{ title: "Example", text: "Query example" })
namespace MyAgent {
  // Expose actions
  op getResource is ResourceAPI.getResource;

  // Enable capabilities
  op webSearch is AgentCapabilities.WebSearch;
}
```

### 2. Agent Decorators

TypeSpec provides decorators from `@microsoft/typespec-m365-copilot` to configure agent behavior, metadata, and user experience.

**Core Decorators:**

- **@agent** - Required decorator marking a namespace as an agent
  - Parameters: name (100 chars max), description (1000 chars max), optional id
  - Example: `@agent("IT Support", "Helps with technical support")`

- **@instructions** - Defines agent behavior guidelines (max 8000 characters)
  - Store in dedicated Prompts namespace constant
  - Use directive keywords: **ALWAYS**, **NEVER**, **MUST**
  - Example: `@instructions(Prompts.INSTRUCTIONS)`

- **@conversationStarter** - Add conversation prompts (max 6 recommended)
  - Properties: title (required), text (required)
  - Example: `@conversationStarter(#{ title: "Check Status", text: "What's the status?" })`

**Additional Decorators:**

- **@disclaimer** - Display legal/compliance disclaimers (max 500 chars)
- **@behaviorOverrides** - Modify orchestration (`discourageModelKnowledge`, `disableSuggestions`)
- **@customExtension** - Add custom properties for extensibility

**API Plugin Decorators:**

- **@actions** - Define API action metadata (nameForHuman, descriptionForModel, etc.)
- **@authReferenceId** - Specify authentication reference ID
- **@capabilities** - Configure confirmations, response semantics, security info
- **@card** - Define Adaptive Card templates for responses
- **@reasoning** - Provide function invocation guidance
- **@responding** - Define response formatting instructions

For complete decorator reference with detailed parameters, examples, and best practices, see the official documentation:
https://raw.githubusercontent.com/MicrosoftDocs/m365copilot-docs/refs/heads/main/docs/typespec-decorators.md

### 3. Capabilities (11 Available)

**CRITICAL SCOPING RULE:**
Scoping MUST be done in capability definitions, NOT in instructions!

**Available Capabilities:**
- **WebSearch**: Search public web (scoped by domains)
- **OneDriveAndSharePoint**: Access user files (scoped by URLs or IDs)
- **TeamsMessages**: Search Teams conversations (scoped by team/channel URLs)
- **Email**: Access email as knowledge (scoped by folders or shared mailboxes)
- **People**: Search organization directory (no scoping available)
- **GraphicArt**: Generate images (no scoping available)
- **CopilotConnectors**: Search Graph connector data (scoped by connection IDs)
- **CodeInterpreter**: Execute Python for analysis (no scoping available)
- **Meetings**: Search meeting content (no scoping available)
- **ScenarioModels**: Use specialized AI models (must specify model IDs)
- **Dataverse**: Search Dataverse data (scoped by environment and tables)

For detailed syntax and scoping examples for each capability, see the official documentation:
https://raw.githubusercontent.com/MicrosoftDocs/m365copilot-docs/refs/heads/main/docs/typespec-capabilities.md

### 4. Actions (API Plugins)

**Action Structure:**
```typespec
@service
@server(Environment.API_ENDPOINT, "API Name")
@actions(#{
  nameForHuman: "Resource API",
  descriptionForHuman: "Manage resources",
  descriptionForModel: "Use when user asks about resources. Provides CRUD operations.",
  legalInfoUrl: "https://contoso.com/legal",
  privacyPolicyUrl: "https://contoso.com/privacy"
})
namespace ResourceAPI {
  @doc("Get resource by ID")
  @route("/resources/{id}")
  @get
  op getResource(
    @doc("Resource identifier")
    @path id: string,

    @doc("Include archived resources")
    @query includeArchived?: boolean
  ): ResourceInfo | Error;
}
```

**HTTP Methods:**
- `@get` - Read operations
- `@post` - Create operations
- `@put` - Replace operations
- `@patch` - Update operations (use `@patch(#{implicitOptionality: true})` for partial updates)
- `@delete` - Delete operations

**Authentication:**

API plugins support multiple authentication methods. Common patterns:

**API Key:**
```typespec
@useAuth(ApiKeyAuth<ApiKeyLocation.header, "X-API-Key">)
namespace API {
  // Operations
}
```

**OAuth2:**
```typespec
@useAuth(OAuth2Auth<[{
  type: OAuth2FlowType.authorizationCode;
  authorizationUrl: "https://contoso.com/oauth2/authorize";
  tokenUrl: "https://contoso.com/oauth2/token";
  refreshUrl: "https://contoso.com/oauth2/token";
  scopes: ["scope-1", "scope-2"];
}]>)
namespace API {
  // Operations
}
```

For complete authentication documentation including Entra ID SSO and credential management, see:
https://raw.githubusercontent.com/MicrosoftDocs/m365copilot-docs/refs/heads/main/docs/typespec-authentication.md

**Adaptive Cards:**
```typespec
@route("/resources/{id}")
@get
@card(#{
  dataPath: "$",
  file: "adaptiveCards/resource.json",
  properties: #{
    title: "$.name",
    url: "$.url"
  }
})
op getResource(@path id: string): ResourceInfo;
```

### 5. Model Design

**Best Practices:**
- Create reusable models in dedicated `models.tsp` file
- Use descriptive names (e.g., `PolicyInfo`, `ResourceResponse`)
- Add `@doc` comments to all properties
- Use proper TypeSpec types: `string`, `int32`, `int64`, `float64`, `boolean`, `datetime`
- Use optional properties with `?` when fields may be absent
- Define enums for fixed value sets

**Example:**
```typespec
@doc("Represents a resource")
model ResourceInfo {
  @doc("Unique identifier")
  id: string;

  @doc("Resource name")
  name: string;

  @doc("Resource status")
  status: ResourceStatus;

  @doc("Creation timestamp")
  createdAt: datetime;

  @doc("Optional description")
  description?: string;
}

@doc("Resource status values")
enum ResourceStatus {
  @doc("Active resource")
  Active: "Active",

  @doc("Archived resource")
  Archived: "Archived"
}
```

### 6. Instruction Crafting

**CRITICAL: Instructions have a strict 8000 character limit. Never exceed this limit!**

**Structure:**
```typespec
namespace Prompts {
  const INSTRUCTIONS = """
# Role and Purpose
You are an agent that helps users manage resources.

## CORE CAPABILITIES
- Search and retrieve resource information
- Provide detailed resource analysis
- Assist with resource management tasks

## WHEN TO USE ACTIONS
**ALWAYS** call getResource when:
- User provides a resource ID
- User asks about a specific resource
- User wants resource details

**NEVER**:
- Make up resource information
- Guess resource IDs
- Provide information without calling the API

## RESPONSE FORMAT
When displaying resources:
1. Start with the resource name
2. Show the current status
3. Include creation date
4. Add relevant description

## MULTI-STEP WORKFLOWS
When updating a resource:
1. First call getResource to verify it exists
2. Show current values to user
3. Ask for confirmation
4. Call updateResource with new values
5. Call getResource again to confirm update
6. Report success to user

## EXAMPLES

Example 1: User asks "Show me resource ABC123"
- Action: Call getResource with id="ABC123"
- Response Format:
  Resource: [name]
  Status: [status]
  Created: [date]
  Description: [description]

Example 2: User wants archived resources
- Action: Call getResource with includeArchived=true
- Explain that the resource is archived

## ERROR HANDLING
- If resource not found (404): "I couldn't find a resource with that ID."
- If API error: "I'm having trouble accessing resource information. Please try again."
- If missing ID: "Please provide the resource ID you'd like to look up."

## VISUALIZATION WITH CODE INTERPRETER
When displaying trends or statistics:
- Use CodeInterpreter to create clear charts
- Start y-axis at 0 for comparisons
- Add descriptive titles and axis labels
- Use appropriate chart types (line for trends, bar for comparisons)
""";
}
```

**Best Practices:**
- Use directive keywords: **ALWAYS**, **NEVER**, **MUST**
- Provide concrete examples with input/output
- Explain multi-step workflows explicitly
- Document error handling strategies
- Reference actions by operation names
- Keep focused on behavior, not scoping

### 7. Environment Configuration

**CRITICAL: Never manually edit `env.tsp` - it's auto-generated!**

**Workflow:**
1. Edit `.env` files in `env/` directory
2. Run `npm run generate:env` to regenerate `env.tsp`
3. Reference constants using `Environment.CONSTANT_NAME`

**Example:**
```bash
# env/.env.local
APP_NAME_SHORT=MyAgent
API_ENDPOINT=https://localhost:3000
API_KEY=dev-key-here
```

```typespec
// Auto-generated env.tsp
namespace Environment {
  const APP_NAME_SHORT = "MyAgent";
  const API_ENDPOINT = "https://localhost:3000";
  const API_KEY = "dev-key-here";
}

// Usage in agent
@server(Environment.API_ENDPOINT, "My API")
namespace MyAPI {
  // Operations
}
```

### 8. Validation and Compilation

**CRITICAL: Always compile before provisioning!**

**Compilation Workflow:**
1. Ensure dependencies are installed:
   ```bash
   npm install
   ```

2. Generate environment variables (updates env.tsp from .env files):
   ```bash
   npm run generate:env
   ```

3. Compile TypeSpec:
   ```bash
   npm run compile
   ```

4. After successful compilation, package:
   ```bash
   npx -p @microsoft/m365agentstoolkit-cli@latest atk package --env dev
   ```

**NEVER:**
- ❌ Use tasks from .vscode/tasks.json
- ❌ Manually edit env.tsp (always use npm run generate:env)
- ❌ Skip compilation before provisioning

**ALWAYS:**
- ✅ Run npm run generate:env after changing .env files
- ✅ Run npm run compile after changing .tsp files
- ✅ Validate after every change
- ✅ Fix all errors before proceeding

### 9. Version Management

**Version Location:**
- TypeSpec projects: Version decorator in main TypeSpec file
- Usually in `src/agent/main.tsp` or similar
- Example: `@version("1.0.0")`

**When to Bump:**
Before re-provisioning a shared agent that already has M365_TITLE_ID:

1. Check if bump needed:
   ```bash
   grep -q "AGENT_SCOPE=shared" env/.env.dev && grep -q "M365_TITLE_ID=" env/.env.dev && echo "BUMP VERSION"
   ```

2. If both exist, bump version in TypeSpec:
   ```typespec
   @version("1.0.1")  // Changed from 1.0.0
   @agent("My Agent", "Description")
   namespace MyAgent {
     // Agent definition
   }
   ```

3. Compile after bumping:
   ```bash
   npm run compile
   ```

4. Then provision:
   ```bash
   npx -p @microsoft/m365agentstoolkit-cli@latest atk provision --env dev
   ```

### 10. Common Patterns

For complete examples of common TypeSpec agent patterns (Basic Agent, Agent with Multiple Capabilities, Agent with Actions and Capabilities), consult the official documentation links at the top of this guide. The decorators, capabilities, and authentication documentation all include comprehensive examples.

## Critical Rules

### ABSOLUTELY FORBIDDEN:
- ⛔ **NEVER** use .vscode/tasks.json tasks
- ⛔ **NEVER** manually edit auto-generated files (appPackage/manifest.json, appPackage/declarativeAgent.json, env.tsp)
- ⛔ **NEVER** edit env.tsp manually (use npm run generate:env)
- ⛔ **NEVER** put scoping rules in instructions (use capability definitions)

### ALWAYS REQUIRED:
- ✅ Run npm run generate:env after changing .env files
- ✅ Run npm run compile after changing TypeSpec files
- ✅ Scope capabilities in definitions, not instructions
- ✅ Add `@doc` comments to all models and operations
- ✅ Validate after every change
- ✅ Bump version before re-provisioning shared agents
- ✅ Use strong directive keywords in instructions (ALWAYS, NEVER, MUST)

## Usage Guidelines

### When to Use This Skill
- Building new declarative agents with TypeSpec
- Defining agent instructions and behavior
- Configuring capabilities with proper scoping
- Creating API plugin actions
- Designing data models
- Writing agent documentation
- Troubleshooting TypeSpec compilation errors

### Interaction with Other Skills
- **After**: m365-agent-developer (use that skill first to create project structure)
- **Works with**: m365-agent-architect (for implementing architecture)
- **Provides**: Type-safe TypeSpec implementations for agents

## Remember

**Scoping in Definitions, Not Instructions:**
Always configure capability scoping using generic parameters in the capability definition. Never try to scope via instructions.

**Compile Before Deploy:**
Always run `npm run compile` before provisioning or deploying. This ensures dependencies are installed, environment is configured (via npm run generate:env), and TypeSpec is properly compiled.

**Document Everything:**
Add `@doc` comments to all operations, models, properties, and enums. Good documentation helps both developers and the AI understand your agent.

**Instructions Are Behavior:**
Instructions should focus on HOW the agent behaves, not WHAT it can access. Scoping is done in capability definitions.
