---
name: refrigerated-cargo-specifics
description: |
  Use this skill when the user asks about refrigerated (reefer) trucking — cold chain compliance, FDA temperature recording requirements, Sanitary Transportation Rule (STR / 21 CFR 1.900-1.934), commodity-specific temperature ranges, refrigeration unit operation, temperature recorder calibration, and how a load is challenged if temperature deviates. Cite 21 CFR Part 1 Subpart Q.
---

# Refrigerated Cargo / Reefer Specifics

Refrigerated trucking has FDA + USDA oversight in addition to FMCSA. The Sanitary Transportation Rule (STR) governs temperature-controlled food shipments. This skill covers cold chain compliance.

## FDA Sanitary Transportation Rule (STR) — 21 CFR Part 1, Subpart Q

Effective 2017. Applies to:
- Carriers transporting food (human + animal) in interstate commerce
- Shippers + receivers of food
- Loaders + brokers

Exempt:
- Vehicles < 10,001 lb GVWR
- Carriers with < $500K annual food transport revenue (small businesses)
- Food transported entirely within one state's borders

## Carrier responsibilities (21 CFR 1.910)

A carrier must:

1. **Provide vehicles + transportation equipment** capable of maintaining temperatures necessary for food safety
2. **Pre-cool / pre-heat** the vehicle to required temperature before loading
3. **Maintain temperature** during transport (using refrigeration units)
4. **Allow shipper inspection** of vehicle interior
5. **Comply with shipper-supplied written procedures** for that specific shipment
6. **Train staff** on sanitary transportation practices
7. **Maintain records** for 12 months OR 6 months after a transportation operation

## Temperature recording

A carrier must:
- Use a continuous temperature recorder OR
- Take periodic readings (typically every 4-6 hours) OR
- Use a real-time monitoring system (like SaveOnFreight, Sensitech, Carrier TRU-Telematics)

The shipper specifies which monitoring method is acceptable. For "Time/Temperature Critical" loads (frozen seafood, raw poultry, etc.) continuous recording is mandatory.

## Typical commodity temperature ranges

| Commodity | Typical Setting | Acceptable Range |
|---|---|---|
| Fresh produce | 32-50°F | varies by commodity |
| Frozen foods | -10 to 0°F | -20 to 5°F |
| Ice cream | -20 to -10°F | -30 to -10°F |
| Dairy | 33-40°F | 28-45°F |
| Fresh meat | 28-38°F | 28-40°F |
| Pharmaceuticals (cold chain) | 35-46°F (refrigerated) or -4 to -22°F (frozen) | strict |
| Bananas | 56-58°F | 55-60°F (specific to ripening) |

Some commodities (e.g., chilled tomatoes) have a narrow range; deviations are claim-eligible.

## Refrigeration units (TRUs — Trailer Refrigeration Units)

Most reefers use diesel-powered TRU:
- Carrier Transicold, Thermo King are dominant brands
- Independent fuel tank
- Set temperature via thermostat
- Continuous run (typical) or cycle-on-demand
- Diesel cost per hour: $1-3 depending on ambient

Pre-cooling (running TRU to chill the trailer before loading) is required. Pre-cooling takes 2-4 hours for a 53' reefer.

## Temperature recorder requirements

For STR compliance:
- **Accuracy:** ±0.5°F or better
- **Calibration:** Verified at least annually; ideally before each high-stakes load
- **Data download:** Available for shipper / receiver inspection
- **Tampering resistance:** Some loads require sealed / tamper-evident recorders

Real-time monitoring (cell-connected) is becoming standard for high-value loads. Provides:
- Continuous data streaming
- Alarms on threshold breaches
- Historical playback for claims

## Loading + unloading

The carrier should:
- Verify driver pre-cooled the trailer
- Check temperature at pickup (record on BOL)
- Watch for delays during loading that exceed safe time (typically 1-2 hours)
- Refuse load if shipper's trailer condition is unsafe (mold, residue, broken seals)
- Inspect upon delivery; record any temperature deviations

## Claims for temperature-deviation

If a load arrives with temperature deviation:

1. **Receiver inspects** + documents condition
2. **Reefer download / monitoring data** retrieved
3. **Claim filed** within ~30 days
4. **Carrier investigates** — was deviation due to:
   - Reefer malfunction?
   - Driver error (turned off)?
   - Loading too long?
   - Trailer integrity?
5. **Claim settlement** with insurance or denial

A claim is more likely to succeed if:
- Pre-loading temperature documented
- Continuous recording shows deviation
- Cargo inspected at delivery
- Insurance carrier notified within 24-48 hours

## Common reefer mistakes

1. **Not pre-cooling the trailer.** Loading hot trailer + product = exceeded temperature on departure.
2. **Driver turns off TRU to save fuel.** Catastrophic. Some carriers monitor TRU runtime to detect this.
3. **No temperature record on BOL at pickup.** No baseline; claims hard.
4. **Trailer with damaged insulation.** Common for older fleet; temperature can't hold.
5. **Calibration not current.** Recorder readings inadmissible.
6. **Delayed loading.** 4-6 hours at loading dock + product temperature rises before transport starts.
7. **Mixed commodities at incompatible temperatures.** Beef + produce in same trailer = compromise temperature, neither happy.

## Specific high-stakes commodities

### Frozen seafood
- Continuous recording required
- Acceptable temperature: 0 to -22°F
- Deviation = $0.50-$1.50/lb of cargo = high-dollar claims

### Pharmaceuticals
- GxP (Good Distribution Practice) often layered on top of STR
- Continuous recording mandatory
- Detailed audit trail
- Carrier liability for full pharmaceutical value (typically $500K+ per load)
- TAPA + ISO 9001 certifications increasingly required

### Raw poultry / ground beef
- USDA FSIS oversight in addition to FDA STR
- Temperature deviations have public health implications
- Mandatory product condemnation if abused

## Where this fits in X3

X3's `vehicles.html` can be configured to recognize a vehicle as "reefer" (refrigerated). Future: integration with TRU telematics for continuous monitoring + automatic claims documentation.

For carriers specializing in reefer:
- Get TRU service contracts (annual maintenance)
- Calibrate temperature recorders annually
- Train drivers on cold chain best practices
- Document pre-cooling routines


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=refrigerated-cargo-specifics

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
