---
name: go-basics
description: Use when writing, building, or reviewing Go programs on an
  authorized engineering task. Covers module setup with go mod, building
  and cross-compiling, gofmt and go vet hygiene, unit testing with the
  testing package, error handling idioms, goroutines and channels for
  concurrency, the race detector, and static binaries for deployment. Use
  when starting a Go CLI, service, scanner, or tool, or when auditing Go
  code for correctness.
version: 1.0.0
domain: engineering
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [code-reviewer, git-workflows]
tools:
  - name: Go
    version: "1.23"
---

Go is a compiled language built for simple, fast, concurrent programs:
one toolchain, fast builds, static binaries, and concurrency primitives
in the language itself. This skill covers the working basics an operator
needs to write, build, test, and ship Go tools, including the error
handling and goroutine patterns that keep Go programs predictable. All
examples target Go 1.23.

## Quick Workflow

1. Verify the toolchain and set up a module with `go mod init`.
2. Write code in small packages with exported names capitalized.
3. Format every file with `gofmt` and check with `go vet` before
   committing.
4. Handle every error explicitly; never ignore a returned `error`.
5. Write table-driven tests and run them with `go test`.
6. Use goroutines and channels for concurrent work; run tests with
   `-race` to catch data races.
7. Cross-compile static binaries for the target platform with
   `GOOS`/`GOARCH` and stripped symbols.
8. Document the module path and minimum Go version in `go.mod`.

## 1. Toolchain and first module

```bash
# Confirm the toolchain
go version

# Start a new module (the path should match the repo location)
mkdir -p ~/go-work/portcheck && cd ~/go-work/portcheck
go mod init example.com/portcheck

# Project layout
tree -L 2 -a 2>/dev/null || find . -maxdepth 2 | sort
```

```bash
cat > main.go <<'EOF'
package main

import (
	"fmt"
	"net"
	"time"
)

func checkPort(host string, port int, timeout time.Duration) bool {
	addr := fmt.Sprintf("%s:%d", host, port)
	conn, err := net.DialTimeout("tcp", addr, timeout)
	if err != nil {
		return false
	}
	conn.Close()
	return true
}

func main() {
	ports := []int{22, 80, 443, 8080}
	for _, p := range ports {
		fmt.Printf("port %d open=%v\n", p, checkPort("127.0.0.1", p, 2*time.Second))
	}
}
EOF

go run .
```

`go run` compiles and runs in one step for development; `go build`
produces a real binary.

## 2. Build, format, and vet

```bash
# Build the binary into ./bin
mkdir -p bin
go build -o bin/portcheck .

# Format all files in place (run before every commit)
gofmt -l .        # lists files that need formatting
gofmt -w .        # formats them

# Static analysis: suspicious constructs, bad printf verbs, unreachable code
go vet ./...

# Tidy the module file after adding or removing imports
go mod tidy
```

`gofmt` is non-negotiable in Go culture: unformatted code stands out
immediately in review. `go vet` catches real bugs such as `fmt.Printf`
with the wrong verb count.

## 3. Error handling idioms

Go has no exceptions. Functions return `error` as the last value and
the caller decides what to do. Check errors at the point of return,
wrap them with context using `%w`, and fail fast.

```go
package main

import (
	"fmt"
	"os"
)

func readConfig(path string) ([]byte, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read config %s: %w", path, err)
	}
	if len(data) == 0 {
		return nil, fmt.Errorf("config %s is empty", path)
	}
	return data, nil
}

func main() {
	data, err := readConfig("config.yaml")
	if err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
	fmt.Println("loaded", len(data), "bytes")
}
```

Use `errors.Is` and `errors.As` to inspect wrapped errors instead of
string matching. Reserve `panic` for programmer errors that mean the
program cannot continue (nil map writes in init paths, impossible
states), never for expected failures like bad user input or network
errors.

## 4. Testing with the standard library

Table-driven tests are the Go standard: one test function, a slice of
cases, a loop.

```bash
cat > main_test.go <<'EOF'
package main

import "testing"

func TestCheckPort(t *testing.T) {
	cases := []struct {
		name string
		host string
		port int
		want bool
	}{
		{"closed high port", "127.0.0.1", 59999, false},
		{"invalid port zero", "127.0.0.1", 0, false},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got := checkPort(tc.host, tc.port, 1000000000) // 1s
			if got != tc.want {
				t.Errorf("checkPort(%s,%d) = %v, want %v",
					tc.host, tc.port, got, tc.want)
			}
		})
	}
}
EOF

go test -v ./...
go test -race ./...   # race detector: required for concurrent code
go test -cover ./...  # coverage summary
```

Subtests with `t.Run` give each case a name in the output. Benchmarks
use `func BenchmarkX(b *testing.B)` and run with `go test -bench=.`.

## 5. Goroutines and channels

Goroutines are cheap concurrent functions; channels move data between
them safely. The pattern below scans ports concurrently with a bounded
worker pool.

```go
package main

import (
	"fmt"
	"sync"
	"time"
)

func worker(host string, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for port := range jobs {
		if checkPort(host, port, 2*time.Second) {
			results <- port
		}
	}
}

func scanHost(host string, ports []int, workers int) []int {
	jobs := make(chan int, len(ports))
	results := make(chan int, len(ports))
	var wg sync.WaitGroup

	for w := 0; w < workers; w++ {
		wg.Add(1)
		go worker(host, jobs, results, &wg)
	}
	for _, p := range ports {
		jobs <- p
	}
	close(jobs)
	wg.Wait()
	close(results)

	var open []int
	for p := range results {
		open = append(open, p)
	}
	return open
}

func main() {
	ports := []int{22, 80, 443, 3000, 8000, 8080, 9000}
	fmt.Println("open:", scanHost("127.0.0.1", ports, 10))
}
```

Rules that prevent the classic mistakes: the sender closes the
channel, never the receiver; use `sync.WaitGroup` to know when workers
are done; never share a map across goroutines without a mutex (the
race detector will find this).

```bash
# Run with the race detector during development and CI
go test -race ./...
go run -race .
```

## 6. Modules and dependencies

```bash
# Add a dependency (picks the latest tagged version)
go get github.com/spf13/cobra@latest

# Pin to a specific version for reproducible builds
go get github.com/spf13/cobra@v1.8.1

# Upgrade all direct dependencies to latest minor/patch
go get -u ./...

# Show the dependency graph and verify checksums
go mod graph | head -20
go mod verify
```

`go.mod` records the module path and Go version; `go.sum` records
hashes of every dependency. Commit both files. Builds verify
dependencies against `go.sum`, which blocks silent substitution of a
dependency's contents.

## 7. Cross-compiling static binaries

```bash
# Linux amd64 static binary with symbols stripped (smaller, no debug info)
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
  go build -trimpath -ldflags="-s -w" -o bin/portcheck-linux .

# Windows and macOS targets from the same source
CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build -o bin/portcheck.exe .
CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build -o bin/portcheck-mac .

# Confirm the result
file bin/portcheck-linux
ls -lh bin/
```

`CGO_ENABLED=0` gives a fully static binary with no libc dependency,
which is what you want for containers and minimal hosts. `-trimpath`
removes local filesystem paths from the binary for reproducible
builds.

## Edge cases

- `go: command not found` after install. Add the Go bin directory to
  PATH: `export PATH=$PATH:/usr/local/go/bin` and the module bin
  dir `$(go env GOPATH)/bin`.
- `go mod tidy` removes a dependency you still need indirectly. This
  happens when an import only exists behind a build tag; verify with
  `go build -tags <tag>` before tidying, or keep the import explicit.
- Tests pass locally but flake in CI. Usually timing assumptions or
  port conflicts; bind test servers to port 0 (random free port) and
  never assume a fixed port is free.
- Race detector reports a race in a map read. Maps are not safe for
  concurrent use; protect with `sync.Mutex` or switch to
  `sync.Map` when the access pattern fits.
- Cross-compiled binary fails with "no such file or directory" on
  the target. The binary was built with CGO against glibc; rebuild
  with `CGO_ENABLED=0` or ship the matching libc.
- `go get` picks a pseudo-version you did not expect. Pin exact
  versions in `go.mod` for anything that ships; pseudo-versions
  (`v0.0.0-20240101-abcdef`) pin a commit but are hard to audit.
- Vendoring is required for offline builds. Run `go mod vendor`
  and build with `-mod=vendor`; commit the `vendor/` directory so
  the build never touches the network.

## Detection and defender view

For engineering skills this section covers detecting misuse and
misconfiguration. A Go binary is suspicious when it is statically
linked, stripped (`-s -w`), and upx-packed while claiming to be a
common utility; check `file` output and string tables for mismatches.
Go programs embed the module path and build metadata, readable with
`go version -m binary`, which reveals the real project and dependency
versions even in stripped builds. Misconfiguration shows up as Go
services running as root, debug endpoints (`net/http/pprof`)
exposed on public interfaces, and binaries built with CGO pulling
unexpected shared libraries. Detect data races and goroutine leaks in
long-running services by watching RSS growth and goroutine counts
exposed through `runtime` metrics endpoints; a leak usually means a
channel nobody drains.

## Key references

- Go 1.23 documentation: https://go.dev/doc/
- Effective Go: https://go.dev/doc/effective_go
- go command reference: https://pkg.go.dev/cmd/go
- testing package: https://pkg.go.dev/testing
- sync package (Mutex, WaitGroup): https://pkg.go.dev/sync
- CWE-362 (Concurrent Execution using Shared Resource with Improper
  Synchronization): data races the race detector finds.
- CWE-400 (Uncontrolled Resource Consumption): unbounded goroutine
  spawning.
