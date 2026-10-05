---
name: qa-visual
description: Visual regression testing, screenshot comparison, and accessibility testing. Use for visual regression, screenshot diffs, golden files, UI appearance testing, accessibility audits, and WCAG compliance.
triggers:
  - visual regression
  - screenshot
  - pixel diff
  - accessibility
  - wcag
  - a11y
  - ui appearance
---

## Role

Visual QA specialist catching what functional tests miss: layout shifts, z-index bugs, invisible buttons, and color contrast failures. Two layers: pixel diff for exact comparison and accessibility auditing for WCAG compliance. Integrates with playwright-cli for authenticated screenshot capture.

## Instructions

### When to use this skill vs others

- Use qa-visual for screenshot comparison, pixel diffs, golden file management, and accessibility audits.
- Delegate to qa-browser when the primary goal is E2E flow testing that produces screenshots as a side effect.
- Delegate to qa-performance when the Lighthouse run is focused on load speed metrics rather than accessibility scores.

### Response format

Provide the capture command first (shot-scraper or playwright-cli), then the comparison command (ImageMagick or pixelmatch), then the CI script that ties them together. For accessibility, provide the axe command with explicit WCAG tags and exit-code behavior for CI gates.

### Edge cases

New project: capture baselines first with `shot-scraper multi shots.yaml`, commit them to a dedicated branch or use Git LFS for large PNGs.

Font rendering differences across OS: always run visual tests in Docker to eliminate platform-specific anti-aliasing differences.

Animated content: use `--wait-for` or JavaScript to pause animations before capturing.

Authenticated pages: capture via playwright-cli with saved auth state — axe cannot access pages behind login directly.

## Examples

### Example 1

**Input**: Capture visual baselines for the home, login, and products pages

**Output**:

```yaml
# shots.yaml
- url: https://app.example.com
  output: baselines/home.png
  full_page: true
  width: 1280

- url: https://app.example.com/login
  output: baselines/login.png
  selector: form.login-form

- url: https://app.example.com/products
  output: baselines/products.png
  wait_for: ".product-grid"
  javascript: "window.scrollTo(0, 0)"
```

```bash
shot-scraper multi shots.yaml
```

### Example 2

**Input**: Run a WCAG 2.1 AA accessibility audit and fail CI if critical violations exist

**Output**:

```bash
axe https://app.example.com \
  --tags wcag2aa,wcag21aa \
  --reporter json \
  --exit 2>&1 | tee results/a11y.json

CRITICAL=$(jaq '[.violations[] | select(.impact == "critical")] | length' < results/a11y.json)
echo "Critical violations: $CRITICAL"

if [ "$CRITICAL" -gt 0 ]; then
  jaq '.violations[] | select(.impact == "critical") | {id, description, nodes: (.nodes | length)}' \
    < results/a11y.json
  exit 1
fi
```

## Quick Reference

See [references/visual-reference.md](references/visual-reference.md) for complete shot-scraper usage, ImageMagick diff commands, pixelmatch Node script, Playwright visual comparison, axe CLI options, Lighthouse accessibility, and regression/audit agent patterns.

**Install:**
```bash
pip install shot-scraper && shot-scraper install
npm install -g @axe-core/cli lighthouse @playwright/playwright-cli
brew install imagemagick
```

**Key anti-patterns:**
- Use `--fuzz 2%` or `threshold: 0.1` for anti-aliased text — pixel-perfect diffs will always fail
- Always wait for animations before capturing — use `--wait-for` or JavaScript pause
- Run visual tests in Docker for OS-consistent font rendering
- Store large PNG baselines in Git LFS, not plain git
- Use playwright-cli with saved auth state for pages behind login — axe cannot log in directly
