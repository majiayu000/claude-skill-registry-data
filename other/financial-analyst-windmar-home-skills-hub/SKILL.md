---
name: financial-analyst
description: Financial analysis and research workflows for market research, equity research, comparable companies, precedent transactions, and DCF valuation. Use when asked to build or critique DCF models, comps/precedents tables, competitor or strategy analysis, market sizing, or to deliver analyst-ready outputs in Excel, PowerPoint, or Markdown from CSV/Excel/SQL/API/web data.
---

# Financial Analyst

## Overview

Deliver industry-standard market research, equity research, comps, precedents, and DCF valuation with explicit assumptions, source citations, and polished outputs in Excel, PowerPoint, or Markdown.

## Quick Intake

- Confirm company name, ticker, industry, geography, currency, and units (USD millions, etc.).
- Confirm scope (DCF, comps, precedents, market sizing, competitive strategy, equity research memo) and output formats.
- Gather data sources (CSV/Excel/SQL/API/web) and ask for access details or files.
- Ask for missing inputs; if the user says proceed, use standard assumptions and list them explicitly.

## Core Workflows

### DCF Model

- Use `references/dcf.md` for standard structure and checks.
- Build a 5-year forecast, WACC via CAPM, and terminal value via Gordon Growth.
- Produce a valuation summary, sensitivity table, and assumptions table.
- Use `assets/templates/dcf-model-template.md` as a starting layout if a template helps.

### Comparable Companies

- Use `references/comps.md` for peer selection and table fields.
- Build a comps table with key operating metrics and trading multiples.
- Call out outliers and justify adjustments or exclusions.
- Use `assets/templates/comps-template.csv` for the table skeleton.

### Precedent Transactions

- Use `references/precedents.md` for deal filters and table fields.
- Build a precedents table with deal values, premiums, and transaction multiples.
- Note deal context (strategic vs. financial buyer, control premium, timing).
- Use `assets/templates/precedents-template.csv` for the table skeleton.

### Market Research

- Use `references/market-research.md` for market sizing and structure.
- Provide TAM/SAM/SOM with both top-down and bottom-up triangulation when possible.
- Cite sources and state any conversions or extrapolations.
- Use `assets/templates/market-research-template.md` for the memo layout.

### Competitive Strategy and Key Competitors

- Use `references/competitive-strategy.md` for frameworks and output structure.
- Identify direct, adjacent, and substitute competitors with brief rationale.
- Assess differentiation, moats, pricing power, and distribution advantages.
- Use `assets/templates/competitive-strategy-template.md` for the memo layout.

### Equity Research Memo

- Use `references/equity-research.md` for the memo structure.
- Present a clear thesis, valuation summary, catalysts, and risks.
- Keep conclusions linked to data and comps/DCF outputs.
- Use `assets/templates/er-memo-template.md` as a starting outline.

## Output Standards

- Provide an assumptions table for every model or valuation.
- Include units, currency, and as-of dates on every table.
- Keep formulas transparent in Excel outputs and document key drivers in Markdown.
- Provide a slide outline when PowerPoint is requested via `assets/templates/ppt-outline.md`.

## Resource Index

- References: `references/dcf.md`, `references/comps.md`, `references/precedents.md`, `references/market-research.md`, `references/competitive-strategy.md`, `references/equity-research.md`
- Assets: `assets/templates/dcf-model-template.md`, `assets/templates/comps-template.csv`, `assets/templates/precedents-template.csv`, `assets/templates/market-research-template.md`, `assets/templates/competitive-strategy-template.md`, `assets/templates/er-memo-template.md`, `assets/templates/ppt-outline.md`
