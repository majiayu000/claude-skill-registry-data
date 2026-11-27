---
name: blazor-ui
description: "Build or review Razor/Blazor UI with correct code-behind files, accessibility, state, render modes, security and performance."
---

# Blazor/Razor UI workflow
- Establish framework/version, hosting model, render mode, auth scheme, CSS system, existing component patterns.
- Name components for user capabilities, split `.razor` markup, `.razor.cs` logic partial class, `.razor.css` isolated CSS for non-trivial components.
- Business logic belongs to application/domain; code-behind only handles UI state, interactions and orchestration of client services.
- Model loading/empty/error/success, async cancellation on navigation/filter changes, concurrency and duplicate actions.
- Validate forms client and server; verify server authorization independently of `AuthorizeView`.
- Use accessible native controls, `@key`, appropriate virtualization and measured render optimizations.
- Test prerender/JS lifecycle, disconnect/reconnect (Interactive Server), browser refresh, unauthorized, slow network and responsive layouts.
- Prefer snapshot/component tests for presentation plus real API integration tests for privileged actions.
- Reference `knowledge/RAZOR_BLAZOR.md`.
