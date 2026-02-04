---
name: "Phone Number Lookup"
description: "Carrier, location, and line type lookup for phone numbers"
allowed-tools:
  - src.tools.phone_lookup
---

# Phone Number Lookup

## Purpose

Investigate phone numbers to identify carrier information, geographic location, line type, and associated risks for fraud prevention and due diligence purposes.

## When to Use

- Fraud investigation and prevention
- Identity verification and authentication
- Due diligence on contact information provided
- Investigation of suspicious communications
- Risk assessment for phone-based transactions
- Verification of business contact details
- Analysis of communication patterns in investigations
- Compliance screening for high-risk regions

## How to Use

The phone lookup tool provides detailed telecommunications intelligence:

- **Carrier Information**: Network provider, carrier type (mobile/landline)
- **Geographic Data**: Country, region, city (where available)
- **Line Type**: Mobile, landline, VoIP, toll-free, premium rate
- **Portability**: Number porting history and original carrier
- **Risk Assessment**: Known fraud indicators, disposable numbers
- **Validation**: Number format validation and active status

## Examples

**Fraud prevention:**
```
Phone: +1-555-0123 provided for account verification
Analysis: VoIP number, no geographic tie to claimed address
Risk: High - potential spoofed or disposable number
```

**Business verification:**
```
Company: ABC Corp claims headquarters phone +1-212-555-0100
Verification: Landline, Manhattan location matches claimed address
Assessment: Low risk - legitimate business line
```

**International investigation:**
```
Contact: Foreign number +44-20-7946-0958 in transaction
Analysis: UK mobile number, London area, major carrier
Cross-check: Correlate with other provided location information
```

**Communication pattern analysis:**
```
Investigation: Multiple calls from +1-800-555-0199
Research: Toll-free number, call center service, bulk registration
Context: Mass marketing or scam operation indicator
```

## Important Notes

- Phone number intelligence varies by country and carrier
- Mobile numbers may not indicate current physical location
- VoIP and internet-based numbers can be easily spoofed or relocated
- Consider timezone and dialing patterns for geographic analysis
- Some carriers provide limited public information
- Number portability can obscure original carrier and location data
- Disposable/burner phone services present elevated fraud risk
- Cross-reference phone data with other contact information
- Be aware of privacy regulations regarding telecommunications data