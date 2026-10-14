---
name: ort-thread-debugging
description: Diagnoses ORT thread-affinity crashes and sort-direction bugs in Go MCP servers.
---

# ORT Thread Debugging Skill

## Problem it solves

ONNX Runtime sessions are bound to the OS thread that created them. When a Go program creates a session on goroutine A and calls `session.Run()` from goroutine B (which may execute on a different OS thread), ORT crashes with cryptic access violations or index-out-of-range panics. This is the single most common failure when embedding ORT in Go MCP servers, CLI tools, or web services.

Additionally, insertion sort bugs (`j++` instead of `j--`) produce panics that look like embedding dimension errors but are actually in sorting code.

## Detection triggers

Activate when:
- `session.Run()` crashes with access violation, index out of range, or segfault
- Error mentions ORT, onnxruntime, or ONNX session together with a thread-related signal, such as native access violations under concurrent use or session creation and `Run` occurring in different goroutines
- Embedding computation works in isolation but crashes in the server
- Panic message says `index out of range [N] with length N` (check if N matches embedding dimension or result count)
- Embeddings work in a test binary but fail when called from MCP/HTTP handlers
- Multiple goroutines share a single ORT session

## Protocol

### 1. Diagnose thread affinity

ORT rule: **session creation and all `session.Run()` calls MUST happen on the same OS thread.**

Check for this pattern (WRONG):
```go
// Created on goroutine A (main thread)
session, _ := ort.NewDynamicAdvancedSession(...)

// Called from goroutine B (MCP handler, HTTP handler, etc.)
go func() {
    session.Run(inputs, outputs) // CRASH — different OS thread
}()
```

### 2. Fix: dedicated goroutine with LockOSThread

The correct pattern routes all ORT operations through a single goroutine that locks its OS thread:

```go
type Embedder struct {
    runCh  chan computeRequest
    stopCh chan struct{}
    done   chan struct{}  // closed when runLoop exits
    // ...
}

func (e *Embedder) runLoop() {
    runtime.LockOSThread()          // Pin this goroutine to one OS thread
    defer runtime.UnlockOSThread()
    defer close(e.done)             // Signal that runLoop has exited

    // Create session HERE — on the locked thread
    session, err := ort.NewDynamicAdvancedSession(modelPath, inputs, outputs, nil)
    if err != nil {
        panic(err)
    }
    defer session.Destroy()

    for {
        select {
        case req := <-e.runCh:
            results, err := e.runOnSession(session, req.texts)
            req.out <- computeResult{results: results, err: err}
        case <-e.stopCh:
            // Drain queued requests so Compute callers don't block forever
            for {
                select {
                case req := <-e.runCh:
                    req.out <- computeResult{err: errors.New("embedder shutting down")}
                default:
                    return
                }
            }
        }
    }
}

func (e *Embedder) Compute(text string) ([]float32, error) {
    req := computeRequest{texts: []string{text}, out: make(chan computeResult, 1)}
    select {
    case e.runCh <- req:
    case <-e.done:
        return nil, errors.New("embedder stopped")
    }
    res := <-req.out
    return res.results, res.err
}
```

Key points:
- `runtime.LockOSThread()` MUST be called before session creation
- Session is created inside the locked goroutine, not in `InitEmbedder`
- All compute calls route through a channel to this goroutine
- Use a buffered channel (`make(chan computeResult, 1)`) to prevent deadlock
- `Compute` checks the `done` channel to avoid blocking forever if `runLoop` has exited
- `runLoop` drains queued requests on shutdown so callers get an error instead of hanging

### 3. Distinguish ORT panics from sort/logic panics

When you see `index out of range [N] with length N`:
- If N equals the embedding dimension (e.g., 384): likely ORT output tensor slice error
- If N equals the number of results/skills: likely insertion sort bug (`j++` instead of `j--`)
- If N is random: likely memory corruption from cross-thread ORT access

Check the stack trace line number. If it's in a sort function, fix the sort direction. If it's in `runBatch` slicing output tensors, investigate the tensor shape and slice indices. Diagnose thread-affinity issues only when session creation and execution occur on different locked OS threads or when native ORT failures provide evidence.

### 4. Verify with isolated test

Create a minimal test that calls `Compute()` from multiple goroutines:

```go
func main() {
    emb, _ := embedding.InitEmbedder()
    defer emb.Close()

    var wg sync.WaitGroup
    for i := 0; i < 10; i++ {
        wg.Add(1)
        go func(n int) {
            defer wg.Done()
            result, err := emb.Compute(fmt.Sprintf("test %d", n))
            if err != nil {
                log.Printf("goroutine %d: %v", n, err)
            } else {
                log.Printf("goroutine %d: %d dims", n, len(result))
            }
        }(i)
    }
    wg.Wait()
}
```

Use this test as evidence about reproducibility, then inspect the native stack, provider, model, inputs, and lifecycle independently; neither a crash nor a successful run is conclusive.

### 5. Check embedding dimensions

After successful compute, verify dimensions match expectations:
```go
result, _ := emb.Compute("hello")
if len(result) != 384 {  // all-MiniLM-L6-v2
    log.Printf("wrong dimensions: got %d, want 384", len(result))
}
```

## When NOT to use

- Python ORT usage (GIL handles thread safety differently)
- Single-threaded programs with no goroutines
- Pure SQLite/database crashes (not ORT-related)
- Dimension mismatches between different models (not a thread issue)

## Cross-references

- **debugging-and-error-recovery** — Apply the structured debugging protocol. ORT crashes often get misdiagnosed as embedding bugs when they're actually thread bugs.

- **anti-phantom-symbols** — Verify ORT API calls (`NewDynamicAdvancedSession`, `NewTensor`, `session.Run`) exist in the version being used. ORT Go API has changed across versions.

- **safe-code-modifications** — When fixing thread affinity, don't remove the old session creation without ensuring the new goroutine-based approach is verified.

- **verify-and-cite** — Verify the fix works under concurrent load, not just single-goroutine tests.

## Lessons learned

Real bugs caught by this skill:
1. `defer embedding.CloseEmbedder()` in MCP handlers kills ORT for all subsequent requests — handlers must NOT own the embedder lifecycle
2. Insertion sort `j++` vs `j--` produces panics that look like embedding dimension errors
3. `runtime.LockOSThread()` in `InitEmbedder` doesn't help if the session is created there but run from handlers — the lock must be in the goroutine that BOTH creates AND runs the session
