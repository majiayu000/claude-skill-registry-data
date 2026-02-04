---
name: lord
description: provides expert guidance on lord, a minimalist paas cli tool for deploying docker containers via ssh. use when user mentions lord deployment, docker container deployment, traefik configuration, remote hosting, or paas management and has a lord.yml file in their repo directory.
---

# Lord - Minimalist PaaS Management

expert knowledge of lord, an ultra-minimalist paas management cli tool for deploying docker containers to remote servers via ssh.
- lord allows a user to deploy and manage several standalone containers to a remote server.
- each container can expose a web service which is auto setup with https certs via traefik.
- when deploying via lord, a "direct push" model or a container registry model is supported for getting the container onto the remote server.
- lord also exposes cli commands for detroying the container, checking status, viewing logs, and system monitoring (see cli reference below).
- lord requires a few things in order to function, which are described in the "prerequisites" section.

the user may ask you to perform some lord actions via the cli tool, troubleshoot usage of lord, or verify/modify the lord configuration for a given repo.

## prerequisites

- the `lord` binary must be installed on the system. this can be done via github release download or `make install` from the repo (requires go to be installed)
- docker must be installed and running on the local machine (lord will auto install it on the remote server)
- A `Dockerfile` must be present in the base repository and follow the conventions described in "container conventions" below
- A `lord.yml` file must be present in the base repository (or a `*.lord.yml` invoked via `-config` flag) to tell lord what to do. this file may be created via the `-init` flag
- the local machine must have ssh access to the remote server specified in the lord config (the ssh keyfile can be specified in the lord config, otherwise the default for the system is used)

## cli reference

```sh
lord -init         # create lord.yml configuration file (populated with dummy values)
lord -deploy       # build and deploy application
lord -logs         # stream container logs from server
lord -destroy      # remove deployed containers
lord -status       # check deployment status (basically remote docker ps)
lord -server       # run/check server setup (includes reverse proxy)
lord -proxy        # run/check reverse proxy setup only
lord -recover      # recover server with bad lord dependency install
lord -logdownload  # download full log file from server
lord -registry     # setup and authenticate to container registry on the server
lord -dozzle       # run dozzle ui locally connected to remote server via ssh (great for searching/inspecting logs and all containers on the server)
lord -monitor      # check system load of the host

lord -config {config variant} {any command from above} # run lord with the specific config variant (config variant}.lord.yml when using multiple configs
```

## configuration reference

projects require a `lord.yml` file:

```yaml
# required
name: myapp
server: 192.168.1.100

# optional registry (omit for registry-less deployment)
registry: my.realregistry.com/me
authfile: ./config.json

# optional settings
email: user@example.com
platform: linux/amd64
target: production
web: true
hostname: myapp.example.com
environmentfile: .env
buildargfile: build.args
hostenvironmentfile: host.env
user: ubuntu
sshkeyfile: /path/to/private/key

volumes:
  - /host/data:/container/data

# advanced web configuration
webadvancedconfig:
  # timeout settings (global traefik - affects all web apps!)
  readtimeout: 300        # seconds, 0 = unlimited
  writetimeout: 300       # seconds, 0 = unlimited
  idletimeout: 180        # seconds

  # buffering settings (per-service, safe)
  maxrequestbodybytes: 10485760
  maxresponsebodybytes: 10485760
  memrequestbodybytes: 1048576
```

## container conventions

- web services must expose port **80** internally
- persistent data should use **/data** volume mount
- additional volumes can be specified in config

### multi-config support

use `config.lord.yml` naming and `-config config` flag for multiple deployment targets in one repo.
this can be used when you need different configs for staging, prod, etc. or if there are separate services built from the same binary/container, which can have different `build args`.

```
project/
├── Dockerfile
├── prod.lord.yml
└── staging.lord.yml
```

deploy with: `lord -config prod -deploy`

## deployment flow

1. build docker container locally with specified platform
2. push to registry OR save/transfer directly (registry-less)
3. ssh to target server and ensure docker/traefik setup
4. if webadvancedconfig timeouts set and traefik running:
   - read existing traefik config from /etc/traefik/traefik.yml
   - apply "maximum wins" logic: update timeouts only if new values are higher
   - restart traefik container if config updated
5. pull container and run with configured volumes/settings
6. for web containers, configure traefik routing with optional buffering middleware

## registry authentication

three methods supported:

### method 1: username/password file (simplest)
plain text file with `username:password`

```yaml
registry: my.realregistry.com/me
authfile: ./registry-auth.txt
```

### method 2: docker config file
json config copied to remote host's `.docker/config.json` (overwrites entire file)

### method 3: dynamic authentication
automatic authentication for:
- **aws ecr**: requires AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
- **digitalocean**: requires DIGITALOCEAN_ACCESS_TOKEN

set via `hostenvironmentfile` in lord.yml

## advanced web configuration

### timeout settings (use with caution!)

affects **global traefik reverse proxy** serving all web containers on host:
- values in seconds
- 0 = unlimited
- "maximum wins" strategy across all deployments
- use for docker registries, large file uploads, long-polling apis

### buffering settings (per-service, safe)

affects only the specific service:
- maxrequestbodybytes: max incoming request body size
- maxresponsebodybytes: max outgoing response body size
- memrequestbodybytes: threshold before buffering to disk

## environment variables

- **hostenvironmentfile**: env vars on remote host during deployment (for registry auth, cloud credentials)
- **environmentfile**: env vars inside container at runtime

## supported linux distributions

automatic docker installation on:
- ubuntu (apt)
- debian (apt)
- amazon linux 2023 (dnf)
- centos (yum)
- rhel (yum)

## key design principles

- **minimalism**: minimal config options and dependencies
- **simplicity**: all you need is docker and ssh
- **flexibility**: deploy from pc or ci/cd to any linux server
- **single responsibility**: one container per deployment, not orchestration
- **automatic reverse proxy**: traefik handles https certificates and routing
- **registry optional**: can deploy without a container registry
