---
name: nextjs-pwa
description: Advanced Progressive Web Application (PWA) implementation for Next.js applications with Supabase integration. Use this skill when converting Next.js applications to PWAs, implementing offline functionality, push notifications, app installation, service workers, caching strategies, background sync, and optimizing for mobile app-like experiences. Covers manifest configuration, workbox integration, Serwist setup, and Supabase offline support.
---

# Next.js PWA Implementation Skill

This skill provides comprehensive guidance for converting Next.js applications into Progressive Web Applications with advanced features including offline support, push notifications, and Supabase integration.

## Quick Start Checklist

Before implementing PWA features, ensure:
- [ ] HTTPS enabled (required for service workers)
- [ ] Next.js 14+ with App Router
- [ ] Supabase project configured (if using push notifications)
- [ ] Mobile-responsive design implemented

## Core PWA Implementation

### 1. Web App Manifest Configuration

Create `app/manifest.ts` for dynamic manifest generation:

```typescript
import type { MetadataRoute } from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Your App Name',
    short_name: 'AppName',
    description: 'Your app description',
    start_url: '/',
    scope: '/',
    display: 'standalone',
    orientation: 'portrait',
    theme_color: '#000000',
    background_color: '#ffffff',
    categories: ['productivity'],
    lang: 'en',
    dir: 'ltr',
    prefer_related_applications: false,
    icons: [
      {
        src: '/icons/icon-72x72.png',
        sizes: '72x72',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/icons/icon-96x96.png',
        sizes: '96x96',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/icons/icon-128x128.png',
        sizes: '128x128',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/icons/icon-144x144.png',
        sizes: '144x144',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/icons/icon-152x152.png',
        sizes: '152x152',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/icons/icon-192x192.png',
        sizes: '192x192',
        type: 'image/png',
        purpose: 'maskable'
      },
      {
        src: '/icons/icon-384x384.png',
        sizes: '384x384',
        type: 'image/png',
        purpose: 'any'
      },
      {
        src: '/icons/icon-512x512.png',
        sizes: '512x512',
        type: 'image/png',
        purpose: 'maskable'
      }
    ],
    screenshots: [
      {
        src: '/screenshots/desktop.png',
        type: 'image/png',
        sizes: '1920x1080',
        form_factor: 'wide'
      },
      {
        src: '/screenshots/mobile.png',
        type: 'image/png',
        sizes: '390x844',
        form_factor: 'narrow'
      }
    ],
    shortcuts: [
      {
        name: 'Dashboard',
        short_name: 'Dashboard',
        description: 'Go to dashboard',
        url: '/dashboard',
        icons: [{ src: '/icons/dashboard.png', sizes: '96x96' }]
      }
    ]
  }
}
```

### 2. Viewport and Theme Configuration

Configure viewport in `app/layout.tsx`:

```typescript
import type { Viewport } from 'next'

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  viewportFit: 'cover',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#ffffff' },
    { media: '(prefers-color-scheme: dark)', color: '#000000' }
  ]
}
```

### 3. Icon Generation Strategy

Generate all required icon sizes using the script in `scripts/generate-icons.js`.

Place source icon (512x512px minimum) in `public/icon-source.png`.

## Offline Support with Serwist

### 1. Install Dependencies

```bash
npm install @serwist/next @serwist/cli
npm install -D @serwist/webpack-plugin
```

### 2. Configure Serwist

Create `next.config.mjs`:

```javascript
import withSerwistInit from '@serwist/next'

const withSerwist = withSerwistInit({
  swSrc: 'app/sw.ts',
  swDest: 'public/sw.js',
  reloadOnOnline: true,
  disable: process.env.NODE_ENV === 'development'
})

export default withSerwist({
  reactStrictMode: true,
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb'
    }
  }
})
```

### 3. Service Worker Implementation

Create `app/sw.ts`:

```typescript
import { defaultCache } from '@serwist/next/browser'
import type { PrecacheEntry } from '@serwist/precaching'
import { installSerwist } from '@serwist/sw'

declare const self: ServiceWorkerGlobalScope & {
  __SW_MANIFEST: (PrecacheEntry | string)[]
  __BUILD_TIME: string
}

// Core service worker setup
installSerwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: true,
  runtimeCaching: [
    ...defaultCache,
    {
      matcher: /^https:\/\/.*\.supabase\.co\/storage\/.*/,
      handler: 'CacheFirst',
      options: {
        cacheName: 'supabase-storage',
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 60 * 60 * 24 * 30 // 30 days
        }
      }
    },
    {
      matcher: /^https:\/\/.*\.supabase\.co\/rest\/.*/,
      handler: 'NetworkFirst',
      options: {
        cacheName: 'supabase-api',
        networkTimeoutSeconds: 10,
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 60 * 5 // 5 minutes
        }
      }
    }
  ],
  offlineGoogleAnalytics: true,
  cleanupOutdatedCaches: true,
  precacheOptions: {
    ignoreURLParametersMatching: [/^utm_/, /^fbclid$/]
  }
})

// Background sync for form submissions
self.addEventListener('sync', (event: any) => {
  if (event.tag === 'sync-forms') {
    event.waitUntil(syncOfflineData())
  }
})

async function syncOfflineData() {
  // Implementation in references/background-sync.md
}

// Push notification handling
self.addEventListener('push', function(event: PushEvent) {
  if (!event.data) return

  const data = event.data.json()
  const options: NotificationOptions = {
    body: data.body,
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [200, 100, 200],
    tag: data.tag || 'default',
    renotify: true,
    requireInteraction: false,
    actions: data.actions || [],
    data: {
      url: data.url || '/',
      timestamp: Date.now()
    }
  }

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  )
})

self.addEventListener('notificationclick', function(event: any) {
  event.notification.close()
  
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  )
})
```

## Push Notifications with Supabase

### 1. Database Schema

Create push subscriptions table in Supabase:

```sql
CREATE TABLE push_subscriptions (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  endpoint TEXT NOT NULL,
  p256dh TEXT NOT NULL,
  auth TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id, endpoint)
);

-- Enable RLS
ALTER TABLE push_subscriptions ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can manage own subscriptions"
  ON push_subscriptions
  FOR ALL
  USING (auth.uid() = user_id);
```

### 2. Server Actions for Push Notifications

Create `app/actions/push-notifications.ts`:

```typescript
'use server'

import webpush from 'web-push'
import { createClient } from '@/lib/supabase/server'

// Configure VAPID
webpush.setVapidDetails(
  `mailto:${process.env.VAPID_EMAIL}`,
  process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!,
  process.env.VAPID_PRIVATE_KEY!
)

export async function subscribeToPush(subscription: PushSubscription) {
  const supabase = await createClient()
  
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('Not authenticated')

  const { error } = await supabase
    .from('push_subscriptions')
    .upsert({
      user_id: user.id,
      endpoint: subscription.endpoint,
      p256dh: subscription.toJSON().keys?.p256dh,
      auth: subscription.toJSON().keys?.auth
    })

  if (error) throw error
  return { success: true }
}

export async function sendPushNotification(
  userId: string,
  payload: { title: string; body: string; url?: string }
) {
  const supabase = await createClient()
  
  const { data: subscriptions } = await supabase
    .from('push_subscriptions')
    .select('*')
    .eq('user_id', userId)

  if (!subscriptions) return

  const notifications = subscriptions.map(sub => 
    webpush.sendNotification(
      {
        endpoint: sub.endpoint,
        keys: {
          p256dh: sub.p256dh,
          auth: sub.auth
        }
      },
      JSON.stringify(payload)
    ).catch(error => {
      if (error.statusCode === 410) {
        // Subscription expired, remove it
        supabase
          .from('push_subscriptions')
          .delete()
          .eq('id', sub.id)
      }
    })
  )

  await Promise.all(notifications)
}
```

### 3. Client Component for Push Management

Create `app/components/push-notifications.tsx`:

```typescript
'use client'

import { useState, useEffect } from 'react'
import { subscribeToPush, unsubscribeFromPush } from '@/app/actions/push-notifications'

function urlBase64ToUint8Array(base64String: string) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4)
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/')
  const rawData = window.atob(base64)
  return new Uint8Array([...rawData].map(char => char.charCodeAt(0)))
}

export function PushNotificationManager() {
  const [permission, setPermission] = useState<NotificationPermission>('default')
  const [subscription, setSubscription] = useState<PushSubscription | null>(null)
  const [isSupported, setIsSupported] = useState(false)

  useEffect(() => {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
      setIsSupported(true)
      setPermission(Notification.permission)
      checkExistingSubscription()
    }
  }, [])

  async function checkExistingSubscription() {
    const registration = await navigator.serviceWorker.ready
    const sub = await registration.pushManager.getSubscription()
    setSubscription(sub)
  }

  async function subscribe() {
    const registration = await navigator.serviceWorker.ready
    
    const permission = await Notification.requestPermission()
    setPermission(permission)
    
    if (permission !== 'granted') return

    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(
        process.env.NEXT_PUBLIC_VAPID_PUBLIC_KEY!
      )
    })

    setSubscription(subscription)
    await subscribeToPush(subscription)
  }

  async function unsubscribe() {
    if (!subscription) return
    
    await subscription.unsubscribe()
    await unsubscribeFromPush()
    setSubscription(null)
  }

  if (!isSupported) {
    return null
  }

  return (
    <div className="push-notifications">
      {subscription ? (
        <button onClick={unsubscribe}>
          Disable Push Notifications
        </button>
      ) : (
        <button onClick={subscribe}>
          Enable Push Notifications
        </button>
      )}
    </div>
  )
}
```

## App Installation Components

### 1. Install Prompt Handler

Create `app/components/install-prompt.tsx`:

```typescript
'use client'

import { useState, useEffect } from 'react'

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>
}

export function InstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null)
  const [isInstalled, setIsInstalled] = useState(false)
  const [isIOS, setIsIOS] = useState(false)
  const [isStandalone, setIsStandalone] = useState(false)

  useEffect(() => {
    // Check if app is already installed
    setIsStandalone(
      window.matchMedia('(display-mode: standalone)').matches ||
      (window.navigator as any).standalone === true
    )

    // Detect iOS
    setIsIOS(
      /iPad|iPhone|iPod/.test(navigator.userAgent) && 
      !(window as any).MSStream
    )

    // Listen for install prompt
    const handleBeforeInstallPrompt = (e: Event) => {
      e.preventDefault()
      setDeferredPrompt(e as BeforeInstallPromptEvent)
    }

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt)

    // Check if app was installed
    window.addEventListener('appinstalled', () => {
      setIsInstalled(true)
      setDeferredPrompt(null)
    })

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt)
    }
  }, [])

  async function handleInstallClick() {
    if (!deferredPrompt) return

    deferredPrompt.prompt()
    const { outcome } = await deferredPrompt.userChoice
    
    if (outcome === 'accepted') {
      setIsInstalled(true)
    }
    setDeferredPrompt(null)
  }

  if (isStandalone || isInstalled) {
    return null
  }

  if (isIOS) {
    return (
      <div className="install-prompt-ios">
        <p>
          To install this app on your iOS device, tap the share button 
          <span aria-label="share icon"> ⎋ </span>
          and then "Add to Home Screen"
          <span aria-label="plus icon"> ⊕ </span>
        </p>
      </div>
    )
  }

  if (deferredPrompt) {
    return (
      <button onClick={handleInstallClick}>
        Install App
      </button>
    )
  }

  return null
}
```

### 2. Update Prompt Component

Create `app/components/update-prompt.tsx`:

```typescript
'use client'

import { useState, useEffect } from 'react'

export function UpdatePrompt() {
  const [showReload, setShowReload] = useState(false)
  const [waitingWorker, setWaitingWorker] = useState<ServiceWorker | null>(null)

  useEffect(() => {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.ready.then(registration => {
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing
          if (newWorker) {
            newWorker.addEventListener('statechange', () => {
              if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                setWaitingWorker(newWorker)
                setShowReload(true)
              }
            })
          }
        })
      })
    }
  }, [])

  function handleUpdate() {
    if (waitingWorker) {
      waitingWorker.postMessage({ type: 'SKIP_WAITING' })
      waitingWorker.addEventListener('statechange', () => {
        if (waitingWorker.state === 'activated') {
          window.location.reload()
        }
      })
    }
  }

  if (!showReload) return null

  return (
    <div className="update-prompt">
      <p>A new version is available!</p>
      <button onClick={handleUpdate}>Update</button>
    </div>
  )
}
```

## Performance Optimizations

### 1. App Shell Architecture

Implement app shell pattern in `app/layout.tsx`:

```typescript
export default async function RootLayout({
  children
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AppShell>
          {children}
        </AppShell>
      </body>
    </html>
  )
}
```

### 2. Resource Hints

Add resource hints to `app/layout.tsx`:

```typescript
export const metadata: Metadata = {
  other: {
    'dns-prefetch': [
      'https://fonts.googleapis.com',
      'https://your-supabase-url.supabase.co'
    ],
    'preconnect': [
      'https://fonts.gstatic.com',
      'https://your-supabase-url.supabase.co'
    ]
  }
}
```

## Security Configuration

### 1. Content Security Policy

Configure CSP in `next.config.js`:

```javascript
async headers() {
  return [
    {
      source: '/sw.js',
      headers: [
        {
          key: 'Cache-Control',
          value: 'no-cache, no-store, must-revalidate'
        },
        {
          key: 'Content-Type',
          value: 'application/javascript; charset=utf-8'
        }
      ]
    },
    {
      source: '/(.*)',
      headers: [
        {
          key: 'X-Content-Type-Options',
          value: 'nosniff'
        },
        {
          key: 'X-Frame-Options', 
          value: 'DENY'
        },
        {
          key: 'X-XSS-Protection',
          value: '1; mode=block'
        }
      ]
    }
  ]
}
```

## Testing & Validation

### PWA Checklist

- [ ] Lighthouse PWA audit score > 90
- [ ] Works offline for critical pages
- [ ] App installs on mobile devices
- [ ] Push notifications work (if implemented)
- [ ] App updates seamlessly
- [ ] HTTPS everywhere
- [ ] Valid manifest.json
- [ ] All icon sizes present
- [ ] Splash screens configured
- [ ] Theme color matches brand

### Browser Testing Matrix

Test on:
- Chrome (Desktop & Mobile)
- Safari (iOS 16.4+)
- Firefox
- Edge
- Samsung Internet

## Troubleshooting

Common issues and solutions:

1. **Service worker not registering**: Check HTTPS, check console errors
2. **Install prompt not showing**: Ensure manifest is valid, check Lighthouse
3. **Push notifications failing**: Verify VAPID keys, check Supabase connection
4. **Offline not working**: Check cache strategies, verify service worker scope
5. **iOS installation issues**: Ensure apple-touch-icons are present

## References

- See `references/serwist-config.md` for advanced Serwist configuration
- See `references/supabase-offline.md` for offline Supabase patterns
- See `references/background-sync.md` for background sync implementation
- See `references/web-share.md` for Web Share API implementation
- See `references/testing-guide.md` for comprehensive testing strategies

## Scripts

- Use `scripts/generate-icons.js` to generate all PWA icons
- Use `scripts/generate-vapid.js` to generate VAPID keys
- Use `scripts/test-push.js` to test push notifications
