---
name: tenant-provisioning
description: Automated tenant onboarding infrastructure patterns. Covers provisioning workflows, resource creation, seed data, and tenant readiness verification.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Tenant Provisioning Skill

Patterns for automating the creation and setup of new tenants in multi-tenant SaaS applications.

## When to Use This Skill

Use this skill when:

- **Tenant Provisioning tasks** - Working on automated tenant onboarding infrastructure patterns. covers provisioning workflows, resource creation, seed data, and tenant readiness verification
- **Planning or design** - Need guidance on Tenant Provisioning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Tenant provisioning is the process of creating all resources needed for a new tenant to use the application. Speed and reliability of provisioning directly impact customer experience and operational efficiency.

## Provisioning Architecture

```text
+------------------------------------------------------------------+
|                  Tenant Provisioning Flow                         |
+------------------------------------------------------------------+
|                                                                   |
|  +----------+   +-------------+   +-------------+   +---------+  |
|  | Signup   |-->| Validation  |-->| Provisioner |-->| Ready   |  |
|  | Request  |   | & Approval  |   | Workflow    |   | State   |  |
|  +----------+   +-------------+   +-------------+   +---------+  |
|                                          |                        |
|                    +---------------------+---------------------+  |
|                    |                     |                     |  |
|                    v                     v                     v  |
|              +-----------+        +-----------+        +---------+|
|              | Database  |        | Storage   |        | Config  ||
|              | Schema    |        | Container |        | Entries ||
|              +-----------+        +-----------+        +---------+|
|                                                                   |
+------------------------------------------------------------------+
```

## Provisioning Models

### Synchronous (Simple)

```text
Use When:
- Pool model (shared resources)
- Fast provisioning (<5 seconds)
- Low complexity setup

Flow:
Signup -> Validate -> Create Tenant Record -> Apply Defaults -> Ready
```

### Asynchronous (Complex)

```text
Use When:
- Silo model (dedicated resources)
- Long-running provisioning (>30 seconds)
- Multiple external dependencies

Flow:
Signup -> Validate -> Queue Job -> [Background Process] -> Ready
         ↓
    Return "Provisioning..."
         ↓
    Poll/Webhook for completion
```

## Provisioning Steps

### Step Catalog

```text
Common Provisioning Steps:
+------------------------------------------------------------------+
| Step                    | Model      | Duration    | Rollback   |
+-------------------------+------------+-------------+------------+
| Create tenant record    | All        | <1s         | Delete     |
| Create admin user       | All        | <1s         | Delete     |
| Apply default settings  | All        | <1s         | N/A        |
| Seed sample data        | All        | 1-5s        | Delete     |
| Create database schema  | Bridge     | 5-30s       | Drop       |
| Create database         | Silo       | 30s-2min    | Drop       |
| Create storage account  | Silo       | 30s-1min    | Delete     |
| Configure DNS           | Silo       | 1-5min      | Remove     |
| Provision SSL cert      | Silo       | 1-5min      | Revoke     |
+-------------------------+------------+-------------+------------+
```

### Provisioning Workflow

```csharp
public sealed class TenantProvisioningWorkflow(
    IDbContext db,
    ITenantSettingsService settings,
    ISeedDataService seedData,
    IStorageProvisioner storage,
    ILogger<TenantProvisioningWorkflow> logger)
{
    public async Task<ProvisioningResult> ProvisionAsync(
        TenantProvisioningRequest request,
        CancellationToken ct)
    {
        var steps = new List<ProvisioningStepResult>();
        Guid? tenantId = null;

        try
        {
            // Step 1: Create tenant record
            tenantId = await CreateTenantRecordAsync(request, ct);
            steps.Add(ProvisioningStepResult.Success("create_tenant"));

            // Step 2: Create admin user
            await CreateAdminUserAsync(tenantId.Value, request.AdminEmail, ct);
            steps.Add(ProvisioningStepResult.Success("create_admin"));

            // Step 3: Apply default settings
            await settings.ApplyDefaultsAsync(tenantId.Value, request.Plan, ct);
            steps.Add(ProvisioningStepResult.Success("apply_settings"));

            // Step 4: Seed sample data (if requested)
            if (request.IncludeSampleData)
            {
                await seedData.SeedAsync(tenantId.Value, ct);
                steps.Add(ProvisioningStepResult.Success("seed_data"));
            }

            // Step 5: Provision storage (if silo model)
            if (request.IsolationLevel == IsolationLevel.Silo)
            {
                await storage.ProvisionAsync(tenantId.Value, ct);
                steps.Add(ProvisioningStepResult.Success("provision_storage"));
            }

            // Mark tenant as ready
            await MarkTenantReadyAsync(tenantId.Value, ct);

            return ProvisioningResult.Success(tenantId.Value, steps);
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Provisioning failed for {Email}", request.AdminEmail);

            // Rollback completed steps
            if (tenantId.HasValue)
            {
                await RollbackAsync(tenantId.Value, steps, ct);
            }

            return ProvisioningResult.Failed(ex.Message, steps);
        }
    }

    private async Task RollbackAsync(
        Guid tenantId,
        List<ProvisioningStepResult> completedSteps,
        CancellationToken ct)
    {
        // Rollback in reverse order
        foreach (var step in completedSteps.AsEnumerable().Reverse())
        {
            try
            {
                await RollbackStepAsync(tenantId, step.StepId, ct);
            }
            catch (Exception ex)
            {
                logger.LogError(ex, "Rollback failed for step {Step}", step.StepId);
                // Continue rollback despite failures
            }
        }
    }
}
```

## Pool Model Provisioning

### Fast Provisioning

```csharp
public sealed class PoolTenantProvisioner(IDbContext db) : ITenantProvisioner
{
    public async Task<Guid> ProvisionAsync(
        TenantProvisioningRequest request,
        CancellationToken ct)
    {
        // All in single transaction - fast and atomic
        await using var transaction = await db.Database.BeginTransactionAsync(ct);

        try
        {
            // Create tenant
            var tenant = new Tenant
            {
                Id = Guid.NewGuid(),
                Name = request.CompanyName,
                Subdomain = request.Subdomain,
                Plan = request.Plan,
                Status = TenantStatus.Active,
                CreatedAt = DateTimeOffset.UtcNow
            };
            db.Tenants.Add(tenant);

            // Create admin user
            var adminUser = new User
            {
                Id = Guid.NewGuid(),
                TenantId = tenant.Id,
                Email = request.AdminEmail,
                Role = UserRole.Admin,
                CreatedAt = DateTimeOffset.UtcNow
            };
            db.Users.Add(adminUser);

            // Apply default settings
            var defaultSettings = GetDefaultSettings(request.Plan);
            foreach (var setting in defaultSettings)
            {
                db.TenantSettings.Add(new TenantSetting
                {
                    TenantId = tenant.Id,
                    Key = setting.Key,
                    Value = setting.Value
                });
            }

            await db.SaveChangesAsync(ct);
            await transaction.CommitAsync(ct);

            return tenant.Id;
        }
        catch
        {
            await transaction.RollbackAsync(ct);
            throw;
        }
    }
}
```

## Silo Model Provisioning

### Async Provisioning with Saga

```csharp
public sealed class SiloProvisioningSaga
{
    private readonly List<IProvisioningStep> _steps;

    public SiloProvisioningSaga(IServiceProvider services)
    {
        _steps =
        [
            services.GetRequiredService<CreateDatabaseStep>(),
            services.GetRequiredService<ApplyMigrationsStep>(),
            services.GetRequiredService<CreateStorageContainerStep>(),
            services.GetRequiredService<SeedDataStep>(),
            services.GetRequiredService<ConfigureDnsStep>(),
            services.GetRequiredService<ProvisionSslStep>()
        ];
    }

    public async Task<SagaResult> ExecuteAsync(
        TenantProvisioningRequest request,
        CancellationToken ct)
    {
        var context = new ProvisioningContext(request);
        var completedSteps = new Stack<IProvisioningStep>();

        try
        {
            foreach (var step in _steps)
            {
                await step.ExecuteAsync(context, ct);
                completedSteps.Push(step);

                // Report progress
                await ReportProgressAsync(context, step, ct);
            }

            return SagaResult.Success(context.TenantId);
        }
        catch (Exception ex)
        {
            // Compensate in reverse order
            while (completedSteps.TryPop(out var step))
            {
                try
                {
                    await step.CompensateAsync(context, ct);
                }
                catch (Exception compensateEx)
                {
                    // Log but continue compensation
                    context.Errors.Add(compensateEx);
                }
            }

            return SagaResult.Failed(ex, context.Errors);
        }
    }
}

// Example step
public sealed class CreateDatabaseStep : IProvisioningStep
{
    public string StepId => "create_database";

    public async Task ExecuteAsync(ProvisioningContext context, CancellationToken ct)
    {
        var dbName = $"tenant_{context.TenantId}";
        await _dbProvisioner.CreateDatabaseAsync(dbName, ct);
        context.Data["database_name"] = dbName;
    }

    public async Task CompensateAsync(ProvisioningContext context, CancellationToken ct)
    {
        if (context.Data.TryGetValue("database_name", out var dbName))
        {
            await _dbProvisioner.DropDatabaseAsync((string)dbName, ct);
        }
    }
}
```

## Progress Tracking

### Provisioning Status

```csharp
public sealed record ProvisioningStatus
{
    public required Guid TenantId { get; init; }
    public required ProvisioningState State { get; init; }
    public required List<StepStatus> Steps { get; init; }
    public decimal ProgressPercent => Steps.Count > 0
        ? (decimal)Steps.Count(s => s.IsCompleted) / Steps.Count * 100
        : 0;
    public string? CurrentStep { get; init; }
    public string? ErrorMessage { get; init; }
    public DateTimeOffset StartedAt { get; init; }
    public DateTimeOffset? CompletedAt { get; init; }
}

public enum ProvisioningState
{
    Pending,
    InProgress,
    Completed,
    Failed,
    RolledBack
}

public sealed record StepStatus
{
    public required string StepId { get; init; }
    public required string DisplayName { get; init; }
    public required bool IsCompleted { get; init; }
    public required bool IsFailed { get; init; }
    public string? ErrorMessage { get; init; }
}
```

### Progress API

```csharp
[ApiController]
[Route("api/provisioning")]
public class ProvisioningController : ControllerBase
{
    [HttpGet("{tenantId}/status")]
    public async Task<ActionResult<ProvisioningStatus>> GetStatus(Guid tenantId)
    {
        var status = await _provisioningService.GetStatusAsync(tenantId);
        return Ok(status);
    }

    [HttpGet("{tenantId}/status/stream")]
    public async Task StreamStatus(Guid tenantId, CancellationToken ct)
    {
        Response.ContentType = "text/event-stream";

        await foreach (var update in _provisioningService.StreamUpdatesAsync(tenantId, ct))
        {
            await Response.WriteAsync($"data: {JsonSerializer.Serialize(update)}\n\n", ct);
            await Response.Body.FlushAsync(ct);
        }
    }
}
```

## Seed Data

### Sample Data Seeding

```csharp
public sealed class SeedDataService(IDbContext db) : ISeedDataService
{
    public async Task SeedAsync(Guid tenantId, CancellationToken ct)
    {
        // Seed sample project
        var project = new Project
        {
            Id = Guid.NewGuid(),
            TenantId = tenantId,
            Name = "My First Project",
            Description = "Welcome! This is a sample project to help you get started.",
            CreatedAt = DateTimeOffset.UtcNow
        };
        db.Projects.Add(project);

        // Seed sample tasks
        var tasks = new[]
        {
            new ProjectTask
            {
                Id = Guid.NewGuid(),
                ProjectId = project.Id,
                TenantId = tenantId,
                Title = "Explore the dashboard",
                Description = "Take a tour of the main features",
                Status = TaskStatus.Todo
            },
            new ProjectTask
            {
                Id = Guid.NewGuid(),
                ProjectId = project.Id,
                TenantId = tenantId,
                Title = "Invite your team",
                Description = "Add team members to collaborate",
                Status = TaskStatus.Todo
            },
            new ProjectTask
            {
                Id = Guid.NewGuid(),
                ProjectId = project.Id,
                TenantId = tenantId,
                Title = "Connect your tools",
                Description = "Set up integrations with your existing tools",
                Status = TaskStatus.Todo
            }
        };
        db.Tasks.AddRange(tasks);

        await db.SaveChangesAsync(ct);
    }
}
```

## Validation

### Pre-Provisioning Validation

```csharp
public sealed class ProvisioningValidator
{
    public async Task<ValidationResult> ValidateAsync(
        TenantProvisioningRequest request,
        CancellationToken ct)
    {
        var errors = new List<string>();

        // Validate subdomain
        if (!IsValidSubdomain(request.Subdomain))
            errors.Add("Invalid subdomain format");

        if (await IsSubdomainTakenAsync(request.Subdomain, ct))
            errors.Add("Subdomain already in use");

        // Validate email
        if (!IsValidEmail(request.AdminEmail))
            errors.Add("Invalid email format");

        if (await IsEmailRegisteredAsync(request.AdminEmail, ct))
            errors.Add("Email already registered");

        // Validate plan
        if (!IsValidPlan(request.Plan))
            errors.Add("Invalid plan selected");

        return errors.Count > 0
            ? ValidationResult.Failed(errors)
            : ValidationResult.Success();
    }
}
```

## Best Practices

```text
Provisioning Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Idempotent steps            | Safe retries                       |
| Saga with compensation      | Clean rollback on failure          |
| Progress reporting          | User confidence                    |
| Async for slow operations   | Don't block signup                 |
| Validate before provision   | Fail fast                          |
| Seed sample data            | Faster time to value               |
| Health check before ready   | Ensure usability                   |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Sync silo provisioning | Blocks signup for minutes | Async with progress UI |
| No rollback on failure | Orphaned resources | Saga pattern |
| No progress feedback | User thinks it's broken | Real-time status updates |
| Hard-coded seed data | Stale samples | Configurable templates |
| Skip validation | Errors mid-provision | Validate upfront |

## References

Load for detailed implementation:

- `references/provisioning-workflows.md` - Workflow patterns
- `references/saga-patterns.md` - Compensation handling

## Related Skills

- `tenancy-models` - Pool/Silo/Bridge model selection
- `tenant-lifecycle` - State management after provisioning
- `database-isolation` - Database provisioning patterns

## MCP Research

For current provisioning patterns:

```text
perplexity: "SaaS tenant provisioning 2024" "saga pattern compensation"
microsoft-learn: "Azure resource provisioning" "Durable Functions orchestration"
```
