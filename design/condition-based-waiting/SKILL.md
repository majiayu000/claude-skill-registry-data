---
name: condition-based-waiting
description: Use when waiting for something async. NEVER use Start-Sleep blindly — wait on conditions.
---

# Condition-Based Waiting

Time-based sleeps are a bet that the world finishes within N seconds. The bet is always wrong eventually — too short on slow machines, too long on fast ones. Wait on the **condition**, not the **clock**.

## Iron Law

**Do not `Start-Sleep` to wait for something to "be ready."** Poll the actual condition, with a timeout, with backoff.

## Red Flags

- `Start-Sleep 5` after starting a server, then hitting it.
- `Start-Sleep 60` to "let things settle."
- Sleeps inside retry loops with no condition check.
- Sleeps tuned to "what worked on my machine."
- Sleep duration in a comment: `# this needs to be at least 3s`.

If you've written any of these, replace them now.

## The Right Pattern

```
loop:
  if condition_met(): break
  if elapsed > timeout: fail("waited too long for X")
  sleep(small backoff)
```

Three pieces — condition check, timeout guard, bounded sleep between polls.

## Common Conditions and How to Wait on Them

### Wait for a port to open (server starting)

```powershell
$deadline = (Get-Date).AddSeconds(30)
$delay = 0.2
while ((Get-Date) -lt $deadline) {
    try {
        $c = New-Object System.Net.Sockets.TcpClient
        $c.Connect('127.0.0.1', 8080)
        $c.Close()
        break
    } catch {
        Start-Sleep -Seconds $delay
        $delay = [Math]::Min($delay * 1.5, 2.0)
    }
}
if ((Get-Date) -ge $deadline) { throw "server did not open port 8080 within 30s" }
```

### Wait for a file to exist

```powershell
$deadline = (Get-Date).AddSeconds(20)
while (-not (Test-Path 'C:\path\to\sentinel.txt')) {
    if ((Get-Date) -ge $deadline) { throw "sentinel.txt never appeared" }
    Start-Sleep -Milliseconds 200
}
```

### Wait for a background job

```powershell
$job = Start-Job { ... }
Wait-Job $job -Timeout 60 | Out-Null
if ($job.State -ne 'Completed') { Stop-Job $job; throw "job timed out" }
Receive-Job $job
```

`Wait-Job` is event-based — no polling needed.

### Wait for an HTTP endpoint to return 200

```powershell
$deadline = (Get-Date).AddSeconds(30)
$delay = 0.25
while ($true) {
    try {
        $r = Invoke-WebRequest -Uri 'http://localhost:8080/health' -UseBasicParsing -TimeoutSec 2
        if ($r.StatusCode -eq 200) { break }
    } catch { }
    if ((Get-Date) -ge $deadline) { throw "health never went 200" }
    Start-Sleep -Seconds $delay
    $delay = [Math]::Min($delay * 1.5, 2.0)
}
```

### Wait for a process to exit

```powershell
$p = Get-Process -Id $pid
$p.WaitForExit(30000)   # 30s timeout, event-based
if (-not $p.HasExited) { throw "process did not exit" }
```

## Backoff Strategy

- Start small (100-250 ms) — fast condition gets caught fast.
- Multiply by ~1.5 each iteration up to a cap (~2 s).
- Hard timeout in the outer loop — never wait forever.

Exponential backoff balances responsiveness (quick wins detected fast) with politeness (no busy-loop hammering the dependency).

## When Sleep IS Appropriate

Narrow exception: you genuinely need to delay, not wait for something. Examples:

- Rate-limiting outbound requests ("at most 10 per second").
- Animation / pacing in a UI.
- Reproducing a race-condition bug with a deterministic delay.

These are *delays by design*, not *waits in disguise*. Comment them explicitly: `# delay for rate limit, not waiting on state`.

## MUST

- MUST have a timeout on every wait loop.
- MUST check the actual condition (port, file, response, state), not "probably ready by now."
- MUST fail loudly when timeout hits — silent timeouts hide deadlocks.

## Cross-references

- [[systematic-debugging]] — race conditions found via Phase 1 reproduction usually need this pattern.
- [[verification-before-completion]] — verifying async behavior means waiting on the condition you care about.
