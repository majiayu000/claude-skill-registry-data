---
name: "template-creation"
description: "Create recurring trip templates with mandatory GPS coordinates for 90%+ accuracy automatic matching"
---

# Skill 4: Template Creation (GPS Mandatory)

**Purpose:** Create recurring trip templates with mandatory GPS coordinates to enable high-confidence automatic matching (90%+ accuracy)

**Activation:** User says "create template", "save this route", "I make this trip every week", or after reconstruction when no matching template exists

---

## Overview

Template Creation allows users to define recurring routes that Car Log will automatically recognize in future checkpoint gaps. The key principle: **GPS coordinates are mandatory** (70% matching weight), while addresses are optional labels (30% weight). This ensures high-confidence matching even when addresses are ambiguous.

**Why GPS is Required:** "Košice" could mean 3 different fuel stations, but GPS 48.7164°N, 21.2611°E is exact - enabling 90%+ confidence matches within 100m radius.

---

## Workflow

### Step 1: Template Name & Purpose
Ask for a descriptive name and whether it's for business or personal use:
```
"What would you like to name this template?"
User: "Warehouse Run"

"Is this for business or personal use?"
User: "Business"

"What's the business purpose?"
User: "Weekly warehouse pickup and delivery"
```

### Step 2: Geocode START Location
Convert address to GPS coordinates using geocoding service:

**MCP Tool:** `geo-routing.geocode_address(address, country_hint="SK")`

**Handling Ambiguity:**
If multiple matches found (confidence <70%), present alternatives:
```
"Multiple locations found for 'Bratislava':

1. Bratislava City Center (48.1486°N, 17.1077°E)
   - Capital city center
   - Confidence: 75%

2. Bratislava-Petržalka (48.1234°N, 17.1100°E)
   - Residential district
   - Confidence: 60%

3. Bratislava Airport (48.1702°N, 17.2127°E)
   - M. R. Štefánik Airport
   - Confidence: 55%

Which location? (1/2/3) or provide more specific address:"
```

**User selects** → Use GPS coordinates from selected alternative

**GPS Validation:**
- Latitude: -90 to 90
- Longitude: -180 to 180
- Slovakia bounds: 47.7-49.6°N, 16.8-22.6°E (warn if outside but allow)

### Step 3: Geocode END Location
Repeat geocoding process for destination:

**MCP Tool:** `geo-routing.geocode_address(address, country_hint="SK")`

Same ambiguity handling as Step 2.

### Step 4: Calculate Route (Optional Enhancement)
Calculate route between coordinates to get accurate distance:

**MCP Tool:** `geo-routing.calculate_route(start_coords, end_coords, alternatives=true)`

**Show Route Alternatives:**
```
"3 routes found:

1. D1 highway: 395km (4.2 hrs) €12 tolls
2. E50: 410km (4.5 hrs) ← Recommended (most direct)
3. Local roads: 385km (5.8 hrs)

Which route do you typically take? (1/2/3 or 'skip')"
```

If user skips, template will have GPS but no distance (can be calculated during matching).

### Step 5: Collect Optional Enhancements
Gather additional data to improve matching confidence:

**Round Trip?**
```
"Is this a round trip? (yes/no)"
If yes → Distance doubled, system will create outbound + return trips
```

**Typical Days?**
```
"Which days do you typically make this trip?
(e.g., 'Monday, Thursday' or 'every day' or 'skip')"

Enables +5% confidence bonus when day-of-week matches
```

**Business Description?** (if purpose is business)
```
"What's the business purpose? (e.g., 'client meeting', 'delivery')"
Required for Slovak tax compliance if trips are business
```

### Step 6: Create Template with GPS Mandatory
Save template with validated GPS coordinates:

**MCP Tool:** `car-log-core.create_template(template_data)`

**Required Fields:**
- `name`: User-provided descriptive name
- `from_coords`: {lat, lng} - MANDATORY
- `to_coords`: {lat, lng} - MANDATORY
- `purpose`: "business" or "personal"

**Optional Fields:**
- `from_address`: Human-readable label
- `to_address`: Human-readable label
- `distance_km`: From route calculation
- `is_round_trip`: Boolean (default false)
- `typical_days`: Array of day names
- `business_description`: Required if purpose is business

### Step 7: Calculate & Show Template Completeness
Assess template quality to inform user:

**MCP Tool:** `trip-reconstructor.calculate_template_completeness(template_id)`

**Completeness Scoring:**
- Essential (GPS coords): 60%
- Distance: +10%
- Typical days: +10%
- Purpose: +10%
- Business description: +10%

**User Confirmation:**
```
"✅ Template created!

'Warehouse Run'
• From: 48.1486°N, 17.1077°E 'Bratislava Office'
• To: 48.7164°N, 21.2611°E 'Košice Warehouse'
• Distance: 820km (round trip)
• Days: Monday, Thursday
• Purpose: Business - Weekly warehouse pickup
• GPS coordinates saved ← 70% matching weight!
• Completeness: 95%

I'll match this template with 90%+ confidence on future trips!"
```

---

## GPS Mandatory Philosophy

**Why GPS is Required:**
- **Addresses are ambiguous:** "Košice" could mean city center, airport, or fuel station
- **GPS is precise:** 48.7164°N, 21.2611°E is exact, enables 90%+ confidence within 100m
- **70% matching weight:** GPS distance is primary signal, addresses are labels

**Matching Weights in Algorithm:**
- GPS coordinates: 70% of confidence score
- Address similarity: 30% of confidence score

**User Messaging:**
Always emphasize GPS benefits:
```
"✓ GPS coordinates saved - I can match future trips within 100m accuracy!"
"This enables 90%+ confidence automatic matching"
```

**Fallback: Manual GPS Entry**
If geocoding fails or user has coordinates directly:
```
User: "GPS is 48.2000, 17.3000"
Claude: "✓ GPS coordinates received: 48.2000°N, 17.3000°E"
[Optionally reverse-geocode for friendly label]
```

---

## Related Skills

**Triggered from:**
- Skill 3 (Trip Reconstruction) → When no matching template found
- Manual user request → "create template", "save route"

**Enables:**
- Skill 3 (Trip Reconstruction) → High-confidence matching for future gaps

---

## Success Criteria

- GPS coordinates mandatory (validates before saving)
- Address ambiguity resolved with user selection
- Route calculation shows alternatives with distance, time, tolls
- Optional fields enhance matching (days, purpose, description)
- Manual GPS entry supported (fallback if geocoding fails)
- Template completeness score calculated and shown
- Clear user messaging about GPS benefits (70% weight)
- Round trip doubles distance automatically
- Business description required if purpose is business
- Slovakia bounds validation (warn if outside, allow international)

---

## Testing Scenarios

**High Confidence Geocoding:**
- Input: "Hlavná 45, Bratislava"
- Expected: Single match, 95% confidence, GPS extracted

**Ambiguous Geocoding:**
- Input: "Košice" (city name only)
- Expected: Multiple alternatives shown, user selects, GPS confirmed

**GPS-Only Template:**
- Input: Manual GPS coordinates (no address)
- Expected: Template created with GPS, optional reverse geocoding for label

**Minimal Template:**
- Input: GPS only, skip all enhancements
- Expected: Template created with 60% completeness, recommendation to add optional fields

**Complete Template:**
- Input: GPS + distance + days + purpose + description
- Expected: 95%+ completeness, confirmation with full details

---

**Implementation Status:** Specification complete, implementation pending
**Estimated Effort:** 3 hours
**Dependencies:** geo-routing (geocoding, routing), car-log-core (template storage), trip-reconstructor (completeness calculation)
