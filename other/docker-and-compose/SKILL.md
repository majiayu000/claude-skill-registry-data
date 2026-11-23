---
name: docker-and-compose
description: How the Dockerfile builds, tests and publishes the solution, how the runtime image runs (non-root, /app/data volume, HEALTHCHECK), and what docker-compose starts. Use when changing the Dockerfile, the compose file or how the app runs in a container.
metadata:
  scope: shared
---

# Docker and Compose

## The rule

One multi-stage `Dockerfile` does everything the pipeline needs:

| Stage | Does |
| --- | --- |
| `build` | Restores (the `.slnx`, the root build files and every project file copied first for layer caching), then builds in Release with the version passed in |
| `test` | Runs every test project with coverage and saves the results and exit code |
| `results` | Exports the test results so the pipeline can report them |
| `publish` | Publishes the Presentation project |
| `run` | The runtime image: non-root `$APP_UID`, `WORKDIR /app`, data in `/app/data`, a `HEALTHCHECK` on `/health/live` |

`docker-compose.yml` runs the app with `DOTNET_ENVIRONMENT=docker`, the `movie-reviews-data` volume a pinned OpenTelemetry Collector that receives the app's OTLP logs, traces and metrics, configured by `otel-collector.yaml`, and a pinned Aspire dashboard the collector forwards them to (`telemetry`). The dashboard UI and the collector's OTLP ports are published on the template's own ports (below), so a `dotnet run` can send to the collector too. The dashboard runs with `ASPIRE_DASHBOARD_UNSECURED_ALLOW_ANONYMOUS` and the collector's OTLP ports take anything sent to them, on purpose: the compose file is for a developer's machine, with nothing to sign in to. Keep it that way rather than adding sign-in, and don't offer the compose file for a shared or deployed environment. Images are built by CI but not pushed anywhere; the template ships the Dockerfile so users can.

The Lambda template's `run` stage is the AWS Lambda .NET base image instead. It runs as user `65534` from `/var/task`, keeps its database in `/tmp`, and has no `HEALTHCHECK`. Its compose file runs the collector and the Aspire dashboard as well. Compose maps the runtime interface emulator to 7350, so the function can be invoked with a `POST` to `/2015-03-31/functions/function/invocations`.

### Ports

Every port published on the developer's machine, by the compose file or by `launchSettings.json`, sits in the template's own block of ten, so any two Lean Mean Clean solutions run side by side. The blocks follow the template order: Minimal API 7310, MCP 7320, GraphQL 7330, Web API 7340, Lambda Function 7350. Each port has the same place in every block:

| Offset | Port |
| --- | --- |
| +0 | The app over HTTP, from Docker Compose or `dotnet run` |
| +1 | The app over HTTPS, `dotnet run` only |
| +2 | The Aspire dashboard |
| +3 | The collector's OTLP over gRPC |
| +4 | The collector's OTLP over HTTP |
| +5 | The MCP Inspector |
| +6 | The MCP chat demo |
| +7 to +9 | Spare |

`docs/RUN.md` lists the ports this solution uses. The app listens on its own port everywhere: under `dotnet run`, in the image (the `Dockerfile` sets `ASPNETCORE_HTTP_PORTS`, `EXPOSE` and the `HEALTHCHECK` to it) and in the compose file, so `docker run -p` maps it to the same number. Change all four together. The Lambda template is the one exception: Lambda's runtime interface emulator always listens on 8080 inside its container, so only the host side of its mapping is ours. The dashboard, the collector and other third-party images keep their usual ports inside (18888, 4317 and 4318), and only the host side of their mappings moves. A new service takes a spare port from the block, never a product's well-known one such as 3000, 5432 or 9000. `docker compose port <service> <container port>` prints where a port ended up.

## Steps

1. Keep restore before `COPY . .` so a code change doesn't redo the restore layer. A new project folder needs nothing extra; the loops pick up every `src/*/*.csproj` and `tests/*/*.csproj`.
2. Anything the app writes goes under `/app/data`, the only folder the app user can write to.
3. Pin every image in compose to a version, and bump them with the monthly package update (`packages-and-dependencies`).
4. Change base images through the `ARG`s at the top, not inside a `FROM`.
5. Test locally with `docker compose up -d --build`, then hit `/health/ready` and the API reference.

## Don't

- Run the runtime image as root, or write outside `/app/data`.
- Use `:latest` for any image.
- Add a push step to a registry.
- Copy secrets or `appsettings.*.json` overrides with real values into the image.

## Check

``` bash
docker build . --target run --tag local-check
docker compose up -d --build --wait   # waits for the image's HEALTHCHECK
# Lambda: curl -fsS -X POST "http://$(docker compose port function 8080)/2015-03-31/functions/function/invocations" -d '{}'
docker compose down
```
