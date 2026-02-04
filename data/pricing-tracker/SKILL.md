---
name: pricing-tracker
description: "Tracks current pricing and availability across multiple retailers with price comparison. Use when user asks about 'price', 'how much', 'where to buy', 'pricing comparison', 'best deal', 'availability', or when orchestrator needs current market pricing data. Checks Amazon and category-specific retailers."
---

# Pricing Tracker

## Mission
Collecter prix actuel et disponibilité depuis multiples retailers (Amazon, sites spécialisés selon catégorie).

## Outils de Scraping

### Priorité 1: MCP Apify (Recommandé)
| Outil | Usage |
|-------|-------|
| `mcp__apify__call-actor` avec `apify/amazon-product-scraper` | Prix Amazon structuré (inclut prix, stock, shipping) |
| `mcp__apify__apify-slash-rag-web-browser` | Prix autres retailers (Decathlon, Darty, etc.) |

### Priorité 2: Fallback
| Outil | Usage |
|-------|-------|
| `WebFetch` | Si MCP échoue ou timeout (>2 min) |

**Avantages MCP Apify**:
- Amazon: Prix exact, stock, shipping en JSON structuré
- RAG Browser: Recherche + extraction prix en une seule requête

## Quick Summary
1. **Amazon**: MCP `apify/amazon-product-scraper` (ou WebFetch fallback)
2. **Autres retailers**: MCP `rag-web-browser` (ou WebFetch fallback)
3. Extract: prix, disponibilité, shipping, promos actives
4. Save comparison table JSON + cache 7j

## Inputs
- **product_name**: Nom produit
- **category**: Catégorie (pour sélectionner retailers appropriés)
- **amazon_url**: URL Amazon (optionnel)

## Outputs
- `pricing.json`: Tableau prix par retailer
- Cache 7j

## Dependencies
- data/category_specs.yaml (retailers par catégorie)
- Load `helpers/retailers.yaml` when scraping for patterns

## Workflow

### 1. Load retailers
```javascript
retailers = category_specs.yaml[category].retailers
// Example velo: ["decathlon.fr", "alltricks.fr", "probikeshop.fr"]
```

### 2. Scrape Amazon (if in retailers)
```javascript
**PRIMARY: MCP Apify**
mcp__apify__call-actor({
  actor: "apify/amazon-product-scraper",
  step: "call",
  input: {
    categoryOrProductUrls: [amazon_url],
    maxItems: 1
  }
})

mcp__apify__get-actor-output({
  datasetId: result.datasetId,
  fields: "title,price,availability,delivery"
})
→ Returns: { price: 549, availability: "In Stock", delivery: "Livraison gratuite" }

**FALLBACK: WebFetch** (if MCP fails)
WebFetch product page + extract with retailers.yaml selectors
```

### 3. Scrape other retailers (2-3)
```javascript
For each retailer:
  query = "{product_name} prix site:{retailer}"

  **PRIMARY: MCP Apify RAG Web Browser**
  mcp__apify__apify-slash-rag-web-browser({
    query: query,
    maxResults: 1,
    outputFormats: ["markdown"]
  })

  Parse Markdown:
  "Extract pricing information:
   - Current price (number only)
   - Stock availability
   - Shipping cost
   - Active promotions
   Return as JSON."

  **FALLBACK: WebFetch**
  WebFetch product page + extract with retailers.yaml selectors
```

### 4. Build comparison table
```javascript
{
  "product": product_name,
  "timestamp": now,
  "retailers": [
    {
      "name": "Amazon",
      "price": 549,
      "availability": "in_stock",
      "shipping": "Gratuit",
      "promo": null
    },
    {
      "name": "Decathlon",
      "price": 549,
      "availability": "in_stock",
      "shipping": "Gratuit en magasin",
      "promo": "-10% membres"
    }
  ],
  "best_price": 494.10,  // Decathlon with promo
  "best_retailer": "Decathlon"
}
```

### 5. Save + cache
- Save: `data/research_{timestamp}/{product}/pricing.json`
- Cache: `data/cache/pricing/{cache_key}.json` (7j TTL)

## Error Handling
- Retailer unavailable → Skip, continue with others
- Price not found → Mark as "N/A"
- Out of stock → Mark availability = false
- MCP timeout → Fallback to WebFetch automatically
