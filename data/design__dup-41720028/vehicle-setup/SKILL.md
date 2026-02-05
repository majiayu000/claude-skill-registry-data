---
name: "vehicle-setup"
description: "Guide users through Slovak VAT Act 2025 compliant vehicle registration with VIN validation"
---

# Vehicle Setup Skill

## Purpose
Guide users through Slovak VAT Act 2025 compliant vehicle registration with VIN validation.

## When to Activate
- Trigger words: "add vehicle", "register car", "new vehicle"
- License plate patterns: "BA-*", "*-123*"
- Vehicle brands: "Ford", "BMW", "Škoda"

## Instructions

### Step 1: Collect Mandatory Fields
Ask conversationally for:

1. **License Plate** (Slovak format: XX-123XX, e.g., BA-456CD)
   - Validate format: 2 letters + hyphen + 3 digits + 2 letters
   - Example: "BA-789XY"

2. **VIN** (17 characters, no I/O/Q - mandatory for Slovak VAT Act 2025)
   - Validate: exactly 17 characters, no I/O/Q letters
   - If invalid: "VIN cannot contain letters I, O, or Q. Please verify."
   - Explain: "VIN is required for tax deduction eligibility in Slovakia"

3. **Fuel Type** (Diesel, Gasoline 95/98, LPG, Hybrid, Electric)
   - Suggest typical efficiency: Diesel 8.5 L/100km, Gasoline 9.5 L/100km
   - Always use L/100km format (European standard), never km/L

4. **Current Odometer** (kilometers)
   - Validate: > 0, < 1,000,000 km
   - Ask: "What's the current odometer reading in kilometers?"

### Step 2: Show Summary & Confirm
Present clear summary before creating:

```
Summary:
• Name: Ford Transit Delivery Van
• Plate: BA-789XY
• VIN: WVWZZZ3CZDP123456
• Fuel: Diesel (avg 8.5 L/100km)
• Odometer: 125,000 km

Create this vehicle? (yes/no)
```

### Step 3: Create Vehicle
- Call MCP tool: `car-log-core.create_vehicle`
- Request: { name, license_plate, vin, fuel_type, make, model, year, initial_odometer_km }
- Success: "✅ [Vehicle name] registered! Ready to track trips."
- Error: Explain issue, offer to retry

## Validation Rules
- **VIN:** Must match `^[A-HJ-NPR-Z0-9]{17}$` (no I, O, Q)
- **License Plate:** Must match `^[A-Z]{2}-[0-9]{3}[A-Z]{2}$`
- **Fuel Efficiency:** Always L/100km (European standard), never km/L

## Slovak Compliance
- VIN mandatory per Slovak VAT Act 2025
- Explain importance: "VIN required for tax deduction eligibility in Slovakia"
- License plate must follow Slovak format

## Error Handling
- **Duplicate plate:** Ask if user wants to update existing vehicle
- **Invalid VIN:** Show why invalid (length, forbidden characters), ask for correction
- **Invalid plate:** Show expected format, ask for correction

## Related Skills
After successful creation:
- Suggest: "Ready to log your first checkpoint!" (links to checkpoint-from-receipt skill)

---

**For detailed examples:** See GUIDE.md
**For MCP tools:** See REFERENCE.md
