---
name: check-env-keys
description: Verify which environment variable keys are present in .env files or shell environment without exposing their values. Use when you need to check env configuration or compare keys between .env files.
---

# Check Environment Variable Keys

This skill allows you to verify which environment variable keys are present in .env files OR shell environment WITHOUT exposing their values.

## Usage

When invoked, check for environment variable keys in the following locations:

**File-based configuration:**
- `.env.local` (local overrides, gitignored)
- `.env` (if it exists, usually gitignored)
- `.env.example` (template file, committed)
- `.env.sample` (alternative template name)

**Shell environment:**
- Exported variables in current shell session
- Variables from `~/.bashrc`, `~/.zshrc`, etc.
- System-level environment variables

## How to Check

### Step 1: List all environment variable keys

Use this command to extract only the keys (not values) from env files:

```bash
for file in .env.local .env .env.example .env.sample; do if [ -f "$file" ]; then echo "=== Keys in $file ==="; grep -v '^#' "$file" | grep -v '^[[:space:]]*$' | grep '=' | cut -d'=' -f1 | sort; echo ""; fi; done
```

### Step 2: Check for missing keys (with shell environment fallback)

Use this command to find keys that are missing from both .env.local AND the shell environment:

```bash
sample_file=""; if [ -f ".env.sample" ]; then sample_file=".env.sample"; elif [ -f ".env.example" ]; then sample_file=".env.example"; fi; local_file=""; if [ -f ".env.local" ]; then local_file=".env.local"; elif [ -f ".env" ]; then local_file=".env"; fi; if [ -n "$sample_file" ]; then sample_keys=$(grep -v '^#' "$sample_file" | grep -v '^[[:space:]]*$' | grep '=' | cut -d'=' -f1 | sort); local_keys=""; if [ -n "$local_file" ]; then local_keys=$(grep -v '^#' "$local_file" | grep -v '^[[:space:]]*$' | grep '=' | cut -d'=' -f1 | sort); fi; missing=""; for key in $sample_keys; do if [ -n "$local_keys" ] && echo "$local_keys" | grep -q "^$key$"; then continue; fi; if printenv "$key" >/dev/null 2>&1; then continue; fi; missing="$missing\n  - $key"; done; if [ -n "$missing" ]; then echo "⚠️ Missing from .env.local and shell environment (present in $sample_file):"; echo -e "$missing"; else echo "✓ All required environment variables are configured (either in .env.local or shell environment)"; fi; else echo "No .env.sample or .env.example file found"; fi
```

**Important**: This command checks if variables are set in the shell environment WITHOUT exposing their values. Variables can be configured in three ways:
1. In `.env.local` file
2. In `.env` file
3. As shell environment variables (e.g., exported in `~/.bashrc`, `~/.zshrc`, or set by the system)

## What This Shows

- ✓ Which environment variables are **defined** (key exists)
- ✓ Comparison between local and example files to find missing keys
- ✗ **NEVER** shows the actual values (for security)

## Verification Logic

Environment variables are considered "configured" if they exist in any of these locations:
1. `.env.local` file
2. `.env` file
3. Shell environment (exported variables)

If a key exists in ANY of these locations:
- Assume the value is set (even if empty string)
- Assume the value is correctly configured
- No need to prompt user for the value
- **NEVER** expose the actual value for security

The verification process ONLY checks for key existence, not values. This ensures API keys and secrets are never exposed in logs or to the AI.

## Common Checks

After running the commands, you can:
- Verify all keys from .env.example/.env.sample are present in .env.local OR shell environment
- Identify truly missing environment variables (not in file AND not in shell)
- Confirm required keys are configured without exposing secrets
- Understand which variables are set globally (shell) vs locally (file)

## Example Output

### Step 1 Output (List keys)
```
=== Keys in .env.local ===
DATABASE_URL
NEXT_PUBLIC_API_URL

=== Keys in .env.sample ===
ANTHROPIC_API_KEY
DATABASE_URL
NEXT_PUBLIC_API_URL
OPENAI_API_KEY
```

### Step 2 Output (Check missing keys)

**Scenario A**: All variables configured
```
✓ All required environment variables are configured (either in .env.local or shell environment)
```

**Scenario B**: Some variables missing from both .env.local and shell
```
⚠️ Missing from .env.local and shell environment (present in .env.sample):
  - ANTHROPIC_API_KEY
  - SOME_OTHER_KEY
```

**Note**: If `OPENAI_API_KEY` was in .env.sample but not reported as missing, it means it's set in the shell environment (e.g., exported in `~/.zshrc`).
