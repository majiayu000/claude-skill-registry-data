---
name: auth-interstate-vs-intrastate
description: |
  Use this skill to determine whether you need interstate FMCSA authority or just intrastate state authority. Covers the federal/state divide.
---

# Interstate vs Intrastate Authority — What Do You Need?

Interstate (federal) vs intrastate (state-only) authority is a fundamental distinction. Wrong choice = unauthorized operation + penalties.

## What's interstate
Any operation that:
- Crosses a state line, OR
- Originates AND terminates in different states, OR
- Crosses an international border (US-Mexico, US-Canada)

## What's intrastate
Operation that:
- Originates AND terminates in the same state
- Doesn't cross state lines
- Doesn't cross international borders

## Special cases
- Some intrastate operations may be subject to federal jurisdiction (interstate commerce regardless of state lines)
- "For hire" vs "private" — different requirements
- Hazmat operations — federal jurisdiction regardless of state

## What you need for interstate
- USDOT number
- MC number (if for-hire transportation)
- BMC-91 (insurance proof)
- BOC-3 (process agents in each state)
- IFTA + IRP if applicable

## What you need for intrastate
- State motor carrier registration
- State insurance proof (varies)
- State-issued license plate
- USDOT number (only if vehicle weight/use exceeds federal threshold)

## State motor carrier registration
- Each state has its own registration process
- Some states use IRP (apportioned plates)
- Some states have separate intrastate registration
- Insurance requirements vary state to state

## How to determine
1. List your operating routes
2. Identify which cross state lines
3. If ANY interstate operation → need federal authority
4. If ALL operations intrastate → state authority only

## Common confusion
- "I deliver only in [state]" — but if you pick up loads from interstate carrier, you may be operating in interstate commerce
- "I deliver locally" — but if you cross a state line (even briefly), interstate authority required

## Penalties for wrong authority
- Federal: $10,000+ per violation
- State: varies, but typically $500-$5,000

## Compass authority module
- Tracks current authority level (federal or state)
- Alerts if interstate operation occurs without federal authority
- Manages USDOT/MC/IFTA/IRP renewal cycle

## CFR citations
- **49 CFR Part 365**
- **State Motor Carrier Laws**

## How Compass surfaces this
Searchable in Compass Ask. Runs against carrier fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=auth-interstate-vs-intrastate

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
