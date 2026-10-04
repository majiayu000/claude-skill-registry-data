---
name: sap-gui
description: "Automate SAP GUI workflows with VBScript or Python, inspect ALV controls, and troubleshoot scripting or landscape configuration."
category: erp
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["sap-gui", "sap-scripting", "alv-grid", "s4hana", "abap-transactions", "saplogon", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# SAP GUI Desktop & Scripting Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
SAP GUI for Windows is the native desktop presentation tier for SAP ECC and SAP S/4HANA, communicating via the binary **DIAG protocol** (TCP port `3200 + SystemNumber`). SAP GUI features an embedded **SAP GUI Scripting Engine (COM API)** for automated robotic process automation (RPA), interactive **ALV Grid controls (`GuiGridView`)**, and centralized connection management via **`SAPUILandscape.xml`**. Claude operates as an Enterprise SAP Basis Administrator and RPA Automation Specialist, specializing in **Python / VBScript SAP GUI Scripting**, **RZ11 server scripting parameter enablement**, **ALV grid table scraping**, and **SNC single sign-on configuration**.

### SAP GUI Client & NetWeaver Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 SAP GUI Presentation Stack                  │
│                                                             │
│  Client Presentation & Scripting Engine                     │
│  ├── SAP Logon Client (`saplogon.exe` / `SAPUILandscape.xml`)│
│  ├── SAP GUI Scripting Engine COM API (`GuiApplication`)    │
│  └── Dynpro Screen & ALV Grid Controls (`GuiGridView`)      │
│                                                             │
│  Network & Security Protocol                                │
│  ├── SAP DIAG Binary Stream (TCP Port 3200-3299)            │
│  ├── Secure Network Communication (SNC / Kerberos SSO)      │
│  └── SAProuter Gateway Relays (`/H/saprouter/S/3299/...`)   │
│                                                             │
│  Application Server & ABAP Runtime                          │
│  ├── ABAP Dispatcher & Work Process Farm (DIA/UPD/BGD)      │
│  └── Profile Parameters (`sapgui/user_scripting = TRUE`)    │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Python SAP GUI Scripting Automation**: Author robust Python scripts using `win32com.client` to attach to active SAP sessions, navigate transaction codes (TCodes), enter header data, and read ALV grid tables.
2. **Server-Side Scripting Security Enablement**: Diagnose and configure SAP profile parameters (`sapgui/user_scripting`, `sapgui/user_scripting_disable_recording`, `sapgui/user_scripting_set_readonly`) in transaction **RZ11**.
3. **ALV Grid & Table Control Extraction**: Parse and export data from complex `GuiGridView` controls (`GetCellValue`, `SelectAll`, `PressToolbarButton`).
4. **`SAPUILandscape.xml` Centralization**: Manage enterprise connection definitions, message servers, routers, and SNC partner names across client fleets.

---

## Production Python Automation: Automated SAP GUI Session Attacher & ALV Scraper

Save this script as `sap_gui_scraper.py` (requires `pip install pywin32`):

```python
"""
SAP GUI Scripting API Automation (Python / COM)
Attaches to active SAP GUI session, executes TCode SE16N, and exports ALV grid data.
"""

import sys
import win32com.client

def attach_sap_session(session_index: int = 0):
    try:
        # Access Running SAP GUI COM Object via ROT (Running Object Table)
        sap_gui_auto = win32com.client.GetObject("SAPGUI")
        if not sap_gui_auto:
            print("Error: SAP GUI is not running.")
            return None

        application = sap_gui_auto.GetScriptingEngine
        if not application:
            print("Error: Scripting Engine not available (check RZ11 parameters).")
            return None

        connection = application.Children(0)
        session = connection.Children(session_index)
        print(f"Connected to SAP System: {session.Info.SystemName} (Client: {session.Info.Client}, User: {session.Info.User})")
        return session

    except Exception as e:
        print(f"Failed to attach to SAP GUI COM engine: {e}")
        return None

def query_sales_orders(session, max_rows: int = 25):
    try:
        # 1. Navigate to Table Viewer Transaction (SE16N)
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nSE16N"
        session.findById("wnd[0]").sendVKey(0) # Press Enter

        # 2. Enter Table Name (VBAK - Sales Document Header)
        session.findById("wnd[0]/usr/ctxtGD-TAB").text = "VBAK"
        session.findById("wnd[0]/usr/txtGD-MAX_LINES").text = str(max_rows)
        session.findById("wnd[0]/tbar[1]/btn[8]").press() # Execute (F8)

        # 3. Read Results from ALV Grid Control
        grid = session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell")
        row_count = grid.RowCount
        print(f"\n--- [EXTRACTED {row_count} SALES ORDERS FROM VBAK] ---")

        for r in range(min(row_count, max_rows)):
            sales_doc = grid.GetCellValue(r, "VBELN")
            doc_type  = grid.GetCellValue(r, "AUART")
            net_val   = grid.GetCellValue(r, "NETWR")
            currency  = grid.GetCellValue(r, "WAERK")
            cust_no   = grid.GetCellValue(r, "KUNNR")
            print(f"• Order: {sales_doc:<10} | Type: {doc_type:<4} | Amount: {net_val:>10} {currency} | Customer: {cust_no}")

        # Return to main screen
        session.findById("wnd[0]/tbar[0]/okcd").text = "/n"
        session.findById("wnd[0]").sendVKey(0)

    except Exception as e:
        print(f"Transaction automation error: {e}")

if __name__ == "__main__":
    sess = attach_sap_session(0)
    if sess:
        query_sales_orders(sess, max_rows=10)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`Scripting API Error: The scripting API is not installed or enabled`** | Server-side profile parameter `sapgui/user_scripting` is set to `FALSE` in the SAP instance. | 1. In SAP GUI, log in as Basis Administrator $\rightarrow$ Open TCode **RZ11**.<br>2. Enter parameter: `sapgui/user_scripting` $\rightarrow$ Click **Change Value** $\rightarrow$ Set to `TRUE`.<br>3. Check client options in *SAP GUI Options $\rightarrow$ Accessibility & Scripting $\rightarrow$ Enable Scripting*. |
| **Session Disconnects: `WSAECONNRESET: Connection to partner broken`** | Network firewall dropped idle TCP connection on port 3200 or SAP dispatcher `rdisp/keepalive` timed out. | 1. In RZ11, increase `rdisp/keepalive` to `1200` seconds.<br>2. Enable TCP KeepAlive on Windows network interface.<br>3. Verify SAProuter connection string. |
| **ALV Grid Selection Fails: `Cannot find GUI element wnd[0]/usr/cntl...`** | The report was executed in Classical List mode rather than modern ALV Grid Control mode. | In report selection screen, ensure **ALV Grid Display** is checked, or adjust the control path. |
| **SAP Shortcut Fails: `sapshcut.exe password rejected`** | SAP GUI 7.70/8.0 security restriction disallowing plaintext password arguments in command-line shortcuts. | Configure **SNC Single Sign-On (Kerberos)** or launch shortcut with user prompt. |

---

## Command Line Syntax & Shortcuts

```bash
# 1. Launch SAP GUI Directly into Transaction via sapshcut
"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\sapshcut.exe" -system=PRD -client=100 -user=JSMITH -command="/nVA01"

# 2. Launch SAP Logon with Dedicated Landscape File
"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe" /LANDSCAPE="\\shared_nas\sap\SAPUILandscape.xml"
```

### Essential File Locations
- **Master Connection Landscape**: `%APPDATA%\SAP\Common\SAPUILandscape.xml`
- **User Settings**: `%APPDATA%\SAP\SAPLogon\SAPLogonTree.xml`
- **SAP GUI Trace Logs**: `%APPDATA%\SAP\SAP GUI\Traces\`

---

## Agent Operational Directive
> **MANDATORY**: Verify that `sapgui/user_scripting` is set to `TRUE` in transaction RZ11 before executing COM automation. In production scripts, uncheck "Notify when a script attaches to SAP GUI" to enable headless background RPA execution.
