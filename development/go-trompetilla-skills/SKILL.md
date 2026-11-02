---
name: Go
description: Write reliable Go code avoiding goroutine leaks, interface traps, and common concurrency bugs.
metadata: {"clawdbot":{"emoji":"🐹","requires":{"bins":["go"]},"os":["linux","darwin","win32"]}}
---

## Goroutine Leaks
- Goroutine blocked on channel with no sender = leak forever — always ensure channel closes or use context
- Unbuffered channel send blocks until receive — deadlock if receiver never comes
- `for range` on channel loops forever until channel closed — sender must `close(ch)`
- Context cancellation doesn't stop goroutine automatically — must check `ctx.Done()` in loop
- Leaked goroutines accumulate memory and never garbage collect

## Channel Traps
- Sending to nil channel blocks forever — receiving from nil also blocks forever
- Sending to closed channel panics — closing already closed channel panics
- Only sender should close channel — receiver closing causes sender panic
- Buffered channel full = send blocks — size buffer for expected load
- `select` with multiple ready cases picks randomly — not first listed

## Defer Gotchas
- Defer arguments evaluated immediately, not when deferred function runs — `defer log(time.Now())` captures now
- Defer in loop accumulates — defers stack, run at function end not iteration end
- Defer runs even on panic — good for cleanup, but recover only in deferred function
- Named return values modifiable in defer — `defer func() { err = wrap(err) }()` works
- Defer order is LIFO — last defer runs first

## Interface Traps
- Nil concrete value in interface is not nil interface — `var p *MyType; var i interface{} = p; i != nil` is true
- Type assertion on wrong type panics — use comma-ok: `v, ok := i.(Type)`
- Empty interface `any` accepts anything but loses type safety — avoid when possible
- Interface satisfaction is implicit — no compile error if method signature drifts
- Pointer receiver doesn't satisfy interface for value type — only `*T` has the method

## Error Handling
- Errors are values, not exceptions — always check returned error
- `err != nil` after every call — unchecked errors are silent bugs
- `errors.Is` for wrapped errors — `==` doesn't work with `fmt.Errorf("%w", err)`
- Sentinel errors should be `var ErrFoo = errors.New()` not recreated
- Panic for programmer errors only — return error for runtime failures

## Slice Gotchas
- Slice is reference to array — modifying slice modifies original
- Append may or may not reallocate — never assume capacity
- Slicing doesn't copy — `a[1:3]` shares memory with `a`
- Nil slice and empty slice differ — `var s []int` vs `s := []int{}`
- `copy()` copies min of lengths — doesn't extend destination

## Map Traps
- Reading from nil map returns zero value — writing to nil map panics
- Map iteration order is random — don't rely on order
- Maps not safe for concurrent access — use `sync.Map` or mutex
- Taking address of map element forbidden — `&m[key]` doesn't compile
- Delete from map during iteration is safe — but add may cause issues

## String Gotchas
- Strings are immutable byte slices — each modification creates new allocation
- `range` over string iterates runes, not bytes — index jumps for multi-byte chars
- `len(s)` is bytes, not characters — use `utf8.RuneCountInString()`
- String comparison is byte-wise — not Unicode normalized
- Substring shares memory with original — large string keeps memory alive

## Struct and Memory
- Struct fields padded for alignment — field order affects memory size
- Zero value is valid — `var wg sync.WaitGroup` works, no constructor needed
- Copying struct with mutex copies unlocked mutex — always pass pointer
- Embedding is not inheritance — promoted methods can be shadowed
- Exported fields start uppercase — lowercase fields invisible outside package

## Build Traps
- `go build` caches aggressively — use `-a` flag to force rebuild
- Unused imports fail compilation — use `_` import for side effects only
- `init()` runs before main, order by dependency — not file order
- `go:embed` paths relative to source file — not working directory
- Cross-compile: `GOOS=linux GOARCH=amd64 go build` — easy but test on target
