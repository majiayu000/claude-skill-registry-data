---
name: blazor-ag-ui-agent-framework
description: Build Blazor-native agent user interfaces using AG-UI protocol with Microsoft Agent Framework (MAF) and ASP.NET Core. Use when implementing the 7 AG-UI protocol features (agentic chat, backend tools, human-in-the-loop approvals, generative UI - async tools, tool-based UI rendering, shared state, and predictive state updates). Covers ASP.NET Core MapAGUI endpoints, Agent Framework integration, Blazor component rendering, SSE streaming architecture, and 2026 UX patterns for agentic interfaces (Dual-Pane Architecture, Observable Plans, HITL governance).
metadata: 
   version: 2.1.0
   author: arisng
---

# AG-UI Blazor + Agent Framework (MAF)

**Version 2.1** - Enhanced with 2026 Agentic UX patterns plus Microsoft Agent Framework Release Candidate guidance (stable API surface, migration paths from Semantic Kernel/AutoGen, and updated package strategy).

## RC Update (Feb 2026)

Use this skill with the Microsoft Agent Framework Release Candidate mindset:
- Treat core `Microsoft.Agents.AI` APIs as stable for production planning.
- Prefer current RC packages and pin versions explicitly in samples and implementation checklists.
- Keep migration guidance ready for teams moving from Semantic Kernel or AutoGen.
- Preserve interoperability-first design: AG-UI for UI runtime events, MCP for tools, and A2A for agent-to-agent boundaries.

## Quick Start

For a basic ASP.NET Core agent with Blazor frontend:

1. Install NuGet package: `Microsoft.Agents.AI.Hosting.AGUI.AspNetCore`
2. Create an `AIAgent` using `IChatClient` (Azure OpenAI, OpenAI, Ollama)
3. Map the AG-UI endpoint: `app.MapAGUI("/api/chat", agent)` in ASP.NET Core startup
4. In Blazor: Connect via HTTP POST + Server-Sent Events (SSE)
5. Parse AG-UI protocol events; render messages and tool UIs dynamically

**Architectural Foundation - Dual-Pane Pattern:**
- Implement **Context Pane** (chat/negotiation) + **Canvas Pane** (artifact/work product) separation
- This is the 2026 standard for agentic interfaces - enables co-creation workflows
- See [blazor-dual-pane-implementation.md](references/blazor-dual-pane-implementation.md) for component structure

**Triggering Generative UI**: Use intent keywords in prompts:
- "Make an interactive..." (highest success rate)
- "Create an interactive..."
- "Simulate... with adjustable..."
- Keep interfaces focused: specify 2-4 controls per prompt for cleaner layouts

For approval workflows, observability, or shared state, see full workflow below.

## Generative UI patterns (2026): pick the right level of freedom

Generative UI (GenUI) is when the agent influences the interface at runtime (structured inputs, progress UI, dynamic panels), not just text. This is a key shift from the "Conversational Era" (2023-2024) to the "Agentic Era" (2025-2026+), where interfaces must support autonomous, multi-step workflows rather than simple Q&A.

AG-UI is the **runtime event/state protocol** that enables GenUI; it is not a UI specification.

**The GenUI Spectrum** (from most controlled to most flexible):

1. **Static GenUI (AG-UI-style)** — Prebuilt UI components; the agent decides *when* to show them and *what data* they receive.
   - **Best for**: Enterprise apps, high-risk workflows, customer support
   - **Pros**: High polish, perfect brand consistency, zero security risk
   - **Cons**: Limited vocabulary - can't generate novel UIs

2. **Declarative GenUI (A2UI / Adaptive Cards)** — The agent returns a constrained UI description (JSON); the app renders it with validation/whitelisting.
   - **Best for**: General-purpose assistants, business process automation, "Canvas" apps
   - **Pros**: High flexibility, secure (no arbitrary code), framework-agnostic
   - **Cons**: Generic appearance; requires schema validation
   - **⭐ Recommended for baseline implementation** (balances flexibility with safety)

3. **Open-ended GenUI (MCP Apps / Claude Artifacts)** — The agent generates raw HTML/CSS/JS or executes code in a sandbox.
   - **Best for**: Prototyping tools, data visualization explorers, coding assistants
   - **Pros**: Infinite flexibility; can build novel interfaces
   - **Cons**: High security risk (XSS, data exfiltration), performance overhead
   - **⚠️ Use only in sandboxed "Playground" modes**

This skill primarily focuses on **Static GenUI in Blazor** (tool lifecycle → Blazor components), while pointing to safe extension paths for declarative/open-ended approaches.

## The 7 AG-UI Protocol Features & Agent Framework Support

Agent Framework's AG-UI integration supports all 7 standardized protocol features:

1. **Agentic Chat** — Streaming chat with automatic tool calling (no manual parsing)
2. **Backend Tool Rendering** — Tools execute server-side via `AIFunctionFactory`; results stream to client
3. **Human-in-the-Loop** — `ApprovalRequiredAIFunction` middleware converts to approval protocol events
4. **Agentic Generative UI** — Async tools with progress updates for long-running operations
5. **Tool-Based UI Rendering** — Custom Blazor components render based on tool definitions
6. **Shared State** — Bidirectional state synchronization between agent and Blazor client
7. **Predictive State Updates** — Stream tool arguments as optimistic updates before execution

Each feature maps directly to Agent Framework abstractions: `AIAgent`, `IChatClient`, `AIFunctionFactory`, `ApprovalRequiredAIFunction`, `ConversationId`, and tool metadata serialization.

## Full Workflow

1. **Install AG-UI hosting package**
   - `dotnet add package Microsoft.Agents.AI.Hosting.AGUI.AspNetCore`
   - Includes all dependencies: Agent Framework, Extensions.AI, protocol implementation
   - For deterministic builds, pin package versions in docs and scripts instead of floating latest

2. **Create an AIAgent** from IChatClient
   - Wire a chat client (Azure OpenAI, OpenAI, Ollama, etc.)
   - Add tools using `AIFunctionFactory.Create()`
   - Optional: wrap with middleware for approvals or state management
   - See [mslearn-ag-ui-getting-started.md](references/mslearn-ag-ui-getting-started.md)

3. **Map the AG-UI endpoint** in ASP.NET Core
   - Use `app.MapAGUI("/api/chat", agent)` to expose agent as HTTP endpoint
   - Handles HTTP POST requests + Server-Sent Events (SSE) streaming automatically
   - Manages ConversationId for session context

4. **Implement Dual-Pane Architecture** (core UX pattern)
   - Build **Context Pane** (left/sidebar): chat, approvals, memory inspector
   - Build **Canvas Pane** (right/main): artifact viewer/editor with versioning
   - Implement **Contextual Scoping**: highlight-to-prompt for spatial referencing
   - Enable **State Synchronization**: JSON Patch over SSE for delta updates
   - See [blazor-dual-pane-implementation.md](references/blazor-dual-pane-implementation.md) for complete implementation

5. **Add Observability** (build trust via transparency)
   - Implement **Accordion of Thought**: collapsible reasoning steps (reduces anxiety by 34%)
   - Show **Chain of Thought**: expose agent's reasoning process progressively
   - Build **Memory Inspector**: visualize active facts, context utilization, tool availability
   - Display **Tool Execution**: show what the agent is doing in real-time
   - See [blazor-observability-patterns.md](references/blazor-observability-patterns.md) for component patterns

6. **Implement Human-in-the-Loop workflows** (governance & control)
   - Use **Approval Queue**: non-blocking, inline approval cards (not modals)
   - Implement **Reversibility**: checkpoint system with time-travel UI
   - Add **Diff Previews**: show before/after for code/document changes
   - Create **Panic Button**: emergency stop that halts + reverts state
   - Risk-based escalation: high-risk actions require confirmation, low-risk proceed autonomously
   - See [blazor-hitl-patterns.md](references/blazor-hitl-patterns.md) for HITL patterns
   - Wrap sensitive functions with `ApprovalRequiredAIFunction` on server-side

7. **Implement backend tools**
   - Define tools that execute server-side: search, database queries, API calls
   - Results stream to client via AG-UI protocol
   - See [mslearn-backend-tool-rendering.md](references/mslearn-backend-tool-rendering.md)

8. **Build frontend UI in Blazor**
   - Connect to HTTP endpoint + SSE stream via `HttpClient` and event parsing
   - Implement Blazor components that parse AG-UI protocol events
   - Display chat messages, tool calls, approval requests, and progress updates
   - Handle SSE streaming: append-only event stream, throttle for performance
   - **Validation**: Sanitize HTML, validate JSON structure before rendering
   - **Error handling**: Display partial results on stream failure; provide clear error messages
   - See [blazor-ag-ui-genui-patterns.md](references/blazor-ag-ui-genui-patterns.md) for component patterns
   - Reference: [copilotkit-generative-ui.md](references/copilotkit-generative-ui.md) for UX/GenUI design patterns (framework-agnostic)

9. **Implement generative UI in Blazor** (optional)
   - Use async tools for long-running operations with progress callbacks
   - Render custom Blazor components based on tool definitions (slots, templates)
   - Implement shared state synchronization: parse state events, update Blazor component state bidirectionally
   - Use predictive updates: render tool arguments optimistically before confirmation
   - See [blazor-ag-ui-genui-patterns.md](references/blazor-ag-ui-genui-patterns.md) for Blazor-specific implementation

10. **Extend beyond static GenUI** (optional)
    - **Declarative GenUI**: add a validated, schema-versioned renderer for a constrained UI spec (e.g., cards/forms/tables)
    - **Open-ended GenUI**: embed external UI surfaces only with strict origin allowlists and server-side authorization
    - See [generative-ui-2026-patterns.md](references/generative-ui-2026-patterns.md) for selection guidance and mappings

11. **Mobile adaptation** (if building responsive/mobile apps)
    - Replace side-by-side panes with modal layers (drawer/sheet patterns)
    - Use selection-heavy inputs (chips, carousels) to minimize typing
    - Implement gesture-based navigation (swipe to dismiss artifacts)
    - Optimize for touch: large targets, bottom-heavy UI, sticky controls
    - See [blazor-mobile-patterns.md](references/blazor-mobile-patterns.md)

12. **Validate protocol compliance and UX**
    - Test event serialization and SSE streaming
    - Ensure session management via ConversationId
    - Verify tool call lifecycle (queued → executing → succeeded/failed)
    - Test accessibility: focus management, `aria-live`, keyboard nav
    - Verify observability: users can see agent reasoning and state
    - Test approval workflows: non-blocking, reversible, with diff previews

13. **Apply migration checks for existing agent stacks**
   - If project currently uses Semantic Kernel or AutoGen, map key workflows to Agent Framework abstractions (`AIAgent`, workflows, tools, approvals)
   - Validate behavior parity for multi-agent orchestration before cutover
   - Keep rollback path for one release cycle during migration

### Core Protocol & Setup
- **7 Features & Agent Framework support**: [ag-ui-protocol-overview.md](references/ag-ui-protocol-overview.md) — All 7 features, Agent Framework abstractions, protocol contracts
- **Getting started** (Step 2-3): [mslearn-ag-ui-getting-started.md](references/mslearn-ag-ui-getting-started.md) — MapAGUI setup, IChatClient wiring, C# examples
- **Backend tools** (Step 7): [mslearn-backend-tool-rendering.md](references/mslearn-backend-tool-rendering.md) — AIFunctionFactory usage, tool metadata, streaming results
- **Blazor SSE & event parsing** (Step 8): [mslearn-frontend-tool-rendering.md](references/mslearn-frontend-tool-rendering.md) — SSE parsing, protocol event structures, Blazor integration

### UX Architecture & Implementation (2026 Patterns)
- **Dual-Pane Architecture** (Step 4): [blazor-dual-pane-implementation.md](references/blazor-dual-pane-implementation.md) — Context Pane + Canvas Pane structure, highlight-to-prompt, state synchronization, JSON Patch integration
- **Observability Patterns** (Step 5): [blazor-observability-patterns.md](references/blazor-observability-patterns.md) — Accordion of Thought, Chain of Thought UI, Memory Inspector, Swarm Status visualization
- **Human-in-the-Loop** (Step 6): [blazor-hitl-patterns.md](references/blazor-hitl-patterns.md) — Approval queues, reversibility (time travel UI), diff previews, panic button, risk-based escalation
- **Mobile Patterns** (Step 11): [blazor-mobile-patterns.md](references/blazor-mobile-patterns.md) — Drawer/sheet patterns, selection-heavy inputs, gesture navigation, responsive adaptation

### Generative UI
- **Blazor GenUI patterns** (Step 8-9): [blazor-ag-ui-genui-patterns.md](references/blazor-ag-ui-genui-patterns.md) — Component composition, DynamicComponent rendering, state flow, shared state in Blazor
- **GenUI pattern selection**: [generative-ui-2026-patterns.md](references/generative-ui-2026-patterns.md) — Static vs declarative vs open-ended GenUI, and how they map to Blazor + AG-UI
- **UX/GenUI design** (reference only): [copilotkit-generative-ui.md](references/copilotkit-generative-ui.md) — Framework-agnostic UX patterns, async tool design, shared state concepts

### Middleware & Advanced
- **Approvals**: [approvals-human-in-the-loop.md](references/approvals-human-in-the-loop.md) — ApprovalRequiredAIFunction, middleware, approval event protocol
4. **Throttle rendering**: Batch rapid SSE updates to avoid render thrash in Blazor
5. **Graceful degradation**: If tool execution fails, display cached/partial results with retry option

## Real-World Applications

**When to use AG-UI with Blazor + MAF:**

1. **Rapid Prototyping**: Generate functional UIs in minutes for testing product concepts or client demos
2. **Custom Dashboards**: Create personalized analytics interfaces tailored to specific metrics and user roles
3. **Educational Tools**: Build interactive simulations and adaptive learning experiences
4. **Internal Tools**: Generate admin panels, form builders, and workflow managers without dedicated frontend dev
5. **Dynamic Forms**: Create context-aware forms that adapt based on user inputs and agent reasoning

**Selection criteria**: Use static GenUI (prebuilt Blazor components) for high-risk workflows; consider declarative GenUI for flexibility with validation.

## References

**When to read each reference:**

- **7 Features & Agent Framework support**: [ag-ui-protocol-overview.md](references/ag-ui-protocol-overview.md) — All 7 features, Agent Framework abstractions, protocol contracts
- **Getting started** (Step 2-3): [mslearn-ag-ui-getting-started.md](references/mslearn-ag-ui-getting-started.md) — MapAGUI setup, IChatClient wiring, C# examples
- **Backend tools** (Step 4): [mslearn-backend-tool-rendering.md](references/mslearn-backend-tool-rendering.md) — AIFunctionFactory usage, tool metadata, streaming results
- **Blazor SSE & event parsing** (Step 6): [mslearn-frontend-tool-rendering.md](references/mslearn-frontend-tool-rendering.md) — SSE parsing, protocol event structures, Blazor integration
- **Blazor component patterns** (Step 6-7): [blazor-ag-ui-genui-patterns.md](references/blazor-ag-ui-genui-patterns.md) — Component composition, DynamicComponent rendering, state flow, shared state in Blazor
### Architecture & Protocol
- **Architecture**: Use `MapAGUI` for endpoint management. Session context flows via `ConversationId` — include in all Blazor requests.
- **Transport**: AG-UI uses HTTP POST + Server-Sent Events (SSE). Blazor Server can use SignalR; ensure Blazor WASM uses SSE fallback.
- **7 Features**: Verify all 7 AG-UI features are implemented (chat, backend tools, approvals, async tools, tool-based UI, shared state, predictive updates).
- **Tools**: Define via `AIFunctionFactory.Create()`. Wrap sensitive tools with `ApprovalRequiredAIFunction`. Test JSON schema serialization.

### UX Patterns (2026 Standards)
- **Dual-Pane**: Always implement Context Pane (chat/meta) + Canvas Pane (artifact/work) separation. Don't put work products inside chat bubbles.
- **Observability**: Expose Chain of Thought. Default to collapsed but expandable. Show active tool execution. Research shows 34% reduction in "black-box anxiety" with visible reasoning.
- **HITL**: Use non-blocking approval queues, NOT blocking modals. Implement reversibility (checkpoints). Show diff previews for code/document changes. High-risk actions must require confirmation.
- **Co-Creation vs Slot Machine**: Enable persistent artifact manipulation, not just transactional Q&A. Users should edit artifacts directly, not regenerate from scratch.

### Prompting & GenUI
- **Prompting**: Use intent keywords ("Make an interactive...", "Create...") to trigger GenUI. Specify 2-4 controls per prompt for cleaner layouts. Test prompt patterns for consistent GenUI activation.
- **GenUI safety**: Default to Static GenUI for high-risk flows. If implementing declarative UI, validate against a schema and whitelist components. If embedding open-ended UI surfaces, isolate/sandbox and enforce strict origin allowlists + server-side authz.
- **GenUI Selection**: Static GenUI for enterprise apps. Declarative GenUI (A2UI/Adaptive Cards) for general-purpose. Open-ended GenUI ONLY in sandboxed playground modes.

### Technical Implementation
- **Validation**: Always sanitize HTML and validate JSON structure before rendering. Use JSON schema validation for structured outputs to ensure type-safe components.
- **Blazor**: Parse AG-UI events safely. Use DynamicComponent for tool UI rendering. Don't block SSE reads; throttle updates (100-200ms batches) to avoid render thrash. Implement graceful degradation for partial failures.
- **State Management**: Use JSON Patch (RFC 6902) for delta updates over SSE. Server is authoritative for artifact state. Consider CRDTs (Yjs/Automerge) for real-time collaboration.
- **Performance**: Stream progressively for perceived speed. Balance quality vs latency based on use case. Include only necessary context in agent calls. Virtualize long lists. Lazy-load details.

### Governance & Control
- **Approval Policies**: Define risk levels (high/medium/low) per action. High-risk: delete, production ops, large-scale changes. Auto-approve low-risk after timeout.
- **Reversibility**: Create automatic checkpoints before every agent action. Enable "undo" and "time travel" UI. Panic button stops execution AND reverts state.
- **Audit Trail**: Log all approvals/rejections with ConversationId for traceability and compliance.

### Mobile & Accessibility
- **Mobile**: Use drawer/sheet patterns instead of side-by-side panes. Bottom-heavy UI for thumb zone. Minimize typing with chips/carousels. Support gestures (swipe to dismiss).
- **Accessibility**: `aria-live` for streaming updates. `aria-expanded` for accordions. Large touch targets (44x44pt minimum). Support dark mode and reduced motion.

### Debugging
- **Traceability**: Log ConversationId with all tool invocations and approval requests.
- **Error Visibility**: Show partial results on stream failure. Provide retry mechanisms. Expose reasoning traces for debugging agent behavior

- **Architecture**: Use `MapAGUI` for endpoint management. Session context flows via `ConversationId` — include in all Blazor requests.
- **Transport**: AG-UI uses HTTP POST + Server-Sent Events (SSE). Blazor Server can use SignalR; ensure Blazor WASM uses SSE fallback.
- **7 Features**: Verify all 7 AG-UI features are implemented (chat, backend tools, approvals, async tools, tool-based UI, shared state, predictive updates).
- **Tools**: Define via `AIFunctionFactory.Create()`. Wrap sensitive tools with `ApprovalRequiredAIFunction`. Test JSON schema serialization.
- **Prompting**: Use intent keywords ("Make an interactive...", "Create...") to trigger GenUI. Specify 2-4 controls per prompt for cleaner layouts. Test prompt patterns for consistent GenUI activation.
- **Validation**: Always sanitize HTML and validate JSON structure before rendering. Use JSON schema validation for structured outputs to ensure type-safe components.
- **Blazor**: Parse AG-UI events safely. Use DynamicComponent for tool UI rendering. Don't block SSE reads; throttle updates to avoid render thrash. Implement graceful degradation for partial failures.
- **Performance**: Stream progressively for perceived speed. Balance quality vs latency based on use case. Include only necessary context in agent calls.
- **GenUI safety**: Default to Static GenUI for high-risk flows. If implementing declarative UI, validate against a schema and whitelist components. If embedding open-ended UI surfaces, isolate/sandbox and enforce strict origin allowlists + server-side authz.
- **Debugging**: Log ConversationId with all tool invocations and approval requests for traceability.
