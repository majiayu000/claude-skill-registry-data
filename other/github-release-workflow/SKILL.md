---
name: github-release-workflow
description: The GitHub Actions release workflow and the semver commit-marker convention. Use when creating or changing .github/workflows/release.yaml, adding a build job or a platform to the matrix, wiring container publishing, or working out how a release version is chosen. Triggers on release.yaml, gh release create, draft releases, actions/checkout, actions/setup-go, actions/setup-node, docker/login-action, docker/build-push-action, multi-arch image publishing, [minor-release], and [major-release].
user-invocable: false
---

# GitHub Release Workflow

**One workflow per repository, triggered by a push to the default branch, that tests, cuts a draft release, builds every artifact in parallel, then publishes.**

Releases are never triggered by pushing a tag. The version is calculated from the last commit message by the Makefile, and the workflow calls that same calculation, so the number in CI is the number `make version` prints on a laptop.

## Versioning

| Last commit contains | Bump | Example |
|---|---|---|
| nothing special | patch | `v1.0.0` to `v1.0.1` |
| `[minor-release]` | minor | `v1.0.1` to `v1.1.0` |
| `[major-release]` | major | `v1.1.0` to `v2.0.0` |

Patch is the default because most commits are one, and a convention that requires a marker for the common case gets forgotten and produces no release at all.

```bash
git commit -m "Add new feature [minor-release]"
git commit -m "Breaking API change [major-release]"
git commit -m "Fix bug in handler"
```

## Shape

Five phases, in order:

1. **test** gates everything. No release exists if the suite fails.
2. **create-release** calculates the version and cuts a draft.
3. **artifacts** build in parallel, each uploading into that draft.
4. **publish** flips the draft to public once every artifact has landed.
5. **cleanup-on-failure** deletes the draft when any earlier job failed.

The draft is what makes the release atomic. Publishing first and uploading after leaves a visible release with missing binaries for as long as the matrix runs, and a failed job leaves it that way permanently.

## Actions

Actions are pinned to a major tag, verified against the action's own releases rather than written from memory.

| Action | Pin |
|---|---|
| `actions/checkout` | `v7` |
| `actions/setup-go` | `v7` |
| `actions/setup-node` | `v7` |
| `docker/login-action` | `v4` |
| `docker/setup-qemu-action` | `v4` |
| `docker/setup-buildx-action` | `v4` |
| `docker/build-push-action` | `v7` |

## Secrets

`GITHUB_TOKEN` is supplied automatically as `github.token` and needs no configuration.

| Secret | Needed by |
|---|---|
| `DOCKER_ACCESS_TOKEN` | any project that publishes a container image |

A CLI Only project needs no secrets at all.

## Go Template

```yaml
name: Release

on:
  push:
    branches: [main]

permissions:
  contents: write
  packages: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: actions/setup-go@v7
        with:
          go-version: '1.27'

      # //go:embed static needs the tree populated before anything compiles.
      # Delete this step for CLI Only.
      - name: Download assets
        run: make assets

      - name: Run tests
        run: go test ./...

  create-release:
    needs: test
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
      release_created: ${{ steps.create_release.outputs.release_created }}
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0

      - name: Calculate version
        id: version
        run: echo "version=$(make -s version)" >> "$GITHUB_OUTPUT"

      - name: Create draft release
        id: create_release
        run: |
          gh release create "${{ steps.version.outputs.version }}" \
            --title "Release ${{ steps.version.outputs.version }}" \
            --draft \
            --notes "[APP_NAME] ${{ steps.version.outputs.version }}" \
            --target ${{ github.sha }}
          echo "release_created=true" >> "$GITHUB_OUTPUT"
        env:
          GH_TOKEN: ${{ github.token }}

  # Delete this job for CLI Only.
  docker:
    needs: create-release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - uses: docker/setup-qemu-action@v4

      - uses: docker/setup-buildx-action@v4

      - uses: docker/login-action@v4
        with:
          username: [GITHUB_USER]
          password: ${{ secrets.DOCKER_ACCESS_TOKEN }}

      - uses: docker/build-push-action@v7
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          build-args: |
            VERSION=${{ needs.create-release.outputs.version }}
          tags: |
            [GITHUB_USER]/[APP_NAME]:latest
            [GITHUB_USER]/[APP_NAME]:${{ needs.create-release.outputs.version }}

  binaries:
    needs: create-release
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [linux, darwin]
        arch: [amd64, arm64]
    steps:
      - uses: actions/checkout@v7

      - uses: actions/setup-go@v7
        with:
          go-version: '1.27'

      # Delete this step for CLI Only.
      - name: Download assets
        run: make assets

      - name: Build binary
        run: make build-for GOOS=${{ matrix.os }} GOARCH=${{ matrix.arch }} VERSION=${{ needs.create-release.outputs.version }}

      - name: Upload release asset
        run: |
          BINARY=$(ls *-${{ matrix.os }}-${{ matrix.arch }} 2>/dev/null | head -1)
          gh release upload "${{ needs.create-release.outputs.version }}" "$BINARY" --clobber
        env:
          GH_TOKEN: ${{ github.token }}

  publish:
    needs: [create-release, docker, binaries]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7

      - name: Publish release
        run: gh release edit "${{ needs.create-release.outputs.version }}" --draft=false
        env:
          GH_TOKEN: ${{ github.token }}

  cleanup-on-failure:
    needs: [create-release, docker, binaries, publish]
    if: always() && (needs.docker.result == 'failure' || needs.binaries.result == 'failure' || needs.publish.result == 'failure') && needs.create-release.outputs.release_created == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Delete draft release
        run: gh release delete "${{ needs.create-release.outputs.version }}" --yes
        env:
          GH_TOKEN: ${{ github.token }}
```

`fetch-depth: 0` in `create-release` fetches the full history and its tags, which the version calculation reads. The default shallow clone has no tags and every run would compute `v0.0.1`.

Both build jobs run `make assets` rather than restoring a cached tree, because the asset directories are not in the repository and the Makefile is the only definition of what they contain.

`cleanup-on-failure` guards on `release_created` so a failure in the version step, before any draft exists, does not try to delete one.

The docker job builds `linux/amd64` and `linux/arm64` into one manifest. `build-push-action` is used rather than `make docker-push` because the buildx driver and the registry cache belong to the runner rather than to the Makefile, and a plain `docker build` on the runner would publish an amd64 image that an arm64 host cannot run.

QEMU is registered before buildx because it is what lets a non-native stage execute at all. A Go build cross-compiles and only its final stage is emulated, so the setup step costs a second; a Node build with a native addon runs its whole builder emulated and takes materially longer.

## Node Template

The Node workflow is the same five phases with different build steps. The matrix runs on architecture-native runners, since a native addon cannot be cross-compiled.

```yaml
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-node@v7
        with:
          node-version: 24.20.0
      - run: npm_config_build_from_source=true npm ci
      - run: node --test

  artifacts:
    needs: create-release
    runs-on: ${{ matrix.runner }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - { os: linux,  arch: x64,   runner: ubuntu-24.04 }
          - { os: linux,  arch: arm64, runner: ubuntu-24.04-arm }
          - { os: darwin, arch: arm64, runner: macos-14 }
          - { os: darwin, arch: x64,   runner: macos-15-intel }
    steps:
      - uses: actions/checkout@v7

      - uses: actions/setup-node@v7
        with:
          node-version: 24.20.0

      - name: Install deps, compiling the addon from source
        run: npm_config_build_from_source=true npm ci

      - name: Vendor assets and assemble the bundle
        run: make bundle

      - name: Smoke-test the bundled tarball
        run: bash scripts/smoke-test.sh ${{ matrix.os }} ${{ matrix.arch }}

      - name: Upload release asset
        run: gh release upload "${{ needs.create-release.outputs.version }}" dist/[APP_NAME]-${{ matrix.os }}-${{ matrix.arch }}.tar.gz --clobber
        env:
          GH_TOKEN: ${{ github.token }}
```

`fail-fast: false` lets the other platforms finish when one fails, so a single broken runner produces one missing artifact to investigate rather than four.

Windows is not in the matrix. Nothing here is tested on it, and shipping an untested artifact is worse than shipping none.

A pure-JS app swaps the bundle step for `make binary` and uploads that file instead.

## Chrome Extension

The extension workflow keeps `test`, `create-release`, `publish`, and `cleanup-on-failure` unchanged, and replaces the build jobs with a single job that runs `make build` and uploads the zip. There is no matrix, since the artifact is platform-independent.
