---
name: "trip-reconstruction"
description: "Fill gaps between checkpoints using hybrid GPS (70%) + address (30%) template matching with high confidence"
---

# Skill 3: Trip Reconstruction (GPS-First Matching)

**Purpose:** Automatically fill gaps between checkpoints using hybrid GPS (70%) + address (30%) template matching with high-confidence proposals

**Activation:** Automatic trigger after checkpoint creation shows gap, or manual request: "fill trips", "reconstruct from November 1"

---

## Overview

Trip Reconstruction is Car Log's core innovation - using GPS-first hybrid matching to automatically propose trips based on recurring route templates. When a checkpoint gap is detected (e.g., 820km between refuels), the system matches against saved templates using precise GPS coordinates (70% weight) combined with address similarity (30% weight) to generate high-confidence proposals.

**Key Innovation:** GPS coordinates are the source of truth, enabling 90%+ confidence matches even when addresses are ambiguous ("Košice" could mean 3 fuel stations, but GPS 48.7164°N, 21.2611°E is exact).

---

## Workflow (7 Steps)

### Step 1: Gap Analysis
When a checkpoint is created, automatically analyze the gap to the previous checkpoint:
- Distance gap (odometer delta)
- Time gap (days between checkpoints)
- Start/end locations (GPS + address)
- Vehicle context

**MCP Tool:** `car-log-core.analyze_gap(checkpoint1_id, checkpoint2_id)`

**User Message Pattern:**
```
"Gap Analysis:
• Start: Bratislava (Nov 1, 45,000 km)
• End: Košice (Nov 8, 45,820 km)
• Distance: 820 km
• Duration: 7 days

How would you like to fill this gap?
1. Use my templates (automatic matching)
2. Tell me specific trips
3. I'll do it later"
```

### Step 2: Template Fetching
If user chooses automatic matching, fetch all saved templates for the vehicle.

**MCP Tool:** `car-log-core.list_templates(vehicle_id)`

**Considerations:**
- If no templates exist, suggest creating one from gap data
- Templates must have GPS coordinates (mandatory for high-confidence matching)
- Show template count and brief summary

### Step 3: Template Matching (GPS-First Algorithm)
Run hybrid GPS + address matching using the core algorithm:

**MCP Tool:** `trip-reconstructor.match_templates(gap_data, templates, gps_weight=0.7, address_weight=0.3)`

**GPS-First Scoring Algorithm:**

**GPS Distance Scoring (70% weight):**
- < 100m: Score 100 (perfect match - within parking lot variance)
- 100m-500m: Score 90 (excellent - same building area)
- 500m-2km: Score 70 (good - same neighborhood)
- 2km-5km: Score 40 (poor - different area)
- > 5km: Score 0 (no match)

**Address Similarity Scoring (30% weight):**
- Exact match: 100
- Substring match: 80 ("Bratislava" in "Bratislava City Center")
- City match: 60 (both contain same city name)
- Levenshtein similarity: 0-100

**Final Confidence Calculation:**
```
confidence = (gps_score * 0.7) + (address_score * 0.3)

Bonus factors (up to +10%):
+ 5% if day-of-week matches template's typical_days
+ 5% if distance matches within 10km
```

**Matching Mode Selection:**
- MODE_A (GPS-only): Both checkpoints have GPS, no addresses → GPS 100%
- MODE_B (Hybrid): Both have GPS + addresses → GPS 70% + Address 30%
- MODE_C (Fallback): No GPS, addresses only → Address 100% (low confidence)

### Step 4: Proposal Presentation
Present matching results based on confidence tiers:

**High Confidence (90-100%):**
```
"Reconstruction Proposal (92% confidence):

✓ Exact GPS match (within 50m)
✓ Day-of-week matches template
✓ Distance matches expected route

Proposal:
2× Warehouse Run (Bratislava ↔ Košice)
• Nov 1-2: Bratislava → Košice (410km)
• Nov 6-7: Košice → Bratislava (410km)

Coverage: 820km / 820km (100%) ✓

This looks very reliable. Accept?"
```

**Medium Confidence (70-89%):**
```
"Reconstruction Proposal (75% confidence):

⚠️ GPS match is approximate (within 1.5km)
✓ City names match (Bratislava, Košice)
⚠️ Days don't match typical pattern

Proposal: 2× Warehouse Run (820km total)

This is likely correct, but please verify:
1. Did you drive to Košice on Nov 1?
2. Did you return to Bratislava on Nov 6?

Accept, modify, or reject?"
```

**Low Confidence (<70%):**
```
"No High-Confidence Match Found

I found potential matches, but none are above 70% confidence:
• Warehouse Run (58%) - Distance matches, but GPS is 8km off
• Client Visit (42%) - Wrong direction

Options:
1. Manually describe the trips
2. Create a new template for this route
3. Skip reconstruction for now"
```

**Multiple High-Confidence Matches:**
Present all options sorted by confidence (descending) and let user choose the best match.

### Step 5: User Approval
Request explicit approval before creating trips:
- Accept proposal → Proceed to Step 6
- Modify proposal → Allow trip adjustments
- Reject → Offer manual entry or skip

**Always require confirmation** - never auto-create trips without approval.

### Step 6: Batch Trip Creation
Create all approved trips in a single batch operation with Slovak compliance fields:

**MCP Tool:** `car-log-core.create_trips_batch(trips[])`

**Required Slovak Compliance Fields:**
- `driver_name`: Full name (MANDATORY for Slovak VAT Act 2025)
- `trip_start_datetime`: ISO 8601 format
- `trip_end_datetime`: ISO 8601 format
- `trip_start_location`: Address/label
- `trip_end_location`: Address/label
- `distance_km`: From template or calculated
- `purpose`: "Business" or "Personal"
- `business_description`: Required if Business purpose
- `reconstruction_method`: "template"
- `template_id`: Reference to matched template
- `confidence_score`: Matching confidence

### Step 7: Automatic Validation
Immediately after trip creation, run validation checks:

**MCP Tools:**
- `validation.validate_checkpoint_pair(checkpoint1_id, checkpoint2_id)` - Check distance sum (±10% threshold)
- `validation.validate_trip(trip_id)` - Check each trip's fuel efficiency

**Validation Thresholds:**
- Distance sum: ±10% (odometer delta vs. sum of trip distances)
- Fuel consumption: ±15% (expected vs. actual fuel)
- Efficiency range: Diesel 5-15 L/100km, Gasoline 6-20 L/100km

**User Message Pattern:**
```
"✅ Validation Passed:
• Distance: 820km / 820km (0% variance) ✓
• Fuel: 72.8L / 69.7L (+4.4%, within 15% threshold) ✓
• Efficiency: 8.9 L/100km (Diesel range: 5-15) ✓

Your trips are ready for tax reporting!"
```

If validation warnings appear (e.g., fuel +25%), show clear explanation but don't block trip creation - allow user to review and adjust.

---

## Related Skills

**Auto-triggered after:**
- Skill 2 (Checkpoint from Receipt) → Gap detection

**May trigger:**
- Skill 4 (Template Creation) → If no templates exist or no match found
- Skill 6 (Data Validation) → Automatic validation after trip creation

---

## Success Criteria

- GPS matching uses 70% weight, address matching 30% weight
- Confidence ≥70% required for automatic proposals
- Multiple high-confidence matches presented with user choice
- Stateless orchestration (Skill fetches all data, servers are stateless)
- Automatic validation runs immediately after trip creation
- Natural language proposals ("2× Warehouse Run" not "trip_001, trip_002")
- Clear confidence breakdown shown to user
- Slovak compliance fields mandatory (driver_name, VIN, etc.)
- Coverage percentage calculated (distance covered / total gap)
- User always has option to reject or modify proposals

---

## Key Algorithms Reference

**GPS Distance Calculation (Haversine):**
```
distance = 2 * R * arcsin(√(sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)))
R = 6371 km (Earth radius)
```

**Confidence Tiers:**
- 90-100%: High (strong recommendation, minimal verification needed)
- 70-89%: Medium (likely correct, user verification recommended)
- <70%: Low (do not show as automatic proposal)

**Template Completeness Score:**
Essential fields (GPS coords): 60%
Distance: +10%
Typical days: +10%
Purpose: +10%
Business description: +10%

---

**Implementation Status:** Specification complete, implementation pending
**Estimated Effort:** 5 hours
**Dependencies:** car-log-core, trip-reconstructor, geo-routing, validation (all functional)
