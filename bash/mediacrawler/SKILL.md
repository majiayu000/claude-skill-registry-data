---
name: mediacrawler
description: >-
  MediaCrawler — crawler multi-plateforme de médias sociaux chinois (Xiaohongshu,
  Douyin, Kuaishou, Bilibili, Weibo, Tieba, Zhihu) basé sur Playwright (61k stars,
  MIT). Clone dans E:\MediaCrawler, venv uv, navigateurs Playwright dans
  E:\MediaCrawler\browsers. WebUI FastAPI (port 8080). Stockage : csv, json,
  jsonl, excel, sqlite, mysql, postgres, mongodb.
  Use when: l'utilisateur demande de crawler Xiaohongshu/Douyin/Bilibili/Weibo,
  récupérer des posts/comments par mot-clé, par ID ou par créateur, crawler avec
  login QR/phone/cookie, nuage de mots des commentaires, ou lancer le WebUI
  MediaCrawler. Triggers: "mediacrawler", "xiaohongshu", "douyin", "weibo crawl",
  "sina weibo", "bilibili crawl", "xhs", "crawl chinese social".
  Don't use when: cible sportive (football/tennis/CS2/MMA — utiliser les skills
  sportifs/scrapling/scrapy), cible une seule page statique (plain fetch), ou
  source tierce SANS autorisation que PariScore monétiserait (refusé par
  défaut — voir garde-fous plus bas).
---

# MediaCrawler — Crawler Médias Sociaux (Xiaohongshu, Douyin, Bilibili, Weibo...)

## Installation (faite le 2026-08-11)

| Élément | Valeur |
|---|---|
| Clone | `E:\MediaCrawler` (depth 1, branche main) |
| Runtime | Python 3.11.15 via `uv sync` (90 paquets, venv `E:\MediaCrawler\.venv`) |
| Navigateurs | Playwright chromium v1228 + headless shell dans `E:\MediaCrawler\browsers` |
| CLI | `E:\MediaCrawler\main.py` (typer), WebUI `E:\MediaCrawler\api\main.py` (FastAPI :8080) |

⚠️ **Variable d'env REQUISE** : `PLAYWRIGHT_BROWSERS_PATH=E:\MediaCrawler\browsers`
(sinon Playwright cherche dans `%LOCALAPPDATA%\ms-playwright` et échoue).

## Commandes

```cmd
cd /d E:\MediaCrawler&& set PLAYWRIGHT_BROWSERS_PATH=E:\MediaCrawler\browsers&& uv run main.py --platform xhs --lt qrcode --type search --keywords "mot-clé1,mot-clé2" --save_data_option jsonl
```

- `--platform` : `xhs` (Xiaohongshu) | `dy` (Douyin) | `ks` (Kuaishou) | `bili` (Bilibili) | `wb` (Weibo) | `tieba` | `zhihu`
- `--type` : `search` (par mots-clés) | `detail` (`--specified_id`) | `creator` (`--creator_id`)
- `--lt` : `qrcode` | `phone` | `cookie` (`--cookies "..."`)
- `--get_comment yes --get_sub_comment no --max_comments_count_singlenote 50`
- `--save_data_option` : csv|db|json|jsonl|sqlite|excel|mongodb|postgres (défaut jsonl, dossier `data/`)
- `--headless yes`, `--max_concurrency_num 3`, proxy : `--enable_ip_proxy yes --static_proxy_url http://u:p@host:port`

WebUI : terminal 1 `uv run uvicorn api.main:app --port 8080 --reload` → http://localhost:8080.
Frontend dev : `cd webui && npm install && npm run dev` (port 5173, proxy /api → 8080).

Config par défaut : `config/base_config.py` (plateformes sur lesquelles on a déjà
un compte : `PLATFORMS`, flags commentaires). Login QR : ouvrir l'app du réseau
pour scanner le QR.

## Pièges connus

1. **CMD** : toujours `cd /d` (changer de lecteur), jamais de syntaxe Bash.
2. `PYTHONUTF8=1` peut être nécessaire pour les flux Unicode lourds.
3. Le 1er run de matplotlib génère le fontManager (lent, une fois).
4. Login requis par plateforme : qrcode → scanne avec l'app mobile (déjà
   connecté à un compte). Cookie login : coller les cookies du navigateur.
5. xhs/dy supportent le mode CDP (connexion à Chrome local) — voir
   `config/base_config.py` si souci de Webdriver.
6. Données par défaut dans `E:\MediaCrawler\data\` (jsonl) — ne pas commit.

## Garde-fous légaux (disclaimer officiel du projet + règles PariScore)

- Usage **strictement pédagogique/recherche**. Le README officiel interdit
  l'usage commercial et le crawling massif ; commercial use prohibited.
- Ne crawler que des sources **autorisées** : si la cible interdit le scraping
  ou que PariScore monétiserait les données, **refuser par défaut** (même
  politique que scrapling/scrapy).
- Ne pas crawler de contenus privés, personnels ou protégés (login d'un compte
  tiers, messages privés, données perso).
- Ne pas contourner de blocage agressif (Cloudflare/Datadome) sans autorisation.
- Les comptes utilisés doivent appartenir à l'utilisateur.

## Liens utiles

- Repo : https://github.com/NanmiCoder/MediaCrawler (README_en.md)
- Guide stockage : `docs/data_storage_guide.md` ; FAQ : https://nanmicoder.github.io/MediaCrawler/