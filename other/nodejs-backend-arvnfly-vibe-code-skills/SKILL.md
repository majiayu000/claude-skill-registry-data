---
name: nodejs-backend
description: "Node.js runtime performance, event loop lag monitoring, cluster worker threads, and memory heap tuning."
---

# Node.js Backend Performance Protocol

Design high-throughput, non-blocking Node.js server architectures.

---

## 1. Non-Blocking Event Loop

1. Never run synchronous CPU-intensive tasks (`fs.readFileSync`, `crypto.pbkdf2Sync`, large JSON parsing) inside main event loop requests.
2. Offload heavy computational tasks to `worker_threads` or background worker queues.

---

## 2. Stream Processing

Process large payloads (file uploads, CSV exports, DB dumps) using Streams (`stream.pipeline`) rather than buffering into memory.
