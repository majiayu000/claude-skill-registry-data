---
name: autopsy
description: "Automate authorized forensic analysis in Autopsy with Sleuth Kit ingest modules, evidence-processing pipelines, and search indexing."
category: digital-forensics
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["autopsy", "the-sleuth-kit", "digital-forensics", "incident-response", "e01-image", "solr-indexing", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Autopsy Digital Forensics AI Skill Guide (Claude)

## Overview & Engine Architecture
Autopsy is the premier open-source digital forensics platform built on **The Sleuth Kit (TSK)** library and the NetBeans platform. It provides automated evidence ingestion, forensic image processing (E01, RAW/DD, VMDK, VHD), file carving, keyword indexing via **Apache Solr**, timeline analysis, and artifact extraction into a unified **Blackboard schema**. Claude operates as a Senior Digital Forensics and Incident Response (DFIR) Specialist and Forensic Tools Developer, specializing in **TSK filesystem analysis**, **custom Python Ingest Module authoring**, **forensic artifact triage (Registry, Prefetch, EVTX, Browser History)**, and **evidence chain-of-custody verification**.

### Autopsy & The Sleuth Kit Execution Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Autopsy Forensics Architecture              │
│                                                             │
│  Evidence Ingestion Layer                                   │
│  ├── Forensic Disk Images (E01, RAW, VHD, VMDK, AFF4)      │
│  ├── The Sleuth Kit Core (Partition Tables: MBR/GPT, NTFS)  │
│  └── Hash Calculation & Verification (MD5, SHA-1, SHA-256) │
│                                                             │
│  Ingest Pipeline & Analysis Layer                           │
│  ├── Ingest Modules (File Type, Hash Lookup, Carving)       │
│  ├── Apache Solr Keyword Search & Regex Indexing Engine     │
│  └── Central Blackboard (`autopsy.db` SQLite / PostgreSQL)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Python Ingest Module Development**: Author Jython/Python Ingest Modules implementing `FileIngestModule` and `DataSourceIngestModule` to parse proprietary artifact files and post entries to the Autopsy Blackboard.
2. **Timeline & Forensic Triage**: Reconstruct chronological event sequences combining NTFS `$MFT` (MACB timestamps), Windows Event Logs, USN Journal records, and Prefetch execution timestamps.
3. **Ingest Pipeline Performance Tuning**: Diagnose pipeline bottlenecks, allocate JVM heap sizes (`-J-Xmx16g`), manage thread pools, and configure NSRL known-file hash sets.
4. **The Sleuth Kit (TSK) CLI Forensic Triage**: Author headless CLI scripts using `mmls`, `fls`, `istat`, and `icat` for rapid evidence triage without GUI initialization.

---

## Production Python Automation: Custom Autopsy File Ingest Module

Save this script inside Autopsy's Python Ingest Modules folder (`%APPDATA%\autopsy\python_modules\`) to flag suspicious PowerShell and script executions:

```python
"""
Autopsy Custom Python Ingest Module
Detects suspicious script extensions (.ps1, .vbs, .bat) and flags them to the Blackboard.
"""

from org.sleuthkit.autopsy.ingest import IngestModule
from org.sleuthkit.autopsy.ingest import FileIngestModule
from org.sleuthkit.autopsy.ingest import IngestServices
from org.sleuthkit.autopsy.ingest import IngestModuleFactoryAdapter
from org.sleuthkit.datamodel import BlackboardArtifact
from org.sleuthkit.datamodel import BlackboardAttribute
from org.sleuthkit.datamodel import TskData

class ScriptDetectorFactory(IngestModuleFactoryAdapter):
    def getModuleDisplayName(self):
        return "Suspicious Script Ingest Module"
    def getModuleDescription(self):
        return "Identifies script files in temporary and user directories."
    def getModuleVersionNumber(self):
        return "1.0"
    def isFileIngestModuleFactory(self):
        return True
    def createFileIngestModule(self, ingestOptions):
        return ScriptDetectorModule()

class ScriptDetectorModule(FileIngestModule):
    def startUp(self, context):
        self.services = IngestServices.getInstance()
        self.SUSPICIOUS_EXTS = [".ps1", ".vbs", ".bat", ".cmd", ".hta"]

    def process(self, file):
        # Skip directories and non-files
        if file.getType() == TskData.TSK_DB_FILES_TYPE_ENUM.FS_FILE and not file.isDir():
            file_name = file.getName().lower()
            
            # Check if file has script extension
            if any(file_name.endswith(ext) for ext in self.SUSPICIOUS_EXTS):
                # Post Interesting Item artifact to Blackboard
                art = file.newArtifact(BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
                attr = BlackboardAttribute(
                    BlackboardAttribute.ATTRIBUTE_TYPE.TSK_SET_NAME.getTypeID(),
                    "Suspicious Script Detector",
                    "High-Risk Execution Script Detected"
                )
                art.addAttribute(attr)
                self.services.fireModuleDataEvent(
                    org.sleuthkit.autopsy.ingest.ModuleDataEvent("ScriptDetector", BlackboardArtifact.ARTIFACT_TYPE.TSK_INTERESTING_FILE_HIT)
                )

        return IngestModule.ProcessResult.OK

    def shutDown(self):
        pass
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Ingest Modules Hang at `Analyzing Data Source (0%)`** | Embedded Apache Solr keyword index server crashed or case storage drive ran out of free space. | 1. In Autopsy, open *Tools $\rightarrow$ Options $\rightarrow$ Keyword Search $\rightarrow$ Restart Solr*.<br>2. Verify case drive has $>50\text{GB}$ free disk space.<br>3. Check Solr logs at `%USERPROFILE%\.autopsy\dev\solr\logs\solr.log`. |
| **E01 Image Fails Ingestion: `Hash Verification Error`** | Image was partially corrupted during network transfer or has damaged E01 header chunks. | 1. Calculate source image SHA-256 hash using `sha256sum`.<br>2. Compare with acquisition log hash.<br>3. Use `ewfinfo disk.E01` to check segment chunk integrity. |
| **High False-Positive Storm in File Carving Results** | File carver processing unallocated pagefile.sys / swap space with fragmented byte patterns. | 1. Disable generic carving on virtual memory files (`pagefile.sys`, `swapfile.sys`).<br>2. Load **NSRL (National Software Reference Library)** known hash set to filter out standard Windows OS binaries.<br>3. Limit carving to specific required signatures (e.g. PDF, JPG, Office docs). |
| **SQLite Case Database Lockup (`database is locked`)** | Large multi-terabyte evidence case overwhelmed single-file SQLite write concurrency. | For multi-user environments or cases $>2\text{TB}$, configure Autopsy to use a **PostgreSQL** database cluster in *Tools $\rightarrow$ Options $\rightarrow$ Multi-User*. |

---

## Command Line Syntax & The Sleuth Kit (TSK) Triage

```bash
# 1. Inspect Partition Table Layout on Forensic Image
mmls -t dos "C:\Evidence\disk_image.E01"

# 2. List Deleted Files in Root NTFS Partition (Offset: 2048 sectors)
fls -r -d -o 2048 "C:\Evidence\disk_image.E01"

# 3. Extract Specific Inode / MFT Record to Disk
icat -o 2048 "C:\Evidence\disk_image.E01" 14250 > extracted_file.exe

# 4. Launch Autopsy with Custom JVM Heap Allocation (16GB)
"C:\Program Files\Autopsy-4.21\bin\autopsy64.exe" -J-Xmx16g
```

### Essential File & Directory Locations
- **Autopsy User Config Directory**: `%USERPROFILE%\.autopsy`
- **Case Database File**: `<Case_Dir>\autopsy.db`
- **Python Ingest Module Directory**: `%APPDATA%\autopsy\python_modules`
- **Solr Index Directory**: `<Case_Dir>\KeywordSearch\data`

---

## Agent Operational Directive
> **MANDATORY**: When handling forensic images, always verify acquisition cryptographic hashes (MD5 / SHA-256) before starting ingest modules. For enterprise cases with $>1\text{M}$ files, configure PostgreSQL rather than SQLite.
