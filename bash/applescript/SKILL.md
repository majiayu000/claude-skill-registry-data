---
name: applescript
description: 'USE THIS SKILL for AppleScript and JavaScript for Automation (JXA) on macOS — secure script execution, safe input interpolation, application dictionaries, async via osascript, and the security pitfalls that make AppleScript dangerous.'
---

# AppleScript & JXA

Drive macOS apps from the command line via `osascript`. AppleScript and JXA both compile to OSA bytecode and run through the same engine — pick whichever syntax you prefer, but understand both. They have full access to the running user account; treat them like shell scripts that can also click buttons.

## When to Use This Skill

- Driving a macOS GUI app that doesn't have a CLI (Mail, Notes, Calendar, Keynote, etc.)
- Reading or writing properties exposed by an app's scripting dictionary
- Triggering keystrokes or menu items via System Events
- Running shell commands inside an AppleScript block (`do shell script`)
- Wrapping AppleScript inside a Python/Node tool

## Execution Methods

```bash
# AppleScript inline
osascript -e 'tell application "Finder" to activate'

# AppleScript from file
osascript script.scpt

# JXA inline
osascript -l JavaScript -e 'Application("Finder").activate()'

# JXA from file
osascript -l JavaScript automation.js
```

From Python:

```python
import subprocess

result = subprocess.run(
    ['osascript', '-e', script],
    capture_output=True, text=True, timeout=30,
)
return result.stdout.strip(), result.stderr.strip()
```

For long-running scripts, use async:

```python
import asyncio

async def run_script(script: str, timeout: float = 30.0):
    proc = await asyncio.create_subprocess_exec(
        'osascript', '-e', script,
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
    return stdout.decode().strip(), stderr.decode().strip()
```

## Core Principles

1. **Never interpolate untrusted input directly into AppleScript.** AppleScript has no parameterized-query equivalent.
2. **Always use `quoted form of`** for shell arguments inside `do shell script`.
3. **Block administrator-privilege scripts.** `with administrator privileges` triggers the auth dialog and runs as root.
4. **Validate target apps against a blocklist.** Don't let scripts touch Keychain Access, password managers, or System Settings.
5. **Always set timeouts.** `delay 999999` is a valid AppleScript and will hang your subprocess indefinitely.

## Safe Input Interpolation

The dangerous mistake:

```python
# Don't ever do this
user_input = "test\"; do shell script \"rm -rf ~\""
script = f'display dialog "{user_input}"'
subprocess.run(['osascript', '-e', script])
```

The user input contains AppleScript syntax, escapes the string, and runs `rm -rf`. Defense in two layers — escape, and use `quoted form of` for shell content:

```python
class SafeScriptBuilder:
    @staticmethod
    def escape_string(value: str) -> str:
        """Escape a string for AppleScript literal interpolation."""
        return value.replace('\\', '\\\\').replace('"', '\\"')

    @staticmethod
    def build_tell(app_name: str, body: str) -> str:
        """Build a `tell application` block. Validates app name."""
        if not re.match(r'^[a-zA-Z0-9 .]+$', app_name):
            raise ValueError(f"Invalid app name: {app_name!r}")
        # body is assumed to come from a trusted template, NOT user input
        return f'tell application "{SafeScriptBuilder.escape_string(app_name)}"\n{body}\nend tell'

    @staticmethod
    def build_shell(command: str, args: list[str]) -> str:
        """Build a `do shell script` for a known-safe command + arbitrary args.

        Only the args may come from user input. The command must be in an allowlist.
        """
        ALLOWED = {'ls', 'pwd', 'date', 'whoami', 'echo', 'sw_vers'}
        if command not in ALLOWED:
            raise PermissionError(f"Command {command} not in allowlist")
        # Each arg becomes "arg1" -- AppleScript handles the quoting via `quoted form of`
        as_args = [f'quoted form of "{SafeScriptBuilder.escape_string(a)}"' for a in args]
        joined = ' & " " & '.join(as_args) if as_args else '""'
        return f'do shell script "{command} " & {joined}'
```

The key idiom: keep raw user data in AppleScript variables and run them through `quoted form of` before they hit the shell:

```applescript
set userInput to "test; rm -rf ~"
do shell script "echo " & quoted form of userInput
-- Runs: echo 'test; rm -rf ~'  (literal string, no command substitution)
```

## Secure Runner Pattern

If you're exposing AppleScript execution as part of a tool, gate it:

```python
import subprocess, re, logging

class SecurityError(Exception):
    pass

class SecureAppleScriptRunner:
    BLOCKED_PATTERNS = [
        re.compile(r'do shell script.*with administrator', re.IGNORECASE),
        re.compile(r'do shell script.*\bsudo\b', re.IGNORECASE),
        re.compile(r'do shell script.*\brm\s+-r', re.IGNORECASE),
        re.compile(r'do shell script.*curl.*\|.*sh', re.IGNORECASE),
        re.compile(r'keystroke.*password', re.IGNORECASE),
        re.compile(r'system attribute.*password', re.IGNORECASE),
    ]

    BLOCKED_APPS = {
        'Keychain Access', '1Password', 'Bitwarden',
        'System Settings', 'System Preferences',  # both names — Ventura renamed
        'Terminal', 'iTerm', 'iTerm2',
    }

    def __init__(self):
        self.log = logging.getLogger('applescript.security')

    def execute(self, script: str, timeout: float = 30.0) -> tuple[str, str]:
        self._check_patterns(script)
        self._check_apps(script)
        self.log.info('applescript.execute', extra={'script_head': script[:100]})
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Script timed out after {timeout}s")
        return result.stdout.strip(), result.stderr.strip()

    def _check_patterns(self, script: str) -> None:
        for pattern in self.BLOCKED_PATTERNS:
            if pattern.search(script):
                raise SecurityError(f"Blocked pattern matched: {pattern.pattern}")

    def _check_apps(self, script: str) -> None:
        for app in self.BLOCKED_APPS:
            if app.lower() in script.lower():
                raise SecurityError(f"Access to {app} blocked")
```

A blocklist is a defense-in-depth signal, not a primary control. The primary control is: don't give untrusted input the ability to construct arbitrary scripts. If you must, design templates with parameterized slots.

## JXA (JavaScript for Automation)

Same engine, JS syntax. Useful when you need real data structures or async-style flow:

```javascript
class SecureJXA {
  constructor() {
    this.blockedApps = ['Keychain Access', 'Terminal', '1Password'];
  }

  runApp(appName, action, ...args) {
    if (this.blockedApps.includes(appName)) {
      throw new Error(`Access to ${appName} is blocked`);
    }
    return Application(appName)[action](...args);
  }

  safeShell(command) {
    const blocked = [/\brm\s+-rf?\b/, /\bsudo\b/, /curl.*\|.*sh/];
    for (const p of blocked) {
      if (p.test(command)) throw new Error(`Blocked command: ${command}`);
    }
    const app = Application.currentApplication();
    app.includeStandardAdditions = true;
    return app.doShellScript(command);
  }
}
```

JXA has the same security properties as AppleScript — it's the same OSA engine. The JS syntax doesn't make it safer.

## Application Dictionaries

To find out what an app supports, inspect its scripting dictionary:

```bash
# Open in Script Editor for browsing
open -a "Script Editor"
# File > Open Dictionary > pick the app

# Dump as XML
sdef /Applications/Mail.app
```

From Python:

```python
def get_app_dictionary(app_path: str) -> str:
    """Return an app's sdef as XML, or empty string if not scriptable."""
    try:
        result = subprocess.run(
            ['sdef', app_path],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return ''
```

Apps without a scripting dictionary aren't scriptable directly, but you can usually still drive them through System Events (`tell application "System Events" to tell process "AppName" ...`).

## Performance

### Compile and cache scripts

Repeatedly executing the same script through `osascript -e` recompiles each time. For hot scripts, compile once:

```python
import tempfile

class CompiledScriptCache:
    def __init__(self):
        self._cache: dict[str, str] = {}  # script_id -> compiled .scpt path

    def execute(self, script_id: str, source: str, timeout: float = 30.0):
        if script_id not in self._cache:
            fd, path = tempfile.mkstemp(suffix='.scpt')
            subprocess.run(['osacompile', '-o', path, '-e', source], check=True)
            self._cache[script_id] = path
        return subprocess.run(
            ['osascript', self._cache[script_id]],
            capture_output=True, text=True, timeout=timeout,
        )
```

### Batch operations into one script

Each `osascript` invocation is a process spawn (~50-100ms). Combine related operations:

```python
# Slow: three process launches
subprocess.run(['osascript', '-e', f'tell app "{app}" to set bounds of window 1 to {{0, 0, 800, 600}}'])
subprocess.run(['osascript', '-e', f'tell app "{app}" to activate'])
subprocess.run(['osascript', '-e', f'tell app "{app}" to set zoomed of window 1 to false'])

# Fast: one process launch
script = f'''
tell application "{app}"
    set bounds of window 1 to {{0, 0, 800, 600}}
    set zoomed of window 1 to false
    activate
end tell
'''
subprocess.run(['osascript', '-e', script])
```

### Filter inside AppleScript, not after

```applescript
-- Bad: returns everything, you filter in Python
tell application "System Events"
    get properties of every window of every process
end tell

-- Good: filters in AppleScript
tell application "System Events"
    set windowList to {}
    repeat with proc in (processes whose visible is true)
        if (count of windows of proc) > 0 then
            set end of windowList to {name:name of proc, title:name of window 1 of proc}
        end if
    end repeat
    return windowList
end tell
```

## Critical Vulnerabilities (CWE Mapping)

| CWE     | Severity | Issue                                                    | Mitigation                                          |
| ------- | -------- | -------------------------------------------------------- | --------------------------------------------------- |
| CWE-78  | CRITICAL | Command injection via `do shell script`                  | Always use `quoted form of`                         |
| CWE-269 | CRITICAL | Privilege escalation via `with administrator privileges` | Block this pattern outright                         |
| CWE-94  | HIGH     | Script injection via interpolation                       | Never interpolate untrusted data into script source |
| CWE-22  | HIGH     | Path traversal in file operations                        | Validate paths, use `POSIX path of` carefully       |
| CWE-200 | MEDIUM   | Information disclosure                                   | Filter output, redact sensitive fields              |

## Anti-Patterns

| Don't                                          | Do                                        |
| ---------------------------------------------- | ----------------------------------------- |
| Interpolate untrusted input into script source | Build with templates and known-safe slots |
| Use `do shell script` without `quoted form of` | Always wrap shell args                    |
| Allow `with administrator privileges`          | Block the pattern                         |
| Run user-provided scripts                      | Allowlist of templates                    |
| Skip timeouts                                  | Always set one, default 30s               |
| Spawn `osascript` per micro-operation          | Batch related ops into one script         |

## Pre-Deployment Checklist

- [ ] Input sanitization wraps every interpolation
- [ ] `quoted form of` used for every shell arg
- [ ] Blocked-pattern regex covers admin, sudo, rm -r, curl|sh
- [ ] Application blocklist includes password managers, Keychain, System Settings
- [ ] Timeout set on every `osascript` invocation
- [ ] Audit logging captures script-head, target-app, exit code
- [ ] Hot scripts compiled to `.scpt` and cached
- [ ] Tested with hostile input (`"; do shell script "..."`)

## References

- `references/advanced-patterns.md` — observer patterns, AppleEvent timing, hybrid Python/AppleScript flows
- `references/security-examples.md` — full attack/defense pairs with CVE references
- `references/threat-model.md` — STRIDE walkthrough for an AppleScript-driven tool
