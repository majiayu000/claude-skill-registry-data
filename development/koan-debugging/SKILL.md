---
name: koan-debugging
description: Framework-specific troubleshooting, boot report analysis, common error patterns
---

# Koan Framework Debugging

## Core Principle

**Framework-specific debugging focuses on boot reports, provider elections, and auto-registration patterns** rather than generic .NET troubleshooting.

## Quick Diagnostics

```bash
# Check boot logs for framework initialization
docker logs koan-app --tail 20 --follow | grep "Koan:"

# Expected success patterns:
[INFO] Koan:discover postgresql: server=localhost... OK
[INFO] Koan:modules data→postgresql
[INFO] Koan:modules web→controllers
[INFO] Koan:modules ai→openai
[INFO] Koan:modules MyApp v1.0.0
```

## Debugging Categories

### 1. Bootstrap and Initialization Issues

**Symptom:** Service not found in DI container
```
System.InvalidOperationException: Unable to resolve service for type 'ITodoService'
```

**Diagnosis:**
1. Check if `KoanAutoRegistrar` exists at `/Initialization/KoanAutoRegistrar.cs`
2. Verify class implements `IKoanAutoRegistrar`
3. Verify class is `public` (not `internal`)
4. Check boot logs for module registration

**Solution:**
```csharp
// Verify KoanAutoRegistrar is discoverable
public sealed class KoanAutoRegistrar : IKoanAutoRegistrar
{
    public string ModuleName => "MyApp";

    public void Initialize(IServiceCollection services)
    {
        services.AddScoped<ITodoService, TodoService>();
    }

    public void Describe(BootReport report, IConfiguration cfg, IHostEnvironment env)
    {
        report.AddModule(ModuleName, "1.0.0");
    }
}
```

---

**Symptom:** Module not discovered
```
[WARNING] Koan:modules MyModule not found
```

**Diagnosis:**
1. Verify `<ProjectReference>` or `<PackageReference>` exists
2. Check assembly is copied to output directory
3. Verify namespace and class visibility

**Solution:**
```xml
<!-- Ensure project reference exists -->
<ProjectReference Include="..\MyModule\MyModule.csproj" />
```

### 2. Entity and Data Layer Issues

**Symptom:** ID not generated
```
System.InvalidOperationException: Entity ID is required but not set
```

**Diagnosis:**
- Using `Entity<T, TKey>` with custom key type requires manual ID assignment
- Verify entity inherits `Entity<T>` (not `Entity<T, TKey>`)

**Solution:**
```csharp
// ✅ CORRECT: Auto GUID v7 generation
public class Todo : Entity<Todo>
{
    public string Title { get; set; } = "";
}

// OR: Manual key management
public class NumericTodo : Entity<NumericTodo, int>
{
    public override int Id { get; set; } // Must set manually
}
```

---

**Symptom:** Query not working
```
System.NotSupportedException: Provider does not support LINQ queries
```

**Diagnosis:**
- Provider lacks LINQ support (JSON, InMemory, Redis)
- Need client-side filtering

**Solution:**
```csharp
// Check capabilities first
var caps = Data<Todo, string>.QueryCaps;

if (caps.Capabilities.HasFlag(QueryCapabilities.LinqQueries))
{
    return await Todo.Query(t => t.Completed);
}
else
{
    var all = await Todo.All();
    return all.Where(t => t.Completed).ToList();
}
```

### 3. Multi-Provider Issues

**Symptom:** Provider not available
```
[ERROR] Koan:discover mongodb: connection failed
[INFO] Koan:modules data→json (fallback)
```

**Diagnosis:**
1. Verify service is running (Docker, local install)
2. Check connection string in `appsettings.json`
3. Verify network connectivity
4. Check provider package is referenced

**Solution:**
```json
// Verify configuration
{
  "Koan": {
    "Data": {
      "Sources": {
        "Default": {
          "Adapter": "mongodb",
          "ConnectionString": "mongodb://localhost:27017/myapp"
        }
      }
    }
  }
}
```

```bash
# Test MongoDB connectivity
docker ps | grep mongo
docker logs mongo-container
```

---

**Symptom:** Wrong provider elected
```
[INFO] Koan:modules data→json (expected: mongodb)
```

**Diagnosis:**
- Configuration missing or incorrect
- Provider package not referenced
- Connection failed, fallback activated

**Solution:**
```csharp
// Force specific provider with attribute
[DataAdapter("mongodb")]
public class Todo : Entity<Todo>
{
    public string Title { get; set; } = "";
}

// Or verify boot report
if (KoanEnv.IsDevelopment)
{
    KoanEnv.DumpSnapshot(logger);
}
```

### 4. Performance and Optimization Issues

**Symptom:** N+1 query problem
```
// App making hundreds of queries
[DEBUG] Executing query: SELECT * FROM Todo WHERE Id = 'id1'
[DEBUG] Executing query: SELECT * FROM Todo WHERE Id = 'id2'
[DEBUG] Executing query: SELECT * FROM Todo WHERE Id = 'id3'
... (repeated hundreds of times)
```

**Diagnosis:**
- Loading entities in loop instead of batch
- Not using batch retrieval

**Solution:**
```csharp
// ❌ WRONG: N queries
foreach (var id in ids)
{
    var todo = await Todo.Get(id);
}

// ✅ CORRECT: 1 query
var todos = await Todo.Get(ids);
```

---

**Symptom:** Out of memory
```
System.OutOfMemoryException: Array dimensions exceeded supported range
```

**Diagnosis:**
- Loading large dataset with `.All()` instead of streaming
- Materializing everything into memory

**Solution:**
```csharp
// ❌ WRONG: Loads everything into memory
var allTodos = await Todo.All(); // 1 million records!

// ✅ CORRECT: Stream in batches
await foreach (var todo in Todo.AllStream(batchSize: 1000))
{
    await ProcessTodo(todo);
}
```

### 5. Container and Environment Issues

**Symptom:** Container fails to start
```
[ERROR] Application startup exception
[ERROR] Unable to connect to database
```

**Diagnosis:**
1. Check container networking (wrong host references)
2. Verify Docker Compose service dependencies
3. Check health check endpoints

**Solution:**
```yaml
# docker-compose.yml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U koan"]
      interval: 5s
      timeout: 5s
      retries: 5
```

```json
// Use container hostname, not localhost
{
  "Koan": {
    "Data": {
      "Sources": {
        "Default": {
          "ConnectionString": "Host=postgres;Database=myapp"
        }
      }
    }
  }
}
```

### 6. Framework-Specific Error Patterns

**Auto-Registration Errors**
- **Symptom**: Service not found in DI
- **Cause**: Missing `KoanAutoRegistrar` or assembly not loaded
- **Solution**: Verify file exists, implements interface, is public

**Provider Capability Mismatches**
- **Symptom**: Query features not working as expected
- **Cause**: Provider doesn't support specific capabilities
- **Solution**: Check `QueryCaps` and implement graceful fallbacks

**Entity Pattern Violations**
- **Symptom**: ID generation issues or manual repository injection
- **Cause**: Not using `Entity<T>` patterns properly
- **Solution**: Migrate to entity-first patterns with proper inheritance

**Context Routing Conflicts**
- **Symptom**: Data going to wrong partition/source
- **Cause**: Nested contexts or Source+Adapter conflict
- **Solution**: Follow Source XOR Adapter rule, check context nesting

## Boot Report Analysis

### Enabling Detailed Boot Reporting

```csharp
// In Development environment
if (KoanEnv.IsDevelopment)
{
    var logger = app.Services.GetRequiredService<ILogger<Program>>();
    KoanEnv.DumpSnapshot(logger);
}
```

### Reading Boot Report

```
[INFO] Koan:discover postgresql: server=localhost;database=myapp;username=koan;password=*** OK
[INFO] Koan:discover mongodb: connection timeout FAILED
[INFO] Koan:modules data→postgresql (elected: connection successful)
[INFO] Koan:modules web→controllers (discovered: 5 controllers)
[INFO] Koan:modules ai→openai (api_key present, model: gpt-4)
[INFO] Koan:modules MyApp v1.0.0 (services: TodoService, EmailService)
[WARNING] Email SMTP configuration missing - using console fallback
```

**What to look for:**
- ✅ `OK` status for expected providers
- ✅ Correct provider elections (`data→postgresql`)
- ✅ Your modules listed with version
- ⚠️ Warnings about missing configuration
- ❌ `FAILED` status for critical services

## Debug Provider Capabilities

```csharp
// Log capabilities for current provider
var caps = Data<Todo, string>.QueryCaps;
logger.LogInformation("Provider: {Provider}", caps.ProviderName);
logger.LogInformation("Capabilities: {Capabilities}", caps.Capabilities);

// Check specific capabilities
if (caps.Capabilities.HasFlag(QueryCapabilities.LinqQueries))
{
    logger.LogInformation("Provider supports server-side LINQ");
}

if (caps.Capabilities.HasFlag(QueryCapabilities.Transactions))
{
    logger.LogInformation("Provider supports transactions");
}

if (Todo.SupportsFastRemove)
{
    logger.LogInformation("Provider supports TRUNCATE/DROP");
}
```

## Environment Detection Debug

```csharp
logger.LogInformation("Environment: {Env}", KoanEnv.CurrentEnvironment);
logger.LogInformation("IsDevelopment: {Dev}", KoanEnv.IsDevelopment);
logger.LogInformation("IsProduction: {Prod}", KoanEnv.IsProduction);
logger.LogInformation("InContainer: {Container}", KoanEnv.InContainer);
logger.LogInformation("AllowMagicInProduction: {Magic}", KoanEnv.AllowMagicInProduction);
```

## Common Debug Commands

```bash
# Container development workflow
./start.bat  # Always use project start scripts

# View structured logs
docker logs koan-app --tail 20 --follow | grep "Koan:"

# Check assembly discovery
docker exec koan-app ls /app/*.dll

# Test database connectivity
docker exec postgres-container psql -U koan -d myapp -c "SELECT 1"

# Check Redis connectivity
docker exec redis-container redis-cli PING
```

## When This Skill Applies

Invoke this skill when:
- ✅ Troubleshooting errors
- ✅ Analyzing boot failures
- ✅ Debugging provider issues
- ✅ Investigating performance problems
- ✅ Validating initialization
- ✅ Reviewing boot reports

## Reference Documentation

- **Troubleshooting Guides:** `docs/guides/troubleshooting/`
- **Bootstrap Failures:** `docs/guides/troubleshooting/bootstrap-failures.md`
- **Adapter Issues:** `docs/guides/troubleshooting/adapter-connection-issues.md`
- **Deep Dive:** `docs/guides/deep-dive/bootstrap-lifecycle.md`
