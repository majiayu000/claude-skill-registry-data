---
name: python-container-image
description: Use when a Python program that ships as a container image gets its image build or changes it — a Dockerfile and its ignore file, the base image, how dependencies get in, the user the process runs as, or how the platform's stop signal reaches the process. Owns a runtime image carrying only the installed program, an install of exactly what the lock file pins that fails where the lock has drifted, one interpreter across build and runtime, a non-root user named by number, no secret in any layer, a build context that admits only what the build reads, one image per runnable distribution and for every environment, unbuffered output, a server reachable from outside the container, and a stop signal the process acts on. Holds for a service of either architecture family and for a CLI tool shipped as an image; a library, and a CLI tool distributed as a package, have no image. Several members and their compose file are `python-workspace`; which version a tag names is `python-toolchain`. - Also when asked to containerize or dockerize a service, write a Dockerfile or a `.dockerignore`, make an image smaller, stop a container running as root, pass a private package index token into a build, or why a container takes the whole timeout to stop.
---

# Python Container Image — the build that ships a program

The image a runnable Python program ships in, written **once** per program: what goes into it, what
stays out, who the process runs as and how it is told to stop. None of it recurs per feature. What the
program does once it starts, and once it is told to stop, is not this skill's; where a member's image
sits among several, and the compose file that runs them, is `python-workspace`.

## When to use vs. neighbours

- Which version a base image, a builder image or the package manager's image names → `python-toolchain`
  rule 12; this skill names where those tags go, never their value.
- The interpreter floor the base image has to satisfy → `python-style`, written by `python-toolchain`.
- Several distributions in one repository, the compose file and one profile per runnable member →
  `python-workspace`; what goes inside a member's `Dockerfile` is still this skill's.
- What the program reads from its environment at start-up, and the secret type that carries a
  credential → `python-settings`.
- A comment in the `Dockerfile` or its ignore file → `python-style`'s **Comments**, which holds in every
  file the project writes by hand.
- Where log events go, and a program whose stdout is its result → `python-logging`.
- One console script per process, or per CLI app → `python-toolchain`; the image runs one of them.
- What the process does once the stop signal arrives → not this skill, which only delivers the signal.
- A library, or a CLI tool its users install as a package → not this skill; it ships as a
  distribution, released under `python-versioning`.

## Templates — Docker and uv

One distribution at the repository root, laid by `python-toolchain`. Both files sit beside its
`pyproject.toml`.

### `Dockerfile`

```dockerfile
ARG PYTHON_IMAGE=python:<pinned-tag>

FROM ${PYTHON_IMAGE} AS build
COPY --from=ghcr.io/astral-sh/uv:<pinned-tag> /uv /bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM ${PYTHON_IMAGE}
RUN groupadd --system --gid 10001 app \
 && useradd --system --uid 10001 --gid app --no-create-home app
COPY --from=build /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
WORKDIR /app
USER 10001:10001
# only where nothing in the process handles SIGTERM itself
STOPSIGNAL SIGINT
CMD ["python", "-m", "myapp"]
```

### `.dockerignore`

```
*
!pyproject.toml
!uv.lock
!src/
# only where pyproject.toml names a readme
!README.md
**/__pycache__
```

`PYTHON_IMAGE` is declared once and both stages start from it, so the environment built in the first
runs on the interpreter it was built against (rule 3); its tag names the interpreter version, a slim
variant and the distribution release, and like the package manager's tag it is read per
`python-toolchain` rule 12. The first sync installs the dependencies alone from the lock file, so a
change to the source rebuilds only the second; `--locked` makes either fail where the lock disagrees
with `pyproject.toml` (rule 2); `UV_NO_DEV` leaves the development group out; `--no-editable` installs
the program into the environment, which is then all the runtime stage copies (rule 1). The copied files
stay root's, so the process cannot rewrite its own code (rule 4).

The last line is the program's own command, in exec form (rule 9): `python -m myapp` only where the
program has a `__main__` module, a console script where it declares one, a server's own command where
an HTTP server runs it — a server or a loop that handles SIGTERM itself drops `STOPSIGNAL`. A program
run with arguments, a CLI tool, names its command as `ENTRYPOINT ["myapp"]` instead of `CMD`, so that
`docker run <image> <arguments>` appends them rather than replacing the program (rule 12).

**In a workspace**, the build context is the repository root and the `Dockerfile` sits in the member's
directory. Both syncs take `--package myapp`, and the first, which sees only the root's `pyproject.toml`
and lock, becomes `uv sync --frozen --no-install-workspace --package myapp`; the second keeps
`--locked`. The ignore file sits beside that `Dockerfile` as `Dockerfile.dockerignore`, since one at
the context root would serve every member at once, and admits files rather than member directories:
the root's `pyproject.toml` and lock, **every member's `pyproject.toml`** — the second sync checks the
lock against the whole workspace, and a member it cannot see fails `--locked` — and the `src/` (and,
where named, the readme) of the member and of each library it depends on, never a member directory
whole, which holds that member's dotenv file.

## Other bindings

- **Another builder — Podman or Buildah.** The file is read as written, and build secrets and cache
  mounts work the same; the CLI changes, nothing in `## Rules` does.
- **pip in place of uv.** The lock is exported to a requirements file with hashes and installed with
  `pip install --require-hashes --no-deps` into a virtual environment the runtime stage copies; a hash
  mismatch is the drift failure. The two stages, the copied environment and every rule are unchanged.
- **A distroless or other minimal runtime base.** Its interpreter must sit at the build stage's path,
  so the build stage comes from the same vendor's matching image; it has no shell and no `useradd`, so
  the user is the base's own non-root UID, and exec form is the only form that runs.
- **An init process.** A program that starts child processes runs under a minimal init (`tini`, or the
  runtime's own `--init`) that reaps them and forwards the signal it receives; the stop signal rule 9
  declares is unchanged.
- **Buildpacks.** No `Dockerfile` is written; the builder decides the stages, so every rule is checked
  on the image it produces rather than on a file.

## Rules

1. **The runtime image carries only the installed program and its dependencies.** It is built in a
   stage separate from the one it runs in and receives only the installed environment: no compiler, no
   package manager or its cache, no development dependency, no source tree, no tests. The program is
   therefore an installable distribution (`python-toolchain` rule 1); a project that is not one becomes
   one before it gets an image, or its runtime stage holds no program.
2. **The image installs exactly what the lock file pins, and the build fails where the lock has drifted
   from the declared dependencies.** It never resolves versions of its own, so the image runs the set
   the tests ran against; a lock that no longer matches `pyproject.toml` stops the build rather than
   being silently re-resolved or ignored.
3. **One interpreter, named once, for build and runtime.** The environment the build stage installs
   points at that stage's interpreter, so the runtime carries the same interpreter at the same path;
   the version it carries satisfies `requires-python` (`python-style`), and its tag is read per
   `python-toolchain` rule 12.
4. **The process runs as a non-root user, named by number, and can write almost nothing.** A numeric
   UID is what lets a platform verify the image is non-root before running it; a user given only by
   name cannot be checked. The program's own files are not writable by that user. Where the program
   writes files, it writes under one directory named by a setting, which the platform mounts or the
   image creates owned by that user; nothing else becomes writable.
5. **No secret reaches any layer.** A credential the build needs — a private package index's token —
   reaches the one step that uses it as a build secret, never as a build argument, an environment
   variable or a copied file: each of those stays in the image or its history, and a later step that
   deletes it removes nothing from the layer before. A credential the program needs arrives from the
   environment when it starts (`python-settings`).
6. **The build context admits only what the build reads.** The ignore file is an allow-list of files
   — the project file, the lock, the source — so a dotenv file, the version-control directory, a local
   virtual environment, tests and whatever is added to the tree later stay out without anyone listing
   them.
7. **One image for every environment.** Nothing environment-specific is built in — no setting's value
   in an `ENV` line, no dotenv file, no per-environment build — so the image the tests passed is the
   image that is promoted, and only its environment differs.
8. **Output is unbuffered.** Outside a terminal the interpreter buffers standard output in blocks, so a
   process killed mid-run loses whatever it wrote last, which is the output that explains why it died.
9. **The platform's stop signal reaches the program, and is one it acts on.** The command starts the
   program directly, in exec form, with nothing chained in front of it — a shell receives the signal in
   its place. The first process in a container is not killed by a signal it has no handler for, and the
   interpreter installs one only for the interrupt signal, so a program with no handler of its own runs
   under the default termination signal until the stop timeout and is killed. The image therefore
   declares the interrupt signal as its stop signal, unless something in the process handles the
   platform's default one.
10. **One image per runnable distribution.** A distribution with several processes ships one image and
    starts each process with a different command, never one image per process built from the same
    source.
11. **A server listens on the container's interfaces.** A server's default address is loopback, which
    nothing outside the container reaches; its address and port come from its settings
    (`python-settings`), and inside a container the address is all interfaces.
12. **A program run with arguments receives them.** Each run's arguments reach the program, never
    replace it, so the image fixes the command and leaves the arguments to the caller.

## Hard stops

- Asked for an image for a library, or for a CLI tool its users install as a package → stop, it has
  none; it ships as a distribution, released under `python-versioning`.
- Asked for a compose file or a profile across several members of one repository → stop, use
  `python-workspace`. A single distribution's compose file is no skill's in this catalogue.
- Asked how the program drains work or exits once told to stop → stop, not this skill; it only
  delivers the signal.
