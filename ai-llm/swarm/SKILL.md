---
name: swarm
version: 1.0.4
description: Parallel task execution using Gemini Flash workers. 200x cheaper than Opus. Use for any parallelizable work to preserve quota.
homepage: https://github.com/Chair4ce/node-scaling
license: MIT
author: Chair4ce
metadata:
  {
    "openclaw": {
      "emoji": "🐝",
      "requires": {
        "bins": ["node"],
        "env": ["GEMINI_API_KEY"]
      },
      "primaryEnv": "GEMINI_API_KEY",
      "install": [
        {
          "id": "release-download",
          "kind": "download",
          "url": "https://github.com/Chair4ce/node-scaling/archive/refs/tags/v1.0.4.zip",
          "archive": "zip",
          "extract": true,
          "stripComponents": 1,
          "targetDir": "~/.openclaw/skills/node-scaling",
          "label": "Download v1.0.4 from GitHub",
          "postInstall": "cd ~/.openclaw/skills/node-scaling && npm install --production"
        }
      ]
    }
  }
---

# Swarm

Parallel task execution for AI agents. Distributes work across cheap LLM workers (Gemini Flash) instead of burning expensive tokens on sequential calls.

**The bottom line:** 200x cheaper, 157x faster.

---

## Installation

```bash
git clone https://github.com/Chair4ce/node-scaling.git ~/.openclaw/skills/node-scaling
cd ~/.openclaw/skills/node-scaling
npm install
npm run setup
```

Setup prompts for your API key. Gemini recommended.

---

## Quick Start

```bash
swarm start                    # Start the daemon
swarm status                   # Check if running
swarm parallel "Q1" "Q2" "Q3"  # Run prompts in parallel
swarm bench --tasks 30         # Benchmark throughput
```

---

## Performance

### Single Node

| Tasks | Time | Throughput |
|-------|------|------------|
| 10 | 700ms | 14/sec |
| 30 | 1,000ms | 30/sec |
| 50 | 1,450ms | 35/sec |

### Distributed Fleet (6 Nodes)

Real benchmark across Mac mini + 5 Linux servers:

| Node | Tasks | Time | Throughput |
|------|-------|------|------------|
| Mac mini | 100 | 3.76s | 26.6/sec |
| Worker 2 | 100 | 3.20s | 31.3/sec |
| Worker 3 | 100 | 3.23s | 31.0/sec |
| Worker 5 | 100 | 3.27s | 30.6/sec |
| Worker 6 | 100 | 3.21s | 31.2/sec |
| Worker 7 | 100 | 3.32s | 30.2/sec |

**Total: 600 tasks in 3.8 seconds**

Combined throughput: 181 tasks/sec

---

## Cost Comparison

| Method | 600 Tasks | Time | Cost |
|--------|-----------|------|------|
| Opus (sequential) | 600 | ~10 min | ~$9.00 |
| Swarm (distributed) | 600 | 3.8 sec | ~$0.045 |

**157x faster. 200x cheaper.**

---

## When to Use

- 3+ independent research queries
- Comparing multiple subjects
- Batch document analysis
- Multi-URL fetching and summarization
- Any parallelizable LLM work

If you're doing it sequentially, you're doing it wrong.

---

## Configuration

`~/.config/clawdbot/node-scaling.yaml`

```yaml
node_scaling:
  enabled: true
  limits:
    max_nodes: 20
    max_concurrent_api: 20
  provider:
    name: gemini
    model: gemini-2.0-flash
  cost:
    max_daily_spend: 10.00
```

---

## Multi-Node Setup

Deploy on additional machines for linear scaling:

```bash
git clone https://github.com/Chair4ce/node-scaling.git ~/.openclaw/skills/node-scaling
cd ~/.openclaw/skills/node-scaling && npm install && npm run setup
swarm start
```

Each node adds ~30 tasks/sec to combined throughput.

---

## Security

- Requires your own API key (no credentials hardcoded)
- Supabase integration is optional and disabled by default
- Uses local file-based coordination by default
- All LLM calls go to the provider you configure

---

## Links

- [GitHub Repository](https://github.com/Chair4ce/node-scaling)
- [Changelog](https://github.com/Chair4ce/node-scaling/blob/main/CHANGELOG.md)
- [Installation Guide](https://github.com/Chair4ce/node-scaling/blob/main/INSTALL.md)
