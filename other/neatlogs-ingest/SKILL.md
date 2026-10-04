---
name: neatlogs-ingest
description: Use when sending traces to Neatlogs from a language without a supported Neatlogs SDK, or when configuring direct HTTP ingest, OTLP/gRPC, an OpenTelemetry exporter, or an OpenTelemetry Collector. Defaults unsupported languages to POST /v1/trace nested JSON and documents the separate OTLP transports.
---

# Neatlogs direct ingest

Choose the transport before changing code:

1. For Python, TypeScript/Node.js, or Go, use the corresponding Neatlogs SDK skill unless the user explicitly requests a direct transport.
2. For any other language, default to the dependency-free HTTP ingest endpoint `POST https://ingest.neatlogs.com/v1/trace`. Read [`references/http-ingest.md`](references/http-ingest.md).
3. If the application already emits OpenTelemetry spans or uses an OpenTelemetry Collector, it may send OTLP over gRPC instead. Read [`references/grpc-ingest.md`](references/grpc-ingest.md).

Keep the endpoints distinct:

| Name | Endpoint | Payload |
|---|---|---|
| HTTP ingest | `POST /v1/trace` | One nested JSON trace; Neatlogs generates IDs |
| OTLP/HTTP | `POST /v1/traces` | OTLP protobuf from an OpenTelemetry exporter |
| OTLP/gRPC | `ingest.neatlogs.com:443` | OTLP `TraceService/Export` |
| OTLP/gRPC (EU projects) | `eu.ingest.neatlogs.com:443` | OTLP `TraceService/Export` |

Never send the nested HTTP-ingest JSON body to `/v1/traces`.

For EU projects, use `https://eu.ingest.neatlogs.com` as the SDK base URL, `POST https://eu.ingest.neatlogs.com/v1/trace` for direct JSON ingest, or `eu.ingest.neatlogs.com:443` for OTLP/gRPC.

For retrieval attributes set directly by the caller, emit `neatlogs.retriever.*`. OpenTelemetry-native sources may emit `gen_ai.retrieval.*`; Neatlogs maps those during ingestion. Do not emit the legacy `neatlogs.retrieval.*` namespace from new integrations.

## Completion gate

Before running a build, validation, restart, or representative workflow, show
the exact command and obtain explicit user approval. Run the project's existing
checks, restart the application or Collector that loads the changed transport,
and exercise the actual application behavior that emits telemetry. Direct HTTP
ingest must submit one complete nested `/v1/trace` payload per workflow;
OTLP must end its spans and drain the exporter according to the process
lifecycle.

Verify the exact resulting trace through the target project's normal product
trace view or supported public read path. Require a finalized trace with one
meaningful root, the expected semantic hierarchy, and no duplicate operations.
Do not infer end-to-end success from source inspection, local serialization,
exporter flush, or HTTP acceptance. Keep credentials in process environment or
client secret storage, never in command arguments, output, files, or agent
context. Do not use a legacy marker-discovery protocol. If the exact persisted
trace cannot be inspected, report the blocker and leave verification
incomplete.
