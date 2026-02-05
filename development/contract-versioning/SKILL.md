---
name: contract-versioning
description: Contract versioning strategies and compatibility management
allowed-tools: Read, Glob, Grep, Write, Edit
---

# Contract Versioning Skill

## When to Use This Skill

Use this skill when:

- **Contract Versioning tasks** - Working on contract versioning strategies and compatibility management
- **Planning or design** - Need guidance on Contract Versioning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Manage contract versions, compatibility requirements, and deprecation strategies.

## MANDATORY: Documentation-First Approach

Before defining versioning strategies:

1. **Invoke `docs-management` skill** for versioning patterns
2. **Verify Pact broker patterns** via MCP servers (perplexity)
3. **Base guidance on contract versioning best practices**

## Contract Versioning Concepts

```text
CONTRACT VERSIONING DIMENSIONS:

┌─────────────────────────────────────────────────────────────────┐
│                    VERSIONING DIMENSIONS                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CONSUMER VERSION                                            │
│     └── Which version of consumer generated the contract        │
│                                                                 │
│  2. PROVIDER VERSION                                            │
│     └── Which version of provider verified the contract         │
│                                                                 │
│  3. CONTRACT VERSION (Implicit)                                 │
│     └── The contract itself (changes when consumer changes)     │
│                                                                 │
│  4. API VERSION                                                 │
│     └── Semantic version of the API (may be in path/header)     │
│                                                                 │
│  5. PACT SPECIFICATION VERSION                                  │
│     └── Version of Pact spec (2, 3, 4)                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Version Identification Strategies

```text
VERSION IDENTIFICATION:

┌─────────────────────────────────────────────────────────────────┐
│ Strategy          │ Example              │ When to Use          │
├─────────────────────────────────────────────────────────────────┤
│ Git SHA           │ abc123def            │ Precise tracking     │
│ Git Tag           │ v1.2.3               │ Releases             │
│ Build Number      │ build-456            │ CI/CD pipelines      │
│ Semantic Version  │ 1.2.3                │ API versions         │
│ Branch + SHA      │ main-abc123          │ Branch tracking      │
│ Timestamp         │ 2024-01-15T10:30:00  │ Simple ordering      │
└─────────────────────────────────────────────────────────────────┘

RECOMMENDED: Git SHA for CI/CD, Semantic Version for releases
```

## Pact Broker Versioning

```text
PACT BROKER VERSION TRACKING:

Publishing Contracts:
┌─────────────────────────────────────────────────────────────────┐
│ pact-broker publish ./pacts \                                   │
│   --broker-base-url https://broker.example.com \               │
│   --consumer-app-version ${GIT_SHA} \    ← Git SHA              │
│   --branch ${GIT_BRANCH} \               ← Branch name          │
│   --tag ${GIT_TAG}                       ← Optional release tag │
└─────────────────────────────────────────────────────────────────┘

Publishing Verification:
┌─────────────────────────────────────────────────────────────────┐
│ Verifier publishes:                                             │
│   --provider-version ${GIT_SHA}                                │
│   --provider-branch ${GIT_BRANCH}                              │
│   --provider-tags ${ENVIRONMENT}                               │
└─────────────────────────────────────────────────────────────────┘

Environment Tracking:
┌─────────────────────────────────────────────────────────────────┐
│ pact-broker record-deployment \                                │
│   --pacticipant OrdersApi \                                    │
│   --version ${GIT_SHA} \                                       │
│   --environment production                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Consumer Version Selectors

```csharp
// Provider verification with version selectors
verifier.WithPactBrokerSource(brokerUri, options =>
{
    options.ConsumerVersionSelectors(
        // Always verify against latest main
        new ConsumerVersionSelector { MainBranch = true },

        // Verify against deployed versions
        new ConsumerVersionSelector { DeployedOrReleased = true },

        // Verify against matching branch (for feature branches)
        new ConsumerVersionSelector { MatchingBranch = true },

        // Verify against specific environment
        new ConsumerVersionSelector { Environment = "production" }
    );

    // Publish results with version info
    options.PublishVerificationResults(
        providerVersion: gitSha,
        providerBranch: gitBranch);
});
```

## API Versioning in Contracts

```text
API VERSIONING STRATEGIES:

1. URL PATH VERSIONING
   /v1/orders/123
   /v2/orders/123

   Contract implications:
   • Different paths = different interactions
   • Each version needs separate contracts
   • Consumer specifies which version they use

2. HEADER VERSIONING
   Accept: application/vnd.api.v1+json
   Api-Version: 2

   Contract implications:
   • Include header in contract
   • Same path, different header = different interaction
   • Flexible but harder to track

3. QUERY PARAMETER VERSIONING
   /orders/123?version=1
   /orders/123?api-version=2

   Contract implications:
   • Query param in contract
   • Easy to see version in contract file
   • Less RESTful

RECOMMENDATION: URL path for major versions, headers for minor negotiation
```

## Multi-Version Contract Example

```csharp
// Consumer tests for multiple API versions
public class OrdersClientV1ConsumerTests
{
    private readonly IPactBuilderV4 _pactBuilder;

    public OrdersClientV1ConsumerTests()
    {
        var pact = Pact.V4("OrdersClient", "OrdersApi-V1");
        _pactBuilder = pact.WithHttpInteractions();
    }

    [Fact]
    public async Task GetOrder_V1_ReturnsLegacyFormat()
    {
        _pactBuilder
            .UponReceiving("a v1 request for an order")
            .Given("an order exists")
            .WithRequest(HttpMethod.Get, "/v1/orders/123")
            .WillRespond()
            .WithStatus(200)
            .WithJsonBody(new
            {
                order_id = Match.Type("123"),       // v1 uses snake_case
                customer_id = Match.Type("c-456"),
                order_status = Match.Type("pending")
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new OrdersClientV1(ctx.MockServerUri);
            var result = await client.GetOrderAsync("123");
            Assert.NotNull(result);
        });
    }
}

public class OrdersClientV2ConsumerTests
{
    private readonly IPactBuilderV4 _pactBuilder;

    public OrdersClientV2ConsumerTests()
    {
        var pact = Pact.V4("OrdersClient", "OrdersApi-V2");
        _pactBuilder = pact.WithHttpInteractions();
    }

    [Fact]
    public async Task GetOrder_V2_ReturnsModernFormat()
    {
        _pactBuilder
            .UponReceiving("a v2 request for an order")
            .Given("an order exists")
            .WithRequest(HttpMethod.Get, "/v2/orders/123")
            .WillRespond()
            .WithStatus(200)
            .WithJsonBody(new
            {
                id = Match.Type("123"),            // v2 uses camelCase
                customerId = Match.Type("c-456"),
                status = Match.Type("pending"),
                metadata = Match.Type(new { })    // v2 adds metadata
            });

        await _pactBuilder.VerifyAsync(async ctx =>
        {
            var client = new OrdersClientV2(ctx.MockServerUri);
            var result = await client.GetOrderAsync("123");
            Assert.NotNull(result);
        });
    }
}
```

## Deprecation Strategy

```text
DEPRECATION WORKFLOW:

Phase 1: ANNOUNCE (Week 0)
┌─────────────────────────────────────────────────────────────────┐
│ • Document deprecation in changelog                             │
│ • Add deprecation header: Deprecation: true                     │
│ • Notify consumers via team channels                            │
│ • Update API documentation                                       │
└─────────────────────────────────────────────────────────────────┘

Phase 2: WARN (Weeks 1-4)
┌─────────────────────────────────────────────────────────────────┐
│ • Return Sunset header: Sunset: Sat, 15 Feb 2025 00:00:00 GMT   │
│ • Log usage of deprecated endpoints                             │
│ • Reach out to heavy users                                      │
│ • Provide migration guides                                       │
└─────────────────────────────────────────────────────────────────┘

Phase 3: MIGRATE (Weeks 5-8)
┌─────────────────────────────────────────────────────────────────┐
│ • Monitor migration progress via Pact Broker                    │
│ • Track which consumers still use old version                   │
│ • Support consumers having issues                               │
│ • Extend deadline if needed                                      │
└─────────────────────────────────────────────────────────────────┘

Phase 4: REMOVE (After Week 8)
┌─────────────────────────────────────────────────────────────────┐
│ • Verify no consumers depend on deprecated version              │
│ • Use can-i-deploy to confirm safety                           │
│ • Remove old version from provider                              │
│ • Update contract verification selectors                        │
└─────────────────────────────────────────────────────────────────┘
```

## Migration Tracking with Pact Broker

```text
TRACKING CONSUMER MIGRATION:

1. IDENTIFY CONSUMERS ON OLD VERSION
   Query Pact Broker for contracts using /v1 paths:

   GET /pacts/provider/OrdersApi/latest
   → Shows all consumers and their versions
   → Filter by interaction paths containing /v1

2. MONITOR MIGRATION PROGRESS
   Dashboard showing:
   - Consumers still on v1: [OrdersUI, MobileApp]
   - Consumers migrated to v2: [AdminPortal, ReportsService]
   - Consumer migration dates

3. BLOCK DEPLOYMENT IF BREAKING
   pact-broker can-i-deploy \
     --pacticipant OrdersApi \
     --version ${NEW_VERSION} \
     --ignore OrdersUI \     # Temporarily ignore during migration
     --to-environment production

4. ENFORCE MIGRATION DEADLINE
   After deadline:
   - Remove --ignore flags
   - Deployments blocked until consumers migrate
```

## Version Compatibility Matrix

```text
COMPATIBILITY MATRIX EXAMPLE:

                    │ Provider v1.0 │ Provider v2.0 │ Provider v2.1 │
────────────────────┼───────────────┼───────────────┼───────────────┤
Consumer v1.0       │      ✓        │      ✗        │      ✗        │
Consumer v1.5       │      ✓        │      ✓        │      ✓        │
Consumer v2.0       │      ✗        │      ✓        │      ✓        │
Consumer v2.1       │      ✗        │      ✗        │      ✓        │

Legend:
✓ = Verified compatible
✗ = Not compatible / Not tested

Pact Broker provides this automatically via verification matrix:
GET /matrix?q[][pacticipant]=OrdersClient&q[][pacticipant]=OrdersApi
```

## Semantic Versioning for Contracts

```text
SEMVER FOR API CONTRACTS:

MAJOR (X.0.0):
• Breaking changes to contract
• Removed endpoints/fields
• Changed field types
• Required field additions
• Consumer MUST update

MINOR (1.X.0):
• New optional fields
• New endpoints
• Backward compatible additions
• Consumer MAY update

PATCH (1.0.X):
• Bug fixes
• Documentation updates
• No contract changes
• Consumer unaffected

CONTRACT EVOLUTION RULES:
┌────────────────────────┬────────────┬─────────────┐
│ Change                 │ Semver     │ Breaking?   │
├────────────────────────┼────────────┼─────────────┤
│ Add optional field     │ Minor      │ No          │
│ Add required field     │ Major      │ Yes         │
│ Remove field           │ Major      │ Yes         │
│ Change field type      │ Major      │ Yes         │
│ Add new endpoint       │ Minor      │ No          │
│ Remove endpoint        │ Major      │ Yes         │
│ Change response code   │ Major      │ Yes         │
│ Relax validation       │ Minor      │ No          │
│ Tighten validation     │ Major      │ Yes         │
└────────────────────────┴────────────┴─────────────┘
```

## Can-I-Deploy Workflow

```text
CAN-I-DEPLOY USAGE:

Before Consumer Deployment:
┌─────────────────────────────────────────────────────────────────┐
│ pact-broker can-i-deploy \                                      │
│   --pacticipant OrdersClient \                                 │
│   --version ${CONSUMER_VERSION} \                              │
│   --to-environment production                                   │
│                                                                 │
│ Checks: Is this consumer version compatible with provider       │
│         version currently in production?                        │
└─────────────────────────────────────────────────────────────────┘

Before Provider Deployment:
┌─────────────────────────────────────────────────────────────────┐
│ pact-broker can-i-deploy \                                      │
│   --pacticipant OrdersApi \                                    │
│   --version ${PROVIDER_VERSION} \                              │
│   --to-environment production                                   │
│                                                                 │
│ Checks: Is this provider version compatible with all consumer   │
│         versions currently in production?                       │
└─────────────────────────────────────────────────────────────────┘

Environment Record:
┌─────────────────────────────────────────────────────────────────┐
│ After successful deployment:                                    │
│ pact-broker record-deployment \                                │
│   --pacticipant OrdersApi \                                    │
│   --version ${VERSION} \                                       │
│   --environment production                                      │
└─────────────────────────────────────────────────────────────────┘
```

## Assessment Template

```markdown
# Contract Versioning Assessment: [API Name]

## Versioning Strategy

- **Consumer Version Format:** [Git SHA/Semver/Build Number]
- **Provider Version Format:** [Git SHA/Semver/Build Number]
- **API Versioning:** [URL Path/Header/Query]
- **Current API Versions:** [v1, v2, etc.]

## Version Tracking

| Participant | Current Version | Environment | Branch |
|-------------|-----------------|-------------|--------|
| [Name] | [Version] | [Env] | [Branch] |

## Deprecation Schedule

| Version | Announced | Sunset Date | Status |
|---------|-----------|-------------|--------|
| [v1] | [Date] | [Date] | [Active/Warning/Deprecated/Removed] |

## Consumer Migration Status

| Consumer | Current API | Target API | Migration Status |
|----------|-------------|------------|------------------|
| [Name] | [v1] | [v2] | [Not Started/In Progress/Complete] |

## CI/CD Integration

- [ ] Consumer version published with Git SHA
- [ ] Provider version published with Git SHA
- [ ] Branch tracking enabled
- [ ] Can-I-Deploy in pipeline
- [ ] Environment recording configured

## Compatibility Matrix

[Include current compatibility matrix from Pact Broker]

## Action Items

| Action | Owner | Due Date |
|--------|-------|----------|
| [Action] | [Owner] | [Date] |
```

## Workflow

When managing contract versions:

1. **Choose Version Scheme**: Git SHA for tracking, semver for releases
2. **Configure Publishing**: Publish with version, branch, tags
3. **Setup Version Selectors**: MainBranch, DeployedOrReleased
4. **Track Environments**: Record deployments to environments
5. **Monitor Compatibility**: Use can-i-deploy before releases
6. **Manage Deprecations**: Follow structured deprecation process

## References

For detailed guidance:

---

**Last Updated:** 2025-12-26
