---
name: storybook-dev-host-launch
description: >-
  Use when the repository's Storybook dev-server target appears to hang and the browser cannot reach
  port 6006, when Storybook must be opened in a real browser for interactive component work, or when
  checking whether a repository's compose stack actually publishes the Storybook port to the host.
---

# Reaching Storybook from the browser

## Profile keys consumed

- `capabilities.storybook`
- `make.storybook_build`
- `framework.package_manager`

## Overview

The Storybook dev-server target only reaches a browser when two conditions hold together: the
compose service publishes the Storybook port, and the dev server binds `0.0.0.0` rather than
loopback inside the container. Where either is missing the command looks like a hang — the server is
running and simply unreachable. Check the compose file before assuming the target is broken.

## Capability gate

This skill applies only where `capabilities.storybook` is `true`; when it is `false` there is no
Storybook lane to reach, so record the skill SKIPPED with a capability-absent note and stop. The
static-build target is `make.storybook_build`; skip any step that depends on it with a recorded note
when it maps to `null`. There is no profile key for the Storybook **dev** server — resolve that
target from the repository's own Makefile, by purpose.

## When to use

- The Storybook dev-server target prints its banner and the browser cannot connect on port 6006.
- Interactive component work needs hot reload against live stories.
- Verifying a Storybook story renders before opening a pull request.
- Not for: the component-library shape's visual-test Storybook — a separate compose service serves a
  static build (the artifact produced by `make.storybook_build`) on the compose network, reached by
  the test runner rather than by a developer's browser.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): no — the dev service already publishes 6006.
- **Next.js app shape** (routed pages, no aggregate duplication gate): partial — the dev service
  publishes only 3000, so container mode is unreachable; the Makefile's `EXEC_MODE` switch is the
  supported escape hatch.
- **Component-library shape** (Storybook-first, no bootable app, published package): yes — the
  Storybook dev-server target runs through `docker compose run --rm` against the package-runner
  service and `docker-compose.yml` declares no `ports:` key at all, so nothing is bridged to the
  host.

## Why the container path fails

`docker compose run` does not apply the service's published ports unless asked to, and a service
with no `ports:` mapping has nothing to publish in the first place. The Storybook dev server binds
6006 inside the container's network namespace; without a mapping, the host has no route to it. A
`--host 0.0.0.0` flag alone does not help — it fixes the bind address, not the missing bridge.

In the component-library shape the separate compose service that serves a _static_ Storybook build
for Playwright is also unpublished by design: the test runner reaches it by service name over the
compose network.

## Running it where the browser can reach it

In the component-library shape there is no port to publish, so run the dev server outside the
container through the runner named by `framework.package_manager`. This is the exception, not the
pattern — the type-check target and the Jest suites still run inside the container there:

```bash # profile-example
bun x storybook dev -p 6006
```

In the Next.js shape, keep the make target and flip the execution mode; the value is a validated
enum, so a typo is a hard error rather than a silent fallback:

```bash # profile-example
EXEC_MODE=host make storybook-start
```

Either way, stop it with `Ctrl+C` in the foreground shell, or by killing the process id if it was
backgrounded. Both host paths need dependencies installed on the host; the container's package
directory is not shared with it.

## Common mistakes

- Reading "no output after the banner" as a hang — the server is up and the port is not bridged.
- Adding `--host 0.0.0.0` and expecting that to be enough when the service publishes no port.
- Pointing a browser at the static Storybook service used by visual tests — it is deliberately
  internal to the compose network.
- Assuming the behaviour is the same in every repository shape — the compose port map differs, so
  check it rather than porting a workaround that is unnecessary elsewhere.
