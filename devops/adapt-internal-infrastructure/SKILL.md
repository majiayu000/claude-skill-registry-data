---
name: adapt-internal-infrastructure
description: Analyze and adapt Dockerfiles, Docker build and runtime configuration, and GitHub Actions or GitLab CI files for a closed organization network. Use when a project must work through a VPN or proxy, pull from an internal registry, trust a corporate CA, use an internal Python package index, inject CI secrets, or satisfy other organization-specific infrastructure requirements without weakening TLS verification or committing credentials.
---

# Adapt Internal Infrastructure

Adapt the project interactively. Discover available configuration first, ask for every required
value that cannot be determined safely, and edit only after the user approves the concrete plan.

## Inspect the project

1. Read `AGENTS.md` and all applicable repository instructions completely.
2. Inspect the worktree status. Preserve unrelated user changes.
3. Locate Dockerfiles, `.dockerignore`, Docker documentation, CI files and inactive CI templates,
   package-manager configuration, lockfiles, and environment examples.
4. Read `docs/closed-network.md` when it exists. Treat it as operational guidance, not as a source
   of organization-specific values.
5. Determine which CI providers are in scope and whether their configurations are active or only
   templates. Do not activate a provider without explicit user authorization.
6. Identify existing conventions for build arguments, secret mounts, registries, package indexes,
   certificate stores, and CI secret names before proposing new ones.

## Resolve infrastructure requirements

Build a requirements inventory from repository files and information supplied by the user. Check
only items relevant to the requested environment:

- Docker host operating system and engine or runner deployment;
- access to the upstream base-image registry or required internal mirror;
- approved base-image reference and version-pinning policy;
- HTTP and HTTPS proxy endpoints and the required `NO_PROXY` domains;
- corporate CA format and how it is delivered locally, during CI, and at runtime;
- whether the CA may persist in the image;
- internal Python package-index URL and index-selection policy;
- names of CI variables or secrets used for credentials, CA files, proxy values, or mTLS;
- runtime VPN, DNS, firewall, network-mode, SSH host-key, and physical-device requirements;
- whether GitHub Actions, GitLab CI, both, or neither should be activated.

Search only the project and user-authorized sources for these values. Do not scan unrelated host
directories, credential stores, CI settings, or organization systems merely to avoid asking a
question.

## Ask when information is missing

If a required value cannot be found with confidence, stop before editing and ask the user a
specific question. Never invent a plausible organization hostname, filesystem path, proxy,
certificate location, package index, CI variable name, or network policy.

Examples of mandatory clarification:

- "What local path contains the PEM corporate CA used by `docker build`?"
- "Which internal registry reference should replace the upstream `FROM` image?"
- "Should the corporate CA be stored in the resulting image or mounted only at runtime?"
- "What are the sanitized proxy URL and required `NO_PROXY` domains?"
- "Which GitLab file variable or GitHub secret contains the CA bundle?"
- "Should the selected CI template be activated or remain under `ci/`?"

Ask only unresolved questions, preferably as one short grouped request. Explain why each answer
affects the implementation. A local certificate path is a path on the machine running
`docker build`; do not place that path directly in a portable Dockerfile or CI template.

Never ask the user to paste a password, access token, client private key, or secret certificate
material into chat or a tracked file. Ask for the name of an existing secret or file variable and
document how it must be supplied. A public CA certificate may be handled as configuration, but
follow the organization's distribution policy.

## Preserve security boundaries

Treat these as separate trust boundaries:

1. The Docker daemon must trust and reach the registry used by `FROM`.
2. Docker build steps must trust and reach package indexes and source repositories.
3. The running container must trust internal services used by tests.

Installing a CA in the image cannot repair a base-image pull failure. Document the required host
or runner setup when daemon trust is involved.

Use system certificate stores, `UV_SYSTEM_CERTS=true`, a PEM bundle through `SSL_CERT_FILE`, or an
approved equivalent. Use Docker BuildKit secret mounts for build-only sensitive files and
credentials. Use Docker's predefined proxy build arguments without persisting credential-bearing
proxy URLs in image layers.

Do not:

- disable TLS verification or add `allow-insecure-host` as a convenience workaround;
- disable SSH host-key verification;
- place credentials in Dockerfiles, image references, package-index URLs, lockfiles, or committed
  environment files;
- copy client private keys or tokens into an image;
- expose secret values in logs, command examples, step messages, diffs, or the final report;
- commit real organization values when target-repository instructions prohibit them.

## Present a plan and wait

Before editing, present:

- discovered requirements and their sources;
- unresolved values and assumptions;
- the selected trust model for daemon, build, and runtime;
- whether CI remains an inactive template or becomes active;
- exact files expected to change;
- names, but never values, of required secrets and variables;
- verification steps and any checks requiring network, Docker daemon, or CI access.

Offer two or three options when certificate delivery, image mirroring, or CI activation has
meaningful tradeoffs. Recommend the safest maintainable option. Wait for explicit approval and
also satisfy any repository-specific architectural or test-change approval gates.

## Implement the approved adaptation

1. Recheck the worktree before editing.
2. Make the smallest coherent change within the approved scope.
3. Keep upstream image and tool versions pinned according to project policy. Use an approved
   internal mirror when the closed network cannot reach the upstream registry.
4. Keep local paths out of Dockerfiles. Accept CA paths through documented CLI inputs, BuildKit
   secrets, CI file variables, or runtime mounts as approved.
5. Configure `uv` to use trusted system certificates or the approved PEM bundle. Configure an
   internal index without embedding credentials; inject authentication through named variables or
   an approved credential provider.
6. Adapt only the selected CI provider. Preserve inactive templates under `ci/` unless activation
   was explicitly approved.
7. Keep hardware tests opt-in. Do not add physical equipment to ordinary CI.
8. Update user-facing documentation with prerequisites, safe commands, required variable names,
   and the division between host administration and repository configuration.
9. Stop and request renewed approval if implementation discovers additional infrastructure,
   secrets, files, dependencies, or security tradeoffs outside the approved plan.

## Verify and report

1. Run syntax and configuration checks for every changed Docker and CI file.
2. Build the image when the required daemon, network, CA, registry, and credentials are available.
   If any are unavailable, report the exact boundary that was not verified.
3. Run the repository's required non-hardware quality gate. Never run hardware tests unless the
   user explicitly requests them and confirms that a real stand is ready.
4. Inspect the final diff for secret values, organization data prohibited by repository rules,
   insecure verification flags, unintended CI activation, and unrelated changes.
5. Report changed files, required external setup, secret and variable names, verification results,
   skipped checks, and remaining manual actions without revealing sensitive values.
