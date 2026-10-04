---
name: agent-news-monitor
description: Monitor Hacker News, Reddit, and arXiv for AI agent developments and trending topics. Use when the user wants a summary of recent AI agent news, needs to search for specific research papers, or wants to set up automated news digests in heartbeats.
---

# Agent News Monitor

Track the cutting edge of AI agent research and community discussion.

## Core Features

- **Daily Digest**: Summarize the last 24 hours of AI agent activity across HN, Reddit, and arXiv.
- **Trending Topics**: Identify what's hot in the agentic AI space right now.
- **Deep Search**: Query historical data for specific topics like "memory systems" or "mcp protocol".
- **Topic Watching**: Configure specific keywords to prioritize in future reports.

## Usage

All operations are handled via the bundled monitor script.

### 1. Generate News Digest
Get a formatted summary of the latest developments:
```bash
bash scripts/agent-news-monitor/scripts/monitor.sh digest
```
*Options:*
- `--quiet`: For background automation (no ASCII art).
- `--json`: For programmatic processing.

### 2. Search Specific Topics
```bash
bash scripts/agent-news-monitor/scripts/monitor.sh search "your query"
```

### 3. Track Trends
```bash
bash scripts/agent-news-monitor/scripts/monitor.sh trending
```

## Maintenance & Config

- **Watch Topics**: Set keywords to watch: `bash monitor.sh watch "memory,tool-use"`
- **Sources**: Hacker News, Reddit (r/LocalLLaMA, r/MachineLearning, r/artificial), and arXiv (cs.AI, cs.CL, cs.LG).

## Implementation Detail
This skill uses a local `jq` binary located in `scripts/jq` for parsing JSON responses. Ensure `scripts/` is in your PATH or call the script with the full path.
