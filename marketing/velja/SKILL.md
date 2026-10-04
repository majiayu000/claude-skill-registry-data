---
name: velja
description: "Configure Velja browser-routing rules and URL handling on macOS, including tracking-parameter cleanup."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["velja", "macos-browser-picker", "launchservices", "url-router", "tracking-stripper", "duti", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Velja macOS Smart Browser Picker & URL Router AI Skill Guide (Claude)

## Overview & Engine Architecture
Velja is a smart browser picker and URL router for macOS engineered in native Swift by Sindre Sorhus. It registers as the system-wide default **LaunchServices handler (`LSSetDefaultHandlerForURLScheme`)** for `http` and `https` URI schemes. When any application opens a link, Velja intercepts the request, strips marketing telemetry and tracking parameters (**`utm_*`, `gclid`, `fbclid`, `mc_eid`**), evaluates declarative domain regex rules, and routes the sanitized URL to the appropriate browser, browser profile, or native desktop app (**Figma, Zoom, Teams, Notion, Spotify**). Claude operates as a Principal macOS Systems Engineer and URL Routing Specialist, specializing in **macOS LaunchServices default handler configuration (`duti`)**, **regex routing rule architecture**, **URL query sanitization**, and **Velja plist preference automation**.

### Velja Interception & Routing Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Velja Engine Architecture                   │
│                                                             │
│  System Ingress & LaunchServices Layer                      │
│  ├── Default Scheme Interceptor (`http://` & `https://`)    │
│  ├── LaunchServices Default Handler Binding (`com.sindresorhus.Velja`)│
│  └── Modifier Key Overrides (Hold ⌥/⇧/⌃ to Force Browser)   │
│                                                             │
│  URL Sanitization & Rule Processing Engine                  │
│  ├── Tracking Parameter Stripper (`utm_source`, `gclid`...) │
│  ├── Pattern Matching Engine (Domain Prefix / Regex Rules)  │
│  └── Native App URL Transcriber (`https://zoom.us/j/...` $\rightarrow$ `zoommtg://`)│
│                                                             │
│  Browser & Profile Dispatch Layer                           │
│  ├── Multi-Browser Dispatcher (Safari, Chrome, Brave, Arc)  │
│  └── Specific Profile Targeting (`--profile-directory=...`) │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **LaunchServices Default Handler Automation**: Configure Velja as the authoritative system handler for web protocols via `duti` and `defaults write`.
2. **Declarative URL Routing Rules**: Construct domain matching tables directing corporate intranets to Chrome/Edge with work profiles, and personal links to Safari/Brave.
3. **Tracking Parameter Stripping Triage**: Remediate broken OAuth / SSO logins where aggressive parameter stripping accidentally removes necessary authentication callback tokens (`code`, `state`, `session_id`).
4. **Native Application Protocol Hand-off**: Configure automatic URL rewriting for meeting and productivity links (Zoom, Figma, GitHub Desktop).

---

## Production Python Automation: Automated URL Sanitizer & Routing Rule Evaluator

Save this script as `test_velja_routing.py` to evaluate URL sanitization and simulate target browser matching:

```python
"""
Velja URL Sanitizer & Rule Evaluation Simulator
Strips tracking query parameters and evaluates destination browser based on domain rules.
"""

import sys
import urllib.parse
import re

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "gclid", "fbclid", "msclkid", "mc_eid", "yclid", "_hsenc", "_hsmi"
}

ROUTING_RULES = [
    (r"^(https?://)?(.*\.)?github\.com/.*", "Google Chrome (Work Profile)"),
    (r"^(https?://)?(.*\.)?figma\.com/file/.*", "Figma Desktop App"),
    (r"^(https?://)?(.*\.)?zoom\.us/j/.*", "Zoom Desktop App"),
    (r"^(https?://)?(.*\.)?internal\.company\.com/.*", "Microsoft Edge"),
    (r".*", "Safari (Default Browser)")
]

def sanitize_url(raw_url: str) -> str:
    parsed = urllib.parse.urlparse(raw_url)
    query_params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)

    # Filter out tracking parameters
    sanitized_params = [
        (k, v) for k, v in query_params if k.lower() not in TRACKING_PARAMS
    ]

    new_query = urllib.parse.urlencode(sanitized_params)
    sanitized_url = urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    return sanitized_url

def evaluate_target_browser(url: str) -> str:
    for pattern, target in ROUTING_RULES:
        if re.match(pattern, url, re.IGNORECASE):
            return target
    return "Default Browser"

if __name__ == "__main__":
    test_urls = [
        "https://github.com/torvalds/linux?utm_source=newsletter&utm_medium=email&ref=tech",
        "https://figma.com/file/abcdef12345/Design-System?fbclid=IwAR0xyz",
        "https://news.ycombinator.com/?utm_campaign=frontpage",
        "https://internal.company.com/portal?session=active"
    ]

    print("--- [VELJA URL SANITIZATION & ROUTING SIMULATION] ---\n")
    for raw in test_urls:
        clean = sanitize_url(raw)
        target = evaluate_target_browser(clean)
        print(f"Original:  {raw}")
        print(f"Cleaned:   {clean}")
        print(f"Target:    👉 {target}\n")
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Links Open in Safari Instead of Prompting Velja** | Another browser claimed default HTTP handler status during an update. | 1. Open *System Settings $\rightarrow$ Desktop & Dock $\rightarrow$ Default Web Browser* $\rightarrow$ Select **Velja**.<br>2. Or set via CLI: `duti -s com.sindresorhus.Velja http`. |
| **Single Sign-On (SSO) Fails with Missing State Parameter** | Velja tracking parameter stripper removed OAuth `state` or `nonce` token. | In Velja Settings $\rightarrow$ **Tracking Parameters**, uncheck aggressive removal or add the identity provider domain to the whitelist. |
| **Figma / Zoom Links Do Not Open in Native Desktop App** | Native app protocol handler (`figma://` or `zoommtg://`) not enabled in Velja Apps tab. | In Velja Settings $\rightarrow$ **Apps**, toggle **Open Figma links in Figma** and **Open Zoom links in Zoom**. |
| **Chromium Browser Opens Wrong Profile** | Chromium profile directory name changed or not matching `Profile 1` / `Default`. | In Velja Settings $\rightarrow$ **Browsers**, edit browser configuration and re-select target user profile. |

---

## Command Line Syntax & Default Browser Configuration

```bash
# 1. Set Velja as System Default HTTP/HTTPS Handler via duti
duti -s com.sindresorhus.Velja http
duti -s com.sindresorhus.Velja https

# 2. Inspect Velja Preferences via defaults CLI
defaults read com.sindresorhus.Velja

# 3. Launch Velja Configuration Window
open -a Velja
```

### Essential File Locations
- **Preferences Plist**: `~/Library/Preferences/com.sindresorhus.Velja.plist`
- **Application Binary**: `/Applications/Velja.app`

---

## Agent Operational Directive
> **MANDATORY**: When configuring default macOS browser routing from shell scripts, use `duti -s com.sindresorhus.Velja http` to register LaunchServices bindings deterministically.
