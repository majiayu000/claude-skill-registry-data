---
name: openhue
description: Control Philips Hue lights and scenes via the Hue Bridge API v2. Use when the user wants to control lights, rooms, scenes, brightness, color, or color temperature.
---

# OpenHue — Hue Bridge API v2 (GenosOS)

Control Philips Hue lights directly via the bridge API using `web_fetch`. No CLI needed.

## First Use — Discovery + Memory

On first use, discover bridges and save everything to memory:

1. **Discover bridges:** `web_fetch({ url: "https://discovery.meethue.com/" })`
2. **Get bridge IP** from discovery response
3. **Add bridge IP to trustedIPs:** `config set tools.webFetch.trustedIps ["ip1","ip2",...]`
4. **List rooms:** `web_fetch({ url: "https://{ip}/clip/v2/resource/room", headers: {"hue-application-key":"{key}"} })`
5. **Save everything as [MEMORY]:**
   - Bridge IDs, IPs, keys, zones
   - Room names + grouped_light IDs
   - Light names + IDs
   - Scene names + IDs

**After first use, you already know all IDs from memory — one single API call per action.**

## Bridge Keys

Bridge application keys are permanent credentials — store in config:
```
config set services.hue.bridges.{bridgeId}.key {appKey}
```

## IPs are Dynamic

Bridge IPs change — always discover first via `https://discovery.meethue.com/` or read from memory (update if changed). The trustedIPs config must include current bridge IPs.

## API Calls

All requests: `https://{bridgeIP}/clip/v2/resource/{endpoint}`

Header: `{ "hue-application-key": "{key}" }`

### Control a Room (grouped_light)

```
web_fetch({
  url: "https://{ip}/clip/v2/resource/grouped_light/{groupedLightId}",
  method: "PUT",
  headers: { "hue-application-key": "{key}", "Content-Type": "application/json" },
  body: '{"on":{"on":true},"color":{"xy":{"x":0.409,"y":0.518}}}'
})
```

### Control a Single Light

```
url: "https://{ip}/clip/v2/resource/light/{lightId}"
```

### Activate a Scene

```
web_fetch({
  url: "https://{ip}/clip/v2/resource/scene/{sceneId}",
  method: "PUT",
  headers: { "hue-application-key": "{key}", "Content-Type": "application/json" },
  body: '{"recall":{"action":"active"}}'
})
```

## Colors (CIE xy)

| Color | x | y |
|---|---|---|
| Red | 0.675 | 0.322 |
| Green | 0.409 | 0.518 |
| Blue | 0.167 | 0.04 |
| Purple | 0.3 | 0.15 |
| Orange | 0.57 | 0.41 |
| Pink | 0.4 | 0.2 |
| Warm white | 0.4573 | 0.41 |
| Cool white | 0.3127 | 0.3291 |

## Brightness + Temperature

```
body: '{"on":{"on":true},"dimming":{"brightness":50.0}}'
body: '{"on":{"on":true},"color_temperature":{"mirek":300}}'
```

Mirek range: 153 (cool) to 500 (warm)

## Presets

- **Bedtime:** brightness 20, mirek 450
- **Work:** brightness 100, mirek 250
- **Movie:** brightness 10
- **Romantic:** brightness 30, color pink/red

## Key Principle

**Memory over config.** After discovery, save all IDs in [MEMORY]. Next time you need to control lights, read from memory — one API call, no discovery needed. Only re-discover if IPs change or new devices are added.
