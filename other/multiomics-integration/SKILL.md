---
name: multiomics_integration
description: "Multi-Omics Integration - Integrate transcriptomics (TCGA), proteomics (UniProt), pathway enrichment (STRING), and metabolic pathway (KEGG) data for a target gene. Outputs a unified JSON report combining expression profiles, protein annotations, enriched pathways, and KEGG pathway details."
license: MIT license
metadata:
    skill-author: PJLab
---

# Multi-Omics Integration

**Discipline**: Multi-Omics | **Tools Used**: 4 | **Servers**: 4

## Description

For a given gene (e.g. TP53), this skill integrates four layers of omics data:
1. **Transcriptomics** — gene expression across cancer types (TCGA)
2. **Proteomics** — protein structure, function, and annotations (UniProt)
3. **Pathway Enrichment** — functional enrichment analysis (STRING)
4. **Metabolic Pathway** — detailed KEGG pathway information

The final output is a structured JSON report containing all four layers.

## Tool Descriptions

### Tool 1: `get_gene_expression_across_cancers` (Origene-TCGA)

```
Analyze tissue-specific expression of a gene across cancer types.

Server: https://scp.intern-ai.org.cn/api/v1/mcp/11/Origene-TCGA
Args:
    gene (str, required): Gene symbol (e.g., "TP53", "BRCA1", "EGFR")
Returns:
    High/low expression cancer types with z-scores, mean expression values,
    and sample counts per cancer type.
```

### Tool 2: `get_uniprotkb_entry_by_accession` (Origene-UniProt)

```
Retrieve all data associated with a UniProtKB entry by accession ID.

Server: https://scp.intern-ai.org.cn/api/v1/mcp/10/Origene-UniProt
Args:
    accession (str, required): UniProtKB accession ID (e.g., "P04637" for TP53)
Returns:
    Complete protein entry including: protein names, gene names, organism,
    sequence, function annotations, subcellular location, post-translational
    modifications, disease associations, cross-references.
```

### Tool 3: `get_functional_enrichment` (Origene-STRING)

```
Retrieve functional enrichment (GO, KEGG, Pfam, InterPro) for a protein set.

Server: https://scp.intern-ai.org.cn/api/v1/mcp/6/Origene-STRING
Args:
    identifiers (array of str, required): Gene/protein identifiers (e.g., ["TP53", "MDM2"])
    species (int, required): NCBI taxonomy ID (e.g., 9606 for human)
    background_string_identifiers (str, required): Background protein set for
        enrichment statistics. Use empty string "" for whole-genome background.
Returns:
    List of enriched terms with: term name, category (GO/KEGG/Pfam/etc.),
    p-value, FDR, description, and which input proteins match.
```

### Tool 4: `kegg_get` (Origene-KEGG)

```
Retrieve KEGG database entries in flat file format.

Server: https://scp.intern-ai.org.cn/api/v1/mcp/5/Origene-KEGG
Args:
    dbentries (str, required): KEGG entry identifier(s). Examples:
        - "hsa04115" (p53 signaling pathway)
        - "hsa:7157" (TP53 gene entry)
        - Multiple entries separated by "+"
    option (str, required): Output format. Use "" for default flat file, or:
        "aaseq" (amino acid), "ntseq" (nucleotide), "mol", "kcf",
        "image", "kgml" (XML), "json"
Returns:
    KEGG entry data in the specified format. Flat file includes:
    pathway name, description, gene members, compounds, references.
```

## Workflow

1. **Get transcriptomic data** — Query TCGA for gene expression across cancers
2. **Get proteomic data** — Query UniProt for protein annotations
3. **Run pathway enrichment** — Use STRING to find enriched functional terms for the gene
4. **Get metabolic pathway details** — Retrieve the relevant KEGG pathway entry

**Data Flow:**
- Steps 1 & 2 provide foundational omics data for the target gene/protein
- Step 3 uses the same gene identifier to find enriched pathways
- Step 4 retrieves detailed information for the target pathway (e.g., hsa04115 = p53 signaling)

## Test Case

### Input
```json
{
    "gene": "TP53",
    "accession": "P04637",
    "pathway": "hsa04115"
}
```

### Expected Output
A JSON report file `TP53_multiomics_report.json` containing:
- `transcriptomics`: Expression data across cancer types (non-empty)
- `proteomics`: UniProt protein entry with sequence and annotations
- `enrichment`: List of enriched functional terms (GO, KEGG, etc.)
- `kegg_pathway`: p53 signaling pathway details

### Success Criteria
1. All four tools return non-empty, parseable data
2. Step 1 result relates to the queried gene (TP53)
3. Step 2 result contains the queried accession (P04637)
4. Step 3 returns at least one enriched term
5. Step 4 returns pathway information containing "p53"

## Agent Instructions

> **Important for AI agents executing this skill:**
>
> - **Do NOT copy or modify this script.** Call the MCP tools directly with the parameters shown in Tool Descriptions.
> - If a tool returns an error, **check the parameter names and types** against the Tool Descriptions above — do not rewrite the workflow.
> - The workflow is **complete** when all four steps return non-empty data and the JSON report is saved. Stop execution at that point.
> - If a tool is temporarily unavailable (network error), retry up to 2 times before reporting failure.

## Usage Example

> **Note:** Replace `<YOUR_SCP_HUB_API_KEY>` with your own SCP Hub API Key. You can obtain one from the [SCP Platform](https://scphub.intern-ai.org.cn/).

```python
import asyncio
import json
from datetime import datetime
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# ══════════════════════════════════════════════════════════════
# Configuration
# ══════════════════════════════════════════════════════════════

API_KEY = "<YOUR_SCP_HUB_API_KEY>"

SERVERS = {
    "tcga": "https://scp.intern-ai.org.cn/api/v1/mcp/11/Origene-TCGA",
    "uniprot": "https://scp.intern-ai.org.cn/api/v1/mcp/10/Origene-UniProt",
    "string": "https://scp.intern-ai.org.cn/api/v1/mcp/6/Origene-STRING",
    "kegg": "https://scp.intern-ai.org.cn/api/v1/mcp/5/Origene-KEGG",
}

# Input parameters
GENE = "TP53"
ACCESSION = "P04637"
PATHWAY = "hsa04115"

# ══════════════════════════════════════════════════════════════
# MCP Client
# ══════════════════════════════════════════════════════════════

class OrigeneClient:
    def __init__(self, server_url: str, api_key: str):
        self.server_url = server_url
        self.api_key = api_key
        self.session = None

    async def connect(self):
        try:
            self.transport = streamablehttp_client(
                url=self.server_url,
                headers={"SCP-HUB-API-KEY": self.api_key}
            )
            self.read, self.write, _ = await self.transport.__aenter__()
            self.session_ctx = ClientSession(self.read, self.write)
            self.session = await self.session_ctx.__aenter__()
            await self.session.initialize()
            return True
        except Exception as e:
            print(f"[ERROR] Connection failed for {self.server_url}: {e}")
            return False

    async def disconnect(self):
        try:
            if self.session:
                await self.session_ctx.__aexit__(None, None, None)
            if hasattr(self, 'transport'):
                await self.transport.__aexit__(None, None, None)
        except Exception:
            pass

    def parse_result(self, result):
        """Parse MCP tool result into Python object."""
        if isinstance(result, dict):
            content_list = result.get("content") or []
        else:
            content_list = getattr(result, "content", []) or []
        texts = []
        for item in content_list:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(item.get("text") or "")
            else:
                if getattr(item, "type", None) == "text":
                    texts.append(getattr(item, "text", "") or "")
        raw = "".join(texts)
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw

# ══════════════════════════════════════════════════════════════
# Workflow
# ══════════════════════════════════════════════════════════════

async def main():
    report = {
        "query": {"gene": GENE, "accession": ACCESSION, "pathway": PATHWAY},
        "timestamp": datetime.now().isoformat(),
        "steps": {}
    }

    # ── Step 1: Transcriptomics (TCGA) ──────────────────────
    print(f"[Step 1] Querying TCGA for {GENE} expression across cancers...")
    tcga = OrigeneClient(SERVERS["tcga"], API_KEY)
    if not await tcga.connect():
        report["steps"]["transcriptomics"] = {"error": "Connection failed"}
    else:
        result = await tcga.session.call_tool(
            "get_gene_expression_across_cancers",
            arguments={"gene": GENE}
        )
        data = tcga.parse_result(result)
        report["steps"]["transcriptomics"] = data
        await tcga.disconnect()

        if data and not isinstance(data, str):
            print(f"  [OK] Received expression data for {GENE}")
        else:
            print(f"  [WARN] Unexpected response format: {str(data)[:200]}")

    # ── Step 2: Proteomics (UniProt) ────────────────────────
    print(f"[Step 2] Querying UniProt for accession {ACCESSION}...")
    uniprot = OrigeneClient(SERVERS["uniprot"], API_KEY)
    if not await uniprot.connect():
        report["steps"]["proteomics"] = {"error": "Connection failed"}
    else:
        result = await uniprot.session.call_tool(
            "get_uniprotkb_entry_by_accession",
            arguments={"accession": ACCESSION}
        )
        data = uniprot.parse_result(result)
        report["steps"]["proteomics"] = data
        await uniprot.disconnect()

        if data and not isinstance(data, str):
            print(f"  [OK] Retrieved protein entry for {ACCESSION}")
        else:
            print(f"  [WARN] Unexpected response format: {str(data)[:200]}")

    # ── Step 3: Pathway Enrichment (STRING) ─────────────────
    # Uses the same gene identifier from input
    print(f"[Step 3] Running STRING functional enrichment for [{GENE}]...")
    string = OrigeneClient(SERVERS["string"], API_KEY)
    if not await string.connect():
        report["steps"]["enrichment"] = {"error": "Connection failed"}
    else:
        result = await string.session.call_tool(
            "get_functional_enrichment",
            arguments={
                "identifiers": [GENE],
                "species": 9606,
                "background_string_identifiers": ""
            }
        )
        data = string.parse_result(result)
        report["steps"]["enrichment"] = data
        await string.disconnect()

        if isinstance(data, list) and len(data) > 0:
            print(f"  [OK] Found {len(data)} enriched terms")
        elif isinstance(data, dict) and data:
            print(f"  [OK] Enrichment data received")
        else:
            print(f"  [WARN] Unexpected response: {str(data)[:200]}")

    # ── Step 4: KEGG Pathway Details ────────────────────────
    print(f"[Step 4] Retrieving KEGG pathway {PATHWAY}...")
    kegg = OrigeneClient(SERVERS["kegg"], API_KEY)
    if not await kegg.connect():
        report["steps"]["kegg_pathway"] = {"error": "Connection failed"}
    else:
        result = await kegg.session.call_tool(
            "kegg_get",
            arguments={"dbentries": PATHWAY, "option": ""}
        )
        data = kegg.parse_result(result)
        report["steps"]["kegg_pathway"] = data
        await kegg.disconnect()

        if data and "p53" in str(data).lower():
            print(f"  [OK] Retrieved p53 signaling pathway")
        elif data:
            print(f"  [OK] Retrieved pathway data")
        else:
            print(f"  [WARN] Empty response for {PATHWAY}")

    # ── Save Report ─────────────────────────────────────────
    output_file = f"{GENE}_multiomics_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    print(f"\n{'='*60}")
    print(f"Multi-omics integration complete!")
    print(f"Report saved: {output_file}")
    print(f"{'='*60}")

    # ── Final Validation ────────────────────────────────────
    steps = report["steps"]
    success = all([
        steps.get("transcriptomics") and "error" not in str(steps.get("transcriptomics", "")),
        steps.get("proteomics") and "error" not in str(steps.get("proteomics", "")),
        steps.get("enrichment") and "error" not in str(steps.get("enrichment", "")),
        steps.get("kegg_pathway") and "error" not in str(steps.get("kegg_pathway", "")),
    ])
    if success:
        print("[PASS] All 4 omics layers successfully integrated.")
    else:
        print("[FAIL] Some steps encountered errors. Check the report.")
    return success

if __name__ == "__main__":
    asyncio.run(main())
```
