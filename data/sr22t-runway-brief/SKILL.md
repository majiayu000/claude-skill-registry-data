---
name: sr22t-runway-brief
description: Calculate takeoff and landing performance for Cirrus SR22T at any runway. Input weather (winds, temp, altimeter) and runway data (elevation, heading, length) to get performance calculations, approach speeds, safety margins, and passenger briefing scripts. Use when evaluating runway feasibility, checking hot day performance, or analyzing unfamiliar airports.
---

# SR22T Runway Brief Skill

## ⚠️ CRITICAL: MANDATORY DATA USAGE - READ FIRST

**SAFETY-CRITICAL REQUIREMENT:** This skill contains actual Cirrus SR22T POH performance data. Using incorrect data could result in runway overruns, accidents, or fatalities.

### BEFORE Writing ANY Code:

**STEP 1: Read the reference files FIRST**
```bash
cat references/sr22t_performance_data.py
cat references/calculation_functions.py
```

**STEP 2: Import and use ONLY the provided data**
```python
import sys
sys.path.insert(0, 'references')
from sr22t_performance_data import EMBEDDED_SR22T_PERFORMANCE
from calculation_functions import (
    calculate_pressure_altitude,
    calculate_isa_temperature,
    calculate_density_altitude,
    calculate_wind_components,
    interpolate_performance
)
```

**STEP 3: Extract performance tables - DO NOT create your own**
```python
takeoff_data = EMBEDDED_SR22T_PERFORMANCE["performance_data"]["takeoff_distance"]["conditions"]
landing_data = EMBEDDED_SR22T_PERFORMANCE["performance_data"]["landing_distance"]["conditions"]
v_speeds = EMBEDDED_SR22T_PERFORMANCE["v_speeds"]["approach_speeds"]
```

### ❌ PROHIBITED:
- **NEVER create performance data from memory**
- **NEVER simplify or approximate POH tables**
- **NEVER skip reading the reference files**
- **NEVER use simple linear interpolation (must be bilinear on PA AND temperature)**

### ✅ VALIDATION:
- [ ] Used data from EMBEDDED_SR22T_PERFORMANCE
- [ ] Used bilinear interpolation on PA AND temperature
- [ ] Rounded to nearest 50 ft
- [ ] Results are conservative

**If you cannot access the reference files, STOP and inform the user. Do not proceed with estimated data.**

---

## Required Inputs

1. Runway elevation (ft MSL), 2. Temperature (°C), 3. Altimeter (inHg), 4. Wind direction (°mag), 5. Wind speed (kt), 6. Runway heading (°mag), 7. Runway length (ft)

**Optional:** Wind gusts, Operation type (takeoff/landing/both)

---

## Workflow

### Step 0: Determine Operation Type

**CRITICAL: The skill MUST analyze the user's request to determine operation type.**

**Automatic Detection (Priority 1):**
Scan the user's request for explicit keywords:
- **Takeoff only**: "departing", "takeoff", "departure", "leaving from"
- **Landing only**: "arriving", "landing", "arrival", "coming into"
- **Both operations**: If NEITHER takeoff NOR landing keywords detected, OR if BOTH detected

**Examples:**
- "I'm departing KBZN runway 30" → Takeoff brief only
- "Give me a landing brief for KSUN runway 09" → Landing brief only
- "Analyze KBZN runway 30" → Both operations (no specific operation mentioned)
- "I need performance data for KASE runway 15" → Both operations (ambiguous)

**Default Behavior:**
- **If ambiguous or unspecified → ALWAYS calculate BOTH operations**
- Never ask the user to clarify operation type
- If in doubt, do both - it's better to provide complete information

**Set Operation Mode:**
```python
# Detect from user input
if "depart" in user_input.lower() or "takeoff" in user_input.lower():
    operation = "takeoff"
elif "arriv" in user_input.lower() or "landing" in user_input.lower():
    operation = "landing"
else:
    operation = "both"  # DEFAULT: Do both when ambiguous
```

Proceed with selected workflows based on detected operation type.

---

### Step 1: Gather and Validate Inputs

**Automatic Airport Data Lookup:**
If the user provides an airport code but is missing elevation or runway length:
1. Use web_search to find airport data
2. Query format: "[AIRPORT_CODE] airport elevation runways"
3. Extract from authoritative sources (Wikipedia, airnav.com, skyvector.com, airport-data.com)
4. Data to retrieve:
   - **Field elevation** (use for all runways - runway-specific elevation differences are negligible for performance)
   - **All runway identifications and lengths**
5. If multiple sources differ on runway length, use the most conservative (shortest) length
6. If search fails or returns unclear results: prompt user for missing data

**Do not let web search failure block the briefing** - simply request the missing data from the user.

**Never assume or estimate critical data** - always get confirmed elevation and runway lengths.

**Prompt format:**
```
RUNWAY INFORMATION:
- Runway ID: [e.g., "09"]
- Airport Code: [e.g., "KBZN"] (optional, enables automatic lookup)
- Airport Name: [e.g., "Sun Valley"] (optional)
- Elevation: [feet MSL] (will search if not provided)
- Runway Heading: [degrees magnetic]
- Runway Length: [feet] (will search if not provided)

CURRENT WEATHER:
- Temperature: [°C]
- Altimeter: [inHg]
- Wind Direction: [degrees magnetic]
- Wind Speed: [knots]
- Wind Gusts: [knots or "none"]
```

**Validation:**
- Elevation: 0-14,000 ft (warn if >14,000)
- Temperature: -40 to +50°C (confirm if unusual)
- Altimeter: 28.00-31.00 inHg (warn if outside)
- Headings: 0-360°
- Wind speed: 0-60 kt (flag if >30 kt)
- Runway length: 1,000-15,000 ft (flag if <2,000 ft)

If validation fails, request correction before proceeding.

---

### Step 2: Calculate Common Performance Data

Execute using Python code in `references/calculation_functions.py`:

**Pressure Altitude:**
```python
pressure_altitude = field_elevation + (29.92 - altimeter) * 1000
pressure_altitude_rounded = round(pressure_altitude / 10) * 10
```

**ISA Temperature:**
```python
isa_temp = 15 - (2 * (pressure_altitude / 1000))
```

**Density Altitude:**
```python
density_altitude = pressure_altitude + (120 * (actual_temp - isa_temp))
density_altitude_rounded = round(density_altitude / 50) * 50
```

**Wind Components:**
```python
# Use the imported function - DO NOT rewrite this calculation
# Signature: calculate_wind_components(wind_dir_mag, wind_speed_kt, runway_heading_mag)
wind_result = calculate_wind_components(wind_direction, wind_speed, runway_heading)

headwind = wind_result["headwind_kt"]  # Positive = headwind, Negative = tailwind
crosswind = wind_result["crosswind_kt"]  # Always positive
wind_type = wind_result["wind_type"]  # "headwind" or "tailwind"
```

**Density Altitude Impact Assessment:**
- <2,000 ft: "Excellent performance"
- 2,000-5,000 ft: "Good performance, minor reduction"
- 5,000-8,000 ft: "Noticeable performance reduction"
- 8,000-10,000 ft: "Significant reduction - caution"
- >10,000 ft: "Severe degradation - high risk"

**Display summary before proceeding to operations.**

---

### Step 3A: Takeoff Brief (if selected)

#### 3A.1: Interpolate Takeoff Distance

Use the imported `interpolate_performance()` function - DO NOT rewrite this:

```python
# Get takeoff data
takeoff_data = EMBEDDED_SR22T_PERFORMANCE["performance_data"]["takeoff_distance"]["conditions"]

# Use the interpolate_performance function (handles bilinear interpolation automatically)
takeoff_result = interpolate_performance(
    takeoff_data,
    pressure_altitude,
    actual_temp,
    ['ground_roll_ft', 'total_distance_ft']
)

takeoff_ground_roll = takeoff_result['ground_roll_ft']  # Already rounded to nearest 50 ft
takeoff_total_distance = takeoff_result['total_distance_ft']  # Already rounded
takeoff_margin = runway_length - takeoff_total_distance
```

#### 3A.2: Calculate Climb Gradients

Use the imported `interpolate_performance()` function - DO NOT rewrite this:

```python
# Get climb gradient data
climb_91_data = EMBEDDED_SR22T_PERFORMANCE["performance_data"]["takeoff_climb_gradient_91"]["conditions"]
climb_120_data = EMBEDDED_SR22T_PERFORMANCE["performance_data"]["enroute_climb_gradient_120"]["conditions"]

# Use interpolate_performance (handles bilinear interpolation and rounding automatically)
# Note: Pass None for value_keys because climb gradient data has values at root level
gradient_91 = interpolate_performance(climb_91_data, pressure_altitude, actual_temp, None)  # ft/NM
gradient_120 = interpolate_performance(climb_120_data, pressure_altitude, actual_temp, None)  # ft/NM

# Already rounded to nearest 10 ft/NM by the function
```

#### 3A.3: Calculate CAPS Altitudes

```python
caps_minimum_msl = runway_elevation + 600  # 600 ft AGL minimum
caps_recommended_msl = runway_elevation + 2000  # 2000 ft AGL optimal
pattern_altitude_msl = runway_elevation + 1000  # Standard pattern
```

#### 3A.4: Generate Departure Passenger Brief

**MANDATORY SAFETY ITEMS (Must ALWAYS be included):**
1. **Sterile Cockpit** - No talking during takeoff/landing/ATC; tap shoulder if urgent
2. **CAPS Parachute** - Red handle location, only pilot touches unless incapacitated
3. **Fire Extinguisher** - Located by pilot's left leg
4. **Emergency Egress Hammer** - Located under center console
5. **Air Sickness Bags** - In seatback pockets
6. **TKS Anti-Ice** - Plane is equipped (mention if icing visible, no alarm needed)

**Additional contextual tidbits encouraged** - Weather, winds, interesting facts, jokes, etc.

```python
# Determine weather tone based on density altitude
if density_altitude < 5000:
    weather_tone = "excellent conditions for takeoff"
    performance_note = "We'll have a nice brisk climb out."
elif density_altitude < 8000:
    weather_tone = "good conditions, though you'll notice a longer takeoff roll at this elevation"
    performance_note = "The takeoff will be a bit longer than sea level—completely normal."
elif density_altitude < 10000:
    weather_tone = "high elevation and warm temperatures, so we'll have an extended takeoff roll"
    performance_note = "We'll use more runway and have a gradual climb—standard for mountain flying."
else:
    weather_tone = "very high density altitude today"
    performance_note = "Expect an extended takeoff roll and gradual climb—this is normal at high elevations in warm weather."

# Add wind mention if significant
if abs(headwind) > 10:
    wind_mention = f"We have a {int(abs(headwind))}-knot {'headwind helping us out' if wind_type == 'headwind' else 'tailwind to account for'}. "
elif crosswind > 10:
    wind_mention = f"There's a {int(crosswind)}-knot crosswind today, so you might feel me working the controls a bit. "
else:
    wind_mention = ""

# MANDATORY safety briefing structure
safety_items = f"""
**Today's Flight:**

{wind_mention}{performance_note} {weather_tone.capitalize()}. Keep your seatbelt snug during the climb, and feel free to ask questions once we're established in cruise flight.

---

**Safety Briefing:**

Before we depart, a quick safety overview:

**Sterile Cockpit:** During takeoff, landing, and when I'm talking to air traffic control, I need you to hold all non-urgent questions—if something is truly urgent, tap me on the shoulder.

**Emergency Equipment:**
- CAPS Parachute System: This Cirrus has a whole-airframe parachute system. The red handle is right here [indicate location between the seats]. This is for emergencies only—never touch it unless I'm incapacitated and we're in an unrecoverable situation. I'll handle it if needed.
- Fire extinguisher: By my left leg
- Emergency egress hammer: Under the center console (for breaking windows if needed)
- Air sickness bags: In the seatback pockets if you need them

**Weather Systems:** This plane is equipped with TKS anti-ice, so if you notice any fluid on the wings or see me activate it in flight, that's normal—no cause for alarm.
"""

# Optional: Add contextual tidbits (airport facts, scenic notes, weather trivia, etc.)
# Example: If high elevation airport, mention interesting facts about the location
# Example: If scenic departure, mention views to expect
# LLM should add 1-2 contextual notes based on conditions/location if appropriate

passenger_brief = safety_items.strip()
```

#### 3A.5: Format Takeoff Brief Output

**OUTPUT ORDER (CRITICAL):**
1. GO/NO-GO Decision
2. Departure Passenger Brief
3. Emergency Brief
4. Safety Notes
5. Takeoff Performance
6. Additional Information

```markdown
# SR22T TAKEOFF BRIEF - {Airport} Runway {ID}

## 1. GO/NO-GO DECISION
**{✅ GO / ⚠️ GO WITH CAUTION / ❌ NO-GO}**

{Decision reasoning with specific factors}

**Runway Margin:** {margin} ft ({percent}% - {EXCELLENT/GOOD/ADEQUATE/MARGINAL/INSUFFICIENT})

---

## 2. DEPARTURE PASSENGER BRIEF
{passenger_brief}

---

## 3. EMERGENCY BRIEF - Phased Approach

**Phase 1 (Ground Roll - 0 to rotation):**
If engine failure occurs before rotation: **ABORT TAKEOFF** - Close throttle, apply brakes, stop on remaining runway ({remaining} ft available).

**Phase 2 (Rotation to {caps_min} ft MSL):**
If engine failure: Land straight ahead or within 30° of runway heading. Insufficient altitude for CAPS deployment.

**Phase 3 ({caps_min} to {caps_rec} ft MSL):**
If engine failure: **IMMEDIATE CAPS DEPLOYMENT** - Pull red handle without hesitation. Limited time for successful deployment at these altitudes.

**Phase 4 (Above {caps_rec} ft MSL):**
If engine failure: Troubleshoot per POH checklist. CAPS available if unable to resolve. Time permits decision-making.

---

## 4. SAFETY NOTES
{context-specific warnings for high DA, crosswinds, gusts, tailwinds, terrain, etc.}

---

## 5. TAKEOFF PERFORMANCE

### Performance Summary
**Pressure Altitude:** {pa} ft
**Density Altitude:** {da} ft (ISA {+/-}X°C - {assessment})

**Wind Analysis:**
- {Headwind/Tailwind}: {component} kt
- Crosswind: {component} kt

### Takeoff Distances
**Ground Roll:** {distance} ft
**Total Distance to 50ft:** {distance} ft

**Runway Analysis:**
- Available: {length} ft
- Required: {total_distance} ft
- **Margin: {margin} ft ({percent}% - {EXCELLENT/GOOD/ADEQUATE/MARGINAL/INSUFFICIENT})**

### Climb Performance
**At 91 KIAS (Initial Climb):** {gradient} ft/NM
**At 120 KIAS (Enroute Climb):** {gradient} ft/NM

### CAPS Altitudes
**Field Elevation:** {elevation} ft MSL
**CAPS Minimum:** {alt} ft MSL (600 ft AGL) - Emergency deployment only
**CAPS Recommended:** {alt} ft MSL (2,000 ft AGL) - Optimal deployment window
**Pattern Altitude:** {alt} ft MSL (1,000 ft AGL) - CAPS fully effective

---

## 6. ADDITIONAL INFORMATION

**Weather Conditions:**
- Temperature: {temp}°C
- Altimeter: {alt} inHg
- Winds: {dir}°/{speed} kt{" gusting " + gusts if gusts else ""}

**Runway Details:**
- Runway: {id}
- Heading: {hdg}° magnetic
- Length: {length} ft
```

**Margin Categories:**
- EXCELLENT: >150%
- GOOD: 125-150%
- ADEQUATE: 110-125%
- MARGINAL: 100-110%
- INSUFFICIENT: <100% → **NO-GO**

---

### Step 3B: Landing Brief (if selected)

#### 3B.1: Determine Flap Configuration

**SR22T ALWAYS uses 100% flaps for landing unless flaps are inoperative.**

```python
gust_factor = wind_gusts - wind_speed if wind_gusts else 0

# SR22T Standard: ALWAYS full flaps
flap_config = "full_flaps"
reason = "SR22T standard configuration (100% flaps)"

# Note crosswind/gust conditions but do NOT reduce flaps
if crosswind >= 15:
    technique_note = f"Strong crosswind ({int(crosswind)} kt) - use wing-low method, full aileron into wind"
elif crosswind >= 10:
    technique_note = f"Moderate crosswind ({int(crosswind)} kt) - maintain positive crosswind correction"
elif gust_factor >= 10:
    technique_note = f"Gusty conditions (+{int(gust_factor)} kt gusts) - maintain extra energy on final"
else:
    technique_note = "Normal wind conditions"

# Get speeds from v_speeds table (always full_flaps for SR22T)
v_speeds = EMBEDDED_SR22T_PERFORMANCE["v_speeds"]["approach_speeds"][flap_config]
base_final = v_speeds["final_approach_base_kias"]
threshold = v_speeds["threshold_crossing_kias"]
touchdown = v_speeds["touchdown_target_kias"]
```

#### 3B.2: Apply Gust Corrections

```python
gust_correction = round(gust_factor * 0.5, 1) if gust_factor > 0 else 0
final_approach_speed = round(base_final + gust_correction)
```

#### 3B.3: Interpolate Landing Distance

Use the imported `interpolate_performance()` function - DO NOT rewrite this:

```python
# Get landing data
landing_data = EMBEDDED_SR22T_PERFORMANCE["performance_data"]["landing_distance"]["conditions"]

# Use interpolate_performance (handles bilinear interpolation automatically)
landing_result = interpolate_performance(
    landing_data,
    pressure_altitude,
    actual_temp,
    ['ground_roll_ft', 'total_distance_ft']
)

landing_ground_roll = landing_result['ground_roll_ft']  # Already rounded to nearest 50 ft
landing_total_distance = landing_result['total_distance_ft']  # Already rounded
landing_margin = runway_length - landing_total_distance
```

#### 3B.4: Generate Arrival Passenger Brief

```python
if crosswind > 10 or gust_factor > 10:
    conditions = f"with {'gusty ' if gust_factor > 10 else ''}{'crosswinds' if crosswind > 10 else 'winds'}, so you might notice the nose pointed into the wind—completely normal"
elif density_altitude > 8000:
    conditions = "at a high-elevation airport with a slightly longer approach—normal for these conditions"
else:
    conditions = "with smooth conditions expected"

arrival_brief = f"We should be landing at {airport_name if provided else 'our destination'} in about twelve minutes. Temperature on the ground is {int(actual_temp)} degrees {conditions}. I'll need to focus on the approach, so I'll go quiet for a few minutes—make sure your seatbelt is snug and anything loose is secured."
```

#### 3B.5: Format Landing Brief Output

**OUTPUT ORDER (CRITICAL):**
1. GO/NO-GO Decision
2. Arrival Passenger Brief
3. Go-Around Brief
4. Safety Notes
5. Landing Performance
6. Additional Information

```markdown
# SR22T LANDING BRIEF - {Airport} Runway {ID}

## 1. GO/NO-GO DECISION
**{✅ GO / ⚠️ GO WITH CAUTION / ❌ NO-GO}**

{Decision reasoning with specific factors}

**Runway Margin:** {margin} ft ({percent}% - {EXCELLENT/GOOD/ADEQUATE/MARGINAL/INSUFFICIENT})

---

## 2. ARRIVAL PASSENGER BRIEF
{arrival_brief}

---

## 3. GO-AROUND BRIEF

**If go-around is required:**
- Full throttle immediately
- Positive rate of climb → Gear up
- Climb at Vy (best rate): 100 KIAS
- Expect reduced climb performance at density altitude {da} ft
- Estimated climb gradient: {gradient_120} ft/NM (from performance data)
- CAPS available above {caps_min} ft MSL if unable to climb

{Density altitude specific considerations}

---

## 4. SAFETY NOTES
{conditions-specific warnings for crosswinds, gusts, density altitude, tailwinds, short runway, etc.}

---

## 5. LANDING PERFORMANCE

### Performance Summary
**Pressure Altitude:** {pa} ft
**Density Altitude:** {da} ft (ISA {+/-}X°C)

**Wind Analysis:**
- {Headwind/Tailwind}: {component} kt
- Crosswind: {component} kt
{if gusts: - **Gusts:** +{factor} kt}

### Approach Configuration
**Configuration:** 100% Flaps (SR22T standard)
- Final Approach: {speed} KIAS ({base} + {correction} gust)
- Threshold: {speed} KIAS
- Touchdown Target: {speed} KIAS

**Technique Notes:** {technique_note}

### Landing Distances
**Ground Roll:** {distance} ft
**Total Distance:** {distance} ft

**Runway Analysis:**
- Available: {length} ft
- Required: {total} ft
- **Margin: {margin} ft ({percent}% - {assessment})**

### Wind Considerations
{Specific guidance for crosswind, gusts, headwind/tailwind}

---

## 6. ADDITIONAL INFORMATION

**Weather Conditions:**
- Temperature: {temp}°C
- Altimeter: {alt} inHg
- Winds: {dir}°/{speed} kt{" gusting " + gusts if gusts else ""}

**Runway Details:**
- Runway: {id}
- Heading: {hdg}° magnetic
- Length: {length} ft
```

---

### Step 4: Combined Analysis (if both selected)

Generate both briefs, then add:

```markdown
## COMPARATIVE ANALYSIS

**Runway Margins:**
- Takeoff: {margin} ft ({percent}%)
- Landing: {margin} ft ({percent}%)
- **Most Restrictive:** {takeoff/landing}

**Performance Considerations:**
{Analysis of which operation is limiting and why}

**Round-Trip Viability:**
{Assessment if both operations viable}

**OVERALL GO/NO-GO: {decision with combined reasoning}**
```

---

## Validation Checklist

Before delivering brief, verify:

**Calculations:**
- [ ] Interpolations used correct bounding data
- [ ] Roundings applied (10 ft for PA, 50 ft for DA/distances)
- [ ] Wind components calculated correctly
- [ ] Margin = available - required (positive = safe)

**Completeness:**
- [ ] All sections present
- [ ] Passenger brief included
- [ ] Specific numbers (no placeholders)
- [ ] Assessment categories correct

**Safety Logic:**
- [ ] Margin <10% or negative → NO-GO
- [ ] Margin 10-25% → GO WITH CAUTION
- [ ] Margin >25% → GO (with advisories if needed)
- [ ] All warnings for high DA, crosswinds, gusts, tailwinds

---

## Reference Files

**Performance Data:** `references/sr22t_performance_data.py`
- Complete takeoff/landing tables
- Climb gradient tables
- V-speeds with approach configurations

**Calculation Functions:** `references/calculation_functions.py`
- All formulas with test cases
- Interpolation algorithms
- Wind component calculations

**V-Speeds Guide:** `references/v-speeds-reference.md`
- Flap configuration selection logic
- Gust correction methodology
- Wind technique guidance

**Examples:** `examples/`
- High density altitude scenario
- Crosswind landing scenario
- Round-trip analysis

---

## Usage Notes

**For LLM:**
1. Request inputs if not provided
2. Execute calculations using provided Python code
3. Use exact interpolation algorithms (don't approximate)
4. Apply validation checklist before delivering
5. Provide clear GO/NO-GO with specific reasoning

**Adaptation:**
- Adjust passenger brief tone for nervous flyers or children
- Flag marginal conditions proactively
- Suggest alternates if NO-GO
- Recommend waiting for better conditions if borderline

**Consistency Critical:**
Same inputs must produce identical outputs across runs for safety.
