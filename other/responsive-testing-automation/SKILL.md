---
name: responsive-testing-automation
description: Automated responsive design testing across all device views (mobile, tablet, desktop). Use this skill when the user needs to test pages across multiple device sizes, check for layout issues, verify element alignment, or automate responsive design validation. Automatically discovers all pages, tests across comprehensive device presets, detects layout issues (horizontal overflow, misaligned elements, tiny text, overlapping elements), captures screenshots, and generates visual HTML reports. Eliminates manual device view switching and provides systematic responsive testing for Next.js applications.
---

# Responsive Testing Automation

Automate responsive design testing across all device views to eliminate time-consuming manual checks.

## Purpose

This skill provides comprehensive automated testing for responsive web applications across mobile, tablet, and desktop device sizes. It automatically discovers all pages in a Next.js application, tests them across multiple device configurations, detects common layout issues, captures screenshots, and generates detailed HTML reports with visual comparisons.

## When to Use This Skill

Trigger this skill when the user:

- Mentions testing pages across different device views or screen sizes
- Wants to check responsive design or mobile/tablet/desktop layouts
- Needs to verify element alignment across devices
- Asks about automating device view testing
- Wants to find layout issues or responsive bugs
- Mentions manually checking pages on different screen sizes
- Needs screenshots of pages across multiple devices
- Wants a report of responsive design issues
- Is working on responsive design implementation
- Mentions time spent switching between device views

Common user requests:
- "Test all pages on mobile and desktop"
- "Check if the layout breaks on tablet"
- "I need to verify responsive design across all devices"
- "Find layout issues on different screen sizes"
- "Generate screenshots for all device sizes"
- "Automate device view testing"

## How to Use This Skill

### Initial Setup (First Time Only)

Before running tests for the first time, install Playwright:

```bash
pip install playwright
playwright install
```

This installs the automation library and necessary browser binaries.

### Running Automated Tests

#### Step 1: Ensure Development Server is Running

The testing script needs a running Next.js server to test against:

```bash
npm run dev
```

Wait for the server to start (usually at `http://localhost:3000`).

#### Step 2: Run the Test Script

Execute the main testing script from the project root:

```bash
python .claude/skills/responsive-testing-automation/scripts/test_all_pages.py
```

The script will:
1. **Discover all pages** - Automatically finds all routes in the `app/` directory
2. **Load device presets** - Uses configurations from `scripts/device_presets.json`
3. **Test each page** - Opens every page in every device configuration
4. **Check for issues** - Detects horizontal overflow, misaligned elements, tiny text, overlapping elements
5. **Capture screenshots** - Takes full-page screenshots for visual comparison
6. **Generate results** - Saves detailed JSON results and screenshots to `./responsive-test-results/`

#### Step 3: Generate Visual HTML Report

After tests complete, generate an interactive HTML report:

```bash
python .claude/skills/responsive-testing-automation/scripts/generate_report.py ./responsive-test-results
```

This creates `responsive-test-results/report.html` with:
- Side-by-side device view comparisons
- Screenshots organized by page and device
- Highlighted layout issues with severity levels
- Interactive filtering by device type or issues
- Summary statistics and counts

#### Step 4: Review Results

Open the HTML report in a browser:

```bash
# The script will output the file path
# Open it manually or use:
start responsive-test-results/report.html  # Windows
open responsive-test-results/report.html   # macOS
xdg-open responsive-test-results/report.html  # Linux
```

### Advanced Usage Options

#### Test Specific Device Categories

Test only mobile devices:
```bash
python scripts/test_all_pages.py --categories mobile
```

Test mobile and tablet:
```bash
python scripts/test_all_pages.py --categories mobile tablet
```

#### Test Specific Devices

```bash
python scripts/test_all_pages.py --devices "iPhone 14 Pro Max" "iPad Pro 11"
```

Available device names are in `scripts/device_presets.json`.

#### Custom Configuration

```bash
python scripts/test_all_pages.py \
  --app-dir ./path/to/app \
  --url http://localhost:3001 \
  --output ./custom-results
```

### Understanding Test Results

The automation detects four types of layout issues:

#### 1. Horizontal Overflow (High Severity)
- **Detection**: Page width exceeds viewport width, causing horizontal scroll
- **Common causes**: Fixed-width elements, oversized images, tables
- **Fix**: Use responsive units, `max-width: 100%`, proper container constraints

#### 2. Elements Outside Viewport (High Severity)
- **Detection**: Specific elements extend beyond screen boundaries
- **Report shows**: Element selectors (tag#id.class) for easy identification
- **Fix**: Apply responsive styling, check absolute positioning, use flexbox/grid wrapping

#### 3. Tiny Text (Medium Severity)
- **Detection**: Text smaller than 12px on mobile/tablet devices
- **Report shows**: Font sizes found
- **Fix**: Increase mobile font sizes, use `clamp()`, minimum 16px for body text

#### 4. Overlapping Elements (High Severity)
- **Detection**: Interactive elements (buttons, links, inputs) positioned on top of each other
- **Fix**: Adjust spacing, fix z-index, proper layout structure

### Interpreting the HTML Report

**Summary Section:**
- Total pages tested
- Total device configurations
- Total test count (pages × devices)
- Total issues found

**Filter Bar:**
- **All**: Show all test results
- **Issues Only**: Show only devices where problems were detected
- **Mobile/Tablet/Desktop**: Filter by device category

**Device Cards:**
- **Green border**: No issues detected
- **Red border**: Layout issues found
- **Orange border**: Error during testing
- **Screenshot**: Click to view full-size image
- **Issues list**: Detailed problems with severity indicators

### Workflow Integration

#### During Development

Run tests after making responsive design changes:

```bash
# Make changes to responsive styles
# Test immediately
python scripts/test_all_pages.py --categories mobile

# Review results
python scripts/generate_report.py ./responsive-test-results
```

#### Before Deployment

Full test across all devices:

```bash
# Run comprehensive tests
python scripts/test_all_pages.py

# Generate report
python scripts/generate_report.py ./responsive-test-results

# Review and fix issues before deploying
```

#### Continuous Integration

Add to CI/CD pipeline to catch responsive issues automatically. See `references/testing_workflow.md` for GitHub Actions example.

### Customizing Device Presets

To add or modify device configurations, edit `scripts/device_presets.json`:

```json
{
  "devices": [
    {
      "name": "Custom Device",
      "category": "mobile",
      "width": 400,
      "height": 900,
      "devicePixelRatio": 2,
      "isMobile": true,
      "hasTouch": true
    }
  ]
}
```

**Categories**: `mobile`, `tablet`, `desktop`

### Bundled Resources

#### Scripts

- **`test_all_pages.py`** - Main automation script
  - Discovers pages automatically
  - Tests across all device configurations
  - Detects layout issues
  - Captures screenshots
  - Generates JSON results

- **`generate_report.py`** - HTML report generator
  - Creates interactive visual report
  - Organizes screenshots by page/device
  - Highlights issues with severity
  - Enables filtering and comparison

- **`device_presets.json`** - Device configurations
  - Comprehensive device library
  - Mobile: iPhone SE through iPhone 14 Pro Max, Samsung Galaxy
  - Tablet: iPad Mini through iPad Pro 12.9
  - Desktop: 1366x768 through 4K (3840x2160)
  - Customizable for project needs

#### References

- **`references/testing_workflow.md`** - Detailed documentation
  - Installation instructions
  - Advanced usage examples
  - Common issues and fixes
  - CI/CD integration
  - Troubleshooting guide

Load this reference when:
- User needs more detailed instructions
- Encountering errors or issues
- Setting up CI/CD integration
- Customizing configurations
- Learning responsive design best practices

### Typical User Workflow

When a user mentions device view testing issues:

1. **Understand the need**:
   - Are they testing all pages or specific ones?
   - Which device categories are most important?
   - Do they need screenshots or just issue detection?

2. **Set up if needed**:
   - Check if Playwright is installed
   - Install if necessary: `pip install playwright && playwright install`

3. **Run appropriate tests**:
   - Full test: `python scripts/test_all_pages.py`
   - Targeted test: Use `--categories` or `--devices` flags
   - Custom config: Use `--app-dir`, `--url`, `--output` as needed

4. **Generate report**:
   - Run `generate_report.py` with results directory
   - Open HTML report for visual review

5. **Help fix issues**:
   - Review detected issues in report
   - Explain severity and impact
   - Provide fixes based on issue type
   - Use examples from `references/testing_workflow.md`

6. **Verify fixes**:
   - Re-run tests after applying fixes
   - Compare before/after results
   - Ensure issues are resolved

### Common Responsive Fixes

When issues are detected, provide context-appropriate fixes:

**For horizontal overflow:**
```jsx
// Use responsive containers
<div className="max-w-full px-4">
  {/* Content */}
</div>

// Responsive images
<img src="..." className="max-w-full h-auto" />
```

**For tiny text on mobile:**
```jsx
// Tailwind responsive typography
<p className="text-sm md:text-base lg:text-lg">Text</p>

// Or use clamp for fluid typography
<style>{`p { font-size: clamp(14px, 4vw, 18px); }`}</style>
```

**For layout breaks:**
```jsx
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Items */}
</div>

// Stack on mobile, row on desktop
<div className="flex flex-col sm:flex-row gap-4">
  {/* Elements */}
</div>
```

**For overlapping elements:**
```jsx
// Add proper spacing
<div className="space-y-4 md:space-y-0 md:space-x-4">
  <button>Button 1</button>
  <button>Button 2</button>
</div>
```

### Troubleshooting

**"Playwright not installed"**
```bash
pip install playwright
playwright install
```

**"No pages found"**
- Verify `app/` directory exists
- Check pages have `page.tsx` or `page.js`
- Ensure running from project root

**"Cannot reach URL"**
- Start dev server: `npm run dev`
- Check correct port
- Use `--url` flag if different port

**Tests timeout**
- Check for slow API calls
- Increase timeout in script
- Verify server is responding

For more troubleshooting, refer to `references/testing_workflow.md`.

## Benefits

- **Time Savings**: Test all pages across all devices in minutes instead of hours
- **Comprehensive Coverage**: Automatically tests every discovered page
- **Consistent Testing**: Same checks applied uniformly across all configurations
- **Visual Documentation**: Screenshots provide visual proof of responsive design
- **Issue Detection**: Catches common layout problems automatically
- **Developer Friendly**: Easy to integrate into development workflow
- **CI/CD Ready**: Can be automated in continuous integration pipelines
- **Customizable**: Flexible device configurations and filtering options

## Implementation Notes

- Uses Playwright for browser automation (headless Chrome)
- Supports Next.js App Router directory structure
- Skips dynamic routes (e.g., `[id]`) to avoid errors
- Full-page screenshots capture entire page, not just viewport
- Network idle wait ensures complete page load
- Results include both JSON data and HTML visualization
- Screenshots organized by page and device for easy comparison
