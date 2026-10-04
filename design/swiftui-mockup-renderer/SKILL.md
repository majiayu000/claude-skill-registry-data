---
name: swiftui-mockup-renderer
description: Generate native SwiftUI mockups, compile them, and capture real screenshots — no HTML approximation.
---
# SwiftUI Mockup Renderer

Generates native SwiftUI source, compiles it with `swiftc`, renders headlessly via `ImageRenderer`, and captures PNG screenshots in both light and dark mode. The output is pixel-accurate platform UI — real system controls, SF Pro typography, correct spacing, vibrancy, and blur.

## Return contract (read first)

When this skill runs inside a subagent (the usual case via `ui-designer` or `/mock`), the subagent's narrative return text is **not shown directly to the user** — the orchestrator surfaces a parseable file list. The last thing the subagent emits MUST be a `<MOCKUP_FILES>` block listing every file written:

```
<MOCKUP_FILES>
.hero/mocks/{slug}/screenshot.png|Screenshot — light|image
.hero/mocks/{slug}/screenshot-dark.png|Screenshot — dark|image
.hero/mocks/{slug}/MockView.swift|SwiftUI source|source
.hero/mocks/{slug}/index.html|Viewer page|primary
.hero/planning/features/{slug}/spec.md|Spec (Mockups section updated)|spec
</MOCKUP_FILES>
```

One file per line, pipe-separated `path|label|kind`. Include both light and dark PNGs even if only one was requested. Skip this block and the user sees no links. See the `ui-designer` agent definition for full rules.

## When to use

Selection is now driven by `hero spec mock detect` (see `hero spec mock detect --help`). The agent does not decide — the CLI does. This skill is loaded whenever the detect output's `renderer` field is `"swiftui"`. Selection drivers (any of):

- Swift stack signals (`.swift`, `Package.swift`, `*.xcodeproj`, `*.xcworkspace`) anywhere `hero spec mock detect` walks
- Explicit `--renderer=swiftui`
- `hero.json` `mockups.renderer: "swiftui"`

**Prerequisites:** macOS with Xcode command-line tools installed (`swiftc` available on PATH). The CLI gates on this and falls back to HTML (with explicit announce) when `swiftc` is missing.

## Source Generation

Generate a single `MockView.swift` containing all the UI. The file must be self-contained — no package dependencies, no custom assets, no external frameworks beyond SwiftUI and AppKit.

### File Structure

```swift
// Hero Mock: {slug} | Generated: {date}
// Description: {one-line description}

import SwiftUI
import AppKit

// MARK: - Mock View

struct MockView: View {
    // @State properties for interactivity

    var body: some View {
        // View hierarchy
    }
}

// MARK: - Supporting Views (if needed)

// Break complex UIs into smaller structs for readability

// MARK: - Capture Entry Point

@main
struct MockApp {
    static func main() {
        let args = CommandLine.arguments
        let isDark = args.contains("--dark")
        let width: CGFloat = 390
        let height: CGFloat = 844

        // Parse --size if provided
        // Parse --scale if provided (default 2)

        let view = MockView()
            .frame(width: width, height: height)
            .environment(\.colorScheme, isDark ? .dark : .light)

        let renderer = ImageRenderer(content: view)
        renderer.scale = 2.0

        guard let image = renderer.nsImage else {
            fputs("error: failed to render view\n", stderr)
            exit(1)
        }

        guard let tiff = image.tiffRepresentation,
              let bitmap = NSBitmapImageRep(data: tiff),
              let png = bitmap.representation(using: .png, properties: [:]) else {
            fputs("error: failed to encode PNG\n", stderr)
            exit(1)
        }

        let outputPath = isDark ? "screenshot-dark.png" : "screenshot.png"
        do {
            try png.write(to: URL(fileURLWithPath: outputPath))
        } catch {
            fputs("error: \(error.localizedDescription)\n", stderr)
            exit(1)
        }
    }
}
```

The `@main` entry point is bundled into the same file. This lets `swiftc` compile and run it as a single unit with no project file.

### Design Guidelines

**Use real SwiftUI components:**
- `NavigationStack` / `NavigationSplitView` for navigation
- `List`, `Form`, `Section` for scrollable content
- `Toggle`, `Picker`, `Slider`, `Stepper` for controls
- `Button`, `Menu`, `Link` for actions
- `TabView` for tab-based layouts
- `TextField`, `TextEditor`, `SecureField` for input
- `ProgressView`, `Gauge` for progress
- `Label`, `LabeledContent` for labeled items
- `GroupBox`, `DisclosureGroup` for grouping

**Icons — use SF Symbols:**
```swift
Image(systemName: "gear")
Image(systemName: "person.circle.fill")
Image(systemName: "chart.bar.fill")
```

Never reference custom image assets. SF Symbols are always available.

**Colors — use system semantic colors:**
```swift
Color.primary          // adapts to light/dark
Color.secondary
Color.accentColor
Color(.systemBackground)
Color(.secondarySystemBackground)
Color(.tertiarySystemBackground)
Color(.separator)
Color(.label)
Color(.secondaryLabel)
```

For brand colors, define them inline:
```swift
extension Color {
    static let heroPrimary = Color(red: 0.29, green: 0.62, blue: 1.0)
}
```

**Typography — use system styles:**
```swift
.font(.largeTitle)
.font(.title)
.font(.title2)
.font(.headline)
.font(.subheadline)
.font(.body)
.font(.callout)
.font(.caption)
.font(.footnote)
```

**Spacing — use system defaults:**
Let SwiftUI handle spacing wherever possible. Use explicit padding only when needed:
```swift
.padding()              // system default (16pt)
.padding(.horizontal)
.padding(8)
```

### Layout Patterns

**Settings / Form screen:**
```swift
Form {
    Section("Account") {
        LabeledContent("Name", value: "Sarah Chen")
        LabeledContent("Email", value: "sarah@example.com")
        Toggle("Notifications", isOn: .constant(true))
    }
    Section("Appearance") {
        Picker("Theme", selection: .constant(0)) {
            Text("System").tag(0)
            Text("Light").tag(1)
            Text("Dark").tag(2)
        }
    }
}
.navigationTitle("Settings")
```

**List / Master-detail:**
```swift
NavigationStack {
    List {
        ForEach(items) { item in
            NavigationLink(value: item) {
                HStack {
                    Image(systemName: item.icon)
                    VStack(alignment: .leading) {
                        Text(item.title).font(.headline)
                        Text(item.subtitle).font(.caption).foregroundStyle(.secondary)
                    }
                }
            }
        }
    }
    .navigationTitle("Items")
}
```

**Dashboard / Metrics:**
```swift
ScrollView {
    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 16) {
        MetricCard(title: "Revenue", value: "$12,847", icon: "dollarsign.circle.fill", color: .green)
        MetricCard(title: "Users", value: "1,284", icon: "person.2.fill", color: .blue)
    }
    .padding()
}
```

**Tab-based app:**
```swift
TabView {
    HomeView()
        .tabItem { Label("Home", systemImage: "house.fill") }
    SearchView()
        .tabItem { Label("Search", systemImage: "magnifyingglass") }
    ProfileView()
        .tabItem { Label("Profile", systemImage: "person.fill") }
}
```

### Realistic Data

Same rules as HTML mockups — use realistic-looking placeholder data:
- Names: "Sarah Chen", "Marcus Johnson", "Aisha Patel"
- Emails: "sarah.chen@example.com"
- Dates: relative where possible (`Date.now.addingTimeInterval(-3600)`)
- Numbers: realistic ranges ("$12,847" not "$10,000")
- Status values: use actual statuses from the spec if available

### What NOT to Do

- Don't import external packages (no SPM dependencies)
- Don't reference custom image assets or asset catalogs
- Don't use UIKit types (this renders via AppKit on macOS)
- Don't use `@Observable` macro (requires Swift 5.9 macro support — use `@State` instead)
- Don't create Xcode projects or Package.swift
- Don't use `PreviewProvider` — the capture entry point replaces previews
- Don't add complex animations — they don't render in `ImageRenderer`
- Don't target iOS-only APIs — the code runs on macOS for capture
- Don't include more than 2-3 screens in one file

### macOS Compatibility Notes

The mockup renders on macOS via `ImageRenderer` + AppKit, even when mocking an iOS app. Key adaptations:

- Use `NavigationStack` (not `NavigationView` deprecated path)
- Avoid `UIScreen`, `UIDevice`, or any UIKit references
- `ImageRenderer` is available on macOS 13+ / Swift 5.7+
- The `.frame(width: 390, height: 844)` constrains the render to iPhone dimensions
- System controls will render in macOS style — this is acceptable for mockup purposes. The layout, spacing, and content are what matter.

## Build and Capture Pipeline

After generating `MockView.swift`, execute this pipeline:

### Step 1: Verify toolchain
```bash
which swiftc || { echo "swiftc not found — falling back to HTML"; exit 1; }
```

### Step 2: Compile
```bash
cd .hero/mocks/{slug}
swiftc MockView.swift -framework SwiftUI -framework AppKit -o MockApp 2>&1
```

If compilation fails, read the error, attempt one auto-fix of the Swift source, and retry. If the retry also fails, fall back to HTML.

### Step 3: Capture light mode
```bash
./MockApp
```
Produces `screenshot.png` in the current directory.

### Step 4: Capture dark mode
```bash
./MockApp --dark
```
Produces `screenshot-dark.png`.

### Step 5: Clean up binary
```bash
rm -f MockApp
```

### Step 6: Generate viewer HTML

Create an `index.html` that displays both screenshots with a light/dark toggle and a collapsible source view. This ensures `hero spec mock --open` and `hero spec mock --serve` keep working.

**The viewer MUST be a single self-contained file.** Do not reference the PNGs by relative path (`<img src="screenshot.png">`) — a relative path only resolves when the file is served with its own directory as the web root (`--open` / `--serve`), and breaks in embedded preview panes that load the HTML detached from its siblings (via `srcdoc`, a blob URL, or a different web root). Embed both PNGs as base64 `data:image/png;base64,…` URIs so there is no path to resolve. This mirrors the `html-mockup-generation` rule: no external resources, ever.

First, base64-encode both screenshots:
```bash
LIGHT_B64=$(base64 < screenshot.png | tr -d '\n')
DARK_B64=$(base64 < screenshot-dark.png | tr -d '\n')
```
Then substitute the values into the template's `data:image/png;base64,{LIGHT_B64}` / `{DARK_B64}` slots. (If `swiftui.capture_dark_mode` is off, embed only the light image and drop the toggle.)

```html
<!DOCTYPE html>
<!-- Hero Mock: {slug} | Generated: {date} | Renderer: swiftui -->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{Title} — Native Mock</title>
    <style>
        body { font-family: -apple-system, system-ui, sans-serif; margin: 0; padding: 32px; background: #f5f5f5; color: #333; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
        h1 { font-size: 20px; font-weight: 600; margin: 0; }
        .badge { background: #d4edda; color: #155724; padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .toggle-bar { display: flex; gap: 8px; margin-bottom: 24px; }
        .toggle-btn { padding: 6px 16px; border: 1px solid #ddd; border-radius: 6px; background: #fff; cursor: pointer; font-size: 13px; }
        .toggle-btn.active { background: #333; color: #fff; border-color: #333; }
        .screenshot-frame { background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1); display: inline-block; padding: 16px; }
        .screenshot-frame img { max-width: 100%; height: auto; border-radius: 8px; }
        .source-toggle { margin-top: 32px; cursor: pointer; font-size: 14px; color: #666; }
        .source-block { display: none; margin-top: 12px; background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 13px; line-height: 1.5; }
        .source-block pre { margin: 0; white-space: pre; }
    </style>
</head>
<body>
    <div class="header">
        <h1>{Title}</h1>
        <span class="badge">SwiftUI</span>
    </div>
    <div class="toggle-bar">
        <button class="toggle-btn active" onclick="showMode('light')">Light</button>
        <button class="toggle-btn" onclick="showMode('dark')">Dark</button>
    </div>
    <div class="screenshot-frame">
        <img id="screenshot"
             src="data:image/png;base64,{LIGHT_B64}"
             data-light="data:image/png;base64,{LIGHT_B64}"
             data-dark="data:image/png;base64,{DARK_B64}"
             alt="Mock screenshot">
    </div>
    <div class="source-toggle" onclick="toggleSource()">&#9654; View SwiftUI source</div>
    <div class="source-block" id="source">
        <pre><code>/* Source loaded from MockView.swift */</code></pre>
    </div>
    <script>
        function showMode(mode) {
            const img = document.getElementById('screenshot');
            img.src = mode === 'dark' ? img.dataset.dark : img.dataset.light;
            document.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
        }
        function toggleSource() {
            const el = document.getElementById('source');
            const toggle = document.querySelector('.source-toggle');
            if (el.style.display === 'block') {
                el.style.display = 'none';
                toggle.innerHTML = '&#9654; View SwiftUI source';
            } else {
                el.style.display = 'block';
                toggle.innerHTML = '&#9660; Hide SwiftUI source';
            }
        }
    </script>
</body>
</html>
```

Replace the `<code>` block with the actual contents of `MockView.swift` (HTML-escaped) when generating.

## Output Manifest

Every SwiftUI mock produces:

| File | Purpose |
|---|---|
| `MockView.swift` | Generated SwiftUI source |
| `screenshot.png` | Light mode render (@2x) |
| `screenshot-dark.png` | Dark mode render (@2x) |
| `index.html` | Viewer page (wraps PNGs + source) |

The compiled binary (`MockApp`) is deleted after capture.

## Configuration

The `mockups` section in `hero.json`:

```json
{
  "mockups": {
    "renderer": "auto",
    "swiftui": {
      "device_frame": "iPhone 15 Pro",
      "size": "390x844",
      "scale": 2,
      "capture_dark_mode": true
    }
  }
}
```

- `renderer` — `"auto"` (detect from stack), `"html"`, or `"swiftui"`
- `swiftui.size` — render dimensions (width x height)
- `swiftui.scale` — display scale factor (1, 2, or 3)
- `swiftui.capture_dark_mode` — whether to produce `screenshot-dark.png`

## Error Recovery

1. **`swiftc` not found:** Fall back to HTML. Log: "SwiftUI renderer unavailable (swiftc not found), using HTML."
2. **Compilation error:** Read the compiler error, attempt one auto-fix of the source, retry. If retry fails, fall back to HTML with the error shown to the user.
3. **Runtime crash:** Fall back to HTML. Log the crash output.
4. **Empty screenshot:** Retry with explicit `.frame()`. If still empty, fall back to HTML.

## Spec Write-back

Same rules as `html-mockup-generation`:

When invoked against a spec slug, append (or update on `--iterate`) a `## Mockups` entry in the originating spec. Entry format:
```
- [{Name}](.hero/mocks/{slug}/screenshot.png) — YYYY-MM-DD — SwiftUI native render
```

Link to `screenshot.png` rather than `index.html` so the mockup image is visible directly in spec viewers that support image embedding.

### Location priority
1. `.hero/planning/features/{slug}/spec.md`
2. `.hero/planning/bugs/{slug}/spec.md`
3. `.hero/specs/{slug}/spec.md` (archive fallback)

### Iteration
On `--iterate`, update the existing entry's date in place rather than appending a duplicate.
