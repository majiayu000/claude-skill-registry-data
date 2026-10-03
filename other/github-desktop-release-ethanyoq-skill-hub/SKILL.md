---
name: github-desktop-release
description: "Qualify Windows desktop installers in GitHub Actions and promote verified Windows/macOS assets from one frozen SHA. Use for cloud packaging, installer failures, or GitHub Release publication; not local packaging or macOS qualification."
---

# GitHub Desktop Release

Treat a desktop release as a state machine, not a build command. Keep application implementation, platform qualification, artifact identity, and public GitHub Release state as separate evidence boundaries.

`electron-development` owns Electron macOS build and qualification. This Skill may validate a macOS qualification artifact before promotion, but does not take over that platform's build work.

## Pick the smallest justified cloud path

Classify the request before spending runner time. Do not turn a past infrastructure failure into a permanent requirement for every release.

- **Compatibility preflight**: a read-only or non-promotable check that proves each requested platform can receive the frozen source: runner label availability, locked-install viability, expected architecture/native binding load, and resolved asset plan. It produces no installer and cannot justify publication.
- **Standard Windows qualification**: the default for ordinary application-source releases when the Windows installer, upgrade path, Electron/Node ABI, signing policy, and installer configuration are unchanged. It builds one installer and proves core installability.
- **Deep Windows acceptance**: adds upgrade-data, native-ABI, and project-specific migration/installer checks. Use it only when its trigger is present or the user explicitly requests it.
- **Promotion/readback**: consumes already-qualified bytes. It never builds, installs, or substitutes an artifact.

For a multi-platform release, choose between a staged canary and a parallel formal matrix from the release-risk delta. Ask `electron-development` to own macOS preflight and qualification work. A staged canary protects expensive minutes when release infrastructure changed; a parallel matrix protects elapsed time when that infrastructure is already proven.

## Establish scope

1. Read the repository's `AGENTS.md`, domain docs, packaging configuration, workflows, release scripts, and tests. Use CodeGraph first when the project is indexed.
2. Record the repository, default branch, full source SHA, tag, version, requested platforms/architectures, signing policy, expected assets, and authorization boundary.
3. Keep project facts in a repository release profile, not in this Skill. Read [references/release-profile.md](references/release-profile.md), then validate the selected profile:

   ```text
   node <skill-root>/scripts/validate-release-profile.mjs --profile <project-profile.json>
   ```

   A project may keep separate committed standard and deep profiles. Select one before qualification and pass the same `profile_path` through qualification and promotion; never alter it to fit a completed run.
4. If Windows is in scope, run the read-only adapter scan without `-OutputPath`, then read [references/stack-adapters.md](references/stack-adapters.md) and the selected adapter:

   ```powershell
   & "<skill-root>\scripts\preflight-windows-release.ps1" -ProjectRoot "<project-root>"
   ```

5. If macOS is in scope, require a qualification artifact produced under `electron-development` from the same frozen SHA. Read [references/macos-qualification.md](references/macos-qualification.md) only to validate the artifact contract used by shared promotion; do not dispatch or own the macOS build/qualification job from this Skill.

Stop at a read-only plan when repository writes, workflow dispatch, tag creation, or Release publication are not authorized.

## Choose the cloud execution strategy

Read [references/cloud-execution-strategy.md](references/cloud-execution-strategy.md) before dispatching a qualification matrix, retrying a failed run, or changing release workflows.

- Use a **staged canary** when packaging, native runtime, runner, smoke, evidence, verifier, profile, or promotion infrastructure changed, or the failure class is unresolved.
- Use a **parallel formal matrix** for an application-only release when those boundaries and the requested runner/toolchains have current green evidence.
- Run platform-neutral source validation once per SHA and bind its receipt to the exact command/toolchain. Keep Windows-native and installer acceptance on Windows; do not convert shared gating into missing platform coverage.

Compatibility probes remain non-promotable. A source or contract change requires fresh formal qualifications from the new SHA even when its canaries pass.

## Freeze formal qualification

Read [references/release-contract.md](references/release-contract.md) and [references/evidence-contract.md](references/evidence-contract.md). Before the first release qualification:

1. Freeze the source SHA, tag/version, runner labels, application toolchains, workflow identities, selected profile, exact artifact set, acceptance receipts, normalization rules, and promotion inputs.
2. 在 install、build 或 acceptance 前冻结并 hash contract。Link the immutable contract hash to every platform ledger and run.
3. Replay real platform receipts through the final consumer when changing an evidence producer/writer, receipt verifier, shared promotion consumer, qualification workflow/adapter, or release-contract schema:

   ```text
   node <skill-root>/scripts/replay-release-evidence.mjs --profile <project-profile.json> --evidence-root <real-fixtures>
   ```

4. Use real platform-produced bytes as positive fixtures. Build negative fixtures independently from the verifier. Read [references/receipt-replay.md](references/receipt-replay.md). A source-only release may reuse a previously verified adapter; do not make replay a per-release cloud-dispatch blocker.
5. For first-time Windows infrastructure with no real fixtures, allow at most one non-publishing Windows canary to collect receipts. Freeze those bytes, add them to the replay set, fix locally, and only then start formal qualification. Any missing macOS canary belongs to `electron-development`.

The formal dispatch gate is complete when the profile and contract are valid, the selected execution strategy's early gates are green, and the receipt semantics are known. No source gate or compatibility canary is a qualification result.

## Qualify Windows artifacts

Dispatch Windows qualification only after the release inputs are bound to the frozen SHA and contract meaning, and the early gates required by the selected cloud strategy are green. A low-risk parallel matrix does not acquire an extra serial compatibility canary merely because multiple platforms are requested. Build the installer once, then use those exact bytes for acceptance, hashing, upload, and later promotion. When macOS is also requested, `electron-development` owns that platform's qualification against the same frozen SHA.

For Windows qualification:

1. Checkout the full frozen SHA with read-only permissions and `persist-credentials: false`.
2. Verify the runner image and application toolchain against the frozen contract.
3. 执行 stack 专属的 locked install, then the project build/package command. Preserve a project-required Windows-native test receipt, but avoid re-running a proven same-SHA suite.
4. 对 installer 做真实安装、launch/mount, quiet/error observation, installed smoke, and quiet uninstall/eject acceptance where the platform/package supports those operations. Keep the bounded quiet window and product-scoped residual checks. Record an unsupported core operation as blocked scope, not silent success.
5. Record signing or notarization status, validation result, and unsigned/unnotarized distribution impact.
6. Upload only the exact contract asset set plus contract, ledger, manifest, checksums, required receipts, and sanitized diagnostics.

The **standard** Windows profile normally contains core receipts such as `install`, `launch`, `quiet-window`, `error-dialogs`, `packaged-smoke`, `uninstall`, and `signing`. It must not silently claim upgrade or native-ABI coverage it did not run.

Require **deep** Windows acceptance when any of these applies:

- first public qualification for the installer path, or a change to NSIS/electron-builder configuration, app ID, install scope/path, silent parameters, custom installer hooks, signing, update channel, or updater format;
- a change to persistent-data format, migration, user-data location, or upgrade/downgrade behavior;
- a change to Electron, Node, a release-critical native module, its rebuild process, or its target architecture;
- an explicit project policy or user request for upgrade/native verification.

Deep acceptance adds the project-specific upgrade-data and native-ABI checks, plus any directly affected test. It does not justify deleting the core installer checks or substituting a different platform. Conversely, ordinary source-only changes do not automatically require an upgrade fixture or a separate ABI rebuild test when the relevant packaging boundary is unchanged.

Windows Electron/NSIS qualification must follow [references/electron-nsis.md](references/electron-nsis.md). A macOS qualification artifact is an external input owned by `electron-development`; validate it against [references/macos-qualification.md](references/macos-qualification.md) before promotion. Qualification success proves an Actions artifact, not a public Release.

Use [assets/electron-nsis-qualification.yml](assets/electron-nsis-qualification.yml) as the fail-closed Windows qualification starting point. The bundled [assets/macos-qualification.yml](assets/macos-qualification.yml) is retained only as a contract-compatible handoff template for `electron-development`; using it does not transfer macOS execution ownership to this Skill.

Promotion is shared infrastructure, not a project adapter. Reuse [scripts/github-desktop-promotion.mjs](scripts/github-desktop-promotion.mjs), [scripts/validate-release-profile.mjs](scripts/validate-release-profile.mjs), and [assets/github-desktop-release-promotion.yml](assets/github-desktop-release-promotion.yml) rather than reimplementing profile validation, artifact selection, same-SHA/contract binding, manifest hashing, resume, upload, channel, or readback logic per project. A project-specific workflow wrapper may adapt invocation, but it must preserve the verified consumer contract. Run the shared offline tests after changing those scripts:

```text
node <skill-root>/scripts/test-github-desktop-promotion.mjs
```

## Diagnose without cloud trial-and-error

Read [references/failure-classification.md](references/failure-classification.md) and [references/failure-playbook.md](references/failure-playbook.md).

1. Classify every failure as `product`, `build`, `acceptance`, `gate-false-positive`, or `promotion` before deciding whether a rebuild is justified.
2. Preserve the run URL/ID, attempt, head SHA, runner/toolchain, failing stage, contract, manifest, receipts, and the smallest sanitized log excerpt.
3. Change one falsifiable hypothesis at a time. For a preflight failure, re-run only that preflight after the fix; for a formal failure, use local or non-promotable replay before another full qualification.
4. After two consecutive failures in the same stage, stop. Do not start a third run until a unified root cause, ranked alternatives, and local red-to-green replay exist.
5. Keep binary identity and normalized semantics separate: installer/DMG/ZIP/blockmap bytes use raw SHA-256; eligible UTF-8 text may additionally use newline-canonical SHA-256. Never compare cross-OS text raw hashes as semantic identity.

When a fix changes the SHA, cancel in-flight runs for the superseded SHA and forward-audit every remaining stage before dispatching the new formal matrix. Do not discover package-smoke, evidence-finalization, and promotion prerequisites one expensive run at a time. A local promotion-tool failure with unchanged qualified bytes is not a reason to rebuild.

Do not restart a full Windows gate merely because another platform has already exposed a known compatibility blocker. Once the repaired source SHA is ready, every requested platform still receives a clean, same-SHA formal qualification.

## Promote the qualified bytes

Read [references/github-release-state-machine.md](references/github-release-state-machine.md).

Before downloading large qualification artifacts, run the zero-side-effect local checks in [references/promotion-preflight.md](references/promotion-preflight.md). A missing archive tool, wrong authenticated account, invalid profile, unwritable output plan, or insufficient disk is a local promotion blocker; repair it and resume from the same immutable run identities without rebuilding.

1. Accept only unique, unexpired qualification artifacts whose workflow, run ID, attempt, head SHA, contract, manifest, and platform all match.
2. Require every requested platform to qualify the same source SHA. Promotion may download and verify artifacts; it must not install, build, or substitute a same-named artifact.
3. Pass `qualification_runs_json` as an exact platform mapping of positive integer `runId`, `attempt`, and `artifactId`. The shared script verifies the profile's workflow and artifact name in addition to those immutable identities.
4. Require every schema-v2 manifest and run ledger to bind `contractRawBytesSha256` and `profileRawBytesSha256`. `release-contract.json` and `signing.evidencePath` must be members of the exact manifest/checksum set; every required platform must carry identical contract/profile raw-byte hashes, and the latter must equal the profile file used for promotion.
5. Verify the exact asset set, raw byte hashes, signing disclosures, tag availability, default-branch ancestry, and existing draft/tag/assets in a read-only job.
6. Grant `contents: write` only to the final publish job. Resume a partial draft only when its provenance is exact and every already uploaded asset is an exact subset by name, size, state, and GitHub `sha256:` digest; upload only the missing assets. Never overwrite or delete a mismatch.
7. After the final mutation, perform bounded authoritative readback of tag target, Release state, draft/prerelease/latest flags against the profile's release-channel policy, exact assets, uploaded state, platform digests, release notes, signing/notarization disclosures, and URL. A verified draft reports `draftVerified: true` and `publicationVerified: false`; only a verified non-draft public state may report publication success.

Workflow success is not publication success. A missing or unverifiable readback leaves the release incomplete.

## Report evidence states

Report `mode`, `qualification tier`, `frozen inputs`, `preflight by platform`, `source-validation receipt`, `qualification by platform`, `failure classification`, `signing/notarization`, `promotion identity`, `authoritative readback`, `unverified/blocked`, and `next action`.

Use only these completion claims:

- `build-success`: packaging command produced an artifact.
- `qualification-success`: a platform artifact passed its frozen acceptance contract.
- `promotion-success`: qualified bytes were promoted without rebuilding.
- `publication-success`: authoritative GitHub readback matches the full release contract and the Release is not a draft.
