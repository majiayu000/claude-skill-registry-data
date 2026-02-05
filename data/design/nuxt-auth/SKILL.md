---
name: nuxt-auth
description: Authentication with Laravel Sanctum and permission-based authorization. Use when implementing login/logout, protecting pages with permissions, checking permissions in components, or understanding the auth flow.
---

# Nuxt Authentication & Authorization

Laravel Sanctum authentication with permission-based access control.

## Core Concepts

**[auth.md](references/auth.md)** - Complete auth patterns, permissions, page protection

## Sanctum Setup

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['nuxt-auth-sanctum'],

  sanctum: {
    baseUrl: process.env.NUXT_PUBLIC_API_URL,
    endpoints: {
      login: '/auth/login',
      user: '/auth/user',
      csrf: '/sanctum/csrf-cookie',
      logout: '/auth/logout',
    },
    redirect: {
      onAuthOnly: '/auth/login',
      onGuestOnly: '/',
    },
  },
})
```

## Auth Composable

```typescript
const { user, isAuthenticated, login, logout, init } = useSanctumAuth()

// Login
await login({ email, password })

// Logout
await logout()

// Check auth
if (isAuthenticated.value) { /* ... */ }
```

## Permission Checking

```typescript
const { can, cannot } = usePermissions()

// Single permission
if (can('leads.create')) { /* ... */ }

// In templates
<UButton v-if="can('leads.create')" @click="createLead">Create</UButton>
```

## Page Protection

```typescript
definePageMeta({
  permissions: 'leads.list',
})
```
