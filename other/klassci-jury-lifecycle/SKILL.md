---
name: klassci-jury-lifecycle
description: Workflow complet jury de délibération LMD UEMOA — création session, composition jury, calcul auto décisions, override motivé, génération PV PDF, signature digital, publication, archivage légal
---

# Skill: klassci-jury-lifecycle

## When to use this skill

- Pour planifier un jury de délibération LMD complet pour une promotion
- Pour comprendre le workflow UEMOA (CC + Examen Terminal + Rattrapage + Délibération)
- Pour générer PV PDF avec signatures et archivage légal
- Pour gérer un cas exceptionnel (override jury motivé)

## Workflow complet — 5 phases

### Phase 1 — Préparation (J-7)

```
1. Identifier session à délibérer
   - Année universitaire + Semestre + Parcours + Niveau
   - Vérifier que toutes les notes session normale (CC + Examen Terminal) sont saisies + publiées
   - Vérifier que session rattrapage (si applicable) est terminée

2. Créer le jury
   POST /esbtp/lmd/jurys
   {
       "session_id": X,
       "parcours_id": Y,
       "niveau_etude_id": Z,
       "semestre": N,
       "date_seance": "2026-07-15 14:00:00",
       "lieu": "Salle Conseil ESBTP",
   }

3. Composer le jury (membres)
   POST /esbtp/lmd/jurys/{id}/membres
   - Président (user_id du Responsable UE chef département)
   - Assesseurs (N enseignants des UE de la session)
   - Secrétaire (admin scolarité)
   - Membres consultatifs (optionnel)

4. Vérifier le quorum
   GET /esbtp/lmd/jurys/{id}/quorum
   {
       "quorum_atteint": true,
       "min_required": 2,
       "actual_members": 5,
       "min_assesseurs": 1,
       "actual_assesseurs": 3,
   }

5. Notifier les membres (email automatique + dashboard)
```

### Phase 2 — Délibération (jour J)

```
1. Démarrer la séance
   PATCH /esbtp/lmd/jurys/{id}
   { "status": "en_cours", "date_seance_actual": now() }

2. Calculer les décisions automatiques (algo UEMOA)
   POST /esbtp/lmd/jurys/{id}/decisions/auto

   Pour chaque étudiant :
   - Charge tous les ECUE de la session
   - Applique settings tenant :
     - lmd_compensation_enabled (UE compensation activée ?)
     - lmd_compensation_min_note (seuil ECUE compensable, ex: 7)
     - lmd_intra_ue_compensation
     - lmd_cc_weight (40%) / lmd_exam_weight (60%)
   - Calcule moyenne pondérée UE → moyenne semestre
   - Détermine décision (ADMIS / ADMISSION_RATTRAPAGE / AJOURNÉ / ...)
   - Attribue mention (Passable / AB / B / TB)

3. Override individuels (jury en réunion)
   Pour chaque cas limite :
   PATCH /esbtp/lmd/jurys/{id}/decisions/{etudiantId}
   {
       "decision": "admis_sous_condition",
       "motif": "Bourse en cours, jury accepte conditionnel après audition. Vote 4 pour / 1 abstention.",
       "vote_unanime": false,
       "vote_resultat": "4 pour / 0 contre / 1 abstention"
   }

   Audit log automatique :
   - decided_by = jury->president_user_id
   - decided_at = now()
   - override_par_jury = true
   - decision_auto_proposee = "admission_rattrapage" (ce que l'algo proposait)
   - decision = "admis_sous_condition" (ce que le jury décide)

4. Suspension/reprise séance (si pause)
   PATCH /esbtp/lmd/jurys/{id} { "status": "suspendu" }
   ... pause ...
   PATCH /esbtp/lmd/jurys/{id} { "status": "en_cours" }
```

### Phase 3 — Signatures membres

```
1. Setting lmd_jury_signature_required = true → canvas HTML5 obligatoire
   Setting = false → checkbox simple suffit

2. Chaque membre du jury :
   POST /esbtp/lmd/jurys/{id}/signatures
   {
       "user_id": current_user_id,
       "signature_base64": "data:image/png;base64,iVBORw0KGgo...",
       "ip_signature": "192.168.1.42",
       "timestamp": now()
   }

3. Tableau bord live (AJAX) :
   GET /esbtp/lmd/jurys/{id}/signatures-status
   {
       "signatures_recueillies": 4,
       "signatures_attendues": 5,
       "membres_non_signe": [{ "user_id": X, "nom": "..." }]
   }
```

### Phase 4 — Génération PV PDF

```
1. Réserver numéro PV (thread-safe DB lock)
   POST /esbtp/lmd/jurys/{id}/reserver-numero
   { "annee_universitaire_id": X }
   → returns: "PV-2025-2026-PRESENTATION-0042"

2. Générer PDF
   POST /esbtp/lmd/jurys/{id}/generer-pv
   {
       "notes_president": "Rapport jury libre, statistiques, points particuliers..."
   }
   → Crée le PDF dans storage/pv/{tenant}/{annee}/{numero}.pdf
   → Update jury :
     - pv_numero
     - pv_url
     - pv_genere_at
     - status = "clos"
   → Audit log immutable

3. Aperçu PDF
   GET /esbtp/lmd/jurys/{id}/pv-preview
   → Retourne le PDF en stream inline (iframe affichage Browsershot)
```

### Phase 5 — Publication + Archivage

```
1. Publier les décisions
   POST /esbtp/lmd/jurys/{id}/publier
   - Update status = "publie"
   - Update pv_publie_at = now()
   - Update ESBTPLMDResultatUE.decision pour chaque étudiant
   - Lock notes (impossible de modifier après PV)
   - Notifications étudiants (email + SMS si setting)
   - Génération auto bulletins LMD via LMDBulletinService

2. Archive automatique (J+1 an, cron job)
   - Status → "archive"
   - Retention legale 5 ans (setting lmd_pv_retention_years)
   - PVs jamais supprimés (soft delete uniquement)
```

## Décisions canoniques (cheatsheet)

| Décision | Code | Critères algo |
|---|---|---|
| ADMIS | `admis` | moyenne ≥ 10 ET tous crédits validés |
| ADMISSION_RATTRAPAGE | `admission_rattrapage` | moyenne < 10 ET au moins 1 ECUE rattrapable |
| AJOURNÉ | `ajourne` | 2e session échouée OU non éligible rattrapage |
| EXCLU | `exclu` | jury décide (motif obligatoire) |
| ADMIS_SOUS_CONDITION | `admis_sous_condition` | jury décide (motif obligatoire) |
| DEFERE | `defere` | jury défère au rectorat (médical, etc.) |

## Mentions (settings tenant)

| Mention | Setting | Default |
|---|---|---|
| Passable | `lmd_mention_p_threshold` | 10 |
| Assez Bien | `lmd_mention_ab_threshold` | 12 |
| Bien | `lmd_mention_b_threshold` | 14 |
| Très Bien | `lmd_mention_tb_threshold` | 16 |

## Audit log

Tous les events critiques sont audités via Auditable trait :
- Création jury
- Composition (ajout/retrait membre)
- Override décision
- Génération PV (numéro réservé)
- Publication
- Archivage

Whitelist `$auditInclude` exclut les données sensibles (signature_base64 trop volumineux).

## Voir aussi

- Memory : `feedback_jury_uemoa_workflow.md`
- Rule projet : `jury-deliberation-uemoa.md`
- Rule projet : `ajax-no-reload-premium.md`
- Master plan : `docs/MASTER-PLAN-emploi-temps-lmd-unification.md` (PR11-13)
- Models : `ESBTPLMDJury`, `ESBTPLMDJuryMembre`, `ESBTPLMDJuryDecision`
- Service : `app/Services/JuryDeliberationService.php`
- Template PV : `resources/views/pdf/lmd-jury-pv.blade.php`
- Directive 03/2007/CM/UEMOA LMD
