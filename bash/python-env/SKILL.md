---
name: python-env
description: Guidelines and requirements for the Python environment setup, running tests (pytest), path normalization, and MCP/stdio IPC troubleshooting on this workspace.
---
# Python Environment & Testing Guide

This skill defines the requirements, environment details, and execution commands for Python development and automated testing in this repository.

---

## 1. Environment Rigging & Python Path (CRITICAL)

On Windows systems, the default `python` or `pytest` commands in the environment PATH might resolve to a restricted shell Python (such as MSYS2/MinGW) which lacks standard package management (`pip`, `pytest`).

* **For standard development machines (default Windows Store Python)**:
  * **Python Path**: `$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\python.exe`
  * **Pip Command**: `$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\python.exe -m pip`
  * **Dependency Installation**:
    ```powershell
    & "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\python.exe" -m pip install -r Tests/requirements.txt --user
    ```
  * **Running the Test Suite**:
    ```powershell
    powershell -File .\run_tests.ps1
    # OR
    & "$env:USERPROFILE\AppData\Local\Microsoft\WindowsApps\python.exe" run_tests.py
    ```
* **For other developer workspaces or CI environments**:
  * Locate the standard user python interpreter or virtual environment.
  * Install dependencies: `python -m pip install -r Tests/requirements.txt --user`.
  * Run tests using the PowerShell runner wrapper: `powershell -File .\run_tests.ps1` (it will automatically resolve the correct environment variables and DLL folders).

---

## 2. C++ Builds & Compilation

Unreal Engine builds are managed via the Unreal Automation Tool (UAT).
* To prevent conflicting concurrent build session locks, you must set the mutex bypass environment variable before compilation:
  ```powershell
  $env:uebp_UATMutexNoWait = '1'
  powershell -ExecutionPolicy Bypass -File .\build_plugin.ps1 -NoZip
  ```

---

## 3. Path Normalization on Windows

Windows is case-insensitive, but SQLite queries, file watchers, and C++ Clang parser paths can perform case-sensitive comparisons or output mixed slashes (e.g. `c:\` vs `C:\` or `/` vs `\`).
* **Rule**: Always normalize file paths before performing lookups, indexing, or unit test assertions:
  ```python
  normalized_path = os.path.normcase(os.path.abspath(path))
  ```

---

## 4. MCP JSON-RPC & Stdio IPC Pitfalls

If you are developing or running the External Python MCP server or any stdio-based subprocesses:
1. **Unbuffered Output**: Python buffers stdout by default when piped. This will hang JSON-RPC handshake readers. Always launch python subprocesses with the `-u` (unbuffered) flag:
   ```bash
   python -u -m UnrealEngine.ExternalServer.src.main
   ```
2. **Stdout Pollution**: The stdio channel is dedicated solely to JSON-RPC messages. Any logs, third-party logs, or subprocess commands (like `pip install`) that write raw text to `stdout` will pollute the channel and crash the client parser.
   * **Rule**: Always redirect stdout of internal commands to `stderr` or `subprocess.DEVNULL`:
     ```python
     subprocess.run([sys.executable, "-m", "pip", "install", ...], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
     ```
3. **Non-Blocking Handshake**: Do not perform heavy synchronous blocking actions (like AST parsing or index building) during the MCP server startup lifecycle. Move heavy initialization to a background worker thread so the stdio initialization handshake completes immediately.

---

## 5. Unreal Engine Python API Search

When writing Python scripts to automate tasks in Unreal Engine:
1. **Never guess API signatures**: Unreal Engine Python API methods frequently change or deprecate across engine versions (e.g. UE 5.8 vs 5.4).
2. **Use Vector Search**: Query `search_vector_db` with terms like `"unreal.SourceControl"` or `"screenshot python"` to retrieve the exact class, function, and parameter signatures parsed directly from `unreal.pyi`.

