---
name: encase
description: "Automate authorized EnCase forensic workflows with EnScript, E01/Ex01 evidence files, and Evidence Processor jobs."
category: digital-forensics
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["encase", "enscript", "digital-forensics", "e01-format", "ex01", "incident-response", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# OpenText EnCase Forensic AI Skill Guide (Claude)

## Overview & Engine Architecture
OpenText EnCase Forensic is the industry-standard court-validated digital investigation and eDiscovery software suite. EnCase operates on **Expert Witness File Formats (`.E01` / `.Ex01` with AES-256 encryption)**, utilizes the **EnCase Evidence Processor (EEP)** for automated artifact ingestion, and provides an object-oriented C++-like scripting language (**EnScript**). Claude operates as an Enterprise Forensics Specialist and EnScript Developer, specializing in **chain-of-custody cryptographic integrity**, **EnScript automation**, **compound file parsing (PST/OST/ZIP/VHD)**, and **remote enterprise endpoint triage via SAFE agents**.

### EnCase Enterprise Architecture & Processing Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 EnCase Forensic Architecture                │
│                                                             │
│  Evidence Acquisition & Integrity Layer                     │
│  ├── E01 / Ex01 Container (MD5/SHA1 Checksums per Chunk)    │
│  ├── Hardware Write-Blocker Integration (Tableau / FastBloc)│
│  └── SAFE Remote Network Endpoint Acquisition Engine        │
│                                                             │
│  Processing & Automation Stack                              │
│  ├── EnCase Evidence Processor (EEP - Registry, LNK, EVTX)  │
│  ├── EnScript Object Model Engine (EntryClass, BookmarkClass│
│  └── Indexed Search Engine (Full Unicode Stemming)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **EnScript Code Authoring**: Write clean, object-oriented EnScript programs implementing `MainClass` and recursive `EntryClass` iterators to automate evidence tagging, search regexes, and export routines.
2. **Cryptographic Chain of Custody**: Verify acquisition hashes vs verification hashes across multi-segment E01 chunk sets (`.E01`, `.E02`, ..., `.E99`), diagnosing CRC32 block corruption.
3. **EnCase Evidence Processor Optimization**: Configure EEP priority passes (File Signature Analysis, Protected File Analysis, Internet Artifacts) to prevent pipeline hangs on multi-terabyte evidence pools.
4. **Registry & Artifact Reconstruction**: Script the extraction of User Assist, Shimcache (AppCompatCache), and Amcache records from mounted logical images.

---

## Production EnScript Automation: Suspicious Execution & LNK File Harvester

Save this script as `ExtractLNKArtifacts.EnScript` and compile inside the EnCase EnScript Editor:

```csharp
// EnScript: Recursive LNK Shortcut & Evidence Bookmark Harvester
class MainClass {
  void Main(CaseClass c) {
    if (!c) {
      SystemClass::Message(SystemClass::MB_ICONEXCLAMATION, "Error", "No case currently open in EnCase.");
      return;
    }

    BookmarkClass rootBookmark = c.BookmarkRoot();
    BookmarkClass targetFolder();
    targetFolder.SetName("Suspicious LNK Shortcuts");
    rootBookmark.AddFolder(targetFolder);

    uint matchCount = 0;

    // Traverse all evidence items in case
    for (ItemIteratorClass iter(c); ItemClass item = iter.GetNextItem();) {
      EntryClass entry = EntryClass::List(item);
      if (entry) {
        ProcessEntry(entry, targetFolder, matchCount);
      }
    }

    SystemClass::Message(SystemClass::MB_ICONINFORMATION, "Complete", 
      String::Format("Completed scan. Tagged {0} LNK files.", matchCount));
  }

  void ProcessEntry(EntryClass entry, BookmarkClass targetFolder, uint &matchCount) {
    // Check if extension is .lnk
    if (entry.Extension().Compare("lnk") == 0) {
      BookmarkClass newBm();
      newBm.SetName(entry.Name());
      newBm.SetComment(String::Format("Logical Size: {0} bytes | Path: {1}", entry.LogicalSize(), entry.FullPath()));
      targetFolder.AddChild(newBm);
      matchCount++;
    }

    // Recurse child directories
    for (EntryClass child = entry.FirstChild(); child; child = child.Next()) {
      ProcessEntry(child, targetFolder, matchCount);
    }
  }
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Evidence Verification Fails: `Hash Mismatch` on E01** | One or more `.E01`, `.E02` segment files in the multi-part evidence volume suffered silent bit rot or network transfer truncation. | 1. Calculate MD5 for every individual `.E0x` file against acquisition manifest.<br>2. Run `ewfinfo disk.E01` (Linux) to check block-level CRC integrity.<br>3. Re-transfer damaged segment using verify-enabled protocol (`robocopy /Z`). |
| **EnScript Fails Compilation: `Type Mismatch / Unknown Class`** | EnScript API breaking changes between EnCase v7/v8 and v21/v22 (e.g. `EntryClass` methods renamed). | 1. Open EnScript in EnCase built-in IDE $\rightarrow$ Press `F7` to compile.<br>2. Replace deprecated types with modern equivalents.<br>3. Consult the *EnScript Language Reference Guide* for active version headers. |
| **Evidence Processor Freezes at 99% during Compound Parsing** | Corrupted multi-gigabyte Outlook PST/OST database or encrypted 7z archive trapped in infinite extraction loop. | 1. In EEP Options $\rightarrow$ *File Types*, uncheck deeply nested compound file extraction for unallocated space.<br>2. Set maximum compound extraction depth to 3 levels. |
| **SAFE Network Agent Connection Timeout** | Target endpoint blocked TCP Port 443/8000 or EnCase SAFE certificate expired. | 1. Verify endpoint firewall allows outbound TLS to EnCase Server.<br>2. Renew and push updated root certificate authority to target endpoints. |

---

## Command Line Syntax & Utilities

```bash
# 1. Inspect E01 Forensic Image Metadata & Hashes via libewf
ewfinfo "C:\Evidence\Workstation_Image.E01"

# 2. Mount E01 Image as Raw Device on Linux Host
ewfmount "C:\Evidence\Workstation_Image.E01" /mnt/ewf/

# 3. Acquire Physical Drive into E01 using Linux CLI
ewfacquire -t evidence_disk -S 2G /dev/nvme0n1
```

### Essential File Locations
- **EnScript User Folder**: `%USERPROFILE%\Documents\EnCase\EnScripts`
- **EnCase User Config**: `%APPDATA%\EnCase\EnCase 22`
- **Global Config Path**: `C:\Program Files\OpenText\EnCase\Config`

---

## Agent Operational Directive
> **MANDATORY**: Always verify and match both acquisition and verification hashes (MD5 / SHA-1) in forensic reports. When authoring EnScripts, ensure memory-safe recursive tree traversal with bounds checking.
