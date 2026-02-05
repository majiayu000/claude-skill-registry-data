---
name: healthcare-ux-standards
description: General healthcare UX standards for Hospital Information Systems (HIS), EMR/EHR, clinic management, and patient portals. WCAG 2.2 Level AA compliant with US/International regulatory alignment (HHS Section 504, ADA, Section 508, EN 301 549, NHS Digital). Covers accessibility, patient safety language, and healthcare-specific design patterns. Auto-activates for healthcare UI design, form validation, error messaging, clinical workflows, and patient-facing interfaces.
---

# Healthcare UX Standards

Comprehensive user experience standards ensuring accessibility, patient safety, and usability for healthcare management applications including Hospital Information Systems (HIS), Electronic Medical Records (EMR/EHR), clinic management software, patient portals, and telehealth platforms.

## When This Skill Activates

- Designing healthcare application interfaces (HIS, EMR, clinic management)
- Creating patient portal experiences
- Building telehealth platforms
- Implementing healthcare forms and workflows
- Conducting accessibility audits for healthcare apps
- Writing error messages, notifications, or system feedback
- Reviewing mobile health applications
- Implementing healthcare AI/chatbot interfaces

---

## Core Principles

### 1. Accessibility is Patient Safety

**WCAG 2.2 Level AA compliance is MANDATORY** for all healthcare interfaces.

**Why it matters:**
- Healthcare access is a right, not a privilege
- Patients with disabilities must have equal access to health services
- Inaccessible interfaces create barriers to care
- Legal requirements: HHS Section 504, ADA Title III, Section 508
- Compliance deadline: May 11, 2026 (entities with 15+ employees)

### 2. Language Shapes Patient Experience

**Error messages must not alarm or undermine trust.**

**Why it matters:**
- Patients may be anxious about their health
- Healthcare professionals rely on system confidence
- Alarming language increases stress and reduces compliance
- Calm, professional tone maintains therapeutic relationship

### 3. Design for Diverse Users

**Healthcare applications serve users with varying abilities and contexts.**

**Consider:**
- Visual impairments (screen readers, magnification)
- Motor impairments (keyboard navigation, touch targets)
- Cognitive disabilities (clear language, consistent patterns)
- Auditory impairments (captions, visual alerts)
- Low health literacy (plain language, clear instructions)

---

## Quick Reference: Critical Requirements

### MUST DO (P0 Priority)

1. **Color Contrast**: 4.5:1 minimum for normal text, 3:1 for large text
2. **Focus Indicators**: Visible 3px outline on all interactive elements
3. **Touch Targets**: Minimum 24x24px (WCAG 2.2), recommended 44x44px
4. **Keyboard Navigation**: All functionality accessible via keyboard
5. **Alt Text**: All images and icons have descriptive alt attributes
6. **Form Labels**: All inputs have visible, associated labels
7. **Patient Safety Language**: NO "Error", "Failed", "Broken", "Denied"
8. **Semantic HTML**: Proper heading hierarchy, list tags, button elements
9. **Accessible Authentication**: Support password managers, biometrics (WCAG 2.2)
10. **Redundant Entry**: Auto-populate previously entered patient information (WCAG 2.2)

### NEVER DO (Critical Violations)

1. **Remove focus indicators** (`outline: none` without replacement)
2. **Use placeholder as label** (placeholders disappear on focus)
3. **Rely on color alone** for status or information
4. **Use alarming terminology** ("Fatal error", "Critical failure")
5. **Make buttons from divs** without proper ARIA roles
6. **Use images of text** instead of actual text
7. **Block keyboard navigation** (keyboard traps)
8. **Require cognitive tests for authentication** (CAPTCHAs without alternatives)
9. **Force re-entry of patient data** across form steps

---

## US Regulatory Framework

### Important Clarification: HIPAA Does NOT Require Accessibility

**HIPAA** (Health Insurance Portability and Accountability Act) covers **privacy and security** of Protected Health Information (PHI) only. It does NOT address accessibility for people with disabilities.

**Accessibility is governed by separate laws:**

### HHS Section 504 Final Rule (May 2024)

**Most significant healthcare accessibility mandate in 50 years.**

**Standard**: WCAG 2.1 Level A and AA (WCAG 2.2 AA recommended as equivalent or better)

**Compliance Deadlines:**
| Organization Size | Deadline |
|-------------------|----------|
| 15+ employees | **May 11, 2026** |
| <15 employees | **May 10, 2027** |

**Who Must Comply:**
- Healthcare providers participating in Medicare/Medicaid
- Hospitals (Medicare Part A)
- Medical services (Medicare Part B)
- Medicare Advantage Plans
- Prescription Drug Plan sponsors
- Insurers in Healthcare.gov Marketplaces

**Covered Digital Assets:**
- Public-facing websites
- Patient portals
- Telehealth software
- Mobile applications
- Medical kiosks
- Third-party vendor tools

**Exceptions:**
- Archived web content
- Preexisting documents (with caveats)
- Third-party posted content
- Individual password-protected documents
- Preexisting social media posts

### ADA Title III

**Applies to**: Private healthcare providers (places of public accommodation)

**Standard**: WCAG 2.1 Level AA (de facto)

**Coverage:**
- Doctor's offices and clinics
- Hospitals
- Pharmacies
- Medical laboratories
- Healthcare providers with 15+ employees

**Enforcement**: DOJ enforcement + private lawsuits (2,500+ filed in 2024)

### Section 508

**Applies to**: Federal agencies, federal contractors, federally-funded programs

**Standard**: WCAG 2.0 Level AA (expected to update)

**Coverage:**
- Federal healthcare agencies (VA, NIH, CDC)
- Healthcare contractors to federal agencies
- Medicare/Medicaid systems

### 21st Century Cures Act

**Patient Portal Requirements:**
- Patients must access Electronic Health Information (EHI) "without delay" and without charge
- Information blocking is illegal
- Penalties: Up to $1,252,992 per violation (effective July 31, 2024)

**Accessibility Implication**: Patient portals must be accessible to comply with patient access rights.

### Section 1557 of the ACA

**Language Access Requirements:**
- Notices in 15 most common non-English languages in state
- Qualified interpreters required
- Cannot rely solely on machine translation
- 20pt or larger sans serif font for notices

---

## International Standards

### EN 301 549 (European Union)

**Current Version**: v3.2.1 (incorporates WCAG 2.1 AA)
**Upcoming**: v4.1.1 (2026) will include WCAG 2.2 AA

**Applies to:**
- Public sector healthcare (EU Web Accessibility Directive)
- Private healthcare for specific services (European Accessibility Act)

**Coverage Beyond WCAG:**
- Hardware accessibility (kiosks, devices)
- Telecommunications
- Documentation and support services
- Biometric authentication

### NHS Digital Service Standard (United Kingdom)

**Standard**: WCAG 2.2 Level AA mandatory, AAA recommended

**Requirements:**
- Public Sector Bodies Accessibility Regulations 2018
- Accessibility statement must be published
- Works with assistive technologies (JAWS, NVDA, VoiceOver)

**NHS Accessible Information Standard (AIS):**
1. **Identify**: Ask about communication needs
2. **Record**: Document needs in standardized way
3. **Flag**: Highlight needs in patient file
4. **Share**: Share needs with other providers
5. **Meet**: Provide accessible information

### Australian Digital Health Agency

**Standard**: WCAG 2.1 Level AA

**Applies to**: My Health Record, government health services

**Known Limitations**: Clinical PDF documents may not be fully accessible if not properly formatted at upload.

### ISO Standards for Medical Device Software

**ISO 62366 (IEC 62366-1:2015)**: Medical device usability engineering
- Risk-based usability engineering
- Formative and summative evaluations required
- Integration with ISO 14971 risk management

**ISO 9241**: Ergonomics of human-system interaction
- ISO 9241-210: Human-centered design
- ISO 9241-11: Usability definitions
- ISO 9241-171: Accessible software design

**IEC 62304**: Medical device software lifecycle
- Software safety classifications (A, B, C)
- Required for FDA submissions and EU MDR

---

## WCAG 2.2 Level AA Requirements

### Perceivable: Users Must Perceive Content

#### Text Alternatives

```html
<!-- Good: Descriptive alt text -->
<img src="patient-vitals.png" alt="Patient vital signs chart showing blood pressure trend over 7 days">

<!-- Good: Decorative images -->
<img src="decorative-line.png" alt="" role="presentation">

<!-- Good: Icon with accessible name -->
<button aria-label="Save patient record">
  <svg aria-hidden="true"><!-- Save icon --></svg>
</button>

<!-- Bad: Missing alt text -->
<img src="chart.png">
```

#### Color Contrast

**Requirements:**
- Normal text (< 18pt): **4.5:1** contrast ratio
- Large text (>= 18pt or 14pt bold): **3:1** contrast ratio
- UI components: **3:1** contrast ratio

```css
/* Good: High contrast */
--text-primary: #212529; /* 16.1:1 on white */
--clinical-blue: #0066CC; /* 7.0:1 on white */

/* Bad: Fails AA */
--text-muted: #ADB5BD; /* 2.85:1 on white - DON'T USE */
```

**Testing Tools:**
- Chrome DevTools contrast indicator
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

#### Status Indicators

```html
<!-- Bad: Color only -->
<span class="text-red">Critical</span>

<!-- Good: Icon + text + color -->
<span class="status-critical">
  <svg aria-hidden="true"><!-- Alert icon --></svg>
  <span>Critical: Requires immediate attention</span>
</span>
```

### Operable: Users Must Operate Interface

#### Keyboard Navigation

```html
<!-- Good: Native button -->
<button onclick="saveRecord()">Save Patient Record</button>

<!-- Bad: Div without keyboard support -->
<div onclick="saveRecord()">Save Patient Record</div>

<!-- Good: Custom element with ARIA -->
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
/* Good: Visible focus indicator */
*:focus-visible {
  outline: 3px solid var(--clinical-blue);
  outline-offset: 2px;
}

/* Bad: Removing outline without replacement */
button {
  outline: none; /* NEVER DO THIS */
}
```

#### Touch Targets (WCAG 2.2)

**2.5.8 Target Size (Minimum) - Level AA:**

```css
/* Good: 24x24px minimum (WCAG 2.2 AA) */
.button-small {
  min-width: 24px;
  min-height: 24px;
}

/* Better: 44x44px recommended */
.button {
  min-width: 44px;
  min-height: 44px;
  padding: 12px 24px;
}

/* Good: Increased padding for small icons */
.icon-button {
  width: 24px;
  height: 24px;
  padding: 10px; /* Total: 44x44px */
}
```

### Understandable: Users Must Understand Content

#### Form Labels

```html
<!-- Bad: Placeholder as label -->
<input type="text" placeholder="Patient Name">

<!-- Good: Visible label + placeholder as hint -->
<label for="patient-name">Patient Name *</label>
<input
  type="text"
  id="patient-name"
  name="patientName"
  placeholder="e.g., John Smith"
  required
  aria-required="true"
>

<!-- Good: Grouped related fields -->
<fieldset>
  <legend>Patient Contact Information</legend>
  <label for="phone">Phone Number</label>
  <input type="tel" id="phone" autocomplete="tel">

  <label for="email">Email Address</label>
  <input type="email" id="email" autocomplete="email">
</fieldset>
```

#### Error Messages

See [Patient Safety Language](#patient-safety-language) section for complete guidelines.

```html
<!-- Bad: Generic, alarming -->
<div class="error">Error: Invalid input</div>

<!-- Good: Specific, helpful, calm -->
<div class="error" role="alert">
  <strong>Please check the following:</strong>
  <ul>
    <li>Patient Name is required</li>
    <li>Date of Birth must be in MM/DD/YYYY format</li>
  </ul>
</div>
```

### WCAG 2.2 New Success Criteria

#### 3.3.7 Redundant Entry (Level A)

**Requirement**: Information previously entered must auto-populate or be selectable.

**Healthcare Impact**: Critical for patient registration, insurance forms, appointment scheduling.

```html
<!-- Good: Auto-populate from previous step -->
<label for="confirm-address">Confirm Address</label>
<input
  type="text"
  id="confirm-address"
  value="123 Main St, Anytown, USA 12345"
  aria-describedby="address-hint"
>
<span id="address-hint">Address from Step 1. Edit if needed.</span>
```

#### 3.3.8 Accessible Authentication (Level AA)

**Requirement**: Authentication cannot rely solely on cognitive function tests.

**Must Support:**
- Password managers (paste allowed)
- Biometric login (fingerprint, face recognition)
- Object recognition (identify photo from your photos)
- Cannot require memorization only

```html
<!-- Good: Allows paste for password managers -->
<input type="password" id="password" autocomplete="current-password">

<!-- Good: Offer biometric alternative -->
<button aria-label="Sign in with fingerprint">
  <svg aria-hidden="true"><!-- Fingerprint icon --></svg>
  Sign in with Fingerprint
</button>
```

#### 2.4.11 Focus Not Obscured (Minimum) (Level AA)

**Requirement**: Keyboard focus must not be entirely hidden by sticky headers, footers, or modals.

**Healthcare Impact**: EHR systems often have sticky navigation that can obscure focus.

```css
/* Good: Account for sticky header height */
:target {
  scroll-margin-top: 80px; /* Height of sticky header */
}

/* Good: Ensure modal doesn't obscure focus */
.modal {
  position: fixed;
  /* Trap focus within modal */
}
```

#### 3.2.6 Consistent Help (Level A)

**Requirement**: Help mechanisms must appear in consistent locations across pages.

```html
<!-- Good: Consistent help placement (e.g., bottom-right) -->
<footer class="help-footer">
  <a href="/help">Help Center</a>
  <button aria-label="Open chat support">Chat with Support</button>
  <a href="tel:+18005551234">Call: 1-800-555-1234</a>
</footer>
```

---

## Patient Safety Language

### Core Principle: Calm, Professional Communication

**Healthcare software must not alarm patients or undermine trust.**

### Word Substitutions

| Avoid | Use Instead |
|-------|-------------|
| Error, Failed, Broken | Unable to process, Not completed |
| Invalid, Illegal | Please check, Please verify |
| Denied, Rejected | Unable to access, Needs review |
| Crashed, Down | Temporarily unavailable |
| Fatal error, Critical failure | Please contact support, Needs immediate attention |
| Alert!, Warning! | Please note, Important |

### Message Templates

#### Form Validation

```
Bad: Error: Field required
Good: Please enter patient name

Bad: Invalid email address
Good: Please enter a valid email address (e.g., name@example.com)

Bad: Error: Value too high
Good: Quantity cannot exceed 500 (available stock)
```

#### Data Not Found

```
Bad: Fatal error: Patient record not found
Good: This patient record is not currently available.
      Please verify the patient ID or contact support if the issue persists.
```

#### Permission Issues

```
Bad: Access denied - forbidden
Good: You don't have permission to access this section.
      Please contact your administrator for assistance.
```

#### Network/System Issues

```
Bad: Server down - error 500
Good: We're experiencing technical difficulties.
      Your data is safe. Please try again in a few moments.
```

### Critical Patient Safety Alerts

**When there IS an actual safety concern, be direct:**

```
ALLERGY ALERT: Patient is allergic to Penicillin.

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

## Healthcare Application Types

### Hospital Information Systems (HIS)

**Key Considerations:**
- Complex workflows with multiple user roles
- High-frequency data entry
- Critical patient safety information
- Integration with medical devices

**Accessibility Priorities:**
- Keyboard shortcuts for power users
- Clear role-based navigation
- High contrast for clinical environments
- Screen reader compatibility for all patient data

### Electronic Medical Records (EMR/EHR)

**Key Considerations:**
- Dense information displays
- Charting and documentation
- Order entry systems
- Clinical decision support

**Accessibility Priorities:**
- Navigable heading structure
- Skip links for long forms
- Clear data tables with proper headers
- Accessible date pickers
- Support for voice dictation

### Clinic/Practice Management

**Key Considerations:**
- Appointment scheduling
- Billing and insurance
- Patient check-in/out
- Reporting

**Accessibility Priorities:**
- Simple, clear workflows
- Accessible calendar components
- Clear form validation
- Print-friendly accessible formats

### Patient Portals

**Key Considerations:**
- Diverse user population (patients, caregivers)
- Varying technical literacy
- Mobile-first usage
- Self-service features

**Accessibility Priorities:**
- Plain language (reading level optimization)
- Large touch targets for mobile
- Accessible authentication (WCAG 3.3.8)
- Clear navigation and help
- Support for caregivers and proxies

### Telehealth Platforms

**Key Considerations:**
- Real-time video communication
- Screen sharing for education
- Virtual waiting rooms
- Integration with patient records

**Accessibility Priorities:**
- Real-time captioning
- Keyboard controls for video
- Screen reader announcements for status changes
- Accessible chat functionality
- Clear audio controls

### Medical Kiosks

**Key Considerations:**
- Public-facing devices
- Check-in and registration
- Payment processing
- Wayfinding

**Accessibility Priorities:**
- Large touch targets (44x44px minimum)
- High contrast for various lighting
- Audio output option
- Height accessibility
- Clear timeout warnings

---

## Mobile Healthcare Apps

### iOS Accessibility

**VoiceOver Compatibility:**
- Use UIAccessibility API
- Provide accessibilityLabel for all controls
- Support Dynamic Type for text sizing
- Implement VoiceOver rotor actions

**Touch Targets:**
- Minimum 44x44 points
- Adequate spacing between elements

**Testing:**
- Accessibility Inspector in Xcode
- Test with VoiceOver enabled

### Android Accessibility

**TalkBack Compatibility:**
- Use contentDescription for meaningful elements
- Implement proper focus order
- Support system font scaling

**Touch Targets:**
- Minimum 48x48 dp
- Minimum 8dp spacing between targets

**Testing:**
- Accessibility Scanner app
- Test with TalkBack enabled

### Cross-Platform Considerations

```
- Support both portrait and landscape
- Pinch-to-zoom support (don't disable)
- Text resizing up to 200%
- Consistent navigation across platforms
- Alternative to complex gestures (swipe, drag)
```

---

## Healthcare AI/Chatbot Accessibility

### WCAG Compliance for Conversational Interfaces

**Keyboard Navigation:**
- All chat controls keyboard accessible
- Clear focus indicators
- Escape to close chat window

**Screen Reader Support:**
```html
<!-- Good: ARIA live region for new messages -->
<div
  role="log"
  aria-live="polite"
  aria-label="Chat conversation"
>
  <div class="message user">What are my appointments?</div>
  <div class="message bot">You have 2 upcoming appointments...</div>
</div>
```

**Clear Message Attribution:**
```html
<!-- Good: Clear speaker identification -->
<div class="message">
  <span class="sr-only">You said:</span>
  <p>What are my appointments?</p>
</div>
<div class="message">
  <span class="sr-only">Assistant replied:</span>
  <p>You have 2 upcoming appointments...</p>
</div>
```

### Voice Interface Accessibility

**Challenges:**
- 5-10% of Americans have communication disorders
- 50-60% accuracy for users with speech impairments

**Best Practices:**
- Always provide text input alternative
- Clear error recovery
- Confirm actions before executing
- Allow retry or fallback to human support

### Alternative Input Methods

- Text input alongside voice
- Button-based options for common tasks
- Support for switch controls
- Predictive text suggestions

---

## HL7 FHIR Patient Access Guidelines

### International Patient Access (IPA) Specification

**Accessible Data Types:**
- Basic patient details
- Problems and conditions
- Medication orders
- Immunization history
- Allergies
- Vital signs
- Lab results
- Clinical notes

### Accessibility Considerations for FHIR Apps

**SMART on FHIR Authorization:**
- OAuth 2.0 flows must be accessible
- Login screens must meet WCAG 2.2 AA
- Support for password managers

**Patient-Facing Data Display:**
- Clear presentation of clinical data
- Plain language explanations where possible
- Accessible charts and graphs
- Downloadable accessible formats

---

## Testing Checklist

### Automated Testing (Catches ~30% of issues)

- [ ] axe DevTools browser extension
- [ ] Lighthouse accessibility audit
- [ ] WAVE accessibility checker
- [ ] Pa11y CI for automated testing

### Keyboard Navigation (Manual)

- [ ] Tab through all interactive elements
- [ ] Verify focus order matches visual order
- [ ] Check focus indicators are visible
- [ ] Test Escape key closes modals/dropdowns
- [ ] Verify Enter/Space activates buttons
- [ ] No keyboard traps

### Screen Reader Testing (Manual)

- [ ] Navigate by headings (H key in NVDA/JAWS)
- [ ] Navigate by landmarks (D key)
- [ ] Navigate by form fields (F key)
- [ ] Verify all images have alt text
- [ ] Verify all buttons have accessible names
- [ ] Check ARIA states announce correctly

**Test With:**
- NVDA (Windows, free): https://www.nvaccess.org/
- JAWS (Windows, paid)
- VoiceOver (macOS): Cmd+F5
- TalkBack (Android)
- VoiceOver (iOS)

### Visual Testing

- [ ] Zoom to 200% - verify no horizontal scrolling
- [ ] Resize window to 320px - verify content reflows
- [ ] Test in Windows High Contrast Mode
- [ ] Test with increased text spacing
- [ ] Verify color contrast meets requirements

### Patient Safety Language Testing

- [ ] All error messages reviewed
- [ ] No alarming terminology (Error, Failed, Broken, Denied)
- [ ] All messages provide clear next steps
- [ ] Messages appropriate for audience
- [ ] Critical alerts properly identified
- [ ] Tone is calm, professional, helpful

### Mobile Testing

- [ ] Test with VoiceOver (iOS)
- [ ] Test with TalkBack (Android)
- [ ] Verify touch targets >= 44x44 (iOS) / 48x48 (Android)
- [ ] Test with system font scaling at 200%
- [ ] Test both orientations

---

## Common Violations & Fixes

### 1. Missing Focus Indicators

**Problem:**
```css
* { outline: none; }
```

**Fix:**
```css
*:focus-visible {
  outline: 3px solid var(--clinical-blue);
  outline-offset: 2px;
}
```

### 2. Placeholder as Label

**Problem:**
```html
<input type="text" placeholder="Patient Name">
```

**Fix:**
```html
<label for="patient-name">Patient Name</label>
<input type="text" id="patient-name" placeholder="e.g., John Smith">
```

### 3. Insufficient Color Contrast

**Problem:**
```css
.text-muted { color: #CCCCCC; } /* 2.5:1 - FAILS */
```

**Fix:**
```css
.text-muted { color: #6C757D; } /* 4.54:1 - PASSES AA */
```

### 4. Alarming Error Messages

**Problem:**
```
Fatal error: Stock transfer failed
```

**Fix:**
```
Unable to complete stock transfer.
Requested quantity (500) exceeds available stock (300).
Please adjust the quantity and try again.
```

### 5. Inaccessible Authentication

**Problem:**
```html
<input type="password" onpaste="return false"> <!-- Blocks password managers -->
```

**Fix:**
```html
<input type="password" autocomplete="current-password"> <!-- Allows paste -->
```

### 6. Redundant Data Entry

**Problem:**
Requiring patients to re-enter address, insurance info, or other data on every form step.

**Fix:**
Auto-populate from previous entries with option to edit.

---

## Resources

### Standards Documentation

- WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- EN 301 549: https://www.etsi.org/deliver/etsi_en/301500_301599/301549/
- Section 508: https://www.section508.gov/
- NHS Digital Service Manual: https://service-manual.nhs.uk/accessibility

### Reference Documents

- [WCAG_2.2_COMPLIANCE.md](reference/WCAG_2.2_COMPLIANCE.md) - Complete WCAG 2.2 checklist
- [PATIENT_SAFETY_LANGUAGE.md](reference/PATIENT_SAFETY_LANGUAGE.md) - Full messaging guidelines

### Testing Tools

- axe DevTools: https://www.deque.com/axe/devtools/
- WAVE: https://wave.webaim.org/extension/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Lighthouse (Chrome DevTools)

### Screen Readers

- NVDA (Windows, free): https://www.nvaccess.org/
- VoiceOver (macOS): Cmd+F5
- TalkBack (Android)
- JAWS (Windows): https://www.freedomscientific.com/products/software/jaws/

### Regulatory Resources

- HHS Section 504 Fact Sheet: https://www.hhs.gov/civil-rights/for-individuals/disability/
- ADA Web Guidance: https://www.ada.gov/resources/web-guidance/
- 21st Century Cures Act: https://www.healthit.gov/curesrule/

---

## Summary Checklist

Before releasing ANY healthcare interface:

**Accessibility (WCAG 2.2 Level AA):**
- [ ] Keyboard navigation works for all functionality
- [ ] Focus indicators visible on all interactive elements
- [ ] Touch targets >= 24x24px (44x44px recommended)
- [ ] Color contrast >= 4.5:1 for normal text
- [ ] All images have alt text
- [ ] All form inputs have visible labels
- [ ] Semantic HTML (proper headings, lists, buttons)
- [ ] Screen reader compatible
- [ ] Works at 200% zoom
- [ ] Accessible authentication (password managers, biometrics)
- [ ] No redundant data entry required

**Patient Safety:**
- [ ] Error messages use patient safety language
- [ ] No alarming terminology
- [ ] Clear next steps provided
- [ ] Critical alerts properly identified

**Regulatory Compliance:**
- [ ] HHS Section 504 requirements met
- [ ] ADA Title III considerations addressed
- [ ] 21st Century Cures Act patient access supported

**Remember:** Accessibility is not optional in healthcare. It's a patient safety requirement, legal obligation, and ethical imperative.
