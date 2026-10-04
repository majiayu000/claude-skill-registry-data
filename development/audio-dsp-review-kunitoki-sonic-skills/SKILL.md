---
name: audio-dsp-review
description: >
  Reviews audio DSP and audio processing code for realtime safety violations. Use whenever the
  user asks to review, audit, or check audio processing code — including plugin process callbacks,
  audio engine render functions, DSP implementations, or any code that runs on the audio thread.
  Trigger on phrases like "review my processBlock", "check this DSP code", "is this safe for the
  audio thread?", "review my JUCE plugin", or when you see an audio callback and spot potential
  realtime violations. Flag issues proactively even when the user hasn't explicitly asked for a
  review.
---

# Audio DSP Realtime Safety Review

> **The cardinal rule:** *If you don't know how long it will take, don't do it.*
>
> The audio callback has a hard deadline — typically 1–5ms per buffer. Miss it once and the
> user hears a glitch. The three categories of violations that cause this are: **allocations**,
> **locking**, and **system calls** — all of which can block for unbounded time.

## Step 1 — Find the realtime context

Identify the audio callback and every function it calls (transitively). Common names:
`processBlock`, `process`, `render`, `getNextAudioBlock`, `audioDeviceIOCallback`,
`AURenderCallback`, `JackProcessCallback`, and the output-stream closure in cpal/JUCE/PortAudio.

## Step 2 — Scan for violations

**Memory allocations** (allocator paths may lock, grow arenas, touch new pages, or run
unbounded bookkeeping):
- `new` / `delete` / `malloc` / `free` / `make_shared` / `make_unique`
- `std::string` construction, concatenation, `to_string()`
- Container growth: `vector::push_back` without pre-reserve, `map::operator[]` on new keys,
  `unordered_map::insert`, `deque::push_back`
- `std::function` with non-trivial captures (may allocate), throwing exceptions

**Locking** (priority inversion: the low-priority UI thread holds the lock your audio thread needs):
- `std::mutex`, `lock_guard`, `unique_lock`, `scoped_lock`, `shared_mutex`
- `pthread_mutex_lock`, `pthread_rwlock_*`
- `condition_variable::wait()`, `future::get()`, `semaphore::acquire()`
- **`std::mutex::try_lock()` + RAII wrapper** — `try_lock()` itself is non-blocking, but the
  RAII destructor calls `unlock()`, which does a system call to wake waiting threads.
  Not realtime-safe. Same for `std::unique_lock(mtx, std::try_to_lock)`.
- Spinlocks without exponential back-off on the non-audio thread — busy-wait burns CPU,
  causes starvation under contention, and drains battery on mobile devices.
  If you must use a spinlock: audio thread calls only `try_lock()` + fallback;
  non-audio thread uses progressive back-off (spin → `_mm_pause()` → batched pauses → occasional yield).

**System calls / blocking I/O** (kernel transitions stall for unbounded time):
- `printf`, `fprintf`, `cout`, `cerr`, `DBG()` (JUCE debug), `syslog`, `os_log`
- File I/O: `fopen`, `fclose`, `fread`, `fwrite`, `open`, `read`, `write`
- `sleep`, `usleep`, `nanosleep`, `std::this_thread::sleep_for`, `yield`
- Network: `connect`, `send`, `recv`, `select`
- `std::system()`, `assert()` (in debug builds: prints + aborts)

**Warnings** (flag but don't block):
- First-touch page faults — allocate and pre-touch buffers in `prepareToPlay`
- Denormal floats — missing `ScopedNoDenormals` or `_MM_SET_FLUSH_ZERO_MODE` causes 100× slowdown
- `std::rand()` — uses a global lock on some implementations

## Step 3 — Write the review

```
## Audio Realtime Safety Review: `[file / function]`

### Verdict
[Safe | Has critical violations | Warnings only] — [one sentence summary]

### Critical Violations
**[Category]: [description]**
`file:line` — `offending code`
Why: [one sentence on the realtime risk]
Fix: [concrete suggestion]

### Warnings
[same format]

### What's Done Well
[correct patterns observed — pre-allocation, atomics, lock-free queues, etc.]

### Recommended Fixes (priority order)
1. ...
```

## Quick fix table

| Violation | Realtime-safe alternative |
|-----------|--------------------------|
| `std::mutex` for shared state | Lock-free `std::atomic<T>` for scalars after checking `is_lock_free()`; SPSC lock-free queue for structs |
| `std::mutex::try_lock()` + RAII | `unlock()` in destructor does a syscall — not safe. Use `std::atomic_flag` spinlock with `try_lock()` only on audio thread + fallback |
| Spinlock with busy-wait on non-audio thread | Progressive back-off: spin 5× → `_mm_pause()` 10× → batched 10× `_mm_pause()` → occasional `std::this_thread::yield()` |
| `new`/`delete` in callback | Allocate in `prepareToPlay`; use pre-allocated pool or ring buffer |
| `printf`/`DBG()` | Write to a lock-free ring buffer; drain from a background thread |
| `std::string` ops | `std::array<char,N>` + `snprintf`; format on UI thread |
| `vector` growing | `reserve()` on init; fixed-capacity container (`etl::vector`, `heapless::Vec`) |
| `map::operator[]` insertion | `find()` + pre-populate; or `std::array` with index lookup |
| Exception throwing | Validate in `prepareToPlay`; use error codes; never throw from callback |
| `std::function` w/ captures | Function pointer + `void*`; or pre-store as member |

For deeper patterns (JUCE-specific, VST3, CLAP, Rust/cpal, Web Audio) see
`references/realtime-violations.md`.
