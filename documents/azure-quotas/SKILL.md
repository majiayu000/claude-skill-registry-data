---
name: azure-quotas
description: Expert knowledge for Azure Quotas development including limits & quotas. Use when requesting per-region Storage account quota increases, checking limits, or filing Azure support requests, and other Azure Quotas related development tasks. Not for Azure Cost Management (use azure-cost-management), Azure Monitor (use azure-monitor), Azure Policy (use azure-policy), Azure Resource Manager (use azure-resource-manager).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Quotas Skill

This skill provides expert guidance for Azure Quotas. Covers limits & quotas. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: Use the **Category Index** below to locate relevant sections. For categories with line ranges (e.g., `L35-L120`), use `read_file` with the specified lines. For categories with file links (e.g., `[security.md](security.md)`), use `read_file` on the linked reference file

This skill requires **network access** to fetch documentation content:
- **Preferred**: Use `mcp_microsoftdocs:microsoft_docs_fetch`. Returns Markdown.
- **Fallback**: Use `WebFetch`. Returns Markdown.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Limits & Quotas | L25-L28 | How to request and manage per-region Azure Storage account quota increases, including limits, prerequisites, and support request steps. |

### Limits & Quotas
| Topic | URL |
|-------|-----|
| Increase Azure Storage account quota per region | https://learn.microsoft.com/en-us/azure/quotas/storage-account-quota-requests |