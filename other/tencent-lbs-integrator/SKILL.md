---
name: tencent-lbs-integrator
description: Integrate Tencent LBS for maps, geocoding, and location services. Use this skill when the application needs interactive maps, address geocoding, location markers, IP geolocation, or place search. Triggers on requests for map display, address lookup, location markers, or geographic services.
_meta_type: sdk
---

# Tencent LBS SDK Integration

## Scenarios

- **Interactive Maps**: Dynamic map display with markers and info windows for meeting/event locations
- **Address Geocoding**: Convert addresses to coordinates for location-based features
- **Reverse Geocoding**: Get address information from coordinates
- **Place Search**: Search for POIs (Points of Interest) by keyword
- **IP Geolocation**: Determine user location from IP address
- **Static Maps**: Generate map images for emails and previews

**Not recommended for:**
- Real-time navigation (requires native SDK)
- Mobile native applications (requires mobile SDK)
- Offline map functionality

## Setup

### 1. Install Dependencies

No npm package required for basic usage. The SDK loads the map API dynamically.

### 2. Copy SDK Wrapper

Read `lib/tencent-lbs.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Built-in API Key

The SDK includes a built-in API Key for immediate use:

```typescript
import { createClient, loadTMapGL, createMap } from './lib/tencent-lbs';

// Ready to use immediately
const client = createClient();
await loadTMapGL();
```

### Domain Whitelist (Required for Production)

For production use, configure your domain in the whitelist:

1. Visit [Tencent LBS Console](https://lbs.qq.com/dev/console/application/mine)
2. Go to "Key Management" -> Select Key -> "Settings"
3. Add your website domain to "Domain Whitelist"
4. Subdomains are automatically authorized

## Quick Start

### JavaScript GL API (Dynamic Maps)

```typescript
import { 
  loadTMapGL, 
  createMap, 
  addMarkerWithInfo,
  createClient 
} from './lib/tencent-lbs';

// 1. Load map API
await loadTMapGL();

// 2. Create map (container element must exist)
const map = createMap('map-container', {
  center: { lat: 39.984120, lng: 116.307484 },
  zoom: 15
});

// 3. Add marker with info window
const { markerLayer, infoWindow } = addMarkerWithInfo(
  map,
  { lat: 39.984120, lng: 116.307484 },
  'Meeting Location',
  '<p>123 Example Street, Beijing</p>'
);
```

### HTML Container

```html
<div id="map-container" style="width: 100%; height: 400px;"></div>
```

### WebService API (Geocoding & Search)

```typescript
import { createClient, LBSError } from './lib/tencent-lbs';

const client = createClient();

// Geocode address
const result = await client.geocode('123 Example Street, Beijing');
console.log(result.result.location); // { lat: 39.984154, lng: 116.307490 }

// Reverse geocode
const address = await client.reverseGeocode(39.984154, 116.307490);
console.log(address.result.address);

// Search places
const places = await client.searchPlace('hotel', {
  boundary: 'region(Beijing,0)'
});

// IP geolocation
const location = await client.ipLocation('111.206.145.41');
```

### Static Map URL

```typescript
const mapUrl = client.getStaticMapUrl({
  center: { lat: 39.908823, lng: 116.397496 },
  zoom: 15,
  size: { width: 600, height: 400 },
  scale: 2,
  markers: [{
    position: { lat: 39.908823, lng: 116.397496 },
    label: 'A',
    color: 'red'
  }]
});

// Use in <img> tag
// <img src={mapUrl} alt="Map" />
```

## React Component Example

```tsx
import { useEffect, useRef, useState } from 'react';
import {
  loadTMapGL,
  createMap,
  addMarkerWithInfo,
  createClient,
  LBSError
} from '@/lib/tencent-lbs';

interface MeetingMapProps {
  address: string;
}

export function MeetingMap({ address }: MeetingMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let map: ReturnType<typeof createMap> | null = null;

    async function init() {
      try {
        // Geocode address
        const client = createClient();
        const { result } = await client.geocode(address);
        const location = result.location;

        // Load map API
        await loadTMapGL();

        // Create map
        if (!containerRef.current) return;
        map = createMap(containerRef.current, {
          center: location,
          zoom: 16
        });

        // Add marker and info window
        addMarkerWithInfo(map, location, 'Location', `
          <div style="padding: 10px;">
            <h4>${address}</h4>
          </div>
        `);

        setLoading(false);
      } catch (err) {
        setLoading(false);
        if (err instanceof LBSError) {
          setError(err.getSolution());
        } else {
          setError('Failed to load map');
        }
      }
    }

    init();
    return () => { map?.destroy(); };
  }, [address]);

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="relative">
      {loading && <div className="loading">Loading...</div>}
      <div ref={containerRef} className="w-full h-80" />
    </div>
  );
}
```

## Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 110 | Unauthorized referer | Add domain to whitelist in console |
| 112 | Unauthorized IP | Configure authorized IP or use domain whitelist |
| 120 | WebService not enabled | Enable WebService in Key settings |
| 121 | Feature not authorized | Apply for permission in console |
| 122 | Quota exceeded | Request higher quota or retry later |
| 311 | Key disabled | Restore Key in console |

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/location.service.ts
import { createClient, loadTMapGL, createMap } from '../lib/tencent-lbs';

export class LocationService {
  private client = createClient();

  async geocodeAddress(address: string) {
    const result = await this.client.geocode(address);
    return result.result.location;
  }

  async searchNearbyPlaces(lat: number, lng: number, keyword: string) {
    return this.client.searchPlace(keyword, {
      boundary: `nearby(${lat},${lng},1000)`
    });
  }

  getStaticMapForAddress(address: string) {
    return this.client.getMapByAddress(address, {
      zoom: 16,
      size: { width: 600, height: 400 }
    });
  }
}
```

## Security Best Practices

1. **Configure domain whitelist**: Restrict API access to your domains
2. **Use backend proxy for sensitive operations**: Don't expose API key in client code for sensitive queries
3. **Implement rate limiting**: Prevent excessive API calls
4. **Cache geocoding results**: Reduce API usage for frequently queried addresses

## Troubleshooting

**Map Not Loading**
- Verify API Key is correct
- Check domain is in whitelist
- Ensure network connectivity

**Error 110: Unauthorized Referer**
- Add your domain to whitelist in LBS console
- Wait 1-2 minutes for changes to take effect

**Map Container Not Displaying**
- Container element must exist before creating map
- Container must have explicit width and height set

**Markers Not Showing**
- Verify coordinates format (latitude first, then longitude)
- Ensure coordinates are within valid range

## Resources

- **SDK Wrapper Source**: `lib/tencent-lbs.ts`
- **JavaScript GL API**: https://lbs.qq.com/webApi/javascriptGL/glGuide/glBasic
- **WebService API**: https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
- **Console**: https://lbs.qq.com/dev/console/application/mine
- **Key Configuration Guide**: https://lbs.qq.com/faq/serverFaq/webServiceKey
