---
name: osirix
description: "Configure OsiriX DICOM networking, database indexing, and hanging protocols for software workflows, not clinical interpretation."
category: medical
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["osirix", "osirix-md", "radiology-workstation", "pacs-networking", "c-find", "c-move", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# OsiriX MD Clinical DICOM Workstation AI Skill Guide (Claude)

## Overview & Engine Architecture
OsiriX MD is a clinical-grade, FDA-cleared and CE-certified medical imaging workstation and DICOM viewer for macOS. Built with high-performance Objective-C, Cocoa, and Metal GPU shaders, OsiriX features **Hanging Protocols for multi-monitor radiology reading suites**, advanced **Curved MPR / 3D Endoscopy / PET-CT Fusion**, an embedded **CoreData SQLite database**, and bidirectional **PACS networking (C-STORE SCP, C-FIND SCU, C-MOVE SCU, DICOMweb WADO-RS/QIDO-RS)**. Claude operates as a Principal Clinical PACS Architect and Medical Systems Engineer, specializing in **DICOM hierarchical query scripting (C-FIND/C-MOVE)**, **OsiriX database maintenance & SQLite vacuuming**, **multi-head display hanging protocol calibration**, and **AppleScript / URL scheme (`osirix://`) automation**.

### OsiriX Clinical Workstation Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 OsiriX System Architecture                  │
│                                                             │
│  Radiology Reading & Presentation Tier                      │
│  ├── Multi-Monitor Hanging Protocols (1x1, 2x2, Dual-Head)  │
│  ├── 2D Viewer (Window/Level, SUV PET-CT Fusion, Cine Loop) │
│  └── 3D Post-Processing (Curved MPR, MIP, Volume Rendering) │
│                                                             │
│  DICOM Networking & Query/Retrieve Engine                   │
│  ├── C-STORE SCP Listener Daemon (Default Port: 11112)      │
│  ├── Hierarchical C-FIND & C-MOVE SCU (Patient/Study/Series)│
│  └── DICOM TLS 1.3 Encryption & Certificate Management      │
│                                                             │
│  Storage & Extensibility Engine                             │
│  ├── CoreData SQLite Database (`OsiriX Data/DATABASE.noindex│
│  └── AppleScript (`tell app "OsiriX"`) & `osirix://` Schemes│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Hierarchical PACS Query & Retrieve Automation**: Author Python scripts utilizing `pynetdicom` to perform Patient, Study, and Series level `C-FIND` queries and issue `C-MOVE` requests directing studies to OsiriX.
2. **Database Maintenance & SQLite Recovery**: Script automated cleanup and indexing routines to defragment and repair OsiriX's `DATABASE.noindex/OsiriXDB.sqlite`.
3. **Multi-Head Hanging Protocol Triage**: Configure multi-display hanging protocols to ensure bilateral mammography or pre/post-operative CT studies open consistently across designated medical monitors.
4. **URL Scheme & AppleScript Automation**: Trigger automated study loading, series selection, and ROI export via `osirix://loadStudy?patientID=...` and AppleScript.

---

## Production Python Automation: Automated Hierarchical PACS Query (C-FIND) & Move (C-MOVE) Client

Save this script as `pacs_query_retrieve.py` (requires `pip install pydicom pynetdicom`):

```python
"""
Hierarchical PACS C-FIND Query & C-MOVE Retrieval Client
Queries central hospital PACS and instructs it to route matching studies to OsiriX.
"""

import sys
from pynetdicom import AE, QueryRetrievePresentationContexts
from pydicom.dataset import Dataset

PACS_HOST = "192.168.1.100"
PACS_PORT = 104
PACS_AE_TITLE = "CENTRAL_PACS"

OSIRIX_AE_TITLE = "OSIRIX_MD"

def query_and_retrieve_study(patient_id: str):
    # 1. Initialize Application Entity with Query/Retrieve Contexts
    ae = AE(ae_title=OSIRIX_AE_TITLE)
    ae.requested_contexts = QueryRetrievePresentationContexts

    print(f"--- [QUERYING PACS: {PACS_HOST}:{PACS_PORT} (AE: {PACS_AE_TITLE})] ---")
    assoc = ae.associate(PACS_HOST, PACS_PORT, ae_title=PACS_AE_TITLE)

    if not assoc.is_established:
        print("🚨 Error: Could not establish association with PACS server.")
        return

    # 2. Build Study-Level C-FIND Query Dataset
    query_ds = Dataset()
    query_ds.QueryRetrieveLevel = "STUDY"
    query_ds.PatientID = patient_id
    query_ds.PatientName = ""
    query_ds.StudyDate = ""
    query_ds.StudyDescription = ""
    query_ds.StudyInstanceUID = ""
    query_ds.ModalitiesInStudy = ""

    print(f"Executing Study-Level C-FIND for Patient ID: '{patient_id}'...")
    responses = assoc.send_c_find(query_ds, query_model="1.2.840.10008.5.1.4.1.2.2.1") # Study Root

    matching_studies = []
    for status, identifier in responses:
        if status and status.Status in (0xFF00, 0xFF01): # Pending
            study_uid = identifier.get("StudyInstanceUID")
            study_desc = identifier.get("StudyDescription", "No Description")
            study_date = identifier.get("StudyDate", "Unknown Date")
            modality = identifier.get("ModalitiesInStudy", "CT")
            matching_studies.append((study_uid, study_desc, study_date, modality))

    print(f"Found {len(matching_studies)} matching study/studies.")

    # 3. Issue C-MOVE Request to Route Study to Local OsiriX Workstation
    for study_uid, desc, sdate, mod in matching_studies:
        print(f"\nTriggering C-MOVE for: {desc} [{sdate}] ({study_uid})...")
        move_ds = Dataset()
        move_ds.QueryRetrieveLevel = "STUDY"
        move_ds.StudyInstanceUID = study_uid

        # Send C-MOVE request targeting local OsiriX AE Title
        move_responses = assoc.send_c_move(move_ds, move_aetitle=OSIRIX_AE_TITLE, query_model="1.2.840.10008.5.1.4.1.2.2.2")
        for m_status, m_ident in move_responses:
            if m_status and m_status.Status in (0xFF00, 0xFF01):
                continue

        print(f"✅ Dispatched C-MOVE for Study: {study_uid}")

    assoc.release()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pacs_query_retrieve.py <Patient_ID>")
        sys.exit(1)
    query_and_retrieve_study(sys.argv[1])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **OsiriX Database Slow / Table List Stalls** | SQLite database file `OsiriXDB.sqlite` fragmented after importing thousands of series. | 1. In OsiriX, navigate to *File $\rightarrow$ Database $\rightarrow$ Rebuild Database*.<br>2. Or vacuum via CLI: `sqlite3 ~/Documents/OsiriX\ Data/DATABASE.noindex/OsiriXDB.sqlite "VACUUM;"`. |
| **Inbound C-STORE Fails: `Connection Refused` on 11112** | OsiriX DICOM listener daemon is stopped or macOS Firewall blocked inbound traffic. | 1. In OsiriX Preferences $\rightarrow$ **Listener**, verify **Activate DICOM Listener** is checked on port 11112.<br>2. In macOS System Settings, allow OsiriX in Network Firewall. |
| **Multi-Monitor Hanging Protocol Opens on Wrong Screen** | Monitor index sequence shifted following a display resolution change or display disconnection. | In OsiriX Preferences $\rightarrow$ **Hanging Protocols**, re-assign specific series viewports to Display 1 (Main) and Display 2 (Diagnostic). |
| **DICOM TLS Association Handshake Fails** | Expired client SSL certificate or CA root certificate missing in macOS Keychain. | In Preferences $\rightarrow$ **Security**, verify imported PKCS#12 client certificate validity date. |

---

## Command Line Syntax & macOS Diagnostics

```bash
# 1. Vacuum and Optimize OsiriX SQLite Database
sqlite3 ~/Documents/OsiriX\ Data/DATABASE.noindex/OsiriXDB.sqlite "VACUUM; ANALYZE;"

# 2. Inspect Inbound DICOM Port Listener Status
lsof -i :11112

# 3. Read OsiriX Configuration Defaults
defaults read com.rossetantoine.osirix
```

### Essential File Locations
- **OsiriX Database**: `~/Documents/OsiriX Data/`
- **Preferences Plist**: `~/Library/Preferences/com.rossetantoine.osirix.plist`
- **Application Support Directory**: `~/Library/Application Support/OsiriX/`

---

## Agent Operational Directive
> **MANDATORY**: Periodically execute `VACUUM` on `OsiriXDB.sqlite` when managing databases containing over 10,000 studies to prevent table query timeouts during PACS auto-routing.
