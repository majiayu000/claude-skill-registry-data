---
name: horos
description: "Configure Horos DICOM and PACS workflows, automate DCMTK transfers, and troubleshoot plugins without interpreting clinical findings."
category: medical
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["horos", "dicom-viewer", "pacs-networking", "pynetdicom", "c-store", "medical-imaging", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Horos Open-Source DICOM Viewer AI Skill Guide (Claude)

## Overview & Engine Architecture
Horos is a 64-bit open-source medical imaging and DICOM workstation for macOS, derived from the OsiriX foundation. Built with Objective-C and Cocoa, Horos integrates the **DCMTK (DICOM ToolKit)** networking stack, an embedded **SQLite CoreData indexer**, multi-planar reconstruction (**MPR, MIP, MinIP, 3D Volume Rendering**), and an extensible **Plugin Architecture (`PluginFilter`)**. Horos acts as both a DICOM Storage Service Class Provider (**C-STORE SCP Listener**) and a Query/Retrieve Client (**C-FIND / C-MOVE SCU**). Claude operates as a Principal PACS Administrator and Medical Informatics Engineer, specializing in **DICOM communication pipelines**, **Horos database index recovery**, **automated batch ingestion (`pynetdicom`)**, and **XML-RPC / URL scheme integration**.

### Horos PACS & Visualization Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Horos System Architecture                   │
│                                                             │
│  Presentation & Multi-Planar Visualization                  │
│  ├── 2D DICOM Viewport (Window/Level, ROIs, Cine Loop)      │
│  ├── 3D Post-Processing (MPR, Maximum Intensity Projection) │
│  └── 3D Surface / Volume Rendering & Endoscopy Navigation   │
│                                                             │
│  DICOM Networking & Protocol Layer (DCMTK)                  │
│  ├── C-STORE SCP Daemon (Background Ingestion Listener:11112│
│  ├── C-FIND & C-MOVE SCU (PACS Query & Retrieve Engine)     │
│  └── DICOM TLS 1.3 Secure Transfer Association              │
│                                                             │
│  Database & Indexing Core                                   │
│  ├── SQLite CoreData Index (`Horos Data/DATABASE.noindex/`) │
│  └── Objective-C Plugin SDK (`PluginFilter.h`) & XML-RPC IPC│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **DICOM Networking & PACS Automation**: Author Python scripts using `pynetdicom` to verify DICOM connectivity (`C-ECHO`) and dispatch medical imaging series (`C-STORE`) to Horos listeners.
2. **Database Index & SQLite Triage**: Repair and rebuild corrupted Horos database index structures (`DATABASE.noindex`) without losing patient image files.
3. **Automated Anonymization & HIPAA Compliance**: Build automated workflows stripping protected health information (PHI) tags from DICOM headers before research exports.
4. **URL Scheme Integration**: Trigger remote study retrieval and viewport loading via `horos://openStudy?accession=...`.

---

## Production Python Automation: Automated DICOM Dispatcher & Verification Client (`pynetdicom`)

Save this script as `send_dicom_to_horos.py` (requires `pip install pydicom pynetdicom`):

```python
"""
DICOM C-STORE SCU Pipeline for Horos
Verifies C-ECHO availability and sends patient DICOM studies to the local Horos listener.
"""

import sys
import os
from pydicom import dcmread
from pynetdicom import AE, StoragePresentationContexts, VerificationPresentationContexts

HOROS_AE_TITLE = "HOROS"
HOROS_HOST = "127.0.0.1"
HOROS_PORT = 11112

def send_study_to_horos(dicom_dir: str):
    if not os.path.exists(dicom_dir):
        print(f"Error: Directory '{dicom_dir}' does not exist.")
        return

    # 1. Initialize Application Entity
    ae = AE(ae_title="PYTHON_DISPATCH")
    ae.requested_contexts = StoragePresentationContexts + VerificationPresentationContexts

    print(f"--- [CONNECTING TO HOROS DICOM LISTENER: {HOROS_HOST}:{HOROS_PORT}] ---")
    assoc = ae.associate(HOROS_HOST, HOROS_PORT, ae_title=HOROS_AE_TITLE)

    if not assoc.is_established:
        print("🚨 Error: Could not establish DICOM association. Is Horos running and DICOM listener active?")
        return

    # 2. Test Connection via C-ECHO (Ping)
    print("Testing connection with C-ECHO...")
    echo_status = assoc.send_c_echo()
    if echo_status and echo_status.Status == 0:
        print("✅ C-ECHO Verification Successful!")
    else:
        print("🚨 C-ECHO Verification Failed.")
        assoc.release()
        return

    # 3. Transmit All DICOM Files via C-STORE
    sent_count = 0
    for root, _, files in os.walk(dicom_dir):
        for f in files:
            file_path = os.path.join(root, f)
            try:
                ds = dcmread(file_path, stop_before_pixels=False)
                patient_name = ds.get("PatientName", "Anonymous")
                study_uid = ds.get("StudyInstanceUID", "Unknown")

                status = assoc.send_c_store(ds)
                if status and status.Status == 0:
                    sent_count += 1
                    print(f"  • Sent [#{sent_count}]: {f} (Patient: {patient_name})")
                else:
                    print(f"  🚨 Failed to store: {f} (Status: {status.Status if status else 'None'})")
            except Exception:
                continue # Skip non-DICOM files

    print(f"\n✅ Successfully transferred {sent_count} DICOM slice(s) to Horos database.")
    assoc.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 send_dicom_to_horos.py <path_to_dicom_folder>")
        sys.exit(1)
    send_study_to_horos(sys.argv[1])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **PACS C-MOVE Fails / No Images Transferred** | Hospital PACS firewall blocking inbound TCP port 11112 back to the Mac or mismatched AE Title. | 1. In Horos Preferences $\rightarrow$ **Listener**, verify port (default `11112`) and AE Title (`HOROS`).<br>2. Ensure macOS Firewall allows inbound connections to Horos.<br>3. Verify Horos AE Title and IP are registered in hospital PACS routing table. |
| **Horos Freezes on Launch at `Updating Database`** | SQLite index `DATABASE.noindex/HorosData.sqlite` corrupted due to force-quitting. | 1. Navigate to `~/Documents/Horos Data/DATABASE.noindex/`.<br>2. Rename `HorosData.sqlite` to `HorosData.sqlite.bak`.<br>3. Launch Horos $\rightarrow$ Select *File $\rightarrow$ Rebuild Database*. |
| **Application Crashes Opening Large 4D Cardiac CT** | Out of memory loading uncompressed cine frame volume series into system RAM. | In Horos Preferences $\rightarrow$ **Viewers**, check **Load images in 2D Viewer only when needed** and enable frame caching. |
| **Anonymization Leaves Private Patient Metadata** | Vendor-specific private tags (e.g. `(0019, 1010)`) not listed in standard HIPAA tag removal filter. | In Anonymize dialog, check **Remove all Private Tags** and verify output in metadata viewer. |

---

## Command Line Syntax & macOS DCMTK Recipes

```bash
# 1. Test DICOM Echo Connectivity to Horos via DCMTK
echoscu -v -aet PYTHON_SCU -aec HOROS 127.0.0.1 11112

# 2. Open Specific Study in Horos via URL Scheme
open "horos://openStudy?accession=ACC987654"

# 3. Read Horos Preferences via defaults CLI
defaults read org.horosproject.horos
```

### Essential File Locations
- **Horos Database Directory**: `~/Documents/Horos Data/`
- **Preferences Plist**: `~/Library/Preferences/org.horosproject.horos.plist`
- **Installed Plugins**: `~/Library/Application Support/Horos/Plugins/`

---

## Agent Operational Directive
> **MANDATORY**: Verify that the Horos C-STORE SCP listener is active on TCP port 11112 using `echoscu` before diagnosing PACS image retrieval and transfer failures.
