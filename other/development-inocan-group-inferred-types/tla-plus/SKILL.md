---
name: tla-plus
description: |
  TLA+ formal verification for modeling and verifying concurrent algorithms and distributed systems.
  Use when asked about: TLA+, formal verification, model checking, verify algorithm, verify spec,
  check invariants, race condition analysis, concurrency model, TLC, Apalache, formal spec,
  temporal logic, prove correctness, state machine verification, model concurrent, TOCTOU,
  double-check locking, create TLA spec, run TLC, explain counterexample, verify safety,
  liveness property, deadlock detection, formal methods.
  Capabilities: Create specs from templates, run TLC/Apalache, generate CI pipelines,
  check code-spec drift, explain counterexamples, generate tests from invariants.
---

# TLA+ Formal Verification Skill

Model and verify concurrent algorithms, race conditions, and distributed protocols using TLA+ formal methods.

## Role in Quality Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ software-       │     │ tla-plus        │     │ code-review     │
│ architect       │ ──► │ skill           │ ──► │ skill           │
│ (Design)        │     │ (Verify)        │     │ (Implement)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
      DESIGN              FORMAL VERIFY           CODE CHECK
        │                       │                       │
        └───────────────────────┴───────────────────────┘
                    Continuous Verification
```

This skill is the **FORMAL VERIFY** phase. It mathematically proves properties about algorithms before or during implementation.

## When to Use TLA+

| Situation | Use TLA+ | Why |
|-----------|----------|-----|
| Concurrent operations | Yes | TLA+ explores all interleavings |
| Race condition suspected | Yes | Find bugs impossible to test empirically |
| Token/session management | Yes | Verify rotation, expiry, refresh logic |
| Distributed consensus | Yes | TLA+'s sweet spot |
| State machine design | Yes | Verify all transitions are safe |
| CRUD operations | No | Overkill for simple operations |
| UI rendering | No | Not the right tool |

**Prime candidates:**
- Database operations with optimistic concurrency
- Token refresh/rotation flows
- Leader election, distributed locks
- Saga patterns, two-phase commits
- Rate limiters, circuit breakers

## Quick Start

### Run Existing Specs

```bash
# Run all models (quick simulation)
python3 ~/.claude/skills/tla-plus/scripts/run_tlc.py --all --mode quick

# Run specific model with full verification
python3 ~/.claude/skills/tla-plus/scripts/run_tlc.py --model node-registration --mode thorough

# Get JSON output for CI
python3 ~/.claude/skills/tla-plus/scripts/run_tlc.py --model token-refresh --format json
```

### Create New Specification

```bash
# From pattern template
python3 ~/.claude/skills/tla-plus/scripts/generate_spec.py \
  --pattern optimistic-concurrency \
  --name "OrderLocking" \
  --output specs/tla+/order-locking/

# From code (LLM-assisted)
python3 ~/.claude/skills/tla-plus/scripts/generate_from_code.py \
  --source src/Services/OrderService.cs \
  --method ProcessOrder \
  --concern "race condition"
```

### Generate CI Pipeline

```bash
# Azure DevOps
python3 ~/.claude/skills/tla-plus/scripts/generate_pipeline.py \
  --platform azure-devops \
  --output .azure-pipelines/tla-verification.yml

# GitHub Actions
python3 ~/.claude/skills/tla-plus/scripts/generate_pipeline.py \
  --platform github \
  --output .github/workflows/tla-verification.yml
```

## Core Workflows

### 1. Creating a New Specification

**Step 1: Identify the Concern**

What concurrent/distributed behavior needs verification?
- Race conditions in shared state
- Ordering of operations
- Safety invariants (bad things never happen)
- Liveness properties (good things eventually happen)

**Step 2: Choose a Pattern**

| Pattern | Use Case | Template |
|---------|----------|----------|
| Optimistic Concurrency | DB updates with version check | `optimistic-concurrency.tla` |
| Token Rotation | JWT refresh, session management | `token-rotation.tla` |
| State Machine | Workflow, lifecycle management | `state-machine.tla` |
| Leader Election | Distributed coordination | `leader-election.tla` |
| Circuit Breaker | Resilience patterns | `circuit-breaker.tla` |
| Rate Limiter | Token bucket, sliding window | `rate-limiter.tla` |
| Saga Pattern | Distributed transactions | `saga-pattern.tla` |
| Two-Phase Commit | Atomic distributed operations | `two-phase-commit.tla` |

**Step 3: Generate and Customize**

```bash
python3 ~/.claude/skills/tla-plus/scripts/generate_spec.py \
  --pattern optimistic-concurrency \
  --name "NodeClaiming" \
  --entities "NODES" \
  --actors "USERS" \
  --output specs/tla+/node-claiming/
```

**Step 4: Add Code Mappings**

Document the relationship between TLA+ and code:

```bash
python3 ~/.claude/skills/tla-plus/scripts/add_mapping.py \
  --model node-claiming \
  --action "UserClaimNode" \
  --file "src/Features/AccessPoint/RegisterAccessPointCommandHandler.cs" \
  --method "ClaimSelfRegisteredNode" \
  --line 204
```

**Step 5: Verify**

```bash
# Quick check during development
python3 ~/.claude/skills/tla-plus/scripts/run_tlc.py --model node-claiming --mode quick

# Full verification before merge
python3 ~/.claude/skills/tla-plus/scripts/run_tlc.py --model node-claiming --mode thorough
```

**Step 6: Create Buggy Variant (Recommended)**

Create a version that intentionally lacks safety measures to verify TLC catches bugs:

```bash
python3 ~/.claude/skills/tla-plus/scripts/generate_buggy.py \
  --model node-claiming \
  --remove-guard "version check" \
  --expected-violation "SingleOwnership"
```

### 2. Understanding Counterexamples

When TLC finds an invariant violation, it produces a counterexample trace.

```bash
# Explain the counterexample in plain English
python3 ~/.claude/skills/tla-plus/scripts/explain_counterexample.py \
  --model node-registration \
  --format markdown
```

**Example Output:**

```markdown
## Counterexample Analysis: NodeRegistrationBuggy

### Invariant Violated: `NoDoubleClaimSuccess`

### Trace (5 states):

**State 1** (Initial):
- Node N1 is unregistered
- No claims in progress

**State 2** (Action: `NodeSelfRegister(N1)`):
- Node N1 becomes self-registered (owner = SYSTEM)
- Code: `RegisterNodeCommandHandler.CreateNewNode()` at line 96

**State 3** (Action: `UserReadForClaim(U1, N1)`):
- User U1 reads N1, sees it's claimable (self_registered)
- Code: Start of `ClaimSelfRegisteredNode()` at line 204

**State 4** (Action: `UserReadForClaim(U2, N1)`) *RACE CONDITION*:
- User U2 also reads N1, sees it's claimable
- Both U1 and U2 now believe they can claim N1

**State 5** (Action: `UserCompleteClaim(U1, N1)`, then `UserCompleteClaim(U2, N1)`):
- Both complete their claims
- **INVARIANT VIOLATED**: Two users successfully claimed the same node

### Root Cause
Time-of-check to time-of-use (TOCTOU) vulnerability. The check for claimability
and the claim operation are not atomic.

### Recommended Fix
Implement optimistic concurrency control:
1. Add version column to the entity
2. Check version at write time
3. Retry on conflict

See template: `optimistic-concurrency.tla`
```

### 3. Checking Code-Spec Drift

After code changes, verify specs are still accurate:

```bash
python3 ~/.claude/skills/tla-plus/scripts/check_drift.py --all --format table
```

**Example Output:**

```
┌─────────────────────┬──────────────────────────┬──────────┬────────────────────────────────┐
│ Model               │ Mapping                  │ Severity │ Issue                          │
├─────────────────────┼──────────────────────────┼──────────┼────────────────────────────────┤
│ node-registration   │ UserClaimNode → line 204 │ Medium   │ Method moved to line 245       │
│ token-refresh       │ TokenRevoke → file       │ Critical │ File renamed to TokenService   │
│ order-locking       │ All mappings             │ Low      │ OK - no drift detected         │
└─────────────────────┴──────────────────────────┴──────────┴────────────────────────────────┘
```

### 4. CI/CD Integration

**Verification Strategy:**

| Branch | Mode | Timeout | Purpose |
|--------|------|---------|---------|
| PR (any) | simulation | 5 min | Fast feedback, catch most bugs |
| develop | standard | 15 min | Thorough check before integration |
| main | thorough | 30 min | Complete verification |

**Smart Triggers:**

The generated pipeline only runs when relevant files change:
- Any `.tla` or `.cfg` file in `specs/tla+/`
- Source files mapped to specifications (from `mappings.json`)

**Negative Testing:**

Pipeline includes verification that buggy variants fail:
- Confirms TLC can catch the bugs we're protecting against
- Guards against regressions in the spec itself

### 5. Generating Tests from Specs

Extract testable properties from TLA+ invariants:

```bash
python3 ~/.claude/skills/tla-plus/scripts/spec_to_tests.py \
  --model node-registration \
  --language csharp \
  --output tests/NodeRegistration.Invariants.Tests.cs
```

**Generated Test Example:**

```csharp
/// <summary>
/// Tests derived from TLA+ invariant: SingleOwnership
/// Spec: Every registered node has exactly one owner
/// </summary>
[Fact]
public async Task SingleOwnership_NodeCannotHaveMultipleOwners()
{
    // Arrange: Create self-registered node
    var node = await CreateSelfRegisteredNode();

    // Act: Two users attempt to claim simultaneously
    var claim1 = ClaimNodeAsync(node.Id, user1);
    var claim2 = ClaimNodeAsync(node.Id, user2);
    await Task.WhenAll(claim1, claim2);

    // Assert: Exactly one claim succeeded
    var owner = await GetNodeOwner(node.Id);
    Assert.NotEqual(SystemConstants.SystemNodeRegistrationOwnerId, owner);
    Assert.True(
        (claim1.Result.IsSuccess && !claim2.Result.IsSuccess) ||
        (!claim1.Result.IsSuccess && claim2.Result.IsSuccess),
        "Exactly one claim should succeed (TLA+ invariant: SingleOwnership)"
    );
}
```

## Verification Modes

### TLC (Default)

Explicit state model checker. Explores all reachable states.

| Mode | States | Time | Use Case |
|------|--------|------|----------|
| `quick` | ~100k (simulation) | Seconds | Development, CI |
| `standard` | All (small config) | Minutes | Pre-merge |
| `thorough` | All (large config) | 10-30 min | Release verification |

### Apalache (Symbolic)

Symbolic model checker using Z3. Better for:
- Large/infinite state spaces
- Integer arithmetic
- Inductive invariant checking

```bash
python3 ~/.claude/skills/tla-plus/scripts/run_apalache.py \
  --model token-refresh \
  --check-inductive \
  --length 20
```

### When to Use Which

| Situation | Tool | Why |
|-----------|------|-----|
| Small state space (<1M states) | TLC | Fast, complete |
| Large integers/unbounded | Apalache | Symbolic handling |
| Inductive invariant proof | Apalache | Built-in support |
| Liveness properties | TLC | Better temporal support |
| Quick feedback | TLC simulation | Fastest |

## Project Structure

```
project/
├── .tla-plus/
│   ├── project.json      # TLA+ project configuration
│   └── mappings.json     # Code-to-spec traceability
└── specs/tla+/
    ├── README.md
    ├── .tools/
    │   ├── run-tlc.sh    # Shell runner (legacy)
    │   └── tla2tools.jar # TLC (downloaded)
    ├── common/
    │   └── ProjectCommon.tla
    └── {model-name}/
        ├── README.md
        ├── {Model}.tla       # Main specification
        ├── {Model}.cfg       # Small configuration
        ├── {Model}_Large.cfg # Large configuration
        └── {Model}Buggy.tla  # Negative test variant
```

## Pattern Templates

### Optimistic Concurrency

For database updates with version-based conflict detection.

**Use when:**
- Multiple actors can update the same entity
- Updates should not silently overwrite each other
- Conflicts should be detected and handled

**Key invariants:**
- Version monotonicity (versions only increase)
- No lost updates (conflicts detected)
- Single writer wins (exactly one concurrent update succeeds)

### Token Rotation

For JWT refresh, session management, API key rotation.

**Use when:**
- Old token must be invalidated when new one is issued
- Concurrent refresh requests possible
- Token chain must be maintained

**Key invariants:**
- Single active token per user
- Replacement chain integrity
- No double refresh (same token refreshed twice)

### State Machine

For lifecycle management, workflow engines, order processing.

**Use when:**
- Entity has defined states
- Transitions have guards/preconditions
- Some transitions should be impossible

**Key invariants:**
- Only valid transitions occur
- Guards are respected
- Terminal states are reachable (liveness)

## Integration with Other Skills

### With findings Skill

Discoveries from TLA+ verification are captured as persistent findings:

```bash
# After TLC finds a bug
python3 ~/.claude/skills/findings/scripts/query_findings.py --capture \
  --title "Race condition in ClaimSelfRegisteredNode" \
  --severity critical \
  --type discovery \
  --category thread-safety \
  --file "src/Features/AccessPoint/RegisterAccessPointCommandHandler.cs" \
  --line 204 \
  --during "tla-verification"
```

### With azure-devops Skill

Promote TLA+ findings to work items:

```bash
# Create bug for race condition
python3 ~/.claude/skills/findings/scripts/promote_to_ado.py f-abc123 --type Bug
```

### With code-review Skill

Code review checklist includes TLA+ considerations:

- If modifying code mapped to a TLA+ spec, run verification
- If adding concurrency, consider adding TLA+ model
- Check code-spec drift after changes

### With architecture-review Skill

Architecture assessments include formal verification coverage:

```markdown
### Formal Verification
**Rating**: Partial

**Observations**:
- TLA+ specs exist for: node-registration, token-refresh
- Missing specs for: order processing, payment flow

**Recommendations**:
- P2: Add TLA+ model for payment saga pattern
- P3: Add TLA+ model for rate limiting
```

## Learning Resources

### In-Skill References

| File | Content |
|------|---------|
| `references/tlaplus-quickstart.md` | TLA+ syntax and concepts |
| `references/common-patterns.md` | Pattern catalog with examples |
| `references/tlc-optimization.md` | TLC performance tuning |
| `references/apalache-guide.md` | Symbolic model checking |
| `references/code-spec-mapping.md` | Mapping TLA+ to code |

### External Resources

- [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html) - Lamport's TLA+ book (free)
- [Learn TLA+](https://learntla.com/) - Practical tutorial
- [TLA+ Video Course](https://lamport.azurewebsites.net/video/videos.html) - By Leslie Lamport
- [AWS and TLA+](https://cacm.acm.org/magazines/2015/4/184701-how-amazon-web-services-uses-formal-methods/fulltext) - Industry case study

## Example: Complete Workflow

**Scenario:** Verify a new "order claiming" feature has no race conditions.

```bash
# 1. Generate spec from template
python3 ~/.claude/skills/tla-plus/scripts/generate_spec.py \
  --pattern optimistic-concurrency \
  --name "OrderClaiming" \
  --output specs/tla+/order-claiming/

# 2. Customize the generated spec (edit in VS Code with TLA+ extension)

# 3. Add code mappings
python3 ~/.claude/skills/tla-plus/scripts/add_mapping.py \
  --model order-claiming \
  --action "ClaimOrder" \
  --file "src/Features/Orders/ClaimOrderHandler.cs" \
  --method "Handle" \
  --line 45

# 4. Run verification
python3 ~/.claude/skills/tla-plus/scripts/run_tlc.py \
  --model order-claiming \
  --mode thorough

# 5. If counterexample found, understand it
python3 ~/.claude/skills/tla-plus/scripts/explain_counterexample.py \
  --model order-claiming

# 6. Fix the bug (add version check), re-verify

# 7. Create buggy variant for negative testing
python3 ~/.claude/skills/tla-plus/scripts/generate_buggy.py \
  --model order-claiming \
  --remove-guard "version check"

# 8. Generate CI pipeline
python3 ~/.claude/skills/tla-plus/scripts/generate_pipeline.py \
  --platform azure-devops \
  --output .azure-pipelines/tla-verification.yml

# 9. Capture as finding for documentation
python3 ~/.claude/skills/findings/scripts/query_findings.py --capture \
  --title "Order claiming verified with TLA+" \
  --type note \
  --category architecture
```

## Troubleshooting

### TLC hangs or runs forever

**Cause:** State space too large.

**Solutions:**
1. Use simulation mode: `--mode quick`
2. Reduce constants (fewer nodes, users)
3. Add state constraints
4. Use Apalache for symbolic checking

### Counterexample is confusing

**Solution:** Use explain_counterexample.py for plain English explanation.

### Spec doesn't match code

**Solution:**
1. Run drift check: `check_drift.py --model X`
2. Update mappings
3. Re-verify

### Java not found

**Solution:**
```bash
# macOS
brew install openjdk@17

# Ubuntu
sudo apt install openjdk-17-jdk

# Verify
java -version
```

### TLA+ tools not downloaded

**Solution:**
```bash
# Auto-download on first run, or manually:
curl -sL -o specs/tla+/.tools/tla2tools.jar \
  "https://github.com/tlaplus/tlaplus/releases/download/v1.8.0/tla2tools.jar"
```

## CLI Reference

All scripts are located in `~/.claude/skills/tla-plus/scripts/`.

### tla_store.py - Project Configuration

Manages TLA+ project metadata and code-to-spec mappings.

```bash
# Initialize TLA+ project
python3 scripts/tla_store.py init --specs-dir specs/tla+

# List registered models
python3 scripts/tla_store.py list

# Discover models from specs directory
python3 scripts/tla_store.py discover

# Add a new model
python3 scripts/tla_store.py add-model node-claiming \
  --description "Node claiming flow" \
  --spec-file NodeClaiming.tla

# Add code-to-spec mapping
python3 scripts/tla_store.py add-mapping \
  --model node-claiming \
  --action UserClaimNode \
  --file src/Features/AccessPoint/RegisterAccessPointCommandHandler.cs \
  --method ClaimSelfRegisteredNode \
  --line 204

# Get CI trigger paths for a model
python3 scripts/tla_store.py trigger-paths --model node-claiming
```

### run_tlc.py - TLC Model Checker

Run TLC explicit state model checker.

```bash
# List available models
python3 scripts/run_tlc.py --list

# Run specific model (quick simulation)
python3 scripts/run_tlc.py --model node-registration --mode quick

# Run with full BFS verification
python3 scripts/run_tlc.py --model node-registration --mode standard

# Run thorough verification (large config)
python3 scripts/run_tlc.py --model node-registration --mode thorough

# Run all models
python3 scripts/run_tlc.py --all --mode quick

# Output formats
python3 scripts/run_tlc.py --model X --format text|json|markdown

# Custom settings
python3 scripts/run_tlc.py --model X \
  --workers 4 \
  --depth 200000 \
  --timeout 60 \
  --config MyConfig.cfg
```

| Option | Description |
|--------|-------------|
| `--model, -m` | Model name to verify |
| `--all, -a` | Verify all models |
| `--mode` | `quick` (simulation), `standard` (BFS), `thorough` (large BFS) |
| `--config, -c` | Specific config file |
| `--workers, -w` | Number of workers (-1 = auto) |
| `--depth, -d` | Simulation depth (default: 100000) |
| `--timeout, -t` | Timeout in minutes (default: 30) |
| `--format, -f` | Output format: text, json, markdown |

### run_apalache.py - Apalache Symbolic Checker

Run Apalache symbolic model checker with Z3.

```bash
# Check installation / download Apalache
python3 scripts/run_apalache.py --check-install

# Run bounded model checking
python3 scripts/run_apalache.py --model node-registration --length 10

# Check specific invariant
python3 scripts/run_apalache.py --model X --inv SafetyInvariant

# Check if invariant is inductive
python3 scripts/run_apalache.py --model X --check-inductive --inv SafetyInvariant

# Type checking only
python3 scripts/run_apalache.py --model X --mode typecheck

# Simulation mode
python3 scripts/run_apalache.py --model X --mode simulate --length 20

# Run all models
python3 scripts/run_apalache.py --all --length 5

# Output formats
python3 scripts/run_apalache.py --model X --format text|json|markdown
```

| Option | Description |
|--------|-------------|
| `--model, -m` | Model name to verify |
| `--all, -a` | Verify all models |
| `--mode` | `check`, `typecheck`, `simulate`, `test` |
| `--length, -l` | Maximum trace length/bound (default: 10) |
| `--inv` | Specific invariant to check |
| `--check-inductive` | Check if invariant is inductive |
| `--init` | Init predicate name |
| `--next` | Next predicate name |
| `--timeout, -t` | Timeout in minutes (default: 30) |
| `--format, -f` | Output format: text, json, markdown |
| `--check-install` | Check/download Apalache installation |

### validate_spec.py - SANY Syntax Validation

Validate TLA+ specification syntax.

```bash
# List available models
python3 scripts/validate_spec.py --list

# Validate specific file
python3 scripts/validate_spec.py --file specs/tla+/node-registration/NodeRegistration.tla

# Validate all files in a model
python3 scripts/validate_spec.py --model node-registration

# Validate all models
python3 scripts/validate_spec.py --all

# Output formats
python3 scripts/validate_spec.py --model X --format text|json|markdown

# Skip structure extraction (faster)
python3 scripts/validate_spec.py --file X.tla --no-structure

# Verbose output with raw SANY output
python3 scripts/validate_spec.py --file X.tla --verbose
```

| Option | Description |
|--------|-------------|
| `--file, -f` | Specific .tla file to validate |
| `--model, -m` | Model name (validates all .tla in model dir) |
| `--all, -a` | Validate all models |
| `--no-structure` | Skip module structure extraction |
| `--timeout, -t` | Timeout in seconds (default: 60) |
| `--format` | Output format: text, json, markdown |
| `--verbose, -v` | Show detailed raw output |

### generate_spec.py - Generate from Templates

Generate TLA+ specifications from pattern templates.

```bash
# List available patterns
python3 scripts/generate_spec.py --list

# Generate from pattern (interactive)
python3 scripts/generate_spec.py \
  --pattern optimistic-concurrency \
  --name OrderLocking \
  --output specs/tla+/order-locking/

# With placeholder substitutions
python3 scripts/generate_spec.py \
  --pattern state-machine \
  --name OrderWorkflow \
  --substitute "STATES=Pending,Active,Completed" \
  --substitute "ACTORS=Users"

# Generate buggy variant
python3 scripts/generate_spec.py \
  --pattern optimistic-concurrency \
  --name OrderLocking \
  --buggy

# Dry run (preview without writing)
python3 scripts/generate_spec.py --pattern X --name Y --dry-run
```

| Option | Description |
|--------|-------------|
| `--list, -l` | List available pattern templates |
| `--pattern, -p` | Pattern template to use |
| `--name, -n` | Module name for generated spec |
| `--output, -o` | Output directory |
| `--substitute, -s` | Placeholder substitution (KEY=VALUE) |
| `--buggy` | Also generate buggy variant |
| `--interactive, -i` | Interactive mode for customization |
| `--dry-run` | Show what would be generated |
| `--no-register` | Don't register with TLAStore |

### generate_from_code.py - LLM-Assisted Extraction

Generate TLA+ specifications from source code analysis.

```bash
# Analyze source file
python3 scripts/generate_from_code.py \
  --source src/Services/OrderService.cs

# Focus on specific method
python3 scripts/generate_from_code.py \
  --source src/Services/OrderService.cs \
  --method ProcessOrder

# Specify concern type
python3 scripts/generate_from_code.py \
  --source src/Services/TokenService.cs \
  --concern race-condition

# Interactive refinement
python3 scripts/generate_from_code.py \
  --source src/Services/LockManager.cs \
  --interactive

# Dry run (show what would be generated)
python3 scripts/generate_from_code.py \
  --source X.cs \
  --dry-run \
  --format tla|json
```

| Option | Description |
|--------|-------------|
| `--source, -s` | Source file to analyze (required) |
| `--method, -m` | Specific method to focus on |
| `--concern, -c` | Concern type: race-condition, deadlock, lost-update, starvation, atomicity, ordering, general |
| `--output, -o` | Output directory |
| `--interactive, -i` | Interactive refinement mode |
| `--no-register` | Don't register with TLAStore |
| `--dry-run` | Preview without writing |
| `--format, -f` | Dry-run format: tla, json |

### generate_pipeline.py - CI Pipeline Generation

Generate CI/CD pipelines for TLA+ verification.

```bash
# Auto-detect platform and generate
python3 scripts/generate_pipeline.py --output .ci/tla-verify.yml

# Azure DevOps pipeline
python3 scripts/generate_pipeline.py \
  --platform azure-devops \
  --output .azure-pipelines/tla-verification.yml

# GitHub Actions workflow
python3 scripts/generate_pipeline.py \
  --platform github \
  --output .github/workflows/tla-verification.yml

# For specific model only
python3 scripts/generate_pipeline.py \
  --model node-registration \
  --platform azure-devops

# Dry run
python3 scripts/generate_pipeline.py --platform github --dry-run
```

| Option | Description |
|--------|-------------|
| `--platform, -p` | Platform: azure-devops, github, auto |
| `--output, -o` | Output file path |
| `--model, -m` | Specific model (default: all) |
| `--simulation-depth` | Depth for quick mode (default: 100000) |
| `--timeout` | Verification timeout in minutes |
| `--no-negative` | Skip negative testing (buggy variants) |
| `--dry-run` | Preview without writing |

### check_drift.py - Code-Spec Synchronization

Check for drift between code and TLA+ specifications.

```bash
# Check all models
python3 scripts/check_drift.py --all

# Check specific model
python3 scripts/check_drift.py --model node-registration

# Output formats
python3 scripts/check_drift.py --all --format table|json|markdown

# Include INFO level issues
python3 scripts/check_drift.py --all --include-info

# Auto-fix line number drift
python3 scripts/check_drift.py --model X --fix

# Dry run auto-fix
python3 scripts/check_drift.py --model X --fix --dry-run
```

| Option | Description |
|--------|-------------|
| `--model, -m` | Specific model to check |
| `--all, -a` | Check all models |
| `--format, -f` | Output format: table, json, markdown |
| `--include-info` | Include INFO severity issues |
| `--fix` | Auto-fix line number drift |
| `--dry-run` | Preview fixes without applying |

**Severity Levels:**
- **CRITICAL**: Mapped file no longer exists
- **HIGH**: Mapped method/function not found
- **MEDIUM**: Line number drift > 20 lines
- **LOW**: Line number drift 5-20 lines
- **INFO**: Minor drift < 5 lines

### explain_counterexample.py - Counterexample Analysis

Parse and explain TLC counterexamples.

```bash
# Explain latest counterexample for model
python3 scripts/explain_counterexample.py --model node-registration

# From specific TLC output file
python3 scripts/explain_counterexample.py \
  --tlc-output specs/tla+/node-registration/states/tlc-output.txt

# Output formats
python3 scripts/explain_counterexample.py --model X --format text|json|markdown

# Include fix suggestions
python3 scripts/explain_counterexample.py --model X --suggest-fix

# Verbose trace output
python3 scripts/explain_counterexample.py --model X --verbose
```

| Option | Description |
|--------|-------------|
| `--model, -m` | Model name (reads latest output) |
| `--tlc-output` | Specific TLC output file |
| `--format, -f` | Output format: text, json, markdown |
| `--suggest-fix` | Include fix suggestions |
| `--verbose, -v` | Verbose trace details |

### spec_to_tests.py - Test Generation

Generate unit tests from TLA+ invariants.

```bash
# List available models
python3 scripts/spec_to_tests.py --list

# Generate C# tests (xUnit)
python3 scripts/spec_to_tests.py \
  --model node-registration \
  --language csharp \
  --output tests/NodeRegistration.Invariants.Tests.cs

# Generate Python tests (pytest)
python3 scripts/spec_to_tests.py \
  --model node-registration \
  --language python \
  --framework pytest

# Generate Java tests (JUnit)
python3 scripts/spec_to_tests.py \
  --model node-registration \
  --language java \
  --framework junit

# Generate TypeScript tests (Jest)
python3 scripts/spec_to_tests.py \
  --model node-registration \
  --language typescript \
  --framework jest

# Skip negative tests
python3 scripts/spec_to_tests.py --model X --language csharp --no-negative

# Preview without writing
python3 scripts/spec_to_tests.py --model X --language csharp --dry-run
```

| Option | Description |
|--------|-------------|
| `--model, -m` | Model name (required) |
| `--language, -l` | Target: csharp, java, python, typescript |
| `--framework, -f` | Test framework (auto-detected if omitted) |
| `--output, -o` | Output file path |
| `--no-negative` | Skip negative test generation |
| `--dry-run` | Preview without writing |

**Supported Frameworks:**
- C#: xunit (default), nunit, mstest
- Java: junit
- Python: pytest
- TypeScript: jest (default), mocha

## Files Reference

| File | Purpose |
|------|---------|
| `SKILL.md` | This documentation |
| `DESIGN.md` | Detailed design document |
| `scripts/tla_store.py` | Project configuration management |
| `scripts/run_tlc.py` | TLC model checker runner |
| `scripts/run_apalache.py` | Apalache symbolic checker |
| `scripts/validate_spec.py` | SANY syntax validation |
| `scripts/generate_spec.py` | Generate spec from template |
| `scripts/generate_from_code.py` | LLM-assisted spec extraction |
| `scripts/generate_pipeline.py` | CI pipeline generator |
| `scripts/check_drift.py` | Code-spec synchronization |
| `scripts/explain_counterexample.py` | Counterexample explanation |
| `scripts/spec_to_tests.py` | Test generation from invariants |
| `templates/patterns/*.tla` | Pattern templates |
| `templates/pipelines/*.yml` | CI templates |
| `references/*.md` | Learning materials |

---

*See DESIGN.md for implementation details and ADRs.*
