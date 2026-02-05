---
name: mobile-testing-playwright
description: Mobile device testing with Playwright MCP for iOS and Android. Use when testing mobile apps, responsive layouts, touch interactions, device emulation, viewport testing, mobile browser testing, visual regression testing, or working with iPhone, iPad, Pixel, Galaxy devices. Covers test patterns, execution workflows, device configurations, and Playwright MCP tools.
---

# Mobile Testing with Playwright MCP

## Purpose

Comprehensive guide for testing mobile devices using Playwright MCP integration in Claude Code. Covers test patterns, execution helpers, device configurations, and visual regression testing for iOS and Android.

## When to Use

Auto-triggers when:
- Testing mobile devices or responsive layouts
- Working with Playwright MCP tools
- Testing touch interactions or gestures
- Running visual regression tests
- Configuring device emulation
- Testing iOS/Android browsers

Manual trigger when:
- Creating mobile test suites
- Debugging mobile-specific issues
- Setting up device testing workflows

---

## Quick Reference

### Target Devices

**iOS:**
- iPhone 13 Pro (390×844)
- iPhone 14 Pro (393×852)
- iPhone 15 Pro (393×852)
- iPad Pro 11" (834×1194)
- iPad Pro 12.9" (1024×1366)

**Android:**
- Pixel 5 (393×851)
- Pixel 7 (412×915)
- Pixel 8 (412×915)
- Galaxy S21 (360×800)
- Galaxy S22 (360×780)

### Playwright MCP Tools

**Navigation:**
- `mcp__playwright__browser_navigate` - Navigate to URL
- `mcp__playwright__browser_navigate_back` - Go back
- `mcp__playwright__browser_resize` - Change viewport

**Interaction:**
- `mcp__playwright__browser_click` - Tap elements
- `mcp__playwright__browser_type` - Enter text
- `mcp__playwright__browser_fill_form` - Fill multiple fields
- `mcp__playwright__browser_drag` - Drag and drop
- `mcp__playwright__browser_hover` - Hover (limited on mobile)

**Inspection:**
- `mcp__playwright__browser_snapshot` - Accessibility snapshot (preferred)
- `mcp__playwright__browser_take_screenshot` - Visual screenshot
- `mcp__playwright__browser_console_messages` - Console errors
- `mcp__playwright__browser_network_requests` - Network activity

**Waiting:**
- `mcp__playwright__browser_wait_for` - Wait for elements/text

---

## Testing Patterns

### 1. Touch Interaction Testing

**Touch Target Validation:**

```typescript
// Test touch target sizes (min 44px, recommended 48px)
// 1. Navigate and resize to mobile viewport
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
mcp__playwright__browser_resize({ width: 393, height: 852 }) // iPhone 14 Pro

// 2. Take snapshot to identify interactive elements
mcp__playwright__browser_snapshot()

// 3. Click/tap target element
mcp__playwright__browser_click({
  element: "Add to Cart button",
  ref: "button-add-to-cart" // from snapshot
})

// 4. Verify touch feedback (active states)
mcp__playwright__browser_take_screenshot({
  filename: "touch-active-state.png"
})
```

**Swipe/Scroll Testing:**

```typescript
// Test horizontal scrolling (carousels, galleries)
// 1. Take initial snapshot
mcp__playwright__browser_snapshot()

// 2. Perform swipe via drag
mcp__playwright__browser_drag({
  startElement: "carousel container",
  startRef: "div-carousel",
  endElement: "carousel end position",
  endRef: "div-carousel-end"
})

// 3. Verify scroll position changed
mcp__playwright__browser_snapshot()
```

**Form Input Testing:**

```typescript
// Test mobile keyboard interactions
// 1. Focus input field
mcp__playwright__browser_click({
  element: "email input field",
  ref: "input-email"
})

// 2. Type with mobile keyboard simulation
mcp__playwright__browser_type({
  element: "email input",
  ref: "input-email",
  text: "test@example.com",
  slowly: true // Simulate human typing
})

// 3. Submit form
mcp__playwright__browser_type({
  element: "email input",
  ref: "input-email",
  text: "",
  submit: true // Press Enter/Return
})
```

**[📖 Complete Guide: resources/test-patterns.md](resources/test-patterns.md)**

### 2. Responsive Layout Testing

**Breakpoint Verification:**

```typescript
// Test all major breakpoints
const breakpoints = [
  { name: "Mobile S", width: 320, height: 568 },
  { name: "Mobile M", width: 375, height: 667 },
  { name: "Mobile L", width: 414, height: 896 },
  { name: "Tablet", width: 768, height: 1024 },
  { name: "Laptop", width: 1024, height: 768 }
];

// For each breakpoint:
// 1. Resize viewport
mcp__playwright__browser_resize({ width: 375, height: 667 })

// 2. Take snapshot to verify layout
mcp__playwright__browser_snapshot()

// 3. Take screenshot for visual comparison
mcp__playwright__browser_take_screenshot({
  filename: "mobile-m-375px.png",
  fullPage: true
})
```

**Layout Shift Detection:**

```typescript
// Detect unwanted layout shifts during load
// 1. Navigate to page
mcp__playwright__browser_navigate({ url: "http://localhost:3000/product" })

// 2. Take immediate snapshot
mcp__playwright__browser_snapshot()

// 3. Wait for page load
mcp__playwright__browser_wait_for({ time: 2 })

// 4. Take second snapshot
mcp__playwright__browser_snapshot()

// 5. Compare for unexpected changes
// Manual verification: Check if layout shifted unexpectedly
```

**Hidden/Visible Elements:**

```typescript
// Verify mobile menu vs desktop nav
// Mobile viewport
mcp__playwright__browser_resize({ width: 375, height: 667 })
mcp__playwright__browser_snapshot()
// Verify: Mobile menu button visible, desktop nav hidden

// Desktop viewport
mcp__playwright__browser_resize({ width: 1024, height: 768 })
mcp__playwright__browser_snapshot()
// Verify: Desktop nav visible, mobile menu button hidden
```

### 3. Visual Regression Testing

**Screenshot Comparison Workflow:**

```typescript
// Baseline capture (first run)
// 1. Set device viewport
mcp__playwright__browser_resize({ width: 393, height: 852 }) // iPhone 14 Pro

// 2. Navigate to page
mcp__playwright__browser_navigate({ url: "http://localhost:3000/home" })

// 3. Wait for stability
mcp__playwright__browser_wait_for({ time: 1 })

// 4. Take baseline screenshot
mcp__playwright__browser_take_screenshot({
  filename: "baseline-iphone14-home.png",
  fullPage: true,
  type: "png"
})

// Comparison run (after changes)
// Repeat steps 1-4 with different filename
mcp__playwright__browser_take_screenshot({
  filename: "current-iphone14-home.png",
  fullPage: true,
  type: "png"
})

// Manual: Compare baseline vs current using diff tool
```

**Element-Specific Screenshots:**

```typescript
// Screenshot specific component
// 1. Navigate and resize
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
mcp__playwright__browser_resize({ width: 393, height: 852 })

// 2. Take snapshot to identify element
mcp__playwright__browser_snapshot()

// 3. Screenshot specific element
mcp__playwright__browser_take_screenshot({
  element: "product card component",
  ref: "div-product-card", // from snapshot
  filename: "product-card-mobile.png"
})
```

**Multi-Device Visual Testing:**

```typescript
// Test across all target devices
const devices = [
  { name: "iPhone14Pro", width: 393, height: 852 },
  { name: "Pixel7", width: 412, height: 915 },
  { name: "iPadPro11", width: 834, height: 1194 }
];

// For each device:
// 1. Resize
mcp__playwright__browser_resize({ width: 393, height: 852 })

// 2. Navigate
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })

// 3. Screenshot
mcp__playwright__browser_take_screenshot({
  filename: "home-iPhone14Pro.png",
  fullPage: true
})

// Repeat for all devices
```

**[📖 Complete Guide: resources/visual-regression-guide.md](resources/visual-regression-guide.md)**

---

## Execution Helpers

### Test Workflow Template

**Complete Mobile Test Session:**

```typescript
// 1. SETUP - Install browser if needed
// Check if browser is installed, if not:
mcp__playwright__browser_install()

// 2. CONFIGURE - Set mobile device
mcp__playwright__browser_resize({
  width: 393,  // iPhone 14 Pro width
  height: 852  // iPhone 14 Pro height
})

// 3. NAVIGATE - Load application
mcp__playwright__browser_navigate({
  url: "http://localhost:3000"
})

// 4. INSPECT - Check initial state
mcp__playwright__browser_snapshot()
mcp__playwright__browser_console_messages({ onlyErrors: true })

// 5. INTERACT - Perform actions
mcp__playwright__browser_click({
  element: "menu button",
  ref: "button-menu"
})

// 6. VERIFY - Check results
mcp__playwright__browser_snapshot()
mcp__playwright__browser_take_screenshot({
  filename: "test-result.png"
})

// 7. CLEANUP - Close when done
mcp__playwright__browser_close()
```

### Common Test Scenarios

**Scenario 1: Login Flow**

```typescript
// Mobile login test
mcp__playwright__browser_resize({ width: 375, height: 667 })
mcp__playwright__browser_navigate({ url: "http://localhost:3000/login" })

// Fill form
mcp__playwright__browser_fill_form({
  fields: [
    { name: "email", type: "textbox", ref: "input-email", value: "test@example.com" },
    { name: "password", type: "textbox", ref: "input-password", value: "password123" }
  ]
})

// Submit
mcp__playwright__browser_click({
  element: "login button",
  ref: "button-login"
})

// Verify redirect
mcp__playwright__browser_wait_for({ text: "Dashboard" })
mcp__playwright__browser_snapshot()
```

**Scenario 2: Product Card Interaction**

```typescript
// Test product card touch interactions
mcp__playwright__browser_resize({ width: 393, height: 852 })
mcp__playwright__browser_navigate({ url: "http://localhost:3000/products" })

// Tap product card
mcp__playwright__browser_click({
  element: "first product card",
  ref: "product-card-1"
})

// Verify navigation
mcp__playwright__browser_wait_for({ text: "Product Details" })
mcp__playwright__browser_snapshot()

// Test add to cart
mcp__playwright__browser_click({
  element: "add to cart button",
  ref: "button-add-to-cart"
})

// Verify cart updated
mcp__playwright__browser_wait_for({ text: "Added to cart" })
```

**Scenario 3: Mobile Navigation Menu**

```typescript
// Test hamburger menu
mcp__playwright__browser_resize({ width: 375, height: 667 })
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })

// Open menu
mcp__playwright__browser_click({
  element: "hamburger menu button",
  ref: "button-hamburger"
})

// Verify menu opened
mcp__playwright__browser_wait_for({ text: "Navigation Menu" })
mcp__playwright__browser_snapshot()

// Click menu item
mcp__playwright__browser_click({
  element: "About link",
  ref: "nav-link-about"
})

// Verify navigation
mcp__playwright__browser_wait_for({ text: "About Us" })
```

**[📖 More Examples: resources/test-scenarios.md](resources/test-scenarios.md)**

---

## Device Configurations

### iOS Devices

**iPhone 13 Pro:**
```typescript
mcp__playwright__browser_resize({ width: 390, height: 844 })
// User Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)
// Touch: Enabled
// Pixel Ratio: 3
```

**iPhone 14 Pro:**
```typescript
mcp__playwright__browser_resize({ width: 393, height: 852 })
// User Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)
// Touch: Enabled
// Pixel Ratio: 3
```

**iPhone 15 Pro:**
```typescript
mcp__playwright__browser_resize({ width: 393, height: 852 })
// User Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)
// Touch: Enabled
// Pixel Ratio: 3
```

**iPad Pro 11":**
```typescript
mcp__playwright__browser_resize({ width: 834, height: 1194 })
// User Agent: Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X)
// Touch: Enabled
// Pixel Ratio: 2
```

### Android Devices

**Pixel 5:**
```typescript
mcp__playwright__browser_resize({ width: 393, height: 851 })
// User Agent: Mozilla/5.0 (Linux; Android 11; Pixel 5)
// Touch: Enabled
// Pixel Ratio: 2.75
```

**Pixel 7:**
```typescript
mcp__playwright__browser_resize({ width: 412, height: 915 })
// User Agent: Mozilla/5.0 (Linux; Android 13; Pixel 7)
// Touch: Enabled
// Pixel Ratio: 2.625
```

**Galaxy S21:**
```typescript
mcp__playwright__browser_resize({ width: 360, height: 800 })
// User Agent: Mozilla/5.0 (Linux; Android 11; SM-G991B)
// Touch: Enabled
// Pixel Ratio: 3
```

**[📖 Complete Specs: resources/device-presets.md](resources/device-presets.md)**

---

## Integration with Mobile UX Standards

When testing, verify against mobile-ux-improver standards:

### Touch Target Checklist

```typescript
// Test each interactive element for:
// ✓ Min height: 44px (absolute minimum)
// ✓ Recommended height: 48px
// ✓ Spacing between targets: 8px minimum
// ✓ Active state feedback visible
// ✓ No accidental adjacent taps

// Example test:
mcp__playwright__browser_snapshot() // Identify button
mcp__playwright__browser_click({ element: "button", ref: "btn-1" })
mcp__playwright__browser_take_screenshot({
  filename: "active-state.png" // Verify visual feedback
})
```

### Responsive Design Checklist

```typescript
// Test each breakpoint:
// ✓ Mobile S (320px): Single column layout
// ✓ Mobile M (375px): Comfortable spacing
// ✓ Mobile L (414px): Optimized for large phones
// ✓ Tablet (768px): Multi-column where appropriate
// ✓ Desktop (1024px+): Full desktop layout

// Example test:
const breakpoints = [320, 375, 414, 768, 1024];
breakpoints.forEach(width => {
  mcp__playwright__browser_resize({ width, height: 800 })
  mcp__playwright__browser_snapshot()
  mcp__playwright__browser_take_screenshot({
    filename: `layout-${width}px.png`
  })
})
```

### Performance Checklist

```typescript
// Monitor during tests:
// ✓ Console errors: Check for JS errors
// ✓ Network requests: Verify mobile-optimized assets
// ✓ Load time: < 3 seconds on mobile
// ✓ Layout shifts: Minimal CLS

mcp__playwright__browser_console_messages({ onlyErrors: true })
mcp__playwright__browser_network_requests()
```

---

## Debugging Mobile Issues

### Console Errors

```typescript
// Check for mobile-specific errors
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
mcp__playwright__browser_wait_for({ time: 2 })

// Get all console messages
mcp__playwright__browser_console_messages({ onlyErrors: true })

// Look for:
// - Touch event errors
// - Viewport warnings
// - Resource loading failures
// - JavaScript errors
```

### Network Issues

```typescript
// Monitor network activity
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
mcp__playwright__browser_wait_for({ time: 2 })

// Get network requests
mcp__playwright__browser_network_requests()

// Check for:
// - Failed requests (404, 500)
// - Large mobile assets
// - Slow loading resources
// - Missing mobile-specific resources
```

### Visual Debugging

```typescript
// Take diagnostic screenshots
// 1. Initial load
mcp__playwright__browser_navigate({ url: "http://localhost:3000" })
mcp__playwright__browser_take_screenshot({
  filename: "01-initial-load.png"
})

// 2. After interaction
mcp__playwright__browser_click({ element: "button", ref: "btn-1" })
mcp__playwright__browser_take_screenshot({
  filename: "02-after-click.png"
})

// 3. Error state
mcp__playwright__browser_take_screenshot({
  filename: "03-error-state.png"
})

// Compare sequence to identify issue
```

---

## Best Practices

### 1. Always Start with Snapshot

```typescript
// ✅ CORRECT - Snapshot first to identify elements
mcp__playwright__browser_snapshot()
// Now you have element refs for interactions

// ❌ WRONG - Guessing element refs
mcp__playwright__browser_click({ element: "button", ref: "unknown" })
```

### 2. Use Appropriate Wait Times

```typescript
// ✅ CORRECT - Wait for specific condition
mcp__playwright__browser_wait_for({ text: "Loading complete" })

// ⚠️ OK - Short time for animations
mcp__playwright__browser_wait_for({ time: 1 })

// ❌ AVOID - Long arbitrary waits
mcp__playwright__browser_wait_for({ time: 10 })
```

### 3. Test Multiple Devices

```typescript
// ✅ CORRECT - Test iOS + Android
const devices = [
  { name: "iPhone14Pro", width: 393, height: 852 },
  { name: "Pixel7", width: 412, height: 915 }
];

// Test each device
devices.forEach(device => {
  mcp__playwright__browser_resize({
    width: device.width,
    height: device.height
  })
  // Run tests...
})

// ❌ WRONG - Only test one device
mcp__playwright__browser_resize({ width: 375, height: 667 })
// Single device not representative
```

### 4. Capture Both Snapshots and Screenshots

```typescript
// ✅ CORRECT - Use both tools
mcp__playwright__browser_snapshot() // For structure/accessibility
mcp__playwright__browser_take_screenshot({
  filename: "visual.png"
}) // For visual verification

// ❌ WRONG - Only screenshots
// Missing accessibility info and element refs
```

### 5. Clean Up After Tests

```typescript
// ✅ CORRECT - Close browser when done
mcp__playwright__browser_close()

// Not critical but good practice
```

---

## Related Skills

- **mobile-ux-improver**: Mobile UX standards to test against
- **frontend-dev-guidelines**: React/TypeScript patterns for components being tested
- **route-tester**: Backend API testing patterns

---

## Resource Files

- **[device-presets.md](resources/device-presets.md)** - Complete device specifications
- **[test-patterns.md](resources/test-patterns.md)** - Comprehensive test patterns
- **[test-scenarios.md](resources/test-scenarios.md)** - Real-world test examples
- **[visual-regression-guide.md](resources/visual-regression-guide.md)** - Visual testing workflows
- **[mcp-tool-reference.md](resources/mcp-tool-reference.md)** - Complete Playwright MCP tool guide

---

**Skill Status**: Active - Mobile testing guidance for Playwright MCP
**Line Count**: ~500 (following 500-line rule) ✅
**Progressive Disclosure**: Reference files for detailed guides ✅
