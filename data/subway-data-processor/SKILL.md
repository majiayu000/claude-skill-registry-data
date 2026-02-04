---
name: subway-data-processor
description: Process and transform Seoul subway data including station info, real-time arrivals, and timetables. Use when working with Seoul Open Data API responses or subway data normalization.
---

# Subway Data Processor Skill

## Purpose

Handle Seoul subway data transformations, API response parsing, and data normalization for LiveMetro.

## When to Use
- Parsing Seoul Open Data API responses
- Normalizing subway data (Korean ↔ English)
- Handling service disruption detection
- Processing timetable data
- Implementing caching logic

## Data Types

### TrainArrival
```typescript
interface TrainArrival {
  trainNo: string;
  stationName: string;
  direction: 'up' | 'down';
  arrivalTime: number;     // Seconds until arrival
  destinationName: string;
  lineId: string;
  status: 'NORMAL' | 'DELAYED' | 'SUSPENDED' | 'EMERGENCY';
  congestion?: 'RELAXED' | 'NORMAL' | 'CROWDED' | 'VERY_CROWDED';
  updatedAt: Date;
}
```

### Station
```typescript
interface Station {
  id: string;
  name: string;            // Korean name
  nameEn?: string;
  lineId: string;
  coordinates: { latitude: number; longitude: number };
  transfers?: string[];
}
```

## Seoul API Response Structure

### Real-Time Arrival
```json
{
  "realtimeArrivalList": [{
    "arvlMsg2": "2분후[1번째전]",   // Arrival message
    "btrainNo": "T1001",           // Train number
    "bstatnNm": "신도림",           // Destination
    "updnLine": "상행",             // Direction
    "trainLineNm": "2호선",         // Line name
    "statnNm": "강남역",            // Station name
    "recptnDt": "2025-12-28 09:30:15"
  }]
}
```

## Key Parsing Rules

### Arrival Time
| Message | Seconds |
|---------|---------|
| `2분후[1번째전]` | 120 |
| `곧 도착` | 30 |
| `전역 도착` | 60 |
| `[0]분후[...]` | 0 |

### Direction Normalization
| Korean | English |
|--------|---------|
| `상행` | `up` |
| `하행` | `down` |
| `내선` | `up` (circular) |
| `외선` | `down` (circular) |

### Line ID Mapping
| Korean | ID |
|--------|-----|
| `1호선` - `9호선` | `line1` - `line9` |
| `신분당선` | `shinbundang` |
| `경의중앙선` | `gyeongui` |
| `공항철도` | `airport` |
| `수인분당선` | `suin` |

## Service Disruption Keywords

| Severity | Keywords |
|----------|----------|
| **SEVERE** | 운행중단, 전면중단, 운행불가 |
| **MAJOR** | 장애, 고장, 사고, 탈선, 화재 |
| **MODERATE** | 지연, 혼잡, 서행 |

## Common Issues & Solutions

### Issue 1: Station Name Mismatch
**Problem**: "강남역" vs "강남"
**Solution**: Remove "역" suffix: `name.replace(/역$/, '').trim()`

### Issue 2: Circular Line Directions
**Problem**: Line 2 has "inner/outer" not "up/down"
**Solution**: Map "내선" → "up", "외선" → "down"

### Issue 3: Arrival Time "0분후"
**Problem**: `[0]분후` should be "곧 도착"
**Solution**: Treat 0 minutes as 30 seconds

### Issue 4: Multiple Stations Same Name
**Problem**: Same name on multiple lines
**Solution**: Always include `lineId` in queries

## Data Fetching Priority

```
1. AsyncStorage Cache (TTL: 30s)
   ↓ (cache miss or expired)
2. Seoul API (Primary)
   ↓ (API error)
3. Firebase (Fallback)
   ↓ (all failed)
4. Return empty array []
```

## Best Practices

1. **Always Normalize Data** - Convert Korean to English enums
2. **Handle Missing Data** - Use optional chaining and defaults
3. **Cache Aggressively** - Seoul API has implicit rate limits
4. **Validate Responses** - Check `RESULT.CODE === 'INFO-000'`
5. **Log Data Issues** - Track parsing failures for debugging
6. **Use Fuzzy Matching** - Station names vary across APIs

## Resources

- `src/services/api/seoulSubwayApi.ts` - Seoul API integration
- `src/services/data/dataManager.ts` - Multi-tier data fetching
- `src/models/train.ts` - TypeScript interfaces
- `src/utils/subwayMapData.ts` - Station metadata

## Reference Documentation

For complete implementations, see [references/parsing-examples.md](references/parsing-examples.md):
- Arrival time parsing functions
- Direction normalization
- Station name fuzzy matching
- Line ID extraction
- Data caching with TTL
- Multi-tier data fetching
- Timetable processing
- API error handling
