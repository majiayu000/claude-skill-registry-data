---
name: scrapy
description: |
  Scrapy — framework Python de crawling web massif (framework officiel, pas un simple fetcher).
  Spiders déclaratifs, pipelines, middlewares, autothrottle, cache HTTP, exports JSON/CSV.
  Exposé comme serveur MCP #10 de PariScore (4 outils : list_spiders, crawl, crawl_to_json, check_robots).
  Use when: user asks to crawl a whole site/domain (pas juste 1 page), bulk-scrape paginated data,
  build a recurring data pipeline from an authorized source, backfill historical data from a partner,
  extract thousands of items with dedup/validation pipelines.
  Triggers: "scrapy", "crawl site", "bulk scrape", "spider", "crawl paginated", "data pipeline",
  "backfill history", "bulk extraction", "crawl league", "crawl season", "crawl standings".

  Don't use when: target is a single page (use scrapling Fetcher — faster), target is protected
  by Cloudflare/Datadome and you're authorized (use scrapling StealthyFetcher — anti-detection),
  target is a known API endpoint (use the sport-specific MCP/service), target is a third-party
  site WITHOUT authorization and PariScore monetizes (refused by default — see garde-fous).

  Requires: Python ≥ 3.10, `scrapy` installé (déjà fait). Aucune clé API requise.
license: BSD-3-Clause
metadata:
  author: Zyte (lib ex-Scrapinghub) / pariscore-cto (intégration)
  version: "2.17.0"
  source: https://github.com/scrapy/scrapy
---

# Scrapy — Framework de crawling massif + MCP natif

> **Rôle** : Crawler des sites entiers (des dizaines à milliers de pages) avec spiders
> déclaratifs, pipelines de validation/dédup, autothrottle, cache HTTP, exports structurés.
> Complémentaire de Scrapling : Scrapy = bulk, Scrapling = ciblé/stealth.

## ⚖️ Garde-fous LÉGAUX (OBLIGATOIRES)

Scrapy est encore plus puissant que Scrapling (bulk par nature) — donc le risque juridique
est plus élevé si mal utilisé. **Toujours appliquer** la procédure du skill `metier-scraping-websearch` :

1. **`robots.txt`** — le wrapper MCP expose `check_robots` ; l'appeler AVANT tout nouveau domaine.
2. **`ROBOTSTXT_OBEY=True`** par défaut dans `scrapy_project/pariscore_scrapy/settings.py` (vérifié).
3. **ToS** + **données sous licence** → API officielle obligatoire (ATP/WTA → Sportradar).
4. **Politesse** — `DOWNLOAD_DELAY=1.0`, `AUTOTHROTTLE_ENABLED=True`, `CONCURRENT_REQUESTS_PER_DOMAIN=2`.
5. **Cadre commercial** — PariScore monétise → risque asymétrique, exiger une autorisation explicite.

**✅ LÉGITIME** : site partenaire licencié, données publiques (RSS/Wikipedia/fbref public),
sitemap autorisé, backfill d'historique sur un contrat API trop juste en quota.

**❌ REFUSÉ PAR DÉFAUT** : crawl massif d'un site tiers qui bloque l'extraction, sans
autorisation, pour réinjecter dans un produit commercial. Demander confirmation explicite.

## Scrapy vs Scrapling — quand utiliser quoi

| Critère | **Scrapy** | **Scrapling** |
|---------|-----------|---------------|
| Scope | Site entier (milliers de pages) | 1 à quelques pages |
| Pattern | Spider déclaratif + pipeline | Appel unitaire `Fetcher.get()` |
| Anti-bot | ❌ Nu (middleware à ajouter) | ✅ Built-in (Camoufox stealth) |
| Bulk/dedup | ✅ Pipelines natifs | ❌ Manuel |
| MCP | Via wrapper (4 outils) | Natif (10 outils) |
| Latence/page | ~0.5-2s (async massif) | 1-60s selon mode |

**Règle** : Scrapy pour le volume + la régularité (cron, sitemap, pagination). Scrapling pour
le ponctuel + le protégé. Les deux coexistent dans PariScore.

## Structure du projet Scrapy

```
scrapy_project/
├── scrapy.cfg                                    # config (default settings module)
└── pariscore_scrapy/
    ├── __init__.py
    ├── settings.py                               # ROBOTSTXT_OBEY, autothrottle, cache, reactor
    ├── items.py                                  # DemoQuoteItem, TeamLogoItem (typed containers)
    ├── middlewares.py                            # hooks request/response (UA rotation, proxy)
    ├── pipelines.py                              # NormalizeFieldsPipeline, DedupPipeline
    └── spiders/
        ├── __init__.py
        └── demo_quotes.py                        # spider de démo (quotes.toscrape.com sandbox)
```

## Setup (déjà fait)

```bash
pip install scrapy                                 # déjà installé (2.17.0)
# Pas de `scrapy install` (contrairement à Scrapling) — pas de binaire navigateur requis
# pour le mode statique. Pour scrapy-playwright (rendu JS), voir "Extensions" plus bas.
```

## Usage CLI direct

Toujours `cd scrapy_project/` d'abord (scrapy.cfg doit être trouvé) :

```bash
cd scrapy_project

# Lister les spiders
scrapy list

# Lancer un spider
scrapy crawl demo_quotes

# Avec arguments spider
scrapy crawl demo_quotes -a tag=love

# Exporter vers JSON
scrapy crawl demo_quotes -o quotes.json

# Override un setting (limiter à 50 items pour test)
scrapy crawl demo_quotes -s CLOSEDSPIDER_ITEMCOUNT=50 -o quotes.json
```

## Usage via serveur MCP (depuis l'agent ZCode)

Le serveur MCP Scrapy (déclaré dans `.mcp.json`) expose **4 outils** :

| Outil | Description | Quand |
|-------|-------------|-------|
| `list_spiders` | Liste les spiders disponibles | Avant tout crawl, pour vérifier le nom |
| `crawl` | Lance un spider, retourne items inline (max 200) | Tests, petits crawls, debug |
| `crawl_to_json` | Lance un spider, exporte vers fichier JSON persistant | Crawls massifs (>200 items) |
| `check_robots` | Vérifie robots.txt d'une URL | **AVANT** tout nouveau domaine |

**Architecture du wrapper** : chaque `crawl` lance un **subprocess frais** `scrapy crawl <spider>`.
C'est nécessaire car le reactor Twisted de Scrapy n'est pas réentrant — un process long-lived
qui appellerait `CrawlerProcess.crawl()` en boucle casserait au 2e crawl. Le subprocess isole
parfaitement le reactor. Trade-off : ~2s de startup par crawl (négligeable vs la durée du crawl).

### Exemple MCP — crawl inline (petit)
```json
{
  "name": "crawl",
  "arguments": {
    "spider": "demo_quotes",
    "limit": 50,
    "log_level": "WARNING"
  }
}
```
Retourne `{spider, returncode, item_count, items: [...], stats}`.

### Exemple MCP — crawl massif vers fichier
```json
{
  "name": "crawl_to_json",
  "arguments": {
    "spider": "demo_quotes",
    "output": "data/scrapy-exports/quotes-all.json"
  }
}
```
Retourne `{spider, output, output_size_bytes, returncode, stats}`.

## Écrire un nouveau spider (template)

```python
# scrapy_project/pariscore_scrapy/spiders/standings_spider.py
import scrapy
from pariscore_scrapy.items import PariscoreScrapyItem


class StandingsSpider(scrapy.Spider):
    """Exemple — classement d'une ligue (source publique autorisée)."""

    name = "standings"
    allowed_domains = ["example-partner.com"]

    def __init__(self, league=None, season=2026, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not league:
            raise ValueError("Argument -a league=<slug> requis")
        self.start_urls = [f"https://example-partner.com/{league}/{season}/standings"]

    def parse(self, response):
        for row in response.css("table.standings tr"):
            item = PariscoreScrapyItem()
            item["team_name"] = row.css("td.team::text").get()
            item["url"] = response.url
            yield item

        # Pagination
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
```

Pour activer les pipelines (normalisation + dédup), décommenter dans `settings.py` :
```python
ITEM_PIPELINES = {
    "pariscore_scrapy.pipelines.NormalizeFieldsPipeline": 100,
    "pariscore_scrapy.pipelines.DedupPipeline": 200,
}
```

## Settings notables (scrapy_project/pariscore_scrapy/settings.py)

| Setting | Valeur | Raison |
|---------|--------|--------|
| `ROBOTSTXT_OBEY` | `True` | Politesse par défaut (politique projet) |
| `USER_AGENT` | `pariscore-scrapy-bot/1.0 (+contact)` | Identification honnête |
| `CONCURRENT_REQUESTS_PER_DOMAIN` | `2` | Ne pas saturer la source |
| `DOWNLOAD_DELAY` | `1.0` | 1 req/sec/domaine |
| `AUTOTHROTTLE_ENABLED` | `True` | Adaptation auto à la charge serveur |
| `HTTPCACHE_ENABLED` | `True` (24h) | Dev-friendly : pas de re-hit en re-run |
| `RETRY_TIMES` | `2` | Conservateur (ne pas hammer) |
| `asyncioreactor.install()` | — | Compat Windows + asyncio middlewares |

**Override ponctuel** via `-s KEY=VALUE` ou var env `KEY=VALUE` (le wrapper MCP supporte les deux).

## Extensions futures (pas installées par défaut)

- **`scrapy-playwright`** — rendu JS via Playwright (pour SPAs). Installer via
  `pip install scrapy-playwright` puis activer dans `DOWNLOAD_HANDLERS`. Pour les pages
  Cloudflare-protégées, **préférer Scrapling StealthyFetcher** (Camoufox > Chromium).
- **`scrapy-rotating-proxies`** — rotation de proxies (à combiner avec un provider résidentiel).
- **Scrapyd** — serveur de crawl pour orchestrer des spiders en prod (deploy target dans scrapy.cfg).

## Limites & coûts

- **Latence startup** : ~2s par crawl (subprocess fresh). Pour du live/in-play, garder les APIs.
- **Pas d'anti-bot built-in** : Scrapy nu est détecté par Cloudflare/Datadome. Pour les sources
  protégées, utiliser Scrapling (StealthyFetcher) ou un middleware proxy+UA rotation.
- **Cache occupe de l'espace** : `scrapy_project/.scrapy/httpcache/` peut grossir. Le vider
  périodiquement (`rm -rf scrapy_project/.scrapy/httpcache/`).
- **Windows quirks** : paths avec `:` cassent `-o C:/abs/path` (scrapy le lit comme `path:format`).
  Le wrapper MCP gère ça en passant des chemins relatifs au cwd `scrapy_project/`.

## Anti-patterns

- ❌ Lancer un crawl sans avoir appelé `check_robots` sur le domaine au préalable.
- ❌ Mettre `ROBOTSTXT_OBEY=False` sans autorisation explicite documentée.
- ❌ Crawler en rafale (`CONCURRENT_REQUESTS_PER_DOMAIN=16`) — DoS involontaire + ban IP.
- ❌ Compter sur Scrapy pour passer Cloudflare → utiliser Scrapling StealthyFetcher à la place.
- ❌ Désactiver `AUTOTHROTTLE_ENABLED` sur une source qui ne t'appartient pas.
- ❌ Lancer `CrawlerProcess` en boucle dans un process long-lived (reactor non-réentrant → crash).
  Le wrapper MCP utilise subprocess par crawl pour ça.

## Fichiers de référence

- `scrapy_project/scrapy.cfg` — config déclarative
- `scrapy_project/pariscore_scrapy/settings.py` — tous les settings documentés
- `scrapy_project/pariscore_scrapy/spiders/demo_quotes.py` — spider template
- `scripts/scrapy-mcp-server.py` — wrapper MCP (4 outils, subprocess-isolé)
- `scripts/test-scrapy.py` — validateur (5 tests)
- `data/scrapy-tests/` — résultats JSON des tests
- `.mcp.json` — déclaration du serveur MCP Scrapy
- https://github.com/scrapy/scrapy — source officielle
- https://docs.scrapy.org — documentation

## Résultats de validation (2026-07-13)

| Test | Résultat | Détail |
|------|----------|--------|
| Scrapy CLI | ✅ | `scrapy version` → 2.17.0 |
| MCP handshake | ✅ | serverInfo `scrapy 1.0.0`, 4 outils exposés |
| `list_spiders` | ✅ | `demo_quotes` détecté |
| `crawl demo_quotes` | ✅ | 100 items, returncode 0, 10s |
| `check_robots` | ✅ | quotes.toscrape.com autorisé |
| `ROBOTSTXT_OBEY` | ✅ | `True` par défaut dans settings.py |

---

*Skill crawling PariScore — Scrapy 2.17.0 intégré comme serveur MCP #10.*
