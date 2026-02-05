---
name: bun-cli
description: Build production-grade CLI tools with Bun. Reference implementation covering argument parsing patterns (--flag value, --flag=value, --flag), dual markdown/JSON output, error handling, subcommands, and testing. Use when building CLIs, designing argument parsing, implementing command structures, reviewing CLI quality, or learning Bun CLI best practices.
triggers:
  - bun cli
  - command line tool
  - argument parsing
  - cli development
  - cli architecture
---

# Bun CLI Development

Build powerful, production-grade CLI tools with Bun. Master argument parsing, output formatting, error handling, subcommands, and testing patterns proven in production across the SideQuest marketplace.

## Quick Navigation

- **[Quick Start](#quick-start)** — Get a working CLI in 5 minutes
- **[Core Patterns](#core-patterns)** — Argument parsing, output, usage, errors, subcommands
- **[Advanced Features](#advanced-features)** — Dry-run, auto-commit, git integration
- **[Testing Your CLI](#testing-your-cli)** — Unit and integration test patterns
- **[Reference](#reference)** — Comprehensive pattern guide + Para Obsidian example (9/10)

---

## Quick Start

**Goal:** Build a CLI tool that feels natural to use and is easy to maintain.

### Minimal CLI Template

```typescript
#!/usr/bin/env bun

import { color } from "@sidequest/core/formatters";

function printUsage(): void {
  console.log(color("cyan", "My CLI Tool v1.0"));
  console.log("Usage: my-cli <command> [options]");
  console.log("  config    Show configuration");
  console.log("  help      Show this help");
}

async function main(): Promise<void> {
  const [, , command] = process.argv;

  if (!command || command === "help") {
    printUsage();
    return;
  }

  try {
    switch (command) {
      case "config":
        console.log("Config: {...}");
        break;
      default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
  } catch (error) {
    console.error("Error:", error instanceof Error ? error.message : error);
    process.exit(1);
  }
}

main();
```

---

## Core Patterns

### 1. Argument Parsing

The marketplace standard uses **manual parsing** (not external libraries). This keeps CLIs simple, dependency-light, and predictable.

**Handle three flag formats:**
- `--flag value` — Spaced syntax
- `--flag=value` — Equals syntax
- `--flag` — Boolean flag

```typescript
function parseArgs(argv: string[]) {
  const positional: string[] = [];
  const flags: Record<string, string | boolean> = {};

  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (!arg) continue;

    if (arg.startsWith("--")) {
      const [keyRaw, value] = arg.split("=");
      const key = keyRaw?.slice(2);
      if (!key) continue;

      const next = argv[i + 1];
      if (value !== undefined) {
        flags[key] = value;
      } else if (next && !next.startsWith("--")) {
        flags[key] = next;
        i++;
      } else {
        flags[key] = true;
      }
    } else {
      positional.push(arg);
    }
  }

  const [command, subcommand, ...rest] = positional;
  return { command: command ?? "", subcommand, positional: rest, flags };
}
```

For detailed patterns and edge cases, see [bun-cli-patterns.md § Argument Parsing](bun-cli-patterns.md#argument-parsing).

---

### 2. Output Formatting

Always support **both markdown (human) and JSON (machine)** formats.

```typescript
import { OutputFormat, parseOutputFormat } from "@sidequest/core/formatters";

type Result = { title: string; items: string[] };

function formatMarkdown(result: Result): string {
  return `# ${result.title}\n\n${result.items.map(i => `- ${i}`).join("\n")}`;
}

function formatJson(result: Result): string {
  return JSON.stringify(result, null, 2);
}

function formatOutput(result: Result, format: OutputFormat): string {
  return format === "json" ? formatJson(result) : formatMarkdown(result);
}

// In main()
const format = parseOutputFormat(flags.format);
console.log(formatOutput(result, format));
```

**Benefits:** Humans read markdown (colored, readable), scripts parse JSON (structured, typeable).

For color palettes and advanced formatting, see [bun-cli-patterns.md § Output Formatting](bun-cli-patterns.md#output-formatting).

---

### 3. Usage Text

Make your CLI **self-documenting** with clear, scannable usage text.

```typescript
function printUsage(): void {
  const lines = [
    color("cyan", "My CLI Tool"),
    "",
    "Usage:",
    "  my-cli config [--format md|json]",
    "  my-cli list [path] [--format md|json]",
    "  my-cli create --template <type> [options]",
    "",
    "Options:",
    "  --format md|json     Output format (default: md)",
    "  --dry-run            Show changes without applying",
    "  --help               Show this help",
    "",
    "Examples:",
    "  my-cli config --format json",
    "  my-cli list . --format md",
    "  my-cli create --template project --dry-run",
  ];

  console.log(lines.map(line => color("cyan", line)).join("\n"));
}
```

**Key points:**
- Colored headers (cyan)
- Real, copy-paste examples
- All three flag formats shown
- Structure: Usage → Options → Examples

---

### 4. Error Handling

Be explicit and contextual with errors.

```typescript
try {
  const config = loadConfig();

  if (!config.vault) {
    console.error("Error: VAULT environment variable required");
    process.exit(1);
  }

  // Do work...

} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Error: ${message}`);
  process.exit(1);
}
```

**Conventions:**
- Exit code 0 = success
- Exit code 1 = error
- Prefix errors with "Error:"
- Include contextual information (missing env, invalid file, etc.)
- Avoid stack traces in user output

---

### 5. Subcommands

For CLIs with many operations, use two-level commands:

```typescript
case "frontmatter": {
  const subcommand = args[0];
  switch (subcommand) {
    case "get":
      // ...
    case "validate":
      // ...
    case "migrate":
      // ...
    default:
      console.error(`Unknown subcommand: frontmatter ${subcommand}`);
      process.exit(1);
  }
  break;
}
```

**Benefits:**
- Flat namespace `frontmatter get` vs. `frontmatter-get`
- Easy to add subcommands
- Clear semantic grouping

---

## Advanced Features

### Dry-Run Support

Every write operation should support `--dry-run`:

```typescript
const dryRun = flags["dry-run"] === true;
const result = await deleteFile(vault, file, { dryRun });

if (dryRun) {
  console.log("Would delete:", file);
} else {
  console.log("Deleted:", file);
}
```

### Auto-Commit Integration

For tools that modify files, consider git integration:

```typescript
if (flags["auto-commit"]) {
  const { isRepo, isClean } = await checkGitStatus(vault);
  if (!isRepo) throw new Error("Must be in a git repository");
  if (!isClean) throw new Error("Working tree must be clean");

  await autoCommitChanges(vault, changedFiles);
}
```

---

## Testing Your CLI

### Unit Testing with Bun

```typescript
import { describe, expect, test } from "bun:test";
import { parseArgs } from "./args";

describe("CLI argument parsing", () => {
  test("parses --key value format", () => {
    const result = parseArgs(["command", "--name", "test"]);
    expect(result.flags.name).toBe("test");
  });

  test("parses --key=value format", () => {
    const result = parseArgs(["command", "--name=test"]);
    expect(result.flags.name).toBe("test");
  });

  test("handles boolean flags", () => {
    const result = parseArgs(["command", "--verbose"]);
    expect(result.flags.verbose).toBe(true);
  });
});
```

### Integration Testing

```bash
# Test real CLI invocation
bun run src/cli.ts config --format json

# Verify output is valid JSON
bun run src/cli.ts config --format json | jq .

# Test error handling
bun run src/cli.ts unknown-command
echo $?  # Should be 1
```

---

## Reference

### 📚 Comprehensive Pattern Guide

See [**bun-cli-patterns.md**](bun-cli-patterns.md) for the complete, detailed reference:
- **File structure** — Project layout and organization
- **Entry point** — Shebang, imports, main flow
- **Argument utilities** — Parsing key=value, lists, type coercion
- **Output utilities** — Color palettes, formatting helpers
- **Exit codes** — Success (0), errors (1-3)
- **Configuration & environment** — Loading, validation
- **Testing** — Unit and integration test patterns
- **Bun-specific patterns** — Process I/O, file I/O, shell commands
- **Command dispatch** — Simple vs. complex CLI architectures
- **Examples** — Real implementations from marketplace
- **Checklist** — Implementation, testing, documentation verification
- **Anti-patterns** — Don't do these!
- **Migration guide** — Updating existing CLIs to standard

### 🔍 Example Implementation

See [**bun-cli-patterns.md § Para Obsidian CLI Review**](bun-cli-patterns.md#para-obsidian-cli---reference-implementation-910):
- **Score: 9/10** — Exemplary reference implementation
- Real implementation analyzed against standard
- All patterns demonstrated in production code
- Subcommands, dry-run, auto-commit, error handling

Use Para Obsidian CLI as a template for:
- Argument parsing pattern
- Usage output structure
- Output formatting (md/json)
- Error handling
- Subcommand dispatch

---

## Common Pitfalls

### ❌ Don't

- **Use external CLI libraries** (oclif, yargs, commander) — Keep it simple
- **Skip error handling** — Users need clear feedback
- **Ignore markdown output** — Always support both markdown + JSON
- **Create confusing flag names** — Be explicit and consistent
- **Forget the shebang** — `#!/usr/bin/env bun` at the top

### ✅ Do

- **Start with manual parsing** — It's simpler than you think
- **Test all three flag formats** — Users will use all of them
- **Provide real examples** — Copy-paste examples in usage text
- **Support --help** — Make your CLI self-documenting
- **Exit with proper codes** — 0 for success, 1 for error

---

## Checklist: Building a CLI

- [ ] Shebang at top: `#!/usr/bin/env bun`
- [ ] JSDoc explaining CLI purpose
- [ ] Argument parsing (--flag value, --flag=value, --flag)
- [ ] Usage function with examples
- [ ] Subcommand dispatch (if needed)
- [ ] Try/catch error handling with contextual messages
- [ ] Support both markdown (default) and JSON output
- [ ] Exit codes: 0 for success, 1 for error
- [ ] Tests for argument parsing
- [ ] Tests for each command/subcommand
- [ ] README explaining usage
- [ ] Package.json bin entry (if applicable)

---

## Pro Tips

**Tip 1: Progressive Disclosure in Help**
```typescript
// Basic help (what I do)
my-cli help
// Shows: command list + brief descriptions

// Advanced help (how to use me)
my-cli help create
// Shows: create command + all options + examples
```

**Tip 2: Output to Stderr for Errors**
```typescript
// Use console.error for errors (goes to stderr)
console.error("Error:", message);  // ✅ Correct

// Avoid using console.log for errors
console.log("Error:", message);   // ❌ Goes to stdout
```

**Tip 3: Use Color Strategically**
```typescript
// Color headers and important info
console.log(color("green", "✅ Success"));
console.log(color("yellow", "⚠️  Warning"));
console.error(color("red", "❌ Error"));

// Don't color everything — readers get fatigued
```

**Tip 4: Validate at Boundaries**
```typescript
// Validate user input (flags, args) immediately
if (!flags.name || typeof flags.name !== "string") {
  console.error("Error: --name flag required");
  process.exit(1);
}

// Trust internal functions (already validated)
function processName(name: string) {
  // name is guaranteed to be a non-empty string
}
```

---

## FAQ

**Q: Should I use oclif or similar frameworks?**
A: No. Manual parsing is simpler and keeps CLIs lean. The marketplace standard uses manual parsing across all CLIs.

**Q: How do I handle secrets in CLIs?**
A: Use environment variables. Never accept secrets as flags (they'd appear in shell history).

**Q: Should subcommands have their own help?**
A: Yes. `my-cli subcommand --help` should show help for that subcommand specifically.

**Q: When should I add colors?**
A: For headers, success messages, and errors. Don't color everything — let contrast do the work.

**Q: How do I test CLIs effectively?**
A: Unit test argument parsing. Integration test actual CLI invocations with real files.

**Q: Why manual parsing instead of libraries?**
A: Zero dependencies, explicit and predictable, easy to extend, familiar across all marketplace CLIs.

---

**Last Updated:** 2025-12-05
**Status:** Reference Implementation
**Related:** [bun-cli-patterns.md](bun-cli-patterns.md) (comprehensive reference + example)
