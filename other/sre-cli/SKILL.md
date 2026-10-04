---
name: reverse-engineer
description: |
  Authorized software reverse engineering, binary analysis, and program comprehension for legitimate purposes including security review, interoperability, migration, modernization, debugging, and documentation.
  
  USE WHEN: user needs to analyze software they own or have explicit authorization to inspect, including legacy systems, internal applications, binaries for debugging/migration, malware analysis for defense, API/protocol discovery, or understanding undocumented software.
  
  COVERS: source code analysis, binary/executable analysis, mobile apps (APK/IPA), web apps, firmware, databases, configuration extraction, architecture reconstruction, and behavior mapping.
  
  DOES NOT: assist with cracking, DRM bypass, unauthorized access, credential theft, or any illegal activities.
---

# Reverse Engineer Skill

## Authorization Checkpoint

**STOP: Verify authorization before proceeding.**

Only assist with reverse engineering when:
- Software is owned by the user
- Internal company applications with permission
- Legacy systems authorized for inspection/migration
- Security research with proper scope/authorization
- Interoperability under applicable law

**Refuse requests involving:**
- Cracking licenses, DRM, paywalls, activation systems
- Bypassing authentication or access controls
- Malware development or stealth techniques
- Credential theft or data exfiltration
- Evading detection or violating terms of service

---

## First Response Protocol

When user provides a target, immediately produce:

1. **Target Classification** - Type, platform, suspected stack
2. **Investigation Plan** - Prioritized analysis sequence
3. **Recommended Tools** - Specific to this target
4. **Python Automation** - Relevant bundled scripts
5. **First Actions** - Commands/scripts to run
6. **Expected Outputs** - What we'll learn
7. **Risk/Legal Note** - Authorization reminder

---

## Workspace Setup

Run `scripts/init_workspace.py` to create:

```
/reverse_engineering_workspace
  /input          - Original artifacts (read-only)
  /copies         - Working copies
  /extracted      - Unpacked contents
  /strings        - String extractions
  /traffic        - Network captures
  /screenshots    - Visual documentation
  /notes          - Investigation log
  /scripts        - Automation scripts
  /reports        - Generated reports
  /artifacts      - Intermediate findings
  /timelines      - Event sequences
```

---

## Investigation Workflow

### Phase 1: Initial Discovery (Non-destructive)
1. **File inventory** - `scripts/file_inventory.py`
2. **Type identification** - magic numbers, headers
3. **String extraction** - `scripts/strings_extractor.py`
4. **Entropy analysis** - `scripts/entropy_scanner.py` (detect packing)
5. **Format-specific headers** - PE/ELF/Mach-O parsing

### Phase 2: Static Analysis
1. **Disassembly** - Function identification, CFG
2. **Decompilation** - C-like pseudocode where available
3. **Import/Export analysis** - API dependencies
4. **String clustering** - Categorize extracted strings
5. **Configuration extraction** - Parse embedded configs

### Phase 3: Dynamic Analysis (Sandboxed only)
1. **Behavior observation** - Sandboxed execution
2. **API monitoring** - System call tracing
3. **Network capture** - Traffic analysis
4. **Memory analysis** - Runtime state inspection

### Phase 4: Documentation
1. **Architecture reconstruction** - Component diagram
2. **Data flow mapping** - Information flow
3. **Report generation** - `scripts/report_generator.py`

---

## Tool Selection

### Python Libraries (pip install)
Core: `pip install pwntools angr capstone lief pefile pyelftools python-magic`
Mobile: `pip install androguard frida-tools`
Network: `pip install scapy mitmproxy`
Bindings: `pip install r2pipe pyghidra`

See [references/tool_installation.md](references/tool_installation.md) for full details.

### External Tools by Target Type

| Target | Primary Tools | Secondary Tools |
|--------|---------------|-----------------|
| Windows PE | Ghidra, x64dbg | IDA Pro, PEiD, Resource Hacker |
| Linux ELF | Ghidra, GDB | Radare2, strace, ltrace |
| macOS Mach-O | Ghidra, LLDB | Hopper, class-dump |
| Android APK | JADX, APKTool | Androguard, MobSF |
| iOS IPA | Frida, class-dump | objection |
| Firmware | Binwalk, Ghidra | ImHex, QEMU |
| Web App | Browser DevTools, mitmproxy | Burp Suite |

---

## Output Format

Use this structure for every analysis step:

```markdown
## Goal
[What we're trying to learn]

## Evidence Available
[Artifacts/data at hand]

## Approach
[Methodology]

## Tools Needed
[Specific tools]

## Commands / Python Scripts
[Executable commands]

## Findings
[What was discovered]

## Confidence
[High/Medium/Low + justification]

## Risks / Unknowns
[Limitations, gaps]

## Next Step
[Logical follow-up]
```

---

## Bundled Scripts

| Script | Purpose |
|--------|---------|
| `scripts/init_workspace.py` | Create workspace structure |
| `scripts/file_inventory.py` | Generate artifact inventory with hashes |
| `strings_extractor.py` | Extract and cluster strings |
| `pe_analyzer.py` | Windows PE analysis |
| `elf_analyzer.py` | Linux ELF analysis |
| `macho_analyzer.py` | macOS Mach-O analysis |
| `entropy_scanner.py` | Detect packed/encrypted sections |
| `report_generator.py` | Generate analysis reports |

---

## Target-Specific Workflows

See [references/analysis_workflows.md](references/analysis_workflows.md) for detailed workflows:
- Windows PE executables
- Linux ELF binaries
- macOS applications
- Android APKs
- iOS IPAs
- Firmware images
- Web applications
- Database files

---

## Reference Materials

- [tool_installation.md](references/tool_installation.md) - Setup guides per platform
- [analysis_workflows.md](references/analysis_workflows.md) - Target-specific workflows
- [pe_format.md](references/pe_format.md) - PE format reference
- [elf_format.md](references/elf_format.md) - ELF format reference
- [report_templates.md](references/report_templates.md) - Report templates

---

## Deliverables Checklist

Maintain these outputs throughout analysis:

- [ ] Executive Summary (what software does, stack, findings)
- [ ] Artifact Inventory (files, hashes, types)
- [ ] Architecture Reconstruction (components, boundaries, flows)
- [ ] Behavior Notes (startup, auth, data persistence)
- [ ] Reverse Engineering Log (timestamped actions)
- [ ] Open Questions (unknowns, unresolved paths)
- [ ] Final Report (technical, engineer-ready)

---

## Special Handling

### Packed/Obfuscated Binaries
1. Identify packer signature
2. Explain analysis limitations
3. Suggest sandboxed dynamic analysis
4. Do NOT provide unpacking instructions for protected software

### Malware Analysis
1. Emphasize isolated/sandboxed environment
2. Focus on defensive IOCs
3. Never assist with weaponization

### Encrypted Binaries
1. Document encryption presence
2. Explain static analysis limitations
3. Recommend dynamic approaches
4. Never help break copy protection
