---
name: serilog
description: How logging works with Serilog - registration with AddSerilog, configuration from appsettings, sinks per environment, logs over OTLP, the enrichers and properties on every event, the request log, the LoggingBehaviour, who logs an unexpected exception, levels, and source-generated log messages. Use when adding a log line, changing log configuration or levels, adding a property, or looking for where logs go.
metadata:
  scope: shared
---

# Serilog

## The rule

Serilog is the logger. Application and Infrastructure code log through `Microsoft.Extensions.Logging.ILogger<T>`, and Serilog does the writing. The presentation layer's startup registers it with `builder.Services.AddSerilog(...)`, which reads the `Serilog` section of the appsettings files and also sets the static `Log.Logger` that `Program.cs` uses for the start and fatal messages.

| Environment | Sink | Where to look |
| --- | --- | --- |
| `local` | Console, with the output template in `appsettings.local.json` | The terminal |
| `docker` | Console, and OTLP through the collector to the Aspire dashboard | The Aspire dashboard, on the port `docs/RUN.md` lists, or `docker compose logs` |
| Lambda, anywhere | Console, as compact JSON, and OTLP when the endpoint is set | CloudWatch Logs, or `docker compose logs` for the emulator, and the Aspire dashboard in Docker Compose |
| Any, when `OTEL_EXPORTER_OTLP_ENDPOINT` is set | Also OTLP, through `Serilog.Sinks.OpenTelemetry` | Whatever receives the OTLP (`telemetry`) |

The OTLP sink is added in code, not in the appsettings files, because it follows the standard `OTEL_*` settings like the trace and metric exporters do. It sends the same `service.name`, `service.version` and `deployment.environment.name` as the traces, and each event carries the trace and span IDs of whatever was running when it was written, so a log line links to its trace.

Every event carries these properties:

| Property | Comes from |
| --- | --- |
| `ApplicationName` | `Serilog:Properties` in the environment's appsettings |
| `EnvironmentName`, `MachineName` | `Serilog.Enrichers.Environment`, listed under `Serilog:Enrich` |
| `AssemblyVersion`, `AssemblyInformationalVersion` | Added in code at startup |
| Anything pushed with `LogContext` | `FromLogContext` |

Levels are set in configuration, never in code: `Information` by default and `Debug` in `local`, with `Information` for `Microsoft`, `Warning` for `Microsoft.AspNetCore` and `Microsoft.EntityFrameworkCore.Database.Command` (a line per SQL statement buries everything else, and EF Core's meter already counts them), and `Error` for `System`. The built-in `Logging` section is set to `None` so nothing is written twice.

Three things log a request, and each says something the others don't:

| What | Where | Logs |
| --- | --- | --- |
| The request log | `UseSerilogRequestLogging()`, in web templates only | One line per request with its method, path, status code and time. It's registered before the exception handler, so it logs the status code the client actually got |
| `LoggingBehaviour` | `src/Application/Common/Behaviours/`, around every use case | `Information` when a request is handled, fails validation or finds nothing, with the request name and its time in milliseconds |
| The presentation error handler | The exception handler or error filter | `Error`, with the exception, for anything it reports as unexpected |

An unexpected exception is logged once, by the class that turns it into a response, because handling it stops the framework logging it. `LoggingBehaviour` leaves it alone. In Lambda the exception goes back to the caller as a function error and the runtime writes it to CloudWatch Logs, so nothing logs it a second time.

The Lambda template has no appsettings files. Its startup sets the same levels and properties in code, and environment variables such as `Serilog__MinimumLevel__Default` override them.

## Steps

1. Take `ILogger<T>` through the constructor where you need it. Never reference Serilog types outside the presentation layer.
2. Write each message as a `[LoggerMessage]` method on a `partial` class, with named holes in the template. The source generator writes the code, so nothing is formatted when the level is off. Put the methods in a `#region Log Messages` at the bottom of the class.
3. Pick the level for the reader at 3am: `Information` for something that happened, `Warning` for something odd that was handled, `Error` for a failed request, `Debug` for detail you'd only want while developing.
4. Name new properties in PascalCase with no spaces, so they can be used in templates and queried in any backend without quoting.
5. Add a sink or change a level in the appsettings files. A new sink package goes in `Directory.Packages.props` (`packages-and-dependencies`).
6. In the Aspire dashboard's structured logs, filter on any property, or open a log's trace from its trace ID.

## Example

```csharp
// src/Application/Common/Behaviours/LoggingBehaviour.cs
[LoggerMessage(Level = LogLevel.Information, Message = "{RequestName} handled in {ElapsedMilliseconds:0.0} ms")]
private static partial void LogHandled(ILogger logger, string requestName, double elapsedMilliseconds);
```

```csharp
// src/Presentation/Extensions, where startup registers services
_ = builder.Services.AddSerilog((services, loggerConfiguration) =>
{
    var configuration = services.GetRequiredService<IConfiguration>();

    _ = loggerConfiguration.ReadFrom.Configuration(configuration)
        .Enrich.WithProperty(
            "AssemblyVersion",
            assembly.GetCustomAttribute<AssemblyFileVersionAttribute>()?.Version);

    if (telemetry.Enabled)
    {
        _ = loggerConfiguration.WriteTo.OpenTelemetry(
            options =>
            {
                options.ResourceAttributes = telemetry.ResourceAttributes;
                options.OnBeginSuppressInstrumentation = SuppressInstrumentationScope.Begin;
            },
            key => configuration[key]);
    }
});
```

```json
// src/Presentation/appsettings.docker.json
"Serilog": {
  "WriteTo": [ { "Name": "Console", "Args": { "outputTemplate": "..." } } ],
  "Properties": { "ApplicationName": "CleanMinimalApi-Docker" }
}
```

## Don't

- Use string interpolation in a log message (`$"Created {id}"`). It loses the property and allocates on every call.
- Call `logger.LogInformation(...)` and its friends directly. Write a `[LoggerMessage]` method instead.
- Log an exception that something else will log, such as one you rethrow.
- Log tokens, connection strings, passwords or personal data.
- Use `Console.WriteLine`.
- Reference Serilog from Application or Infrastructure.
- Register Serilog with `builder.Host.UseSerilog`. `AddSerilog` is the current registration.
- Add a second request logger, such as `UseHttpLogging`. Requests are logged once, by Serilog.
- Move the request log after the exception handler. It would log every handled error as a `500`.

## Check

``` bash
dotnet run --project ./src/Presentation   # watch the console, then make a request
docker compose up -d --build              # then open the Aspire dashboard on the port docs/RUN.md lists
dotnet test tests/Application.Tests.Unit  # LoggingBehaviourTests check the messages with FakeLogger
```
