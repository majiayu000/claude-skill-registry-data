---
name: add-agents-mcp-server
description: Add an MCP (Model Context Protocol) server to a Mattermost plugin so the Agents plugin can call its tools. Use when implementing cross-plugin MCP, exposing AI tools from a Mattermost plugin to the Agents plugin, or wiring up the `pluginmcp` helper from mattermost-plugin-agents.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# Add Agents MCP Server

Add a cross-plugin MCP (Model Context Protocol) server to a Mattermost plugin so the [Mattermost Agents plugin](https://github.com/mattermost/mattermost-plugin-agents) can discover and call its tools. Uses the `github.com/mattermost/mattermost-plugin-agents/external/pluginmcp` helper, which handles tool-name namespacing, inter-plugin auth, user-ID propagation, and async registration retries.

## When to use this skill

Use this skill when a developer wants their Mattermost plugin to expose tools (look up records, query state, create artifacts) that the Agents plugin's LLM agents can call on the user's behalf. The reference implementation lives at `mattermost/mattermost-plugin-demo` (`server/mcp.go`, `server/mcp_tools.go`).

## Prerequisites

Before starting, confirm these against the target plugin:

- **Mattermost server**: 11.3 or newer (the helper uses `Plugin.PluginHTTPStream`).
- **Go**: 1.26+ (matches the demo plugin's `go 1.26.2`).
- **Plugin server code lives in `server/`** and uses `github.com/mattermost/mattermost/server/public/plugin` (the standard Mattermost plugin layout). If the plugin is webapp-only or uses a non-standard server layout, this skill does not apply.
- **`plugin.json` has a stable `id`** that is reverse-DNS style (e.g. `com.example.plugin-foo`) and **does not contain `__`**. Double-underscore is the namespace separator on the Agents side and a plugin ID containing `__` parses ambiguously.

No `plugin.json` changes are required — MCP integration is entirely server-side.

## Instructions

### Phase 0: Prepare the branch

1. Ensure the working tree is clean.
2. Switch to the default branch (`master` or `main`) and pull.
3. Create a feature branch: `git switch -c add-mcp-server`.

### Phase 1: Add dependencies

Edit `server/go.mod` (or the repo's `go.mod` if there is no separate server module) to add:

```
require (
    github.com/mattermost/mattermost-plugin-agents v0.0.0-<commit-from-master>
    github.com/modelcontextprotocol/go-sdk v1.4.1
)
```

Then run `go mod tidy` from the directory that owns `go.mod`.

If a tagged release of `mattermost-plugin-agents` that exports `external/pluginmcp/` is not yet available, ask the user whether to use a `replace` directive against a local checkout:

```
replace github.com/mattermost/mattermost-plugin-agents => ../mattermost-plugin-agents
```

### Phase 2: Add MCP server fields to the Plugin struct

Find the file declaring the `Plugin` struct (typically `server/plugin.go`). Add a thread-safe holder for the MCP server:

```go
import (
    "sync"

    "github.com/mattermost/mattermost-plugin-agents/external/pluginmcp"
)

type Plugin struct {
    plugin.MattermostPlugin
    // ... existing fields ...

    mcpServerLock sync.RWMutex
    mcpServer     *pluginmcp.Server
}
```

The lock guards lazy initialization in `OnActivate` and concurrent reads from `ServeHTTP`.

### Phase 3: Create `server/mcp.go`

This file owns the MCP server lifecycle. Use indirected `var` function references (`mcpNewServer`, `mcpRegister`, `mcpUnregister`) so tests can override them — this matches the demo plugin's pattern.

```go
package main

import (
    "errors"
    "net/http"
    "strings"

    "github.com/mattermost/mattermost-plugin-agents/external/pluginmcp"
)

const mcpBasePath = "/mcp"

var (
    mcpNewServer = pluginmcp.NewServer
    mcpRegister  = func(server *pluginmcp.Server) error {
        return server.Register()
    }
    mcpUnregister = func(server *pluginmcp.Server) error {
        return server.Unregister()
    }
)

func (p *Plugin) ensureMCPServer() error {
    p.mcpServerLock.Lock()
    defer p.mcpServerLock.Unlock()

    if p.mcpServer != nil {
        return nil
    }

    if manifest.Id == "" {
        return errors.New("plugin manifest id is required for MCP server")
    }
    if manifest.Version == "" {
        return errors.New("plugin manifest version is required for MCP server")
    }

    serverName := strings.TrimSpace(manifest.Name)
    if serverName == "" {
        return errors.New("plugin manifest name is required for MCP server")
    }

    server := mcpNewServer(p.API, pluginmcp.Config{
        PluginID:       manifest.Id,
        Name:           serverName + " MCP",
        Path:           mcpBasePath,
        ExposeExternal: false, // Defaults false. Directive: Ask the user whether they want this MCP server exposed externally or not - false is the default for security reasons.
        Version:        manifest.Version,
    })

    p.registerMCPTools(server)
    p.mcpServer = server
    return nil
}

func (p *Plugin) registerMCPServerBestEffort() {
    server := p.currentMCPServer()
    if server == nil {
        p.API.LogWarn("MCP registration unavailable; continuing plugin activation", "reason", "server not initialized")
        return
    }

    if err := mcpRegister(server); err != nil {
        p.API.LogWarn("MCP registration unavailable; continuing plugin activation", "err", err.Error())
    }
}

func (p *Plugin) unregisterMCPServerBestEffort() {
    server := p.currentMCPServer()
    if server == nil {
        return
    }

    if err := mcpUnregister(server); err != nil {
        p.API.LogWarn("MCP unregister failed; continuing plugin shutdown", "err", err.Error())
    }
}

func (p *Plugin) serveMCPIfMatch(w http.ResponseWriter, r *http.Request) bool {
    if r.URL.Path != mcpBasePath && !strings.HasPrefix(r.URL.Path, mcpBasePath+"/") {
        return false
    }

    server := p.currentMCPServer()
    if server == nil {
        http.NotFound(w, r)
        return true
    }

    server.ServeHTTP(w, r)
    return true
}

func (p *Plugin) currentMCPServer() *pluginmcp.Server {
    p.mcpServerLock.RLock()
    defer p.mcpServerLock.RUnlock()

    return p.mcpServer
}
```

`Register()` returns immediately and retries asynchronously (1s → 2s → 4s → 8s, up to 15 attempts) until the Agents plugin acknowledges, so plugin activation is not blocked when the Agents plugin is not yet up.

### Phase 4: Create `server/mcp_tools.go`

Define typed input/output structs and register each tool with `pluginmcp.AddTool`. Tool names are prefixed with `{pluginID}__` automatically — the LLM sees `com_example_plugin_foo__echo`, but you write `echo`.

```go
package main

import (
    "context"
    "fmt"

    "github.com/mattermost/mattermost-plugin-agents/external/pluginmcp"
    "github.com/mattermost/mattermost/server/public/model"
    "github.com/modelcontextprotocol/go-sdk/mcp"
)

type EchoArgs struct {
    Message string `json:"message" jsonschema:"The string to echo back,minLength=1"`
}

type EchoOutput struct {
    Echoed string `json:"echoed" jsonschema:"The same string that was passed in"`
}

type GetUserDisplayNameArgs struct{}

type GetUserDisplayNameOutput struct {
    UserID      string `json:"user_id" jsonschema:"Mattermost user ID of the caller"`
    Username    string `json:"username" jsonschema:"Username of the caller"`
    DisplayName string `json:"display_name" jsonschema:"Full-name display name of the caller, falling back to username"`
}

func (p *Plugin) registerMCPTools(server *pluginmcp.Server) {
    pluginmcp.AddTool(server, &mcp.Tool{
        Name:        "echo",
        Description: "Echo a string back to the caller. Useful for verifying the MCP round-trip.",
    }, p.echoHandler)

    pluginmcp.AddTool(server, &mcp.Tool{
        Name:        "get_user_display_name",
        Description: "Look up the calling user's display name.",
    }, p.getUserDisplayNameHandler)
}

func (p *Plugin) echoHandler(_ context.Context, _ *mcp.CallToolRequest, in EchoArgs) (*mcp.CallToolResult, EchoOutput, error) {
    return nil, EchoOutput{Echoed: in.Message}, nil
}

func (p *Plugin) getUserDisplayNameHandler(ctx context.Context, _ *mcp.CallToolRequest, _ GetUserDisplayNameArgs) (*mcp.CallToolResult, GetUserDisplayNameOutput, error) {
    userID := pluginmcp.GetUserID(ctx)
    if userID == "" {
        return nil, GetUserDisplayNameOutput{}, fmt.Errorf("no Mattermost user ID in tool context (did the request arrive via pluginmcp.ServeHTTP?)")
    }

    user, err := p.client.User.Get(userID)
    if err != nil {
        return nil, GetUserDisplayNameOutput{}, fmt.Errorf("failed to fetch user %s: %w", userID, err)
    }

    return nil, GetUserDisplayNameOutput{
        UserID:      user.Id,
        Username:    user.Username,
        DisplayName: user.GetDisplayName(model.ShowFullName),
    }, nil
}
```

Handler signature is the go-sdk's `mcp.ToolHandlerFor[In, Out]`:

```
func(context.Context, *mcp.CallToolRequest, In) (*mcp.CallToolResult, Out, error)
```

Return `(nil, out, nil)` and the helper packs `out` into a `CallToolResult`. Return a non-nil `*mcp.CallToolResult` to fully control the response (multi-content replies, `IsError`, etc.).

Replace the demo tools above with tools meaningful to the target plugin. Aim for **about 10 tools maximum** with union-typed args, not many narrow tools — every tool costs schema tokens in every LLM request.

### Phase 5: Wire into `OnActivate` / `OnDeactivate`

In the file with `OnActivate` (typically `server/activate_hooks.go` or `server/plugin.go`):

```go
func (p *Plugin) OnActivate() error {
    // ... existing activation logic ...

    if err := p.ensureMCPServer(); err != nil {
        return errors.Wrap(err, "failed to initialize MCP server")
    }
    p.registerMCPServerBestEffort()

    return nil
}

func (p *Plugin) OnDeactivate() error {
    // ... existing deactivation logic ...

    p.unregisterMCPServerBestEffort()
    return nil
}
```

Order matters:

- `ensureMCPServer` must run **after** `p.client = pluginapi.NewClient(...)` and any other initialization tool handlers depend on.
- `registerMCPServerBestEffort` must run after `ensureMCPServer`. `Register()` errors are logged and swallowed so a temporarily-down Agents plugin does not block activation.
- `unregisterMCPServerBestEffort` should run regardless of whether the rest of deactivation succeeded.

### Phase 6: Route MCP requests in `ServeHTTP`

Find the plugin's `ServeHTTP` method (typically `server/http_hooks.go` or `server/plugin.go`). Match the MCP path **before** falling through to the regular router:

```go
func (p *Plugin) ServeHTTP(c *plugin.Context, w http.ResponseWriter, r *http.Request) {
    if p.serveMCPIfMatch(w, r) {
        return
    }

    p.router.ServeHTTP(w, r)
}
```

Do **not** add an additional auth gate around `serveMCPIfMatch` — `pluginmcp.Server.ServeHTTP` already rejects requests that lack `Mattermost-Plugin-ID: mattermost-ai` (a header Mattermost strips on external requests, so only inter-plugin RPC sees it).

### Phase 7: Add a smoke test (recommended)

Create `server/mcp_tools_test.go` mirroring the demo plugin. The test wires `ServeHTTP` into a `httptest.Server`, sets `Mattermost-Plugin-ID: mattermost-ai`, and uses the go-sdk client to call `ListTools` / `CallTool`. See `mattermost-plugin-demo/server/mcp_tools_test.go` (branch `IDEA-006-cross-plugin-mcp`) for a full example.

Key test setup:

```go
const agentsPluginID = "mattermost-ai"

req.Header.Set("Mattermost-Plugin-ID", agentsPluginID)
req.Header.Set("X-Mattermost-UserID", "test-user-id") // only if testing user-context tools
```

### Phase 8: Verify

1. `make` (or `make dist`) to confirm the plugin builds.
2. `make test` to run unit tests.
3. `make check-style` to ensure no linter regressions.
4. Manual end-to-end test:
   - Install the Agents plugin (master/main branch with cross-plugin MCP support, see references).
   - Install this plugin.
   - In the Agents system console, open the **Tools** tab. The plugin's tools should appear as `{sanitized-plugin-id}__{tool-name}`, with per-tool policy controls.
   - Trigger a chat with an agent and exercise a tool.
   - Tail server logs for `Connected to plugin MCP server <pluginID>` from the Agents plugin — its absence means `Register()` never succeeded.

## Configuration reference

```go
type Config struct {
    PluginID       string // required; must equal plugin.json "id"
    Name           string // human-readable; shown in admin UI
    Path           string // your plugin's MCP endpoint, e.g. "/mcp"
    ExposeExternal bool   // if true, tools may appear on Agents' external MCP aggregate
                          // (still subject to admin Enabled toggle and per-tool policy)
    Version        string // optional; defaults to "0.0.1"
}
```

## API reference

- `pluginmcp.NewServer(api, cfg) *Server` — `p.API` satisfies the `PluginAPI` interface.
- `pluginmcp.AddTool[In, Out](s, tool, handler)` — free function, not a method, because Go disallows type parameters on methods.
- `(*Server).ServeHTTP(w, r)` — `http.Handler`; route to it from your `ServeHTTP` for requests under `cfg.Path`.
- `(*Server).Register() error` — start async registration; returns immediately, retries in a goroutine.
- `(*Server).Unregister() error` — synchronously cancels pending retries and POSTs one unregister.
- `pluginmcp.GetUserID(ctx) string` — returns the user ID stashed by `ServeHTTP`, or `""` if absent.

## Constraints and gotchas

- **Tool-name sanitization.** `AddTool` prepends `{sanitizedPluginID}__` to `tool.Name`, replacing any character outside `[A-Za-z0-9_-]` with `_` to satisfy Bifrost / Anthropic's `^[a-zA-Z0-9_-]{1,128}$`. If `tool.Name` already starts with the prefix, it is not duplicated.
- **`PluginID` must not contain `__`.** Use a normal reverse-DNS ID like `com.example.plugin-foo`.
- **`GetUserID` is trustworthy only inside a request that came through `pluginmcp.Server.ServeHTTP`.** External callers can't inject one. Don't read `X-Mattermost-UserID` directly from headers; always go through `GetUserID`.
- **Don't double-gate auth.** Adding your own plugin-ID check around `serveMCPIfMatch` is redundant and will likely break the helper's own check.
- **Registration is one-shot per `OnActivate`.** If the Agents plugin restarts later, the in-memory registration is lost on the Agents side. Admin-persisted entries are restored on Agents-plugin restart, but a never-saved registration only comes back when your plugin re-activates. Permanent (non-retriable) errors log `registration with Agents plugin failed permanently` and stop.
- **Tool budget.** Each tool costs ~20–200 schema tokens in every LLM request. Aim for ~10 tools per plugin, with union-typed args, over many narrow tools.
- **`ExposeExternal` vs admin `Enabled`.** Each register POST sends `expose_external` from your `Config`. Admins still control the server's `Enabled` state and per-tool policy in the Agents system console; those settings are preserved across re-registration.

## Troubleshooting

- **Tool doesn't appear in the admin Tools tab.** Look for `Connected to plugin MCP server <pluginID>` in the Agents-plugin log; absence indicates `Register()` was never called or kept failing. The retry loop logs `registration with Agents plugin gave up after N attempts` on terminal failure and `failed permanently` on a non-retriable 4xx.
- **`GetUserID` returns `""`.** Either the request didn't go through `pluginmcp.Server.ServeHTTP` (typical in unit tests — inject a context yourself), or your outer `ServeHTTP` isn't routing to it (check `mcpBasePath` matches your `Config.Path`).
- **Registration keeps retrying.** Common causes: Agents plugin disabled, in a crash loop, or `cfg.PluginID` doesn't match `plugin.json`'s `id` (the Agents plugin returns 403, which is non-retriable).
- **403 from `serveMCPIfMatch` during local curl.** Expected — Mattermost strips `Mattermost-Plugin-ID` on external requests. Test cross-plugin calls through the Agents plugin or a unit test that sets the header explicitly.

## References

- Helper package and reference docs: `mattermost-plugin-agents/external/pluginmcp/` (`README.md`, `pluginmcp.go`, `server.go`, `tools.go`, `context.go`, `registration.go`).
- Reference plugin implementation: `mattermost-plugin-demo` branch `IDEA-006-cross-plugin-mcp` — see `server/mcp.go`, `server/mcp_tools.go`, `server/activate_hooks.go`, `server/http_hooks.go`, and `server/mcp_tools_test.go`.
- MCP Go SDK: <https://github.com/modelcontextprotocol/go-sdk>.
