---
name: detecting-agent-environment
description: Utilities and patterns for detecting execution environment (CI/CD vs local, network access, available ports, timeouts). Use when you need to adapt scripts or workflows based on where the agent is running, or when creating helper scripts that need environment-aware behavior.
---

# Agent Helper Scripts

Utilities for GitHub Copilot agents working on Y-Not Radio site.

## Environment Detection

Use `detect-environment.sh` to adapt scripts to different environments:

```bash
# Source the utility
source bin/agent-helpers/detect-environment.sh

# Print environment info
print_environment

# Check environment
if detect_ci; then
  echo "Running in CI/CD"
  # Use optimized workflow
fi

if ! detect_network; then
  echo "Network restricted - cannot pull packages"
  exit 1
fi

# Get appropriate timeout
TIMEOUT=$(get_timeout "service_ready")
timeout $TIMEOUT bash -c 'until service_ready; do sleep 5; done'
```

## Creating New Helper Scripts

When creating helper scripts:

1. **Source environment detection**
   ```bash
   source "$(dirname "$0")/detect-environment.sh"
   print_environment
   ```

2. **Use appropriate timeouts**
   ```bash
   TIMEOUT=$(get_timeout "npm_install")
   timeout $TIMEOUT npm install
   ```

3. **Provide clear output**
   ```bash
   echo "✅ Success message"
   echo "⚠️  Warning message"
   echo "❌ Error message"
   ```

4. **Exit with proper codes**
   ```bash
   exit 0  # Success
   exit 1  # Failure
   ```

5. **Log to .agent-tmp/**
   ```bash
   mkdir -p .agent-tmp
   command 2>&1 | tee .agent-tmp/command.log
   ```

## Related Skills

Before creating scripts or PRs, see:

- `testing-pr-changes` skill - Success criteria and testing workflows
- `agent-automation-infrastructure` skill - Current automation state and pre-built images

## Performance Baselines

Scripts should respect these baselines:

| Operation | Expected | Warning | Failure |
|-----------|----------|---------|---------|
| Container start | < 60s | 60-120s | > 120s |
| npm install | < 120s | 120-300s | > 300s |
| Service ready | < 180s | 180-360s | > 360s |

If exceeding "Warning" thresholds, report performance issues in PR.
