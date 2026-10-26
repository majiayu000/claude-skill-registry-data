---
name: backoffice-security
description: 'Règles de sécurité du back-office HIVMeet : accès par capacités, MFA TOTP, audit, masquage des données de santé, en-têtes et sessions. À charger pour tout module touchant authentification, permissions ou données personnelles.'
argument-hint: 'Indiquer le module ou la capacité concernée.'
user-invocable: true
---

# Sécurité du back-office HIVMeet

Tous les utilisateurs de l'application vivent avec le VIH : **tout enregistrement identifiable
est une donnée de santé de catégorie spéciale**. Principe : minimum nécessaire, audité.

## Barrière d'accès (tous les contrôles, dans cet ordre)
`is_authenticated` + `is_active` + `is_staff` + **session MFA vérifiée et non expirée** +
capacité ∈ groupes de l'utilisateur. Refus par défaut (deny by default) : toute vue
`backoffice` non marquée publique exige la barrière complète.
- Les capacités sont des **constantes de code** (`backoffice/access.py`), pas des permissions
  Django (`has_perm` donne tout à un superuser). **Un superuser n'a aucun accès implicite**,
  y compris au KYC (règle de `docs/kyc/KYC_PHASE_3_IMPLEMENTATION.md`).
- Aucune auto-modification de ses groupes ou de son statut; garde « dernier admin ».
- Un modérateur ne peut pas désactiver un membre du staff ni un superuser.

## Matrice des capacités
| Capacité | admin | moderator | support | kyc_reviewer | kyc_supervisor |
|---|---|---|---|---|---|
| dashboard | ✓ | ✓ | ✓ | ✓ | ✓ |
| users.search / view (masqué) | ✓ | ✓ | ✓ | | |
| users.view_pii (audité) | ✓ | | | | |
| users.deactivate | ✓ | ✓ | | | |
| users.reactivate | ✓ | | | | |
| staff.manage | ✓ | | | | |
| reports.* | ✓ | ✓ | | | |
| moderation.* | ✓ | ✓ | | | |
| payments.view / reconcile | ✓ | | ✓ | | |
| gdpr.view | ✓ | | ✓ | | |
| gdpr.act | ✓ | | | | |
| audit.view | ✓ | | | | |
| kyc.* | | | | ✓ | ✓ (+ file, assignation, alertes) |

Groupes : `backoffice_admin`, `backoffice_moderator`, `backoffice_support` (créés par
migration `backoffice/0002` **et** par `ensure_backoffice_groups()` pour les tests); KYC :
`kyc_reviewer`, `kyc_supervisor` existants. `User.role` est legacy : lecture seule, jamais
synchronisé.

## MFA (TOTP RFC 6238, implémenté en interne avec hmac/hashlib, aucune dépendance)
- Modèles propres `backoffice.StaffMfaDevice` (secret chiffré Fernet, clé
  `BACKOFFICE_MFA_ENCRYPTION_KEY`; dérivée de `SECRET_KEY` seulement en DEBUG/TESTING;
  `last_totp_counter` anti-rejeu) et `StaffMfaEnrollmentToken` (haché, 24 h, usage unique).
  **Ne pas réutiliser les tables MFA KYC.**
- Connexion en deux étapes : mot de passe (`authenticate`, message d'erreur générique, **pas
  de `login()`**) → TOTP → `login()` + `session['bo_mfa_at']`. Inactivité 900 s,
  plafond absolu 8 h.
- **Step-up 300 s** pour accès document KYC, décision, actions RGPD et staff.
- Verrouillage (cache Redis en prod) : 5 échecs mot de passe/compte/15 min, 20/IP/15 min;
  5 échecs TOTP = verrouillage 15 min. Clés HMAC-hachées. Chaque verrouillage est audité.
- Enrôlement : commande `backoffice_bootstrap_admin` (TTY requis, secret affiché une
  seule fois, jamais journalisé) puis jeton émis par un admin. Pas d'auto-enrôlement par
  simple mot de passe. Reset = suppression de l'appareil + purge des sessions + audit.

## Audit (`backoffice.StaffAuditLog`, append-only)
UUID, `actor` (SET_NULL) + `actor_ref`, `action` (slug d'une liste blanche), `target_type`/
`target_id` (chaînes), `reason`, `metadata` (clés et types scalaires en liste blanche),
`ip_hash` (HMAC). Écrit dans la transaction de l'action. À journaliser : connexions
(succès/échec hachés), MFA, verrouillages, consultation d'une fiche, révélation PII, vue
photo pleine taille, **toute écriture**. Pas les listes. Les actions KYC restent dans
`KycAuditEvent` via les services existants (pas de doublon).

## Affichage des données
- Email masqué `j***@d***.tld` partout, sauf `users.view_pii` (audité).
- Recherche utilisateur par **email exact ou UUID** uniquement (pas de navigation libre).
- **Jamais** : contenu des messages, localisation, bio, statut VIH, document KYC hors flux
  audité, téléchargement d'export RGPD.
- Fiche utilisateur : nom affiché, dates, actif, libellé du statut KYC, premium, compteurs.

## Réseau et navigateur (middleware `backoffice` uniquement)
CSP `default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;
form-action 'self'; frame-ancestors 'none'; base-uri 'none'`; `Cache-Control: no-store`;
`Referrer-Policy: same-origin`; `X-Robots-Tag: noindex`. Cookies `Secure`, `HttpOnly`,
SameSite Strict, noms distincts. Documents sensibles : `no-store` + `CSP: sandbox`.
Recommandation de déploiement : allow-list IP/VPN sur `/backoffice/`.

## Logs
`hivmeet.backoffice`, identifiants uniquement : ni email complet, ni jeton, ni secret TOTP,
ni donnée de santé. Le filtre `PrivacyRedactionFilter` existant s'applique.

## Checklist avant livraison d'un module
- [ ] Barrière complète testée (anonyme, sans groupe, mauvais rôle, bon rôle, sans MFA)
- [ ] Motif + audit sur chaque écriture, step-up sur les actions sensibles
- [ ] Aucune PII/santé superflue (assertion sur le HTML)
- [ ] Aucun accès implicite superuser
