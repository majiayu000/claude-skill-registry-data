---
name: rust-async
description: This skill should be used when the user asks to "use tokio broadcast channels", "manage async processes in Rust", "stream subprocess output", "implement graceful shutdown in Rust", "handle crash recovery with Tokio", "race futures with select!", "cancel async tasks", or mentions tokio::process, tokio::sync::broadcast, JoinHandle::abort, or CancellationToken.
triggers:
  - tokio broadcast
  - async process rust
  - subprocess async rust
  - tokio process
  - graceful shutdown rust
  - cancel async task
  - tokio select
  - crash recovery rust
  - tokio spawn
  - joinhandle abort
---

## Role

Expert Rust async developer specializing in production Tokio patterns: subprocess lifecycle, broadcast event channels, log streaming, crash recovery, and graceful cancellation — all derived from real-world process management code.

## Core Tokio Patterns

### broadcast::channel — Multi-Consumer Fan-Out

`tokio::sync::broadcast` is the right channel type when multiple independent consumers must receive the same event stream (e.g., UI + logger + metrics all watching process state changes):

```rust
use tokio::sync::broadcast;

// Sender held by the publisher; subscribe() creates per-consumer receivers
let (tx, _) = broadcast::channel::<ProcessEvent>(64);

// Each consumer subscribes independently
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

// Publisher sends once; all active receivers get a copy
let _ = tx.send(ProcessEvent::StateChanged { from, to, connection });
```

**Lagged receiver**: if a consumer is too slow, it gets `Err(RecvError::Lagged(n))`. Always handle this:

```rust
loop {
    match rx.recv().await {
        Ok(event)                     => handle(event),
        Err(RecvError::Lagged(n))     => eprintln!("dropped {n} events"),
        Err(RecvError::Closed)        => break,
    }
}
```

### tokio::process — Spawn External Binaries

```rust
use tokio::process::Command;
use std::process::Stdio;

let mut child = Command::new(&self.binary_path)
    .args(&["run", "-c", config_path])
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;

// child.id() → Option<u32> (PID, None after process exits)
// child.wait().await → ExitStatus
// child.kill().await → sends SIGKILL
```

**Important**: `child.kill()` sends SIGKILL. For graceful SIGTERM, use the `nix` crate:

```rust
use nix::sys::signal::{kill, Signal};
use nix::unistd::Pid;

if let Some(pid) = child.id() {
    let _ = kill(Pid::from_raw(pid as i32), Signal::SIGTERM);
}
```

### Graceful Shutdown Sequence

SIGTERM → timed wait → SIGKILL. Use a **fresh** `context::Background()` for the stop timeout — the application context is likely already cancelled:

```rust
async fn graceful_stop(child: &mut Child, log_handles: &mut Vec<JoinHandle<()>>) {
    // 1. Request graceful exit
    if let Some(pid) = child.id() {
        let _ = kill(Pid::from_raw(pid as i32), Signal::SIGTERM);
    }

    // 2. Wait up to 5s — use a fresh context, not the (cancelled) parent
    let result = timeout(Duration::from_secs(5), child.wait()).await;

    // 3. Force kill if timeout
    if result.is_err() {
        child.kill().await.ok();
        child.wait().await.ok();
    }

    // 4. Abort log streaming tasks
    for handle in log_handles.drain(..) {
        handle.abort();
    }
}
```

### Log Streaming — Async Line-by-Line

```rust
use tokio::io::{AsyncBufReadExt, BufReader};

fn capture_pipe(pipe: impl AsyncRead + Unpin + Send + 'static, tx: broadcast::Sender<ProcessEvent>) {
    tokio::spawn(async move {
        let reader = BufReader::new(pipe);
        let mut lines = reader.lines();
        while let Ok(Some(line)) = lines.next_line().await {
            let _ = tx.send(ProcessEvent::LogLine(line));
        }
        // Loop exits naturally when the pipe closes (process exits)
    });
}
```

Call once for `child.stdout.take()` and once for `child.stderr.take()`.

### Crash Recovery — Windowed Counter

Track recent crash timestamps in a `Vec<Instant>`. Before each append, filter out entries older than the window. No timers or external state needed:

```rust
const MAX_CRASHES: usize  = 3;
const CRASH_WINDOW: Duration = Duration::from_secs(60);
const RESTART_DELAY: Duration = Duration::from_secs(2);

fn retain_recent(crashes: &mut Vec<Instant>) {
    let cutoff = Instant::now() - CRASH_WINDOW;
    crashes.retain(|&t| t > cutoff);
}

async fn handle_unexpected_exit(&mut self, ctx: &Context) {
    retain_recent(&mut self.crash_times);
    self.crash_times.push(Instant::now());

    if self.crash_times.len() >= MAX_CRASHES {
        self.transition_to_error("crash loop detected");
        return;
    }

    sleep(RESTART_DELAY).await;
    self.start(ctx).await.ok();
}
```

### Detecting Signal vs. Crash Exit

```rust
use std::os::unix::process::ExitStatusExt;

fn is_signal_exit(status: std::process::ExitStatus) -> bool {
    status.signal().is_some()
}

// In watchExit:
let status = child.wait().await?;
if ctx.is_done() || is_signal_exit(status) {
    return; // intentional — do not restart
}
handle_unexpected_exit().await;
```

### JoinHandle Management

Store handles and abort on shutdown. A task that panics sets the handle to an error state — always `await` or `abort`:

```rust
struct Manager {
    handles: Vec<JoinHandle<()>>,
}

impl Manager {
    fn spawn_task(&mut self, fut: impl Future<Output = ()> + Send + 'static) {
        self.handles.push(tokio::spawn(fut));
    }

    async fn shutdown(&mut self) {
        for handle in self.handles.drain(..) {
            handle.abort();
            let _ = handle.await; // await after abort to let cleanup run
        }
    }
}
```

### tokio::select! — Race Futures

```rust
tokio::select! {
    biased; // check branches top-to-bottom (no random)

    result = child.wait() => {
        // Process exited
        handle_exit(result).await;
    }
    _ = ctx.done() => {
        // Context cancelled — stop the process
        graceful_stop(&mut child, &mut log_handles).await;
    }
}
```

## Edge Cases

If `child.id()` returns `None`: the process has already exited; skip the signal.

If a broadcast receiver lags: handle `RecvError::Lagged` — log the gap and continue; don't abort.

If `tokio::time::timeout` wraps a future that holds a `std::sync::Mutex`: the mutex guard won't be released across `.await`. Use `tokio::sync::Mutex` instead.

If background task needs access to shared state: wrap in `Arc<Mutex<T>>` — move the `Arc` into the spawn closure, not the `Mutex` guard.

For CancellationToken (structured cancellation without context): see the reference file.

## References

- [Process Manager Patterns](references/process-patterns.md)
- [Channel Selection Guide](references/channel-guide.md)
