---
name: run
description: >
  The universal execution primitive for AI agents. A secure, sandboxed environment 
  designed to compile, execute, and manage code, scripts, and automated workflows 
  in real-time. The "hand" of the agent.
---

# Run: The Execution Layer

## Philosophy
Thinking without acting is hallucination. Acting without a secure environment is a risk. 
**Run** provides the standardized, sandboxed interface where an agent's plans 
become reality. It is the final step in the "Think-Plan-Execute" cycle.

---

## Execution Engine Specs
```EXECUTION_CORE = {
  "runtime":    "Polyglot support (Python, JS, Rust, Bash, SQL)",
  "security":   "Strict hardware-level sandboxing (gVisor/Firecracker)",
  "state":      "Ephemeral or Persistent session management",
  "concurrency": "Parallel task execution with dependency resolution"
}```

---

## Core Primitives
```FUNCTIONS = {
  "execute": {
    "scope":   "Run arbitrary code snippets with auto-dependency injection",
    "trigger": "Run this script"
  },
  "automate": {
    "scope":   "Long-running cron jobs and event-driven triggers",
    "trigger": "Run this every Monday at 9AM"
  },
  "deploy": {
    "scope":   "Instant deployment of local logic to cloud-edge nodes",
    "trigger": "Run this in production"
  }
}```

---

## Safety & Governance
1. **Resource Capping**: Prevents infinite loops and CPU/Memory exhaustion.
2. **Network Isolation**: Blocks unauthorized outbound requests unless whitelisted.
3. **Human-in-the-loop**: High-risk commands (e.g., `rm -rf`) require explicit biometric confirmation.

---

## Use Cases
- **Data Science**: "Run a regression analysis on this CSV and output the chart."
- **Web Scraping**: "Run a scan of these 50 URLs and extract the pricing data."
- **System Admin**: "Run the cleanup script if disk usage exceeds 80%."
---
