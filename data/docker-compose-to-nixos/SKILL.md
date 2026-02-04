---
name: docker-compose-to-nixos
description: Converts Docker Compose configurations to NixOS modules using the dendritic pattern with Arion. Creates modules with system users, sops secrets, Arion docker-compose config, and Tailscale integration. Use when converting docker-compose.yaml files to NixOS modules or creating new Arion-based services.
---

# Docker Compose to NixOS Module

This skill converts Docker Compose configurations to NixOS modules following the dendritic pattern used in this repository.

## Dendritic Pattern Overview

The dendritic pattern organizes modules by **aspect** (functionality) rather than **class** (nixos/home/shared):
- File: `modules/services/service-name.nix` (NOT `modules/nixos/services/service-name.nix`)
- Contains both nixosModules and homeModules in the same file
- Flake inputs defined in module files, materialized with `nix run '.#write-flake'`
- Every module MUST have a unique `key` attribute for deduplication

## Conversion Workflow

Follow this checklist when converting a docker-compose.yaml:

- [ ] **1. Analyze docker-compose.yaml**: Identify services, volumes, networks, secrets
- [ ] **2. Determine UID/GID allocation**: Add to `inventory/users-groups.nix` if system user needed
- [ ] **3. Create module skeleton**: Use template in this document
- [ ] **4. Add system user/group**: Reference inventory values with flakeConfig
- [ ] **5. Configure sops secrets**: Use hierarchical naming (e.g., `service/secret-name`)
- [ ] **6. Create sops template**: Environment file with placeholders
- [ ] **7. Set up directories**: systemd tmpfiles.rules
- [ ] **8. Convert services**: Map docker-compose to Arion configuration
- [ ] **9. Add Tailscale serve** (optional): For external access
- [ ] **10. Stage with git add**: Flakes only see committed/staged files
- [ ] **11. Validate**: Run `just nixOpts= eval-nixos` in a loop until fixed
- [ ] **12. Add secrets**: Use `sops set` commands to populate secret values
- [ ] **13. Run comprehensive validation**: `just eval-all`
- [ ] **14. Format**: `just lint` (may reformat, amend if needed)
- [ ] **15. Commit changes**: Follow git workflow in CLAUDE.md

## Module Template

```nix
{
  inputs,
  self,
  config,
  ...
}:
let
  flakeConfig = config;
in
{
  flake.nixosModules.service-name =
    { config, lib, ... }:
    let
      inherit (lib) mkDefault;
    in
    {
      key = "nixos-config.modules.nixos.service-name";

      # Explicit imports for all dependencies
      imports = [
        inputs.sops-nix.nixosModules.sops
        inputs.arion.nixosModules.arion
        self.nixosModules.tailscale
        self.nixosModules.inventory
      ];

      config = {
        # User/group creation
        users.groups.service-name = {
          gid = flakeConfig.inventory.usersGroups.systemUsers.service-name.gid;
        };

        users.users.service-name = {
          isSystemUser = true;
          group = "service-name";
          uid = flakeConfig.inventory.usersGroups.systemUsers.service-name.uid;
        };

        # Sops secrets
        sops.secrets."service-name/secret1" = { };
        sops.secrets."service-name/secret2" = { };

        # Sops template for environment variables
        sops.templates."service-name-env".content = ''
          SECRET1=${config.sops.placeholder."service-name/secret1"}
          SECRET2=${config.sops.placeholder."service-name/secret2"}
          PUID=${toString flakeConfig.inventory.usersGroups.systemUsers.service-name.uid}
          PGID=${toString flakeConfig.inventory.usersGroups.systemUsers.service-name.gid}
        '';

        # Directory structure
        systemd.tmpfiles.rules = [
          "d /mnt/service-name 0755 service-name service-name -"
          "d /mnt/service-name/data 0755 service-name service-name -"
        ];

        # Arion docker-compose configuration
        virtualisation.arion.backend = "docker";
        virtualisation.arion.projects.service-name = {
          serviceName = "service-name-docker-compose";
          settings = {
            services = {
              main-service = {
                service = {
                  image = "namespace/image:pinned-version"; # NEVER use :latest
                  container_name = "service-name";
                  restart = "unless-stopped";
                  ports = [ "3000:3000" ];
                  volumes = [
                    "/mnt/service-name/data:/data"
                  ];
                  env_file = [
                    config.sops.templates.service-name-env.path
                  ];
                };
              };
            };
          };
        };

        # Tailscale serve (optional)
        services.tailscale.serve = {
          enable = mkDefault true;
          services.service-name = {
            serviceName = "service-name";
            protocol = "https";
            target = "localhost:3000";
          };
        };
      };
    };
}
```

## Key Patterns

### 1. System User Management

**Add to `inventory/users-groups.nix`:**
```nix
{
  systemUsers = {
    existing-service = { uid = 2001; gid = 2001; };
    new-service = { uid = 2002; gid = 2002; }; # Next sequential
  };
}
```

**Reference in module with flakeConfig:**
```nix
{ inputs, self, config, ... }:
let
  flakeConfig = config;  # CRITICAL: Access flake-level data
in
{
  flake.nixosModules.service-name = { config, lib, ... }: {
    config = {
      users.groups.service-name = {
        gid = flakeConfig.inventory.usersGroups.systemUsers.service-name.gid;
      };
      users.users.service-name = {
        isSystemUser = true;
        group = "service-name";
        uid = flakeConfig.inventory.usersGroups.systemUsers.service-name.uid;
      };
    };
  };
}
```

**Why flakeConfig?** The outer `config` parameter is at the flake level (same level as `self`, `inputs`). The inner `config` parameter inside `flake.nixosModules.service-name` is at the NixOS module level. Use `flakeConfig` to access flake-level inventory data, matching the pattern in `modules/lxc.nix` and `modules/inventory.nix`.

### 2. Sops Secrets Management

**Hierarchical naming with `/`:**
```nix
sops.secrets."service-name/nextauth-secret" = { };
sops.secrets."service-name/database-password" = { };
sops.secrets."service-name/api-key" = { };
```

**Create template for environment file:**
```nix
sops.templates."service-name-env".content = ''
  NEXTAUTH_SECRET=${config.sops.placeholder."service-name/nextauth-secret"}
  DATABASE_URL="postgresql://user:${config.sops.placeholder."service-name/database-password"}@host/db"
  API_KEY=${config.sops.placeholder."service-name/api-key"}
  PUID=${toString flakeConfig.inventory.usersGroups.systemUsers.service-name.uid}
  PGID=${toString flakeConfig.inventory.usersGroups.systemUsers.service-name.gid}
'';
```

**IMPORTANT: SOPS YAML Structure**

Secrets with `/` in Nix (like `service-name/secret`) MUST be structured as nested YAML:

```yaml
# CORRECT - nested structure
service-name:
  nextauth-secret: value
  database-password: value
  api-key: value

# WRONG - flat structure (will cause build errors)
service-name/nextauth-secret: value
service-name/database-password: value
```

**Add actual secrets with sops set (using nested path):**
```bash
sops set secrets/docker-on-nixos/secrets.yaml '["service-name"]["nextauth-secret"]' "$(echo '"'$(apg -x16 -m16 -MLCN -n1)'"')"
sops set secrets/docker-on-nixos/secrets.yaml '["service-name"]["database-password"]' "$(echo '"'$(apg -x16 -m16 -MLCN -n1)'"')"
sops set secrets/docker-on-nixos/secrets.yaml '["service-name"]["api-key"]' '""'  # Empty for manual population
```

### 3. Directory Structure

**Mount strategy:**
- `/mnt/service-name/data` - Application data (persistent)
- `/mnt/service-name/var/component` - Per-component state

**Example:**
```nix
systemd.tmpfiles.rules = [
  "d /mnt/service-name 0755 service-name service-name -"
  "d /mnt/service-name/data 0755 service-name service-name -"
  "d /mnt/service-name/var 0755 service-name service-name -"
  "d /mnt/service-name/var/database 0755 service-name service-name -"
  "d /mnt/service-name/var/cache 0755 service-name service-name -"
];
```

### 4. Docker Compose Service Translation

**Docker Compose:**
```yaml
services:
  app:
    image: namespace/app:1.2.3
    container_name: myapp
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
    environment:
      SECRET: ${SECRET}
    depends_on:
      - database
```

**Arion Configuration:**
```nix
services = {
  app = {
    service = {
      image = "namespace/app:1.2.3";  # ALWAYS pin version
      container_name = "myapp";
      restart = "unless-stopped";
      ports = [ "3000:3000" ];
      volumes = [
        "/mnt/service-name/data:/app/data"
      ];
      env_file = [
        config.sops.templates.service-name-env.path
      ];
      depends_on = [ "database" ];
    };
  };
};
```

**Key differences:**
- `ports: ["3000:3000"]` - Array of strings
- `volumes: ["/host:/container"]` - Absolute host paths, array format
- `env_file: [path]` - Reference sops template path
- `depends_on: ["service"]` - Array of service names
- `expose: ["7700"]` - For internal-only ports
- **NEVER use `:latest`** - Always pin to specific version

### 5. Tailscale Serve Integration

**Basic pattern:**
```nix
services.tailscale.serve = {
  enable = mkDefault true;
  services.service-name = {
    serviceName = "service-name";  # Will be svc:service-name
    protocol = "https";
    target = "localhost:3000";
  };
};
```

This exposes the service at `https://svc:service-name` on the Tailscale network.

## Image Version Pinning

**CRITICAL:** Never use `:latest` tag. Always pin to specific versions:

- ✅ `ghcr.io/karakeep-app/karakeep:0.29.1`
- ✅ `getmeili/meilisearch:v1.13.3`
- ✅ `gcr.io/zenika-hub/alpine-chrome:124`
- ❌ `archivebox/archivebox:latest`
- ❌ `postgres:latest`

Find current versions:
- Check project's GitHub releases
- Check Docker Hub/GHCR tags
- Use `docker pull image:latest && docker inspect image:latest` to find current digest

## Validation Workflow

**Iterative validation:**
```bash
# Fast iteration on current machine
just nixOpts= eval-nixos

# Fix errors, repeat until clean

# Comprehensive validation (all 12 configs, ~45s)
just eval-all

# Format and fix any linting issues
just lint

# If lint changed files, amend commit
git add . && git commit --amend --no-edit
```

## Common Patterns

### Multiple Services in One Project

```nix
virtualisation.arion.projects.service-name = {
  serviceName = "service-name-docker-compose";
  settings = {
    services = {
      # Main app
      app = {
        service = {
          image = "namespace/app:1.0.0";
          depends_on = [ "database" "cache" ];
          # ...
        };
      };

      # Database
      database = {
        service = {
          image = "postgres:16.1";
          expose = [ "5432" ];  # Internal only
          volumes = [
            "/mnt/service-name/var/database:/var/lib/postgresql/data"
          ];
          environment = {
            POSTGRES_PASSWORD = config.sops.placeholder."service-name/db-password";
          };
        };
      };

      # Cache
      cache = {
        service = {
          image = "redis:7.2.3";
          expose = [ "6379" ];
        };
      };
    };
  };
};
```

### Environment Variables vs env_file

**Use env_file for secrets:**
```nix
env_file = [
  config.sops.templates.service-name-env.path
];
```

**Use environment for non-sensitive config:**
```nix
environment = {
  NODE_ENV = "production";
  PORT = "3000";
  MEILI_NO_ANALYTICS = "true";
};
```

### Container Commands

```nix
service = {
  image = "namespace/app:1.0.0";
  command = [
    "schedule"
    "--foreground"
    "--update"
    "--every=day"
  ];
};
```

## Git Workflow

**Critical for flakes:**
1. Stage new files immediately: `git add modules/services/service-name.nix inventory/users-groups.nix`
   - Flakes only see committed or staged files
2. Validate before committing
3. Check for existing unpushed commits - consider using `--fixup` if related
4. Follow commit message format in CLAUDE.md

## Troubleshooting

**"flake is dirty" warning**: Normal during development, flake sees uncommitted changes

**Evaluation fails with "attribute missing"**:
- Check if module is imported in machine configuration
- Verify inventory.usersGroups exists if using it
- Ensure all imports (sops-nix, arion) are available

**UID/GID conflicts**: Check `inventory/users-groups.nix` for next available ID

**Secrets not decrypted**: Ensure sops secrets file exists and is properly encrypted for the target machine's key

## Examples and References

- **Detailed examples**: See [EXAMPLES.md](EXAMPLES.md) for complete archivebox and karakeep conversions
- **Technical reference**: See [REFERENCE.md](REFERENCE.md) for docker-compose to Arion mapping tables and advanced patterns

## Quick Reference

**File locations:**
- Module: `modules/services/service-name.nix`
- UID/GID: `inventory/users-groups.nix`
- Secrets: `secrets/docker-on-nixos/secrets.yaml`

**Validation commands:**
- Fast: `just nixOpts= eval-nixos`
- Comprehensive: `just eval-all`
- Lint: `just lint`

**Secrets commands (use nested path for hierarchical structure):**
```bash
sops set secrets/docker-on-nixos/secrets.yaml '["service"]["secret"]' "$(echo '"'$(apg -x16 -m16 -MLCN -n1)'"')"
```

**Module structure:**
1. Outer: `{ inputs, self, config, ... }:` with `let flakeConfig = config; in`
2. Module: `flake.nixosModules.name = { config, lib, ... }:`
3. Key: `key = "nixos-config.modules.nixos.name";`
4. Imports: All dependencies explicitly listed
5. Config: User, secrets, dirs, arion, tailscale
