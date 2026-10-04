---
name: socmint
description: "Renseignement sur les réseaux sociaux : vérification d'email et de username sur 2500+ plateformes. Utiliser pour identifier la présence en ligne d'une personne ou d'un contact professionnel."
metadata: { "openclaw": { "emoji": "👤", "requires": { "bins": ["python3", "holehe", "maigret"] } } }
user-invocable: true
---

# SOCMINT — Social Media Intelligence

## Déclencheur
- `/socmint john.doe@acme.com`
- `/socmint @username`
- "vérifie la présence en ligne de ce contact"
- "sur quels réseaux sociaux est cette personne"

## Ce que fait ce skill
Skill de type **KNOWLEDGE** — l'agent exécute directement les outils installés dans l'image Docker.

### Recherche par email
Utilise **holehe** pour vérifier si un email est enregistré sur 120+ sites.

```bash
holehe john.doe@acme.com
```

Holehe vérifie passivement si l'email est associé à un compte sur :
- Réseaux sociaux : Twitter, Instagram, Facebook, LinkedIn, TikTok...
- Services tech : GitHub, GitLab, Docker Hub, Stack Overflow...
- Services pro : Slack, Notion, Trello, Asana...
- Autres : Spotify, Discord, Pinterest, Tumblr...

### Recherche par username
Utilise **maigret** pour scanner un pseudo sur 2500+ sites.

```bash
maigret @username --timeout 15
```

Maigret détecte la présence d'un username sur :
- Réseaux sociaux majeurs et de niche
- Forums et communautés
- Plateformes de développement
- Sites de portfolio et créatifs

### Recherche sociale via SearXNG
Pour compléter, utiliser le skill `web-search` avec la catégorie `social_media` :

```bash
source /opt/albert-ml/bin/activate
python3 /home/node/.openclaw/skills/osint/web-search/scripts/search.py \
    --query "John Doe site:linkedin.com OR site:twitter.com" \
    --category social_media --limit 20
```

## Interprétation des résultats

### holehe
- `[+]` = email enregistré sur le site (compte existant)
- `[-]` = email non trouvé
- `[x]` = erreur de vérification (rate limit, captcha)

### maigret
- Résultats classés par probabilité de correspondance
- URL directe vers chaque profil trouvé
- Rapport HTML généré automatiquement

## Workflow recommandé
1. Commencer par holehe sur l'email professionnel
2. Si un username est identifié, lancer maigret
3. Compléter avec SearXNG en social_media
4. Croiser les informations pour valider l'identité

## RGPD et éthique
- **Données publiques uniquement** — aucune tentative d'accès non autorisé
- **Intérêt légitime B2B** — prospection commerciale sur données professionnelles publiques
- **Pas de profilage personnel** — uniquement contexte professionnel
- **Droit d'opposition** — respecter toute demande de suppression
- Conforme à l'article 6.1.f du RGPD (intérêt légitime)

## Garde-fous RGPD (obligatoires — Art. 6.1.f)

**Base légale :** Intérêt légitime B2B (Art. 6.1.f RGPD) — uniquement pour entités immatriculées  
**Voir :** workspace-albert/COMPLIANCE.md pour le test de balance documenté

### CONDITIONS D'UTILISATION STRICTES
- **SIREN requis** en input — entités immatriculées uniquement (pas de personnes physiques isolées)
- **Interdit :** personnes physiques sans lien commercial préexistant établi
- **Interdit :** mineurs
- **Durée conservation résultats :** 30 jours maximum
- **Traçabilité :** logger SIREN + date dans la session

### INFORMATION DES PERSONNES (Art. 14 RGPD)
Si contact établi → mentionner la source lors du premier contact
Exemple : "J'ai trouvé vos coordonnées via [source publique] dans le cadre de..."
