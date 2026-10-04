---
name: invoice-tracker
description: "Suivi simple des factures et dépenses via un fichier JSON dans le workspace. Ajouter, lister, marquer payé, résumé mensuel. Utiliser quand l'utilisateur parle de factures, paiements, suivi financier, ou chiffre d'affaires."
metadata: { "openclaw": { "emoji": "💰" } }
user-invocable: true
---

# Invoice Tracker

## Objectif

Gérer un **livre de factures et dépenses simplifié** sous forme de fichier JSON dans le workspace. Pas de dépendance externe — tout est stocké dans `invoices.json`.

## Déclencheurs

- `/factures list` — Lister toutes les factures
- `/factures add ACME 5000€ audit RGPD` — Ajouter une facture
- `/factures paid FAC-2026-003` — Marquer une facture comme payée
- `/factures summary` ou `/factures résumé` — Résumé mensuel
- `/factures summary 2026-03` — Résumé d'un mois spécifique
- "combien j'ai facturé ce mois ?"
- "ajoute une facture pour ACME"
- "est-ce que ACME a payé ?"
- "quel est mon CA de ce trimestre ?"

## Opérations

### 1. Ajouter une facture

**Commande :** `/factures add <client> <montant> <description>`

**Paramètres :**
| Paramètre | Obligatoire | Exemple |
|-----------|-------------|---------|
| `client` | Oui | "ACME Corp", "Association XYZ" |
| `montant` | Oui | "5000", "5000€", "5 000 EUR" |
| `description` | Oui | "Audit RGPD", "DevSecOps 5 jours" |
| `date_emission` | Non | "2026-03-15" (défaut: aujourd'hui) |
| `echeance` | Non | "2026-04-15" (défaut: J+30) |
| `type` | Non | "facture" (défaut) ou "avoir" |

**Comportement :**
- Génère un numéro de facture auto-incrémenté : `FAC-2026-001`, `FAC-2026-002`, etc.
- Ajoute l'entrée dans `invoices.json`
- Confirme avec le récapitulatif

### 2. Lister les factures

**Commande :** `/factures list [filtres]`

**Filtres optionnels :**
- `--client ACME` — Filtrer par client
- `--status impayé` / `--status payé` — Filtrer par statut
- `--mois 2026-03` — Filtrer par mois d'émission
- `--en-retard` — Factures dont l'échéance est dépassée

**Affichage :**
```
| # | Référence | Client | Montant | Date | Échéance | Statut |
|---|-----------|--------|--------:|------|----------|--------|
| 1 | FAC-2026-001 | ACME Corp | 5 000 € | 01/03 | 31/03 | ✅ Payé |
| 2 | FAC-2026-002 | Asso XYZ | 2 550 € | 10/03 | 09/04 | ⏳ En attente |
| 3 | FAC-2026-003 | PME Beta | 4 250 € | 15/03 | 14/04 | ⚠️ En retard |
```

### 3. Marquer comme payé

**Commande :** `/factures paid FAC-2026-002`

**Paramètres optionnels :**
- `--date 2026-03-25` — Date de paiement (défaut: aujourd'hui)
- `--mode virement` — Mode de paiement (virement, chèque, CB)

### 4. Résumé mensuel

**Commande :** `/factures summary [mois]`

**Affichage :**
```
📊 RÉSUMÉ — Mars 2026

Factures émises : 5
Montant total facturé : 17 850 €
  ✅ Encaissé : 7 550 € (42%)
  ⏳ En attente : 6 800 € (38%)
  ⚠️ En retard : 3 500 € (20%)

Top clients :
  1. ACME Corp — 5 000 €
  2. PME Beta — 4 250 €
  3. Asso XYZ — 2 550 €

Jours facturés : 21 j (TJM moyen effectif : 850 €)
```

### 5. Ajouter une dépense

**Commande :** `/factures expense <montant> <description>`

Les dépenses sont stockées séparément dans le même fichier pour le suivi de la rentabilité.

## Structure du fichier `invoices.json`

```json
{
  "metadata": {
    "version": "1.0",
    "derniere_mise_a_jour": "2026-03-20T14:30:00Z",
    "prochain_numero": 4
  },
  "factures": [
    {
      "reference": "FAC-2026-001",
      "type": "facture",
      "client": "ACME Corp",
      "montant_ht": 5000,
      "devise": "EUR",
      "description": "Audit RGPD complet",
      "date_emission": "2026-03-01",
      "date_echeance": "2026-03-31",
      "statut": "paye",
      "date_paiement": "2026-03-20",
      "mode_paiement": "virement",
      "notes": ""
    }
  ],
  "depenses": [
    {
      "reference": "DEP-2026-001",
      "montant_ht": 45,
      "devise": "EUR",
      "description": "Hébergement VPS mensuel",
      "date": "2026-03-01",
      "categorie": "infrastructure"
    }
  ]
}
```

## Emplacement du fichier

Le fichier `invoices.json` est stocké dans le **workspace** de l'agent (pas dans le dossier du skill). Chemin typique :
- `workspace-albert/invoices.json`

Si le fichier n'existe pas, il est créé automatiquement avec la structure vide lors de la première opération.

## Règles

- Les montants sont toujours en **EUR HT**.
- Le numéro de facture suit le format `FAC-YYYY-NNN` (auto-incrémenté par année).
- Les dépenses suivent le format `DEP-YYYY-NNN`.
- Une facture ne peut être supprimée, seulement annulée (créer un avoir).
- Les données sont persistées dans le workspace JSON — pas de base de données externe.
- Toujours confirmer après chaque opération avec un récapitulatif.
- Les montants sont formatés avec séparateur de milliers (espace) et le symbole EUR.
- Ce n'est **pas** un logiciel de comptabilité — c'est un outil de suivi opérationnel. Pour la comptabilité officielle, utiliser un logiciel certifié.
