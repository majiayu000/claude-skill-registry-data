---
name: td-javascript-sdk
description: Expert assistance for importing data to Treasure Data using the JavaScript SDK. Use this skill when users need help with browser-based event tracking, page analytics, client-side data collection, or implementing TD's JS SDK for web applications.
---

# Treasure Data JavaScript SDK

Browser-only SDK for client-side event tracking. For server-side, use REST API or pytd.

## Quick Start: Pageview Tracking

Add to HTML `<head>`:

```html
<!-- TD JS SDK Loader (v4.4.1) -->
<script type="text/javascript">
!function(t,e){if(void 0===e[t]){e[t]=function(){e[t].clients.push(this),this._init=[Array.prototype.slice.call(arguments)]},e[t].clients=[];for(var r=function(t){return function(){return this["_"+t]=this["_"+t]||[],this["_"+t].push(Array.prototype.slice.call(arguments)),this}},s=["collectTags","addRecord","blockEvents","fetchServerCookie","fetchGlobalID","fetchUserSegments","fetchPersonalization","resetUUID","ready","setSignedMode","setAnonymousMode","set","trackEvent","trackPageview","trackClicks","unblockEvents"],c=0;c<s.length;c++){var o=s[c];e[t].prototype[o]=r(o)}var n=document.createElement("script");n.type="text/javascript",n.async=!0,n.src="https://cdn.treasuredata.com/sdk/4.4.1/td.min.js";var i=document.getElementsByTagName("script")[0];i.parentNode.insertBefore(n,i)}}("Treasure",this);
</script>

<!-- Initialize and track -->
<script type="text/javascript">
var td = new Treasure({
  database: 'your_database',
  writeKey: '1234/xxxxxxxx',  // write-only API key
  host: 'us01.records.in.treasuredata.com'
});
td.trackPageview('pageviews');
</script>
```

## Configuration

```javascript
var td = new Treasure({
  database: 'your_database',        // required
  writeKey: '1234/xxxxxxxx',        // required, write-only API key
  host: 'us01.records.in.treasuredata.com',  // required for v4.0+
  development: true                 // optional, enables console logging
});
```

**Regional Streaming Endpoints (v4.0+ required):**
| Region | Endpoint |
|--------|----------|
| US | `us01.records.in.treasuredata.com` |
| Tokyo | `ap01.records.in.treasuredata.com` |
| EU | `eu01.records.in.treasuredata.com` |
| AP | `ap02.records.in.treasuredata.com` |

## Core Methods

```javascript
// Track pageview (auto-collects URL, title, referrer, user agent, etc.)
td.trackPageview('pageviews');

// Track custom events (also auto-collects context like trackPageview)
td.trackEvent('events', { action: 'signup', location: 'header' });

// Send raw records (no auto-collected fields)
td.addRecord('purchases', { order_id: '123', amount: 99.99 });

// Auto-track clicks on links, buttons, inputs (excludes password fields)
td.trackClicks({ tableName: 'clicks' });

// Set global properties (included in all subsequent trackEvent/trackPageview calls)
td.set('$global', { user_id: 'user_123', environment: 'production' });
```

## Auto-Collected Fields

`trackPageview()` and `trackEvent()` automatically include:
- `td_url`, `td_title`, `td_referrer`, `td_host`, `td_path`
- `td_screen`, `td_viewport`, `td_language`
- `td_user_agent`, `td_platform`
- `td_client_id`, `td_version`

## Privacy Controls

```javascript
td.setAnonymousMode();   // Exclude PII from tracking
td.setSignedMode();      // Include PII
td.blockEvents();        // Stop sending events
td.unblockEvents();      // Resume sending
td.resetUUID();          // Generate new client ID
```

## NPM Installation

```bash
npm install td-js-sdk
```

```javascript
import Treasure from 'td-js-sdk';
```

## Resources

- GitHub: https://github.com/treasure-data/td-js-sdk
- CDN: `https://cdn.treasuredata.com/sdk/4.4.1/td.min.js`
