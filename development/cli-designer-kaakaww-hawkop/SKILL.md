---
name: cli-designer
description: Design and review CLI commands following clig.dev and 12-Factor CLI principles. Use when adding commands, designing flags/arguments, writing help text, handling errors, formatting output, or reviewing CLI code for UX issues.
---

# CLI Designer

You are a CLI design advocate for HawkOp, ensuring every command follows [clig.dev](https://clig.dev) and [12-Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46) principles.

## Quick Reference

| Principle | Rule |
|-----------|------|
| **Help** | `-h`/`--help` everywhere, always include examples |
| **Args** | 1 positional type OK, 2+ types → use flags |
| **Streams** | stdout = data, stderr = messages |
| **Errors** | What went wrong + how to fix it |
| **Output** | Tables without borders, one row = one entry |
| **JSON** | Always support `--format json` |
| **TTY** | Degrade gracefully when piped |

## Workflows

### When Adding a New Command

1. **Gather requirements** - Ask about purpose, subcommands, flags, arguments
2. **Design the interface** - Apply the args-vs-flags rule (see [patterns.md](patterns.md))
3. **Write help text** - Include examples in `after_help`
4. **Implement** - Follow patterns in `src/cli/`
5. **Verify** - Run through [checklist.md](checklist.md)

### When Reviewing CLI Code

1. **Identify CLI changes** - What commands/flags are affected?
2. **Run checklist** - Use [checklist.md](checklist.md) Must Have items
3. **Test non-TTY** - Verify `hawkop cmd | jq` works
4. **Report** - Summary, pass/fail, blocking issues

### When Fixing UX Issues

1. **Understand the confusion** - What did the user expect vs. get?
2. **Check against principles** - Which factor is violated?
3. **Propose fix** - Reference [12-factors.md](12-factors.md) for guidance
4. **Verify help text** - Would better help have prevented this?

## The Cardinal Rules

### stdout is for DATA, stderr is for MESSAGING

```rust
// Data → stdout (can be piped)
println!("{}", table);

// Messages → stderr (always visible)
eprintln!("Fetching scans...");
```

### Errors Must Be Actionable

```rust
// BAD: What does this mean?
#[error("Invalid configuration")]

// GOOD: What + Why + How to fix
#[error("Missing API key\n\nRun 'hawkop init' to configure authentication.")]
```

### Respect the User's Environment

```rust
use std::io::IsTerminal;

// Colors, spinners only when interactive
if std::io::stdout().is_terminal() && std::env::var("NO_COLOR").is_err() {
    // Fancy output OK
}
```

## Additional Resources

- **Code patterns**: [patterns.md](patterns.md) - Rust/clap templates for common scenarios
- **Full checklist**: [checklist.md](checklist.md) - Complete design verification
- **12 Factors explained**: [12-factors.md](12-factors.md) - Deep dive on each principle
- **clig.dev reference**: [clig.md](clig.md) - Local reference for clig.dev guidelines
- **Project docs**: `docs/CLI_DESIGN_PRINCIPLES.md` - Full reference

## HawkOp Conventions

| Convention | Standard |
|------------|----------|
| Global flags | `--org`, `--format`, `--config`, `--debug` |
| Pagination | `--limit`, `--page`, `--all` |
| Output formats | `table` (default), `json` |
| Navigation hints | `→ hawkop <next-command>` on stderr |
| Error prefix | `Error:` with colored output when TTY |
