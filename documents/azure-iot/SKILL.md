---
name: azure-iot
description: Expert knowledge for Azure IoT development including decision making, architecture & design patterns, and integrations & coding patterns. Use when using MQTT/IoT Plug and Play, DPS/IoT Hub, SAP ERP integration, industrial IoT architectures, or device schemas, and other Azure IoT related development tasks. Not for Azure IoT Hub (use azure-iot-hub), Azure IoT Edge (use azure-iot-edge), Azure IoT Central (use azure-iot-central), Azure Defender For Iot (use azure-defender-for-iot).
compatibility: Requires network access. Uses mcp_microsoftdocs:microsoft_docs_fetch or WebFetch to retrieve documentation.
user-invocable: false
---
# Azure IoT Skill

This skill provides expert guidance for Azure IoT. Covers decision making, architecture & design patterns, and integrations & coding patterns. It combines local quick-reference content with remote documentation fetching capabilities.

## How to Use This Skill

> **IMPORTANT for Agent**: Use the **Category Index** below to locate relevant sections. For categories with line ranges (e.g., `L35-L120`), use `read_file` with the specified lines. For categories with file links (e.g., `[security.md](security.md)`), use `read_file` on the linked reference file

This skill requires **network access** to fetch documentation content:
- **Preferred**: Use `mcp_microsoftdocs:microsoft_docs_fetch`. Returns Markdown.
- **Fallback**: Use `WebFetch`. Returns Markdown.

## Category Index

| Category | Lines | Description |
|----------|-------|-------------|
| Decision Making | L27-L32 | Guidance on designing Azure Device Registry namespaces and schema registries, including structure, organization, and planning for IoT device data models and metadata. |
| Architecture & Design Patterns | L33-L38 | Reference architectures and patterns for industrial IoT on Azure, including dataspace-based designs, component choices, and end-to-end implementation guidance for industrial scenarios. |
| Integrations & Coding Patterns | L39-L42 | Patterns and code for integrating devices via MQTT and IoT Plug and Play, building device/service apps, formatting payloads, using DPS/IoT Hub, and connecting SAP ERP to Azure IoT. |

### Decision Making
| Topic | URL |
|-------|-----|
| Design and choose Azure Device Registry namespaces | https://learn.microsoft.com/en-us/azure/iot/iot-device-registry-namespace-guidance |
| Plan Azure Device Registry schema registries for IoT | https://learn.microsoft.com/en-us/azure/iot/iot-device-registry-schema-registry-guidance |

### Architecture & Design Patterns
| Topic | URL |
|-------|-----|
| Enable industrial dataspace architectures on Azure | https://learn.microsoft.com/en-us/azure/iot/howto-iot-industrial-dataspaces |
| Implement Azure industrial IoT reference architecture | https://learn.microsoft.com/en-us/azure/iot/tutorial-iot-industrial-solution-architecture |

### Integrations & Coding Patterns
| Topic | URL |
|-------|-----|
| Connect on-premises SAP ERP to Azure industrial IoT | https://learn.microsoft.com/en-us/azure/iot/howto-connect-on-premises-sap-to-azure |