---
name: frmr-analysis
description: Analyzes FedRAMP FRMR documents to extract control mappings, KSI entries, and version changes. Use when the user asks about FedRAMP requirements, control mappings, compliance data, or needs to understand FRMR document content.
---

When analyzing FRMR documents:

1. Identify the document type (KSI, MAS, VDR, SCN, FRD, ADS, CCM, FSI, ICP, PVA, RSC, UCM)
2. Extract control mappings between NIST SP 800-53 and FedRAMP requirements
3. Identify Key Security Indicators (KSI) when relevant
4. Highlight significant changes between document versions
5. Map controls to specific compliance requirements
6. Provide citations to specific FRMR sections and item IDs

Use the fedramp-docs MCP server tools:
- `list_frmr_documents` to enumerate available documents
- `get_frmr_document` to retrieve full document content
- `list_ksi` to filter KSI requirements
- `list_controls` to get control mappings
- `diff_frmr` to compare document versions
