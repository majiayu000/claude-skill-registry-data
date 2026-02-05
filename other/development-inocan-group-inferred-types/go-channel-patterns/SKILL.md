---
name: go-channel-patterns
description: Common channel patterns and idioms
---

# Channel Patterns

## Core Rule
**Only the sender closes channels.** Receivers never close.

## CORRECT - Sender closes
```go
func generator() <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch) // Sender closes
        for i := 0; i < 10; i++ {
            ch <- i
        }
    }()
    return ch
}

func main() {
    for num := range generator() {
        fmt.Println(num)
    }
}
```

## WRONG - Receiver closes
```go
func main() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 10; i++ {
            ch <- i // Panic: send on closed channel
        }
    }()

    for i := 0; i < 5; i++ {
        <-ch
    }
    close(ch) // WRONG: receiver closes
}
```

## Pattern: Fan-Out (Multiple Workers)
```go
func fanOut(input <-chan int, workers int) []<-chan int {
    outputs := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        outputs[i] = worker(input)
    }
    return outputs
}

func worker(input <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range input {
            out <- n * 2
        }
    }()
    return out
}
```

## Pattern: Fan-In (Merge Channels)
```go
func fanIn(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup

    wg.Add(len(channels))
    for _, ch := range channels {
        go func(c <-chan int) {
            defer wg.Done()
            for n := range c {
                out <- n
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(out)
    }()

    return out
}
```

## Pattern: Or-Done (Early Exit)
```go
func orDone(ctx context.Context, ch <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for {
            select {
            case <-ctx.Done():
                return
            case v, ok := <-ch:
                if !ok {
                    return
                }
                select {
                case out <- v:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()
    return out
}
```

## Rules
1. Use directional channels: `<-chan` (receive), `chan<-` (send)
2. Unbuffered for synchronization, buffered for non-blocking
3. Check `ok` when not using `range`: `v, ok := <-ch`
4. Close to signal "no more values", not to stop receivers
5. Nil channels block forever (useful in `select`)

## Buffered vs Unbuffered
```go
// Unbuffered: synchronous handoff
ch := make(chan int)

// Buffered: decouples sender/receiver
ch := make(chan int, 10)
```
