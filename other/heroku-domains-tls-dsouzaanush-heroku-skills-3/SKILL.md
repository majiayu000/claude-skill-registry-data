---
name: heroku-domains-tls
description: Configure custom domains and TLS on Heroku with ACM-first guidance. Use when the agent needs to add or inspect domains, enable or refresh automated certificate management, review certificate status, attach or replace manual certificates, or manage domain cutover safely on Heroku.
---

# Heroku Domains and TLS

Manage custom domains and certificates without treating DNS or certificate changes as harmless.

## Preferred model

For common-runtime apps, prefer Automated Certificate Management (ACM) first:

- `heroku domains:add`
- `heroku certs:auto:enable`
- `heroku certs:auto:refresh` only when verification or renewal needs to be retriggered

Use manual certificates only when ACM is not viable or the user explicitly requires manual certificate control.

## Read-only-first flow

Begin with:

- `heroku domains:info <hostname> -a <app>`
- `heroku domains:wait <hostname> -a <app>`
- `heroku certs:info -a <app> --show-domains`

Use inspection to confirm:

- the target hostname
- the DNS target that must exist before TLS can activate
- whether the hostname is an apex domain that needs ALIAS, ANAME, or equivalent flattening instead of an A record
- whether ACM already covers the domain
- whether a manual certificate is currently attached

## Manual certificate workflow

Use manual certificate management intentionally:

- `heroku certs:add <crt> <key> -a <app>`
- `heroku certs:update <crt> <key> -a <app> --name <name>`
- `heroku domains:update <hostname> -a <app> --cert <name>`
- `heroku certs:remove -a <app> --name <name>`

## Guardrails

Ask for confirmation before:

- adding or removing a custom domain
- changing DNS targets during a live cutover
- enabling manual certificates instead of ACM
- replacing or removing a certificate
- repointing a hostname to a different certificate

## References

- Read `references/domains-tls.md` for DNS validation, ACM troubleshooting, and source links.
