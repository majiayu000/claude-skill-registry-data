---
name: ci-systemic-analyzer
description: |
  Systemic CI/CD failure pattern analysis for MSBuild SDK and NuGet package projects.

  TRIGGERS (activate this skill when user provides):
  - GitHub Actions workflow URLs showing repeated failures
  - Commit history with back-and-forth fixes
  - "CI keeps failing", "why does CI break every SDK change"
  - Pattern of: SDK change → CI fail → fix → different CI fail → repeat
  - Request for root cause analysis across multiple runs

  NOT for:
  - Single one-off CI failure (use msbuild-nuget-master instead)
  - Simple "what broke" questions

  What it does:
  - Correlates failures across workflow runs (not just latest)
  - Identifies architectural flaws causing cascading failures
  - Maps SDK ↔ CI coupling violations
  - Produces isolation strategy to prevent recurrence
---

# CI Systemic Failure Analyzer

## Mental Model: Failure Cascades

```
SDK Change → Build Logic Changes → CI Assumptions Break → Symptom Fix → New SDK Assumption Breaks → Repeat
     ↓              ↓                     ↓                    ↓
  props/targets   Import order       Version/TFM/Path      Partial fix
  Shared code     Pack timing        coupling exposed      introduces
  Package refs    Restore behavior                         new coupling
```

**The trap**: Fixing symptoms creates NEW coupling. Each fix adds implicit assumptions.

## Analysis Protocol

### Phase 1: Gather Evidence (Don't Skip)

```bash
# 1. Fetch recent workflow runs
gh run list --limit 20 --json conclusion,headBranch,startedAt,url,displayTitle

# 2. Get commit history correlation
git log --oneline --since="2 weeks ago" | head -30

# 3. Map failures to commits
gh run list --status failure --limit 10 --json headSha,url,displayTitle
```

**What to look for:**
- Same error appearing → disappearing → reappearing (yo-yo pattern)
- Fixes that reference previous fixes ("revert", "undo", "try different")
- Commits touching same files repeatedly
- Error migration: NU1xxx → MSBxxx → CS8xxx → NU1xxx

### Phase 2: Classify Failure Pattern

| Pattern | Signature | Root Cause Category |
|---------|-----------|---------------------|
| **Yo-yo** | Error A fixed → Error B → Fix B breaks A | Coupling violation |
| **Cascade** | One change → 3+ different errors | Missing boundary |
| **Environment drift** | Works local, fails CI | Implicit state dependency |
| **Order sensitivity** | Fails on first build, passes on rebuild | Import order / cache |
| **TFM whack-a-mole** | Fix net10 → break netstandard2.0 | Polyfill injection |

### Phase 3: Root Cause Categories

#### Category A: SDK ↔ Consumer Coupling

**Symptoms:**
- SDK .props/.targets assume consumer state
- Consumer .csproj assumes SDK internal structure
- Canary tests break when SDK internals change

**Fix pattern:**
```xml
<!-- BAD: SDK assumes consumer has CPM -->
<PackageReference Include="X" Version="$(SomeVersion)" IsImplicitlyDefined="true"/>

<!-- GOOD: SDK provides both version AND override capability -->
<PackageReference Include="X" Version="$(XVersion)" VersionOverride="$(XVersion)" />
```

#### Category B: Resolution Timing Violations

**Symptoms:**
- Works in IDE, fails in CLI
- Works on rebuild, fails on clean build
- "Version not specified" after restore succeeds

**Root cause:** MSBuild SDK versions resolve at parse time, PackageReference at restore time.

**Fix pattern:**
```
global.json → SDK version (parse time)
nuget.config → PackageReference sources (restore time)
```

Never reference `$(Version)` or computed properties in `msbuild-sdks` block.

#### Category C: Multi-TFM Polyfill Leakage

**Symptoms:**
- net10.0 builds fine, netstandard2.0 fails
- Missing `IsExternalInit`, `RequiredMemberAttribute`
- `_NeedsPolyfills=true` but `InjectPolyfills=false`

**Root cause:** Polyfill injection condition doesn't match detection condition.

**Fix pattern:**
```xml
<!-- Detection and injection MUST use same condition -->
<PropertyGroup>
  <_NeedsPolyfills Condition="'$(TargetFramework)' == 'netstandard2.0'">true</_NeedsPolyfills>
</PropertyGroup>

<ItemGroup Condition="'$(_NeedsPolyfills)' == 'true'">
  <Compile Include="$(PolyfillPath)*.cs" />
</ItemGroup>
```

#### Category D: Cache/State Pollution

**Symptoms:**
- CI passes → same commit fails → passes again
- "Works after clearing NuGet cache"
- Different results on self-hosted vs GitHub runners

**Fix pattern:**
```yaml
# CI must be hermetic
- name: Clear NuGet caches
  run: dotnet nuget locals all --clear

- name: Restore with --force
  run: dotnet restore --force
```

### Phase 4: Isolation Strategy

**Goal:** SDK changes CANNOT cascade into CI failures.

```
┌─────────────────────────────────────────────────────────┐
│  Layer 0: Global Config (nuget.config, global.json)    │
│  - IMMUTABLE unless explicitly versioned               │
├─────────────────────────────────────────────────────────┤
│  Layer 1: SDK Package                                  │
│  - Self-contained (no external version references)     │
│  - Published version pinned in Layer 0                 │
├─────────────────────────────────────────────────────────┤
│  Layer 2: SDK Canary                                   │
│  - Simulates EXTERNAL consumer                         │
│  - Own NuGet.config, own Directory.Packages.props      │
│  - CPM DISABLED (tests SDK's version injection)        │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Main Solution                                │
│  - Uses SDK via Layer 0's pinned version               │
│  - CPM ENABLED                                         │
└─────────────────────────────────────────────────────────┘
```

**Isolation rules:**
1. Canary MUST NOT inherit any config from main solution
2. SDK MUST NOT reference main solution's CPM versions
3. CI MUST build layers in order: 0 → 1 → 2 → 3
4. Each layer failure STOPS build (no partial success)

## Output Format

When activated, produce this analysis:

```markdown
## Systemic CI Failure Analysis

### Failure Pattern Detected
[Yo-yo | Cascade | Environment drift | Order sensitivity | TFM whack-a-mole]

### Evidence (from workflow history)
- Run #X (date): [Error A]
- Run #Y (date): [Error B after "fixing" A]
- Run #Z (date): [Error A returns]
- Commit correlation: [list commits touching same area]

### Root Cause Category
[A | B | C | D] - [description]

### Why Current Approach Fails
[Explain the coupling/assumption that causes cascading failures]

### Isolation Strategy
[Specific changes to break the cascade]

### Verification Checklist
- [ ] SDK builds independently
- [ ] Canary builds with SDK changes without inheriting main config
- [ ] Main solution builds with published SDK version
- [ ] CI matrix covers: clean build, rebuild, each TFM
```

## References

- **Failure Patterns**: See `references/failure-patterns.md`
- **Isolation Templates**: See `references/isolation-templates.md`
- **CI Workflow Patterns**: See `references/ci-workflows.md`