---
name: swap-dns
description: Move an environment's DNS, and its certificates' DNS-01 validation, off Cloudflare (to a name server of our own over RFC 2136) or to another DNS provider. Use when the user wants to leave Cloudflare, run their own DNS, or asks how DNS, external-dns or the certificate solver are chosen. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the DNS provider

- **Interface:** `dns` in `infra/tofu/envs/k3s/variables.tf` (`provider`, and the
  provider's settings). Each provider is a module that takes the same records
  (`local.records` in `envs/k3s/main.tf`: the zone, site hosts, origins, the preview
  host, the mail records) and outputs `records` in one shape: `modules/cloudflare`,
  `modules/rfc2136`.
- **The cluster learns it** from OpenTofu's annotations on its Argo CD Secret
  (`dns-provider`, `trusted-hops`, `origin-pulls`, and the provider's own: RFC 2136's
  `dns-nameserver`, `dns-tsig-key-name`, `dns-tsig-algorithm`), which the platform's
  add-ons read through `clusterParameters` (`deploy/platform/addons`):
  cert-manager's solver (`tls.dns01` in `deploy/platform/config`), external-dns's
  `provider.name` (`deploy/platform/values/external-dns.yaml`), and what the gateway
  trusts (`gateway.trustedHops`, `gateway.originPulls`).
- **Today:** Cloudflare (`dns.provider = "cloudflare"`, the default), with its proxy in
  front of the site. RFC 2136 is built in: `dns = { provider = "rfc2136", rfc2136 = {
  server, key_name } }` and `TF_VAR_dns_tsig_secret`.

## Move to RFC 2136 (a name server of our own)

1. A name server for the zone that accepts dynamic updates signed with a TSIG key
   (BIND `allow-update { key ...; }`, Knot, PowerDNS), reachable from where OpenTofu
   runs and from the cluster on port 53. Delegate the zone to it at the registrar.
2. In the environment's tfvars: `dns` as above; drop `cloudflare_account_id` and
   `managed_waf`. Export `TF_VAR_dns_tsig_secret`.
3. SOPS secrets in `deploy/platform/secrets/<env>/` (rotate-secrets skill): `rfc2136-tsig`
   in `cert-manager` (key `secret`), and `external-dns-rfc2136` in `external-dns` (keys
   `host`, `zone`, `tsig-keyname`, `tsig-secret`, `tsig-secret-alg`). Remove the
   Cloudflare token's.
4. `tofu apply`: the records move, the annotations change, and Argo CD re-renders the
   issuer, external-dns and the gateway (which now trusts no proxy and asks for no
   client certificate). Previews' and the mail host's records are unchanged in kind.
5. The captcha was Cloudflare's Turnstile widget (`tofu output turnstile`): keep the
   widget on Cloudflare's account, or turn the captcha off (unset `TURNSTILE_*`).

## Another provider

1. A module `infra/tofu/modules/<provider>` with the same inputs as `modules/rfc2136` and
   a `records` output of the same shape, with a `tests/*.tftest.hcl` against
   `mock_provider`. Add it to `envs/k3s/main.tf` with `count` on `var.dns.provider`, its
   settings to `dns`, and its provider to `versions.tf`.
2. cert-manager's solver for it in `deploy/platform/config/templates/issuer.yaml` (and
   a helm-unittest case), and external-dns's credentials in its values, each optional.
3. Annotations for anything the cluster needs that isn't secret; secrets go in SOPS.

## Tests

`bun run infra:check` (the env root's tests run each provider), `bun run charts:check`
(the issuer for each provider), `bun test scripts/appsets.test.ts` (every cluster fact an
add-on reads is one OpenTofu writes). A real zone is tried only on a real cluster: the
first certificate after a switch is the proof (`kubectl get certificate -A`).

## Finish

1. The verify skill.
2. Ask the `security-reviewer` agent to review the change: it moves who can change the
   zone's records and who the gateway trusts for the client's address.
3. Update the DNS row in the README's "Scaling path" table if what's "Now" changed.
