---
name: azure-payment-hsm
description: Expert knowledge for Azure Payment Hsm development including troubleshooting, best practices, decision making, architecture & design patterns, security, and configuration. Use when configuring Payment HSM VNets/FastPath, payShield Manager access, HA/DR topologies, SKUs, or traffic inspection, and other Azure Payment Hsm related development tasks. Not for Azure Dedicated HSM (use azure-dedicated-hsm), Azure Cloud Hsm (use azure-cloud-hsm), Azure Key Vault (use azure-key-vault), Azure Information Protection (use azure-information-protection).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Payment Hsm Skill

This skill provides expert guidance for Azure Payment Hsm. Covers troubleshooting, best practices, decision making, architecture & design patterns, security, and configuration. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: Use the **Category Index** below to locate relevant sections. For categories with line ranges (e.g., `L35-L120`), use `read_file` with the specified lines. For categories with file links (e.g., `[security.md](security.md)`), use `read_file` on the linked reference file

This skill requires **network access** to fetch documentation content:
- **Preferred**: Use `mcp_microsoftdocs:microsoft_docs_fetch`. Returns Markdown.
- **Fallback**: Use `WebFetch`. Returns Markdown.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Troubleshooting | L30-L34 | Diagnosing and resolving common Azure Payment HSM deployment issues, including provisioning failures, configuration problems, and known platform limitations or workarounds. |
| Best Practices | L35-L39 | Guidance on inspecting, monitoring, and routing network traffic to Azure Payment HSM, including using firewalls, NSGs, and network appliances for secure traffic control. |
| Decision Making | L40-L45 | Guidance on choosing/changing Azure Payment HSM performance SKUs, and understanding support options, roles, and responsibilities for operating the service. |
| Architecture & Design Patterns | L46-L51 | Designing Azure Payment HSM architectures: HA/DR patterns, device lifecycle management, supported topologies, deployment constraints, and planning resilient HSM solutions. |
| Security | L52-L58 | Security setup for Payment HSM: configuring SSH/payShield manager access, understanding compliance certifications/scope, and applying hardening and security best practices. |
| Configuration | L59-L70 | Configuring Azure Payment HSM networking and access: VNets/peering, FastPath, ARM/CLI deployment, IP layout (split/reused VNets), provider registration, and payShield Manager browser access. |

### Troubleshooting
| Topic | URL |
|-------|-----|
| Resolve known issues with Azure Payment HSM deployments | https://learn.microsoft.com/en-us/azure/payment-hsm/known-issues |

### Best Practices
| Topic | URL |
|-------|-----|
| Inspect and route network traffic for Azure Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/inspect-traffic |

### Decision Making
| Topic | URL |
|-------|-----|
| Select and change Azure Payment HSM performance SKUs | https://learn.microsoft.com/en-us/azure/payment-hsm/change-performance-level |
| Use Azure Payment HSM support and understand responsibilities | https://learn.microsoft.com/en-us/azure/payment-hsm/support-guide |

### Architecture & Design Patterns
| Topic | URL |
|-------|-----|
| Design high availability and DR for Azure Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/deployment-scenarios |
| Plan solution topologies and constraints for Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/solution-design |

### Security
| Topic | URL |
|-------|-----|
| Configure SSH access to Azure Payment HSM payShield manager | https://learn.microsoft.com/en-us/azure/payment-hsm/access-payshield-manager-ssh |
| Understand Payment HSM compliance certifications and scope | https://learn.microsoft.com/en-us/azure/payment-hsm/certification-compliance |
| Apply security best practices to Azure Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/secure-payment-hsm |

### Configuration
| Topic | URL |
|-------|-----|
| Configure browser access to payShield Manager for Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/access-payshield-manager |
| Configure Payment HSM IPs in different VNets via ARM | https://learn.microsoft.com/en-us/azure/payment-hsm/create-different-ip-addresses |
| Configure Azure Payment HSM across separate VNets | https://learn.microsoft.com/en-us/azure/payment-hsm/create-different-vnet |
| Deploy Payment HSM with split VNets via ARM template | https://learn.microsoft.com/en-us/azure/payment-hsm/create-different-vnet-template |
| Configure FastPathEnabled feature flag and tag for Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/fastpathenabled |
| Configure VNet peering and fastpath for Payment HSM | https://learn.microsoft.com/en-us/azure/payment-hsm/peer-vnets |
| Manage Azure Payment HSM resources with Azure CLI | https://learn.microsoft.com/en-us/azure/payment-hsm/quickstart-cli |
| Register Azure Payment HSM resource providers and features | https://learn.microsoft.com/en-us/azure/payment-hsm/register-payment-hsm-resource-providers |
| Reuse existing virtual networks for Azure Payment HSM deployment | https://learn.microsoft.com/en-us/azure/payment-hsm/reuse-vnet |