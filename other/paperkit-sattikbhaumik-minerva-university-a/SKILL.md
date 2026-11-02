---
name: paperkit
description: "Add drawings, shapes, and a consistent markup experience using PaperKit. Use when integrating PaperMarkupViewController for markup editing, adding shape recognition, working with PaperMarkup data models, embedding markup tools in document editors, or building annotation features that need the system-standard markup toolbar. New in iOS 26."
---

# PaperKit

> **Beta-sensitive.** PaperKit is new in iOS/iPadOS 26, macOS 26, and visionOS 26. API surface may change. Verify details against current Apple documentation before shipping.

PaperKit provides a unified markup experience — the same framework powering markup in Notes, Screenshots, QuickLook, and Journal. It combines PencilKit drawing with structured markup elements (shapes, text boxes, images, lines) in a single canvas managed by `PaperMarkupViewController`. Requires Swift 6.3 and the iOS 26+ SDK.

## Contents

- [Setup](#setup)
- [PaperMarkupViewController](#papermarkupviewcontroller)
- [PaperMarkup Data Model](#papermarkup-data-model)
- [Insertion Controllers](#insertion-controllers)
- [FeatureSet Configuration](#featureset-configuration)
- [Integration with PencilKit](#integration-with-pencilkit)
- [SwiftUI Integration](#swiftui-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Setup

PaperKit requires no entitlements or special Info.plist entries.

```swift
import PaperKit
```

**Platform availability:** iOS 26.0+, iPadOS 26.0+, Mac Catalyst 26.0+, macOS 26.0+, visionOS 26.0+.

Three core components:

| Component | Role |
|---|---|
| `PaperMarkupViewController` | Interactive canvas for creating and displaying markup and drawing |
| `PaperMarkup` | Data model for serializing all markup elements and PencilKit drawing |
| `MarkupEditViewController` / `MarkupToolbarViewController` | Insertion UI for adding markup elements |

## PaperMarkupViewController

The primary view controller for interactive markup. Provides a scrollable canvas for freeform PencilKit drawing and structured markup elements. Conforms to `Observable` and `PKToolPickerObserver`.

### Basic UIKit Setup

```swift
import PaperKit
import PencilKit
import UIKit

class MarkupViewController: UIViewController, PaperMarkupViewController.Delegate {
    var paperVC: PaperMarkupViewController!
    var toolPicker: PKToolPicker!

    override func viewDidLoad() {
        super.viewDidLoad()

        let markup = PaperMarkup(bounds: view.bounds)
        paperVC = PaperMarkupViewController(
            markup: markup,
            supportedFeatureSet: .latest
        )
        paperVC.delegate = self

        addChild(paperVC)
        paperVC.view.frame = view.bounds
        paperVC.view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        view.addSubview(paperVC.view)
        paperVC.didMove(toParent: self)

        toolPicker = PKToolPicker()
        toolPicker.addObserver(paperVC)
        paperVC.pencilKitResponderState.activeToolPicker = toolPicker
        paperVC.pencilKitResponderState.toolPickerVisibility = .visible
    }

    func paperMarkupViewControllerDidChangeMarkup(
        _ controller: PaperMarkupViewController
    ) {
        guard let markup = controller.markup else { return }
        Task { try await save(markup) }
    }
}
```

### Key Properties

| Property | Type | Description |
|---|---|---|
| `markup` | `PaperMarkup?` | The current data model |
| `selectedMarkup` | `PaperMarkup` | Currently selected content |
| `isEditable` | `Bool` | Whether the canvas accepts input |
| `isRulerActive` | `Bool` | Whether the ruler overlay is shown |
| `drawingTool` | `any PKTool` | Active PencilKit drawing tool |
| `contentView` | `UIView?` / `NSView?` | Background view rendered beneath markup |
| `zoomRange` | `ClosedRange<CGFloat>` | Min/max zoom scale |
| `supportedFeatureSet` | `FeatureSet` | Enabled PaperKit features |

### Touch Modes

`PaperMarkupViewController.TouchMode` has two cases: `.drawing` and `.selection`.

```swift
paperVC.directTouchMode = .drawing    // Finger draws
paperVC.directTouchMode = .selection  // Finger selects elements
paperVC.directTouchAutomaticallyDraws = true  // System decides based on Pencil state
```

### Content Background

Set any view beneath the markup layer for templates, document pages, or images being annotated:

```swift
paperVC.contentView = UIImageView(image: UIImage(named: "template"))
```

### Delegate Callbacks

| Method | Called when |
|---|---|
| `paperMarkupViewControllerDidChangeMarkup(_:)` | Markup content changes |
| `paperMarkupViewControllerDidBeginDrawing(_:)` | User starts drawing |
| `paperMarkupViewControllerDidChangeSelection(_:)` | Selection changes |
| `paperMarkupViewControllerDidChangeContentVisibleFrame(_:)` | Visible frame changes |

## PaperMarkup Data Model

`PaperMarkup` is a `Sendable` struct that stores all markup elements and PencilKit drawing data.

### Creating and Persisting

```swift
// New empty model
let markup = PaperMarkup(bounds: CGRect(x: 0, y: 0, width: 612, height: 792))

// Load from saved data
let markup = try PaperMarkup(dataRepresentation: savedData)

// Save — dataRepresentation() is async throws
func save(_ markup: PaperMarkup) async throws {
    let data = try await markup.dataRepresentation()
    try data.write(to: fileURL)
}
```

### Inserting Content Programmatically

```swift
// Text box
markup.insertNewTextbox(
    attributedText: AttributedString("Annotation"),
    frame: CGRect(x: 50, y: 100, width: 200, height: 40),
    rotation: 0
)

// Image
markup.insertNewImage(cgImage, frame: CGRect(x: 50, y: 200, width: 300, height: 200), rotation: 0)

// Shape
let shapeConfig = ShapeConfiguration(
    type: .rectangle,
    fillColor: UIColor.systemBlue.withAlphaComponent(0.2).cgColor,
    strokeColor: UIColor.systemBlue.cgColor,
    lineWidth: 2
)
markup.insertNewShape(configuration: shapeConfig, frame: CGRect(x: 50, y: 420, width: 200, height: 100), rotation: 0)

// Line with arrow end marker
let lineConfig = ShapeConfiguration(type: .line, fillColor: nil, strokeColor: UIColor.red.cgColor, lineWidth: 3)
markup.insertNewLine(
    configuration: lineConfig,
    from: CGPoint(x: 50, y: 550), to: CGPoint(x: 250, y: 550),
    startMarker: false, endMarker: true
)
```

Shape types: `.rectangle`, `.roundedRectangle`, `.ellipse`, `.line`, `.arrowShape`, `.star`, `.chatBubble`, `.regularPolygon`.

### Other Operations

```swift
markup.append(contentsOf: otherMarkup)       // Merge another PaperMarkup
markup.append(contentsOf: pkDrawing)          // Merge a PKDrawing
markup.transformContent(CGAffineTransform(...)) // Apply affine transform
markup.removeContentUnsupported(by: featureSet) // Strip unsupported elements
```

| Property | Description |
|---|---|
| `bounds` | Coordinate space of the markup |
| `contentsRenderFrame` | Tight bounding box of all content |
| `featureSet` | Features used by this data model's content |
| `indexableContent` | Extractable text for search indexing |

Use `suggestedFrameForInserting(contentInFrame:)` on the view controller to get a frame that avoids overlapping existing content.

## Insertion Controllers

### MarkupEditViewController (iOS, iPadOS, visionOS)

Presents a popover menu for inserting shapes, text boxes, lines, and other elements.

```swift
func showInsertionMenu(from barButtonItem: UIBarButtonItem) {
    let editVC = MarkupEditViewController(
        supportedFeatureSet: .latest,
        additionalActions: []
    )
    editVC.delegate = paperVC  // PaperMarkupViewController conforms to the delegate
    editVC.modalPresentationStyle = .popover
    editVC.popoverPresentationController?.barButtonItem = barButtonItem
    present(editVC, animated: true)
}
```

### MarkupToolbarViewController (macOS, Mac Catalyst)

Provides a toolbar with drawing tools and insertion buttons.

```swift
let toolbar = MarkupToolbarViewController(supportedFeatureSet: .latest)
toolbar.delegate = paperVC
addChild(toolbar)
toolbar.view.frame = toolbarContainerView.bounds
toolbarContainerView.addSubview(toolbar.view)
toolbar.didMove(toParent: self)
```

Both controllers must use the same `FeatureSet` as the `PaperMarkupViewController`.

## FeatureSet Configuration

`FeatureSet` controls which markup capabilities are available.

| Preset | Description |
|---|---|
| `.latest` | All current features — recommended starting point |
| `.version1` | Features from version 1 |
| `.empty` | No features enabled |

### Customizing

```swift
var features = FeatureSet.latest
features.remove(.stickers)
features.remove(.images)

// Or build up from empty
var features = FeatureSet.empty
features.insert(.drawing)
features.insert(.text)
features.insert(.shapeStrokes)
```

### Available Features

| Feature | Description |
|---|---|
| `.drawing` | Freeform PencilKit drawing |
| `.text` | Text box insertion |
| `.images` | Image insertion |
| `.stickers` | Sticker insertion |
| `.links` | Link annotations |
| `.loupes` | Loupe/magnifier elements |
| `.shapeStrokes` | Shape outlines |
| `.shapeFills` | Shape fills |
| `.shapeOpacity` | Shape opacity control |

### HDR Support

Set `colorMaximumLinearExposure` above `1.0` on both the `FeatureSet` and `PKToolPicker`:

```swift
var features = FeatureSet.latest
features.colorMaximumLinearExposure = 4.0
toolPicker.maximumLinearExposure = features.colorMaximumLinearExposure
```

Use `view.window?.windowScene?.screen.potentialEDRHeadroom` to match the device screen's capability. Use `1.0` for SDR-only.

### Shapes, Inks, and Line Markers

```swift
features.shapes = [.rectangle, .ellipse, .arrowShape, .line]
features.inks = [.pen, .pencil, .marker]
features.lineMarkerPositions = .all  // .single, .double, .plain, or .all
```

## Integration with PencilKit

PaperKit accepts `PKTool` for drawing and can append `PKDrawing` content.

```swift
import PencilKit

// Set drawing tool
paperVC.drawingTool = PKInkingTool(.pen, color: .black, width: 3)

// Merge existing PKDrawing into markup
markup.append(contentsOf: existingPKDrawing)
```

### Tool Picker Setup

```swift
let toolPicker = PKToolPicker()
toolPicker.addObserver(paperVC)
paperVC.pencilKitResponderState.activeToolPicker = toolPicker
paperVC.pencilKitResponderState.toolPickerVisibility = .visible
```

Setting `toolPickerVisibility` to `.hidden` keeps the picker functional (responds to Pencil gestures) but not visible, enabling the mini tool picker experience.

### Content Version Compatibility

`FeatureSet.ContentVersion` maps to `PKContentVersion`:

```swift
let pkVersion = features.contentVersion.pencilKitContentVersion
```

## SwiftUI Integration

Wrap `PaperMarkupViewController` in `UIViewControllerRepresentable`:

```swift
struct MarkupView: UIViewControllerRepresentable {
    @Binding var markup: PaperMarkup

    func makeUIViewController(context: Context) -> PaperMarkupViewController {
        let vc = PaperMarkupViewController(markup: markup, supportedFeatureSet: .latest)
        vc.delegate = context.coordinator
        let toolPicker = PKToolPicker()
        toolPicker.addObserver(vc)
        vc.pencilKitResponderState.activeToolPicker = toolPicker
        vc.pencilKitResponderState.toolPickerVisibility = .visible
        context.coordinator.toolPicker = toolPicker
        return vc
    }

    func updateUIViewController(_ vc: PaperMarkupViewController, context: Context) {
        if vc.markup != markup { vc.markup = markup }
    }

    func makeCoordinator() -> Coordinator { Coordinator(parent: self) }

    class Coordinator: NSObject, PaperMarkupViewController.Delegate {
        let parent: MarkupView
        var toolPicker: PKToolPicker?
        init(parent: MarkupView) { self.parent = parent }

        func paperMarkupViewControllerDidChangeMarkup(
            _ controller: PaperMarkupViewController
        ) {
            if let markup = controller.markup { parent.markup = markup }
        }
    }
}
```

## Common Mistakes

### Mismatched FeatureSets

```swift
// DON'T
let paperVC = PaperMarkupViewController(markup: m, supportedFeatureSet: .latest)
let editVC = MarkupEditViewController(supportedFeatureSet: .version1, additionalActions: [])

// DO — use the same FeatureSet for both
let features = FeatureSet.latest
let paperVC = PaperMarkupViewController(markup: m, supportedFeatureSet: features)
let editVC = MarkupEditViewController(supportedFeatureSet: features, additionalActions: [])
```

### Ignoring Content Version on Load

```swift
// DON'T
let markup = try PaperMarkup(dataRepresentation: data)
paperVC.markup = markup

// DO — check version compatibility
let markup = try PaperMarkup(dataRepresentation: data)
if markup.featureSet.isSubset(of: paperVC.supportedFeatureSet) {
    paperVC.markup = markup
} else {
    showVersionMismatchAlert()
}
```

### Blocking Main Thread with Serialization

```swift
// DON'T — dataRepresentation() is async, don't try to work around it

// DO — save from an async context
func paperMarkupViewControllerDidChangeMarkup(_ controller: PaperMarkupViewController) {
    guard let markup = controller.markup else { return }
    Task {
        let data = try await markup.dataRepresentation()
        try data.write(to: fileURL)
    }
}
```

### Forgetting to Retain the Tool Picker

```swift
// DON'T — local variable gets deallocated
func viewDidLoad() {
    let toolPicker = PKToolPicker()
    toolPicker.addObserver(paperVC)
}

// DO — store as instance property
var toolPicker: PKToolPicker!
```

### Wrong Insertion Controller for Platform

```swift
// DON'T — MarkupEditViewController is iOS/iPadOS/visionOS only

// DO
#if os(macOS)
let toolbar = MarkupToolbarViewController(supportedFeatureSet: features)
#else
let editVC = MarkupEditViewController(supportedFeatureSet: features, additionalActions: [])
#endif
```

## Review Checklist

- [ ] `import PaperKit` present; deployment target is iOS 26+ / macOS 26+ / visionOS 26+
- [ ] `PaperMarkup` initialized with bounds matching content size
- [ ] Same `FeatureSet` used for `PaperMarkupViewController` and insertion controller
- [ ] `dataRepresentation()` called in async context
- [ ] `PKToolPicker` retained as a stored property
- [ ] Delegate set on `PaperMarkupViewController` for change callbacks
- [ ] Content version checked when loading saved data
- [ ] Correct insertion controller per platform (`MarkupEditViewController` vs `MarkupToolbarViewController`)
- [ ] `MarkupError` cases handled on deserialization
- [ ] HDR: `colorMaximumLinearExposure` set on both `FeatureSet` and `PKToolPicker`

## References

- [PaperKit documentation](https://sosumi.ai/documentation/paperkit)
- [Integrating PaperKit into your app](https://sosumi.ai/documentation/paperkit/getting-started-with-paperkit)
- [Meet PaperKit — WWDC25](https://sosumi.ai/videos/play/wwdc2025/285/)
- The `pencilkit` skill covers PencilKit drawing, tool pickers, and PKDrawing serialization
- [references/paperkit-patterns.md](references/paperkit-patterns.md) — data persistence, rendering, multi-platform setup, custom feature sets
