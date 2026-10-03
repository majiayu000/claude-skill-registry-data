---
name: evaluate-deployment-options
description: Inspect software projects and evaluate application, database, and infrastructure deployment architectures across static hosting, serverless, containers, managed platforms, cloud servers, and managed or self-hosted data services. Use for deployment selection, hosting comparisons, database deployment, architecture reviews, cost and compliance assessment, ICP/region decisions, free-domain-first rollouts, multi-cloud choices, high-concurrency or high-performance architecture planning, or deployment planning for static sites, H5, mini programs, plugins with remote updates, and Python, Java/Kotlin, Node.js, Go, PHP, Ruby, Rust, .NET, Docker, and mixed-stack projects.
---

# Evaluate Deployment Options

Produce an evidence-based deployment recommendation without creating cloud resources or changing DNS unless the user explicitly asks for implementation.

## Workflow

1. Read workspace `AGENTS.md` and applicable project instructions.
2. Locate the project root, archives, manifests, lockfiles, build files, Docker files, infrastructure configuration, and environment examples.
3. Run the read-only scanner:

   ```powershell
   python "<skill-dir>/scripts/inspect_project.py" "<project-path>"
   ```

4. Verify scanner findings against source imports, entry points, build scripts, network calls, persistence, database schemas and migrations, background work, file uploads, native binaries, and environment variables. Treat detection as evidence, not proof.
5. Establish requirements. Infer low-risk defaults, but mark unknowns that can change the recommendation:
   - target users and regions;
   - acceptable cost and free-tier preference;
   - domain ownership and desired temporary domain;
   - state, database, file storage, queues, WebSockets, scheduled or long-running work;
   - traffic model, concurrency, throughput, latency SLO, availability target, growth, and peak-to-average ratio;
   - runtime, CPU, memory, disk, GPU, native library, and process-duration needs;
   - security, privacy, availability, recovery, and operational capacity;
   - release frequency and whether Git-based automation is desired.
6. Apply hard gates and the complexity gate before scoring. Read [references/decision-model.md](references/decision-model.md).
7. Load only relevant references:
   - runtime and product patterns: [references/runtime-patterns.md](references/runtime-patterns.md);
   - database selection, topology, backup, and migration: [references/database-patterns.md](references/database-patterns.md);
   - high-concurrency and high-performance architecture: [references/high-scale-architecture.md](references/high-scale-architecture.md);
   - provider and architecture routing: [references/provider-routing.md](references/provider-routing.md);
   - region, ICP, and regulatory cautions: [references/compliance-and-regions.md](references/compliance-and-regions.md);
   - capability boundaries and required disclaimers: [references/limitations.md](references/limitations.md);
   - required response structure: [references/output-template.md](references/output-template.md).
8. Browse current primary documentation for volatile facts such as pricing, quotas, runtime support, custom domains, marketplace rules, and filing requirements. State the verification date. Do not rely on remembered free-tier numbers.
9. Select one output mode:
   - **Simple deployment evaluation:** rank a recommended option, a low-cost or low-operations alternative, and a portable or server-based fallback.
   - **Architecture design:** when the complexity gate triggers, do not treat the task as a simple deployment. Produce a separate application, database, cache, queue, network, scaling, reliability, observability, capacity, load-test, rollout, rollback, and disaster-recovery plan.
10. Give separate confidence values for requirement understanding and deployment or architecture design. Explain material confidence reducers and the cheapest validation that would raise confidence.

## Decision Principles

- Prefer the simplest managed option that satisfies all hard constraints.
- Prefer free provider-assigned domains for validation when requested, then add the branded domain after acceptance.
- Prefer Git-based CI/CD when the user has GitHub or another supported Git provider and expects continued development.
- Do not recommend a server for a purely static project.
- Do not recommend serverless for workloads requiring unsupported runtimes, persistent local state, long execution, special networking, GPU, or incompatible native binaries.
- Treat Docker support as portability evidence, not automatic proof that a VM is required.
- Keep frontend, API, database, object storage, and update distribution independently replaceable when practical.
- Evaluate database deployment as a first-class decision. Compare managed and self-hosted choices, topology, connection limits, pooling, replication, backup, restore, migration, encryption, observability, and data residency.
- Do not claim a high-concurrency or high-performance design without a workload model and measurable SLOs. When those inputs are missing, state explicit capacity assumptions and require load testing before production sizing.
- Treat Tencent Cloud as the preferred tie-breaker when it is operationally or geographically suitable, not as a forced winner. Compare Cloudflare, Tencent Cloud, Alibaba Cloud, Volcengine, Baidu AI Cloud, AWS, and other relevant providers against the same gates.
- Consider an overseas region when avoiding mainland ICP filing is a requirement, while explicitly assessing cross-border latency, availability, data residency, platform-domain rules, and support implications.
- Never put server credentials in public frontend variables or repositories.
- For remote updates, require versioning, integrity hashes, cryptographic signatures, rollback, channels, and compliance with the target marketplace's remote-code policy.
- Separate evaluation from execution. DNS edits, deployments, purchases, account authorization, and production data changes require explicit user authorization.
- Always state applicable limitations. Do not present heuristic detection, estimated cost, legal/compliance interpretation, generated architecture, or untested capacity as verified production fact.

## Confidence

Always report:

```text
Requirements confidence: 0.00-1.00
Deployment design confidence: 0.00-1.00
```

Base confidence on evidence coverage, not optimism. Do not lower confidence merely because multiple good architectures exist; lower it when missing facts can change the ranking or when current platform behavior has not been verified.
