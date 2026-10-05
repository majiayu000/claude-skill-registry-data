---
name: ini2xml
description: Use when converting INI-style configuration files into XML for downstream EDirect or XML-based processing.
disable-model-invocation: true
user-invocable: true
---

# ini2xml

## Quick Start

- Command: `ini2xml < config.ini > config.xml`
- Local executable: `/home/vimalinx/miniforge3/envs/bio/bin/ini2xml`
- Full reference: `references/help.md`

## When To Use This Tool

- Convert section/key-value configuration files into XML.
- Normalize lightweight INI metadata before feeding it into XML-centric tooling.
- Bridge configuration snippets into the same XML-oriented inspection workflow used by the rest of EDirect.

## Common Patterns

```bash
# 1) Convert an INI file into XML
ini2xml < config.ini > config.xml
```

```bash
# 2) Convert and inspect the resulting hierarchy quickly
ini2xml < config.ini | sed -n '1,40p'
```

## Recommended Workflow

1. Make sure the source file follows a normal section/key-value INI layout.
2. Run `ini2xml` through stdin redirection or a pipe.
3. Confirm the output hierarchy matches the source sections and keys.
4. Use the XML with downstream `xtract` or XML-side converters as needed.

## Guardrails

- This wrapper simply runs `transmute -i2x`, so `transmute` must be on `PATH`.
- The installed wrapper does not expose a meaningful `--help` / `--version` response.
- Prefer stdin/pipes over relying on undocumented positional-file behavior.
- In practice the converter emits a `<ConfigFile>` root, so check downstream expectations if you need a different top-level tag.
