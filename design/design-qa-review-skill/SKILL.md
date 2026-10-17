---
name: design-qa-review-skill
description: UI design review and QA tool for comparing design mockups against implementation screenshots to check visual restoration accuracy
triggers:
  - "run a design QA review"
  - "compare design mockup with implementation"
  - "check UI restoration accuracy"
  - "perform visual walkthrough of design"
  - "validate design implementation"
  - "review design versus development"
  - "analyze design-dev differences"
  - "conduct UI visual inspection"
---

# design-qa-review-skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

UI设计走查skill。当用户需要对比设计稿和开发实现的截图、检查UI还原度、进行视觉走查时使用。

## What It Does

This skill enables automated UI/UX design quality assurance by:
- Comparing design mockups against development implementation screenshots
- Checking visual restoration accuracy (还原度检查)
- Identifying discrepancies in layout, spacing, colors, typography, and components
- Generating detailed visual walkthrough reports
- Supporting both image file comparisons and URL-based page analysis

## Installation

Clone the repository:

```bash
git clone https://github.com/ColourCloudSky/design-qa-review-skill.git
cd design-qa-review-skill
```

Install dependencies (if applicable):

```bash
npm install
# or
pip install -r requirements.txt
# or
yarn install
```

## Trigger Conditions

The skill automatically activates when:
1. User mentions keywords: 走查, 设计走查, UI走查, 还原度检查, 对比设计稿, 视觉比对
2. User provides two images (design mockup + implementation screenshot)
3. User provides page URL + design mockup URL/file
4. User explicitly requests design QA review

## Key Commands

Based on the project structure, typical usage patterns:

```bash
# Run design review comparison
design-qa-review --mockup design.png --implementation screenshot.png

# Compare with URLs
design-qa-review --mockup-url https://figma.com/file/... --page-url https://staging.example.com

# Generate detailed report
design-qa-review --mockup design.png --implementation dev.png --output report.json --verbose

# Specify review focus areas
design-qa-review --mockup design.png --implementation dev.png --focus layout,spacing,colors
```

## Configuration

Configuration file example (`config.json` or `.design-qa-rc`):

```json
{
  "tolerance": {
    "color": 5,
    "spacing": 2,
    "fontSize": 1
  },
  "checkAreas": [
    "layout",
    "spacing",
    "typography",
    "colors",
    "borders",
    "shadows",
    "images",
    "icons"
  ],
  "ignoreAreas": [
    {
      "x": 0,
      "y": 0,
      "width": 100,
      "height": 50,
      "reason": "dynamic content"
    }
  ],
  "output": {
    "format": "json",
    "includeScreenshots": true,
    "highlightDifferences": true
  },
  "thresholds": {
    "critical": 95,
    "warning": 85,
    "pass": 75
  }
}
```

Environment variables:

```bash
# API keys for screenshot services
export BROWSERLESS_API_KEY=your_api_key_here
export FIGMA_ACCESS_TOKEN=your_figma_token_here

# Screenshot service endpoint
export SCREENSHOT_SERVICE_URL=https://screenshot.example.com

# Report storage
export REPORT_OUTPUT_DIR=./qa-reports
```

## Usage Patterns

### Pattern 1: Basic Image Comparison

```javascript
const DesignQA = require('design-qa-review-skill');

const qa = new DesignQA({
  mockup: './designs/homepage-mockup.png',
  implementation: './screenshots/homepage-dev.png'
});

const report = await qa.compare();

console.log(`Overall Score: ${report.score}%`);
console.log(`Issues Found: ${report.issues.length}`);
```

### Pattern 2: URL-Based Review

```javascript
const DesignQA = require('design-qa-review-skill');

const qa = new DesignQA({
  mockupUrl: 'https://www.figma.com/file/abc123',
  pageUrl: 'https://staging.myapp.com/dashboard',
  viewport: { width: 1920, height: 1080 }
});

const report = await qa.compare({
  captureFullPage: true,
  waitForSelector: '.main-content'
});

// Generate visual diff
await qa.generateDiffImage('./output/diff.png');
```

### Pattern 3: Detailed Area Analysis

```javascript
const DesignQA = require('design-qa-review-skill');

const qa = new DesignQA({
  mockup: './design.png',
  implementation: './dev.png'
});

// Define specific areas to check
const areas = [
  { name: 'header', bounds: { x: 0, y: 0, width: 1920, height: 80 } },
  { name: 'sidebar', bounds: { x: 0, y: 80, width: 240, height: 1000 } },
  { name: 'content', bounds: { x: 240, y: 80, width: 1680, height: 1000 } }
];

for (const area of areas) {
  const areaReport = await qa.compareArea(area.bounds);
  console.log(`${area.name}: ${areaReport.score}% match`);
  
  areaReport.issues.forEach(issue => {
    console.log(`  - ${issue.type}: ${issue.description}`);
  });
}
```

### Pattern 4: Automated Workflow Integration

```python
from design_qa_review import DesignReviewer

reviewer = DesignReviewer(
    mockup_path="./designs/feature-x.png",
    implementation_path="./screenshots/feature-x-dev.png",
    config_file="./qa-config.json"
)

# Run comprehensive review
results = reviewer.run_review()

# Check against thresholds
if results['score'] < 85:
    print("⚠️  Design restoration below threshold!")
    for issue in results['issues']:
        if issue['severity'] == 'critical':
            print(f"CRITICAL: {issue['description']} at {issue['location']}")

# Export report
reviewer.export_report(
    output_path="./reports/feature-x-qa.html",
    format="html",
    include_visuals=True
)
```

### Pattern 5: Batch Processing

```javascript
const DesignQA = require('design-qa-review-skill');
const fs = require('fs').promises;
const path = require('path');

async function batchReview(designDir, screenshotDir) {
  const designs = await fs.readdir(designDir);
  const reports = [];
  
  for (const design of designs) {
    const screenshot = path.join(screenshotDir, design);
    
    if (await fs.access(screenshot).then(() => true).catch(() => false)) {
      const qa = new DesignQA({
        mockup: path.join(designDir, design),
        implementation: screenshot
      });
      
      const report = await qa.compare();
      reports.push({
        file: design,
        score: report.score,
        issues: report.issues.length
      });
    }
  }
  
  // Generate summary
  const avgScore = reports.reduce((sum, r) => sum + r.score, 0) / reports.length;
  console.log(`Average restoration score: ${avgScore.toFixed(2)}%`);
  
  return reports;
}

batchReview('./designs', './screenshots');
```

## Report Structure

Typical QA report output:

```json
{
  "score": 87.5,
  "timestamp": "2026-06-25T10:20:04Z",
  "mockup": "design.png",
  "implementation": "dev.png",
  "dimensions": {
    "mockup": { "width": 1920, "height": 1080 },
    "implementation": { "width": 1920, "height": 1080 }
  },
  "issues": [
    {
      "type": "spacing",
      "severity": "critical",
      "description": "Header padding differs by 8px",
      "expected": "24px",
      "actual": "16px",
      "location": { "x": 100, "y": 20, "width": 1720, "height": 60 },
      "screenshot": "./diff-images/issue-1.png"
    },
    {
      "type": "color",
      "severity": "warning",
      "description": "Button background color mismatch",
      "expected": "#007AFF",
      "actual": "#0077F2",
      "location": { "x": 500, "y": 400, "width": 120, "height": 40 }
    }
  ],
  "summary": {
    "layout": 90,
    "spacing": 85,
    "typography": 88,
    "colors": 92,
    "overall": 87.5
  }
}
```

## Troubleshooting

### Issue: Image dimensions don't match

```javascript
const qa = new DesignQA({
  mockup: './design.png',
  implementation: './dev.png',
  options: {
    resizeToMatch: true,
    resizeMethod: 'mockup' // resize implementation to match mockup
  }
});
```

### Issue: False positives from dynamic content

```javascript
const qa = new DesignQA({
  mockup: './design.png',
  implementation: './dev.png',
  ignoreRegions: [
    { x: 100, y: 200, width: 300, height: 100, reason: 'user avatar' },
    { selector: '.timestamp', reason: 'dynamic timestamp' }
  ]
});
```

### Issue: Screenshots not loading from URLs

Ensure environment variables are set and service is accessible:

```bash
export BROWSERLESS_API_KEY=${BROWSERLESS_API_KEY}
export SCREENSHOT_TIMEOUT=30000

# Test connectivity
curl -X POST https://chrome.browserless.io/screenshot \
  -H "Authorization: Bearer ${BROWSERLESS_API_KEY}" \
  -d '{"url": "https://example.com"}'
```

### Issue: Color comparison too strict

Adjust tolerance in configuration:

```json
{
  "tolerance": {
    "color": 10,
    "colorSpace": "LAB"
  }
}
```

## Integration Examples

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Design QA Review

on: [pull_request]

jobs:
  design-qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Design QA
        env:
          FIGMA_ACCESS_TOKEN: ${{ secrets.FIGMA_ACCESS_TOKEN }}
        run: |
          npm install design-qa-review-skill
          node scripts/design-qa-check.js
      - name: Upload Report
        uses: actions/upload-artifact@v2
        with:
          name: qa-report
          path: ./reports/
```

### Automated Notification

```javascript
const DesignQA = require('design-qa-review-skill');
const { WebClient } = require('@slack/web-api');

const slack = new WebClient(process.env.SLACK_TOKEN);

async function runAndNotify() {
  const qa = new DesignQA({
    mockup: process.env.MOCKUP_PATH,
    implementation: process.env.IMPL_PATH
  });
  
  const report = await qa.compare();
  
  if (report.score < 85) {
    await slack.chat.postMessage({
      channel: '#design-qa',
      text: `⚠️  Design QA Score: ${report.score}%\nIssues: ${report.issues.length}`,
      attachments: [{ 
        text: report.issues.map(i => `• ${i.description}`).join('\n')
      }]
    });
  }
}
```
