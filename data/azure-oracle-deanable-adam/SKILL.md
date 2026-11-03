---
name: azure-oracle
description: Expert knowledge for Azure Oracle development including troubleshooting, security, configuration, and integrations & coding patterns. Use when configuring Oracle Database@Azure connectivity, TDE with Key Vault, VNet topology, or Exadata logs to Sentinel, and other Azure Oracle related development tasks. Not for Azure SQL Database (use azure-sql-database), Azure SQL Managed Instance (use azure-sql-managed-instance), SQL Server on Azure Virtual Machines (use azure-sql-virtual-machines), SAP HANA on Azure Large Instances (use azure-sap).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Oracle Skill

This skill provides expert guidance for Azure Oracle. Covers troubleshooting, security, configuration, and integrations & coding patterns. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: This file may be large. Use the **Category Index** below to locate relevant sections, then use `read_file` with specific line ranges (e.g., `L136-L144`) to read the sections needed for the user's question
This skill requires **network access** to fetch documentation content.
Use `mcp_microsoftdocs:microsoft_docs_fetch` to retrieve full articles.
- **Fallback**: Use the built-in `WebFetch` tool if the Microsoft Learn MCP server is not available.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Troubleshooting | L26-L30 | Operational FAQs and fixes for common Oracle Database@Azure issues, including connectivity, performance, deployment, configuration, and known platform limitations. |
| Security | L32-L35 | Configuring Oracle Transparent Data Encryption (TDE) to use Azure Key Vault, including key management, integration steps, and security best practices. |
| Configuration | L37-L41 | Onboarding Oracle Database@Azure, required prerequisites, and designing secure virtual network topologies (subnets, connectivity, routing) for Oracle DB deployments in Azure. |
| Integrations & Coding Patterns | L43-L46 | Configuring Oracle Exadata log collection and pipelines into Azure Monitor and Microsoft Sentinel for monitoring, analytics, and security SIEM/SOAR use cases. |

### Troubleshooting
| Topic | URL |
|-------|-----|
| Answer operational FAQs for Oracle Database@Azure | https://learn.microsoft.com/en-us/azure/oracle/oracle-db/faq-oracle-database-azure |
| Resolve common Oracle Database@Azure known issues | https://learn.microsoft.com/en-us/azure/oracle/oracle-db/oracle-database-known-issues |

### Security
| Topic | URL |
|-------|-----|
| Configure Oracle TDE keys with Azure Key Vault | https://learn.microsoft.com/en-us/azure/oracle/oracle-db/manage-oracle-transparent-data-encryption-azure-key-vault |

### Configuration
| Topic | URL |
|-------|-----|
| Configure onboarding for Oracle Database@Azure deployments | https://learn.microsoft.com/en-us/azure/oracle/oracle-db/onboard-oracle-database |
| Plan Oracle Database@Azure virtual network topology | https://learn.microsoft.com/en-us/azure/oracle/oracle-db/oracle-database-network-plan |

### Integrations & Coding Patterns
| Topic | URL |
|-------|-----|
| Integrate Oracle Exadata logs with Azure Monitor and Sentinel | https://learn.microsoft.com/en-us/azure/oracle/oracle-db/oracle-exadata-database-dedicated-infrastructure-logs |
