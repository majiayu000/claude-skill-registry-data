---
name: "checkpoint-from-receipt"
description: "Create checkpoints from receipt photos using QR scanning, e-Kasa API, and GPS extraction (10-40s)"
---

# Checkpoint from Receipt Skill

## Purpose
Automatically create checkpoints from receipt photos using QR scanning, e-Kasa API, and GPS extraction.

## When to Activate
- User pastes image (auto-detect)
- Keywords: "refuel", "fill up", "got gas", "checkpoint", "receipt"
- File extensions: .jpg, .png, .pdf

## Instructions

### Workflow: 3-Stage Orchestration
```
QR scan (2-5s) → e-Kasa API (5-30s) → GPS extraction (2-5s) → Checkpoint creation → Gap detection
```

**Total time:** 10-40 seconds typically

---

### Stage 1: QR Code Scanning

1. **When image pasted:** "📷 Receipt detected. Scanning QR code..."
2. **Call:** `ekasa-api.scan_qr_code` (multi-scale: 1x, 2x, 3x)
3. **Progress:**
   - "Trying 1x scale..."
   - "Trying 2x scale... Found!"
4. **Extract:** receipt_id (e.g., "O-123456789ABC")

**If QR not found:**
- "QR code not detected. Try better lighting or different angle."
- Fallback: "What's the e-Kasa receipt ID? (starts with O-)"

---

### Stage 2: e-Kasa API (SLOW - Show Progress!)

1. **Start:** "🔄 Fetching from e-Kasa API... (may take up to 60s)"
2. **Call:** `ekasa-api.fetch_receipt_data`
3. **Progress updates:**
   - 15s: "Still fetching... (15s elapsed)"
   - 30s: "Almost there... (30s elapsed)"
   - 45s: "Taking longer than usual... (45s elapsed)"

**If timeout (60s):**
- "⏱️ e-Kasa timed out. Options:"
- "1) Retry"
- "2) Manual entry (fuel type, liters, price)"

**If success:**
- Parse fuel items using Slovak patterns:
  - "Diesel", "Nafta", "Motorová nafta"
  - "Natural 95", "BA 95", "Benzín 95"
  - "Natural 98", "BA 98", "Benzín 98"
  - "LPG", "Autoplyn"
- **Show:** "✅ 52.3L Diesel @ €1.45/L = €75.84"

**If multiple fuel items:**
- List all items
- Ask: "Which fuel was for your vehicle?"

---

### Stage 3: Dashboard Photo GPS

1. **Ask:** "📸 Now paste dashboard photo for GPS location"
2. **Call:** `dashboard-ocr.extract_metadata`
3. **Extract:**
   - GPS coordinates (latitude, longitude) from EXIF
   - Timestamp from EXIF
   - Odometer reading (OCR with confidence > 80%)

**If GPS found:**
- "📍 Location: 48.1486, 17.1077 (Bratislava)"
- Optional: Reverse geocode to show address

**If no GPS:**
- "📍 No GPS data found. Options:"
- "1) Enable location services and retake photo"
- "2) Enter GPS coordinates manually"
- "3) Enter address (I'll geocode it)"

**If OCR odometer found:**
- "📊 Detected odometer: 125,340 km (confidence: 92%)"
- "Is this correct? (yes/no)"

**If OCR fails or low confidence:**
- "What's the current odometer reading in kilometers?"

---

### Stage 4: Create Checkpoint & Detect Gap

1. **Combine data:**
   - Receipt: fuel_type, fuel_liters, price, vendor, receipt_id
   - GPS: latitude, longitude, address (optional)
   - Datetime: from receipt or dashboard photo
   - Odometer: from OCR or user input

2. **Slovak compliance check:**
   - Ask for driver name if missing
   - Separate refuel timing from trip timing
   - Note: Refuel location may differ from trip start/end

3. **Call:** `car-log-core.create_checkpoint`
4. **Success:** "✅ Checkpoint created at 125,340 km!"

5. **Auto-detect gap:**
   - Call: `car-log-core.detect_gap`
   - If gap > 100km: "⚠️ Gap detected: 820 km over 7 days. Reconstruct trips?"
   - If gap detected → Auto-trigger trip-reconstruction skill

---

## Timing Breakdown
- **QR scan:** 2-5 seconds
- **e-Kasa API:** 5-30 seconds (show progress!)
- **GPS extraction:** 1-2 seconds
- **Checkpoint creation:** 1 second
- **Gap detection:** 1 second
- **Total:** 10-40 seconds typically

## Error Handling

### QR Scan Failed
- Try multi-scale (1x, 2x, 3x)
- If all fail: Manual receipt ID entry

### e-Kasa Timeout
- Show elapsed time
- Offer retry or manual entry
- Cache successful responses

### No GPS
- Fallback to address geocoding
- Manual GPS entry
- Continue without location (warn about compliance)

### Multiple Fuel Items
- List all items with prices
- Ask user to select correct one

### Ambiguous Geocoding
- Show alternatives with confidence
- Ask user to select correct location

## Slovak Compliance

### Critical Requirements
- **Driver name:** Mandatory for tax deduction
- **Refuel timing:** Separate from trip start/end timing
- **Location:** Refuel station may differ from trip origin/destination
- **L/100km format:** Always use European standard

### Data Storage
- Store `refuel_datetime` separately from trip timing
- Store `refuel_location` separately from trip endpoints
- Link checkpoint to trips via gap detection

## Related Skills

### Auto-triggers
- **trip-reconstruction:** If gap > 100km detected
- **data-validation:** Automatic validation after checkpoint creation

### Links to
- **vehicle-setup:** If no vehicle registered
- **report-generation:** After sufficient checkpoints collected

---

**For detailed examples:** See GUIDE.md
**For MCP tools:** See REFERENCE.md
**For timeout troubleshooting:** See ../TROUBLESHOOTING.md
