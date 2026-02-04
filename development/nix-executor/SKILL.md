---
name: nix-executor
description: Use when you need to test Nix expressions, validate Nix configuration syntax before applying, debug Nix code or understand evaluation results, inspect derivation attributes, or evaluate flake outputs and inputs
license: MIT
---

# Nix Code Executor

This skill provides safe execution and evaluation of Nix code, including expressions, derivations, and configuration validation.

## What This Skill Does

This skill helps you:
- Evaluate Nix expressions and see their results
- Test Nix derivations before building
- Validate Nix configuration syntax
- Debug Nix code issues
- Inspect Nix store paths and attributes

## When to Use This Skill

Use this skill when you need to:
- Test a Nix expression to see what it evaluates to
- Validate Nix configuration syntax before applying
- Debug Nix code or understand evaluation results
- Inspect derivation attributes
- Evaluate flake outputs or inputs

## Instructions

When this skill is activated, follow these steps:

### 1. Determine the Execution Type

Identify what kind of Nix operation is needed:

- **Expression evaluation**: Use `nix eval` for simple expressions
- **Instantiation**: Use `nix-instantiate` to build derivations
- **Flake evaluation**: Use `nix eval` with flake references
- **Build testing**: Use `nix build --dry-run` for dry runs
- **Configuration check**: Use `nix-instantiate --eval` for config validation

### 2. Choose the Appropriate Command

**For simple expressions:**
```bash
nix eval --expr 'EXPRESSION'
```

**For file-based expressions:**
```bash
nix-instantiate --eval FILE.nix
```

**For flake outputs:**
```bash
nix eval .#OUTPUT_PATH
```

**For pretty JSON output:**
```bash
nix eval --json --expr 'EXPRESSION' | jq
```

**For dry-run builds:**
```bash
nix build --dry-run .#PACKAGE
```

**For checking derivation attributes:**
```bash
nix derivation show .#PACKAGE
```

### 3. Safety Considerations

- Use `--dry-run` when you don't want to actually build anything
- Use `--read-only` flag when evaluating untrusted code
- Wrap expressions in `--expr` to avoid file system modifications
- Check for evaluation errors before proceeding with builds

### 4. Common Use Cases

**Evaluate a simple expression:**
```bash
nix eval --expr '1 + 1'
nix eval --expr 'builtins.toString (map (x: x * 2) [1 2 3])'
```

**Check flake configuration:**
```bash
nix eval .#nixosConfigurations.HOSTNAME.config.system.build.toplevel
```

**Test attribute existence:**
```bash
nix eval --expr 'builtins.hasAttr "attr" { attr = 1; }'
```

**Inspect package metadata:**
```bash
nix eval --json nixpkgs#package.meta | jq
```

**Validate Nix file syntax:**
```bash
nix-instantiate --parse FILE.nix
```

### 5. Error Handling

When evaluation fails:

1. Check the error message for syntax issues
2. Use `--show-trace` for detailed error traces
3. Validate individual subexpressions
4. Check for infinite recursion with `--max-call-depth`

**Example with trace:**
```bash
nix eval --show-trace --expr 'EXPRESSION'
```

### 6. Output Formatting

Control output format based on needs:

- Default: Nix expression format
- `--json`: JSON format (parseable)
- `--raw`: Raw output without quotes
- `--apply`: Transform output with a function

### 7. Working with Files

**Evaluate specific attributes:**
```bash
nix-instantiate --eval --strict --attr attrPath file.nix
```

**Import and evaluate:**
```bash
nix eval --expr 'import ./file.nix'
```

## Examples

### Example 1: Test a Nix Expression
```bash
nix eval --expr 'let pkgs = import <nixpkgs> {}; in pkgs.lib.version'
```

### Example 2: Validate Flake Output
```bash
nix eval .#darwinConfigurations.MacBook-Pro-Maxim.system
```

### Example 3: Debug Configuration Value
```bash
nix eval --json .#nixosConfigurations.hostname.config.services.openssh.enable
```

### Example 4: Check Package Availability
```bash
nix eval --expr 'builtins.hasAttr "opencode" (import <nixpkgs> {})'
```

### Example 5: Inspect Derivation
```bash
nix derivation show nixpkgs#hello
```

## Best Practices

1. **Start Simple**: Test small expressions before complex ones
2. **Use --dry-run**: Avoid unintended builds during testing
3. **Check Syntax First**: Use `nix-instantiate --parse` to validate syntax
4. **Use --show-trace**: Get detailed error information when debugging
5. **Format Output**: Use `--json` with `jq` for readable structured output
6. **Test Incrementally**: Break complex expressions into smaller testable parts

## Troubleshooting

### Common Issues

**Infinite Recursion:**
```bash
# Use --max-call-depth to prevent runaway evaluation
nix eval --max-call-depth 1000 --expr 'EXPRESSION'
```

**Path Not Found:**
```bash
# Ensure you're in the right directory for relative imports
# Or use absolute paths
nix eval --expr 'import /absolute/path/to/file.nix'
```

**Attribute Missing:**
```bash
# Check if attribute exists first
nix eval --expr 'builtins.attrNames (import ./file.nix)'
```

## References

- [Nix Manual - nix eval](https://nixos.org/manual/nix/stable/command-ref/new-cli/nix3-eval.html)
- [Nix Manual - nix-instantiate](https://nixos.org/manual/nix/stable/command-ref/nix-instantiate.html)
- [Nix Manual - Built-in Functions](https://nixos.org/manual/nix/stable/language/builtins.html)
