---
name: element-html-builder
description: Element is a zero dependency library to efficiently generate HTML programmatically, without templates in Go
---

# Element Library: Programmatic HTML Generation in Go

> A comprehensive guide to using `github.com/rohanthewiz/element` for building HTML without templates.

## Overview

Element is a Go library that generates HTML programmatically by leveraging Go's natural function execution order. Instead of templates, you write Go code that mirrors HTML's tree structure.

**Key Insight:** When you call a builder method like `b.Div()`, the opening tag `<div>` is **written immediately** to an internal buffer. The element returned must be **terminated** with `R()`, `T()`, or `F()` to write the closing tag.

---

## Getting Started

### Creating a Builder

Start with a builder for creating elements

```go
import "github.com/rohanthewiz/element"

// Method 1: Standard creation
b := element.NewBuilder()

// Method 2: Shorthand
b := element.B()

// Method 3: From pool (high-throughput HTTP handlers)
b := element.AcquireBuilder()
defer element.ReleaseBuilder(b)
```

### The Critical Concept: Immediate Tag Writing

When you call an element method, the **opening tag is written immediately**:

```go
b := element.NewBuilder()
b.Div("id", "container")  // "<div id="container">" is NOW in the buffer
// The element is returned, waiting for termination
```

This is why Element works - Go's function argument evaluation order means children are processed (and their tags written) before the parent's `R()` closes the parent tag.

---

## Termination Methods

Every non-self-closing element **must** be terminated. This writes the closing tag.

### R() - Render with Children

Use when the element has child elements, mixed content, or no children:

```go
// With child elements
b.Div().R(
    b.P().T("First paragraph"),
    b.P().T("Second paragraph"),
)
// Output: <div><p>First paragraph</p><p>Second paragraph</p></div>

// Empty element
b.Div().R()
// Output: <div></div>
```

### T() - Text Only

Use when the element contains **only** text (most efficient for text-only):

```go
b.P().T("Hello, World!")
// Output: <p>Hello, World!</p>

// Multiple strings are concatenated
b.Span().T("Hello", " ", "World")
// Output: <span>Hello World</span>
```

### F() - Formatted Text

Use for `fmt.Sprintf`-style formatted text:

```go
count := 42
b.P().F("You have %d items", count)
// Output: <p>You have 42 items</p>
```

### Self-Closing Elements

Elements like `<br>`, `<img>`, `<input>`, `<hr>`, `<meta>` don't require termination, but you **can** call `R()` for consistency:

```go
b.Br()                              // <br>
b.Img("src", "logo.png", "alt", "Logo")  // <img src="logo.png" alt="Logo">
b.Input("type", "text", "name", "email") // <input type="text" name="email">

// R() is safe to call on single-tag elements (does nothing extra)
b.Br().R()  // Still just <br>
```

---

## Attributes

Attributes are passed as **key-value string pairs**:

```go
// Multiple attributes
b.Div("id", "main", "class", "container", "data-role", "content").R()
// Output: <div id="main" class="container" data-role="content"></div>

// Using Class convenience methods (cleaner for class attribute)
b.DivClass("container", "id", "main").R()
// Output: <div class="container" id="main"></div>
```

**Important:** Always provide an even number of attribute strings. In debug mode, an odd count triggers a warning and the last value is dropped.

---

## Class Convenience Methods

Over 90 elements have `*Class` methods that accept `class` as the first attribute:

```go
// Instead of:
b.Div("class", "card").R()
b.P("class", "intro").R()
b.Button("class", "btn primary", "type", "submit").R()

// Use:
b.DivClass("card").R()
b.PClass("intro").R()
b.ButtonClass("btn primary", "type", "submit").R()
```

---

## Building Complex Structures

### Nesting Elements

Go's function execution order makes nesting natural:

```go
b.Html().R(
    b.Head().R(
        b.Title().T("My Page"),
        b.Meta("charset", "utf-8"),
    ),
    b.Body().R(
        b.DivClass("container").R(
            b.H1().T("Welcome"),
            b.PClass("intro").R(
                b.T("This is "),
                b.SpanClass("highlight").T("important"),
                b.T(" content."),
            ),
        ),
    ),
)
```

### Using Wrap() for Logic

`Wrap()` allows arbitrary Go code within the render tree:

```go
b.Div().R(
    b.H2().T("Items"),
    b.Wrap(func() {
        if len(items) == 0 {
            b.P().T("No items found")
        } else {
            for _, item := range items {
                b.P().T(item)
            }
        }
    }),
)
```

### Using ForEach() for Iteration

`ForEach` is a generic helper for iterating slices:

```go
items := []string{"Apple", "Banana", "Cherry"}

b.Ul().R(
    element.ForEach(items, func(item string) {
        b.Li().T(item)
    }),
)
// Output: <ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>
```

### Using b.T() for Direct Text

`b.T()` writes text directly to the builder (outside element context):

```go
b.P().R(
    b.T("Start of paragraph. "),
    b.Strong().T("Bold text"),
    b.T(" End of paragraph."),
)
```

---

## Components

Components are reusable HTML fragments implementing the `Component` interface:

```go
type Component interface {
    Render(b *element.Builder) (x any)
}
```

### Creating a Component

```go
type Card struct {
    Title   string
    Content string
}

func (c Card) Render(b *element.Builder) (x any) {
    b.DivClass("card").R(
        b.H3().T(c.Title),
        b.P().T(c.Content),
    )
    return
}
```

### Using Components

```go
// Method 1: Direct render call
card := Card{Title: "Hello", Content: "World"}
b.Div().R(
    card.Render(b),
)

// Method 2: RenderComponents for multiple
cards := []element.Component{
    Card{Title: "One", Content: "First"},
    Card{Title: "Two", Content: "Second"},
}
b.Div().R(
    element.RenderComponents(b, cards...),
)
```

### HtmlPage Helper

For complete HTML documents with a body component:

```go
type PageBody struct {
    Title string
}

func (pb PageBody) Render(b *element.Builder) (x any) {
    b.H1().T(pb.Title)
    b.P().T("Welcome to the page")
    return
}

func generatePage() string {
    b := element.B()
    b.HtmlPage(
        "body { font-family: sans-serif; }",  // CSS
        "<title>My Page</title>",              // Head content
        PageBody{Title: "Home"},               // Body component
    )
    return b.String()
}
```

---

## Builder Pool for High-Throughput

In HTTP handlers processing many requests, use the builder pool to reduce GC pressure:

```go
func handler(w http.ResponseWriter, r *http.Request) {
    b := element.AcquireBuilder()
    defer element.ReleaseBuilder(b)

    b.Html().R(
        b.Body().R(
            b.H1().T("Hello"),
        ),
    )

    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.Write(b.Bytes())  // Use Bytes() to avoid string allocation
}
```

**When to use pooling:**
- High-traffic HTTP handlers
- Server-side rendering APIs
- Any scenario creating many short-lived builders

**When pooling isn't needed:**
- CLI tools, batch processing
- Low-traffic applications
- One-off page generation

---

## Debug Mode

Debug mode helps catch malformed HTML during development:

```go
// Enable debug mode
element.DebugSet()

// Check for issues
html := element.DebugShow()

// Clear debug mode
element.DebugClear()
```

Debug mode detects:
- Unclosed tags
- Odd number of attributes
- Children on self-closing elements
- Unwrapped text content

---

## Output Methods

```go
b := element.NewBuilder()
// ... build HTML ...

// Get as string (allocates)
html := b.String()

// Get as bytes (better for HTTP responses)
w.Write(b.Bytes())

// Reset for reuse
b.Reset()
```

---

## Common Patterns

### Conditional Elements

```go
// Using Wrap
b.Div().R(
    b.Wrap(func() {
        if showHeader {
            b.H1().T("Header")
        }
    }),
    b.P().T("Always shown"),
)

// Using component conditional
func renderOptional(b *element.Builder, show bool, content string) any {
    if show {
        b.P().T(content)
    }
    return nil
}
```

### Building Tables

```go
b.Table().R(
    b.THead().R(
        b.Tr().R(
            b.Th().T("Name"),
            b.Th().T("Value"),
        ),
    ),
    b.TBody().R(
        element.ForEach(data, func(row DataRow) {
            b.Tr().R(
                b.Td().T(row.Name),
                b.Td().T(row.Value),
            )
        }),
    ),
)
```

### Form Elements

```go
b.Form("method", "post", "action", "/submit").R(
    b.Label("for", "email").T("Email:"),
    b.Input("type", "email", "id", "email", "name", "email"),
    b.Br(),
    b.Label("for", "password").T("Password:"),
    b.Input("type", "password", "id", "password", "name", "password"),
    b.Br(),
    b.ButtonClass("btn", "type", "submit").T("Submit"),
)
```

---

## Best Practices

1. **Always use Builder** - Never create Elements directly
2. **Terminate all elements** - Use `R()`, `T()`, or `F()` on every non-self-closing element
3. **Use Class methods** - `DivClass()` is cleaner than `Div("class", ...)`
4. **Prefer T() for text-only** - More efficient than `R(b.T(...))`
5. **Use pooling in handlers** - `AcquireBuilder()`/`ReleaseBuilder()` for HTTP
6. **Use Bytes() for responses** - Avoids string allocation
7. **Create components** - For reusable UI patterns
8. **Enable debug mode** - During development to catch issues early

---

## Quick Reference

| Task | Code |
|------|------|
| Create builder | `b := element.B()` |
| Pooled builder | `b := element.AcquireBuilder()` |
| Element with children | `b.Div().R(children...)` |
| Element with text | `b.P().T("text")` |
| Formatted text | `b.P().F("Count: %d", n)` |
| Add class | `b.DivClass("name")` |
| Attributes | `b.A("href", "/", "class", "link")` |
| Iterate slice | `element.ForEach(items, func(i T) { ... })` |
| Render component | `comp.Render(b)` |
| Multiple components | `element.RenderComponents(b, c1, c2)` |
| Get output | `b.String()` or `b.Bytes()` |
