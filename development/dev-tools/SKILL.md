---
name: Dev Tools
description: Run CLI dev tools for game development (world inspection, benchmarks, assets, simulation). Use when user wants to 'check performance', 'inspect world', 'validate assets', 'stress test', or asks about new CLI features.
---

# Dev Tools

CLI development tools for Stapledons Voyage game. Provides performance benchmarks, world inspection, asset validation, and simulation stress testing.

## Quick Start

```bash
# Build CLI first
make cli

# Run commands
./bin/voyage world -summary      # Quick world state
./bin/voyage bench -n 1000       # Performance benchmarks
./bin/voyage assets              # Validate game assets
./bin/voyage sim -steps 1000     # Stress test simulation
```

## When to Use This Skill

Invoke this skill when user asks to:
- "check performance" or "run benchmarks"
- "inspect world" or "show world state"
- "validate assets" or "check assets"
- "stress test" or "test simulation"
- "what CLI tools do we have?"
- Debug simulation issues or performance problems

## Available Commands

### World Inspection
```bash
./bin/voyage world                    # Full world state (truncated)
./bin/voyage world -summary           # Quick stats only
./bin/voyage world -json              # Raw JSON output
./bin/voyage world -seed 123          # Use specific seed
./bin/voyage world -steps 100         # Run N steps first
```

### Performance Benchmarks
```bash
./bin/voyage bench                    # Default 1000 iterations
./bin/voyage bench -n 10000           # More iterations
./bin/voyage bench -warmup 50         # Custom warmup
./bin/voyage bench -profile           # With CPU profiling
```

### Asset Validation
```bash
./bin/voyage assets                   # Check assets/
./bin/voyage assets -dir ./custom     # Custom directory
./bin/voyage assets -v                # Verbose (list files)
./bin/voyage assets -fix              # Create missing dirs
```

### Simulation Stress Test
```bash
./bin/voyage sim                      # 10000 steps default
./bin/voyage sim -steps 100000        # Longer test
./bin/voyage sim -seed 123            # Specific seed
./bin/voyage sim -validate            # Validate state each step
```

### AI Handler Testing
```bash
./bin/voyage ai -list                 # Show available providers
./bin/voyage ai -prompt "Hello"       # Auto-detect provider
./bin/voyage ai -generate-image       # Image generation
./bin/voyage ai -list-voices          # TTS voices
```

## Scripts

### `scripts/quick_bench.sh`
Run benchmarks with filtered output (removes debug noise).

### `scripts/full_report.sh`
Generate comprehensive development report.

### `scripts/suggest_tools.sh`
Analyze codebase for potential new CLI tools.

## Workflow

1. **Build CLI** - `make cli`
2. **Run command** - Execute voyage command
3. **Interpret results** - Check output
4. **Report issues** - Use ailang-feedback for codegen bugs

## Suggesting New CLI Tools

When identifying CLI needs, consider:
- `voyage save` - Inspect/manage save files
- `voyage replay` - Replay recorded inputs
- `voyage export` - Export data for analysis
- `voyage config` - Manage game configuration
- `voyage starmap` - Starmap data tools

To add a new tool:
1. Add command case to `cmd/cli/main.go`
2. Implement `run<Command>Command()` function
3. Update this skill documentation
4. Run `make cli`

## Known Issues

**Debug output noise:** Filter with `| grep -v "^tick"` - tracked as AILANG bug.

## Resources

See [resources/cli_reference.md](resources/cli_reference.md) for complete documentation.
