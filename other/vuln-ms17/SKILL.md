---
name: vuln-ms17
description: "```bash"
domain: cybersecurity
---
## CyberSecSuite Integration

```bash
# Open a case before starting investigation
mcp__cybersec__case_open --title "ms17" --type investigation

# Persist findings to PostgreSQL
mcp__cybersec__add_finding --title "..." --severity high --description "..."

# Log IOCs
mcp__cybersec__add_ioc --type domain --value "..." --confidence 0.9

# Map to MITRE
mcp__cybersec__suggest_mitre --description "..."
```

**Agent:** `@cybersec-agent` → delegates to appropriate specialist
