---
name: sharex
description: "Configure ShareX capture, recording, OCR, and custom uploader workflows with CLI or API integrations."
category: windows
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["sharex", "ffmpeg-screen-recording", "custom-uploader-sxcu", "windows-ocr", "scrolling-capture", "windows-11", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# ShareX Advanced Screen Capture & Automation AI Skill Guide (Claude)

## Overview & Engine Architecture
ShareX is an open-source screen capture, file sharing, and productivity utility for Windows built on **C# / .NET and WinForms**. Operating via **GDI+ and Direct2D** capture pipelines, ShareX integrates an embedded **FFmpeg engine** for high-framerate desktop video/GIF recording, native **Windows Media OCR & Tesseract 5**, and a **Custom Uploader System (`.sxcu`)** supporting HTTP REST endpoint integrations. Claude operates as a Principal Windows Systems Automation Architect and Media Pipeline Specialist, specializing in **ShareX Custom Uploader (`.sxcu`) engineering**, **FFmpeg recording optimization**, **OCR pipeline scripting**, and **automated workflow orchestration via CLI**.

### ShareX Engine Architecture & Media Ingress Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                 ShareX System Architecture                  │
│                                                             │
│  Capture Engine & Input Interceptors                        │
│  ├── Region, Window, Full Screen & Scrolling Capture GDI+   │
│  ├── Global Hotkey Manager (`RegisterHotKey` Win32 API)     │
│  └── Image Editor & Annotator (Canvas Drawing, Pin to Screen│
│                                                             │
│  Processing, OCR & Transcoding Subsystems                   │
│  ├── Embedded FFmpeg Core (NVENC, x264, VP9, GIF PalettGen) │
│  ├── Windows Media OCR & Tesseract 5 Multi-Language Engine  │
│  └── Post-Capture Tasks (Auto-Watermark, Border, Metadata)  │
│                                                             │
│  Uploaders & Automation Core                                │
│  ├── Custom Uploader Engine (`.sxcu` JSON REST Profiles)    │
│  ├── CLI Execution Engine (`ShareX.exe -workflow ...`)      │
│  └── Config Stores (`%DOCUMENTS%\ShareX\ApplicationConfig`) │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Custom Uploader (`.sxcu`) Architecture**: Author JSON custom uploader configurations defining HTTP `POST` multipart/form-data parameters, authorization headers, and JSON response body parsing paths (`$json:url$`).
2. **FFmpeg Screen Recording & Audio Device Triage**: Resolve missing audio capture drivers by provisioning DirectShow virtual audio devices (`virtual-audio-capturer`) and tuning NVENC hardware encoding.
3. **Automated CLI Workflow Execution**: Construct shell scripts triggering specific ShareX workflows (*e.g. OCR to clipboard, active window screenshot to cloud*) headlessly.
4. **Scrolling Capture Calibration**: Optimize scroll delay and client area edge detection on modern smooth-scrolling browsers.

---

## Production Python Automation: Custom ShareX Upload Server & `.sxcu` Profile

### 1. `ShareX_Custom_Uploader.sxcu` (ShareX Profile Schema)
Save and double-click to import into ShareX:

```json
{
  "Version": "15.0.0",
  "Name": "Local Python Secure Vault",
  "DestinationType": "ImageUploader, FileUploader",
  "RequestMethod": "POST",
  "RequestURL": "http://127.0.0.1:5000/upload",
  "Headers": {
    "X-Auth-Token": "secret_vault_token_123"
  },
  "Body": "MultipartFormData",
  "FileFormName": "file",
  "URL": "$json:url$",
  "ErrorMessage": "$json:error$"
}
```

### 2. `upload_server.py` (Local Secure File Receiver)
Save and execute with `python upload_server.py` (requires `pip install flask`):

```python
"""
ShareX Custom Uploader HTTP Endpoint Server (Flask)
Receives multipart uploads from ShareX, validates auth tokens, stores files, and returns JSON URLs.
"""

import sys
import os
import uuid
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
UPLOAD_DIR = r"C:\ShareX_Vault"
AUTH_TOKEN = "secret_vault_token_123"
SERVER_PORT = 5000

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def handle_sharex_upload():
    # 1. Validate Authentication Token
    client_token = request.headers.get("X-Auth-Token")
    if client_token != AUTH_TOKEN:
        return jsonify({"error": "Unauthorized: Invalid auth token"}), 403

    # 2. Extract Uploaded File
    if "file" not in request.files:
        return jsonify({"error": "Bad Request: Missing 'file' form data"}), 400

    uploaded_file = request.files["file"]
    if uploaded_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    # 3. Save File with Unique Name
    ext = os.path.splitext(uploaded_file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
    dest_path = os.path.join(UPLOAD_DIR, unique_filename)
    uploaded_file.save(dest_path)

    file_url = f"http://127.0.0.1:{SERVER_PORT}/files/{unique_filename}"
    print(f"✅ Received and stored: {unique_filename} -> URL: {file_url}")

    # 4. Return JSON response for ShareX parser ($json:url$)
    return jsonify({"url": file_url, "filename": unique_filename})

@app.route("/files/<filename>")
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

if __name__ == "__main__":
    print(f"--- [SHAREX UPLOAD SERVER RUNNING ON PORT {SERVER_PORT}] ---")
    app.run(host="0.0.0.0", port=SERVER_PORT, debug=False)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **FFmpeg Screen Recording Fails with Audio Error** | Virtual audio capture device not installed or DirectShow source missing. | In ShareX $\rightarrow$ *Task Settings $\rightarrow$ Screen Recorder*, click **Screen recording options** $\rightarrow$ Click **Install virtual-audio-capturer**. |
| **Custom Uploader Returns `HTTP 400/500 Error`** | Mismatch between `FileFormName` in `.sxcu` and server parameter (e.g. `file` vs `image`). | Match form name: ensure `FileFormName: "file"` in `.sxcu` corresponds to `request.files['file']` in server code. |
| **OCR Returns Empty String / Question Marks** | OCR engine attempting to parse non-Latin characters without language pack. | In ShareX Settings $\rightarrow$ OCR, switch engine from Tesseract to **Windows Media OCR** and install target language in Windows Settings. |
| **Hotkey Fails to Register: `Error code 1409`** | Another background app (Discord, Snipping Tool) already registered the global hotkey. | In ShareX $\rightarrow$ *Hotkey settings*, rebind the conflict hotkey (e.g. change `PrintScreen` to `Ctrl + Shift + S`). |

---

## Command Line Syntax & ShareX CLI Invocations

```bash
# 1. Capture Rectangle Region
"C:\Program Files\ShareX\ShareX.exe" -RectangleRegion

# 2. Trigger Screen Recording (Video/GIF)
"C:\Program Files\ShareX\ShareX.exe" -ScreenRecorder

# 3. Capture Screen and Trigger OCR Text Extraction
"C:\Program Files\ShareX\ShareX.exe" -OCR
```

### Essential File Locations
- **Application Config**: `%USERPROFILE%\Documents\ShareX\ApplicationConfig.json`
- **Custom Uploaders**: `%USERPROFILE%\Documents\ShareX\CustomUploaders.json`
- **Capture History**: `%USERPROFILE%\Documents\ShareX\History.json`

---

## Agent Operational Directive
> **MANDATORY**: When developing `.sxcu` Custom Uploader files for ShareX, verify that the `URL` response regex matches the exact JSON schema emitted by the backend server (`$json:url$`).
