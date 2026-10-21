---
name: ddev-legacy-php
description: Run end-of-life PHP (5.6-8.0) in DDEV v1.24+, where those versions are no longer in the web image. Use for "php7.4 not found in ddev", "legacy PHP in DDEV", "old PHP version for a legacy site", `ddev exec php7.4 -v` failing, or install_php_extensions.sh errors on Apple Silicon.
---

# DDEV Legacy PHP Setup

DDEV v1.24.0+ no longer ships PHP 5.6, 7.0, 7.1, 7.2, 7.3, 7.4, or 8.0 in the web image ([ddev/ddev#6835](https://github.com/ddev/ddev/issues/6835)). DDEV installs them at image-build time with `install_php_extensions.sh`.

## Case 1: the project runs the legacy version

Set the version and restart. DDEV injects the install step into the web build itself, so no Dockerfile is needed:

```bash
ddev config --php-version=7.4
ddev restart
ddev exec php -v
```

The first build takes several minutes.

## Case 2: legacy version alongside a newer default

To keep, say, PHP 8.3 as the default and also run 7.4 for specific scripts, create `.ddev/web-build/pre.Dockerfile.php7.4`:

```dockerfile
RUN /usr/local/bin/install_php_extensions.sh "php7.4" "${TARGETARCH}"
```

Replace `php7.4` with the version needed (e.g. `php7.2`, `php5.6`). After `ddev restart`, run it with `ddev exec php7.4 -v`.

## Fallback: force amd64 on Apple Silicon

If the native ARM64 build fails for a specific version, run the web container under x86_64 emulation. Create `.ddev/docker-compose.amd64.yaml`:

```yaml
services:
  web:
    platform: linux/amd64
```

Then `ddev restart` (the first build pulls amd64 images and is slow). Emulation makes PHP execution slower; the database and router stay native. Remove the file as soon as the native build works or the project moves to a supported PHP.

## When to remove

When the project upgrades to a supported PHP version:

1. Delete `.ddev/docker-compose.amd64.yaml` and any `pre.Dockerfile.phpX.Y` added above.
2. Update `php_version` in `.ddev/config.yaml` (or run `ddev config --php-version=<new>`).
3. Run `ddev restart`.

## Reference

- [DDEV Docs: Adding EOL Versions of PHP](https://docs.ddev.com/en/stable/users/extend/customizing-images/#adding-eol-versions-of-php)
- [DDEV Blog: AMD64 with Rosetta on macOS](https://ddev.com/blog/amd64-with-rosetta-on-macos/)
