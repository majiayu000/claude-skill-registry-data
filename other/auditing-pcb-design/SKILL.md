---
name: auditing-pcb-design
description: Runs KiCad DRC/ERC checks, exports gerbers and BOM, and generates a structured findings report. Use when reviewing PCB designs, running design rule checks, or preparing manufacturing outputs.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Bash, Glob, Grep
  argument-hint: [kicad-project-path]
  stability: stable
  content-hash: sha256:9555a45ff552da34c27b43cc8037cc7101d3054816b547b92974e30a02430775
  last-verified-cc-version: 1.0.34
---

# PCB Design Audit

**Target**: $ARGUMENTS

Run KiCad design rule checks and export manufacturing outputs.

## References (MUST READ)

Read these before proceeding:

- `references/kicad-cli-reference.md` — DRC/ERC commands, JSON output schema, gerber/BOM export

## Workflow

1. **Detect kicad-cli** — Verify `kicad-cli` is available, report version
2. **Find project files** — Glob for `*.kicad_pro`, `*.kicad_sch`, `*.kicad_pcb`
3. **Run ERC** on schematic:

   ```bash
   kicad-cli sch erc --output erc-report.json --format json <schematic.kicad_sch>
   ```

4. **Run DRC** on PCB:

   ```bash
   kicad-cli pcb drc --output drc-report.json --format json <pcb.kicad_pcb>
   ```

5. **Parse JSON reports** — Categorize violations by severity (error/warning/exclusion)
6. **If clean** (no errors), export manufacturing outputs:
   - Gerbers: `kicad-cli pcb export gerbers --output gerbers/ <pcb.kicad_pcb>`
   - Drill: `kicad-cli pcb export drill --output gerbers/ <pcb.kicad_pcb>`
   - BOM: `kicad-cli sch export bom --output bom.csv <schematic.kicad_sch>`
7. **Generate findings report** at `docs/pcb-audit-report.md`

## Output Format

```markdown
# PCB Audit Report: <Project Name>

## Tool Version
kicad-cli <version>

## ERC Results
- Errors: N
- Warnings: N
  - <violation description> @ <sheet:component>

## DRC Results
- Errors: N
- Warnings: N
  - <violation description> @ <coordinates>

## Manufacturing Outputs
- [ ] Gerbers exported to gerbers/
- [ ] Drill files exported to gerbers/
- [ ] BOM exported to bom.csv

## Recommendations
...
```

## Rules

- Never export gerbers if DRC has unresolved errors
- Report all warnings even if they are excluded in KiCad
- Include exact coordinates/references for every DRC/ERC finding
- Do not modify KiCad project files — this is a read-only audit
