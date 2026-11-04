---
name: add-agent-tool
description: >-
  Add an Agent-callable tool to Greenhouse: defineTool with meta and implementation in one file,
  registered in CORE_TOOL_MODULES (core, apps/api/src/tools) or a plugin's defineExtension tools
  (plugins/<id>/api), surface deciding proxy/MCP exposure, a grant path (global, Advanced tools
  bucket or a plugin feature point), description rules and guard tests. Use for: add a tool / agent
  tool / function calling / let the model call X, 加个工具, 新增 agent tool, 让模型能调用 xx.
  Red lines: no tools/index.ts, meta lives with the implementation, writes declare proxy 'write',
  every non-global tool has exactly one grant path.
---

# Add an Agent tool

Source of truth: the header comments of apps/api/src/tools/define.ts (field semantics), apps/api/src/AGENTS.md "Tool catalog and proxy", EXTENDING.md "Requests, permissions and writes". On conflict those win.

## Decide first
- Can an existing tool take one more `action`? Most tools are action-enum query/mutation pairs; register why a new tool is needed.
- Core or plugin: plugin data belongs in plugins/<id>/api; a plugin dataSource already derives `<plugin>_query` and optional `<plugin>_mutation`, so do not hand-register duplicates.
- Every tool dilutes the model's attention; prefer fewer, sharper tools.

## Step 1: meta + implementation in one file
- Core: apps/api/src/tools/<name>.ts (a folder such as compute/ or external-search/ when large). Plugin: plugins/<id>/api/<name>.ts importing defineTool from @greenhouse/api/extension-kit.
```typescript
import { tool } from 'ai';
import { z } from 'zod';
import { defineTool, type ToolMeta } from './define.js';

const meta: ToolMeta = {
  id: 'widget_query',            // global, snake_case
  name: 'Widgets',               // display name
  brief: 'List my widgets',      // catalogs and permission UI; never injected into prompts
  description: 'Full model-facing usage …',
  category: 'team',              // 'core' | 'team' | 'admin'
  is_global: false,
  icon: 'Wrench',                // Lucide name
  sort_order: 50,
  surface: { proxy: 'read', mcp: '<group>', unattendedReplaySafe: true },
};

export const widgetQueryTool = defineTool({
  meta,
  kind: 'static',
  create: () =>
    tool({
      description: meta.description,
      inputSchema: z.object({ action: z.enum(['list', 'get']).describe('What to do') }),
      execute: async ({ action }) => ({ action }),
    }),
});
```
- Every zod field has `.describe()`; the AI SDK description is `meta.description`, never a second copy.
- `kind: 'static'` builds once (`create` receives the shared db); `kind: 'lazy'` builds per request from the caller.
- Plugin lazy tools implement `createLazy(ctx)` (LazyToolContext: db, userId, userRole, sessionId…); see plugins/example/api/tool.ts.
- Core lazy tools omit create and get a branch in buildLazyServerTools (apps/api/src/agent-runtime/tool-resolution.ts), session-bound ones under `if (sessionId)`; the generic createLazy path is walked only for plugin tools.

## Step 2: register
- Core: import the module explicitly in apps/api/src/tools/registry.ts and add it to CORE_TOOL_MODULES; there is no tools/index.ts and no glob registration.
- Plugin: list it in `tools: [...]` of defineExtension; the registry appends active plugin tools and derives every set.
- `routes/chat.ts` never imports tools/registry.ts; tool-metadata logic lives in agent-runtime/tool-resolution.ts.

## Step 3: surface (proxy and MCP)
- No surface: neither proxied (/api/agent) nor on MCP (/api/mcp); chat and automations still assemble it.
- `proxy: 'read'`: read-only proxy set, no confirm gate. `proxy: 'write'`: mutating set, `confirm: true` on every proxy call.
- `mcp: '<group>'`: also on MCP inside that consent group; it needs a proxy tier too. Core groups are McpResourceGroup (@greenhouse/types/mcp); plugins add `mcpGroups`.
- A tool that changes data declares `proxy: 'write'`; never label a write as read. A tool mixing reads and writes gets no surface (the memory tool).
- `unattendedReplaySafe`: may run with nobody present and be replayed; paid calls and reads that create durable objects stay false.
- `unattendedDenied`, `interactiveOnly`, `openWorld`, `additiveOnly`, `externalOnly`, `builtin`, `runtime_risk`: read their define.ts comments before setting them.
- `builtin` only widens profile filtering, never member permissions.

## Step 4: grant path
- `is_global: true`: every internal member gets it without assignment.
- A non-global tool reaches team members through exactly one path: a plugin feature point's `toolIds` (rides its flag) or the core "Advanced tools" bucket (toolsetToolIds in apps/api/src/plugin-host/feature-points.ts), assigned per member in the Admin place's permissions dialog.
- A flag-owned plugin tool missing from its feature point leaks into the bucket and bypasses the flag; plugin-host/__tests__/feature-point-parity.test.ts catches both mistakes.
- Unattended runs: UNATTENDED_TOOL_DENYLIST (agent-runtime/tool-policy.ts) and filterUnattendedToolIds; opt-ins come from @greenhouse/types/automation-tools plus plugin automationTools and never widen permissions.

## Step 5: description and error text (they are prompt)
- Declared capabilities must work; unconfigured paths return an explicit error.
- Errors name the next step ("use search to find the id"), never a tool the caller lacks.
- Quote interpolated values: `(ID: "${id}", Name: "${name}")`, so friction mining groups them.
- Search tools tell an empty corpus from a miss.
- Openable rows carry `url` from entityUrl() (@greenhouse/types/entity-links); cite with CITE_URL_INSTRUCTION (tools/cite-url.ts).
- Constants interpolated into descriptions live in zero-import leaf modules (plugins/memory/api/llm/memory-limits.ts); registry.ts imports every tool, so a cycle is a TDZ crash at boot while units stay green.
- New text must fit tools/__tests__/description-budget.test.ts; cut duplication before raising the budget.
- Prompts and profile YAML never restate a tool's rules; built-in profiles use `tools: []`, so a new tool needs no sprouty.yaml edit.

## Step 6: client wording (optional)
- The client humanizes unknown ids; for a friendly step label add the id to KNOWN_TOOLS (apps/client/src/chat/tool-words.ts) with `tools.name.<id>` and `tools.doing.<id>` in apps/client/src/lib/i18n/en.ts and zh.ts.

## Step 7: tests
- Tool tests in tests/api/, apps/api/src/tools/__tests__/ or plugins/<id>/api/__tests__/: each action, validation, permission denial; real-DB cases as *.db.test.ts.
- tools/__tests__/surface-derivation.test.ts pins the exact membership of every derived core set (proxy read/write, MCP groups, lazy ids); update it to the intended change.
- Plugin write tools also cover governed writes: preview before `confirm: true` on delete-like actions (plugins/example/api/__tests__/example-write-tool.db.test.ts).
- A dynamic import() of a CJS package uses `default`; vitest interop hides the bug, so load the real file with tsx or node once.

## Gate
```bash
pnpm typecheck
pnpm lint
TEST_DATABASE_URL=<loopback test db> pnpm test
DATABASE_URL=<loopback e2e db> pnpm test:e2e:ci   # when proxy or MCP exposure changed
```
Plugin tools also run `pnpm plugins:sync --check` and `pnpm test:core` (quality-gate).

## Checklist
- [ ] Extending an existing tool ruled out; core vs plugin decided
- [ ] meta and implementation in one file via defineTool; description = meta.description
- [ ] Registered (CORE_TOOL_MODULES or defineExtension tools); lazy wiring done
- [ ] surface chosen deliberately; writes are proxy 'write'; mcp has a proxy tier
- [ ] Exactly one grant path; feature point toolIds updated for flag-owned tools
- [ ] Error text names the next step and quotes values; constants in leaf modules
- [ ] Guard tests updated to the intended sets; gate green
