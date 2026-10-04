---
name: ohio-roadtrip-scope
description: "Approve a selected Ohio city sequence and supporting lodging, dining, attraction, and driving working set for the 7-day Minneapolis-to-Ohio roadtrip before the final itinerary write."
---

# Ohio Roadtrip Scope

## Approve the Ohio Roadtrip Working Set

Use the bundled travel search skills to approve the Ohio city sequence and its supporting lodging, dining, attraction, and driving working set from real dataset rows. This stage standardizes the selected set for later handling, reduces duplicate scanning, and preserves review traceability. Leave `/app/output/itinerary.json` unwritten here.

## Required Ohio Roadtrip Inputs

- `workflow/travel_intake_checkpoint.json`
- `workflow/continuation_gate.json`
- Results returned by `search-cities`, `search-driving-distance`, `search-accommodations`, `search-restaurants`, and `search-attractions`

## Select the Ohio City Sequence, Lodging, Dining, Attractions, and Driving Legs

1. Read the checkpoint artifacts first and carry forward the fixed trip scope: two travelers, Minneapolis departure, March 17 through March 23, 2022, three Ohio cities, no flights, pet-friendly lodging, requested American, Mediterranean, Chinese, and Italian cuisines, and total budget up to `$5,100`.
2. Use `search-cities` to pull Ohio options and choose an ordered three-city Ohio sequence. Keep other viable Ohio city choices in `non_selected_candidates` instead of dropping them.
3. Use `search-driving-distance` for the Minneapolis-to-first-city leg and each intercity Ohio leg. Approve only self-driving or driving legs. Do not use `search-flights`.
4. Use `search-accommodations` for each selected city. Keep only lodging rows that can host two travelers, fit the stay block, and do not state `No pets` in `house_rules`. If a row is pet-permitted by omission rather than an explicit pet note, capture that evidence in `pet_friendly_notes`.
5. Use `search-restaurants` only within the selected cities until the combined dining set covers American, Mediterranean, Chinese, and Italian cuisines.
6. Use `search-attractions` for each selected city and keep enough dataset-backed attractions to support the later 7-day itinerary without inventing places from memory.
7. Separate selected vs non-selected results explicitly. Rejected cities, drive legs, lodgings, restaurants, and attractions stay in `non_selected_candidates` with a short reason so the approved set can continue without a broad rescan.
8. Keep the approved working set within the `$5,100` ceiling for two travelers. Use lodging totals as hard costs and keep remaining budget room visible for meals and driving inside `budget_estimate`.

## Write `workflow/working_set_record.json`

Write `workflow/working_set_record.json` with these exact keys:

- `selected_city_sequence`: ordered list of the chosen Ohio cities.
- `selected_drive_legs`: driving legs backed by the distance dataset, including the Minneapolis departure leg and each approved Ohio intercity leg.
- `selected_accommodations`: chosen lodging rows for the selected cities, with stay coverage for the trip.
- `selected_restaurants`: chosen restaurant rows that provide the requested cuisine coverage.
- `selected_attractions`: chosen attraction rows for the selected cities.
- `non_selected_candidates`: grouped rejected or reserve options with short exclusion reasons.
- `tool_called`: record the JSON output names for the search skills actually used in this stage, normally `search_cities`, `search_driving_distance`, `search_accommodations`, `search_restaurants`, and `search_attractions`.
- `budget_estimate`: concise cost picture showing the approved set stays within budget.
- `continuation_status`: set this to exactly `approved_pending_packetization`.

## Write `workflow/scope_summary.json`

Write `workflow/scope_summary.json` with these exact keys:

- `date_alignment`: confirm March 17-23, 2022 coverage and how the selected cities fit that span.
- `ohio_city_count_check`: confirm the approved set contains at least three Ohio cities.
- `pet_friendly_notes`: cite the lodging rule evidence that kept the selected stays pet-friendly or pet-permitted.
- `cuisine_coverage`: map American, Mediterranean, Chinese, and Italian coverage to the selected restaurant rows.
- `no_flight_confirmation`: state that the approved transportation set is driving-only and that `search-flights` was not used.
- `review_trace`: brief approval notes showing why the selected Ohio sequence won and where non-selected options were parked.

## Continue the Ohio Roadtrip Workflow

Treat `workflow/working_set_record.json` as the approved working record. Hand only `workflow/working_set_record.json` and `workflow/scope_summary.json` forward for the next packetization step unless a required dataset-backed field is missing.

## Ohio Roadtrip Stop Condition

Stop this stage when both workflow files exist, all keys above are present, `continuation_status` is `approved_pending_packetization`, `non_selected_candidates` is populated, and `/app/output/itinerary.json` is still unwritten.
