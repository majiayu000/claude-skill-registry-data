---
name: slipstream
description: Expert assistance for Slipstream static site generation. Use when building static websites with Slipstream, a SwiftUI-like static site generator.
---

# Slipstream Expert

You are an expert in the Slipstream static site generation framework. Slipstream is a SwiftUI-like declarative framework for building static HTML websites with Tailwind CSS integration.

## Core Principles

1. **SwiftUI-like Syntax**: Slipstream uses result builders and the `View` protocol to create HTML in a declarative, hierarchical manner
2. **Tailwind CSS Integration**: All utility modifiers map to Tailwind CSS classes
3. **Static Site Generation**: Designed for building static HTML that can be deployed to platforms like GitHub Pages
4. **Type-Safe HTML**: Provides Swift types for W3C HTML elements with compile-time safety

## Architecture

### View Protocol

The `View` protocol is the foundation of Slipstream:

```swift
public protocol View {
  associatedtype Content: View
  @ViewBuilder var body: Self.Content { get }
  func render(_ container: Element) throws
}
```

- Implement `body` for custom views
- Use `@ViewBuilder` to enable declarative syntax
- Only implement `render(_:environment:)` when creating new HTML element types

### Result Builders

Slipstream uses Swift result builders (`@ViewBuilder`) to enable hierarchical view construction. This allows:
- Multiple children in a single block
- Conditional content with `if/else`
- Loops with `ForEach`
- Optional content

## Common View Types

### Layout Views

- `VStack(alignment:spacing:)` - Vertical stack (maps to flex column)
- `HStack(alignment:spacing:)` - Horizontal stack (maps to flex row)
- `Container` - Tailwind CSS container for centered, max-width content
- `ResponsiveStack` - Adapts between vertical/horizontal based on breakpoints

### Text and Typography

- `Text("content")` - Basic paragraph text (renders as `<p>`)
- `H1`, `H2`, `H3`, `H4`, `H5`, `H6` - Heading elements
- `Paragraph` - Explicit paragraph wrapper
- `Bold`, `Strong`, `Italic`, `Emphasis` - Text styling
- `Code`, `Variable`, `SampleOutput` - Code-related elements
- `MarkdownText` - Render Markdown as HTML

### Forms

- `Form` - Form container
- `TextField(name:type:placeholder:)` - Text input
- `TextArea(name:placeholder:)` - Multi-line text
- `Button`, `SubmitButton`, `ResetButton` - Buttons
- `Checkbox`, `RadioButton` - Selection inputs
- `Picker` with `Option` and `OptGroup` - Dropdown selects
- `Slider`, `ColorPicker`, `FileInput` - Specialized inputs
- `Label`, `Fieldset`, `Legend` - Form organization

### Media

- `Image(URL)` - Images
- `Picture` with `Source` - Responsive images
- `Audio`, `Video` with `Source` and `Track` - Media playback
- `Canvas` - Canvas element
- `IFrame` - Embedded content

### Semantic HTML

- `Header`, `Footer`, `Navigation` - Page structure
- `Article`, `Section`, `Aside` - Content organization
- `DocumentMain` - Main content area
- `Figure`, `FigureCaption` - Figures with captions
- `Blockquote` - Quotations
- `List`, `ListItem` - Lists
- `DescriptionList`, `DescriptionTerm`, `DefinitionDescription` - Definition lists
- `Table`, `TableHeader`, `TableBody`, `TableFooter`, `TableRow`, `TableCell`, `TableHeaderCell` - Tables
- `Details`, `Summary` - Collapsible content
- `Divider` - Horizontal rule
- `LineBreak` - Line break

### SVG and MathML

- `SVG`, `SVGCircle`, `SVGRect`, `SVGPath`, `SVGDefs`, `SVGLinearGradient`, `SVGStop` - SVG graphics
- `Math`, `MRow`, `MI`, `MO`, `MN`, `MFrac`, `MSqrt`, `MSup`, `MSub` - Mathematical notation

### Utilities

- `Comment("text")` - HTML comments
- `DOMString("raw html")` - Raw HTML injection
- `ForEach(collection, id:)` - Iterate over collections

## Tailwind CSS Modifiers

### Typography

```swift
.fontSize(.extraLarge)
.fontWeight(.bold)
.bold()
.fontStyle(.italic)
.italic()
.fontDesign(.monospaced)  // .serif, .sans
.fontLeading(.loose)  // line height
.textAlignment(.center)
.textColor(.blue, shade: .x500)
.textDecoration(.underline)  // .lineThrough
.listStyle(.disc)  // .decimal, .none
```

### Spacing

```swift
.padding()  // all edges
.padding(.horizontal, 16)
.padding(.vertical, 8)
.padding(.top, 4)
.margin(8)
.margin(.bottom, 16)
```

### Sizing

```swift
.frame(width: 48, height: 48)
.frame(minWidth: 48, maxWidth: 96)
.frame(minHeight: 100)
```

### Colors and Backgrounds

```swift
.textColor(.red, shade: .x500)
.backgroundColor(.blue, shade: .x100)
.background(.ultraThin)  // material background
```

### Borders and Effects

```swift
.border(1, .black)
.cornerRadius(.large)
.shadow(.large)
.outline(.solid, width: 2, color: .red)
.ring(width: 2, color: .blue)
```

### Layout

```swift
.display(.block)  // .flex, .grid, .none
.position(.absolute, edges: .top, 0)
.placement(top: 10, left: 10, zIndex: 10)
.zIndex(100)
.overflow(.scroll)  // .hidden, .auto
.float(.left)
.visibility(.hidden)
```

### Flexbox and Grid

```swift
.flexDirection(.row)  // .column
.justifyContent(.spaceBetween)  // .center, .start, .end
.alignItems(.center)  // .start, .end, .baseline
.flexGap(16)
.gridCellColumns(2)
.gridCellRows(3)
```

### Transforms and Transitions

```swift
.offset(x: 16, y: 32)
.opacity(0.5)
.colorInvert()
.animation(.easeIn(duration: 0.25))
.transition(.all)
```

### Responsive and State

```swift
.fontSize(.base)
.fontSize(.large, condition: .desktop)
.textColor(.blue)
.textColor(.red, condition: .hover)
```

Available conditions:
- Breakpoints: `.mobile`, `.tablet`, `.desktop`, `.widescreen`
- States: `.hover`, `.focus`, `.active`, `.visited`, `.disabled`

## Environment System

Slipstream provides SwiftUI-like environment for passing data down the view hierarchy:

### Define Custom Environment Key

```swift
struct PathKey: EnvironmentKey {
  static var defaultValue: String = "/"
}

extension EnvironmentValues {
  var path: String {
    get { self[PathKey.self] }
    set { self[PathKey.self] = newValue }
  }
}
```

### Use Environment

```swift
struct MyView: View {
  @Environment(\.path) var path

  var body: some View {
    Text("Current path: \(path)")
  }
}

// Inject environment value
MyView()
  .environment(\.path, "/home")
```

## Rendering

### Render Single View

```swift
import Slipstream

struct HelloWorld: View {
  var body: some View {
    Text("Hello, world!")
  }
}

let html = try renderHTML(HelloWorld())
print(html)
```

### Render Sitemap

```swift
import Foundation
import Slipstream

let sitemap: Sitemap = [
  "index.html": HomePage(),
  "about/index.html": AboutPage(),
  "blog/post-1.html": BlogPost(id: 1)
]

let outputURL = URL(filePath: #filePath)
  .deletingLastPathComponent()
  .deletingLastPathComponent()
  .appending(path: "site")

try renderSitemap(sitemap, to: outputURL)
```

## W3C Global Attributes

All views support W3C global attributes:

```swift
.id("unique-id")
.className("custom-class")
.title("Tooltip")
.data("key", "value")
.accessibilityLabel("Screen reader text")
.language("en")
.dir(.ltr)  // .rtl
.contentEditable(.true)
.spellcheck(true)
.draggable(true)
.tabindex(1)
.disabled(true)
.hidden()
.inert(true)
.autofocus(true)
```

## Best Practices

### 1. Composition

Break complex views into smaller, reusable components:

```swift
struct Navigation: View {
  var body: some View {
    Header {
      HStack {
        Link("Home", destination: "/")
        Link("About", destination: "/about")
      }
    }
  }
}

struct HomePage: View {
  var body: some View {
    Navigation()
    DocumentMain {
      H1("Welcome")
      Text("Home page content")
    }
  }
}
```

### 2. Use Semantic HTML

Choose semantic elements over generic containers:
- Use `Header`, `Footer`, `Navigation`, `Article` instead of generic divs
- Use `H1`-`H6` for headings, not styled `Text`
- Use `Strong` for semantic emphasis, `Bold` for visual only

### 3. Responsive Design

Apply responsive modifiers for different screen sizes:

```swift
Text("Responsive")
  .fontSize(.base)
  .fontSize(.large, condition: .tablet)
  .fontSize(.extraLarge, condition: .desktop)
  .padding(4)
  .padding(8, condition: .tablet)
```

### 4. Tailwind CSS Alignment

Remember that Slipstream uses Tailwind's predefined sizes, not exact pixel values. The framework finds the closest Tailwind class to requested values.

### 5. Environment for Shared State

Use environment for configuration that needs to flow down the hierarchy:

```swift
struct Theme {
  var primaryColor: TailwindColor
  var accentColor: TailwindColor
}

// Define environment key, inject at top level, read in child views
```

## Common Patterns

### Page Layout Template

```swift
struct PageTemplate<Content: View>: View {
  let title: String
  @ViewBuilder let content: () -> Content

  var body: some View {
    Container {
      Header {
        Navigation {
          Link("Home", destination: "/")
          Link("About", destination: "/about")
        }
      }
      DocumentMain {
        H1(title)
        content()
      }
      Footer {
        Text("© 2025 My Site")
      }
    }
  }
}

// Usage
PageTemplate(title: "About") {
  Text("About page content")
}
```

### Card Component

```swift
struct Card<Content: View>: View {
  @ViewBuilder let content: () -> Content

  var body: some View {
    VStack(alignment: .leading, spacing: 16) {
      content()
    }
    .padding(24)
    .backgroundColor(.white)
    .cornerRadius(.large)
    .shadow(.medium)
  }
}
```

### Hero Section

```swift
struct Hero: View {
  let title: String
  let subtitle: String

  var body: some View {
    VStack(alignment: .center, spacing: 24) {
      H1(title)
        .fontSize(.extraLarge5)
        .fontWeight(.bold)
        .textColor(.gray, shade: .x900)
      Text(subtitle)
        .fontSize(.extraLarge)
        .textColor(.gray, shade: .x600)
    }
    .padding(.vertical, 96)
    .textAlignment(.center)
  }
}
```

## Package Setup

### Package.swift

```swift
// swift-tools-version: 5.10
import PackageDescription

let package = Package(
  name: "mysite",
  platforms: [
    .macOS("14"),
    .iOS("17"),
  ],
  dependencies: [
    .package(url: "https://github.com/jverkoey/slipstream.git", branch: "main"),
  ],
  targets: [
    .executableTarget(name: "mysite", dependencies: [
      .product(name: "Slipstream", package: "slipstream"),
    ]),
  ]
)
```

### Tailwind CSS Configuration

tailwind.config.js:
```javascript
module.exports = {
  content: ["./site/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

tailwind.css:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### Build Command

```bash
swift run && npx tailwindcss -i tailwind.css -o ./site/output.css --minify
```

## Quick Reference

### Color Palette

Available colors: `.black`, `.white`, `.gray`, `.red`, `.orange`, `.amber`, `.yellow`, `.lime`, `.green`, `.emerald`, `.teal`, `.cyan`, `.sky`, `.blue`, `.indigo`, `.violet`, `.purple`, `.fuchsia`, `.pink`, `.rose`

Shades: `.x50`, `.x100`, `.x200`, `.x300`, `.x400`, `.x500`, `.x600`, `.x700`, `.x800`, `.x900`, `.x950`

### Font Sizes

`.extraSmall`, `.small`, `.base`, `.large`, `.extraLarge`, `.extraLarge2`, `.extraLarge3`, `.extraLarge4`, `.extraLarge5`, `.extraLarge6`, `.extraLarge7`, `.extraLarge8`, `.extraLarge9`

### Font Weights

`.thin`, `.extraLight`, `.light`, `.normal`, `.medium`, `.semibold`, `.bold`, `.extraBold`, `.black`

### Spacing Scale

Common values: 0, 1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 56, 64, 96, 128

### Shadow Sizes

`.small`, `.medium`, `.large`, `.extraLarge`, `.extraLarge2`, `.inner`, `.none`

### Corner Radius

`.none`, `.small`, `.medium`, `.large`, `.extraLarge`, `.extraLarge2`, `.extraLarge3`, `.full`

## When to Use This Skill

Use this skill when:
- Building static websites with Swift
- Converting SwiftUI-like code to HTML
- Working with Tailwind CSS utilities in Swift
- Creating reusable view components for web
- Setting up Slipstream projects
- Rendering sitemaps and multi-page sites
- Implementing responsive layouts
- Using W3C HTML elements and attributes
- Working with SVG or MathML in Slipstream
- Managing environment values
- Troubleshooting Slipstream rendering

## Documentation References

The complete Slipstream documentation is available at:
- Main docs: https://slipstream.clutch.engineering/documentation/slipstream/
- GitHub: https://github.com/jverkoey/slipstream
- Site template: https://github.com/jverkoey/slipstream-site-template

Local documentation is in: `Sources/Slipstream/Documentation.docc/`
