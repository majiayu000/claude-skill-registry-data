---
name: docling-mcp-skill
description: >-
  Docling reference and workflows — layout-aware extraction for complex tables,
  multi-column, scanned PDFs where markitdown fails. CLI and MCP tiers, consent
  policy. Triggers: docling, scanned PDF OCR, markitdown insufficient.
license: Apache-2.0
compatibility: opencode
metadata:
  pattern: cli-on-demand
category: Configuration
---

## What this skill does

- Documents **docling** as a Tier 2 escalation engine for the AGENTS.md → Office Document Extraction Routing rule
- Provides the **CLI-on-demand recipe** (primary path — codegraph-init analog): detect, ask consent, install, convert, read
- Documents the **optional persistent MCP tier** via `--enable-pack docling`
- States the **trust-boundary honestly**: unlike markitdown (zero phone-home), docling downloads ML models from huggingface.co on first use
- Prescribes the **consent policy**: primary asks; headless/subagent soft-fails; never auto-install ~3-4 GB

**Reference:** [docling on PyPI](https://pypi.org/project/docling/) · [docling-mcp on PyPI](https://pypi.org/project/docling-mcp/)

## When to use docling (Tier 2)

Follow the **AGENTS.md → Office Document Extraction Routing** rule — this skill does NOT re-derive the full markitdown/pdf-specialist tree. Docling is the escalation target when:

- markitdown returns **empty/garbage** (scanned PDFs, image-only)
- markitdown **mangles complex tables** (multi-column, merged cells, nested headers)
- markitdown **drops layout** that matters (multi-column text flow, footnotes, sidebars)
- The PDF needs **OCR** (docling's OCR pipeline handles scanned docs markitdown cannot)

Do NOT use docling for: plain text dumps of clean born-digital docs (markitdown is faster, lighter), visual understanding (image-analyzer-subagent), or structured form-field extraction (pdf-specialist-skill).

## CLI-on-demand recipe (primary path)

This is the codegraph-init analog — docling is **not installed by default** (~3-4 GB with models). The agent detects absence, asks consent, installs, converts — all within the session, no restart.

```
1. DETECT:  command -v docling >/dev/null 2>&1
2. ABSENT → ASK CONSENT (primary session only — see Consent Policy below)
3. INSTALL: pip install --user docling
4. CONVERT: docling convert <file> --to md -o <output-dir>
5. READ:    Read the generated <output-dir>/<file>.md
```

### Consent Policy

| Context | Behavior |
|---------|----------|
| **Primary session (interactive)** | Ask consent via `question` before installing (~3-4 GB + ~hundreds of MB models on first convert). Never auto-install. Harness binding (§Portability contract): OpenCode `question` · Claude Code `AskUserQuestion` · Other/none — ask in a plain reply; no answer → treat as declined and soft-fail per the Headless row. |
| **Subagent** | Subagents cannot ask — return the consent request in the Return Contract as a `Questions for the user` field. The primary agent relays it. |
| **Headless / CI** | Soft-fail to markitdown's best-effort output. Log that docling escalation was skipped (not installed, non-interactive). Never block the pipeline. |

**Never silently install 3-4 GB.** The consent prompt is mandatory in any interactive context.

### First-convert note

The `pip install` is fast, but the **first `docling convert`** downloads ML models (~hundreds of MB) from huggingface.co. Subsequent converts use the cached models. Set expectations: "install + first convert takes a few minutes."

## Persistent MCP recipe (optional Tier 2)

For users who want docling always available without per-session CLI installs:

```bash
./deploy/setup.sh --enable-pack docling
```

This installs `docling-mcp[local]` (the MCP server wrapper) and sets `mcp.servers.docling.disabled: false` + appends the `permissions` rule `{ "action": "docling*", "resource": "*", "effect": "allow" }` in `opencode.json`. After an opencode restart, `docling*` tools register and are callable directly.

Use the MCP tier when: you process complex/scanned PDFs regularly and want zero per-session friction. Use CLI-on-demand when: you only need it occasionally and don't want a persistent 3-4 GB dependency.

## Trust Boundary (honest)

Unlike markitdown (which is **zero phone-home** — fully local conversion), docling:

- **Downloads ML models from `huggingface.co`** on first use (OCR models, table recognition models, layout models)
- Uses `torch` + `rapidocr` + huggingface transformers as transitive dependencies
- Sets `DOCLING_CONVERSION_MODE=local` to prevent accidental remote API calls (conversion stays local after models are cached)

**Mitigations:**
- Model download is **one-time** — cached in `~/.cache/huggingface/` after first convert
- `DOCLING_CONVERSION_MODE=local` is hard-set in both the MCP config and recommended CLI usage
- No document content leaves the machine (only model weights are fetched, once)

If your organization blocks huggingface.co or requires air-gapped operation, pre-download models or do not use docling.

## Version Pinning

Pin `docling>=2.0,<3.0` (mirrors markitdown's `<0.2` discipline). Version bumps may introduce new OCR engines or model changes that shift the trust boundary — a major version bump requires a trust-boundary re-audit documented in this skill.

## Fallback Strategy

If docling is unavailable (not installed, consent declined, huggingface.co blocked):

1. Accept markitdown's best-effort output (may be empty/garbage for scanned PDFs)
2. For scanned/image-only PDFs: `pdftoppm` (bash) → `image-analyzer-subagent` (visual understanding, not structured text)
3. For structured data: `pdf-specialist-skill` (purpose-built for forms/tables)

These fallbacks are **inferior to docling** for layout-aware extraction but are zero-install.
