---
name: "blazor"
description: 'Build Blazor applications with Razor components, lifecycle management, and C# web patterns. Use when creating Blazor Server or WebAssembly apps, building Razor components, implementing state management, adding JavaScript interop, or optimizing Blazor performance.'
metadata:
 author: "AgentX"
 version: "1.0.0"
 created: "2025-01-15"
 updated: "2025-01-15"
compatibility:
 languages: ["csharp"]
 frameworks: ["blazor", "dotnet", "aspnet-core"]
 platforms: ["windows", "linux", "macos"]
---

# Blazor Framework Development

> **Purpose**: Production-ready Blazor development for building interactive web applications with C#. 
> **Audience**: .NET engineers building Blazor Server or WebAssembly applications. 
> **Standard**: Follows [github/awesome-copilot](https://github.com/github/awesome-copilot) Blazor patterns.

---

## When to Use This Skill

- Building Blazor Server or WebAssembly applications
- Creating Razor components with parameters and binding
- Implementing Blazor dependency injection
- Adding JavaScript interop to Blazor apps
- Optimizing Blazor rendering performance

## Prerequisites

- C# and .NET 8+ knowledge
- Basic HTML/CSS understanding
- Visual Studio or VS Code with C# extension

## Quick Reference

| Need | Solution | Pattern |
|------|----------|---------|
| **Component** | Razor component | `@code { }` block |
| **Data binding** | Two-way binding | `@bind="propertyName"` |
| **Event handling** | Click events | `@onclick="HandleClick"` |
| **Dependency injection** | Inject services | `@inject IUserService UserService` |
| **Routing** | Page directive | `@page "/users/{UserId:int}"` |
| **Lifecycle** | Async initialization | `protected override async Task OnInitializedAsync()` |

---

## Blazor Hosting Models

### Blazor Server
- Runs on server, updates sent via SignalR
- Full .NET runtime on server
- Small download size, fast initial load
- Requires persistent connection

### Blazor WebAssembly
- Runs in browser via WebAssembly
- Larger initial download
- Works offline after loading
- No server connection needed after initial load

### Blazor United (.NET 8+)
- Combines Server and WebAssembly
- Progressive enhancement
- Optimal performance

**Choose Server for**: Line-of-business apps, intranet, backend-heavy applications 
**Choose WebAssembly for**: Public-facing apps, offline support, minimal server load

---

## Component Structure

```razor
@* Counter.razor - Basic component *@
@page "/counter"

<h1>Counter</h1>

<p>Current count: @currentCount</p>

<button class="btn btn-primary" @onclick="IncrementCount">
 Click me
</button>

@code {
 private int currentCount = 0;

 private void IncrementCount()
 {
 currentCount++;
 }
}
```

---

## Common Pitfalls

| Issue | Problem | Solution |
|-------|---------|----------|
| **Missing @bind** | One-way binding only | Use `@bind="property"` for two-way |
| **StateHasChanged not called** | UI doesn't update | Call `StateHasChanged()` after async operations |
| **Memory leaks** | Event handlers not removed | Implement `IDisposable` and unsubscribe |
| **Wrong lifecycle method** | Code runs at wrong time | Use `OnInitializedAsync` for async init |
| **Scoped service in Singleton** | Service lifetime mismatch | Match service lifetimes properly |
| **Missing [Parameter]** | Parameters not working | Add `[Parameter]` attribute |

---

## Resources

- **Blazor Docs**: [learn.microsoft.com/aspnet/core/blazor](https://learn.microsoft.com/aspnet/core/blazor)
- **bUnit Testing**: [bunit.dev](https://bunit.dev)
- **Blazor WebAssembly**: [learn.microsoft.com](https://learn.microsoft.com/aspnet/core/blazor/hosting-models)
- **Awesome Blazor**: [github.com/AdrienTorris/awesome-blazor](https://github.com/AdrienTorris/awesome-blazor)
- **Awesome Copilot**: [github.com/github/awesome-copilot](https://github.com/github/awesome-copilot)

---

**See Also**: [Skills.md](../../../../Skills.md) - [AGENTS.md](../../../../AGENTS.md)

**Last Updated**: January 27, 2026

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Component not re-rendering | Call StateHasChanged() or ensure parameter values are new object references |
| JS interop errors | Ensure JS files loaded with script tag, use IJSRuntime for interop calls |
| Blazor WASM slow initial load | Enable AOT compilation, use lazy loading for assemblies |

## References

- [Component Patterns](references/component-patterns.md)
- [Di Routing Jsinterop](references/di-routing-jsinterop.md)
- [State Perf Testing](references/state-perf-testing.md)