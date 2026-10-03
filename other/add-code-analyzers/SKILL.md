---
name: add-code-analyzers
description: Turn the mechanical code-quality rules into build errors for .NET (banned time APIs, unnecessary usings, accessibility modifiers, nullable) using Directory.Build.props, .editorconfig and BannedSymbols.txt from the kit templates. Manual command.
disable-model-invocation: true
---
Delegate to implementer with a pointer prompt:
1. Templates: `.ai/templates/dotnet/`. For each of `Directory.Build.props`, `BannedSymbols.txt`: if absent at the solution root, copy with a shell command; if present, add only the missing properties/items with targeted edits.
2. `.editorconfig`: if absent, copy `editorconfig.template` as `.editorconfig`; if present and it lacks the `# ai-kit:code-quality` marker, append the template content.
3. Run `dotnet build`. Do not fix violations. Output `VIOLATIONS: <rule id> <count>` per diagnostic id, then `NEXT: fix in a separate task`.
