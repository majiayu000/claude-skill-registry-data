---
name: mpls-permits
description: Query the City of Minneapolis building permit register (CCS_Permits ArcGIS) live — who is building, remodeling, tearing down or finishing work, where, by which contractor. Use for "pull permits", "what's being built in Minneapolis", "teardowns", "new restaurants opening", "tenant build-outs", "final inspection", "who's the contractor", or any gift/lead list built from permits. Tool skill; task skills forward-reference it.
---

# Minneapolis permits, live

Endpoint (no auth, updated daily):
`https://services.arcgis.com/afSMGVsC7QlRK1kZ/arcgis/rest/services/CCS_Permits/FeatureServer/0/query`
Page with `resultOffset` + `resultRecordCount=2000` until `exceededTransferLimit` is false.
Dates in `where`: `issueDate >= date '2026-03-01'`. Epoch-ms in results.

Older structural traps: there is no project value; a row is not a project (one project
spans many trade permits); the trade mix skews to plumbing/mechanical; and there are two
different definitions of "commercial".

## Fields that matter
`Display` (address), `APN` (= Hennepin PID, joins to parcels), `Latitude/Longitude`,
`Neighborhoods_Desc`, `permitType`, `occupancyType`, `workType`, `status`, `milestone`,
`comments` (free text, the richest field), `issueDate`, `completeDate`, `applicantName`
(contractor OR homeowner), `totalFees`. `value` is empty on every row.

## Values, measured fall 2026
- `permitType` since Mar 1: Plumbing, Mechanical, Res, Commercial, Wrecking, Site. **No Sign type.**
- `occupancyType`: SFD, TFD, 3to4, MFD, TH, Comm, Mixed, Accessory, blank.
- `workType`: Res → Misc, Remodel, Addition, Accessory, New. Commercial → Remodel, RoofWind, Addition, New. Wrecking → Private.
- `status`: Issued, Closed, Cancelled, Expired. `milestone`: Inspection, Final Inspection, Closed.
  **"Final Inspection" = about to open**, the best timing signal in the register.

## Traps, each hit in practice
- **`permitType='Commercial'` includes condo and apartment units**, one row per unit
  (one building x7). Filter `occupancyType IN ('Comm','Mixed')` and dedupe on
  (Display, first 80 chars of comments). *Why:* otherwise one condo kitchen reads as seven restaurants.
- **`comments` is boilerplate-heavy.** Cut at "certificate of occupancy", "const type",
  "Building Code", reviewer initials "(JJL)", "-ACW", "(DMH - Pdox)"; some rows are
  "Source Information is Not Available" — show those as blank.
- **Keyword filters over-match**: "repair shop" (hospital bed repair), "gym" (bleacher
  replacement), "kitchen" (residential units, kitchen fire). Exclude explicitly and eyeball
  the top 40 rows before rendering.
- **Don't parse business names out of comments.** Regex output was wrong 3 of 4 times.
- **`applicantName` is sometimes the homeowner.** Show it only when it reads as a company
  (INC/CORP/CONSTRUCTION/BUILDERS/HOMES or another company suffix); never show `fullName`.
- An **open wrecking permit** doesn't mean the building still stands. Say so on the page.
- **Year built** isn't in the register: POST PIDs in batches of 150 to
  `https://gis.hennepin.us/arcgis/rest/services/HennepinData/LAND_PROPERTY/MapServer/1/query`
  (`where=PID IN (...)`, `outFields=PID,BUILD_YR`). ~98% of PIDs match.
- **Minneapolis only.** Saint Paul's register stopped publishing 2025-06-30.
- **Saint Paul demolitions live in their own layer**: `services1.arcgis.com/9meaaHE3uiba0zr8/.../Permit_Tppe_Demolition_Permit/FeatureServer/0`, ~1,100 rows to 2025-06-30, `WORK_TYPE` Residential/Commercial Demo vs accessory structures. `CONTRACTORNAME` prefixes a PERSON's name to the company ("FIRSTNAME LASTNAME LASTNAME & SONS INC"): strip the person before display. Contractor phones for haulers: FMCSA SAFER by curl; its keyword search is fuzzy, so require the query in the LEGAL name.

Related: `counterparty-gift` (a task that builds a lead list from this).
