---
name: toolforge-cli
description: Marketplace CLI and reviewed read-only JSON-input pilot invocation.
compatibility: |
  - Runtime: PowerShell 5.1+
  - Dependencies: toolforge-registry-manager, toolforge-submission-validator
  - Input pilot: Node 24; copied commands require PowerShell 7+
---

# Toolforge CLI

Command-line entry point for Toolforge Marketplace operations (list/install/submit).

## Trigger

```powershell
pwsh src/cli.ps1 -Command <list|install|submit> [options]
```

For a reviewed input pilot:

```text
node <toolforge-root>/skills/toolforge-cli/src/invoke-skill.mjs --skill <id> --workspace-root <absolute-root>
```

Repeat `--workspace-root` for additional trusted roots. Stdin contains exactly one
JSON object, strict UTF-8, at most 65,536 raw bytes. Unknown/missing arguments,
arbitrary entrypoints/exports, unknown fields, and coercion are rejected.

| Pilot ID | JSON input |
| --- | --- |
| roadmap-validator | roadmapPath: absolute readable .md path; strict and verbose: optional booleans, default false |
| agent-drift-detector | agentName: nonempty string, trimmed; expectedSchema and actualSchema: objects |
| retro-schema-validator | filePaths: 1-32 distinct absolute readable .json paths, selected order preserved |

Paths must resolve inside trusted roots; each selected file caps at 1 MiB.
Agent comparison uses top-level keys only. Results preserve native handler fields.

Pilot envelope: `{contractVersion:1, skillId, state, outcome, result, error, durationMs}`.
Completed state has pass/findings outcome and native result; other states have null
outcome/result and a stable safe error. Invalid target has null skillId.
Exit 0 means pass; 1 means findings; 2 means rejected, unavailable, failed,
timed_out, or cancelled. Only the result envelope reaches stdout.

`createInvocationRunner(context)` returns `invokeSkill`, `inspectInvocation`, and
async `dispose`. `formatInvocationCommand(skillId,input,options)` is a pure portable
formatter. See [Pilot usage and troubleshooting](docs/USAGE.md) for their contracts.

## Input Schema

```typescript
interface CliInput {
  command: "list" | "install" | "submit";
  id?: string;                // For install
  path?: string;              // For submit
  category?: string;          // Filter for list
  status?: string;            // Filter for list
  format?: "table" | "json";  // Output format
  dryRun?: boolean;
}
```

## Output Schema

```typescript
interface CliOutput {
  status: "success" | "error";
  command: string;
  result: Array<any> | object;
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).
