---
name: scrapling
description: |
  Scrapling — framework Python de web scraping adaptatif avec 3 fetchers gradués
  (statique / dynamique / stealth anti-détection) + serveur MCP natif (10 outils).
  Use when: user asks to scrape a page that Playwright nu ne passe pas, fetch a JS-rendered
  page, bypass Cloudflare/Datatome/Akamai on an AUTHORIZED source, extract structured data
  from a protected page, capture a screenshot headless, scrape with realistic fingerprint.
  Triggers: "scrapling", "stealth fetch", "bypass cloudflare", "camoufox", "fetch protected",
  "scrape anti-bot", "realistic fingerprint", "page dynamique", "rendu JS".

  Don't use when: target is httpbin/standard HTML (use plain fetch/curl), target is a known
  API endpoint (use the sport-specific service/MCP), target is a third-party site WITHOUT
  authorization and PariScore monetizes the data (see garde-fous below — refusé par défaut).

  Requires: Python ≥ 3.10, `scrapling[fetchers,ai,shell]` installé, `scrapling install` exécuté
  (Camoufox + Playwright binaires). Aucune clé API requise pour l'usage local.
license: MIT
metadata:
  author: D4Vinci (lib) / pariscore-cto (intégration)
  version: "0.4.11"
  source: https://github.com/D4Vinci/Scrapling
---

# Scrapling — Scraping adaptatif 3 modes + MCP natif

> **Rôle** : Scraper des pages web avec 3 niveaux de furtivité gradués, du simple HTTP statique
> jusqu'au navigateur Firefox patché C++ (Camoufox) qui passe les gates anti-bot modernes.
> Exposé comme **serveur MCP #9** de PariScore (10 outils) — l'agent peut l'appeler directement.

## ⚖️ Garde-fous LÉGAUX (OBLIGATOIRES — lire avant tout usage)

Scrapling est un outil **dual-use**. Avant toute collecte, appliquer la procédure du skill
`metier-scraping-websearch` :

1. **`robots.txt`** — la cible autorise-t-elle le chemin visé ?
2. **ToS** — la cible autorise-t-elle l'accès automatisé ?
3. **Données sous licence** — propriétaires (ATP/WTA, Sportradar) ? → API officielle.
4. **Autorisation** — PariScore a-t-il une licence/contrat avec la source ?
5. **Cadre commercial** — PariScore monétise → risque juridique asymétrique.

**✅ LÉGITIME** : tes propres sites, partenaires licenciés, données publiques (RSS/Wikipedia),
recherche sécurité, CTF, sources où tu as une autorisation explicite.

**❌ REFUSÉ PAR DÉFAUT** : bypass furtif contre un tiers qui a délibérément déployé un WAF
(Cloudflare/Datadome) pour refuser l'extraction, pour un usage commercial, sans autorisation.
Demande confirmation explicite à l'utilisateur + nature de l'autorisation avant d'agir.

## When not to use

- **HTML statique simple** — Utiliser `fetch()` ou `curl` directement
- **API endpoint connu** — Utiliser le skill sportif ou MCP correspondant
- **Site sans WAF** — `Fetcher` suffit, pas besoin de StealthyFetcher
- **Données sous licence** — Utiliser l'API officielle (Sportradar, ATP/WTA)
- **Scraping massif** — Utiliser `scrapy` (framework dédié)
- **Site tiers sans autorisation** — REFUSÉ par défaut (voir garde-fous)

## Les 3 fetchers (à choisir selon la résistance de la cible)

| Mode | Classe | Tech | Quand l'utiliser | Latence |
|------|--------|------|------------------|---------|
| **Statique** | `Fetcher` / `AsyncFetcher` | `curl_cffi` (TLS fingerprinting, JA3/JA4) | HTML statique, APIs JSON, pages sans WAF agressif. Bypass déjà les détections TLS basiques. | ~1-2s |
| **Dynamique** | `DynamicFetcher` | Playwright (Chromium) | Pages SPA / JS-rendered (React/Vue). PAS pour Cloudflare — Chromium est détecté. | ~30-60s |
| **Stealth** | `StealthyFetcher` | **Camoufox** (Firefox patché C++) | Pages protégées (Cloudflare Turnstile, Datadome, Akamai). Fingerprint consistant, `humanize=True` pour les mouvements souris. | ~30-60s |

**Règle de progression** : toujours commencer par `Fetcher` (le moins coûteux). Si bloqué (403,
challenge JS), monter à `DynamicFetcher`. Si toujours bloqué (Turnstile, Datadome), `StealthyFetcher`.

## Setup (déjà fait dans ce projet)

```bash
# Installation (déjà effectuée)
pip install "scrapling[fetchers,ai,shell]"   # parser + 3 fetchers + MCP server + CLI shell
scrapling install                            # télécharge Camoufox + Playwright binaires

# Test de validation (déjà exécuté, voir data/scrapling-tests/)
python scripts/test-scrapling.py             # 3 modes sur cibles de référence
```

## Usage Python direct (scripts/)

### Mode statique — Fetcher
```python
from scrapling.fetchers import Fetcher

page = Fetcher.get(
    "https://httpbin.org/get",
    stealthy_headers=True,      # UA + headers réalistes (Chrome random OS)
    follow_redirects=True,
    timeout=20,
)
print(page.status)             # 200 (int)
data = page.json()             # parse le body JSON
text = page.get_all_text()     # texte nettoyé
# Sélecteurs adaptatifs (le parser apprend des changements de structure)
titles = page.css("h1")        # liste d'éléments
first_h1 = page.find("h1")     # premier match
```

### Mode dynamique — DynamicFetcher (Playwright)
```python
from scrapling.fetchers import DynamicFetcher

page = DynamicFetcher.fetch(
    "https://spa-site.com/",
    headless=True,
    network_idle=True,         # attend fin du réseau (JS rendu)
    wait_selector="main",      # attend qu'un sélecteur apparaisse
    timeout=60000,
)
```

### Mode stealth — StealthyFetcher (Camoufox, anti-détection)
```python
from scrapling.fetchers import StealthyFetcher

# Capture screenshot avant fetch via page_action callback
def screenshot_before(page):
    page.screenshot(path="proof.png", full_page=True)
    return page

page = StealthyFetcher.fetch(
    "https://protected-site.com/",
    headless=True,
    humanize=True,             # mouvements souris humains (anti-CF comportemental)
    os_randomize=True,         # fingerprint OS cohérent aléatoire
    solve_cloudflare=True,     # résout automatiquement les challenges Cloudflare JS
    network_idle=True,
    wait_selector="body",
    timeout=90000,
    page_action=screenshot_before,   # callback exécuté dans le contexte Playwright
)
```

## Usage via serveur MCP (depuis l'agent ZCode)

Le serveur MCP Scrapling (déclaré dans `.mcp.json`) expose **10 outils** :

| Outil | Description |
|-------|-------------|
| `get` | GET HTTP statique sur une URL (Fetcher + curl_cffi) |
| `bulk_get` | GET statique sur un groupe d'URLs |
| `fetch` | Ouvre un navigateur Playwright pour fetch une URL (rendu JS) |
| `bulk_fetch` | Playwright sur plusieurs URLs simultanément |
| `stealthy_fetch` | **Camoufox** — fetch furtif (passe Cloudflare/Datadome) |
| `bulk_stealthy_fetch` | Camoufox sur plusieurs URLs |
| `open_session` | Ouvre une session navigateur persistante (réutilisable) |
| `close_session` | Ferme une session persistante |
| `list_sessions` | Liste les sessions actives |
| `screenshot` | Capture une page via une session existante |

Le MCP est auto-démarré par le client (ZCode/Claude Code/opencode). Pour test manuel :
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' | scrapling mcp
```

## API Scrapling — quick reference

L'objet `Response` retourné par tous les fetchers (type `scrapling.engines.toolbelt.custom.Response`) :

| Attribut/méthode | Type | Description |
|------------------|------|-------------|
| `.status` | `int` | Code HTTP (200, 403, …) |
| `.text` | `str` | Body texte brut |
| `.body` | `bytes` | Body bytes |
| `.json()` | `dict/list` | Parse le body en JSON |
| `.html_content` | `str` | HTML source |
| `.headers` | `dict` | Headers de réponse |
| `.url` | `str` | URL finale (après redirects) |
| `.cookies` | `dict` | Cookies |
| `.get_all_text()` | `str` | Texte nettoyé (sans balises) |
| `.css(selector)` | `list[Adaptor]` | Sélecteur CSS → éléments |
| `.find(tag)` / `.find_all(tag)` | `Adaptor` / `list` | BeautifulSoup-like |
| `.xpath(expr)` | `list[Adaptor]` | Sélecteur XPath |
| `.find_by_text(text)` | `Adaptor` | Match par texte |
| `.find_similar()` | `list[Adaptor]` | **Auto-healing** : éléments similaires au courant |
| `.prettify()` | `str` | HTML formaté |

**⚠️ L'objet Response n'a PAS** : `.status_code` (utiliser `.status`), `.type`, `.content`,
`.save_screenshot()`. Pour les screenshots, utiliser `page_action` callback (cf. mode stealth).

## Limites & coûts

- **Latence** : statique ~1-2s, dynamique/stealth ~30-60s (démarrage navigateur). Pour du
  live/in-play, garder les APIs dédiées (BSD, Odds API).
- **Camoufox binaire** : ~80 Mo, téléchargé une fois via `scrapling install`.
- **`solve_cloudflare=True`** : peut échouer sur Turnstile interactif (CAPTCHA image).
  Dans ce cas, proxy résidentiel + solver cloud (voir `.env` SCRAPLING_PROXY_URL).
- **Windows** : `scrapling install` peut afficher des warnings `publicsuffix.org` (DNS sandbox)
  — non bloquants.
- **Pas de retry/backoff built-in** : wrapper dans le service PariScore si besoin.

## Anti-patterns

- ❌ Démarrer directement en `StealthyFetcher` sur une page statique (latence ×30 inutile).
- ❌ Scraper en rafale sans rate-limit (DoS involontaire + ban IP).
- ❌ Compter sur `solve_cloudflare=True` pour Turnstile interactif (échec fréquent).
- ❌ Utiliser `DynamicFetcher` contre Cloudflare (Chromium détecté → utiliser `StealthyFetcher`).
- ❌ Stocker des screenshots de pages licenciées dans git (risque légal + taille repo).
- ❌ Bypass furtif sur un tiers sans autorisation pour un usage commercial (voir garde-fous).

## Fichiers de référence

- `scripts/test-scrapling.py` — validateur 3 modes (static/dynamic/stealth) + screenshot
- `data/scrapling-tests/` — résultats JSON + screenshots des tests
- `.mcp.json` — déclaration du serveur MCP Scrapling (entry `scrapling`)
- `requirements.txt` — pin `scrapling[fetchers,ai,shell]>=0.4.11`
- `.env.example` — variables optionnelles (proxy, solver cloud)
- https://github.com/D4Vinci/Scrapling — source officielle
- https://scrapling.readthedocs.io — documentation

## Résultats de validation (2026-07-13)

Test sur cibles publiques de référence :

| Mode | Cible | Statut | Latence | Résultat |
|------|-------|--------|---------|----------|
| Static (`Fetcher`) | httpbin.org/get | ✅ 200 | 1.75s | UA rendu Chrome 146 macOS (alors qu'on est sur Windows — fingerprinting OK) |
| Dynamic (`DynamicFetcher`) | creepjs (GitHub Pages) | ✅ 200 | 75s | Page rendue, JS exécuté |
| Stealth (`StealthyFetcher`) | creepjs (GitHub Pages) | ✅ 200 | 29-57s | `0% headless` / `0% stealth` = Camoufox invisible aux détecteurs |

---

*Skill scraping PariScore — Scrapling (D4Vinci) intégré comme serveur MCP #9.*
