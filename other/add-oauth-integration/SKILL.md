---
name: add-oauth-integration
description: Guide for adding new OAuth-based integrations to Fabric. Use when implementing OAuth providers like Microsoft Teams, GitHub, Google Drive, Slack, or similar services that need OAuth 2.0 authentication for user data access.
---

# Add OAuth Integration Skill

This skill guides you through adding a new OAuth-based integration to the Fabric platform.

## When to Use This Skill

- Adding a new OAuth provider (Microsoft Teams, Slack, Notion, etc.)
- Connecting third-party services via OAuth 2.0 flow
- Creating MCP tools that require user authentication
- Building integrations that access external APIs on behalf of users

## Overview

OAuth integrations allow users to connect third-party services using OAuth 2.0 flow. Credentials are stored server-side (encrypted), not in the browser. The integration appears in the Fabric AI Agent's available tools.

## Architecture Overview

```
User clicks "Connect" → OAuth popup → Provider auth → Callback stores token
                                                            ↓
                                                   WorkflowIntegration table
                                                            ↓
                        ┌───────────────────────────────────┴───────────────────────────────────┐
                        ↓                                                                       ↓
              TASK AGENT PATH                                                      ORCHESTRATOR PATH
         (Custom agents: /app/agents/{id})                                 (Fabric AI: /app/agents/fabric-ai)
                        ↓                                                                       ↓
         mcp-tools.ts → loadMcpConfiguration                               preload-resources.ts → loadOAuthIntegrationTools
         agent-execution.ts → workflow guidance                            initialization.ts → passes enabledIntegrationIds
```

## ⚠️ CRITICAL: Two Code Paths

OAuth integrations must be implemented in **BOTH** code paths:

| Path | Interface | When Used | Key Files |
|------|-----------|-----------|-----------|
| **Task Agent** | `/app/agents/{agentId}` | Custom registered agents | `mcp-tools.ts`, `agent-execution.ts` |
| **Orchestrator** | `/app/agents/fabric-ai` | Fabric AI Agent (main interface) | `preload-resources.ts`, `initialization.ts` |

**If you only implement the Task Agent path, your integration will NOT work in Fabric AI Agent!**

## Files to Update (Checklist)

### 1. OAuth Provider Configuration
**File:** `packages/api/modules/integrations/lib/oauth-providers.ts`

```typescript
// 1. Add to OAuthProviderType union
export type OAuthProviderType =
	| "GITHUB"
	| "GOOGLE_DRIVE"
	| "MICROSOFT_GRAPH"  // Microsoft Teams uses this
	| "SLACK"
	| "NOTION"
	| "YOUR_NEW_PROVIDER"; // Add here

// 2. Create provider config
const yourNewProvider: OAuthProviderConfig = {
	type: "YOUR_NEW_PROVIDER",
	name: "Your Provider Display Name", // IMPORTANT: This name is returned in OAuth callback
	authorizationUrl: "https://provider.com/oauth/authorize",
	tokenUrl: "https://provider.com/oauth/token",
	scopes: ["scope1", "scope2"],
	clientIdEnvVar: "YOUR_PROVIDER_CLIENT_ID",
	clientSecretEnvVar: "YOUR_PROVIDER_CLIENT_SECRET",
	supportsRefreshToken: true, // or false
	authParams: { // optional
		access_type: "offline",
	},
	getUserInfo: async (accessToken: string): Promise<OAuthUserInfo> => {
		const response = await fetch("https://api.provider.com/user", {
			headers: { Authorization: `Bearer ${accessToken}` },
		});
		const data = await response.json();
		return {
			id: data.id,
			login: data.username,
			name: data.displayName,
			email: data.email,
			avatarUrl: data.avatar,
		};
	},
	refreshAccessToken: async (refreshToken, clientId, clientSecret) => {
		// Implement if supportsRefreshToken is true
	},
};

// 3. Add to oauthProviders record
export const oauthProviders: Record<OAuthProviderType, OAuthProviderConfig> = {
	// ... existing providers
	YOUR_NEW_PROVIDER: yourNewProvider,
};
```

### 2. MCP Registry - Workflow Guidance
**File:** `packages/mcp-registry/src/workflow-guidance.ts`

Add workflow guidance so the AI knows how to use your tools:

```typescript
export const YOUR_PROVIDER_WORKFLOW_GUIDANCE = `## Your Provider Workflow

When user asks about Your Provider data:
1. Use your_provider__list_items to get available items
2. Use your_provider__get_item for specific item details
3. Use your_provider__search for searching

### Example Usage
- "Show me my items" → your_provider__list_items
- "Search for X" → your_provider__search({ query: "X" })
`;
```

### 3. MCP Registry - Conditional Account
**File:** `packages/mcp-registry/src/conditional-accounts.ts`

Define the account and its tools:

```typescript
export const YOUR_PROVIDER_ACCOUNT: AccountDefinition = {
	id: "your_provider",
	name: "Your Provider",
	credentialType: "your_provider_oauth",
	authType: "oauth",
	requiredScopes: ["scope1", "scope2"],
	mcps: [
		{
			id: "your-provider-tools",
			name: "Your Provider Tools",
			serverName: "your_provider",
			available: true,
			tools: [
				{
					name: "list_items",
					description: "List all items from Your Provider",
					inputSchema: {
						type: "object",
						properties: {
							limit: { type: "number", description: "Max items to return" },
						},
					},
				},
				// ... more tools
			],
		},
	],
};

// Add to CONDITIONAL_ACCOUNTS array
export const CONDITIONAL_ACCOUNTS: AccountDefinition[] = [
	GITHUB_ACCOUNT,
	MICROSOFT_TEAMS_ACCOUNT,
	YOUR_PROVIDER_ACCOUNT, // Add here
];
```

### 4. MCP Registry - Exports
**File:** `packages/mcp-registry/src/index.ts`

```typescript
// Export workflow guidance
export {
	// ... existing exports
	YOUR_PROVIDER_WORKFLOW_GUIDANCE,
} from "./workflow-guidance";

// Export account
export {
	// ... existing exports
	YOUR_PROVIDER_ACCOUNT,
} from "./conditional-accounts";
```

### 5. Tool Execution in Temporal
**File:** `packages/temporal/src/activities/task-agent/mcp-tools.ts`

Add tool execution handler:

```typescript
// 1. Add check in executeTaskAgentTool
if (mcpTool.configId.startsWith("your-provider-connected:")) {
	const methodName = toolName.split("__")[1] || toolName;
	return executeYourProviderTool(methodName, args, userId, organizationId);
}

// 2. Implement the execution function
async function executeYourProviderTool(
	methodName: string,
	args: Record<string, unknown>,
	userId: string,
	organizationId?: string,
): Promise<unknown> {
	// Get token from WorkflowIntegration (uses XOR pattern)
	const integration = organizationId
		? await db.workflowIntegration.findFirst({
				where: { organizationId, provider: "YOUR_PROVIDER", isActive: true },
			})
		: await db.workflowIntegration.findFirst({
				where: { userId, organizationId: null, provider: "YOUR_PROVIDER", isActive: true },
			});

	if (!integration?.credentials) {
		throw new Error("Provider not connected. Please connect in Settings > Integrations.");
	}

	const credentialsJson = decryptApiKey(integration.credentials);
	const { access_token } = JSON.parse(credentialsJson);

	// Call provider API based on methodName
	switch (methodName) {
		case "list_items":
			// Implement API call
			break;
		// ... more cases
	}
}

// 3. Add conditional loading in loadMcpConfiguration
const yourProviderIntegration = organizationId
	? await db.workflowIntegration.findFirst({
			where: { organizationId, provider: "YOUR_PROVIDER", isActive: true },
		})
	: await db.workflowIntegration.findFirst({
			where: { userId, organizationId: null, provider: "YOUR_PROVIDER", isActive: true },
		});

if (yourProviderIntegration) {
	const { YOUR_PROVIDER_ACCOUNT } = await import("@repo/mcp-registry");
	// Add tools from YOUR_PROVIDER_ACCOUNT.mcps
}
```

### 6. Agent Execution - Add Workflow Guidance
**File:** `packages/temporal/src/activities/task-agent/agent-execution.ts`

```typescript
// 1. Import the guidance
import {
	GITHUB_WORKFLOW_GUIDANCE,
	MICROSOFT_TEAMS_WORKFLOW_GUIDANCE,
	YOUR_PROVIDER_WORKFLOW_GUIDANCE, // Add import
	getAlwaysEnabledWorkflowGuidance,
} from "@repo/mcp-registry";

// 2. Check if tools are connected
const hasYourProviderConnected = mcpConfig.tools.some((t) =>
	t.configId.startsWith("your-provider-connected:"),
);

// 3. Add guidance in buildAgentSystemPrompt
if (hasYourProviderConnected && YOUR_PROVIDER_WORKFLOW_GUIDANCE) {
	workflowGuidance = workflowGuidance
		? `${workflowGuidance}\n\n${YOUR_PROVIDER_WORKFLOW_GUIDANCE}`
		: YOUR_PROVIDER_WORKFLOW_GUIDANCE;
}
```

### 7. Orchestrator Path - Preload Resources (CRITICAL!)
**File:** `packages/temporal/src/activities/orchestrator/preload/preload-resources.ts`

This is the **most commonly missed step**. Without this, your integration works in custom agents but NOT in Fabric AI Agent.

```typescript
// In loadOAuthIntegrationTools function, add a new block for your provider:

// ========== YOUR PROVIDER Integration ==========
const yourProviderIntegration = await db.oAuthIntegration.findFirst({
	where: {
		userId,
		organizationId: organizationId ?? null,
		provider: "your_provider", // lowercase provider name
	},
});

if (yourProviderIntegration?.accessToken) {
	// Check if enabled via direct integrationIds OR prefixed filterIds
	const newFormatId = `oauth:your_provider:${yourProviderIntegration.id}`;
	const legacyFormatId = `oauth:yourprovider:${yourProviderIntegration.id}`; // if applicable

	// CRITICAL: Check BOTH formats - UI may pass either one
	const isEnabledViaIntegrationIds = integrationIds
		? integrationIds.includes(yourProviderIntegration.id)
		: false;
	const isEnabledViaFilterIds = filterIds
		? filterIds.includes(newFormatId) ||
		  filterIds.includes(legacyFormatId) ||
		  filterIds.includes(yourProviderIntegration.id)
		: false;

	// If no filter specified at all, allow all (backward compatibility)
	const noFiltersSpecified = !filterIds && !integrationIds;
	const isEnabled = noFiltersSpecified || isEnabledViaIntegrationIds || isEnabledViaFilterIds;

	if (!isEnabled) {
		console.log("[Preload] Your Provider integration disabled in orchestrator preferences");
	} else {
		try {
			const { YOUR_PROVIDER_ACCOUNT } = await import("@repo/mcp-registry");

			let toolCount = 0;
			for (const mcp of YOUR_PROVIDER_ACCOUNT.mcps) {
				if (mcp.available === false) {
					continue;
				}

				const serverName = mcp.serverName || mcp.name;
				const tools: McpToolInfo[] = [];

				for (const tool of mcp.tools || []) {
					const toolName = `${serverName}__${tool.name}`;
					tools.push({
						name: toolName,
						description: tool.description || "",
						inputSchema: (tool.inputSchema as Record<string, unknown>) || {
							type: "object",
						},
					});
					toolCount++;
				}

				if (tools.length > 0) {
					results.push({
						serverId: `your-provider-connected:${yourProviderIntegration.id}`,
						serverName,
						tools,
						serverType: "oauth",
					});
				}
			}

			console.log(`[Preload] Loaded ${toolCount} Your Provider tools from registry`);
		} catch (e) {
			console.warn("[Preload] Failed to load Your Provider tools from registry", e);
		}
	}
}
```

### 8. Orchestrator Path - Initialization Phase
**File:** `packages/temporal/src/workflows/orchestrator/phases/initialization.ts`

Ensure `enabledIntegrationIds` is passed to the preload activity:

```typescript
// In executeInitializationPhase function:
const preloadedResources = await preloadResourcesActivity({
	userId: input.userId,
	organizationId: input.organizationId,
	enabledMcpConfigIds: input.enabledMcpConfigIds ?? undefined,
	enabledAgentIds: input.enabledAgentIds ?? undefined,
	enabledIntegrationIds: input.enabledIntegrationIds ?? undefined, // CRITICAL: Don't forget this!
});
```

**Also verify** that `PreloadResourcesInput` interface includes `enabledIntegrationIds`:
```typescript
export interface PreloadResourcesInput {
	userId: string;
	organizationId?: string;
	enabledMcpConfigIds?: string[];
	enabledAgentIds?: string[];
	enabledIntegrationIds?: string[];  // Must be present!
}
```

---

## Part 2: UI and Configuration

### 9. Plugin UI Components
**Directory:** `apps/web/modules/saas/workflows/lib/plugins/your-provider/`

Create these files:

#### `icon.tsx`
```typescript
export function YourProviderIcon({ className }: { className?: string }) {
	return (
		<svg className={className} viewBox="0 0 24 24" fill="currentColor">
			{/* SVG path */}
		</svg>
	);
}
```

#### `YourProviderSettings.tsx`
```typescript
"use client";

import { OAuthSettings } from "../shared/OAuthSettings";
import { YourProviderIcon } from "./icon";
import type { IntegrationSettingsProps } from "../types";

export function YourProviderSettings({
	onApiKeyChange,
	organizationId,
}: IntegrationSettingsProps) {
	return (
		<OAuthSettings
			provider="YOUR_NEW_PROVIDER"
			// CRITICAL: This MUST match exactly the 'name' field in oauth-providers.ts
			providerName="Your Provider Display Name"
			providerIcon={YourProviderIcon}
			providerColor="text-blue-600"
			description="Connect your account to access data."
			helpText="We request read-only access to your data."
			scopes={["scope1", "scope2"]}
			organizationId={organizationId}
			onConnectionChange={(connected) => {
				if (connected) {
					onApiKeyChange("oauth_connected");
				} else {
					onApiKeyChange("");
				}
			}}
		/>
	);
}
```

#### `index.ts`
```typescript
import { registerIntegration } from "../registry";
import type { IntegrationPlugin } from "../types";
import { YourProviderIcon } from "./icon";
import { YourProviderSettings } from "./YourProviderSettings";

export const yourProviderPlugin: IntegrationPlugin = {
	type: "YOUR_NEW_PROVIDER",
	label: "Your Provider",
	description: "Access your provider's data for AI-powered workflows",
	icon: YourProviderIcon,
	color: "text-blue-600",
	formFields: [],
	SettingsComponent: YourProviderSettings,
	testConfig: { skipClientTest: true },
	actions: [
		{ id: "list_items", label: "List Items", description: "Get all items" },
		// ... more actions
	],
};

registerIntegration(yourProviderPlugin);
export default yourProviderPlugin;
```

### 8. Register Plugin
**File:** `apps/web/modules/saas/workflows/lib/plugins/index.ts`

```typescript
import "./your-provider";
export { yourProviderPlugin } from "./your-provider";
```

### 9. Environment Variables
**File:** `.env.example` and `.env.local`
```bash
YOUR_PROVIDER_CLIENT_ID="your-client-id"
YOUR_PROVIDER_CLIENT_SECRET="your-client-secret"
```

## Testing the Integration

### Important: Use Fabric AI Agent, NOT Basic Chat

MCP tools are only available in the **Fabric AI Agent** interface, not the basic AI Chat.

### Step 1: Set Environment Variables
```bash
# .env.local
YOUR_PROVIDER_CLIENT_ID="your-actual-client-id"
YOUR_PROVIDER_CLIENT_SECRET="your-actual-client-secret"
```

### Step 2: Restart Development Server
```bash
pnpm dev
# OR if using Aspire:
./aspire.sh restart
```

### Step 3: Connect the Integration
1. Go to **Settings > Integrations** (or `/app/settings/integrations`)
2. Find your provider in the list
3. Click **Connect with [Provider]**
4. Complete OAuth flow in popup
5. Verify "Connected" status appears

### Step 4: Test Tools in Fabric AI Agent
1. Navigate to **Fabric AI Agent**: `/app/agents/fabric-ai`
   - Or for organization: `/app/{org-slug}/agents/fabric-ai`
2. Try prompts that use your tools:
   ```
   Show me my items from [Provider]
   Search [Provider] for "keyword"
   ```

### Step 5: Verify Tool Execution
Check Temporal worker logs for:
- Tool calls to `your_provider__*`
- API requests to your provider

## Common Pitfalls

### 1. Missing Orchestrator Path (CRITICAL!)
**Problem:** Integration works in custom agents (`/app/agents/{id}`) but NOT in Fabric AI Agent (`/app/agents/fabric-ai`).

**Cause:** You only implemented the Task Agent path and forgot the Orchestrator path.

**Solution:** Add your integration to BOTH:
1. `packages/temporal/src/activities/task-agent/mcp-tools.ts` (Task Agent)
2. `packages/temporal/src/activities/orchestrator/preload/preload-resources.ts` (Orchestrator)

See sections 7-8 above for the Orchestrator implementation.

### 2. enabledIntegrationIds Not Passed Through
**Problem:** Integration is connected and enabled in UI, but tools don't load in Fabric AI Agent.

**Cause:** `enabledIntegrationIds` isn't being passed from workflow input to preload activity.

**Solution:** Check `initialization.ts` passes `enabledIntegrationIds`:
```typescript
const preloadedResources = await preloadResourcesActivity({
	// ...other params
	enabledIntegrationIds: input.enabledIntegrationIds ?? undefined,
});
```

### 3. Integration ID Format Mismatch
**Problem:** Integration shows as enabled in UI but preload function says "disabled in preferences".

**Cause:** The UI may pass IDs in different formats:
- Direct: `"integration-uuid-here"`
- Prefixed: `"oauth:provider:integration-uuid-here"`

**Solution:** Check BOTH formats in your enable check:
```typescript
const isEnabledViaIntegrationIds = integrationIds?.includes(integration.id) ?? false;
const isEnabledViaFilterIds = filterIds
	? filterIds.includes(`oauth:provider:${integration.id}`) ||
	  filterIds.includes(integration.id)
	: false;
```

### 4. Provider Name Mismatch
**Problem:** After OAuth completes, UI doesn't update to show connected state.

**Cause:** The `providerName` in your Settings component doesn't match the `name` field in `oauth-providers.ts`.

**Solution:** Ensure exact match:
```typescript
// oauth-providers.ts
const provider = { name: "Microsoft 365" };

// Settings component - MUST MATCH!
<OAuthSettings providerName="Microsoft 365" ... />
```

### 5. "OAuth not configured on server"
**Problem:** Integration shows this message instead of Connect button.

**Solution:**
1. Check env vars are set in `.env.local`
2. Restart the dev server (env vars are loaded at startup)

### 6. Tools Not Appearing in Fabric AI Agent
**Problem:** Connected but AI doesn't use your tools.

**Causes & Solutions:**
1. **Missing Orchestrator path**: Add to `preload-resources.ts` (most common!)
2. **Missing from loadMcpConfiguration**: Add conditional loading check in Task Agent path
3. **Missing workflow guidance**: Add guidance to agent-execution.ts
4. **Using wrong interface**: Use Fabric AI Agent (`/app/agents/fabric-ai`), not basic Chat

### 7. Tool Execution Fails
**Problem:** AI tries to use tool but gets error.

**Solutions:**
1. Check `executeYourProviderTool` function exists in mcp-tools.ts
2. Check configId prefix matches (`your-provider-connected:`)
3. Verify WorkflowIntegration record exists with correct provider enum

### 8. Tenant Isolation Issues
**Problem:** Personal credentials used in org context or vice versa.

**Solution:** Always use XOR pattern in queries:
```typescript
// For org context
{ organizationId, provider: "...", isActive: true }

// For personal context - explicitly check null!
{ userId, organizationId: null, provider: "...", isActive: true }
```

## Testing Checklist

- [ ] Environment variables set in `.env.local`
- [ ] Dev server restarted
- [ ] Integration appears in Settings > Integrations
- [ ] OAuth Connect button shows (not "not configured")
- [ ] OAuth flow completes successfully
- [ ] UI shows "Connected" status
- [ ] **Task Agent path**: Tools load in custom agents (`/app/agents/{id}`)
- [ ] **Orchestrator path**: Tools load in Fabric AI Agent (`/app/agents/fabric-ai`)
- [ ] Enable/disable toggle in Orchestrator preferences works
- [ ] AI can execute tools successfully
- [ ] Test in both personal AND organization contexts

## Example: Microsoft Teams Integration

For reference, see the Microsoft Teams implementation:

| Component | File |
|-----------|------|
| OAuth Provider | `packages/api/modules/integrations/lib/oauth-providers.ts` → `microsoftGraphProvider` |
| Workflow Guidance | `packages/mcp-registry/src/workflow-guidance.ts` → `MICROSOFT_TEAMS_WORKFLOW_GUIDANCE` |
| Account Definition | `packages/mcp-registry/src/conditional-accounts.ts` → `MICROSOFT_TEAMS_ACCOUNT` |
| **Task Agent Path** | |
| Tool Execution | `packages/temporal/src/activities/task-agent/mcp-tools.ts` → `executeMicrosoftTeamsTool` |
| Agent Guidance | `packages/temporal/src/activities/task-agent/agent-execution.ts` |
| **Orchestrator Path** | |
| Preload Resources | `packages/temporal/src/activities/orchestrator/preload/preload-resources.ts` → `loadOAuthIntegrationTools` |
| Initialization | `packages/temporal/src/workflows/orchestrator/phases/initialization.ts` → passes `enabledIntegrationIds` |
| **UI** | |
| UI Plugin | `apps/web/modules/saas/workflows/lib/plugins/microsoft-teams/` |

## Debugging Tips

### Check if OAuth is configured
```typescript
// Temporary logging in oauth.ts isConfigured handler
console.log("[OAuth] Provider:", provider.name, "clientId exists:", !!clientId);
```

### Verify tools are loaded
In browser console on Fabric AI Agent page, check for tool loading logs.

### Check WorkflowIntegration record
```sql
SELECT * FROM "WorkflowIntegration"
WHERE provider = 'YOUR_PROVIDER' AND "isActive" = true;
```
