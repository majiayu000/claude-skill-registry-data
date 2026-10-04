---
name: my-wiki
description: Work with a local My Wiki knowledge base, Dashboard, and knowledge graph. Also use for explicitly requested remote/public knowledge access, including “远程知识库”, “远程服务”, “公网知识库”, and “公网服务”.
---

# My Wiki

This Skill routes Agent work to the My Wiki project or an explicitly requested remote service. It contains a lightweight CLI bridge, not the application or a vault.

## Choose A Route

Without a saved remote connection, normal My Wiki, knowledge-base, Dashboard, and graph requests use the local installation. Only explicit remote/public requests or a remote server URL initiate a first remote connection. A saved, enabled remote authorization makes ordinary bridge commands default to that service; use the Remote access reference when `where` reports remote mode. Explicit local intent overrides the saved connection with `--local` or `--vault`. Bare “连接 mywiki” must not initiate a first public connection.

| Request | Read |
| --- | --- |
| Local installation, missing project/vault, selecting a local vault | [Local setup](references/setup.md) |
| Local CLI syntax and Dashboard launch commands | [Local commands](references/commands.md) |
| Query or answer from knowledge | [Query workflow](references/workflows.md#query) |
| Capture a URL, document, folder, or image bundle | [Ingest workflow](references/workflows.md#ingest) |
| Distill, repair, or inspect knowledge health | [Maintenance workflow](references/workflows.md#maintain) |
| Galaxy naming, Concept/Reference structure, and OKF metadata | [Knowledge model](references/knowledge-model.md) |
| Evidence gates, OCR quality, formula review, and closure | [Evidence rules](references/evidence-rules.md) |
| Import or export a knowledge galaxy | [Sharing workflow](references/workflows.md#share-a-galaxy) |
| Open or operate the local Dashboard | [Dashboard workflow](references/workflows.md#dashboard) |
| Explicit remote/public connection and operations | [Remote access](references/remote.md) |
| Dashboard Agent/provider behavior | [Dashboard Agent reference](references/dashboard-agent.md) |
| IMA migration requested | [IMA import](references/ima-local-import.md) |
| Firecrawl requested or ordinary webpage capture failed | [Firecrawl](references/firecrawl-mcp.md) |

Read only the references relevant to the task. Use the bundled `scripts/my-wiki.mjs where` to resolve the current target; follow Local setup only when a local layer is missing. Operational knowledge comes from the selected vault, not from searching the application source.

Use native OKF terms: Concept, Reference, and original. Keep private knowledge, credentials, and runtime state out of the application repository.
