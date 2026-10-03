---
name: docker-ssh-clone
description: Clone a GitHub repo (via SSH) into a Docker container using the host's SSH key.
---

# Docker Container SSH Git Clone

Clone a GitHub repo (via SSH) into a Docker container using the host's SSH key.

## Steps

1. **Create container** (if not exists):
   ```bash
   docker run -d --name <name> -v ~/MountDir:/data --restart unless-stopped ubuntu:24.04 sleep 86400
   ```

2. **Install git and openssh inside the container**:
   ```bash
   docker exec <name> apt-get update && docker exec <name> apt-get install -y git openssh-client
   ```

3. **Copy SSH key from host to container**:
   ```bash
   docker exec <name> mkdir -p /root/.ssh
   docker cp ~/.ssh/id_ed25519 <name>:/root/.ssh/id_ed25519
   docker cp ~/.ssh/id_ed25519.pub <name>:/root/.ssh/id_ed25519.pub
   ```

4. **Set permissions and SSH config, then clone**:
   ```bash
   docker exec <name> sh -c "
     chmod 700 /root/.ssh && chmod 600 /root/.ssh/id_ed25519 && chmod 644 /root/.ssh/id_ed25519.pub &&
     echo 'Host github.com
       HostName github.com
       User git
       IdentityFile /root/.ssh/id_ed25519
       StrictHostKeyChecking no' > /root/.ssh/config &&
     git clone git@github.com:<owner>/<repo>.git /data/<repo>
   "
   ```

## Pitfalls

- **HTTPS with token fails** inside container — `docker exec` has no interactive credential helper. Use SSH instead.
- **SSH key permissions** must be correct (700 for `.ssh`, 600 for private key, 644 for public key).
- **`StrictHostKeyChecking no`** is needed to avoid interactive prompt on first connect.
- **`docker cp` fails** if target directory doesn't exist — create it first with `docker exec`.
- If the container already has `/root/.ssh`, skip the `mkdir` step.
