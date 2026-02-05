---
name: timestamp
description: Generate deterministic timestamps in YYYYMMDDHHMMSS format using bash. Use when you need timestamps for filenames, logging, or any situation requiring consistent timestamp formatting without LLM generation.
allowed-tools: Bash
---

# Timestamp

## Overview

Generate timestamps in YYYYMMDDHHMMSS format (e.g., `20251030143215`) using bash date command for deterministic, reliable timestamp generation.

## When to Use

- Creating timestamped filenames or directories
- Adding timestamps to logs or commit messages
- Any situation requiring consistent timestamp formatting
- When deterministic bash execution is preferred over LLM-generated timestamps

## Usage

Always use the bash script to generate timestamps:

```bash
bash ./skills/timestamp/scripts/generate_timestamp.sh
```

### Examples

**Timestamped filename:**

```bash
timestamp=$(bash ./skills/timestamp/scripts/generate_timestamp.sh)
echo "backup_${timestamp}.tar.gz"
# Output: backup_20251030143215.tar.gz
```

**Timestamped directory:**

```bash
timestamp=$(bash ./skills/timestamp/scripts/generate_timestamp.sh)
mkdir "logs_${timestamp}"
```

**In file content:**

```bash
timestamp=$(bash ./skills/timestamp/scripts/generate_timestamp.sh)
echo "Generated at: ${timestamp}" > output.txt
```

## Format Specification

- **Format:** YYYYMMDDHHMMSS
- **Example:** 20251030143215
- **Breakdown:**
  - YYYY: 4-digit year (2025)
  - MM: 2-digit month (10)
  - DD: 2-digit day (30)
  - HH: 2-digit hour, 24h format (14)
  - MM: 2-digit minute (32)
  - SS: 2-digit second (15)

## Resources

### scripts/generate_timestamp.sh

Executable bash script using `date +"%Y%m%d%H%M%S"` to generate timestamps in YYYYMMDDHHMMSS format.
