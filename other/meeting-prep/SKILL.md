---
name: meeting-prep
description: "Prépare un briefing complet avant un rendez-vous prospect. Orchestre TOUS les skills d'intelligence (sirene, scorer, audit-flash, nis2-radar, aides, bodacc) pour produire une fiche synthétique d'une page. Utiliser quand l'utilisateur a un RDV à préparer."
metadata: { "openclaw": { "emoji": "📋" } }
user-invocable: true
---

# Meeting Prep (Orchestrateur)

## Objectif

Produire un **briefing d'une page** avant un rendez-vous commercial en orchestrant automatiquement tous les skills d'intelligence disponibles. Le consultant arrive au RDV avec toutes les informations clés déjà synthétisées.

## Déclencheurs

- `/rdv ACME Corp demain 14h`
- `/rdv Association Les Petits Pas jeudi`
- `/meeting-prep SIRET 44306184100047`
- "prépare mon RDV avec Association XYZ"
- "j'ai un RDV avec la boîte [nom] — prépare-moi"
- "briefing pour mon rendez-vous de demain"

## Orchestration complète

Ce skill est un **orchestrateur** : il appelle séquentiellement les skills et data-pipes suivants, puis synthétise les résultats.

### Étape 1 — Identification (sirene)
- Résoudre le nom/SIRET vers les données entreprise complètes
- Extraire : raison sociale, SIRET, NAF, effectif, adresse, date de création, forme juridique

### Étape 2 — Scoring (prospect-scorer)
- Lancer le scoring complet avec la grille de points
- Récupérer : score total, signaux détectés, approche recommandée

### Étape 3 — Audit cyber (audit-flash-cyber)
- Si un domaine web est identifiable (site web dans les données entreprise ou déductible du nom), lancer l'audit passif
- Récupérer : note A-F, findings principaux, recommandations

### Étape 4 — Analyse NIS2 (nis2-radar)
- Croiser NAF + effectif avec la table NIS2
- Récupérer : statut NIS2, obligations, échéances

### Étape 5 — Aides et subventions (aides)
- Vérifier l'éligibilité aux dispositifs d'aide
- Récupérer : aides disponibles, montants, conditions

### Étape 6 — Signaux BODACC (bodacc)
- Chercher les publications récentes (< 12 mois)
- Récupérer : événements notables (création, modification, procédure)

### Étape 7 — Structure groupe (group-mapper)
- Si l'entité fait partie d'un groupe, cartographier rapidement
- Récupérer : nombre de filiales, potentiel multi-entités

## Format de sortie — Briefing 1 page

```markdown
# BRIEFING RDV — [RAISON SOCIALE]
**Date RDV :** [date et heure]
**Préparé le :** [date du jour]

---

## 1. Fiche entreprise
| | |
|---|---|
| **Raison sociale** | ACME SAS |
| **SIRET** | 44306184100047 |
| **Activité (NAF)** | 6201Z — Programmation informatique |
| **Effectif** | 120 salariés |
| **Localisation** | Toulouse (31) — Occitanie |
| **Création** | 15/03/2005 |
| **Forme juridique** | SAS |

## 2. Score prospect : 65/125 — LEAD CHAUD 🔥
- ✅ Pas de DPO déclaré (+30)
- ✅ Cible NIS2 — 50-250 salariés (+20)
- ✅ Secteur cible NAF IT (+15)
- ⬜ Pas de recrutement DevSecOps/RGPD détecté
- **Approche recommandée :** Email personnalisé

## 3. Sécurité web : Note C (6/10)
- ⚠️ Pas de DKIM configuré
- ⚠️ DMARC en mode `none` (pas de protection)
- ⚠️ Pas de Content-Security-Policy
- ✅ HSTS actif, certificat SSL valide

## 4. NIS2 : ENTITÉ IMPORTANTE
- Secteur "Gestion des services TIC" (NAF 6201Z)
- 120 salariés > seuil de 50
- Obligations : gestion risques cyber, notification incidents ANSSI, audits réguliers
- Sanctions potentielles : jusqu'à 7 M EUR

## 5. Aides disponibles
- 🏦 **France Num** : diagnostic numérique (reste à charge 0€ possible)
- 🏦 **Aide régionale Occitanie** : accompagnement cybersécurité PME

## 6. Signaux récents (BODACC)
- Aucun événement notable sur les 12 derniers mois

## 7. Structure groupe
- Entité indépendante (pas de groupe identifié)

---

## 💬 TALKING POINTS pour le RDV

1. **Accroche NIS2** : "Votre entreprise est directement concernée par NIS2 en tant qu'entité importante. La direction sera personnellement responsable. On peut structurer votre mise en conformité."

2. **Levier DPO** : "Je n'ai pas trouvé de DPO déclaré à la CNIL pour votre structure. Selon votre activité, c'est potentiellement obligatoire. Je peux vous accompagner sur ce point."

3. **Quick win sécurité** : "Un audit rapide de votre domaine montre quelques points d'amélioration simples sur la configuration email et les headers de sécurité — ce sont des actions rapides à fort impact."

4. **Argument subvention** : "Des aides France Num permettent de financer un diagnostic numérique avec un reste à charge potentiellement nul. On peut monter le dossier ensemble."

## 📌 OBJECTIF DU RDV
- Qualifier le besoin NIS2 / RGPD
- Proposer un audit de maturité (entrée en relation)
- Mentionner le financement par les aides
```

## Gestion des cas particuliers

| Cas | Comportement |
|-----|-------------|
| **Association** | Adapter le vocabulaire (adhérents vs clients, bureau vs direction). Vérifier aides spécifiques ESS. |
| **TPE < 10 salariés** | NIS2 non applicable en général. Focus sur RGPD et aides France Num. |
| **Grande entreprise > 250** | NIS2 entité essentielle probable. Insister sur les sanctions. |
| **Pas de site web trouvé** | Sauter l'audit cyber, signaler comme point de discussion. |
| **Groupe avec filiales** | Mettre en avant le potentiel multi-entités "1 vente = N filiales". |

## Règles

- Toujours produire le briefing même si certaines sources sont indisponibles — indiquer les données manquantes.
- Le briefing doit tenir en **une page imprimable** — être synthétique.
- Les talking points doivent être **directement utilisables en conversation** — ton professionnel mais pas robotique.
- Ne jamais inventer de données — si une info n'est pas trouvée, l'indiquer.
- Adapter le ton selon le type de structure (entreprise vs association vs collectivité).
