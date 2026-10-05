---
name: sunrise-sunset-integrator
description: Integrate sunrise, sunset, and twilight times API for geographic locations. Use this skill when the application needs daylight information, golden hour times for photography, astronomical twilight data, or location-based sun schedules. Triggers on requests for sunrise/sunset times, golden hour, twilight, or daylight information.
_meta_type: sdk
---

# Sunrise Sunset Times SDK Integration

## Scenarios

- **Location-based Sun Times**: Display sunrise/sunset times for any geographic location
- **Photography Planning**: Calculate golden hour and blue hour for optimal photography lighting
- **Outdoor Activity Planning**: Travel and outdoor apps needing daylight information
- **Astronomy Applications**: Twilight phases for stargazing and astronomical observations
- **Smart Home Automation**: Daylight-based lighting and automation triggers

**Not recommended for:**
- Applications without geographic location features
- Real-time sun position tracking (this API provides scheduled times only)
- Offline-only applications (requires internet connectivity)

## Setup

### 1. Install Dependencies

```bash
npm install axios
```

### 2. Copy SDK Wrapper

Read `lib/sunrise-sunset-times.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `rapidapi.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createSunTimesClient } from './lib/sunrise-sunset-times';
const client = createSunTimesClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
RAPIDAPI_KEY=your-rapidapi-key-here
```

**Obtaining Credentials** (if needed):
1. Visit [RapidAPI - Sunrise Sunset Times](https://rapidapi.com/Macca895/api/sunrise-sunset-times)
2. Sign up or log in to RapidAPI
3. Subscribe to the Sunrise Sunset Times API
4. Copy your RapidAPI Key from the dashboard

## Quick Start

### Basic Usage

```typescript
import { createSunTimesClient } from './lib/sunrise-sunset-times';

const client = createSunTimesClient();

// Get sun times for New York City
const sunTimes = await client.getSunTimes({
  latitude: 40.7128,
  longitude: -74.006,
  date: '2024-01-15',
  timeZoneId: 'America/New_York'
});

console.log(`Sunrise: ${sunTimes.sunrise}`);
console.log(`Sunset: ${sunTimes.sunset}`);
console.log(`Golden Hour Morning: ${sunTimes.goldenHourMorning}`);
```

### Photography Golden Hour

```typescript
// Get golden hour times for photography
const times = await client.getSunTimes({
  latitude: 48.8566,
  longitude: 2.3522,
  date: '2024-06-21',
  timeZoneId: 'Europe/Paris'
});

console.log('Morning Golden Hour:', times.goldenHourMorning);
console.log('Evening Golden Hour:', times.goldenHourEvening);
console.log('Morning Blue Hour:', times.blueHourMorning);
console.log('Evening Blue Hour:', times.blueHourEvening);
```

## Response Structure

```typescript
{
  sunrise: string;                    // Sun rises above horizon
  sunset: string;                     // Sun sets below horizon
  solarNoon: string;                  // Sun at highest point
  civilTwilightMorning: string;       // Morning civil twilight start
  civilTwilightEvening: string;       // Evening civil twilight end
  nauticalTwilightMorning: string;    // Morning nautical twilight start
  nauticalTwilightEvening: string;    // Evening nautical twilight end
  astronomicalTwilightMorning: string; // Morning astronomical twilight start
  astronomicalTwilightEvening: string; // Evening astronomical twilight end
  goldenHourMorning: string;          // Morning golden hour start
  goldenHourEvening: string;          // Evening golden hour start
  blueHourMorning: string;            // Morning blue hour start
  blueHourEvening: string;            // Evening blue hour start
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/sun-times.service.ts
import { createSunTimesClient, SunTimesResponse } from '../lib/sunrise-sunset-times';

export class SunTimesService {
  private client = createSunTimesClient();

  async getSunTimesForLocation(
    latitude: number,
    longitude: number,
    date?: string,
    timeZoneId?: string
  ): Promise<SunTimesResponse> {
    return this.client.getSunTimes({
      latitude,
      longitude,
      date: date || new Date().toISOString().split('T')[0],
      timeZoneId: timeZoneId || 'UTC'
    });
  }

  async getGoldenHours(latitude: number, longitude: number, date: string) {
    const times = await this.getSunTimesForLocation(latitude, longitude, date);
    return {
      morning: times.goldenHourMorning,
      evening: times.goldenHourEvening
    };
  }
}
```

### Express Route Example

```typescript
// src/routes/sun-times.routes.ts
import { Router } from 'express';
import { SunTimesService } from '../services/sun-times.service';

const router = Router();
const sunTimesService = new SunTimesService();

router.get('/sun-times', async (req, res) => {
  const { latitude, longitude, date, timeZoneId } = req.query;
  
  const times = await sunTimesService.getSunTimesForLocation(
    Number(latitude),
    Number(longitude),
    date as string,
    timeZoneId as string
  );
  
  res.json(times);
});

export default router;
```

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Use environment variables**: Store RapidAPI Key in `.env`
3. **Implement rate limiting**: Prevent excessive API calls
4. **Cache results**: Sun times don't change frequently, cache to reduce API usage

## Troubleshooting

**Authentication Errors (401/403)**
- Verify `RAPIDAPI_KEY` environment variable is set correctly if using custom configuration
- Check API subscription status on RapidAPI dashboard
- Ensure API key has not expired

**Invalid Coordinates**
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180
- Date format must be YYYY-MM-DD

**Timezone Issues**
- Use IANA timezone identifiers (e.g., `America/New_York`, `Asia/Shanghai`)
- Invalid timezone will return times in incorrect local time

**Network Errors**
- Check internet connectivity
- Verify firewall allows connections to RapidAPI or proxy endpoint

## Resources

- **SDK Wrapper Source**: `lib/sunrise-sunset-times.ts`
- **API Documentation**: [RapidAPI - Sunrise Sunset Times](https://rapidapi.com/Macca895/api/sunrise-sunset-times)
- **IANA Timezones**: [Wikipedia IANA Timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
