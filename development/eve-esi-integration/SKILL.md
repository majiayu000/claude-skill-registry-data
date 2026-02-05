---
name: eve-esi-integration
description: EVE Online ESI API integration skill for third-party development. Use when building EVE Online tools, apps, or games that need ESI endpoints, SSO authentication, image server assets, or SDE data. Triggers on EVE Online API work, ESI integration, EVE developer tools, ship renders, map data, character authentication, or EVE static data.
---

# EVE ESI Integration Skill

Comprehensive guide for integrating EVE Online's official APIs into third-party applications.

## Quick Reference

| Service | Base URL | Auth Required |
|---------|----------|---------------|
| ESI API | `https://esi.evetech.net/latest/` | Some endpoints |
| Image Server | `https://images.evetech.net/` | No |
| SSO | `https://login.eveonline.com/v2/oauth/` | Yes |

## Critical Rules (CCP Terms of Service)

1. **Always set User-Agent header** with app name + contact email
2. **Respect cache headers** - Don't poll faster than `Expires` header
3. **Error budget**: 100 errors per 60 seconds → HTTP 420 ban
4. **Never use ESI to discover** structures/characters (bannable)
5. **Rate limit**: Prefer consistent slow traffic over spiky bursts

## ESI Endpoints by Project Type

### For Map/Navigation Apps (EVE_Starmap)

Public endpoints (no auth):
```
GET /universe/systems/                    → All 8,285 system IDs
GET /universe/systems/{system_id}/        → Position, security, stargates
GET /universe/stargates/{stargate_id}/    → Destination system (for connections)
GET /universe/constellations/{id}/        → System groupings
GET /universe/regions/                    → Region list
GET /route/{origin}/{destination}/        → Shortest path (flag=shortest|secure|insecure)
GET /universe/system_jumps/               → Live jump activity (heatmaps)
GET /universe/system_kills/               → Live kill activity (heatmaps)
GET /incursions/                          → Active incursions
GET /sovereignty/map/                     → Sovereignty data
```

Auth endpoints (SSO required):
```
GET /characters/{id}/location/            → esi-location.read_location.v1
POST /ui/autopilot/waypoint/              → esi-ui.write_waypoint.v1
GET /characters/{id}/assets/              → esi-assets.read_assets.v1
```

### For Games/Visual Apps (EVE_Rebellion, EVE_Ships)

Image Server (no auth, no rate limit):
```
https://images.evetech.net/types/{type_id}/render?size=512    → Ship 3D render
https://images.evetech.net/types/{type_id}/icon?size=64       → Inventory icon
https://images.evetech.net/alliances/{id}/logo?size=128       → Alliance logo
https://images.evetech.net/corporations/{id}/logo?size=128    → Corp logo
https://images.evetech.net/characters/{id}/portrait?size=256  → Character portrait
```

Sizes: 32, 64, 128, 256, 512, 1024

Type info (for ship stats):
```
GET /universe/types/{type_id}/            → Name, description, dogma attributes
GET /universe/categories/{category_id}/   → Category info
GET /dogma/attributes/{attribute_id}/     → Attribute definitions
```

Common ship type IDs: Rifter=587, Tristan=593, Caracal=621, Drake=24690, Machariel=17738

### For Overview/UI Tools

Client-interaction endpoints (auth required):
```
POST /ui/openwindow/information/          → Open info window
POST /ui/openwindow/marketdetails/        → Open market window
POST /ui/autopilot/waypoint/              → Set waypoint
GET /characters/{id}/skills/              → Character skills
GET /characters/{id}/ship/                → Current ship
```

## Implementation Pattern

```python
import httpx
from datetime import datetime

class ESIClient:
    BASE = "https://esi.evetech.net/latest"
    
    def __init__(self, app_name: str, contact_email: str):
        self.headers = {
            "User-Agent": f"{app_name}/1.0 ({contact_email})",
            "Accept": "application/json"
        }
        self._cache = {}
    
    async def get(self, endpoint: str, params: dict = None) -> dict:
        cache_key = f"{endpoint}:{params}"
        
        # Check cache
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if datetime.now() < cached["expires"]:
                return cached["data"]
        
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.BASE}{endpoint}/",
                headers=self.headers,
                params=params
            )
            
            # Check error limit headers
            if "X-ESI-Error-Limit-Remain" in r.headers:
                remain = int(r.headers["X-ESI-Error-Limit-Remain"])
                if remain < 20:
                    print(f"⚠️ ESI error budget low: {remain} remaining")
            
            r.raise_for_status()
            
            # Cache based on Expires header
            if "Expires" in r.headers:
                expires = datetime.strptime(
                    r.headers["Expires"], 
                    "%a, %d %b %Y %H:%M:%S %Z"
                )
                self._cache[cache_key] = {
                    "data": r.json(),
                    "expires": expires
                }
            
            return r.json()
```

## SSO Authentication Flow

For authenticated endpoints, see `references/sso-flow.md`.

Quick summary:
1. Register app at https://developers.eveonline.com/applications
2. OAuth2 Authorization Code flow
3. Token refresh via `/v2/oauth/token`
4. Include `Authorization: Bearer {token}` header

## SDE (Static Data Export)

For offline/bulk data, use SDE instead of hitting ESI repeatedly:

- Official: https://developers.eveonline.com/resource/resources
- SQLite conversion: https://www.fuzzwork.co.uk/dump/
- Contains: All systems, stargates, types, attributes, coordinates

Recommended for:
- Initial map data load (8k+ systems)
- Ship/module attributes
- Industry recipes
- Anything that doesn't change between patches

## Compliance Checklist

Run `scripts/esi_compliance_check.py` on any project to verify:

- [ ] User-Agent header set with contact info
- [ ] Cache headers respected
- [ ] Error limit headers monitored
- [ ] No discovery abuse patterns
- [ ] Rate limiting implemented
- [ ] Versioned endpoints used (/latest/ or /v{n}/)

## Project-Specific Guidance

### EVE_Rebellion Integration Points

Current: Procedural audio, data-driven enemies, no ESI
Opportunities:
1. **Ship renders from Image Server** - Replace placeholder sprites
2. **Type attributes from ESI** - Real ship stats for enemy scaling
3. **zkillboard API** - Leaderboards, kill tracking

### EVE_Starmap Integration Points

Current: Architecture planned, needs implementation
Required:
1. **SDE import** - Bulk system/stargate data
2. **Live layers** - `/universe/system_kills/`, `/universe/system_jumps/`
3. **Route API** - `/route/{origin}/{destination}/`
4. **SSO for location** - Character position overlay

### EVE_Ships Integration Points

Current: SVG assets
Opportunities:
1. **Image Server automation** - Script to fetch all ship renders
2. **Type metadata** - Associate renders with ship stats
3. **Category organization** - Group by ship class from ESI

## File References

- `references/sso-flow.md` - Complete SSO authentication guide
- `references/endpoints-map.md` - All map/navigation endpoints
- `references/endpoints-character.md` - Character-scoped endpoints
- `references/image-server.md` - Image URL patterns and sizes
- `scripts/esi_compliance_check.py` - Project compliance scanner
- `scripts/fetch_ship_renders.py` - Bulk image downloader
- `scripts/sde_to_sqlite.py` - SDE conversion helper
