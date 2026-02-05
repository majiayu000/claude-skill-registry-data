---
name: breaking-change-detection
description: Detect and analyze breaking changes in API contracts
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Breaking Change Detection Skill

## When to Use This Skill

Use this skill when:

- **Breaking Change Detection tasks** - Working on detect and analyze breaking changes in api contracts
- **Planning or design** - Need guidance on Breaking Change Detection approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Detect, analyze, and manage breaking changes in API contracts.

## MANDATORY: Documentation-First Approach

Before analyzing breaking changes:

1. **Invoke `docs-management` skill** for compatibility patterns
2. **Verify change detection patterns** via MCP servers (perplexity)
3. **Base guidance on API compatibility best practices**

## Breaking Change Categories

```text
BREAKING CHANGE TAXONOMY:

┌─────────────────────────────────────────────────────────────────┐
│                    BREAKING CHANGES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STRUCTURAL CHANGES                                             │
│  ├── Remove endpoint                                            │
│  ├── Remove field from response                                 │
│  ├── Remove query/path parameter                                │
│  ├── Change field type (string → number)                        │
│  ├── Change array to single value (or vice versa)               │
│  └── Change object structure (flatten/nest)                     │
│                                                                 │
│  SEMANTIC CHANGES                                               │
│  ├── Change field meaning (same name, different data)           │
│  ├── Change enum values (remove options)                        │
│  ├── Change date/time format                                    │
│  ├── Change numeric precision                                   │
│  └── Change null handling                                       │
│                                                                 │
│  CONTRACT CHANGES                                               │
│  ├── Make optional field required                               │
│  ├── Tighten validation rules                                   │
│  ├── Reduce allowed values                                      │
│  ├── Add required headers                                       │
│  └── Change authentication requirements                         │
│                                                                 │
│  BEHAVIORAL CHANGES                                             │
│  ├── Change response codes (200 → 201)                          │
│  ├── Change error response format                               │
│  ├── Change pagination behavior                                 │
│  ├── Change sorting default                                     │
│  └── Change rate limiting                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Breaking vs Non-Breaking Changes

```text
CHANGE CLASSIFICATION:

BREAKING (❌ Requires consumer update):
┌────────────────────────────────────────────────────────────────┐
│ • Remove field: { name, email } → { name }                     │
│ • Change type: { age: "25" } → { age: 25 }                     │
│ • Remove endpoint: DELETE /v1/users                            │
│ • Required field: { email? } → { email }                       │
│ • Rename field: { user_name } → { username }                   │
│ • Change path: /users/{id} → /customers/{id}                   │
│ • Remove enum: ["A","B","C"] → ["A","B"]                        │
│ • Change code: 200 OK → 201 Created                            │
└────────────────────────────────────────────────────────────────┘

NON-BREAKING (✓ Safe to deploy):
┌────────────────────────────────────────────────────────────────┐
│ • Add optional field: { name } → { name, bio? }                │
│ • Add endpoint: POST /users/bulk                               │
│ • Add enum value: ["A","B"] → ["A","B","C"]                     │
│ • Relax validation: maxLength 50 → maxLength 100               │
│ • Add optional query param: ?filter=                           │
│ • Widen type: int → int|null                                   │
│ • Add response header: X-Request-Id                            │
└────────────────────────────────────────────────────────────────┘

POTENTIALLY BREAKING (⚠️ Context-dependent):
┌────────────────────────────────────────────────────────────────┐
│ • Change default value                                          │
│ • Change order of array items                                   │
│ • Change precision of numbers                                   │
│ • Change date format (ISO 8601 variant)                         │
│ • Add required response field (may break lenient parsers)       │
└────────────────────────────────────────────────────────────────┘
```

## Detection with Contract Tests

```text
PACT-BASED DETECTION:

How Pact Catches Breaking Changes:

1. CONSUMER DEFINES EXPECTATIONS
   Consumer test: "I expect { id, name, email }"

2. PROVIDER REMOVES FIELD
   Provider response: { id, name }

3. VERIFICATION FAILS
   Error: $.email was not found in response

4. DEPLOYMENT BLOCKED
   can-i-deploy returns: ❌ Cannot deploy

DETECTION MATRIX:
┌────────────────────────┬─────────────────────────────────────────┐
│ Change                 │ How Pact Catches It                     │
├────────────────────────┼─────────────────────────────────────────┤
│ Remove field           │ Response body mismatch                  │
│ Change type            │ Type mismatch in matching rules         │
│ Remove endpoint        │ 404 instead of expected status          │
│ Required field added   │ Request validation fails                │
│ Auth change            │ 401/403 instead of expected status      │
│ Enum removed           │ Regex match fails                       │
│ Path change            │ 404 on old path                         │
└────────────────────────┴─────────────────────────────────────────┘
```

## Impact Analysis

```csharp
// Breaking change impact analyzer
// File: ContractAnalyzer/BreakingChangeAnalyzer.cs

public class BreakingChangeAnalyzer
{
    private readonly IPactBrokerClient _broker;

    public async Task<ImpactAnalysis> AnalyzeChange(
        string provider,
        string affectedEndpoint,
        BreakingChangeType changeType)
    {
        // Get all consumers of this provider
        var pacts = await _broker.GetLatestPactsForProvider(provider);

        var impactedConsumers = new List<ImpactedConsumer>();

        foreach (var pact in pacts)
        {
            // Check if consumer uses the affected endpoint
            var interactions = pact.Interactions
                .Where(i => InteractionAffected(i, affectedEndpoint, changeType))
                .ToList();

            if (interactions.Any())
            {
                impactedConsumers.Add(new ImpactedConsumer
                {
                    ConsumerName = pact.Consumer.Name,
                    ConsumerVersion = pact.Consumer.Version,
                    AffectedInteractions = interactions.Select(i => i.Description),
                    DeployedEnvironments = await GetDeployedEnvironments(pact.Consumer),
                    ContactTeam = await GetTeamContact(pact.Consumer.Name)
                });
            }
        }

        return new ImpactAnalysis
        {
            Provider = provider,
            ChangeType = changeType,
            AffectedEndpoint = affectedEndpoint,
            ImpactedConsumers = impactedConsumers,
            TotalConsumers = pacts.Count,
            ImpactedConsumerCount = impactedConsumers.Count,
            SafeToDeploy = impactedConsumers.Count == 0,
            Recommendation = GenerateRecommendation(impactedConsumers)
        };
    }

    private bool InteractionAffected(
        Interaction interaction,
        string endpoint,
        BreakingChangeType changeType)
    {
        // Check if this interaction uses the affected endpoint
        if (!interaction.Request.Path.Contains(endpoint))
            return false;

        // For field removal, check if response uses the field
        if (changeType == BreakingChangeType.FieldRemoval)
        {
            // Parse interaction to check field usage
            return true; // Simplified - real implementation parses body
        }

        return true;
    }

    private string GenerateRecommendation(List<ImpactedConsumer> impacted)
    {
        if (!impacted.Any())
            return "Safe to deploy. No consumers affected.";

        var inProduction = impacted.Where(c =>
            c.DeployedEnvironments.Contains("production")).ToList();

        if (inProduction.Any())
        {
            return $"BLOCKED: {inProduction.Count} consumers in production affected. " +
                   $"Coordinate with: {string.Join(", ", inProduction.Select(c => c.ContactTeam))}";
        }

        return $"WARNING: {impacted.Count} consumers affected (not in production). " +
               "Coordinate migration before their deployment.";
    }
}

public record ImpactAnalysis
{
    public string Provider { get; init; }
    public BreakingChangeType ChangeType { get; init; }
    public string AffectedEndpoint { get; init; }
    public List<ImpactedConsumer> ImpactedConsumers { get; init; }
    public int TotalConsumers { get; init; }
    public int ImpactedConsumerCount { get; init; }
    public bool SafeToDeploy { get; init; }
    public string Recommendation { get; init; }
}

public enum BreakingChangeType
{
    FieldRemoval,
    TypeChange,
    EndpointRemoval,
    RequiredFieldAddition,
    AuthenticationChange,
    ResponseCodeChange
}
```

## OpenAPI Diff Detection

```text
OPENAPI-BASED DETECTION:

Tools:
• openapi-diff (Java)
• oasdiff (Go)
• optic (Node.js)
• Swagger Compare

Example with oasdiff:
┌─────────────────────────────────────────────────────────────────┐
│ oasdiff breaking original.yaml updated.yaml                    │
│                                                                 │
│ Output:                                                         │
│ ❌ GET /orders/{id}                                             │
│    - removed property: 'legacy_id' from response                │
│ ❌ POST /orders                                                  │
│    - property 'metadata' changed from optional to required      │
│ ✓ GET /orders                                                   │
│    - added optional property: 'page_token' to response          │
└─────────────────────────────────────────────────────────────────┘

CI Integration:
┌─────────────────────────────────────────────────────────────────┐
│ - name: Check for breaking changes                              │
│   run: |                                                        │
│     oasdiff breaking \                                          │
│       --base main:api/openapi.yaml \                           │
│       --revision HEAD:api/openapi.yaml \                       │
│       --fail-on ERR                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Breaking Change Response Workflow

```text
BREAKING CHANGE RESPONSE:

When Breaking Change is Detected:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. IDENTIFY IMPACT                                             │
│     ├── Which consumers affected?                               │
│     ├── Which environments?                                     │
│     └── How critical is each consumer?                          │
│                                                                 │
│  2. CHOOSE STRATEGY                                             │
│     ├── A) Don't make the change                                │
│     ├── B) Version the API (v1 → v2)                            │
│     ├── C) Coordinate consumer migration                        │
│     └── D) Feature flag the change                              │
│                                                                 │
│  3. EXECUTE STRATEGY                                            │
│     ├── If B: Create new version, maintain old                  │
│     ├── If C: Contact teams, set timeline                       │
│     └── If D: Roll out gradually                                │
│                                                                 │
│  4. VERIFY RESOLUTION                                           │
│     ├── All consumers migrated                                  │
│     ├── can-i-deploy passes                                     │
│     └── Old version deprecated                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Compatibility Strategies

```text
MAINTAINING COMPATIBILITY:

1. ADDITIVE CHANGES ONLY
   - Only add new fields, endpoints, options
   - Never remove or rename
   - Old consumers ignore new fields

2. VERSIONED ENDPOINTS
   - /v1/orders continues to work
   - /v2/orders has breaking changes
   - Support both during migration

3. EXPAND-CONTRACT PATTERN
   Phase 1: Add new field alongside old
   Phase 2: Migrate consumers to new field
   Phase 3: Remove old field

   Example:
   Phase 1: { user_name: "x", username: "x" }
   Phase 2: Consumers switch to username
   Phase 3: { username: "x" }

4. TOLERANT READER PATTERN
   - Consumers ignore unknown fields
   - Consumers handle missing optional fields
   - Reduces breaking change surface

5. FEATURE FLAGS
   - New behavior behind flag
   - Enable per-consumer or gradually
   - Rollback if issues
```

## Detection Checklist

```markdown
# Breaking Change Detection Checklist

## Before Making API Changes

### Structural Changes
- [ ] Are any fields being removed?
- [ ] Are any fields being renamed?
- [ ] Are any types being changed?
- [ ] Are any endpoints being removed?
- [ ] Are any paths being changed?

### Contract Changes
- [ ] Are any optional fields becoming required?
- [ ] Are any validation rules being tightened?
- [ ] Are any allowed values being reduced?
- [ ] Are any new required headers being added?

### Behavioral Changes
- [ ] Are any response codes changing?
- [ ] Are any default values changing?
- [ ] Are any sorting/ordering behaviors changing?
- [ ] Are any pagination behaviors changing?

## Impact Analysis
- [ ] Run oasdiff/openapi-diff against main
- [ ] Query Pact Broker for affected consumers
- [ ] Identify consumers in production
- [ ] Document affected teams and contacts

## Mitigation Planning
- [ ] Chosen strategy: [Version/Migrate/Feature Flag]
- [ ] Migration timeline defined
- [ ] Consumer teams notified
- [ ] Deprecation schedule set

## Verification
- [ ] All affected consumers updated
- [ ] can-i-deploy passes for all environments
- [ ] Old version deprecated (if applicable)
- [ ] Documentation updated
```

## CI Pipeline Integration

```yaml
# Breaking change detection in CI
# .github/workflows/api-changes.yml

name: API Change Detection

on:
  pull_request:
    paths:
      - 'api/**'
      - 'src/**/*.cs'

jobs:
  detect-breaking:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get base OpenAPI spec
        run: git show origin/main:api/openapi.yaml > base.yaml

      - name: Detect breaking changes
        id: detect
        run: |
          oasdiff breaking base.yaml api/openapi.yaml --format json > changes.json
          BREAKING=$(jq '.breaking | length' changes.json)
          echo "breaking_count=$BREAKING" >> $GITHUB_OUTPUT

      - name: Comment on PR
        if: steps.detect.outputs.breaking_count > 0
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const changes = JSON.parse(fs.readFileSync('changes.json'));
            const body = `## ⚠️ Breaking API Changes Detected

            ${changes.breaking.map(c => `- ${c.path}: ${c.message}`).join('\n')}

            Please ensure:
            1. These changes are intentional
            2. Consumer teams have been notified
            3. Migration plan is documented`;

            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body
            });

      - name: Fail if breaking
        if: steps.detect.outputs.breaking_count > 0
        run: |
          echo "::error::${{ steps.detect.outputs.breaking_count }} breaking changes detected"
          exit 1
```

## Workflow

When detecting breaking changes:

1. **Integrate Detection**: Add oasdiff/Pact to CI
2. **Block on Breaking**: Fail builds that introduce breaks
3. **Analyze Impact**: Query broker for affected consumers
4. **Plan Mitigation**: Version, migrate, or feature flag
5. **Coordinate Migration**: Work with consumer teams
6. **Verify Safety**: Can-i-deploy before release

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
