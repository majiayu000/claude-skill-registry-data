---
name: go-makefile
description: The Makefile for a Go project - pinned asset downloads, build targets with ldflags version injection, docker targets, and the semver version calculation. Use when creating or changing a Makefile, adding an asset to download, wiring a build for another platform, or working out how the release version is computed. Triggers on Makefile, make assets, make build-all, GOOS, GOARCH, CGO_ENABLED, ldflags, AppVersion, and the version target.
user-invocable: false
---

# Go Makefile

**One Makefile that downloads pinned assets, builds every platform binary, and calculates the next version from the last commit.**

A Web Only or CLI + Web project uses the whole file. A CLI Only project deletes the two blocks marked below, since it has no frontend and no container. A Headless API Service keeps the docker block and deletes the assets block.

## Assets Are Never Committed

`make assets` downloads everything under `css/`, `js/`, `fonts/`, and `fontawesome/`, and the release workflow calls that same target rather than reimplementing the downloads. One definition means CI and a laptop produce the same tree.

Those directories are listed in `.gitignore`. A downloaded asset in a commit is a binary nobody reviews, a version nobody can trace, and a merge conflict nobody can resolve.

Every version is pinned to an exact release. A floating `@latest` makes two builds of one commit differ, and a new major arriving overnight breaks rendering with no diff to point at. Moving a pin is an edit to this file, which is the intended maintenance cost.

The whole target is guarded by a stamp file whose only prerequisite is the Makefile. `make build` on an unchanged checkout then downloads nothing, and moving any pin re-downloads everything, because every pin lives in the file the stamp depends on.

`.gitignore` needs its own entry for `internal/server/static/.assets-stamp`, which sits beside the asset directories rather than inside one. Its leading dot also keeps it out of `//go:embed static`, which skips names starting with `.` or `_`.

## Fonts

Three families are downloaded by default and all three come from Google Fonts as woff2. Nothing is converted, since the css2 endpoint already serves woff2 to a browser-shaped User-Agent.

| Family | Role |
|---|---|
| Inter | body and UI text |
| Google Sans | display headings and branding |
| JetBrains Mono | code and monospace |

Only the `latin` and `latin-ext` blocks of each stylesheet are kept. Google Fonts declares every subset it has, which for Google Sans is twenty-five files covering scripts the page never renders, and `go:embed` compiles all of them into the binary whether a browser asks for them or not. Filtering leaves six woff2 files across the three families.

The Nerd Font variant is off by default. It exists only for a page that renders Nerd Font glyphs, and it costs two megabytes and roughly ten seconds of woff2 compression against sixty kilobytes and half a second for the plain family. Set `NERDFONT := 1` in the Makefile when a page needs the glyphs; the target then fills the same `css/jetbrains-mono.css` under the same `JetBrains Mono` family name, so no page changes either way.

## Template

```makefile
.PHONY: help assets verify-assets font nerdfont fontawesome clean build build-for build-all docker-build docker-push version

# =============================================================================
# Variables
# =============================================================================
APP_NAME    := [APP_NAME]
DOCKER_USER := [GITHUB_USER]
MODULE      := github.com/[GITHUB_USER]/[APP_NAME]

VERSION ?= dev-build
GOOS    ?= $(shell go env GOOS)
GOARCH  ?= $(shell go env GOARCH)

# Pinned asset versions. Bump deliberately, never float.
TAILWIND_VERSION    := 4.3.3
LUCIDE_VERSION      := 1.34.0
FONTAWESOME_VERSION := 7.3.1
DEVICON_VERSION     := 2.17.0
MARKED_VERSION      := 18.0.11
HIGHLIGHTJS_VERSION := 11.12.0
MERMAID_VERSION     := 11.17.2
CHARTJS_VERSION     := 4.5.1
NERDFONT_VERSION    := 3.5.1

# Only a page that renders Nerd Font glyphs needs 1 here.
NERDFONT := 0

STATIC_DIR := internal/server/static
JS_DIR     := $(STATIC_DIR)/js
CSS_DIR    := $(STATIC_DIR)/css
FONTS_DIR  := $(STATIC_DIR)/fonts
FA_DIR     := $(STATIC_DIR)/fontawesome
STAMP      := $(STATIC_DIR)/.assets-stamp

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
# Assets  --  delete this whole block for CLI Only
# =============================================================================
assets: $(STAMP) ## Download pinned frontend assets (never committed)
	@:

# Every pin lives in this file, so bumping one invalidates the stamp and re-downloads.
$(STAMP): $(MAKEFILE_LIST)
	@mkdir -p $(JS_DIR) $(CSS_DIR) $(FONTS_DIR) $(FA_DIR)/css $(FA_DIR)/webfonts
	@curl -sfL "https://cdn.jsdelivr.net/npm/@tailwindcss/browser@$(TAILWIND_VERSION)" -o "$(JS_DIR)/tailwind.js"
	@curl -sfL "https://cdn.jsdelivr.net/npm/lucide@$(LUCIDE_VERSION)/dist/umd/lucide.min.js" -o "$(JS_DIR)/lucide.min.js"
	@curl -sfL "https://cdn.jsdelivr.net/npm/marked@$(MARKED_VERSION)/lib/marked.umd.js" -o "$(JS_DIR)/marked.umd.js"
	@curl -sfL "https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@$(HIGHLIGHTJS_VERSION)/highlight.min.js" -o "$(JS_DIR)/highlight.min.js"
	@curl -sfL "https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@$(HIGHLIGHTJS_VERSION)/styles/github-dark.min.css" -o "$(CSS_DIR)/github-dark.min.css"
	@curl -sfL "https://cdn.jsdelivr.net/npm/mermaid@$(MERMAID_VERSION)/dist/mermaid.min.js" -o "$(JS_DIR)/mermaid.min.js"
	@curl -sfL "https://cdn.jsdelivr.net/npm/chart.js@$(CHARTJS_VERSION)/dist/chart.umd.js" -o "$(JS_DIR)/chart.umd.js"
	@curl -sfL "https://cdn.jsdelivr.net/npm/devicon@$(DEVICON_VERSION)/devicon.min.css" -o "$(CSS_DIR)/devicon.min.css"
	@$(MAKE) --no-print-directory fontawesome
	@$(MAKE) --no-print-directory font FAMILY="Inter" SLUG=inter WEIGHTS="400;500;600;700"
	@$(MAKE) --no-print-directory font FAMILY="Google+Sans" SLUG=google-sans WEIGHTS="400;500;700"
	@$(MAKE) --no-print-directory $(MONO)
	@touch $(STAMP)
	@echo "$(GREEN)Assets downloaded$(NC)"

# URLs are repointed locally so no font is fetched at run time, and only the latin
# blocks are kept because `go:embed` compiles every other subset into the binary too.
font:
	@curl -sfL -H "User-Agent: $(UA)" \
	  "https://fonts.googleapis.com/css2?family=$(FAMILY):wght@$(WEIGHTS)&display=swap" \
	  -o "$(CSS_DIR)/$(SLUG).raw"
	@awk '/^\/\* /{keep = ($$0 ~ /^\/\* latin(-ext)? \*\/$$/)} keep' \
	  "$(CSS_DIR)/$(SLUG).raw" > "$(CSS_DIR)/$(SLUG).css"
	@rm -f "$(CSS_DIR)/$(SLUG).raw"
	@grep -o 'https://fonts.gstatic.com/[^)]*' "$(CSS_DIR)/$(SLUG).css" | sort -u \
	  | xargs -P 8 -I{} sh -c 'curl -sfL "$$1" -o "$(FONTS_DIR)/$$(basename "$$1")"' _ {}
	@sed -i.bak -E 's|https://fonts\.gstatic\.com/[^)]*/([^/)]+)|/static/fonts/\1|g' "$(CSS_DIR)/$(SLUG).css"
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
	    printf '@font-face{font-family:"JetBrains Mono";font-style:normal;font-weight:%s;font-display:swap;src:url("/static/fonts/JetBrainsMonoNerdFontMono-%s.woff2") format("woff2");}\n' \
	      "$${pair%%:*}" "$${pair##*:}"; \
	  done; \
	} > "$(CSS_DIR)/jetbrains-mono.css"

# Font Awesome's stylesheet points at ../webfonts, which does not resolve once the
# file is served from /static/fontawesome/css/.
fontawesome:
	@curl -sfL "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@$(FONTAWESOME_VERSION)/css/all.min.css" -o "$(FA_DIR)/css/all.min.css"
	@for f in fa-brands-400 fa-regular-400 fa-solid-900; do \
	  curl -sfL "https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@$(FONTAWESOME_VERSION)/webfonts/$$f.woff2" -o "$(FA_DIR)/webfonts/$$f.woff2"; \
	done
	@sed -i.bak 's|../webfonts/|/static/fontawesome/webfonts/|g' "$(FA_DIR)/css/all.min.css"
	@rm -f "$(FA_DIR)/css/all.min.css.bak"

verify-assets: ## Fail early if the embedded tree is missing an asset
	@test -s $(JS_DIR)/tailwind.js || (echo "tailwind.js missing, run 'make assets'" && exit 1)
	@test -s $(CSS_DIR)/inter.css || (echo "inter.css missing, run 'make assets'" && exit 1)
	@test -s $(CSS_DIR)/google-sans.css || (echo "google-sans.css missing, run 'make assets'" && exit 1)
	@test -s $(CSS_DIR)/jetbrains-mono.css || (echo "jetbrains-mono.css missing, run 'make assets'" && exit 1)

# =============================================================================
# Build
# =============================================================================
clean: ## Remove built binaries and downloaded assets
	@rm -f $(APP_NAME) $(APP_NAME)-* $(STAMP)
	@rm -rf $(JS_DIR) $(CSS_DIR) $(FONTS_DIR) $(FA_DIR)
	@echo "$(GREEN)Cleaned$(NC)"

build: assets verify-assets ## Build for the current platform
	@go build -ldflags="-s -w -X '$(MODULE)/cmd.AppVersion=$(VERSION)'" -o $(APP_NAME) .
	@echo "$(GREEN)Built: ./$(APP_NAME)$(NC)"

build-for: verify-assets ## Build for a specific GOOS/GOARCH
	@CGO_ENABLED=0 GOOS=$(GOOS) GOARCH=$(GOARCH) go build \
	  -ldflags="-s -w -X '$(MODULE)/cmd.AppVersion=$(VERSION)'" \
	  -o $(APP_NAME)-$(GOOS)-$(GOARCH) .
	@echo "$(GREEN)Built: ./$(APP_NAME)-$(GOOS)-$(GOARCH)$(NC)"

build-all: assets verify-assets ## Build every platform binary
	@$(MAKE) build-for GOOS=linux  GOARCH=amd64
	@$(MAKE) build-for GOOS=linux  GOARCH=arm64
	@$(MAKE) build-for GOOS=darwin GOARCH=amd64
	@$(MAKE) build-for GOOS=darwin GOARCH=arm64

# =============================================================================
# Docker  --  delete this whole block for CLI Only
# =============================================================================
docker-build: ## Build the container image for this machine
	@docker build --build-arg VERSION=$(VERSION) -t $(DOCKER_USER)/$(APP_NAME):$(VERSION) .
	@docker tag $(DOCKER_USER)/$(APP_NAME):$(VERSION) $(DOCKER_USER)/$(APP_NAME):latest

# buildx cannot load a multi-platform result into the local daemon, so the
# manifest is built and pushed in one step rather than built then pushed.
docker-push: ## Build linux/amd64 and linux/arm64 and push one manifest
	@docker buildx build --platform linux/amd64,linux/arm64 \
	  --build-arg VERSION=$(VERSION) \
	  -t $(DOCKER_USER)/$(APP_NAME):$(VERSION) \
	  -t $(DOCKER_USER)/$(APP_NAME):latest \
	  --push .

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

`make build` depends on `assets` so a fresh clone compiles. `//go:embed static` fails at compile time when the directory it names is empty, and an untracked asset tree means it always is on a first checkout.

`build-for` depends on `verify-assets` rather than `assets`, so a matrix of platform builds downloads once and then checks, instead of re-downloading per architecture.

Every target is silent on success apart from the one line that says what it produced. A tool that narrates its own progress buries the one line a failed build needs, which is why `fonttools` has both its streams redirected and `uv` runs under `-q`.

`docker-push` builds both architectures with buildx rather than tagging whatever the local daemon produced, so the pushed manifest serves an arm64 host an arm64 image.

`CGO_ENABLED=0` produces a static binary with no libc dependency, which is what lets one Linux build run on any distribution and lets the container's final stage be almost empty.

`-ldflags "-s -w"` strips the symbol table and DWARF data. The version is injected into the same flag, so `AppVersion` is a build input rather than a constant somebody has to remember to edit.

The `-X` path matches the package holding `AppVersion`. It is `$(MODULE)/cmd.AppVersion` when the variable lives in `cmd/root.go`, and `main.Version` when it lives in `main.go`.

`version` is the single definition of how a release number is derived, and the release workflow calls `make -s version` rather than repeating the logic. Two implementations of a version calculation drift, and the one in CI is the one nobody runs locally.

| Last commit contains | Bump | Example |
|---|---|---|
| nothing special | patch | `v1.0.0` to `v1.0.1` |
| `[minor-release]` | minor | `v1.0.1` to `v1.1.0` |
| `[major-release]` | major | `v1.1.0` to `v2.0.0` |

## Extension Variant

A Chrome extension replaces the build block with a zip target and reads its version from `manifest.json`, since the manifest is what the browser installs against.

```makefile
EXT_NAME := [EXTENSION_NAME]
VERSION  ?= $(shell grep '"version"' manifest.json | head -1 | sed 's/.*"version": "\(.*\)".*/\1/')
DIST_DIR := dist
SRC_FILES := manifest.json popup/ content/ background/ icons/ lib/

build: clean ## Build the distributable zip
	@mkdir -p $(DIST_DIR)
	@zip -r $(DIST_DIR)/$(EXT_NAME)-$(VERSION).zip \
	  $(shell for f in $(SRC_FILES); do [ -e "$$f" ] && echo "$$f"; done) \
	  -x "*.DS_Store" -x "*/.git/*"

dev: ## Print how to load the unpacked extension
	@echo "chrome://extensions -> Developer mode -> Load unpacked -> $(PWD)"
```

Only directories that exist are zipped, so an extension with no content script produces a valid archive rather than a shell error.
