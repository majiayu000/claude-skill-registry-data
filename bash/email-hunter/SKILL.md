---
name: email-hunter
description: "Recherche de contacts professionnels pour un domaine : emails, noms, postes. Utiliser pour identifier les décideurs d'une entreprise cible."
metadata: { "openclaw": { "emoji": "📧", "requires": { "bins": ["python3", "theHarvester"] } } }
user-invocable: true
---

# Email Hunter — Recherche de contacts professionnels

## Déclencheur
- `/contacts acme.com`
- "trouve les contacts de cette entreprise"
- "qui sont les décideurs chez X"
- "emails professionnels de acme.fr"

## Ce que fait ce skill
Skill de type **KNOWLEDGE** — l'agent exécute directement les outils installés dans l'image Docker.

### Outil principal : theHarvester
theHarvester est un outil OSINT spécialisé dans la collecte d'emails, noms, sous-domaines et IP à partir de sources publiques.

```bash
theHarvester -d acme.com -b google,bing,linkedin -l 100
```

### Paramètres theHarvester
| Paramètre | Description                                    |
|-----------|------------------------------------------------|
| `-d`      | Domaine cible                                  |
| `-b`      | Sources (google, bing, linkedin, dnsdumpster)  |
| `-l`      | Limite de résultats                            |
| `-f`      | Fichier de sortie (HTML/XML)                   |

### Sources disponibles
- **google** : Google dorking pour emails et noms
- **bing** : Recherche Bing
- **linkedin** : Profils LinkedIn (noms et postes)
- **dnsdumpster** : Sous-domaines et enregistrements DNS
- **crtsh** : Certificate Transparency logs
- **rapiddns** : DNS rapide
- **sublist3r** : Énumération de sous-domaines

### Exemples de requêtes

#### Recherche standard
```bash
theHarvester -d acme.com -b google,bing,linkedin -l 100
```

#### Recherche approfondie
```bash
theHarvester -d acme.com -b google,bing,linkedin,dnsdumpster,crtsh -l 500 -f /home/node/.openclaw/data/harvest_acme
```

#### Google dorking complémentaire via SearXNG
Pour compléter les résultats, utiliser le skill `web-search` :
```bash
source /opt/albert-ml/bin/activate
python3 /home/node/.openclaw/skills/osint/web-search/scripts/search.py \
    --query "site:linkedin.com/in acme.com DSI OR RSSI OR DPO OR CTO" \
    --category general --limit 20
```

## Workflow recommandé

### 1. Collecte initiale
```bash
theHarvester -d cible.com -b google,bing -l 100
```

### 2. Enrichissement LinkedIn
```bash
theHarvester -d cible.com -b linkedin -l 50
```

### 3. Validation des emails
Les patterns d'email détectés permettent de déduire le format :
- `prenom.nom@cible.com`
- `p.nom@cible.com`
- `prenom@cible.com`

### 4. Croisement avec SOCMINT
Utiliser le skill `socmint` pour valider les emails trouvés :
```bash
holehe prenom.nom@cible.com
```

## Contacts prioritaires pour la prospection
Cibler en priorité les décideurs IT et conformité :
- **RSSI** (Responsable SSI) — décideur cybersécurité
- **DSI** (Directeur SI) — décideur IT
- **DPO** (Délégué Protection Données) — décideur RGPD
- **CTO/CIO** — direction technique
- **DAF** (Directeur Administratif et Financier) — décideur budget

## RGPD et conformité
- **Données publiques professionnelles uniquement** — emails corporate publiés sur le web
- **Base légale** : intérêt légitime B2B (article 6.1.f RGPD)
- **Pas de données personnelles** : uniquement emails professionnels, pas de données privées
- **Droit d'opposition** : honorer immédiatement toute demande de désinscription
- **Conservation limitée** : supprimer les contacts non répondants après 3 relances
- **Finalité déclarée** : prospection commerciale B2B de services DevSecOps/RGPD

## Filtre post-collecte RGPD (obligatoire)

Exclure tout email dont le domaine est personnel :
```
gmail.com, hotmail.com, hotmail.fr, yahoo.com, yahoo.fr,
orange.fr, free.fr, sfr.fr, laposte.net, outlook.com,
wanadoo.fr, bbox.fr, numericable.fr, neuf.fr
```

**Conserver uniquement** les emails au domaine de l'entité cible (ex: @association-nom.fr)  
**Base légale :** emails professionnels au domaine de l'entité = intérêt légitime B2B Art. 6.1.f
