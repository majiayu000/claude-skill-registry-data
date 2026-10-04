---
name: webapp-testing
description: |
  Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and managing server processes. Trigger when asked to write browser tests, run web automation scripts, debug frontend components, inspect DOM elements, or launch webapps with local servers. Keywords: webapp-testing, with_server.py, playwright, sync_playwright, chromium, networkidle, wait_for_selector, screenshot.

  Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and managing server processes. Trigger when asked to write browser tests, run web automation scripts, debug frontend components, inspect DOM elements, or launch webapps with local servers. Keywords: webapp-testing, with_server.py, playwright, sync_playwright, chromium, networkidle, wait_for_selector, screenshot.

license: Complete terms in LICENSE.txt
---

# Web Application Testing - Playwright Workflows & Standards

A professional testing framework using Playwright and server lifecycles to validate web applications with speed and reliability.

## Progressive Disclosure & Helper Utilities

This skill relies on local utility scripts in `scripts/` and examples in `examples/`. Rather than parsing or reading their code directly, execute them as black boxes:

- **Server Manager**: `scripts/with_server.py` manages one or more server lifecycles during testing. Execute `python scripts/with_server.py --help` to verify CLI args.
- **Reference Implementations**: Refer to files under `examples/` (like `element_discovery.py` or `console_logging.py`) to copy boilerplate for common selector and logging setups.

## Freedom Calibration & Constraints
- **Constraint Level: Medium**
  - **High Rigidity**: All browser processes must run headlessly (`headless=True`), and elements must be interacted with using explicit wait states (no raw `time.sleep`).
  - **Medium Rigidity**: Usage of the `with_server.py` runner to run tests in CI or headless local servers.
  - **High Freedom**: Selection of assertion libraries, DOM traversal patterns, and custom reporting structures.

## Decision Tree: Choosing the Server & Automation Framework

```
What type of web application target is being tested?
 ├─ Pure Static HTML File (No Server)
 │   └─ Open file directly using local path syntax
 │       └─ Code: page.goto("file:///absolute/path/to/index.html")
 ├─ Single-Process Server Webapp (Node/Vite, Flask, Django)
 │   └─ Run test script wrapped with single process wrapper
 │       └─ Command: python scripts/with_server.py --server "npm run dev" --port 5173 -- python test_script.py
 └─ Multi-Service Environment (Separate Frontend and Backend API)
     └─ Run test script wrapping both processes
         └─ Command: python scripts/with_server.py --server "npm run backend" --port 8000 --server "npm run frontend" --port 3000 -- python test_script.py
```

## Professional Mindset & Design Principles
1. **Determinism (Anti-Flakiness)**: Avoid static waits at all costs. Web applications load asynchronously. Always pair actions (clicks, navigation) with expectation states (locator visible, network idle).
2. **Reconnaissance-then-Action**: When debugging headless test failures:
   - Capture full-page screenshots to check layout states.
   - Inspect console logs programmatically to catch uncaught JavaScript exceptions.
   - Dump DOM content to look for text fragments when element matches fail.
3. **Clean Teardowns**: Always close pages, contexts, and browsers within `try-finally` blocks or context managers to prevent orphaned browser processes from hogging system memory.

---

## Core Automation Patterns

### 1. Robust Script Boilerplate (With Error Capturing & Logs)
```python
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_page()
        
        # Capture console messages
        context.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
        
        try:
            # Navigate to local server
            context.goto("http://localhost:5173")
            context.wait_for_load_state("networkidle")
            
            # Assert element visibility before acting
            button = context.locator("button#submit-action")
            button.wait_for(state="visible", timeout=5000)
            button.click()
            
            # Verify result state
            result = context.locator(".success-message")
            result.wait_for(state="visible", timeout=5000)
            assert "Saved successfully" in result.inner_text()
            
        except Exception as e:
            # Capture diagnostic screenshot on failure
            context.screenshot(path="error_diagnostic.png", full_page=True)
            print(f"Test Execution Failed: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    run_test()
```

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** use static `time.sleep()` | Hardcoded pauses slow down suites and cause flaky tests under varying CPU loads. | Use `locator.wait_for(state='visible')` or `page.wait_for_selector()`. |
| **NEVER** launch in headed mode (`headless=False`) | Running headed browsers in containerized, CI, or headless CLI environments throws display crashes. | Always use `p.chromium.launch(headless=True)`. |
| **NEVER** ignore page errors / console logs | Silent UI crashes (uncaught JS exceptions) leave tests failing without context. | Bind console events `context.on("console", ...)` or page error listeners. |
| **NEVER** make assertions on unstable DOM states | Checking inner text immediately after click without waiting for load causes race conditions. | Wait for the specific element containing the expected text to load. |
| **NEVER** hardcode server setup script within tests | Bundling server start commands (like subprocess startup) in testing scripts makes processes leak on crash. | Delegate server lifecycle to `scripts/with_server.py`. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: Port conflict / Server address already in use
- **Root Cause**: A previously run server crashed without releasing the port, or another process is occupying the required testing port.
- **Fallback**:
  1. Kill the process running on that port manually (e.g., `fuser -k 5173/tcp` or `kill -9 $(lsof -t -i:5173)`).
  2. Configure a dynamic port or pass an alternate port to the test suite script and server launcher:
     ```bash
     python scripts/with_server.py --server "npm run dev -- --port 5174" --port 5174 -- python test_script.py
     ```

### Scenario 2: TimeoutError: waiting for selector/locator
- **Root Cause**: Element is dynamically generated, slow API response, or selector is incorrect.
- **Fallback**:
  1. Increase the wait timeout threshold to confirm if it's a speed issue: `button.wait_for(state="visible", timeout=15000)`.
  2. Take a screenshot right before the failure to inspect what is rendered: `page.screenshot(path="timeout_debug.png")`.
  3. Verify if the selector text/ID matches the current DOM snapshot.

### Scenario 3: Click Intercepted (element not clickable)
- **Root Cause**: A loading spinner, modal dialog overlay, or floating navbar is physically blocking the target element.
- **Fallback**:
  1. Wait for the blocking element to become hidden: `page.locator(".spinner").wait_for(state="hidden")`.
  2. Force the click event directly via JavaScript (bypasses physical intersection checks):
     ```python
     page.locator("button#submit").click(force=True)
     ```


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
