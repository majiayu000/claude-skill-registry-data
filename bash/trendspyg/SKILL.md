---
name: trendspyg
description: Free Google Trends data - real-time trending topics and keyword analysis over time (interest over time, related queries, interest by region).
---

# trendspyg
Free, open-source Python library for Google Trends data: trending now plus keyword interest over time, related queries, and interest by region. A maintained pytrends alternative with CLI and API.
```bash
export UVX_TRENDSPYG='uvx --from "trendspyg[mcp]" trendspyg-mcp'
```

## List available tools
```bash
alias trendspyg-list="npx -y mcporter list --stdio '$UVX_TRENDSPYG'"
trendspyg-list --all-parameters

# Get the schema of the specified tool
trendspyg-list --json | jq '.tools[] | select(.name == "<tool_name>")'
```

## Call specified tool
```bash
alias trendspyg-call="npx -y mcporter call --stdio '$UVX_TRENDSPYG'"
trendspyg-call --tool <tool_name> --args '{"key":"val"}'
```

## About `mcporter`
To improve compatibility, use `npx -y mcporter` instead of `mcporter` when executing commands.
