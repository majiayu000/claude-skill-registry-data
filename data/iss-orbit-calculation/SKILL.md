---
name: iss-orbit-calculation
description: Calculate ISS orbital positions, propagate TLEs, and validate satellite tracking accuracy. Use when working with satellite.js, TLE data, orbital mechanics, position calculations, or SGP4 propagation.
allowed-tools: Read, Bash, Write, Grep
---

# ISS Orbit Calculation Skill

This skill provides comprehensive capabilities for satellite orbital calculations, TLE propagation, and position validation specific to the International Space Station.

## When to Use This Skill

Automatically invoke this skill when:
- Implementing satellite.js integration
- Working with Two-Line Element (TLE) data
- Calculating ISS positions from orbital parameters
- Converting between coordinate systems (ECI, geodetic)
- Validating orbital calculations
- Implementing pass predictions
- Debugging position accuracy issues

## Core Competencies

### 1. TLE Data Management

**TLE Format Understanding:**
```
Line 0: ISS (ZARYA)
Line 1: 1 25544U 98067A   24001.50000000  .00016717  00000-0  10270-3 0  9005
Line 2: 2 25544  51.6400 208.9163 0006317  69.9862  25.2906 15.54225995 00001
```

**Line 1 breakdown:**
- Position 1: Line number (1)
- Position 3-7: Satellite catalog number (25544 for ISS)
- Position 10-17: Epoch year and day
- Position 34-43: First derivative of mean motion
- Position 54-61: Drag term
- Position 63-68: Element set number
- Position 69: Checksum

**Line 2 breakdown:**
- Position 1: Line number (2)
- Position 3-7: Satellite catalog number
- Position 9-16: Inclination (degrees)
- Position 18-25: Right ascension of ascending node (degrees)
- Position 27-33: Eccentricity
- Position 35-42: Argument of perigee (degrees)
- Position 44-51: Mean anomaly (degrees)
- Position 53-63: Mean motion (revolutions per day)
- Position 64-68: Revolution number at epoch
- Position 69: Checksum

### 2. Implementation Pattern

```typescript
import * as satellite from 'satellite.js';

class ISSOrbitCalculator {
  private satrec: satellite.SatRec | null = null;
  private tleEpoch: Date | null = null;
  
  /**
   * Initialize with TLE data
   * @param line1 - TLE line 1
   * @param line2 - TLE line 2
   */
  initializeTLE(line1: string, line2: string): void {
    // Validate TLE format
    if (!this.validateTLEFormat(line1, line2)) {
      throw new Error('Invalid TLE format');
    }
    
    // Parse TLE
    this.satrec = satellite.twoline2satrec(line1, line2);
    
    // Check for parsing errors
    if (this.satrec.error) {
      throw new Error(`TLE parsing error: ${this.satrec.error}`);
    }
    
    // Extract epoch
    this.tleEpoch = this.extractEpoch(line1);
    
    console.log('TLE initialized:', {
      epoch: this.tleEpoch.toISOString(),
      inclination: this.satrec.inclo * (180 / Math.PI),
      eccentricity: this.satrec.ecco
    });
  }
  
  /**
   * Calculate position at current time
   */
  getCurrentPosition(): ISSPosition {
    return this.getPositionAt(new Date());
  }
  
  /**
   * Calculate position at specific time
   */
  getPositionAt(date: Date): ISSPosition {
    if (!this.satrec) {
      throw new Error('TLE not initialized');
    }
    
    // Propagate orbit to specified time
    const positionAndVelocity = satellite.propagate(this.satrec, date);
    
    // Check for propagation errors
    if ((positionAndVelocity.position as any) === false) {
      throw new Error('Propagation error - position calculation failed');
    }
    
    const positionEci = positionAndVelocity.position as satellite.EciVec3<number>;
    const velocityEci = positionAndVelocity.velocity as satellite.EciVec3<number>;
    
    // Convert ECI to geodetic coordinates
    const gmst = satellite.gstime(date);
    const positionGd = satellite.eciToGeodetic(positionEci, gmst);
    
    // Calculate velocity magnitude
    const velocity = Math.sqrt(
      velocityEci.x ** 2 + velocityEci.y ** 2 + velocityEci.z ** 2
    );
    
    const position: ISSPosition = {
      latitude: satellite.degreesLat(positionGd.latitude),
      longitude: satellite.degreesLong(positionGd.longitude),
      altitude: positionGd.height, // km
      velocity: velocity, // km/s
      timestamp: date.getTime(),
      visibility: this.calculateVisibility(positionEci, date)
    };
    
    // Validate position
    this.validatePosition(position);
    
    return position;
  }
  
  /**
   * Generate orbital path
   */
  generatePath(startTime: Date, durationMinutes: number, stepSeconds: number = 10): ISSPosition[] {
    const path: ISSPosition[] = [];
    const endTime = new Date(startTime.getTime() + durationMinutes * 60 * 1000);
    
    for (let time = startTime.getTime(); time <= endTime.getTime(); time += stepSeconds * 1000) {
      const position = this.getPositionAt(new Date(time));
      path.push(position);
    }
    
    return path;
  }
  
  private validateTLEFormat(line1: string, line2: string): boolean {
    // Check line lengths
    if (line1.length !== 69 || line2.length !== 69) {
      return false;
    }
    
    // Check line numbers
    if (line1[0] !== '1' || line2[0] !== '2') {
      return false;
    }
    
    // Verify checksums
    return this.verifyChecksum(line1) && this.verifyChecksum(line2);
  }
  
  private verifyChecksum(line: string): boolean {
    const data = line.substring(0, 68);
    const checksum = parseInt(line[68]);
    
    let sum = 0;
    for (const char of data) {
      if (char >= '0' && char <= '9') {
        sum += parseInt(char);
      } else if (char === '-') {
        sum += 1;
      }
    }
    
    return (sum % 10) === checksum;
  }
  
  private extractEpoch(line1: string): Date {
    const yearDay = line1.substring(18, 32);
    const year = parseInt(yearDay.substring(0, 2));
    const fullYear = year < 57 ? 2000 + year : 1900 + year;
    const dayOfYear = parseFloat(yearDay.substring(2));
    
    const epoch = new Date(fullYear, 0, 1);
    epoch.setDate(dayOfYear);
    
    return epoch;
  }
  
  private validatePosition(position: ISSPosition): void {
    // ISS altitude range: 370-460 km typically
    if (position.altitude < 300 || position.altitude > 500) {
      console.warn(`Altitude outside typical range: ${position.altitude.toFixed(2)} km`);
    }
    
    // ISS velocity: ~7.66 km/s
    if (position.velocity < 7.4 || position.velocity > 7.9) {
      console.warn(`Velocity outside typical range: ${position.velocity.toFixed(3)} km/s`);
    }
    
    // Coordinate bounds
    if (position.latitude < -90 || position.latitude > 90) {
      throw new Error(`Invalid latitude: ${position.latitude}`);
    }
    
    if (position.longitude < -180 || position.longitude > 180) {
      throw new Error(`Invalid longitude: ${position.longitude}`);
    }
  }
  
  private calculateVisibility(positionEci: satellite.EciVec3<number>, date: Date): 'daylight' | 'eclipse' {
    // Simplified visibility calculation
    // ISS is in daylight if sun-ISS vector and earth-ISS vector
    // have positive dot product
    
    const sunPosition = this.getSunPositionECI(date);
    
    // Vector from ISS to Sun
    const toSun = {
      x: sunPosition.x - positionEci.x,
      y: sunPosition.y - positionEci.y,
      z: sunPosition.z - positionEci.z
    };
    
    // Dot product with position vector
    const dotProduct = 
      toSun.x * positionEci.x +
      toSun.y * positionEci.y +
      toSun.z * positionEci.z;
    
    return dotProduct > 0 ? 'daylight' : 'eclipse';
  }
  
  private getSunPositionECI(date: Date): satellite.EciVec3<number> {
    // Simplified sun position (good enough for ISS visibility)
    const T = (this.julianDate(date) - 2451545.0) / 36525.0;
    const L = 280.460 + 36000.771 * T; // Mean longitude
    const M = 357.5291092 + 35999.05034 * T; // Mean anomaly
    
    const lambda = (L + 1.915 * Math.sin(M * Math.PI / 180)) * Math.PI / 180;
    const epsilon = 23.439 * Math.PI / 180; // Obliquity
    
    const AU = 149597870.7; // km
    
    return {
      x: AU * Math.cos(lambda),
      y: AU * Math.cos(epsilon) * Math.sin(lambda),
      z: AU * Math.sin(epsilon) * Math.sin(lambda)
    };
  }
  
  private julianDate(date: Date): number {
    return (date.getTime() / 86400000.0) + 2440587.5;
  }
  
  /**
   * Check TLE age (should refresh if > 12 hours old)
   */
  getTLEAge(): number {
    if (!this.tleEpoch) return Infinity;
    return (Date.now() - this.tleEpoch.getTime()) / (1000 * 60 * 60);
  }
}
```

### 3. Coordinate System Conversions

**ECI (Earth-Centered Inertial) to Geodetic:**
- ECI: Fixed coordinate system with origin at Earth's center
- Geodetic: Latitude, longitude, altitude on Earth's surface
- Requires GMST (Greenwich Mean Sidereal Time) for conversion
- GMST accounts for Earth's rotation

```typescript
// Example conversion
const gmst = satellite.gstime(new Date());
const positionGd = satellite.eciToGeodetic(positionEci, gmst);

const latitude = satellite.degreesLat(positionGd.latitude);
const longitude = satellite.degreesLong(positionGd.longitude);
const altitude = positionGd.height; // km
```

### 4. Accuracy Validation

Always validate calculated positions against known data:

```typescript
async function validateAccuracy(calculated: ISSPosition): Promise<number> {
  // Fetch reference position from API
  const response = await fetch('https://api.wheretheiss.at/v1/satellites/25544');
  const reference = await response.json();
  
  // Calculate distance error using Haversine formula
  const R = 6371; // Earth radius (km)
  const dLat = (reference.latitude - calculated.latitude) * Math.PI / 180;
  const dLon = (reference.longitude - calculated.longitude) * Math.PI / 180;
  
  const a = 
    Math.sin(dLat / 2) ** 2 +
    Math.cos(calculated.latitude * Math.PI / 180) *
    Math.cos(reference.latitude * Math.PI / 180) *
    Math.sin(dLon / 2) ** 2;
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  
  console.log('Position accuracy:', {
    calculated: [calculated.latitude, calculated.longitude],
    reference: [reference.latitude, reference.longitude],
    error: distance.toFixed(2) + ' km'
  });
  
  // Error should be < 50km for good TLE
  return distance;
}
```

## Technical Standards

### TLE Freshness
- **Optimal**: < 3 days old
- **Acceptable**: < 7 days old  
- **Warning**: 7-14 days old
- **Critical**: > 14 days old

### ISS Orbital Parameters
- **Altitude**: 370-460 km (typically ~420 km)
- **Velocity**: 7.4-7.9 km/s (typically ~7.66 km/s)
- **Inclination**: ~51.6 degrees
- **Orbital period**: ~90 minutes
- **Eccentricity**: < 0.01 (nearly circular)

### Position Validation Thresholds
- **Latitude**: Must be [-90, 90]
- **Longitude**: Must be [-180, 180]
- **Altitude**: Warn if outside [300, 500] km
- **Velocity**: Warn if outside [7.4, 7.9] km/s
- **Position error**: < 50 km vs API is good

## Common Issues and Solutions

### Issue: Stale TLE Data
**Symptom**: Positions drift from reality
**Solution**: Implement automatic TLE refresh every 12 hours
```typescript
setInterval(async () => {
  const tle = await fetchFreshTLE();
  calculator.initializeTLE(tle.line1, tle.line2);
}, 12 * 60 * 60 * 1000);
```

### Issue: Propagation Errors
**Symptom**: position returns false or NaN
**Solution**: Always check error codes and handle gracefully
```typescript
const result = satellite.propagate(satrec, date);
if ((result.position as any) === false) {
  // Fall back to API or use last known position
  console.error('Propagation failed, using fallback');
}
```

### Issue: Coordinate Conversion Errors
**Symptom**: Longitude jumps or invalid values
**Solution**: Ensure GMST is calculated correctly
```typescript
// Always use satellite.gstime, not custom calculation
const gmst = satellite.gstime(date);
const positionGd = satellite.eciToGeodetic(positionEci, gmst);
```

### Issue: Performance on Mobile
**Symptom**: Calculations slow on mobile devices
**Solution**: Throttle calculations and cache results
```typescript
// Calculate once per second, interpolate for 60 FPS
setInterval(() => {
  const position = calculator.getCurrentPosition();
  positionCache = position;
}, 1000);

// Use cached position for rendering
requestAnimationFrame(() => {
  renderPosition(positionCache);
});
```

## Testing Requirements

Every orbital calculation implementation should include:

1. **TLE validation tests**: Format, checksum, freshness
2. **Position calculation tests**: Valid coordinates, ranges
3. **Accuracy validation tests**: Compare against API
4. **Edge case tests**: Date boundaries, orbit wrapping
5. **Performance tests**: Calculation time < 10ms
6. **Error handling tests**: Invalid TLE, propagation failures

## Integration Checklist

- [ ] TLE fetching from wheretheiss.at API
- [ ] TLE validation (format, checksum, age)
- [ ] satellite.js integration
- [ ] Position calculation with error handling
- [ ] Coordinate conversion (ECI → geodetic)
- [ ] Position validation against thresholds
- [ ] Accuracy validation against API
- [ ] Periodic TLE refresh (every 12 hours)
- [ ] Visibility calculation (daylight/eclipse)
- [ ] Comprehensive test coverage
- [ ] Performance optimization
- [ ] Error logging and monitoring

## Common Troubleshooting Issues

### Issue 1: Race Condition - TLE Not Initialized

**Symptom**: Error "TLE not initialized, cannot calculate position" appears when SSE stream starts sending position updates.

**Root Cause**: SSE connection establishes and starts emitting position events before TLE data has been fetched and initialized in the orbit calculator service.

**Impact**:
- Position calculations fail
- Marker doesn't update
- Error floods console

**Solution**: Make ngOnInit async and await TLE initialization before starting SSE connection.

```typescript
// app.component.ts - INCORRECT (race condition)
ngOnInit(): void {
  // TLE fetch is async, may not complete before SSE starts
  this.orbitCalculator.initializeTLE();

  // SSE starts immediately, calculator not ready!
  this.sseClient.connect();
}

// app.component.ts - CORRECT (awaits initialization)
async ngOnInit(): Promise<void> {
  try {
    // Wait for TLE to be fetched and initialized
    await this.orbitCalculator.initializeTLE();
    console.log('✓ TLE initialized successfully');

    // Only start SSE after calculator is ready
    this.sseClient.connect();
    console.log('✓ SSE connection established');
  } catch (error) {
    console.error('Failed to initialize ISS tracker:', error);
    this.errorMessage = 'Failed to fetch satellite data. Please refresh.';
  }
}
```

**OrbitCalculatorService Pattern**:
```typescript
export class OrbitCalculatorService {
  private satrec: satellite.SatRec | null = null;
  private tleInitialized = false;

  async initializeTLE(): Promise<void> {
    try {
      // Fetch TLE from backend
      const response = await fetch('http://localhost:8000/api/iss/tle');
      if (!response.ok) {
        throw new Error(`TLE fetch failed: ${response.status}`);
      }

      const data = await response.json();

      // Validate and parse
      this.satrec = satellite.twoline2satrec(data.tle.line1, data.tle.line2);
      if (this.satrec.error) {
        throw new Error(`TLE parsing error: ${this.satrec.error}`);
      }

      this.tleInitialized = true;
      console.log('TLE initialized:', data.tle.epoch);

    } catch (error) {
      console.error('TLE initialization failed:', error);
      throw error; // Propagate to caller
    }
  }

  getCurrentPosition(): ISSPosition {
    if (!this.tleInitialized || !this.satrec) {
      throw new Error('TLE not initialized, cannot calculate position');
    }

    // Calculate position...
  }
}
```

### Issue 2: TypeScript Null Check Errors

**Symptom**: Compilation errors like `'positionAndVelocity' is possibly 'null'`

**Root Cause**: satellite.js `propagate()` can return null or `{position: false}` on errors, but TypeScript doesn't know this.

**Solution**: Add proper null/error checks:

```typescript
const positionAndVelocity = satellite.propagate(this.satrec, date);

// Check for null return
if (!positionAndVelocity) {
  throw new Error('Propagation returned null');
}

// Check for false position (propagation error)
if ((positionAndVelocity.position as any) === false) {
  throw new Error('Propagation error - position calculation failed');
}

// Now safe to use
const posECI = positionAndVelocity.position as satellite.EciVec3<number>;
const velECI = positionAndVelocity.velocity as satellite.EciVec3<number>;
```

### Issue 3: Incorrect Position Calculation

**Symptom**: Calculated positions don't match API reference positions (error > 50km)

**Common Causes**:
1. **Stale TLE data**: TLE older than 7 days
2. **Wrong epoch**: Using current time instead of TLE epoch for GMST
3. **Coordinate conversion error**: Missing or incorrect ECI → geodetic conversion

**Debugging Checklist**:
```typescript
// 1. Check TLE age
const tleAge = Date.now() - this.tleEpoch.getTime();
const ageHours = tleAge / (1000 * 60 * 60);
console.log(`TLE age: ${ageHours.toFixed(1)} hours`);
if (ageHours > 168) { // 7 days
  console.warn('TLE data is stale, accuracy degraded');
}

// 2. Verify GMST calculation
const gmst = satellite.gstime(date);
console.log('GMST:', gmst);

// 3. Check ECI coordinates before conversion
console.log('ECI position:', posECI);
console.log('ECI velocity:', velECI);

// 4. Verify geodetic conversion
const gdPos = satellite.eciToGeodetic(posECI, gmst);
console.log('Geodetic:', {
  lat: satellite.degreesLat(gdPos.latitude),
  lon: satellite.degreesLong(gdPos.longitude),
  alt: gdPos.height
});

// 5. Validate against expected ranges
if (gdPos.height < 370 || gdPos.height > 460) {
  console.error('Altitude out of range:', gdPos.height);
}
```

### Issue 4: Performance Degradation

**Symptom**: Position calculation taking >50ms, causing frame drops

**Common Causes**:
1. Re-initializing TLE on every calculation
2. Creating new Date objects unnecessarily
3. Not caching GMST calculations

**Optimization Pattern**:
```typescript
class OptimizedOrbitCalculator {
  private satrec: satellite.SatRec;
  private lastCalcTime = 0;
  private cachedPosition: ISSPosition | null = null;
  private readonly CACHE_DURATION = 100; // ms

  getCurrentPosition(): ISSPosition {
    const now = Date.now();

    // Return cached result if within 100ms
    if (this.cachedPosition && (now - this.lastCalcTime) < this.CACHE_DURATION) {
      return this.cachedPosition;
    }

    // Calculate new position
    const date = new Date(now);
    const position = this.calculatePosition(date);

    // Cache result
    this.cachedPosition = position;
    this.lastCalcTime = now;

    return position;
  }
}
```

### Issue 5: TLE Checksum Validation Failures

**Symptom**: Valid TLE data rejected with "Invalid checksum"

**Cause**: Checksum calculation doesn't account for special characters correctly

**Correct Checksum Implementation**:
```typescript
private calculateTLEChecksum(line: string): number {
  // Use only first 68 characters (position 69 is checksum)
  const data = line.substring(0, 68);
  let checksum = 0;

  for (const char of data) {
    if (char >= '0' && char <= '9') {
      checksum += parseInt(char, 10);
    } else if (char === '-') {
      checksum += 1; // Minus sign counts as 1
    }
    // Letters, spaces, periods, + signs don't count
  }

  return checksum % 10;
}

private validateTLEChecksum(line: string): boolean {
  const expectedChecksum = parseInt(line.charAt(68), 10);
  const calculatedChecksum = this.calculateTLEChecksum(line);

  if (calculatedChecksum !== expectedChecksum) {
    console.error('TLE checksum mismatch:', {
      expected: expectedChecksum,
      calculated: calculatedChecksum,
      line: line
    });
    return false;
  }

  return true;
}
```

## Resources

- satellite.js documentation: https://github.com/shashwatak/satellite-js
- TLE format specification: https://celestrak.org/NORAD/documentation/tle-fmt.php
- SGP4 propagation model: https://celestrak.org/publications/AIAA/2006-6753/
- wheretheiss.at API: https://wheretheiss.at/w/developer
