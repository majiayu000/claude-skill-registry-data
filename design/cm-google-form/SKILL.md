---
name: cm-google-form
description: Google App Script form-to-sheet integration with auto-retry, toast notifications, and Zalo/contact fallback. Reusable across any static website.
allowed-tools: Read, Write, Edit, Glob, Grep, Browser
version: 1.0
priority: HIGH
---

# Google Forms → Sheet Integration Skill

> **Connect HTML forms → Google Sheets via Google Apps Script.**
> Auto-retry, toast UI, contact fallback on errors. Zero dependencies, works on any static site.

---

## 🎯 When to Use

| Trigger | Action |
|---------|--------|
| User says "create form", "connect Google Sheet" | Activate this skill |
| User says "form broken", "submit not working" | Debug using Phase 4-5 |
| User says "add new form to page" | Start from Phase 2 |
| User says "form for another website" | Start from Phase 1 |

---

## 📋 5-Phase Workflow

```
Phase 1: DISCOVER → Scan forms, identify fields, determine sheet structure
Phase 2: PLAN → Design sheet columns, map form fields, create deployment plan
Phase 3: BUILD → Generate Apps Script + Frontend JS + Toast CSS
Phase 4: INTEGRATE → Wire forms to JS, add CSS, deploy Apps Script
Phase 5: VERIFY → Test submit, test retry, test error fallback
```

> 🔴 **Rule:** NEVER skip Phase 1. Always read existing forms first.

---

## Phase 1: DISCOVER (Scan & Analyze)

**Goal:** Understand what forms exist and what fields they have.

### Actions:

1. **Search for forms** in the project:
   ```
   grep -r "data-form-type\|onsubmit\|<form" --include="*.html" .
   ```

2. **For each form found, extract:**

| Info | How to Find |
|------|-------------|
| Form type | `data-form-type` attribute |
| Fields | `<input name="...">`, `<select name="...">` |
| Submit handler | `onsubmit` attribute |
| Page URL | File path |

3. **Ask user** (Socratic Gate):
   - How many separate Google Sheets? (1 shared sheet or separate?)
   - What columns does each sheet need?
   - Is there a fallback contact channel? (WhatsApp, Messenger, Hotline?)
   - Fallback contact URL (e.g., `https://wa.me/15551234567`)

### Output: Form Inventory Table

```markdown
| # | Form Type | Pages | Fields | Target Sheet |
|---|-----------|-------|--------|-------------|
| 1 | massage   | 7     | name, phone, branch, problem, time, package | Sheet Massage |
| 2 | course    | 1     | name, phone, goal | Course Sheet |
```

---

## Phase 2: PLAN (Design & Map)

**Goal:** Map form fields → Sheet columns → Apps Script params.

### Sheet Column Design

For each sheet, define columns in order:

| Column | Source | Always Include |
|--------|--------|---------------|
| Timestamp | `new Date()` — auto | ✅ Yes |
| (form fields) | `e.parameter.xxx` | From inventory |
| Page Source | `e.parameter.url` | ✅ Yes |

### Naming Convention

| Element | Convention |
|---------|-----------|
| Sheet tab name | `Data` |
| Form attribute | `data-form-type="<type>"` |
| Hidden URL field | `<input type="hidden" name="url" value="">` |
| JS global function | `window.submitToGoogleSheet` |

### Deliverables Checklist

- [ ] Apps Script code per sheet
- [ ] Frontend JS with retry + toast
- [ ] Toast CSS component
- [ ] HTML form markup template
- [ ] Deploy instructions
- [ ] Verification test plan

---

## Phase 3: BUILD (Generate Code)

### 3A. Google Apps Script Template

> See `templates/apps-script.js` for the full template.

**Key rules:**
- Always use `doPost(e)` — NOT `doGet`
- Always wrap in `try/catch`
- Always return JSON with `{status: "success"}` or `{status: "error", message: "..."}`
- Column order MUST match `sheet.appendRow([...])` order
- Tab name MUST match `SHEET_NAME` constant

### 3B. Frontend JavaScript

> See `templates/form-submit.js` for the full template.

**Key features:**

| Feature | Detail |
|---------|--------|
| Auto-retry | 3 attempts, exponential backoff (1s → 2s → 4s) |
| Toast UI | Success (green), Error (red), Retrying (amber) |
| Phone validation | Vietnamese format: `/^0\d{8,10}$/` |
| Button states | "Submitting..." → "Retrying (X/3)..." → reset |
| CORS handling | Handles opaque responses from Apps Script |
| Fallback | Zalo button in error toast |
| Auto-dismiss | Success: 6s, Error: 15s, Retrying: 10s |

### 3C. Toast CSS

> See `templates/toast.css` for the full template.

**3 variants:** `--success`, `--error`, `--retrying`

### 3D. HTML Form Markup

> See `templates/form-markup.html` for examples.

**Required attributes:**
```html
<form data-form-type="TYPE" onsubmit="window.submitToGoogleSheet(event)">
  <input type="hidden" name="url" value="">
  <!-- form fields with name="..." -->
  <button type="submit">Submit Text</button>
</form>
```

---

## Phase 4: INTEGRATE (Wire Everything)

### Step-by-step:

1. **Add Toast CSS** → Append to main CSS file (e.g., `design-system.css`)
2. **Add Form JS** → Add to shared JS file or create `js/form-handler.js`
3. **Update HTML forms:**
   - Add `data-form-type="..."` attribute
   - Add `onsubmit="window.submitToGoogleSheet(event)"`
   - Add `<input type="hidden" name="url" value="">`
   - Ensure all inputs have `name="..."` matching Apps Script params
4. **Configure URLs:**
   - Replace placeholder URLs in JS with deployed Apps Script URLs
5. **Configure fallback contact:**
   - Replace Zalo URL in JS toast with project's contact URL

### Customization Points

| Setting | Location | Default |
|---------|----------|---------|
| Apps Script URLs | JS `URLS` object | placeholder |
| Fallback contact | Toast Zalo link | `https://zalo.me/...` |
| Max retries | `fetchWithRetry` arg | 3 |
| Phone regex | Validation block | `/^0\d{8,10}$/` |
| Toast auto-dismiss | `showFormToast` timeouts | 6s/15s/10s |
| Success message | `.then()` block | Customizable |
| Error message | `.catch()` block | Customizable |

---

## Phase 5: VERIFY (Test & Report)

### Test Checklist

| # | Test Case | Expected | Status |
|---|-----------|----------|--------|
| 1 | Submit valid form | Toast success (green) + Zalo opens | |
| 2 | Submit invalid phone | Toast error "Invalid phone number" | |
| 3 | Network offline | 3 retries → Toast error with Zalo button | |
| 4 | Check Google Sheet | New row appears with correct data | |
| 5 | Button states | Disabled during submit, resets after | |
| 6 | Toast close button | Toast disappears on click | |
| 7 | Mobile responsive | Toast visible above sticky CTA | |
| 8 | Multiple forms same page | Each form submits independently | |

### How to Test Retry

1. Open DevTools → Network tab
2. Block domain `script.google.com`
3. Submit form → Should see 3 retry attempts
4. Unblock → Submit again → Should succeed

### Report Template

```markdown
## Form Integration Test Report

**Date:** YYYY-MM-DD
**Pages tested:** X/Y

| Page | Form Type | Submit | Retry | Fallback | Sheet |
|------|-----------|--------|-------|----------|-------|
| index.html | massage | ✅ | ✅ | ✅ | ✅ |
| khoa-hoc.html | course | ✅ | ✅ | ✅ | ✅ |

**Issues found:** None / [list issues]
**Resolution:** [fixes applied]
```

---

## ❌ Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|------|
| Use `alert()` for feedback | Use toast notifications |
| No retry on failure | Auto-retry 3x with backoff |
| Silently fail | Show error + contact fallback |
| Hardcode form URLs | Use config object (`URLS`) |
| Skip phone validation | Validate before submit |
| Forget `name` attribute | Every input MUST have `name` |
| Use `doGet` for form submit | Use `doPost` only |
| Multiple submit handlers | One shared `submitToGoogleSheet` |

---

## 📑 Templates

| File | Purpose |
|------|---------|
| `templates/apps-script.js` | Google Apps Script doPost handler |
| `templates/form-submit.js` | Frontend JS with retry + toast |
| `templates/toast.css` | Toast notification CSS component |
| `templates/form-markup.html` | HTML form examples |

---

## 🔗 Related Skills

| Need | Skill |
|------|-------|
| Form UI/UX design | `@[skills/cm-ux-master]` |
| SEO for forms | `@[skills/cm-dockit]` |
| Form security | `@[skills/vulnerability-scanner]` |
| Deployment | `@[skills/deployment-procedures]` |
