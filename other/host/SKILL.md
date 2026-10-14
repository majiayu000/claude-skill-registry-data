---
name: host
description: Take a machine that has Docker to a Foundry host that answers. Covers the clone, the image, the sign-ins, installing the plugins, and the calls that prove it. Use when setting a machine up to run Foundry work. Not for joining a host to a repository, which is floor's join.sh.
---

# Host

> "Docker installed is not a host. A host is a machine something answers in."

## When

A person points at a machine and says *set this up to work on its own*.

Once per machine. Docker is the one thing it must already have.

## The path

### 1. Ask Docker

```sh
docker info
```

Anything but a clean answer stops every step below, and `bin/host.sh` refuses at exit 2 rather
than guessing.

### 2. Clone Foundry onto the machine

```sh
git clone https://github.com/attac-t/the-foundry.git
cd the-foundry
```

**The image carries no Foundry.** `bin/host.sh` is in this clone, and every container mounts the
clone at `/src`, read-only. **That mount is how the scripts get in.** The plugins come in at step
4's first start when `FOUNDRY_KEYS` is set, and step 6 says how, and what to do without it.

### 3. Name a place for the sign-ins

`FOUNDRY_KEYS` names it, and the value's own shape picks the mechanism. A bare word is a Docker
volume. Anything holding a slash is a directory on this machine.

```sh
FOUNDRY_KEYS=foundry-keys
```

**Unset, nothing is kept.** Every sign-in below is then asked again in the next container, and that
is the default everywhere.

**What it holds:** three directories and nothing above them — where the forge, the harness and the
judge each keep their own. The host's own credential stores never cross in. That is the owner's
decision, in writing, and this switch is the whole of the exception.

**Who can read it, and it is not comfortable:** anyone who can run as this user. **A volume is not
a vault.** Every process in the container runs as that one user, so a suite, a plugin and a judge
all reach all three. That is what the grant costs. It stops the machine's stores crossing in; it
does not stop the person at the keyboard.

### 4. Start the host that can work

```sh
FOUNDRY_KEYS=foundry-keys sh bin/host.sh --worker
```

It builds, then opens a shell inside. Measured 11 September 2026: 258 MB for the host, 1.56 GB once
both harnesses sit on it. The build is once, and a later container costs about fifteen seconds.

**`--worker` is what puts the harnesses in.** The plain host answers *not found* for both — it
carries `git`, `gh` and certificates, and it grades.

**With `FOUNDRY_KEYS` set, its first start also installs Foundry's plugins**, before the shell
opens. It exits 6 if that fails, and starts nothing. Step 6 says what it reads.

### 5. Sign in, inside, once

```sh
gh auth login
claude
codex login
```

Three tools, three stores, and the place named in step 3 keeps all three. **Every login is
interactive**, so this is the step no command replaces.

**Two of the three are login commands. `claude` is not.** It opens a session, and the sign-in
happens inside it.

| | |
|---|---|
| it asks on the way in | no sign-in is kept yet, so the first start walks you through it |
| it opens straight to a prompt | one is kept and it is not the account you want — type `/login` |
| either way | it prints a URL. **The container has no browser**, so open that on the machine you are sitting at, authorise, and paste the code back at the prompt |
| to leave | `/exit`, or Ctrl-D |

**Leaving the session is not leaving the host.** Step 4's shell is still there, and `codex login` is
the next line in it.

### 6. Put Foundry in the host

**A clone is not an install, and step 2 gave you a clone.** `/src` is read-only, and its
`.claude/settings.json` names kernel, signal and floor as enabled.

Measured 22 September 2026, in a fresh container:

| | |
|---|---|
| `/src/.claude/settings.json` | names `kernel@the-foundry`, `signal@the-foundry`, `floor@the-foundry` |
| `~/.claude/plugins/marketplaces` | holds `claude-plugins-official`, and nothing else |

So the checkout asks for three plugins from a marketplace this machine never registered.

**With `FOUNDRY_KEYS` set, the host installs them itself, at a worker's first start.** It reads
three things from the checkout it was started in: the marketplace in
`.claude-plugin/marketplace.json`, the source `.claude/settings.json` declares for it, and the
plugins that file enables. `FOUNDRY_PLUGINS` names the plugins instead. No name is written in the
code.

Measured 23 September 2026, on a fresh volume:

| | |
|---|---|
| the first start | added the marketplace and installed kernel, signal and floor, in 17 seconds |
| the second | installed nothing, in 10 |
| floor's `run.sh`, from the installed plugin | answered |

**A failed install starts nothing.** The host exits 6 and says which of four it was: no
marketplace, no source a container can reach, no plugin named, or the install itself.

**The source is the one the checkout declares, never its origin.** Added from the origin's URL,
the harness recorded `git` where the checkout says `github`, and `plugins.sh declared` below then
called a sound host faulty. A `path` source is this machine's own disk, which no container reaches.

**A worker can still rewrite what a later start carries.** The volume is writable by every process
in the container, and the host knows a marketplace and a plugin by name. It never re-adds a
marketplace that is there, and the harness refuses one whose source changed under the same name.

**Without `FOUNDRY_KEYS` nothing would keep an install, so the host makes none.** Run these in each
container instead. A project setting reaches a session started inside that project, so `cd /src`
first.

```sh
cd /src
claude plugin marketplace add attac-t/the-foundry
claude plugin install kernel@the-foundry
claude plugin install signal@the-foundry
claude plugin install floor@the-foundry
```

## The three are not all of Foundry

`/src` asks for three. [README.md](../../../../README.md) holds which of the rest need an install
of their own, and this page does not repeat the list.

**Floor's own code needs none of them.** Measured 22 September 2026: `run.sh charter derive` wrote
three clauses in a container carrying no plugins at all.

**What goes missing is the half a worker invokes.** `panel:craft-charter` and
`panel:decide-boundary` are skills, and a worker with no plugins reaches neither. So a charter
derives and nothing shapes it. **The deriving half works, which is what hides the other.**

Installing them is step 6's command with a different name after it, and **nobody has driven that
here either.**

## Prove it answers

A version is not a call. Leave the shell and make three calls, each from outside:

```sh
FOUNDRY_KEYS=foundry-keys sh bin/host.sh --worker sh -c 'gh api user --jq .login'
FOUNDRY_KEYS=foundry-keys sh bin/host.sh --worker claude -p 'reply with ok'
FOUNDRY_KEYS=foundry-keys sh bin/host.sh --worker sh -c 'cd /src && codex exec "reply with ok"'
```

| | |
|---|---|
| the forge | names the account the sign-in belongs to |
| the harness | replies |
| the judge | replies, and **only from a git repository** — it refuses any other directory, and says so |

**Each starts a fresh container.** So a reply proves the sign-in survived one, and not that a
shell was still warm.

**`ok` proves the harness and not Foundry.** It comes back the same on a host carrying no plugins
at all, which is what step 6 is for. One more call reads that half:

```sh
FOUNDRY_KEYS=foundry-keys sh bin/host.sh --worker sh -c 'cd /src && sh plugins/floor/lib/plugins.sh declared .'
```

Silent means the checkout and the host agree. Otherwise it names the marketplace nobody registered
and says an install from it finds nothing.

Then ask floor, which is what the host is for:

```sh
FOUNDRY_KEYS=foundry-keys sh bin/host.sh --worker sh -c 'cd /src/plugins/floor && sh bin/join.sh'
```

It ends `joined.`, or names the one thing the machine still owes. It writes nothing.

**Six things it can ask for, and they are not all the machine's to give:**

| It says | Exit | What it wants, and what answering costs |
|---|---|---|
| this host is missing: `git` `awk` | 1 | floor declares `sh`, `git` and `awk`, and needs all three. **The image carries them**, so this only fires outside a container |
| there is no repository here | 3 | you are not standing in one. `cd /src` — the clone from step 2, mounted read-only |
| this host has no git author | 1 | a git `user.name` and `user.email`. It prints two `--global` lines, and **`~/.gitconfig` is on the container's own layer** — step 3 keeps three directories and that is not one. So set it outside, on the clone, where it arrives at `/src` with the mount |
| `FOUNDRY_WHO` is not set | 1 | outside as well. `host.sh` sends it in from the machine's `git config user.email`, so empty there is empty inside. **It is a record, never a credential** — [`identity.md`](../../../../.claude/rules/identity.md) says so |
| `source  nothing answers` | 1 | a work source a run can ask. On a GitHub remote that is a `gh` that answers. **The image carries `gh`**, so here it is the sign-in, and `gh`'s own words follow the line. Or name the directory adapter, `lib/source-dir.sh`, in `FOUNDRY_SOURCE` |
| not joined. A run here would stop at… | 4 | the **repository's** declarations, not the machine's: `.foundry/gates`, `.foundry/practice`, `.foundry/judged`. No sign-in and no install ends this one. The first two are written by hand, and the refusal prints the command that declares a judge |

**One of those is unverified here.** `host.sh` also sends `GIT_AUTHOR_NAME` and `GIT_AUTHOR_EMAIL`
into the container, and join reads `git config`. Whether the second sees the first has not been
driven on this machine. **Setting the identity on the clone answers it either way.**

Everything else it prints is a report, and reports never stop it. They are the home, the authority,
the work source whenever one answers, what the repository declares, and the skills its rules name.

**`joined.` is not *installed*.** Join reports the plugins a rule names, and refuses on none of
them. So a host with all three missing ends `joined.` all the same. On a fresh keys store, join's
own line reads *cannot tell*, because there is no `~/.claude/settings.json` yet to read.

## When a step refuses

| Exit | What it means |
|---|---|
| 2 | Docker is not answering. **Two causes, and the refusal names one** — read the next section |
| 3 | the image would not build. Run the same `docker build` without `-q` and read it |
| 4 | the machine has no home for runs. Set `FOUNDRY_HOME`, or set `HOME` |
| 5 | the place `FOUNDRY_KEYS` names could not be prepared. **Two causes as well**, and `host.sh` says which |
| 6 | a worker could not be given Foundry. The checkout names no marketplace, no source a container can reach, or no plugin, or the install failed, and `host.sh` says which |

### Exit 2 is not always a stopped daemon

`host.sh` asks `docker info` and says *start it*. **That answer is right for one of the two
faults.** Run the command yourself and read which you have:

```sh
docker info
```

| What it says | What it is | What to do |
|---|---|---|
| cannot connect to the Docker daemon | it is not running | start it — `sudo systemctl start docker`, or open Docker Desktop |
| permission denied on `/var/run/docker.sock` | it is running, and this user cannot reach it | the user is not in the `docker` group: `sudo usermod -aG docker "$USER"` |

**On a fresh machine the second is the common one**, and it is the one *start it* sends the wrong
way. Docker is already up.

**A new shell does not pick the group up.** Membership is read at login, so log out and back in.
`newgrp docker` covers the shell you are standing in and nothing else.

### Exit 5 is whichever shape step 3 chose

The value picks the mechanism, so it picks the failure too. **`host.sh` prints one line of the two,
and both hide the output of the command that failed.** Run that command yourself.

| The line | The cause | Run this |
|---|---|---|
| the directory named by `FOUNDRY_KEYS` could not be made | a value holding a slash. `mkdir -p` was refused under it — a parent you cannot write, a parent that is not there, or a read-only path | `mkdir -p "$FOUNDRY_KEYS/gh"` and read the error. Then name a path you own, under your home |
| the volume named by `FOUNDRY_KEYS` could not be prepared | a bare word. Either Docker would not make the volume, or the one-off root container that gives the three directories to `forge` did not run | `docker volume create "$FOUNDRY_KEYS"`, and read the error |

**A volume is prepared by a container**, run as root to hand the three directories to `forge`. So
this exit can mean Docker answered step 1 and refused a container, and the error is Docker's to
give.

**`FOUNDRY_KEYS` has no third shape.** A word with no slash is a Docker volume whatever you meant.
So a relative path is a directory, and `keys` is a volume named `keys`.

## Where to disagree

Three of the choices above belong to the machine, not to Foundry.

| | |
|---|---|
| the harnesses | drop `--worker` where a machine only grades. It is 1.3 GB lighter and cannot do the work |
| where sign-ins are kept | `FOUNDRY_KEYS=/srv/foundry-keys` puts them in a directory instead, readable with Docker stopped |
| where runs land | `FOUNDRY_HOME`, else `$HOME/.foundry`. `--volume` puts them in Docker instead, and then only Docker reaches them |

**Nothing here is baked into the image.** The identity, the home and the sign-ins are the machine's,
and they arrive when a container starts.
