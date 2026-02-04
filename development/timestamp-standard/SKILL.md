---
name: timestamp-standard
description: Frontend-backend time data transmission standard, using millisecond timestamps for time points (timezone-independent); Duration/Period use ISO 8601 string format.
---

## Time Representation Standard

### Time Point (Instant)

| Type | Format | Description |
|------|--------|-------------|
| Time Point | number | Millisecond timestamp, UTC-based, timezone-independent |

**Core Principles**:
- All time points use **millisecond timestamps** (Unix Epoch Milliseconds)
- Timestamps are timezone-independent, frontend converts display based on user timezone
- Database storage, API transmission, frontend-backend interaction all use numeric type

### Duration

| Type | Format | Example | Description |
|------|--------|---------|-------------|
| Duration | string | `PT1H30M` | ISO 8601 duration format |

**Duration Format**: `PT[n]H[n]M[n]S`
- `PT1H` - 1 hour
- `PT30M` - 30 minutes
- `PT1H30M` - 1 hour 30 minutes
- `PT45S` - 45 seconds
- `PT1H30M45S` - 1 hour 30 minutes 45 seconds

### Period

| Type | Format | Example | Description |
|------|--------|---------|-------------|
| Period | string | `P1Y2M3D` | ISO 8601 date period format |

**Period Format**: `P[n]Y[n]M[n]D`
- `P1Y` - 1 year
- `P2M` - 2 months
- `P3D` - 3 days
- `P1Y2M3D` - 1 year 2 months 3 days

## Usage Examples

### Interface Definition

```typescript
interface Event {
  createdAt: number    // 1732608000000
  updatedAt: number    // 1732694400000
  duration: string     // "PT2H30M"
  validPeriod: string  // "P1Y"
}
```

### Frontend Conversion

```typescript
// timestamp to local display
const display = new Date(timestamp).toLocaleString()

// local time to timestamp
const timestamp = new Date().getTime()
```

### Backend Processing (Kotlin/Java)

```kotlin
// Instant and timestamp conversion
val instant = Instant.ofEpochMilli(timestamp)
val timestamp = instant.toEpochMilli()

// Duration parsing
val duration = Duration.parse("PT1H30M")

// Period parsing
val period = Period.parse("P1Y2M")
```

## Design Philosophy

- **Timestamps**: Numeric type for efficient transmission, no timezone ambiguity, cross-language compatible
- **Duration/Period**: ISO 8601 standard format, clear semantics, native parsing support
