---
name: spa-integration
description: Configure SPA integration for affolterNET.Web.Bff. Use when setting up Vue/React/Angular apps, handling 401 responses, static files, or SPA fallback routing.
---

# SPA Integration

Configure single-page application integration with the BFF.

For complete reference, see [Library Guide](../../LIBRARY_GUIDE.md).

## Overview

The BFF provides SPA-friendly authentication:
- Returns 401 instead of redirecting to Keycloak
- Serves static files from wwwroot
- Fallback routing for client-side navigation
- API 404 returns JSON, SPA routes return HTML

## Authentication Flow

```
1. SPA makes API request
2. BFF returns 401 if not authenticated
3. SPA redirects to /bff/account/login
4. User authenticates with Keycloak
5. BFF creates session cookie
6. User redirected back to SPA
```

## SPA Login Handling

```typescript
// api.ts - Axios interceptor
import axios from 'axios';

const api = axios.create({
    baseURL: '/',
    withCredentials: true
});

api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            const returnUrl = encodeURIComponent(window.location.pathname);
            window.location.href = `/bff/account/login?returnUrl=${returnUrl}`;
        }
        return Promise.reject(error);
    }
);

export default api;
```

## Static Files Configuration

Static files are served from `wwwroot/`:

```
wwwroot/
├── index.html
├── assets/
│   ├── main.js
│   └── style.css
└── favicon.ico
```

## SPA Fallback Routing

The BFF automatically handles SPA routing:
- `/api/*` routes return 404 JSON if not found
- All other routes fall back to `index.html`

## Vue.js Integration

### vite.config.ts

```typescript
export default defineConfig({
    build: {
        outDir: '../wwwroot'
    },
    server: {
        proxy: {
            '/api': 'https://localhost:5001',
            '/bff': 'https://localhost:5001'
        }
    }
});
```

### Auth Store (Pinia)

```typescript
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: null,
        loading: false
    }),
    actions: {
        async fetchUser() {
            this.loading = true;
            try {
                const { data } = await api.get('/bff/account/user');
                this.user = data;
            } catch {
                this.user = null;
            } finally {
                this.loading = false;
            }
        },
        login(returnUrl?: string) {
            const url = returnUrl
                ? `/bff/account/login?returnUrl=${encodeURIComponent(returnUrl)}`
                : '/bff/account/login';
            window.location.href = url;
        },
        async logout() {
            window.location.href = '/bff/account/logout';
        }
    }
});
```

## Antiforgery for SPAs

Include CSRF token in state-changing requests:

```typescript
// Get token from cookie
function getCsrfToken(): string | null {
    const match = document.cookie.match(/XSRF-TOKEN=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : null;
}

// Include in requests
api.interceptors.request.use(config => {
    if (['post', 'put', 'delete', 'patch'].includes(config.method?.toLowerCase() ?? '')) {
        config.headers['X-XSRF-TOKEN'] = getCsrfToken();
    }
    return config;
});
```

## Troubleshooting

### SPA routes return 404
- Ensure fallback is configured in endpoint mapping
- Check wwwroot contains index.html
- Verify static files middleware is enabled

### Login redirect loop
- Check returnUrl is properly encoded
- Verify Keycloak client redirect URIs
- Review cookie settings (SameSite, Secure)
