---
name: azure-osconfig
description: Expert knowledge for Azure Osconfig development including troubleshooting, security, configuration, and integrations & coding patterns. Use when running OSConfig via IoT for commands/networking, SSH Posture Control, agent health, or Windows security baselines, and other Azure Osconfig related development tasks. Not for Azure Update Manager (use azure-update-manager), Azure Automation (use azure-automation), Azure Policy (use azure-policy).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Osconfig Skill

This skill provides expert guidance for Azure Osconfig. Covers troubleshooting, security, configuration, and integrations & coding patterns. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: Use the **Category Index** below to locate relevant sections. For categories with line ranges (e.g., `L35-L120`), use `read_file` with the specified lines. For categories with file links (e.g., `[security.md](security.md)`), use `read_file` on the linked reference file

This skill requires **network access** to fetch documentation content:
- **Preferred**: Use `mcp_microsoftdocs:microsoft_docs_fetch`. Returns Markdown.
- **Fallback**: Use `WebFetch`. Returns Markdown.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Troubleshooting | L28-L32 | Diagnosing OSConfig agent status and connectivity issues when using Azure IoT Hub, including checking logs, health, and troubleshooting deployment or reporting problems. |
| Security | L33-L39 | Configuring Windows security with OSConfig: App Control for Business policies, Windows Server 2025 security baselines, and applying CIS benchmarks to Azure Windows Server. |
| Configuration | L40-L45 | Tracking OSConfig breaking changes over time and configuring/standardizing sshd settings across fleets using SSH Posture Control. |
| Integrations & Coding Patterns | L46-L58 | Patterns for using OSConfig with Azure IoT to run custom commands, manage Linux networking, firewall, packages, hostnames, reboots, and report device/OS hardware info. |

### Troubleshooting
| Topic | URL |
|-------|-----|
| Diagnose OSConfig status when using Azure IoT Hub | https://learn.microsoft.com/en-us/azure/osconfig/howto-troubleshoot |

### Security
| Topic | URL |
|-------|-----|
| Configure App Control for Business policies via OSConfig | https://learn.microsoft.com/en-us/azure/osconfig/osconfig-how-to-configure-app-control-for-business |
| Configure Windows Server 2025 security baselines with OSConfig | https://learn.microsoft.com/en-us/azure/osconfig/osconfig-how-to-configure-security-baselines |
| Apply CIS security benchmarks to Azure Windows Server | https://learn.microsoft.com/en-us/azure/osconfig/overview-cis-benchmarks-windows-server |

### Configuration
| Topic | URL |
|-------|-----|
| Track major OSConfig breaking changes over time | https://learn.microsoft.com/en-us/azure/osconfig/concept-majorchanges |
| Manage sshd configuration fleetwide with SSH Posture Control | https://learn.microsoft.com/en-us/azure/osconfig/ssh-brownfield-mc |

### Integrations & Coding Patterns
| Topic | URL |
|-------|-----|
| Use OSConfig CommandRunner for custom device commands | https://learn.microsoft.com/en-us/azure/osconfig/concept-commandrunner |
| Implement custom configuration and reporting with OSConfig CommandRunner | https://learn.microsoft.com/en-us/azure/osconfig/howto-customconfigreport |
| Report device hardware and OS info with OSConfig | https://learn.microsoft.com/en-us/azure/osconfig/howto-deviceinfo |
| Manage Linux host firewall using OSConfig and Azure IoT | https://learn.microsoft.com/en-us/azure/osconfig/howto-firewall |
| Manage OS hostnames using OSConfig and Azure IoT | https://learn.microsoft.com/en-us/azure/osconfig/howto-hostname |
| Control /etc/hosts content with OSConfig and Azure IoT | https://learn.microsoft.com/en-us/azure/osconfig/howto-hosts |
| Configure Linux network settings via OSConfig and Azure IoT | https://learn.microsoft.com/en-us/azure/osconfig/howto-network |
| Manage Linux package manager through OSConfig and Azure IoT | https://learn.microsoft.com/en-us/azure/osconfig/howto-pmc |
| Trigger device reboot and shutdown via OSConfig and Azure IoT | https://learn.microsoft.com/en-us/azure/osconfig/howto-rebootshutdown |
| Run Azure IoT Hub queries for OSConfig-enabled devices | https://learn.microsoft.com/en-us/azure/osconfig/quickstart-useful-queries |