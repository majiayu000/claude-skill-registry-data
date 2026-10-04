---
name: azure-copilot
description: Expert knowledge for Azure Copilot development including troubleshooting, decision making, architecture & design patterns, security, configuration, and integrations & coding patterns. Use when sizing VMs, generating Bicep/Terraform, configuring Cosmos DB storage, or debugging App Service/VM disks, and other Azure Copilot related development tasks. Not for Azure AI services (use microsoft-foundry-tools), Azure Machine Learning (use azure-machine-learning), Azure AI Search (use azure-cognitive-search), Azure AI Bot Service (use azure-bot-service).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Copilot Skill

This skill provides expert guidance for Azure Copilot. Covers troubleshooting, decision making, architecture & design patterns, security, configuration, and integrations & coding patterns. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: Use the **Category Index** below to locate relevant sections. For categories with line ranges (e.g., `L35-L120`), use `read_file` with the specified lines. For categories with file links (e.g., `[security.md](security.md)`), use `read_file` on the linked reference file

This skill requires **network access** to fetch documentation content:
- **Preferred**: Use `mcp_microsoftdocs:microsoft_docs_fetch`. Returns Markdown.
- **Fallback**: Use `WebFetch`. Returns Markdown.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Troubleshooting | L30-L35 | Using Copilot to diagnose and resolve Azure App Service/Functions issues and analyze Azure VM disk performance problems, including slow I/O and bottlenecks. |
| Decision Making | L36-L44 | Using Copilot to compare options and make cost‑efficient Azure decisions: VM sizing, workload templates, Marketplace offers, storage estate insights, and Load Balancer SKU selection. |
| Architecture & Design Patterns | L45-L49 | Using Copilot to design, validate, and troubleshoot Azure network architectures, including connectivity, routing, security, and performance issues across VNets and hybrid setups. |
| Security | L50-L58 | Security and access control for Azure Copilot: storage hardening, user/tenant access, agent access policies, attack surface insights, and responsible AI/data use. |
| Configuration | L59-L63 | How to set up and configure Azure Cosmos DB as the storage backend for Azure Copilot conversation data, including required settings and integration steps. |
| Integrations & Coding Patterns | L64-L69 | Using Azure Copilot to generate and refine infra-as-code and automation: APIM policies, Azure CLI/PowerShell scripts, Kubernetes YAML for AKS, and Terraform/Bicep templates. |

### Troubleshooting
| Topic | URL |
|-------|-----|
| Troubleshoot Azure App Service and Functions with Copilot | https://learn.microsoft.com/en-us/azure/copilot/troubleshoot-app-service |
| Troubleshoot Azure VM disk performance using Copilot | https://learn.microsoft.com/en-us/azure/copilot/troubleshoot-disk-performance |

### Decision Making
| Topic | URL |
|-------|-----|
| Use Azure Copilot to analyze and optimize cloud costs | https://learn.microsoft.com/en-us/azure/copilot/analyze-cost-management |
| Choose and deploy cost-efficient Azure VMs with Copilot | https://learn.microsoft.com/en-us/azure/copilot/deploy-vms-effectively |
| Find and deploy workload templates using Azure Copilot | https://learn.microsoft.com/en-us/azure/copilot/deploy-workload-templates |
| Find suitable Azure Marketplace solutions with Copilot | https://learn.microsoft.com/en-us/azure/copilot/discover-marketplace |
| Select and manage Azure Load Balancer SKUs with Copilot | https://learn.microsoft.com/en-us/azure/copilot/work-load-balancer |

### Architecture & Design Patterns
| Topic | URL |
|-------|-----|
| Design and troubleshoot Azure networks with Copilot | https://learn.microsoft.com/en-us/azure/copilot/copilot-networking |

### Security
| Topic | URL |
|-------|-----|
| Improve and migrate Azure storage accounts with Copilot | https://learn.microsoft.com/en-us/azure/copilot/improve-storage-accounts |
| Manage user access and authorization for Azure Copilot | https://learn.microsoft.com/en-us/azure/copilot/manage-access |
| Control tenant access to Azure Copilot agents preview | https://learn.microsoft.com/en-us/azure/copilot/manage-agents-preview |
| Query Defender EASM attack surface insights with Azure Copilot | https://learn.microsoft.com/en-us/azure/copilot/query-attack-surface |
| Understand responsible AI and data use in Azure Copilot | https://learn.microsoft.com/en-us/azure/copilot/responsible-ai-faq |

### Configuration
| Topic | URL |
|-------|-----|
| Configure Cosmos DB storage for Azure Copilot conversations | https://learn.microsoft.com/en-us/azure/copilot/bring-your-own-storage |

### Integrations & Coding Patterns
| Topic | URL |
|-------|-----|
| Author Azure API Management policies using Copilot | https://learn.microsoft.com/en-us/azure/copilot/author-api-management-policies |
| Generate Kubernetes YAML for AKS with Azure Copilot | https://learn.microsoft.com/en-us/azure/copilot/generate-kubernetes-yaml |
| Create Terraform and Bicep configurations with Azure Copilot | https://learn.microsoft.com/en-us/azure/copilot/generate-terraform-bicep |