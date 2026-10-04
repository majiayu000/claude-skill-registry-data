---
name: azure-bastion
description: Expert knowledge for Azure Bastion development including best practices, decision making, architecture & design patterns, limits & quotas, security, configuration, and integrations & coding patterns. Use when configuring Bastion for AKS private clusters, VM scale sets, Entra ID auth, hub/spoke VNets, or native SSH/RDP clients, and other Azure Bastion related development tasks. Not for Azure Virtual Network (use azure-virtual-network), Azure Virtual Machines (use azure-virtual-machines), Azure VPN Gateway (use azure-vpn-gateway), Azure Firewall (use azure-firewall).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Bastion Skill

This skill provides expert guidance for Azure Bastion. Covers best practices, decision making, architecture & design patterns, limits & quotas, security, configuration, and integrations & coding patterns. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: Use the **Category Index** below to locate relevant sections. For categories with line ranges (e.g., `L35-L120`), use `read_file` with the specified lines. For categories with file links (e.g., `[security.md](security.md)`), use `read_file` on the linked reference file

This skill requires **network access** to fetch documentation content:
- **Preferred**: Use `mcp_microsoftdocs:microsoft_docs_fetch`. Returns Markdown.
- **Fallback**: Use `WebFetch`. Returns Markdown.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Best Practices | L31-L35 | Guidance on reducing Azure Bastion costs through sizing, scaling, and usage patterns while maintaining secure remote access and compliance best practices. |
| Decision Making | L36-L42 | Guidance on choosing and upgrading Bastion SKU tiers and using IP-based Bastion connections across VNets, subscriptions, and environments. |
| Architecture & Design Patterns | L43-L49 | Architectural options and patterns for Azure Bastion: hub/spoke and peered VNets, private-only deployments, network/topology design, and deployment guidance for secure remote access. |
| Limits & Quotas | L50-L54 | Configuring Azure Bastion host scaling limits, including max concurrent RDP/SSH sessions, connection thresholds, and how to adjust or plan capacity for different SKUs. |
| Security | L55-L61 | Configuring secure Azure Bastion access: Entra ID authentication, required NSG rules, and hardening best practices to lock down Bastion hosts and connections. |
| Configuration | L62-L73 | Configuring Azure Bastion settings, auth (Kerberos), monitoring/metrics/logs, native client access, session management, recording, and shareable links for secure RDP/SSH access |
| Integrations & Coding Patterns | L74-L81 | How to use Azure Bastion with AKS private clusters, VM scale sets, and native Windows/Linux clients, including SSH/RDP connectivity patterns and file transfer via Bastion native clients. |

### Best Practices
| Topic | URL |
|-------|-----|
| Optimize Azure Bastion costs without reducing security | https://learn.microsoft.com/en-us/azure/bastion/cost-optimization |

### Decision Making
| Topic | URL |
|-------|-----|
| Select the appropriate Azure Bastion SKU tier | https://learn.microsoft.com/en-us/azure/bastion/bastion-sku-comparison |
| Use Azure Bastion IP-based connections across environments | https://learn.microsoft.com/en-us/azure/bastion/connect-ip-address |
| View and upgrade Azure Bastion SKU tiers safely | https://learn.microsoft.com/en-us/azure/bastion/upgrade-sku |

### Architecture & Design Patterns
| Topic | URL |
|-------|-----|
| Understand Azure Bastion deployment architectures | https://learn.microsoft.com/en-us/azure/bastion/design-architecture |
| Design and deploy private-only Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/private-only-deployment |
| Use Azure Bastion with VNet peering architectures | https://learn.microsoft.com/en-us/azure/bastion/vnet-peering |

### Limits & Quotas
| Topic | URL |
|-------|-----|
| Configure Azure Bastion host scaling limits | https://learn.microsoft.com/en-us/azure/bastion/configure-host-scaling |

### Security
| Topic | URL |
|-------|-----|
| Configure Microsoft Entra ID auth for Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/bastion-entra-id-authentication |
| Configure Azure Bastion NSG rules for secure access | https://learn.microsoft.com/en-us/azure/bastion/bastion-nsg |
| Harden and secure your Azure Bastion deployment | https://learn.microsoft.com/en-us/azure/bastion/secure-bastion |

### Configuration
| Topic | URL |
|-------|-----|
| Azure Bastion configuration settings and options | https://learn.microsoft.com/en-us/azure/bastion/configuration-settings |
| Configure Kerberos authentication for Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/kerberos-authentication-portal |
| Configure monitoring and diagnostics for Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/monitor-bastion |
| Reference monitoring metrics and logs for Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/monitor-bastion-reference |
| Configure Azure Bastion for native client access | https://learn.microsoft.com/en-us/azure/bastion/native-client |
| Monitor and manage active Azure Bastion sessions | https://learn.microsoft.com/en-us/azure/bastion/session-monitoring |
| Configure and use Azure Bastion session recording | https://learn.microsoft.com/en-us/azure/bastion/session-recording |
| Create and use Azure Bastion shareable links | https://learn.microsoft.com/en-us/azure/bastion/shareable-link |

### Integrations & Coding Patterns
| Topic | URL |
|-------|-----|
| Connect to AKS private clusters via Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/bastion-connect-to-aks-private-cluster |
| Connect to VM scale sets using Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/bastion-connect-vm-scale-set |
| Connect from Linux native clients through Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/connect-vm-native-client-linux |
| Connect from Windows native clients through Azure Bastion | https://learn.microsoft.com/en-us/azure/bastion/connect-vm-native-client-windows |
| Transfer files via Azure Bastion native clients | https://learn.microsoft.com/en-us/azure/bastion/vm-upload-download-native |