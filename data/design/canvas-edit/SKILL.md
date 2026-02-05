---
name: canvas-edit
description: Live Annotation Feedback Toolbar that overlays design review findings directly on web pages. Displays numbered badges on elements with issues, severity indicators, filtering, and screenshot capture. Integrates with design-review for real-time issue display. Triggers on "show annotations", "display issues", "annotate page", "overlay findings", or after running design-review.
---

# Canvas Edit - Live Annotation Toolbar

Floating toolbar that overlays design review findings directly on web pages in real-time. Displays numbered badges on problematic elements with severity-colored borders, hover popovers for issue details, and one-click screenshot capture.

**Key features:**
- **Live annotations** - Numbered badges appear on elements as issues are found
- **Severity indicators** - Color-coded badges (red/orange/blue) with counts
- **Issue popovers** - Click badges to see full issue details and recommendations
- **Screenshot capture** - Capture annotated page (toolbar hidden, annotations visible)
- **Shadow DOM** - Toolbar is invisible to agent-eyes screenshots
- **Filtering** - Filter by severity or pillar category

## Breaking Changes from v1

> **This is a complete redesign.** Canvas-edit is now a **viewing tool**, not an editing tool.

| Old Functionality | New Behavior |
|-------------------|--------------|
| Text editing via textarea | **REMOVED** |
| Style sliders (fontSize, etc.) | **REMOVED** |
| "Save All to Code" button | **REPLACED** with screenshot capture |
| contentEditable toggle | **REMOVED** |
| `edit` command | **REPLACED** with `inject` command |

For live editing, use `agent-canvas --with-edit` instead.

## Prerequisites

- Python 3.10+
- `uv` package manager
- Playwright browsers: `playwright install chromium`

## Commands

```bash
SKILL_DIR=".claude/skills/canvas-edit/scripts"
```

### Inject Annotations onto Page

```bash
# Inject toolbar with issues from JSON file
uv run $SKILL_DIR/canvas_edit.py inject http://localhost:3000 --issues issues.json

# Inject with issues from stdin
echo '[{"id": 1, "selector": "h1", "severity": "major", "title": "Contrast issue"}]' | \
  uv run $SKILL_DIR/canvas_edit.py inject http://localhost:3000 --issues -

# Auto-screenshot on load
uv run $SKILL_DIR/canvas_edit.py inject http://localhost:3000 --issues issues.json --screenshot
```

### Typical Workflow: Design Review + Annotations

```bash
# 1. Run design review to find issues
uv run .claude/skills/design-review/scripts/design_review.py review http://localhost:3000 \
  --output-json issues.json

# 2. Inject annotations onto the page
uv run $SKILL_DIR/canvas_edit.py inject http://localhost:3000 --issues issues.json

# 3. User interacts with annotations, takes screenshots, closes browser
```

## Toolbar Controls

The floating toolbar (top-right by default) provides:

**Status Display**
- Issue count ("5 Issues" or "All looks good!")
- Severity badges: 🔴 blocking, 🟡 major, 🔵 minor

**Actions**
- **👁 Visibility**: Show/hide all annotations
- **⚙ Filter**: Filter by severity or pillar category
- **📸 Screenshot**: Capture page with annotations (toolbar hidden)
- **↕/↔ Orientation**: Toggle vertical/horizontal toolbar
- **✕ Dismiss**: Remove toolbar and all annotations

**Dragging**
- Grab the ☰ handle to drag toolbar anywhere on screen
- Position persists during session

## Annotation Badges

Each issue appears as a numbered badge on its target element:

- **Position**: Top-right of target element (auto-adjusts at screen edges)
- **Color**: Border matches severity (red/orange/blue)
- **Click**: Opens popover with full issue details
- **Hover**: Highlights the target element

### Badge Popover Contents

```
┌─────────────────────────────────────┐
│ #3  Contrast issue         [major] │
├─────────────────────────────────────┤
│ Color contrast ratio 3.2:1 fails   │
│ WCAG AA requirement of 4.5:1       │
│                                     │
│ Pillar: Quality Craft               │
│ Check: color-contrast               │
├─────────────────────────────────────┤
│ Recommendation:                     │
│ Change text color to #1a1a1a or    │
│ background to #ffffff              │
└─────────────────────────────────────┘
```

## Issue JSON Format

Issues can come from design-review output or be manually constructed:

```json
[
  {
    "id": 1,
    "selector": ".hero-title",
    "severity": "major",
    "title": "Contrast ratio insufficient",
    "description": "Text contrast 3.2:1 fails WCAG AA (4.5:1 required)",
    "pillar": "Quality Craft",
    "checkId": "color-contrast",
    "recommendation": "Use darker text (#1a1a1a) or lighter background"
  },
  {
    "id": 2,
    "selector": "button.submit",
    "severity": "minor",
    "title": "Touch target too small",
    "description": "Button is 36x28px, minimum is 44x44px",
    "pillar": "Quality Craft",
    "checkId": "touch-target-size"
  }
]
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | Unique identifier |
| `selector` | string | CSS selector for target element |
| `severity` | string | `"blocking"`, `"major"`, or `"minor"` |
| `title` | string | Short issue title |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | Detailed explanation |
| `pillar` | string | Design pillar category |
| `checkId` | string | Identifier for the check that found this |
| `recommendation` | string | Suggested fix |

## Event API (Canvas Bus)

Canvas-edit integrates with other skills via the canvas bus event system.

### Events Emitted

| Event | Payload | When |
|-------|---------|------|
| `annotation.clicked` | `{issueId, selector, severity}` | User clicks a badge |
| `screenshot.requested` | `{directory, filename, issueCount}` | Screenshot button clicked |
| `screenshot.captured` | `{path, issueCount}` | Screenshot saved (Python-side) |
| `annotations.cleared` | `{}` | Dismiss button clicked |
| `filter.changed` | `{severity, pillars}` | Filter settings changed |

### Events Subscribed

| Event | Action |
|-------|--------|
| `review.started` | Show "Scanning..." state |
| `review.issue_found` | Add badge for new issue |
| `review.completed` | Show final count or success message |
| `capture_mode.changed` | Hide/show toolbar for agent-eyes |

### Integration Example

```javascript
// In another skill's JavaScript
const bus = window.__canvasBus;

// Listen for annotation clicks
bus.subscribe('annotation.clicked', (payload) => {
  console.log(`Issue ${payload.issueId} clicked: ${payload.selector}`);
});

// Add an issue programmatically
window.__annotationLayer.addIssue({
  id: 99,
  selector: '.problematic-element',
  severity: 'major',
  title: 'New issue found'
});
```

## Screenshot Output

Screenshots are saved to `.canvas/screenshots/` with timestamp filenames:

```
.canvas/screenshots/
├── 2026-01-23T15-30-45_5-issues.png
└── 2026-01-23T15-45-12_0-issues.png
```

Filename format: `YYYY-MM-DDTHH-MM-SS_N-issues.png`

Screenshots capture:
- Full page content
- All visible annotation badges
- Element highlights (if active)
- **NOT** the toolbar (hidden during capture)

## Toolbar States

| State | Display | Trigger |
|-------|---------|---------|
| **Issues Found** | "N Issues" + severity badges | Default when issues > 0 |
| **All Clear** | "✓ All looks good!" (randomized) | Zero issues after review completes |
| **Scanning** | "⟳ Analyzing..." with spinner | During `review.started` |

Success messages rotate randomly:
- "All looks good!"
- "Ship it!"
- "Pixel perfect"
- "Zero issues found"
- "Looking sharp!"

## Keyboard Navigation

| Key | Action |
|-----|--------|
| `Tab` | Navigate toolbar controls |
| `1-9` | Jump to badge by number |
| `Arrow keys` | Navigate between visible badges |
| `Enter/Space` | Activate focused button/badge |
| `Escape` | Close open popover |

## Shadow DOM Isolation

The toolbar is rendered inside a closed Shadow DOM:
- Invisible to `document.querySelector()`
- Excluded from agent-eyes DOM snapshots
- Hidden from screenshots (annotations remain visible)
- Page styles cannot affect toolbar appearance

## Notes

- Toolbar auto-repositions to stay on screen when dragged or resized
- Badges reposition when window resizes or scrolls
- Multiple badges on the same element stack with offset
- Orphaned badges (element removed) are automatically cleaned up
- Filter state persists during session but resets on page reload
