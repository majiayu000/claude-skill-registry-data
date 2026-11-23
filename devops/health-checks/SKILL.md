---
name: health-checks
description: How liveness and readiness are reported - the database readiness check from Infrastructure, /health/live and /health/ready, and the Docker HEALTHCHECK. Use when adding a dependency that should affect readiness or changing the health endpoints.
metadata:
  scope: shared
---

# Health checks

## The rule

Two questions, two endpoints, in every template that runs a web host.

| Endpoint | Answers | Runs |
| --- | --- | --- |
| `/health/live` | Is the process up? | No checks. It only fails when the app can't answer at all. |
| `/health/ready` | Can it do its job? | Every check tagged `ready`, which today is the database. |

Both are anonymous and answer with plain text, because Docker, load balancers and orchestrators call them without a token. Neither is traced (`telemetry`). The Docker image's `HEALTHCHECK` calls `/health/live`. Infrastructure owns the checks for what it talks to (`AddInfrastructureHealthChecks` in `src/Infrastructure/DependencyInjection.cs`); Presentation maps the endpoints. The Lambda template has no health endpoints, because Lambda manages its own lifecycle.

## Steps

1. New external dependency in Infrastructure (a queue, another database)? Add its check inside `AddInfrastructureHealthChecks` and pass the `tags` through, so it lands on readiness.
2. Keep liveness free of dependency checks. A database outage shouldn't get the container restarted.
3. Test both endpoints with a real request (`integration-tests`).

## Example

```csharp
// src/Infrastructure/DependencyInjection.cs
public static IHealthChecksBuilder AddInfrastructureHealthChecks(this IHealthChecksBuilder builder, params string[] tags)
{
    return builder.AddDbContextCheck<MovieReviewsDbContext>("MovieReviewsDatabase", HealthStatus.Unhealthy, tags);
}
```

## Don't

- Put a dependency check on `/health/live`.
- Require authentication on either endpoint.
- Return version or configuration details from a health endpoint. Anyone can call it; the version is on every span, metric and log as `service.version`, and behind auth at the version endpoint.

## Check

``` bash
dotnet test --filter "FullyQualifiedName~Health"
```
