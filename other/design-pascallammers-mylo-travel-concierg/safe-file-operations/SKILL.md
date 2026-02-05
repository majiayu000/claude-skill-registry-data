---
name: safe-file-operations
description: "Guidelines for safely executing destructive file operations (mv, rm, cp). Use when performing file moves, deletions, or overwrites to prevent accidental data loss. Provides verification steps and best practices for batch operations."
---

# Safe File Operations

**CRITICAL:** Before running any potentially destructive commands (mv, rm, cp with overwrite, etc.), ALWAYS verify the environment first:

1. **Check working directory:** Run `pwd` to confirm you're in the expected location
2. **Verify file existence:** Use `ls -la <file>` to check files exist and are what you expect
3. **Check file types:** Verify if files are regular files or symlinks before operations
4. **Test on one file first:** For batch operations, test the command on a single file before looping
5. **Verify after operations:** Check the result with `ls -la` to confirm success

**Example safe workflow:**
```bash
# DON'T DO THIS:
mv CLAUDE.md AGENTS.md  # Blind execution

# DO THIS INSTEAD:
pwd                      # Verify location
ls -la CLAUDE.md         # Confirm file exists
mv CLAUDE.md AGENTS.md   # Execute
ls -la AGENTS.md         # Verify success
```

**For batch operations:**
```bash
# Test on ONE file first
cd /path/to/first/dir && pwd && ls -la CLAUDE.md && mv CLAUDE.md AGENTS.md && ls -la AGENTS.md

# Only after confirming success, proceed with batch
for dir in ...; do ...; done
```

The user is trusting you with their files. Be careful!
