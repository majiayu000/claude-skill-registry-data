---
name: backoffice-testing
description: 'Stratégie et patrons de tests du back-office HIVMeet : sessions, matrice de permissions, audit, confidentialité, non-régression de l''application. À charger pour écrire ou exécuter les tests d''une phase.'
argument-hint: 'Indiquer le module testé.'
user-invocable: true
---

# Tests du back-office HIVMeet

## Commandes
Toujours avec `PYTHONDONTWRITEBYTECODE=1` (des `.pyc` sont suivis par git).
```
# Tests du back-office (settings dédiés, dérivés de test_settings : PostgreSQL hivmeet_test)
python manage.py test backoffice --settings=backoffice.conf.settings_test

# Non-régression de l'application : settings PRINCIPAUX, rien ne doit changer
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test <suites existantes pertinentes> --settings=hivmeet_backend.test_settings

# Cohérence des settings back-office
python manage.py check --settings=backoffice.conf.settings
python manage.py makemigrations backoffice --check --dry-run --settings=backoffice.conf.settings

# Gouvernance et indépendance
python .agents/skills/backoffice-independence-guard/scripts/check_independence.py verify
python D:/Projets/HIVMeet/.agents/skills/hivmeet-governance/scripts/validate_governance.py
```
Ne jamais lancer `migrate` sans label. Les migrations sont désactivées dans
`test_settings` : les groupes se créent par `ensure_backoffice_groups()` (et
`Group.objects.get_or_create` pour les groupes KYC), pas par la migration de données.

## Environnement de test (acquis Phase 1)
- PostgreSQL local requis (`postgres/postgres`, port 5432). Utiliser **une base de test dédiée**
  pour ne jamais entrer en collision avec d'autres suites :
  `HIVMEET_TEST_DB_NAME=hivmeet_bo_test python manage.py test backoffice
  --settings=backoffice.conf.settings_test --noinput` (la base de test est détruite ensuite).
- `settings_test` hérite de `hivmeet_backend.test_settings` : migrations désactivées, cache
  mémoire, hasher MD5, `SECRET_KEY` de test. Les groupes viennent de `ensure_backoffice_groups()`.
- `BackofficeTestCase` vide le cache (verrouillage) et fournit un `self.client` en **anglais**
  (`Accept-Language: en`) car le français est la langue par défaut; les tests de langue
  utilisent `self.client_class()` sans en-tête.
- Base jetable pour essais de migration/serveur : créer `hivmeet_bo_scratch` (psycopg2,
  `CREATE DATABASE`), exporter `DATABASE_URL`, y lancer `migrate`/`runserver 8001`/curl, puis la
  **supprimer**. Le serveur démarré en arrière-plan doit être arrêté (port 8001).
- Parcours de fumée réel (curl, cookies, CSRF) : voir `docs/backoffice/HANDOFF.md`, Phase 1.

## Patrons
- **Utilisateurs** : `User.objects.create_user(email=, password=, display_name=, birth_date=)`.
  Staff : `is_staff=True` + groupe voulu. Pour un utilisateur de l'application ciblé par une
  action : `profiles.test_support.grant_social_access(user)`.
- **Session** : `Client` + helper `backoffice.tests.helpers.login_staff(client, user,
  mfa=True)` qui pose `bo_mfa_at`/`bo_last_seen` (et `mfa=False`, `stale_mfa=True` pour les
  cas d'échec). Un test de bout en bout par module passe réellement par mot de passe + TOTP
  (code via `backoffice.mfa.totp_code`).
- **Firebase / FCM / Celery** : `@patch` comme dans `notifications/tests.py` (FCM) et
  `authentication/tests_phase4_registration.py`; Celery est eager en test.
- **Stockage** : backends `memory` (par défaut en test) pour KYC/photos.

## Matrice obligatoire pour chaque vue
| Cas | Attendu |
|---|---|
| Anonyme | redirection vers la connexion |
| Staff sans groupe / non staff / inactif | refus (403 ou message générique) |
| Staff d'un autre rôle | 403, aucune écriture, aucun audit de succès |
| Bon rôle sans MFA vérifiée ou MFA expirée | redirection MFA |
| Bon rôle, action sensible, step-up expiré | redirection step-up |
| Bon rôle | succès |
| Superuser sans groupe | refus (aucun accès implicite) |

## Assertions systématiques
- Une entrée `StaffAuditLog` par écriture (action, cible, motif, **pas de PII** en métadonnées).
- Motif obligatoire : POST sans motif → 400, aucune écriture.
- HTML sans email complet (hors `view_pii`), sans contenu de message, localisation, bio.
- Parité : un service réimplémenté produit exactement les mêmes effets/payloads que l'API
  existante (comparer Notification, statut, champs `resolved_*`).
- `assertNumQueries` sur listes et tableau de bord; pagination à 25.
- Idempotence / double soumission des actions critiques.
- En-têtes de sécurité du back-office présents; l'API reste inchangée (aucun header ajouté).

## Définition de « terminé » d'une phase
Tests du back-office verts; `check`/`makemigrations --check` principaux inchangés; suites
existantes concernées vertes; `check_independence verify` PASS; `validate_governance` PASS.
Si une suite existante échoue **pour une raison antérieure** à la phase, le consigner dans
le HANDOFF avec la preuve (échec reproduit sans le back-office), sans la corriger.
