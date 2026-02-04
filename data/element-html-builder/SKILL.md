---
name: element-html-builder
description: Element is a zero dependency library to efficiently generate HTML, without templates in Go
---

# Element - AI Agent Documentation

> Programmatic HTML generation in Go without templates.

## Overview

Element is a zero-dependency Go library that generates HTML programmatically by leveraging Go's natural function execution order. Instead of templates, you write Go code that mirrors HTML's tree structure.

## Benefits

1. You never leave the safety, speed, and familiarity of Go
    - Compiles single-pass with the rest of your Go program -- no extra annotations or build steps
    - All of Go is available at any point in your code
2. Zero dependencies
3. Buffer pools for super-high traffic situations
4. Go's formatting naturally follows the HTML tree structure

## Installation

```bash
go get -u github.com/rohanthewiz/element
```

## General Strategy

1. Write the opening tag with attributes
2. Render the children and closing tag

## Core Concepts

### The Builder Pattern

All HTML generation flows through a `Builder` instance. The builder maintains an internal buffer where tags are written immediately upon method calls.

### Immediate Tag Writing

**Key Insight:** When you call a builder method like `b.Div()`, the opening tag `<div>` is written **immediately** to an internal buffer. The returned element must be **terminated** with `R()`, `T()`, or `F()` to write the closing tag.

```go
b := element.NewBuilder()
b.Div("id", "container")  // "<div id="container">" is NOW in the buffer
// The element is returned, waiting for termination
```

Go's function argument evaluation order means children are processed (and their tags written) before the parent's `R()` closes the parent tag. This is what makes nested structures work correctly.

### Terminate all tags

Every non-self-closing element **must** be terminated with `R()`, `T()`, or `F()`. Self-closing elements like `Br`, `Img`, `Input`, `Hr`, and `Meta` don't require termination, but to keep things consistent, close these tags with a sole `R()` or `T()`.

## Basic Usage

### Creating a Builder

```go
import "github.com/rohanthewiz/element"

// Standard creation
b := element.NewBuilder()

// Shorthand (equivalent)
b := element.B()

// From pool (for high-throughput HTTP handlers)
b := element.AcquireBuilder()
defer element.ReleaseBuilder(b)
```

### Simple Elements

```go
b := element.B()

// Element with text content
b.P().T("Hello, World!")
// Output: <p>Hello, World!</p>

// Element with children
b.Div().R(
    b.P().T("First paragraph"),
    b.P().T("Second paragraph"),
)
// Output: <div><p>First paragraph</p><p>Second paragraph</p></div>

// Empty element
b.Div().R()
// Output: <div></div>

// Get the HTML string
html := b.String()
```

### Complete Page Example

```go
b := element.B()
b.Html().R(
    b.Head().R(
        b.Title().T("My Page"),
        b.Meta("charset", "utf-8"),
    ),
    b.Body().R(
        b.DivClass("container").R(
            b.H1().T("Welcome"),
            b.P().T("Hello from Element!"),
        ),
    ),
)
html := b.String()
```

### Building with Multiple Functions

```go
func main() {
	b := element.B()

	b.DivClass("container").R(
		b.H2().T("Section 1"),
		generateList(b),
	)

	fmt.Println(b.Pretty())
	/* // Output:
	<div class="container">
	  <h2>Section 1</h2>
	  <ul>
	    <li>Item 1</li>
	    <li>Item 2</li>
	  </ul>
	</div>
	 */
}

func generateList(b *element.Builder) (x any) { // we don't care about the return
	// Everything is rendered in the builder immediately!
	b.Ul().R(
		b.Li().T("Item 1"),
		b.Li().T("Item 2"),
	)
	return
}
```

## API Reference

### Builder Creation

| Function                    | Description                             |
| --------------------------- | --------------------------------------- |
| `element.NewBuilder()`      | Create a new builder                    |
| `element.B()`               | Shorthand for NewBuilder()              |
| `element.AcquireBuilder()`  | Get builder from pool (high-throughput) |
| `element.ReleaseBuilder(b)` | Return builder to pool                  |

### Termination Methods

| Method               | Use Case                           | Example                    |
| -------------------- | ---------------------------------- | -------------------------- |
| `R(children...)`     | Elements with children or empty    | `b.Div().R(b.P().T("hi"))` |
| `T(strings...)`      | Text-only content (most efficient) | `b.P().T("Hello")`         |
| `F(format, args...)` | Formatted text (like fmt.Sprintf)  | `b.P().F("Count: %d", 42)` |

### Element Methods

All standard HTML elements are available: `Div`, `Span`, `P`, `A`, `H1`-`H6`, `Ul`, `Ol`, `Li`, `Table`, `Tr`, `Td`, `Th`, `Form`, `Input`, `Button`, `Label`, `Img`, `Br`, `Hr`, `Meta`, `Link`, `Script`, `Style`, and 90+ more.

### Class Convenience Methods

Most elements have a `*Class` variant where the first argument is the class attribute:

```go
b.DivClass("container")           // <div class="container">
b.PClass("intro", "id", "p1")     // <p class="intro" id="p1">
b.ButtonClass("btn primary")      // <button class="btn primary">
```

### Utility Functions

| Function                                | Description                              |
| --------------------------------------- | ---------------------------------------- |
| `b.T(strings...)`                       | Write raw text directly to buffer        |
| `b.Wrap(func())`                        | Execute arbitrary Go code in render tree |
| `element.ForEach(slice, func(item))`    | Generic iteration helper                 |
| `element.RenderComponents(b, comps...)` | Render multiple components               |

### Output Methods

| Method       | Description                          |
| ------------ | ------------------------------------ |
| `b.String()` | Get HTML as string                   |
| `b.Bytes()`  | Get HTML as []byte (better for HTTP) |
| `b.Reset()`  | Clear buffer for reuse               |

## Common Patterns

### Attributes as Key-Value Pairs

Attributes are passed as alternating key-value string pairs:

```go
b.Div("id", "main", "class", "container", "data-role", "content").R()
// Output: <div id="main" class="container" data-role="content"></div>

b.A("href", "/about", "class", "nav-link").T("About Us")
// Output: <a href="/about" class="nav-link">About Us</a>
```

### Mixed Content (Text and Elements)

Use `b.T()` to inject text alongside child elements:

```go
b.P().R(
    b.T("This is "),
    b.Strong().T("important"),
    b.T(" information."),
)
// Output: <p>This is <strong>important</strong> information.</p>
```

### Conditional Rendering with Wrap()

`Wrap()` executes arbitrary Go code within the render tree:

```go
b.Div().R(
    b.H2().T("Items"),
    b.Wrap(func() {
        if len(items) == 0 {
            b.P().T("No items found")
        } else {
            for _, item := range items {
                b.Li().T(item)
            }
        }
    }),
)
```

### Iteration with ForEach()

`ForEach` is a generic helper for slices:

```go
items := []string{"Apple", "Banana", "Cherry"}

b.Ul().R(
    element.ForEach(items, func(item string) {
        b.Li().T(item)
    }),
)
// Output: <ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>
```

### Standard Components

A growing list of ready-to-use components will be found in [element/components](https://github.com/rohanthewiz/element/tree/master/components)

### Custom Components

Implement the `Component` interface for reusable HTML fragments:

```go
// Define the component
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

// Use the component
card := Card{Title: "Hello", Content: "World"}
b.Div().R(
    card.Render(b),
)
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
        element.ForEach(rows, func(row DataRow) {
            b.Tr().R(
                b.Td().T(row.Name),
                b.Td().T(row.Value),
            )
        }),
    ),
)
```

### Forms

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

### HTTP Handler with Pooling

```go
func handler(w http.ResponseWriter, r *http.Request) {
    // Acquire builder from pool to reduce GC pressure
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

### Full Page with HtmlPage Helper

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
        "<title>My Page</title>",              // Head content (raw HTML), minus the '<style>' tag
        PageBody{Title: "Home"},               // Body component
    )
    return b.String()
}
```

## Anti-Patterns

### ❌ Forgetting to Terminate Elements

```go
// WRONG: Missing termination - closing tag never written
b.Div("id", "container")
b.P().T("Content")
// Output: <div id="container"><p>Content</p>  (missing </div>)

// CORRECT: Always terminate with R(), T(), or F()
b.Div("id", "container").R(
    b.P().T("Content"),
)
// Output: <div id="container"><p>Content</p></div>
```

### ❌ Odd Number of Attributes

```go
// WRONG: Odd attribute count - "disabled" has no value
b.Button("class", "btn", "disabled").T("Click")
// The last attribute is dropped

// CORRECT: Use empty string for boolean-like attributes
b.Button("class", "btn", "disabled", "").T("Click")
// Output: <button class="btn" disabled="">Click</button>

// OR: Use the attribute name as its value
b.Button("class", "btn", "disabled", "disabled").T("Click")
// Output: <button class="btn" disabled="disabled">Click</button>
```

### ❌ Using T() When You Need R()

```go
// WRONG: T() only accepts text, not child elements
b.Div().T(b.P().T("Content"))  // This won't work as expected

// CORRECT: Use R() for child elements
b.Div().R(
    b.P().T("Content"),
)
```

### ❌ Creating Elements Without a Builder

```go
// WRONG: Don't try to create elements directly
// There is no public Element constructor

// CORRECT: Always use a Builder
b := element.B()
b.Div().R()
```

### ❌ Not Using Pooling in High-Throughput Handlers

```go
// SUBOPTIMAL: Creates GC pressure under load
func handler(w http.ResponseWriter, r *http.Request) {
    b := element.B()  // New allocation every request
    // ...
}

// BETTER: Use pooling for high-traffic handlers
func handler(w http.ResponseWriter, r *http.Request) {
    b := element.AcquireBuilder()
    defer element.ReleaseBuilder(b)
    // ...
}
```

### ❌ Using String() When Writing to io.Writer

```go
// SUBOPTIMAL: Unnecessary string allocation
w.Write([]byte(b.String()))

// BETTER: Use Bytes() directly
w.Write(b.Bytes())
```

### ❌ Forgetting to Reset Reused Builders

```go
// WRONG: Reusing without reset appends to existing content
b := element.B()
b.P().T("First")
html1 := b.String()  // "<p>First</p>"

b.P().T("Second")
html2 := b.String()  // "<p>First</p><p>Second</p>" - probably not intended

// CORRECT: Reset before reuse
b.Reset()
b.P().T("Second")
html2 := b.String()  // "<p>Second</p>"
```

### Note

- Builder has no method `Textarea()` it is `TextArea()`

## Integration Notes

### With github.com/rohanthewiz/rweb

Element integrates naturally with the rweb web framework:

```go
import (
    "github.com/rohanthewiz/element"
    "github.com/rohanthewiz/rweb"
)

func main() {
		server := rweb.NewServer(rweb.ServerOptions{
			Address: "localhost:8080",
		})

    server.Get("/", func(ctx *rweb.Context) error {
        b := element.AcquireBuilder()
        defer element.ReleaseBuilder(b)

        b.Html().R(
            b.Head().R(
                b.Title().T("Home"),
            ),
            b.Body().R(
                b.H1().T("Welcome to RWeb + Element"),
            ),
        )

        return ctx.WriteHTML(b.String())
    })

    server.Run()
}
```

### With Standard net/http

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
    w.Write(b.Bytes())
}
```

### With HTMX

Element works well for HTMX partial responses:

```go
// Handler returning an HTMX partial
func itemsHandler(w http.ResponseWriter, r *http.Request) {
    b := element.AcquireBuilder()
    defer element.ReleaseBuilder(b)

    items := getItems()
    b.Ul("id", "item-list").R(
        element.ForEach(items, func(item Item) {
            b.Li().R(
                b.Span().T(item.Name),
                b.Button(
                    "hx-delete", fmt.Sprintf("/items/%d", item.ID),
                    "hx-target", "closest li",
                    "hx-swap", "outerHTML",
                ).T("Delete"),
            )
        }),
    )

    w.Write(b.Bytes())
}
```

## Debug Mode

Enable debug mode during development to catch common mistakes:

```go
// Enable debug mode
element.DebugSet()

// Build your HTML...

// Check for issues (returns diagnostic string)
issues := element.DebugShow()

// Clear debug mode
element.DebugClear()
```

Debug mode detects:

- Unclosed tags
- Odd number of attributes
- Children on self-closing elements
- Unwrapped text content

## Quick Reference

| Task                  | Code                                        |
| --------------------- | ------------------------------------------- |
| Create builder        | `b := element.B()`                          |
| Pooled builder        | `b := element.AcquireBuilder()`             |
| Element with children | `b.Div().R(children...)`                    |
| Element with text     | `b.P().T("text")`                           |
| Formatted text        | `b.P().F("Count: %d", n)`                   |
| Add class easily      | `b.DivClass("name")`                        |
| Multiple attributes   | `b.A("href", "/", "class", "link")`         |
| Raw text in tree      | `b.T("some text")`                          |
| Conditional logic     | `b.Wrap(func() { if x { ... } })`           |
| Iterate slice         | `element.ForEach(items, func(i T) { ... })` |
| Render component      | `comp.Render(b)`                            |
| Multiple components   | `element.RenderComponents(b, c1, c2)`       |
| Get HTML string       | `b.String()`                                |
| Get HTML bytes        | `b.Bytes()`                                 |
| Reset builder         | `b.Reset()`                                 |

## Links

- **Repository:** https://github.com/rohanthewiz/element
- **Go Package:** https://pkg.go.dev/github.com/rohanthewiz/element
