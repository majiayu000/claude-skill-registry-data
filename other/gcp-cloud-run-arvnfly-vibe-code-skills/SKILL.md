---
name: gcp-cloud-run
description: "Google Cloud Run microservices, container concurrency, autoscaling limits, and Cloud SQL connection proxies."
---

# GCP Cloud Run Protocol

1. Set concurrency per container instance based on CPU memory profile (typically 40-80).
2. Connect to Cloud SQL via unix domain sockets or Cloud SQL Auth Proxy.
3. Configure min-instances > 0 for zero-cold-start latency on critical paths.
