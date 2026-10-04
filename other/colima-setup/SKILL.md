---
name: colima-setup
description: This skill should be used when the user asks to "set up Colima", "replace Docker Desktop", "install Colima", "configure Testcontainers with Colima", or needs a free Docker Desktop alternative on macOS.
---

# Colima Setup — Docker Desktop replacement on macOS

## Purpose

Replace Docker Desktop with Colima (free, open source) on macOS Apple Silicon,
configured for Java Testcontainers with Ryuk support.

## Prerequisites

- macOS Apple Silicon (aarch64)
- Homebrew installed
- `docker` CLI already present (or install via `brew install docker`)
- Dotfiles at `~/Progetti/dotfiles`, managed with GNU Stow

## Installation

```bash
brew install colima
```

## First start (saves profile)

```bash
colima start --cpus 4 --memory 8 --disk 100 --network-address
```

`--network-address` assigns a static IP to the VM — required for Testcontainers Ryuk
to reach the VM from the host. Without it, Ryuk fails at test startup.

## Enable autostart at login

```bash
brew services start colima
```

## Configure env vars for Testcontainers

Add to `~/Progetti/dotfiles/zsh/exports.zsh`:

```bash
# Colima — Testcontainers config
# /var/run/docker.sock is symlinked to the colima XDG socket at boot via launchd.
# DOCKER_HOST is intentionally unset — the active docker context (colima) handles routing.
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
# Pin the Docker API version: the docker-java client used by Testcontainers
# defaults to an old API (1.32) that Colima's Docker engine rejects ("too old").
export DOCKER_API_VERSION=1.41
```

Do NOT set `DOCKER_HOST` — it overrides the active docker context and causes routing issues.

Then reload: `source ~/.zshrc`

## ~/.testcontainers.properties

Verify (or create) `~/.testcontainers.properties` contains:

```properties
docker.client.strategy=org.testcontainers.dockerclient.UnixSocketClientProviderStrategy
```

No need for `ryuk.disabled=true` — Ryuk works with Colima when
`--network-address` is used and `TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE` is set.

## Verify setup

```bash
colima list                        # should show: Running, aarch64, address assigned
docker run --rm hello-world        # should print "Hello from Docker!"
docker context list                # colima should be active (*)
```

## Notes

- Socket path: `~/.config/colima/default/docker.sock` (not `/var/run/docker.sock`)
- Colima creates a Docker context named `colima` automatically on first start
- `~/.config/zsh/exports.zsh` may be a hardlink (not symlink) to dotfiles source —
  edits propagate automatically to `~/Progetti/dotfiles/zsh/exports.zsh`
- Idle memory on host: ~74 MB (limactl processes); VM allocates lazily via
  Apple Virtualization Framework — does not physically reserve 8 GB upfront
- Docker Desktop can coexist during transition; switch context with
  `docker context use colima` / `docker context use desktop-linux`

## Uninstall Docker Desktop (after validation)

```bash
brew uninstall --cask docker
```

## Cleanup dopo rimozione manuale di Docker Desktop

Se Docker Desktop era già stato rimosso manualmente (senza `brew uninstall --cask docker`),
possono restare symlink rotti in `/usr/local/bin`:

```bash
ls -la /usr/local/bin/docker* 2>/dev/null
# se puntano ad /Applications/Docker.app (non esistente) → rimuoverli
sudo rm /usr/local/bin/docker /usr/local/bin/docker-compose
sudo rm /usr/local/bin/docker-credential-desktop /usr/local/bin/docker-credential-osxkeychain
# ignora "no such file or directory" per quelli già mancanti
```

Poi installa il docker CLI standalone:

```bash
brew install docker
```

## Fix: Colima XDG config (`~/.colima` → `~/.config/colima`)

Colima crea `~/.colima` per default e legge `XDG_CONFIG_HOME` solo se quella directory non
esiste già. `brew services` rigenera il LaunchAgent plist dalla formula ad ogni
start/restart/upgrade, **senza mai includere `XDG_CONFIG_HOME`** — quindi una migrazione
one-shot (`mv ~/.colima ~/.config/colima`) o un patch del plist regrediscono al riavvio
successivo (successo apparente, poi si ripresenta lo stesso problema).

**Fix permanente:** rendere `~/.colima` uno **symlink** verso `~/.config/colima`, invece di
spostare la directory. Colima risolve sempre `~/.colima` per primo, quindi finisce sulla
directory XDG indipendentemente da come/quando il servizio viene avviato — nessuna
dipendenza da env var che brew possa cancellare.

**Ansible lo gestisce automaticamente** (task `Symlink ~/.colima to ~/.config/colima` in
`roles/macos/tasks/main.yml`, idempotente — riapplicato ad ogni run).

Per applicare manualmente (senza Ansible):

```bash
colima stop
rm -rf ~/.colima          # o: mv ~/.colima ~/.config/colima se contiene ancora dati reali
ln -sfn ~/.config/colima ~/.colima
colima start
```

Il warning `found ~/.colima, ignoring $XDG_CONFIG_HOME` continua a comparire anche con lo
symlink (colima non distingue directory reale da symlink) — è cosmetic, ignoralo: `colima
status` mostra comunque `docker socket: unix:///Users/.../.colima/default/docker.sock`, che
risolve a `~/.config/colima/default/docker.sock`.

## Fix: `/var/run/docker.sock` mancante o punta a Docker Desktop

Dopo la rimozione di Docker Desktop, `/var/run/docker.sock` può mancare o puntare a
`~/.docker/run/docker.sock` (non più esistente). Testcontainers fallisce con
`Could not find a valid Docker environment`.

**Ansible lo gestisce automaticamente** via LaunchDaemon (`com.lucatrifilio.colima-docker-sock`)
installato in `/Library/LaunchDaemons/`. Il daemon ricrea il symlink al boot:

```
/var/run/docker.sock → ~/.config/colima/default/docker.sock
```

Per applicare manualmente senza Ansible:

```bash
sudo ln -sf "$HOME/.config/colima/default/docker.sock" /var/run/docker.sock
```

**Nota:** il fix manuale non persiste ai reboot — usare il LaunchDaemon via Ansible.

## Fix: `default` docker context punta a path inesistente

Il context `default` è built-in e non può essere rimosso né aggiornato. Se mostra un
path sbagliato (es. `~/.colima/default/docker.sock`), ignorarlo — è cosmetic.
Verificare che il context `colima` sia attivo (`*`) con `docker context list`.

Se `DOCKER_HOST` è impostato nel shell, sovrascrive il context attivo e fa comparire
`default *` anche se il context colima è selezionato. Soluzione: non impostare `DOCKER_HOST`.
