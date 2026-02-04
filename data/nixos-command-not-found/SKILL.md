---
name: nixos-command-not-found
description: Auto-install missing commands in NixOS environments. Detects NixOS, searches for packages containing the missing command, and re-runs with nix shell. Use when commands fail with "command not found" errors.
---

# NixOS Command Not Found Handler

Automatically handles "command not found" errors in NixOS environments by searching for packages and retrying with `nix shell`.

## When to Use

Activate this skill when:
- Command fails with "command not found" or "No such file or directory"
- User is in NixOS environment (detected by `/etc/nixos` existence or `NIX_STORE` env var)
- Command appears to be a standard Unix tool or known package

## Workflow

1. **Detect NixOS environment**: Check for `/etc/nixos` or `NIX_STORE` env var
2. **Extract command name**: Get the missing command from error output
3. **Delegate everything to nixos agent**: Agent finds package AND runs command
4. **Return command output**: Agent provides the actual command result

## Implementation Steps

### 1. Environment Detection
Check if we're in NixOS:
```bash
test -d /etc/nixos || test -n "$NIX_STORE"
```

### 2. Delegate Complete Task
Use Task tool with nixos agent to handle everything:
```
Task(
  description="Run missing command with nix shell",
  prompt="The command '<original-command>' failed with 'command not found'. Please:
1. Search for the NixOS package that provides this command
2. Run the command using 'nix shell nixpkgs#<package> -c <original-command>'
3. Return the actual command output/result",
  subagent_type="nixos"
)
```

### 3. Return Results
The nixos agent returns the actual command execution result, not just package info.

## Examples

### Missing `tree` command
1. User runs: `tree /some/path`
2. Error: `zsh: command not found: tree`
3. Detect NixOS environment ✓
4. Delegate to nixos agent: "Run 'tree /some/path' with nix shell"
5. Agent finds `tree` package, runs `nix shell nixpkgs#tree -c tree /some/path`
6. Agent returns: actual directory tree output

### Missing `jq` command
1. User runs: `cat data.json | jq '.name'`
2. Error: `command not found: jq`
3. Delegate to nixos agent: "Run 'jq '.name'' with nix shell"
4. Agent finds `jq` package, runs with stdin preserved
5. Agent returns: actual JSON parsing result

### Missing `cargo` command
1. User runs: `cargo build`
2. Error: `command not found: cargo`
3. Delegate to nixos agent: "Run 'cargo build' with nix shell"
4. Agent finds `cargo` package, runs `nix shell nixpkgs#cargo -c cargo build`
5. Agent returns: actual build output or errors

## Edge Cases

### Multiple Package Options
Nixos agent handles all selection logic internally:
- Uses nixos MCP tools to find best match
- Considers exact name matches, package descriptions, etc.
- Picks most appropriate option or asks user if truly ambiguous

### Complex Commands  
Nixos agent handles command complexity:
- Preserves pipes, redirects, and shell syntax
- Uses appropriate shell escaping when needed
- Maintains stdin/stdout/stderr as expected

### Already in Nix Shell
Nixos agent handles this case:
- Detects if already in nix shell
- Still proceeds (might need different package)
- Can inform user about current nix shell context

## Error Handling

### Package Not Found
Nixos agent handles all error scenarios:
- Tries broader search terms and fallbacks
- Searches programs, options, or suggests alternatives
- Returns helpful error message if no package found

### Command Failures
Nixos agent returns actual command results:
- Shows real command output if successful
- Returns actual error messages if command fails
- Distinguishes between "package not found" vs "command failed"

## Integration Notes

### Detection Triggers
Monitor for these error patterns:
- `command not found: <cmd>`
- `<cmd>: No such file or directory`
- `zsh: command not found: <cmd>`
- `bash: <cmd>: command not found`

### Agent Responsibilities
Nixos agent handles all technical details:
- Maintains current working directory
- Preserves environment variables  
- Keeps stdin/stdout/stderr intact
- Shows what package was used
- Provides appropriate feedback

### Main Agent Role
Main agent just:
- Detects NixOS environment
- Delegates to nixos agent
- Returns agent's command results to user

## Configuration

### Excluded Commands
Don't handle these (likely typos or not packages):
- Single letters: `a`, `b`, `x`
- Common typos: `sl`, `gerp`
- Shell builtins that failed: `cd`, `export`

### Channel Preference
- Default to `nixpkgs#` (follows system channel)
- Could use `nixpkgs/unstable#` for newest versions
- Respect user's flake configuration if detected