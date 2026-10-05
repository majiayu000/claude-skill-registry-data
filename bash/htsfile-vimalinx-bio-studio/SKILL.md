---
name: htsfile
description: Use when you need to identify, view, or copy HTS-format files (BAM, CRAM, VCF, BCF). Use for inspecting file headers or viewing textual representations of binary HTS files.
disable-model-invocation: true
user-invocable: true
---

# htsfile

## Quick Start
- **Command:** `htsfile [OPTIONS] FILE...`
- **Local executable:** `/home/vimalinx/miniforge3/envs/bio/bin/htsfile`
- **Version:** 1.22.1
- **Full reference:** See `references/help.md` for complete options and usage details

## When To Use This Tool

- Quickly identify whether a file is BAM, CRAM, VCF, BCF, or another HTSlib-supported format.
- View the text form or just the header of a binary HTS file.
- Debug “what format is this file actually?” problems before using heavier tools.
- Use it as a lightweight probe, not a full analysis step.

## Common Patterns

```bash
# 1) Identify file type
htsfile sample.bam
```

```bash
# 2) Show only the header
htsfile -c -h sample.bam
```

```bash
# 3) View textual representation
htsfile -c sample.bcf
```

```bash
# 4) Copy exact contents
htsfile --copy sample.bam sample.copy.bam
```

## Recommended Workflow

1. Use `htsfile` first when file-type confusion is blocking the workflow.
2. Switch to `samtools` or `bcftools` once the file type is confirmed.
3. Use header-only viewing when you just need metadata and not the full text dump.
4. Keep it as a diagnostic helper in scripts that need early format validation.

## Guardrails
- `--copy` is a dedicated mode and requires one source plus one destination.
- `-h` and `-H` mean opposite things in view mode.
- `htsfile` is for inspection and diagnosis, not rich editing or filtering.
- Text view of large files can be enormous, so prefer header-only mode when possible.

## Guardrails
- The `--copy` subcommand requires exactly one source FILE and one DESTFILE
- Options `-h` (header-only) and `-H` (no-header) have opposite effects in view mode
- Verbosity increases with `-v`; use for additional diagnostics and warnings
