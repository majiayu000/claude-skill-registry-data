---
name: rust-tracing
description: Rust tracing and structured logging with the tracing ecosystem. Use when adding logging, instrumenting functions, setting up observability, configuring log output, or debugging with traces.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Rust Tracing and Structured Logging

Comprehensive guide for observability with the `tracing` ecosystem.

## Setup

### Basic Setup

```toml
# Cargo.toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```

```rust
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

fn init_tracing() {
    tracing_subscriber::registry()
        .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| {
            // Default log level
            "info,nebula=debug,tower_http=debug".into()
        }))
        .with(tracing_subscriber::fmt::layer())
        .init();
}

fn main() {
    init_tracing();
    // ...
}
```

### Production Setup with JSON

```rust
use tracing_subscriber::{
    fmt::{self, format::FmtSpan},
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter,
};

fn init_production_tracing() {
    let env_filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| "info".into());

    let fmt_layer = fmt::layer()
        .json()                           // JSON output for log aggregation
        .with_current_span(true)          // Include current span
        .with_span_list(true)             // Include span hierarchy
        .with_file(true)                  // Include file name
        .with_line_number(true)           // Include line number
        .with_thread_ids(true)            // Include thread ID
        .with_target(true);               // Include target module

    tracing_subscriber::registry()
        .with(env_filter)
        .with(fmt_layer)
        .init();
}
```

### Development Setup with Pretty Output

```rust
fn init_dev_tracing() {
    tracing_subscriber::registry()
        .with(EnvFilter::try_from_default_env().unwrap_or_else(|_| "debug".into()))
        .with(
            tracing_subscriber::fmt::layer()
                .pretty()                  // Human-readable output
                .with_file(true)
                .with_line_number(true)
                .with_thread_names(true)
        )
        .init();
}
```

## Log Levels

### Choosing the Right Level

```rust
use tracing::{trace, debug, info, warn, error};

fn process_request(req: &Request) -> Result<Response, Error> {
    // TRACE: Very detailed debugging, high volume
    trace!(headers = ?req.headers(), "Raw request headers");
    
    // DEBUG: Diagnostic information for debugging
    debug!(method = %req.method(), path = %req.path(), "Processing request");
    
    // INFO: Notable events in normal operation
    info!(user_id = %user.id, "User authenticated successfully");
    
    // WARN: Unexpected but recoverable situations
    warn!(retry_count = 3, "Request failed, retrying");
    
    // ERROR: Failures that need attention
    error!(error = ?err, "Failed to process request");
    
    Ok(response)
}
```

### Level Guidelines

| Level | When to Use | Examples |
|-------|-------------|----------|
| `error` | Failures requiring immediate attention | DB connection lost, unhandled errors |
| `warn` | Unexpected but handled situations | Retry succeeded, deprecated API used |
| `info` | Notable business events | User login, request completed, job started |
| `debug` | Diagnostic information | Request details, internal state |
| `trace` | Very detailed debugging | Loop iterations, raw data |

## Structured Fields

### Field Types

```rust
use tracing::info;

fn log_examples() {
    let user_id = 42;
    let username = "alice";
    let request = Request::new();
    
    // Display formatting (uses Display trait)
    info!(%user_id, "User action");  // user_id=42
    
    // Debug formatting (uses Debug trait)
    info!(?request, "Request received");  // request=Request { ... }
    
    // Named fields
    info!(user.id = user_id, user.name = username, "User logged in");
    
    // Literal values
    info!(version = 1, "API version");
    
    // Empty message with just fields
    info!(user_id, action = "login");
}
```

### Consistent Field Naming

```rust
// Use consistent, hierarchical field names across the codebase

// Request context
info!(
    request.id = %request_id,
    request.method = %method,
    request.path = %path,
    "Handling request"
);

// User context
info!(
    user.id = %user_id,
    user.role = %role,
    "User action"
);

// Database operations
debug!(
    db.query = query,
    db.duration_ms = duration.as_millis(),
    db.rows_affected = rows,
    "Query executed"
);

// External service calls
info!(
    service.name = "payment-api",
    service.operation = "charge",
    service.duration_ms = duration.as_millis(),
    "External call completed"
);

// Error context
error!(
    error.kind = %err.kind(),
    error.message = %err,
    error.source = ?err.source(),
    "Operation failed"
);
```

## Spans

### Function Instrumentation

```rust
use tracing::{instrument, info, debug, Span};

// Basic instrumentation
#[instrument]
fn process_item(item_id: u64) -> Result<(), Error> {
    info!("Processing started");
    // All logs here are within the span
    do_work()?;
    info!("Processing completed");
    Ok(())
}

// Skip sensitive fields
#[instrument(skip(password, api_key))]
fn authenticate(username: &str, password: &str, api_key: &str) -> Result<User, AuthError> {
    info!("Authentication attempt");
    // password and api_key won't be logged
    Ok(user)
}

// Custom span name and level
#[instrument(name = "handle_request", level = "info")]
async fn handle(req: Request) -> Response {
    // ...
}

// Add custom fields
#[instrument(fields(request_id = %generate_id()))]
async fn process_request(req: Request) -> Response {
    // ...
}

// Skip all parameters, add specific ones
#[instrument(skip_all, fields(user_id = %user.id, action = "update"))]
fn update_user(user: &User, data: UpdateData) -> Result<(), Error> {
    // ...
}
```

### Manual Spans

```rust
use tracing::{span, Level, info, Instrument};

async fn complex_operation() {
    // Create a span
    let span = span!(Level::INFO, "complex_operation", phase = "init");
    let _guard = span.enter();
    
    info!("Starting phase 1");
    
    // Nested span
    {
        let inner_span = span!(Level::DEBUG, "phase_1");
        let _inner_guard = inner_span.enter();
        do_phase_1().await;
    }
    
    // Update span fields
    Span::current().record("phase", "complete");
    info!("All phases complete");
}

// For async code, use .instrument()
async fn async_operation() {
    let span = span!(Level::INFO, "async_op");
    
    async move {
        info!("Inside async operation");
        do_async_work().await;
    }
    .instrument(span)
    .await;
}
```

### Span Events

```rust
use tracing::{span, Level, event};

fn with_span_events() {
    let span = span!(Level::INFO, "operation");
    let _guard = span.enter();
    
    // Event within span
    event!(Level::INFO, "Operation started");
    
    // Event with fields
    event!(Level::DEBUG, items = 42, "Processing items");
    
    // Parent span is automatically included
}
```

## Async Tracing

### Instrument Async Functions

```rust
use tracing::{instrument, info, Instrument};
use std::future::Future;

#[instrument]
async fn fetch_data(url: &str) -> Result<Data, Error> {
    info!("Fetching data");
    let response = client.get(url).await?;
    info!(status = %response.status(), "Response received");
    Ok(response.json().await?)
}

// For closures
async fn process_items(items: Vec<Item>) {
    let futures = items.into_iter().map(|item| {
        let span = tracing::info_span!("process_item", item_id = %item.id);
        async move {
            process(item).await
        }
        .instrument(span)
    });
    
    futures::future::join_all(futures).await;
}
```

### Tokio Console Integration

```toml
# Cargo.toml
[dependencies]
console-subscriber = "0.4"
tokio = { version = "1", features = ["full", "tracing"] }
```

```rust
fn init_with_console() {
    console_subscriber::init();  // For tokio-console debugging
}
```

## Request Tracing

### HTTP Request Spans

```rust
use axum::{
    extract::Request,
    middleware::Next,
    response::Response,
};
use tracing::{info_span, Instrument};
use uuid::Uuid;

pub async fn trace_request(request: Request, next: Next) -> Response {
    let request_id = Uuid::new_v4();
    let method = request.method().clone();
    let uri = request.uri().clone();
    
    let span = info_span!(
        "http_request",
        request.id = %request_id,
        request.method = %method,
        request.path = %uri.path(),
        request.query = ?uri.query(),
        response.status = tracing::field::Empty,
        response.duration_ms = tracing::field::Empty,
    );
    
    async move {
        let start = std::time::Instant::now();
        let response = next.run(request).await;
        let duration = start.elapsed();
        
        // Record response fields
        tracing::Span::current()
            .record("response.status", response.status().as_u16())
            .record("response.duration_ms", duration.as_millis() as u64);
        
        tracing::info!("Request completed");
        
        response
    }
    .instrument(span)
    .await
}
```

### Tower HTTP Tracing

```rust
use axum::Router;
use tower_http::trace::{self, TraceLayer};
use tracing::Level;

fn create_router() -> Router {
    Router::new()
        .route("/", get(handler))
        .layer(
            TraceLayer::new_for_http()
                .make_span_with(trace::DefaultMakeSpan::new().level(Level::INFO))
                .on_request(trace::DefaultOnRequest::new().level(Level::INFO))
                .on_response(trace::DefaultOnResponse::new().level(Level::INFO))
                .on_failure(trace::DefaultOnFailure::new().level(Level::ERROR))
        )
}
```

## Error Tracing

### Logging Errors

```rust
use tracing::{error, warn, instrument};

#[instrument(err)]  // Automatically logs errors at ERROR level
fn fallible_operation() -> Result<(), Error> {
    do_something()?;
    Ok(())
}

#[instrument(err(level = "warn"))]  // Log errors at WARN level
fn recoverable_operation() -> Result<(), Error> {
    // ...
}

// Manual error logging with context
fn process() -> Result<Output, Error> {
    match do_work() {
        Ok(result) => Ok(result),
        Err(e) => {
            error!(
                error = %e,
                error.kind = ?e.kind(),
                "Operation failed"
            );
            Err(e)
        }
    }
}

// Chain of errors
fn with_error_chain() {
    if let Err(e) = operation() {
        error!(error = ?e, "Top-level error");
        
        let mut source = e.source();
        while let Some(cause) = source {
            error!(cause = %cause, "Caused by");
            source = cause.source();
        }
    }
}
```

## Filtering and Output

### Environment Filter Syntax

```bash
# Set via environment variable
RUST_LOG=info                           # All modules at INFO
RUST_LOG=debug,hyper=info               # Default DEBUG, hyper at INFO
RUST_LOG=nebula=debug,tower_http=debug  # Specific modules
RUST_LOG=nebula::api=trace              # Specific path
RUST_LOG="info,nebula[user_id]=debug"   # Filter by span field
```

### Programmatic Filtering

```rust
use tracing_subscriber::{filter, layer::SubscriberExt, util::SubscriberInitExt};

fn init_filtered() {
    let filter = filter::Targets::new()
        .with_default(tracing::Level::INFO)
        .with_target("nebula", tracing::Level::DEBUG)
        .with_target("hyper", tracing::Level::WARN)
        .with_target("tower_http", tracing::Level::DEBUG);
    
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(filter)
        .init();
}
```

### Multiple Outputs

```rust
use tracing_subscriber::{
    fmt::{self, writer::MakeWriterExt},
    layer::SubscriberExt,
    util::SubscriberInitExt,
};
use std::io;

fn init_multi_output() {
    // Stderr for errors, stdout for everything else
    let stderr = io::stderr.with_max_level(tracing::Level::WARN);
    let stdout = io::stdout.with_max_level(tracing::Level::INFO);
    
    tracing_subscriber::registry()
        .with(fmt::layer().with_writer(stderr))
        .with(fmt::layer().with_writer(stdout))
        .init();
}
```

## OpenTelemetry Integration

### Setup with Jaeger

```toml
[dependencies]
opentelemetry = "0.27"
opentelemetry_sdk = { version = "0.27", features = ["rt-tokio"] }
opentelemetry-otlp = "0.27"
tracing-opentelemetry = "0.28"
```

```rust
use opentelemetry::trace::TracerProvider;
use opentelemetry_sdk::trace::SdkTracerProvider;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

fn init_otel() -> Result<SdkTracerProvider, Box<dyn std::error::Error>> {
    let exporter = opentelemetry_otlp::SpanExporter::builder()
        .with_tonic()
        .build()?;
    
    let provider = SdkTracerProvider::builder()
        .with_batch_exporter(exporter)
        .build();
    
    let tracer = provider.tracer("nebula");
    let telemetry = tracing_opentelemetry::layer().with_tracer(tracer);
    
    tracing_subscriber::registry()
        .with(telemetry)
        .with(tracing_subscriber::fmt::layer())
        .init();
    
    Ok(provider)
}

// Shutdown properly
async fn shutdown(provider: SdkTracerProvider) {
    provider.shutdown().expect("Failed to shutdown tracer");
}
```

## Testing

### Capturing Logs in Tests

```rust
#[cfg(test)]
mod tests {
    use tracing_test::traced_test;
    
    #[traced_test]
    #[test]
    fn test_with_logs() {
        tracing::info!("This will be captured");
        assert!(logs_contain("captured"));
    }
    
    #[traced_test]
    #[tokio::test]
    async fn test_async_with_logs() {
        tracing::debug!("Async test log");
        assert!(logs_contain("Async test"));
    }
}
```

### Test Subscriber

```rust
use tracing_subscriber::fmt::MakeWriter;
use std::sync::{Arc, Mutex};

struct TestWriter {
    logs: Arc<Mutex<Vec<String>>>,
}

impl std::io::Write for TestWriter {
    fn write(&mut self, buf: &[u8]) -> std::io::Result<usize> {
        let log = String::from_utf8_lossy(buf).to_string();
        self.logs.lock().unwrap().push(log);
        Ok(buf.len())
    }
    
    fn flush(&mut self) -> std::io::Result<()> {
        Ok(())
    }
}

#[test]
fn test_logging() {
    let logs = Arc::new(Mutex::new(Vec::new()));
    let writer = TestWriter { logs: logs.clone() };
    
    let subscriber = tracing_subscriber::fmt()
        .with_writer(move || writer.clone())
        .finish();
    
    tracing::subscriber::with_default(subscriber, || {
        tracing::info!("Test message");
    });
    
    let captured = logs.lock().unwrap();
    assert!(captured.iter().any(|l| l.contains("Test message")));
}
```

## Nebula Conventions

### Standard Span Names

```rust
// HTTP requests
#[instrument(name = "http.request")]

// Database operations
#[instrument(name = "db.query")]
#[instrument(name = "db.transaction")]

// Background jobs
#[instrument(name = "job.execute")]

// Workflow operations
#[instrument(name = "workflow.run")]
#[instrument(name = "workflow.step")]

// External services
#[instrument(name = "external.call")]
```

### Standard Field Names

```rust
// Request context
request.id
request.method
request.path

// Response context
response.status
response.duration_ms

// User context
user.id
user.role

// Workflow context
workflow.id
workflow.name
workflow.step

// Database context
db.query
db.table
db.duration_ms
db.rows_affected

// Error context
error.kind
error.message
error.code
```

### Log Message Style

```rust
// Use lowercase, present tense, no trailing punctuation
info!("processing request");           // Good
info!("Processing Request.");          // Bad

// Include context in fields, not message
info!(user_id = %id, "user logged in");  // Good
info!("User {} logged in", id);           // Less structured

// Be specific
info!("workflow step completed");         // Good
info!("done");                            // Too vague
```
