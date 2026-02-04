---
name: healthcare-ux-guidelines
description: Healthcare UX design standards for MYCURE products combining WCAG 2.2 Level AA accessibility compliance with patient safety language guidelines. Auto-activates for healthcare UI design, form validation, error messaging, clinical workflows, patient-facing interfaces, and government health system integration. Includes Philippine healthcare context (LGU, RHU, BHS, FHSIS systems).
---

# Healthcare UX Guidelines

Comprehensive healthcare user experience standards ensuring accessibility, patient safety, and usability for MYCURE clinical and government health products.

## When This Skill Activates

- Designing healthcare interfaces (clinical systems, patient portals, LGU health centers)
- Creating forms for patient data, medical records, or health services
- Writing error messages, notifications, or system feedback
- Conducting accessibility audits (WCAG 2.2)
- Implementing clinical workflows (consultation, pharmacy, laboratory)
- Building government health reporting interfaces (FHISIS, PhilHealth)

---

## Core Principles

### 1. Accessibility is Patient Safety

**WCAG 2.2 Level AA compliance is MANDATORY** for all MYCURE interfaces.

**Why it matters:**
- Healthcare access is a right, not a privilege
- Patients with disabilities must have equal access to health services
- Inaccessible interfaces create barriers to care
- Legal requirements in many jurisdictions

### 2. Language Shapes Patient Experience

**Error messages must not alarm or undermine trust.**

**Why it matters:**
- Patients may be anxious about their health
- Healthcare professionals rely on system confidence
- Alarming language increases stress and reduces compliance
- Calm, professional tone maintains therapeutic relationship

### 3. Philippine Healthcare Context

**Design for variable infrastructure and diverse users.**

**Challenges:**
- Low-quality displays in rural health units (RHUs)
- Limited bandwidth in barangay health stations (BHS)
- Mixed technical literacy among government health workers
- Multiple languages (Filipino, English, regional languages)

---

## Quick Reference: Critical Requirements

### ✅ MUST DO (P0 Priority)

1. **Color Contrast**: 4.5:1 minimum for normal text, 3:1 for large text
2. **Focus Indicators**: Visible 3px outline on all interactive elements
3. **Touch Targets**: Minimum 44×44px for all clickable elements
4. **Keyboard Navigation**: All functionality accessible via keyboard
5. **Alt Text**: All images and icons have descriptive alt attributes
6. **Form Labels**: All inputs have visible, associated labels
7. **Patient Safety Language**: NO "Error", "Failed", "Broken", "Denied"
8. **Semantic HTML**: Proper heading hierarchy, list tags, button elements

### ❌ NEVER DO (Critical Violations)

1. **Remove focus indicators** (`outline: none` without replacement)
2. **Use placeholder as label** (placeholders disappear on focus)
3. **Rely on color alone** for status or information
4. **Use alarming terminology** ("Fatal error", "Critical failure")
5. **Make buttons from divs** without proper ARIA roles
6. **Use images of text** instead of actual text
7. **Block keyboard navigation** (keyboard traps)
8. **Ignore screen reader compatibility**

---

## Accessibility Standards (WCAG 2.2 Level AA)

### Perceivable: Users Must Perceive Content

#### Text Alternatives

```html
<!-- ✅ Good: Descriptive alt text -->
<img src="patient-chart.png" alt="Patient vital signs chart showing blood pressure trend over 7 days">

<!-- ✅ Good: Decorative images -->
<img src="decorative-line.png" alt="" role="presentation">

<!-- ✅ Good: Icon with accessible name -->
<button aria-label="Save patient record">
  <svg aria-hidden="true"><!-- Save icon --></svg>
</button>

<!-- ❌ Bad: Missing alt text -->
<img src="chart.png">

<!-- ❌ Bad: Icon without label -->
<button><svg><!-- Icon --></svg></button>
```

#### Color Contrast

**Test all color combinations:**

```css
/* ✅ Good: High contrast (7.0:1 on white) */
--clinical-blue: #0066CC;
--text-primary: #212529; /* 16.1:1 */

/* ✅ Good: Passes AA (4.54:1 on white) */
--text-secondary: #6C757D;

/* ❌ Bad: Fails AA (2.85:1 on white) */
--text-muted: #ADB5BD; /* Don't use for critical text */
```

**Tools:**
- Chrome DevTools: Inspect element → Contrast ratio indicator
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

#### Status Indicators

```html
<!-- ❌ Bad: Color only -->
<span class="text-red">Critical</span>

<!-- ✅ Good: Icon + text + color -->
<span class="status-critical">
  <svg aria-hidden="true"><!-- Alert icon --></svg>
  <span>Critical: Requires immediate attention</span>
</span>
```

### Operable: Users Must Operate Interface

#### Keyboard Navigation

**All functionality must work via keyboard:**

```html
<!-- ✅ Good: Native button -->
<button onclick="saveRecord()">Save Patient Record</button>

<!-- ❌ Bad: Div without keyboard support -->
<div onclick="saveRecord()">Save Patient Record</div>

<!-- ✅ Good: Div with proper ARIA -->
<div
  role="button"
  tabindex="0"
  aria-label="Save patient record"
  onclick="saveRecord()"
  onkeydown="if(event.key==='Enter'||event.key===' ')saveRecord()"
>
  Save Patient Record
</div>
```

**Test:** Navigate entire interface using only Tab, Shift+Tab, Enter, Space, Arrow keys.

#### Focus Indicators

```css
/* ✅ Good: Visible focus indicator */
*:focus-visible {
  outline: 3px solid var(--clinical-blue);
  outline-offset: 2px;
}

/* ❌ Bad: Removing outline without replacement */
button {
  outline: none; /* NEVER DO THIS */
}
```

#### Touch Targets (Mobile/Tablet)

```css
/* ✅ Good: 44×44px minimum */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 24px;
}

/* ✅ Good: Increased padding for small icons */
.icon-button {
  width: 24px;
  height: 24px;
  padding: 10px; /* Total: 44×44px */
}

/* ❌ Bad: Too small for touch */
.tiny-button {
  width: 20px;
  height: 20px;
  padding: 2px; /* Total: 24×24px - TOO SMALL */
}
```

### Understandable: Users Must Understand Content

#### Form Labels

```html
<!-- ❌ Bad: Placeholder as label -->
<input type="text" placeholder="Patient Name">

<!-- ✅ Good: Visible label + placeholder as hint -->
<label for="patient-name">Patient Name *</label>
<input
  type="text"
  id="patient-name"
  name="patientName"
  placeholder="e.g., Juan Dela Cruz"
  required
  aria-required="true"
>

<!-- ✅ Good: Grouped related fields -->
<fieldset>
  <legend>Patient Contact Information</legend>
  <label for="phone">Phone Number</label>
  <input type="tel" id="phone" autocomplete="tel">

  <label for="email">Email Address</label>
  <input type="email" id="email" autocomplete="email">
</fieldset>
```

#### Error Messages

**See Patient Safety Language section below for complete guidelines.**

```html
<!-- ❌ Bad: Generic, alarming -->
<div class="error">Error: Invalid input</div>

<!-- ✅ Good: Specific, helpful, calm -->
<div class="error" role="alert">
  <strong>Please check the following:</strong>
  <ul>
    <li>Patient Name is required</li>
    <li>Date of Birth must be in MM/DD/YYYY format</li>
  </ul>
</div>
```

#### Consistent Navigation

```html
<!-- ✅ Good: Consistent button labels -->
<!-- Across all forms: -->
<button>Save Changes</button>
<button>Cancel</button>

<!-- ❌ Bad: Inconsistent labels -->
<!-- Form 1: -->
<button>Submit</button>
<!-- Form 2: -->
<button>Save</button>
<!-- Form 3: -->
<button>OK</button>
```

### Robust: Works with Assistive Technologies

#### Semantic HTML

```html
<!-- ❌ Bad: Divs for everything -->
<div class="heading">Patient Information</div>
<div class="list">
  <div>Name: Juan Dela Cruz</div>
  <div>Age: 45</div>
</div>

<!-- ✅ Good: Semantic HTML -->
<h2>Patient Information</h2>
<dl>
  <dt>Name</dt>
  <dd>Juan Dela Cruz</dd>
  <dt>Age</dt>
  <dd>45 years old</dd>
</dl>
```

#### ARIA Roles and States

```html
<!-- ✅ Good: Custom checkbox with ARIA -->
<div
  role="checkbox"
  aria-checked="true"
  aria-label="Enable appointment reminders"
  tabindex="0"
  onclick="toggleCheckbox()"
  onkeydown="if(event.key===' ')toggleCheckbox()"
>
  ✓ Enable appointment reminders
</div>

<!-- ✅ Good: Dropdown menu with ARIA -->
<button
  aria-expanded="false"
  aria-controls="patient-menu"
  onclick="toggleMenu()"
>
  Actions ▼
</button>
<ul id="patient-menu" hidden>
  <li><a href="/edit">Edit Record</a></li>
  <li><a href="/delete">Delete Record</a></li>
</ul>
```

---

## Patient Safety Language

### Core Principle: Calm, Professional Communication

**Healthcare software must not alarm patients or undermine trust.**

### Word Substitutions

| ❌ Avoid | ✅ Use Instead |
|---------|---------------|
| Error, Failed, Broken | Unable to process, Not completed |
| Invalid, Illegal | Please check, Please verify |
| Denied, Rejected | Unable to access, Needs review |
| Crashed, Down | Temporarily unavailable |
| Fatal error, Critical failure | Please contact support, Needs immediate attention |
| Alert!, Warning! | Please note, Important |

### Message Templates

#### Form Validation

```
❌ Error: Field required
✅ Please enter patient name

❌ Invalid email address
✅ Please enter a valid email address (e.g., name@example.com)

❌ Error: Value too high
✅ Quantity cannot exceed 500 (available stock)
```

#### Data Not Found

```
❌ Fatal error: Patient record not found
✅ This patient record is not currently available.
   Please verify the patient ID or contact support if the issue persists.
```

#### Permission Issues

```
❌ Access denied - forbidden
✅ You don't have permission to access this section.
   Please contact your administrator for assistance.
```

#### Network/System Issues

```
❌ Server down - error 500
✅ We're experiencing technical difficulties.
   Your data is safe. Please try again in a few moments.
```

### Critical Patient Safety Alerts

**When there IS an actual safety concern, be direct:**

```
✅ ALLERGY ALERT: Patient is allergic to Penicillin.

This medication (Amoxicillin) contains Penicillin.

Action required: Do not dispense. Select alternative medication.

[View Alternatives] [Cancel Order]
```

**Use "WARNING" or "ALERT" only for:**
- Actual patient safety risks (allergies, drug interactions)
- Regulatory compliance issues (expired medications)
- Critical system failures affecting patient care
- Data integrity issues impacting treatment decisions

---

## Philippine Healthcare Context

### LGU/Government Health Systems

**Design for:**
- Rural Health Units (RHUs) with limited infrastructure
- Barangay Health Stations (BHS) with basic facilities
- City/Municipal Health Offices (CHO/MHO)
- Provincial Health Offices (PHO)

**Technical Constraints:**
- Low-quality displays (often older monitors)
- Limited bandwidth (2G/3G in rural areas)
- Inconsistent power supply
- Shared/public computers

**Design Adaptations:**

```css
/* High contrast for low-quality displays */
:root {
  --text-primary: #1A1A1A; /* Darker than standard */
  --border-strong: #000000; /* Pure black for definition */
}

/* Larger minimum font sizes */
body {
  font-size: 16px; /* Never below 16px */
}

.data-label {
  font-size: 14px; /* Never below 14px */
}

/* Performance: CSS-only animations */
.loading {
  animation: pulse 1.5s ease-in-out infinite;
}
/* NO video backgrounds, NO heavy JavaScript animations */
```

### FHISIS Reporting

**Field Health Service Information System (FHISIS) integration:**

```html
<!-- ✅ Good: Clear FHISIS field labels -->
<label for="fhisis-report-type">FHISIS Report Type</label>
<select id="fhisis-report-type" name="fhisisReportType">
  <option value="m1">M1 - Target Client List</option>
  <option value="m2">M2 - Summary of Services</option>
  <option value="individual">Individual Treatment Record</option>
</select>

<label for="reporting-period">Reporting Period</label>
<input
  type="month"
  id="reporting-period"
  name="reportingPeriod"
  aria-describedby="period-help"
>
<small id="period-help">Select month and year for FHISIS submission</small>
```

### Multilingual Support

**English + Filipino (Tagalog) minimum:**

```html
<html lang="en">
<!-- Primary language: English -->

<!-- Filipino text sections -->
<section lang="tl">
  <h2>Pangalan ng Pasyente</h2>
  <p>Ilagay ang buong pangalan ng pasyente.</p>
</section>

<!-- Switch language based on user preference -->
<label for="language">Language / Wika</label>
<select id="language" name="language">
  <option value="en">English</option>
  <option value="tl">Filipino</option>
</select>
```

---

## Testing Checklist

### Accessibility Testing

**Automated (30% of issues):**
- [ ] axe DevTools browser extension
- [ ] Lighthouse accessibility audit
- [ ] WAVE accessibility checker

**Keyboard Navigation (Manual):**
- [ ] Tab through all interactive elements
- [ ] Verify focus order matches visual order
- [ ] Check focus indicators are visible
- [ ] Test Escape key closes modals/dropouts
- [ ] Verify Enter/Space activates buttons

**Screen Reader (Manual):**
- [ ] Navigate by headings (H key in NVDA/JAWS)
- [ ] Navigate by landmarks (D key)
- [ ] Navigate by form fields (F key)
- [ ] Verify all images have alt text
- [ ] Verify all buttons have accessible names
- [ ] Check ARIA states announce correctly

**Visual Testing:**
- [ ] Zoom to 200% - verify no horizontal scrolling
- [ ] Resize window to 320px - verify content reflows
- [ ] Test in Windows High Contrast Mode
- [ ] Test with increased text spacing

### Patient Safety Language Testing

**Before Release:**
- [ ] All error messages reviewed by healthcare professional
- [ ] No alarming terminology (Error, Failed, Broken, Denied)
- [ ] All messages provide clear next steps
- [ ] Messages appropriate for audience (patient vs. staff)
- [ ] Critical alerts properly identified
- [ ] Spelling and grammar checked
- [ ] Tone is calm, professional, helpful

---

## Common Violations & Fixes

### 1. Missing Focus Indicators

**Problem:**
```css
/* ❌ Removes all focus indicators */
* {
  outline: none;
}
```

**Fix:**
```css
/* ✅ Replace with visible focus indicator */
*:focus-visible {
  outline: 3px solid var(--clinical-blue);
  outline-offset: 2px;
}
```

### 2. Placeholder as Label

**Problem:**
```html
<!-- ❌ Placeholder disappears when typing -->
<input type="text" placeholder="Patient Name">
```

**Fix:**
```html
<!-- ✅ Visible label + placeholder as hint -->
<label for="patient-name">Patient Name</label>
<input
  type="text"
  id="patient-name"
  placeholder="e.g., Juan Dela Cruz"
>
```

### 3. Insufficient Color Contrast

**Problem:**
```css
/* ❌ Light gray on white (2.5:1 - FAILS) */
.text-muted {
  color: #CCCCCC;
}
```

**Fix:**
```css
/* ✅ Darker gray (4.54:1 - PASSES AA) */
.text-muted {
  color: #6C757D;
}
```

### 4. Alarming Error Messages

**Problem:**
```
❌ Fatal error: Stock transfer failed
```

**Fix:**
```
✅ Unable to complete stock transfer.
   Requested quantity (500) exceeds available stock (300).
   Please adjust the quantity and try again.
```

---

## Resources

**Reference Documents:**
- [WCAG_COMPLIANCE.md](reference/WCAG_COMPLIANCE.md) - Complete WCAG 2.2 checklist
- [PATIENT_SAFETY_LANGUAGE.md](reference/PATIENT_SAFETY_LANGUAGE.md) - Full messaging guidelines

**Testing Tools:**
- axe DevTools: https://www.deque.com/axe/devtools/
- WAVE: https://wave.webaim.org/extension/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Lighthouse (built into Chrome DevTools)

**Screen Readers:**
- NVDA (Windows, free): https://www.nvaccess.org/
- VoiceOver (macOS, built-in): Cmd+F5
- TalkBack (Android, built-in)

**WCAG Guidelines:**
- WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/

---

## Summary Checklist

Before releasing ANY healthcare interface:

- [ ] **WCAG 2.2 Level AA compliant** (minimum)
- [ ] **Keyboard navigation works** for all functionality
- [ ] **Focus indicators visible** on all interactive elements
- [ ] **Touch targets ≥ 44×44px** for all clickable elements
- [ ] **Color contrast ≥ 4.5:1** for normal text, ≥ 3:1 for large text
- [ ] **All images have alt text** (or alt="" for decorative)
- [ ] **All form inputs have visible labels** (not just placeholders)
- [ ] **Error messages use patient safety language** (no "Error", "Failed", etc.)
- [ ] **Semantic HTML** (proper headings, lists, buttons)
- [ ] **Screen reader compatible** (tested with NVDA/VoiceOver)
- [ ] **Works at 200% zoom** without horizontal scrolling
- [ ] **High contrast mode supported**
- [ ] **Filipino/multilingual support** (where applicable)
- [ ] **Optimized for LGU/low-bandwidth** contexts (where applicable)

**Remember:** Accessibility is not optional in healthcare. It's a patient safety requirement and legal obligation.
