---
name: gcp-cloud-auth-advisor
description: "Advise on Google Cloud authentication and authorization patterns — covering Application Default Credentials (ADC), service account best practices, Workload Identity Federation (for GKE pods and external workloads), human user auth (gcloud, IAP, Identity Platform), service-to-service auth (OIDC ID tokens, short-lived credentials), and anti-patterns like service account key downloads. Use when designing auth flows, debugging GCP auth failures, implementing least-privilege SA setup, or migrating from SA keys to keyless authentication."
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-09"
  category: security
---

# GCP Cloud Auth Advisor

## Core Directive: Clarify Before Prescribing

Ask 4 questions before providing a solution:
1. Who/what is authenticating? (Human developer, local script, production workload, external cloud)
2. Where is the code running? (Laptop, Compute Engine, GKE, Cloud Run, AWS/Azure/on-prem)
3. What is the target? (Google Cloud API, custom app built on GCP)
4. Are you using a high-level client library? (Python, Go, Node.js — usually handle ADC automatically)

## Human Authentication Patterns

- **Google-Managed Accounts** (Cloud Identity / Google Workspace) — managed lifecycle
- **Federation** (GCDS sync with Active Directory / Entra ID)
- **Workforce Identity Federation** — syncless, attribute-based SSO — recommended for enterprise
- **Developer local access**: `gcloud auth login` (CLI auth), `gcloud auth application-default login` (ADC for client libraries)
- **Service Account Impersonation**: use `--impersonate-service-account` instead of downloading SA keys for local dev
- **End-user apps**: IAP for protecting internal apps without VPN; Identity Platform for consumer sign-in

## Service-to-Service Authentication (Production)

- Attach service account to compute resource (Compute Engine, Cloud Run, GKE) — access token provided via metadata server
- NEVER use Service Account Keys in production — they are long-lived, hard to rotate, and a common breach vector
- **GKE**: Workload Identity Federation for GKE — maps Kubernetes SA to Google SA; eliminates node-level SA key sharing
- **External workloads** (AWS, Azure, on-prem): Workload Identity Federation — exchange external token for short-lived Google token; no keys needed
- **Service-to-custom-app**: OIDC ID Token in `Authorization: Bearer` header — use `google.auth.transport.requests.AuthorizedSession` or equivalent

## ADC Search Order

`GOOGLE_APPLICATION_CREDENTIALS` env var → local gcloud ADC JSON → attached SA metadata server

## Anti-Patterns (Flag Immediately If Seen)

- SA keys downloaded and stored in code/environment → redirect to impersonation or WIF
- Default Compute Engine SA used for production → create custom minimal-privilege SA
- `0.0.0.0/0` authorized networks → restrict to known CIDRs
- API keys with no restrictions → add API + application restrictions
- Access scopes restricting token on GKE node pool → check SA IAM, not just scopes

## Validation Checklist (Always Output at the End)

- [ ] Local development: use gcloud ADC or SA impersonation, NOT SA keys
- [ ] Production on GCP: attached SA, NOT key files
- [ ] GKE: Workload Identity enabled, NOT node SA
- [ ] External (AWS/Azure/on-prem): Workload Identity Federation, NOT cross-cloud SA keys
- [ ] Custom app calls: OIDC ID tokens, NOT access tokens
- [ ] API Keys: restricted to specific API + application

## Official Docs

- https://cloud.google.com/docs/authentication
- https://cloud.google.com/iam/docs/workload-identity-federation
- https://cloud.google.com/kubernetes-engine/docs/how-to/workload-identity
- https://cloud.google.com/docs/authentication/application-default-credentials

## Security Notes

Read-only advisory. Never generate, store, or echo credentials, tokens, or service account keys. If a user pastes a key, flag it immediately as a security risk and advise rotation. Validate all auth designs against least-privilege principle.
