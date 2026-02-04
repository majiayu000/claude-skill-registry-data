---
name: rust-ms-applications
description: Microsoft Pragmatic Rust Application Guidelines. Use when building CLI tools, binaries, services, or user-facing applications.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Microsoft Pragmatic Rust - Application Guidelines

Guidelines for building robust user-facing applications and services.

## Error Handling with anyhow

### Use anyhow for Applications
```rust
use anyhow::{anyhow, bail, Context, Result};

fn main() -> Result<()> {
    let config = load_config()
        .context("failed to load configuration")?;
    
    run_application(config)
        .context("application failed")?;
    
    Ok(())
}

fn load_config() -> Result<Config> {
    let path = std::env::var("CONFIG_PATH")
        .context("CONFIG_PATH not set")?;
    
    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read {}", path))?;
    
    let config: Config = toml::from_str(&content)
        .context("invalid config format")?;
    
    if config.workers == 0 {
        bail!("workers must be greater than 0");
    }
    
    Ok(config)
}
```

### Error Context Chain
```rust
fn process_file(path: &Path) -> Result<Output> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("reading {}", path.display()))?;
    
    let parsed = parse(&content)
        .with_context(|| format!("parsing {}", path.display()))?;
    
    let result = transform(parsed)
        .context("transformation failed")?;
    
    Ok(result)
}

// Error output:
// Error: transformation failed
// 
// Caused by:
//     0: parsing /path/to/file.txt
//     1: invalid syntax at line 42
```

## CLI Development

### Use clap for Arguments
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "nebula")]
#[command(about = "Workflow automation toolkit")]
#[command(version, author)]
struct Cli {
    /// Enable verbose output
    #[arg(short, long, global = true)]
    verbose: bool,
    
    /// Configuration file path
    #[arg(short, long, default_value = "config.toml")]
    config: PathBuf,
    
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Run a workflow
    Run {
        /// Workflow name or ID
        workflow: String,
        
        /// Input parameters (key=value)
        #[arg(short, long)]
        param: Vec<String>,
    },
    
    /// List available workflows
    List {
        /// Output format
        #[arg(short, long, default_value = "table")]
        format: OutputFormat,
    },
}
```

### Exit Codes
```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("Error: {e:?}");
            ExitCode::from(1)
        }
    }
}

// Or with custom codes
#[repr(u8)]
enum Exit {
    Success = 0,
    ConfigError = 1,
    RuntimeError = 2,
    UserAbort = 130,
}

impl From<Exit> for ExitCode {
    fn from(e: Exit) -> Self {
        ExitCode::from(e as u8)
    }
}
```

## Logging and Tracing

### Use tracing for Observability
```rust
use tracing::{info, warn, error, debug, instrument, Level};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

fn init_logging() {
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer()
            .with_target(false)
            .with_thread_ids(true))
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .init();
}

#[instrument(skip(config), fields(workflow_id = %id))]
async fn execute_workflow(id: WorkflowId, config: &Config) -> Result<()> {
    info!("starting workflow execution");
    
    let result = do_work().await;
    
    match &result {
        Ok(_) => info!("workflow completed successfully"),
        Err(e) => error!(error = ?e, "workflow failed"),
    }
    
    result
}
```

### Structured Logging
```rust
use tracing::{info, Span};

fn process_request(req: &Request) {
    let span = tracing::info_span!(
        "request",
        method = %req.method,
        path = %req.path,
        request_id = %req.id,
    );
    
    let _guard = span.enter();
    
    info!(
        user_id = %req.user_id,
        "processing request"
    );
}
```

## Configuration

### Layered Configuration
```rust
use config::{Config, ConfigError, Environment, File};

#[derive(Debug, Deserialize)]
pub struct AppConfig {
    pub server: ServerConfig,
    pub database: DatabaseConfig,
    pub logging: LoggingConfig,
}

impl AppConfig {
    pub fn load() -> Result<Self, ConfigError> {
        Config::builder()
            // Start with defaults
            .set_default("server.port", 8080)?
            .set_default("server.host", "0.0.0.0")?
            
            // Load from file
            .add_source(File::with_name("config/default"))
            .add_source(File::with_name("config/local").required(false))
            
            // Override with environment variables
            // NEBULA_SERVER_PORT, NEBULA_DATABASE_URL, etc.
            .add_source(
                Environment::with_prefix("NEBULA")
                    .separator("_")
            )
            
            .build()?
            .try_deserialize()
    }
}
```

### Validate Configuration Early
```rust
impl AppConfig {
    pub fn validate(&self) -> Result<()> {
        if self.server.port == 0 {
            bail!("server.port cannot be 0");
        }
        
        if self.database.pool_size < 1 {
            bail!("database.pool_size must be at least 1");
        }
        
        if self.database.url.is_empty() {
            bail!("database.url is required");
        }
        
        Ok(())
    }
}

fn main() -> Result<()> {
    let config = AppConfig::load()
        .context("failed to load configuration")?;
    
    config.validate()
        .context("invalid configuration")?;
    
    // Now we know config is valid
    run(config)
}
```

## Initialization

### Ordered Initialization
```rust
async fn initialize(config: &Config) -> Result<AppState> {
    // 1. Initialize logging first
    init_logging(&config.logging)?;
    info!("logging initialized");
    
    // 2. Connect to database
    let db = Database::connect(&config.database)
        .await
        .context("database connection failed")?;
    info!("database connected");
    
    // 3. Initialize cache
    let cache = Cache::new(&config.cache)
        .context("cache initialization failed")?;
    info!("cache initialized");
    
    // 4. Start background services
    let scheduler = Scheduler::start(db.clone())
        .context("scheduler start failed")?;
    info!("scheduler started");
    
    Ok(AppState { db, cache, scheduler })
}
```

### Graceful Shutdown
```rust
use tokio::signal;
use tokio::sync::broadcast;

async fn run(config: Config) -> Result<()> {
    let (shutdown_tx, _) = broadcast::channel::<()>(1);
    let state = initialize(&config).await?;
    
    // Start server
    let server = start_server(state.clone(), shutdown_tx.subscribe());
    
    // Wait for shutdown signal
    tokio::select! {
        result = server => {
            result.context("server error")?;
        }
        _ = signal::ctrl_c() => {
            info!("shutdown signal received");
        }
    }
    
    // Graceful shutdown
    info!("initiating graceful shutdown");
    let _ = shutdown_tx.send(());
    
    // Wait for cleanup with timeout
    tokio::time::timeout(
        Duration::from_secs(30),
        state.shutdown()
    )
    .await
    .context("shutdown timeout")?
    .context("shutdown error")?;
    
    info!("shutdown complete");
    Ok(())
}
```

## Performance

### Custom Allocator
```rust
// For improved performance in multi-threaded apps
#[global_allocator]
static ALLOC: mimalloc::MiMalloc = mimalloc::MiMalloc;

// Or jemalloc
#[global_allocator]
static ALLOC: tikv_jemallocator::Jemalloc = tikv_jemallocator::Jemalloc;
```

### Release Profile
```toml
[profile.release]
lto = "thin"
codegen-units = 1
panic = "abort"
strip = true

[profile.release-with-debug]
inherits = "release"
debug = true
strip = false
```

## User Interaction

### Progress Reporting
```rust
use indicatif::{ProgressBar, ProgressStyle};

fn process_files(files: &[PathBuf]) -> Result<()> {
    let pb = ProgressBar::new(files.len() as u64);
    pb.set_style(ProgressStyle::default_bar()
        .template("{spinner:.green} [{bar:40.cyan/blue}] {pos}/{len} {msg}")?
        .progress_chars("#>-"));
    
    for file in files {
        pb.set_message(file.display().to_string());
        process_file(file)?;
        pb.inc(1);
    }
    
    pb.finish_with_message("done");
    Ok(())
}
```

### Colored Output
```rust
use owo_colors::OwoColorize;

fn print_status(status: &Status) {
    match status {
        Status::Success => println!("{}", "✓ Success".green()),
        Status::Warning(msg) => println!("{} {}", "⚠".yellow(), msg),
        Status::Error(msg) => eprintln!("{} {}", "✗".red(), msg),
    }
}
```

## Testing Applications

### Integration Tests
```rust
// tests/cli_tests.rs
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_help() {
    Command::cargo_bin("nebula")
        .unwrap()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("Workflow automation"));
}

#[test]
fn test_missing_config() {
    Command::cargo_bin("nebula")
        .unwrap()
        .arg("--config")
        .arg("nonexistent.toml")
        .arg("run")
        .arg("test")
        .assert()
        .failure()
        .stderr(predicate::str::contains("failed to load"));
}
```
