---
name: deserialization-parser-review
description: "Reviews parsers, deserialization, uploads, archives, YAML/JSON/XML/pickle, paths, templates, SSRF, and unsafe loaders."
---

# Deserialization Parser Review

Review parser and loader attack surfaces.

## Workflow

1. Identify all attacker-controlled bytes, paths, URLs, archive entries, and
   structured documents.
2. Trace into parser, loader, resolver, filesystem, network, or command use.
3. Check safe loader modes, size limits, recursion/decompression limits, path
   normalization, symlink handling, and schema validation.
4. Validate exploitability or mark proof gaps.
5. Recommend a minimal defensive change.

## Output

- input source
- parser/loader sink
- control weakness
- exploit path
- mitigation
- validation plan

## Rule

Do not claim a parser bug from library reputation alone. Tie the concern to how
this repo uses the parser.
