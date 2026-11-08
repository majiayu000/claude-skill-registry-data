---
name: git-workflow-docker
kind: pattern
rule: deploy-flow
description: Pattern of rule deploy-flow. Load when working with images on your own machine — starting and restarting the daemon, diagnosing a hanging command, building for the production server platform, registry login from a service. Production server commands — pattern git-workflow-restart.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-docker.md · 7eeae5a95d28 · правится надстройкой, не здесь -->

# Images on one's own machine

Pattern of the rule `deploy-flow`. What must be true meanwhile — the law
`docs/constitution/delivery.md`.

The daemon here is someone else's: on the owner's machine it holds their development storage,
their stand and the containers of their other works. Every command is written so that it can be
cancelled without asking the owner, and so that it touches nothing except what it created itself.

## When to use

- A daemon command does not answer, and the reason must be found.
- A one-off container is needed next to those already running.
- An image is being built that will go to the production server.
- The pipeline runner on this machine cannot log in to the registry.

## What is not yours is not touched

Before any action that touches the daemon whole, read what lives in it and whether it survives a
restart:

```bash
docker ps --format '{{.Names}} | {{.Image}} | {{.Status}}'
docker inspect <контейнер> --format '{{.Name}} restart={{.HostConfig.RestartPolicy.Name}}'
```

`unless-stopped` comes up by itself, `no` does not, and it is brought back by hand right after the
daemon comes up. The owner's stand is usually created with `no`: after a restart it stays down,
and its port answers with nothing — this looks like a broken stand, not like the trace of a
restart.

One's own containers are named with a prefix and removed by name. `docker system prune`,
`docker rm` by a mask and `docker volume prune` are never written: they take away what is not
yours silently.

```bash
docker rm -f <приставка>-ci-db >/dev/null 2>&1 || true   # remove the previous run
```

The port of one's own container is chosen free: the development storage port is taken, and a
foreign migration must not land in it.

```bash
lsof -nP -iTCP:<свободный порт> -sTCP:LISTEN     # empty — the port is free
```

## Space is asked before the run

The virtual machine's disk is separate from the host's disk: the host has room, inside it is
empty, and this is visible only from inside.

```bash
docker system df                       # images, volumes and build cache with the reusable share
docker run --rm alpine:3 df -h /       # how much the virtual machine itself has left
```

The shortage surfaces wearing someone else's face: a container comes up and goes out at once, the
schema audit answers about a chain that does not apply, the push gate goes red whole. By these
signs the repository gets fixed, while the cause is in the machine — so the first thing on any of
them is `docker system df`.

The host disk meanwhile stays free and says "plenty of room": the end-to-end suite fell on
`could not extend file … No space left on device` with 98 GB free on the host. Space is measured
at docker, not at the machine.

## Garbage is removed by selection, and what is not yours is excluded by label

Volumes outlive their containers and pile up silently: `docker ps` does not show them, and
`docker system df` counts them as one line. They pile up differently — a container without `--rm`
always leaves its volume, while `docker run --rm` removes an anonymous volume together with the
container itself, and adding `-v` to it is not needed: for `docker run` that flag means a mount
and without a value breaks the command. Volumes are removed by `-v` of `docker rm`, not of
`docker run`.

The sign of one's own is the absence of the compose label: a volume created by someone's
`docker compose` carries `com.docker.compose.project` and belongs to that project, including
someone else's.

```bash
docker volume ls -q -f dangling=true | wc -l          # how many unused have piled up
for v in $(docker volume ls -q -f dangling=true); do
    [ -z "$(docker volume inspect "$v" --format '{{index .Labels "com.docker.compose.project"}}')" ] \
        && docker volume rm "$v"
done
docker builder prune --builder <name> --force --filter until=24h   # yesterday's cache is nobody's, the fresh one the build needs
```

A threshold on the cache, not a full cleanup: removed whole, it makes the next build go from
scratch. The cache is pruned with the builder named: without `--builder` the command prunes the
current builder, and a pipeline running on the same machine changes which one that is, so the cache
the pipeline builds with goes with it.

A pipeline run living on the owner's machine cleans up after itself, and does it in a step that
runs on failure too: space runs out exactly when the run fails, and a cleanup skipped on failure
does not happen the one time it was needed.

Space is freed by selection, not by a general cleanup: the image cleanup script is first asked
what it would remove, and only then allowed to remove.

**Removing images is refused not by the gate but by the session mode.** In the automatic mode a
command with an irreversible deletion — removing an image, cleaning layers — is rejected whatever
the permissions, and an allow rule on the same command does not lift the refusal. A repeated
call is refused the same way: the refusal does not depend on how the command is typed, so
rewording is not the way here. Two ways from here — free space by what needs no deletion, or name
it to the owner: they switch the mode, and they remove the images too. Named at the end of the
session it costs a whole run: the pipeline stays red all that time for lack of space.

## The daemon is brought up by its own CLI

Opening the application does not bring up the virtual machine: the application counts as
running, and the daemon does not answer for hours. Only the client's own command brings it up,
and readiness is checked by the daemon itself:

```bash
docker desktop restart
until docker info >/dev/null 2>&1; do sleep 5; done
docker version --format 'daemon: {{.Server.Version}}'
```

The state the application prints speaks about the application: it answers "running" even when
the daemon accepts not a single command. The only sign of a live daemon is the answer of
`docker info`. For the first half a minute after coming up it answers with an error and writes to
its log that there is no route to the virtual machine: that is a normal start, not a breakage.

## "The command hangs" — first check whether it really hangs

Output is not wrapped in `tail`, `head` and not muted by a quiet mode: they hold it in a buffer
until the command ends, and work in progress looks hung. The direct output is read:

```bash
docker pull alpine:3            # progress is visible line by line
```

Downloads are not started in parallel. Several at once choke the channel for each other: an
image that pulls in three seconds went for half an hour — and that looked like a broken daemon,
while it was a queue arranged by the one checking.

## Where it breaks: three tiers

The tiers are checked separately, otherwise the wrong thing gets fixed. Each answers in seconds:

```bash
# 1. The machine's network: the registry gives out the manifest
curl -s -m 30 -w '%{http_code} in %{time_total}s\n' -o /dev/null '<адрес токена реестра>'

# 2. The containers' network: volume passes inside
docker run --rm alpine:3 sh -c 'time wget -q -O /dev/null <адрес пробы канала>'

# 3. The daemon: does it pull by itself
docker pull busybox:latest
```

The host pulls fast, the container pulls fast, and the download stands — the daemon is the
matter, and it is restarted. All three stand — the machine's network is the matter, and the
daemon has nothing to do with it. What the daemon itself was doing, its logs answer: the calls to
the registry, the startup and state, the virtual machine console — three different files in the
client's data directory.

## A command from a service: its own settings directory and an explicit daemon address

The pipeline runner is started as a service, and registry login from it refuses: the password is
saved by the system keychain helper, and a service has no user session. A settings directory of
its own with an empty helper does not save it — the client substitutes the helper itself and
rewrites the empty value silently. So login is not called at all, and the password is written
into the settings file directly:

```bash
export DOCKER_CONFIG="$(mktemp -d)"
export DOCKER_HOST="unix://${HOME}/.docker/run/docker.sock"
auth=$(printf '%s:%s' "${REGISTRY_USER}" "${REGISTRY_TOKEN}" | base64)
printf '{"auths":{"<реестр>":{"auth":"%s"}}}' "${auth}" > "${DOCKER_CONFIG}/config.json"
chmod 600 "${DOCKER_CONFIG}/config.json"
```

`DOCKER_HOST` here is not for decoration: a directory of one's own takes the current context with
it, and without it the client goes to the system-wide socket, which does not exist at all on a
machine with a desktop client, and answers "no such file" to anything. The connection is checked
before the build:

```bash
docker info --format 'daemon: {{.ServerVersion}}'
```

The field in `docker info` is named differently from `docker version`: the first command does not
understand the name from the second, and the connection looks unchecked though the daemon
answers.

That the password is accepted is seen by the registry's answer: to an anonymous one it answers
`401`, to an authorised one — with content or `403`, but not `401`. The directory is removed at
the end — the runner lives between runs, and the registry password would stay lying on the
owner's disk.

## Token rights are asked before the pipeline leans on them

The token used by hand and the token the rollout uses are one and the same exactly until the
first write to the image registry: its scopes may end at reading. This is learned by a refusal
when the whole rollout path is already written, so it is asked earlier — and not by a guess but
by the host's answer header:

```bash
curl -sI -H "Authorization: Bearer <токен>" '<адрес хостинга>' | grep -i '^x-oauth-scopes:'
```

The first rollout done by hand because of such a refusal does not check the rollout path — it
checks the images. This is said to the owner directly: otherwise a green production reads as a
passed pipeline.

## The image is built for the production server platform

The owner's machine and the production server can be of different architectures. Without an
explicit platform the image is built for the builder: it goes to the registry, from there to the
server and does not start there at all.

```bash
docker buildx build --platform <платформа сервера> -f <файл сборки> --output type=cacheonly .
```

`--output type=cacheonly` runs the build without saving anything — that is how time is measured
without littering the machine with an image. A foreign platform goes by emulation, so build time
on the machine and in the cloud is compared by a number, not by expectation.

A builder with the `docker-container` driver is needed for a foreign platform and is created
separately; its first startup pulls its own image from the registry:

```bash
docker buildx create --name <приставка>-ci-builder --driver docker-container
docker buildx inspect <приставка>-ci-builder --bootstrap    # shows the platforms and the state
docker buildx build --builder <приставка>-ci-builder …      # the owner's builder is not switched
```

The builder is not torn down after the run: its cache holds the layers and the package store, and
without them the next build pulls all dependencies anew. The `--use` flag is not written either —
it switches the owner's builder; instead of it `--builder` on the build itself. Builder
declarations lie in the settings directory, so under a directory of one's own they are not
visible at all — `BUILDX_CONFIG` with the address of the owner's directory helps leave them in
place.

Dependency installation inside the build is limited by the number of requests, otherwise it
brings the build down whole — and not because the channel is slow, but because hundreds of
requests choke it for themselves.

## Common misses

- **The daemon restart is declared done by the application's state.** The application says
  "running", and `docker info` at the same time answers with an error.
- **The stand is not brought back after the restart.** Its policy is `no`, and the owner finds a
  dead port instead of the stand.
- **The command output is fed into `tail`** — and a working command is declared hung.
- **Several downloads at once** — and the machine is declared slow, not one's own queue.
- **The image is built without naming the platform** — production gets an image of a foreign
  architecture, and this is visible only at the container restart.
- **One's own container took the development storage port** — the pipeline writes into the
  owner's data.
- **Registry login from a service is done by the login command** — the password goes to the
  keychain helper even from a settings directory of one's own, and the step fails before the
  build.
- **The settings directory is substituted, and the daemon address is not set** — and fixing the
  registry login looks like a fallen daemon.
- **The builder is torn down after the run** — together with the cache, and the next build goes as
  the first.
- **A general cleanup for the sake of space** — takes away someone else's images and volumes, and
  there is nothing to restore them with.
- **Space is freed by the rollout script whole.** The script is written for the production
  server: there the pipeline builds, and the server only pulls the ready-made, so as the last step
  the script tears down the builder cache. On the owner's machine the runner builds, and the same
  step leaves the builder without a cache. The script's selection of the images themselves suits
  here too — it goes by the name of its own registry, keeps the last three sha and skips running
  containers — but its tail on this machine is run only when a full build wait was agreed to.

## The age of the cache guarantees no space

A section of this tree: the runner lives on the owner's machine, and the cleanup after a run
stands in the pipeline itself.

A threshold by age frees what piled up yesterday, and the space runs out from what piled up today.
In one session the cache grew by twenty-one gigabytes, and a cleanup by day freed ninety-five
megabytes — the next run stopped on a lack of space. So the cache has two limiters, not one:

```bash
docker builder prune --force --filter until=24h        # yesterday's cache belongs to nobody
docker builder prune --force --max-used-space 10GB     # a size limit, regardless of age
```

The limit stands in one place — the step «Убрать за прогоном» in `.github/workflows/ci.yml` — and
is revised there if the builds get heavier.

Someone else's is not cured by this: thirteen gigabytes were held by a volume of an outside
project on the same machine, and a run has no right to remove it. The only thing it can do is
refuse in time and clearly.

## A lack of space is named by the step that can see it

A section of this tree.

Space that ran out brings down not the step that ate it but the one that needed it next: the stand
database goes into an endless restart, and it is the end-to-end suite that turns red — a list of
red screens on a branch that touched not a line of code. On that face the run was restarted twice
and the cause looked for in the edit.

So the stand asks the database by a health probe before the suite itself and, having waited in
vain, refuses with its log and the occupied space:

```bash
db=$(docker compose ps -q db)                                        # the name is assembled from the directory
docker inspect --format '{{.State.Health.Status}}' "$db"             # healthy or nothing
docker logs --tail 20 "$db"                                          # this goes into the refusal
docker system df                                                     # and this
```

The incident analysis is the record «2026-08-19-red-run-blamed-on-a-busy-machine» in the intake.
