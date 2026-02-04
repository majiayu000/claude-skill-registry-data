---
name: auth-components
description: Pre-built and custom Clerk authentication component templates with theming and customization patterns. Use when building authentication UI, creating sign-in/sign-up pages, customizing Clerk components, implementing user buttons, theming auth flows, or when user mentions Clerk components, SignIn, SignUp, UserButton, auth UI, appearance customization, or authentication theming.
allowed-tools: Bash, Read, Write, Edit
---

# Clerk Auth Components Skill

This skill provides comprehensive templates and patterns for implementing and customizing Clerk authentication components including pre-built components, Clerk Elements for custom flows, and appearance theming.

## Overview

Clerk offers two approaches for authentication UI:

1. **Pre-built Components** - Ready-to-use `<SignIn />`, `<SignUp />`, `<UserButton />` with minimal configuration
2. **Clerk Elements** - Custom components with granular control for advanced use-cases

This skill covers both approaches with practical templates and customization patterns.

## Available Scripts

### 1. Generate Authentication UI Pages

**Script**: `scripts/generate-auth-ui.sh <output-dir> <component-type>`

**Purpose**: Generates complete authentication page templates

**Component Types**:
- `signin` - SignIn page with routing
- `signup` - SignUp page with routing
- `both` - Both SignIn and SignUp pages
- `profile` - User profile page
- `all` - Complete auth UI set

**Usage**:
```bash
# Generate sign-in page
./scripts/generate-auth-ui.sh ./app/sign-in signin

# Generate both sign-in and sign-up
./scripts/generate-auth-ui.sh ./app signup

# Generate complete auth UI
./scripts/generate-auth-ui.sh ./app all
```

**Generated Files**:
- `app/sign-in/[[...sign-in]]/page.tsx`
- `app/sign-up/[[...sign-up]]/page.tsx`
- `app/profile/[[...profile]]/page.tsx`
- `components/auth/protected-wrapper.tsx`

### 2. Customize Appearance and Theming

**Script**: `scripts/customize-appearance.sh <config-file> <theme-preset>`

**Purpose**: Generates appearance configuration for Clerk components

**Theme Presets**:
- `default` - Clerk default theme
- `dark` - Dark mode theme
- `neobrutalist` - Neobrutalist theme
- `shadesOfPurple` - Shades of Purple theme
- `custom` - Custom theme template

**Usage**:
```bash
# Generate dark theme config
./scripts/customize-appearance.sh ./lib/clerk-config.ts dark

# Generate custom theme template
./scripts/customize-appearance.sh ./lib/clerk-config.ts custom

# Generate theme with custom variables
BRAND_COLOR="#6366f1" ./scripts/customize-appearance.sh ./lib/clerk-config.ts custom
```

**Environment Variables**:
- `BRAND_COLOR` - Primary brand color (hex)
- `BACKGROUND` - Background color (hex)
- `TEXT_COLOR` - Text color (hex)

### 3. Validate Component Implementation

**Script**: `scripts/validate-components.sh <project-dir>`

**Purpose**: Validates Clerk component setup and configuration

**Checks**:
- Clerk dependencies installed (@clerk/nextjs)
- Environment variables configured
- ClerkProvider setup in layout
- Authentication pages exist
- Middleware configured
- No hardcoded secrets

**Usage**:
```bash
# Validate current project
./scripts/validate-components.sh .

# Validate specific directory
./scripts/validate-components.sh /path/to/project
```

**Exit Codes**:
- `0`: Validation passed
- `1`: Validation failed (must fix issues)

## Available Templates

### 1. Sign-In Page Template

**Template**: `templates/sign-in-page.tsx`

**Features**:
- Next.js App Router integration
- Catch-all routing `[[...sign-in]]`
- After sign-in redirect configuration
- Centered layout with responsive design

**Usage**:
```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from '@clerk/nextjs'

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn
        appearance={{
          elements: {
            rootBox: "mx-auto",
            card: "shadow-lg"
          }
        }}
        afterSignInUrl="/dashboard"
      />
    </div>
  )
}
```

### 2. Sign-Up Page Template

**Template**: `templates/sign-up-page.tsx`

**Features**:
- Next.js App Router integration
- Catch-all routing `[[...sign-up]]`
- After sign-up redirect configuration
- Custom appearance configuration

### 3. Custom User Button Template

**Template**: `templates/user-button-custom.tsx`

**Features**:
- Custom menu items
- Appearance customization
- Avatar size control
- Dropdown actions

**Customization Example**:
```typescript
<UserButton
  appearance={{
    elements: {
      userButtonAvatarBox: "w-10 h-10",
      userButtonPopoverCard: "shadow-xl"
    }
  }}
>
  <UserButton.MenuItems>
    <UserButton.Link
      label="Dashboard"
      labelIcon={<LayoutDashboard size={16} />}
      href="/dashboard"
    />
    <UserButton.Action
      label="Settings"
      labelIcon={<Settings size={16} />}
      onClick={() => router.push('/settings')}
    />
  </UserButton.MenuItems>
</UserButton>
```

### 4. Protected Route Wrapper

**Template**: `templates/protected-wrapper.tsx`

**Features**:
- Authentication guard for routes
- Loading states
- Redirect configuration
- Reusable HOC pattern

**Usage**:
```typescript
// app/dashboard/page.tsx
import { ProtectedRoute } from '@/components/auth/protected-wrapper'

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div>Protected Dashboard Content</div>
    </ProtectedRoute>
  )
}
```

## Available Examples

### 1. Custom Sign-In with Clerk Elements

**Example**: `examples/custom-sign-in-guide.md` (code: `examples/custom-sign-in.tsx`)

**Demonstrates**:
- Clerk Elements for custom sign-in flow
- Step-based authentication
- Strategy selection (password, OAuth)
- Form validation
- Error handling
- Custom styling

**Key Components**:
```typescript
<SignIn.Root>
  <SignIn.Step name="start">
    {/* Email/username input */}
    <SignIn.Strategy name="password">
      {/* Password input */}
    </SignIn.Strategy>
    <SignIn.Strategy name="email_code">
      {/* Email verification */}
    </SignIn.Strategy>
  </SignIn.Step>
</SignIn.Root>
```

### 2. Social Authentication Buttons

**Example**: `examples/social-authentication-guide.md` (code: `examples/social-buttons.tsx`)

**Demonstrates**:
- OAuth provider buttons
- Custom social button styling
- Loading states
- Error handling
- Multiple providers (Google, GitHub, Discord)

**Supported Providers**:
- Google
- GitHub
- Discord
- Microsoft
- Facebook
- Apple

### 3. Complete Theme Configuration

**Example**: `examples/theming-guide.md` (code: `examples/theme-config.tsx`)

**Demonstrates**:
- Complete appearance configuration
- CSS variables customization
- Layout configuration
- Element-specific styling
- Dark mode support
- Responsive design

## Appearance Customization Guide

### 1. Appearance Prop Structure

The `appearance` prop accepts:

```typescript
appearance={{
  baseTheme: dark,           // Base theme
  layout: {                  // Layout options
    shimmer: true,
    logoPlacement: 'inside'
  },
  variables: {               // CSS variables
    colorPrimary: '#6366f1',
    colorBackground: '#ffffff',
    colorText: '#1f2937',
    borderRadius: '0.5rem'
  },
  elements: {                // Element overrides
    card: 'shadow-lg',
    formButtonPrimary: 'bg-blue-500',
    footerActionLink: 'text-blue-600'
  }
}}
```

### 2. Global vs Component-Level Theming

**Global (ClerkProvider)**:
```typescript
<ClerkProvider appearance={{
  baseTheme: dark,
  variables: { colorPrimary: '#6366f1' }
}}>
  {children}
</ClerkProvider>
```

**Component-Level**:
```typescript
<SignIn appearance={{
  elements: {
    card: 'shadow-xl',
    rootBox: 'mx-auto'
  }
}} />
```

### 3. Tailwind CSS v4 Integration

For Tailwind CSS v4 support:

```typescript
<ClerkProvider
  appearance={{
    cssLayerName: 'clerk'  // Ensures Tailwind utilities override
  }}
>
```

### 4. Element Targeting

Common element selectors:

- `rootBox` - Root container
- `card` - Main card container
- `headerTitle` - Header text
- `formButtonPrimary` - Submit buttons
- `formFieldInput` - Input fields
- `footerActionLink` - Footer links
- `userButtonAvatarBox` - User avatar
- `userButtonPopoverCard` - Dropdown menu

## Security Compliance

This skill follows strict security rules:
- All code examples use placeholder values only
- No real API keys, passwords, or secrets
- Environment variable references in all code
- `.gitignore` protection documented
- CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY read from environment

## Best Practices

1. **Use Pre-built Components First** - Start with `<SignIn />`, `<SignUp />` before custom Elements
2. **Apply Global Themes** - Configure appearance at `<ClerkProvider>` level for consistency
3. **Leverage CSS Variables** - Use `variables` prop for brand colors, spacing, and typography
4. **Element Overrides for Fine-Tuning** - Use `elements` prop for specific component styling
5. **Protect Routes** - Always wrap protected content in authentication checks
6. **Handle Loading States** - Show loading indicators during authentication state checks
7. **Configure Redirects** - Set `afterSignInUrl` and `afterSignUpUrl` for better UX
8. **Responsive Design** - Test auth components on mobile and desktop viewports

## Requirements

- Clerk account with API keys
- Next.js 13+ with App Router (for examples)
- React 18+
- Environment variables:
  - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
  - `CLERK_SECRET_KEY`
- Optional: `@clerk/themes` for pre-built themes
- Optional: Tailwind CSS for styling examples

## Progressive Disclosure

For advanced customization patterns, see:
- `examples/custom-sign-in.tsx` - Complete Clerk Elements implementation
- `examples/social-buttons.tsx` - OAuth provider integration
- `examples/theme-config.tsx` - Advanced theming patterns
