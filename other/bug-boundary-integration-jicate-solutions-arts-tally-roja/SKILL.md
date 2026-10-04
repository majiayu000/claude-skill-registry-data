---
name: bug-boundary-integration
description: Production-ready Bug Boundary (JKKN Bug Reporter SDK) integration for Next.js 15+ projects with Supabase. This skill should be used when integrating the @boobalan_jkkn/bug-reporter-sdk package, setting up bug reporting features, troubleshooting integration issues, or implementing error tracking in Next.js applications. Automatically triggers when user mentions 'bug reporter', 'bug boundary', 'bug tracking', '@boobalan_jkkn/bug-reporter-sdk', or requests help with bug reporting integration.
---

# Bug Boundary Integration Skill

This skill provides comprehensive guidance for integrating the JKKN Bug Reporter SDK (`@boobalan_jkkn/bug-reporter-sdk`) into Next.js 15+ applications with production-ready patterns, automated diagnostics, and troubleshooting workflows.

## Purpose

The Bug Reporter SDK enables users to report bugs directly from the application with automatic screenshot capture, console log collection, and user context tracking. This skill ensures error-free integration by providing:

1. **Step-by-step integration workflows** for Next.js App Router
2. **Automated diagnostic tools** to identify configuration issues
3. **Production-ready patterns** for Supabase authentication
4. **Troubleshooting guides** for common integration errors
5. **Quick setup scripts** to accelerate initial configuration

## When to Use This Skill

Use this skill when:

- Installing and configuring the Bug Reporter SDK for the first time
- Integrating bug reporting into an existing Next.js 15+ application
- Setting up bug reporting with Supabase authentication
- Troubleshooting SDK integration issues (widget not appearing, API errors, etc.)
- Implementing programmatic bug reporting from error boundaries
- Adding user-facing "My Bugs" panels
- Debugging screenshot capture or console log issues
- Upgrading from older SDK versions

## Integration Workflows

### Workflow 1: Fresh Integration (No Existing Bug Reporter)

Follow this workflow when adding Bug Reporter SDK to a project for the first time.

#### Step 1: Verify Prerequisites

Before starting integration, verify the project meets these requirements:

- **Next.js**: Version 15 or higher with App Router (check `package.json`)
- **React**: Version 19 or higher
- **Node.js**: Version 18 or higher (run `node --version`)
- **TypeScript**: Version 5+ (recommended, check `tsconfig.json`)

To verify Next.js App Router, check for an `app` directory in the project root.

#### Step 2: Install Required Packages

Install the Bug Reporter SDK and react-hot-toast (for notifications):

```bash
npm install @boobalan_jkkn/bug-reporter-sdk react-hot-toast
```

**Alternative: Use Quick Setup Script**

Run the automated setup script:

```bash
bash .claude/skills/bug-boundary-integration/scripts/setup-bug-reporter.sh
```

This script automatically installs packages, creates environment variables, and provides setup guidance.

**Troubleshooting Package Installation:**

If encountering "404 Not Found" errors:

1. Clear npm cache: `npm cache clean --force`
2. Retry installation: `npm install @boobalan_jkkn/bug-reporter-sdk`
3. If still failing, use explicit registry: `npm install @boobalan_jkkn/bug-reporter-sdk --registry=https://registry.npmjs.org/`
4. Wait 5-10 minutes if package was recently published

#### Step 3: Configure Environment Variables

Create or update `.env.local` in the project root:

```env
# JKKN Bug Reporter Configuration
NEXT_PUBLIC_BUG_REPORTER_API_KEY=app_your_api_key_here
NEXT_PUBLIC_BUG_REPORTER_API_URL=https://your-platform.vercel.app
```

**Important Security Notes:**

- Never commit `.env.local` to version control
- Ensure `.env.local` is listed in `.gitignore`
- API keys must start with `app_` prefix

**How to Obtain API Credentials:**

1. Visit the JKKN Bug Reporter platform login page
2. Create or join an organization (typically department name)
3. Navigate to Applications → New Application
4. Register the application with:
   - **Name**: Application name (e.g., "Mentor Module")
   - **Slug**: Unique identifier (e.g., "mentor-module")
   - **Description**: Brief description
5. Copy the generated API key (format: `app_xxxxxxxxxx`)
6. Note the platform URL (e.g., `https://bug-reporter.vercel.app`)

#### Step 4: Integrate into Next.js Layout

Choose the appropriate integration pattern based on authentication requirements.

**Pattern A: Basic Integration (No Authentication)**

Update `app/layout.tsx`:

```typescript
import { BugReporterProvider } from '@boobalan_jkkn/bug-reporter-sdk';
import { Toaster } from 'react-hot-toast';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <BugReporterProvider
          apiKey={process.env.NEXT_PUBLIC_BUG_REPORTER_API_KEY!}
          apiUrl={process.env.NEXT_PUBLIC_BUG_REPORTER_API_URL!}
          enabled={true}
          debug={process.env.NODE_ENV === 'development'}
        >
          {children}
        </BugReporterProvider>
        <Toaster position="top-right" />
      </body>
    </html>
  );
}
```

**Pattern B: Supabase Authentication Integration** (Recommended for this project)

1. Create `components/bug-reporter-wrapper.tsx`:

```typescript
'use client';

import { BugReporterProvider } from '@boobalan_jkkn/bug-reporter-sdk';
import { useEffect, useState } from 'react';
import { createClient } from '@/lib/supabase/client';

export function BugReporterWrapper({
  children
}: {
  children: React.ReactNode
}) {
  const [user, setUser] = useState<any>(null);
  const supabase = createClient();

  useEffect(() => {
    // Get initial user
    supabase.auth.getUser().then(({ data }) => {
      setUser(data.user);
    });

    // Subscribe to auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null);
      }
    );

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return (
    <BugReporterProvider
      apiKey={process.env.NEXT_PUBLIC_BUG_REPORTER_API_KEY!}
      apiUrl={process.env.NEXT_PUBLIC_BUG_REPORTER_API_URL!}
      enabled={true}
      debug={process.env.NODE_ENV === 'development'}
      userContext={user ? {
        userId: user.id,
        name: user.user_metadata?.full_name || user.email,
        email: user.email
      } : undefined}
    >
      {children}
    </BugReporterProvider>
  );
}
```

2. Update `app/layout.tsx`:

```typescript
import { BugReporterWrapper } from '@/components/bug-reporter-wrapper';
import { Toaster } from 'react-hot-toast';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <BugReporterWrapper>
          {children}
        </BugReporterWrapper>
        <Toaster position="top-right" />
      </body>
    </html>
  );
}
```

#### Step 5: Verify Integration

Run the automated diagnostic tool:

```bash
node .claude/skills/bug-boundary-integration/scripts/diagnose-integration.js
```

This script checks:

- Package installation and versions
- Environment variable configuration
- Next.js layout integration
- Supabase auth integration (if applicable)
- TypeScript configuration

Address any issues reported by the diagnostic before proceeding.

#### Step 6: Test the Integration

1. Start the development server: `npm run dev`
2. Open the application in a browser
3. Look for the floating bug button (default: bottom-right corner)
4. Click the button and test bug reporting:
   - Screenshot should be captured automatically (mandatory in v1.1.0+)
   - Console logs should be captured automatically
   - User context should be populated (if authenticated)
5. Verify the bug appears in the Bug Reporter platform

### Workflow 2: Fixing Integration Issues

Follow this workflow when the Bug Reporter SDK is already installed but not working correctly.

#### Step 1: Run Diagnostics

Always start troubleshooting by running the diagnostic script:

```bash
node .claude/skills/bug-boundary-integration/scripts/diagnose-integration.js
```

The diagnostic will identify common issues and provide specific recommendations.

#### Step 2: Common Issue Resolution

**Issue: Widget Not Appearing**

Possible causes and solutions:

1. **`enabled` prop is false**
   - Solution: Ensure `enabled={true}` in `BugReporterProvider`

2. **Invalid API key**
   - Solution: Verify API key in `.env.local` starts with `app_`
   - Regenerate API key from Bug Reporter platform if needed

3. **API URL unreachable**
   - Solution: Test API URL in browser, ensure platform is accessible
   - Verify URL in `.env.local` matches platform URL exactly

4. **JavaScript errors blocking initialization**
   - Solution: Check browser console for errors
   - Ensure all imports are correct
   - Verify package version: `npm list @boobalan_jkkn/bug-reporter-sdk`

**Issue: API Key Validation Failed**

Possible causes and solutions:

1. **Incorrect API key format**
   - Solution: API key must start with `app_`
   - Copy key again from Bug Reporter platform

2. **Inactive application**
   - Solution: Check application status in Bug Reporter platform
   - Ensure application is active/enabled

3. **Mismatched API URL**
   - Solution: API URL must match the platform where API key was generated
   - Verify both values in `.env.local`

**Issue: Screenshots Not Capturing (v1.1.0+)**

Note: Screenshots are **mandatory** in v1.1.0+. The widget won't open without successful screenshot capture.

Possible causes and solutions:

1. **Browser blocking html2canvas library**
   - Solution: Check browser console for html2canvas errors
   - Try different browser (Chrome recommended)

2. **Content Security Policy (CSP) restrictions**
   - Solution: Update CSP headers to allow html2canvas
   - Add `img-src 'self' data: blob:` to CSP

3. **Conflicting screenshot libraries**
   - Solution: Temporarily disable other screenshot tools
   - Check for multiple screenshot capture libraries

4. **Modal/overlay interference**
   - Solution: Close modals/overlays before clicking bug button
   - Ensure bug button is not obscured by other elements

**Issue: Console Logs Empty (v1.1.0+)**

Note: Console logs are captured automatically in v1.1.0+.

Possible causes and solutions:

1. **Using version older than v1.1.0**
   - Solution: Update to latest: `npm install @boobalan_jkkn/bug-reporter-sdk@latest`
   - Verify version: `npm list @boobalan_jkkn/bug-reporter-sdk`

2. **No console activity before reporting**
   - Solution: Perform actions that generate console output
   - Test with `console.log('test')` before reporting bug

3. **BugReporterProvider not wrapping app correctly**
   - Solution: Ensure `<BugReporterProvider>` wraps all app content in layout
   - Check provider is at root level, not nested incorrectly

#### Step 3: Check Network Requests

If issues persist, check browser DevTools Network tab:

1. Open browser DevTools (F12)
2. Go to Network tab
3. Click the bug button
4. Look for requests to the Bug Reporter API
5. Check for:
   - Failed requests (red status codes)
   - CORS errors
   - 401/403 authentication errors
   - Network timeouts

#### Step 4: Enable Debug Mode

Temporarily enable debug mode for verbose logging:

```typescript
<BugReporterProvider
  apiKey={process.env.NEXT_PUBLIC_BUG_REPORTER_API_KEY!}
  apiUrl={process.env.NEXT_PUBLIC_BUG_REPORTER_API_URL!}
  enabled={true}
  debug={true}  // Enable debug mode
  // ... other props
>
```

Check browser console for detailed debug logs.

### Workflow 3: Advanced Features Integration

Follow this workflow when adding advanced Bug Reporter features.

#### Feature: "My Bugs" Panel

Allow users to view their submitted bug reports:

1. Create a new page or component (e.g., `app/profile/bugs/page.tsx`):

```typescript
import { MyBugsPanel } from '@boobalan_jkkn/bug-reporter-sdk';

export default function MyBugsPage() {
  return (
    <div className="container mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">My Bug Reports</h1>
      <MyBugsPanel />
    </div>
  );
}
```

2. Add navigation link to user profile or dashboard
3. Ensure user is authenticated (requires `userContext` in `BugReporterProvider`)

#### Feature: Programmatic Bug Reporting

Report bugs from error boundaries or catch blocks:

1. Create an error boundary component:

```typescript
'use client';

import { Component, ReactNode } from 'react';
import { useBugReporter } from '@boobalan_jkkn/bug-reporter-sdk';

class ErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    // Report to Bug Reporter SDK
    this.reportError(error, errorInfo);
  }

  async reportError(error: Error, errorInfo: any) {
    const { apiClient } = useBugReporter();

    try {
      await apiClient?.createBugReport({
        title: `Error: ${error.name}`,
        description: `${error.message}\n\nStack: ${error.stack}\n\nComponent Stack: ${errorInfo.componentStack}`,
        page_url: window.location.href,
        category: 'error',
        console_logs: [],
      });
    } catch (err) {
      console.error('Failed to report error to Bug Reporter:', err);
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>The error has been automatically reported.</p>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

2. Wrap components with error boundary:

```typescript
<ErrorBoundary>
  <YourComponent />
</ErrorBoundary>
```

#### Feature: Custom Widget Styling

Override default styles to match application design:

1. Add custom styles to `globals.css` or component CSS:

```css
/* Custom floating button position */
.bug-reporter-widget {
  bottom: 2rem !important;
  right: 2rem !important;
  /* Adjust z-index if needed */
  z-index: 9999 !important;
}

/* Custom modal/widget styles */
.bug-reporter-sdk {
  font-family: 'Inter', sans-serif !important;
  /* Match application color scheme */
  --primary-color: #your-brand-color;
}
```

2. Test custom styles in development mode
3. Ensure styles don't break widget functionality

#### Feature: Conditional Rendering

Show/hide bug reporter based on environment or user role:

```typescript
<BugReporterProvider
  apiKey={process.env.NEXT_PUBLIC_BUG_REPORTER_API_KEY!}
  apiUrl={process.env.NEXT_PUBLIC_BUG_REPORTER_API_URL!}
  enabled={
    // Only enable in production for beta testers
    process.env.NODE_ENV === 'production' &&
    user?.role === 'beta-tester'
  }
  debug={false}
>
  {children}
</BugReporterProvider>
```

Common conditional patterns:

- **Production only**: `process.env.NODE_ENV === 'production'`
- **Development only**: `process.env.NODE_ENV === 'development'`
- **Specific user roles**: `user?.role === 'admin' || user?.role === 'tester'`
- **Feature flag**: `featureFlags.bugReporter === true`

### Workflow 4: Upgrading to Latest Version

Follow this workflow when updating from an older SDK version.

#### Step 1: Check Current Version

```bash
npm list @boobalan_jkkn/bug-reporter-sdk
```

#### Step 2: Update to Latest Version

```bash
npm install @boobalan_jkkn/bug-reporter-sdk@latest
```

#### Step 3: Review Breaking Changes

**v1.1.0 Updates:**

- ✅ **Fully backward compatible** - no code changes required
- ✨ **New feature**: Mandatory screenshot capture (automatic)
- ✨ **New feature**: Automatic console log capture (automatic)
- No configuration changes needed

**Future versions:**

Check the package changelog for breaking changes:

```bash
npm view @boobalan_jkkn/bug-reporter-sdk versions
```

#### Step 4: Test After Upgrade

1. Run diagnostics: `node .claude/skills/bug-boundary-integration/scripts/diagnose-integration.js`
2. Start dev server: `npm run dev`
3. Test bug reporting functionality
4. Verify new features (screenshots, console logs) work correctly

## Bundled Resources

### Scripts

#### `scripts/diagnose-integration.js`

Automated diagnostic tool that checks:

- Package installation and versions
- Environment variable configuration
- Next.js layout integration
- Supabase authentication setup
- TypeScript configuration

**Usage:**

```bash
node .claude/skills/bug-boundary-integration/scripts/diagnose-integration.js
```

Run this script whenever integration issues occur or after making configuration changes.

#### `scripts/setup-bug-reporter.sh`

Automated setup script that:

- Verifies prerequisites (Node.js, npm, Next.js)
- Installs required packages
- Creates environment variables
- Prompts for API credentials
- Provides next steps guidance

**Usage:**

```bash
bash .claude/skills/bug-boundary-integration/scripts/setup-bug-reporter.sh
```

Use this for quick initial setup of the Bug Reporter SDK.

### References

#### `references/integration-guide.md`

Comprehensive reference documentation covering:

- Detailed package information
- All installation methods
- Environment requirements
- Integration patterns (basic, Supabase, conditional)
- Advanced features (My Bugs Panel, programmatic reporting, custom styling)
- API key setup process
- Complete feature list for v1.1.0+
- Troubleshooting guide for all common issues
- Version upgrade instructions

**When to reference:**

- Need detailed information about specific integration patterns
- Troubleshooting complex issues
- Implementing advanced features
- Understanding API requirements and limitations

Load this reference when detailed documentation is needed beyond the workflows in SKILL.md.

## Implementation Guidelines

### Always Follow This Sequence

1. **Verify prerequisites** before starting integration
2. **Run diagnostics** before making changes to identify issues
3. **Use the appropriate workflow** based on the situation:
   - Workflow 1 for fresh integrations
   - Workflow 2 for fixing issues
   - Workflow 3 for adding features
   - Workflow 4 for upgrades
4. **Test after each change** using the diagnostic script and manual testing
5. **Enable debug mode** when troubleshooting difficult issues

### Best Practices

- **Always use environment variables** for API credentials
- **Never commit** `.env.local` to version control
- **Verify API key format** (must start with `app_`)
- **Use Supabase integration pattern** for authenticated applications
- **Run diagnostics regularly** to catch configuration drift
- **Test in production mode** before deploying (bugs may behave differently)
- **Monitor browser console** for errors during testing
- **Keep SDK updated** to latest version for security and features

### Common Pitfalls to Avoid

- ❌ **Don't hardcode API keys** in source code
- ❌ **Don't skip environment variable setup**
- ❌ **Don't ignore diagnostic warnings**
- ❌ **Don't test only in development mode**
- ❌ **Don't forget to add Toaster component**
- ❌ **Don't wrap BugReporterProvider incorrectly** (must wrap all content)
- ❌ **Don't use outdated package versions** (update to v1.1.0+)

## Quick Reference

### Essential Commands

```bash
# Install Bug Reporter SDK
npm install @boobalan_jkkn/bug-reporter-sdk react-hot-toast

# Run diagnostics
node .claude/skills/bug-boundary-integration/scripts/diagnose-integration.js

# Quick setup (automated)
bash .claude/skills/bug-boundary-integration/scripts/setup-bug-reporter.sh

# Update to latest version
npm install @boobalan_jkkn/bug-reporter-sdk@latest

# Check current version
npm list @boobalan_jkkn/bug-reporter-sdk

# Clear npm cache (if 404 errors)
npm cache clean --force
```

### Key Package Information

- **Package**: `@boobalan_jkkn/bug-reporter-sdk`
- **Latest Version**: 1.1.0
- **Size**: 18.6 KB
- **NPM**: https://www.npmjs.com/package/@boobalan_jkkn/bug-reporter-sdk

### Required Environment Variables

```env
NEXT_PUBLIC_BUG_REPORTER_API_KEY=app_xxxxx
NEXT_PUBLIC_BUG_REPORTER_API_URL=https://your-platform.vercel.app
```

### Minimum Requirements

- Next.js 15+
- React 19+
- Node.js 18+
- TypeScript 5+ (recommended)

## Conclusion

This skill provides everything needed for production-ready Bug Reporter SDK integration. Follow the workflows sequentially, use the diagnostic tools proactively, and reference the bundled documentation when needed. The automated scripts handle tedious setup tasks, allowing focus on proper integration and testing.
