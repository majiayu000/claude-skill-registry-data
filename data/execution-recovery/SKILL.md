---
name: execution-recovery
description: Handle common execution failures with specialized recovery strategies. Fix syntax errors, import/dependency issues, path/file problems, permission denial, and connection timeouts. Use proactively when encountering errors or as automatic recovery mechanism.
allowed-tools: Read, Edit, Execute, Grep
---

# Execution Recovery

Apex2's execution optimization suite implemented as a Claude Code skill. Provides robust recovery from common execution failures.

## Instructions

When invoked (automatically on errors or explicitly when help is needed), diagnose and fix execution problems:

### 1. Immediate Error Triage
Quickly categorize the error type to apply the right recovery strategy:

**Syntax Errors:**
- Python: SyntaxError, IndentationError, NameError
- JavaScript: SyntaxError, ReferenceError
- Shell: syntax error near token, unexpected operator

**Import/Module Errors:**
- ModuleNotFoundError, ImportError (Python)
- Cannot find module (Node.js)
- dependency resolution failures

**Path/File Issues:**
- No such file or directory
- Permission denied
- File already exists
- Directory not empty

**Network/Connection Problems:**
- Connection refused, timeout
- DNS resolution failures
- Authentication failures
- Rate limiting

### 2. Recovery Strategies by Error Type

#### Syntax Error Recovery
1. **Diagnose the specific line**:
   ```bash
   # Python syntax checking
   python -m py_compile filename.py
   # or specific line diagnosis
   python -c "import ast; ast.parse(open('filename.py').read())"
   
   # JavaScript syntax checking  
   node -c filename.js
   npm install eslint --save-dev && npx eslint filename.js
   ```

2. **Common fixes to apply**:
   - Fix missing parenthesis, brackets, quotes
   - Correct indentation (Python-specific)
   - Add missing semicolons (JS-specific)
   - Escape special characters in strings
   - Fix function call syntax

3. **Heredoc Management** (for shell scripts):
   ```bash
   # Validate heredoc syntax
   cat << 'EOF' > script.sh
   # script content here
   EOF
   ```

#### Import/Dependency Recovery
1. **Diagnose missing dependencies**:
   ```bash
   # Python imports
   python -c "import missing_module" 2>&1 | grep ModuleNotFoundError
   
   # Node.js
   npm ls missing-package
   ```
   
2. **Install solutions**:
   ```bash
   # Python
   pip install missing-package
   # Add to requirements.txt
   
   # Node.js
   npm install missing-package
   # Add to package.json dependencies
   ```

3. **Version conflicts**:
   ```bash
   # Check versions
   pip show package-name
   npm list package-name
   
   # Install specific version
   pip install package==version
   npm install package@version
   ```

#### Path/File Recovery
1. **Path validation**:
   ```bash
   # Check if file exists
   ls -la file-path
   dirname file-path && ls -la $(dirname file-path)
   
   # Current working directory
   pwd
   
   # Relative vs absolute path testing
   echo $(pwd)/relative-path
   ```

2. **Permission fixes**:
   ```bash
   # Make executable
   chmod +x script.sh
   
   # Read/write permissions
   chmod 644 file.txt
   chmod 755 directory/
   ```

3. **Directory creation**:
   ```bash
   # Create parents as needed
   mkdir -p path/to/directory
   
   # Safe file creation
   touch new-file.txt
   ```

#### Network/Connection Recovery
1. **Connectivity testing**:
   ```bash
   # Test basic connectivity
   ping -c 3 example.com
   curl -I https://example.com
   
   # Check specific ports
   telnet host port
   nc -zv host port
   ```

2. **DNS resolution**:
   ```bash
   # Check DNS
   nslookup hostname
   dig hostname
   
   # Test different DNS servers
   nslookup hostname 8.8.8.8
   ```

3. **Authentication and retries**:
   ```bash
   # Retry with exponential backoff
   # Use auth tokens appropriately
   # Check rate limits and wait periods
   ```

### 3. Advanced Recovery Techniques

#### Heredoc Repair (for shell scripts)
```bash
# Fix indentation in heredoc
cat << 'EOF' > fixed-script.sh
#!/bin/bash
echo "Fix indentation issues"
# Other commands
EOF
```

#### Session Recovery
```bash
# Detect stuck tmux/session issues
tmux list-sessions
tmux kill-session -t session-name

# Start fresh session
tmux new-session -d -s work-session
```

#### Long-Running Task Management
```bash
# Resume interrupted tasks
# Check progress of long operations
# Implement timeouts for very long commands
timeout 300s command-that-might-hang
```

### 4. Systematic Debugging Process

1. **Capture the exact error message**
2. **Reproduce the error to isolate cause**
3. **Check recent changes that might have broken things**
4. **Apply the appropriate recovery strategy**
5. **Verify the fix works before proceeding**

### 5. Prevention Strategies

Add safeguards to prevent recurrence:
- Input validation in scripts
- Error handling that catches common failures
- Automated testing before deployment
- Configuration validation on startup

## Error Categories and Fixes

### Docker/Microservice Issues
```bash
# Container not found
docker ps -a
docker logs container-name

# Port conflicts
netstat -tulpn | grep port-number
docker run -p different-port:port
```

### Database Connection Problems
```bash
# Connection testing
psql -h host -U user -d database -c "SELECT 1;"
mysql -h host -u user -e "SELECT 1;"

# Service status
systemctl status postgresql
systemctl status mysql
```

### Git Repository Issues
```bash
# Permission denied
git config --global core.sharedRepository group

# Corrupted repository
git fsck
git gc --prune=now
```

## Output Format

Provide structured recovery report:

```
Error Analysis:
  Type: [syntax/import/path/network/other]
  Severity: [low/medium/high]
  Criticality: [blocking/warning/info]

Root Cause:
  Immediate cause: [what happened]
  Underlying issue: [why it happened]
  Contributing factors: [other factors]

Recovery Applied:
  Step 1: [action taken]
  Result: [success/failure]
  Step 2: [next action if needed]
  Result: [success/failure]

Solution Details:
  Code fixed: [show corrected code]
  Command executed: [show command]
  Changes made: [describe modifications]

Verification:
  Test performed: [how fix was verified]
  Result: [successful/unsuccessful]
  Additional steps: [if needed]

Prevention:
  Future safeguards: [how to prevent recurrence]
  Monitoring: [what to watch]
  Documentation: [what to update]
```

## When to Use

This recovery skill is designed for:
- Automatic recovery when execution commands fail
- Manual intervention when complex errors occur
- Debugging mysterious failures
- Learning from mistakes to prevent recurrence
- Building robust execution pipelines

The goal is to turn execution failures into learning opportunities, with the system becoming more reliable through each recovery.
