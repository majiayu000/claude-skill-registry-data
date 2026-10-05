---
name: asn2xml
description: Use when converting NCBI-style ASN.1 payloads into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# asn2xml

## Quick Start

- **Command**: `asn2xml < input.asn > output.xml`
- **Local executable**: `/home/vimalinx/miniforge3/envs/bio/bin/asn2xml`
- **Full reference**: See [references/help.md](references/help.md) for complete documentation

## When To Use This Tool

- Convert ASN.1 records into XML so they can be inspected with `xtract` or other XML tooling.
- Bridge older NCBI / EDirect data representations into the XML-centric parts of a pipeline.
- Normalize ASN.1 content before storing or diffing records in text-oriented workflows.

## Common Patterns

```bash
# 1) Convert an ASN.1 record to XML
asn2xml < record.asn > record.xml
```

```bash
# 2) Convert and inspect selected fields immediately
asn2xml < record.asn | xtract -pattern "*" -element "*" | sed -n '1,20p'
```

## Recommended Workflow

1. Start with a representative ASN.1 payload from the upstream source you actually use.
2. Run `asn2xml` through stdin redirection or a pipe.
3. Validate that non-empty XML is produced before batching larger jobs.
4. Pass the XML to `xtract`, `xml2json`, or other downstream converters as needed.

## Guardrails

- This is a thin wrapper around `transmute -a2x`, so the companion `transmute` binary must also be on `PATH`.
- The current build does not expose a real `--help` or `--version` interface.
- Prefer stdin redirection or pipes; positional-argument behavior is not documented by the wrapper itself.
- Unsupported or malformed ASN.1 can result in empty output rather than a friendly format-specific error message.
