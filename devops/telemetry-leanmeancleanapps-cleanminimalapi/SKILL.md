---
name: telemetry
description: How OpenTelemetry traces, metrics and logs work - the standard OTEL_* settings that switch exporting on, the span LoggingBehaviour gives every use case, EF Core's built-in metrics, what each presentation layer instruments, the Aspire dashboard in Docker Compose, and the signals we're waiting on. Use when adding a span, metric or tag, changing what's exported or where, reading telemetry locally, or adding a dependency that should be traced.
metadata:
  scope: shared
---

# Telemetry

## The rule

Telemetry is OpenTelemetry, and it leaves the app over OTLP and nothing else. No vendor SDK, no Aspire package, nothing that ties the code to one backend. Signals come from stable Microsoft and OpenTelemetry instrumentation; we write our own only where nothing covers it, and that's one span per use case. Traces and metrics are always collected; they're exported, with the logs, only when `OTEL_EXPORTER_OTLP_ENDPOINT` is set. Every standard `OTEL_*` setting works as the OpenTelemetry SDK documents it.

| Signal | What we send | Where it comes from |
| --- | --- | --- |
| Traces | A span for each incoming request and each use case, plus outgoing HTTP calls | Presentation instrumentation, `LoggingBehaviour` |
| Metrics | EF Core's own meter, ASP.NET Core, HttpClient and runtime metrics, with exemplars linking a measurement to a trace | `Microsoft.EntityFrameworkCore`, Presentation instrumentation |
| Logs | Every Serilog event, carrying the trace and span IDs of whatever was running when it was written. Validation failures and missing entities are logged inside the use case span, so they sit on its trace | Serilog's OpenTelemetry sink (`serilog`) |
| Baggage | Propagated with the trace context by the ASP.NET Core and HttpClient instrumentation | W3C `baggage` header |
| Events | An `exception` event on the use case span for unexpected errors | `LoggingBehaviour` |

Each layer publishes under its own name, and only the presentation layer's startup knows about the OpenTelemetry SDK:

| Layer | Publishes | How |
| --- | --- | --- |
| Application | `ApplicationTelemetry.Name` activity source: a span per use case, named after the request, tagged with `application.request.name` and `application.request.outcome` | `LoggingBehaviour`, with `System.Diagnostics` only, so Application stays free of telemetry packages |
| Infrastructure | `Microsoft.EntityFrameworkCore` meter: queries, saves, active contexts, compiled query cache | Built into EF Core; startup subscribes to it by name |
| Presentation | `service.name`, `service.version` and `deployment.environment.name` on everything, plus its own instrumentation | `TelemetrySettings` and the startup's Telemetry region |

What each presentation layer adds:

| Template | Instrumentation |
| --- | --- |
| Minimal API, Web API | ASP.NET Core and HttpClient traces and metrics, runtime metrics and, with authentication, its meters. Health endpoints aren't traced |
| GraphQL | The same, plus Hot Chocolate's resolver and operation spans from `HotChocolate.Diagnostics` |
| MCP | The same, plus the MCP SDK's own `Experimental.ModelContextProtocol` spans and `mcp.*.operation.duration` metrics |
| Lambda | A span per invocation from `OpenTelemetry.Instrumentation.AWSLambda`, and runtime metrics. Traces and metrics are flushed before the function returns, because Lambda can freeze the environment as soon as it does |

The Lambda template builds its tracer and meter providers once in `Startup` with `Sdk.CreateTracerProviderBuilder()` and `Sdk.CreateMeterProviderBuilder()` rather than `AddOpenTelemetry()`, because the classes Lambda Annotations generates build two service providers from the same services, and each would otherwise export everything again. X-Ray context extraction is off, so a "not sampled" header from Lambda can't switch tracing off; the collector can still send to X-Ray. Lambda container images can't use layers, so in AWS the collector is either built into the image (the ADOT collector extension) or runs as a gateway.

The app sends to an OpenTelemetry Collector, never straight to a backend, because that's how it should run in production: the collector owns batching, retries, sampling, scrubbing and the choice of backend, so none of that lives in the app. `otel-collector.yaml` holds its configuration: an OTLP receiver on 4317 (gRPC) and 4318 (HTTP), the `memory_limiter` and `batch` processors, and one exporter per backend.

Locally, Docker Compose runs the collector (`otel/opentelemetry-collector`) and the Aspire dashboard (`mcr.microsoft.com/dotnet/aspire-dashboard`), and the collector forwards everything to the dashboard. The dashboard is only a container that receives OTLP and shows logs, traces and metrics on the template's dashboard port (`docker-and-compose`); it keeps everything in memory, so it's empty after a restart. In production, run a collector beside the app or as a gateway and swap the dashboard exporter for your backend's.

## Steps

1. A new use case needs nothing: `LoggingBehaviour` gives it a span named after the request class, with its outcome as a tag.
2. Before writing any telemetry code, check what the instrumentation already records. Request durations per route, GraphQL operations, MCP tool calls and Lambda invocations are all covered, so we don't count or time them again.
3. To trace work inside Application, start a child span with `using var activity = ApplicationTelemetry.ActivitySource.StartActivity("Name");`, and use the [semantic convention](https://opentelemetry.io/docs/specs/semconv/) tag names where one exists.
4. A new dependency in Infrastructure (a queue, an HTTP API) gets its spans and metrics from its own instrumentation package, if a stable one exists. Subscribe to its source or meter name in the presentation layer's startup.
5. Use stable packages only. When the only instrumentation is a prerelease package, go without that signal and add it to the watch list below.
6. Test spans with an `ActivityListener` that keeps only the test's own trace (`unit-tests`). The integration tests send a `traceparent` header and check the request and use case spans join up.
7. To send telemetry somewhere new, add an exporter to `otel-collector.yaml` and list it in the pipelines. The app's settings don't change.
8. To see it locally, run `docker compose up -d --build` and open the dashboard on the port `docs/RUN.md` lists. For a `dotnet run`, start the collector with `docker compose up -d otel-collector` and set `OTEL_EXPORTER_OTLP_ENDPOINT` to its gRPC port, `http://$(docker compose port otel-collector 4317)`.

## Example

```csharp
// src/Application/Common/Behaviours/LoggingBehaviour.cs
using var activity = ApplicationTelemetry.ActivitySource.StartActivity(RequestName);
_ = activity?.SetTag(ApplicationTelemetry.RequestNameTag, RequestName);
...
catch (Exception exception)
{
    _ = activity?.SetTag(ApplicationTelemetry.RequestOutcomeTag, "error")
        .SetStatus(ActivityStatusCode.Error, exception.Message)
        .AddException(exception);

    throw;
}
```

```yaml
# docker-compose.yml
environment:
  OTEL_EXPORTER_OTLP_ENDPOINT: http://otel-collector:4317
  OTEL_EXPORTER_OTLP_PROTOCOL: grpc
```

```yaml
# otel-collector.yaml
exporters:
  otlp_grpc/aspire:
    endpoint: aspire-dashboard:18889
    tls:
      insecure: true
```

## Watch list

These signals and packages aren't stable for .NET yet. Check them when dependencies are updated, and adopt each one once it has a stable release:

- `OpenTelemetry.Instrumentation.EntityFrameworkCore`: adds a span per SQL command. Until it's stable there are no database spans, only EF Core's metrics.
- Profiles: there's no stable .NET SDK for the profiling signal.
- The OpenTelemetry Events API: until then, events are `[LoggerMessage]` logs.

## Don't

- Reference an OpenTelemetry, Aspire or vendor package from Application or Infrastructure. They publish with `System.Diagnostics`, and Presentation subscribes.
- Export anywhere but OTLP, or hard-code an endpoint. Settings come from the `OTEL_*` variables.
- Point the app straight at a backend, the dashboard included. It sends to a collector, and the collector decides where things go.
- Add a prerelease package, or hand-write instrumentation, to get a signal a package will give us later.
- Add a custom metric that repeats one the instrumentation already records.
- Put ids, tokens or personal data in span names, tags or metric tags.
- Mark a span as an error for a validation failure or a missing entity. The caller got an answer; the outcome tag and the log say what happened.
- Trace the health endpoints. Probes would bury everything else.
- Start a span with `new Activity(...)`. Use the layer's `ActivitySource`, so nothing is recorded when nobody is listening.

## Check

``` bash
dotnet test --filter "FullyQualifiedName~Telemetry|FullyQualifiedName~LoggingBehaviour"   # use case span and end-to-end trace tests
docker compose up -d --build                         # then open the dashboard on the port docs/RUN.md lists and make a request
```
