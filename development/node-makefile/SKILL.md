---
name: node-makefile
description: The Makefile for a Node Web Only project - vendoring pinned frontend assets into public/, compiling a native addon from source, verifying it loads, and the semver version calculation. Use when creating or changing the Makefile, adding a vendored asset, or wiring the native addon build. Triggers on make vendor, make verify, make setup, npm ci, npm_config_build_from_source, node-gyp, fnm, uv tool run, and fonttools woff2 compression.
user-invocable: false
---

# Node Makefile

**Vendor the frontend, compile any native addon from source, prove it loads, then hand off to the release step.**

The native-addon targets exist only when the project has one. A pure-JS app drops `verify` and the `npm_config_build_from_source` prefix and uses a plain `npm ci`.

## Assets Are Never Committed

`make vendor` produces everything under `public/fonts/`, `public/css/`, and `public/vendor/`, and the release workflow calls that same target rather than reimplementing the copies. Those directories are listed in `.gitignore`, so the tree in git holds only what a person wrote.

Every version is pinned to an exact release. A floating range makes two builds of one commit differ, and moving a pin is an edit to this file, which is the intended maintenance cost.

A stamp file guards the whole target and depends on the Makefile and the lockfile. `make bundle` on an unchanged checkout then vendors nothing, and a moved pin re-vendors everything.

`.gitignore` needs its own entry for `public/.vendor-stamp`, which sits beside the vendored directories rather than inside one.

## Fonts

Three families are downloaded by default and all three come from Google Fonts as woff2. Nothing is converted, since the css2 endpoint already serves woff2 to a browser-shaped User-Agent.

| Family | Role |
|---|---|
| Inter | body and UI text |
| Google Sans | display headings and branding |
| JetBrains Mono | code and monospace |

Only the `latin` and `latin-ext` blocks of each stylesheet are kept. Google Fonts declares every subset it has, which for Google Sans is twenty-five files covering scripts the page never renders, and the release bundle carries all of them. Filtering leaves six woff2 files across the three families.

The Nerd Font variant is off by default. It exists only for a page that renders Nerd Font glyphs, and it costs two megabytes and roughly ten seconds of woff2 compression against sixty kilobytes and half a second for the plain family. Set `NERDFONT := 1` in the Makefile when a page needs the glyphs; the target then fills the same `css/jetbrains-mono.css` under the same `JetBrains Mono` family name, so no page changes either way.

## Toolchain

`fnm` pins Node to `.node-version`, so `make` is run from a shell where it has activated.

`uv` supplies both the Python `node-gyp` needs and the `fonttools` used for woff2 compression, neither of which is installed globally or into the system interpreter.

## Template

```makefile
.PHONY: help setup vendor font nerdfont verify clean bundle binary version

# =============================================================================
# Variables
# =============================================================================
APP_NAME     := [APP_NAME]
VERSION      ?= dev-build
NODE_VERSION := 24.20.0

PUBLIC_DIR := public
VENDOR_DIR := $(PUBLIC_DIR)/vendor
CSS_DIR    := $(PUBLIC_DIR)/css
FONTS_DIR  := $(PUBLIC_DIR)/fonts
STAMP      := $(PUBLIC_DIR)/.vendor-stamp

NERDFONT_VERSION := 3.5.1

# Only a page that renders Nerd Font glyphs needs 1 here.
NERDFONT := 0

MONO := $(if $(filter 1,$(NERDFONT)),nerdfont,font FAMILY="JetBrains+Mono" SLUG=jetbrains-mono WEIGHTS="400;700")

# Google Fonts serves woff2 only to a browser-shaped User-Agent; an unrecognized
# one gets ttf, which is roughly twice the bytes.
UA := Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
# `uv tool run` is the always-present equivalent of uvx.
UVX := uv tool run

CYAN  := \033[0;36m
GREEN := \033[0;32m
NC    := \033[0m

# =============================================================================
# Help
# =============================================================================
help: ## Show this help
	@echo "$(CYAN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

# =============================================================================
# Setup and the native addon
# =============================================================================
setup: node_modules vendor verify ## Install deps, vendor assets, verify the addon

# Compiling the addon from source is required on Linux, where no prebuilt exists,
# and avoids the broken prebuilt spawn-helper on macOS. PYTHON points node-gyp at
# uv's managed interpreter so nothing depends on a system Python.
node_modules: package-lock.json
	@uv python install
	npm_config_build_from_source=true PYTHON="$$(uv python find)" npm ci
	@touch node_modules

# =============================================================================
# Vendor the frontend
# =============================================================================
vendor: $(STAMP) ## Copy JS deps and download fonts into public/
	@:

# Every pin lives in this file or the lockfile, so moving one invalidates the stamp.
$(STAMP): Makefile package-lock.json | node_modules
	@mkdir -p $(VENDOR_DIR) $(CSS_DIR) $(FONTS_DIR)
	@cp node_modules/@tailwindcss/browser/dist/index.global.js $(VENDOR_DIR)/tailwind.js
	@cp node_modules/lucide/dist/umd/lucide.min.js $(VENDOR_DIR)/lucide.min.js
	@cp node_modules/@xterm/xterm/lib/xterm.js $(VENDOR_DIR)/xterm.js
	@cp node_modules/@xterm/xterm/css/xterm.css $(VENDOR_DIR)/xterm.css
	@$(MAKE) --no-print-directory font FAMILY="Inter" SLUG=inter WEIGHTS="400;500;600;700"
	@$(MAKE) --no-print-directory font FAMILY="Google+Sans" SLUG=google-sans WEIGHTS="400;500;700"
	@$(MAKE) --no-print-directory $(MONO)
	@touch $(STAMP)
	@echo "$(GREEN)Assets vendored$(NC)"

# URLs are repointed locally so no font is fetched at run time, and only the latin
# blocks are kept because the release bundle carries every other subset too.
font:
	@curl -sfL -H "User-Agent: $(UA)" \
	  "https://fonts.googleapis.com/css2?family=$(FAMILY):wght@$(WEIGHTS)&display=swap" \
	  -o "$(CSS_DIR)/$(SLUG).raw"
	@awk '/^\/\* /{keep = ($$0 ~ /^\/\* latin(-ext)? \*\/$$/)} keep' \
	  "$(CSS_DIR)/$(SLUG).raw" > "$(CSS_DIR)/$(SLUG).css"
	@rm -f "$(CSS_DIR)/$(SLUG).raw"
	@grep -o 'https://fonts.gstatic.com/[^)]*' "$(CSS_DIR)/$(SLUG).css" | sort -u \
	  | xargs -P 8 -I{} sh -c 'curl -sfL "$$1" -o "$(FONTS_DIR)/$$(basename "$$1")"' _ {}
	@sed -i.bak -E 's|https://fonts\.gstatic\.com/[^)]*/([^/)]+)|/fonts/\1|g' "$(CSS_DIR)/$(SLUG).css"
	@rm -f "$(CSS_DIR)/$(SLUG).css.bak"

# The Nerd Font variant carries the extra glyphs and is not on Google Fonts, so it
# comes from the nerd-fonts release as ttf and is compressed to woff2 here.
nerdfont:
	@set -e; tmp="$$(mktemp -d)"; trap 'rm -rf "$$tmp"' EXIT; \
	curl -sfL -o "$$tmp/JetBrainsMono.tar.xz" \
	  "https://github.com/ryanoasis/nerd-fonts/releases/download/v$(NERDFONT_VERSION)/JetBrainsMono.tar.xz"; \
	tar -xJf "$$tmp/JetBrainsMono.tar.xz" -C "$$tmp" \
	  JetBrainsMonoNerdFontMono-Regular.ttf JetBrainsMonoNerdFontMono-Bold.ttf; \
	for w in Regular Bold; do \
	  $(UVX) -q --from "fonttools[woff]" fonttools ttLib.woff2 compress \
	    -o "$(FONTS_DIR)/JetBrainsMonoNerdFontMono-$$w.woff2" \
	    "$$tmp/JetBrainsMonoNerdFontMono-$$w.ttf" >/dev/null 2>&1; \
	done
	@{ \
	  for pair in 400:Regular 700:Bold; do \
	    printf '@font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:%s;font-display:swap;src:url("/fonts/JetBrainsMonoNerdFontMono-%s.woff2") format("woff2");}\n' \
	      "$${pair%%:*}" "$${pair##*:}"; \
	  done; \
	} > "$(CSS_DIR)/jetbrains-mono.css"

# =============================================================================
# Verify the native addon
# =============================================================================
verify: ## Prove the compiled addon loads and runs
	@node --input-type=module -e "import pty from 'node-pty'; const t=pty.spawn('/usr/bin/env',['sh','-c','echo pty-ok'],{name:'xterm-256color',cols:120,rows:36,env:process.env}); let o=''; t.onData(d=>{o+=d;}); t.onExit(e=>{const ok=o.includes('pty-ok')&&e.exitCode===0; console.log(ok?'verify: node-pty OK':'verify: node-pty FAILED'); process.exit(ok?0:1);});"
	@echo "$(GREEN)Native addon verified$(NC)"

# =============================================================================
# Release artifacts
# =============================================================================
bundle: vendor ## Assemble the runtime-bundled tarball for this platform
	@bash scripts/bundle.sh "$$(node -p 'process.platform')" "$$(node -p 'process.arch')"
	@echo "$(GREEN)Bundle assembled in dist/$(NC)"

binary: vendor ## Compile a single self-contained binary (pure-JS apps only)
	@bun build ./bin/$(APP_NAME).js --compile --minify --outfile dist/$(APP_NAME)
	@echo "$(GREEN)Built: dist/$(APP_NAME)$(NC)"

clean: ## Remove node_modules, vendored assets, and build output
	@rm -rf node_modules $(VENDOR_DIR) $(CSS_DIR)/inter.css $(CSS_DIR)/google-sans.css $(CSS_DIR)/jetbrains-mono.css $(FONTS_DIR) $(STAMP) dist
	@echo "$(GREEN)Cleaned$(NC)"

# =============================================================================
# Version
# =============================================================================
version: ## Print the next version, derived from the last commit message
	@LATEST_TAG=$$(git tag --sort=-v:refname | head -n1 || echo "0.0.0"); \
	LATEST_TAG=$${LATEST_TAG#v}; \
	MAJOR=$$(echo "$$LATEST_TAG" | cut -d. -f1); \
	MINOR=$$(echo "$$LATEST_TAG" | cut -d. -f2); \
	PATCH=$$(echo "$$LATEST_TAG" | cut -d. -f3); \
	MAJOR=$${MAJOR:-0}; MINOR=$${MINOR:-0}; PATCH=$${PATCH:-0}; \
	COMMIT_MSG="$$(git log -1 --pretty=%B)"; \
	if echo "$$COMMIT_MSG" | grep -q "\[major-release\]"; then \
		MAJOR=$$((MAJOR + 1)); MINOR=0; PATCH=0; \
	elif echo "$$COMMIT_MSG" | grep -q "\[minor-release\]"; then \
		MINOR=$$((MINOR + 1)); PATCH=0; \
	else \
		PATCH=$$((PATCH + 1)); \
	fi; \
	echo "v$${MAJOR}.$${MINOR}.$${PATCH}"
```

## Notes

`node_modules` is a file target gated on `package-lock.json` and touched afterwards, so `make vendor` twice in a row reinstalls nothing. Without the `touch`, make compares against a directory timestamp that npm updates unpredictably.

`npm_config_build_from_source=true` forces `node-gyp` to compile rather than download a prebuilt binary. A prebuilt addon is compiled against a different Node ABI and a different libc than the release targets, which surfaces as a load failure at run time rather than at build time.

`verify` spawns the addon and asserts on its actual output rather than checking that a file exists. A `.node` file that is present but built for the wrong architecture passes a file check and fails on the first request.

`vendor` copies JS from `node_modules` rather than downloading it, because the version is already pinned in `package-lock.json` and a second source of truth would drift from it. Fonts are downloaded, since they are not npm packages.

Tailwind and Lucide are vendored the same way, from `@tailwindcss/browser` and `lucide` in `package.json`, so the Node frontend styles itself with the same utilities and icons as the Go one.

Every target is silent on success apart from the one line that says what it produced. A tool that narrates its own progress buries the one line a failed build needs, which is why `fonttools` has both its streams redirected and `uv` runs under `-q`.

The `version` target uses the same commit-marker convention and the same calculation as the Go Makefile. The release workflow calls `make -s version` rather than reimplementing it.

| Placeholder | Replace with |
|---|---|
| `[APP_NAME]` | the application name |
| `@xterm/xterm` copies | whatever JS the frontend vendors beyond Tailwind and Lucide |
| `node-pty` in `verify` | the project's real native addon, or delete the target |
| `NODE_VERSION` | the pinned version, matching `.node-version` |
