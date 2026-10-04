---
name: osint-recon
description: "Reconnaissance passive sur un domaine : certificats, DNS, headers HTTP, stack technique. Utiliser pour l'analyse OSINT d'un domaine cible."
metadata: { "openclaw": { "emoji": "🕵️", "requires": { "bins": ["python3"] } } }
user-invocable: true
---

# OSINT Recon — Reconnaissance passive de domaine

## Déclencheur
- `/recon example.com`
- "reconnaissance sur le domaine X"
- "analyse le domaine de cette entreprise"

## Ce que fait ce skill
Effectue une reconnaissance 100% passive sur un domaine :
1. **Certificate Transparency** via crt.sh — découverte de sous-domaines
2. **DNS records** via DNS-over-HTTPS (Google) — A, AAAA, MX, TXT, NS, CNAME
3. **HTTP headers** — détection du serveur web, technologies
4. **Tech detection** — analyse Wappalyzer-like des headers et réponses

## Utilisation

```bash
source /opt/albert-ml/bin/activate
python3 scripts/recon.py --domain example.com
```

## Arguments
| Argument    | Description              | Défaut   |
|------------|--------------------------|----------|
| `--domain`  | Domaine cible            | (requis) |
| `--timeout` | Timeout HTTP en secondes | `15`     |

## Sortie
Objet JSON contenant :
- `domain` : domaine analysé
- `subdomains` : liste des sous-domaines découverts via crt.sh
- `dns_records` : enregistrements DNS par type
- `http_headers` : headers HTTP significatifs
- `tech_stack` : technologies détectées
- `ssl_info` : informations sur le certificat SSL

## Avertissement légal
Ce skill effectue uniquement de la reconnaissance **passive** :
- Consultation de bases de données publiques (crt.sh, DNS publics)
- Requête HTTP standard avec User-Agent déclaré
- Aucun scan de port, aucune tentative d'intrusion
- Conforme au cadre légal OSINT français
