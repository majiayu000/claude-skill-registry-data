---
name: barbatos-mcp-ai
description: "MCP servers and bring-your-own-key AI in Barbatos.Wpf.Core (Barbatos.Wpf.Mcp) - ConfigureMcp, IMcpServerRegistry (stdio/HTTP, OAuth), IAiApiKeyProvider, IAiChatClientFactory, IAiChatService, IAiAgentFactory tool approval, IAiSessionStore. Use for an AI chat or assistant panel, end users pasting their own OpenAI/Gemini/Claude API key so the publisher never pays, a provider or model picker, connecting or signing in to an MCP server, confirming before a tool runs, keeping a conversation after restart, sending an image, or when the AI ignores the tools or a server never connects. For SecureStorage outside AI use barbatos-wpf-essentials. Vietnamese prompts too - chat AI, trợ lý ảo, tự nhập khóa API, chọn mô hình, kết nối MCP server, hỏi trước khi chạy tool, lưu hội thoại, gửi ảnh cho AI."
---

# Barbatos.Wpf.Mcp - MCP servers + BYOK AI

An MCP client plus a bring-your-own-key chat/agent layer inside `Barbatos.Wpf.Core` (types in
`Barbatos.Wpf.Mcp`, `ConfigureMcp` in `Barbatos.Wpf.Hosting`), composing `Microsoft.Extensions.AI`,
the official MCP C# SDK (`ModelContextProtocol.Core`) and the Microsoft Agent Framework
(`AIAgent`) without wrapping them. The analogue is Claude Desktop/Cursor: a user-managed server
list, an `env` block per stdio server, the user's own key. Not here: `ISecureStorage` itself
(`barbatos-wpf-essentials`), the builder and other `ConfigureXxx` features (`barbatos-wpf-host`).

## BYOK is non-negotiable

**The application publisher never pays for LLM usage.** The end user enters their own key in a
settings screen the app builds; `IAiApiKeyProvider` stores it DPAPI-encrypted via `ISecureStorage`.
Never bake a key into code, `appsettings.json`, an options default or a test fixture, and never add
an API that routes usage through a publisher-owned account. `AiProviderOptions` deliberately has no
key or secret field - do not add one. OAuth follows suit: consent happens in the user's browser.

## Sources of truth

- Docs: README [AI chat + MCP](../../../src/Barbatos.Wpf.Core/README.md#ai-chat--mcp-barbatoswpfmcp)
  ([OAuth](../../../src/Barbatos.Wpf.Core/README.md#hosted-servers-that-need-a-sign-in-oauth),
  [Agents](../../../src/Barbatos.Wpf.Core/README.md#agents-microsoft-agent-framework),
  [Providers](../../../src/Barbatos.Wpf.Core/README.md#providers),
  [Models](../../../src/Barbatos.Wpf.Core/README.md#models-iaimodelcatalog),
  [Attachments](../../../src/Barbatos.Wpf.Core/README.md#attachments-images-documents),
  [Configuration](../../../src/Barbatos.Wpf.Core/README.md#configuration)) and
  [API-REFERENCE `Barbatos.Wpf.Mcp`](../../../src/Barbatos.Wpf.Core/API-REFERENCE.md#barbatoswpfmcp-namespace).
- Code wins over docs: `src/Barbatos.Wpf.Core/Essentials/Mcp/` - `AppHostBuilderExtensions.cs`,
  `McpServerRegistry.cs` (status lifecycle, OAuth wiring), `AiChatClientFactory.cs` (provider
  split, caching), `AiAgentFactory.cs` (approval wrapping, invalidation), `Providers/`.
- Sample: `samples/Barbatos.Wpf.Core.Sample/` - `WpfProgram.cs` (`ConfigureMcp`),
  `MainViewModel.cs` (settings save, model refresh, OAuth buttons, streaming agent loop, inline
  approval panel), `MainWindow.xaml` ("AI Chat + MCP" tab).
- Tests that pin behaviour: `tests/Barbatos.Wpf.Core.UnitTests/McpFeatureTests.cs` (registration,
  routing, model catalog, tool merging), `McpOAuthTests.cs`, `AgentFeatureTests.cs` (wrapping,
  caching, approval round trip, sessions), `FeatureTestFakes.cs`.
- [patterns.md](patterns.md) - read when building the settings screen, a streaming chat with an
  inline approval panel, OAuth buttons, a resume list, a replacement seam, or a test for these.

## Registration

```csharp
using Barbatos.Wpf.Hosting;
using Barbatos.Wpf.Mcp;

builder.ConfigureMcp(
    options => options.Servers.Add(new McpServerDescriptor
    {
        Name = "NuGet",
        TransportKind = McpTransportKind.Stdio,
        Command = "dotnet",
        Arguments = { "dnx", "NuGet.Mcp.Server", "--version", "<version>", "--yes" },
        EnvironmentVariables = { ["NUGET_SOURCE"] = "https://api.nuget.org/v3/index.json" },
    }),
    configureProvider: options =>
    {
        options.Providers.Add(new AiProviderDescriptor { Key = "openai", Provider = "openai", Model = "<model-id>" });
        options.Providers.Add(new AiProviderDescriptor { Key = "gemini", Provider = "gemini", Model = "<model-id>",
            Endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/" });
        options.Providers.Add(new AiProviderDescriptor { Key = "anthropic", Provider = "anthropic", Model = "<model-id>" });
        options.Provider = "gemini";            // active on startup - copy all three fields
        options.Model = "<model-id>";
        options.Endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/";
    },
    configureAgent: options =>
    {
        options.Name = "Assistant";
        options.Instructions = "Be concise.";   // ToolApproval stays AiToolApprovalMode.Always
    });
```

Adapted from `WpfProgram.cs` (the `EnvironmentVariables` line is the README's); all three
parameters are optional. The `dnx` form was verified by running it: `--version` is a separate
flag - a `pkg@version` id failed to resolve.

| Section | Options type | Holds |
| --- | --- | --- |
| `Barbatos:Mcp` | `McpOptions` | `Enabled` (default `true`), `Servers` |
| `Barbatos:Mcp:Provider` | `AiProviderOptions` | `Provider` (default `"openai"`), `Model` (default `null`), `Endpoint`, `Providers` |
| `Barbatos:Mcp:Agent` | `AiAgentOptions` | `Name` (`"Assistant"`), `Description`, `Instructions`, `ToolApproval` (`Always`), `IncludeMcpTools` (`true`), `EnableLogging` (`true`), `EnableOpenTelemetry` (`false`), `OpenTelemetrySourceName` (`"Barbatos.Wpf.Mcp"`) |

- File values override code values (`ConfigurationOverridesCodeForProviderOptions`,
  `ConfigurationOverridesCodeForAgentOptions`). The provider name key is
  `Barbatos:Mcp:Provider:Provider`, not `Barbatos:Mcp:Provider`.
- `Servers` and `Providers` do bind from array-index keys (`ProvidersListBindsFromConfiguration`),
  but seed them from code - `Providers:0:Key` is unwieldy to hand-author.
- **Everything is read once.** Seed servers connect during `builder.Build()` (fire-and-forget,
  one task per server; a connect failure is logged and recorded on its status, a `Validate()`
  failure only logged, never fatal; `Enabled = false` skips only this). The chat client factory
  snapshots provider/model/endpoint and the `Providers` catalog; the agent factory keeps `AiAgentOptions.Value`. Change things at runtime
  through the APIs below, not through options.
- With `WpfApp.CreateBuilder(useDefaults: false)`, call `builder.UseEssentials()` first: the
  defaults need `ISecureStorage`, `IFileSystem` and `ILauncher`, and `Build()` resolves the
  registry for the startup connect.

Every service is `TryAddSingleton`, so a registration made **before** `ConfigureMcp` wins
(`CustomApiKeyProviderRegisteredBeforeConfigureMcpTakesPrecedence`):

| Interface | Default | Replace when |
| --- | --- | --- |
| `IAiApiKeyProvider` | `SecureStorageAiApiKeyProvider` (DPAPI, current user) | keys belong in Credential Manager or a vault |
| `IMcpTokenStore` | `SecureStorageMcpTokenStore` (DPAPI) | same, for OAuth tokens |
| `IMcpAuthorizationHandler` | `BrowserMcpAuthorizationHandler` (system browser + loopback) | consent should happen in an embedded WebView2, or to change `Timeout`/`CompletionHtml` |
| `IAiSessionStore` | `FileAiSessionStore` (plain JSON) | conversations need encryption or a database |
| `IAiChatClientFactory` | `AiChatClientFactory` | a provider neither SDK path covers - Azure OpenAI needs its own client |

## Chat or agent - pick deliberately

| | `IAiChatService` | `IAiAgentFactory` |
| --- | --- | --- |
| Memory between calls | none | `AgentSession` carries history |
| Tool calls | run immediately, no confirmation | paused for approval by default |
| Use for | one-shot "summarize this" requests | the conversational surface |

Both stay registered. If end users can add servers, the conversational surface must be an agent
under `AiToolApprovalMode.Always`. `IAiChatService` appends `IMcpServerRegistry.Tools` to a clone
of the caller's `ChatOptions` (caller tools kept, caller object untouched).
`IAiChatClientFactory.GetChatClientAsync()` is the raw BYOK `IChatClient` without MCP tools, but
it is wrapped in `UseFunctionInvocation()` - tools you pass still auto-run.

```csharp
var response = await aiChatService.GetResponseAsync([new ChatMessage(ChatRole.User, "Summarize this.")]);
```

## Running the agent

```csharp
var agent = await agentFactory.GetAgentAsync();          // per conversation, not held forever
var session = await agent.CreateSessionAsync();
var response = await agent.RunAsync(userText, session);

while (response.GetToolApprovalRequests() is { Count: > 0 } pending)
{
    var name = (pending[0].ToolCall as FunctionCallContent)?.Name ?? pending[0].ToolCall.CallId;
    var (allow, dontAskAgain) = await AskUserAsync(name);
    response = await agent.RunAsync(pending.CreateApprovalResponse(allow, alwaysApprove: dontAskAgain), session);
}
Transcript.Add(response.Text);
```

- **The loop is required.** Requested tools surface one at a time; while
  `GetToolApprovalRequests()` is non-empty nothing has run and `response.Text` is not the answer.
- `alwaysApprove: true` records a standing per-session rule (one prompt per distinct tool); it is
  ignored when denying. A denial is not an error - the model is told (pass `reason`).
- The tool name lives on `FunctionCallContent` (`ToolCall` is the base type). Show its
  `Arguments` too - `delete_file(path: ...)` reads very differently from `delete_file`.
- Only `AIFunction` tools are wrapped (`ApprovalRequiredAIFunction`, schema kept -
  `ApprovalWrappingKeepsTheToolDescribableToTheModel`); hosted tools pass through.
- Streaming: collect `RunStreamingAsync` updates, then `updates.ToAgentResponse()` to check for
  approvals ([patterns.md](patterns.md)). `AIAgent` is Microsoft's own type, used as documented.
- **Per-turn instructions** (current date/time, the working folder) go in
  `new ChatClientAgentRunOptions(new ChatOptions { Instructions = ... })` passed to each run; the
  agent keeps its tools (`PerRunChatOptionsDoNotDropTheAgentsTools`). Editing `AiAgentOptions` at
  runtime does not rebuild a cached agent.
- **Tell the model what path-taking tools need.** The sample's NuGet tools need an absolute
  solution directory; without it in the instructions the model quietly answers from memory, which
  looks exactly like broken tool calling.
- **The default agent is cached**, rebuilt on `IAiChatClientFactory.ConfigurationChanged`, on
  `IMcpServerRegistry.Changed` (tools are fixed at build) - both forwarded as
  `IAiAgentFactory.ConfigurationChanged`, which also fires when a seed server connects - and when
  the factory returns a new `IChatClient` (key stored without `RefreshApiKeyAsync`). An
  `AgentSession` survives rebuilds of the same agent shape; the sample resets it anyway.
- `CreateAgentAsync(new AiAgentDescriptor { Name = "Summarizer", Tools = { AIFunctionFactory.Create(...) } })`
  builds an uncached second agent; its own `Tools` are gated by the descriptor's `ToolApproval`
  (default `Always`). It snapshots tools and chat client - rebuild it on
  `IAiAgentFactory.ConfigurationChanged`.
- `AiToolApprovalMode.Never` (auto-execute) only suits an app that picks and trusts every server.

## Provider, model and key at runtime

```csharp
await apiKeyProvider.SetApiKeyAsync("gemini", usersOwnKey);       // keyed by the Provider string
chatClientFactory.UpdateProvider("gemini", modelTypedByUser, geminiEndpoint);
await chatClientFactory.RefreshApiKeyAsync();                     // fire ConfigurationChanged now
var ready = await chatClientFactory.IsConfiguredAsync();          // model set and key stored, no network call
```

- **Routing:** case-insensitive `"anthropic"` uses the Anthropic SDK and **ignores `Endpoint`**.
  Any other free string uses the OpenAI SDK - `Endpoint = null` is the real OpenAI API, otherwise
  any OpenAI-wire endpoint (Gemini's URL above, Ollama, LM Studio, vLLM, OpenRouter, a proxy). A new
  provider never needs a library release. Azure OpenAI is not covered.
- **The key is stored under the `Provider` string** (trimmed, lowercased), not the catalog `Key`.
  Two catalog entries backed by `"openai"` share one key; storing under `"claude"` when the entry's
  `Provider` is `"anthropic"` yields "No API key has been set for provider 'anthropic'".
- A key-less local endpoint still needs a stored non-empty key (store a placeholder).
- `SelectProvider(key)` searches the catalog **snapshot** and throws `InvalidOperationException`
  for an unknown key or an entry without `Model`; for runtime entries or a freely typed model,
  call `UpdateProvider` (the sample does). `AiProviderDescriptor.Validate()` checks `Key`/`Provider`.
- `GetChatClientAsync` re-reads the key every call and rebuilds (disposing the old client) on any
  change. `SetApiKeyAsync` raises no event - call `RefreshApiKeyAsync` to refresh bound status.
- `IAiModelCatalog.GetModelsAsync(provider, endpoint)` needs a stored key and does no caching
  (use a button), filtering (embedding/audio included) or sorting. Pass the chat's endpoint. A
  proxy without `GET {endpoint}/models` throws - keep typed names working (editable ComboBox,
  `IsTextSearchEnabled="False"`). `AiModelInfo.Id` is what `UpdateProvider` takes.
- **Nothing persists itself.** Persist the chosen provider/model/endpoint and any user-added
  servers yourself; never persist the key anywhere but `IAiApiKeyProvider`.

## MCP servers

```csharp
var status = await registry.AddServerAsync(descriptor);   // throws on failure, and records it
await registry.RemoveServerAsync("NuGet");                // false if unknown
```

- `Stdio` launches `Command`/`Arguments`/`WorkingDirectory`; `EnvironmentVariables` applies on top
  of what `InheritEnvironmentVariables` (default `true`) lets through, and a **`null` value removes**
  an inherited variable. Set `InheritEnvironmentVariables = false` to give a third-party binary an
  empty environment. `Http` uses `Endpoint`, `AdditionalHeaders` (a static token) and
  `HttpTransportMode` (`AutoDetect` probes Streamable HTTP, falls back to SSE).
- `McpServerDescriptor.Validate()` is the settings-UI pre-flight. `AddServerAsync` throws
  `InvalidOperationException` (invalid) or `ArgumentException` (duplicate `Name`, case-sensitive).
- **Status lifecycle:** the entry appears at once (`IsConnected = false`, `LastError = null` -
  connecting), then connects or fails (`LastError` set, exception rethrown). A failed entry stays
  tracked, so re-adding its name throws (`AddServerAsyncThrowsForDuplicateNamesEvenIfThePreviousAttemptFailedToConnect`).
  A live server that dies flips back with `LastError`. **No automatic reconnect** - Remove, then Add.
- **`Changed` is raised on whatever thread caused it** - after a connect or a drop-off that is a
  thread-pool thread. `IAiAgentFactory.ConfigurationChanged` forwards it. Marshal to the UI
  thread before touching an `ObservableCollection` or other UI state.
- `IMcpServerRegistry.Tools` aggregates connected servers only. On a name collision the server
  later in `Servers` (registration order, not connect order) wins, with a warning naming both.
- A stdio `LastError` carries the exit code and stderr tail - usually the real reason; every
  stderr line is also logged at `Debug`. Servers see the client as the static
  `AppInfo.Current.Name` (`"Barbatos.Wpf"` if empty) and `VersionString`, not a DI-replaced
  `IAppInfo`.

## OAuth for hosted servers

```csharp
await registry.AddServerAsync(new McpServerDescriptor
{
    Name = new Uri(endpoint).Host,       // tokens are keyed by Name - see below
    TransportKind = McpTransportKind.Http,
    Endpoint = endpoint,
    OAuth = new McpOAuthOptions(),       // discovered: auth server, scopes, client registration
});
```

- **An empty `McpOAuthOptions()` is the intended case.** The SDK takes the `401` challenge, finds
  the authorization server, registers the app dynamically (consent screen shows `ClientName`,
  default `AppInfo.Current.Name`), and `BrowserMcpAuthorizationHandler` opens the user's real
  browser and catches the redirect on `http://127.0.0.1:<free port>/` - OAuth 2.1 / RFC 8252 with PKCE.
- Set a property only when a server forces it: `ClientId` (no dynamic registration), `Scopes`
  (a fallback after `WWW-Authenticate` and protected-resource metadata), `RedirectUri` (a fixed
  registered URL - a fixed port can be taken on the user's machine),
  `AdditionalAuthorizationParameters`, `PersistTokens = false` (re-consent every run).
- `Validate()` rejects `OAuth` on `Stdio`, `ClientSecret` without `ClientId`, and a `RedirectUri`
  that is not an absolute `http://` loopback URL. A desktop binary cannot keep a secret.
- `McpAuthorizationException` (`Error`, `ErrorDescription`) is an ordinary outcome - denied
  (`access_denied`), closed tab, `Timeout` (5 minutes), no browser, port in use - and lands in
  `LastError`. Disable the connect button while in flight (a second tab, a second port).
- `SignOutAsync(name)` forgets tokens but leaves a connected server connected - call
  `RemoveServerAsync` too for a full sign-out. Tokens are keyed by the exact (trimmed,
  case-sensitive) `Name`: rename a server and it re-consents.
- The `IMcpTokenStore` payload is an opaque SDK-owned secret - never parse it; an unreadable one
  is discarded and the user re-authorizes.
- A custom `IMcpAuthorizationHandler` must honour `descriptor.OAuth.RedirectUri` when set and pass
  `state` and `iss` back unchanged in `McpAuthorizationResult` (CSRF and RFC 9207 mix-up checks).

## Sessions

```csharp
var restored = await sessionStore.LoadAsync("last-chat", agent) ?? await agent.CreateSessionAsync();
await sessionStore.SaveAsync("last-chat", agent, session);
```

- `LoadAsync` returns `null` when nothing was saved - no catch needed. Pass the agent from
  `IAiAgentFactory` to both calls; a session is tied to the agent shape that created it.
- Default files: `{IFileSystem.AppDataDirectory}/ai-sessions/<id>.json`, written via temp file +
  move (a kill mid-save keeps the old one). `ListAsync` order is unspecified.
- Ids are rejected, not sanitized: anything invalid in a file name, either separator, and **any
  `.`** (`"v1.2"`, `"chat:1"`, `".."` all throw `ArgumentException`). Use `Guid.NewGuid().ToString("N")`.
- **A saved session is the conversation itself** - often personal data - in plain, per-user,
  unencrypted JSON. Replace `IAiSessionStore` when that is not enough, and only load sessions this
  app wrote: restoring one is accepting input.

## Attachments

No attachment API - a `ChatMessage` with several `AIContent` items:

```csharp
new ChatMessage(ChatRole.User,
[
    new TextContent("What's in this screenshot?"),
    new DataContent(await File.ReadAllBytesAsync(path), "image/png"),   // or "application/pdf"
]);
```

`DataContent` embeds bytes inline (prefer it for local files); `UriContent` references hosted
content. Media types pass straight through - nothing is transformed, downscaled or validated, and
provider support varies. **`ChatMessage.Text` reflects only `TextContent`**: a transcript built on
`.Text` silently drops attachments - walk `Contents`.

## Hard rules

- BYOK always; keys only through `IAiApiKeyProvider`, tokens only through `IMcpTokenStore`.
- `AiToolApprovalMode.Always` for anything conversational; marshal `Changed` handlers to the UI.
- Register replacements before `ConfigureMcp`; never edit options after `Build()` expecting effect.
- `ISecureStorage.RemoveAll()` also wipes every stored AI key (`Barbatos:Mcp:ApiKey:<provider>`) and
  OAuth token (`Barbatos:Mcp:OAuth:<name>`) - don't call it from an unrelated "reset" path.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| "No API key has been set for provider 'x'" | key never stored, or stored under the catalog `Key` instead of the `Provider` string; or a key-less local endpoint | `SetApiKeyAsync(providerString, key)`; store a placeholder for a local endpoint |
| "AiProviderOptions.Model must be set" | `Model` defaults to `null` | set it in `configureProvider`/config, or `UpdateProvider` |
| `SelectProvider` throws for a key you just added | catalog snapshotted at construction | `UpdateProvider` for runtime entries |
| The AI answers from memory, never calls a tool | server not connected yet or failed; an old agent held across `Changed`; `IncludeMcpTools = false`; the tool needs an argument (a path) the model doesn't know | check `Servers`/`LastError`; `GetAgentAsync()` per conversation; put the needed context in the instructions |
| A tool runs without asking | `IAiChatService`, or `ToolApproval = Never` | agent under `Always` |
| After one approval another request appears | requests are surfaced one at a time | loop until `GetToolApprovalRequests()` is empty |
| Server never connects; `LastError` shows an exit code/stderr | wrong command, missing env var, `dnx pkg@version` syntax | fix from `LastError`; enable Debug logging; `dnx <pkg> --version <v> --yes` |
| A seed server is missing from `Servers` entirely | its descriptor failed `Validate()` before an entry existed; only the startup Error log says so | call `Validate()` on seeds; read the log |
| Retrying a failed server throws `ArgumentException` | the failed entry is still tracked | `RemoveServerAsync` first |
| Tools vanish mid-session | server dropped off; no auto reconnect | watch `Changed`, then Remove + Add |
| Cross-thread exception in a `Changed` handler | raised on a thread-pool thread | `Dispatcher` before touching UI |
| "configured for OAuth but no IMcpAuthorizationHandler is registered" | an `IMcpAuthorizationHandler` registered before `ConfigureMcp` resolved to `null` | register a real handler, or none so the browser default is used |
| "Could not listen for the OAuth redirect ... port may already be in use" | a fixed `RedirectUri` port is taken | leave `RedirectUri` null unless the server demands it |
| Sign-in "timed out after 5 minutes" / "No browser could be opened" | user left the tab; `ILauncher.OpenAsync` returned false | report it, offer retry; `Timeout` on a self-registered handler |
| Signed out but tools still work | `SignOutAsync` forgets tokens only | also `RemoveServerAsync` |
| Browser consent on every launch | `PersistTokens = false`, the server `Name` changed, or a custom store that doesn't persist | stable `Name` (e.g. the host) |
| Changing `AiAgentOptions` at runtime does nothing | the cached agent is rebuilt only on `ConfigurationChanged` | per-run `ChatClientAgentRunOptions`, or `CreateAgentAsync` |
| `GetModelsAsync` throws | no key yet, or endpoint lacks `/models` | save the key first; keep typed entry |
| `Build()` cannot resolve `ILauncher`/`ISecureStorage`/`IFileSystem` | `CreateBuilder(useDefaults: false)` | `builder.UseEssentials()` |

## Changing Barbatos.Wpf.Mcp itself

Load `barbatos-package-authoring` too. Feature-specific checklist:

- Keep MCP SDK types out of the public surface (`McpHttpTransportMode` mirrors the SDK enum, tools
  are typed `AITool`, tokens are an opaque `string`); `AIAgent`/`ChatMessage` are exposed on purpose.
- A singleton holding async-only resources also implements `IDisposable` (fire-and-forget
  `DisposeAsync`) or the container's synchronous `Dispose()` throws
  (`RealRegistryAndFactoryImplementSynchronousDisposableForContainerSafety`).
- Pure `Validate()` on descriptors, `TryAdd*` registrations, and nothing in
  `IWpfInitializeService.Initialize` may throw - startup has no try/catch.
- **Version lockstep:** `Microsoft.Extensions.AI`, `.Abstractions` and `.OpenAI` are pinned in
  `Directory.Packages.props` to the floor `ModelContextProtocol.Core` depends on - bump them
  together or restore fails with `NU1605`.
- Tests register fakes before `ConfigureMcp` and resolve the internal implementation through DI
  (per CLAUDE.md, no `InternalsVisibleTo`) - [patterns.md](patterns.md#testing). Some launch
  `cmd.exe`; run per TFM (`barbatos-wpf-testing`).
- Update the README AI section and the API-REFERENCE `Barbatos.Wpf.Mcp` namespace
  (`barbatos-docs-sync`), and the sample's AI tab if the flow changed.

## Related skills

- `barbatos-wpf-essentials` - `ISecureStorage`, `IFileSystem`, `ILauncher`, `IAppInfo` underneath the defaults.
- `barbatos-wpf-host` - the builder, `IWpfInitializeService`, configuration layering, dispatching.
- `barbatos-aquarius-view` - the chat View/ViewModel if it uses `aq:`.
- `barbatos-package-authoring`, `barbatos-wpf-testing`, `barbatos-docs-sync` - changing this module.
