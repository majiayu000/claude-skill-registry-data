---
name: logic-vulnerabilities
description: File descriptor abuse, race conditions, and TOCTOU vulnerabilities
---

# Logic Vulnerabilities

Exploits targeting program logic rather than memory corruption.

---

## 1. File Descriptor (FD) Abuse

**Concept:** Manipulate which file a hardcoded FD refers to.

**Signals:**
- Program uses constant FD (e.g., `read(3, buf, n)`)
- FD assignment can be influenced before target code runs

**FD basics:**
```
0 = stdin, 1 = stdout, 2 = stderr
3+ = assigned in order by open()
```

**Approach A - Claim target FD:**
```
1. Close lower FDs to influence assignment
2. Open desired file (gets lowest available FD)
3. dup2() to target FD number
4. Execute vulnerable program
```

**Approach B - FD exhaustion:**
```
1. Open many files to consume FD numbers
2. Next open() returns predictable FD
```

**Approach C - Symlink redirection:**
```
1. Program opens user-controlled path
2. Create symlink pointing to sensitive file
```

---

## 2. TOCTOU (Time-of-Check to Time-of-Use)

**Concept:** Change what a path refers to between validation and use.

**Signals:**
- Check: `stat()`, `access()`, `lstat()`
- Gap/delay
- Use: `open()`, `read()`, `exec()`
- Path-based (not FD-based) operations

**The race window:**
```
Victim:    [CHECK path] ----delay---- [USE path]
Attacker:              [SWAP target]
```

**Approach A - Symlink race:**
```
Thread 1: Rapidly flip symlink between allowed and sensitive targets
Thread 2: Repeatedly trigger victim until race succeeds
```

**Approach B - Rename race:**
```
Rapidly rename/swap files at target path
```

**Improving success rate:**
- Multiple racing processes
- Tune timing based on victim's check-use gap
- Use inotify to detect access and trigger swap

---

## Detection Patterns

**FD abuse indicators:**
```c
// Hardcoded FD without validation
read(3, buf, size);

// Sequential FD assumption
int fd = open(path, O_RDONLY);
// Assumes fd == 3
```

**TOCTOU indicators:**
```c
// Vulnerable: path-based check then use
if (access(path, R_OK) == 0) {
    fd = open(path, O_RDONLY);  // Race window!
}

// Safer: FD-based throughout
fd = open(path, O_RDONLY);
fstat(fd, &st);  // Uses FD, not path
```

---

## Debugging

```bash
# Trace FD operations
strace -e trace=open,openat,read,write,dup2 <program>

# Watch file access for timing
inotifywait -m <path> -e access
```

---

## Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| O_NOFOLLOW | Symlinks not followed | Use rename instead |
| openat() | FD-relative paths | Target the directory FD |
| Atomic operations | No race window | Different approach needed |
| Low success rate | Narrow window | More processes, better timing |
