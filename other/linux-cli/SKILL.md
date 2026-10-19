---
name: linux-cli
description: >
  Execute commands and manipulate text, files, and processes safely in GNU/Linux
  environments. Use when composing shell pipelines, finding files, processing
  structured text with grep, sed, and awk, managing system processes, or
  diagnosing command failures using exit codes.
compatibility: >
  Agent Skills-compatible coding agents with access to a Linux terminal
  or shell environment.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "linux, cli, bash, text-processing, pipes, processes"
  topics: "operating-systems, devtools"
---

# Linux CLI Fundamentals

The Linux command-line environment provides high-throughput composability via pipes and text streams. Effective, safe agent execution requires disciplined text processing, robust quote handling, awareness of exit statuses, and a clear distinction between read-only inspection and state-altering commands.

## Core Rules

1. **Quote variable expansions and paths**: Always protect paths containing whitespace or special characters with double quotes (`"$path"`).
2. **Distinguish read-only inspection from mutation**: Commands like `cat`, `grep`, `find`, `ps`, and `df` are safe to explore. Commands like `rm`, `mv`, `chmod`, `kill`, and `truncate` alter state and must be verified before execution.
3. **Never run unbounded searches**: Always limit recursion depth (`find . -maxdepth 3`) or use modern alternatives like `rg` (ripgrep) that respect `.gitignore`.
4. **Inspect exit statuses**: A command returning a non-zero exit code indicates failure. Check `$?` or use pipefail when chaining commands.
5. **Beware of catastrophic wildcards**: Never run `rm -rf *` or `chown -R user *` in unverified or root directories.

---

## 1. File Inspection and Search

### Finding Files Safely
```bash
# Find files by name without crossing filesystem boundaries
find . -maxdepth 4 -type f -name "*.py" -not -path "*/.*"

# Find files modified in the last 24 hours
find /var/log -type f -mtime -1 -name "*.log"

# Find files safely handling spaces and special characters with null delimiters
find . -type f -name "*.tmp" -print0 | xargs -0 rm -f
```

### High-Performance Search with `grep` and `rg`
```bash
# Recursive search with line numbers, ignoring binary files
grep -rnI --exclude-dir={.git,node_modules,.venv} "DATABASE_URL" .

# Preferred if installed: ripgrep (respects .gitignore automatically)
rg -n "DATABASE_URL"
```

---

## 2. Text Processing: Streams, Sed, and Awk

### Streams and Redirection
- `command > file`: Overwrite stdout to file.
- `command >> file`: Append stdout to file.
- `command 2>&1`: Redirect stderr to stdout.
- `command &> file`: Overwrite both stdout and stderr to file.
- `command < file`: Read stdin from file.
- `command1 | command2`: Stream stdout of command1 to stdin of command2.

### Stream Editing with `sed`
Use `sed` for stream substitution without opening interactive editors:
```bash
# Replace first occurrence of pattern per line
sed 's/http:\/\/localhost/https:\/\/api.example.com/' config.json

# Replace all occurrences globally and output to stdout
sed 's/debug = True/debug = False/g' settings.py

# In-place editing (GNU sed):
sed -i 's/OLD_HOST/NEW_HOST/g' /etc/hosts
# Note on macOS (BSD sed): requires empty extension: sed -i '' 's/.../.../g'
```

### Columnar Processing with `awk`
`awk` excels at delimited text and columnar output:
```bash
# Print columns 1 and 3 of colon-delimited /etc/passwd
awk -F: '{print $1, $3}' /etc/passwd

# Filter rows where column 5 (disk usage %) is greater than 80
df -h | awk 'NR>1 {gsub("%","",$5); if ($5 > 80) print $6, $5"%"}'

# Calculate the sum of numbers in the first column
cat numbers.txt | awk '{sum += $1} END {print sum}'
```

---

## 3. Process Inspection and Management

### Identifying Processes
```bash
# View active processes with CPU and Memory utilization
ps aux | grep "[n]ginx"

# Show process hierarchy with PIDs
pstree -p

# Real-time summary
top -b -n 1 | head -n 20
```

### Terminating Processes Safely
Always attempt graceful termination before sending unconditional kill signals:
```bash
# 1. Send SIGTERM (15) to request graceful shutdown
kill -15 <PID>
# Wait 3-5 seconds and verify with ps -p <PID>

# 2. Only if the process remains unresponsive, send SIGKILL (9)
kill -9 <PID>

# Terminate by process name pattern
pkill -15 -f "worker.py"
```

---

## 4. Exit Codes and Pipeline Integrity

Every Linux command produces an exit code between `0` (success) and `255` (failure).

```bash
grep -q "ACTIVE" status.txt
if [ $? -eq 0 ]; then
  echo "System is active"
else
  echo "System inactive or file missing"
fi
```

### Pipeline Exit Code Trap
By default in bash, a pipeline `cmd1 | cmd2 | cmd3` returns the exit code of `cmd3`, even if `cmd1` crashed.
To capture failures anywhere in a pipeline:
```bash
set -o pipefail
cmd1 | cmd2 | cmd3
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `cat file | grep pattern` | Useless use of `cat` process | `grep pattern file` |
| `for file in $(ls *.txt)` | Fails on filenames containing whitespace or newlines | Use `for file in *.txt` or `find ... -print0` |
| `kill -9` as first resort | Leaves sockets open, lockfiles stranded, or data unwritten | Start with `SIGTERM` (`kill -15`), allow cleanup |
| `rm -rf $DIR/*` when `DIR` is unset | Evaluates to `rm -rf /*`, destroying the filesystem | Guard variables: `rm -rf "${DIR:?}/"*` |
| Using GNU flags on macOS BSD tools | Script crashes with illegal option | Use portable POSIX flags or detect OS |

---

## 6. Real-World Scenarios

### Scenario A: Extracting Top Memory-Consuming Processes
```bash
# Sort processes by resident memory size (%MEM) descending, displaying top 5
ps axo pid,user,%mem,%cpu,comm --sort=-%mem | head -n 6
```

### Scenario B: Extracting Unique Client IPs from Access Log
```bash
# Parse Apache/Nginx combined log, extract IP (field 1), count occurrences, sort by frequency
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr | head -n 10
```

---

## 7. Verification Checklist

- [ ] All variable references and file paths in commands are double-quoted.
- [ ] Command exit codes (`$?`) are validated after critical operations.
- [ ] In-place file edits (`sed -i`) have backups or are verified in git before running.
- [ ] Non-zero exit codes are diagnosed before proceeding to dependent steps.
