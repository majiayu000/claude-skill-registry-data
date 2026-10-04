---
name: shottr
description: "Configure Shottr capture and OCR workflows on macOS and investigate scrolling-capture or graphics issues."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["shottr", "macos-screen-capture", "screencapturekit", "vision-framework-ocr", "metal-rendering", "scrolling-screenshot", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Shottr macOS Screen Capture & Annotation AI Skill Guide (Claude)

## Overview & Engine Architecture
Shottr is an ultra-fast, lightweight macOS screenshot and annotation utility engineered in native Swift. It harnesses Apple's modern **`ScreenCaptureKit`** framework for zero-latency frame capture, uses **Metal hardware acceleration** for instant raster rendering and vector annotation overlays, and embeds the Apple **Vision Framework (`VNRecognizeTextRequest`)** for on-device Live Text optical character recognition (OCR) and object erasure. Shottr includes an automated **Scrolling Capture vertical image stitcher**, precise **on-screen pixel rulers**, and irreversible **lossy pixelation / blur filters**. Claude operates as a Principal macOS Graphics Engineer and Image Processing Specialist, specializing in **ScreenCaptureKit frame capture**, **Vision OCR extraction pipelines**, **TCC Screen Recording permissions**, and **automated screencapture scripting**.

### Shottr Core Architecture & Metal Pipeline Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 Shottr Engine Architecture                  │
│                                                             │
│  Capture & Frame Ingestion Tier                             │
│  ├── Apple `ScreenCaptureKit` Hardware Frame Ingestion      │
│  ├── Window ID / Display Stream Selector (`CGWindowList...`)│
│  └── Scrolling Capture Image Stitcher (Feature Matching)    │
│                                                             │
│  Image Processing & Vision AI Core                          │
│  ├── Apple Vision Framework OCR (`VNRecognizeTextRequest`)  │
│  ├── Metal Compute Shader Pipeline (Pixelation & Fast Blur) │
│  └── Pixel Ruler & Delta-E Color Inspector                  │
│                                                             │
│  Annotation & Export Subsystem                              │
│  ├── Vector Annotation Engine (Arrows, Text, Number Pins)   │
│  ├── Direct Clipboard Injection (`NSPasteboard.writeObjects`│
│  └── Lossless OptiPNG / WebP / JPEG Image Encoder           │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **ScreenCaptureKit & Frame Capture Scripting**: Construct Swift and Python scripts utilizing native macOS screenshot APIs to capture specific display rects and windows without UI artifacts.
2. **Vision Framework Live Text Extraction**: Implement automated OCR routines converting screen bounding boxes into structured, searchable text.
3. **Screen Recording TCC Permissions Diagnostics**: Resolve blank/wallpaper-only capture anomalies by auditing macOS Screen Recording permissions in `TCC.db`.
4. **Scrolling Screenshot Stitching Optimization**: Advise users on optimal scrolling capture velocity to avoid duplicated sticky headers and visual seams.

---

## Production Swift Automation: Headless Screen Capture & Vision OCR Pipeline

Save this file as `screen_capture_ocr.swift` and execute via `swift screen_capture_ocr.swift`:

```swift
// ==============================================================================
// Standalone Swift 5.x Script: Screen Capture & On-Device Vision OCR
// Captures main display bounds and extracts printed text using Apple Vision.
// ==============================================================================
import Cocoa
import Vision

// 1. Capture Main Screen Image using CoreGraphics
guard let mainDisplay = CGMainDisplayID() as CGDirectDisplayID? else {
    print("Error: Could not obtain main display ID.")
    exit(1)
}

guard let screenshot = CGDisplayCreateImage(mainDisplay) else {
    print("🚨 Error: Screen capture failed. Ensure Terminal has Screen Recording permissions in System Settings.")
    exit(1)
}

print("--- [CAPTURED SCREENSHOT: \(screenshot.width)x\(screenshot.height) px] ---")

// 2. Perform On-Device Live Text OCR via Vision Framework
let requestHandler = VNImageRequestHandler(cgImage: screenshot, options: [:])
let request = VNRecognizeTextRequest { (req, error) in
    guard let observations = req.results as? [VNRecognizedTextObservation] else {
        print("No text detected on screen.")
        return
    }

    print("\n--- [EXTRACTED ON-SCREEN TEXT VIA APPLE VISION OCR] ---")
    for observation in observations {
        guard let topCandidate = observation.topCandidates(1).first else { continue }
        if topCandidate.confidence > 0.5 {
            print("• \(topCandidate.string)")
        }
    }
}

request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

do {
    try requestHandler.perform([request])
    print("\n✅ OCR processing complete.")
} catch {
    print("Failed to perform OCR: \(error)")
}
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Captured Screenshot Shows Only Desktop Wallpaper** | macOS Screen Recording (TCC) permission not granted to Shottr. | 1. Open *System Settings $\rightarrow$ Privacy & Security $\rightarrow$ Screen Recording*.<br>2. Toggle **Shottr** ON.<br>3. Quit and relaunch Shottr. |
| **Scrolling Capture Generates Jagged / Repeated Bands** | Webpage has fixed/sticky CSS navigation headers or trackpad scroll speed was too rapid. | 1. Scroll at a steady, moderate pace.<br>2. In Shottr Scrolling window, check **Ignore Fixed Headers**.<br>3. Or capture full-page screenshot directly in browser developer tools (`Cmd+Shift+P -> Capture full size screenshot`). |
| **Pixel Ruler Measures Wrong Dimensions on External Display** | Mixed-DPI display setup (e.g. 2x Retina MacBook display paired with 1x 1080p monitor). | Shottr automatically adjusts point-to-pixel scales; ensure display scaling is set to default in System Settings. |
| **Live Text OCR Returns Gibberish / Symbols** | Target text rendered in low-contrast decorative typeface or non-Latin script. | Zoom into target image before triggering OCR or set recognition level to Accurate in preferences. |

---

## Command Line Syntax & macOS Screen Capture Recipes

```bash
# 1. Capture Interactive Rectangle Selection via macOS Native CLI
screencapture -i -c

# 2. Capture Entire Display Silently to Clipboard
screencapture -x -c

# 3. Read Shottr User Preferences via defaults CLI
defaults read cc.ffitch.shottr
```

### Essential File Locations
- **Preferences Plist**: `~/Library/Preferences/cc.ffitch.shottr.plist`
- **Application Support Cache**: `~/Library/Application Support/Shottr/`
- **TCC Screen Capture Service ID**: `kTCCServiceScreenCapture`

---

## Agent Operational Directive
> **MANDATORY**: When screenshots capture only empty desktop wallpaper without application windows, immediately guide the user to verify macOS Screen Recording permissions in System Settings $\rightarrow$ Privacy & Security.
