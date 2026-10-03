---
name: hermes-python-script-wrapper-for-shell-cron
description: Diagnose and safely document Hermes cron script interpreter mismatches, especially when shell scripts are executed as Python or Python wrappers are executed as shell.
---

# Hermes Python Wrapper for Shell Cron

## Purpose
Provide a safe workflow for diagnosing Hermes cron `script=` interpreter mismatches. The common failure modes are shell syntax being interpreted by Python, or Python code being interpreted by shell. The default workflow only diagnoses and proposes a wrapper plan; writing wrapper files requires user approval.

## When to use
- A Hermes cron job fails with syntax errors around shell constructs such as strict mode, heredocs, or bash conditionals.
- A cron job fails with shell errors while the entry file contains Python code.
- The job's configured script extension does not match the interpreter used by the scheduler.
- A user wants a stable wrapper pattern for cron scripts while keeping the existing script path.

## Safety rules
- Default workflow is read-only.
- Do not edit scripts, change permissions, trigger jobs, or update cron definitions without explicit approval.
- Do not copy production scripts into public documentation.
- Replace real paths with `<PROJECT_ROOT>`, `<SCRIPT_PATH>`, `<WRAPPER_PATH>`, or `<IMPLEMENTATION_SCRIPT>`.
- Do not expose script contents if they include credentials, private URLs, tokens, or production data.

## Read-only workflow
1. Identify the failing Hermes cron job and script path from metadata or user-provided error context.
2. Read the error summary and classify the mismatch:
   - shell syntax reported by Python means the entry is being executed as Python;
   - Python syntax reported by shell means the entry is being executed as shell.
3. Inspect cron metadata to determine how the scheduler invokes `script=` for that job.
4. Inspect only the minimum safe lines of the entry script needed to identify its language and shebang.
5. Compare the entry script language, extension, shebang, and scheduler invocation mode.
6. Produce a wrapper plan using placeholders, without writing files.
7. Include a verification plan that compares direct implementation execution with scheduler-style entry execution.

## Evidence to collect
- Redacted job name or identifier.
- Configured script path as `<SCRIPT_PATH>`.
- Error class and first safe error line.
- Detected script language: shell, Python, or mixed.
- Scheduler invocation mode if known.
- Whether arguments need to be forwarded.
- Whether stdout/stderr and exit code must be preserved.

## Stop conditions
- The script contains secrets or production-specific data that cannot be safely summarized.
- The scheduler invocation mode is unknown and cannot be inferred read-only.
- Fixing requires editing the script, chmod, cron update, or a manual job run without approval.
- The proposed wrapper might alter stdout/stderr or exit-code semantics.

## Optional user-approved actions
Only after explicit user approval:
- Move implementation content to `<IMPLEMENTATION_SCRIPT>`.
- Replace the original entry with a wrapper appropriate for the real invocation mode.
- Set execute permissions.
- Run syntax checks and controlled dry-runs.
- Trigger or run the cron job once to verify recovery.

### Generic wrapper patterns
Use these only as templates after approval.

Python entry that delegates to shell:
```python
#!/usr/bin/env python3
import subprocess
import sys

SCRIPT = "<IMPLEMENTATION_SCRIPT>"
result = subprocess.run(["/usr/bin/env", "bash", SCRIPT] + sys.argv[1:])
raise SystemExit(result.returncode)
```

Shell entry that delegates to shell implementation:
```bash
#!/usr/bin/env bash
set -euo pipefail
SCRIPT="<IMPLEMENTATION_SCRIPT>"
exec /usr/bin/env bash "$SCRIPT" "$@"
```

## Final report format
```text
Summary: <interpreter mismatch diagnosis>
Job: <redacted job name/id>
Script: <SCRIPT_PATH>
Observed error: <safe summarized error>
Detected mismatch: <shell-as-python / python-as-shell / unknown>
Read-only evidence: <bullets>
Wrapper plan: <high-level plan with placeholders>
Verification plan: <syntax/direct/scheduler-style checks>
Needs approval before changes: yes
```
