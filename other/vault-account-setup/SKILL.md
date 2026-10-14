---
name: vault-account-setup
type: Skill
title: "Vault account setup"
description: "Provider account and authenticator setup through Matrx Vault. Use when creating a service account, saving its login, enrolling 2FA, or verifying agent sign-in with Vault credentials."
tags: [vault, authenticator, integrations, coding-agents]
timestamp: 2026-10-11
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/vault-account-setup/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# Vault account setup

Create the provider account, keep its login and authenticator on one Vault
credential, confirm 2FA at the provider, then prove a fresh sign-in. A rotating
code in Matrx alone does not prove that the provider accepted enrollment.

## Identity and inventory

1. Read the provider campaign/register and search existing provider accounts,
   Vault metadata, and connections before creating anything. An unavailable
   `credential_login` response is UNKNOWN, not an empty inventory. Resolve it
   through the app's metadata or report the exact unavailable boundary.
2. Use the identity explicitly authorized by the user. For a named personal
   Chrome profile, prefer approved isolated credentials where available; when
   that profile is required, open your own tab there and verify its identity.
   Ordinary Matrx tests use the isolated in-app Browser and authorized admin
   login. Leave pre-existing tabs untouched; close your own tabs when done.
3. Writes carry the shell's active organization and signed-in user. Choose the
   intended organization in the shell before starting, verify it, and retain
   that context throughout setup. Membership discovery never silently chooses
   an organization. A context change cancels pending setup.

## Create and store the login

4. Complete authorized signup steps. Prefer the intended Google identity when
   the provider offers it. Browser policy still requires action-time approval
   for legally binding Terms and CAPTCHAs; credential changes require handoff.
   Prepare the exact action before requesting approval. Never imply that a
   broad instruction to work autonomously overrides those requirements.
5. Save the login through Vault → New → Website login: provider name, exact
   login URL, username/email, and password if that account has one. Use the
   Vault password generator or a supported private credential transfer.
   Do not put passwords, setup seeds, recovery codes, or rotating codes into
   model-visible text, screenshots, logs, or shell commands. Save recovery
   codes in the credential's protected recovery field through a private path.
6. Record only non-secret metadata needed to use the account: login method,
   workspace/account identifier, provider campaign, and recovery/settings URL.
   Verify the saved credential is present before proceeding.

## Enroll the authenticator

7. Start authenticator setup at the provider. In Matrx:
   - Existing login: open its Two-factor section → Add authenticator.
   - New Vault login: Website login → Add authenticator.
   - TOTP-only: Authenticator → Add goes straight to setup; no login required.
8. One setup screen offers camera, image selection, paste/drop, and manual
   setup key. Prefer QR import; transfer sensitive pixels or clipboard content
   privately through documented browser APIs, without emitting it to the model.
   If no supported private transfer exists, report that boundary; never invent
   a tool or extract secrets into chat. Local image decoding sends no image to
   the server. Manual keys and otpauth links use the same enrollment path.
9. Valid intake saves once and immediately shows the current code. Blank/default
   names come from issuer/account metadata; existing custom names stay intact.
   Do not demand a username/password for TOTP-only credentials.
10. If enrollment fails after credential creation, keep its exact ID and retry
    there. Do not create a second login. A recent-authentication refusal offers
    password confirmation in Matrx. A generic 401 requires checking login and
    context, not assuming a missing seed. Preserve input while resolving it.
11. Transfer the displayed code privately into the provider's confirmation
    field. Require the provider's enabled/confirmed state. Store recovery data
    privately. If Matrx enrollment succeeded but provider confirmation failed,
    finish on that same credential rather than declaring success.

## Prove use

12. Sign out of the provider and perform a fresh sign-in using the saved login
    and authenticator through approved private filling. For brokered browser
    tools, inspect their actual advertised schema; use `credential_login` only
    when available. `authenticated` proves sign-in; `unknown` does not.
13. Return value-free evidence: provider, credential ID/name, owning organization,
    provider-confirmed 2FA, fresh sign-in outcome, and any precise open gate.
    For a requested multi-provider trial, every provider needs separate proof.

Eval maintenance only → read `evals.md` for the regression scenarios.
