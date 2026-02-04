---
name: clap-patterns
description: Common Clap patterns and idioms for argument parsing, validation, and CLI design. Use when implementing CLI arguments with Clap v4+.
---

# Clap Patterns Skill

Common patterns and idioms for using Clap v4+ effectively in Rust CLI applications.

## Derive API vs Builder API

### When to Use Derive API

- CLI structure known at compile time
- Want type safety and compile-time validation
- Prefer declarative style
- Standard CLI patterns are sufficient

```rust
#[derive(Parser)]
#[command(version, about)]
struct Cli {
    #[arg(short, long)]
    input: PathBuf,
}
```

### When to Use Builder API

- CLI needs to be built dynamically at runtime
- Building plugin systems
- Arguments depend on configuration
- Need maximum flexibility

```rust
fn build_cli() -> Command {
    Command::new("app")
        .arg(Arg::new("input").short('i'))
}
```

## Common Patterns

### Global Options with Subcommands

```rust
#[derive(Parser)]
struct Cli {
    #[arg(short, long, global = true, action = ArgAction::Count)]
    verbose: u8,

    #[command(subcommand)]
    command: Commands,
}
```

### Argument Groups for Mutual Exclusivity

```rust
#[derive(Parser)]
#[command(group(
    ArgGroup::new("format")
        .required(true)
        .args(&["json", "yaml", "toml"])
))]
struct Cli {
    #[arg(long)]
    json: bool,
    #[arg(long)]
    yaml: bool,
    #[arg(long)]
    toml: bool,
}
```

### Custom Value Parsers

```rust
fn parse_port(s: &str) -> Result<u16, String> {
    let port: u16 = s.parse()
        .map_err(|_| format!("`{s}` isn't a valid port"))?;
    if (1024..=65535).contains(&port) {
        Ok(port)
    } else {
        Err(format!("port not in range 1024-65535"))
    }
}

#[derive(Parser)]
struct Cli {
    #[arg(long, value_parser = parse_port)]
    port: u16,
}
```

### Environment Variable Fallbacks

```rust
#[derive(Parser)]
struct Cli {
    #[arg(long, env = "API_TOKEN")]
    token: String,

    #[arg(long, env = "API_ENDPOINT", default_value = "https://api.example.com")]
    endpoint: String,
}
```

### Flattening Shared Options

```rust
#[derive(Args)]
struct CommonOpts {
    #[arg(short, long)]
    verbose: bool,

    #[arg(short, long)]
    config: Option<PathBuf>,
}

#[derive(Parser)]
struct Cli {
    #[command(flatten)]
    common: CommonOpts,

    #[command(subcommand)]
    command: Commands,
}
```

### Multiple Values

```rust
#[derive(Parser)]
struct Cli {
    /// Tags (can be specified multiple times)
    #[arg(short, long)]
    tag: Vec<String>,

    /// Files to process
    files: Vec<PathBuf>,
}
// Usage: myapp --tag rust --tag cli file1.txt file2.txt
```

### Subcommand with Shared Arguments

```rust
#[derive(Parser)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Build(BuildArgs),
    Test(TestArgs),
}

#[derive(Args)]
struct BuildArgs {
    #[command(flatten)]
    common: CommonOpts,

    #[arg(short, long)]
    release: bool,
}
```

### Argument Counting (Verbosity Levels)

```rust
#[derive(Parser)]
struct Cli {
    /// Verbosity (-v, -vv, -vvv)
    #[arg(short, long, action = ArgAction::Count)]
    verbose: u8,
}
// Usage: -v (1), -vv (2), -vvv (3)
```

### Help Template Customization

```rust
#[derive(Parser)]
#[command(
    after_help = "EXAMPLES:\n  \
        myapp --input file.txt\n  \
        myapp -i file.txt -vv\n\n\
        For more info: https://example.com"
)]
struct Cli {
    // ...
}
```

### Value Hints

```rust
#[derive(Parser)]
struct Cli {
    #[arg(short, long, value_name = "FILE", value_hint = ValueHint::FilePath)]
    input: PathBuf,

    #[arg(short, long, value_name = "DIR", value_hint = ValueHint::DirPath)]
    output: PathBuf,

    #[arg(short, long, value_name = "URL", value_hint = ValueHint::Url)]
    endpoint: String,
}
```

### Default Values with Functions

```rust
fn default_config_path() -> PathBuf {
    dirs::config_dir()
        .unwrap()
        .join("myapp")
        .join("config.toml")
}

#[derive(Parser)]
struct Cli {
    #[arg(long, default_value_os_t = default_config_path())]
    config: PathBuf,
}
```

## Best Practices

1. **Use `value_name`** for clearer help text
2. **Provide both short and long flags** where appropriate
3. **Add help text** to all arguments
4. **Use `ValueEnum`** for fixed set of choices
5. **Validate early** with custom parsers
6. **Support environment variables** for sensitive data
7. **Use argument groups** for mutually exclusive options
8. **Document with examples** in `after_help`
9. **Use semantic types** (PathBuf, not String for paths)
10. **Test CLI parsing** with integration tests

## References

- [Clap Documentation](https://docs.rs/clap/)
- [Clap Derive Reference](https://docs.rs/clap/latest/clap/_derive/index.html)
- [Clap Examples](https://github.com/clap-rs/clap/tree/master/examples)
