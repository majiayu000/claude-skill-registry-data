---
name: backoffice-phase-handoff
description: 'Procédure de fin de phase du back-office HIVMeet : audit de complétude, mise à jour du rapport HANDOFF.md, puis arrêt obligatoire jusqu''à une demande explicite de l''utilisateur. À charger au démarrage (lecture de l''état) et à la fin de chaque phase.'
argument-hint: 'Indiquer la phase terminée.'
user-invocable: true
---

# Hand-off de phase du back-office

## Au démarrage d'une session
1. Lire `AGENTS.md`, `docs/backoffice/PLAN.md`, **`docs/backoffice/HANDOFF.md`** en entier.
2. Charger `backoffice-independence-guard` puis `check_independence verify` (doit être PASS).
3. Ne démarrer que la phase que l'utilisateur a **explicitement** demandée, après vérification
   de ses critères d'entrée dans le HANDOFF.

## À la fin d'une phase (dans cet ordre)
1. Tests de la phase + non-régression (voir `backoffice-testing`).
2. `check_independence verify` → PASS; `validate_governance.py` → PASS.
3. Audit de complétude (`hivmeet-backend-completion-audit`) : exigences → preuves,
   changements → exigences, impact, validation indépendante.
4. **Mettre à jour `docs/backoffice/HANDOFF.md`** (progressivement, jamais en fin de projet) :
   - statut de la phase et date;
   - fichiers créés/modifiés (chemins), migrations (et leur rollback);
   - décisions prises et pourquoi (dont les écarts au plan);
   - commandes exactes exécutées et résultats réels (pas d'invention);
   - défauts de l'application découverts → `RECOMMANDATIONS_HORS_PERIMETRE.md` (non corrigés);
   - limites connues, dette, questions ouvertes pour l'utilisateur;
   - critères d'entrée et premières actions de la phase suivante;
   - rappels de contraintes (indépendance, sécurité, i18n) pour qu'un autre agent agisse
     « exactement comme moi ».
5. **S'ARRÊTER.** Annoncer la fin de la phase et attendre que l'utilisateur demande
   explicitement la suivante. Ne jamais enchaîner de sa propre initiative.

## Format du HANDOFF (sections)
`État global` · `Phase terminée` · `Fichiers` · `Décisions` · `Preuves (commandes/résultats)` ·
`Limites & risques` · `Hors périmètre signalé` · `Phase suivante : entrée & plan` ·
`Contraintes permanentes` · `Journal des phases`.

## Limite du hook de fin de tour (connue)
Le hook Stop de Claude Code (`lifecycle_hook.py`) lit le signal
`<!-- HIVMEET_COMPLETION_AUDIT: PASS request=<id> checks=... -->` dans
`last_assistant_message`, que Claude Code ne transmet pas actuellement (`claude_code:
configured_but_not_activated` dans `.agents/agent-integrations.json`). Conséquence : jusqu'à
2 reprises automatiques, puis état terminal. Ne pas créer de 3e boucle; livrer les preuves.
Ne jamais émettre le signal PASS sans avoir réellement exécuté l'audit.
