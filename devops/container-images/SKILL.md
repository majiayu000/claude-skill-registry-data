---
name: container-images
description: "Container image conventions: every image targets linux/amd64 and linux/arm64, and a base image is pinned by its multi-platform manifest list digest. Use when writing or changing a Dockerfile, pinning a base image digest, or setting up a CI job that builds and publishes a container image."
---

# Container images

Every image this organisation builds and publishes runs on an amd64 machine and an arm64
machine, natively, without emulation at pull time.

## When to use

- Writing or changing a Dockerfile.
- Pinning or updating a base image.
- Setting up or reviewing a CI job that builds or publishes a container image.

## Rules

### Platforms

- An image is built and published for `linux/amd64` and `linux/arm64`. Both, every time, not
  only the platform the build happened to run on.
- The architecture of the machine that will pull the image is not known at build time. Building
  one platform only moves the failure to whoever pulls it on the other one.

### Base image digests

- A base image is pinned by digest, never by a floating tag.
- The digest pinned is the multi-platform manifest list's own digest, never one platform's
  manifest digest underneath it. A manifest list (also called an image index) is the object a
  multi-arch tag resolves to; it holds one manifest digest per platform, each with its own hash.
- Tell them apart with `docker buildx imagetools inspect <image>:<tag>`. A manifest list digest's
  output lists several `Platform:` entries, each with its own digest, under one top digest. A
  platform specific digest's output shows exactly one platform and no list above it.
- Pin the digest printed for the manifest list itself, never one of the nested platform entries.
  A platform specific digest is exactly the mistake this rule exists to prevent: it builds clean
  on that one platform and silently emulates, or fails outright, on every other one.
- A base image with no `linux/arm64` manifest in its list is named in the Dockerfile, as a
  comment next to the `FROM` line, and in the pull request. State the consequence: the image
  being built cannot run natively on arm64 either, as long as that base image stays amd64 only.
  Pinning amd64 only is a stated exception, never a silent default.

### CI build and publish

- The build job sets the build action's `platforms` input to `linux/amd64,linux/arm64`, on every
  build that publishes, not only on a release or a tag.
- A platform the runner is not native to builds under QEMU emulation, through the matching setup
  action, unless a native runner for that architecture is available.
- An emulated build is several times slower than a native one and that cost lands on every
  build, every change. Where a native runner per architecture exists, prefer one job per
  architecture, each building its own platform natively, with the per-architecture images merged
  into one manifest list as a separate step, over a single job emulating the platform it lacks.
- The published reference is one tag resolving to the manifest list, both platforms underneath
  it. A tag per architecture, with no manifest list tying them together, is not multi-platform:
  nothing picks the right one for the puller.
- After publishing, `docker buildx imagetools inspect` the published tag and confirm both
  `linux/amd64` and `linux/arm64` are listed, before relying on the job as done.

## Guardrails

- Never pin a base image by a platform specific digest.
- Never publish an image for one platform only without naming the exception and its consequence.
- Never call a build multi-platform without the manifest list inspection confirming both
  platforms landed.
- Never let an emulated build stand in for a native runner per architecture without a reason the
  job's cost does not matter here.

## References

- `release-conventions` for the Renovate rule that keeps a pinned digest current.
- `ci-conventions` for workflow shape: jobs, permissions, pinned actions.
- <https://docs.docker.com/dhi/explore/security-concepts/digests/>
- <https://github.com/docker/build-push-action>
