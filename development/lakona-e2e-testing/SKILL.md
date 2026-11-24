---
name: lakona-e2e-testing
description: Verify Lakona.Tool generated projects through real RPC using local source, local packages, or nuget.org; excludes unit-only and client UI testing.
metadata:
  internal: true
---

# Lakona E2E Testing

Follow `CONTRIBUTING.md` and reuse applicable context already read. Validate
scaffold, build, server startup, and real RPC round trips through the existing
script; do not substitute repository tests for package-level evidence.

## Quick Reference: Feed Modes

The `-Feed` parameter selects the package source independently of test coverage:

| Mode | Flag | Package source | Use case | Speed |
|------|------|---------------|----------|-------|
| **ProjectReference** | `-Feed ProjectReference` (default) | Local source via `<ProjectReference>` | Dev feedback after code changes | Fastest |
| **LocalFeed** | `-Feed LocalFeed` | Locally packed `.nupkg` files | Pre-publish validation | Medium |
| **NuGetOrg** | `-Feed NuGetOrg` | Published packages on nuget.org | Post-publish verification | Slower (restore) |

All three modes scaffold, build, start the server, and run an RPC verification client. Only the dependency resolution differs.

### Select the Feed

1. Honor the user's explicit feed choice, including a choice already established
   in the conversation.
2. Otherwise infer the source from the validation target: local packages or
   pre-publish verification use `LocalFeed`; published packages or post-publish
   verification use `NuGetOrg`.
3. With no source or release-stage indication, use `ProjectReference` without
   asking. A request for quick feedback changes coverage, not an established
   package source.
4. Ask only when conflicting requirements leave the intended source unresolved
   and choosing one would change what the result proves.

Report the selected feed and the coverage actually run. Choose combinations
using Validation Strategy below; selecting a feed does not require a full matrix.

## Run

From the repository root with PowerShell 7 or later:

```powershell
pwsh -NoProfile -File .agents/skills/lakona-e2e-testing/scripts/run-e2e.ps1
```

This defaults to ProjectReference, Godot, WebSocket, MemoryPack, and in-memory
Membership with runtime verification. Set `-Feed` when the selected source differs.
External Membership providers require `-SkipRuntime`; those runs prove generated
package/configuration shape and builds, while Daily Validation owns the real
provider runtime contracts.

| Need | Read |
| --- | --- |
| Non-default combinations, package modes, ports, retained scaffolds, or other options | [commands.md](references/commands.md) |
| Understand dependency patching, generated client wiring, or script phases | [execution.md](references/execution.md) |
| Diagnose a failing run | [failure-triage.md](references/failure-triage.md) |

## Validation Strategy

Choose the smallest run that can answer the question, independently of the feed.
Honor the user's requested coverage and any applicable repository gate:

- **Default smoke**: `godot + websocket + memorypack` with runtime verification (all modes).
- **Tool template or generated layout change**: Run the affected engine plus the affected transport/serializer.
- **Transport change**: Run the changed transport with both serializers.
- **Serializer change**: Run the changed serializer across at least websocket and one socket transport.
- **Source generator or shared contract shape change**: Run default runtime verification first, then expand if it fails or passes but risk remains.
- **Pre-publish verification** (LocalFeed): Run default smoke or the affected combinations above. Selecting local packages alone does not require the full matrix.
- **Post-publish verification** (NuGetOrg): Run default smoke or the affected combinations above against the published packages.
- **Full matrix** (any feed): Run when the user requests complete coverage or an applicable repository gate requires it. Preserve that gate's specified feed and combinations.
- **Fast dev iteration** (any feed): Default smoke covers the most common code path while preserving the selected package source.

Runtime verification remains enabled unless build-only validation is requested
or required by the external Membership provider limitation described above.

Do not claim package-level confidence from repository tests alone. The point of the LocalFeed and NuGetOrg modes is to validate the package restore surface that generated users experience.

## Failure Handling

For verification-only or review-only requests, report findings and proposed
improvements without implementing them. For implementation or repair requests,
continue through fixes within the authorized scope and rerun the affected
verification. Existing authorization remains valid; ask only when a material
product or architecture decision cannot be resolved from available evidence,
or the next action falls outside the authorized scope. Continue independent
authorized work while that decision is pending.

Read the relevant failure-triage section before rerunning. For generation
failures, consult `docs/tool/generation-architecture.md` before proposing fixes.

## Output Contract

After running this skill, report:

- Exact command run (including `-Feed` mode).
- Combination matrix covered.
- Feed mode used and what it means for the results.
- Report path under `$WorkDir`.
- Pass/fail count.
- Most likely root cause for each failure.
- Whether the problem appears to be the framework, generated template, package metadata, or test wrapper.
- Concrete improvement options, with a recommended option.

Finish when the requested verification is reported or the authorized repair and
affected verification are complete. State any unresolved failures or blocked
checks explicitly; a proposed fix alone does not complete a repair request.
