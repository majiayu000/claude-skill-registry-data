---
name: specs-collector
description: "Collects complete technical specifications from manufacturer sites, Amazon, and review sites with schema validation. Use when user asks to 'get specs', 'collect specifications', 'find technical details', 'product specifications', or when orchestrator needs detailed product specs. Validates data completeness against category requirements."
---

# Specs Collector

## Mission
Collecter les spécifications techniques complètes d'un produit depuis multiples sources (manufacturer, Amazon, sites reviews), valider contre schema catégorie, sauver en JSON structuré.

## Quick Summary
1. Détecte catégorie produit (ou utilise fournie)
2. Charge specs requises depuis category_specs.yaml
3. Scrape specs depuis 3 sources: manufacturer, Amazon, review site
4. Merge + déduplique + normalise
5. Valide complétude (% specs requises obtenues)
6. Sauve data/research_{timestamp}/{product}/specs.json + cache

## Inputs
- **product_name**: Nom produit (ex: "Dyson V15 Detect")
- **category**: Catégorie (electromenager, auto, sport, velo)
- **manufacturer_url**: URL site manufacturer (optionnel, auto-détecté)
- **amazon_url**: URL Amazon (optionnel, auto-détecté)
- **cache_check**: Boolean - vérifier cache avant fetch (default: true)

## Outputs
- `data/research_{timestamp}/{product}/specs.json`: Specs structurées
- `data/cache/specs/{cache_key}.json`: Cache 7 jours
- `data/research_{timestamp}/{product}/specs_log.json`: Log sources + complétude

## Dependencies
- data/category_specs.yaml
- Load `helpers/scraping_patterns.md` when scraping for detailed patterns
- Load `helpers/parsers.js` when parsing HTML tables

## Workflow Details
Load `helpers/scraping_patterns.md` when executing collection for detailed scraping patterns.

## Error Handling
- Source inaccessible → Continue avec autres sources
- Specs incomplètes (< 70%) → Flag warning, sauve données partielles
- Parsing échoue → Raw HTML saved pour debug
