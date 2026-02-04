---
name: echo
description: Comprehensive guide for the Echo web framework. Use when building scalable, high-performance web applications and REST APIs in Go with features like flexible routing, middleware support, request/response binding, static file serving, and template rendering. Applies to installing Echo, defining routes, implementing middleware, handling requests/responses, and building web services.
---

# Echo Web Framework

Echo is a high-performance, minimalist Go web framework for building robust REST APIs and web applications with simplicity and efficiency.

## Installation

Initialize a Go module and install Echo v4:

```bash
mkdir myapp && cd myapp
go mod init myapp
go get github.com/labstack/echo/v4
```

For Go v1.14 or earlier, enable module mode explicitly:

```bash
GO111MODULE=on go get github.com/labstack/echo/v4
```

## Quick Start

### Hello World Server

```go
package main

import (
	"net/http"
	"github.com/labstack/echo/v4"
)

func main() {
	e := echo.New()
	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, World!")
	})
	e.Logger.Fatal(e.Start(":1323"))
}
```

Run with `go run server.go` and visit `http://localhost:1323`.

## Routing

### Basic Routes

Define routes using HTTP methods (GET, POST, PUT, DELETE, PATCH, etc.):

```go
e.POST("/users", saveUser)
e.GET("/users/:id", getUser)
e.PUT("/users/:id", updateUser)
e.DELETE("/users/:id", deleteUser)
```

### Path Parameters

Extract dynamic segments from URL paths:

```go
func getUser(c echo.Context) error {
	id := c.Param("id")
	return c.String(http.StatusOK, id)
}
```

### Query Parameters

Access query string parameters:

```go
func show(c echo.Context) error {
	team := c.QueryParam("team")
	member := c.QueryParam("member")
	return c.String(http.StatusOK, "team:" + team + ", member:" + member)
}
```

## Request Handling

### Bind Request Data

Echo supports automatic binding of JSON, XML, form, and query data into Go structs:

```go
type User struct {
	Name  string `json:"name" xml:"name" form:"name" query:"name"`
	Email string `json:"email" xml:"email" form:"email" query:"email"`
}

e.POST("/users", func(c echo.Context) error {
	u := new(User)
	if err := c.Bind(u); err != nil {
		return err
	}
	return c.JSON(http.StatusCreated, u)
})
```

### Form Data

Handle `application/x-www-form-urlencoded` requests:

```go
func save(c echo.Context) error {
	name := c.FormValue("name")
	email := c.FormValue("email")
	return c.String(http.StatusOK, "name:" + name + ", email:" + email)
}
```

### File Uploads

Handle multipart form data with file uploads:

```go
func save(c echo.Context) error {
	name := c.FormValue("name")
	avatar, err := c.FormFile("avatar")
	if err != nil {
		return err
	}

	src, err := avatar.Open()
	if err != nil {
		return err
	}
	defer src.Close()

	dst, err := os.Create(avatar.Filename)
	if err != nil {
		return err
	}
	defer dst.Close()

	if _, err = io.Copy(dst, src); err != nil {
		return err
	}

	return c.HTML(http.StatusOK, "<b>Thank you! " + name + "</b>")
}
```

## Response Handling

### JSON and XML Responses

Send structured data as JSON or XML:

```go
e.GET("/users", func(c echo.Context) error {
	u := &User{
		Name:  "Jon",
		Email: "[email protected]",
	}
	return c.JSON(http.StatusOK, u)
	// or
	// return c.XML(http.StatusOK, u)
})
```

### Pretty-Printed JSON

Format JSON responses for readability:

```go
return c.JSONPretty(http.StatusOK, u, "  ")
```

## Static Files

### Serve Directory

Map a URL path to a local directory:

```go
e.Static("/static", "assets")
e.Static("/", "public")  // serve from root
```

### Serve Single File

Serve individual files:

```go
e.File("/", "public/index.html")
e.File("/favicon.ico", "images/favicon.ico")
```

### Embedded Filesystem (SPA)

Serve Single Page Application assets from embedded Go filesystem:

```go
//go:embed web
var webAssets embed.FS

func main() {
	e := echo.New()

	e.Use(middleware.StaticWithConfig(middleware.StaticConfig{
		HTML5:      true,
		Root:       "web",
		Filesystem: http.FS(webAssets),
	}))

	api := e.Group("/api")
	api.GET("/users", func(c echo.Context) error {
		return c.String(http.StatusOK, "users")
	})

	if err := e.Start(":8080"); err != nil && !errors.Is(err, http.ErrServerClosed) {
		log.Fatal(err)
	}
}
```

## Middleware

Middleware intercepts requests at root, group, or route levels:

### Root-Level Middleware

Applied to all routes:

```go
e.Use(middleware.Logger())
e.Use(middleware.Recover())
```

### Group-Level Middleware

Applied to specific route groups:

```go
g := e.Group("/admin")
g.Use(middleware.BasicAuth(func(username, password string, c echo.Context) (bool, error) {
	if username == "joe" && password == "secret" {
		return true, nil
	}
	return false, nil
}))
```

### Route-Level Middleware

Applied to individual routes:

```go
track := func(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c echo.Context) error {
		println("request to /users")
		return next(c)
	}
}
e.GET("/users", func(c echo.Context) error {
	return c.String(http.StatusOK, "/users")
}, track)
```

## Server Startup

### HTTP Server

```go
func main() {
	e := echo.New()
	// add middleware and routes...
	if err := e.Start(":8080"); err != http.ErrServerClosed {
		log.Fatal(err)
	}
}
```

### HTTPS/TLS Server

```go
if err := e.StartTLS(":8443", "server.crt", "server.key"); err != http.ErrServerClosed {
	log.Fatal(err)
}
```

### HTTP/2 Server

```go
if err := e.StartTLS(":1323", "cert.pem", "key.pem"); err != http.ErrServerClosed {
	log.Fatal(err)
}
```

### HTTP/2 Cleartext (H2C)

```go
s := &http2.Server{
	MaxConcurrentStreams: 250,
	MaxReadFrameSize:     1048576,
	IdleTimeout:          10 * time.Second,
}
if err := e.StartH2CServer(":8080", s); err != http.ErrServerClosed {
	log.Fatal(err)
}
```

### Custom HTTP Server

For advanced configuration:

```go
s := http.Server{
	Addr:    ":8080",
	Handler: e,
	//ReadTimeout: 30 * time.Second,
}
if err := s.ListenAndServe(); err != http.ErrServerClosed {
	log.Fatal(err)
}
```

## Advanced Features

### Session Management

Use session middleware for maintaining user state:

```go
import "github.com/labstack/echo-contrib/session"
import "github.com/gorilla/sessions"

func main() {
	e := echo.New()
	e.Use(session.Middleware(sessions.NewCookieStore([]byte("secret"))))

	e.GET("/create-session", func(c echo.Context) error {
		sess, _ := session.Get("session", c)
		sess.Values["foo"] = "bar"
		sess.Save(c.Request(), c.Response())
		return c.NoContent(http.StatusOK)
	})

	e.GET("/read-session", func(c echo.Context) error {
		sess, _ := session.Get("session", c)
		return c.String(http.StatusOK, fmt.Sprintf("foo=%v", sess.Values["foo"]))
	})

	e.Start(":8080")
}
```

### Observability (OpenTelemetry + Sentry)

Integrate distributed tracing with OpenTelemetry SDK and error tracking with Sentry:

```go
import (
	"github.com/getsentry/sentry-go"
	sentryecho "github.com/getsentry/sentry-go/echo"
	"go.opentelemetry.io/contrib/instrumentation/github.com/labstack/echo/otelecho"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
)

func initTracer() (*sdktrace.TracerProvider, error) {
	exporter, err := otlptracehttp.New(context.Background(),
		otlptracehttp.WithEndpoint("signoz-collector:4318"),
		otlptracehttp.WithInsecure(),
	)
	if err != nil {
		return nil, err
	}

	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName("myapp"),
		)),
	)
	otel.SetTracerProvider(tp)
	return tp, nil
}

func main() {
	// Initialize Sentry for error tracking
	sentry.Init(sentry.ClientOptions{
		Dsn:              os.Getenv("SENTRY_DSN"),
		Environment:      os.Getenv("APP_ENV"),
		TracesSampleRate: 1.0,
	})
	defer sentry.Flush(2 * time.Second)

	// Initialize OpenTelemetry tracer
	tp, _ := initTracer()
	defer tp.Shutdown(context.Background())

	e := echo.New()

	// OpenTelemetry middleware for distributed tracing
	e.Use(otelecho.Middleware("myapp"))

	// Sentry middleware for error tracking
	e.Use(sentryecho.New(sentryecho.Options{Repanic: true}))

	e.GET("/hello", func(c echo.Context) error {
		return c.String(http.StatusOK, "hello")
	})

	e.Start(":8080")
}
```

For structured logging with trace correlation, use zerolog:

```go
import (
	"github.com/rs/zerolog"
	"go.opentelemetry.io/otel/trace"
)

func LoggerFromContext(ctx context.Context, logger zerolog.Logger) zerolog.Logger {
	span := trace.SpanFromContext(ctx)
	if span.SpanContext().IsValid() {
		return logger.With().
			Str("trace_id", span.SpanContext().TraceID().String()).
			Str("span_id", span.SpanContext().SpanID().String()).
			Logger()
	}
	return logger
}
```

### Request Logger with ZeroLog

Configure structured logging:

```go
import (
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

// Initialize logger (or use global log.Logger)
logger := zerolog.New(os.Stderr).With().Timestamp().Logger()

e.Use(middleware.RequestLoggerWithConfig(middleware.RequestLoggerConfig{
	LogURI:    true,
	LogStatus: true,
	LogValuesFunc: func(c echo.Context, v middleware.RequestLoggerValues) error {
		logger.Info().
			Str("URI", v.URI).
			Int("status", v.Status).
			Msg("request")
		return nil
	},
}))


### Route Export

Export all registered routes as JSON:

```go
routes := e.Routes()
// Each route contains Method, Path, and Name
```

## Key Echo Methods

**Context Methods**: `c.Param()`, `c.QueryParam()`, `c.FormValue()`, `c.FormFile()`, `c.Bind()`, `c.String()`, `c.JSON()`, `c.XML()`, `c.HTML()`, `c.File()`, `c.Redirect()`, `c.NoContent()`

**Echo Methods**: `e.GET()`, `e.POST()`, `e.PUT()`, `e.DELETE()`, `e.Static()`, `e.File()`, `e.Group()`, `e.Use()`, `e.Start()`, `e.StartTLS()`, `e.Routes()`

## Best Practices

- Use middleware for cross-cutting concerns (logging, auth, CORS)
- Bind request data to typed structs for safety
- Return appropriate HTTP status codes
- Group related routes for shared middleware
- Use `echo.Context` for request/response manipulation
- Handle errors explicitly and return meaningful responses
- Leverage middleware ecosystem for common features (JWT, CORS, compression, etc.)
