---
name: add-event
description: Add, schedule, or tune street events in Vỉa Hè Online — touches STREET_EVENTS, SCHEDULED_EVENTS, SEASONAL_EVENTS in server/src/events.ts or hot-reloadable server/data/events.json. Use this skill whenever the user wants a new event, says "thêm sự kiện", "tạo event", "sự kiện đường phố", "lễ hội", "thời tiết", "chợ tết", "giờ cao điểm", or wants to change event spawn factors, boosted products, or seasonal decorations.
---

# Add a street or seasonal event

Events in Vỉa Hè Online create variety and liveliness on the street. They are data-driven: an event specifies when it runs and which rules it changes.

> [!IMPORTANT]
> **Golden Rule**: Events only ever **add opportunities**; none of them ever costs an absent player anything or causes penalties.

Events can be declared in two places:
1. **Code events** in `server/src/events.ts`: Core random street events, weekly events, and yearly seasonal milestones.
2. **Data events** in `server/data/events.json`: Dated events loaded at runtime without needing a server rebuild or client update.

## Step 1 — Choose the Event Kind

### 1. Random Street Event (`STREET_EVENTS`)
Triggers randomly per street during normal gameplay.
```ts
{
  id: 'heatwave',
  name: 'Đợt nắng nóng',
  seconds: 600,             // duration in seconds
  minFame: 50,              // optional: minimum street fame to trigger
  rules: { boost: ['iced_tea', 'popsicle', 'fresh_cane'] }
}
```

### 2. Scheduled Weekly Event (`SCHEDULED_EVENTS`)
Repeats every week at specific days and hours (Vietnam local time, UTC+7).
```ts
{
  id: 'night_market',
  name: 'Chợ đêm cuối tuần',
  weekday: 6,               // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
  hours: [18, 23],          // [startHour, endHour] (24h format)
  rules: { sidewalkFeePct: 5, spawnFactor: 1.3 }
}
```

### 3. Dated Seasonal Event (`SEASONAL_EVENTS` or `server/data/events.json`)
Runs between specific ISO 8601 start and end timestamps.
```ts
{
  id: 'mid_autumn',
  name: 'Tết Trung Thu',
  from: '2026-09-24T00:00:00+07:00',
  to: '2026-09-28T00:00:00+07:00',
  rules: {
    products: ['mooncake'],
    decorations: ['star_lantern'],
    gift: 'Tặng đèn lồng',
    spawnFactor: 1.2
  }
}
```

## Step 2 — Configure `EventRules`

| Field | Type | Description |
|---|---|---|
| `spawnFactor` | `number` | Multiplier for customer spawn rate (e.g. `1.5` = +50% traffic, `0.7` = -30% rain lull) |
| `boost` | `string[]` | Product IDs customers ask for twice as often (e.g. `['sweet_soup', 'iced_tea']`) |
| `sidewalkFeePct` | `number` | Temporary replacement for the standard 10% sidewalk fee (e.g. `5` for 5%) |
| `autoWater` | `boolean` | When true (like rain), every crop plot on the street is watered automatically |
| `tourists` | `boolean` | Triggers a bus of wealthy tourists who pay +50% above normal prices |
| `order` | `{ quantity, reward }` | Special street-wide quota; completing it pays bonus money |
| `products` | `string[]` | Seasonal products enabled in the shop for the duration |
| `decorations` | `string[]` | Seasonal decorations available for district lots |
| `gift` | `string` | Vietnamese action label for special holiday gifting |
| `community` | `{ target, steps, rewardPerStep }` | Cooperative goal where all players submit items for milestone rewards |

## Step 3 — Consistency Checks

1. **Product IDs**: Any ID referenced in `boost` or `products` must exist in `PRODUCTS` in `server/src/data.ts`.
2. **Decoration IDs**: Any ID referenced in `decorations` must exist in `DECORATIONS` in `server/src/data.ts`.
3. **Player-facing text**: `name` and `gift` must be natural Vietnamese.
4. **Timezones**: Always append `+07:00` to ISO timestamps for Vietnam time.

## Step 4 — Verify with Tests

Run the event and world test suite:
```bash
cd server && npm run test:world
```
Verify that events combine rules cleanly and seasonal calendars parse correctly.

## Step 5 — Sync Skills

```bash
node tools/sync-skills.mjs
```
