---
name: xplat-checks
description: Cross-platform compatibility checking tools. Detects path issues, line endings, environment variables, shell commands, and other patterns that break on Windows or Linux.
---

# Cross-Platform Checks Skill

Scripts for detecting cross-platform compatibility issues in Python code.

## Scripts

### check_paths.py

Detect hardcoded path separators.

```bash
python .claude/skills/xplat-checks/scripts/check_paths.py [directory]
```

Finds:
- Hardcoded forward slashes in string paths
- Hardcoded backslashes
- Forward slashes inside os.path.join()

### check_line_endings.py

Detect line ending issues.

```bash
python .claude/skills/xplat-checks/scripts/check_line_endings.py [directory]
```

Finds:
- Files with CRLF line endings
- Mixed line endings in single file
- Missing .gitattributes

### check_env_vars.py

Find platform-specific environment variable usage.

```bash
python .claude/skills/xplat-checks/scripts/check_env_vars.py [directory]
```

Finds:
- $HOME, $USER (Unix-only)
- %USERPROFILE%, %USERNAME%, %TEMP% (Windows-only)

### check_case_sensitivity.py

Detect case sensitivity issues.

```bash
python .claude/skills/xplat-checks/scripts/check_case_sensitivity.py [directory]
```

Finds:
- Files differing only by case
- Import statements with wrong case

### check_shell_commands.py

Detect shell command compatibility issues.

```bash
python .claude/skills/xplat-checks/scripts/check_shell_commands.py [directory]
```

Finds:
- os.system() calls
- subprocess with shell=True
- Bash-specific commands

### check_temp_paths.py

Find hardcoded temp directory paths.

```bash
python .claude/skills/xplat-checks/scripts/check_temp_paths.py [directory]
```

Finds:
- /tmp references
- C:\Temp references
- /var/tmp references

## Output Format

All scripts output JSON:

```json
{
  "status": "PASS|FAIL",
  "files_scanned": 156,
  "issues": [
    {
      "file": "src/config.py",
      "line": 47,
      "column": 12,
      "issue": "Hardcoded forward slash in path",
      "code": "config_path = 'data/config.yaml'",
      "suggestion": "Use Path('data') / 'config.yaml'"
    }
  ]
}
```

## Fix Reference

| Issue | Bad | Good |
|-------|-----|------|
| Path separator | `"data/file.txt"` | `Path("data") / "file.txt"` |
| Home directory | `os.environ["HOME"]` | `Path.home()` |
| Temp directory | `"/tmp/file"` | `Path(tempfile.gettempdir()) / "file"` |
| Shell command | `os.system("rm -rf x")` | `shutil.rmtree("x")` |
| Username | `os.environ["USER"]` | `getpass.getuser()` |
