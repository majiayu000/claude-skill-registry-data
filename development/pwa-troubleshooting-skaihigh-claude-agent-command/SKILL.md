---
name: pwa-troubleshooting
description: Automatically helps debug PWA issues including service workers, caching, offline functionality, and storage problems in VSSK-shadecn
---

# PWA Troubleshooting Skill

This skill activates when you encounter PWA-related issues.

## When to Use

Automatically activates for:
- Service worker not registering
- Offline mode not working
- Cache not updating
- Storage quota exceeded
- IndexedDB errors
- PWA install issues
- Update notifications not showing

## Troubleshooting Steps

### 1. Service Worker Issues

**Not Registering**
```javascript
// Check registration
navigator.serviceWorker.getRegistration()
  .then(reg => console.log('SW registered:', !!reg))
  .catch(err => console.error('SW error:', err))

// Common causes:
// - Not served over HTTPS (localhost is OK)
// - Path issues (SW scope)
// - JavaScript errors in SW file
// - Browser doesn't support SW
```

**Not Activating**
```javascript
// Check SW state
navigator.serviceWorker.getRegistration().then(reg => {
  console.log('Active:', reg?.active)
  console.log('Installing:', reg?.installing)
  console.log('Waiting:', reg?.waiting)
})

// Force activate waiting SW
registration.waiting?.postMessage({ type: 'SKIP_WAITING' })
```

**Not Updating**
```javascript
// Force update check
registration.update()

// Clear old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CURRENT_CACHE)
          .map(key => caches.delete(key))
      )
    )
  )
})
```

### 2. Caching Issues

**Cache Not Working**
- [ ] Cache name versioned correctly?
- [ ] Fetch event listener registered?
- [ ] Network-first for metadata, cache-first for assets?
- [ ] CORS headers on audio files?

**Diagnostic**
```javascript
// List all caches
caches.keys().then(keys => console.log('Caches:', keys))

// Check specific cache
caches.open('audio-v1').then(cache =>
  cache.keys().then(requests =>
    console.log('Cached URLs:', requests.map(r => r.url))
  )
)

// Test cache match
caches.match('/audio/song.mp3').then(response =>
  console.log('Cache hit:', !!response)
)
```

**Fix Stale Cache**
```javascript
// Clear all caches (dev only!)
caches.keys().then(keys =>
  Promise.all(keys.map(key => caches.delete(key)))
).then(() => console.log('All caches cleared'))
```

### 3. Offline Functionality

**App Not Working Offline**
- [ ] Service worker installed and active?
- [ ] All critical assets cached?
- [ ] Offline fallback implemented?
- [ ] IndexedDB working for user data?

**Test Offline Mode**
```javascript
// Simulate offline
if ('serviceWorker' in navigator && 'controller' in navigator.serviceWorker) {
  // Go offline in DevTools Network tab
  // Or use: window.dispatchEvent(new Event('offline'))
}

// Listen for offline events
window.addEventListener('offline', () => {
  console.log('App is offline')
  // Show offline UI
})

window.addEventListener('online', () => {
  console.log('App is online')
  // Sync data
})
```

### 4. Storage Issues

**Quota Exceeded**
```javascript
// Check quota
const estimate = await navigator.storage.estimate()
const percentUsed = (estimate.usage / estimate.quota) * 100
console.log(`Storage: ${percentUsed.toFixed(2)}% used`)

if (percentUsed > 80) {
  console.warn('Storage almost full!')
  // Implement cache eviction (LRU)
}
```

**IndexedDB Errors**
```javascript
// Check IndexedDB availability
if (!('indexedDB' in window)) {
  console.error('IndexedDB not supported')
}

// Test IndexedDB connection
const request = indexedDB.open('vssk-db', 1)
request.onerror = () => console.error('IndexedDB error:', request.error)
request.onsuccess = () => console.log('IndexedDB opened successfully')
```

### 5. PWA Install Issues

**Install Prompt Not Showing**
- [ ] Manifest.json valid and served?
- [ ] HTTPS (or localhost)?
- [ ] Service worker registered?
- [ ] User hasn't dismissed recently?
- [ ] beforeinstallprompt event captured?

**Check Manifest**
```javascript
// Verify manifest loading
fetch('/manifest.json')
  .then(res => res.json())
  .then(manifest => console.log('Manifest:', manifest))
  .catch(err => console.error('Manifest error:', err))
```

## Common Fixes

### Force Service Worker Update
```javascript
// In your app
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js')
    .then(reg => {
      // Check for updates every hour
      setInterval(() => reg.update(), 60 * 60 * 1000)
    })
}
```

### Handle Update Notification
```javascript
registration.addEventListener('updatefound', () => {
  const newWorker = registration.installing
  newWorker.addEventListener('statechange', () => {
    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
      // Show "Update available" notification
      showUpdateNotification()
    }
  })
})
```

### LRU Cache Eviction
```javascript
// Evict oldest cached audio when quota reached
async function evictOldestAudio() {
  const cache = await caches.open('audio-v1')
  const requests = await cache.keys()

  // Sort by last accessed (you'll need to track this)
  const oldest = requests[0] // Simplification
  await cache.delete(oldest)
}
```

## Output Format

Provide:
1. **Issue Identified**: What's not working
2. **Diagnosis**: Why it's happening
3. **Fix**: Step-by-step solution with code
4. **Verification**: How to test it's fixed
5. **Prevention**: Avoid in future
