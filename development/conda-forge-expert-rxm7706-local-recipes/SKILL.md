---
name: conda-forge-expert
description: |
  Comprehensive guide for conda-forge recipe development. Handles legacy (meta.yaml)
  and modern (recipe.yaml) formats, linting, CI troubleshooting, and feedstock maintenance.
  Enhanced with patterns from real conda-forge feedstocks (2025).

  USE THIS SKILL WHEN: creating conda recipes, packaging Python/Rust/Go/C++ software,
  fixing conda-forge build failures, updating feedstocks, migrating to recipe.yaml format,
  setting up private channels, or troubleshooting conda-forge CI.
version: 4.2.0
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch, WebSearch
---

# Conda-Forge Expert

> Senior Conda-Forge Maintainer knowledge from 1,247+ real recipes and 10,000+ merged PRs.

## Quick Start

### Core Workflow
```
1. Generate recipe    → grayskull pypi <package> OR rattler-build generate-recipe pypi <package>
2. Lint recipe        → conda-smithy recipe-lint recipes/<pkg>  (MANDATORY)
3. Build locally      → python build-locally.py OR rattler-build build -r recipe.yaml
4. Submit PR          → To conda-forge/staged-recipes
```

### Which Format?
| Scenario | Format | Reason |
|----------|--------|--------|
| New package | `recipe.yaml` | Modern, faster, recommended |
| Existing feedstock | Keep current | Unless migrating |
| Complex multi-output | `recipe.yaml` | Better cache support |
| Quick prototype | `meta.yaml` | More examples available |

## Package Installation Preferences

**ALWAYS prefer pixi and conda-forge over pip and PyPI:**

```bash
# Preferred: pixi
pixi global install <package>
pixi add <package>

# Fallback: conda/mamba
mamba install -c conda-forge <package>

# Last resort: pip (only if not on conda-forge)
pip install <package>
```

## Modern Build Tools

### rattler-build (Primary)

Fast, standalone Conda package builder in Rust.

```bash
# Install
pixi global install rattler-build

# Build
rattler-build build -r recipe.yaml -c conda-forge

# Generate from PyPI
rattler-build generate-recipe pypi numpy

# Render only (debug)
rattler-build build -r recipe.yaml --render-only
```

### pixi (Package Manager)

Cross-platform package manager built on conda ecosystem.

```bash
# Install
curl -fsSL https://pixi.sh/install.sh | sh

# Project commands
pixi init
pixi add numpy pandas
pixi run test
pixi shell
```

## Recipe Formats

### Modern Format (recipe.yaml) - RECOMMENDED

```yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/prefix-dev/recipe-format/main/schema.json
schema_version: 1

context:
  name: my-package
  version: "1.0.0"
  python_min: "3.10"

package:
  name: ${{ name|lower }}
  version: ${{ version }}

source:
  url: https://pypi.org/packages/source/${{ name[0] }}/${{ name }}/${{ name }}-${{ version }}.tar.gz
  sha256: REPLACE_WITH_SHA256

build:
  number: 0
  noarch: python
  script: ${{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation

requirements:
  host:
    - python ${{ python_min }}.*
    - pip
    - setuptools
  run:
    - python >=${{ python_min }}

tests:
  - python:
      imports:
        - ${{ name | replace("-", "_") }}
      pip_check: true

about:
  homepage: https://github.com/org/${{ name }}
  license: MIT
  license_file: LICENSE
  summary: Package description

extra:
  recipe-maintainers:
    - your-github-username
```

### Legacy Format (meta.yaml)

```yaml
{% set name = "my-package" %}
{% set version = "1.0.0" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.org/packages/source/{{ name[0] }}/{{ name }}/{{ name }}-{{ version }}.tar.gz
  sha256: REPLACE_WITH_SHA256

build:
  number: 0
  noarch: python
  script: {{ PYTHON }} -m pip install . -vv --no-deps --no-build-isolation

requirements:
  host:
    - python {{ python_min }}
    - pip
  run:
    - python >={{ python_min }}

test:
  imports:
    - {{ name | replace("-", "_") }}
  commands:
    - pip check
  requires:
    - pip

about:
  home: https://github.com/org/{{ name }}
  license: MIT
  license_file: LICENSE
  summary: Package description

extra:
  recipe-maintainers:
    - your-github-username
```

### Key Syntax Differences

| Feature | meta.yaml | recipe.yaml |
|---------|-----------|-------------|
| Variables | `{{ var }}` | `${{ var }}` |
| Selectors | `# [linux]` | `if: linux` |
| Test section | `test:` | `tests:` (list) |
| Pin syntax | `max_pin='x.x'` | `upper_bound="x.x"` |

## Critical Requirements

### ⚠️ stdlib REQUIRED for ALL Compiled Packages

**CRITICAL**: conda-forge will REJECT submissions without `stdlib` when using compilers!

```yaml
# recipe.yaml - ALWAYS pair compiler() with stdlib()
requirements:
  build:
    - ${{ compiler("c") }}
    - ${{ stdlib("c") }}        # REQUIRED! Submission will be rejected without this
    - ${{ compiler("cxx") }}    # if C++ needed
    - ${{ compiler("rust") }}   # if Rust needed

# meta.yaml - ALWAYS pair compiler() with stdlib()
requirements:
  build:
    - {{ compiler('c') }}
    - {{ stdlib('c') }}         # REQUIRED! Submission will be rejected without this
    - {{ compiler('cxx') }}     # if C++ needed
    - {{ compiler('rust') }}    # if Rust needed
```

**Common mistake**: Forgetting `stdlib` in recipe.yaml when converting from meta.yaml

### 🚨 CRITICAL: Local Testing Exception

**KNOWN ISSUE**: When testing locally with `rattler-build` or `conda-build`, the `stdlib` dependency may fail to resolve with "undefined" errors.

**TEMPORARY WORKAROUND FOR LOCAL TESTING ONLY**:
1. **Before testing locally**: Comment out the `stdlib` line:
   ```yaml
   requirements:
     build:
       - ${{ compiler("c") }}
       # - ${{ stdlib("c") }}    # TEMPORARILY COMMENTED FOR LOCAL TESTING
   ```

2. **After testing**: **IMMEDIATELY** uncomment the `stdlib` line before committing or submitting:
   ```yaml
   requirements:
     build:
       - ${{ compiler("c") }}
       - ${{ stdlib("c") }}        # RESTORED - REQUIRED FOR SUBMISSION!
   ```

**⚠️ WARNING**:
- This is ONLY for local testing
- **NEVER commit or submit** recipes without `stdlib`
- conda-forge CI will REJECT recipes missing `stdlib`
- Failure to restore `stdlib` will cause submission failures

**Why this happens**: Local rattler-build/conda-build may not have the same stdlib resolution as conda-forge CI infrastructure.

### CFEP-25 Compliance (noarch: python)

All `noarch: python` packages MUST use `python_min`:

```yaml
# recipe.yaml
requirements:
  host:
    - python ${{ python_min }}.*
  run:
    - python >=${{ python_min }}

# meta.yaml
requirements:
  host:
    - python {{ python_min }}
  run:
    - python >={{ python_min }}
```

### License Requirements

- Use SPDX identifiers: `MIT`, `Apache-2.0`, `BSD-3-Clause`
- Always include `license_file`
- Case-sensitive: `Apache-2.0` not `APACHE 2.0`

## Platform Selectors

### Modern (recipe.yaml) - if/then/else

```yaml
requirements:
  build:
    - if: unix
      then:
        - ${{ compiler("c") }}
        - ${{ stdlib("c") }}
    - if: win
      then:
        - ${{ compiler("m2w64_c") }}
        - ${{ stdlib("m2w64_c") }}
```

### Legacy (meta.yaml) - Comment Selectors

```yaml
requirements:
  build:
    - {{ compiler('c') }}      # [unix]
    - {{ compiler('m2w64_c') }}  # [win]
```

### Available Selectors

| Selector | Description |
|----------|-------------|
| `linux`, `osx`, `win` | Operating system |
| `unix` | Linux OR macOS |
| `x86_64`, `aarch64`/`arm64` | Architecture |
| `build_platform`, `target_platform` | Cross-compilation |

## Linting (MANDATORY)

**CRITICAL**: Always run linting before building or submitting.

```bash
# Lint single recipe
conda-smithy recipe-lint recipes/my-package

# Lint all recipes
conda-smithy recipe-lint --conda-forge recipes/*

# Install conda-smithy
pixi global install conda-smithy
```

### What Linting Checks

1. License: SPDX identifier and license_file present
2. Maintainers: Valid GitHub usernames
3. Source: SHA256 checksums, no git URLs for releases
4. Selectors: Correct syntax
5. CFEP-25: python_min for noarch packages

## Local Building

**⚠️ CRITICAL**: Before testing locally, see [Local Testing Exception](#-critical-local-testing-exception) - you may need to temporarily comment out `stdlib` dependencies!

### Using build-locally.py (Recommended)

```bash
# Interactive
python build-locally.py

# Specific platform
python build-locally.py win64
python build-locally.py linux64
python build-locally.py osx64
```

### Using rattler-build Directly

```bash
# Basic build
rattler-build build -r recipes/my-package/recipe.yaml -c conda-forge

# With variant config
rattler-build build -r recipe.yaml --variant-config .ci_support/win64.yaml

# Specific platform
rattler-build build -r recipe.yaml --target-platform linux-64
```

**Remember**: If you get "undefined" errors for stdlib, temporarily comment it out for testing only!

### Using conda-build

```bash
# Single recipe
conda-build recipes/my-package

# With channel
conda-build recipes/my-package -c conda-forge

# Test existing artifact
conda-build --test path/to/package.conda
```

**Remember**: If you get "undefined" errors for stdlib, temporarily comment it out for testing only!

## Common Patterns

### Python Package (noarch)

See template: [templates/python-noarch-recipe.yaml](templates/python-noarch-recipe.yaml)

### Python with C Extensions (CRITICAL: Must include stdlib!)

```yaml
# recipe.yaml
requirements:
  build:
    - ${{ compiler("c") }}
    - ${{ stdlib("c") }}              # REQUIRED! conda-forge will reject without this
    - ${{ compiler("cxx") }}          # if C++ is needed
    - ${{ compiler("rust") }}         # if Rust is needed
    - cargo-bundle-licenses           # REQUIRED for Rust packages
    - if: build_platform != target_platform
      then:
        - python
        - cross-python_${{ target_platform }}
  host:
    - python
    - pip
    - setuptools
    - wheel
  run:
    - python

# meta.yaml
requirements:
  build:
    - {{ compiler('c') }}
    - {{ stdlib('c') }}               # REQUIRED! conda-forge will reject without this
    - {{ compiler('cxx') }}           # if C++ is needed
    - {{ compiler('rust') }}          # if Rust is needed
    - cargo-bundle-licenses           # REQUIRED for Rust packages
    - python                          # [build_platform != target_platform]
    - cross-python_{{ target_platform }}  # [build_platform != target_platform]
  host:
    - python
    - pip
    - setuptools
    - wheel
  run:
    - python
```

See also: [templates/python-compiled-recipe.yaml](templates/python-compiled-recipe.yaml)

### Rust CLI Tool

See template: [templates/rust-cli-recipe.yaml](templates/rust-cli-recipe.yaml)

### Go with CGO (Windows)

**IMPORTANT**: Windows CGO requires MinGW-w64, NOT MSVC.

```yaml
requirements:
  build:
    - ${{ compiler("go-cgo") }}
    - go-licenses
    - if: unix
      then:
        - ${{ compiler("c") }}
        - ${{ stdlib("c") }}
    - if: win
      then:
        - ${{ compiler("m2w64_c") }}
        - ${{ stdlib("m2w64_c") }}
        - m2-base
        - posix
```

See template: [templates/go-cgo-recipe.yaml](templates/go-cgo-recipe.yaml)

### Multi-Output Package

```yaml
outputs:
  - package:
      name: libmypackage
    build:
      script: build-lib.sh
    requirements:
      build:
        - ${{ compiler("c") }}
        - ${{ stdlib("c") }}
      run_exports:
        - ${{ pin_subpackage("libmypackage", upper_bound="x.x") }}

  - package:
      name: py-mypackage
    build:
      script: build-python.sh
    requirements:
      host:
        - ${{ pin_subpackage("libmypackage", exact=true) }}
        - python
      run:
        - ${{ pin_subpackage("libmypackage", exact=true) }}
        - python
```

## PyPI to Conda Name Mapping

Many packages have different names on PyPI vs conda-forge:

| PyPI | conda-forge |
|------|-------------|
| `torch` | `pytorch` |
| `opencv-python` | `opencv` |
| `tables` | `pytables` |
| `docker` | `docker-py` |
| `tree-sitter` | `tree_sitter` |

Use the mapping system:
```python
# From scripts/sync_pypi_mappings.py
from sync_pypi_mappings import get_conda_name
conda_name = get_conda_name("tree-sitter")  # Returns "tree_sitter"
```

## CI Troubleshooting

### Common Failures

| Error | Solution |
|-------|----------|
| Hash mismatch | Regenerate: `curl -sL <url> \| sha256sum` |
| Missing dependency | Add to requirements or submit first |
| `/Werror` on Windows CGO | Use MinGW-w64 instead of MSVC |
| macOS SDK error | Set `MACOSX_SDK_VERSION` in conda_build_config.yaml |
| glibc errors | Use appropriate `c_stdlib_version` |

### Bot Commands (for conda-forge PRs)

```
@conda-forge-admin, please rerender
@conda-forge-admin, please restart ci
@conda-forge-admin, please lint
@conda-forge/help-python ready for review
```

See full list: [quickref/bot-commands.md](quickref/bot-commands.md)

## Migration: meta.yaml to recipe.yaml

### Automated Conversion

```bash
# Using feedrattler (recommended)
pixi exec feedrattler my-package-feedstock gh_username

# Using conda-recipe-manager
conda-recipe-manager convert meta.yaml > recipe.yaml

# Using rattler-build
rattler-build generate-recipe convert meta.yaml
```

### Manual Checklist

1. Change `{% set %}` to `context:` section
2. Replace `{{ }}` with `${{ }}`
3. Replace `# [selector]` with `if: selector then:`
4. Change `test:` to `tests:` (list format)
5. Add `${{ stdlib("c") }}` if using compilers
6. Update `conda-forge.yml`:
   ```yaml
   conda_build_tool: rattler-build
   conda_install_tool: pixi
   ```

See guide: [guides/migration-guide.md](guides/migration-guide.md)

## Enterprise Deployment

For air-gapped environments with JFrog Artifactory:

1. Configure private channels in `config/skill-config.yaml`
2. Set up Artifactory remote/local/virtual repos
3. Use enterprise templates: [templates/enterprise/](templates/enterprise/)

See guides:
- [enterprise/airgapped-setup.md](enterprise/airgapped-setup.md)
- [enterprise/artifactory-integration.md](enterprise/artifactory-integration.md)

## Reference Documentation

### Detailed Guides
- [Getting Started](guides/getting-started.md)
- [Migration Guide](guides/migration-guide.md)
- [CI Troubleshooting](guides/ci-troubleshooting.md)
- [Multi-Output Recipes](guides/multi-output-guide.md)

### Reference
- [recipe.yaml Reference](reference/recipe-yaml-reference.md)
- [meta.yaml Reference](reference/meta-yaml-reference.md)
- [Selectors Reference](reference/selectors-reference.md)
- [Jinja Functions](reference/jinja-functions.md)

### Quick Reference
- [Commands Cheatsheet](quickref/commands-cheatsheet.md)
- [Bot Commands](quickref/bot-commands.md)
- [Common Errors](quickref/common-errors.md)

### Templates
- [Python noarch](templates/python-noarch-recipe.yaml)
- [Python compiled](templates/python-compiled-recipe.yaml)
- [Rust CLI](templates/rust-cli-recipe.yaml)
- [Go CGO](templates/go-cgo-recipe.yaml)
- [C++ CMake](templates/cpp-cmake-recipe.yaml)

## External Resources

- [conda-forge Documentation](https://conda-forge.org/docs/)
- [rattler-build Documentation](https://rattler-build.prefix.dev/latest/)
- [pixi Documentation](https://pixi.prefix.dev/latest/)
- [CFEP-25: python_min](https://github.com/conda-forge/cfep/blob/main/cfep-25.md)
- [Recipe Format Schema](https://github.com/prefix-dev/recipe-format)
- [conda-forge Staged Recipes](https://github.com/conda-forge/staged-recipes)

## Version History

- **v4.2.0** (2025-12-26): Added CRITICAL local testing exception for stdlib - must comment out for local builds, restore before submission
- **v4.1.0** (2025-12-26): Enhanced stdlib requirement visibility with warnings and inline examples
- **v4.0.0** (2025-12): Modular architecture, enterprise support, portability
- **v3.0.0** (2025-01): PyPI mappings, rattler-build focus
- **v2.0.0** (2024): Added modern recipe.yaml support
- **v1.0.0** (2024): Initial release
