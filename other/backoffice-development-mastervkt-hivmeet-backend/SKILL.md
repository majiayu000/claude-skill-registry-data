---
name: backoffice-development
description: 'Constitution et recette de module du back-office HIVMeet (app Django dédiée backoffice/, server-rendered, isolée de l''API). À charger pour créer ou modifier tout module du back-office.'
argument-hint: 'Décrire le module ou la phase (ex: P4 signalements).'
user-invocable: true
---

# Développement du back-office HIVMeet

Charger d'abord `backoffice-independence-guard`, puis `docs/backoffice/PLAN.md` et
`docs/backoffice/HANDOFF.md` (état réel, décisions, prochaine phase). Les skills
`backoffice-security` et `backoffice-testing` s'appliquent à tout module.

## Décisions figées
App Django dédiée `backoffice/`, server-rendered (templates + formulaires, **sans framework
JS**), session Django, revue KYC complète, sanction = `is_active` + motif + audit, MFA TOTP
obligatoire pour tout le staff, **indépendance totale** vis-à-vis de l'application.

## Exécution isolée
- Settings dédiés `backoffice/conf/settings.py` : `from hivmeet_backend.settings import *`
  puis override (middleware propre, `ROOT_URLCONF='backoffice.conf.urls'`, cookies
  `bo_sessionid`/`bo_csrftoken` SameSite Strict, pas d'admin Django, pas de CORS/daphne).
- Tests : `backoffice/conf/settings_test.py` dérivé de `hivmeet_backend.test_settings`.
- Lancement dev : `python manage.py runserver 8001 --settings=backoffice.conf.settings`.
- Migrations : `python manage.py migrate backoffice --settings=backoffice.conf.settings`.

## Arborescence
```
backoffice/
  conf/ (settings, settings_test, urls, wsgi)   access.py (capacités)   audit.py
  mfa/  services/  views/  forms.py  middleware.py  models.py  checks.py
  templates/backoffice/  static/backoffice/  locale/fr/  tests/  management/commands/
```

## Recette d'un module
1. **Lire l'existant réel** (le comportement implémenté prime sur les spécifications) :
   modèles, services, tâches concernés. Utiliser le graphe de revue avant le grep.
2. **Définir la capacité** dans `access.py` (matrice dans `backoffice-security`).
3. **Service** dans `backoffice/services/<module>.py` : toute la logique d'écriture, dans
   `transaction.atomic`; effets de bord (FCM, WebSocket, tâches Celery) via
   `transaction.on_commit`; écrit une entrée `StaffAuditLog`.
4. **Vue** : vue Django pure avec `BackofficeAccessMixin(capability=...)`; lecture = GET,
   toute écriture = POST + CSRF; action destructive = page de confirmation avec **motif
   obligatoire**; listes avec `Paginator` (25).
5. **Template** étendant `backoffice/base.html`; textes en `gettext_lazy` (msgid anglais),
   catalogue FR dans `backoffice/locale`; CSS écrit main, **ni CDN ni police externe ni
   script inline** (CSP `script-src 'self'`).
6. **Tests** (voir `backoffice-testing`) puis `check_independence verify`.
7. Mettre à jour le HANDOFF via `backoffice-phase-handoff`, puis **s'arrêter**.

## Acquis de la Phase 1 (à respecter)
- **URLs** : le processus back-office sert `/backoffice/…` (pas de préfixe de langue; la langue
  vient de `LocaleMiddleware`, français par défaut). Racine `/` → redirection publique.
- **Déclarer chaque vue** (sinon 403, *deny by default*, `middleware.process_view`) :
  fonction → `@public_view` (connexion/MFA/déconnexion seulement) ou `@requires(access.CAP)` ;
  classe → `class X(access.BackofficeView, View): capability = access.CAP`. Les capacités sont
  des constantes de `backoffice/access.py` (matrice testée dans `tests/test_gate.py`).
- **Audit** : `audit.record(action=..., actor=..., request=..., ...)`. Toute **nouvelle action**
  doit être ajoutée à `audit.ALLOWED_ACTIONS` et toute nouvelle clé de métadonnée à
  `ALLOWED_METADATA_KEYS` (sinon `ValueError` / clé écartée avec avertissement).
- **Réglages** : ajouter un réglage back-office dans `conf/overrides.py` (`apply(globals())`,
  partagé par `settings.py` et `settings_test.py`), jamais dans `hivmeet_backend/`.
- **Session** : Django **n'enregistre pas la session sur une réponse 5xx**. Ne jamais renvoyer
  de 5xx après avoir modifié la session (compteurs, purge de l'état pending, etc.) : utiliser
  403/429.
- **i18n par phase** (pas à la P11) : après chaque ajout de texte,
  `cd backoffice && PYTHONPATH=<racine> DJANGO_SETTINGS_MODULE=backoffice.conf.settings
  python -m django makemessages -l fr --no-obsolete --no-location -i tests -i migrations`, traduire
  `locale/fr/LC_MESSAGES/django.po`, puis `msgfmt --check-format -o django.mo django.po` et
  **committer le `.mo`**. `tests/test_i18n.py` échoue si une entrée est vide ou si le `.mo`
  diverge du `.po`. Dans les vues, `gettext` à l'exécution (pas au chargement du module).
- **Migrations** : `makemigrations backoffice` puis `migrate backoffice` **sur une base jetable**
  (`DATABASE_URL=…/hivmeet_bo_scratch`), jamais sur la base de développement de l'utilisateur.

## Réutiliser sans modifier (API publique existante)
`profiles/kyc_review.py` : `reviewer_role` (62), `assign_kyc_case` (222),
`issue_reviewer_document_url` (249), `decide_kyc_case` (294), `DECISION_REASON_CODES` (47);
`notifications/fcm.py:send_fcm_to_user` (87); `subscriptions/tasks.py:reconcile_mycoolpay_payment`;
`profiles/tasks.py:process_account_deletion`; `profiles/private_storage.py` (stockage privé).

Si la logique utile est privée ou inline dans une vue (ex. `resolve_report_view`,
`authentication/views.py:736-850`) : **la réimplémenter dans `backoffice/services/`** avec un
test de parité, sans refactorer l'existant. Ne jamais importer de fonction `_privée`
sauf lecture indispensable, documentée dans le HANDOFF.

## Interdits
Voir `backoffice-independence-guard` (écriture hors zones, `migrate` sans label, correction
d'un défaut existant, nouvelle dépendance). Ne jamais afficher : contenu des messages,
localisation, bio, document KYC hors flux audité, statut VIH. Logs : identifiants seulement.

## Checklist module
- [ ] Capacité déclarée, refus testé pour chaque autre rôle
- [ ] Écritures atomiques, motif + audit, effets de bord en `on_commit`
- [ ] Aucune donnée de santé/PII superflue dans le HTML ni les logs
- [ ] Textes FR/EN, aucun script inline, aucun CDN
- [ ] Tests verts, `check_independence verify` PASS, HANDOFF à jour
