---
name: go-http-server
description: The canonical net/http server for Go web services, with an embedded static frontend. Use when creating internal/server/server.go, serving a frontend out of the binary, adding a route or an API handler, or adding middleware. Triggers on net/http, http.ServeMux, go:embed static, embed.FS, fs.Sub, http.StripPrefix, http.FileServer, ListenAndServe, and any mention of gin, chi, or echo.
user-invocable: false
---

# Go HTTP Server

**One `Server` struct, the standard library's `ServeMux`, and a frontend served straight out of the binary.**

Third-party routers (gin, chi, echo) are not used. `net/http` has had method-and-pattern routing since Go 1.22, so a router dependency now buys syntax rather than capability, and it costs a version to track and an API to relearn.

The server owns the `embed.FS` boilerplate for the whole project. A frontend skill covers what goes inside `static/`; this covers how those bytes reach a browser.

## The Server

```go
package server

import (
    "embed"
    "fmt"
    "io/fs"
    "net/http"

    "github.com/rs/zerolog/log"
)

//go:embed static
var staticFiles embed.FS

type Server struct {
    host string
    port int
    mux  *http.ServeMux
}

func New(host string, port int) *Server {
    return &Server{host: host, port: port, mux: http.NewServeMux()}
}

func (s *Server) Setup() error {
    staticFS, err := fs.Sub(staticFiles, "static")
    if err != nil {
        return err
    }
    s.mux.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.FS(staticFS))))

    s.mux.HandleFunc("/api/health", s.handleHealth)
    s.mux.HandleFunc("/api/data", s.handleData)

    s.mux.HandleFunc("/", s.handleIndex)
    return nil
}

func (s *Server) Run() error {
    addr := fmt.Sprintf("%s:%d", s.host, s.port)
    log.Info().Str("addr", addr).Msg("starting")
    return http.ListenAndServe(addr, s.mux)
}

func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    w.Write([]byte(`{"status":"ok"}`))
}

func (s *Server) handleIndex(w http.ResponseWriter, r *http.Request) {
    data, err := staticFiles.ReadFile("static/index.html")
    if err != nil {
        http.Error(w, "Not found", http.StatusNotFound)
        return
    }
    w.Header().Set("Content-Type", "text/html")
    w.Write(data)
}
```

`Setup` is separate from `Run` so a caller can report a mount failure before the process commits to listening on a port.

`fs.Sub` strips the `static` prefix from the embedded tree, and `http.StripPrefix` strips it from the request path. Both are needed: without the first, `/static/css/app.css` resolves to `static/static/css/app.css` inside the FS.

A PWA service worker needs its own exact route rather than the `/static/` mount, because a worker's scope is the directory it is served from. One served under `/static/` cannot control the app at `/`.

`handleIndex` is registered on `/` rather than on an exact pattern, so a deep link into a client-routed single-page app returns the page instead of a 404.

The server layer logs through zerolog, the same as every other part of every project type. A CLI + Web hybrid keeps its `utils` printers for the command surface and uses zerolog here, so the binary has one logger rather than one per command.

## Skeleton

A fresh project drops the concrete API handlers and keeps the embed wiring exactly as it is, because that wiring is the part that fails silently when retyped from memory.

```go
func (s *Server) Setup() error {
    staticFS, err := fs.Sub(staticFiles, "static")
    if err != nil {
        return err
    }
    s.mux.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.FS(staticFS))))
    s.mux.HandleFunc("/", s.handleIndex)

    // TODO: add API routes

    return nil
}
```

## Headless API Service

A service with no frontend keeps the `Server` struct, `New`, `Setup`, and `Run`, and drops `//go:embed static`, `fs.Sub`, the `/static/` mount, and `handleIndex`. Its `Setup` registers API routes only, and an unmatched path falls through to the mux's own 404.

## Middleware

Middleware is added case by case rather than by default, since a wrapper applied to every route runs on the health check too.

```go
func withLogging(next http.HandlerFunc) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        log.Info().Str("method", r.Method).Str("path", r.URL.Path).Msg("request")
        next(w, r)
    }
}

s.mux.HandleFunc("/api/data", withLogging(s.handleData))
```

Wrapping at the registration site keeps the applied middleware visible in `Setup`, where the route list already is.
