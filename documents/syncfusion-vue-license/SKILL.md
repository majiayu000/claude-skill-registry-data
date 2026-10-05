---
name: syncfusion-vue-license
description: Use this skill when the user asks about Syncfusion Vue licensing, license keys, license registration, license validation errors, trial licenses, or license troubleshooting. This skill provides comprehensive guidance on generating, registering, and managing Syncfusion license keys for Vue applications, including edition-based and platform-based licensing models, registration methods, CI/CD integration, and resolving common licensing errors.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Licensing"
---

# Syncfusion Vue Licensing

This skill guides you through Syncfusion Vue licensing requirements, license key generation, registration methods, and troubleshooting validation errors.

## Table of Contents

- [Licensing Overview](#licensing-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start](#quick-start)
- [Common Registration Methods](#common-registration-methods)

## Licensing Overview

Syncfusion license key validation was introduced in the 2022 Volume 1 release (v20.1.0.47) for Essential JS2 platforms. All Vue applications referencing Syncfusion packages from npm, CDN, or build must register a valid license key to avoid validation warnings.

### Key Licensing Details

**License Key vs Unlock Key:**
- **License Key:** String registered in application code to validate Syncfusion package usage
- **Unlock Key:** Used only during Syncfusion installer process
- **⚠️ Important:** License key is NOT the same as installer unlock key

**Core Requirements:**
- License key validation introduced in v20.1.0.47+ (2022 Volume 1)
- License keys are **version and platform/edition specific**
- Validation occurs **offline** (no internet required during runtime)
- Required when using npm packages or trial installers
- Not required when using licensed installers

**License Types:**
- **Trial license:** 30-day evaluation period, full functionality, generates trial key, displays warning after expiration
- **Community license:** Free for qualifying individuals/organizations (<$1M USD revenue), same functionality as paid license, annual renewal required
- **Paid license:** Commercial license for enterprise use, perpetual or subscription-based, technical support included

**Edition-Based vs Platform-Based:**
- **v31.1.17+ (Edition-based):** UI Edition, Document SDK, PDF Viewer SDK, DOCX Editor SDK, Spreadsheet Editor SDK, Enterprise Edition (all editions combined)
- **v30.x.x and earlier (Platform-based):** Vue, JavaScript, Angular, React, Blazor, etc.

**Build Server Scenarios:**
- **Using npm packages:** License key required - register using NPX command
- **Using trial installer:** License key required - trial warnings appear after 30 days
- **Using licensed installer:** License key NOT required - embedded license validation included

**Offline Validation:**
- No internet connection required during application runtime
- License validated locally against package metadata at startup
- Works in air-gapped environments and offline development
- No external API calls or performance impact

## Documentation and Navigation Guide

### Generating License Keys
📄 **Read:** [references/license-generation.md](references/license-generation.md)
- **Edition-based licensing (v31.1.17+):** UI Edition, Document SDK, PDF Viewer SDK, DOCX Editor SDK, Spreadsheet Editor SDK, Enterprise Edition
- **Platform-based licensing (v30.x.x and earlier):** Vue, JavaScript, Angular, etc.
- Generating keys from License & Downloads page
- Claim License Key page usage
- Version and platform specific license key

### Registering License Keys
📄 **Read:** [references/license-registration.md](references/license-registration.md)
- Environment variable method: `SYNCFUSION_LICENSE`
- CI/CD integration: GitHub Actions, Azure Pipelines
- Active license, active trial, expired license scenarios

### Troubleshooting License Errors
📄 **Read:** [references/licensing-errors.md](references/licensing-errors.md)
- License key not registered error
- Invalid key error
- Trial expired error (30 days)
- Platform mismatch error
- Version mismatch error
- NPX command validation errors

## Quick Start

### 1. Generate License Key

Visit [License & Downloads](https://www.syncfusion.com/account/downloads) page:

**For v31.1.17+ (Edition-based):**
- Select version 31.x.x or higher
- Select required editions: UI Edition, Document SDK, PDF Viewer SDK, DOCX Editor SDK, Spreadsheet Editor SDK
- **Recommended:** Select all 5 editions for Enterprise Edition key
- Click "Get License Key"

**For v30.x.x and earlier (Platform-based):**
- Select version 30.x.x or earlier
- Select platforms: Vue, JavaScript, etc.
- Click "Get License Key"

### 2. Register License Key in Application

**Recommended Method:** Use environment variables to register your license key. This prevents accidentally committing license keys to source control.

**Step 1:** Set the environment variable:

```bash
# Windows
setx SYNCFUSION_LICENSE "Your_License_Key_Here"

# Mac/Linux
export SYNCFUSION_LICENSE='Your_License_Key_Here'
```

**Step 2:** Activate the license using NPX command:

```bash
npx syncfusion-license activate
```

**Step 3:** Clear the cache:

```bash
# Windows PowerShell
Remove-Item -Recurse -Force node_modules\.cache

# macOS/Linux
rm -rf node_modules/.cache
```

> **Note:** For alternative license registration methods, kindly refer to the [Syncfusion license key registration documentation](https://ej2.syncfusion.com/vue/documentation/licensing/license-key-registration).
