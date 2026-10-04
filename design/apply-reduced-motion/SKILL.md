---
name: apply-reduced-motion
description: Use when adding animations, transitions, parallax effects, or auto-playing video to a UI — to respect users' motion sensitivity preferences and prevent content that could trigger seizures.
source: W3C WCAG 2.1 SC 2.3.1 Three Flashes (Level A), SC 2.3.3 Animation from Interactions (Level AAA); CSS prefers-reduced-motion media query; Vestibular Disorders Association guidelines
tags: [accessibility, wcag, a11y, reduced-motion, animation, seizures, vestibular, developer]
related: [design-accessibility-standards, apply-accessible-color]
---

# Apply Reduced Motion

Respect `prefers-reduced-motion` to prevent animation-triggered vestibular episodes, and never flash content more than 3 times per second.

## Why This Is Best Practice

**Adopted by:** `prefers-reduced-motion` is supported in all modern browsers (Chrome,
Firefox, Safari, Edge) since 2019 and is natively supported by macOS, iOS, Windows,
and Android OS-level settings. Apple, Google (Material Design), and Microsoft (Fluent
Design) all include reduced motion as a required accessibility consideration in their
design systems. WCAG 2.1 SC 2.3.1 (Level A) prohibits content that flashes more than
3 times per second — this is legally required under all major accessibility laws.
**Impact:** 35% of people with migraine disorders report sensitivity to motion and
flashing. The Vestibular Disorders Association estimates 35 million Americans experience
vestibular dysfunction — animations can trigger vertigo, nausea, and disorientation.
The 2006 Pokemon epilepsy incident (685 children hospitalized after a flashing scene)
is the documented case that established the 3 Hz flash threshold in broadcasting and
later WCAG.
**Why best:** Motion that can't be turned off affects users persistently across every
visit. `prefers-reduced-motion` provides a system-level user preference — one CSS
media query respects it across all animations without requiring an in-app setting.

Sources: W3C WCAG 2.1 SC 2.3.1, 2.3.3 (2018); CSS `prefers-reduced-motion` MDN
documentation; Vestibular Disorders Association; Apple HIG Accessibility (Motion)

## Steps

### Step 1: Respect `prefers-reduced-motion` in CSS

```css
/* Default animations for users without preference */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.spinner {
  animation: spin 1s linear infinite;
}

/* Override: remove or reduce motion when user prefers */
@media (prefers-reduced-motion: reduce) {
  .card {
    transition: none;
  }

  .spinner {
    animation-duration: 3s;   /* slow down rather than stop, if needed */
  }

  /* Catch-all for unidentified animations */
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

The catch-all rule at the bottom is a safety net. Prefer explicit per-component
overrides so reduced-motion doesn't accidentally break loading states.

### Step 2: Read the preference in JavaScript for programmatic animations

```javascript
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function animateElement(el) {
  if (prefersReducedMotion.matches) {
    // Skip animation — show final state immediately
    el.style.opacity = '1';
    el.style.transform = 'translateY(0)';
    return;
  }

  el.animate([
    { opacity: 0, transform: 'translateY(20px)' },
    { opacity: 1, transform: 'translateY(0)' }
  ], { duration: 300, fill: 'forwards' });
}

// React equivalent
const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)');
```

### Step 3: Never flash content more than 3 times per second (WCAG 2.3.1)

The threshold: content that covers ≥25% of screen area and flashes more than 3 Hz
can trigger photosensitive seizures.

```javascript
// Wrong — 10 flashes per second
setInterval(() => toggleHighlight(), 100);

// Right — safe rate (max 3/sec = minimum 333ms interval)
setInterval(() => toggleHighlight(), 400);

// Better — avoid flashing entirely; use smooth transitions
```

Test with the Photosensitive Epilepsy Analysis Tool (PEAT) or Harding Test for video
content before publishing.

### Step 4: Pause, stop, or hide all auto-playing animated content

```html
<!-- Auto-playing animation: always provide pause control -->
<video autoplay muted loop aria-label="Product feature demo">
  <source src="demo.mp4" type="video/mp4">
</video>
<button id="pause-btn" aria-controls="demo-video">Pause animation</button>

<script>
  const video = document.getElementById('demo-video');
  document.getElementById('pause-btn').addEventListener('click', () => {
    video.paused ? video.play() : video.pause();
  });
</script>
```

WCAG 2.2.2 (Level A) requires that any animation or video that auto-plays for more
than 5 seconds has a mechanism to pause, stop, or hide it.

### Step 5: Test by enabling reduced motion in OS settings

- **macOS**: System Settings → Accessibility → Display → Reduce Motion
- **iOS**: Settings → Accessibility → Motion → Reduce Motion
- **Windows**: Settings → Ease of Access → Display → Show animations in Windows (off)
- **Android**: Settings → Accessibility → Remove animations

Verify all animations are removed or reduced after enabling the OS preference.

## When NOT to Use

- **Animations that convey critical state** (loading spinner, progress bar) — don't remove entirely; slow them down instead. A stopped spinner looks like a hang.
- **Non-animated transitions** — CSS `color` transitions without movement do not trigger vestibular symptoms. Short color transitions (< 200ms) are generally acceptable.

## Common Mistakes

**Checking `prefers-reduced-motion` only in CSS but not in JavaScript animations.** GSAP, Three.js, Framer Motion, and canvas animations require a JavaScript check. CSS `prefers-reduced-motion` does not affect JavaScript-driven animations.

**Removing all transitions but keeping scroll-jacking.** Parallax scroll effects and scroll-jacking trigger vestibular symptoms even without CSS animations. Disable `scroll-behavior: smooth` and parallax under `prefers-reduced-motion`.

**Assuming reduced motion means no motion.** Some users prefer less motion, not zero motion. Subtle fade-in (opacity only, no position change) is generally acceptable. Test with actual users who have vestibular sensitivities.