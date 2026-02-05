---
name: SystematicDebugging
description: Evidence-based debugging methodology emphasizing observation over assumptions following the scientific method. USE WHEN user reports a bug OR system behavior is unexpected OR troubleshooting issues OR investigating errors OR debugging failures. Follows observe, hypothesize, test, verify cycle with disciplined evidence gathering.
---

# SystematicDebugging

Disciplined evidence-based approach to finding and fixing bugs using the scientific method.

## The Scientific Method for Debugging

```
OBSERVE → HYPOTHESIZE → TEST → VERIFY
    ↑                              ↓
    └──────────────────────────────┘
         (Repeat until solved)
```

## Core Principle

**Evidence Over Assumptions**

Never assume you know what's wrong. Always:
- Gather evidence first
- Form hypothesis based on evidence
- Test hypothesis with minimal changes
- Verify the fix works

## The Process

### Phase 1: Observe (Don't Assume)

**Gather evidence systematically:**

```bash
# Check application logs
journalctl -u ${service} -n 100 --no-pager

# Check system logs
tail -f /var/log/syslog

# Check service status
systemctl status ${service}

# Check resource usage
top -bn1 | head -20

# Check recent changes
git log --oneline --since="1 week ago" -- ${relevant_paths}

# Check environment
env | grep -i ${service}
```

**Critical questions to answer:**
1. What is the EXACT error message (copy it verbatim)?
2. When did this start happening?
3. What changed recently (code, config, environment)?
4. Can you reproduce it reliably?
5. What's the minimum reproduction case?

**Document your observations:**
```bash
# Create debug log
cat > /tmp/debug-$(date +%Y%m%d-%H%M%S).log <<EOF
## Observations

**Error**: [Exact error message]
**Started**: [When it began]
**Frequency**: [Always/Sometimes/Rare]
**Recent changes**: [Git commits, deployments, config changes]
**Environment**: [OS, version, dependencies]

## Reproduction Steps
1. [Step 1]
2. [Step 2]
3. [Observed result]
4. [Expected result]
EOF
```

### Phase 2: Form Hypothesis

**Based on evidence, create testable hypothesis:**

**Template:**
```
Given [observation],
I hypothesize [root cause],
because [reasoning].

If this is true, then [expected outcome].
```

**Example:**
```
Given: Service fails to start after reboot with "connection refused"
I hypothesize: Missing network dependency in systemd unit
because: Service likely starts before network is ready

If this is true, then: Adding After=network-online.target should fix it
```

**Document your hypothesis:**
```bash
cat >> /tmp/debug-*.log <<EOF

## Hypothesis #1

**Given**: [Observation]
**Hypothesis**: [Root cause]
**Reasoning**: [Why you think this]
**Test**: [How to verify]
**Expected**: [What should happen if correct]
EOF
```

### Phase 3: Test Hypothesis

**Design minimal, isolated test:**

**Rules for testing:**
1. **Change ONE variable at a time**
2. **Add logging/instrumentation**
3. **Create reproducible test case**
4. **Document what you're changing**

**Example - Add debugging:**
```bash
# Add logging to startup script
cat > /tmp/debug-startup.sh <<'EOF'
#!/bin/bash
echo "DEBUG: Starting service at $(date)" >> /tmp/service-debug.log
echo "DEBUG: Network status: $(ip addr show)" >> /tmp/service-debug.log
exec /usr/bin/actual-service
EOF
```

**Example - Test specific condition:**
```bash
# Test if file exists
if [ -f /var/run/service.pid ]; then
    echo "FOUND: PID file exists"
    cat /var/run/service.pid
else
    echo "MISSING: PID file does not exist"
    ls -la /var/run/
fi
```

**Example - Isolate component:**
```go
// Add logging to isolate which component fails
func StartService() error {
    log.Println("DEBUG: Initializing database connection")
    db, err := initDB()
    if err != nil {
        log.Printf("DEBUG: Database init failed: %v", err)
        return err
    }

    log.Println("DEBUG: Starting HTTP server")
    return startHTTP(db)
}
```

**Document your test:**
```bash
cat >> /tmp/debug-*.log <<EOF

## Test #1

**Change**: [What you changed]
**Expected**: [What should happen if hypothesis is correct]
**Command**: \`[Command you ran]\`
**Result**: [What actually happened]
**Conclusion**: [Hypothesis confirmed/rejected]
EOF
```

### Phase 4: Verify Fix

**After implementing a fix:**

1. **Verify bug no longer reproduces**
2. **Verify no new bugs introduced**
3. **Run full test suite**
4. **Check logs for expected behavior**
5. **Test edge cases**

**Verification checklist:**
```bash
# 1. Original bug doesn't reproduce
[reproduction command]
# Expected: Works correctly

# 2. Related functionality still works
[test related features]

# 3. Tests pass
go test ./...
pytest
cargo test

# 4. Clean logs
journalctl -u ${service} -n 20 --no-pager
# Expected: No errors

# 5. Edge cases work
[test boundary conditions]
```

**Add regression test:**
```go
// Prevent bug from returning
func TestBugFix_NegativePriceHandling(t *testing.T) {
    // Bug: Negative prices caused panic
    // Fix: Added validation to reject negative prices
    order := Order{Price: -10}
    err := order.Validate()
    if err == nil {
        t.Error("Expected error for negative price, got nil")
    }
    if !strings.Contains(err.Error(), "negative") {
        t.Errorf("Expected error about negative price, got: %v", err)
    }
}
```

**Document the fix:**
```bash
cat >> /tmp/debug-*.log <<EOF

## Solution

**Root cause**: [What was actually wrong]
**Fix**: [What you changed]
**Verification**:
- [✓] Original bug resolved
- [✓] No regressions
- [✓] Tests pass
- [✓] Regression test added

**Files changed**:
- [file1]: [description]
- [file2]: [description]

**Commit**: [commit hash]
EOF

# Save to history
cp /tmp/debug-*.log ~/.config/claude/history/debugging/$(date +%Y-%m)/
```

## Debugging Checklist

### Before Diving In

- [ ] Read the COMPLETE error message (including stack trace)
- [ ] Check logs for full context (before and after error)
- [ ] Identify what changed recently (git log, deployments)
- [ ] Create minimal reproduction case
- [ ] State your hypothesis explicitly before testing

### While Debugging

- [ ] Test ONE hypothesis at a time
- [ ] Add logging, don't assume
- [ ] Document what you tried and results
- [ ] Keep track of working states
- [ ] Don't change multiple things simultaneously
- [ ] Take breaks if stuck (fresh perspective helps)

### After Fixing

- [ ] Verify fix solves original problem
- [ ] Check for side effects
- [ ] Run full test suite
- [ ] Add regression test
- [ ] Remove debug logging
- [ ] Document root cause
- [ ] Update relevant documentation

## Common Pitfalls

### Don't Do This

❌ **Changing multiple things without testing**
```bash
# Wrong: Shotgun debugging
sed -i 's/timeout=5/timeout=30/' config.yaml
systemctl restart service
sed -i 's/retries=3/retries=10/' config.yaml
systemctl restart service
```

❌ **Assuming you know the cause**
```
"It's probably the database connection"
[Spends hours investigating database]
[Actual cause: typo in config file]
```

❌ **Debugging without logs**
```go
// Wrong: No visibility
func Process() error {
    db.Connect()
    data := fetch()
    process(data)
    return nil
}
```

❌ **Skipping reproduction**
```
"User says it sometimes fails"
[Tries to fix without reproducing]
[Can't verify fix works]
```

### Do This Instead

✅ **Change one thing, test, observe**
```bash
# Right: Systematic testing
sed -i 's/timeout=5/timeout=30/' config.yaml
systemctl restart service
journalctl -u service -n 20  # Check result
```

✅ **Gather evidence first**
```bash
# Check recent changes
git log --oneline --since="2 days ago"

# Check logs
journalctl -u service --since="2 days ago" | grep -i error

# Check config
diff config.yaml.backup config.yaml
```

✅ **Add comprehensive logging**
```go
// Right: Instrument for visibility
func Process() error {
    log.Println("DEBUG: Connecting to database")
    if err := db.Connect(); err != nil {
        log.Printf("DEBUG: DB connection failed: %v", err)
        return err
    }

    log.Println("DEBUG: Fetching data")
    data := fetch()
    log.Printf("DEBUG: Fetched %d records", len(data))

    log.Println("DEBUG: Processing data")
    process(data)
    return nil
}
```

✅ **Create reproduction case**
```bash
# Minimal reproduction script
cat > reproduce-bug.sh <<'EOF'
#!/bin/bash
set -e

echo "Step 1: Start service"
systemctl start service

echo "Step 2: Send request"
curl http://localhost:8080/trigger-bug

echo "Step 3: Check logs"
journalctl -u service -n 10
EOF

chmod +x reproduce-bug.sh
./reproduce-bug.sh
```

## Debugging Tools by Language/Environment

### NixOS/systemd Services
```bash
# Service status and recent logs
systemctl status ${service}

# Follow logs in real-time
journalctl -u ${service} -f

# Check service dependencies
systemctl list-dependencies ${service}

# Verify configuration
nixos-rebuild build && nix-instantiate --eval '<nixpkgs/nixos>' -A config.systemd.services.${service}
```

### Go
```go
// Use delve debugger
dlv debug ./cmd/app -- --config=dev.yaml

// Add instrumentation
import _ "net/http/pprof"

// Runtime stack traces
import "runtime/debug"
debug.PrintStack()
```

### Python
```python
# Use pdb
import pdb; pdb.set_trace()

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Trace function calls
import sys
sys.settrace(trace_function)
```

### Rust
```rust
// Use RUST_BACKTRACE
RUST_BACKTRACE=1 cargo run

// Debug logging
env_logger::init();
log::debug!("Value: {:?}", value);

// Use rust-lldb
rust-lldb target/debug/app
```

### Network Issues
```bash
# Check connectivity
ping ${host}
telnet ${host} ${port}
curl -v http://${host}:${port}

# Check DNS
dig ${domain}
nslookup ${domain}

# Check open ports
ss -tlnp | grep ${port}
netstat -tlnp | grep ${port}

# Packet capture
tcpdump -i any -n port ${port}
```

## Integration with Other Skills

**Before debugging:**
- Use **Grep** and **Read** to examine code
- Check **Git** history for recent changes
- Review service configurations

**After fixing:**
- Use **TestDrivenDevelopment** to add regression tests
- Update documentation with **Notes** skill
- Consider if fix should be documented in troubleshooting guide

**When debugging is extensive:**
- Document the investigation process
- Create **Notes** entry with solution
- Add to troubleshooting documentation

## Examples

**Example 1: Service won't start**
```
User: "The jellyfin service fails to start after reboot"

→ Invoke SystematicDebugging skill
→ OBSERVE: Check systemctl status jellyfin
→ OBSERVE: Check journalctl -u jellyfin
→ Error: "Failed to bind to port 8096: address already in use"
→ OBSERVE: Check what's using port 8096
→ Find: Old process still running
→ HYPOTHESIS: Process not cleaned up on shutdown
→ TEST: Add KillMode=control-group to systemd unit
→ TEST: Reboot and verify
→ VERIFY: Service starts successfully
→ FIX: Update NixOS configuration
→ Add regression test in CI
```

**Example 2: Intermittent failures**
```
User: "API sometimes returns 500, can't reproduce consistently"

→ Invoke SystematicDebugging skill
→ OBSERVE: Gather error logs with timestamps
→ OBSERVE: Check for patterns (time of day, request rate, specific endpoints)
→ Pattern found: Errors increase under load
→ HYPOTHESIS: Race condition or resource exhaustion
→ TEST: Add connection pool monitoring
→ Find: Database connection pool exhausted during spikes
→ HYPOTHESIS: Connection pool too small
→ TEST: Increase pool size from 10 to 50
→ TEST: Load test with monitoring
→ VERIFY: No more 500 errors under load
→ FIX: Update configuration
→ Add metrics for connection pool usage
→ Set up alerts for pool exhaustion
```

**Example 3: Configuration issue after NixOS update**
```
User: "After updating to nixos-unstable, my service is broken"

→ Invoke SystematicDebugging skill
→ OBSERVE: What changed in the update?
→ Check: nix store diff-closures
→ Find: Service package updated from 2.1 to 2.2
→ OBSERVE: Check service logs
→ Error: "Unknown configuration option: legacy_mode"
→ HYPOTHESIS: Config option removed in v2.2
→ TEST: Check v2.2 changelog
→ Confirmed: Option removed, replaced with new_mode
→ FIX: Update NixOS config to use new_mode
→ TEST: nixos-rebuild build
→ TEST: nixos-rebuild switch
→ VERIFY: Service starts successfully
→ Document: Add note about migration in comments
```

**Example 4: Memory leak investigation**
```
User: "Service memory usage keeps growing until it crashes"

→ Invoke SystematicDebugging skill
→ OBSERVE: Monitor memory over time
→ OBSERVE: Check for goroutine leaks (if Go)
→ Find: Goroutines increasing steadily
→ HYPOTHESIS: Goroutines not being cleaned up
→ TEST: Add pprof profiling
→ Analyze goroutine stack traces
→ Find: WebSocket connections not closing properly
→ HYPOTHESIS: Missing context cancellation
→ TEST: Add context with timeout to WebSocket handler
→ TEST: Monitor goroutine count
→ VERIFY: Goroutines stable, memory stable
→ FIX: Update WebSocket handler
→ Add test: Verify connections close on timeout
→ Add metrics: Track active WebSocket connections
```

**Example 5: Performance degradation**
```
User: "Queries are getting slower over time"

→ Invoke SystematicDebugging skill
→ OBSERVE: Measure current query performance
→ OBSERVE: Check database indices
→ OBSERVE: Check table sizes
→ Find: Large table with no index on commonly queried column
→ HYPOTHESIS: Missing index causing table scans
→ TEST: Analyze query execution plan
→ Confirmed: Full table scan on 10M rows
→ HYPOTHESIS: Adding index will improve performance
→ TEST: Add index in development environment
→ TEST: Measure query time improvement
→ Result: Query time: 5s → 50ms
→ FIX: Add index migration
→ VERIFY: Performance in production
→ Document: Add comment explaining index purpose
```
