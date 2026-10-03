---
name: license-compliance
description: >
  Use when incorporating or distributing code, libraries, assets, or content with
  licensing requirements. This skill provides procedures for identifying, tracking,
  and complying with licenses across all dependencies and third-party materials.
---

# License Compliance

## Overview
This skill defines how to manage license compliance when using third-party code, libraries, content, or assets. License violations can cause legal liability, forced code removal, and reputational damage. Every dependency must be checked for license compatibility.

## When to Use
- When adding any third-party library, package, or dependency
- When incorporating open-source code into your project
- When using images, fonts, media, or creative assets
- Before distributing or publishing any product
- When evaluating software for commercial use
- **Don't use when:** Working exclusively with internally developed, fully owned code and assets

## Core Procedures

### Step 1: Identify All Licenses
For every external dependency:
- What is the license? (MIT, Apache 2.0, GPL, LGPL, AGPL, BSD, proprietary, unknown)
- Where is the license documented? (LICENSE file, package.json, website)
- Is the license version specified? (v2 vs v3 can have very different requirements)

### Step 2: Check Compatibility
| Your License | Can Use | Cannot Use | Notes |
|-------------|---------|-----------|-------|
| MIT | Almost anything | Nothing major | Very permissive |
| Apache 2.0 | MIT, BSD, ISC | GPL-only | Patent protection clause |
| GPL v3 | GPL-compatible | Proprietary, some Apache | Strong copyleft |
| AGPL | AGPL-compatible | Most commercial | Network use = distribution |
| Proprietary | Explicitly licensed | GPL, most open source | Check contract terms |

### Step 3: Understand Obligations
For each license, document required actions:
- **Attribution:** Must include copyright notice, license text
- **Source Disclosure:** Must provide source code if distributing binary
- **Copyleft:** Derivative works must use same license
- **Patent Grant:** License includes patent rights from contributors
- **Network Clause:** Network use triggers sharing obligations (AGPL)
- **State Changes:** Must document any changes made to the code

### Step 4: Track All Licenses
Maintain a dependency registry:
```
DEPENDENCY LICENSE RECORD
=========================
Package/Asset: [name and version]
License: [license name and version]
Source: [where obtained from]
Obligations: [what we must do to comply]
Usage: [how it is used in product]
Compatibility: [compatible with our distribution? yes/no/conditional]
```

### Step 5: Compliance Actions
- [ ] All license texts included in NOTICE or LICENSE file
- [ ] Copyright notices preserved in source code
- [ ] Source code available if required by license
- [ ] No copyleft contamination of proprietary code
- [ ] License-compliant version of dependencies verified

## Quality Checklist
- [ ] All dependencies identified with licenses
- [ ] License compatibility verified for each dependency
- [ ] Required obligations documented and fulfilled
- [ ] Dependency registry maintained and current
- [ ] Distribution packages include required license notices
- [ ] No unknown-license dependencies in product

## Error Handling
- **Error:** License for dependency unknown
  **Response:** Do NOT use until license is determined, find alternative with known license
- **Error:** License incompatible with distribution model
  **Response:** Find alternative compatible library, or change distribution model
- **Error:** Copyleft dependency incorporated into proprietary code
  **Response:** Isolate copyleft code, re-archecute to use as separate process, consult legal

## Cross-Team Integration
**Related Skills:** secrets-handling, data-privacy-check, audit-trail-management, source-verification
**Used By:** ALL agents incorporating external code/assets, especially Integrators, Developers, Legal, Procurement