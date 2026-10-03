---
name: desktop-controller
description: |
  Universal desktop application controller for Windows. Automate any desktop app — send messages, click buttons, type text, take screenshots, and interact with native Windows applications.
  Use this skill when the user asks to: "control my computer", "automate desktop", "send a message on [any chat app]", "click on [something]", "type into [app]", "take a screenshot", "操控电脑", "自动化桌面", "给某某发消息", "打开某某软件", "截个屏", or any task involving interacting with Windows desktop applications.
  WeChat triggers: "send a WeChat message", "message someone on WeChat", "打开微信发消息", "给某某发微信", "微信发送", "微信发消息", "用微信发", "帮我发微信".
  Email/Web triggers: "打开邮箱", "发邮件", "send email", "open browser", "操控浏览器", "网页操作".
  Supports: WeChat, WeCom, DingTalk, Feishu/Lark, QQ, Telegram, Slack, Teams, any browser-based web app, and any other Windows desktop application.
  Inspired by OpenAI's playwright-interactive skill, combining code-based automation with visual screenshot feedback loops.
  ROUTING: For web/Electron apps (email, Slack, browser), prefer Playwright with CSS selectors for speed and precision. For native desktop apps (WeChat, QQ, DingTalk), use Win32 API automation.
---

# Universal Desktop Controller

Automate any Windows desktop application using a combination of **Win32 API**, **Playwright** (for web/Electron apps), and **screenshot-based visual feedback**. Inspired by OpenAI's `playwright-interactive` Codex skill, adapted for Claude Code.

## Smart Routing: Choose the Right Engine

**CRITICAL DECISION**: Before any action, determine which engine to use:

```
User Request → Is it a web/browser/Electron app?
                 ├── YES → Playwright (CSS selectors, instant, precise)
                 │         Examples: email webmail, Slack, browser tasks, web forms
                 │         ✅ page.click('#compose')  — instant, 100% accurate
                 │
                 └── NO  → Win32 API (native desktop automation)
                           Examples: WeChat, QQ, DingTalk, Notepad, File Explorer
                           ✅ SetCursorPos + mouse_event — works for any native app
```

**Why this matters**: For the Tsinghua email (a web app), using Playwright CSS selectors is 10-50x faster than screenshot→analyze→click. OpenAI's playwright-interactive proved this: DOM selectors beat vision-based coordinate guessing every time for web content.

| Engine | Speed | Precision | Use For |
|--------|-------|-----------|---------|
| Playwright | <1s per action | 100% (DOM selector) | Web apps, Electron apps, browser tasks |
| Win32 API | 2-3s per action | 95% (coordinate-based) | Native desktop apps (WeChat, QQ, etc.) |
| Screenshot+Vision | 10-15s per action | 80% (AI guessing) | Last resort / unknown UI |

## Architecture

```
┌──────────────────────────────────────────────────┐
│             Desktop Controller Skill              │
├──────────────┬──────────────┬────────────────────┤
│  Win32 Layer │ Playwright   │  Visual Feedback   │
│  (Native)    │ (Web/Electron)│  (Screenshot+AI)   │
├──────────────┼──────────────┼────────────────────┤
│ FindWindow   │ Browser      │ CaptureScreen      │
│ SendKeys     │ Page.click   │ CaptureWindow      │
│ SetCursorPos │ Page.fill    │ → Claude Vision    │
│ mouse_event  │ Page.goto    │ → Verify State     │
│ Clipboard    │ Locator      │ → Decide Next Step │
└──────────────┴──────────────┴────────────────────┘
```

## Two Automation Modes

### Mode 1: Win32 Native (for desktop apps — WeChat, QQ, etc.)
Best for: WeChat, QQ, DingTalk, WeCom, Feishu, Notepad, File Explorer, etc.

**How it works:**
1. Find the app window by process name
2. Bring to foreground (ShowWindow + SetForegroundWindow)
3. Use keyboard (SendKeys) and mouse (SetCursorPos + mouse_event) automation
4. Use clipboard for text input (handles Unicode/Chinese perfectly)
5. Take screenshots for visual verification

### Mode 2: Playwright (for web & Electron apps — email, Slack, etc.)
Best for: Email webmail, Slack, Discord, Teams (web), VS Code, Notion, any browser-based or Electron app.

**How it works:**
1. Connect to running Chrome via CDP (Chrome DevTools Protocol) or launch new browser
2. Use CSS selectors for precise, instant element targeting — NO screenshots needed
3. `page.click()`, `page.fill()`, `page.goto()` for all interactions
4. DOM inspection for finding the right selectors
5. 10-50x faster than screenshot+coordinate approach

### Chrome CDP Setup (REQUIRED for browser control)

**⚠️ CRITICAL RULE: NEVER kill/restart Chrome (`taskkill /IM chrome.exe`). This destroys all user's open tabs!**

The user's Chrome is configured to ALWAYS start with CDP enabled:
- Chrome shortcut already includes `--remote-debugging-port=9222` flags
- CDP is available whenever Chrome is running — no restart needed

**Step 1: Check if CDP is available (ALWAYS do this first)**
```bash
curl --noproxy localhost -s http://localhost:9222/json/version
```

**If CDP responds** → Great! Go to Step 2.

**If CDP does NOT respond** (Chrome running without CDP, or Chrome not running):
- **DO NOT** kill Chrome. Instead, tell the user:
  "Chrome 没有开启调试端口。请关闭 Chrome，然后双击桌面的 Chrome-CDP.bat 重新打开。"
- Or if Chrome is not running at all, launch it fresh (safe, no tabs to lose):
  ```bash
  MSYS_NO_PATHCONV=1 "/c/Program Files/Google/Chrome/Application/chrome.exe" \
    --remote-debugging-port=9222 --user-data-dir="C:\\ChromeCDP" \
    --profile-directory=Default --restore-last-session > /dev/null 2>&1 &
  ```

**Step 2: Connect with Playwright**
```javascript
// CRITICAL: Must bypass proxy for localhost
process.env.NO_PROXY = 'localhost,127.0.0.1';
const { chromium } = require('playwright');
const browser = await chromium.connectOverCDP('http://localhost:9222', { timeout: 60000 });
const ctx = browser.contexts()[0];
const page = await ctx.newPage(); // or ctx.pages()[0] for existing tab
```

**Step 3: Automate anything**
```javascript
await page.goto('https://example.com');
await page.click('#button');
await page.fill('input[name="email"]', 'test@test.com');
await page.screenshot({ path: 'verify.png' });
```

### Proven Web App Patterns

**Coremail (Tsinghua email mails.tsinghua.edu.cn):**
- Buttons have spaces: "写 信", "发 送" — use regex `/^写\s*信$/` in `page.evaluate`
- To field: click 150px right of "收件人" label → `keyboard.type(email)` → Enter
- Subject: `input[name="subject"]` — set `.value` + `dispatchEvent(new Event('input'))`
- Body: find iframe with `document.body.contentEditable === 'true'` → set `innerHTML`
- Send button class: `j-tbl-send`
- Wait for "收件箱" text to confirm inbox loaded after login

**General pattern for complex web apps:**
```javascript
// When CSS selectors fail, use page.evaluate to walk the DOM
const result = await page.evaluate(() => {
  const els = document.querySelectorAll('span, button, div');
  for (const el of els) {
    if (/^发\s*送$/.test(el.textContent?.trim()) && el.offsetParent !== null) {
      el.click();
      return true;
    }
  }
  return false;
});
```

### Important Notes
- **⚠️ NEVER `taskkill /IM chrome.exe`** — this destroys all user's open tabs and work!
- **⚠️ NEVER `browser.close()`** — it kills the user's Chrome! Use `process.exit(0)` instead
- **Proxy**: User has v2ray at 127.0.0.1:2080. Always set `NO_PROXY=localhost,127.0.0.1` before Node.js commands
- **Playwright is at** `D:\cc-workspace\node_modules\playwright` (already installed)
- **DPAPI**: Junction approach causes some decrypt warnings (harmless), saved passwords are lost but sessions work after re-login
- **If CDP not available**: Ask user to restart Chrome via `Chrome-CDP.bat`, NEVER force-kill

## Supported Applications

| App | Process Name | Mode | Search Key | Notes |
|-----|-------------|------|------------|-------|
| WeChat | Weixin | Win32 | Ctrl+F | Tested and verified |
| WeCom | WXWork | Win32 | Ctrl+F | Enterprise WeChat |
| DingTalk | DingTalk | Win32 | Ctrl+K | Alibaba's chat |
| Feishu/Lark | Feishu | Win32 | Ctrl+K | ByteDance's chat |
| QQ | QQ | Win32 | Ctrl+F | Tencent QQ |
| Telegram | Telegram | Win32 | Ctrl+K | - |
| Slack | slack | Playwright | Ctrl+K | Electron app |
| Teams | ms-teams | Win32/Playwright | Ctrl+E | - |
| VS Code | Code | Playwright | Ctrl+P | Electron app |
| Any browser | chrome/msedge/firefox | Playwright | - | Via CDP |

## Core Workflow

### Step 1: Identify the target app and automation mode

```python
# Use the app registry to determine process name and mode
python scripts/app_registry.py identify "WeChat"
# Output: { "process": "Weixin", "mode": "win32", "search_key": "Ctrl+F" }
```

### Step 2: Execute the action

**For Win32 native apps:**
```bash
# Send a message to a contact in a chat app
python scripts/desktop_control.py send-message --app weixin --contact "张三" --message "你好"

# Click at specific coordinates
python scripts/desktop_control.py click --app weixin --x 500 --y 400

# Type text into the focused app
python scripts/desktop_control.py type --app weixin --text "Hello World"

# Take a screenshot of a specific app window
python scripts/desktop_control.py screenshot --app weixin --output screenshot.png
```

**For Playwright/Electron apps:**
```bash
# Interact with a web page
python scripts/desktop_control.py web-click --url "http://localhost:3000" --selector "#submit-btn"

# Fill a form field
python scripts/desktop_control.py web-fill --url "http://localhost:3000" --selector "input[name=email]" --text "test@example.com"
```

### Step 3: Visual verification (screenshot feedback loop)

After every action, optionally capture a screenshot and analyze it to verify the action succeeded. This is the key insight from OpenAI's playwright-interactive: **always verify visually**.

```bash
# Take screenshot and return for Claude to analyze
python scripts/desktop_control.py screenshot --app weixin --output verify.png
# Claude reads the screenshot and decides next steps
```

## Key Technical Patterns

### Pattern 1: Chat App Message Sending (Win32)

The universal pattern for sending messages in any chat app:

```
1. FindProcess(process_name) → window handle
2. ShowWindow(handle, SW_RESTORE) + SetForegroundWindow(handle)
3. SendKeys(search_shortcut)        # Open search (Ctrl+F, Ctrl+K, etc.)
4. Clipboard.SetText(contact_name)  # Set contact name
5. SendKeys(Ctrl+V)                 # Paste contact name
6. Sleep(2000)                      # Wait for search results
7. SendKeys(Enter)                  # Select contact
8. Sleep(2500)                      # Wait for chat to load
9. ClickAt(input_area_x, input_area_y)  # CRITICAL: Mouse click to focus input
10. Clipboard.SetText(message)      # Set message
11. SendKeys(Ctrl+V)               # Paste message
12. SendKeys(Enter)                 # Send
```

**Critical insight**: After search+Enter selects a contact, the message input area does NOT automatically get keyboard focus. You MUST use mouse click automation to click on the input area. This was discovered empirically with WeChat and applies to most chat apps.

### Pattern 2: Visual Feedback Loop

```
while not task_complete:
    1. Execute action (click, type, etc.)
    2. Take screenshot
    3. Analyze screenshot (Claude vision)
    4. Determine if action succeeded
    5. If failed → adjust and retry
    6. If succeeded → next action
```

### Pattern 3: Unicode Text Handling

For Chinese/CJK text, always use Unicode code points to avoid encoding issues:

```python
def text_to_char_codes(text):
    return ",".join(str(ord(c)) for c in text)

# In PowerShell, reconstruct from codes:
# [string]::new([char[]]@(20320,22909))  → "你好"
```

### Pattern 4: Clipboard Safety

```powershell
function Set-ClipboardSafe($text) {
    for ($i = 0; $i -lt 5; $i++) {
        try {
            [System.Windows.Forms.Clipboard]::Clear()
            Start-Sleep -Milliseconds 100
            [System.Windows.Forms.Clipboard]::SetText($text)
            return $true
        } catch {
            Start-Sleep -Milliseconds 300
        }
    }
    return $false
}
```

### Pattern 5: Window Position Calculation

Click coordinates are calculated relative to the app window:

```powershell
# Get window rect
$rect = New-Object Win32.RECT
GetWindowRect($hwnd, [ref]$rect)
$winW = $rect.Right - $rect.Left
$winH = $rect.Bottom - $rect.Top

# Chat app input area is typically at bottom-center
$inputX = $rect.Left + [int]($winW * 0.65)
$inputY = $rect.Bottom - [int]($winH * 0.12)
```

## Timing Guidelines

| Operation | Recommended Delay |
|-----------|------------------|
| After ShowWindow/SetForeground | 1000ms |
| After opening search | 600ms |
| After pasting search text | 2000ms |
| After selecting contact (Enter) | 2500ms |
| After clicking input area | 1000ms |
| After pasting message | 800ms |
| Between clipboard Clear and Set | 100ms |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Window not found | Check process name with `Get-Process` |
| Window won't come to foreground | App may be in system tray; activate manually first |
| Clipboard errors | Use retry loop; close other clipboard-heavy apps |
| Wrong contact selected | Use more specific search term (full name/remark) |
| Input area not focused | Adjust click coordinates for the specific app |
| Chinese text garbled | Use Unicode char code arrays instead of literal strings |
| Screenshot is black | Some apps use hardware acceleration; try with software rendering |

## Extending to New Apps

To add support for a new app:

1. Find the process name: `Get-Process | Where-Object { $_.MainWindowTitle -like "*AppName*" }`
2. Identify the search shortcut (usually Ctrl+F or Ctrl+K)
3. Determine the input area position (take a screenshot and measure)
4. Add to the app registry in `scripts/app_registry.py`
5. Test the full send-message flow
6. Add visual verification screenshots
