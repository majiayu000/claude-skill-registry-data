---
name: azure-relay
description: Expert knowledge for Azure Relay development including troubleshooting, security, configuration, and integrations & coding patterns. Use when configuring Hybrid Connections, WCF relays, Entra ID/SAS auth, Private Link, or .NET/Node.js Relay clients, and other Azure Relay related development tasks. Not for Azure Service Bus (use azure-service-bus), Azure Event Hubs (use azure-event-hubs), Azure Web PubSub (use azure-web-pubsub), Azure Application Gateway (use azure-application-gateway).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure Relay Skill

This skill provides expert guidance for Azure Relay. Covers troubleshooting, security, configuration, and integrations & coding patterns. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: This file may be large. Use the **Category Index** below to locate relevant sections, then use `read_file` with specific line ranges (e.g., `L136-L144`) to read the sections needed for the user's question
This skill requires **network access** to fetch documentation content.
Use `mcp_microsoftdocs:microsoft_docs_fetch` to retrieve full articles.
- **Fallback**: Use the built-in `WebFetch` tool if the Microsoft Learn MCP server is not available.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Troubleshooting | L26-L29 | Diagnosing and fixing common Azure Relay exceptions, including connection, authentication, quota, and configuration errors, with guidance on causes and resolutions. |
| Security | L31-L39 | Authentication and network security for Azure Relay: Entra ID and SAS auth, managed identities, IP firewall, virtual network rules, and Private Link Service configuration. |
| Configuration | L41-L44 | Network and firewall requirements for Azure Relay, including which ports/protocols to open for Hybrid Connections and WCF relays and how to configure them. |
| Integrations & Coding Patterns | L46-L51 | Using Azure Relay Hybrid Connections from .NET and Node.js (WebSockets), plus low-level protocol details for implementing custom clients and integrations |

### Troubleshooting
| Topic | URL |
|-------|-----|
| Resolve common Azure Relay exceptions | https://learn.microsoft.com/en-us/azure/azure-relay/relay-exceptions |

### Security
| Topic | URL |
|-------|-----|
| Authenticate applications to Azure Relay with Entra ID | https://learn.microsoft.com/en-us/azure/azure-relay/authenticate-application |
| Use managed identities to access Azure Relay | https://learn.microsoft.com/en-us/azure/azure-relay/authenticate-managed-identity |
| Configure IP firewall rules for Azure Relay | https://learn.microsoft.com/en-us/azure/azure-relay/ip-firewall-virtual-networks |
| Configure network security for Azure Relay | https://learn.microsoft.com/en-us/azure/azure-relay/network-security |
| Secure Azure Relay with Private Link Service | https://learn.microsoft.com/en-us/azure/azure-relay/private-link-service |
| Configure SAS and Entra ID auth for Azure Relay | https://learn.microsoft.com/en-us/azure/azure-relay/relay-authentication-and-authorization |

### Configuration
| Topic | URL |
|-------|-----|
| Configure required port settings for Azure Relay | https://learn.microsoft.com/en-us/azure/azure-relay/relay-port-settings |

### Integrations & Coding Patterns
| Topic | URL |
|-------|-----|
| Use Azure Relay Hybrid Connections .NET APIs | https://learn.microsoft.com/en-us/azure/azure-relay/relay-hybrid-connections-dotnet-api-overview |
| Use Azure Relay Node.js WebSocket APIs | https://learn.microsoft.com/en-us/azure/azure-relay/relay-hybrid-connections-node-ws-api-overview |
| Implement Azure Relay Hybrid Connections protocol | https://learn.microsoft.com/en-us/azure/azure-relay/relay-hybrid-connections-protocol |
