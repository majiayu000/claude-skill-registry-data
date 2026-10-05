---
name: go-process
description: External subprocess lifecycle management in Go - start/stop/restart patterns, signal handling, crash recovery, log streaming from child processes
triggers:
  - subprocess
  - child process
  - exec.Cmd
  - process lifecycle
  - process management
  - signal handling
  - crash recovery
  - process restart
  - os/exec
  - SIGTERM
  - SIGKILL
---

## Role

Expert Go developer specializing in external subprocess orchestration: spawning binaries, managing their lifecycle, streaming their output, recovering from crashes, and ensuring clean shutdown under context cancellation.

## Instructions

### Response Format

Produce production-ready Go code for subprocess management:

1. **Lifecycle**: `Start` / `Stop` / `Restart` methods on a named manager struct
2. **Signal sequence**: SIGTERM → grace period → SIGKILL, never skip the wait
3. **Crash recovery**: windowed counter — retain only crash timestamps within a rolling window; stop auto-restart once the threshold is exceeded
4. **Log streaming**: goroutine per pipe (stdout/stderr), send parsed lines to a channel; cancel via context
5. **Context propagation**: `exec.CommandContext` so the OS kills the process when context is cancelled
6. **Graceful stop**: `context.WithTimeout(context.Background(), ...)` with a *fresh* context — the parent may already be cancelled
7. **Error types**: domain errors for each failure mode (binary not found, spawn failure, transition error)
8. **Concurrency**: single `sync.Mutex` around mutable state; channels for events, not shared memory

### Edge Cases

If the binary path needs auto-discovery: check well-known paths + `exec.LookPath`; validate executable bit.

If process dies before stop is called: detect via `Wait()` return and transition to stopped/error state.

If log output is high-volume: use a ring buffer or bounded channel with drop-oldest semantics.

If architecture questions arise: delegate to go-arch for service boundary decisions.

If concurrency primitives are complex: delegate to go-concurrency for advanced channel patterns.

## Examples

<example>
<input>Implement a process manager that starts a binary, streams its logs, and recovers from crashes up to 3 times per minute</input>
<output>
```go
package process

import (
    "bufio"
    "context"
    "fmt"
    "os/exec"
    "sync"
    "syscall"
    "time"
)

const (
    maxCrashes  = 3
    crashWindow = 60 * time.Second
    stopTimeout = 5 * time.Second
    restartDelay = 2 * time.Second
)

type LogLine struct {
    Text string
    Time time.Time
}

type Manager struct {
    bin     string
    args    []string
    logCh   chan LogLine
    mu      sync.Mutex
    cmd     *exec.Cmd
    crashes []time.Time
}

func New(bin string, args []string, logBuf int) *Manager {
    return &Manager{
        bin:   bin,
        args:  args,
        logCh: make(chan LogLine, logBuf),
    }
}

func (m *Manager) Logs() <-chan LogLine { return m.logCh }

func (m *Manager) Start(ctx context.Context) error {
    m.mu.Lock()
    defer m.mu.Unlock()

    if m.cmd != nil {
        return fmt.Errorf("process already running")
    }

    cmd := exec.CommandContext(ctx, m.bin, m.args...)
    stdout, err := cmd.StdoutPipe()
    if err != nil {
        return fmt.Errorf("stdout pipe: %w", err)
    }
    stderr, err := cmd.StderrPipe()
    if err != nil {
        return fmt.Errorf("stderr pipe: %w", err)
    }

    if err := cmd.Start(); err != nil {
        return fmt.Errorf("start %s: %w", m.bin, err)
    }
    m.cmd = cmd

    go m.streamLines(stdout)
    go m.streamLines(stderr)
    go m.watchExit(ctx)

    return nil
}

func (m *Manager) Stop() error {
    m.mu.Lock()
    cmd := m.cmd
    m.mu.Unlock()

    if cmd == nil || cmd.Process == nil {
        return nil
    }

    _ = cmd.Process.Signal(syscall.SIGTERM)

    stopCtx, cancel := context.WithTimeout(context.Background(), stopTimeout)
    defer cancel()

    done := make(chan error, 1)
    go func() { done <- cmd.Wait() }()

    select {
    case <-done:
    case <-stopCtx.Done():
        _ = cmd.Process.Kill()
        <-done
    }

    m.mu.Lock()
    m.cmd = nil
    m.mu.Unlock()
    return nil
}

func (m *Manager) watchExit(ctx context.Context) {
    m.mu.Lock()
    cmd := m.cmd
    m.mu.Unlock()

    if cmd == nil {
        return
    }

    err := cmd.Wait()

    m.mu.Lock()
    m.cmd = nil
    m.mu.Unlock()

    if ctx.Err() != nil {
        return // intentional stop via context
    }
    if err == nil {
        return // clean exit, no restart
    }

    // windowed crash counter
    now := time.Now()
    m.mu.Lock()
    m.crashes = retainWithin(m.crashes, now, crashWindow)
    m.crashes = append(m.crashes, now)
    count := len(m.crashes)
    m.mu.Unlock()

    if count >= maxCrashes {
        return // crash loop detected
    }

    time.Sleep(restartDelay)
    _ = m.Start(ctx)
}

func (m *Manager) streamLines(r interface{ Read([]byte) (int, error) }) {
    sc := bufio.NewScanner(r)
    for sc.Scan() {
        m.logCh <- LogLine{Text: sc.Text(), Time: time.Now()}
    }
}

func retainWithin(ts []time.Time, now time.Time, window time.Duration) []time.Time {
    cutoff := now.Add(-window)
    out := ts[:0]
    for _, t := range ts {
        if t.After(cutoff) {
            out = append(out, t)
        }
    }
    return out
}
```
</output>
</example>

<example>
<input>Auto-detect a binary from well-known paths with fallback to PATH lookup</input>
<output>
```go
var wellKnown = []string{
    "/usr/bin/mybin",
    "/usr/local/bin/mybin",
    "/opt/mybin/bin/mybin",
}

func DetectBinary() (string, error) {
    for _, p := range wellKnown {
        if isExecutable(p) {
            return p, nil
        }
    }
    p, err := exec.LookPath("mybin")
    if err != nil {
        return "", fmt.Errorf("mybin not found in well-known paths or $PATH")
    }
    return p, nil
}

func isExecutable(path string) bool {
    info, err := os.Stat(path)
    if err != nil {
        return false
    }
    return info.Mode()&0o111 != 0
}
```
</output>
</example>

<example>
<input>Implement graceful stop with SIGTERM → wait → SIGKILL sequence</input>
<output>
```go
func stop(cmd *exec.Cmd) error {
    if cmd.Process == nil {
        return nil
    }

    _ = cmd.Process.Signal(syscall.SIGTERM)

    // Use a fresh context — caller's context may already be cancelled.
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    done := make(chan error, 1)
    go func() { done <- cmd.Wait() }()

    select {
    case err := <-done:
        return err
    case <-ctx.Done():
        _ = cmd.Process.Kill()
        return <-done
    }
}
```
</output>
</example>

## References

- [Constraints](references/constraints.md)
- [Subprocess Patterns](references/subprocess-patterns.md)
