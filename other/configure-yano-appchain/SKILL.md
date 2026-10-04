---
name: configure-yano-appchain
description: Create, explain, update, validate, and diagnose Yano app-chain projects using the version-matched blueprint, capability catalog, and appchain CLI. Use for topology, state-machine, effects, integrations, deployment exports, drift checks, and custom-plugin metadata. Never invent Yano properties or handle secret values.
---

# Configure Yano App-Chain

Use the `yano.sh` or `yano` executable shipped with the target Yano distribution. Treat its
catalog, recipes, generated lock file, and validation results as authoritative for that release.

## Workflow

1. Run `./yano.sh appchain recipes` and `./yano.sh appchain capabilities` before choosing features.
2. Create or edit only `appchain.yaml`. Do not hand-edit generated runtime files.
3. Run `./yano.sh appchain render`, then `./yano.sh appchain config validate --mode project`.
4. Run `./yano.sh appchain doctor` before startup or delivery.
5. Use `./yano.sh appchain diff` before applying a blueprint change and `./yano.sh appchain drift`
   against running nodes when identities are available.
6. Summarize selected capabilities, generated files, unresolved operator inputs, validation
   coverage, and any warnings.

## Safety Rules

- Never request, print, copy, infer, or commit secret values. Refer only to documented
  environment-variable or secret-provider names.
- Never invent configuration keys, values, defaults, recipes, or compatibility claims.
- Keep blueprint, resolved-config, release, plugin-catalog, and consensus identities distinct.
- Do not mutate a running node or call privileged runtime APIs unless the user explicitly asks.
- Treat custom-plugin metadata as PARTIAL coverage unless Yano reports FULL coverage. Verify
  signed metadata and runtime-manifest binding before trusting a third-party artifact.
- If a requested capability is unavailable in this release, report it as unsupported. Do not
  bypass the blueprint by hand-writing runtime configuration unless the user explicitly chooses
  an advanced unsupported workflow.

## Command Patterns

```bash
./yano.sh appchain init --recipe <recipe> --network <network> --members <count> \
  --output <project-directory>
./yano.sh appchain capabilities
./yano.sh appchain render <project-directory>
./yano.sh appchain config validate --mode project <project-directory>
./yano.sh appchain doctor <project-directory> --distribution <yano-directory-or-zip>
./yano.sh appchain diff <old-lock> <new-lock>
./yano.sh appchain gitops <project-directory> --target helm --output <empty-directory>
./yano.sh appchain gitops <project-directory> --target kustomize --output <empty-directory>
./yano.sh appchain drift <project-directory> --peer <node-identity-url>
./yano.sh appchain metadata verify <plugin-jar> --trust-key <key-id=public-key-hex>
```

Read command help from the version-matched executable when an option is uncertain.
