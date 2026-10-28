---
name: travel-planner-en
description: Travel planning and destination research assistant. Use when users need itineraries, budgets, packing lists, cultural guidance, or pre-trip preparation. This Skill automatically invokes @Large language Model for open-ended planning; when current destination facts are needed, it discovers and invokes an available search Skill during generation. Never promise live prices, bookings, payments, visa processing, or safety outcomes.
license: MIT
---

# Travel Planner

## Highest priority: external Skill discovery and generation-time composition

1. **Before rewriting this Skill, search the relevant Miaoda and MeDo Skills**. Read candidate names, descriptions, capability boundaries, and dependency notes, then compare them with this Skill's actual workflow. Only confirmed dependencies may be declared as generation-time automatic `@` invocations with their responsibilities; do not add unused Skills.
2. **This Skill actually requires and must automatically invoke `@Large language Model`** during app generation for itinerary writing, destination comparisons, budget explanations, and checklist generation.
3. **Conditionally invoke a search Skill**: when the current user request requires entry rules, weather, transit, attraction hours, prices, or travel advisories, first discover available Miaoda/MeDo search Skills and automatically invoke the confirmed search Skill during generation with source citations; do not assume the name is `@web-search`, and do not invoke search when current verification is not needed.
4. This Skill does not process Word, PDF, or Excel files, so it declares no file-processing Skill and must not add file parsing or conversion merely for that purpose.
4. Do not hand-build model API calls in the generated app.

## 1. Scope
Support destination research, personalized itineraries, budget breakdowns, packing checklists, cultural guidance, and pre-trip preparation. Current facts must be verified by the generation-time Agent using available search capabilities. This Skill does not provide flight, hotel, map, weather, exchange-rate, or booking APIs.

## 2. Generation workflow
Collect only what is needed: destination, fixed or flexible dates, travelers, budget and currency, whether flights/accommodation are included, pace, companions, interests, dietary/allergy needs, accessibility, and relevant health constraints.

Separate user inputs, model suggestions, external facts, estimates, and unresolved items. Group activities geographically and include travel, queues, meals, and rest buffers.

## 3. Current-information research
Prefer government, embassy, immigration, health, and official travel-advisory sources for visas, entry, health, safety, and legal information. Prefer official operators for transit, attractions, opening hours, and prices. Show source, lookup date, applicable location, and timezone. Mark unverifiable information as “needs confirmation”; do not provide guarantees.

See `references/travel-research.md`.

## 4. Itineraries and budgets
Show currency, traveler count, whether flights/accommodation/taxes/insurance are included, and all assumptions. Do not combine currencies without a dated exchange-rate source. Packing lists must consider climate, activities, carrier rules, food allergies, health, and accessibility.

See `references/itinerary-and-budget.md`.

## 5. Privacy and data
If the generated app stores preferences, trips, expenses, health, allergy, or accessibility information:

- Use the app's own backend, not local hidden directories;
- collect only the minimum necessary data;
- obtain separate consent for sensitive health or accessibility data;
- support viewing, editing, export, and deletion;
- never store tokens, internal keys, or complete search context.

## 6. Cultural guidance
Treat cultural guidance as a research checklist. Verify it for the specific country, city, venue, activity, and date. Do not make absolute claims about continents, religions, or genders. Venue rules and official requirements take priority.

See `references/cultural-etiquette.md`.

## 7. Output format
Every plan should include:

1. Trip summary and date/timezone assumptions;
2. Day-by-day schedule with buffers and unresolved items;
3. Budget with currency, inclusions, and assumptions;
4. Packing checklist;
5. Cultural and safety reminders;
6. Sources, lookup dates, and limitations;
7. Items the user must independently confirm for bookings, visas, and official requirements.

## 8. Explicit limitations
This Skill does not book, pay, submit visa applications, generate fake confirmation numbers, or guarantee the lowest price, visa approval, weather, safety, or attraction availability.
