---
name: html-visual-verify
description: Validation, testing, auto-fix for local HTML. Static checks (tag balance, JSON, JS, WCAG AA contrast) + Playwright interaction tests + bounded contrast fixes.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: @playwright/test (see package.json)
  - Requires: Chromium or Chrome available
---

# HTML Visual Verify

Validation, testing, and auto-fix pipeline for local HTML.

## Trigger

`/skill html-visual-verify` — invoke with file path and options

## Input Schema

```typescript
interface Input {
  filePath: string;             // HTML file path
  fix?: boolean;                // auto-fix contrast (default: false)
  screenshot?: boolean;         // capture screenshot only (default: false)
  test?: boolean;               // run Playwright tests (default: false)
}
```

## Output Schema

```typescript
interface Output {
  status: "success" | "error" | "warning";
  passed: boolean;
  validation: {
    tagBalance: boolean;
    embeddedJson: boolean;
    jsSyntax: boolean;
    wcagContrast: boolean;
    errors: string[];
    warnings: string[];
  };
  testing?: {
    consoleErrors: string[];
    cardCountMatch: boolean;
    screenshotPath?: string;
  };
  fixed?: string[];
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For API reference and integration workflow:** See [docs/USAGE.md](docs/USAGE.md).
