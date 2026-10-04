---
name: proposal-writer
description: "Génère des propositions commerciales complètes à partir de templates (audit RGPD, DevSecOps, NIS2). Utiliser quand l'utilisateur demande de rédiger une proposition, un devis, ou une offre commerciale pour un prospect."
metadata: { "openclaw": { "emoji": "📝" } }
user-invocable: true
---

# Proposal Writer

## Objectif

Générer une **proposition commerciale complète** en Markdown, prête à être convertie en PDF, en utilisant les templates de référence et les données du prospect.

## Déclencheurs

- `/proposition ACME Corp audit RGPD`
- `/proposition 44306184100047 DevSecOps`
- `/devis Association XYZ NIS2`
- "rédige une proposition pour ACME Corp"
- "prépare un devis audit RGPD pour ce prospect"
- "fais une offre commerciale NIS2"

## Templates disponibles

Les templates sont dans `references/templates/` :

| Template | Fichier | Usage |
|----------|---------|-------|
| Audit RGPD | `proposition-audit-rgpd.md` | Audit de conformité RGPD, registre des traitements, DPO externalisé |
| DevSecOps | `proposition-devsecops.md` | Accompagnement DevSecOps, CI/CD sécurisé, audit technique |
| NIS2 | `proposition-nis2.md` | Mise en conformité NIS2, analyse de risques, politique de sécurité |
| Grille tarifaire | `tarifs.md` | Référence de prix par prestation |

## Paramètres d'entrée

| Paramètre | Obligatoire | Exemple |
|-----------|-------------|---------|
| `prospect` | Oui | Nom ou SIRET du prospect |
| `type` | Oui | `audit-rgpd`, `devsecops`, `nis2` |
| `personnalisation` | Non | Contexte spécifique du prospect |

## Processus

1. **Récupérer les données prospect** : Si un SIRET ou nom est fourni, utiliser le data-pipe `sirene` pour enrichir (raison sociale, effectif, NAF, adresse).
2. **Sélectionner le template** adapté au type de prestation demandé.
3. **Personnaliser** le template avec :
   - Les données de l'entreprise (nom, adresse, effectif, secteur)
   - Le contexte spécifique (si fourni par l'utilisateur)
   - Les tarifs de la grille tarifaire
   - Les aides disponibles (si applicable — mentionner France Num, subventions régionales)
4. **Produire** la proposition complète en Markdown.

## Format de sortie

La proposition Markdown complète, prête à export PDF, incluant :
- Page de garde avec coordonnées
- Contexte et compréhension du besoin
- Périmètre et livrables
- Méthodologie
- Planning
- Budget avec détail
- Conditions générales
- Mention des aides disponibles

## Règles

- Toujours utiliser les tarifs de `references/templates/tarifs.md` — ne jamais inventer de prix.
- Adapter le vocabulaire au type de structure (association = "membres/adhérents", entreprise = "collaborateurs/salariés").
- Mentionner systématiquement les possibilités de financement par les aides (France Num, aides régionales).
- La proposition doit être professionnelle et prête à envoyer — pas de placeholder `[À COMPLÉTER]`.
- Les données du prospect doivent être factuelles (issues de sirene) — ne rien inventer.
- Inclure les coordonnées de Teddy Deberdt dans la page de garde.
