---
name: huashu-html-to-pptx-conversion
description: "PPTX generation from web data payloads. Use when programmatically generating PowerPoint presentations from application data."
version: "2.0.0"
verified_date: 2026-04-29
category: core
---

# Data-to-PPTX Generation (Redesigned)

## Purpose
Programmatically generate PowerPoint (PPTX) presentations from underlying application data state, bypassing the DOM entirely.

## When to Use This Skill
Use when:
- Exporting dashboard analytics, tables, or structured reporting data to PowerPoint.
- Mapping directly from JSON state to `PptxGenJS` models.

Do NOT use when:
- Attempting to parse, scrape, or translate HTML/DOM elements into PPTX coordinates.

## Phase 1: Data-to-Presentation Mapping
1. **Abandon DOM Scraping**: Do not attempt to map raw DOM nodes or CSS styles to `PptxGenJS` layouts.
2. **Data Extraction**: Extract the raw JSON payload powering the dashboard components.
3. **Transformation Pipeline**: Generate a pure JavaScript transformation function that translates the JSON data array directly into structured `PptxGenJS` slide models.
4. **Explicit Coordinates**: Define PPTX component coordinates (x, y, w, h) purely via mathematical offsets based on data arrays, completely ignoring visual HTML layouts.

## Output Format / Delivery
- JavaScript transformation functions translating JSON payloads to direct PptxGenJS slide models.

## Behavior Rules
1. Never use `document.querySelector` or DOM traversal to build PPTX slides.
2. If asked to convert raw HTML elements to PPTX, self-reject immediately.

## Maintenance Notes
- Complete redesign from v1. Banned DOM-to-PPTX translation due to high failure rate, replacing it with strict JSON-to-PptxGenJS data modeling.