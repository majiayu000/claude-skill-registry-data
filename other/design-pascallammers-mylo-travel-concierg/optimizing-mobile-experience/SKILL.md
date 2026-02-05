---
name: optimizing-mobile-experience
description: Optimizing StickerNest for mobile devices and touch interactions. Use when the user asks about mobile responsiveness, touch gestures, pinch-to-zoom, mobile UI, touch targets, viewport handling, safe areas, mobile accessibility, or making components work on phones and tablets. Covers gestures, responsive hooks, breakpoints, haptics, and touch-friendly patterns.
---

# Optimizing Mobile Experience for StickerNest

This skill provides comprehensive guidance for implementing industry-standard mobile responsiveness, touch interactions, and accessibility in StickerNest.

## When to Use This Skill

Use this skill when you need to:
- Implement or fix touch gestures (pinch, pan, tap, swipe)
- Make components responsive across device sizes
- Add mobile-specific UI patterns (bottom sheets, FABs, mobile toolbars)
- Ensure touch targets meet accessibility standards (44-48px minimum)
- Handle safe areas on notched devices
- Optimize canvas interactions for touch devices
- Add haptic feedback to interactions
- Debug mobile-specific issues

---

## Core Concepts

### Breakpoint System

StickerNest uses a mobile-first breakpoint system defined in `src/styles/responsive.css`:

| Breakpoint | Width Range | Target Devices |
|------------|-------------|----------------|
| `xs` | 0-479px | Small phones |
| `sm` | 480-767px | Large phones, small tablets |
| `md` | 768-1023px | Tablets |
| `lg` | 1024-1279px | Small desktops, landscape tablets |
| `xl` | 1280-1535px | Desktops |
| `2xl` | 1536px+ | Large desktops |

### Touch Target Standards

Per WCAG 2.1 and Apple/Google HIG:
- **Minimum touch target**: 44×44px (iOS) / 48×48dp (Android)
- **Recommended spacing**: 8px between targets
- **Interactive elements**: Always provide visual feedback on touch

### Viewport Units

Use dynamic viewport units for mobile:
- `dvh` (dynamic viewport height) - accounts for mobile browser chrome
- `svh` (small viewport height) - excludes browser chrome
- `lvh` (large viewport height) - includes browser chrome

---

## Responsive Hooks Reference

All responsive hooks are in `src/hooks/useResponsive.ts`:

```typescript
import {
  useViewport,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  useTouchDevice,
  useOrientation,
  useSafeArea,
  useResponsiveValue,
  useKeyboardVisible,
  useScrollLock,
  usePrefersReducedMotion
} from '@/hooks/useResponsive';

// Example usage
function MyComponent() {
  const { isMobile, isTablet, breakpoint } = useViewport();
  const { hasTouch, isHybrid } = useTouchDevice();
  const orientation = useOrientation(); // 'portrait' | 'landscape'
  const safeArea = useSafeArea(); // { top, right, bottom, left }
  const keyboardVisible = useKeyboardVisible();
  const reducedMotion = usePrefersReducedMotion();

  // Responsive values by breakpoint
  const padding = useResponsiveValue({
    xs: 8,
    sm: 12,
    md: 16,
    lg: 24,
    xl: 32
  });

  return (
    <div style={{
      padding,
      paddingBottom: safeArea.bottom
    }}>
      {isMobile ? <MobileLayout /> : <DesktopLayout />}
    </div>
  );
}
```

---

## Canvas Touch Gestures

### Existing Implementation

The canvas gesture system is in `src/hooks/useCanvasGestures.ts` and supports:

| Gesture | Action | Implementation |
|---------|--------|----------------|
| Pinch | Zoom in/out | Two-finger distance tracking |
| Two-finger pan | Move canvas | Touch midpoint tracking |
| Single-finger pan | Move canvas (view mode) | Configurable per mode |
| Double-tap | Toggle zoom (1x ↔ 2x) | 300ms timeout detection |
| Long-press | Select widget | 350ms hold detection |
| Momentum scroll | Continue pan after release | Velocity + friction physics |

### Using Canvas Gestures

```typescript
import { useCanvasGestures } from '@/hooks/useCanvasGestures';
import { useCanvasStore } from '@/state/useCanvasStore';

function CanvasContainer() {
  const { viewport, pan, zoom } = useCanvasStore();

  const gestureHandlers = useCanvasGestures({
    // Current viewport state
    viewport,

    // Callbacks
    onPan: (deltaX, deltaY) => pan(deltaX, deltaY),
    onZoom: (factor, centerX, centerY) => zoom(factor, centerX, centerY),

    // Options
    enableMomentum: true,
    momentumFriction: 0.92,
    enablePinchZoom: true,
    enableDoubleTapZoom: true,
    doubleTapZoomLevel: 2,
    longPressDelay: 350,

    // Mode-specific behavior
    mode: 'edit', // 'view' | 'edit' | 'preview'

    // Gesture lifecycle callbacks
    onGestureStart: () => {
      // Prevent widget interactions during canvas gestures
    },
    onGestureEnd: () => {
      // Re-enable widget interactions
    }
  });

  return (
    <div
      ref={gestureHandlers.ref}
      onPointerDown={gestureHandlers.onPointerDown}
      onPointerMove={gestureHandlers.onPointerMove}
      onPointerUp={gestureHandlers.onPointerUp}
      onWheel={gestureHandlers.onWheel}
      style={{ touchAction: 'none' }}
    >
      <Canvas />
    </div>
  );
}
```

### Zoom Levels

Predefined zoom stops for consistent UX:
```typescript
const ZOOM_LEVELS = [0.1, 0.25, 0.33, 0.5, 0.67, 0.75, 1, 1.25, 1.5, 2, 3, 4, 5];
```

---

## Haptic Feedback

Use haptics for tactile feedback on supported devices. Located in `src/utils/haptics.ts`:

```typescript
import { haptic, useHaptic } from '@/utils/haptics';

// Direct usage
haptic.light();      // Light tap
haptic.medium();     // Medium impact
haptic.heavy();      // Heavy impact
haptic.success();    // Success pattern
haptic.warning();    // Warning pattern
haptic.error();      // Error pattern
haptic.select();     // Selection feedback
haptic.dragStart();  // Drag initiated
haptic.dragEnd();    // Drag completed
haptic.snap();       // Snapped to grid

// React hook usage
function DraggableWidget() {
  const triggerHaptic = useHaptic();

  const handleDragStart = () => {
    triggerHaptic('dragStart');
  };

  const handleSnap = () => {
    triggerHaptic('snap');
  };
}
```

---

## Mobile Component Patterns

### Mobile Navigation

Use `MobileNav` components from `src/components/MobileNav.tsx`:

```typescript
import {
  MobileNav,
  MobileHeader,
  MobileBottomSheet,
  MobileActionButton
} from '@/components/MobileNav';

// Bottom tab navigation
<MobileNav
  tabs={[
    { id: 'canvas', icon: <CanvasIcon />, label: 'Canvas' },
    { id: 'library', icon: <LibraryIcon />, label: 'Library' },
    { id: 'settings', icon: <SettingsIcon />, label: 'Settings' }
  ]}
  activeTab={activeTab}
  onTabChange={setActiveTab}
/>

// Mobile header with back button
<MobileHeader
  title="Edit Widget"
  onBack={() => navigate(-1)}
  actions={[
    { icon: <SaveIcon />, onClick: handleSave }
  ]}
/>

// Bottom sheet modal
<MobileBottomSheet
  isOpen={isOpen}
  onClose={() => setIsOpen(false)}
  snapPoints={['50%', '90%']}
>
  <WidgetLibrary />
</MobileBottomSheet>

// Floating action button
<MobileActionButton
  icon={<AddIcon />}
  onClick={handleAdd}
  position="bottom-right"
/>
```

### Responsive Canvas Layout

Use `ResponsiveCanvasLayout` from `src/components/ResponsiveCanvasLayout.tsx`:

```typescript
import {
  ResponsiveCanvasLayout,
  useCanvasLayout
} from '@/components/ResponsiveCanvasLayout';

function CanvasPage() {
  return (
    <ResponsiveCanvasLayout
      header={<CanvasHeader />}
      sidebar={<WidgetLibrary />}
      toolbar={<CanvasToolbar />}
      canvas={<Canvas />}
      // Mobile-specific
      mobileToolbarPosition="bottom"
      sidebarAsMobileSheet={true}
    />
  );
}

// Access layout context in children
function ChildComponent() {
  const {
    isMobile,
    availableHeight,
    availableWidth,
    safeArea,
    panelRegions
  } = useCanvasLayout();
}
```

---

## Touch-Friendly Widget Interactions

### Implementing Touch-Optimized Handles

When creating interactive widget handles, ensure touch-friendly sizing:

```typescript
// src/canvas/interactions/TouchHandle.tsx
interface TouchHandleProps {
  position: 'nw' | 'n' | 'ne' | 'e' | 'se' | 's' | 'sw' | 'w';
  onDrag: (delta: { x: number; y: number }) => void;
}

function TouchHandle({ position, onDrag }: TouchHandleProps) {
  const { hasTouch } = useTouchDevice();

  // Larger handles on touch devices
  const size = hasTouch ? 44 : 12;
  const visualSize = hasTouch ? 24 : 8;

  return (
    <div
      className="touch-handle"
      style={{
        // Hit area (invisible, larger)
        width: size,
        height: size,
        // Visual indicator (smaller, centered)
        '--visual-size': `${visualSize}px`,
        // Position adjustments
        transform: getHandleTransform(position, size)
      }}
      onPointerDown={handlePointerDown}
    >
      <div className="touch-handle-visual" />
    </div>
  );
}
```

```css
/* Touch handle styles */
.touch-handle {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  touch-action: none;
  /* Prevent text selection during drag */
  user-select: none;
  -webkit-user-select: none;
}

.touch-handle-visual {
  width: var(--visual-size);
  height: var(--visual-size);
  background: var(--color-primary);
  border: 2px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Active state for touch feedback */
.touch-handle:active .touch-handle-visual {
  transform: scale(1.2);
  background: var(--color-primary-dark);
}

/* Hover state for mouse devices only */
@media (hover: hover) {
  .touch-handle:hover .touch-handle-visual {
    transform: scale(1.1);
  }
}
```

### Widget Selection on Touch

```typescript
function useWidgetTouchSelection(widgetId: string) {
  const { selectWidget } = useSelectionStore();
  const triggerHaptic = useHaptic();
  const [isLongPress, setIsLongPress] = useState(false);
  const longPressTimer = useRef<number>();

  const handleTouchStart = (e: React.TouchEvent) => {
    // Start long-press detection
    longPressTimer.current = window.setTimeout(() => {
      setIsLongPress(true);
      selectWidget(widgetId);
      triggerHaptic('select');
    }, 350);
  };

  const handleTouchEnd = () => {
    clearTimeout(longPressTimer.current);

    if (!isLongPress) {
      // Single tap - toggle selection or open
      selectWidget(widgetId);
      triggerHaptic('light');
    }
    setIsLongPress(false);
  };

  const handleTouchMove = () => {
    // Cancel long-press if finger moves
    clearTimeout(longPressTimer.current);
  };

  return { handleTouchStart, handleTouchEnd, handleTouchMove };
}
```

---

## CSS Responsive Patterns

### Using the Responsive CSS System

Import responsive styles in your component CSS modules:

```css
/* MyComponent.module.css */
@import '@/styles/responsive.css';

.container {
  padding: var(--spacing-md);

  /* Mobile-first: default is mobile */
  display: flex;
  flex-direction: column;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    flex-direction: row;
    padding: var(--spacing-lg);
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: var(--spacing-xl);
  }
}

/* Touch-specific styles */
@media (pointer: coarse) {
  .button {
    min-height: 44px;
    min-width: 44px;
    padding: var(--spacing-md);
  }
}

/* High precision pointer (mouse) */
@media (pointer: fine) {
  .button {
    min-height: 32px;
  }
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .animated {
    animation: none;
    transition: none;
  }
}
```

### Safe Area Handling

```css
.bottom-toolbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  /* Account for iPhone notch/home indicator */
  padding-bottom: env(safe-area-inset-bottom, 0);
  padding-left: env(safe-area-inset-left, 0);
  padding-right: env(safe-area-inset-right, 0);
}

.top-header {
  padding-top: env(safe-area-inset-top, 0);
}
```

### Preventing Unwanted Touch Behaviors

```css
/* Prevent pull-to-refresh on the canvas */
.canvas-container {
  overscroll-behavior: none;
}

/* Prevent zoom on double-tap for inputs */
input, textarea, select {
  font-size: 16px; /* Prevents iOS zoom on focus */
}

/* Prevent text selection during interactions */
.interactive-element {
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
}

/* Remove tap highlight on iOS */
.button {
  -webkit-tap-highlight-color: transparent;
}

/* Proper touch action for different elements */
.scrollable {
  touch-action: pan-y;
}

.zoomable {
  touch-action: pinch-zoom pan-x pan-y;
}

.draggable {
  touch-action: none;
}
```

---

## Mobile Accessibility Checklist

### Touch Targets
- [ ] All interactive elements are at least 44×44px
- [ ] Touch targets have 8px minimum spacing
- [ ] Resize/rotate handles are enlarged on touch devices

### Visual Feedback
- [ ] Touch states provide visual feedback (scale, color change)
- [ ] Haptic feedback on key interactions
- [ ] Loading states are visible during async operations

### Gestures
- [ ] All gestures have alternative methods (buttons)
- [ ] Gesture hints shown on first use
- [ ] Long-press doesn't conflict with scroll

### Keyboard & Screen Readers
- [ ] Virtual keyboard doesn't obscure inputs
- [ ] Focus management works with keyboard navigation
- [ ] ARIA labels on icon-only buttons

### Performance
- [ ] Animations respect `prefers-reduced-motion`
- [ ] Heavy operations don't block main thread
- [ ] Images are lazy-loaded and properly sized

---

## Step-by-Step: Adding Mobile Support to a Component

### Step 1: Add Responsive Hooks

```typescript
import { useViewport, useTouchDevice, useSafeArea } from '@/hooks/useResponsive';

function MyComponent() {
  const { isMobile, isTablet } = useViewport();
  const { hasTouch } = useTouchDevice();
  const safeArea = useSafeArea();
```

### Step 2: Conditional Rendering

```typescript
  return (
    <div style={{ paddingBottom: safeArea.bottom }}>
      {isMobile ? (
        <MobileLayout>
          {/* Mobile-optimized UI */}
        </MobileLayout>
      ) : (
        <DesktopLayout>
          {/* Desktop UI */}
        </DesktopLayout>
      )}
    </div>
  );
}
```

### Step 3: Add Touch Interactions

```typescript
  const handleInteraction = (e: React.PointerEvent) => {
    if (e.pointerType === 'touch') {
      // Touch-specific handling
      haptic.light();
    }
    // Common logic
  };
```

### Step 4: Update CSS

```css
.my-component {
  /* Mobile-first base styles */
  padding: 16px;
}

@media (min-width: 768px) {
  .my-component {
    padding: 24px;
  }
}

@media (pointer: coarse) {
  .my-component .button {
    min-height: 44px;
  }
}
```

---

## Reference Files

### Core Mobile Infrastructure
- **Responsive Hooks**: `src/hooks/useResponsive.ts`
- **Responsive CSS**: `src/styles/responsive.css`
- **Canvas Gestures**: `src/hooks/useCanvasGestures.ts`
- **Haptic Feedback**: `src/utils/haptics.ts`

### Mobile Components
- **Mobile Navigation**: `src/components/MobileNav.tsx`
- **Responsive Layout**: `src/components/ResponsiveCanvasLayout.tsx`

### Canvas & Interactions
- **Main Canvas**: `src/canvas/Canvas2.tsx`
- **Unified Interactions**: `src/canvas/interactions/useUnifiedInteraction.ts`
- **Drag Controller**: `src/canvas/interactions/useDragController.ts`
- **Resize Controller**: `src/canvas/interactions/useResizeController.ts`
- **Coordinate Service**: `src/canvas/CoordinateService.ts`

### State Management
- **Canvas Store**: `src/state/useCanvasStore.ts`
- **Selection Store**: `src/state/useSelectionStore.ts`

### CSS Modules with Mobile Styles
- **Canvas Page**: `src/pages/CanvasPage.module.css`
- **Canvas Toolbar**: `src/canvas/CanvasToolbar.module.css`
- **Zoom Controls**: `src/components/ZoomControls.module.css`

---

## Troubleshooting

### Issue: Pinch-to-zoom zooms the entire page instead of canvas
**Cause**: Missing `touch-action: none` on canvas container
**Fix**: Add `touch-action: none` to the canvas wrapper and handle all gestures manually

### Issue: Scroll conflicts with canvas pan
**Cause**: Parent scrollable container capturing touch events
**Fix**: Use `overscroll-behavior: none` on canvas and `touch-action: pan-y` on scrollable areas only

### Issue: Touch targets too small on mobile
**Cause**: Fixed pixel sizes not accounting for touch input
**Fix**: Use `@media (pointer: coarse)` to increase sizes for touch devices

### Issue: Content hidden behind iPhone notch
**Cause**: Missing safe area insets
**Fix**: Apply `env(safe-area-inset-*)` padding to edge-positioned elements

### Issue: Virtual keyboard covers input
**Cause**: Fixed positioning doesn't account for keyboard
**Fix**: Use `useKeyboardVisible()` hook to adjust layout when keyboard is open

### Issue: Gestures trigger during text selection
**Cause**: Missing prevention of default behaviors
**Fix**: Add `user-select: none` and `-webkit-touch-callout: none` to gesture areas

### Issue: Animations cause jank on mobile
**Cause**: Expensive animations or not using GPU acceleration
**Fix**: Use `transform` and `opacity` for animations, add `will-change` hints, respect `prefers-reduced-motion`

---

## Advanced: Implementing Swipe Gestures

For swipe gestures not covered by `useCanvasGestures`:

```typescript
// src/hooks/useSwipeGesture.ts
import { useRef, useCallback } from 'react';

interface SwipeConfig {
  threshold?: number;      // Minimum distance for swipe (default: 50)
  velocity?: number;       // Minimum velocity (default: 0.3)
  direction?: 'horizontal' | 'vertical' | 'both';
  onSwipeLeft?: () => void;
  onSwipeRight?: () => void;
  onSwipeUp?: () => void;
  onSwipeDown?: () => void;
}

export function useSwipeGesture(config: SwipeConfig) {
  const startPos = useRef({ x: 0, y: 0 });
  const startTime = useRef(0);

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    const touch = e.touches[0];
    startPos.current = { x: touch.clientX, y: touch.clientY };
    startTime.current = Date.now();
  }, []);

  const handleTouchEnd = useCallback((e: React.TouchEvent) => {
    const touch = e.changedTouches[0];
    const deltaX = touch.clientX - startPos.current.x;
    const deltaY = touch.clientY - startPos.current.y;
    const elapsed = Date.now() - startTime.current;

    const velocityX = Math.abs(deltaX) / elapsed;
    const velocityY = Math.abs(deltaY) / elapsed;

    const threshold = config.threshold ?? 50;
    const minVelocity = config.velocity ?? 0.3;

    // Detect horizontal swipe
    if (Math.abs(deltaX) > threshold && velocityX > minVelocity) {
      if (deltaX > 0) {
        config.onSwipeRight?.();
      } else {
        config.onSwipeLeft?.();
      }
    }

    // Detect vertical swipe
    if (Math.abs(deltaY) > threshold && velocityY > minVelocity) {
      if (deltaY > 0) {
        config.onSwipeDown?.();
      } else {
        config.onSwipeUp?.();
      }
    }
  }, [config]);

  return { handleTouchStart, handleTouchEnd };
}
```

---

## Testing Mobile on Desktop

### Chrome DevTools
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select device preset or set custom dimensions
4. Enable touch simulation in device toolbar

### Testing Gestures
- Use touch simulation in DevTools
- Test on actual devices for accurate gesture behavior
- Use BrowserStack or similar for device matrix testing

### Common Test Scenarios
1. Pinch zoom on canvas - verify smooth zoom at cursor position
2. Two-finger pan - verify momentum continues after release
3. Double-tap zoom - verify toggles between 1x and 2x
4. Long-press widget - verify selection with haptic feedback
5. Rotate device - verify layout adapts correctly
6. Open keyboard - verify content remains visible
7. Scroll content - verify no conflicts with canvas gestures
