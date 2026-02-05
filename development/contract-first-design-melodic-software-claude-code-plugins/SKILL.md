---
name: contract-first-design
description: Design and manage API contracts before implementation using OpenAPI and AsyncAPI specifications for contract-first development
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Contract-First Design Skill

## When to Use This Skill

Use this skill when:

- **Contract First Design tasks** - Working on design and manage api contracts before implementation using openapi and asyncapi specifications for contract-first development
- **Planning or design** - Need guidance on Contract First Design approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Apply contract-first development methodology for APIs, ensuring specifications drive implementation.

## Contract-First Methodology

### Core Principles

```yaml
contract_first_principles:
  design_before_code:
    description: "API specification comes before implementation"
    benefits:
      - "Early feedback from consumers"
      - "Parallel development enabled"
      - "Clear contract for testing"
      - "Documentation from day one"

  specification_as_source_of_truth:
    description: "Spec is authoritative, code conforms to it"
    enforcement:
      - "Generate code from spec"
      - "Validate implementation against spec"
      - "CI/CD gates on spec compliance"

  consumer_centric:
    description: "Design for consumer needs, not provider convenience"
    practices:
      - "Involve consumers in design reviews"
      - "Consumer-driven contract testing"
      - "Gather real-world usage patterns"

  evolution_over_revolution:
    description: "Evolve contracts without breaking consumers"
    practices:
      - "Semantic versioning"
      - "Backward compatibility by default"
      - "Deprecation before removal"
```

### Development Workflow

```yaml
contract_first_workflow:
  phases:
    1_design:
      activities:
        - "Identify API consumers and use cases"
        - "Define resources and operations"
        - "Draft specification (OpenAPI/AsyncAPI)"
        - "Review with stakeholders"
      artifacts:
        - "Draft API specification"
        - "Use case documentation"
      gate: "Specification approved by consumers"

    2_validate:
      activities:
        - "Lint specification for style/standards"
        - "Check backward compatibility"
        - "Generate mock server"
        - "Consumer acceptance testing with mocks"
      artifacts:
        - "Lint report"
        - "Compatibility report"
        - "Mock server configuration"
      gate: "Consumers validated against mocks"

    3_implement:
      activities:
        - "Generate server stubs"
        - "Implement business logic"
        - "Contract testing against spec"
        - "Integration testing"
      artifacts:
        - "Generated code"
        - "Contract test results"
      gate: "Implementation passes contract tests"

    4_publish:
      activities:
        - "Publish specification to catalog"
        - "Generate documentation"
        - "Update changelog"
        - "Notify consumers"
      artifacts:
        - "Published specification"
        - "API documentation portal"
        - "Changelog entry"
      gate: "Documentation live, consumers notified"

    5_operate:
      activities:
        - "Monitor API usage"
        - "Collect consumer feedback"
        - "Track breaking change requests"
        - "Plan next version"
      artifacts:
        - "Usage metrics"
        - "Feedback log"
        - "Deprecation schedule"
```

## Contract Management

### Specification Organization

```yaml
specification_organization:
  directory_structure:
    recommended:
      specs/
        openapi/
          order-service.yaml
          customer-service.yaml
          inventory-service.yaml
        asyncapi/
          order-events.yaml
          inventory-events.yaml
        shared/
          schemas/
            common-types.yaml
            error-responses.yaml
          parameters/
            pagination.yaml
          security/
            auth-schemes.yaml

  file_naming:
    pattern: "{service-name}.yaml"
    versioned: "{service-name}-v{major}.yaml"

  modular_specs:
    description: "Split large specs into components"
    approach:
      main_file: "Defines paths, references components"
      components_dir: "Reusable schemas, parameters, responses"
      shared_dir: "Cross-API shared definitions"

    example_main:
      openapi: "3.1.0"
      info:
        title: "Order Service API"
        version: "1.0.0"
      paths:
        $ref: "./paths/orders.yaml"
      components:
        schemas:
          $ref: "./schemas/_index.yaml"
```

### Version Management

```yaml
version_management:
  semantic_versioning:
    major: "Breaking changes"
    minor: "Backward-compatible additions"
    patch: "Backward-compatible fixes"

  version_in_spec:
    location: "info.version"
    format: "MAJOR.MINOR.PATCH"

  api_versioning_strategies:
    url_path:
      spec_example:
        servers:
          - url: "https://api.example.com/v1"
      change_approach: "New spec file for major versions"

    header:
      spec_example:
        parameters:
          API-Version:
            in: header
            required: false
            schema:
              type: string
              default: "2025-01-01"

  changelog_requirements:
    location: "CHANGELOG.md alongside spec"
    format: "Keep a Changelog"
    content:
      - "Version number and date"
      - "Added: new endpoints/fields"
      - "Changed: modified behavior"
      - "Deprecated: marked for removal"
      - "Removed: breaking deletions"
      - "Fixed: bug fixes"
      - "Security: vulnerability patches"
```

### Breaking Change Detection

```yaml
breaking_changes:
  definition: "Changes that can break existing consumers"

  openapi_breaking:
    removals:
      - "Remove endpoint"
      - "Remove required response field"
      - "Remove enum value"
      - "Remove supported content type"

    modifications:
      - "Change field type"
      - "Add required request field"
      - "Narrow validation (smaller max, larger min)"
      - "Change authentication requirements"

    renames:
      - "Rename field (equivalent to remove + add)"
      - "Change endpoint path"

  asyncapi_breaking:
    removals:
      - "Remove channel"
      - "Remove message type"
      - "Remove required payload field"

    modifications:
      - "Change payload schema incompatibly"
      - "Change channel address format"
      - "Modify required headers"

  detection_tools:
    openapi:
      - "openapi-diff"
      - "oasdiff"
      - "speccy"
    asyncapi:
      - "asyncapi/diff"

  ci_integration:
    script: |
      # Compare current spec against main branch
      oasdiff breaking main.yaml current.yaml
      if [ $? -ne 0 ]; then
        echo "Breaking changes detected!"
        exit 1
      fi
```

## C# Models for Contract Management

```csharp
namespace SpecDrivenDevelopment.ContractFirst;

/// <summary>
/// Represents an API contract lifecycle state
/// </summary>
public enum ContractStatus
{
    Draft,
    InReview,
    Approved,
    Implementing,
    Published,
    Deprecated,
    Retired
}

/// <summary>
/// API contract metadata
/// </summary>
public record ApiContract
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required string Version { get; init; }
    public required ContractType Type { get; init; }
    public required ContractStatus Status { get; init; }
    public required string SpecificationPath { get; init; }
    public string? Description { get; init; }
    public List<string> Owners { get; init; } = [];
    public List<string> Consumers { get; init; } = [];
    public DateTimeOffset CreatedAt { get; init; }
    public DateTimeOffset? PublishedAt { get; init; }
    public DateTimeOffset? DeprecatedAt { get; init; }
    public DateTimeOffset? SunsetAt { get; init; }
}

public enum ContractType
{
    OpenApi,
    AsyncApi,
    GraphQL,
    gRPC
}

/// <summary>
/// Tracks changes between contract versions
/// </summary>
public record ContractChange
{
    public required string ContractId { get; init; }
    public required string FromVersion { get; init; }
    public required string ToVersion { get; init; }
    public required ChangeType Type { get; init; }
    public required BreakingLevel Breaking { get; init; }
    public required string Path { get; init; }
    public required string Description { get; init; }
    public string? MigrationGuide { get; init; }
}

public enum ChangeType
{
    Added,
    Modified,
    Deprecated,
    Removed
}

public enum BreakingLevel
{
    None,
    Minor,     // Backward compatible
    Major      // Breaking change
}

/// <summary>
/// Contract validation result
/// </summary>
public record ContractValidationResult
{
    public required bool IsValid { get; init; }
    public List<ValidationIssue> Issues { get; init; } = [];
    public List<ContractChange> Changes { get; init; } = [];
    public bool HasBreakingChanges => Changes.Any(c => c.Breaking == BreakingLevel.Major);
}

public record ValidationIssue
{
    public required ValidationSeverity Severity { get; init; }
    public required string Code { get; init; }
    public required string Message { get; init; }
    public required string Path { get; init; }
    public string? Suggestion { get; init; }
}

public enum ValidationSeverity
{
    Error,
    Warning,
    Info
}

/// <summary>
/// Consumer contract registration
/// </summary>
public record ConsumerContract
{
    public required string ConsumerId { get; init; }
    public required string ConsumerName { get; init; }
    public required string ProviderId { get; init; }
    public required string ProviderVersion { get; init; }
    public List<string> UsedEndpoints { get; init; } = [];
    public List<string> UsedSchemas { get; init; } = [];
    public DateTimeOffset RegisteredAt { get; init; }
    public DateTimeOffset? LastVerifiedAt { get; init; }
}

/// <summary>
/// Service for contract management
/// </summary>
public interface IContractService
{
    Task<ApiContract> CreateContractAsync(CreateContractRequest request);
    Task<ApiContract> GetContractAsync(string id);
    Task<IReadOnlyList<ApiContract>> ListContractsAsync(ContractFilter? filter = null);
    Task<ContractValidationResult> ValidateContractAsync(string id);
    Task<ContractValidationResult> CompareVersionsAsync(string id, string fromVersion, string toVersion);
    Task PublishContractAsync(string id);
    Task DeprecateContractAsync(string id, DateTimeOffset sunsetDate);
    Task RegisterConsumerAsync(string contractId, ConsumerContract consumer);
    Task<IReadOnlyList<ConsumerContract>> GetConsumersAsync(string contractId);
}

public record CreateContractRequest
{
    public required string Name { get; init; }
    public required ContractType Type { get; init; }
    public required string SpecificationContent { get; init; }
    public string? Description { get; init; }
    public List<string> Owners { get; init; } = [];
}

public record ContractFilter
{
    public ContractType? Type { get; init; }
    public ContractStatus? Status { get; init; }
    public string? Owner { get; init; }
    public string? Consumer { get; init; }
}
```

## Contract Testing

### Provider Verification

```yaml
provider_verification:
  description: "Verify implementation matches specification"

  approaches:
    schema_validation:
      description: "Validate request/response against spec"
      tools:
        - "express-openapi-validator"
        - "NSwag middleware"
        - "Spectral"

    contract_tests:
      description: "Test endpoints match spec exactly"
      tools:
        - "Dredd"
        - "Schemathesis"
        - "Prism"

  dotnet_example:
    integration_test: |
      [Fact]
      public async Task GetOrder_ReturnsValidResponse()
      {
          // Arrange
          var spec = await OpenApiDocument.FromFileAsync("specs/order-service.yaml");
          var validator = new OpenApiValidator(spec);

          // Act
          var response = await _client.GetAsync("/orders/123");
          var body = await response.Content.ReadAsStringAsync();

          // Assert
          var result = validator.ValidateResponse(
              "/orders/{orderId}",
              "get",
              (int)response.StatusCode,
              body);

          Assert.True(result.IsValid, result.ErrorMessage);
      }

  ci_pipeline:
    steps:
      - "Load OpenAPI/AsyncAPI spec"
      - "Start application under test"
      - "Run contract tests against all endpoints"
      - "Fail build if any contract violation"
```

### Consumer-Driven Contracts

```yaml
consumer_driven_contracts:
  description: "Consumers define expected provider behavior"

  workflow:
    1_consumer_defines:
      action: "Consumer creates contract with expected interactions"
      artifact: "Pact file or similar contract"

    2_provider_verifies:
      action: "Provider runs consumer contracts"
      validation: "Provider can satisfy all consumer expectations"

    3_publish:
      action: "Publish verified contracts to broker"
      enables: "Can-I-Deploy checks"

  pact_example:
    consumer_test: |
      [Fact]
      public async Task GetOrder_ExpectedBehavior()
      {
          var pact = Pact.V3("OrderConsumer", "OrderProvider");

          pact.Given("Order 123 exists")
              .UponReceiving("A request for order 123")
              .WithRequest(HttpMethod.Get, "/orders/123")
              .WillRespond()
              .WithStatus(200)
              .WithJsonBody(new
              {
                  id = "123",
                  status = Match.Type("pending"),
                  totalAmount = Match.Decimal(99.99m)
              });

          await pact.VerifyAsync(async ctx =>
          {
              var client = new OrderClient(ctx.MockServerUri);
              var order = await client.GetOrderAsync("123");
              Assert.NotNull(order);
          });
      }

  asyncapi_contracts:
    approach: "Message schema contracts"
    verification:
      - "Producer publishes valid messages"
      - "Consumer can deserialize all message versions"
      - "Schema registry enforces compatibility"
```

## API Governance

### Style Guidelines

```yaml
api_style_guidelines:
  naming:
    resources:
      - "Use plural nouns (users, orders, products)"
      - "Use kebab-case for multi-word (order-items)"
      - "Avoid verbs in resource names"

    operations:
      - "operationId: camelCase (getUser, createOrder)"
      - "Consistent verb usage across APIs"

    fields:
      - "camelCase for JSON properties"
      - "Consistent date format (ISO 8601)"
      - "Use standard field names (id, createdAt, updatedAt)"

  structure:
    versioning: "URL path versioning (/v1/)"
    pagination: "Cursor-based or offset, consistent approach"
    errors: "RFC 7807 Problem Details"
    filtering: "Query parameters with consistent naming"

  security:
    authentication: "OAuth 2.0 / API Key as standard"
    authorization: "Scopes documented in spec"
    sensitive_data: "Never in URL parameters"

  documentation:
    required:
      - "Summary for every operation"
      - "Description for complex operations"
      - "Examples for request/response bodies"
      - "Error response documentation"
```

### Automated Enforcement

```yaml
automated_enforcement:
  linting:
    tools:
      - "Spectral (OpenAPI)"
      - "AsyncAPI Studio"
      - "Redocly CLI"

    spectral_rules: |
      extends: ["spectral:oas", "spectral:asyncapi"]

      rules:
        operation-operationId:
          severity: error
        operation-summary:
          severity: error
        operation-tags:
          severity: warn
        info-contact:
          severity: error
        response-error-format:
          description: "Errors must use RFC 7807"
          severity: error
          given: "$.paths.*.*.responses[?(@property >= '400')]"
          then:
            field: content.application/problem+json
            function: truthy

  breaking_change_detection:
    ci_step: |
      - name: Check Breaking Changes
        run: |
          oasdiff breaking \
            --base main:specs/api.yaml \
            --revision HEAD:specs/api.yaml \
            --fail-on ERR

  pre_commit_hooks:
    config: |
      repos:
        - repo: local
          hooks:
            - id: lint-openapi
              name: Lint OpenAPI
              entry: spectral lint specs/**/*.yaml
              language: node
              types: [yaml]
```

### API Catalog

```yaml
api_catalog:
  purpose: "Central registry of all API contracts"

  features:
    discovery: "Find APIs by name, domain, capability"
    documentation: "Auto-generated from specs"
    versioning: "Track all versions and changes"
    dependencies: "Consumer/provider relationships"
    metrics: "Usage, errors, latency"

  metadata_per_api:
    identity:
      - "Name and description"
      - "Owner team"
      - "Domain/capability"
    lifecycle:
      - "Current version"
      - "Status (draft/published/deprecated)"
      - "Sunset date if deprecated"
    consumers:
      - "Registered consumers"
      - "Usage statistics"
    quality:
      - "Documentation score"
      - "Test coverage"
      - "Breaking change history"

  integration:
    specification_source: "Git repository"
    ci_cd: "Publish on merge to main"
    portal: "Developer portal generation"
```

## Validation Checklist

```yaml
contract_first_checklist:
  pre_design:
    - "Consumer use cases documented"
    - "Resource model defined"
    - "Authentication/authorization strategy chosen"
    - "Versioning strategy agreed"

  specification:
    - "Valid OpenAPI/AsyncAPI syntax"
    - "Passes linting rules"
    - "All operations have operationId"
    - "Examples provided for complex types"
    - "Error responses documented"
    - "Security schemes defined"

  review:
    - "Consumer representatives reviewed"
    - "No unnecessary breaking changes"
    - "Backward compatibility verified"
    - "Documentation complete"

  implementation:
    - "Generated stubs used"
    - "Contract tests passing"
    - "Response validation enabled"
    - "Schema changes go through spec first"

  publication:
    - "Changelog updated"
    - "Catalog entry created"
    - "Consumers notified"
    - "Deprecation warnings if applicable"
```

## References

- Related skill: `openapi-authoring` - OpenAPI specification authoring
- Related skill: `asyncapi-authoring` - AsyncAPI specification authoring
- Related skill: `gherkin-authoring` - Acceptance criteria in Gherkin format

---

**Last Updated:** 2025-12-26
