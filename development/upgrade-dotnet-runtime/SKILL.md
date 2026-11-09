---
name: upgrade-dotnet-runtime
description: Execute and verify .NET runtime/framework upgrades with minimal behavioral drift.
engines: [AGNOSTIC]
---

## When to use
Use when modernizing .NET projects or solutions to newer target frameworks such as .NET 8.

## Command
../commands/dotnet-upgrade-assistant.sh

## Output
- selected solution/project migration target
- upgrade execution result summary
- breaking changes or manual follow-up list
- post-upgrade restore/build/test status

## Notes
- Pair with `framework-migration-plan` before executing large upgrades.
- Follow with package auditing and regression verification.
