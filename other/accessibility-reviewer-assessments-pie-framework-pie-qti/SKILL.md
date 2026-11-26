---
name: accessibility-reviewer-assessments
description: Reviews educational assessment interfaces for WCAG 2.2 Level AA compliance and assessment-specific accessibility needs. Use when implementing new interactions, reviewing UI changes, or conducting accessibility audits of test-taking interfaces.
allowed-tools: Read, Glob, Grep, Bash
model: Codex-sonnet-4-20250514
---

# Accessibility Reviewer for Assessments

This skill helps review educational assessment interfaces for accessibility compliance, with special focus on test-taking contexts, K-12 learners, and standardized testing requirements.

## When to Use This Skill

Invoke this skill when:
- Implementing new interaction types or question formats
- Reviewing changes to assessment player UI
- Conducting accessibility audits of test-taking interfaces
- Ensuring WCAG 2.2 Level AA compliance
- Reviewing math content (MathML, LaTeX) accessibility
- Evaluating keyboard navigation for test scenarios
- Checking screen reader compatibility
- Reviewing for K-12 accessibility needs (younger learners, diverse abilities)

## Assessment-Specific Accessibility Considerations

Educational assessments have unique accessibility requirements beyond standard web content:

### Test-Taking Context
- **Timed assessments**: Screen reader users need extra time, clear time announcements
- **High-stakes environment**: Errors must not cause anxiety; clear error recovery
- **Focus preservation**: Navigation between items must maintain user context
- **Progress indication**: Clear communication of position in assessment
- **Submit workflows**: Confirmation dialogs must be accessible and clear

### K-12 Learners
- **Younger students**: Simpler language, larger touch targets, forgiving interactions
- **Cognitive load**: Minimize distractions, clear instructions, consistent patterns
- **Reading levels**: Support for text-to-speech, simplified language options
- **Motor skills**: Larger interaction areas, forgiving drag-and-drop, keyboard alternatives

### Interaction Types
- **Drag-and-drop**: Must have keyboard alternatives (arrow keys, Enter/Space to pick/drop)
- **Drawing/hotspot**: Alternative input methods for motor impairments
- **Math input**: Accessible equation editors, LaTeX/MathML screen reader support
- **Multimedia**: Captions, transcripts, audio descriptions where needed

## WCAG 2.2 Level AA Review Checklist

### 1. Perceivable

#### 1.1 Text Alternatives (Level A)
- [ ] **1.1.1**: All images have appropriate alt text or are marked as decorative
- [ ] **Assessment context**: Question images have descriptive alt text that doesn't give away answers
- [ ] **Math content**: MathML includes text alternatives or uses aria-label
- [ ] **Diagrams**: Complex diagrams have detailed descriptions (aria-describedby or longdesc)

**Example Issues to Catch:**
```svelte
<!-- ❌ Missing alt text on question image -->
<img src="diagram.png" />

<!-- ❌ Alt text gives away answer -->
<img src="triangle.png" alt="equilateral triangle" />

<!-- ✅ Descriptive without revealing answer -->
<img src="triangle.png" alt="A triangle with three sides and three angles" />

<!-- ✅ Decorative image properly marked -->
<img src="decorative-border.png" alt="" role="presentation" />
```

#### 1.2 Time-based Media (Level A)
- [ ] **1.2.1**: Audio-only and video-only have alternatives (transcripts)
- [ ] **1.2.2**: Videos have captions
- [ ] **1.2.3**: Audio descriptions or media alternatives provided
- [ ] **Assessment context**: Listening comprehension questions properly marked (accessibility features may be disabled)

#### 1.3 Adaptable (Level A)
- [ ] **1.3.1**: Info/structure/relationships conveyed programmatically
- [ ] **1.3.2**: Reading sequence is logical and meaningful
- [ ] **1.3.3**: Instructions don't rely solely on sensory characteristics (shape, size, position, sound)
- [ ] **1.3.4** (Level AA): Orientation not locked (works in portrait/landscape)
- [ ] **1.3.5** (Level AA): Form inputs have programmatic purpose (autocomplete attributes)

**Example Issues to Catch:**
```svelte
<!-- ❌ Relies on visual position -->
<p>Select the answer in the top-right box</p>

<!-- ✅ Position-independent instructions -->
<p>Select the answer labeled "B"</p>

<!-- ❌ Structure not programmatic -->
<div class="heading">Question 1</div>

<!-- ✅ Semantic structure -->
<h2>Question 1</h2>

<!-- ❌ Instructions rely on color -->
<p>Click the green button to continue</p>

<!-- ✅ Color-independent -->
<p>Click the "Continue" button (highlighted in green) to proceed</p>
```

#### 1.4 Distinguishable (Level A/AA)
- [ ] **1.4.1**: Color not used as only visual means of conveying information
- [ ] **1.4.2**: Audio control (pause, stop, volume) if audio plays automatically
- [ ] **1.4.3** (Level AA): Contrast ratio minimum 4.5:1 (text), 3:1 (large text)
- [ ] **1.4.4** (Level AA): Text can be resized to 200% without loss of content/functionality
- [ ] **1.4.5** (Level AA): Images of text avoided (use real text)
- [ ] **1.4.10** (Level AA): Content reflows to 320px width without horizontal scrolling
- [ ] **1.4.11** (Level AA): Non-text contrast 3:1 (UI components, graphics)
- [ ] **1.4.12** (Level AA): Text spacing can be adjusted without loss of content
- [ ] **1.4.13** (Level AA): Content on hover/focus is dismissible, hoverable, persistent

**Example Issues to Catch:**
```css
/* ❌ Insufficient contrast: 2.8:1 */
.choice-option {
  color: #999; /* gray */
  background: #fff; /* white */
}

/* ✅ Sufficient contrast: 4.6:1 */
.choice-option {
  color: #595959; /* darker gray */
  background: #fff;
}

/* ❌ Touch target too small: 30×30px */
.drag-handle {
  width: 30px;
  height: 30px;
}

/* ✅ K-12 house target: 44×44px (WCAG 2.5.5, AAA); the AA minimum is 24×24px (2.5.8) */
.drag-handle {
  width: 44px;
  height: 44px;
}
```

### 2. Operable

#### 2.1 Keyboard Accessible (Level A)
- [ ] **2.1.1**: All functionality available via keyboard
- [ ] **2.1.2**: No keyboard trap (can navigate away from all components)
- [ ] **2.1.4** (Level A): Character key shortcuts can be turned off or remapped

**Assessment-specific keyboard patterns:**
- [ ] Tab/Shift+Tab: Navigate between questions, choices, and controls
- [ ] Arrow keys: Navigate within choice lists, drag-and-drop zones
- [ ] Space/Enter: Select choices, activate buttons
- [ ] Space: Pick up/drop items in drag-and-drop interactions
- [ ] Escape: Cancel operations, close dialogs
- [ ] Home/End: Jump to first/last item in lists

**Example Issues to Catch:**
```svelte
<!-- ❌ Click handler without keyboard support -->
<div on:click={selectChoice}>Choice A</div>

<!-- ✅ Keyboard accessible -->
<button on:click={selectChoice}>Choice A</button>

<!-- ✅ Custom keyboard support for drag-and-drop -->
<div
  role="button"
  tabindex="0"
  on:keydown={(e) => {
    if (e.key === ' ' || e.key === 'Enter') {
      toggleGrab();
    }
  }}
>
  Draggable item
</div>
```

#### 2.2 Enough Time (Level A)
- [ ] **2.2.1**: Time limits can be turned off, adjusted, or extended (at least 10x), unless the limit is essential. A timed test can fall under the essential exception, but extended time (PNP) must still be honoured and candidates must be warned before time runs out
- [ ] **2.2.2**: Moving/blinking/scrolling content can be paused/stopped/hidden
- [ ] **Assessment context**: Screen reader users may need extended time for timed assessments

**Example Issues to Catch:**
```svelte
<!-- ❌ Hard time limit without extension -->
<Timer duration={60} onExpire={submitAssessment} />

<!-- ✅ Configurable time with extensions -->
<Timer
  duration={timeLimit}
  allowExtensions={true}
  extensionMultiplier={1.5}
  maxExtensions={2}
  onExpire={handleTimeUp}
/>
```

#### 2.3 Seizures and Physical Reactions (Level A)
- [ ] **2.3.1**: No content flashes more than 3 times per second
- [ ] **Assessment context**: Animations in feedback should be subtle

#### 2.4 Navigable (Level A/AA)
- [ ] **2.4.1** (Level A): Bypass blocks (skip links to main content)
- [ ] **2.4.2** (Level A): Pages have descriptive titles
- [ ] **2.4.3** (Level A): Focus order is logical and intuitive
- [ ] **2.4.4** (Level A): Link purpose clear from link text or context
- [ ] **2.4.5** (Level AA): Multiple ways to access content (not always applicable to assessments)
- [ ] **2.4.6** (Level AA): Headings and labels are descriptive
- [ ] **2.4.7** (Level AA): Focus indicator is visible
- [ ] **2.4.11** (Level AA, New in 2.2): Focus Not Obscured (Minimum) — the focused component is not entirely hidden by author-created content (sticky headers, navigation bars, timers)
- [ ] **2.4.13** (Level AAA, New in 2.2): Focus Appearance — indicator area at least a 2px perimeter with 3:1 change of contrast. Not required for AA, but it is this project's house style for focus rings (`outline: 2px solid` with 3:1 contrast, which also satisfies 1.4.11 for the indicator)

**Example Issues to Catch:**
```svelte
<!-- ❌ Missing skip link -->
<nav><!-- Navigation --></nav>
<main><!-- Assessment content --></main>

<!-- ✅ Skip link present -->
<a href="#main-content" class="skip-link">Skip to assessment</a>
<nav><!-- Navigation --></nav>
<main id="main-content"><!-- Assessment content --></main>

<!-- ❌ Focus indicator removed -->
<style>
  button:focus { outline: none; }
</style>

<!-- ✅ Clear focus indicator -->
<style>
  button:focus-visible {
    outline: 2px solid #0066cc;
    outline-offset: 2px;
  }
</style>
```

#### 2.5 Input Modalities (Level A/AA)
- [ ] **2.5.1** (Level A): Pointer gestures have keyboard/single-pointer alternatives
- [ ] **2.5.2** (Level A): Pointer Cancellation — actions fire on the up-event (or can be aborted/undone), not on the down-event
- [ ] **2.5.3** (Level A): Labels match accessible names
- [ ] **2.5.4** (Level A): Motion actuation can be disabled
- [ ] **2.5.5** (Level AAA): Target Size (Enhanced) — at least 44×44 CSS pixels. Not required for AA, but the house target for primary K-12 controls (choices, drag handles, navigation)
- [ ] **2.5.7** (Level AA, New in 2.2): Dragging movements have single-pointer alternative
- [ ] **2.5.8** (Level AA, New in 2.2): Target Size (Minimum) — at least 24×24 CSS pixels, or sufficient spacing (with exceptions)

**Example Issues to Catch:**
```svelte
<!-- ❌ Touch target too small: 20×20px -->
<button style="width: 20px; height: 20px;">×</button>

<!-- ✅ Meets AA (2.5.8, ≥24×24px) and the K-12 house target (44×44px) -->
<button style="width: 44px; height: 44px;" aria-label="Close">×</button>

<!-- ❌ Drag-only interaction -->
<div draggable="true" on:drag={handleDrag}>
  Drag to reorder
</div>

<!-- ✅ Keyboard alternative provided -->
<div
  draggable="true"
  role="button"
  tabindex="0"
  on:drag={handleDrag}
  on:keydown={handleKeyboardReorder}
>
  Drag to reorder or use arrow keys
</div>
```

### 3. Understandable

#### 3.1 Readable (Level A/AA)
- [ ] **3.1.1**: Language of page specified (lang attribute)
- [ ] **3.1.2** (Level AA): Language changes marked (lang attribute on elements)
- [ ] **Assessment context**: Math notation may need language markup

**Example Issues to Catch:**
```html
<!-- ❌ Missing language attribute -->
<html>

<!-- ✅ Language specified -->
<html lang="en">

<!-- ❌ Foreign language not marked -->
<p>The French phrase "bonjour" means hello.</p>

<!-- ✅ Language change marked -->
<p>The French phrase <span lang="fr">bonjour</span> means hello.</p>
```

#### 3.2 Predictable (Level A/AA)
- [ ] **3.2.1**: Focus doesn't trigger unexpected context changes
- [ ] **3.2.2**: Input doesn't trigger unexpected context changes
- [ ] **3.2.3** (Level AA): Navigation is consistent across pages/items
- [ ] **3.2.4** (Level AA): Components are identified consistently
- [ ] **3.2.6** (Level A, New in 2.2): Help is consistent across pages

**Example Issues to Catch:**
```svelte
<!-- ❌ Focus triggers navigation -->
<button on:focus={goToNextQuestion}>Next</button>

<!-- ✅ Explicit action required -->
<button on:click={goToNextQuestion}>Next</button>

<!-- ❌ Inconsistent button labels -->
<!-- On item 1: --><button>Continue</button>
<!-- On item 2: --><button>Next</button>
<!-- On item 3: --><button>Proceed</button>

<!-- ✅ Consistent labeling -->
<button>Next Question</button>
```

#### 3.3 Input Assistance (Level A/AA)
- [ ] **3.3.1**: Error messages identify errors clearly
- [ ] **3.3.2**: Labels or instructions provided for user input
- [ ] **3.3.3** (Level AA): Error suggestions provided when possible
- [ ] **3.3.4** (Level AA): Error prevention for legal/financial/data modifications (confirmation/undo)
- [ ] **3.3.7** (Level A, New in 2.2): Redundant entry not required (unless necessary)
- [ ] **3.3.8** (Level AA, New in 2.2): Accessible authentication (no cognitive function tests)

**Example Issues to Catch:**
```svelte
<!-- ❌ Vague error message -->
<div role="alert">Invalid input</div>

<!-- ✅ Specific, actionable error -->
<div role="alert">
  Please enter a number between 1 and 100. You entered "abc".
</div>

<!-- ❌ Submit without confirmation -->
<button on:click={submitAssessment}>Submit Test</button>

<!-- ✅ Confirmation before irreversible action -->
<button on:click={confirmSubmit}>Submit Test</button>
{#if showConfirmation}
  <dialog>
    <p>Are you sure you want to submit? You cannot change answers after submitting.</p>
    <button on:click={submitAssessment}>Yes, Submit</button>
    <button on:click={cancelSubmit}>No, Go Back</button>
  </dialog>
{/if}
```

### 4. Robust

#### 4.1 Compatible (Level A/AA)
- [ ] **4.1.2**: Name, role, value available for UI components (ARIA)
- [ ] **4.1.3** (Level AA): Status messages programmatically determined (aria-live)

**Example Issues to Catch:**
```svelte
<!-- ❌ Custom component without ARIA -->
<div class="checkbox" on:click={toggle}>
  {#if checked}✓{/if}
</div>

<!-- ✅ Proper ARIA attributes -->
<div
  role="checkbox"
  aria-checked={checked}
  tabindex="0"
  on:click={toggle}
  on:keydown={handleKey}
>
  {#if checked}✓{/if}
</div>

<!-- ❌ Status update not announced -->
<div>Answer saved</div>

<!-- ✅ Status announced to screen readers -->
<div role="status" aria-live="polite">
  Answer saved
</div>
```

## Assessment-Specific Patterns

### Question Navigation
```svelte
<!-- ✅ Accessible navigation bar -->
<nav aria-label="Assessment navigation">
  <button on:click={previousQuestion} disabled={isFirstQuestion}>
    Previous Question
  </button>
  <span aria-live="polite" aria-atomic="true">
    Question {currentIndex + 1} of {totalQuestions}
  </span>
  <button on:click={nextQuestion} disabled={isLastQuestion}>
    Next Question
  </button>
</nav>
```

### Choice Interactions
```svelte
<!-- ✅ Accessible radio/checkbox group -->
<fieldset>
  <legend>Which of the following is a prime number?</legend>
  {#each choices as choice, i}
    <label>
      <input
        type="radio"
        name="question-1"
        value={choice.id}
        checked={selected === choice.id}
      />
      {choice.text}
    </label>
  {/each}
</fieldset>
```

### Drag-and-Drop Interactions
```svelte
<!-- ✅ Keyboard-accessible drag-and-drop -->
<div
  role="button"
  tabindex="0"
  aria-grabbed={isGrabbed}
  aria-label="Draggable item: {label}. Press space to pick up."
  on:keydown={(e) => {
    if (e.key === ' ') {
      e.preventDefault();
      toggleGrab();
    } else if (isGrabbed && e.key.startsWith('Arrow')) {
      e.preventDefault();
      moveWithKeyboard(e.key);
    }
  }}
>
  {label}
</div>

<!-- Screen reader feedback -->
<div role="status" aria-live="assertive" aria-atomic="true">
  {#if isGrabbed}
    {label} picked up. Use arrow keys to move, space to drop.
  {:else if justDropped}
    {label} dropped.
  {/if}
</div>
```

### Math Content
```svelte
<!-- ✅ Accessible math with MathML and fallback -->
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <mrow>
    <mi>x</mi>
    <mo>=</mo>
    <mfrac>
      <mrow><mo>−</mo><mi>b</mi></mrow>
      <mrow><mn>2</mn><mi>a</mi></mrow>
    </mfrac>
  </mrow>
</math>
<span class="sr-only">
  x equals negative b divided by 2a
</span>

<!-- Or with aria-label -->
<div class="math-formula" aria-label="x equals negative b over 2a">
  [rendered LaTeX]
</div>
```

### Timer Warnings
```svelte
<!-- ✅ Accessible time warnings -->
<div role="timer" aria-live="polite" aria-atomic="true">
  {#if minutesRemaining <= 5}
    <span aria-label="Warning: {minutesRemaining} minutes remaining">
      ⚠️ {minutesRemaining}:00
    </span>
  {:else}
    {minutesRemaining}:00
  {/if}
</div>

<!-- Additional aria-live region for critical warnings -->
{#if minutesRemaining === 1}
  <div role="alert" aria-live="assertive">
    Warning: Only 1 minute remaining
  </div>
{/if}
```

## Review Process

When conducting an accessibility review:

1. **Keyboard Navigation Test**
   - Tab through entire interface without mouse
   - Verify all interactions work with keyboard
   - Check focus indicators are visible
   - Test logical tab order

2. **Screen Reader Test**
   - Use VoiceOver (Mac), NVDA (Windows), or JAWS
   - Verify all content is announced
   - Check ARIA labels make sense
   - Test with eyes closed if possible

3. **Color/Contrast Check**
   - Use browser DevTools or WebAIM contrast checker
   - Verify 4.5:1 for text, 3:1 for UI components
   - Test with color blindness simulators

4. **Touch Target Audit**
   - Verify all interactive elements are at least 24×24px (2.5.8, AA) and primary K-12 controls reach 44×44px (house target)
   - Check spacing between adjacent targets

5. **Code Review**
   - Check HTML semantics (heading hierarchy, landmarks, form structure)
   - Review ARIA usage (roles, states, properties)
   - Verify alt text and labels

6. **Automated Testing**
   - Run axe-core or similar tool
   - Review Playwright accessibility test results
   - Check for ARIA violations

## Output Format

Provide feedback in this structure:

### ✅ Accessibility Strengths
- What's working well
- Good patterns to reinforce

### 🚨 Critical Issues (WCAG Violations)
For each violation:
- **WCAG Criterion**: e.g., 1.4.3 Contrast (Level AA)
- **Severity**: Blocker / High / Medium
- **Location**: File and line number or component name
- **Issue**: What's wrong
- **Example**: Code showing the violation
- **Fix**: Specific solution with code

### ⚠️ Assessment-Specific Concerns
- Test-taking context issues
- K-12 learner considerations
- Interaction type accessibility

### 💡 Enhancements
- Optional improvements beyond WCAG AA
- Level AAA considerations
- UX improvements for accessibility

## Tool Usage

- **Read**: Examine Svelte components, CSS files, HTML templates
- **Glob**: Find all component files, style files
- **Grep**: Search for ARIA attributes, alt attributes, role attributes, focus/keyboard handlers
- **Bash**: Run accessibility tests, check test results, run axe-core if available

## Testing Commands

```bash
# Run Playwright accessibility tests
bun --filter @pie-qti/example test:e2e

# Run specific a11y test suite
bun --filter @pie-qti/example test:e2e a11y

# Check for ARIA violations with axe-core (if configured)
npm run test:a11y
```

## Resources

- **WCAG 2.2**: https://www.w3.org/WAI/WCAG22/quickref/
- **WebAIM**: https://webaim.org/
- **axe DevTools**: Browser extension for accessibility testing
- **Accessible Rich Internet Applications (ARIA)**: https://www.w3.org/WAI/ARIA/apg/
- **QTI Accessibility**: IMS Global accessibility guidelines for QTI content
