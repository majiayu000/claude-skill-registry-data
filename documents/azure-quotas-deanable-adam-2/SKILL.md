---
name: azure-quotas
description: Expert knowledge for Azure Quotas development including limits & quotas. Use when requesting per-region Storage account quota increases, checking limits, or filing Azure support requests, and other Azure Quotas related development tasks. Not for Azure Cost Management (use azure-cost-management), Azure Monitor (use azure-monitor), Azure Policy (use azure-policy), Azure Resource Manager (use azure-resource-manager).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Quotas Skill

This skill provides expert guidance for Azure Quotas. Covers limits & quotas. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: This file may be large. Use the **Category Index** below to locate relevant sections, then use `read_file` with specific line ranges (e.g., `L136-L144`) to read the sections needed for the user's question
This skill requires **network access** to fetch documentation content.
Use `mcp_microsoftdocs:microsoft_docs_fetch` to retrieve full articles.
- **Fallback**: Use the built-in `WebFetch` tool if the Microsoft Learn MCP server is not available.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Limits & Quotas | L23-L26 | How to request and manage per-region Azure Storage account quota increases, including limits, prerequisites, and support request steps. |

### Limits & Quotas
| Topic | URL |
|-------|-----|
| Increase Azure Storage account quota per region | https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests |
