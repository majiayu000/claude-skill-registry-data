---
name: wiztree
description: "Analyze disk usage with WizTree, export storage-audit CSVs, and troubleshoot NTFS scan behavior."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["wiztree", "ntfs-mft-parser", "disk-space-analyzer", "treemap-storage", "wiztree-cli", "storage-audit", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# WizTree Disk Space Analyzer & MFT Engine AI Skill Guide (Claude)

## Overview & Engine Architecture
Antibody Software WizTree is a high-speed disk space visualizer and storage diagnostics utility for Microsoft Windows. Operating by directly parsing raw **NTFS Master File Table (`$MFT`)** binary streams bypassing standard Win32 file enumeration APIs, WizTree indexes millions of files across terabyte drives in under 2 seconds. The platform generates interactive **Treemap visual partitions**, supports non-NTFS fallback scans, and provides rich command-line automation (**`wiztree64.exe`**) for silent CSV storage auditing. Claude operates as a Principal Windows Storage Systems Architect and Disk Analytics Specialist, specializing in **WizTree headless CLI automation**, **MFT permission diagnostics**, **storage report aggregation pipelines**, and **automated enterprise disk reclamation**.

### WizTree Engine Architecture & MFT Direct Scan Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 WizTree Engine Architecture                 │
│                                                             │
│  User Interface & Visual Treemap Tier                       │
│  ├── Color-Coded Interactive Treemap Visualizer             │
│  ├── File Extension Breakdown Grid (Space & File Count)     │
│  └── Top 1000 Largest Files Enumerator Viewport             │
│                                                             │
│  MFT Parser & Disk Scanning Core                            │
│  ├── Direct Raw `$MFT` Binary Parser (Physical Volume Read) │
│  ├── Non-NTFS / Network Share Fallback Scanner (Win32 API)  │
│  └── Multi-Threaded In-Memory Directory Tree Aggregator     │
│                                                             │
│  Command Line & Export Automation Subsystem                 │
│  ├── Headless Batch Export Engine (`/export="...csv"`)      │
│  ├── Filter Engine (`/filter="*.log;*.iso"`, `/sortby=1`)   │
│  └── Settings Store (`%APPDATA%\WizTree\WizTree.ini`)       │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Headless CSV Storage Audit Automation**: Author Python and PowerShell scripts invoking `wiztree64.exe` with `/export` and `/admin=1` to generate comprehensive CSV storage catalogs without user interaction.
2. **Automated Storage Triage & Aggregation**: Build analytical pipelines parsing WizTree CSV outputs to group disk usage by top directories, identify duplicate ISO/VMDK images, and locate stale log archives.
3. **MFT Permission & Elevation Triage**: Remediate `$MFT` access failures by ensuring scripts and executables request `SeManageVolumePrivilege` and run under elevated Administrator security tokens.
4. **Automated Enterprise Drive Cleanup Routines**: Script targeted storage remediation deleting identified orphaned temporary files (`*.tmp`, `*.dmp`, `node_modules`, `AppData\Local\Temp`).

---

## Production Python Automation: Headless WizTree Storage Auditor & CSV Parser

Save this script as `audit_disk_storage.py` (requires WizTree installed at default path):

```python
"""
WizTree Automated Disk Storage Auditor & Reporter
Executes WizTree in headless batch mode, exports CSV report, and aggregates top disk consumers.
"""

import sys
import os
import subprocess
import pandas as pd

WIZTREE_EXE = r"C:\Program Files\WizTree\wiztree64.exe"

def run_storage_audit(drive_letter: str = "C:", output_csv: str = "C:\\Temp\\disk_audit.csv"):
    print(f"--- [INITIALIZING WIZTREE DISK STORAGE AUDIT: {drive_letter}] ---")

    if not os.path.exists(WIZTREE_EXE):
        print(f"🚨 Error: WizTree executable not found at: {WIZTREE_EXE}")
        return

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # 1. Execute WizTree Headless Batch Scan & Export
    print(f"Executing direct MFT scan on {drive_letter} -> Exporting to {output_csv}...")
    cmd = [
        WIZTREE_EXE,
        drive_letter,
        f"/export={output_csv}",
        "/admin=1",
        "/sortby=1" # Sort by size descending
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"🚨 WizTree CLI returned error code: {res.returncode}")
        return

    print("✅ MFT scan and CSV export completed.")

    # 2. Parse and Aggregate CSV Report
    if not os.path.exists(output_csv):
        print("🚨 Error: Output CSV was not generated.")
        return

    print("\n--- [TOP DISK CONSUMERS ANALYSIS] ---")
    try:
        # WizTree CSV columns: "File Name", "Size", "Allocated", "Modified", "Attributes", "Files", "Folders"
        df = pd.read_csv(output_csv, encoding="utf-8", on_bad_lines="skip")

        # Convert size to GB
        df["Size_GB"] = df["Size"] / (1024**3)

        # Filter top files
        files_df = df[df["Folders"] == 0].sort_values(by="Size", ascending=False)
        print(f"Top 5 Largest Individual Files on {drive_letter}:")
        for idx, row in files_df.head(5).iterrows():
            print(f"• [{row['Size_GB']:>6.2f} GB] {row['File Name']}")

        # Group by File Extension
        print("\nTop 5 Largest Storage Allocations by File Extension:")
        df["Ext"] = df["File Name"].apply(lambda x: os.path.splitext(str(x))[1].lower())
        ext_summary = df.groupby("Ext")["Size_GB"].sum().sort_values(ascending=False)
        for ext, size_gb in ext_summary.head(5).items():
            if ext:
                print(f"• {ext:<10}: {size_gb:>8.2f} GB total")

        print("\n✅ Storage analysis completed successfully.")

    except Exception as e:
        print(f"Failed to analyze CSV: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "C:"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "C:\\Temp\\WizTree_Report.csv"
    run_storage_audit(target, out_file)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **WizTree Shows "Access Denied" on Scanning Drive** | Process running without Administrator elevation, preventing raw NTFS `$MFT` access. | Launch WizTree with Administrator privileges or pass `/admin=1` in the CLI command. |
| **Network Drive (SMB/NFS) Scans Slowly** | Network shares do not expose raw physical `$MFT` streams and fall back to Win32 directory traversal. | Allow the standard directory walk to complete or execute WizTree locally on the file server host. |
| **Exported CSV Contains Garbled Non-Latin Characters** | CSV exported with ANSI encoding instead of UTF-8 on international filenames. | In WizTree *Options $\rightarrow$ Export*, ensure **UTF-8 Export Encoding** is enabled. |
| **Treemap View Stutters on Large Array of Small Files** | Rendering millions of tiny file bounding boxes exceeding GDI canvas limits. | In WizTree Options $\rightarrow$ Treemap, increase the **Minimum file size to display** threshold (e.g. $\ge 1\text{MB}$). |

---

## Command Line Syntax & WizTree Recipes

```bash
# 1. Export Entire Drive Storage Report to CSV via Elevated CLI
"C:\Program Files\WizTree\wiztree64.exe" C: /export="C:\Reports\C_Drive.csv" /admin=1

# 2. Export Filtered File List (Only ISO and VMDK files larger than 1GB)
"C:\Program Files\WizTree\wiztree64.exe" D: /export="D:\LargeMedia.csv" /filter="*.iso;*.vmdk" /admin=1

# 3. Dump Raw Master File Table (MFT) for Forensics Analysis
"C:\Program Files\WizTree\wiztree64.exe" C: /dumpmft="C:\Forensics\C_MFT.bin" /admin=1
```

### Essential File Locations
- **Application Binary**: `C:\Program Files\WizTree\wiztree64.exe`
- **Configuration**: `%APPDATA%\WizTree\WizTree.ini`

---

## Agent Operational Directive
> **MANDATORY**: When executing WizTree from command-line scripts, always append `/admin=1` to ensure direct access to the raw NTFS `$MFT` stream for instant sub-second drive scans.
