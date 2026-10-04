---
name: ruview
description: >-
  RuView (ruvnet) — plateforme de sensing WiFi (WiFi DensePose) : présence,
  respiration, rythme cardiaque, chutes, pose 17 keypoints à travers les murs,
  via CSI ESP32 (MIT, 1463 tests). Installé dans E:\RuView (clone + venv uv
  Python 3.11 + paquet ruview/wifi-densepose + MetaHarness npm @ruvnet/ruview).
  Use when: l'utilisateur demande du sensing WiFi, présence à travers les murs,
  signes vitaux sans contact, pose estimation par WiFi, ESP32 CSI, module edge
  (fall-detect, sleep-apnea, occupant), Home Assistant bridge, MetaHarness ruview,
  "RuView", "wifi densepose", "CSI", "see through walls", "contactless vitals".
  Triggers: "ruview", "wifi sensing", "densepose", "CSI ESP32", "presence detection",
  "through-wall", "vital signs", "home assistant sensing".
  Don't use when: tâche web classique (scrapling/scrapy/playwright), données
  sportives (skills sportifs), ou analyse RF nécessitant du matériel non présent.
---

# RuView — WiFi Sensing / WiFi DensePose (ruvnet)

## Installation (faite le 2026-08-11)

| Élément | Valeur |
|---|---|
| Clone | `E:\RuView` (depth 1, branche master — ~2935 fichiers) |
| Python | venv uv `.venv` (CPython 3.11.15) + `ruview[client]` (wheel PyO3) |
| npm | MetaHarness `@ruvnet/ruview@0.3.1` (via npx, PAS d'install persistante) |
| Matériel | NON présent — sensing CSI réel exige ESP32-S3 ($9) + routeur |

⚠️ **Bug upstream patché localement** : les wheels PyPI 2.0.0a1 sont incohérentes
(ruview attend `__rust_version__` absent de wifi_densepose). Fix appliqué dans
`.venv\Lib\site-packages\ruview\__init__.py` (getattr fallback). Ne pas
réinstaller sans re-patch. De plus les wheels 2.0.0a1 n'exposent QUE
`WiFiDensePose` (+ `client.*`) — les `BreathingExtractor`/`HeartRateExtractor`
de la doc ne sont PAS dans le wheel publié (stale) ; ils existent dans le code
source `v2/` (Rust, non compilé ici).

## Usage (sans matériel)

```cmd
cd /d E:\RuView && .venv\Scripts\python.exe -c "from wifi_densepose import WiFiDensePose; m = WiFiDensePose(); print(m)"
```

- Vérification pipeline déterministe (README) : `python archive/v1/data/proof/verify.py` (répertoire archive/v1 = DEPRECATED, vérifier compat)
- Docker demo (données simulées, ~2 Go) : `docker pull ruvnet/wifi-densepose:latest && docker run -p 3000:3000 ruvnet/wifi-densepose:latest`
- MetaHarness (agents) dans le repo : `npx -y @ruvnet/ruview@0.3.1 doctor|guidance|brain|agent|claim-check|verify|mcp start`

## Options matérielles (si un jour)

| Option | Coût | Capacités |
|---|---|---|
| ESP32-S3 + Cognitum Seed | ~$140 | Tout (pose 17 kpts, vital signs, catalogue 105 cogs, vector store, MCP proxy) |
| Mesh 3-6× ESP32-S3 | ~$54 | Idem sans mémoire persistante |
| ESP32-C6 devkit | ~$10 | CSI Wi-Fi 6, TWT (recherche) |
| LAN laptop | $0 | RSSI only : présence/mouvement grossier |

Flash : `python -m esptool --chip esp32s3 ... write_flash` (firmware `firmware/esp32-csi-node/`), puis `provision.py --ssid --password --target-ip`. Serveur : sensing server + WebUI demo `https://ruvnet.github.io/RuView/`.

## Pièges connus

1. **CMD** : `cd /d` obligatoire ; jamais de syntaxe Bash.
2. Faux espoir : « 100% présence » = ancien chiffre RETRACTÉ (vrai : 82,3% triplet temporel) ; pose 17 kpts on-device = modèle « first-cut » PCK@20 = 3,0% (cible ≥ 35%, stub `confidence=0`) — le vrai SOTA est le benchmark MM-Fi (82,69% torso-PCK@20, modèle séparé Hugging Face). Toujours citer le niveau de maturité (ADR-187).
3. Le wheel PyPI est stale vs repo main (API réduite). Build Rust complet = `v2/` (rust-toolchain.toml, ~long) — non installé ici (pas de matériel, C: saturé).
4. Ne PAS cloner plus profond que depth 1 sans besoin (repo gros).

## Garde-fous (confidentialité + légal)

- Le sensing sans caméra contourne les règles vidéo — ne PAS l'utiliser pour
  surveiller des personnes sans consentement (domicile, soins, lieu de travail).
- Données de santé (rythme cardiaque/respiration/apnée) = données sensibles en
  Europe (RGPD art. 9) — jamais de surveillance de tiers sans base légale.
- Le README exige la transparence sur les claims (« honest labeling », ADR-187) :
  ne pas amplifier la précision des modèles.

## Liens utiles

- Repo : https://github.com/ruvnet/RuView ; docs ADR : `docs/adr/`
- Modèles : https://huggingface.co/ruvnet/wifi-densepose-pretrained · /ruvnet/wifi-densepose-mmfi-pose
- Wheel PyPI : `pip install ruview` / `wifi-densepose` ; crate Rust : `wifi-densepose-ruvector`